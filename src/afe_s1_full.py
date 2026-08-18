"""Arb certificate for the infinite AFE main sum of sym^2 Delta.

The finite certificate ``src/afe_s1_arb.py`` encloses only the explicitly
truncated ``S1[N,T]``.  This module closes the two remaining gaps of that
object with proof-level bounds and certifies the infinite main sum

    S1 = sum_{n>=1} A(n)/n * W(n/12),

where ``A(n)`` are the normalized symmetric-square-Delta coefficients and

    W(y) = (1/(2*pi)) int_{Re(u)=1} G(1+u)/G(1) y^{-u} exp(u^2)/u du,
    G(s) = Gamma_R(s) Gamma_C(s+11),
    Gamma_R(s) = pi^{-s/2} Gamma(s/2),
    Gamma_C(s) = 2 (2*pi)^{-s} Gamma(s).

The certificate decomposes the error ``S1 - S1[N,T]`` as

    E_t(N,T) = sum_{n<=N} A(n)/n * (W - W_T)(n/12)      (vertical tail),
    E_n(N,T) = sum_{n>N}  A(n)/n * W(n/12)              (coefficient tail).

Both are bounded with three elementary ingredients:

1. ``|A(n)| <= d_3(n)`` for every ``n`` (baseline entry DEL-D.1).
2. ``|Gamma(x+it)| <= Gamma(x)`` for ``x >= 1``, which follows from the
   Weierstrass product.  Consequently ``|G(2+m+it)| <= G(2+m)`` on the whole
   vertical line, so all modulus integrals reduce to Gaussian integrals.
3. Abel summation with ``sum_{n<=x} d_3(n) <= x (log x + 1)^2`` gives the
   explicit tail
   ``sum_{n>M} d_3(n)/n^beta <= beta M^{1-beta} [(log M+1)^2/(beta-1)
   + 2(log M+1)/(beta-1)^2 + 2/(beta-1)^3]``.

* ``E_t`` is bounded on the original line ``Re(u)=1`` by
  ``|E_t| <= 12 C_T sum_{n<=N} |A(n)|/n^2`` with
  ``C_T = (G(2)/G(1)) e e^{-T^2}/(2 pi T^2)``.
* ``E_n`` uses the contour shift ``Re(u): 1 -> 1+m`` (no poles in the strip,
  Gaussian decay), which yields the pointwise bound
  ``|W(y)| <= A_m y^{-(1+m)}`` with
  ``A_m = (G(2+m)/G(1)) e^{(1+m)^2}/(2 sqrt(pi) (1+m))``, hence
  ``|E_n| <= 12^{1+m} A_m sum_{n>N} d_3(n)/n^{2+m}``.

The certificate certifies only the infinite main sum ``S1``; it does not
certify the dual/contour term ``J`` or ``L(1,sym^2 Delta)``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

from flint import acb, arb, ctx


FULL_CERTIFICATE_METHOD = "afe-s1-full-v1"
DEFAULT_N = 20000
DEFAULT_T = 8.0
DEFAULT_ABS_T = 8.0
DEFAULT_M = 200000
DEFAULT_PRECISION = 128
CONTOUR_M = 2


def _compute_tau(N):
    if __package__:
        from src.tau_sieve import compute_tau
    else:
        from tau_sieve import compute_tau
    return compute_tau(N)


def _gamma_r(s: acb) -> acb:
    return arb.pi() ** (-s / 2) * (s / 2).gamma()


def _gamma_c(s: acb) -> acb:
    return 2 * (2 * arb.pi()) ** (-s) * s.gamma()


def _sym2_gamma(s: acb) -> acb:
    """Canonical weight-12 symmetric-square archimedean factor ``G(s)``."""
    return _gamma_r(s) * _gamma_c(s + 11)


class _PrecisionGuard:
    def __init__(self, precision: int):
        self.precision = precision
        self.old_precision = None

    def __enter__(self):
        self.old_precision = ctx.prec
        ctx.prec = self.precision

    def __exit__(self, exc_type, exc_value, traceback):
        ctx.prec = self.old_precision
        return False


def _with_precision(precision: int):
    if not isinstance(precision, int) or precision < 53:
        raise ValueError(f"precision must be an integer >= 53, got {precision!r}")
    return _PrecisionGuard(precision)


def arb_sym2_coeffs(N: int, precision: int, tau_values=None) -> list[acb]:
    """Compute interval enclosures of normalized ``A(n)`` for ``1 <= n <= N``."""
    if tau_values is None:
        tau_values = _compute_tau(N)
    if len(tau_values) != N:
        raise ValueError(f"expected {N} tau values, received {len(tau_values)}")

    with _with_precision(precision):
        coeffs = [acb(0)] * (N + 1)
        coeffs[1] = acb(1)
        smallest_prime = [0] * (N + 1)
        is_prime = [True] * (N + 1)
        is_prime[0] = is_prime[1] = False

        for p in range(2, N + 1):
            if not is_prime[p]:
                continue
            smallest_prime[p] = p
            c = acb(tau_values[p - 1]) / arb(p) ** (acb(11) / 2)
            q = c * c - 1
            local = [acb(1), q, q * q - q]
            max_power = 1
            power = p
            while power <= N:
                power *= p
                max_power += 1
            for _ in range(3, max_power + 1):
                local.append(q * local[-1] - q * local[-2] + local[-3])

            power = p
            exponent = 1
            while power <= N:
                coeffs[power] = local[exponent]
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
            coprime = n // prime_power
            if coprime > 1:
                coeffs[n] = coeffs[prime_power] * coeffs[coprime]

    return coeffs[1:]


def d3_values(M: int) -> list[int]:
    """Return ``d_3(n)`` for ``1 <= n <= M`` by a linear prime sieve."""
    if not isinstance(M, int) or M < 1:
        raise ValueError(f"M must be a positive integer, got {M!r}")

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


def _finite_s1_interval(N, T, precision, coefficients):
    """Enclose the finite simultaneous sum/integral ``S1[N,T]``."""
    with _with_precision(precision):
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
                _sym2_gamma(one + u)
                / g_one
                * (acb(12) ** u)
                * (u * u).exp()
                / u
                * polynomial
            )

        value = acb.integral(integrand, arb(-T), arb(T)) / (2 * arb.pi())
    return value


def _vertical_tail_bound(N, T, precision, coefficients):
    """Rigorous bound on ``E_t`` via ``|G(2+it)| <= G(2)`` and ``e^{-t^2}``."""
    with _with_precision(precision):
        g_two = _sym2_gamma(acb(2)).real
        g_one = _sym2_gamma(acb(1)).real
        absolute_coefficient_sum = arb(0)
        for n, coefficient in enumerate(coefficients, start=1):
            absolute_coefficient_sum += abs(coefficient) / arb(n * n)

        c_t = (
            g_two
            / g_one
            * arb(1).exp()
            * (-(arb(T) * T)).exp()
            / (2 * arb.pi() * T * T)
        )
        return arb(12) * absolute_coefficient_sum * c_t


def _absolute_contour_constant(m, precision):
    """Upper bound on ``A_m`` from ``|G(2+m+it)| <= G(2+m)``."""
    with _with_precision(precision):
        g_shift = _sym2_gamma(acb(2 + m)).real
        g_one = _sym2_gamma(acb(1)).real
        value = (
            g_shift
            / g_one
            * (arb((1 + m) * (1 + m))).exp()
            / (2 * arb.pi().sqrt() * arb(1 + m))
        )
    return value


def _d3_tail_bound(N, M, m, d3, precision):
    """Exact partial sum ``N < n <= M`` plus Abel bound for ``n > M``.

    With ``D(x) = sum_{n<=x} d_3(n) <= x (log x + 1)^2``, Abel summation gives
    ``sum_{n>M} d_3(n)/n^beta <= beta M^{1-beta} [(log M+1)^2/(beta-1)
    + 2(log M+1)/(beta-1)^2 + 2/(beta-1)^3]``.
    """
    beta = 2 + m
    with _with_precision(precision):
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


def _outward_float_interval(value: acb | arb, ulps: int = 32) -> list[float]:
    real = value.real if isinstance(value, acb) else value
    lower = float(real.lower())
    upper = float(real.upper())
    if not math.isfinite(lower) or not math.isfinite(upper):
        raise ValueError("cannot convert a non-finite Arb interval")
    for _ in range(ulps):
        lower = math.nextafter(lower, -math.inf)
        upper = math.nextafter(upper, math.inf)
    return [lower, upper]


def _tau_hash(tau_values) -> str:
    payload = "\n".join(str(value) for value in tau_values).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def full_s1_certificate(
    N: int = DEFAULT_N,
    T: float = DEFAULT_T,
    M: int = DEFAULT_M,
    precision: int = DEFAULT_PRECISION,
    abs_T: float = DEFAULT_ABS_T,
) -> dict:
    """Generate a replayable certificate for the infinite main sum ``S1``."""
    if not isinstance(N, int) or N < 100:
        raise ValueError("N must be an integer >= 100 for a convergent tail certificate")
    if not isinstance(M, int) or M <= N:
        raise ValueError("M must be an integer strictly greater than N")
    if not isinstance(T, (int, float)) or isinstance(T, bool) or not math.isfinite(T) or T <= 0:
        raise ValueError("T must be finite and positive")
    if not isinstance(abs_T, (int, float)) or isinstance(abs_T, bool) or not math.isfinite(abs_T) or abs_T <= 0:
        raise ValueError("abs_T must be finite and positive")
    T = float(T)
    abs_T = float(abs_T)
    if T < 4.0:
        raise ValueError("T < 4 makes the Gaussian tail bounds vacuous")
    if abs_T < 4.0:
        raise ValueError("abs_T < 4 leaves too little of the shifted-line integral")
    if N > 50000 or M > 1000000 or precision > 512:
        raise ValueError("certificate generator caps are N<=50000, M<=1000000, precision<=512")

    tau_values = _compute_tau(N)
    coefficients = arb_sym2_coeffs(N, precision, tau_values)
    d3 = d3_values(M)

    with _with_precision(precision):
        finite = _finite_s1_interval(N, T, precision, coefficients)
        contour_constant = _absolute_contour_constant(CONTOUR_M, precision)
        t_tail = _vertical_tail_bound(N, T, precision, coefficients)
        coefficient_tail = (
            contour_constant
            * arb(12) ** (CONTOUR_M + 1)
            * _d3_tail_bound(N, M, CONTOUR_M, d3, precision)
        )
        error = t_tail.upper() + coefficient_tail.upper()
        lo = finite.real.lower() - error
        hi = finite.real.upper() + error
        center = (lo + hi) / 2
        radius = (hi - lo) / 2
        total = arb(center, radius)

    return {
        "method": FULL_CERTIFICATE_METHOD,
        "form": {"label": "delta", "weight": 12, "level": 1},
        "precision_bits": precision,
        "N": N,
        "T": T,
        "M": M,
        "abs_T": abs_T,
        "contour_m": CONTOUR_M,
        "tau_sha256": _tau_hash(tau_values),
        "finite_interval": _outward_float_interval(finite),
        "finite_interval_semantics": "S1[N,T] by one simultaneous Arb vertical integral",
        "t_tail_bound": _outward_float_interval(t_tail),
        "n_tail_bound": _outward_float_interval(coefficient_tail),
        "contour_constant_interval": _outward_float_interval(contour_constant),
        "s1_interval": _outward_float_interval(total),
        "interval_semantics": "32 binary ulps outward beyond Arb endpoints",
        "baseline_inputs": ["DEL-D.1"],
        "certifies": "only the infinite AFE main sum S1; not J, not L(1)",
        "certifies_infinite_s1": True,
        "certifies_l1": False,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--N", type=int, default=DEFAULT_N)
    parser.add_argument("--T", type=float, default=DEFAULT_T)
    parser.add_argument("--M", type=int, default=DEFAULT_M)
    parser.add_argument("--precision", type=int, default=DEFAULT_PRECISION)
    parser.add_argument("--abs-T", type=float, default=DEFAULT_ABS_T, dest="abs_T")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    certificate = full_s1_certificate(args.N, args.T, args.M, args.precision, args.abs_T)
    text = json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        sys.stdout.write(text)
    else:
        args.output.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
