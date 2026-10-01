# Curation guidelines

These tell you *how to assist*: how we decide whether a dataset belongs in TabArena
and how we curate the ones we keep. The full rendered version is the dashboard's
**Guidelines** tab (`src/data_foundry/curation/static/guidelines.html`).

## Background: IID vs non-IID

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

## Dataset selection criteria (a dataset must satisfy all)

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

**Licence and redistribution terms are not a selection criterion at this stage** (Lennart, 2026-09-23).
A non-commercial clause, a request-only download, or a no-redistribution rule is *noted* in
`## Comments` (one line: what the terms are and where they are stated) and is never the reason for
a `No`, a `TBD -> 2nd Tier`, or a marker. Decide on the data. `lucas_topsoil` is the example: JRC's
terms forbid redistribution, and the record still gets triaged on what the survey measures.

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

If the publisher's copy is paywalled, first spend a short search on a free copy: Unpaywall / Europe PMC, arXiv,
Semantic Scholar, the authors' or institution's pages, and a web search for the exact title in quotes plus "pdf".
Try it with and without the quotes, and also with the first author's name. Copies often sit on PDF mirrors such as
ResearchGate, SciSpace (`scispace.com/pdf/<title-slug>-<id>.pdf`, formerly typeset.io), oa.mg, CORE and
Academia.edu. Some of these block automated fetches (ResearchGate and SciSpace return 403), and the agent's
search engine does not rank like Google. So when a mirror is listed but cannot be fetched, or nothing turns up,
**ask the human for it** and give them the exact query: a Google search for the title plus "pdf" usually finds
it (`garments_worker_productivity`: the Inderscience paper was on SciSpace). They can put the PDF in the workspace. Ask as soon as the paper
turns out to matter rather than working around it. If you go on without it, say
so explicitly and mark the claim as unverified rather than paraphrasing the abstract as if it were the text.

## Quick decision patterns (generalized — apply, then verify per-dataset)

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
  * **Under class imbalance, accuracy against the majority class is not evidence** of anything, in either
    direction (Lennart, 2026-09-23). "78% accuracy on an 80% majority class" does not show a task is
    unlearnable, and a high accuracy does not show it is trivial. Judge learnability with ROC AUC (per class
    or one-vs-rest macro), log loss against the class-prior baseline, or another proper score, and when the
    data can be loaded, fit a quick gradient-boosting model on the features known at prediction time and
    report those numbers. `us_accidents` is the example: the published "78% accuracy" was quoted as if it
    settled the matter; only an AUC check does.
* **Target leakage / irreversible damage** (PCA-transformed, anonymized leaking features, **or a feature
  that is itself the output of a supervised transform fit on the whole dataset** — a discriminant-analysis
  score, target / mean encoding, a model's own prediction) → `Data Quality Issue` → **No** (crit. 4D).
  Such a feature bakes label / whole-set information into every row and cannot be recomputed per
  train/test split, so it leaks the test distribution irreversibly. E.g. `yeast` ships a column *"Score of
  discriminant analysis of the amino acid content of vacuolar and extracellular proteins"* — a DA fit on
  the full dataset, already baked in and unfixable → leak → **No**.
* **Too small** to evaluate meaningfully → `Too Small` → **No** or `TBD -> 2nd Tier`.
* **Ethical concern** (sensitive use, creators ask it not be used for ML) → `Ethical Issue` → **No**.
* **Licence / redistribution restriction** (non-commercial, request form, no redistribution) → **not a
  reason** and no marker: write it down as a note in `## Comments` and triage the data on its merits.
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

## Checking for duplicates (recommended method)

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

## Kaggle sources: read the discussions and notebooks, not just the data card

A Kaggle competition or dataset page is a *claim* about the data; the **Discussion** tab and the public
**Code** notebooks are where the problems surface. Before triaging anything sourced from Kaggle, skim both
(discussions sorted by votes, notebooks by votes) and look for: leak threads and "hack" baselines (a
trivial rule that scores near the top), disputes about the test set (random vs temporal, ground truth
recoverable from a public upstream), duplicated or mislabelled rows, a column that is the target in
disguise, and uploader answers about where the data really came from. Write what you find in
`## Comments` with the thread / notebook link, and let it feed the verdict and the `decision_markers`.

* `pkdd-15-taxi-trip-time-prediction-ii` (Porto, ECML/PKDD 2015): a public snippet predicting
  `max((len(POLYLINE) - 1) * 15, 660)` reportedly scores well. That is not test data leaking from
  elsewhere: the test polylines are *truncated prefixes* of the trips (de Brébisson et al. 2015: "The
  testing dataset is composed of 320 partial trajectories, which were created from five snapshots taken at
  different timestamps"), so the elapsed time is a lower bound on the target. The competition is "remaining
  travel time from a partial GPS trajectory" — a trajectory task, not a tabular ETA regression — and only
  the notebooks make that visible from the outside. Whether a tabular reframing survives is then a curation
  question the data card cannot answer (the record stays an open candidate).

Kaggle pages do not render for a plain fetch (JS-only, reCAPTCHA), so read them through the `kaggle` CLI.
The credentials are in `~/.kaggle/`. Use **kaggle >= 2.2.2** (run it with `uvx`, so the project venv is not
touched): the 2.2.0 in the venv gets a 403 from the discussions API.

```bash
K="uvx --from kaggle==2.2.2 kaggle -W"
$K datasets metadata <owner>/<slug> -p .          # data card text (description, licence) as JSON
$K datasets files <owner>/<slug>                  # file names, sizes, upload dates
$K datasets topics list <owner>/<slug>            # Discussion tab: id, title, author, comments, votes
$K datasets topics show <owner>/<slug> <topic_id> # one thread with all its comments
$K competitions topics list <competition>         # the same for a competition (and `topics show`)
$K kernels list --dataset <owner>/<slug> --sort-by voteCount   # Code tab, by votes
$K kernels list --user <owner>                    # the uploader's own notebooks
$K kernels pull <owner>/<kernel> -p <dir> -m      # a notebook's source and metadata
```

Ask the human for a page only when the CLI cannot reach it, and say explicitly when this check was skipped.

## Suggestion values

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

## Reading markers & optional fields (don't over-flag)

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

## Dataset processing conventions

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
  * **How many splits (TabArena convention):** roll the time horizon back from the newest data to create
    several split time points. At each point, train on all data before it and test on the data after it
    within the time horizon. Create the same number of splits as an IID or grouped task of that size would
    get (`get_recommended_splits_dimensions`, e.g. 10 x 3 = 30 for 500-2,500 training rows), but never use a
    split with less than 50% of the original data as training data: such a split is too unrepresentative
    of the original application.
  * **Check that the test windows are still meaningful.** With the 50% floor, all test windows come from the
    newest half of the data. Count the minority-class rows (or the target's spread) per window: if the
    windows the convention asks for hold only a handful of positives, or none, the scores are noise and the
    dataset is too small for a temporal task (`seismic_bumps`: 49 positives in the newest half, 0-5 per
    window for 30 windows). Do not fall back to an IID split for a non-stationary sequence; treat it as
    `Too Small` instead.
  * **Widen the windows when they get too small.** Finer windows do not add test rows (the 50% floor fixes
    the test pool); they only cut it into smaller, noisier pieces. If the convention's window count leaves
    windows with fewer than about 50 test rows, use wider windows and fewer splits instead, and say so in the
    splits comment (`coffee_rating_prediction`: 26 monthly windows held 2-72 reviews each and doubled the
    confidence interval of a model comparison; 13 two-month windows hold 54-115).

