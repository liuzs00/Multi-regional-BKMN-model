# What Each Validation Gate Does

Companion to [CHAPTER_VALIDATION.md](CHAPTER_VALIDATION.md), which argues *why*
the model is tested structurally. This note is the reference: for every gate in
[`tests/test_validation.py`](../tests/test_validation.py), what it does, what a
pass establishes, and how to read the number it prints.

Covers **groups A, B and C** — isolation, symmetry, and broken symmetry — which
are 21 of the 44 gates. Groups D, E and F are not documented here yet.

```
py -3 tests/test_validation.py
```

⚠️ On a non-UTF-8 console the run dies partway through group C with
`UnicodeEncodeError: 'gbk' codec can't encode character '−'` — the minus
sign in the C8 detail string. This is a printing failure, not a model failure.
Run `PYTHONIOENCODING=utf-8 py -3 tests/test_validation.py` instead.

---

## How to read a gate

Every line has the same shape:

```
  PASS  A1 shock to isolated region does not leak out  max |other| = 0.0e+00
        ^^                                             ^^^^^^^^^^^^^^^^^^^^^
        which gate                                     the quantity it measured
```

The printed number is not decoration. It is the quantity the assertion was made
about, so a gate that passes with `9.8e-18` and one that passes with `4.3e-4`
against a loose threshold are telling you very different things. Where a gate
reports `0.0e+00` the answer is *bitwise* zero, not merely small.

**Two kinds of gate, and they are not interchangeable.** *Invariance* gates
assert that a quantity must be zero — no leakage, no asymmetry, no dependence
where none was put. They catch wiring mistakes. *Liveness* gates (marked
**control** below) assert that something is strictly non-zero, and they exist
because an invariance gate proves nothing on its own: a channel that never fires,
or a shock quietly dropped on the floor, satisfies every "must be zero" test
perfectly. Each invariance gate in this suite is paired with a control, and the
pairing is what makes the zero mean anything.

---

## Group A — isolation

**The economy.** A synthetic world of 4 identical regions × 3 sectors. One
region, `R0`, is then cut out of world trade: every off-diagonal block of
$\mathbf{A}$ linking `R0` to anyone else is zeroed, in *both* directions —
$\mathbf{A}^{R0,s}$ (what R0 sells) and $\mathbf{A}^{r,R0}$ (what R0 buys). R0
keeps its own internal input–output structure. It simply trades with nobody.

**Why the answers are known in advance.** The transition shock travels through
the modified dual $\widetilde{\mathcal{L}}(\varphi) = (\mathbf{I}-\hat\varphi\mathbf{A}^{\!\top})^{-1}\hat\varphi$.
If $\mathbf{A}$ has no path between R0 and the rest, neither does any power of
it, and neither does the operator built from it. Nothing can travel either way —
and because the blocked entries are genuine structural zeros rather than small
numbers, the result should come out bitwise zero rather than merely close to it.

| Gate | What it does | A pass means | Result |
|---|---|---|--:|
| **A1** | Charge carbon to R0 only; measure every *other* region | R0's shock cannot leak **out** | `0.0e+00` |
| **A1b** | *Control*: same run, measure R0 itself | The shock was actually applied | `−0.2961 %` |
| **A2** | Charge everyone *except* R0; measure R0 | Others' shocks cannot leak **in** | `0.0e+00` |
| **A2b** | *Control*: same run, measure the others | The shock was actually applied | all `< 0` |
| **A3** | Compare isolated R0 inside the 4-region model against a standalone 1-region model | The generalisation reduces correctly | `0.0e+00` |
| **A4** | *Control*: same shock on the **untouched**, still-connected economy | Connected regions genuinely do transmit | `0.0491 %` |

### A1 and A2 are not the same test run twice

This is the part worth understanding, because at a glance they look redundant.
They exercise **different blocks of the matrix**.

Cost propagates through $\mathbf{A}^{\!\top}$, so the charge reaching an industry
$(s,j)$ from its suppliers is

$$\bigl[\mathbf{A}^{\!\top}\mathbf{ct}\bigr]_{(s,j)} \;=\; \sum_{(r,i)} A^{rs}_{ij}\,ct_{(r,i)} .$$

**A1** charges only R0, so the sum reduces to $\sum_i A^{R0,s}_{ij}\,ct_{(R0,i)}$
— it tests R0's **export** blocks. **A2** charges everyone but R0 and reads off
R0's own row, giving $\sum_{r\neq R0}\sum_i A^{r,R0}_{ij}\,ct_{(r,i)}$ — it tests
R0's **import** blocks. A bug that zeroed only one direction, or a transposition
that swapped the region indices, passes one and fails the other. Since a
one-directional leak produces entirely plausible-looking output, this is exactly
the class of error the suite exists to catch.

### What "stays put" means

Informally A2 is stated as "the isolated region stays put". Precisely: **R0's
value-added shock is identically zero.** Charging carbon to every other region on
earth leaves R0's GVA exactly where it was, as though nothing had happened
anywhere. The contrast with A2b makes it sharp — every other region moves, and
moves down; R0 alone is pinned at zero.

### Reading A1b against A4

These two numbers are the most informative pair in the group, and they say
something economic rather than merely computational. A1b is the shock a region
suffers from **its own** carbon price: `−0.2961 %`. A4 is the largest shock a
region suffers from **someone else's**: `0.0491 %`. A carbon charge therefore
lands about **six times harder at home than abroad** — the leakage result of
§3.2, reproduced on a made-up economy where it can be checked exactly.

---

## Group B — symmetry

**The economy.** 5 regions × 4 sectors, identical in every respect: technology,
carbon intensity, size, vulnerability, and trade shares, each region shipping the
same fraction to every partner. The same carbon price is applied everywhere.

**Why the answers are known in advance.** Identical inputs must give identical
outputs. Every region should receive the same shock, and since exchange rates are
*differences* between regions, every exchange-rate move should be zero. This is a
sharper test than it sounds: the expected answers are exact, so the tolerance can
be $10^{-15}$, and an asymmetry of $0.1\%$ — which nobody would spot by eye —
fails by twelve orders of magnitude.

| Gate | What it does | A pass means | Result |
|---|---|---|--:|
| **B1** | Uniform charge; spread of GVA shocks across the 5 regions | No region is treated differently from any other | `4.3e-18` |
| **B1b** | *Control*: the common shock is negative | A carbon charge costs value added | `−0.6298 %` |
| **B2** | Spot FX between every pair | Equal inflation ⇒ **exactly** zero spot move | `0.0e+00` |
| **B3** | 5-year forward points between every pair | Equal policy rates ⇒ zero forward points, to rounding | `9.8e-18` |
| **B4** | *Control*: the common shock is non-negligible | The operator is not silently degenerate | passes |

### Why B2 is exact and B3 is not

The two tolerances differ deliberately, and the reason is worth stating because
it looks like an inconsistency.

**B2 is bitwise zero.** Spot FX is a difference of cumulative inflation
deviations, each built by multiplying identical inputs through
$k\,[\mathrm{XCE}(t)-\mathrm{XCE}(t_0)]\,\chi_r$. Identical inputs through
identical operations produce bitwise identical floats, so the difference is
exactly `0.0`. Anything else would be a genuine defect.

**B3 is zero to rounding**, at `9.8e-18` absolute and `3.1e-15` relative to
$\Delta r$. Forward points descend from the GVA shock, which passes through a
$60\times60$ matrix inversion. Identical rows are solved independently by LAPACK
and agree only to machine precision, so the honest claim is "zero to rounding"
and the tolerance says so rather than pretending to more. Asserting exactness
here would produce a gate that fails on a different BLAS build.

The relative figure is the one to read. `9.8e-18` in isolation could mean the
rate shift itself was tiny; `3.1e-15` of $\Delta r$ says the cancellation is
complete to fifteen digits.

### Why B4 exists

B1 says all regions agree. That is satisfied trivially if the operator returns
zero for everyone. B4 demands the common shock be larger than $10^{-6}$ in
magnitude, so symmetry is a property of a live calculation and not of a dead one.

---

## Group C — one broken symmetry

**The economy.** The same 5 × 4 symmetric world, with exactly one thing changed.
C1–C5 charge carbon to `R2` alone; C6–C7 instead make `R3` twice as
carbon-intensive as everyone else and apply a uniform price.

**Why the answers are known in advance.** Asymmetry must appear where it was put
and nowhere else, with the right sign and the right ordering. This is the group
that distinguishes a model which is *consistent* from one which is *correct*: a
transposed block or a leak between regions survives groups A and B far more
easily than it survives C.

| Gate | What it does | A pass means | Result |
|---|---|---|--:|
| **C1** | Charge R2 only; check R2 is the minimum | The charged region is the worst hit | `−0.4139 %` |
| **C2** | Spread across the four *unshocked* regions | They are symmetric to the shock, so must be identical | `1.1e-19` |
| **C3** | Compare spillover against direct hit | Spillover is negative but strictly smaller | `−0.0540` vs `−0.4139 %` |
| **C4** | Forward points among unshocked pairs | Currencies with equal shocks do not move against each other | `3.0e-17` of the shocked pair |
| **C5** | Sign of R2's forward points | Matches $\operatorname{sign}(\Delta r_{R2}-\Delta r_{\mathrm{base}})$, as CIP requires | `−17.99 bp` → `−81.54 bp` |
| **C5b** | Magnitude of R2's forward points | Equals $B(5)\cdot\Delta r$ gap exactly | `< 1e-18` |
| **C6** | Make R3 carbon-intensive, price uniform; check R3 is the minimum | Intensity asymmetry lands on the intensive region | `−1.0437 %` |
| **C7** | Spread across the other four | Only the intensity was changed, so only R3 should differ | `4.3e-18` |
| **C8** | Double the carbon price, compare $2s(p)$ against $s(2p)$ | The charge channel is exactly linear | `0.0e+00` |
| **C9** | Shock R1, shock R4, shock both; compare sum against joint | Shocks superpose with no interaction term | `2.2e-19` |

### C5 pins a sign the rest of the suite cannot

C5 is the most important gate in the group, and the reason is that **groups A and
B are sign-blind**. They are built on quantities that must be zero, and zero has
no sign: a global sign flip in the spot channel leaves every zero at zero and
every magnitude unchanged. Mutation testing confirmed this directly — flipping
the sign of `fx.spot_ppp` passed every symmetry and invariance gate in the suite.

C5 closes the hole by asserting a *direction* on a case where the right answer is
unambiguous. R2 is hit hardest, so it takes the deepest rate cut, so under covered
interest parity its currency trades at a forward **premium**. With $S$ quoted in
units of $r$ per base, that means `pts < 0`: **the harder-hit economy strengthens
on the forward leg**. This is the counter-intuitive result the FX chapter
documents, and the gate asserts it as a *mechanism* —
$\operatorname{sign}(\text{pts}) = \operatorname{sign}(\Delta r_r - \Delta r_{\mathrm{base}})$
— rather than as an intuition someone might later "correct".

C5b then checks the magnitude against the closed form $B(5)\cdot\Delta r$ to
$10^{-18}$: `−17.99 bp` of rate gap becomes `−81.54 bp` of forward points, an
amplification of $4.53\times$, which is $B(5)$ at $a=0.04$. This is the tenor
amplification of §3.6 verified numerically.

### C3 is a magnitude gate, not an invariance gate

C3 asserts an *inequality* — spillover negative, and strictly smaller in absolute
value than the direct hit. It is the only ordering claim in the group that does
not reduce to a symmetry, and it encodes real economics: a carbon charge must
cost the region that pays it more than it costs anyone else. A model that
transmitted a shock more strongly abroad than at home would pass C1, C2 and C4
and fail here.

### C8 and C9 licence the results chapter

These two are not tests of correctness so much as of a property the reporting
depends on. **C8** establishes that the charge channel is exactly linear in the
carbon price, which is what allows a single matrix inversion to serve every
scenario, horizon and price path. **C9** establishes that shocks superpose with
no interaction term, which is what makes contribution decomposition *exact*
rather than an approximation from a particular ordering — the property the tariff
stack relies on when it attributes a combined result to four separate measures.

Both come out at or below `2.2e-19`, so the decomposition claims made downstream
are exact to machine precision rather than merely close.

---

## What groups A–C do not establish

Three limits are worth stating plainly, since they bound what a green run means.

**They say nothing about external accuracy.** Every economy in groups A–C is
synthetic and chosen so its answer is known by symmetry. A pass is evidence that
the shipped code has the structure it claims, not that its numbers describe the
world. There is no realised 2040 to test against, and there never will be in time
to matter.

**Symmetry is sign-blind.** As noted under C5, invariance gates cannot detect an
inverted channel. Group C supplies the only direction-pinning gates in these
three groups (C1, C3, C5, C6), and group F — not documented here — exists
entirely to close the remaining orientation and composition holes.

**A pass is conditional on the controls being live.** A1b, A2b, A4, B1b, B4 are
doing more work than their position in the list suggests. If any control were
silently broken, its paired invariance gate would keep passing and would mean
nothing at all.
