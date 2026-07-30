# Scenario mixture: priors, the transition matrix, and transition probabilities

How the Bayesian scenario layer works in the multi-regional BKMN model — the four
priors and where their numbers come from, the transition matrix and how it is
computed, and how the two combine into an expectation. Implements paper §2.2
(Dirichlet-categorical, Eq. 1) and §3.1.5 (expected output, Eq. 20–21).

Code: [`bkmn/mixture.py`](../bkmn/mixture.py) · coordinates from
[`bkmn/scenarios.py`](../bkmn/scenarios.py) `Scenarios.coords()` ·
gates in [`tests/test_extensions.py`](../tests/test_extensions.py).

---

## 1. What the layer is for

We do not know which climate future we are in, so we do not pick one. Each of the
seven NGFS narratives gets a probability, and every model output is reported as a
probability-weighted expectation across them (Eq. 21):

$$\mathbb{E}[\Delta X] \;=\; \sum_{s} p_s \, \Delta X_s$$

The per-scenario results `ΔX_s` are computed once and never touched by this layer —
the mixture is strictly a post-processing step. A degenerate prior (all mass on one
scenario) reproduces that scenario exactly; this is gate-checked.

## 2. The two layers of the Bayesian setup

**Categorical** — "which scenario are we in?" A draw from 7 outcomes with
probabilities **p**.

**Dirichlet** — **p** is itself unknown, so it gets a distribution, `Dir(α)`. The
α are *pseudo-counts*: `α = (2,2,2,2,2,2,2)` means "as if I had seen two pieces of
evidence for each scenario".

The Dirichlet is the **conjugate prior** of the categorical, so updating on
observed events is addition, not integration:

$$\text{prior } \mathrm{Dir}(\boldsymbol\alpha) \;+\; \text{counts } \mathbf{c}
\;\longrightarrow\; \text{posterior } \mathrm{Dir}(\boldsymbol\alpha + \mathbf{c})$$

We report the Dirichlet mean, `p_s = α_s / Σα` (`mixture.weights`).

**Σα is the prior's *strength***, not its direction: it is how many observed events
it takes to overturn the prior. All four priors below are therefore normalised to
the same **Σα = 14**, so switching prior changes the direction of belief and never
its stiffness. Rescaling leaves the implied probabilities unchanged (they are
proportions) — verified: expected-FX tables move by at most 5e-15 pp.

## 3. The four priors, and where the numbers come from

| Prior | Provenance | The belief it encodes |
|---|---|---|
| **`consensus`** | **Citable** — UNEP EGR 2025 / CAT COP30 2025 | *"We are on the published current-policy trajectory"* |
| `uniform` | Conventional (flat / uninformative) | *"I have no view"* |
| `policy-sceptic` | **Asserted by us** | *"Policy will disappoint"* |
| `ambition` | **Asserted by us** | *"The transition actually happens"* |

Resulting probabilities:

| scenario | consensus | uniform | policy-sceptic | ambition |
|---|--:|--:|--:|--:|
| Net Zero 2050 | 0.0 % | 14.3 % | 6.2 % | 23.5 % |
| Below 2 °C | 0.3 % | 14.3 % | 6.2 % | 23.5 % |
| Low demand | 0.0 % | 14.3 % | 6.2 % | 17.6 % |
| Delayed transition | 0.5 % | 14.3 % | 12.5 % | 11.8 % |
| NDCs | 6.7 % | 14.3 % | 25.0 % | 11.8 % |
| Fragmented World | 11.8 % | 14.3 % | 18.8 % | 5.9 % |
| Current Policies | **80.7 %** | 14.3 % | 25.0 % | 5.9 % |

### 3.1 `consensus` — the only one with a source

Built by the paper's own §3.1.4 construction: take an authoritative statement about
where current policies lead, and put the mass on the matching scenario. The paper
used IPCC (2023) — *"a path closer to SSP2 combined with RCP4.5 or RCP6.0"* — and
assigned 90 %. The NGFS-era equivalents are the published warming estimates:

| Source | Current policies | NDCs | Optimistic |
|---|--:|--:|--:|
| UNEP *Emissions Gap Report 2025* | **2.8 °C** | 2.3–2.5 °C | — |
| Climate Action Tracker, COP30 update (Nov 2025) | **~2.6 °C** | 2.6 °C | 1.6 °C |

Anchor **μ = 2.7 °C** (midpoint), **sd = 0.3 °C** (spread across the two
assessments). Weights are Gaussian in each scenario's *own* end-century warming:

$$\alpha_s \;\propto\; \exp\!\left(-\tfrac{1}{2}\left(\frac{T_{2100,s}-\mu}{sd}\right)^{2}\right),
\qquad \textstyle\sum_s \alpha_s = 14$$

Current Policies (T₂₁₀₀ = 2.75 °C) lands within **0.05 K** of the anchor, hence
80.7 %. Like the paper's 90 %, the result is concentrated — and that is itself the
finding: on the published trajectory the carbon price stays near zero, so expected
transition-FX moves collapse (IND −6.20 % under `uniform` → **−0.54 %** under
`consensus` at 2040). **Transition FX risk lives in the tail, not the expectation.**

⚠️ Mapping caveat: NGFS's own *NDCs* scenario reaches 2.03 °C while UNEP and CAT
put full NDC implementation at 2.3–2.6 °C. The NGFS NDC narrative is more
optimistic than the external assessments, which is part of why weight shifts onto
Current Policies rather than NDCs.

### 3.2 `uniform`, and the two asserted bookends

`uniform` (all α equal) is the standard uninformative choice and needs no defence.

**`policy-sceptic` and `ambition` are ours.** The directions are narrative logic —
mass on the low- or high-ambition end — but the magnitudes are arbitrary round
numbers chosen to give a visible spread. There is no standard to borrow: **NGFS
deliberately publishes no scenario probabilities**, stating its scenarios are not
forecasts. Report them as illustrative bookends, not estimates. The spread across
all four priors is the honest measure of prior uncertainty.

### 3.3 Updating on observed events

`mixture.alphas(prior, counts=...)` exposes the §2.2 conjugate update. Counts are
events the user attributes to each narrative — e.g. three policy rollbacks and one
net-zero commitment since the prior date:

```
counts = {"Current Policies": 3, "Net Zero 2050": 1}
```

Effect (Current Policies weight): uniform 14.3 % → 27.8 %, policy-sceptic
25.0 % → 36.1 %, ambition 5.9 % → 21.2 %. Because all priors share Σα = 14, the
same evidence moves them by comparable amounts.

---

## 4. The transition matrix

### 4.1 What it does, and the paper's version

Eq. 1 lets the mixture **drift** year on year, because *"policy makers can change,
so it may be possible to move between scenarios"*:

$$q(j,k) \;=\; \frac{\exp(-\lambda\, d(j,k))}{\sum_{h}\exp(-\lambda\, d(j,h))}$$

The paper's `d(j,k) = |j−k|` is the gap between **RCP concentration labels** (1.9,
2.6, 3.4, 4.5, 6.0) — a physical number the scenario set supplies.

The paper's Q is **25 × 25 over SSP/RCP pairs and block diagonal**: transitions
between RCP states are allowed, between SSP states are not (§2.2), because an SSP
is an immutable socioeconomic storyline while an RCP is a mutable policy outcome.
Five 5×5 blocks, off-diagonal blocks structurally zero, 20 % density.

**Ours is a dense 7 × 7.** NGFS narratives are flat — they do not factor into a
mutable × immutable pair, so there is no block structure to impose. Implausible
transitions are suppressed by the distance metric (soft zeros) rather than by
structural zeros: Net Zero ⇄ Current Policies carries an annual probability of
**0.00012**. Imposing a block structure on "international coordination" was tested
and rejected — NGFS Phase 5 has only one fragmented narrative, so its block becomes
absorbing, which is an artefact.

The non-uniform stationary distribution is **inherent to Eq. 1**, not to our metric:
an exponential kernel on a bounded set gives interior states more inflow than edge
states. The paper's own five RCP levels give `[0.194, 0.222, 0.225, 0.204, 0.155]`.

### 4.2 The distance metric for NGFS

NGFS narratives carry no numeric label, so `d` had to be defined. We use the
**Euclidean distance in standardised (T₂₁₀₀, XCE₂₀₅₀) space** — end-century warming
and carbon price, the two characteristics that distinguish the scenarios and that
drive this model. Eq. 1 explicitly permits it: the distance *"can be generalized to
include any function of RCP characteristics"*.

The obvious 1-D substitute — warming alone, the direct analogue of an RCP level —
**fails empirically**. Correlation between pairwise distance and how differently the
model behaves (mean |ΔFX| across the 14 currencies, 2040):

| coordinate | correlation |
|---|--:|
| \|ΔT₂₁₀₀\| | 0.28 |
| \|ΔXCE\| | **0.98** |

The decisive case: **Net Zero 2050 vs Low demand are 0.01 K apart** in end-warming —
so a warming metric calls them the same state — yet **$306/t apart** in carbon price
and **3.2 pp apart** in mean FX impact, the largest gap of any near-neighbour pair.
They reach the same temperature by different means, and the model cares. 2-D also
stays valid if the physical channel is scaled up later (where warming *would*
matter), whereas a price-only metric would then be wrong.

*Method note:* the metric is defined on scenario **characteristics** (inputs). The
output correlation above is a **diagnostic** that it separates scenarios the model
treats differently — not the definition, which would be circular.

---

## 5. Computing the transition probabilities, step by step

### Step 1 — coordinates, straight from the NGFS data (no choices)

| scenario | T₂₁₀₀ (K) | XCE₂₀₅₀ ($/t) |
|---|--:|--:|
| Net Zero 2050 | 1.45 | 626 |
| Low demand | 1.47 | 320 |
| Below 2 °C | 1.69 | 153 |
| Delayed transition | 1.75 | 168 |
| NDCs | 2.03 | 90 |
| Fragmented World | 2.11 | 120 |
| Current Policies | 2.75 | 3 |

### Step 2 — standardise each axis (z-score)

T: mean 1.893, sd 0.421 K · XCE: mean 211.4, sd 191.1 $/t. This makes λ
dimensionless and stops $/t swamping K.

### Step 3 — pairwise Euclidean distance in that space

Sanity: Below 2 °C ⇄ Delayed transition = **0.17** (near-identical);
Net Zero ⇄ Current Policies = **4.49** (the far corners).

### Step 4 — apply the Eq. 1 kernel and normalise each row

Worked example, the row from Below 2 °C at λ = 2:

```
exp(-2d):  Below2C 1.0000   Delayed 0.7105   NDCs 0.1729   LowDem 0.1312
           Fragm   0.1304   NetZero 0.0063   CurrPol 0.0050
row sum = 2.1562  ->  divide through
        =  0.464    0.330     0.080     0.061     0.060     0.003    0.002
```

λ is the **only free parameter**. The paper gives no value (Table 17: *"the
narrative users set the value of λ"*), so it is swept over 5.0 / 2.0 / 0.5.

The resulting annual matrix Q (λ = 2):

| from ↓ / to → | Below2°C | CurrPol | Delayed | Fragm | LowDem | NDCs | NetZero |
|---|--:|--:|--:|--:|--:|--:|--:|
| **Below 2 °C** | 0.464 | 0.002 | **0.330** | 0.060 | 0.061 | 0.080 | 0.003 |
| **Current Policies** | 0.005 | **0.928** | 0.006 | 0.034 | 0.001 | 0.026 | 0.000 |
| **Delayed transition** | **0.319** | 0.003 | 0.449 | 0.076 | 0.056 | 0.095 | 0.003 |
| **Fragmented World** | 0.066 | 0.019 | 0.086 | 0.507 | 0.012 | **0.309** | 0.001 |
| **Low demand** | 0.097 | 0.001 | 0.092 | 0.018 | **0.741** | 0.020 | 0.030 |
| **NDCs** | 0.084 | 0.014 | 0.103 | **0.297** | 0.013 | 0.487 | 0.001 |
| **Net Zero 2050** | 0.006 | 0.000 | 0.006 | 0.002 | 0.038 | 0.002 | **0.945** |

Reading it: the isolated extremes are sticky (Current Policies 0.928, Net Zero
0.945 annual self-persistence); the close pairs are near-interchangeable
(Below 2 °C ⇄ Delayed transition ≈ 0.32, NDCs ⇄ Fragmented World ≈ 0.30); and
Net Zero ⇄ Current Policies is effectively unreachable (0.0001).

### Step 5 — push the prior forward and take the expectation

$$p_T = p_0 \, Q^{\,T-2022}, \qquad
\mathbb{E}_T[\Delta X] = \sum_s p_T[s]\,\Delta X_s$$

Under the `ambition` prior (λ = 2):

| | NetZero | Below2°C | Delayed | NDCs | Fragm | CurrPol |
|---|--:|--:|--:|--:|--:|--:|
| **2022** (prior) | 0.235 | 0.235 | 0.118 | 0.118 | 0.059 | 0.059 |
| **2040** | 0.145 | 0.172 | 0.178 | 0.160 | 0.154 | 0.073 |

The prior erodes toward the stationary distribution — Net Zero 0.235 → 0.145 while
Fragmented World rises 0.059 → 0.154.

---

## 6. Status: static mixture is the headline, drift is a sensitivity

The **static** mixture (`out_ext_fx_expected_*.csv`, fig3) is the base case,
because it rests on **one** assumption (the prior). The transition matrix needs
**three** (prior, λ, and a distance over narratives), so it is reported separately
(`out_sens_fx_drift_*_lam*.csv`, fig9).

Its result is worth having: **drift erodes the prior, so the priors converge** — by
2045 at λ = 0.5 they are indistinguishable, where the static mixture keeps them
~6 pp apart. In other words the narrative choice matters at 5–10 years and stops
mattering by 20.

## 7. Gates

`Σα` equal across priors · weights sum to 1 · a degenerate prior reproduces its
scenario exactly · `E[X]` within the scenario range · all 7 scenarios carry
positive weight (this caught a real bug where a label mismatch silently dropped
*Below 2 °C*) · counts shift the posterior toward the counted scenario ·
Q rows are probabilities · the diagonal is the mode · **λ → ∞ reproduces the static
mixture exactly** · `consensus` puts most weight on the scenario nearest the anchor
and falls monotonically with distance from it.
