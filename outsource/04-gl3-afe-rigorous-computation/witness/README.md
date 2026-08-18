# Witness — GL_3 AFE computation

The witness is the certified interval [L_lo, L_hi] at each grid point,
computed using python-flint (Arb) with outward rounding. These intervals
are stored in baseline/zero_free_scan.json (current: discovery tier with
mpmath floats; Arb version pending).
