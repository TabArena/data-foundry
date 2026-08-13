Triage candidate datasets in the curation backlog: start the local dashboard and help the
user decide which candidates belong in the benchmark. Invoking this skill loads the
**curation guidelines** (below) into context so you can advise on selection and processing
decisions the way a human curator would.

## When to invoke

* The user wants to **open the curation dashboard** / work on the dataset backlog.
* The user asks whether a dataset **belongs in the benchmark**, what split it needs,
  or how to **process** it — answer using the guidelines below.
* The user wants to **add, edit, or triage** a candidate dataset record.

If the user instead wants to scaffold a *curation notebook* for an already-decided
dataset, use `/process-dataset`; to check a filled-in notebook / saved bundle before it
ships, use `/verify-dataset`.

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
  `required_split`, `problem_type`, `original_data_state`, `source_links`, `notebook_path`,
  `comments`, `reference`, `needs_review`).
* **`notebook_path` is the record's own pointer to its curation notebook** — one dataset, one
  notebook, stored in the record rather than resolved from the tree. See *The notebook pointer*
  below for when to set it and how to check it.
* Editable dropdown options live in `curation/vocabularies.yaml` (add new options
  there, via the dashboard's ＋ header buttons, or with `save_vocabularies`).
* **The `data_foundry_status` field is a merged multi-tag field** ("Data Foundry" column):
  it holds the *work state* (`DF: Yes`, `WIP (DF)`, `WIP (Triage)`, `DF: Much work`,
  `DF: Suspended`) **and** *benchmark-collection membership* (`TabArena (v0.1)`, `BeyondArena`).
  The two WIP values are mutually exclusive by meaning: `WIP (Triage)` = the verdict is still
  open (a `TBD -> …` / disputed suggestion) and someone is working on settling it;
  `WIP (DF)` = the verdict is a final `Yes` and the Data Foundry integration (notebook) is in
  progress. A record whose suggestion is not yet a final `Yes` must **not** carry `WIP (DF)`.
  Every dataset
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
  is not an accepted verdict — i.e. not `Yes`/`Yes (Disagreement)`/`No (Retired)`). To add a new automated check,
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

**`## Comments` hold substance, not a change log.** Write down the details we care about —
provenance, leak mechanisms, the real target/split, why a verdict was reached, what still
needs checking. Do **not** append entries that merely restate a field edit ("marked WIP",
"set suggestion to No", "added tag X"): git history already records who changed what and
when, so such notes are pure noise. A dated `CC (YYYY-MM-DD, Name):` comment is for *new
reasoning or facts* accompanying a change, not for the change itself.

**Keep comments minimal — substance is not volume.** Record only the key information a curator
needs to act: what the dataset really is, the decisive reason for the verdict, where the data can
be obtained, what still needs checking. A few sentences is normal; a screenful is almost always too
much. Do **not** dump everything you learned while investigating — per-column missingness, byte
sizes, checksums, download-endpoint mechanics, side observations, or restatements of front-matter
fields. Those belong in the curation notebook, not the record. If you were asked for one thing (a
download link, a duplicate check), write *that* down, not a report of the whole investigation.

**Cite papers by location in the text, never from memory.** A dataset's paper is often the decisive
evidence, so any claim you attribute to one must come with a *text reference* — the section, table or
page, and the load-bearing sentence quoted — and you must have read that text, not the title,
abstract or your recollection of the field. State it in the form "Sec. 6.1, p. 12: \"…\"" so the next
curator can check it in one step. Two traps this prevents, both real:

* **A paper can refute the claim you were about to make.** `kddcup99`: the simulation-artifact
  critique (Mahoney & Chan, RAID 2003) looks like it condemns KDD, but Tavallaee et al. (CISDA 2009,
  Sec. III) state the artifacts "do not affect the KDD data set since the 41 features used in KDD are
  not related to any of the weaknesses mentioned" — the artifacts are packet-header fields absent from
  KDD's features. Cite the section and the contradiction surfaces; cite from memory and it doesn't.
* **A paper's own framing can decide the verdict.** `intrusion_detection`: the BCCC/NTLFlowLyzer paper
  (Shafi et al., Computers & Security 148:104160, 2025) says in Sec. 6.1 "our focus is on developing a
  profiling system, not a detection system", so its headline ">99.8%" is profile-coverage, not
  predictive accuracy, and the release ships no target/split/baseline — that quote is the reason the
  record is `No` + `No Good Target / Scientific Discovery`.

If a paper is paywalled and you could not read the passage, say so explicitly and mark the claim as
unverified rather than paraphrasing the abstract as if it were the text.

### Quick decision patterns (generalized — apply, then verify per-dataset)

Recurring signals → the usual `decision_markers` + `suggestion`. These are heuristics to
*speed triage*, not hard rules; the dataset still wins over the pattern. A signal is often in
the dataset **name** alone (e.g. `*-recommendation-challenge`, `*-forecasting-*`).

**Always read the record's `## Comments` and understand what they *mean* before triaging or overturning —
they usually already contain the decisive fact** (the true source, a leak mechanism, the experimental
setup, the provenance). Many datasets that look "unknown" are decidable from the comment alone: e.g.
`jannis` looks like anonymised numeric columns, but its comment ("From AutoML challenge … SAIAPR-TC12")
identifies it as **image-derived** → `Image` → **No**; `sonar`'s comment shows it is an outdated,
handcrafted sonar-return toy experiment → out on its **setup**, not merely its acoustic features.

* **Scope by the *original* task, not the first source's framing.** A re-upload frequently relabels a
  dataset into a different task — e.g. an OpenML page presenting a recommendation dataset as a plain
  regression, or a Kaggle mirror renaming it. Do **not** accept the first source you land on at face
  value: trace what the data was *originally collected and used for* (the same original-source tracing
  used for duplicates) and let that decide scope. `yearprediction_the_million_song_dataset` is the
  canonical trap: OpenML id 4352 serves it as YearPredictionMSD *regression*, but it is the Million Song
  Dataset Challenge — a **song-recommendation** task — repackaged, so it is correctly
  `Out-of-scope Task (CTR/RecSys/Ranking)` → **No**, and the regression re-framings are fake / duplicates.
* **Recommendation / ranking / CTR / "recommendation"/"recommender" task** → `Out-of-scope Task
  (CTR/RecSys/Ranking)` → **No** (criterion 3). Applies even when a mirror re-serves it as
  classification/regression (see the "original task" note above, e.g. `yearprediction_the_million_song_dataset`).
* **Time-series *forecasting*** (predict future values of a series: demand/sales/price over a
  horizon) → `Time-series (Forecasting)` → **No** (excluded). *Distinguish* from a fixed
  predictive task that merely needs a **temporal split** (e.g. delay/price regression) — that is
  in-scope; tag `Non-IID (Temporal)` + `Temporal (NON-IID)`, not Forecasting.
  * **A missing or hidden timestamp does NOT make a task IID — check the task *design*, not just the
    columns.** The time index is often absent: dropped by an uploader, never shipped, or only implied by
    how the data was collected (samples logged sequentially over months/years; every feature and the
    target are *contemporaneous* readings that would all be known at prediction time `t`). Do not take
    "no timestamp column" as evidence of IID and rubber-stamp a random split — that silently leaks
    temporal structure. If the underlying setup is "values unfolding over time from a stream of
    signals", it is temporal / forecasting regardless of whether a literal date column survived; treat
    it as such (or reject as `Time-series (Forecasting)`), and note that the timestamp must be recovered.
    `combined_cycle_power_plant` is the trap: no timestamp column, so it *looks* like IID sensor
    regression, but it is a 6-year hourly sensor stream predicting the plant's hourly output — a
    (multivariate) forecasting setup a random split corrupts → correctly `Time-series (Forecasting)` → **No**.
  * **Don't trust the split the paper / source prescribes — verify it against the task design.** The
    original authors (or the dataset page) can choose a *leaking* evaluation split — most commonly a
    random split on data that is really temporal — and papers get this wrong often. A prescribed "random
    split" is **not** evidence the task is IID; treat the documented protocol as a claim to check, not a
    fact. `appliances_energy_prediction` is the example: it *has* a date column (10-min readings over
    ~4.5 months) and is a forecasting task, but was evaluated with a leaking random split, so it is
    correctly `Time-series (Forecasting)` → **No**, not the in-scope temporal regression an uncritical
    reading of the paper suggests.
* **Artificial / handmade / deterministic / simulated** (synthetic, toy, simulated physics with
  dedicated benchmarks) → `AHDS (Artifical/Handmade/Deterministic/Simulated)` → **No** (crit. 4B).
* **Pure non-tabular modality** where modality models clearly dominate (raw images / audio /
  text) → `Image` / `NLP (Text)` / `Wrong Domain / Source Modality` → usually **No**; vectorized
  features where tabular models are competitive can be in-scope (judge per dataset, crit. 4A).
  * **Features that are an algorithmic vectorization of image/video content → exclude even when the
    columns are numeric.** If the features are *computed from an image/video to describe its content* —
    raw pixels, HOG, colour/texture histograms, **or** morphological / geometric / spectral descriptors
    extracted by a CV / image-analysis pipeline, video-derived kinematics, remote-sensing spectra — then
    the underlying task is a vision task and a vision model is the natural tool, so it is correctly
    `Image` / `Wrong Domain / Source Modality` → **No**. The pre-extracted feature vector does **not**
    make it tabular. This covers both recognition sets (`letter`, `mfeat_*`, `gina`/`gina_agnostic`,
    `gtsrb_*`, `optdigits`, `pendigits`, `usps`, `semeion`, `texture`, `one_hundred_plants_*`) **and**
    measured-from-image tables (`magic_gamma_telescope` shower geometry, `wdbc` Xcyt nuclei descriptors,
    `image_gesture_phase_segmentation` video kinematics, `dry_bean`/`raisin`/`pumpkin_seeds`/`rice`
    seed-photo morphology, `satimage`/`wilt` remote sensing, `banknote_authentication` wavelet stats).
  * **"One more layer of abstraction" is still image-derived — a non-pixel or human-in-the-loop feature
    does not escape the Image exclusion.** Two traps that look like carve-ins but are **not**:
    * **Descriptors / encodings *of* an image** (its geometry, shape, layout) stay image-derived even when
      mixed with a few genuinely non-visual columns. `internet_advertisements` is the canonical case:
      per UCI its features "encode the geometry of the image (if available) as well as phrases occurring
      in the URL, the image's URL and alt text" — the task is *is this on-page object an ad image?*, a
      vision task with some text metadata bolted on, so it is correctly `Image` → **No**. The URL /
      alt-text tokens do **not** turn it into a carve-in.
    * **A human *scoring what they see in an image* is still an image feature.** When a person grades the
      content of a photo / microscope slide / scan, the value measures the image, not an independent
      instrument. `breast_w`'s 1–10 cytology grades (clump thickness, cell-size uniformity, …) are a
      pathologist's scoring of cell morphology seen under a microscope → image-derived → **No**. "A human
      assigned it by eye" does **not** rescue it when *the thing being scored is an image*.
  * **Narrow carve-in (stay in-scope):** attributes that are *not* a description / scoring of image (or
    other non-tabular) content — genuinely non-visual measurements or metadata taken from the real-world
    entity directly (lab values, sensor readings, questionnaire responses, transaction fields), **not**
    read off a photo / scan of it. Signals (audio/sonar) are the same call case-by-case: interpretable
    engineered acoustic *measures* the field uses as the instrument (jitter/shimmer in the shipped
    Parkinsons voice data) can be in-scope; raw-signal spectral bins lean out. (`wbcatt` — expert-annotated
    white-blood-cell morphology attributes — sits on the same boundary as `breast_w` and is only kept
    **provisionally** for a possible causal/counterfactual framing; treat it as borderline, not a clean
    in-scope precedent.) **Decide on the data's actual columns, not the dataset's fame** — "features
    extracted from / describing an image" is the exclude signal, not a thing to auto-flag as wrongly rejected.
* **Re-upload / processed copy of a known dataset** → `Duplicate`. If it is the version we keep,
  it can still be `Yes` (the marker is provenance); if it is redundant, **No** and name it
  `<canonical>_duplicate` (see the `_duplicate` convention enforced in tests).
  * **Different versions / cuts of one underlying dataset are duplicates too — "duplicate" is not only an
    *exact* re-upload.** Two records built from the *same underlying data* with only a minor variation — a
    swapped target / outcome column, a different slice of the same cohort, added or dropped rows / features —
    are duplicates when neither adds a genuinely distinct task. E.g. `arsenic_male_lung` is the
    lung-cancer-outcome version of the *same* arsenic-exposure data as `arsenic_male_bladder` (bladder
    outcome) → `Duplicate` → **No**. This is the flip side of the next bullet: reach for `Duplicate` when it
    is the *same data wearing a new target / slice*, and for the "Shared source ≠ duplicate" carve-out only
    when the shared source genuinely yields *different tasks*.
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
* **Target leakage / irreversible damage** (PCA-transformed, anonymized leaking features, **or a feature
  that is itself the output of a supervised transform fit on the whole dataset** — a discriminant-analysis
  score, target / mean encoding, a model's own prediction) → `Data Quality Issue` → **No** (crit. 4D).
  Such a feature bakes label / whole-set information into every row and cannot be recomputed per
  train/test split, so it leaks the test distribution irreversibly. E.g. `yeast` ships a column *"Score of
  discriminant analysis of the amino acid content of vacuolar and extracellular proteins"* — a DA fit on
  the full dataset, already baked in and unfixable → leak → **No**.
* **Too small** to evaluate meaningfully → `Too Small` → **No** or `TBD -> 2nd Tier`.
* **Ethical concern** (sensitive use, creators ask it not be used for ML) → `Ethical Issue` → **No**.
* **Genuine real-world tabular classification/regression, clear target, adequate size** →
  **Yes** (well-known/strong) or **TBD -> Yes** (plausible, unverified).
* **Source / provenance unknown even with a working link** → `Missing source information` → **No**.
  A live download link is **not** a known source: if following it bottoms out at an anonymous
  Kaggle / OpenML / PMLB re-upload with no documentation and no traceable upstream (paper, competition,
  institution, an identifiable original uploader), the origin is unknown and criterion 1 (unique
  original source) is not met. Do **not** treat "the link still resolves" or "the data looks fine" as
  grounds to recover it — **clear provenance / documentation is itself a strong positive indicator of a
  good dataset, and its absence is a real negative signal.** (e.g. `water_quality_and_potability`,
  `3d_estimation_using_rssi_of_wlan_dataset_complete_1_target`, `calendardow`.)
* **Too little information *in our record* to decide** (bare link, no description, but the dataset's
  *origin is otherwise known / traceable*) → do **not** reject for that alone: use **TBD -> Yes** /
  **TBD -> 2nd Tier** and note in `## Comments` exactly what must be inspected (size after cleaning, the
  real target, the split regime). This is a sparse *record*, not an unknowable *source* — contrast the
  bullet above, where the dataset's provenance itself cannot be established.

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

`suggestion` is the include/exclude verdict **as of now** — it is what we suggest for the dataset
*right now*, and an earlier verdict can change over time (a shipped dataset can later be excluded; see
`No (Retired)` below). It is also the one field that, left empty, marks a record
untriaged → Review queue:

* `Yes` — include. `TBD -> Yes` — likely include, pending verification.
* `TBD -> 2nd Tier` — plausible but secondary. `No` — exclude.
* `No (Retired)` — exclude, **but it did ship in a collection before the verdict changed**
  (e.g. later found trivial, or an ethical concern surfaced). Keep the collection tag
  (`TabArena (v0.1)` / `BeyondArena`) — it really did ship — and record *why* it was retired
  in `## Comments`. On a never-shipped record, plain `No` is the right value.
* `Disagreement` — curators genuinely disagree; **not yet shipped**, needs resolution.
* `Yes (Disagreement)` — **shipped on purpose, but with an unresolved disagreement to
  re-evaluate**. It counts as *accepted* (so a shipped dataset carrying it is not a
  `ship_conflict`), but it surfaces under the dashboard's **⚡ Disagreement** filter (status ⚡),
  not as a settled `Yes`. Use it for datasets already in a collection whose verdict is still open.

**Invariant:** a dataset shipped in a collection (`TabArena (v0.1)` / `BeyondArena`) must carry an
*accepted* verdict — `Yes` or `Yes (Disagreement)` — **or** `No (Retired)`. Anything
else on a shipped record is a `ship_conflict` (flagged in the Review queue and asserted in
`tests/test_records_integrity.py`).

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
* **`problem_type` is not always a property of the dataset.** Some tables support *either* a
  regression target *or* a classification one, where taking one means dropping the other:
  `pva_revenue_prediction_kddcup98` has the donation amount (`TARGET_D`) and the response flag
  (`TARGET_B` = did they donate at all), so each is a framing of the same signal and keeping
  both would leak. There the field records the task *we* decided on — it follows whichever run
  we ship — and the alternative belongs in `## Comments`.
  This is the one case `Multi-target` does **not** cover: that tag is for several targets
  predicted **at once** (multi-output), which is the right call whenever the targets are
  distinct quantities that could be modelled jointly (next-day min *and* max temperature,
  several soil nutrients). Both patterns are legitimate — read the record's comments before
  deciding which one you are looking at, and don't strip a `Multi-target` tag a curator set.

### The notebook pointer (`notebook_path`)

A curated dataset comes from exactly one notebook, and the record stores which one:

```yaml
notebook_path: datasets/beyond_iid/new_iid/student_portuguese_performance/student_portuguese_performance.ipynb
```

It lives in the record, not in a lookup, so the record names its notebook on its own — readable in
the file, in a PR diff, and by anything that never runs the dashboard — and so a later
reorganisation of `datasets/` is a path edit instead of a change to resolution rules. The
dashboard's 📓 button reads it directly, and only falls back to searching the tree for a record
that has no pointer yet.

**Which tree it must point into.** A dataset we *ship* is curated in its collection's tree, and
its pointer has to name that copy:

| The record ships in | Its notebook lives under |
|---|---|
| `BeyondArena` | `datasets/beyond_iid/{new_iid,old_iid,temporal,grouped}/` |
| `TabArena (v0.1)` only | `datasets/_maintenance/_old_collections/tabarena-v0pt1/` |
| nothing (a candidate) | `datasets/_dev/` while in progress, or `datasets/_maintenance/` once deprecated / suspended / out of scope |

**`datasets/_dev/` never backs a shipped dataset.** It holds work in progress *and* older copies of
notebooks that have since shipped from `beyond_iid` — most `_dev/feature_selection/<name>.ipynb`
files are exactly that. Pointing a shipped record there sends every reader to preprocessing that
produced no released data. For an unshipped candidate the reverse holds: `_dev` or `_maintenance` is
the right and only answer (`datasets/_maintenance/_deprecated/chronic_kidney_disease/…` is a correct
pointer). `sync-notebooks` enforces this — it resolves a shipped dataset only within its collection
tree, and leaves the pointer empty rather than naming a `_dev` copy, which the integrity tests then
report as a shipped record missing its notebook.

**Set it when:**

* a notebook is created — `/process-dataset` does this as its own step;
* a notebook is renamed, moved between trees (`_dev/` → `beyond_iid/`, or into `_maintenance/`
  when a dataset is retired), or a dataset directory is renamed;
* the run that ships changes — a `<name>_1m.ipynb` sub-sample or a `<name>_clf.ipynb` alternative
  target supersedes the full-size run. Point at the run that shipped and say why in `## Comments`;
  a reader following the wrong sibling reads preprocessing that produced no shipped data.

**Check it when:**

* you are about to open a PR that touches `datasets/` or the records — `data-foundry-curation
  sync-notebooks --check` prints every drifted record and exits non-zero, and plain
  `sync-notebooks` writes the fixes;
* a 📓 link opens something unexpected (the wrong tree, the wrong variant, a 404);
* you are verifying a dataset — `/verify-dataset` carries this as a rubric item: the pointer must
  name the notebook whose output holds the UUID the collection pins.

`tests/test_records_integrity.py` fails on a pointer that is missing on a shipped dataset, does not
exist, is not a `.ipynb`, sits outside its dataset's directory, has drifted from the tree, or names
a sibling run that did not ship. So it is enforced, not merely conventional — but the enforcement
compares against the tree, so a *deliberate* pointer to something the resolver would not pick needs
its reason in `## Comments` (and will still fail the sync check).

**Do not** hand-write a pointer you have not verified exists, and do not point a shipped dataset at
a working copy under `datasets/_dev/`: the shipped notebook is the one that produced the data.

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
  even when the AI already filled a Yes/No suggestion, and a `DF: Yes` row shows ✓ whatever its
  verdict). Click the column to sort by it, or the funnel in its header to filter: each status
  cycles **✓ require → ✕ exclude → off**, so "hide everything rejected" is one click.
* **Column filters combine with AND and NOT.** Every dropdown column's header has a filter
  button opening a popover that lists all its values (vocabulary ∪ values actually present ∪
  **(empty)**, each with a count; ⚠ marks a value missing from `vocabularies.yaml`). Clicking a
  value cycles **✓ require → ✕ exclude → off**. Multi-value columns carry a **match ALL ✓ /
  match ANY ✓** switch at the top of the popover — set it before (or after) ticking values, it
  persists per column for the session; ALL is the default, so `tags` ✓Non-IID (Temporal)
  ✓Review Prio 1 means both. On single-value columns ✓ values read as "any of". Different
  columns always AND together, so e.g. `BeyondArena` ✓ + `DF: Yes` ✕ is expressible.
  Free-text column filters and the top **search** box take the same query syntax: several
  terms must all match, `!word` excludes, `"quoted phrase"` keeps spaces.
* An amber **filter strip** under the top bar spells out every constraint in effect in words
  (`Tags: A AND B · NOT C`), with a ✕ per constraint and a ✕ Clear-all — read it instead of
  guessing why rows are missing.
* Top **pills** (Data Foundry / TabArena v0.1 / BeyondArena | Review / ⚡ Disagreement) are
  exclusive filters (clicking one resets the others) but layer on top of the status funnel —
  pick a pill, then narrow by status. All three of **Data Foundry** / **TabArena v0.1** /
  **BeyondArena** read the merged `data_foundry_status` field: **Data Foundry** counts collection
  membership (TabArena ∪ BeyondArena = 144 shipped datasets), **TabArena v0.1** / **BeyondArena**
  the respective tag. **Review** surfaces *everything a curator still owns* — untriaged rows (⚠)
  **and** AI-reviewed-but-unverified rows (🤖); use the status funnel to see one group at a time.
  The **search** box deliberately spans all datasets, overriding the pills / status / column
  filters while a term is present (the filter strip labels it *(all datasets)*).
* **📌 pin** (far-left column) keeps a row visible through any filter and sticks it to
  the top while scrolling. The same column links every row's **curation record (📄)** —
  its `curation/records/<name>.md` on GitHub — and, for curated datasets, the
  **curation notebook (📓)**, read straight from the record's `notebook_path`; on 🤖 rows it also
  holds the ✓ verify action.
* **🔗 Copy link** (appears next to **✕ Clear filters** whenever the view is filtered)
  copies a URL that reopens the exact current view — active pill, status constraints, search
  term, and every column filter are encoded in the hash
  (`#pill=bey&status=+in-df|-no&hf.tags=mode=any|+New IID|-Tiny Data`). Opening such a link
  restores the view; this works on the live dashboard and the static GitHub Pages build alike
  (live-only states like the Review pill are ignored there), and links made before
  include/exclude existed still work (a bare value means "require").
* Dropdown columns show a **▾** on hover and a **＋** in the header to add a new option;
  the **Optional Tags** column opens a panel for the less-common fields.

## Notes

* The dashboard runs locally per curator (edit → `git` commit → PR). It is not hardened
  for multi-user or public exposure.
* `data-foundry-curation build-site <out>` produces a read-only static copy (e.g. for
  GitHub Pages); `export` writes a flat CSV/Parquet/XLSX snapshot or pushes to a Sheet.
