"""Validate the transition-risk engine against Table 4 of the paper."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from bkmn import economy, data

# Table 4 from the paper: relative GVA shock (%) per sector, phi = 0..100%.
PHIS = [0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1.0]
PAPER = {
    "A": [-77.9, -63.2, -48.2, -33.2, -18.0, -2.6, 13.0, 28.8, 44.9, 61.2, 77.9],
    "B": [-17.2, -14.1, -11.0, -7.9, -4.7, -1.3, 2.1, 5.6, 9.2, 13.1, 17.2],
    "C": [-7.0, -6.1, -5.1, -4.1, -2.9, -1.7, -0.3, 1.2, 2.9, 4.8, 7.0],
    "D": [-110.5, -93.8, -76.5, -58.4, -39.4, -19.3, 2.2, 25.3, 50.7, 78.7, 110.5],
    "E": [-12.6, -10.3, -8.1, -5.7, -3.4, -0.9, 1.6, 4.2, 6.8, 9.6, 12.6],
    "H": [-16.4, -13.5, -10.6, -7.6, -4.5, -1.4, 1.9, 5.2, 8.8, 12.5, 16.4],
}

print(f"{'sec':>3} {'phi':>4} {'paper':>8} {'model':>8} {'diff':>7}")
maxdiff = 0.0
for s, paper_row in PAPER.items():
    i = data.SECTORS.index(s)
    for p, pv in zip(PHIS, paper_row):
        mv = economy.gva_relative_shock_transition(70.0, p)[i] * 100
        d = mv - pv
        maxdiff = max(maxdiff, abs(d))
        flag = "" if abs(d) < 0.6 else "  <-- check"
        print(f"{s:>3} {int(p*100):>3}% {pv:8.1f} {mv:8.1f} {d:7.2f}{flag}")

print(f"\nMax abs diff vs paper: {maxdiff:.3f} pp")
print("PASS" if maxdiff < 0.6 else "FAIL (>0.6pp)")
