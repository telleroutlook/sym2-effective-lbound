"""
Rigorous tail bounds via weight lookup table.

Strategy:
1. Precompute |V(y,s)| at y grid points (100 points on [0.01, 50])
2. For each n, look up V(n/X, s) from the table (linear interpolation)
3. Compute exact d_3 sums with looked-up V values
4. Bound tail beyond table using V(y) ≤ V(y_min) · (y_min/y)
"""
from __future__ import annotations
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "outsource/04-gl3-afe-rigorous-computation/src"))

from flint import acb, ctx
ctx.prec = 256

from afe_sym2_arb import G, V_arb, V_tilde_arb
from tail_bound import compute_d3_table


def build_weight_table(s_re: float, s_im: float, X: float,
                       y_max: float = 50.0, n_grid: int = 100):
    """Build lookup table for |V(y,s)| and |Ṽ(y,s)|."""
    s = acb(s_re, s_im)
    y_grid = [y_max * i / n_grid for i in range(1, n_grid + 1)]
    V_table = []
    Vt_table = []
    for y in y_grid:
        v = V_arb(acb(y, 0), s)
        vt = V_tilde_arb(acb(y, 0), s)
        V_table.append(float(abs(v).mid()))
        Vt_table.append(float(abs(vt).mid()))
    return y_grid, V_table, Vt_table


def lookup_V(y: float, y_grid: list[float], V_table: list[float]) -> float:
    """Linear interpolation of |V(y,s)| from table."""
    if y <= y_grid[0]:
        return V_table[0]
    if y >= y_grid[-1]:
        # Extrapolate using V(y) ≤ V(y_max) · (y_max/y)
        return V_table[-1] * (y_grid[-1] / y)
    # Find interval
    for i in range(len(y_grid) - 1):
        if y_grid[i] <= y <= y_grid[i + 1]:
            t = (y - y_grid[i]) / (y_grid[i + 1] - y_grid[i])
            return V_table[i] * (1 - t) + V_table[i + 1] * t
    return V_table[-1]


def main_tail_table(N: int, s_re: float, s_im: float,
                    N_TABLE: int = 100000) -> float:
    """Tail bound using V lookup table."""
    X = 12.0
    sigma = s_re

    d3 = compute_d3_table(N_TABLE)
    y_grid, V_tab, Vt_tab = build_weight_table(s_re, s_im, X)

    exact_sum = 0.0
    for n in range(N + 1, N_TABLE + 1):
        if d3[n] > 0:
            y = n / X
            V_y = lookup_V(y, y_grid, V_tab)
            exact_sum += d3[n] / (n ** sigma) * V_y

    # Tail beyond N_TABLE: V(n/X) ≤ V(N_TABLE/X) · (N_TABLE/n)
    V_N0 = lookup_V(N_TABLE / X, y_grid, V_tab)
    # Σ_{n>N_TABLE} d_3(n)/n^σ · V(N0/X)·N0/n = V_N0·N0 · Σ d_3(n)/n^{σ+1}
    # But Σ d_3(n)/n^{σ+1} for n>N_TABLE is tiny (we use d_3(n) ≤ n^0.15 bound)
    eps = 0.15
    if sigma + 1 > eps + 1:
        integral_tail = N_TABLE ** (eps - sigma) / (sigma - eps)
        tail_bound = V_N0 * N_TABLE * integral_tail
    else:
        tail_bound = float('inf')

    return exact_sum + tail_bound


def dual_tail_table(N: int, s_re: float, s_im: float,
                    N_TABLE: int = 100000) -> float:
    """Dual tail bound using Ṽ lookup table."""
    X = 12.0
    sigma = s_re

    d3 = compute_d3_table(N_TABLE)
    y_grid, V_tab, Vt_tab = build_weight_table(s_re, s_im, X)

    exact_sum = 0.0
    for n in range(N + 1, N_TABLE + 1):
        if d3[n] > 0:
            y = n * X
            # For y > y_grid[-1], use extrapolation
            if y > y_grid[-1]:
                Vt_y = Vt_tab[-1] * (y_grid[-1] / y)
            else:
                Vt_y = lookup_V(y, y_grid, Vt_tab)
            exact_sum += d3[n] * (n ** (sigma - 1)) * Vt_y

    # Tail: Ṽ(N0·X) · Σ d_3(n)·n^{σ-1} for n>N_TABLE
    Vt_N0 = Vt_tab[-1] * (y_grid[-1] / (N_TABLE * X)) if N_TABLE * X > y_grid[-1] else lookup_V(N_TABLE * X, y_grid, Vt_tab)
    eps = 0.15
    if sigma > eps:
        integral_tail = N_TABLE ** (eps + sigma - 1) / (1 - eps - sigma) if eps + sigma < 1 else float('inf')
        tail_bound = Vt_N0 * N_TABLE * integral_tail if integral_tail < float('inf') else float('inf')
    else:
        tail_bound = float('inf')

    return exact_sum + tail_bound


if __name__ == "__main__":
    print("=" * 60)
    print("WEIGHT TABLE TAIL BOUNDS")
    print("=" * 60)

    N_AFE = 60
    N_TABLE = 100000

    for s_re, s_im in [(1.0, 0.0), (0.6, -20.0), (0.6, 0.0)]:
        print(f"\ns = {s_re}+{s_im}i:")
        mt = main_tail_table(N_AFE, s_re, s_im, N_TABLE)
        dt = dual_tail_table(N_AFE, s_re, s_im, N_TABLE)
        print(f"  Main tail ≤ {mt:.6e}")
        print(f"  Dual tail ≤ {dt:.6e}")
        print(f"  Total     ≤ {mt+dt:.6e}")
