# Validation

## 1. What needs validating, and what cannot be

A climate stress test produces numbers that nobody can check against an outcome.
There is no realised 2040 to compare a −3.6 % INR forward against, and there will
not be one in time to matter. Backtesting is unavailable in principle, not merely
inconvenient.

That leaves three things one *can* establish, and it is worth being precise about
which is which:

| | question | how |
|---|---|---|
| **Reproduction** | does the code compute what the paper specifies? | reduce to the paper's own case and compare printed numbers |
| **Structure** | does the model have the properties it claims? | run it on economies whose answer is known by symmetry |
| **Plausibility** | are the magnitudes credible? | compare aggregates against independent estimates |

Only the second is a genuine test of the *multi-regional generalisation*, and it
is the one this chapter is mostly about. Reproduction cannot see it, because the
paper is single-region: a bug that couples two regions wrongly reproduces the
single-region case perfectly. Plausibility cannot see it either, because a
transposed block or a leak between regions produces numbers that look entirely
reasonable — that is precisely what makes such bugs dangerous.

The failure mode to defend against is not a crash. It is a model that runs, whose
outputs are the right order of magnitude, and which is silently wrong about which
region is affected by what.

## 2. The principle: test where the answer is known in advance

The technique is to construct economies for which symmetry dictates the answer,
run the **production code** on them, and check that it returns it.

Two properties make this stronger than it first appears.

**The answers are exact, not approximate.** If two regions are identical in every
input, their outputs must be identical — not close. A tolerance of 10⁻¹⁵ is
available, which means the test detects errors far too small to notice in a
results table. A 0.1 % asymmetry in a GVA shock would pass any eyeball check and
fail this one by twelve orders of magnitude.

**They exercise the shipped code path.** The synthetic economies are constructed
as the same `Model20R` object the real loader returns
([`bkmn/synthetic.py`](../bkmn/synthetic.py)), so `transition`, `macro` and `fx`
run on them unmodified. A pass is evidence about the code that produces the
results, not about a reimplementation of it written to agree.

The suite is [`tests/test_validation.py`](../tests/test_validation.py) — 32 gates,
run with `py -3 tests/test_validation.py`.

## 3. The three constructions

### 3.1 Isolation — a region with no trade links

Take a symmetric economy and cut one region's trade: zero the off-diagonal blocks
of **A** that connect region *k* to everyone else, in both directions. Region *k*
still has its own internal input–output structure; it simply neither buys from nor
sells to anyone.

Because the transition channel propagates through the Leontief dual
$\tilde{\mathcal{L}}(\phi) = (\mathbf{I}-\phi\mathbf{A}^{\top})^{-1}\phi$, a
block-diagonal **A** must give a block-diagonal operator. So:

* a carbon price levied **only on *k*** must move nothing outside *k*;
* a carbon price levied **on everyone but *k*** must not move *k*;
* *k*'s own response must equal that of a genuinely standalone single-region
  model of *k*.

All three hold to **exactly zero** — not to tolerance, but to bitwise zero,
because the blocked entries are structural zeros rather than small numbers.

> **The control matters more than the test.** A test that a quantity is zero is
> worthless if the quantity is zero for a trivial reason. So the same shock is run
> on the *unmodified* symmetric economy, where the spillover must be non-zero: it
> is 0.049 %, comfortably measurable. The isolation test has teeth because the
> connected case demonstrably fails it.

This construction also gives the cleanest statement of what the multi-regional
extension *is*: under autarky the model decomposes into $R$ independent
single-region models, each reproducing the paper's case exactly. That is gate
group D, and it is the formal sense in which the generalisation contains the
original.

### 3.2 Symmetry — identical regions must give identical answers

Construct an economy of $R$ regions that are identical in every respect:
technology, carbon intensity, size, vulnerability, and trade shares (each ships
the same fraction to every partner). Apply a uniform carbon price.

Every region must then receive an identical GVA shock, and — because FX is built
entirely from *differences* between regions — **every exchange rate must be
exactly unmoved**.

This is the most informative of the three, because FX is a difference and
differences are where sign errors live. Any asymmetry the model reports here is
spurious by construction: there is no input that could justify it.

The results distinguish two kinds of zero, and the distinction is worth keeping:

| | result | why |
|---|---|---|
| spot FX | **exactly 0.0** | built by multiplying identical inputs, so the floats are bitwise identical |
| forward points | **9.8 × 10⁻¹⁸** | descends from the GVA shock, which passes through a matrix inversion; identical rows are solved independently and agree only to rounding |

The second is 3 × 10⁻¹⁵ relative to the rate shift it derives from — machine
precision, not a modelling asymmetry. Reporting it as "exactly zero" would be
false, and the gate asserts the relative bound rather than an absolute one for
that reason.

### 3.3 One broken symmetry — effects appear where they were put

Start from the symmetric economy and change exactly one thing. Everything that
follows should be attributable to that one change, and nothing else should move
relative to anything else.

Two versions are run:

**Price asymmetry** — charge carbon in one region only. Then the shocked region
must be worst hit (−0.414 % against −0.054 % for the others); every unshocked
region must be affected *identically to every other* (spread 1 × 10⁻¹⁹); the
spillover must be negative and smaller than the direct hit; and the unshocked
currencies must not move against **each other** (2 × 10⁻¹⁹) even though they all
move against the shocked one.

**Intensity asymmetry** — make one region carbon-intensive and price everyone
equally. The dirty region must be worst hit (−1.044 %), and the rest must remain
identical to each other.

Together these establish that asymmetry propagates through the intended channels
and only those.

#### A test that caught a wrong expectation

The gate on the *sign* of the shocked region's currency move initially asserted
the wrong thing. The intuition was that a region taking a large hit should see its
currency weaken. The model said the opposite, and the model was right: the shocked
region takes the deeper rate cut, and under covered interest parity a lower-rate
currency trades at a **forward premium**. With $S$ in units of *r* per base, the
forward points are

$$\Delta\text{pts} = B(\tau)\,\bigl[\Delta r_r - \Delta r_{\text{base}}\bigr] < 0,$$

i.e. *r* appreciates forward. The gate now asserts the mechanism —
$\operatorname{sign}(\Delta\text{pts}) = \operatorname{sign}(\Delta r_r - \Delta
r_{\text{base}})$, and the magnitude equals $B(5)$ times the rate gap exactly —
rather than an intuition about direction.

This is worth recording because it is what the exercise is for. The same
counter-intuitive sign appears throughout the results ([FX_REPORT.md](FX_REPORT.md)
§3: a strengthening currency is a distress signal), and having derived it from a
controlled case makes it a property of the model rather than a surprise in the
output.

## 4. Linearity and superposition

Two further properties are tested because the analysis depends on them rather
than because they are in doubt:

**Exact linearity in the carbon price.** Doubling the price doubles every regional
shock, to 0.0 — the charge channel is linear in $\mathrm{XCE}$ by Eq 10, and the
gate confirms no non-linearity has crept in through the implementation.

**Exact superposition across regions.** Shocking regions *a* and *b* together
gives precisely the sum of shocking each alone (2 × 10⁻¹⁹ on the synthetic
economy, 7 × 10⁻¹⁸ on the real calibration). This is what licenses attributing
results to individual policies: contributions decompose **exactly**, with no
Shapley machinery and no order dependence. The same property underwrites the
tariff decomposition in [TARIFF_METHOD.md](TARIFF_METHOD.md) §7.

## 5. The same properties on the real calibration

The synthetic tests establish that the machinery is right. They cannot establish
that the *data* is wired to it correctly — a mis-ordered region vector would pass
every symmetric test, because symmetric data is invariant to ordering.

So group E repeats the structural checks on the shipped 13-region build:

| gate | result |
|---|---|
| shocks superpose | 6.9 × 10⁻¹⁸ |
| isolating China removes every spillover | exactly 0 |
| *control*: connected China does reach others | largest spillover RASIA −0.110 % against China's own −2.496 % |
| the priced region is the worst hit | China −2.496 %, the minimum |
| no region is inert under a world price | least affected CHE −0.277 % |
| φ = 0 reduces to −CT/GVA | exactly 0 |

The last is the analytic anchor: at zero pass-through the shock must equal minus
the carbon bill over value added, region by region, with no Leontief propagation
at all. It holds to bitwise zero, which confirms the operator assembles correctly
on real data.

## 6. Reproduction and plausibility, for completeness

The other two validation modes are covered elsewhere and are summarised here only
so the picture is complete.

**Reproduction (`tests/test_fx.py`, 9 gates).** A flat carbon price of \$70/t
reproduces the committed transition tables to 5.6 × 10⁻¹⁷ pp; the UK region shock
at φ = 0 is −0.851 %, the paper's own printed value; Hull-White limits, EUR-base
self-consistency and forward-point triangular consistency all hold to machine
precision.

**Plausibility.** The one external benchmark the model passes is on GDP: after
the scenario-consistent-intensity correction, the worst regional transition shock
under Net Zero is −4.7 %, inside NGFS's own NiGEM range of roughly −1 % to −4 %.
The static-intensity version put it at −11.3 %, three times outside — which is how
the error was found. **The FX numbers themselves have no external benchmark**,
and this should be stated wherever they are quoted.

**Aggregation invariance.** One further check falls out of the region work: the
EU-side results of the tariff illustration are *identical* under the 20- and
13-region builds (\$157 bn revenue, −0.0842 % EU GVA, +0.603 % consumer prices).
They must be — the EU's own composition is unchanged and the aggregate cannot
depend on how the rest of the world is partitioned — and that they are is a
non-trivial check on the aggregation code. The complementary test, whether
partitioning the residual more finely moves the *named* regions, is in
[`tools/test_row_sufficiency.py`](../tools/test_row_sufficiency.py): splitting ROW
into its six most significant members changes analytical-region GVA shocks by at
most 0.007 pp.

## 7. What this does not establish

**Structural correctness is not empirical correctness.** Every gate in §3–§5 would
pass for a model with the wrong damage coefficient, the wrong carbon prices, or a
mis-specified Taylor rule. They test that the machinery does what it claims, not
that the claim describes the world.

**Symmetric tests cannot see ordering errors in symmetric data.** This is why
group E exists, but group E is weaker: on real data the right answer is not known
in advance, so those gates test invariants (superposition, isolation, the φ = 0
identity) rather than values.

**The synthetic economies violate material balance.** Cutting trade links breaks
$\mathbf{x} = \mathbf{A}\mathbf{x} + \mathbf{f}$. This is deliberate and harmless
— the transition channel is a *price* calculation that consumes only **A**, **x**,
GVA and **ct** — but it means these constructions could not be used to validate a
quantity-side model.

**Tolerances are asserted, not derived.** The relative bound of 10⁻¹⁴ on the
rounding-level gates is a judgement about what double precision should deliver
through one matrix inversion. It is loose enough to be robust and tight enough
that any real asymmetry would fail it by many orders of magnitude, but it is not
derived from a conditioning analysis.

**Coverage is uneven.** The transition and FX channels are tested hardest. The
mixture, volatility and operational-risk layers are covered by
`tests/test_extensions.py` in the reproduction sense — identities, monotonicity,
sign — but not by the symmetry constructions used here.

## 8. Summary

| suite | gates | establishes |
|---|--:|---|
| `tests/test_fx.py` | 9 | reproduction — the code computes the specified relations |
| `tests/test_extensions.py` | 79 | identities, monotonicity and sign across every channel |
| `tests/test_validation.py` | **32** | **structure — isolation, symmetry, superposition, reduction** |

The structural suite is the one that addresses the multi-regional generalisation
directly. It establishes that regions are coupled only through trade; that the
model reduces exactly to the single-region case under autarky; that identical
inputs produce identical outputs and exactly zero FX; that breaking symmetry in
one place moves results in exactly that place; and that shocks superpose
exactly, so contributions decompose without approximation.

None of that makes the forecasts right. It makes them *interpretable*: when the
model says India's currency moves and Switzerland's does not, that difference can
be attributed to inputs rather than to arithmetic.
