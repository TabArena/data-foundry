---
unique_name: sdss_17
name: SDSS17
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 3
decision_markers:
- Selection Bias
tags:
- Non-IID (Temporal)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Varying Delay'
- Expanding Science Catalogue
original_source: Other
year: '2021'
required_split:
- Temporal (NON-IID)
source_links:
- https://www.kaggle.com/datasets/fedesoriano/stellar-classification-dataset-sdss17
notebook_path: datasets/beyond_iid/old_iid/sdss_17/sdss_17.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/sdss_17/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

The data consists of 100,000 observations of space taken by the SDSS (Sloan Digital Sky Survey). Every observation is described by 17 feature columns and 1 class column which identifies it to be either a star, galaxy or quasar. Spatial correlations. Might require spatial/temporal split. Sounds like a pretty cool task. Might have spatial information with alpha and delta

Potential issue: -

Lennart: Likely impact of time can be ingored and all features are time invariant as far as I can tell. Spatial impact might be ignorable as well, or remove these features

Andrej: Possibly license issues

CC (2026-10-01, Lennart): Leak audit fixes (v2 definition), now a photometric task (position + u, g, r, i, z + cam_col):
- Dropped `redshift`: the SDSS pipeline fits class and redshift in one step and stars are only fitted within +-1200 km/s (Bolton et al. 2012, Sec. 3.1), so |redshift| <= 0.0041 marks stars almost perfectly.
- Dropped `plate` and `fiber_ID`: a plate is one spectroscopic pointing (6,284 plates vs 6,352 plate-MJD pairs, so it duplicates the already dropped MJD) designed for one targeting program; it encodes how the object was pre-selected from photometry, not what it is. 11% of rows sit on plates that are >= 99% one class (5,860 galaxy and 5,428 star rows), and plate + fiber alone give OvR AUC 0.80. A new object has no plate before it is targeted, and the fiber is only a slot on the plate. Adding both to the photometry also hurts LightGBM (log loss 0.334 -> 0.404, high-cardinality overfit); grouping folds by plate does not change the photometry-only score (0.340), so the split stays IID.
- Deduplication by sky position instead of `obj_ID`: the Kaggle CSV stores obj_ID as a rounded float, so `drop_duplicates(obj_ID)` had removed 21,947 distinct objects (78,053 -> now 99,999 rows); by position there is one object observed on two plates.
- The sentinel -9999 (one row in u, g, z) is set to missing.
Photometric LightGBM: log loss about 0.33, OvR AUC about 0.96.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback log_loss — SDSS DR17 (Abdurro'uf et al. 2022) is a data release with no prediction task or metric; the Kaggle 'Stellar Classification Dataset - SDSS17' is a dataset page, not a competition, with no evaluation metric. Our task (photometric classification, redshift/plate/fiber dropped) also differs from the SDSS pipeline's spectroscopic classification.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): codes shipped as numbers, left for the curator's review: `cam_col`.

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): cam_col a category.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `desi_dr1_star_galaxy_quasar` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship as defined: a photometric star/galaxy/quasar task from public-domain SDSS DR17 with the spectroscopic leaks dropped and the selection marked. Priority 3: gap 1, use case 0, source 1, shape 1, risk -1.

CC (2026-11-11, Andrej): split by the year of the spectrum instead of at random, and the collection facts corrected (review page, issues 2, 4 and 5):
- Split: nine one-year windows, 2012 to 2020, newest first, each trained on every spectrum taken before it (51.3% to 99.9% of the 99,999 objects; 141 to 11,044 test spectra). Every row is a spectrum taken on a dated night through a plate drilled for one targeting programme, and the programmes changed what they observed (quasars 3-11% of each year's spectra in 2000-2009, 14-16% in 2010-2013, 31-46% from 2014 on). A classifier in use is trained on the spectra taken so far and labels objects the survey has not yet observed, so it has neither the test object's plate-mates nor the later programmes, which the random split gave it. The raw `MJD` returns as the time column `date`, never as a feature of its own right; `required_split` is Temporal (NON-IID).
- Measured (log loss, lower is better; untuned LightGBM on the shipped features): 0.331 random, 0.338 by plate, 0.354 by sky cell of 10 degrees, 0.506 by year. On the same rows, the 48,743 spectra of 2012-2020, 0.391 random against 0.506 by year; trained on a random draw of the other years instead of the earlier ones, the loss on 2014 falls from 0.530 to 0.470 and on 2016 from 0.501 to 0.444. The sky position lowers the random score (0.353 -> 0.331) and raises the year score (0.491 -> 0.506): it teaches the sky footprints of past programmes. Under the year split TabPFN 3.5 scores 0.439 and logistic regression 0.755, against the class shares at 1.121.
- Window sizes: the 2019 and 2020 windows hold 935 and 141 spectra, both above the 50 test rows below which windows are widened, and nine windows is what a task of this size gets as folds; 0 to 5 plates per window were also observed before it, at most 90 test rows (0.9% of the 2013 window).
- No time basis: a temporal split carries no time-basis tag, so neither `Timeless` nor any other is set (issue 4, option B).
- Collection facts (issue 5, option C): `Samples: Over Time` and `Time: Dated` in place of `Samples: No Time Dimension` — the spectra arose over 2000 to 2020, each on a dated night — plus `Target: Varying Delay`: the class comes with a spectrum taken after the imaging, by a delay that differs from object to object.

CC (2026-11-11, Andrej): the photometric task stays as defined (Review issue 3, A): u to z are the SDSS model magnitudes, not a spectrum; the spectra are recoverable from DR17 but set the label (class and redshift come from one template fit), so no spectral dataset is built. A `curation_comments` bullet says so.

CC (2026-11-12, Andrej): the date of the spectrum is no model input any more (Review issue 6, A):
- The prediction point is an object imaged but not yet observed spectroscopically, so the date of its spectrum arrives with its class. `date` still orders the rows and sets the nine yearly windows, but `Temporal(..., feature=False)` leaves it out of `feature_columns`: 8 features instead of 9.
- Measured before the change (untuned LightGBM, year split): log loss 0.540 with the date, 0.506 without; the score is not the reason, the actor's knowledge is.
- The capability is new in the v2 framework (`Temporal.feature`, stored as `time_is_feature` in the task metadata), added for this dataset.

CC (2026-11-12, Andrej): 2019 and 2020 form one last test window, and DR17's full set gets its own record (Review issues 7, B, and 8):
- Split: eight windows, newest first: 1 January 2019 to 24 March 2020 (1,076 test spectra, 72 plates), then the calendar years 2018 to 2012, each trained on every earlier spectrum (51.3% to 98.9% of the rows); a custom `_make_splits`, since declared windows have one length.
- Why: the windows shrink with DR17 itself (579,078 spectra in 2012, 56,989 in 2019, 5,957 in 2020; the file holds 1.6% to 2.4% of each year with DR17's class mix), not by a bias of the sample. eBOSS ended on 1 March 2019, and 2020 is 7 eFEDS plates of X-ray sources observed before the observatory closed for COVID-19 on 24 March 2020. A 2020 window alone (141 spectra, 8 plates) gave untuned LightGBM's log loss a standard error of 0.083 and 77% of the noise of the nine-window mean; merged with 2019 the newest window's is 0.024.
- Larger data: the Kaggle cut stays for now. DR17's full set (4,618,684 objects, the file's own query without its cut at 100,000 rows) has its own record, `sdss_dr17_star_galaxy_quasar`, to be considered for inclusion, with the evidence of issue 8 (LightGBM 0.509 to 0.485 at the 1M row budget, logistic regression unchanged).

CC (2026-11-12, Andrej): ship (Review issue 1 closed on Andrej's note, verdict ship); nothing open on the review page.
- Split and metric marked `ok`: the eight windows by the year of the spectrum, the date no model input, and log loss stay as decided in issues 2, 6 and 7.

## Review

**Outcome:** added. A 100,000-object sample of the Sloan Digital Sky Survey's Data Release 17 (shared on Kaggle):
whether an object is a galaxy, a star or a quasar, as the survey's spectroscopic pipeline classified it, predicted from
its sky position, its brightness in the five colour bands of the survey's images and the camera column; split by the
year of the spectrum, 2019 and 2020 in one window (issues 2 and 7; added with random splits). The AI recommends shipping
it as the photometric task it is (issue 3: the spectra can be recovered, but they set the label) with the split changed
to the year of the spectrum (issue 2, 2026-11-05; earlier: as defined). Reviewed without a panel, from the gathered
evidence: the record, the curator's leak-audit decision of 2026-10-01 and a model run on TabArena's copy, which still
had the redshift, plate and fibre; the split and the spectra were checked on the Kaggle file and DR17's own files on
2026-11-05 and 2026-11-06. Validity: the redshift (fitted together with the class) and the plate and fibre (which record
how the object was chosen for a spectrum) are dropped, so the task is classification from the images; every object was
chosen for a spectrum by its colours, which the `Selection Bias` marker and the approximate fit state. Value: the
curator's photometric probe reaches log loss about 0.33 (ROC AUC about 0.96, untuned LightGBM) on random splits, 0.485
on the eight year windows (issue 7); the benchmark spread was measured with the redshift, which made stars trivial, so
it does not carry over. Quality: non-detections are stored as the asinh magnitude of zero flux (u 24.6346, g 25.1143, z
22.8269), which are real values of the survey's magnitude system and stay; the one -9999 sentinel is set to missing.
Weighed: a public survey with documented classes and a real cataloguing use (+), the spectroscopic selection (-).

**Main points:** Nothing open: ship (issue 1, A, resolved 2026-11-12; split and metric `ok`). Settled 2026-11-12: the date of the spectrum orders the split but is no model input (issue 6, A; new framework capability); 2019 and 2020 form one last window, eight windows (issue 7, B); the Kaggle cut stays for now, and DR17's full set (4.6M objects) has its own record, `sdss_dr17_star_galaxy_quasar`, to be considered (issue 8). Settled 2026-11-11: split by the year of the spectrum (issue 2), the photometric task kept, not spectra (issue 3), no time-basis tag (issue 4), the record's facts corrected (issue 5).

**Record judgment:** valid. Andrej's early question on the licence is answered by the survey: "All SDSS data released
in our public data releases are considered in the public domain" ([SDSS image and data use
policy](https://www.sdss.org/collaboration/image-use-policy/)); the Kaggle file is a cut of DR17. The sky position
stays while the plate goes: a position exists before an object is targeted, a plate does not; the position also
carries the footprint of the targeting programmes, part of the selection the marker names. `cam_col` is a category
(Lennart, 2026-10-31). The data-scouting run of 2026-10-31 found better data for the same task,
`desi_dr1_star_galaxy_quasar` (priority 3), screened in its own record and not added yet. The record has no
`problem_type` or `domain`; the definition's values can be filled in without a mark.

**Issues for Andrej:**

1. **Ship as defined?**

   * **Problem:**
     - Nothing open was found: the redshift, plate and fibre are dropped, the licence is the survey's public domain,
       and the spectroscopic selection is marked with an approximate fit.
     - The benchmark spread was measured with the redshift, so the spread of the photometric task is known only from the
       curator's probe (log loss about 0.33, untuned LightGBM).
     - Ship as defined, or retire?
   * **Background:** SDSS: "All SDSS data released in our public data releases are considered in the public domain"
     ([SDSS](https://www.sdss.org/collaboration/image-use-policy/)). `desi_dr1_star_galaxy_quasar` (priority 3) is
     screened as better data and not added.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Ship as defined (implemented) | 99,999 objects, position, five magnitudes and camera column, log loss | a public survey; a real cataloguing use; no leak left | spectroscopic selection; spread of the photometric task not measured on benchmark methods |
     | B | Retire | `No (Retired)`, a CC line, the folder removed | leaves the place to the DESI set once added | no defect of the data found |

   * **Recommendation:** A: no reason in the task itself to retire it[^1a]. **Decision:** A or B?

   [^1a]: **TP-2** (Should): retire, fix or keep a task for a concrete reason found in the task itself; until one is
     found, the task stays.

   **Answer (AI, 2026-11-05):**

   * "As defined" no longer holds for the split: issue 2 recommends predicting each year's spectra from the earlier
     years instead of random objects. The rest of A stands: the rows, the features, the target, log loss and the
     licence.
   * The spread of the photometric task is now measured on probes: under that split TabPFN 3.5 0.439, untuned
     LightGBM 0.506, logistic regression 0.755 and the class shares 1.121 (log loss, 9 windows); under the random
     split 0.294, 0.331, 0.656 and 0.955.

   **Andrej (2026-11-12):** This issue is resolved, close it

   **Resolved (2026-11-12, Andrej):** A: ship, verdict `ship`, with the split and the metric marked `ok`: the eight
   windows by the year of the spectrum (issues 2 and 7), the date no model input (issue 6) and log loss stay. Nothing
   changed in `dataset.py` for this issue; CC line in the record.

2. **Which split: by the year of the spectrum, by plate, or by sky region, instead of random objects?**

   * **Problem:**
     - Every row is a spectrum taken on a dated night through a plate drilled for one patch of sky and one targeting
       programme, and the class mix follows the programme: quasars are 3-11% of each year's spectra in 2000-2009,
       14-16% in 2010-2013 and 31-46% from 2014 on.
     - The random split trains on the test object's plate-mates (99.5% of test objects have one) and on later
       programmes: on the same spectra of 2012-2020, untuned LightGBM scores log loss 0.391 under it against 0.506
       when each year is predicted from the years before, and the sky position, which helps under the random split,
       hurts on later years.
     - A classifier in use is trained on the spectra taken so far and labels objects the survey has not yet observed,
       so the split should follow the date of the spectrum (the raw file's MJD, which the definition drops), which
       also holds out the test object's plate: predict each year from 2012 to 2020 from the years before it[^2a]?
   * **Background:**
     - A plate is an aluminium disc for one patch of sky, "a radius of 1.49 deg", drilled with "holes corresponding to
       the sky positions of objects in that area" and observed on one night or a few; SDSS plates held 640 fibres,
       BOSS plates 1,000 ([SDSS DR17, spectroscopic basics](https://www.sdss4.org/dr17/spectro/spectro_basics/)).
     - The programme observing chooses a plate's targets: the earlier SDSS programmes (2000-2009), BOSS ("Fall 2009 -
       Spring 2014", [BOSS](https://www.sdss3.org/surveys/boss.php)), mostly galaxies, and eBOSS ("July 2014 – March
       2019", [eBOSS](https://www.sdss4.org/surveys/eboss/)), whose targets include "500,000 quasars over 6,000 square
       degrees, 0.8 < z < 3.5". Stars are 62% of the 2008 spectra and 91% of the 2009 ones.
     - In the sample, 6,284 plates hold a median of 13 objects each; 11% of the rows sit on plates of one class only
       and 24% on plates at least 90% one class. Plates overlap: within one plate radius of an object lie objects of a
       median of 11 plates, so the position finds both plate-mates and objects of overlapping plates of the same
       programme.
     - The plate, the fibre, the date and the redshift are not features (issue 1); the date returns only as the time
       column of a split by year. No object appears twice: no two rows lie within 2 arcseconds of each other.
     - The survey published a data release about once a year (DR8 in January 2011 to DR16 in December 2019, [SDSS
       data releases](https://www.sdss.org/data-releases)), so a model refit at each release and used until the next
       predicts one year ahead.
   * **Effect on the task:** under the random split a model learns from spectra taken around the test object, through
     the same plates and by the same programme, and from programmes that came later; a classifier labelling objects
     without spectra has neither. The sky position shows it: added to the five magnitudes, it lowers LightGBM's loss
     under the random split (0.353 to 0.331) and raises it on later years (0.491 to 0.506), because it teaches the
     sky footprints of past programmes. A split by plate or by sky cell removes the plate-mates but still trains on
     later programmes; the split by year removes both.
   * **Experiments:** the Kaggle file re-downloaded on 2026-11-05, the definition's 99,999 objects and shipped
     features (position, five magnitudes, camera column). Untuned LightGBM (500 trees), logistic regression, the sky
     position alone (the 50 nearest objects), TabPFN 3.5 (10,000 training rows, up to 5,000 test rows, first
     repeat); log loss, lower is better:

     | Split | Class shares | Position alone | Logistic regression | LightGBM, magnitudes only | LightGBM, as shipped | TabPFN 3.5 |
     |---|---|---|---|---|---|---|
     | A: random objects, 3 x 3 folds | 0.955 | 0.791 | 0.656 | 0.353 | 0.331 | 0.294 |
     | B: by plate, 3 x 3 folds | 0.956 | 0.901 | 0.657 | 0.354 | 0.338 | 0.292 |
     | C: by sky cell of 10 degrees, 3 x 3 folds | 0.957 | 0.992 | 0.663 | 0.357 | 0.354 | 0.301 |
     | D: by year, 9 windows 2012-2020 | 1.121 | 1.169 | 0.755 (with the date) | 0.491 | 0.506 (0.540 with the date) | 0.439 (with the date) |

     - Same rows: on the 48,743 spectra of 2012-2020, LightGBM scores 0.391 out of fold under the random split and
       0.506 under D; on 2014 alone, the first eBOSS year, 0.441 against 0.530.
     - Later programmes: trained on a random draw of the other years (later ones included, as many rows) instead of
       the earlier years, LightGBM's loss falls on 2014 from 0.530 to 0.470 and on 2016 from 0.501 to 0.444.
     - The plate itself: under the random split, the class shares of a test object's plate-mates in training give
       0.744 alone, and added to LightGBM they take 0.331 to 0.320, so the position already recovers part of what the
       plate tells.
     - Sky cells of 5 and 20 degrees give LightGBM 0.345 and 0.373 and the position alone 0.942 and 1.019; the size
       of the cell sets the score.
     - D in detail: the windows train on 51% (2012) to 99.9% (2020) of the rows; 0 to 5 plates per window were also
       observed before it, with at most 90 test rows (0.9% of 2013); the windows 2019 and 2020 hold 935 and 141
       spectra. TabPFN beats LightGBM trained on the same 10,000 rows in 9 of 9 windows (0.439 against 0.729).
   * **Consistency:**
     - Lennart's audit of 2026-10-01 kept the random split because grouping by plate left the score nearly unchanged
       (0.340); the size of a gap never decides the split, the use does[^2b].
     - infrared_thermography_temperature kept a random split over a year-to-year shift, as a calibration should not
       depend on the day[^2c]; here the year sets which objects get a spectrum and the class mix, which a classifier
       meets anew with each programme, so D departs from it for that reason.
     - sarcoma kept random patients over tissue source sites because new patients come from the same sites; a new
       object here comes on a plate and a night that training does not have. covertype and the forced random splits
       stay random because they have no date or group to split by; this file has the date.
   * **Unknown:** how soon after a night the pipeline's class reached the team choosing the next targets; a public user
     waits for the next data release, about a year, which a one-year gap between training and test would
     simulate[^2d].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random objects (implemented) | 3 x 3 random folds over the 99,999 objects | every programme on both sides; LightGBM 0.331 | trains on the test object's plate-mates and on later programmes; the position helps here and hurts on later years; a classifier in use never has later spectra |
     | B | By plate | `plate` becomes the group column (not a feature); 3 x 3 folds over 6,284 plates | the source's own id for a pointing; a test object's plate is new; LightGBM 0.338 | still trains on later programmes; objects of overlapping plates of the same programme stay in training (position alone 0.901) |
     | C | By sky cell | cells of about 10 x 10 degrees as groups; 3 x 3 folds | a new region of sky; the position stops helping (LightGBM 0.354) | the cell size is our choice and sets the score (0.345 to 0.373); objects without spectra mostly lie in sky that has spectra; still trains on later programmes |
     | D | By year of the spectrum | the date from MJD as time column; 9 one-year windows 2012-2020, each trained on every earlier spectrum | the order in which the survey took its spectra and would refit a classifier; holds out the test object's plate too; the class mix moves as the programmes did; TabPFN 0.439, LightGBM 0.506, logistic regression 0.755 | part of the loss is a change of class mix no model can foresee; the date becomes a feature (untuned LightGBM 0.506 without, 0.540 with it); the 2019 and 2020 windows are small (935 and 141 spectra) |

   * **Recommendation:** D: the spectra are dated, and a classifier in use is trained on those taken so far and
     labels objects not yet observed; the year split also holds out the test object's plate, so the position can no
     longer recognise it[^2e]. **Decision:** random objects (A), by plate (B), by sky cell (C) or by year (D)?

   **Notes for the AI:** on D, in `dataset.py`:
   - `_clean`, before the drop: `df["date"] = pd.to_datetime(df["MJD"], unit="D", origin=pd.Timestamp("1858-11-17"))`;
     `MJD`, `plate` and `fiber_ID` stay in the drop list, with the MJD comment changed to "observation date, now the
     time column `date`".
   - `temporal = Temporal(on="date", splits=TemporalSplits(window=1, unit="years", n_windows=9,
     min_train_fraction=0.5))` (windows 2020 back to 2012; the 2012 window trains on 51.3% of the rows), imported
     from `data_foundry.v2`; `_feature_types` returns `FeatureTypes(categorical=["cam_col"], datetime=["date"])`.
   - `splits_comment`: "Nine one-year windows, 2012 to 2020, newest first; each trains on every spectrum taken before
     it, as a classifier refit at each yearly data release (DR8, January 2011, to DR16, December 2019) would. No
     gap. The 2019 and 2020 windows hold 935 and 141 spectra."
   - `task_summary.split`: "Later spectra: each year from 2012 to 2020 is predicted by a model trained on every
     spectrum taken before it, as the survey's classifier would be refit at each data release and used on the
     objects observed next." Add to `fit_reason`: each programme picked its own kind of object, so the class mix of
     later years differs (quasars 15% of the spectra in 2010-2013, 31-46% from 2014 on).
   - `curation_comments`: a split bullet with the table's numbers (A 0.331, D 0.506; same rows 0.391 against
     0.506; position +0.015 under D, -0.022 under A; 0 to 90 test rows on plates seen before).
   - Then `dataset check`, a CHANGELOG entry, and the record: `required_split: Temporal (NON-IID)` and a
     `CC (2026-11-05, Andrej):` line with the reason.
   On B: `grouping = Grouping(on="plate", labels="per_sample", definition=...)` quoting the spectroscopic basics page,
   `plate` out of the drop list. On C: a cell id built in `_clean` from declination bands of 10 degrees and right
   ascension bins of 10 / cos(declination) degrees, as the group column.

   [^2a]: **SPLIT-1** (Must): the split is the one that most closely mirrors the real-world application.
     **SPLIT-3** (Must): a non-IID task is grouped or temporal, never both, and the use case decides which; a temporal
     split holds the test rows strictly after the training rows (SPLIT-2). **SPLIT-7** (Must): a missing or hidden
     timestamp does not make a task IID.
   [^2b]: **SPLIT-4** (Must): the split follows what the task does in reality, not the size of the gap; if the
     deployed model predicts for an entity new data would not contain, the test entities must be new, even when a
     random split costs little. **SPLIT-29** (Must): an IID split is wrong when many rows share an entity that new
     data would not have and the entity carries the label; **SPLIT-30** (Must): re-split when the source calls the
     column an id or the use case predicts for new entities.
   [^2c]: **SPLIT-31** (Should): over related entities, IID can match how a task is framed even when it is
     optimistic; such a task is a candidate for a grouped or temporal variant (infrared_thermography_temperature,
     2026-10-21, Lennart; sarcoma under SPLIT-29, 2026-10-22, Lennart).
   [^2d]: **SPLIT-10** (Should): when a label is known only some time after its row, train on the rows whose label is
     known by the window's start, with a gap of about the label's delay.
   [^2e]: **SPLIT-11** (Should): train on everything before the window; **SPLIT-12** (Should): the horizon is the
     refit cadence or the source's own, here the yearly data release; **SPLIT-14** (Must): at least 3 windows, no train
     side below 50% of the data; **SPLIT-15** (Should): as many windows as a task of that size gets folds (3 x 3).
     **LEAK-10** (Must): pointing ids that encode the pre-selection or the observation date are no features, so the
     plate stays out; the date comes back only as the time column, which a temporal task's models get.

   **Andrej (2026-11-05, discuss):** I am very certain that this cannot be a random split.. Think harder again.

   **Answer (AI, 2026-11-06):** the recommendation is the year split (D), not a random one; the time framing below
   is why.

   * **When each part of a row arrives:** the features come from the imaging, which precedes any spectrum (the raw
     file's `run_ID`, dropped, names the imaging run); the class arrives with a spectrum taken on a dated night (MJD,
     2000 to 2020) through a plate a programme drilled for its own targets. So the target comes after the features, at
     a delay that differs from object to object, and which objects get a target at all depends on the year.
   * **Where the time-basis questions lead:** the first question stops at `Timeless`, since the class is a fixed
     property of the object. But the use case labels objects the survey has not yet observed, and what moves with the
     year is which objects get a label (quasars 3-11% of the spectra before 2010, 31-46% from 2014 on) and how the
     features relate to it (the sky position helps under the random split and hurts on later years). Asked of the
     samples, the fourth question answers yes, and the time is dated: the split is temporal, D. `Timeless` would have
     justified the random split by the target alone and missed the drift of the catalogue[^2f].
   * **What follows for D:** a temporal split needs no time-basis tag (issue 4), and the record's collection facts
     should say the spectra arrived over time, dated (issue 5). A public user gets the classes with the next data
     release, up to a year after the night; the yearly windows already train only on spectra taken before each year,
     and whether a further gap is due stays under Unknown, as no measurement here moves D.

   [^2f]: **SPLIT-32** (Should): the prototypes, by the questions that tell them apart: `Timeless` when the target is a
     fixed property of the item; when samples arrive over time and the target, how often it occurs or its relation to
     the features moves with the period, and the time is dated, the split is temporal (SPLIT-7, SPLIT-14).

   **Andrej (2026-11-11, discuss):** Agree.

   **Resolved (2026-11-11, Andrej):** D applied. `MJD` becomes the time column `date` in `_clean` and stays out of
   the features as an id; `Temporal(on="date", splits=TemporalSplits(window=1, unit="years", n_windows=9,
   min_train_fraction=0.5))` gives the nine calendar-year windows 2012 to 2020, each trained on every earlier
   spectrum (51,256 to 99,858 training rows, 51.3% to 99.9%; 141 to 11,044 test spectra), no gap. The 935 and 141
   spectra of 2019 and 2020 stay above SPLIT-17's 50 test rows, so the years are not merged, and nine windows is
   what SPLIT-15 gives a task of this size. `task_summary` (`known`, `split`, `changes`, `fit_reason`),
   `splits_comment` and the curation comments restated with the table above; the check's
   `meta_time_horizon_mismatch` is accepted, as DR17's spectra end on 2020-03-24 and the newest calendar-year window
   spans 38 days. `dataset check` 0 errors, 0 warnings (1 accepted); record `required_split` Temporal (NON-IID), tag
   `Non-IID (Temporal)`, `CC (2026-11-11, Andrej)` line.

3. **Keep the photometric task, or build one from the recovered spectra?**

   * **Problem:**
     - The shipped features are not a spectrum but five broad-band brightnesses from the survey's images (the
       catalogue's model magnitudes u, g, r, i, z, identical to those in the spectrum files on 36 of 36 rows), the sky
       position and the camera column; the spectrum gives only the label, the class the pipeline fitted to it
       together with the redshift, which the definition already drops.
     - The spectra can be recovered: plate, night and fibre identify every row's spectrum in the DR17 catalogue
       (99,999 of 99,999 rows, with the same class and redshift), and the survey's public archive serves them at
       about 0.2 MB each, about 20 GB for all.
     - A spectral task would ask a model to redo the fit that sets its own label, as the redshift shows (alone it
       takes log loss from 0.955 to 0.159; with the photometry 0.086 against 0.331 without), so the AI recommends
       keeping the photometric task as defined: keep it, put the redshift back, or build a spectral dataset?
   * **Background:**
     - The Kaggle page explains the question: it says the dataset "aims to classificate stars, galaxies, and quasars
       based on their spectral characteristics", while its column list calls u to z a "filter in the photometric
       system" and the redshift a "redshift value based on the increase in wavelength"
       ([Kaggle](https://www.kaggle.com/datasets/fedesoriano/stellar-classification-dataset-sdss17)).
     - Photometry is the brightness through five filters from the ultraviolet (u) to the near-infrared (z), one
       number per object and filter. A spectrum is the light split by wavelength: 4,216 to 4,638 flux values from
       about 3,560 to 10,390 Å for the BOSS and eBOSS spectrographs, 3,741 to 3,839 values from about 3,800 to 9,200 Å
       for the earlier SDSS one, each spectrum on a log-wavelength grid that starts at its own wavelength.
     - The pipeline fits each spectrum with star, galaxy and quasar templates, so the class and the redshift are two
       outputs of one fit ("the automated spectral classification, redshift determination, and parameter measurement
       pipeline", [Bolton et al. 2012](https://arxiv.org/abs/1207.7326)); stars are fitted only within 1,200 km/s,
       so a redshift of at most 0.0041 in size holds for 99.95% of the stars and 0.65% of the other objects.
     - Each spectrum is a file `spec-<plate>-<mjd>-<fiber>.fits` in
       `https://data.sdss.org/sas/dr17/<sdss or eboss>/spectro/redux/<run2d>/spectra/lite/<plate>/`, with run2d 26,
       103 or 104 for the earlier plates and v5_13_2 for BOSS and eBOSS; the catalogue
       `specObj-dr17.fits` (6.7 GB, in `https://data.sdss.org/sas/dr17/sdss/spectro/redux/`) names each one's run2d.
       The SkyServer SQL service, which astroquery.sdss calls, did not answer from our machine; the file archive did.
       The data are public domain (see the record judgment).
     - A spectrum file also holds the pipeline's best-fit model spectrum and the programme's targeting flags, which
       give the label or the selection away.
   * **Effect on the task:** as defined, a model sees what a classifier for objects without spectra sees, and the
     class arrives later with a spectrum: the photometric classification the use case names. With the redshift or
     the spectrum, the model reads the measurement the label is fitted from, which exists only once the spectrum is
     taken, when the pipeline already gives the class. With the redshift the choice of split also matters less
     (LightGBM 0.086 random against 0.172 by year), since the redshift carries the class in every programme; without
     it the year split shows what the programmes change (0.331 against 0.540).
   * **Experiments:** the Kaggle file and DR17's catalogue and spectrum files, downloaded on 2026-11-06; log loss,
     untuned LightGBM, logistic regression and TabPFN 3.5 as in issue 2 (TabPFN on another draw of 5,000 test rows
     under the random split); the year split is issue 2's D, with the date as a feature:

     | Features | Random, 3 x 3: LightGBM | Logistic regression | TabPFN 3.5 | By year, 9 windows: LightGBM | Logistic regression | TabPFN 3.5 |
     |---|---|---|---|---|---|---|
     | as defined (position, magnitudes, camera column) | 0.331 | 0.656 | 0.285 | 0.540 | 0.755 | 0.439 |
     | as defined + redshift | 0.086 | 0.148 | 0.068 | 0.172 | 0.250 | 0.131 |
     | redshift alone | 0.159 | 0.205 | | 0.289 | 0.306 | |
     | class shares | 0.955 | | | 1.121 | | |

     - Recovery: the catalogue matches every row by plate, night and fibre (99,999 of 99,999, one match each, all
       the object's primary spectrum), with the same class, the redshift within 0.00001 and the position within one
       arcsecond for 99.7%. 36 spectrum files fetched one by one (4 per period and class) match their rows; 2,998 of
       3,000 more came in about five minutes over 16 connections (two connection resets), 587 MB.
     - The spectral task on those 2,998 rows (each spectrum in 100 bins from 3,800 to 9,200 Å, divided by its median,
       5 random folds): LightGBM log loss 0.427 and accuracy 93.4% (96.3% on spectra without a pipeline warning,
       61.2% on those with one); the photometry of the same rows 0.595 (81.6%), photometry and redshift 0.173
       (97.8%).
   * **Also found:** the pipeline flags 8.2% of the rows' fits with a warning (`ZWARNING` not 0, mostly a small
     chi-square difference between the two best fits): 6% of the galaxies, 14% of the quasars and 9% of the stars,
     2-5% of each year's spectra before 2010 and 11-26% from 2014 on. The Kaggle file has no warning column, so
     these classes ship as certain; whether to drop them is a decision of its own, raised here and not in the
     options.
   * **Consistency:**
     - The redshift was dropped on 2026-10-01 (Lennart) for the reason the rule on labels the field defines by shipped
       measurements gives: drop the defining columns when the rest is a real task, otherwise retire. The same rule
       retired audiology_diagnosis and biomechanical_orthopaedic_prediction (2026-11-05, Andrej); here the photometry
       left after the drop is the real task of classifying objects without spectra[^3a].
     - The spectral datasets of the copy (pancreatic_cancer_mouse_detection, micro_mass, open_soil_spectral_library)
       ship spectra whose label comes from elsewhere (the mouse's diagnosis, the strain's species, the soil's lab
       analysis); here the label is fitted from the spectrum itself[^3b].
     - Magnitudes are the camera's reading of a physical quantity, which the rules count as a tabular measurement,
       not an image descriptor[^3c].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Photometric task as defined (implemented) | position, five magnitudes and camera column; redshift, plate, fibre and date dropped | the use the definition names: classify objects without a spectrum; no column comes from the label's own fit | the class arrives with a spectrum that a programme chose to take (`Selection Bias`) |
     | B | Put the redshift back | adds `redshift`, as TabArena v0.1 shipped it | the column the Kaggle file has | the redshift and the class come from one fit, and the redshift alone gives 0.159; a spectrum must exist first, and then the pipeline already gives the class |
     | C | A spectral dataset instead | the 99,999 spectra (about 20 GB) on one wavelength grid as a declared spectrum; the pipeline's class as label | real, recoverable, public-domain spectra | the label is the template fit of the same spectrum, so models learn to imitate the pipeline; no decision waits on it; the photometric task leaves |
     | D | A, and the spectra as a separate record | A ships; a new record screens the spectral task | keeps the photometric task | the spectral record meets C's problem; 20 GB to fetch and put on one grid for a task the rules exclude |

   * **Recommendation:** A: the features are photometry, the spectrum is where the label comes from, and the use is
     to classify an object before its spectrum exists; a spectral task would need a label that is not fitted from
     the same spectrum. **Decision:** as defined (A), with the redshift (B), spectra instead (C), or both (D)?

   **Notes for the AI:** on A, the data stay; add to `curation_comments`: "u, g, r, i, z are the SDSS model
   magnitudes (equal to `MODELMAG` in the DR17 spectrum files); the spectra are not in the file: they set the label,
   class and redshift being two outputs of one template fit (Bolton et al. 2012)", and a `CC (<date>, Andrej):` line
   in the record. On B, take `redshift` out of the drop list and its curation bullet; the record then departs from
   the rule on labels defined by shipped measurements and needs an exception text. On C or D, screen a new record
   first; the spectra come from the archive pattern above with the run2d from `specObj-dr17.fits`; every BOSS and
   SDSS spectrum lies on the log10 wavelength grid with step 0.0001, so a common grid is an offset in pixels; ship
   `flux` only, declared as a spectrum (Å, optical spectroscopy, state `processed`: sky-subtracted and
   flux-calibrated), never the `model` column or the targeting flags. The warning share needs its own issue if
   Andrej wants it decided.

   [^3a]: **SEL-19** (Must): a label the field defines by measurements that ship as columns is no prediction target;
     when the rest still makes a real task with a decision, drop the defining columns, otherwise the task is out
     (audiology_diagnosis, biomechanical_orthopaedic_prediction). **LEAK-10** (Must): a value fitted from the same
     measurement that gives the label is no feature (sdss_17 `redshift`, in the Mechanisms table).
   [^3b]: **CLEAN-26** (Should): a spectrum ships as the source publishes it, one column per position, declared as a
     spectrum; the spectrum guide's cases are spectra measured on a specimen whose label comes from another test.
     **SEL-3** (Must): the dataset simulates a decision someone makes with the prediction.
   [^3c]: **SEL-15** (Must): a physical quantity measured through an imaging device and used by the field as the
     instrument's reading is a measurement, not an image descriptor (**SEL-13**).

   **Andrej (2026-11-05, discuss):** Wait, is this actually spectral data? Can we recover the original spectra?

   **Resolved (2026-11-11, Andrej):** A (ok): the photometric task stays as defined; `curation_comments` now says that u to z
   are the SDSS model magnitudes and that the spectra, recoverable from DR17, set the label (one template fit gives class
   and redshift). No spectral record is opened; the data are unchanged.

4. **Time basis: no tag under the year split; `Timeless` only if a split that is not temporal stays?**

   * **Problem:**
     - The spectra that give the class were taken 2000 to 2020 on dated nights, and the class mix moves with the
       programme observing; issue 2 recommends predicting each year from the years before it.
     - The definition's random split names no time basis; a temporal split needs none, while a random, plate or sky
       split would need one, and the only prototype that fits it is `Timeless`, since the class is a fixed property.
     - Follow issue 2 and set no tag, or, if a split that is not temporal stays, name it `Timeless` with a line that
       states the drift[^4a]?
   * **Background:** `Timeless` says time cannot affect the target; here the target of an object does not move, but the
     objects that get one do, so a `Time basis:` line under `Timeless` must say that the split tests the catalogue
     as a whole, not the objects observed next. `Snapshot` (filling in the finished imaging catalogue) would fit a
     cataloguing use, but the definition's use labels objects without spectra as the survey goes on, and the class
     mix of the next objects is not that of the past ones.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random split, no time basis (implemented) | as now | nothing to change | a split that is not temporal on a dated, drifting source, with no stated reason |
     | B | Year split, no tag | issue 2's D; a temporal split carries no time basis | follows the use case and the dated source; nothing to justify | depends on issue 2 |
     | C | Split that is not temporal, `Timeless` | issue 2's A, B or C kept; the tag and a line that the class is fixed while the programmes picked different objects over 2000-2020 | the target is a property; the line names the drift | the prototype rests on the target only, and the drift it names is what the split does not test |
     | D | Split that is not temporal, `Snapshot` | as C with `Snapshot`, the line naming the imaging catalogue as the one period filled in | reads the use as filling in one catalogue | the definition's use labels objects observed later; the class mix moves with the year |

   * **Recommendation:** B, with issue 2's D. If a split that is not temporal stays, C, with the drift in its line.
     **Decision:** A, B, C or D?

   **Notes for the AI:** on B, nothing beyond issue 2's notes (`data_tags` stays as it is; the class sets `Non-IID`,
   `Temporal` from the windows). On C, once PR #50 is in: `data_tags = ("Timeless",)` and a curation bullet `- Time
   basis: Timeless: an object's class is a fixed property, but the programmes observing from 2000 to 2020 chose
   different objects (quasars 3-11% of the spectra before 2010, 31-46% from 2014), so the split tests the catalogue as
   a whole, not the objects observed next; a split by year scores LightGBM 0.506 against 0.331 random.`; on D, the
   same with `Snapshot` and the imaging catalogue as the period.

   [^4a]: **SPLIT-32** (Should): a definition can name the use-case prototype it follows, with a `Time basis:` line;
     a temporal split is temporal and needs no tag. `Timeless`: the target is a fixed property of the item; `Snapshot`:
     the use case only fills in a time the data covers. When none fits, the dataset goes to the curator with the
     arrival facts rather than under the nearest tag.

   **Andrej (2026-11-11, change):** Option B: Year split, no tag.

   **Resolved (2026-11-11, Andrej):** B applied with issue 2's D: the definition declares no `data_tags` and no
   `Time basis:` line, as a temporal split carries no time-basis tag; the regime tags `Non-IID` and `Temporal` come
   from the task itself.

5. **Correct the record's collection facts: spectra over time, dated, the class after the imaging?**

   * **Problem:**
     - The rows are spectra taken from 2000 to 2020, each on a dated night (the raw file's MJD), chosen by programmes
       whose targets changed over the years; the features come from the earlier imaging.
     - The record carries only `Samples: No Time Dimension`, the fact for designed runs or a catalogue whose values do
       not depend on when an item was measured.
     - Set `Samples: Over Time` and `Time: Dated`, and `Target: Varying Delay` for a class that comes with a spectrum
       taken months to years after the imaging[^5a]?
   * **Background:** the class itself does not depend on the night, but which objects were measured does (issue 2's
     table: quasars 3-11% of each year's spectra before 2010, 31-46% from 2014), so the release is a dated stream, not
     a catalogue outside time. The delay tag records that the label is a follow-up measurement; it does not change
     issue 2's windows, which train on spectra taken before each year.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | `Samples: No Time Dimension` (implemented) | as now | the class does not depend on the night | hides a dated stream whose selection moves with the year |
     | B | `Samples: Over Time`, `Time: Dated` | the record's tags replaced | the source as it is; agrees with the year split | says nothing of when the class arrives |
     | C | As B, plus `Target: Varying Delay` | the third fact added | records that the class comes with a spectrum after the imaging, by a delay that differs per object | the delay matters little for the split chosen |

   * **Recommendation:** C: all three are facts of the source, whatever split is chosen. **Decision:** A, B or C?

   **Notes for the AI:** on B or C, in the record's `tags`: `'Samples: No Time Dimension'` becomes `'Samples: Over
   Time'`, plus `'Time: Dated'` (and `'Target: Varying Delay'` on C); `Andrej` added to `checked_by`.

   [^5a]: **SPLIT-32** (Should): the record's collection facts: `Samples: No Time Dimension` (designed runs, or a
     catalogue of properties where it plays no role when an item was measured), `Samples: One Moment` or `Samples:
     Over Time`; for samples over time `Time: Dated` when the release or its source keeps the time; `Target: Varying
     Delay` when the target comes after a delay that differs between samples.

   **Andrej (2026-11-11, change):** Option C: As B, plus Target: Varying Delay.

   **Resolved (2026-11-11, Andrej):** C applied: the record's `tags` now hold `Samples: Over Time`, `Time: Dated`
   and `Target: Varying Delay` in place of `Samples: No Time Dimension`, with the reason in the
   `CC (2026-11-11, Andrej)` line; `Andrej` was already in `checked_by`.


6. **Should the date of the spectrum be a model input?**

   * **Problem:**
     - The prediction point is an object that has been imaged but not yet observed spectroscopically, so the date of
       its spectrum does not exist when the prediction is made: it arrives with the target[^6a].
     - The year split (issue 2, D) needs that date as its time column, and the framework ships a declared time column
       to models, so the task as implemented hands the actor a column the actor does not hold.
     - Measured, untuned LightGBM scores log loss 0.506 without the date and 0.540 with it; the lower score is not
       the reason to prefer either option, since what decides is whether the actor holds the column.
   * **Background:**
     - A declared time column is a model input: `feature_columns` excludes the target, the group columns and the
       scoring columns, and nothing else.
     - Declaring it a scoring column is refused: the bundle check `task_scoring_column_is_feature` is an error when a
       scoring column is the time or stratification column, and scoring columns are metric inputs, not a way to hide
       a feature.
     - Dropping the declared column from the shipped frame in `_make_splits` does not work either: `split_summary`
       reads `time_on` from the frame it is given and raises `KeyError: 'date'` (verified on 2026-11-11), so the
       README's split table cannot be built; the bundle checks themselves would pass, as every time check first asks
       whether the column is there.
     - All 60 temporal datasets of the working copy keep their time column in the frame, so there is no precedent
       either way. The one that comes closest, medical_facility_operational_data, keeps its time column as an input
       on purpose, the arrival rank being known at check-in, and drops only the helper columns its split step built.
   * **Effect on the task:** under B a model may read the date and learn which years hold which class mix, which the
     actor cannot do; under A the same windows score the same models without it, and the 0.034 log loss is the size
     of what the column adds.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Add the capability | a `feature=False` style field on `Temporal` and the task metadata, `feature_columns` excluding the column, a bundle check that it is set only on a temporal task, the documentation and a benchmark-side TODO | the actor's inputs are the model's inputs; the year split keeps its time column without handing it over | a framework change that reaches the benchmark side, so it is not applied by editing this folder; a new metadata field on every v2 task |
     | B | Ship as it stands (implemented) | the date stays the time column and a model input, with the prediction-point gap stated in the notes | nothing to build; the windows and every number in issue 2 stand | a model reads a column the actor does not hold; 0.540 against 0.506 is what it adds |

   * **Recommendation:** A, and not for this dataset alone: any task whose time column is the date of the label event
     rather than of the prediction has the same problem, so the capability would be used again wherever a label's
     date orders the rows[^6b]. Until it exists, B is what the folder ships, and the gap belongs in the notes.
     **Decision:** A or B?

   [^6a]: **USE-3** (Must): name the prediction point, when the model is used and what is known then; a value that
     did not exist at that point is a leak. **LEAK-10** (Must): a feature holds only what existed at the prediction
     point, and targeting or pointing ids that encode pre-selection or the observation date are out.
   [^6b]: **USE-6** (Must): anything known at the prediction point is a legitimate input, so the question is the
     actor's knowledge, not the score. **SPLIT-7** (Must): a missing or hidden timestamp does not make a task IID, so
     the answer is not to give up the year split.

   **Resolved (2026-11-12, Andrej):** A ("Option A: Add the capability. Also check whether other datasets might be
   affected"):

   * **Framework:** `Temporal(..., feature=False)` in `data_foundry.v2`; the container stores it as the task's
     `time_is_feature` (left out of the checksum and the saved JSON while True, so built containers keep verifying),
     `feature_columns` leaves the column out, and a non-temporal task cannot set it. The column stays in the frame,
     so the splits, `split_summary` and the README's split table work; the README shows `time_is_feature: false`
     and a line under Splits. Tests in `tests/test_v2_dataset.py` and `tests/test_curation_container.py`; the API
     in the knowledge-data-foundry `definitions.md`; a harness entry in `BENCHMARK_CHANGES_TODO.md`.
   * **sdss_17:** `feature=False`; `known`, `changes` and two curation bullets restated; record CC line. `dataset
     check`: 0 errors, 0 warnings (1 accepted), 8 features (was 9), the same nine windows.
   * **The other 64 temporal definitions:** in 7 the time column arrives with the target, so the actor does not
     hold it; each got the issue "Should the time column be a model input?", nothing changed there:

     | Dataset | Time column | What it is | Why the actor lacks it | Issue |
     |---|---|---|---|---|
     | apistox | `first_publication_year` | first literature year | screened before the bee test | 2 |
     | qsar_biodeg | `test_year` | year of the biodegradability test | screening decides whether to test | 3 |
     | qsar_tid_11 | `first_year` | year the potency was published | screened before synthesis | 4 |
     | superconductivity | `first_year` | year the critical temperature was first reported | screened before synthesis | 3 |
     | california_house_prices_2020 | `time_index` | sale order | predicted at the listing | 8 |
     | coffee_rating_prediction | `review_date` | month the score was published | submission decided before review | 6 |
     | labour_inspection_compliance | `file_row` | inspection's place in the file order | inspection decided beforehand | 4 |

   * **Not affected (57):** the time column is the moment of prediction (application, order, purchase, booking,
     launch, quote, exam, admission, start of a period), or the date the use case predicts for, which the actor
     sets: the sale month of a valuation (ames_housing, house_sales, melbourne_housing_market, miami_housing,
     perth_house_prices, sberbank_housing_market_forecasting, zillow_prize), the survey year of
     noaa_afsc_bottom_trawl_survey_cpue, the forecast time of bias_correction and climate_model. Closest call:
     mercedes_benz_greener_manufacturing's `time_index` (the Kaggle id, read as the production order), which a car
     probably has before its bench test is planned; not opened.
   * **Claims:** all 7 are claimed by Andrej; none skipped.

7. **Test windows: keep the nine calendar years, merge 2019 and 2020, or end at 2018?**

   * **Problem:**
     - DR17 itself took fewer spectra after 2013 (579,078 in 2012, 56,989 in 2019, 5,957 in 2020), and the Kaggle file
       keeps 1.6% to 2.4% of every window's spectra with DR17's class mix within 4 points, so the windows shrink with
       the survey and the sample adds no selection by year or class.
     - The survey history explains each drop: BOSS used all the dark time until June 2014, eBOSS half of it from July
       2014 until it ended on 1 March 2019, and 2020 holds only 7 eFEDS plates of X-ray sources, observed on 20 to 24
       March before the observatory closed for COVID-19.
     - The one cost is the 2020 window, 141 spectra of one programme on 8 plates, whose LightGBM log loss has a
       standard error of 0.083 and 77% of the noise of the nine-window mean: keep it, merge 2019 and 2020, or end the
       windows at 2018[^7a]?
   * **Background:**
     - The file is SkyServer's own sample query (`PhotoObj` joined to `SpecObj`, the same 18 columns in the same
       order, [SkyServer SQL search](https://skyserver.sdss.org/dr17/SearchTools/sql)) cut at 100,000 rows with no
       filter: run today with `TOP 100000`, it returns 98,685 of the 100,000 Kaggle rows. The cut follows the order
       the database returns rows in, so the share per year wobbles (1.6% to 2.5% over 2000-2020, no trend) and the
       counts per plate clump (variance 9.5 times a random draw's).
     - "Both SEGUE-2 and BOSS were conducted using the dark time"; from 1 July 2014 APOGEE-2, MaNGA and eBOSS shared
       the telescope, "Using half of the dark time at APO, eBOSS ..." ([Blanton et al.
       2017](https://arxiv.org/abs/1703.00052)). eBOSS "concluded its observations of galaxies and quasars ... on
       March 1, 2019"; 12 eFEDS plates were meant "to be observed at APO during the first quarter of 2020", but
       "because of the COVID19-related closure of APO ... only a small fraction of the originally designed plates were
       observed"; "APO closed on the morning of March 24, 2020" ([Abdurro'uf et al.
       2022](https://arxiv.org/abs/2112.02026); 7 plates, [DR17 special
       plates](https://www.sdss4.org/dr17/spectro/special_plates/)).
     - Plates in DR17: 703 in 2012 (BOSS), 261 to 389 a year in 2016-2018 (eBOSS), 72 in 2019, 8 in 2020 (7 eFEDS,
       1 reverberation mapping).
   * **Experiments** (DR17 counts from SkyServer's SQL service on 2026-11-12, over the 4,618,753 spectra the query
     draws from; untuned LightGBM, 500 trees, on the shipped features without the date, each window trained on every
     earlier spectrum; standard errors from 2,000 bootstrap draws of plates; the last column is the paired standard
     error of the gap between LightGBM with and without the sky position, 0.015 on average):

     | Window | DR17 spectra | In the file (share) | Plates | Galaxies / quasars / stars, % (DR17) | Programme | LightGBM log loss (SE) | SE of a model gap |
     |---|---|---|---|---|---|---|---|
     | 2012 | 579,078 | 11,044 (1.9%) | 684 | 71 / 15 / 13 (71 / 15 / 13) | BOSS | 0.316 (0.008) | 0.004 |
     | 2013 | 474,146 | 9,843 (2.1%) | 566 | 70 / 16 / 14 (70 / 17 / 13) | BOSS | 0.347 (0.011) | 0.005 |
     | 2014 | 243,837 | 5,849 (2.4%) | 293 | 46 / 33 / 21 (45 / 35 / 20) | BOSS to June, eBOSS from August | 0.530 (0.018) | 0.007 |
     | 2015 | 159,733 | 3,364 (2.1%) | 185 | 39 / 41 / 20 (38 / 44 / 18) | eBOSS | 0.598 (0.022) | 0.009 |
     | 2016 | 211,992 | 4,873 (2.3%) | 262 | 43 / 44 / 13 (45 / 41 / 14) | eBOSS | 0.501 (0.014) | 0.005 |
     | 2017 | 257,923 | 5,989 (2.3%) | 329 | 59 / 31 / 10 (60 / 30 / 10) | eBOSS | 0.547 (0.012) | 0.006 |
     | 2018 | 314,285 | 6,705 (2.1%) | 388 | 42 / 44 / 15 (44 / 42 / 14) | eBOSS | 0.507 (0.011) | 0.004 |
     | 2019 | 56,989 | 935 (1.6%) | 64 | 39 / 45 / 15 (36 / 48 / 16) | eBOSS, 1 January to 1 March | 0.516 (0.025) | 0.009 |
     | 2020 | 5,957 | 141 (2.4%) | 8 | 43 / 45 / 13 (44 / 47 / 9) | eFEDS (139 rows), 16 February to 24 March | 0.690 (0.083) | 0.028 |
     | 2019-2020 merged | 62,946 | 1,076 (1.7%) | 72 | 40 / 45 / 15 (36 / 48 / 15) | eBOSS (87%), eFEDS | 0.537 (0.024) | 0.008 |

     | Windows | SE of the mean log loss | Share of its variance from 2020 |
     |---|---|---|
     | nine calendar years (as now) | 0.0105 | 77% |
     | 2019 and 2020 merged (eight) | 0.0056 | |
     | ending at 2018 (seven) | 0.0054 | |

     - No window is nearly one class; 2020 is one programme (139 of 141 rows eFEDS) in one field of about 140 square
       degrees, observed on 5 nights.
   * **Effect on the task:** each window is one fold of the benchmark with the same weight, so the 141 spectra of 8
     plates count as much as the 11,044 of 684. 2020 is also the hardest window (0.690 against 0.50 to 0.60 in the
     other eBOSS years): its X-ray targets come from a programme no training year has, a real change of programme
     measured on 8 plates, too few to tell apart two models 0.015 apart.
   * **Consistency:**
     - coffee_rating_prediction widened monthly windows of 2 to 72 reviews into two-month windows because the small
       ones doubled the confidence interval of a model comparison[^7b]; the rules also ask to widen newest windows that
       fall in an atypical stretch, and 2020 is one programme cut short by the COVID-19 closure[^7a].
     - The options rest on counts, programmes and noise. The mean scores differ (LightGBM 0.506 over nine windows,
       0.485 merged, 0.478 to 2018) only because 2020 is hard, which decides nothing[^7c].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Nine calendar years (implemented), the reason in `splits_comment` | the split stays; `splits_comment` says the sizes are DR17's and names the 2020 window | the yearly release cadence; nine windows; nothing to build | the 2020 window is 141 spectra on 8 plates of one programme; it holds 77% of the noise of the mean |
     | B | Merge 2019 and 2020 | eight windows: the years 2012 to 2018, then 1 January 2019 to 24 March 2020 (1,076 spectra, 72 plates), each trained on every earlier spectrum | every spectrum stays tested, the eFEDS programme included; the newest window's SE (0.024) is like the others'; SE of the mean 0.0056 | eight windows, not nine; a custom `_make_splits`, since declared windows have one length; the last window spans 15 months |
     | C | End the windows at 2018 | seven windows, 2012 to 2018; the 1,076 spectra of 2019-2020 are in no split | declared windows (`cutoffs`), no custom code; SE of the mean 0.0054 | drops the newest spectra and the eFEDS programme; seven windows; the windows no longer start at the newest data |

   * **Recommendation:** B: the windows shrink with the survey and the sample adds no bias, so only the 2020 window
     needs a change; merging widens it as the rules ask for small and atypical newest windows, keeps every spectrum
     tested and halves the noise of the mean[^7a]. **Decision:** A, B or C?

   **Notes for the AI:** on A, in `splits_comment` replace "Nine windows is what a task of this size gets as folds (3
   repeats x 3 folds), and the two smallest windows stay above the 50 test rows below which windows are widened, so
   the years are not merged." with "The sizes follow DR17, of which the file holds 1.6% to 2.4% a year: BOSS used all
   the dark time until June 2014, eBOSS half of it until 1 March 2019, and 2020 holds only 7 eFEDS plates observed
   before APO closed on 24 March 2020. The 2020 window (141 spectra, 8 plates, one programme) gives LightGBM's log loss
   a standard error of 0.08, 77% of the noise of the nine-window mean; kept for the yearly cadence (2026-11-12,
   Andrej)." On B: `temporal = Temporal(on="date", horizon=1, horizon_unit="years", feature=False)` without `splits`,
   and a `_make_splits` that sorts by `date` (stable, RangeIndex) and returns `{i: {0: (train, test)}}` for the window
   from 2019-01-01 to the end of the data, then [Y-01-01, Y+1-01-01) for Y from 2018 down to 2012, train = every row
   before the window's start (51.3% to 98.9% of the rows); `splits_comment` (eight windows, the sizes and the reason
   above), `task_summary.split` ("each year from 2012 to 2018, and January 2019 to March 2020 together, ..."), the
   accepted `meta_time_horizon_mismatch` text (the newest window spans 15 months), "9 windows" in the curation split
   bullet; then `dataset check`, a CHANGELOG entry and a `CC (<date>, Andrej):` line in the record. On C:
   `TemporalSplits(window=1, unit="years", cutoffs=tuple(range(2012, 2019)))`, `splits_rows_unused` accepted for the
   1,076 spectra of 2019-2020, the same texts and `dataset check`.

   **Andrej (2026-11-12, discuss):** Why do the test sizes keep getting lower and lower? This doesn't make sense? There
   might be a bias?

   **Answer (AI, 2026-11-12):** the survey took fewer spectra each year after 2013, and the sample adds no bias by year
   or class; the evidence and the options are above.

   * DR17 holds 579,078 spectra from 2012 and 5,957 from 2020: BOSS used all the dark time until June 2014, eBOSS half
     of it until 1 March 2019, and 2020 holds only 7 eFEDS plates, observed before the COVID-19 closure of 24 March
     2020.
   * The Kaggle file is SkyServer's sample query cut at 100,000 rows: 1.6% to 2.4% of every window's spectra, with no
     trend, and the class mix within 4 points of DR17's.
   * What it costs is noise: the 2020 window (141 spectra, 8 plates, one programme) gives LightGBM's log loss a
     standard error of 0.083; merging 2019 and 2020 (B) brings the newest window to 0.024.

   [^7a]: **SPLIT-17** (Should): widen windows that get too small; below about 50 test rows per window, use wider
     windows and fewer splits, as finer windows cut the test pool into smaller, noisier pieces. **SPLIT-20** (Should):
     check the history for breaks (COVID-19, a change of the data collection) and whether the newest windows fall in an
     atypical season, and widen them so most do not.
   [^7b]: **SPLIT-17** (Should), case coffee_rating_prediction: 26 monthly windows of 2-72 reviews doubled the
     confidence interval of a model comparison; 13 two-month windows hold 54-115.
   [^7c]: **SPLIT-21** (Must): decide neither the training history nor the windows from a comparison over a few test
     windows. **SPLIT-14** (Must): at least 3 windows, no train side below 50% of the data. **SPLIT-15** (Should): as
     many windows as an IID task of that size gets folds (3 x 3).

   **Andrej (2026-11-12, change):** Option B: Merge 2019 and 2020.

   **Resolved (2026-11-12, Andrej):** B: eight windows, newest first: 1 January 2019 to 24 March 2020 (1,076 test
   spectra, 72 plates, trained on 98.9% of the rows), then the calendar years 2018 to 2012, each trained on every
   earlier spectrum.

   * `dataset.py`: `Temporal(on="date", horizon=1, horizon_unit="years", feature=False)` without declared windows, and
     a `_make_splits` over `WINDOW_STARTS` (2019-01-01, then 1 January of 2018 down to 2012); `splits_comment` says
     why the last window spans two years (eBOSS ended on 1 March 2019, 2020 is 7 eFEDS plates before the COVID-19
     closure; standard error 0.083 alone, 0.024 merged); `task_summary.split` and `changes`; a sentence under the
     curation split table (it was measured on nine windows).
   * The accepted `meta_time_horizon_mismatch` is removed, not reworded: the newest window now spans 449 days, inside
     the check's band of half to twice the one-year horizon, so the warning no longer fires.
   * `dataset check` (sbatch): 0 errors, 0 warnings, 0 info; record: a `CC (2026-11-12, Andrej)` line.

     | README split table | Windows | Train rows | Test rows | Newest window |
     |---|---|---|---|---|
     | before | 9 | 51,256 to 99,858 | 141 to 11,044 | 16 Feb to 24 Mar 2020, 141 |
     | now | 8 | 51,256 to 98,923 | 1,076 to 11,044 | 1 Jan 2019 to 24 Mar 2020, 1,076 |

8. **Use DR17's full set of spectra instead of the Kaggle file's 100,000?**

   * **Problem:**
     - DR17 holds 4,618,684 objects with a spectrum and the file's photometry, 46 times the Kaggle file, and
       SkyServer's public SQL service returned all of them without an account in 11 queries (5 minutes, 760 MB).
     - Trained on every earlier spectrum instead of the file's rows, untuned LightGBM improves only from log loss
       0.509 to 0.483 (0.485 on the 1M rows a split may hold) and logistic regression not at all, while the test
       windows grow 42 to 61 times but 2020 stays 8 plates of one programme, which keeps most of the noise of issue 7.
     - Replace the Kaggle cut with DR17's full set, capped as `sdss_17_1m`, or keep the cut[^8a]?
   * **What the larger dataset is:**
     - The Kaggle file's own query (`PhotoObj` joined to `SpecObj`, the same 18 columns) without its cut at 100,000
       rows. `SpecObj` holds only the primary spectrum of each position (`sciencePrimary`: 5,112,724 of 5,801,200
       spectra); 4,618,753 of them have a photometric object, and dropping the 69 positions with two spectra leaves
       one row per object. Every Kaggle row is among them (99,999 of 99,999).

       | | Kaggle file (implemented) | DR17, full |
       |---|---|---|
       | Objects | 99,999 | 4,618,684 |
       | Galaxies / stars / quasars, % | 59.4 / 21.6 / 19.0 | 60.4 / 20.8 / 18.8 |
       | Raw file (18 columns, CSV) | 17 MB | 760 MB |
       | Frame (8 features, target, date), in memory | 12 MB | 550 MB |
       | Training rows per window, 2012 to 2020 | 51,256 to 99,858 | 2,314,762 to 4,612,727 |

   * **Feasibility:**
     - Fetch: SkyServer's SQL search (`https://skyserver.sdss.org/dr17/SkyServerWS/SearchTools/SqlSearch?cmd=<sql>&format=csv`)
       needs no account but refuses more than 500,000 rows ("error: limit is top 500000" for a 600,000-row query), so
       the pull runs over 11 ranges of nights (MJD) of at most 440,000 spectra, 13 to 34 s each, every count equal to
       DR17's count per night. CasJobs, the batch service without that limit, asks to "login or create an account"
       ([CasJobs](https://skyserver.sdss.org/CasJobs/)).
     - Reproducible: the queries name the release (`/dr17/`), so the same rows come back; the Kaggle cut cannot be
       redrawn (today's `TOP 100000` returns 98,685 of its rows, issue 7).
     - Licence unchanged: "All SDSS data released in our public data releases are considered in the public domain"
       ([SDSS image and data use policy](https://www.sdss.org/collaboration/image-use-policy/)).
   * **Experiments** (2026-11-12; untuned LightGBM, 500 trees, and logistic regression on the shipped features, no
     date; issue 2's year windows, each trained on spectra before it; scored on all of DR17's spectra of the window
     unless named; standard errors from 1,000 bootstrap draws of plates; three random draws for sizes up to 10%, which
     move LightGBM's mean by 0.004 to 0.006):

     | Training rows per window (mean of nine windows) | Rows | LightGBM | Logistic regression | Gap, logistic minus LightGBM (SE) |
     |---|---|---|---|---|
     | the file's rows (as now) | 80,252 | 0.509 | 0.772 | 0.263 (0.004) |
     | a random 2.2% of DR17 | 80,418 | 0.508 | 0.774 | 0.266 (0.004) |
     | 5% | 185,296 | 0.496 | 0.775 | 0.280 (0.004) |
     | 10% | 370,593 | 0.488 | 0.775 | 0.287 (0.004) |
     | 1M, the row budget | 1,000,000 | 0.485 | 0.775 | 0.290 (0.004) |
     | all | 3,705,931 | 0.483 | 0.775 | 0.292 (0.004) |

     | Window | Test spectra, file (plates) | Test spectra, DR17 (plates) | LightGBM SE on the file's test | SE on DR17's test | LightGBM, file's rows / all of DR17 |
     |---|---|---|---|---|---|
     | 2012 | 11,044 (684) | 579,075 (709) | 0.008 | 0.003 | 0.338 / 0.352 |
     | 2013 | 9,843 (566) | 474,140 (575) | 0.011 | 0.005 | 0.343 / 0.335 |
     | 2014 | 5,849 (293) | 243,837 (309) | 0.018 | 0.010 | 0.560 / 0.499 |
     | 2015 | 3,364 (185) | 159,730 (198) | 0.021 | 0.010 | 0.582 / 0.526 |
     | 2016 | 4,873 (262) | 211,990 (267) | 0.013 | 0.005 | 0.540 / 0.524 |
     | 2017 | 5,989 (329) | 257,920 (335) | 0.012 | 0.005 | 0.540 / 0.514 |
     | 2018 | 6,705 (388) | 314,284 (400) | 0.011 | 0.004 | 0.500 / 0.476 |
     | 2019 | 935 (64) | 56,989 (74) | 0.024 | 0.007 | 0.504 / 0.480 |
     | 2020 | 141 (8) | 5,957 (8) | 0.093 | 0.061 | 0.672 / 0.640 |
     | 2019-2020 merged | 1,076 (72) | 62,946 (82) | 0.024 | 0.011 | 0.520 / 0.495 |

     | Test rows (model trained on the file's rows) | SE of the mean, nine windows | Share of it from 2020 | SE of the mean, 2019-2020 merged | SE of the logistic-LightGBM gap, nine windows |
     |---|---|---|---|---|
     | the file's (as now) | 0.011 | 82% | 0.0055 | 0.009 |
     | DR17's | 0.007 | 91% | 0.0025 | 0.004 |

     - The file gives the same expected score: trained on its rows, LightGBM scores 0.504 on its test rows and 0.509
       on DR17's windows. With 8 plates the 2020 standard error is itself rough (issue 7 drew 0.083).
   * **Effect on the task ("more accurate"):**
     - Better models, by a little: LightGBM gains 0.024 at the budget, most of it by 10% of DR17, mainly in the
       eBOSS years (2014: 0.560 to 0.499), nothing in 2012; logistic regression gains nothing, so the gap widens from
       0.263 to 0.290 and LightGBM leads in 9 of 9 windows at every size. A classifier in use trains on every
       spectrum taken so far, not on 2.2% of them, so the larger training side is also closer to the use case.
     - A more reliable score, except in 2020: the SE of a model gap halves (0.009 to 0.004), but 2020 stays 8 plates
       of one eFEDS field and its SE falls only from 0.093 to 0.061, since the plates vary, not the spectra; so the
       larger set does not make issue 7's merge unnecessary (SE of the mean 0.0025 with both, 0.007 without the merge).
   * **Consistency:**
     - Better versions: a version the source itself defines replaces the current one, a fix of our own invention does
       not[^8a]; the full set is the source's own release, the 100,000 a third-party cut in database order.
     - Same record: the origin (DR17), the columns and the units stay, and the record already names DR17 as the
       source, so the record stays; only a rebuild from other sources is a new dataset[^8b]. The cut and the full set
       give the same task, so only one ships[^8c] (`stellar_classification_dataset_sdss17` already marks the Kaggle
       page as a duplicate).
     - Size: training sides of 2.3M to 4.6M exceed the budget of 1M training and 500k test rows per split, so the
       full set ships only as `sdss_17_1m`, each window training on a random 1M of the earlier spectra[^8d]; the copy
       has 19 such versions, nyc_taxi_trip_duration_1m among them under its record nyc_taxi_trip_duration.
   * **Cost:** each method trains on 9M rows over the nine windows instead of 0.72M (12 times) and predicts 2.2M
     test rows instead of 49k (46 times; 2012 capped at 500k). LightGBM took 12 s per window on 16 CPUs at 1M rows
     against 7 s at the file's size, logistic regression 6 s against 1 s (fit and prediction on DR17's window). The
     benchmark's TabPFN 3.5 "accepts up to 1,000,000 rows" (its wrapper) and runs on GPUs, as for the other `_1m`
     datasets; a model's input cap is no curation argument[^8e].
   * **Unknown:** how TabPFN 3.5 and the tuned methods move at 1M training rows (issue 2: TabPFN 0.439 on 10,000 rows,
     with the date); that needs GPU runs.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Kaggle cut (implemented) | 99,999 objects from the Kaggle file; the windows of issue 7 | nothing to build; cheap for every method; the same expected score (0.504 against 0.509 on DR17's windows) | 2.2% of what the source offers; a cut that cannot be redrawn; a model gap measured half as precisely; LightGBM 0.024 worse |
     | B | DR17's full set as `sdss_17_1m` | 4,618,684 objects from 11 SkyServer queries; each window trains on a random 1M earlier spectra and tests on up to 500k; same record, task and windows; the Kaggle definition leaves | the source's own release, fetched again exactly; LightGBM 0.485; test windows 42 to 61 times larger; the SE of a model gap halves | 12 times the training rows and 46 times the test rows per method; a query service instead of one file; 2020 stays 8 plates |
     | C | A random 10% of DR17 as `sdss_17` | 461,868 objects drawn once with a fixed seed; no `_1m` (training sides 231k to 461k) | most of the model gain (LightGBM 0.488 at 10%); no row cap; 4.6 times the file | a fraction of our own choosing; test windows only 4.6 times the file's; 2020 stays 8 plates |

   * **Recommendation:** B, with issue 7's merge: the source offers the whole release under the same public-domain
     terms and it can be fetched again exactly, a classifier in use trains on all spectra taken so far, and every
     window but 2020 gets a far more precise score; the model gain is small, and the cost is that of the other `_1m`
     datasets[^8a]. **Decision:** keep the Kaggle cut (A), DR17's full set as `sdss_17_1m` (B) or a 10% draw (C)?

   **Notes for the AI:** on B, the definition moves to a new folder `sdss_17_1m/` (`unique_name = "sdss_17_1m"`,
   `version_of = "sdss_17"`, a `version_comment` with the sizes and the budget), `sdss_17/` keeps no definition (as
   nyc_taxi_trip_duration), and the record's `v2_path` follows. `download_description`: the query `SELECT p.objid,
   p.ra, p.dec, p.u, p.g, p.r, p.i, p.z, p.run, p.rerun, p.camcol, p.field, s.specobjid, s.class, s.z AS redshift,
   s.plate, s.mjd, s.fiberid FROM PhotoObj AS p JOIN SpecObj AS s ON s.bestobjid = p.objid WHERE s.mjd BETWEEN <lo>
   AND <hi>` against the SQL search URL above, over 11 MJD ranges split at 52721, 53566, 54574, 55517, 55855, 56074,
   56385, 56935, 57713 and 58224 (51578 to 58932), one CSV each in `local-data-warehouse/sdss_17/`. `_load_raw`
   concatenates them (skip the `#Table1` line) and renames to the Kaggle names (`objid` to `obj_ID`, `ra` to `alpha`,
   `dec` to `delta`, `run` to `run_ID`, `rerun` to `rerun_ID`, `camcol` to `cam_col`, `field` to `field_ID`,
   `specobjid` to `spec_obj_ID`, `mjd` to `MJD`, `fiberid` to `fiber_ID`), so `_clean` stays; add
   `drop_duplicates(subset=["obj_ID"])` after the position drop (0 rows on the pull of 2026-11-12). Splits: with
   issue 7's A or C, `subsample_to_budget = True`; with its B, the custom `_make_splits` draws the samples itself
   (one random order of all rows, each window taking the first 1M earlier rows, and a random 500k of 2012's 579,075
   test spectra), as `subsample_to_budget` is refused next to a custom `_make_splits`. Texts: `task_summary.row`,
   `predicted` (galaxy 60.41%, star 20.83%, quasar 18.76%), `splits_comment`, `fit_reason` (quasars 14-17% of the
   spectra in 2010-2013), a curation bullet with the tables above, `source_links` plus the SQL search page. Then
   `dataset check` through sbatch, a CHANGELOG entry and a `CC (<date>, Andrej):` line. On C: the same download and
   loading in `sdss_17/`, `df.sample(frac=0.1, random_state=0)` after the cleaning, the same texts.

   **Andrej (2026-11-12, dataset note):** Another question: Why don't we use the larger dataset? Wouldn't that be more
   accurate?

   **Answer (AI, 2026-11-12):** more accurate in both senses, but the models gain little; the evidence and the
   options are above.

   * Better models: LightGBM's log loss falls from 0.509 to 0.485 on the 1M training rows a split may hold; logistic
     regression does not move, so the gap between them widens a little and holds in every window.
   * A more reliable score: DR17's windows hold 42 to 61 times the file's spectra and halve the noise of a model
     comparison, but 2020 stays 8 plates of one programme, so issue 7's merge is still needed.
   * The full set is public domain and is fetched again exactly in 11 queries without an account; over the row budget
     it ships as `sdss_17_1m` (B).

   [^8a]: **TP-6** (Must): keep apart whether a task is valid and whether it is the best version; a valid task
     stays, a better version the source itself defines replaces the current one, and a fix of our own invention is
     not a better version.
   [^8b]: **PROV-14** (Must): a repair stays under its record, with the same units and features; only a rebuild from
     other sources (new data, new units or new columns; PROV-11) is a new dataset with its own record.
   [^8c]: **PROV-6** (Must): versions or cuts of one underlying dataset are duplicates when neither adds a distinct
     task, added or dropped rows included.
   [^8d]: Row budget (knowledge-data-foundry `definitions.md`, "Larger than the row budget"; Lennart, 2026-10-21): at
     most 1M training and 500k test rows per split; a dataset whose splits have a larger side ships only as
     `<name>_1m` with `version_of` and a `version_comment`; in a temporal one the windows are built on all rows, then
     each train side is a random 1M of the earlier rows and each test window at most 500k.
   [^8e]: Principles, the tension of width against model limits: "a model's input cap is never an argument" (coad,
     Lennart, 2026-10-15).

   **Andrej (2026-11-12, change):** For now we keep the sdss dataset, but I want you to add a curation record for the
   larger dataset to be considered for inclusion as well.

   **Resolved (2026-11-12, Andrej):** A for now: `sdss_17` stays the Kaggle cut (99,999 objects, issue 7's eight
   windows); nothing changed in `dataset.py` for this issue. DR17's full set has its own record,
   [`sdss_dr17_star_galaxy_quasar`](sdss_dr17_star_galaxy_quasar.md): 4,618,684 objects
   (`SpecObj`, `sciencePrimary`, joined to `PhotoObj`), the 11 SkyServer queries, public domain, a `_1m` version as
   it exceeds the row budget; `TBD -> Yes`, priority 3, `Selection Bias`, claimed by Andrej (triage). Its CC line
   holds this issue's evidence; `sdss_17`'s record links it in a `CC (2026-11-12, Andrej)` line.

## Reference

fedesoriano. (January 2022). Stellar Classification Dataset - SDSS17. Retrieved [Date Retrieved] from https://www.kaggle.com/fedesoriano/stellar-classification-dataset-sdss17.
