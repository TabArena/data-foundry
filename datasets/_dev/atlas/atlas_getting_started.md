# [Atlas] Getting Started with Dataset Curation

Welcome! This guide gets you from zero to your first curated Atlas dataset: what
Atlas is, how to set up Data Foundry, where the curation notes live, and the two
workflows you will actually do — **curating a dataset record** and **adding a new
dataset to Data Foundry** — each with a list of getting-started datasets to pick from.

---

## 1. Goal & scope: what is Atlas?

**Atlas** is a new benchmark we are building: a curated collection of **large-scale, real-world tabular ML
tasks with roughly 1M–10M usable training samples**. It is the next step after
[TabArena](https://tabarena.ai/) and
[BeyondArena](https://huggingface.co/datasets/TabArena/BeyondArena), and like them it
is built on Data Foundry.

We look for **real-world predictive
tasks** (classification or regression) at the 1M–10M-row scale, with a defensible
train–test protocol — random (IID), **temporal** (predict the future), or **grouped**
(generalize to unseen entities). Most datasets at this scale are non-IID. The general selection criteria (unique
source, real predictive task, no irreversible leakage, ethically unambiguous, not
trivial) are the same as for TabArena/BeyondArena — the curation dashboard's
[**📖 Guidelines**](https://tabarena.github.io/data-foundry/guidelines.html) tab is
the authoritative reference.

Current state:

* **11 seed datasets** (inherited from BeyondArena, most subsampled to 1M rows there)
  already have curation notebooks in this folder (`datasets/_dev/atlas/`).
* A **candidate backlog** of new datasets is tracked in the curation log, tagged
  **`Review Prio 1 (Atlas)`** — see [section 3](#3-the-curation-log--reading-the-atlas-notes).
* A temporary size/viability tracker lives at
  [`_tmp_dataset_sizes.md`](_tmp_dataset_sizes.md).

The workflow, at a glance:

```
candidate record (curation log)  →  triage / verify (accepted? split? size?)
        →  curation notebook (raw download → CuratedContainer)
        →  PR review  →  promoted & pinned into the Atlas collection
```

## 2. Install & set up Data Foundry

Requires Python 3.10+; [`uv`](https://docs.astral.sh/uv/) recommended.

```bash
git clone https://github.com/TabArena/data-foundry.git
cd data-foundry
uv venv --seed && source .venv/bin/activate
uv pip install -e ".[dev,tests]"   # dev extra = curation deps (openml, kaggle, …)
pytest -q                          # sanity check the install
```

TL;DR of the repo structure:

```
data-foundry/
├── src/data_foundry/       # the package — schema, CuratedContainer, collections API,
│                           #   dataset checks, split helpers, curation-log toolkit
├── curation/               # the curation log (git-tracked data):
│   ├── records/            #   one markdown record per candidate dataset
│   └── vocabularies.yaml   #   the dropdown options for record fields
├── datasets/               # curation notebooks
│   ├── _template/          #   canonical notebook skeleton (copy this)
│   ├── _dev/               #   new work lands here — Atlas lives in _dev/atlas/
│   └── beyond_iid/         #   released datasets, pinned by (name, uuid)
├── examples/               # runnable demos of the whole API
└── local-data-warehouse/   # gitignored — raw downloads + saved containers
```

Deeper dives: [`README.md`](../../../README.md) (API + use cases),
[`CONTRIBUTING_DATASETS.md`](../../../CONTRIBUTING_DATASETS.md) (the notebook
pipeline, field by field), [`AGENTS.md`](../../../AGENTS.md) (if you work with
coding agents).

## 3. The curation log — reading the Atlas notes

Every candidate dataset has **one markdown record** under
[`curation/records/`](../../../curation/records) (YAML front-matter for the
structured fields + free-text `## Comments`). The records are the collective memory
of the curation effort.

The log is published read-only at
[**tabarena.github.io/data-foundry**](https://tabarena.github.io/data-foundry/).
For an intro to the Atlas notes, open the **Atlas-filtered view**:

> 🗂️ **[Atlas candidates — filtered curation log](https://tabarena.github.io/data-foundry/#hf.tags=Review+Prio+1+%28Atlas%29)**
> — or, with the local dashboard running ([section 4](#4-workflow-a-curating-a-dataset-record)):
> [the same view locally](http://127.0.0.1:8765/#hf.tags=Review+Prio+1+%28Atlas%29)

(Any filtered view can be shared like this — set your filters and click the
**🔗 Copy link** button next to *✕ Clear filters*.)

## 4. Workflow A: curating a dataset record

"Curating a record" means settling a candidate's verdict: read the sources and
comments, decide whether it belongs in Atlas (`suggestion`), flag issues
(`decision_markers`), fill in the metadata (problem type, required split, …), and
write your reasoning into `## Comments`.

The recommended way to work is Claude-assisted: open Claude Code in the repo and run

```
/triage-candidates
```

The command ([`.claude/commands/triage-candidates.md`](../../../.claude/commands/triage-candidates.md))
starts the local dashboard for you **and** loads the curation guidelines into
context — so Claude can research candidates, draft provisional triages (honestly
labelled `AI (UNVERIFIED)` for you to verify), and answer "does this belong in
Atlas?" the way a curator would.

As the backup (or if you prefer working without Claude), start the dashboard
yourself — a Sheets-like grid over the records; edits rewrite the markdown files
in place, so your `git diff` is exactly what you changed:

```bash
data-foundry-curation serve        # → http://127.0.0.1:8765
# equivalently: python -m data_foundry.curation.cli serve
```

Either way, in the dashboard:

* Filter to Atlas: use the **tags** column filter → `Review Prio 1 (Atlas)`, or open
  [the local Atlas view](http://127.0.0.1:8765/#hf.tags=Review+Prio+1+%28Atlas%29) directly.
* Read the [**📖 Guidelines**](http://127.0.0.1:8765/guidelines.html) tab once before
  your first triage — it defines the selection criteria and the recurring decision
  patterns (same content as the [public copy](https://tabarena.github.io/data-foundry/guidelines.html)).
* Click a cell to edit; the leftmost status column shows what each row needs
  (🤖 = AI-drafted, a human must verify — use the ✓ action on the row; ⚠ = untriaged;
  ★ = accepted but not yet in Data Foundry).
* Every row links its record file (📄) and, once curated, its notebook (📓).

When done, ask Claude to wrap up: it validates the records, sanity-checks the
diff, and prepares the commit and PR (it won't commit or push without your
explicit go-ahead). As the backup, do it yourself: `data-foundry-curation validate`,
then commit the changed records and open a PR. (Records are plain markdown — you
can also skip the dashboard and edit `curation/records/<unique_name>.md` by hand,
keeping the YAML front-matter valid.)

## 5. Workflow B: adding a new dataset to Data Foundry

Once a record is **accepted**, the dataset needs a **curation notebook** that turns
the raw download into a reproducible `CuratedContainer`: metadata → load & clean →
sanity checks → outer CV splits → save (with uuid + checksum). The five steps are
documented in [`CONTRIBUTING_DATASETS.md`](../../../CONTRIBUTING_DATASETS.md); the
skeleton to copy is [`datasets/_template/_template.ipynb`](../../_template/_template.ipynb),
and for Atlas the notebook goes to `datasets/_dev/atlas/<unique_name>/<unique_name>.ipynb`.

**The fast way:** inside Claude Code, run the **`/process-dataset`** slash command
([`.claude/commands/process-dataset.md`](../../../.claude/commands/process-dataset.md)) and
**link the dataset's curation record from the prior step**
(`curation/records/<unique_name>.md`) as the metadata source — it scaffolds the
notebook with the metadata, BibTeX, and the right split helper pre-filled, and the
record's comments carry the curation decisions (target, split, caveats) the
notebook must implement. The scaffold is just the start, though: from there you
step in and do the actual data science by hand — download and load the raw data,
clean it (dtypes, missing values, IDs, target), inspect the check outputs, design
and verify the splits, and judge whether the result is a sound benchmark task.

**Learn from the seed datasets** — the 11 Atlas notebooks in this folder are worked
examples across all three split regimes:

| Example | Regime | Why it is a good read |
|---|---|---|
| [`delivery_eta`](delivery_eta/delivery_eta.ipynb) | temporal | large temporal task (~17M rows), time-index handling |
| [`amex_non_iid`](amex_non_iid/amex_non_iid.ipynb) | grouped | grouped split on customers, multi-file raw data |
| [`electric_motor_temperature_prediction`](electric_motor_temperature_prediction/electric_motor_temperature_prediction.ipynb) | grouped | sensor streams, per-session groups, warm-up handling |
| [`mercari_price_suggestion`](mercari_price_suggestion/mercari_price_suggestion.ipynb) | IID | large IID task with text-ish features |

Atlas-specific conventions: target **1M–10M usable rows** (subsample defensibly if
larger), and follow the processing conventions from the Guidelines (drop
uninformative IDs, explicit NAs, shuffle IID/grouped data, sort temporal data,
verify no feature leaks the future at prediction time).

## 6. Getting-started datasets

### 6.1 Records to triage & verify (Workflow A)

Six Atlas candidates whose records still need a curator — verify the AI-drafted
ones, settle the open verdicts, and pin down target/split/size against the
1M–10M bar:

| Record | Current state | What's needed |
|---|---|---|
| [`nyc_taxi_trip_duration`](../../../curation/records/nyc_taxi_trip_duration.md) | `TBD -> Yes`, 🤖 AI-drafted | Verify: temporal trip-duration regression (Kaggle 2016, ~1.46M rows); confirm task & split. |
| [`expresso_churn_prediction`](../../../curation/records/expresso_churn_prediction.md) | `TBD -> Yes`, 🤖 AI-drafted | Verify: Zindi telecom churn (~2.15M rows); check IID vs temporal split. |
| [`molecularproperties`](../../../curation/records/molecularproperties.md) | `TBD -> 2nd Tier` | Decide: CHAMPS scalar coupling (Kaggle) — is there a genuinely tabular task without expert feature engineering? |
| [`open_soil_data`](../../../curation/records/open_soil_data.md) | `TBD -> Yes` | Investigate: iSDA Africa soil nutrients, multi-element regression, temporal; confirm target choice & usable size. |
| [`usa_airport_dataset`](../../../curation/records/usa_airport_dataset.md) | `TBD -> Yes` | Define the task: ~3.5M flight records but no settled non-leaking target yet. |
| [`wind_turbine_scada_data_for_early_fault_detection`](../../../curation/records/wind_turbine_scada_data_for_early_fault_detection.md) | `TBD -> 2nd Tier` | Investigate: CARE-to-Compare SCADA (~4.7M rows); per-turbine grouped/temporal setup and real task unclear. |

### 6.2 Accepted datasets that need a curation notebook (Workflow B)

All Atlas candidates currently **accepted (`Yes`) but not yet in Data Foundry** —
each needs the Workflow B notebook treatment:

| Record | Task (one line) |
|---|---|
| [`alfa_battle_2_0_task_1`](../../../curation/records/alfa_battle_2_0_task_1.md) | Next-action prediction from 270 days of mobile-banking event logs. |
| [`alfa_battle_2_0_task_2`](../../../curation/records/alfa_battle_2_0_task_2.md) | Credit-default prediction (binary), temporal train/test. |
| [`force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition`](../../../curation/records/force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition.md) | Lithofacies multiclass from well logs (~1.17M rows), grouped by well. |
| [`g_research_crypto_forecasting`](../../../curation/records/g_research_crypto_forecasting.md) | Crypto-returns regression (~24M rows), temporal + grouped — split design needs care. |
| [`huntprohibited`](../../../curation/records/huntprohibited.md) | Avito prohibited-content detection (binary, Russian-text-heavy, ~4M rows). |
| [`numerai_v5_2`](../../../curation/records/numerai_v5_2.md) | Obfuscated stock-market regression (~2.4M rows), temporal split on `era`. |
| [`rosbank1`](../../../curation/records/rosbank1.md) | Card-transaction churn + spending-volume prediction. |
| [`sasol_customer_retention_recruitment_competition`](../../../curation/records/sasol_customer_retention_recruitment_competition.md) | 90-day customer-inactivity probability (~1.5M clients) — **check the restrictive license first**. |
| [`zillow_prize`](../../../curation/records/zillow_prize.md) | Home-value error (`logerror`) regression, temporal horizons — pick one reproducible target. |

Pick one, claim it by letting the team know, and off you go. When in doubt at any
step, the record's comments, the Guidelines tab, and the seed notebooks in this
folder answer most questions — for everything else, including questions on how to
use any of this, reach out to the team / Lennart.
