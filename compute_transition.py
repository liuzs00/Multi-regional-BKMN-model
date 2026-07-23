"""
Transition-risk core of the multi-regional BKMN model.

Computes, from the current data (OECD ICIO 2025 @2022 + Scope-1 carbon intensity):
  * A   = Z x^{-1}                        technical coefficients (global MRIO)
  * L   = (I - A)^{-1}                    Leontief inverse (demand-side multiplier)
  * dp  = (I - A^T phi_hat)^{-1} phi_hat ct_direct     price change (Eq 8)
  * dV/V= [(I-A^T)L~(phi) - I + phi_hat] ct  -> per-sector GVA shock (Eq 10, Table 4)

Carbon price XCE = 70 (paper's Table 4 value; USD/tCO2e here as the data is USD).
Pass-through phi swept 0 -> 100% as in the paper's Table 4.
"""
import numpy as np
import pandas as pd

XCE = 70.0                                   # USD/tCO2e  (paper Table 4 uses GBP 70)
PHIS = np.round(np.arange(0, 1.0001, 0.10), 2)
REG_ORDER = ["EU27", "USA", "CHN", "GBR", "JPN", "IND", "CAN",
             "NOR", "IDN", "MEA", "AFR", "ROW"]

# --- load ICIO -------------------------------------------------------------
ic = pd.read_csv("DATA_12R/ICIO2025_12R_2022.csv", index_col=0)
ri = [r for r in ic.index if r not in ("TLS", "VA", "OUT")]     # 650 region_industry
Z   = ic.loc[ri, ri].to_numpy(float)                            # intermediate flows
x   = ic.loc["OUT", ri].to_numpy(float)                         # gross output
gva = ic.loc["VA",  ri].to_numpy(float)                         # value added
regions = np.array([lbl.split("_", 1)[0] for lbl in ri])
inds    = [lbl.split("_", 1)[1] for lbl in ri]

# --- A and Leontief inverse L ---------------------------------------------
x_safe = np.where(x == 0, 1.0, x)
A = Z / x_safe[None, :]                                          # A[i,j] = Z[i,j]/x[j]
n = A.shape[0]
Ide = np.eye(n)
L = np.linalg.inv(Ide - A)
AT = A.T

# --- carbon charge per unit output ct_direct = CI*XCE*1e-6 -----------------
ci = pd.read_csv("DATA_12R/CARBON_INTENSITY_12R_2022.csv", index_col=0)
ci_vec = np.array([ci.loc[j, r] for j, r in zip(inds, regions)], float)
ct = ci_vec * XCE * 1e-6

# --- phi sweep: dp (price change) and dV/V (GVA shock) ---------------------
dV_by_phi, dp_by_phi = {}, {}
for phi in PHIS:
    Ltil = np.linalg.inv(Ide - phi * AT) * phi                  # modified Leontief dual
    dp = Ltil @ ct                                              # Eq 8
    dv = ((Ide - AT) @ Ltil - Ide + phi * Ide) @ ct            # Eq 10
    dp_by_phi[phi] = dp
    dV_by_phi[phi] = x * dv

# --- aggregate to region level --------------------------------------------
def region_gva_shock(dV):                    # GDP-weighted: sum dV / sum GVA
    return {r: dV[regions == r].sum() / gva[regions == r].sum() for r in REG_ORDER}

def region_price(dp):                         # output-weighted mean price change
    return {r: np.average(dp[regions == r], weights=x[regions == r]) for r in REG_ORDER}

cols = [f"{int(p*100)}%" for p in PHIS]
gva_tbl   = pd.DataFrame({c: region_gva_shock(dV_by_phi[p]) for c, p in zip(cols, PHIS)}).reindex(REG_ORDER) * 100
price_tbl = pd.DataFrame({c: region_price(dp_by_phi[p])     for c, p in zip(cols, PHIS)}).reindex(REG_ORDER) * 100

# --- FULL per-sector GVA shock (Table 4 format) for all 650 region-sectors -
gva_nan = np.where(gva == 0, np.nan, gva)
midx = pd.MultiIndex.from_arrays([regions, inds], names=["region", "sector"])
sector_shock = pd.DataFrame(
    {c: dV_by_phi[p] / gva_nan * 100 for c, p in zip(cols, PHIS)}, index=midx)
price_shock = pd.DataFrame(               # per-sector price change dp (%), same shape
    {c: dp_by_phi[p] * 100 for c, p in zip(cols, PHIS)}, index=midx)

# --- report ----------------------------------------------------------------
pd.set_option("display.width", 200, "display.max_columns", 20, "display.float_format", lambda v: f"{v:7.2f}")
print(f"XCE = {XCE:.0f} USD/tCO2e   |   A,L shape = {A.shape}   |   spectral radius(A) = {max(abs(np.linalg.eigvals(A))):.4f}\n")

print("=== L (Leontief inverse) — sector total-output multipliers (col sums of L) ===")
mult = pd.Series(L.sum(axis=0), index=ri)
print("  global mean multiplier:", round(mult.mean(), 3),
      "| min:", round(mult.min(), 3), "| max:", round(mult.max(), 3))
print("  highest-multiplier sectors:")
for k, v in mult.sort_values(ascending=False).head(6).items():
    print(f"    {k:14s} {v:6.3f}")

print("\n=== Table 4 analogue: region GDP-weighted GVA shock (%), phi sweep ===")
print(gva_tbl.to_string())

print("\n=== dp: region output-weighted average price change (%), phi sweep ===")
print(price_tbl.to_string())

print("\n=== UK per-sector GVA shock (%) — direct Table 4 analogue (50 sectors x phi) ===")
print(sector_shock.loc["GBR"].to_string())

print("\n=== UK per-sector PRICE change dp (%) — same shape, monotonic in phi ===")
print(price_shock.loc["GBR"].to_string())

# --- sanity checks ---------------------------------------------------------
gbr = regions == "GBR"
ct_over_gva = -(x * ct)[gbr].sum() / gva[gbr].sum() * 100
print(f"\n[sanity] UK region shock at phi=0   = {gva_tbl.loc['GBR','0%']:.3f}%   (should equal -CT/GVA = {ct_over_gva:.3f}%)")
print(f"[sanity] UK region shock at phi=100 = {gva_tbl.loc['GBR','100%']:.3f}%   (should equal +CT/GVA = {-ct_over_gva:.3f}%)")

# --- save ------------------------------------------------------------------
gva_tbl.to_csv("out_gva_shock_by_region_phi.csv")
price_tbl.to_csv("out_price_change_by_region_phi.csv")
sector_shock.to_csv("out_gva_shock_by_sector_phi.csv")     # full 650 region-sectors x phi
price_shock.to_csv("out_price_change_by_sector_phi.csv")   # full 650 region-sectors x phi
print("\nsaved: out_gva_shock_by_region_phi.csv, out_price_change_by_region_phi.csv,"
      "\n       out_gva_shock_by_sector_phi.csv, out_price_change_by_sector_phi.csv")
