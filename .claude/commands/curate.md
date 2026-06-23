Start the local curation dashboard and help the user triage / curate the dataset
backlog. Invoking this skill loads the **curation guidelines** (below) into context
so you can advise on selection and processing decisions the way a human curator would.

## When to invoke

* The user wants to **open the curation dashboard** / work on the dataset backlog.
* The user asks whether a dataset **belongs in the benchmark**, what split it needs,
  or how to **process** it — answer using the guidelines below.
* The user wants to **add, edit, or triage** a candidate dataset record.

If the user instead wants to scaffold a *curation notebook* for an already-decided
dataset, use `/new-dataset`.

## Step 1 — Start the dashboard

Run the server in the background, then point the user at the URL:

```bash
data-foundry-curation serve            # → http://127.0.0.1:8765
# (equivalently: python -m data_foundry.curation.cli serve)
```

Tell the user to open **http://127.0.0.1:8765** and hard-refresh. The dashboard
edits the markdown records in place; the **📖 Guidelines** button opens the same
guidelines summarized below.

## How the backlog is stored

* The source of truth is **one markdown file per dataset** at
  `curation/records/<unique_name>.md`: YAML **front-matter** for the structured /
  dropdown fields, plus a body with `## Comments` and `## Reference`.
* **Add / triage a dataset** = create or edit its `.md` record — by hand, with you
  (the agent), or in the dashboard. Keep the front-matter valid YAML; empty fields
  are simply omitted.
* The per-record schema is `CurationRecord` in
  [`src/data_foundry/curation/record.py`](../../src/data_foundry/curation/record.py)
  (fields: `unique_name`, `name`, `checked_by`, `data_foundry_status`, `suggestion`,
  `decision_markers`, `tags`, `collections`, `original_source`, `year`, `domain`,
  `required_split`, `problem_type`, `original_data_state`, `source_links`,
  `comments`, `reference`, `needs_review`).
* Editable dropdown options live in `curation/vocabularies.yaml` (add new options
  there, via the dashboard's ＋ header buttons, or with `save_vocabularies`).
* After editing records, sanity-check with `data-foundry-curation validate`.

## Curation guidelines — read before advising

These tell you *how to assist*: how we decide whether a dataset belongs in TabArena
and how we curate the ones we keep. The full rendered version is the dashboard's
**Guidelines** tab (`src/data_foundry/curation/static/guidelines.html`).

### Background: IID vs non-IID

Whether a dataset is IID or non-IID is decided by the **appropriate train–test split**
— the split that most closely mirrors the original real-world application.

* **IID** — test samples follow no particular structure; a random hold-out is right.
* **Non-IID** — the application requires a temporal or grouped split:
  * **Temporal** — a time index exists; test samples occur strictly *after* training
    (predicting the future, e.g. future transactions).
  * **Grouped** — a group index exists; all samples of a group stay together so no
    group appears in both train and test (generalize to unseen entities). Either
    *label-per-group* (one shared label per group) or *label-per-sample*.
* A temporal split doesn't remove group structure and vice-versa — the split only
  decides which dependency matters. **Time-series forecasting is excluded** (different
  assumptions / validation); distinguish temporal tabular regression from forecasting.

### Dataset selection criteria (a dataset must satisfy all)

1. **Unique** — unique original data source (re-uploads under new names are common;
   first determine the original source / whether it's an original contribution).
2. **IID or non-IID tabular task** — a random, temporal, or grouped split is the
   appropriate validation protocol.
3. **Published for a predictive task** — explicitly a classification/regression task.
   Exclude scientific-discovery (survey / non-predictive) tables, click-through-rate,
   and ranking / information-retrieval (recommender) tasks.
4. **Representative of a real tabular-ML application** — exclude datasets that are:
   (A) from a non-tabular modality where modality-specific models are clearly superior
   (judged per-dataset; vectorized image/text/audio/time-series is OK if tabular models
   are competitive); (B) not from a real random distribution (artificial / deterministic;
   also exclude simulated-physics data that has dedicated benchmarks); (C) trivial (all
   untuned models reach the same better-than-random score, or solve it perfectly);
   (D) have irreversible data-quality issues that leak the target / test distribution
   (e.g. PCA-transformed); (E) lack enough information to make an informed decision.
5. **Ethically unambiguous** — exclude tasks with ethical concerns, including data whose
   subjects/creators ask that it not be used for ML.

Curation is **manual and human-verified**; criteria involve subjective judgment, so
record the reasoning in the record's `## Comments` and the `decision_markers`.

### Dataset processing conventions

* **Identifiers** — drop uninformative sample IDs; keep informative ones (e.g. a time
  index) and process them to their real meaning.
* **Missing values** — convert proxy missing values (e.g. `999`, `-1`) to explicit `NA`
  when reliably inferable.
* **Targets** — consider log-scaling skewed/heavy-tailed numeric targets (e.g. prices).
* **Naming** — `snake_case` dataset names.
* **Order** — shuffle IID and grouped data (avoid order leakage); sort temporal data by
  the time index.
* **Dtypes** — object/string → categorical (fixed finite set) or string; dates →
  `YYYY-MM-DD`; everything else numeric.
* **Temporal tasks/splits** — manually set the prediction horizon and test time points;
  verify every feature was available at prediction time (no future leakage); watch for
  grouped-temporal structure; the first split uses the most recent test point (most
  training data, most representative), then descending.

## Dashboard features to mention

* Leftmost **status** cell encodes priority (⚡ disagreement = purple, ✓ in Data Foundry
  = green, ✗ suggestion No = red, ★ accepted-not-yet-in-DF = blue, ⚠ needs review =
  orange, • other = yellow). Click its header **▾** to filter by status.
* Top **pills** (Data Foundry / Review needed / Disagreement) are exclusive filters
  (clicking one resets the others). The **search** box always spans all datasets.
* **📌 pin** (far-left column) keeps a row visible through any filter and sticks it to
  the top while scrolling.
* Dropdown columns show a **▾** on hover and a **＋** in the header to add a new option;
  the **Optional Tags** column opens a panel for the less-common fields.

## Notes

* The dashboard runs locally per curator (edit → `git` commit → PR). It is not hardened
  for multi-user or public exposure.
* `data-foundry-curation build-site <out>` produces a read-only static copy (e.g. for
  GitHub Pages); `export` writes a flat CSV/Parquet/XLSX snapshot or pushes to a Sheet.
