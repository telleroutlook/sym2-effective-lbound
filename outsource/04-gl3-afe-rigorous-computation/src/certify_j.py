"""Certify J = S1 - L(1) from existing certificates.

J is the dual sum / contour integral in the AFE:
  L(1) = S1 - J
  J = S1 - L(1)

Since both S1 and L(1) are certified, J is certified by interval arithmetic.
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent.parent
WITNESS = Path(__file__).parent.parent / "witness"

# Load S1 certificate (from baseline/)
s1_cert = json.load(open(REPO / "baseline" / "s1_full_certificate.json"))
S1_lo = s1_cert["s1_interval"][0]
S1_hi = s1_cert["s1_interval"][1]

# Load L(1) certificate
l1_cert = json.load(open(WITNESS / "single_point_certificate.json"))
L1_lo = l1_cert["L_lo"]
L1_hi = l1_cert["L_hi"]

# J = S1 - L(1)
# Worst case: J_lo = S1_lo - L1_hi, J_hi = S1_hi - L1_lo
J_lo = S1_lo - L1_hi
J_hi = S1_hi - L1_lo
J_width = J_hi - J_lo

print("=== J Certification ===")
print(f"S1  in [{S1_lo:.6f}, {S1_hi:.6f}]  (width {S1_hi - S1_lo:.2e})")
print(f"L(1) in [{L1_lo:.10f}, {L1_hi:.10f}]  (width {L1_hi - L1_lo:.2e})")
print(f"J = S1 - L(1) in [{J_lo:.10f}, {J_hi:.10f}]  (width {J_width:.2e})")
print(f"J is negative: {J_hi < 0}")
print(f"|J| in [{-J_hi:.6f}, {-J_lo:.6f}]")
print()

# Save certificate
j_cert = {
    "J_interval": [J_lo, J_hi],
    "J_width": J_width,
    "J_is_negative": bool(J_hi < 0),
    "J_abs_interval": [-J_hi, -J_lo],
    "S1_interval": [S1_lo, S1_hi],
    "L1_interval": [L1_lo, L1_hi],
    "method": "J = S1 - L(1) from certified intervals",
    "status": "CERTIFIED",
}

out_path = WITNESS / "j_certificate.json"
with open(out_path, "w") as f:
    json.dump(j_cert, f, indent=2)
print(f"Certificate saved to {out_path}")
