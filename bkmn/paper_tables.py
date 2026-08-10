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

# --- Tables 7-8: SIC section -> CDS-sector index weights ---------------------
# Fraction of each CDS sector index attributable to each UK SIC section.  These
# are PUBLISHED weights, so the credit channel needs no licensed data to run --
# only to RE-ESTIMATE the betas below, which we do not attempt (see CDS_BETA).
# Columns sum over sections to the index; rows do not sum to 1 (a section can
# feed several indices, and "FTSE" is the equity column, kept for cross-check).
CDS_WEIGHTS = {
    #        BasMat  ConsGd  ConsSv    Fin    Govt  Health   Indus   Oil&G    Tech  Telecom  RealEs   Utils    FTSE
    "A": (0.052, 0.028, 0.000, 0.0, 0.000, 0.000, 0.000, 0.000, 0.0, 0.0, 0.0, 0.000, 0.000),
    "B": (0.060, 0.000, 0.000, 0.0, 0.000, 0.000, 0.000, 0.058, 0.0, 0.0, 0.0, 0.000, 0.000),
    "C": (0.888, 0.482, 0.208, 0.0, 0.000, 0.553, 0.286, 0.862, 0.0, 0.0, 0.0, 0.000, 0.179),
    "D": (0.000, 0.000, 0.000, 0.0, 0.000, 0.000, 0.000, 0.080, 0.0, 0.0, 0.0, 0.421, 0.102),
    "E": (0.000, 0.000, 0.000, 0.0, 0.000, 0.000, 0.036, 0.000, 0.0, 0.0, 0.0, 0.579, 0.038),
    "F": (0.000, 0.000, 0.000, 0.0, 0.000, 0.000, 0.187, 0.000, 0.0, 0.0, 0.0, 0.000, 0.005),
    "G": (0.000, 0.490, 0.212, 0.0, 0.000, 0.000, 0.000, 0.000, 0.0, 0.0, 0.0, 0.000, 0.050),
    "H": (0.000, 0.000, 0.000, 0.0, 0.000, 0.000, 0.098, 0.000, 0.0, 0.0, 0.0, 0.000, 0.019),
    "I": (0.000, 0.000, 0.062, 0.0, 0.000, 0.000, 0.000, 0.000, 0.0, 0.0, 0.0, 0.000, 0.064),
    "J": (0.000, 0.000, 0.159, 0.0, 0.000, 0.000, 0.000, 0.000, 1.0, 1.0, 0.0, 0.000, 0.066),
    "K": (0.000, 0.000, 0.000, 1.0, 0.000, 0.000, 0.000, 0.000, 0.0, 0.0, 0.0, 0.000, 0.245),
    "L": (0.000, 0.000, 0.000, 0.0, 0.000, 0.000, 0.000, 0.000, 0.0, 0.0, 1.0, 0.000, 0.026),
    "M": (0.000, 0.000, 0.175, 0.0, 0.000, 0.000, 0.240, 0.000, 0.0, 0.0, 0.0, 0.000, 0.000),
    "N": (0.000, 0.000, 0.111, 0.0, 0.000, 0.000, 0.153, 0.000, 0.0, 0.0, 0.0, 0.000, 0.000),
    "O": (0.000, 0.000, 0.000, 0.0, 0.460, 0.000, 0.000, 0.000, 0.0, 0.0, 0.0, 0.000, 0.000),
    "P": (0.000, 0.000, 0.000, 0.0, 0.540, 0.000, 0.000, 0.000, 0.0, 0.0, 0.0, 0.000, 0.000),
    "Q": (0.000, 0.000, 0.000, 0.0, 0.000, 0.447, 0.000, 0.000, 0.0, 0.0, 0.0, 0.000, 0.206),
    "R": (0.000, 0.000, 0.032, 0.0, 0.000, 0.000, 0.000, 0.000, 0.0, 0.0, 0.0, 0.000, 0.000),
    "S": (0.000, 0.000, 0.038, 0.0, 0.000, 0.000, 0.000, 0.000, 0.0, 0.0, 0.0, 0.000, 0.000),
    "T": (0.000, 0.000, 0.003, 0.0, 0.000, 0.000, 0.000, 0.000, 0.0, 0.0, 0.0, 0.000, 0.000),
}
CDS_SECTORS = ("Basic Materials", "Consumer Goods", "Consumer Services",
               "Financials", "Government", "Health Care", "Industrials",
               "Oil & Gas", "Technology", "Telecommunications",
               "UK Real Estate", "Utilities", "FTSE")

# --- Table 9: CDS spread vs GVA log-regression slopes ------------------------
# UK/iTraxx-Europe estimates, used unchanged for every region [PROXY] -- the
# same treatment OPRISK_BETA already gets, and for the same reason: the
# coefficients are published, the histories needed to re-estimate them per
# region are licensed.  Sign convention: a NEGATIVE slope means the spread
# WIDENS as GVA falls, which is the economically expected direction.
# Financials and UK Real Estate carry positive slopes in the paper's own
# estimates; that is a property of the UK sample, not of our extension, and it
# is why those two move against the rest of the cross-section.
CDS_BETA = {
    "Health Care": -3.416546,
    "Telecommunications": -0.713071,
    "Consumer Goods": -2.328037,
    "Industrials": -1.750705,
    "Basic Materials": -1.971414,
    "Government": -3.111547,
    "Utilities": -1.509932,
    "Technology": -0.382102,
    "Financials": 2.077736,
    "Oil & Gas": -1.325491,
    "Consumer Services": -0.590066,
    "UK Real Estate": 7.206283,
    "FTSE": 2.00,                    # the equity column, = EQUITY_BETA
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
