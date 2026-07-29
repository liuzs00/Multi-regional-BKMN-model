"""
Calibration constants from the single-region BKMN paper (Berrahoui, Kenyon,
Macrina, Nathanael 2025), for use as [PAPER]-tagged inputs / [PROXY] fallbacks
in the extension phases (docs/EXT_PLAN.md).

  * TABLE6_VL      sector physical-vulnerability pattern (paper Table 6,
                   20 UK SIC sections, health Q = 1 reference)
  * SIC_TO_ICIO    UK SIC section -> ICIO-2025 50-industry codes, to expand the
                   pattern onto the model's sector grid
  * EQUITY_BETA    FTSE100 log-GVA regression slope (paper Table 9)  [PROXY]
  * OPRISK_BETA    op-risk loss ~ unemployment slopes (paper Table 10) [PROXY]
"""

# --- Table 6: sector vulnerability to physical risk (health = 1) ------------
TABLE6_VL = {
    "A": 1.8, "B": 1.7, "C": 1.5, "D": 1.7, "E": 1.9, "F": 1.3, "G": 0.9,
    "H": 1.2, "I": 1.1, "J": 0.5, "K": 1.2, "L": 1.3, "M": 0.4, "N": 0.6,
    "O": 1.0, "P": 1.0, "Q": 1.2, "R": 0.7, "S": 0.8, "T": 0.9,
}

# --- UK SIC section -> ICIO 2025 industry codes ------------------------------
SIC_TO_ICIO = {
    "A": ["A01", "A02", "A03"],
    "B": ["B05", "B06", "B07", "B08", "B09"],
    "C": ["C10T12", "C13T15", "C16", "C17_18", "C19", "C20", "C21", "C22",
          "C23", "C24A", "C24B", "C25", "C26", "C27", "C28", "C29", "C301",
          "C302T309", "C31T33"],
    "D": ["D"], "E": ["E"], "F": ["F"], "G": ["G"],
    "H": ["H49", "H50", "H51", "H52", "H53"],
    "I": ["I"],
    "J": ["J58T60", "J61", "J62_63"],
    "K": ["K"], "L": ["L"], "M": ["M"], "N": ["N"], "O": ["O"], "P": ["P"],
    "Q": ["Q"], "R": ["R"], "S": ["S"], "T": ["T"],
}

# industry -> pattern value, expanded onto the 50 ICIO codes
PATTERN_ICIO = {ind: vl for sic, vl in TABLE6_VL.items()
                for ind in SIC_TO_ICIO[sic]}

# --- Table 9: equity index vs GVA log-regression slope ----------------------
EQUITY_BETA = 2.00           # FTSE 100 slope, R2 = 74% (paper Table 9) [PROXY]

# --- Table 10: op-risk loss-frequency vs unemployment log-slopes ------------
OPRISK_BETA = {
    "Conduct": 1.306037776,          # CPBP, R2 = 0.54  (paper Table 10)
    "Execution": 1.566813512,        # EDPM, R2 = 0.62  (paper Table 10)
}


def _check():
    from .regions import load
    m = load()
    missing = sorted(set(m.industry_of) - set(PATTERN_ICIO))
    assert not missing, f"ICIO industries without a VL pattern: {missing}"
    print(f"pattern covers all {len(set(m.industry_of))} ICIO industries; "
          f"range {min(PATTERN_ICIO.values())} - {max(PATTERN_ICIO.values())}")


if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    _check()
