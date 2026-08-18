"""Independent verifier for finite sym^2-Delta AFE partial-sum certificates.

The checker deliberately duplicates the exact tau sieve, coefficient recurrence,
and finite Arb vertical integral instead of importing ``src/``.  It verifies only
the explicitly truncated S1[N,T] object; it never accepts a claim about the
infinite main sum or L(1,sym^2 Delta).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math

from flint import acb, arb, ctx


EXPECTED_METHOD = "afe-s1-finite-v1"
MAX_N = 5000
MAX_PRECISION = 512


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
    """Independently compute tau(1),...,tau(N) from the eta-product identity."""
    coefficients = [0] * (N + 1)
    coefficients[0] = 1
    for k in range(1, N + 1):
        for _ in range(24):
            for n in range(N, k - 1, -1):
                coefficients[n] -= coefficients[n - k]
    return [coefficients[n - 1] for n in range(1, N + 1)]


def _gamma_r(s):
    return arb.pi() ** (-s / 2) * (s / 2).gamma()


def _gamma_c(s):
    return 2 * (2 * arb.pi()) ** (-s) * s.gamma()


def _sym2_gamma(s):
    return _gamma_r(s) * _gamma_c(s + 11)


def _truncated_weight(y, T, precision):
    if y <= 0:
        raise ValueError("y must be positive")
    with _PrecisionGuard(precision):
        one = acb(1)
        g_one = _sym2_gamma(one)

        def integrand(t, _analytic):
            u = one + t * acb(0, 1)
            return (
                _sym2_gamma(one + u)
                / g_one
                * acb(y) ** (-u)
                * (u * u).exp()
                / u
            )

        value = acb.integral(integrand, arb(-T), arb(T)) / (2 * arb.pi())
    return value


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
            normalized = acb(tau_values[p - 1]) / (
                arb(p) ** (acb(11) / 2)
            )
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


def check_finite_s1_certificate(certificate):
    """Return ``(ok, message)`` after independently replaying the certificate."""
    if not isinstance(certificate, dict):
        return False, "certificate must be a JSON object"

    if certificate.get("method") != EXPECTED_METHOD:
        return False, f"unexpected method {certificate.get('method')!r}"

    form = certificate.get("form", {})
    if form.get("label") != "delta" or form.get("weight") != 12 or form.get("level") != 1:
        return False, "this verifier accepts only the level-one weight-12 Delta form"

    if certificate.get("certifies_infinite_s1") is not False:
        return False, "certifies_infinite_s1 must be false"
    if certificate.get("certifies_l1") is not False:
        return False, "certifies_l1 must be false"
    if certificate.get("tail_bound") is not None:
        return False, "a finite S1 certificate must not attach an unverified tail bound"
    if certificate.get("interval_semantics") != "32 binary ulps outward beyond Arb endpoints":
        return False, "unsupported interval endpoint semantics"

    N = certificate.get("N")
    T = certificate.get("T")
    precision = certificate.get("precision_bits")
    if not isinstance(N, int) or N <= 0:
        return False, "N must be a positive integer"
    if N > MAX_N:
        return False, f"N={N} exceeds checker cap {MAX_N}; obtain a dedicated verifier"
    if not isinstance(T, (int, float)) or isinstance(T, bool):
        return False, "T must be numeric"
    T = float(T)
    if not math.isfinite(T) or T <= 0:
        return False, "T must be finite and positive"
    if not isinstance(precision, int) or precision < 53:
        return False, "precision_bits must be an integer >= 53"
    if precision > MAX_PRECISION:
        return False, f"precision_bits={precision} exceeds checker cap {MAX_PRECISION}"

    interval = certificate.get("finite_interval")
    if (
        not isinstance(interval, list)
        or len(interval) != 2
        or not all(isinstance(x, (int, float)) and math.isfinite(x) for x in interval)
    ):
        return False, "finite_interval must contain two finite numeric endpoints"
    lower, upper = float(interval[0]), float(interval[1])
    if not lower < upper:
        return False, "finite_interval must have increasing endpoints"

    try:
        tau_values = _compute_tau(N)
        coefficients = _coefficients(N, tau_values, precision)
        with _PrecisionGuard(precision):
            total = acb(0)
            for n, coefficient in enumerate(coefficients, start=1):
                weight = _truncated_weight(n / 12, T, precision)
                total += coefficient / n * weight.real
            replay_lower = total.real.lower()
            replay_upper = total.real.upper()
    except (ValueError, ArithmeticError, RuntimeError) as error:
        return False, f"independent replay failed: {error}"

    expected_hash = _tau_hash(tau_values)
    if certificate.get("tau_sha256") != expected_hash:
        return False, "tau checksum mismatch"

    if replay_lower < lower or replay_upper > upper:
        return False, (
            "replayed interval is not contained in claimed interval: "
            f"replay=[{replay_lower}, {replay_upper}], "
            f"claimed=[{lower}, {upper}]"
        )

    width = upper - lower
    return True, (
        "finite S1[N,T] replay OK: "
        f"N={N}, T={T}, precision={precision}; "
        f"replay=[{replay_lower}, {replay_upper}] subset claimed=[{lower}, {upper}] "
        f"(width={width:.3e}); no tail or L(1) claim"
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", help="JSON certificate path")
    args = parser.parse_args(argv)
    with open(args.certificate, encoding="utf-8") as handle:
        certificate = json.load(handle)
    ok, message = check_finite_s1_certificate(certificate)
    print(message)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
