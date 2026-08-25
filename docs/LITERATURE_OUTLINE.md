# Literature review — outline for editing

Planning document, not prose. For each work: the **one point** taken from it, the
**milestone** it moves the argument to, and **where it bites** in the
dissertation. Edit here; full text follows on approval.

---

## The graph

Nine chains. Arrows are "this work creates the problem the next one answers".

```
A  Carney ──> ECB ──> Acharya et al.
   (why stress test)      (why the current ones fail: not auditable)
                                     │
                                     ├──────────────┐
                                     ▼              ▼
B  Battiston ──> Bolton&Kacperczyk   │        I  Kenyon et al. ──> BKMN
   (network is necessary)            │           (auditable chain answers Acharya)
        └──> Desnos                  │                     │
             (scenario is random)    │                     │
                                     ▼                     │
C  Nordhaus ──> Pindyck / Weitzman / Dietz&Stern ──> SwissRe│
   (damage fn)   (it has no empirical basis)   (5x range)   │
        └──> ND-GAIN (ranks, does not measure)              │
        └──> NGFS (3 IAMs + NiGEM; NO price->sector map) ───┤
                                     │                      │
                                     ▼                      │
D  Hafner ──> Böhringer (CGE) / Mercure (macroecon)         │
   (4 families)  Dafermos (SFC) / Lamperti (ABM)            │
                 (what each omission costs)                 │
                                     │                      │
                                     ▼                      │
E  Leontief'36 ──> Hawkins&Simon ──> Leontief'70 ──> Miller&Blair
   (the system)     (when it exists)  (emissions in)  (dual, blocks, aggregation)
                                     │                      │
                                     ▼                      │
F  Isard ──> Chenery/Moses ──> Leontief&Strout ──> Stone     │
   (exact, unusable) (weaken)   (estimate flows)  (fit them) │
        └──> Tukker&Dietzenbacher ──> Timmer / Moran&Wood ──> OECD
             (measure them instead)   (databases agree ~10%)  │
        └──> Davis&Caldeira (trade weight != embodied emissions)
                                     │                      │
                                     ▼                      │
G  Weitzman'74 ──> Green ──> Kay&Jolley ──> Roncalli&Semet  │
   (instrument)    (modest)  (IO+NGFS, 1 country) (incidence open)
        └──> RBB / Weber&Wasner (pass-through varies, can exceed 1)
        └──> Böhringer again (leakage 5-20%, BCA is a carbon tariff)
                                     │                      │
                                     ▼                      ▼
H  Moessner vs Konradt&Weder / Bauer&Känzig ──> Taylor ──> Hull&White ──> Sarno&Taylor
   (inflation: DISPUTED)                        (rule)     (curve)      (parities)
                                                                        │
                                                                        ▼
                                                            THE GAP: nothing joins
                                                            BKMN's chain to the MRIO
                                                            apparatus
```

---

## A. Why stress test at all, and why the existing ones fall short

**Milestone reached:** climate is a prudential problem; the exercises that answer
it are credible but unauditable.

| Work | Point taken | Where it bites |
|---|---|---|
| Carney (2015) | *Tragedy of the horizon* — costs fall beyond every relevant planning horizon; remedy is forward-looking scenario analysis | §1 opening motivation |
| ECB (2022) | The largest implementation; establishes the standard shape: external scenario → exposure map → propagate → revalue. Also the object Acharya et al. criticise, so it must be cited for that critique to be checkable | §1; the shape our chain also follows |
| Acharya et al. (2023) | Four criticisms. Transition risk treated as exogenous when it is a policy choice; no climate–economy feedback; no compound scenarios; **and not reproducible by the tested institution** | §1 (why auditability matters), §5 conclusion |

**Edit note:** the fourth criticism is the one that justifies the whole BKMN
design. Consider whether to lead with it rather than list all four.

---

## B. Which network does a shock travel through?

**Milestone reached:** indirect exposure must be computed through an explicit
network — but *which* network is open.

| Work | Point taken | Where it bites |
|---|---|---|
| Battiston et al. (2017) | Indirect exposure via counterparties ≈ direct exposure; affected loan share ≈ bank capital. Networks must be computed, not inferred | §1, §2 — our argument for an IO network is theirs with a different network |
| Bolton & Kacperczyk (2023) | Carbon premium exists across 14,000 firms / 77 countries; larger where policy stricter → transition risk **already partly priced** | §3.5 equity beta caveat; §5 limitation |
| Desnos et al. (2023) | Turns a deterministic stress test into stochastic climate VaR: a scenario is a *draw*, not a state | §3.1 — the direct antecedent for the Dirichlet mixture |

**Edit note:** Desnos is from Roncalli's group — worth saying, since it links
strand B to strand G.

---

## C. Where scenarios come from, and the damage-function fight

**Milestone reached:** the damage function is the least-evidenced object in the
chain, and NGFS hands users a scenario with no sectoral cost map.

| Work | Point taken | Where it bites |
|---|---|---|
| Nordhaus (2017) | DICE: Ramsey growth + carbon cycle + quadratic damage | §3.4 the Ω form |
| Barrage & Nordhaus (2024) | DICE-2023 recalibration — the coefficient actually used | §3.4, §4.1 |
| Pindyck (2013) | No theoretical or empirical basis for curvature at high T; outputs are illustrations | §5 limitation; justifies carrying two calibrations |
| Weitzman (2012) | Quadratic implies implausibly small losses under large warming; needs a high-exponent term | §5 — our quadratic inherits this |
| Dietz & Stern (2015) | Damage on capital/growth rather than level → SCC far higher | §5 — our damage is a *level* effect only |
| Swiss Re Institute (2024) | Coefficient ≈5× DICE at any temperature | §3.4 second calibration; §4 sensitivity |
| ND-GAIN (2024) | Ranks vulnerability; does **not** measure loss — must be paired with a damage function | §3.4 σ_r; §4.1 |
| NGFS (2024) | 3 IAMs (GCAM, MESSAGEix, REMIND) + NiGEM; prices at R5; **no carbon-price → sectoral-cost mapping** | §4.1 data; and this absence is *the reason an IO layer exists at all* |

**Edit note:** the NGFS row is doing double duty — it is both a data source and
the argument for the method. Possibly split.

---

## D. Four alternative ways to translate a scenario into an economy

**Milestone reached:** IO is one of four choices, and each omission has a known,
signed cost.

| Work | Point taken | Where it bites |
|---|---|---|
| Hafner et al. (2020) | Classification: E-CGE / macroeconometric / E-SFC / E-AB | §2 framing of the choice |
| Böhringer et al. (2012) | CGE exemplar. Cross-model spread driven by **substitution elasticities** — invisible in an IO table | §5: fixed coefficients = no substitution = upper bound on transition cost |
| Mercure et al. (2018) | Macroeconometric (E3ME). \$1–4tn stranded assets — a result requiring the economy **not to clear** | §5: our inelastic-demand assumption |
| Dafermos, Nikolaidi & Galanis (2018) | E-SFC. Damage → defaults → asset deflation → **feeds back to worsen damage** | §5: we have no financial feedback loop |
| Lamperti et al. (2018) | E-AB. Damages ≫ standard IAMs; smoothness of the damage function matters more than its coefficient | §5: challenges our Ω directly |

**Milestone statement to write:** three of four literatures point the bias the
same way — *toward understatement*.

---

## E. The input–output tradition

**Milestone reached:** IO can carry emissions, and its inverse is an economic
statement, not a computational trick.

| Work | Point taken | Where it bites |
|---|---|---|
| Leontief (1936) | The system: x = Ax + f, hence the Leontief inverse | §3.2 |
| Hawkins & Simon (1949) | Existence condition via leading principal minors of I−A → "productive economy" | §3.2 spectral bound; Appendix A |
| Leontief (1970) | **Pollutants as rows of the accounting system** — origin of environmentally extended IO | §3.3 — every carbon intensity descends from this |
| Miller & Blair (2022) | Three things: the price dual; the inter-country block structure; **aggregation is not neutral** | §3.2 dual + blocks; §4.2 (aggregation bias is why regions are derived, not asserted) |

**Edit note:** Leontief (1970) is the single most important addition from the
last revision — it was previously missing entirely.

---

## F. Multi-regional IO: the data problem, and its dissolution

**Milestone reached:** the flows that once had to be estimated are now measured,
which removes an entire layer of error.

| Work | Point taken | Where it bites |
|---|---|---|
| Isard (1951) | Exact interregional formulation — and unusable, needs a full bilateral flow matrix | §2 sets up the problem |
| Chenery (1953) / Moses (1955) | Keep accounting exact, weaken behaviour: one trade coefficient per commodity for all using sectors | §2 — the alternative we don't need |
| Leontief & Strout (1963) | Estimate the missing flows by gravity | §2 — the alternative we don't need |
| Stone (1961) | Biproportional fitting: how the gravity frictions are solved | §2 |
| Tukker & Dietzenbacher (2013) | The 2000s programme that *measured* global MRIO tables | §2 turning point |
| Timmer et al. (2015) | WIOD — the main alternative database (43 economies, ends 2014) | §4.1 database choice |
| Moran & Wood (2014) | Cross-database carbon accounts agree within ~10% after harmonisation | §4.1 — reassurance, not equivalence |
| OECD (2025) | The table used: 81 economies, off-diagonal blocks supplied directly | §4.1 |
| Davis & Caldeira (2010) | Consumption-based accounting: much of developed-economy consumption is produced elsewhere → **trade-weight ranking ≠ embodied-emissions ranking** | §4.2 — the entire justification for the carbon-linkage measure |

**Edit note:** this is the longest strand (9 works). Candidate for trimming if
the chapter runs long — Stone could go.

---

## G. Pricing carbon, and who actually pays

**Milestone reached:** a price can be set but its incidence cannot be derived
from an IO table — pass-through must be a swept parameter.

| Work | Point taken | Where it bites |
|---|---|---|
| Weitzman (1974) | Prices vs quantities: instrument choice depends on relative slopes | §2 background only |
| Green (2021) | Ex post, measured reductions modest → a carbon price is a **contested policy variable** | §3.1 — supports treating the scenario as a random variable |
| Kay & Jolley (2023) | IO price model + NGFS scenarios, **single economy**: 10–30% price rises in carbon-intensive industries at \$200/t | §2 — the closest antecedent; same method, same scenarios, one country |
| Roncalli & Semet (2024) | Cost-push model; separates own-emissions charge from embodied charge; **indirect burden often larger**; incidence genuinely open | §3.3 direct vs propagated term |
| RBB Economics (2014) | Pass-through rates vary widely with market structure and shock type | §3.3 — grounds φ |
| Weber & Wasner (2023) | Under general cost pressure, market power → pass-through **above 1** | §3.3, §4.5 — why the sweep should not stop at φ=1 |
| Böhringer et al. (2012) *(reused)* | Leakage 5–20%; BCA reduces but does not eliminate; **a BCA is a tariff differentiated by embodied carbon** | §3.7 — CBAM needs no new machinery |

---

## H. From a real shock to a market price

**Milestone reached:** each link is available off the shelf, but the first one is
disputed.

| Work | Point taken | Where it bites |
|---|---|---|
| Moessner (2022) | \$10/t → +0.08pp headline inflation, OECD panel 1995–2020 | §3.5 the coefficient we adopt |
| Konradt & Weder di Mauro (2023) | Europe/Canada, 3 decades: effect **indistinguishable from zero**; relative price change, not inflation | §5 — the dispute our point estimate sits inside |
| Bauer & Känzig (2024) | Carbon pricing moves **expectations** even where realised inflation does not | §5 |
| Taylor (2007) | The monetary reaction function | §3.5 |
| Hull & White (1994) | One-factor: ΔR(τ) = B(τ)/τ · Δr, **volatility-independent** | §3.5 — why no vol surface is needed |
| Sarno & Taylor (2002) | PPP poor at short horizons; CIP close to an arbitrage identity | §3.6 — grades the two FX legs unequally |

**Edit note:** the Moessner/Konradt disagreement is the strongest "honest
weakness" in the chapter. Consider giving it its own paragraph rather than
folding it in.

---

## I. The framework, and the gap

| Work | Point taken | Where it bites |
|---|---|---|
| Kenyon, Macrina & Berrahoui (2022) | Provenance: pricing carbon consistently inside financial instruments | §2 — shows BKMN is not a one-off |
| Berrahoui et al. (2025) | The ensemble: short chain, individually auditable, two proved propositions. Answers Acharya's fourth criticism | §1, §3 throughout |

**The gap, stated as three existing things and one absence:**

1. An auditable stress-testing chain exists — for **one** economy (BKMN).
2. A mature MRIO apparatus exists, with **measured** tables (Miller & Blair;
   Tukker & Dietzenbacher; OECD).
3. IO carbon-tax incidence exists — for **one** economy (Kay & Jolley; Roncalli
   & Semet).
4. Nothing joins them. And by Leontief (1970) + Davis & Caldeira (2010), costs
   demonstrably cross borders; by definition, relative prices do not exist in a
   one-country model.

---

## Counts

| | |
|---|--:|
| Works cited | 47 |
| Strands | 9 |
| Longest strand | F (9 works) |
| Decades | 1930s–2020s, thinnest at 1980s (0) and 1990s (1) |

## Open questions for you

1. **Strand F** is the longest at 9 works. Trim Stone? Or keep — it is the
   strand that explains why the 1950s–60s references belong at all.
2. **Böhringer (2012)** appears in two strands (D and G). Deliberate — it is both
   a CGE exemplar and the leakage reference — but flag if it reads as padding.
3. **1980s empty, 1990s = 1.** Fillable with early environmentally-extended IO
   work between Leontief (1970) and the database era, if the histogram matters.
4. **Should the "where it bites" column survive into the prose?** It is what the
   supervisor objected to ("you mention a lot of what my work does"). My
   suggestion: keep it in this outline for your own use, and in the prose let
   only the closing gap statement refer to the present work.
