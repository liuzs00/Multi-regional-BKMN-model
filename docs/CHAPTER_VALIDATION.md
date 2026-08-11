# Validation

## 1. Why the model is tested structurally

A climate stress test cannot be backtested. There is no realised 2040 to compare a
projected exchange-rate move against, and there never will be in time to matter. So the
usual test of a financial model — did it predict well? — simply is not available.

What can be checked is whether the model behaves the way it claims to. The danger here
is not a crash. It is a model that runs cleanly, produces numbers of a believable size,
and is quietly wrong about which region is affected by what. A transposed block or a
leak between regions gives output that looks perfectly reasonable, and that is exactly
what makes those errors hard to catch.

The approach taken is to build economies whose answer is obvious in advance, run the
real model code on them, and see whether it gives that answer. Three such economies are
used. Between them they establish that regions are connected only through trade, that
the connection is symmetric when the inputs are, and that asymmetry shows up only where
it is put in.

Two things make this sharper than it sounds. First, the expected answers are exact, not
approximate. If two regions are identical in every input, their results must be
identical — so the test can be run at a tolerance of $10^{-15}$, and an asymmetry of
$0.1\%$, which no one would spot by eye, fails it by twelve orders of magnitude. Second,
the synthetic economies are built as the same model object the real loader produces, so
the transition, macro and exchange-rate code runs on them untouched. A pass says
something about the code that produces the published results, not about a second version
written to agree with it.

The suite is `tests/test_validation.py`, 44 gates in all; the economies are built in
`bkmn/synthetic.py`.

---

## 2. Isolation: one region cut off

**What is done.** Start from a symmetric economy and cut one region out of world trade,
zeroing the off-diagonal blocks of $\mathbf{A}$ that link region $k$ to everyone else in
both directions. Region $k$ keeps its own internal input–output structure. It simply
buys from no one and sells to no one.

**Why the answer is obvious.** The transition shock travels through the modified
Leontief dual

$$\tilde{\mathcal{L}}(\phi) = \bigl(\mathbf{I}-\phi\mathbf{A}^{\top}\bigr)^{-1}\phi ,$$

and if $\mathbf{A}$ is block-diagonal then so is the operator built from it. With no
path between $k$ and the rest of the world, nothing can travel either way. The answer
has to be zero — and structurally zero, since the blocked entries are genuine zeros
rather than small numbers, so the result should come out bitwise zero rather than merely
close to it.

**The control.** Showing that something is zero proves nothing if it would have been
zero anyway. A transmission channel that never fires, or a shock quietly dropped on the
floor, would give the same clean zero. So gate A4 applies the same shock to the
*untouched*, still-connected economy and demands that the spillover be strictly
positive. Only with that in hand does the zero mean what it looks like it means.

| Gate | What it asserts | Result |
|---|---|---|
| A1 | Shock the isolated region → nothing else moves | $0.0\times10^{0}$ |
| A1b | …but it does move itself | $-0.2961\%$ |
| A2 | Shock everyone else → the isolated region stays put | $0.0\times10^{0}$ |
| A2b | …but the others do move | pass |
| A3 | Isolated region $=$ standalone single-region model | $0.0\times10^{0}$ |
| A4 | *Control*: connected regions really do transmit | $0.0491\%$ |

Comparing A1b with A4 says something economic as well as computational: a carbon charge
lands about six times harder at home than abroad. That is the leakage result of the
input–output chapter, showing up again on a made-up economy.

---

## 3. Symmetry: every region the same

**What is done.** Build an economy of $R$ regions that are identical in every way —
technology, carbon intensity, size, vulnerability, and trade shares, each shipping the
same fraction to every partner — then apply the same carbon price everywhere.

**Why the answer is obvious.** Identical inputs have to give identical outputs. Every
region must take the same hit to value added. And because exchange rates in this model
are built entirely out of *differences* between regions, every exchange rate must come
out exactly unmoved. If the model reports any asymmetry here, it is spurious by
construction — there is no input that could have caused it. That is what makes this the
most revealing of the three tests: differences are where sign errors and indexing
mistakes hide.

| Gate | What it asserts | Result |
|---|---|---|
| B1 | Identical regions take identical shocks | spread $5.2\times10^{-18}$ |
| B1b | …and the shock is negative | $-0.6298\%$ each |
| B2 | Spot exchange rate is exactly zero | $0.0\times10^{0}$ |
| B3 | Forward points vanish, to rounding | $7.9\times10^{-18}$ ($2.5\times10^{-15}$ relative) |
| B4 | *Control*: the operator is not degenerate | pass |

The two kinds of zero here are different, and the difference is worth keeping straight.
The spot rate comes from multiplying identical inputs, so the floating-point numbers are
bitwise identical and the answer is exactly zero. Forward points come from the
value-added shock, which passes through a matrix inversion where identical rows get
solved separately and agree only to rounding. What is left is machine precision, not a
real asymmetry, which is why B3 asserts a relative bound rather than an absolute one.

---

## 4. Broken symmetry: identical regions, then change one thing

**What is done.** Start from the symmetric economy and change exactly one input. Two
versions are run. In the first, carbon is charged in one region only. In the second, one
region is made carbon-intensive and then every region is priced the same.

**Why the answer is obvious.** Section 3 has already established a world in which
nothing moves. Break the symmetry in one place and anything that now moves has to be
down to that one change, because everything else is still identical and there is nothing
else it could be. So the test checks not just that the model reacts, but that it reacts
*only* where the change was made.

| Gate | What it asserts | Result |
|---|---|---|
| C1 | The shocked region is worst hit | $-0.4139\%$ (the minimum) |
| C2 | Every unshocked region is hit identically | spread $1.1\times10^{-19}$ |
| C3 | Spillover is negative, but smaller than the direct hit | $-0.0540\%$ vs $-0.4139\%$ |
| C4 | Unshocked currencies do not move against each other | $2.5\times10^{-19}$ |
| C5 | The shocked currency moves with the sign CIP requires | $-17.99$ bp gap → $-81.54$ bp (forward premium) |
| C5b | …and the size is $B(5)$ times the rate gap, exactly | pass |
| C6 | The carbon-intensive region is worst hit | $-1.0437\%$ |
| C7 | The rest stay identical to each other | spread $6.1\times10^{-18}$ |
| C8 | The charge channel is exactly linear in the carbon price | $0.0\times10^{0}$ |
| C9 | Shocks add up exactly | $8.7\times10^{-19}$ |

Three of these are worth pausing on. C5 pins down a sign that looks wrong at first: the
shocked region gets the deeper rate cut, and under covered interest parity a lower-rate
currency trades at a *forward premium*, so the currency of the worst-hit economy
strengthens. The same sign turns up throughout the results, where a strengthening
currency is a distress signal rather than a good one, and pinning it down on a
controlled case turns it from a surprise in the output into a known property of the
model. C8 and C9 establish linearity and superposition, and those are what allow results
to be attributed to individual policies: the contributions add up exactly, with no
approximation and no dependence on the order they are applied in.

---

## 5. Reduction to the single-region model

A fourth case falls out of the first. Zero *every* off-diagonal block and the whole
system is in autarky, at which point it has to break apart into $R$ separate
single-region economies, each reproducing the original model exactly.

| Gate | What it asserts | Result |
|---|---|---|
| D1 | Under autarky each region depends only on its own price | $0.0\times10^{0}$ |
| D2 | Each autarkic region $=$ standalone single-region model (R0–R3) | $0.0\times10^{0}$ |

This is the precise sense in which the multi-regional model *contains* the single-region
one it extends: turn trade off and the original comes back exactly, not approximately.
It is the direct answer to the obvious question — has extending the model broken the
thing it was extending?

---

## 6. Reading the results

There are two kinds of gate here, and both are needed.

*Invariance* gates say a quantity must be zero — A1, A2, A3, B2, C2, C4, D1, D2. They
catch leakage, asymmetry that should not be there, and wiring mistakes. *Liveness* gates
say a quantity must **not** be zero, and must have the right sign and ordering — A1b,
A4, B1b, C1, C3, C6. They catch a model that has stopped doing anything at all.

That second group is not padding. A model that returned zero for everything would sail
through every invariance gate — no leakage, perfect symmetry, exact reduction — while
being completely dead. So the non-zero numbers in the tables above are required results,
not leftovers: the $-0.2961\%$ in A1b says a carbon charge does hurt the region paying
it, and the $0.0491\%$ in A4 says connected regions do pass shocks between them.

All 44 gates pass.

---

## 7. Testing the tests: mutation

A suite is worth exactly what it *rejects*. Every gate above passes, but that is equally
consistent with the gates being too weak to fail. The check is to break the model
deliberately and confirm the suite notices.

Seven plausible implementation errors were injected one at a time, each a single edit a
real implementation could contain, and every gate was run against each:

| injected bug | caught by |
|---|---|
| Hull–White $B(\tau)$ uses $+a\tau$ instead of $-a\tau$ | all three suites |
| technical matrix transposed | reproduction |
| $\mathbf{A}$ normalised by row instead of column | reproduction |
| Eq 10 sign error ($+\mathbf{I}$ for $-\mathbf{I}$) | all three suites |
| forward-points sign flipped | structural |
| **spot sign flipped** | **nothing — survived** |
| **forward $=$ spot $-$ points** | **nothing — survived** |

Two survived, and the reason generalises: **symmetry testing is sign-blind.** Every
invariance gate in §3 asserts that a quantity is *zero*, and zero has no sign. Flipping
the sign of the spot channel leaves every zero at zero and every magnitude unchanged. The
one non-symmetric spot gate elsewhere in the project compares $|\text{spot}|$, so it is
sign-blind too. A model reporting *"a country that prices carbon sees its currency
strengthen"* — the exact reverse of the economics — would have passed every gate then in
the suite, 120 of them.

Composition was simply never tested: `forward_total` is a one-line sum, which is precisely
why nobody thought to check whether it added or subtracted.

**Group F** closes both, by pinning direction and composition where the answer is
unambiguous rather than zero:

* a region with *higher* carbon-pricing scope than the base must **depreciate**
  (spot $> 0$), and one with lower scope must appreciate — the relative-PPP direction;
* the forward must equal spot **plus** points exactly, collapsing to each leg when the
  other gap vanishes, with a control confirming the two legs have opposite signs in the
  test case so the identity is not satisfied trivially;
* on the real calibration EU27 holds the **highest** carbon-pricing scope (0.645 against
  0.467 next), so relative PPP *requires* every other currency to appreciate against the
  euro.

That last gate turns a result into an explanation: the absence of spot sign reversals is
forced by the EU being the most carbon-priced economy in the set, not a coincidence, and
the gate fails the day that stops being true. After group F, all seven mutants are caught.

The lesson outlives this project. Symmetry arguments establish that a model is
*internally consistent*, not that it points the right way, so any suite built on them
needs at least one asymmetric, direction-pinning test per channel — and the way to find
out whether it has one is to break the model on purpose.

---

## 8. Cross-implementation reading

A fourth mode sits outside the three above, and in practice it found more than they did:
reading an independent implementation of the same paper and diffing the *specifications*
rather than the numbers. The single-region reproduction this project extends is such an
implementation, and a full read produced four findings no gate could have.

**An inconsistency of ours, corrected.** We had accepted that a tax wedge is not an output
gap and removed the transition shock from the Taylor rule — then left it in the
operational-risk channel, which runs Okun's law. Okun maps real *output* to employment; a
wedge destroys no output. The reference is unambiguous: it calls `oprisk.shift(omega, …)`
and never passes it the carbon shock. Correcting it moved conduct losses at 2040 under Net
Zero from 2.0–37.1 % to **2.0–10.2 %**.

The 37.1 % is the instructive part. The reference's Eq 25 is a *saturating* form bounded
above by 23.77 % for conduct; ours is the linearisation of the same regression and is
unbounded, so it had produced a number the reference's functional form **cannot generate
at any damage level**. Dimensionally fine, correctly signed, monotone, and wrong.

**An open question closed.** The deviation register carried Eq 15's integral as an
ambiguity. The reference *defines* `short_rate_shift` for it and never calls it, passing
the Taylor output straight into the Hull–White expansion, which is what we do.

**A choice quantified.** Proposition 1 admits a direct reading and a cascading one. The
direct form reproduces $\Omega$ exactly by the Prop-1 identity; the cascade gives 0.42× of
it at $\phi = 0.5$, so applying both — as the text can be read to suggest — would count the
damage 1.42 times.

**A framing difference recorded.** The reference evaluates $\Omega$ at the *valuation
date* for the Taylor rule and op-risk, so its climate rate shift is constant across
tenors. Correct for its question, a repricing of today's damage; wrong for a 2025–2045
projection, and it means our rate path is not comparable to the paper's Table 12.

Two of these four were unreachable by self-consistency testing, because the model was
internally consistent about the wrong specification. Where a second implementation exists,
reading it is cheaper than re-deriving the same conclusions from prose, and more reliable:
code cannot be ambiguous about which of two readings it took.

---

## 9. What this does not show

Structural correctness is not empirical correctness. Every gate above would pass just as
happily for a model with the wrong damage coefficient, the wrong carbon prices, or a
badly specified Taylor rule. They show that the machinery does what it says it does, not
that what it says describes the world.

Symmetric tests also cannot spot ordering errors in symmetric data, since symmetric data
looks the same however it is ordered. So the same invariants are run again on the real
thirteen-region calibration, where shocks superpose to $6.9\times10^{-18}$, isolating
China removes every spillover exactly, and the $\phi = 0$ reduction to
$-\mathrm{CT}/\mathrm{GVA}$ holds to bitwise zero.

One last caveat: the synthetic economies do not balance. Cutting trade links breaks
$\mathbf{x} = \mathbf{A}\mathbf{x} + \mathbf{f}$. That is deliberate and does no harm
here, because the transition channel is a price calculation that only ever touches
$\mathbf{A}$, $\mathbf{x}$, value added and the charge vector — but these constructions
could not be used to check a quantity-side model.

None of this makes the projections right. It makes them interpretable. When the model
says one currency moves and another does not, that difference can be traced to the
inputs rather than to the arithmetic.
