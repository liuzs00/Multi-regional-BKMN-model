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

## 7. What this does not show

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
