"""
Every model input that the BKMN paper does NOT give a concrete value for is
collected here, with a note on the source/choice.  These are the knobs you would
replace with real market / IPCC data for a production reproduction.

Tagging:
  [PAPER]      value stated in the paper text/Table 17
  [SIMULATED]  no value in paper -> chosen here to make the model runnable
  [MARKET]     would normally come from observed market data; stubbed here
"""

# --- carbon tax level used for the Table 4 reproduction --------------------
XCE_TABLE4 = 70.0          # [PAPER] "carbon tax of GBP 70" (Table 4 caption)

# --- pass-through ----------------------------------------------------------
PHI = 0.50                 # [PAPER] examples use phi = 50% (Tables 11-13)

# --- damage function -------------------------------------------------------
# Omega(dT) = DAMAGE_COEF * dT^2 ; coefficient = 1.6768 / (2.2*2.2)
DAMAGE_COEF_BN = 1.6768 / (2.2 * 2.2)   # [PAPER] Barrage-Nordhaus 2024 (Eq 11) ~ 0.34645
DAMAGE_COEF_SR = 8.5 / (2.2 * 2.2)      # [PAPER] SwissRe 2024 (Eq 12), for comparison

# --- inflation -------------------------------------------------------------
INFLATION_PER_10USD = 0.08 / 100.0      # [PAPER] +0.08pp headline per +$10/t (Moessner)
CARBON_SCOPE = 1.0                      # [SIMULATED] fraction of emissions priced; paper
                                        #   leaves scope time-series unspecified -> assume full

# --- Taylor rule -----------------------------------------------------------
PHI_PI = 0.5               # [PAPER] reaction to inflation gap
PHI_Y = 0.5                # [PAPER] reaction to output gap

# --- Hull-White 1F ---------------------------------------------------------
HW_A = 0.04                # [PAPER] Table 17 "mean reversion equals 0.04"
HW_SIGMA = 0.01            # [MARKET] not given; rate-shift (Prop 2) is sigma-independent

# --- operational risk (macro) ---------------------------------------------
OKUN_KAPPA = -0.182        # [PAPER] UK Okun coefficient (Goto & Burgi 2020)
PHILLIPS_BETA = 0.0        # [PAPER] "no strong evidence Phillips applies to UK -> beta=0"

# --- scenario probability structure ---------------------------------------
# Starting SSP / RCP mixtures (Eq 18-19): 90% on SSP2 / RCP4.5.
SSP_PRIOR = {"SSP1": 0.025, "SSP2": 0.90, "SSP3": 0.025, "SSP4": 0.025, "SSP5": 0.025}  # [PAPER]
RCP_PRIOR = {"RCP1.9": 0.025, "RCP2.6": 0.025, "RCP3.4": 0.025, "RCP4.5": 0.90, "RCP6.0": 0.025}  # [PAPER]
TRANSITION_LAMBDA = 1.0    # [SIMULATED] exponential transition param (Eq 1); paper: user-set

# --- horizon / time grid ---------------------------------------------------
# Aligned to the observed BoE curve snapshot date (2026-06-11) so the market
# base date and the climate start date coincide.  (The paper uses 2024 only in
# the Eq.14 damage worked example; structural data is 2021, IPCC anchor 2023.)
START_YEAR = 2026          # [DATA] = observed yield-curve date
HORIZON_YEARS = 20         # [PAPER] examples go out to 20 years
# Reporting tenors matching Table 11 columns (in years):
REPORT_TENORS = {"1 day": 1/365, "10 days": 10/365, "3 months": 0.25,
                 "1 year": 1.0, "5 years": 5.0, "10 years": 10.0, "20 years": 20.0}

# --- climate input data (MESSAGE-GLOBIOM, SSP2 marker) ---------------------
# [DATA] Carbon prices: region R5.2OECD, variable Price|Carbon, US$2005/tCO2.
#        Temperature: region World, MAGICC6 Global Mean, deg C vs pre-industrial.
# Convert carbon price US$2005 -> GBP (2021, to match the IO/GVA vintage):
#   US CPI 2005->2021 ~= 1.39 ; FX 2021 USD->GBP ~= 0.726 ; product ~= 1.01.
USD2005_TO_GBP = 1.0       # [DATA] documented above; set precisely if needed

# --- market base curve -----------------------------------------------------
# [DATA] Observed GBP nominal + implied-inflation spot curves now come from the
# Bank of England GLC snapshot (2026-06-11), loaded via bkmn/curves.py.  Used to
# report absolute stressed levels (base + climate shift).  The flat fallback
# below is retained only for environments without the curve CSVs.
BASE_FLAT_RATE = 0.04
