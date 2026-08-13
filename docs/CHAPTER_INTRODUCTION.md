# Abstract

A climate stress test has to join a scenario measured in decades to market prices
quoted daily. The framework of Berrahoui, Kenyon, Macrina and Nathanael (2025)
makes that join through a short chain of individually auditable relations running
from a carbon price and a temperature path to inflation, interest rates, equity
and credit. It does so for a single economy, and a single economy has no exchange
rate.

This dissertation extends the framework to a system of thirteen regions built
from the 2022 OECD inter-country input–output tables. A carbon charge levied in
one region then propagates to every other through the Leontief price dual, so
cross-border leakage is measured rather than assumed, and the exchange rate
becomes derivable as the difference between two economies' yield-curve changes —
separating into a spot leg governed by relative purchasing-power parity and a
forward leg governed by covered interest parity. The seven NGFS narratives are
treated not as competing forecasts but as components of a Dirichlet-categorical
mixture, over which four priors are carried.

The organising empirical finding is that transition risk is a policy choice while
physical risk, at this horizon, is not: the mean transition cost varies by a
factor of thirty-seven across the narratives against eight per cent for physical
damage. That asymmetry separates the financial channels which cannot be reported
without a view on climate policy from those which can.

**Keywords:** climate stress testing; multi-regional input–output analysis;
foreign exchange; covered interest parity; NGFS scenarios; Dirichlet-categorical
mixture; carbon pricing.

---

# 1 Introduction

Bank regulators have spent the better part of a decade asking a question the
financial industry is not well equipped to answer: what does climate change do to
the value of what you hold? The exercises that have addressed it at scale —
the European Central Bank's climate risk stress test (ECB, 2022) and the Bank of
England's Climate Biennial Exploratory Scenario (Bank of England, 2022) — reach
their answers through large macro-financial models whose internal workings are
not, in general, reproducible by the institutions being tested. Their outputs are
credible; their mechanisms are opaque. An institution asked to hold capital
against a number it cannot reconstruct is in an uncomfortable position, and one
asked to *manage* a risk it cannot decompose is in a worse one, since it has no
way of knowing which of its exposures the number is about.

Berrahoui, Kenyon, Macrina and Nathanael (2025) — hereafter BKMN — take the
opposite approach, and it is their framework that this dissertation extends. They
propose an *ensemble*: a short chain of relations, each simple enough to be
checked on its own, running from a climate scenario to a set of market shocks. A
carbon price becomes a cost on each sector in proportion to its emissions
intensity; an input–output description of the economy propagates that cost to
every other sector; a temperature path becomes a loss of output allocated across
sectors by vulnerability; the resulting change in value added drives inflation,
and inflation drives the policy rate, the yield curve, equity indices and credit
spreads in turn. Two of the links are stated as propositions with proofs. Every
relation is visible and can therefore be disagreed with individually, which is
the property a regulated institution needs and a black box cannot offer.

The framework is developed for one economy and calibrated on the United Kingdom.
That is a coherent choice for a first exposition, but it forces an assumption
that is plainly false and forecloses a question that matters. The false
assumption is that a carbon price levied in one country stays there. Production
is international: a charge on Chinese steel is paid, in part, by whoever buys
goods made with Chinese steel, and a single-region model cannot see that leakage,
because it has nowhere for the cost to leak to. The foreclosed question is the
exchange rate. An exchange rate is a *relative* price — the value of one economy
expressed in terms of another — and it is not merely hard to compute in a
one-country model but undefined in it. BKMN say as much themselves, observing
that while their model "does not provide stressed FX, it could be expanded to
include multiple economies, enabling such calculations via the difference in the
changes of yield curves." That sentence is the specification this dissertation
implements.

The objective is therefore to build a multi-regional version of the BKMN model
that produces climate-attributable exchange-rate moves alongside the
interest-rate and inflation shifts the original already produces, taking
published regional projections of carbon prices and temperature as its inputs.
Three requirements shape the construction. The world must be resolved into a
manageable number of regions, and that choice must be argued for rather than
asserted, since within an aggregate every member necessarily shares one carbon
price, one carbon intensity and one currency — so the relevant question is not
which economies are largest but which, if left inside a block, would cause that
block to misrepresent them. The sectoral input–output model must be replaced by
an international one, in the sense of Miller and Blair (2022), in which the flow
matrix is blocked by region and the off-diagonal blocks are trade. And the
exchange-rate result must fall out of machinery the model already contains rather
than being bolted on as a separate behavioural equation, since a currency model
estimated independently of the rest of the chain would sacrifice exactly the
auditability that motivates the framework.

Three contributions follow. The first is the extension itself: a thirteen-region
calibration on the OECD tables, with the region set derived from a stated linkage
rule, on which a carbon charge propagates across borders and the exchange rate is
obtained as a pure recombination of the inflation and interest-rate channels,
introducing no new parameter. The second is the treatment of scenario
uncertainty. NGFS publishes seven narratives and no probabilities over them, and
reporting results under one silently assigns it probability one; treating the
narrative as a categorical draw with a Dirichlet prior makes every reported
quantity an expectation, and carrying four priors makes it possible to say which
conclusions depend on a view about climate policy and which do not. The third is
a set of results the single-region setting cannot produce, of which the clearest
is that "climate exposure" is not one quantity: ranking regions by exchange rate,
policy rate, credit spread and equity gives four different answers from the same
two underlying shocks. A stretch objective is pursued at the end, since a tariff
and a carbon charge are the same mathematical object placed on different blocks
of the input–output matrix, and pricing trade measures therefore requires no new
machinery.

The remainder of the dissertation is organised as follows. Chapter 2 surveys the
two literatures this work sits between and identifies the gap it occupies.
Chapter 3 develops the model: the stress-testing frame, the multi-regional
input–output apparatus, the transition and physical channels, the
macro-financial transmission, the exchange-rate derivation and the tariff
extension. Chapter 4 turns to the numerical example — data and calibration, the
derivation of the region set, the scenario mixture, validation, results, and the
tariff stack. Chapter 5 separates the model's assumptions from what those
assumptions cost, and concludes. Three appendices carry the mathematics that
would otherwise interrupt the argument: the existence and convergence of the
Leontief inverse, and the proofs of the two propositions inherited from BKMN.
