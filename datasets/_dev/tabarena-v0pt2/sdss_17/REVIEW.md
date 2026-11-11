# sdss_17

**Outcome:** added. A 100,000-object sample of the Sloan Digital Sky Survey's Data Release 17 (shared on Kaggle):
whether an object is a galaxy, a star or a quasar, as the survey's spectroscopic pipeline classified it, predicted from
its sky position, its brightness in the five colour bands of the survey's images and the camera column; random splits.
The AI recommends shipping it as the photometric task it is (issue 3: the spectra can be recovered, but they set the
label) with the split changed to the year of the spectrum (issue 2, 2026-11-05; earlier: as defined). Reviewed without a
panel, from the gathered evidence: the record, the curator's leak-audit decision of 2026-10-01 and a model run on
TabArena's copy, which still had the redshift, plate and fibre; the split and the spectra were checked on the Kaggle
file and DR17's own files on 2026-11-05 and 2026-11-06. Validity: the redshift (fitted together with the class) and the
plate and fibre (which record how the object was chosen for a spectrum) are dropped, so the task is classification from
the images; every object was chosen for a spectrum by its colours, which the `Selection Bias` marker and the approximate
fit state. Value: the curator's photometric probe reaches log loss about 0.33 (ROC AUC about 0.96, untuned LightGBM);
the benchmark spread was measured with the redshift, which made stars trivial, so it does not carry over. Quality:
non-detections are stored as the asinh magnitude of zero flux (u 24.6346, g 25.1143, z 22.8269), which are real values
of the survey's magnitude system and stay; the one -9999 sentinel is set to missing. Weighed: a public survey with
documented classes and a real cataloguing use (+), the spectroscopic selection (-).

**Main points:** Ship (issue 1) as the photometric task it is, not as spectra, which can be recovered but set the
label (issue 3), with each year's spectra predicted from the earlier years instead of random objects (issue 2)? No
time-basis tag under the year split, `Timeless` only if a split that is not temporal stays (issue 4)? Record the
spectra as dated, over time, with the class after the imaging (issue 5)?

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
