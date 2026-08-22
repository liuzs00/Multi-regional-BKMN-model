# Abstract

A climate stress test has to join a scenario measured in decades to market prices
quoted daily. The framework of Berrahoui, Kenyon, Macrina and Nathanael (2025)
makes that join through a short chain of auditable relations running from a
carbon price and a temperature path to inflation, interest rates, equity and
credit — but does so for a single economy, and a single economy has no exchange
rate. This dissertation asks how far a carbon price levied in one region reaches
the output, rates and currency of another, and whether the exchange-rate response
can be derived from machinery the framework already contains rather than
estimated beside it.

The framework is extended to thirteen regions built from the 2022 OECD
inter-country input–output tables. A carbon charge levied in one region
propagates to every other through the Leontief price dual, so leakage is measured
rather than assumed, and the exchange rate follows as the difference between two
economies' yield-curve changes — a spot leg under relative purchasing-power
parity and a forward leg under covered interest parity. The seven NGFS narratives
are treated not as competing forecasts but as components of a
Dirichlet-categorical mixture, over which four priors are carried.

The main finding is that transition risk is a policy choice while physical risk,
at this horizon, is not. The mean transition cost varies by a factor of
thirty-seven across the seven narratives; physical damage varies by eight per
cent. That asymmetry divides the financial channels into those which cannot be
reported without a view on climate policy and those which can. Three further
results follow that a single-region model cannot produce. Currency appreciation
is a symptom of harm rather than of resilience. Ranking regions by exchange rate,
policy rate, credit spread and equity gives four different answers from the same
two shocks. And a pegged economy carries a wedge of some twenty-five basis points
between the policy rate its own damage calls for and the one its anchor delivers.

**Keywords:** climate stress testing; multi-regional input–output analysis;
foreign exchange; covered interest parity; NGFS scenarios; Dirichlet-categorical
mixture; carbon pricing.

---

# 1 Introduction

Bank regulators have spent the better part of a decade asking a question the
financial industry is not well equipped to answer: what does climate change do to
the value of what you hold? The exercises that have addressed it at scale answer
through large macro-financial models whose workings are not, in general,
reproducible by the institutions being tested. The framework this dissertation
extends takes the opposite approach: Berrahoui, Kenyon, Macrina and Nathanael
(2025) — hereafter BKMN — propose an *ensemble*, a short chain of individually
auditable relations running from a carbon price and a temperature path to
inflation, interest rates, equity and credit. Every relation is visible and can
therefore be disagreed with individually, which is the property a regulated
institution needs and a black box cannot offer. Chapter 2 places both approaches
in their literatures.

BKMN develop the framework for a single economy, and that forecloses two things.
A carbon price levied in one country does not stay there — a charge on Chinese
steel is paid in part by whoever buys goods made with Chinese steel — but a
one-country model has nowhere for the cost to leak to. And an exchange rate is a
*relative* price, not merely hard to compute in such a model but undefined in it.
BKMN say as much themselves, noting that their model could be expanded to include
multiple economies, "enabling such calculations via the difference in the changes
of yield curves". This dissertation implements that specification, and the
question it poses is how far a carbon price levied in one region reaches the
output, rates and currency of another, and whether the exchange-rate response can
be derived from machinery the framework already contains rather than estimated
beside it.

Three requirements shape the construction. The world must be resolved into a
manageable number of regions, and that choice argued for rather than asserted,
since within an aggregate every member shares one carbon price, one carbon
intensity and one currency — so the question is not which economies are largest
but which, left inside a block, would cause that block to misrepresent them. The
input–output model must be international in the sense of Miller and Blair (2022),
the flow matrix blocked by region with trade in the off-diagonal blocks. And the
exchange rate must fall out of machinery the model already contains rather than
being bolted on, since a currency model estimated independently of the rest of
the chain would sacrifice exactly the auditability that motivates the framework.

Three contributions follow. The first is the extension itself: a thirteen-region
calibration on the 2022 OECD inter-country tables, with the region set derived
from a stated linkage rule, on which a carbon charge propagates across borders
and the exchange rate is obtained as a pure recombination of the inflation and
interest-rate channels, introducing no new parameter. The second is the treatment
of scenario uncertainty. NGFS publishes seven narratives and no probabilities
over them, and reporting results under one silently assigns it probability one;
treating the narrative as a categorical draw under a Dirichlet prior makes every
reported quantity an expectation, and carrying four priors makes it possible to
say which conclusions depend on a view about climate policy and which do not. The
third is a stretch objective pursued at the end, since a tariff and a carbon
charge are the same mathematical object placed on different blocks of the
input–output matrix, and pricing trade measures therefore requires no new
machinery.

The results divide along one line. Transition risk is a policy choice and
physical risk, at this horizon, is not: the mean transition cost varies by a
factor of thirty-seven across the seven narratives while physical damage varies
by eight per cent, because warming to 2040 is largely determined by emissions
already made. That asymmetry propagates into the financial channels and sorts
them — the spot exchange rate ranges over a factor of 22.7 across the four
priors, the policy rate over 1.04 — so an institution exposed through interest
rates can use these numbers without holding a view on climate policy, while one
exposed through carbon-intensive credit cannot and should quote a range.

Three findings then emerge that the single-region setting cannot produce.
Appreciation turns out to be a symptom of harm rather than of resilience: the
rupee's five-year forward moves −1.35 per cent against the euro at 2040 while
sterling moves +0.35, and the ordering tracks damage rather than strength.
Ranking regions by exchange rate, policy rate, credit spread and equity gives
four different answers from the same two underlying shocks, so that "climate
exposure" is not one quantity — China is first on credit and last on equity on an
identical value-added shock, because its sectoral composition is what the credit
channel punishes while its market beta is the lowest in the set. And a
dollar-pegged economy carries a wedge of some twenty-five basis points between
the policy rate its own damage calls for and the one its anchor delivers: the
climate component of the peg's cost, priced with nothing beyond machinery the
rate channel already contained.

The remainder is organised as follows. Chapter 2 surveys the two literatures this
work sits between and identifies the gap it occupies. Chapter 3 develops the
model: the stress-testing frame, the multi-regional input–output apparatus, the
transition and physical channels, the macro-financial transmission, the
exchange-rate derivation and the tariff extension. Chapter 4 turns to the
numerical example — data and calibration, the derivation of the region set, the
scenario mixture, validation, results, and the tariff stack. Chapter 5 separates
the model's assumptions from what those assumptions cost, and concludes. Three
appendices carry the mathematics that would otherwise interrupt the argument: the
existence and convergence of the Leontief inverse, and the proofs of the two
propositions inherited from BKMN.
