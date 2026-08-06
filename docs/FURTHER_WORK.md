# Further work: candidate extensions

Where the project stands against the brief, and what is worth building next.
Sources for candidates: the paper's own unimplemented features (catalogued in
[PAPER_AUDIT.md](PAPER_AUDIT.md) §F1) and opportunities that only exist *because*
the model is multi-regional.

---

## 1. The brief is essentially complete

| Brief requirement | Status |
|---|---|
| 5–12 regions, justified selection | **Done** — 20 regions (supervisor-approved), ROW sufficiency proven |
| International IO model per Miller & Blair | **Done** — [CHAPTER_MRIO.md](CHAPTER_MRIO.md) |
| **FX impacts** (primary deliverable) | **Done** — [FX_REPORT.md](FX_REPORT.md) |
| Tariffs (stretch) | **Done** — [TARIFF_METHOD.md](TARIFF_METHOD.md) |
| *"changes in trade flows between regions"* (stretch) | **Not done** — see §3.1 |

So the question is no longer what is required, but what adds most value. That
turns on a framing choice.

## 2. The framing: reproduction versus contribution

Two very different kinds of extension are available, and they are worth different
amounts.

**Reproducing more of the paper** — the CDS channel, IFRS 9, Green KVA/RWA. These
close gaps against the original, but a 20-region version of a channel the paper
already specifies is not a finding; it is more coverage. Several are also
data-blocked.

**Extensions native to the multi-regional setting** — things a single-region model
*cannot express at all*. These are where the dissertation's own contribution
lives, and where the findings so far have come from (the two FX channels, the
import-dependence cross-section, a tariff weakening the currency that levies it,
CBAM self-extinguishing under price convergence).

The recommendation below weights the second heavily.

---

## 3. Tier 1 — highest value

### 3.1 Trade diversion (Armington elasticities)

**Why it matters most.** It is the binding limitation on everything in the tariff
work, it is the brief's own unmet stretch goal (*"changes in trade flows between
regions"*), and it unlocks §3.2 below. With final demand and **A** fixed, nobody
re-sources away from a tariffed or carbon-priced origin, so every tariff result
we have measures cost-push incidence only and *understates* the effect.

**Method.** Apply sector-level Armington elasticities to reallocate **A**'s
off-diagonal blocks in response to the relative price change before inversion.
Elasticities are available from published tables (Caliendo & Parro 2015 give
sectoral trade elasticities); no licensed data needed.

**Cost.** Moderate. It is a new step in front of the existing pipeline rather than
a change to it, and it departs from the paper's inelastic-demand assumption — so
it belongs as a clearly labelled extension with the inelastic case retained as the
base.

### 3.2 Carbon leakage

**Why it matters.** This is *the* multi-regional climate question, the thing a
single-region model definitionally cannot ask, and the entire reason CBAM exists.
The exposure in our own data is large:

| | share of world Scope-1 emissions |
|---|--:|
| regions pricing ≥ \$50/t | **8.6 %** |
| regions pricing \$10–50/t | 31.8 % |
| regions pricing < \$10/t | **59.5 %** |
| effective coverage (emissions × scope) | **28.3 %** |

and 8.6 % of EU intermediate inputs already come from regions pricing below
\$10/t. **The model's leakage response to all of this is currently exactly zero**,
by construction.

**Method.** Once §3.1 exists this is almost free: price carbon asymmetrically, let
sourcing reallocate, and measure the emissions that move rather than fall. It
also gives CBAM a purpose to be evaluated against — right now we can say CBAM
raises \$10.1 bn and costs the EU 0.011 % of GVA, but not whether it prevents any
leakage, which is its entire justification.

**Cost.** Low *given* §3.1. This is the argument for doing them together.

### 3.3 Anchor on observed market curves

**Why it matters.** We report *shifts* (§F1 item 9). That is internally
consistent, but it means we cannot state a stressed **level** — and for an FX
dissertation that is a real gap, because an actual forward rate requires a
starting curve. "The 10-year EUR rate falls 150 bp" is weaker than "it goes from
X to Y", and the CIP forward we compute is a shift on an unnamed base.

**Method.** Add 2022 (and current) zero curves per region, plus market inflation
curves where available. Free sources: ECB Statistical Data Warehouse, Bank of
England, US Treasury, and national central banks. This also unlocks §2.6's
inflation term-structure overlay (F1 item 10), which follows directly.

**Cost.** Moderate, mostly data plumbing. Note FRED was unreachable from this
sandbox, so source selection needs checking first.

---

## 4. Tier 2 — cheap, and each fixes a stated weakness

| Extension | Fixes | Cost |
|---|---|---|
| **PFE(99.9 %)** (F1 item 8) | We report the 95 % quantile; the paper's Table 12 uses 99.9 %. The machinery already exists — it is a parameter change plus a gate. | Trivial |
| **External benchmarking** (F1 item 7) | Our magnitudes have **no external validation at all** — the paper benchmarks against ISDA, which is UK/single-region and does not transfer. Compare instead against published multi-region results: NGFS's own damage estimates, the ECB economy-wide climate stress test, the Bank of England CBES. | Low |
| **Sovereign spreads as a credit proxy** | The CDS channel (F1 items 1–3) is blocked on licensed data, but sovereign **bond yield spreads** are public and would give a region-level credit channel with the same GVA→spread structure. Not the paper's sector-level CDS, but it reopens a channel currently marked absent. | Low–moderate |

The benchmarking item is the one I would not skip. Every number in the report is
currently unvalidated against anything outside the model, and it is the first
thing an examiner will probe.

---

## 5. Tier 3 — larger, do only if time allows

- **RAS update of the IO table** (Miller & Blair ch. 7) to current bilateral trade
  shares. Addresses the 2022 base year, which matters most for tariffs — China is
  20 % of US goods imports in our table against under 10 % now. Improves the
  carbon results too. See [TARIFF_CALIBRATION.md](TARIFF_CALIBRATION.md) §5.1.
- **Full regime-switching Hull–White simulation** (§3.3, F1 item 11). We stress
  inputs by z·σ, which is exact under the chain's monotonicity, but simulation
  would add correlation structure and path-dependent measures.
- **Green KVA / RWA / GRoTE** (§4.2). The bank-facing outputs. Attractive for a
  Mathematical Finance dissertation, but a substantial build on top of a credit
  channel we do not yet have.
- **FX cross-rate network.** We quote everything against EUR; the full 20×20
  cross-rate matrix has structure (co-movement, clustering by carbon exposure)
  that is genuinely multi-regional and cheap to extract from existing output.

---

## 6. What I would not do

**Chase the CDS/IFRS 9 channel as specified.** It needs licensed CDS histories,
it is pure reproduction rather than contribution, and the sovereign-spread proxy
in Tier 2 gets most of the value for a fraction of the effort.

**Add more regions.** 20 is already above the brief, ROW sufficiency is proven,
and the marginal region adds data risk without adding a finding.

---

## 7. Recommendation

**Do §3.1 and §3.2 together** — Armington elasticities then carbon leakage. That
single pair removes the binding limitation on the tariff work, delivers the
brief's last unmet stretch goal, and produces the one result a single-region model
cannot: whether carbon pricing in one region moves emissions to another, and
whether CBAM stops it.

**Then the two cheap credibility items** — external benchmarking and
PFE(99.9 %) — because they cost little and close visible gaps.

**Treat §3.3 (market curves) as the swing item.** If the dissertation needs to
quote stressed FX *levels* rather than shifts, it becomes Tier 1; if shifts are
acceptable throughout, it can wait.

A defensible narrative for the whole project then reads: *reproduce the paper's
mechanism across 20 regions, show FX splits into two channels that measure
different things, and use the multi-regional structure to answer the question the
original could not — where does the carbon go when only some regions price it.*
