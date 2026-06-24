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
* **The `data_foundry_status` field is a merged multi-tag field** ("Data Foundry" column):
  it holds the *integration state* (`DF: Yes`, `DF: WIP`, `DF: Much work`, `DF: Suspended`)
  **and** *benchmark-collection membership* (`TabArena (v0.1)`, `BeyondArena`). Every dataset
  shipped in a collection (`datasets/_maintenance/_old_collections/tabarena-v0pt1`,
  `datasets/beyond_iid`) carries its collection tag(s) **plus `DF: Yes`**; there are 51
  TabArena and 142 BeyondArena (union 144). The `collections` field is now only for *external*
  benchmarks/collections (TabSTAR, TabRed, CARTE/TARTE, …), not our own.
* **`DF: Yes` (or any `DF: …`) with NO collection tag is a valid, intentional state**: the dataset
  is in Data Foundry but **not in a shipped collection** — it lives under `datasets/_maintenance/`
  (`_deprecated`, `_suspended`, `_out_of_scope/*`) or `datasets/_dev/`. Do **not** "fix" these by
  adding `BeyondArena`/`TabArena (v0.1)`. Only datasets under `datasets/beyond_iid/` (and the v0.1
  set) carry a collection tag. See `datasets/_maintenance/_deprecated/README.md`.
* The records are now the source of truth — the one-off migrations that built them from the
  legacy sheet / shipped collections (`import-sheet`, `reconcile-tabarena`) have been removed.
* `curation/_template.md` is a copy-me reference documenting how to fill every field
  (files starting with `_` in `records/` are skipped by the loader, so it never counts as a dataset).
* **The review queue is derived, not hand-set.** `needs_review` is recomputed from
  `CurationRecord.review_reasons()` on every save (server, CLI, scripts) — never edit it by
  hand. A record lands in the dashboard's **Review** pill when `review_reasons()` returns
  anything; today that means: an empty **required** field (`suggestion` → untriaged), a dropdown
  value not in `vocabularies.yaml`, `ai_unverified` (an AI triaged it, no human has verified —
  see below), or `ship_conflict` (carries a `TabArena (v0.1)`/`BeyondArena` tag but `suggestion`
  is not an accepted verdict — i.e. not `Yes`/`Yes (Disagreement)`). To add a new automated check,
  extend `review_reasons()` (it is the single source of truth) and add a matching assertion in
  `tests/test_records_integrity.py`.
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

### Quick decision patterns (generalized — apply, then verify per-dataset)

Recurring signals → the usual `decision_markers` + `suggestion`. These are heuristics to
*speed triage*, not hard rules; the dataset still wins over the pattern. A signal is often in
the dataset **name** alone (e.g. `*-recommendation-challenge`, `*-forecasting-*`).

* **Recommendation / ranking / CTR / "recommendation"/"recommender" task** → `Out-of-scope Task
  (CTR/RecSys/Ranking)` → **No** (criterion 3).
* **Time-series *forecasting*** (predict future values of a series: demand/sales/price over a
  horizon) → `Time-series (Forecasting)` → **No** (excluded). *Distinguish* from a fixed
  predictive task that merely needs a **temporal split** (e.g. delay/price regression) — that is
  in-scope; tag `Non-IID (Temporal)` + `Temporal (NON-IID)`, not Forecasting.
* **Artificial / handmade / deterministic / simulated** (synthetic, toy, simulated physics with
  dedicated benchmarks) → `AHDS (Artifical/Handmade/Deterministic/Simulated)` → **No** (crit. 4B).
* **Pure non-tabular modality** where modality models clearly dominate (raw images / audio /
  text) → `Image` / `NLP (Text)` / `Wrong Domain / Source Modality` → usually **No**; vectorized
  features where tabular models are competitive can be in-scope (judge per dataset, crit. 4A).
  * **Recognition tasks are the leading exception — exclude even when vectorized.** For
    **image/character/object recognition** problems (handwritten digit/letter recognition, traffic-sign /
    face / leaf / texture recognition, …) the vision model is the only reasonable choice, so they are
    correctly `Image` / `Wrong Domain / Source Modality` → **No** *even when the dataset ships as a
    pre-extracted / vectorized feature table* — the feature vector does **not** make it a tabular task.
    This family (e.g. `letter`, the `mfeat_*` digit sets, `gina`/`gina_agnostic`, `gtsrb_*`, `optdigits`,
    `pendigits`, `usps`, `semeion`, `texture`, `one_hundred_plants_*`) has been deliberately and
    consistently excluded, and those calls are correct. Still a **case-by-case** decision: engineered
    morphological/spectral/sensor descriptors of a *physical object or process* where tabular models
    genuinely compete (the kept `wbcatt` is the precedent) stay in-scope — so don't auto-flag every
    "features extracted from images" record as wrongly rejected; for digit/character-and-similar
    *recognition*, the answer is almost always exclude.
* **Re-upload / processed copy of a known dataset** → `Duplicate`. If it is the version we keep,
  it can still be `Yes` (the marker is provenance); if it is redundant, **No** and name it
  `<canonical>_duplicate` (see the `_duplicate` convention enforced in tests).
  * **Shared source ≠ duplicate.** Two records citing the same UCI/OpenML page or DOI — or even
    the same display `name` — can be *legitimately distinct* datasets/tasks. E.g.
    `parkinsons_biomedical_voice_measurements` (Little 2007, voice-disorder **detection**) and
    `telemonitoring_parkinsons_biomedical_voice_measurements` (Tsanas 2009, **UPDRS-progression**)
    live in the same UCI repo so share a DOI but are different tasks; `amex_iid` / `amex_non_iid`
    are the IID vs grouped versions of one competition. **The record's `## Comments` are
    authoritative — read them before marking `Duplicate`**, and when two records share a source the
    comments should state why they are distinct (ideally each citing its own specific DOI).
* **Survey / scientific-discovery / non-predictive table** (no genuine predictive target) →
  `No Good Target / Scientific Discovery` → **No** or `TBD -> 2nd Tier`.
* **Trivial** (all untuned models tie / solved perfectly) → `Trivial` → **No** (crit. 4C).
* **Target leakage / irreversible damage** (PCA-transformed, anonymized leaking features) →
  `Data Quality Issue` → **No** (crit. 4D).
* **Too small** to evaluate meaningfully → `Too Small` → **No** or `TBD -> 2nd Tier`.
* **Ethical concern** (sensitive use, creators ask it not be used for ML) → `Ethical Issue` → **No**.
* **Genuine real-world tabular classification/regression, clear target, adequate size** →
  **Yes** (well-known/strong) or **TBD -> Yes** (plausible, unverified).
* **Too little information in our record to decide** (bare link, no description) → do **not**
  reject for that alone: use **TBD -> Yes** / **TBD -> 2nd Tier** and note in `## Comments`
  exactly what must be inspected (size after cleaning, the real target, the split regime).

### Checking for duplicates (recommended method)

The reliable signal is the **original source** (first upload / the paper / the competition), **not
the data layout**. Two uploads of the same dataset can look very different — different column names,
dtypes, row counts, even preprocessing — and still be duplicates; and similar-looking tables can be
genuinely different datasets. So trace each candidate back to where the data *first* came from
rather than diffing the tables:

* **Compare the versions and *all* their links** across the candidate records — OpenML ids, Kaggle
  pages, UCI/DOI, GitHub, the originating paper. Overlap in any canonical link is a strong signal.
* **Follow each link to its origin.** A Kaggle/OpenML page usually *references* an upstream source
  (a paper, a UCI entry, an earlier uploader) — chase those references. Two records that bottom out
  at the same original source are duplicates even when their immediate links differ.
* **Spot-check by name and rough field structure** against datasets you already know. Familiarity
  with the usual schema/columns of common datasets lets you recognise a re-upload under a new name
  — and, the other way round, rule out a false match.
* **Rule of thumb:** duplicates can have a *very different data structure* but they **almost always
  share the same source**. A structural diff is weak evidence; shared provenance is strong evidence.

When two records really are the same data, keep the canonical one (`Yes` / shipped) and mark the
other `No` + `Duplicate`, named `<canonical>_duplicate` (the `_duplicate` convention is tested).
When they merely *share a source but are distinct*, record *why* in `## Comments` (see the
"Shared source ≠ duplicate" note above).

### Suggestion values

`suggestion` is the include/exclude verdict (and the one field that, left empty, marks a record
untriaged → Review queue):

* `Yes` — include. `TBD -> Yes` — likely include, pending verification.
* `TBD -> 2nd Tier` — plausible but secondary. `No` — exclude.
* `Disagreement` — curators genuinely disagree; **not yet shipped**, needs resolution.
* `Yes (Disagreement)` — **shipped on purpose, but with an unresolved disagreement to
  re-evaluate**. It counts as *accepted* (so a shipped dataset carrying it is not a
  `ship_conflict`), but it surfaces under the dashboard's **⚡ Disagreement** filter (status ⚡),
  not as a settled `Yes`. Use it for datasets already in a collection whose verdict is still open.

**Invariant:** a dataset shipped in a collection (`TabArena (v0.1)` / `BeyondArena`) must carry an
*accepted* verdict — `Yes` or `Yes (Disagreement)`. Anything else on a shipped record is a
`ship_conflict` (flagged in the Review queue and asserted in `tests/test_records_integrity.py`).

### Reading markers & optional fields (don't over-flag)

Records are deliberately sparse; a *missing* field is usually fine, not a gap. When reviewing or
auditing, do **not** flag these:

* **`decision_markers` are issue flags — a clean, good dataset has *none*.** No marker is the
  expected default and a *positive* signal (a clean, includable dataset); never treat a missing
  marker as incomplete. A `No` with no marker, or a `Yes` with no marker, can be perfectly correct.
* **A marker can be a *provisional best-guess* of a potential issue, not a settled verdict.** It's
  fine for an accepted (`Yes`) dataset to carry e.g. `Trivial` as a "watch out for this"
  hypothesis; if later evidence shows it isn't actually trivial we rule it out and note that in
  `## Comments`. So `Yes` + a concern marker is **not** a contradiction — read the comments.
* **`problem_type`, `required_split`, `original_data_state`, `domain`, `year` are optional metadata**
  (the dashboard's "Optional Tags"). Nice to fill, but their absence — even on an accepted
  dataset — is **not** a problem to flag. Only `suggestion` is required for triage.

### Push back on weak reasoning (you may second-guess a decision)

You are a curator, not a rubber stamp. A decision being *documented* — in a record's `## Comments`,
a verifier's note, or even the user's stated call — does **not** make it *correct*. When the
evidence contradicts the stated reasoning, **say so and argue your case** rather than deferring.

* **Argue from what the data *is*** — feature composition, true source, size, the actual target —
  **not** from how someone might re-solve the broader problem today. (E.g. a task whose features are
  mostly URL/text tokens + a few geometry numbers is not an "image-recognition" dataset just because
  the objects pictured were ads; a vision model couldn't even see the dominant features.)
* **Steelman the existing decision first**, then give a concrete, falsifiable counter-argument
  (numbers, feature breakdown, what a model can/can't access). Vague disagreement isn't useful;
  evidence is.
* **Surface, don't override.** Don't silently flip a human's verdict. Record your counter-argument
  in the record's `## Comments` under a clear heading (e.g. `**Counter-argument (AI):** …`),
  leaving the human the final call. If you change a field, follow the `AI (UNVERIFIED)` convention.
* This cuts both ways: if pushing back means *keeping* an exclusion the user is inclined to overturn,
  argue that too. The goal is the right call, with the reasoning preserved — not agreement.

### AI-assisted triage (the `AI (UNVERIFIED)` convention)

The AI may draft a *provisional* triage for untriaged records, but it must be **honestly
labelled and human-verified** before it counts. When the AI reviews a record it:

1. sets a `suggestion` (a real verdict, not left blank) and any justified `decision_markers`;
2. fills empty metadata (`problem_type`, `required_split`, `domain`, `year`,
   `original_data_state`) **only** where confidently inferable — never overwriting existing values;
3. adds `AI (UNVERIFIED)` to `checked_by` and `AI-Filled (Verify)` to `tags`;
4. prepends the **⚠️ AI-FILLED — UNVERIFIED** disclaimer to `## Comments`, then its assessment,
   **preserving any existing human notes** below it (never delete prior `CC:`/curator reasoning).

Because `AI (UNVERIFIED)` in `checked_by` adds `ai_unverified` to `review_reasons()`, these rows
stay in the **Review** pill (status 🤖) until a human verifies and removes the AI reviewer (or
replaces it with their own name). This is exactly how a curator finds "what the AI did that I
still need to check". The convention is enforced by `test_ai_reviewed_records_follow_convention`.

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
  = green, 🤖 AI-reviewed-but-unverified = cyan, ✗ suggestion No = red, ★ accepted-not-yet-in-DF
  = blue, ⚠ needs review / untriaged = orange, • other = yellow; first match wins, so 🤖 shows
  even when the AI already filled a Yes/No suggestion). Click the funnel in its header to filter
  by status, or click the column to sort by it.
* Top **pills** (Data Foundry / TabArena v0.1 / BeyondArena | Review / ⚡ Disagreement) are
  exclusive filters (clicking one resets the others) but layer on top of the status funnel —
  pick a pill, then narrow by status. All three of **Data Foundry** / **TabArena v0.1** /
  **BeyondArena** read the merged `data_foundry_status` field: **Data Foundry** counts collection
  membership (TabArena ∪ BeyondArena = 144 shipped datasets), **TabArena v0.1** / **BeyondArena**
  the respective tag. **Review** surfaces *everything a curator still owns* — untriaged rows (⚠)
  **and** AI-reviewed-but-unverified rows (🤖); use the status funnel to see one group at a time.
  The **search** box always spans all datasets.
* **📌 pin** (far-left column) keeps a row visible through any filter and sticks it to
  the top while scrolling.
* Dropdown columns show a **▾** on hover and a **＋** in the header to add a new option;
  the **Optional Tags** column opens a panel for the less-common fields.

## Notes

* The dashboard runs locally per curator (edit → `git` commit → PR). It is not hardened
  for multi-user or public exposure.
* `data-foundry-curation build-site <out>` produces a read-only static copy (e.g. for
  GitHub Pages); `export` writes a flat CSV/Parquet/XLSX snapshot or pushes to a Sheet.
