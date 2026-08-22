# Multi-regional BKMN model

A multi-regional extension of the **BKMN climate stress-testing framework**
(Berrahoui, Kenyon, Macrina and Nathanael, 2025 — *Simple climate stress
testing: an ensemble framework*). The original develops the framework for a
single economy; a single economy has no exchange rate, and a carbon price levied
in one country has nowhere to leak to. This repository extends the framework to
a system of thirteen regions built from the OECD inter-country input–output
tables, so that both become computable.

It takes the two outputs of policy-level climate models — a **temperature path**
and a **CO₂e price** — and runs them through a short chain of individually
auditable relations to produce value-added, macroeconomic and financial-market
stresses: inflation, policy rates, the yield curve, equity, credit, operational
risk and, the object of the extension, **exchange rates**.

---

## Quick start

```bash
pip install -r requirements.txt

py -3 -m bkmn.run_extensions      # full pipeline -> results/*.csv
py -3 tools/make_figures.py       # figures/*.png (reads results/, no re-run)
py -3 tests/test_validation.py    # 44 structural gates
```

The committed `results/` and `DATA_final/` mean nothing has to be rebuilt to
reproduce a figure or check a number.

## Layout

| | |
|---|---|
| `bkmn/` | the model — one module per channel, plus the two drivers `run_extensions.py` and `run_fx.py` |
| `DATA_final/` | the thirteen-region calibration: ICIO flows, Scope-1 emissions, carbon intensities, region maps |
| `data/` | upstream sources — NGFS scenarios, GHG footprints, ND-GAIN, World Bank macro, equity indices |
| `results/` | every output table, 117 CSVs, committed so results are reproducible without a re-run |
| `figures/` | 17 publication figures, all drawn from `results/` |
| `docs/` | method write-ups and the dissertation chapters |
| `tests/` | the gate suites |
| `tools/` | builders, downloaders, sweeps and the figure script |

## The chain

Each link is one published relation, and each can be checked on its own.

1. **Transition risk** — a carbon price becomes an ad-valorem cost on each
   sector's Scope-1 emissions and propagates through the multi-regional Leontief
   price dual, so a charge levied in one region reaches every other.
2. **Physical risk** — a temperature path becomes a global output loss through a
   quadratic damage function, allocated across region–industry pairs by
   vulnerability, conserving the global total exactly.
3. **Macro-financial transmission** — the resulting value-added shock drives
   inflation, a Taylor rule, the Hull–White term structure, and the market
   prices of equity, credit and operational-loss exposure.
4. **Foreign exchange** — the difference between two economies' yield-curve
   changes, separating into a spot leg under relative purchasing-power parity
   and a forward leg under covered interest parity. No new parameter enters.
5. **Tariffs** — a trade measure is the same object as a carbon charge placed on
   different blocks of the same matrix, so it needs no new machinery.

Scenario uncertainty is handled by treating the seven NGFS narratives as
components of a Dirichlet-categorical mixture rather than as competing
forecasts, with four priors carried so that conclusions depending on a view
about climate policy can be separated from those that do not.

## Validation

A climate stress test cannot be backtested — there is no realised 2040 — so the
model is checked structurally instead, on synthetic economies whose answers are
known in advance.

```bash
py -3 tests/test_validation.py       # 44 gates: isolation, symmetry, reduction, signs
py -3 tests/test_chapter_results.py  # 532 checks: every number quoted in the write-ups
py -3 tests/test_extensions.py       # 94 gates: mixture, tariffs, CBAM, stress band
py -3 tests/test_fx.py               # 9 gates: parities, triangular consistency
```

`docs/GATES.md` explains what each gate asserts and how to read its output;
`docs/CHAPTER_VALIDATION.md` sets out why this is the right form of test and
what it cannot establish. The suite is itself tested by mutation
(`tools/mutation_test.py`), which found that gates built on symmetry are
sign-blind — a model asserting the reverse of the economics passed all of them.

> On a non-UTF-8 console the suites can die on a minus sign in their output.
> Use `PYTHONIOENCODING=utf-8 py -3 tests/...`.

## Rebuilding from source

Not required for normal use. `tools/build_data_final.py` regenerates
`DATA_final/` from the raw ICIO and emissions files, `tools/build_aux_final.py`
the vulnerability and macro auxiliaries, and the `tools/download_*.py` scripts
fetch the upstream sources. These need the ingestion extras in
`requirements.txt`.

## Documentation

The method write-ups in `docs/` carry the derivations and the audit trail:
`CHAPTER_MRIO.md` for the input–output apparatus, `TRANSITION_METHOD.md` and
`CHAPTER_PHYSICAL.md` for the two shocks, `CHAPTER_MACRO_MARKETS.md` and
`CHAPTER_FX.md` for transmission, `CHAPTER_REGION_SELECTION.md` for how the
thirteen regions are derived rather than asserted, `TARIFF_METHOD.md` and
`TARIFF_CALIBRATION.md` for the trade extension, and `PAPER_AUDIT.md` for every
deviation from the single-region original with its justification.
`docs/REFERENCES.md` is the consolidated reference list.
