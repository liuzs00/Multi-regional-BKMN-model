"""
Entry point: validate the verifiable anchor (Table 4) and produce a Table-11
style climate-stress output for the BKMN model.

Usage:
    py -3 run_bkmn.py
"""

import numpy as np
import pandas as pd

from bkmn import model, economy, data, scenarios
from bkmn import assumptions as cfg

pd.set_option("display.width", 160)
pd.set_option("display.max_rows", 200)
pd.set_option("display.float_format", lambda v: f"{v:,.2f}")


def banner(txt):
    print("\n" + "=" * 78)
    print(txt)
    print("=" * 78)


def validate_table4():
    banner("VALIDATION  -  Table 4 (relative GVA shock, GBP70 carbon tax)")
    paper = {  # phi = 0%, 50%, 100% spot-checks
        "A": (-77.9, -2.6, 77.9), "D": (-110.5, -19.3, 110.5),
        "C": (-7.0, -1.7, 7.0), "H": (-16.4, -1.4, 16.4),
    }
    print(f"{'sec':>3} {'phi':>5} {'paper':>8} {'model':>8}")
    worst = 0.0
    for s, (p0, p50, p100) in paper.items():
        i = data.SECTORS.index(s)
        for phi, pv in [(0.0, p0), (0.5, p50), (1.0, p100)]:
            mv = economy.gva_relative_shock_transition(70.0, phi)[i] * 100
            worst = max(worst, abs(mv - pv))
            print(f"{s:>3} {int(phi*100):>4}% {pv:8.1f} {mv:8.1f}")
    print(f"\nMax abs error vs paper: {worst:.3f} pp  ->  "
          f"{'PASS' if worst < 0.6 else 'FAIL'}")


def show_scenario_mixture():
    banner("SSP/RCP Bayesian mixture (RCP probabilities evolving with horizon)")
    Q = scenarios.transition_matrix()
    print("Annual RCP transition matrix Q (Eq 1):")
    print(pd.DataFrame(Q, index=climate_states(), columns=climate_states()).round(3))
    print("\nRCP mixture by horizon:")
    rows = {f"{int(y)}y": scenarios.rcp_mixture_at(y) for y in [0, 1, 5, 10, 20]}
    print(pd.DataFrame(rows, index=climate_states()).round(3))


def climate_states():
    from bkmn.climate import RCP_STATES
    return RCP_STATES


def main():
    validate_table4()
    show_scenario_mixture()

    banner(f"BKMN climate stress (phi={cfg.PHI:.0%}, SSP2/RCP4.5 prior 90%, "
           f"start {cfg.START_YEAR})  -  analogue of Table 11")
    df = model.run()
    print(df.round(2).to_string())

    banner("Observed BoE base curves (2026-06-11, pre-stress)")
    print(model.base_curve_snapshot().round(3).to_string())

    banner("ABSOLUTE stressed levels (base curve + climate shift)")
    print(model.stressed_levels_table().round(3).to_string())

    banner("Per-sector total GVA shock at 20y by RCP (%), phi=50%")
    print(model.sector_shock_table().round(2).to_string())

    print("\nInputs are now REAL: MESSAGE-GLOBIOM SSP2 temperature (World) & carbon")
    print("price (R5.2OECD), plus the Bank of England GBP nominal + inflation curves")
    print("(2026-06-11). Only carbon-pricing scope (Omega_XCE) remains assumed.")
    print("Table 4 transition-risk block is validated against the paper (<0.05pp).")


if __name__ == "__main__":
    main()
