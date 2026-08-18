"""Independent verifier for the infinite AFE main-sum certificate of sym^2 Delta.

The checker deliberately duplicates the exact tau sieve, coefficient recurrence,
finite Arb vertical integral, d_3 sieve, and all tail-bound arithmetic instead
of importing ``src/``.  It verifies:

1. The finite S1[N,T] integral matches the replayed computation.
2. The vertical tail E_t is bounded by the claimed value.
3. The coefficient tail E_n is bounded by the claimed value.
4. The infinite-S1 interval is consistent with all of the above.

It never accepts a claim about L(1,sym^2 Delta) or the dual term J.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math

from flint import acb, arb, ctx


EXPECTED_METHOD = "afe-s1-full-v1"
MAX_N = 5000
MAX_M = 100000
MAX_PRECISION = 256


class _PrecisionGuard:
    def __init__(self, precision):
        self.precision = precision
        self.old_precision = None

    def __enter__(self):
        self.old_precision = ctx.prec
        ctx.prec = self.precision

    def __exit__(self, exc_type, exc_value, traceback):
        ctx.prec = self.old_precision
        return False


def _compute_tau(N):
    coefficients = [0] * (N + 1)
    coefficients[0] = 1
    for k in range(1, N + 1):
        for _ in range(24):
            for n in range(N, k - 1, -1):
                coefficients[n] -= coefficients[n - k]
    return [coefficients[n - 1] for n in range(1, N + 1)]


def _d3_values(M):
    spf = list(range(M + 1))
    values = [1] * (M + 1)
    values[0] = 0
    for i in range(2, int(M**0.5) + 1):
        if spf[i] == i:
            for multiple in range(i * i, M + 1, i):
                if spf[multiple] == multiple:
                    spf[multiple] = i
    for n in range(2, M + 1):
        p = spf[n]
        prime_power = p
        exponent = 1
        while n % (prime_power * p) == 0:
            prime_power *= p
            exponent += 1
        cofactor = n // prime_power
        values[n] = ((exponent + 1) * (exponent + 2) // 2) * values[cofactor]
    return values


def _gamma_r(s):
    return arb.pi() ** (-s / 2) * (s / 2).gamma()


def _gamma_c(s):
    return 2 * (2 * arb.pi()) ** (-s) * s.gamma()


def _sym2_gamma(s):
    return _gamma_r(s) * _gamma_c(s + 11)


def _coefficients(N, tau_values, precision):
    with _PrecisionGuard(precision):
        result = [acb(0)] * (N + 1)
        result[1] = acb(1)
        is_prime = [True] * (N + 1)
        is_prime[0] = is_prime[1] = False
        smallest_prime = [0] * (N + 1)

        for p in range(2, N + 1):
            if not is_prime[p]:
                continue
            smallest_prime[p] = p
            normalized = acb(tau_values[p - 1]) / (arb(p) ** (acb(11) / 2))
            q = normalized * normalized - 1
            local = [acb(1), q, q * q - q]
            power = p
            exponent = 1
            while power <= N:
                if exponent >= len(local):
                    local.append(q * local[-1] - q * local[-2] + local[-3])
                result[power] = local[exponent]
                power *= p
                exponent += 1
            multiple = p * p
            while multiple <= N:
                is_prime[multiple] = False
                if smallest_prime[multiple] == 0:
                    smallest_prime[multiple] = p
                multiple += p

        for n in range(4, N + 1):
            if is_prime[n]:
                continue
            p = smallest_prime[n]
            prime_power = p
            while n % (prime_power * p) == 0:
                prime_power *= p
            cofactor = n // prime_power
            if cofactor > 1:
                result[n] = result[prime_power] * result[cofactor]
    return result[1:]


def _tau_hash(tau_values):
    payload = "\n".join(str(value) for value in tau_values).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def _replay_finite_s1(N, T, precision, coefficients):
    """Independently compute S1[N,T] via the simultaneous integral."""
    with _PrecisionGuard(precision):
        g_one = _sym2_gamma(acb(1))
        one = acb(1)
        n_arbs = [arb(n) for n in range(1, N + 1)]

        def integrand(t, _analytic):
            u = one + t * acb(0, 1)
            polynomial = acb(0)
            for n, coefficient in enumerate(coefficients, start=1):
                polynomial += (
                    coefficient
                    / (n_arbs[n - 1] * n_arbs[n - 1])
                    * n_arbs[n - 1] ** (-t * acb(0, 1))
                )
            return (
                _sym2_gamma(one + u) / g_one
                * (acb(12) ** u)
                * (u * u).exp()
                / u
                * polynomial
            )

        value = acb.integral(integrand, arb(-T), arb(T)) / (2 * arb.pi())
    return value


def _replay_vertical_tail(N, T, precision, coefficients):
    """Independently compute the vertical tail bound E_t."""
    with _PrecisionGuard(precision):
        g_two = _sym2_gamma(acb(2)).real
        g_one = _sym2_gamma(acb(1)).real
        abs_coeff_sum = arb(0)
        for n, c in enumerate(coefficients, start=1):
            abs_coeff_sum += abs(c) / arb(n * n)
        c_t = g_two / g_one * arb(1).exp() * (-(arb(T) * T)).exp() / (
            2 * arb.pi() * T * T
        )
        return arb(12) * abs_coeff_sum * c_t


def _replay_contour_constant(m, precision):
    """Independently compute the contour constant A_m."""
    with _PrecisionGuard(precision):
        g_shift = _sym2_gamma(acb(2 + m)).real
        g_one = _sym2_gamma(acb(1)).real
        return g_shift / g_one * (arb((1 + m) * (1 + m))).exp() / (
            2 * arb.pi().sqrt() * arb(1 + m)
        )


def _replay_d3_tail(N, M, m, d3, precision):
    """Independently compute the d_3 tail bound."""
    beta = 2 + m
    with _PrecisionGuard(precision):
        partial = arb(0)
        for n in range(N + 1, M + 1):
            partial += arb(d3[n]) / arb(n) ** beta
        log_m_plus = arb(M).log() + 1
        remainder = (
            arb(beta)
            * arb(M) ** (1 - beta)
            * (
                log_m_plus * log_m_plus / (beta - 1)
                + 2 * log_m_plus / ((beta - 1) * (beta - 1))
                + 2 / ((beta - 1) * (beta - 1) * (beta - 1))
            )
        )
        return partial + remainder


def _outward_float_interval(value, ulps=32):
    real = value.real if isinstance(value, acb) else value
    lower = float(real.lower())
    upper = float(real.upper())
    if not math.isfinite(lower) or not math.isfinite(upper):
        raise ValueError("non-finite interval")
    for _ in range(ulps):
        lower = math.nextafter(lower, -math.inf)
        upper = math.nextafter(upper, math.inf)
    return [lower, upper]


def _check_interval_claim(claimed, replayed_lower, replayed_upper, tolerance_ulps=2):
    """Check that the replayed interval is contained in the claimed interval,
    allowing a small tolerance for floating-point differences."""
    if not (
        isinstance(claimed, list)
        and len(claimed) == 2
        and all(isinstance(x, (int, float)) and math.isfinite(x) for x in claimed)
    ):
        return False, "interval must be two finite floats"
    cl, cu = float(claimed[0]), float(claimed[1])
    if not cl < cu:
        return False, "interval must have increasing endpoints"
    lo = float(replayed_lower)
    hi = float(replayed_upper)
    for _ in range(tolerance_ulps):
        lo = math.nextafter(lo, -math.inf)
        hi = math.nextafter(hi, math.inf)
    if lo < cl or hi > cu:
        return False, (
            f"replayed [{lo}, {hi}] not contained in claimed [{cl}, {cu}]"
        )
    return True, "ok"


def check_full_s1_certificate(certificate):
    """Return ``(ok, message)`` after independently replaying the certificate."""
    if not isinstance(certificate, dict):
        return False, "certificate must be a JSON object"

    if certificate.get("method") != EXPECTED_METHOD:
        return False, f"unexpected method {certificate.get('method')!r}"

    form = certificate.get("form", {})
    if form.get("label") != "delta" or form.get("weight") != 12 or form.get("level") != 1:
        return False, "this verifier accepts only the level-one weight-12 Delta form"

    if certificate.get("certifies_infinite_s1") is not True:
        return False, "certifies_infinite_s1 must be True"
    if certificate.get("certifies_l1") is not False:
        return False, "certifies_l1 must be False"
    if certificate.get("interval_semantics") != "32 binary ulps outward beyond Arb endpoints":
        return False, "unsupported interval endpoint semantics"

    # --- parse parameters ---
    N = certificate.get("N")
    T = certificate.get("T")
    M = certificate.get("M")
    abs_T = certificate.get("abs_T")
    contour_m = certificate.get("contour_m")
    precision = certificate.get("precision_bits")

    if not isinstance(N, int) or N < 100:
        return False, "N must be an integer >= 100"
    if N > MAX_N:
        return False, f"N={N} exceeds checker cap {MAX_N}"
    if not isinstance(M, int) or M <= N:
        return False, "M must be an integer strictly greater than N"
    if M > MAX_M:
        return False, f"M={M} exceeds checker cap {MAX_M}"
    if not isinstance(T, (int, float)) or isinstance(T, bool):
        return False, "T must be numeric"
    T = float(T)
    if not math.isfinite(T) or T <= 0:
        return False, "T must be finite and positive"
    if not isinstance(abs_T, (int, float)) or isinstance(abs_T, bool):
        return False, "abs_T must be numeric"
    abs_T = float(abs_T)
    if not math.isfinite(abs_T) or abs_T <= 0:
        return False, "abs_T must be finite and positive"
    if not isinstance(contour_m, int) or contour_m < 0:
        return False, "contour_m must be a non-negative integer"
    if not isinstance(precision, int) or precision < 53:
        return False, "precision_bits must be an integer >= 53"
    if precision > MAX_PRECISION:
        return False, f"precision_bits={precision} exceeds checker cap {MAX_PRECISION}"

    # --- check intervals are valid ---
    for key in ("finite_interval", "t_tail_bound", "n_tail_bound", "contour_constant_interval", "s1_interval"):
        interval = certificate.get(key)
        if not (
            isinstance(interval, list)
            and len(interval) == 2
            and all(isinstance(x, (int, float)) and math.isfinite(x) for x in interval)
        ):
            return False, f"{key} must contain two finite numeric endpoints"

    s1_lo, s1_hi = float(certificate["s1_interval"][0]), float(certificate["s1_interval"][1])
    if not s1_lo < s1_hi:
        return False, "s1_interval must have increasing endpoints"

    # --- independently replay ---
    try:
        tau_values = _compute_tau(N)
        expected_hash = _tau_hash(tau_values)
        if certificate.get("tau_sha256") != expected_hash:
            return False, "tau checksum mismatch"

        coefficients = _coefficients(N, tau_values, precision)
        finite = _replay_finite_s1(N, T, precision, coefficients)
        t_tail = _replay_vertical_tail(N, T, precision, coefficients)

        d3 = _d3_values(M)
        contour_constant = _replay_contour_constant(contour_m, precision)
        d3_tail = _replay_d3_tail(N, M, contour_m, d3, precision)
        n_tail = contour_constant * arb(12) ** (contour_m + 1) * d3_tail

        error = t_tail.upper() + n_tail.upper()
        expected_lower = finite.real.lower() - error
        expected_upper = finite.real.upper() + error

    except (ValueError, ArithmeticError, RuntimeError) as exc:
        return False, f"independent replay failed: {exc}"

    # --- verify finite interval ---
    finite_claimed = certificate["finite_interval"]
    ok, msg = _check_interval_claim(finite_claimed, finite.real.lower(), finite.real.upper())
    if not ok:
        return False, f"finite_interval: {msg}"

    # --- verify t_tail_bound ---
    t_tail_claimed = certificate["t_tail_bound"]
    ok, msg = _check_interval_claim(t_tail_claimed, t_tail.lower(), t_tail.upper())
    if not ok:
        return False, f"t_tail_bound: {msg}"

    # --- verify n_tail_bound ---
    n_tail_claimed = certificate["n_tail_bound"]
    ok, msg = _check_interval_claim(n_tail_claimed, n_tail.lower(), n_tail.upper())
    if not ok:
        return False, f"n_tail_bound: {msg}"

    # --- verify contour_constant_interval ---
    cc_claimed = certificate["contour_constant_interval"]
    ok, msg = _check_interval_claim(cc_claimed, contour_constant.lower(), contour_constant.upper())
    if not ok:
        return False, f"contour_constant_interval: {msg}"

    # --- verify s1_interval is consistent with all bounds ---
    ok, msg = _check_interval_claim(
        certificate["s1_interval"], expected_lower, expected_upper
    )
    if not ok:
        return False, f"s1_interval: {msg}"

    width = s1_hi - s1_lo
    n_tail_val = float(certificate["n_tail_bound"][1])
    t_tail_val = float(certificate["t_tail_bound"][1])
    return True, (
        f"full S1 replay OK: N={N}, T={T}, M={M}, precision={precision}; "
        f"s1=[{s1_lo}, {s1_hi}] (width={width:.3e}); "
        f"E_t={t_tail_val:.2e}, E_n={n_tail_val:.2e}; "
        f"certifies infinite S1 only, not J or L(1)"
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", help="JSON certificate path")
    args = parser.parse_args(argv)
    with open(args.certificate, encoding="utf-8") as handle:
        certificate = json.load(handle)
    ok, message = check_full_s1_certificate(certificate)
    print(message)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
