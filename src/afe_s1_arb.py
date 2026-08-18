"""Finite Arb certificates for the AFE main sum of sym^2 Delta.

This module proves only the finite, explicitly truncated quantity

    S1[N,T] = sum_{n<=N} A(n)/n * W_T(n/12),
    W_T(y) = (1/(2*pi)) integral_{-T}^{T}
        Re[ G(1+(1+it))/G(1) y^{-(1+it)} exp((1+it)^2)/(1+it) ] dt.

Here ``W_T`` is a finite vertical-line integral, not the infinite AFE weight.
No tail of the n-sum and no truncation of the t-integral is estimated.  In
particular, S1[N,T] is not L(1,sym^2 Delta), is not the infinite S1, and is not
a positive lower bound for either quantity.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

from flint import acb, arb, ctx


CERTIFICATE_METHOD = "afe-s1-finite-v1"
DEFAULT_N = 100
DEFAULT_T = 8.0
DEFAULT_PRECISION = 96


def _compute_tau(N):
    """Load the exact tau sieve in both package and direct-script modes."""
    if __package__:
        from src.tau_sieve import compute_tau
    else:
        from tau_sieve import compute_tau
    return compute_tau(N)


def _with_precision(precision: int):
    if not isinstance(precision, int) or precision < 53:
        raise ValueError(f"precision must be an integer >= 53, got {precision!r}")
    return _PrecisionGuard(precision)


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


def _gamma_r(s: acb) -> acb:
    return arb.pi() ** (-s / 2) * (s / 2).gamma()


def _gamma_c(s: acb) -> acb:
    return 2 * (2 * arb.pi()) ** (-s) * s.gamma()


def _sym2_gamma(s: acb) -> acb:
    """Archimedean gamma factor used by ``src/afe_s1.py`` for weight 12."""
    return _gamma_r(s) * _gamma_c(s + 11)


def truncated_afe_weight(y, T: float = DEFAULT_T, precision: int = DEFAULT_PRECISION) -> acb:
    """Return an Arb enclosure of the finite weight ``W_T(y)``.

    ``y`` must be positive.  The output is an ``acb`` whose real part encloses
    the integral above; its imaginary part is expected to contain zero.  This
    routine does not add any bound for the omitted interval ``|t| > T``.
    """
    if T <= 0 or not math.isfinite(T):
        raise ValueError(f"T must be finite and positive, got {T!r}")
    y_acb = acb(y)
    if not y_acb.real > 0:
        raise ValueError(f"y must be positive, got {y!r}")

    with _with_precision(precision):
        one = acb(1)
        g_one = _sym2_gamma(one)
        t_lower = arb(-T)
        t_upper = arb(T)

        def integrand(t, _analytic):
            u = one + t * acb(0, 1)
            return (
                _sym2_gamma(one + u)
                / g_one
                * y_acb ** (-u)
                * (u * u).exp()
                / u
            )

        value = acb.integral(integrand, t_lower, t_upper) / (2 * arb.pi())

    return value


def arb_sym2_coeffs(N: int, precision: int = DEFAULT_PRECISION, tau_values=None) -> list[acb]:
    """Compute interval enclosures of normalized ``A(n)`` for ``n <= N``.

    The local parameters are normalized by ``p^{11/2}`.  For a prime ``p``,
    with ``c=tau(p)/p^{11/2}`` and ``q=c^2-1``, the GL(3) recurrence is
    ``A(p^k)=q A(p^{k-1})-q A(p^{k-2})+A(p^{k-3})``.
    """
    if not isinstance(N, int) or N < 1:
        raise ValueError(f"N must be a positive integer, got {N!r}")
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
            p_half_power = arb(p) ** (acb(11) / 2)
            c = acb(tau_values[p - 1]) / p_half_power
            q = c * c - 1
            local = [acb(1), q]
            local.append(q * local[1] - q * local[0])
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
            coprime_part = n // prime_power
            if coprime_part > 1:
                coeffs[n] = coeffs[prime_power] * coeffs[coprime_part]

    return coeffs[1:]


def _outward_float_interval(value: acb, ulps: int = 32) -> list[float]:
    """Convert an Arb real enclosure to outward-rounded JSON-compatible floats."""
    lower = float(value.real.lower())
    upper = float(value.real.upper())
    if not math.isfinite(lower) or not math.isfinite(upper):
        raise ValueError("cannot convert non-finite Arb interval")
    for _ in range(ulps):
        lower = math.nextafter(lower, -math.inf)
        upper = math.nextafter(upper, math.inf)
    return [lower, upper]


def _tau_hash(tau_values) -> str:
    payload = "\n".join(str(value) for value in tau_values).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def finite_s1_certificate(
    N: int = DEFAULT_N,
    T: float = DEFAULT_T,
    precision: int = DEFAULT_PRECISION,
) -> dict:
    """Generate a replayable certificate for the finite quantity S1[N,T]."""
    if not isinstance(N, int) or N < 1:
        raise ValueError(f"N must be a positive integer, got {N!r}")
    if N > 5000:
        raise ValueError("N is capped at 5000 in this finite certificate generator")
    if precision > 512:
        raise ValueError("precision is capped at 512 bits in this generator")

    tau_values = _compute_tau(N)
    coefficients = arb_sym2_coeffs(N, precision=precision, tau_values=tau_values)

    with _with_precision(precision):
        total = acb(0)
        weights = []
        for n, coefficient in enumerate(coefficients, start=1):
            weight = truncated_afe_weight(arb(n) / 12, T=T, precision=precision)
            weights.append(weight)
            total += coefficient / n * weight.real

        interval = _outward_float_interval(total)

    return {
        "method": CERTIFICATE_METHOD,
        "form": {"label": "delta", "weight": 12, "level": 1},
        "precision_bits": precision,
        "N": N,
        "T": T,
        "tau_sha256": _tau_hash(tau_values),
        "finite_interval": interval,
        "interval_semantics": "32 binary ulps outward beyond Arb endpoints",
        "certifies": "only the explicitly truncated S1[N,T]",
        "certifies_infinite_s1": False,
        "certifies_l1": False,
        "tail_bound": None,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--N", type=int, default=DEFAULT_N)
    parser.add_argument("--T", type=float, default=DEFAULT_T)
    parser.add_argument("--precision", type=int, default=DEFAULT_PRECISION)
    parser.add_argument("--output", type=Path, help="write JSON here (default: stdout)")
    args = parser.parse_args(argv)

    certificate = finite_s1_certificate(args.N, args.T, args.precision)
    text = json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        sys.stdout.write(text)
    else:
        args.output.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
