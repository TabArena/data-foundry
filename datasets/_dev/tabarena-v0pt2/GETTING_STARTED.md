# Getting started with dataset curation for TabArena v0.2

This guide gets a new curator from zero to a first contribution: what this folder is, how to set up Data Foundry,
where the curation notes live, and the two things you will do, **settling a candidate record** and **adding a
dataset**, with a list of candidates to pick from.

## 1. What this folder is

[TabArena](https://tabarena.ai/) benchmarks tabular ML on curated, real-world prediction tasks.
This folder is the working copy of its next version, **TabArena v0.2**: one folder per dataset, each a v2 definition
(`dataset.py`) built as a curated container. It started from the 142 datasets of
[BeyondArena](https://huggingface.co/datasets/TabArena/BeyondArena), re-curated and audited (130 remain), and new
datasets join it here. The datasets come from three split regimes: random (IID), **temporal** (predict the future)
and **grouped** (generalise to unseen entities such as patients or customers).

> [!TIP]
> **Large datasets are a priority.** Real tasks with roughly 1M–10M usable training rows are rare in public
> benchmarks, and most of them are non-IID. Candidates of that size carry the tag **`Review Prio 1 (Atlas)`** in
> the curation log (the tag comes from the earlier Atlas plan for a large-data collection, now folded into
> TabArena v0.2); pick from them first (section 7). A frame above 1.5M rows ships as a sub-sampled `<name>_1m`
> version, and each split trains on at most 1M rows.

The selection criteria (unique source, a real predictive task, no irreversible leakage, ethically unambiguous, not
trivial) are the same for every dataset; the [**📖 Guidelines**](https://tabarena.github.io/data-foundry/guidelines.html)
tab of the curation log is the reference.

The workflow, at a glance:

```
candidate record (curation log)  →  triage: accepted? which split? how large?
        →  v2 definition (dataset.py: raw download → curated container)
        →  dataset check + probes + /verify-dataset  →  PR review  →  a curator builds it (UUID)
```

## 2. Set up Data Foundry

Python 3.10+ and [`uv`](https://docs.astral.sh/uv/):

```bash
git clone https://github.com/TabArena/data-foundry.git
cd data-foundry
uv venv --seed && source .venv/bin/activate
uv pip install -e ".[dev,tests]"   # the dev extra adds the curation dependencies (openml, kaggle, …)
pytest -q                          # sanity check
```

Run the tools with the repository's environment, `.venv/bin/python -m data_foundry.curation.cli …`; a
`data-foundry-curation` on your PATH may be an older install.

The parts of the repository you will touch:

```
data-foundry/
├── curation/records/            # one markdown record per candidate dataset (the curation log)
├── datasets/_dev/tabarena-v0pt2/  # this folder: one v2 folder per dataset
├── datasets/_template/          # the template `dataset new` copies
├── .claude/skills/              # the Claude Code workflows (triage, check, add, verify, rebuild)
└── local-data-warehouse/        # gitignored: raw downloads and saved containers
```

More: [`datasets/README.md`](../../README.md) (the tree), [`CONTRIBUTING_DATASETS.md`](../../../CONTRIBUTING_DATASETS.md)
(the definition, step by step), [`AGENTS.md`](../../../AGENTS.md) (if you work with coding agents).

## 3. This folder

| File | What it holds |
|---|---|
| [`README.md`](README.md) | The table of datasets (regime, size, splits, UUID, open warnings) and how to rebuild them. |
| [`CHANGELOG.md`](CHANGELOG.md) | Every change to the folder, newest first. Add an entry with each PR. |
| [`TODO.md`](TODO.md) | Open decisions and later work. |
| [`LEAK_AUDIT.md`](LEAK_AUDIT.md) | The 2026 leak audit: removed and changed datasets, with severity. |
| [`TASK_PROBES.md`](TASK_PROBES.md) | The sweep against dummy baselines; flagged datasets wait for a decision. |
| [`BENCHMARK_CHANGES_TODO.md`](BENCHMARK_CHANGES_TODO.md) | What the TabArena harness has to change for these datasets. |

Each dataset folder holds `dataset.py` (the definition, the only file edited by hand), `explore.ipynb` (the
workbench: `ds = workbench()`) and `README.md` (generated: the dataset page with sample rows, checks, splits and the
build record).

## 4. The curation log

Every candidate has one markdown record under [`curation/records/`](../../../curation/records) (YAML front-matter
for the structured fields, free text in `## Comments`). The records are the memory of the curation effort: read a
record's comments before you work on its dataset.

The log is published read-only at [**tabarena.github.io/data-foundry**](https://tabarena.github.io/data-foundry/).
The large-data candidates:

> 🗂️ **[Large-data priority — filtered curation log](https://tabarena.github.io/data-foundry/#hf.tags=Review+Prio+1+%28Atlas%29)**
> — or, with the local dashboard running (section 5):
> [the same view locally](http://127.0.0.1:8765/#hf.tags=Review+Prio+1+%28Atlas%29)

Any filtered view can be shared like this: set the filters and click **🔗 Copy link** next to *✕ Clear filters*.

## 5. Workflow A: settling a candidate record

Settling a record means deciding its verdict: read the sources and comments, decide whether it belongs
(`suggestion`), flag issues (`decision_markers`), fill in the metadata (problem type, required split, …) and write
the reasoning into `## Comments`.

With Claude Code, open the repository and run `/triage-candidates`: it starts the local dashboard and loads the
curation guidelines, so Claude can research candidates, draft provisional verdicts (labelled `AI (UNVERIFIED)` for
you to verify) and answer "does this belong?" the way a curator would. For a cited second opinion on one record,
run `/check-candidate <unique_name>`.

Without Claude, start the dashboard yourself, a spreadsheet-like grid over the records whose edits rewrite the
markdown files in place:

```bash
.venv/bin/python -m data_foundry.curation.cli serve        # → http://127.0.0.1:8765
```

* Filter to the large-data candidates: the **tags** column filter → `Review Prio 1 (Atlas)`.
* Read the [**📖 Guidelines**](http://127.0.0.1:8765/guidelines.html) tab before your first triage: the selection
  criteria and the recurring decision patterns.
* The status column shows what a row needs: 🤖 AI-drafted (a human verifies it with the ✓ action), ⚠ untriaged,
  ★ accepted but not yet in Data Foundry. Each row links its record (📄) and, once curated, its definition (🧩).

When you are done: `.venv/bin/python -m data_foundry.curation.cli validate`, then commit the changed records and
open a PR (Claude prepares both on request, and never commits or pushes without your go-ahead).

## 6. Workflow B: adding a dataset

Once a record is accepted (`Yes`), the dataset needs a v2 definition: one `dataset.py` that turns the raw download
into a curated container (metadata → read → clean → dtypes → the regime → splits). The steps are in
[`CONTRIBUTING_DATASETS.md`](../../../CONTRIBUTING_DATASETS.md); the folder goes to
`datasets/_dev/tabarena-v0pt2/<unique_name>/`.

**The fast way:** in Claude Code, run `/add-dataset <unique_name>`. It reads the record, scaffolds the folder with
the metadata, BibTeX and regime pre-filled, and loops on `dataset check`; everything that needs a look at the data
is left as a `TODO(verify)` marker. From there you do the data science: download and load the raw data, clean it
(dtypes, missing values, identifiers, the target), read the check results in the generated README, decide and check
the split, and judge whether the result is a sound benchmark task. Then run the probes and `/verify-dataset
<unique_name>`, and open the PR; a curator builds the container after review.

**Learn from the datasets in this folder**, worked examples across the regimes:

| Example | Regime | Why it is a good read |
|---|---|---|
| [`blood_transfusion`](blood_transfusion/dataset.py) | IID | the smallest complete definition |
| [`mercari_price_suggestion`](mercari_price_suggestion/dataset.py) | IID | 1.48M rows taken in full, text features |
| [`delivery_eta_1m`](delivery_eta_1m/dataset.py) | temporal | 17M rows, sampled per test window into a `_1m` version |
| [`rossmann_store_sales`](rossmann_store_sales/dataset.py) | temporal | horizon from the source, a planning gap |
| [`amex_non_iid_1m`](amex_non_iid_1m/dataset.py) | grouped | one prediction per customer from all its statements (`last`, `all_rows`), sub-sampled by whole customers |
| [`electric_motor_temperature_prediction`](electric_motor_temperature_prediction/dataset.py) | grouped | sensor streams held out by measurement session |
| [`sat11_hand_algo_runtime`](sat11_hand_algo_runtime/dataset.py) | grouped | algorithm selection (`select_min`), censored runtimes |

## 7. Where to start: the large-data candidates

As of 2026-10-02; the [filtered log](https://tabarena.github.io/data-foundry/#hf.tags=Review+Prio+1+%28Atlas%29)
shows the current state. Rows are rough estimates from the records.

### 7.1 Records to settle (Workflow A)

| Record | State | Rows ≈ | What's needed |
|---|---|---:|---|
| [`usa_airport_dataset`](../../../curation/records/usa_airport_dataset.md) | `TBD -> Yes` | 3.5M | Define the task: flight records with no settled non-leaking target yet (forecast one of flights, seats, passengers). |
| [`wind_turbine_scada_data_for_early_fault_detection`](../../../curation/records/wind_turbine_scada_data_for_early_fault_detection.md) | `TBD -> 2nd Tier` | 4.7M | CARE-to-Compare SCADA: the per-turbine grouped / temporal setup and the real task are unclear. |
| [`yelp`](../../../curation/records/yelp.md) | `TBD -> 2nd Tier` | 7M | Probably no tabular task beyond entity matching or recommendation; confirm or reject. |

### 7.2 Accepted, waiting for a definition (Workflow B)

| Record | Rows ≈ | Task (one line) |
|---|---:|---|
| [`g_research_crypto_forecasting`](../../../curation/records/g_research_crypto_forecasting.md) | 24M | Crypto-returns regression, temporal + grouped; the split design needs care (anonymisation). |
| [`fraud_detection_in_electricity_and_gas_consumption`](../../../curation/records/fraud_detection_in_electricity_and_gas_consumption.md) | 4.5M invoices, 135K clients | STEG utility fraud, one label per client from the invoice history; grouped by client, check temporal. |
| [`huntprohibited`](../../../curation/records/huntprohibited.md) | 4M | Avito prohibited-content detection (binary, Russian text), much preprocessing. |
| [`numerai_v5_2`](../../../curation/records/numerai_v5_2.md) | 2.4M | Obfuscated stock-market regression, temporal split on `era`. |
| [`expresso_churn_prediction`](../../../curation/records/expresso_churn_prediction.md) | 2.15M | Zindi telecom churn; check IID against temporal. |
| [`pkdd_15_taxi_trip_time_prediction_ii`](../../../curation/records/pkdd_15_taxi_trip_time_prediction_ii.md) | 1.7M | Porto taxi trip time from partial GPS trajectories, temporal. |
| [`nyc_taxi_trip_duration`](../../../curation/records/nyc_taxi_trip_duration.md) | 1.46M | NYC trip-duration regression (Kaggle 2016), temporal. |
| [`force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition`](../../../curation/records/force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition.md) | 1.17M | Lithofacies multiclass from well logs, grouped by well. |
| [`rosbank1`](../../../curation/records/rosbank1.md) | 1M | Card-transaction churn and spending prediction, transaction level. |
| [`sasol_customer_retention_recruitment_competition`](../../../curation/records/sasol_customer_retention_recruitment_competition.md) | multi-M | 90-day customer inactivity (~1.5M clients); read the licence notes in the record first. |
| [`alfa_battle_2_0_task_1`](../../../curation/records/alfa_battle_2_0_task_1.md) | multi-M | Next-action prediction from 270 days of mobile-banking event logs. |
| [`alfa_battle_2_0_task_2`](../../../curation/records/alfa_battle_2_0_task_2.md) | multi-M | Credit-default prediction (binary), temporal train/test. |
| [`zillow_prize`](../../../curation/records/zillow_prize.md) | 90K labelled | Home-value error (`logerror`) regression; only ~90K labelled rows, so below the large-data bar. |

Pick one, tell the team you are on it (claims are marked in the record's `data_foundry_status`: `WIP (Triage)` or
`WIP (DF)`), and go. The record's comments, the Guidelines tab and the definitions in this folder answer most
questions; for the rest, ask the team (Lennart).
