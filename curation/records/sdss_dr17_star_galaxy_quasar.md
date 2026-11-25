---
unique_name: sdss_dr17_star_galaxy_quasar
name: 'SDSS DR17 optical spectra with photometry (SpecObj joined to PhotoObj): star, galaxy or quasar'
checked_by:
- AI (UNVERIFIED)
- Andrej
data_foundry_status:
- WIP (Triage)
claimed_by: Andrej
suggestion: TBD -> Yes
priority: 4
decision_markers:
- Selection Bias
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Varying Delay'
- 'Target: Revised Later'
- 'Features: Revised Later'
- Survey
original_source: Other
year: '2021'
collection_period: 2000-2020
domain: physics & astronomy
required_split:
- Temporal (NON-IID)
problem_type: Multiclass Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://skyserver.sdss.org/dr17/SearchTools/sql
- https://www.sdss4.org/dr17/
- https://doi.org/10.3847/1538-4365/ac4414
- https://skyserver.sdss.org/dr17/SkyServerWS/SearchTools/SqlSearch
v2_path: datasets/_dev/tabarena-v0pt2/sdss_dr17_star_galaxy_quasar_1m/dataset.py
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Collection facts (AI, 2026-11-25, /add-dataset):** `Target: Revised Later` added, measured: the class of a spectrum is refitted when the spectroscopic pipeline is rerun for a later release. The same 91,063 spectra (plate and fibre) of 5 December 2011 to 3 February 2012 (MJD 55900 to 55960) carry DR12's class (pipeline v5_7_0) and DR17's (v5_13_2) on SkyServer: 1,580 (1.74%) changed class (416 quasar to galaxy, 378 quasar to star, 298 galaxy to quasar, 295 star to quasar, 114 galaxy to star, 79 star to galaxy), 76% of them flagged by DR17's `zWarning`. The photometry of the same objects moved by at most 0.016 mag (5th to 95th percentile per band, the same for every class), so `Features: Revised Later` holds as screening set it, with no class-dependent shift. The shipped labels all come from DR17's reductions, so the windows train and test on labels of the same pipeline versions, not on the classes users had at each window's start.

**Screening (AI, 2026-11-25):** `TBD -> Yes`, priority 4: DR17's full set of optical spectra with photometry, 4,618,684 objects, is the source's own release of `sdss_17`'s task with 46 times the rows; under v0.2's row budget it would be added as `sdss_dr17_star_galaxy_quasar_1m` (this record keeps its plain name, the folder and `v2_path` take the suffix) and replace the Kaggle cut, which then retires as its `Duplicate` (PROV-6, TP-6).
- Source: SDSS-IV Data Release 17 (December 2021; Abdurro'uf et al. 2022, ApJS 259, 35); SkyServer's `SpecObj` (primary spectra, `sciencePrimary`) joined to `PhotoObj` on `bestobjid`. Measured 2026-11-25: SkyServer returned the same 4,618,753 spectra as the pull of 2026-11-12 (galaxy 2,790,253, star 962,162, quasar 866,338), 4,618,684 objects after the 69 repeated positions, 60.4 / 20.8 / 18.8% galaxy / star / quasar, all 99,999 Kaggle objects among them, the same 18 columns. Spectra dated 2000-02-04 to 2020-03-24 (MJD 51578 to 58932): the earlier block's 2000-03-05 is wrong. The photometry is not of the spectrum's date: DR17 adds no imaging ("Data Release 17 does not include any new or updated SDSS imaging data", sdss4.org/dr17/imaging), and its catalogue magnitudes carry DR13's recalibration ("the DR13 hypercalibration has been applied to the catalogs", sdss4.org/dr16/algorithms/fluxcal; Finkbeiner et al. 2016), so `Features: Revised Later` is added (zero points, not the class; an as-of note for LEAK-10).
- Use case: as `sdss_17`: an astronomer classifies imaged objects without a spectrum, to choose spectroscopic targets or build catalogues; fit approximate (`Selection Bias`: every row was picked for a spectrum by a targeting programme, whose mix changes by year); collection `Samples: Over Time`, `Time: Dated` (the night of the spectrum, `mjd`), `Target: Varying Delay` (the class comes with the spectrum, after the imaging); type `Survey` (a survey's data releases, SPLIT-34), as `sdss_17`.
- Split: leaf [L-ORDER.windows] because [SUR.meets] the surveyed population at a later round (yearly releases), [ORDER.order] the spectrum date is recorded, [ORDER.windows] eight windows hold, as `sdss_17`'s eight (2019-2020 merged, then 2018 to 2012), the date no input. Measured: training sides 2.3M to 4.6M, the 2012 window training on 50.1% of the objects (just above the half floor), test windows 62,946 to 579,075 (2012 capped at a random 500,000, `splits_test_over_budget`); 2020 stays 8 plates. Open: none beyond `sdss_17`'s decisions.
- Siblings and duplicates: `sdss_17` (`Yes`, shipped; the Kaggle file is SkyServer's sample query cut at 100,000 rows, so this record is a version of it, PROV-6; its issue on 2026-11-25 recommends B: keep it until `sdss_dr17_star_galaxy_quasar_1m` is built, then retire it); `stellar_classification_dataset_sdss17` (`No`, `Duplicate` of the Kaggle page); `desi_dr1_star_galaxy_quasar` (`TBD -> Yes`, 1: another survey, its own record, PROV-4); `happy_teddy_sdss_photo_z`, `sdss_mpajhu_bpt_class` (other tasks on SDSS data). External collections: TabArena carries the Kaggle cut only.
- Better data: found as better data for `sdss_17`. Nothing better found for this record: DESI DR1 (19.25M useful main-survey spectra, 2021-2022) measured 2026-11-25 as a far easier task with no change over its 13 months (LightGBM 0.107 to 0.128, class shares 0.72), so not better for this task; SDSS DR19 (2025) adds SDSS-V's about 4.18M optical spectra of 2020 onward (sdss.org/dr19/scope), but chosen by other programmes (Milky Way Mapper stars, X-ray sources) on another instrument, so not the same rows' kind; not checked whether they join `PhotoObj` (a lead for a later window, not a hit).
- Papers and pages: Abdurro'uf et al. 2022 (DR17); Blanton et al. 2017 (SDSS-IV programmes); Bolton et al. 2012 (class and redshift fitted in one step); SkyServer SQL search (https://skyserver.sdss.org/dr17/SearchTools/sql); the Kaggle page of the cut.
- Metric: none found (a data release; the DR17 paper and SkyServer define no prediction task), so the fallback `log_loss`, as `sdss_17` (MET-1). Inputs none.
- Baselines (measured 2026-11-25, `sdss_17`'s 8 features, eight windows, log loss, lower is better): untuned LightGBM 0.448 with v0.2's default sampler (1M from the newest years back) against 0.494 trained on the Kaggle file's rows; logistic regression 0.698 against 0.762; LightGBM leads in all eight windows. Random 5-fold on 300k rows 0.315, so the year windows (0.473) are the harder split.
- Risks for /add-dataset: over the row budget, so only the `_1m` version (each method 1M training rows per window and up to 500k test rows); drop `redshift`, `plate`, `fiber_ID` as `sdss_17` does; 155 rows with a -9999 magnitude to set missing; the fetch is 11 SkyServer queries of at most 500,000 rows (760 MB CSV; CasJobs needs an account); the photometry's DR13 recalibration post-dates the older spectra (LEAK-10, zero points only). Licence: public domain (SDSS image and data use policy).
- Priority: gap + (physics & astronomy thin: 1 accepted dataset, `sdss_17`), use case 0 (approximate, as `sdss_17`), source + (DR17 paper and SkyServer schema docs), shape + (4.6M objects, 8 features, dated); no known risk counted (better data none; the version question is the decision in `sdss_17`'s issue, not a risk of the data). Was 3 on 2026-11-12, which counted the version as a risk.

**Screening (AI, 2026-11-12):** `TBD -> Yes`, priority 3: DR17's full set of optical spectra with their photometry (4,618,684 objects), the release the shipped `sdss_17` (a 99,999-row Kaggle cut) is drawn from; the same photometric star, galaxy or quasar task with 46 times the rows, so only one of the two ships (PROV-6).
- Source: SDSS-IV Data Release 17 (December 2021; Abdurro'uf et al. 2022), SkyServer's public tables `SpecObj` (only the primary spectrum of each position, `sciencePrimary`: 5,112,724 of DR17's 5,801,200 spectra) joined to `PhotoObj` on `bestobjid`. As published: 4,618,753 spectra with a photometric object, 4,618,684 objects after dropping the 69 positions with two spectra; the Kaggle file's 18 columns (sky position, u, g, r, i, z model magnitudes, run, rerun, camera column, field, spectrum id, class, redshift, plate, night as MJD, fibre); target `class`: galaxy 60.4%, star 20.8%, quasar 18.8%; spectra of 2000-03-05 to 2020-03-24. All 99,999 Kaggle objects are among them.
- Use case: as `sdss_17`: an astronomer classifies objects that have images but no spectrum, to choose targets for spectroscopy or build catalogues; fit approximate (`Selection Bias`: every row is an object a targeting programme picked by its colours for a spectrum); regime temporal by the year of the spectrum, as decided for `sdss_17` (calendar years 2012 to 2018, then 2019-2020 as one window), the date no model input.
- Siblings and duplicates: `sdss_17` (`Yes`, shipped: the same query cut at 100,000 rows in database order; PROV-6, the curator decides which one enters, and on 2026-11-12 kept `sdss_17` for now); `stellar_classification_dataset_sdss17` (`No`, `Duplicate` of the Kaggle page); `desi_dr1_star_galaxy_quasar` (`TBD -> Yes`, 3: the same task on another survey, PROV-4); `happy_teddy_sdss_photo_z` and `sdss_mpajhu_bpt_class` (other tasks on SDSS data, PROV-7). External collections: TabArena carries the Kaggle cut, not this set.
- Better data: this record is the better data found for `sdss_17` (its REVIEW.md issue 8); no further search.
- Papers and pages: Abdurro'uf et al. 2022 (the DR17 paper); Blanton et al. 2017 (SDSS-IV, the programmes that set the class mix per year); Bolton et al. 2012 (the pipeline that fits class and redshift in one step); SkyServer SQL search (https://skyserver.sdss.org/dr17/SearchTools/sql).
- Metric: none found (DR17 is a data release; the DR17 paper and SkyServer define no prediction task), so the fallback `log_loss`, as for `sdss_17` (MET-1). Inputs none.
- Risks for /add-dataset: training sides of 2.3M to 4.6M rows exceed the row budget, so it ships only as `sdss_dr17_star_galaxy_quasar_1m` (each window a random 1M of the earlier spectra, at most 500k test rows; with the merged last window a custom `_make_splits` draws them, since `subsample_to_budget` is refused next to one); drop `redshift`, `plate` and `fiber_ID` as `sdss_17` does (the redshift is fitted with the class, the plate records the targeting); 155 rows with a -9999 magnitude to set missing; the fetch is 11 queries on a public SQL service that refuses more than 500,000 rows per query.
- Priority: gap + (physics & astronomy is thin, 0 accepted datasets counted, as `sdss_17` carries no domain; multiclass is thin), use case 0 (approximate, as `sdss_17`), source + (the DR17 paper and SkyServer's schema documentation), shape + (4.6M objects, 8 features, dated), risk - (a version of the shipped `sdss_17`, only one ships; the spectroscopic selection).

CC (2026-11-12, Andrej): record created to be considered for inclusion; `sdss_17` stays the Kaggle cut for now (`sdss_17` REVIEW.md issue 8, his words: "For now we keep the sdss dataset, but I want you to add a curation record for the larger dataset to be considered for inclusion as well"). Evidence from that issue, 2026-11-12:
- A version of `sdss_17`, not a new task: the Kaggle file is SkyServer's sample query cut at 100,000 rows in database order; all its 99,999 objects are here, with the same columns and a class mix within 1 point (galaxies, stars, quasars 60.4, 20.8, 18.8% against 59.4, 21.6, 19.0%), so only one of the two ships (PROV-6). This set is the source's own release and can be fetched again exactly; the Kaggle cut cannot be redrawn (`TOP 100000` today returns 98,685 of its rows).
- Fetch without an account: SkyServer's SQL search (https://skyserver.sdss.org/dr17/SkyServerWS/SearchTools/SqlSearch?cmd=<sql>&format=csv) refuses more than 500,000 rows per query, so the pull is 11 queries over ranges of nights (MJD 51578 to 58932, split at 52721, 53566, 54574, 55517, 55855, 56074, 56385, 56935, 57713 and 58224), 13 to 34 s each, 760 MB of CSV, every count equal to DR17's count per night: `SELECT p.objid, p.ra, p.dec, p.u, p.g, p.r, p.i, p.z, p.run, p.rerun, p.camcol, p.field, s.specobjid, s.class, s.z AS redshift, s.plate, s.mjd, s.fiberid FROM PhotoObj AS p JOIN SpecObj AS s ON s.bestobjid = p.objid WHERE s.mjd BETWEEN <lo> AND <hi>`. CasJobs, the batch service without the limit, needs an account.
- Licence: public domain: "All SDSS data released in our public data releases are considered in the public domain" (SDSS image and data use policy, https://www.sdss.org/collaboration/image-use-policy/).
- Over the row budget: training sides of 2,314,762 to 4,612,727 rows per yearly window (budget 1M training, 500k test rows per split), so it ships as a 1M-row version; per method 12 times the training rows and 46 times the test rows of `sdss_17` (LightGBM 12 s per window on 16 CPUs at 1M rows against 7 s).
- Small model gain (log loss, lower is better; untuned LightGBM with 500 trees and logistic regression on `sdss_17`'s 8 features without the date; nine yearly windows 2012-2020, each trained on earlier spectra and scored on all of DR17's spectra of the window):

  | Training rows per window | Mean rows | LightGBM | Logistic regression |
  |---|---|---|---|
  | the Kaggle file's | 80,252 | 0.509 | 0.772 |
  | a random 10% of DR17 | 370,593 | 0.488 | 0.775 |
  | 1M, the row budget | 1,000,000 | 0.485 | 0.775 |
  | all of DR17 | 3,705,931 | 0.483 | 0.775 |

- More precise scores, except in 2020: DR17's test windows hold 42 to 61 times the file's spectra and halve the standard error of a model gap over nine windows (0.009 to 0.004), but 2020 stays 8 plates of one programme (standard error 0.093 to 0.061), so the merge of 2019 and 2020 holds here too.
- Not measured: TabPFN 3.5 and the tuned methods at 1M training rows (GPU runs).

**Assessment (AI, 2026-11-25):** corrections to today's screening from the review panel of /add-dataset: the sibling line's `desi_dr1_star_galaxy_quasar` ("`TBD -> Yes`, 1") is `DF: Suspended` (CC 2026-11-05, Myunghwan: "Credible physical-class correctness above 90% has not been established for the intended population"), and its target is the same kind as this one, a survey pipeline's class (the consistency check under issue 1 of the review); the Split line's "Open: none beyond `sdss_17`'s decisions" no longer holds: the classes DR17 flags as unreliable (`zWarning`, issue 1) and the reason for no gap (the Horizon) are open. Changed since the screening, not corrected: the definition now drops the 19,581 spectra whose fibre carried no light (`zWarning` UNPLUGGED or NODATA) and adds the five PSF magnitudes, so the dataset holds 4,599,104 objects (68 repeated positions dropped) with 13 features, not 4,618,684 with 8; the files are 975 MB, not 760 MB.

**Assessment (AI, 2026-11-25):** review panel (full): ship after changes; disputed: the spectra DR17 flags as unreliable (USE-5, ruled a weighing call, not a Must: issue 1, with the DESI consistency check), the sky position as a leak or a shift (LEAK-10 against USE-6, settled: a shift, kept with a note), the PSF magnitudes (CLEAN-1 or USE-6, settled either way: added), the reason for no gap (SPLIT-10 against SPLIT-14, settled: no gap, the reason rewritten and its cost put to the sign-off); for the curator: issues H and 1-2. Priority 4: gap + (physics & astronomy and multiclass are thin), use case 0 (approximate, `Selection Bias`), source + (the DR17 paper and SkyServer's schema documentation), shape + (4,599,104 objects, 13 features, dated), risk 0 (the open label-quality call ships either way; the one exploit, reading the test window's other rows, is closed by a protocol line).

CC (2026-11-25, Andrej): issue 1, B ("Option B: Drop every flagged spectrum."): the definition drops every spectrum the source flags (`zWarning` not 0: 368,771 of the 4,618,753 fetched, the 19,581 from fibres without light among them), following DR17's own quality flag; 4,249,921 objects remain.

CC (2026-11-25, Andrej): the declared horizon (one calendar year, no gap, windows starting 1 January 2019 for 2019 with 2020, then 2018 back to 2012) is checked, as implemented (A): the yearly data releases set the length, and the user, the survey team, has its spectra and classes within days, so no gap; a 6-month gap would put the 2012 window at 48.0% of the objects.

**Assessment (AI, 2026-11-25):** after the drop of the flagged spectra: 4,249,921 objects (61 repeated positions dropped, 2 of them with differing classes; 149 with a -9999 magnitude set missing), galaxy 61.60%, star 20.73%, quasar 17.68%; test windows 52,526 (2019-2020), 253,228, 200,290, 179,009, 135,619, 212,680, 447,141 and 546,222 (2012, scored on 500,000), training on 98.8% down to 52.3%. `dataset check`: 0 errors, 0 warnings. Leak probe: all features AUC 0.972, the best single one `psfMag_g` 0.792, no exact copy across the split. Task probe (5 of 8 windows, log loss): LightGBM 0.255, random forest 0.265, logistic regression 0.393, the class shares 1.247.

CC (2026-11-25, Andrej): issue 2, d ("Add both"): the imaging pipeline's object type (`photo_type`, decoded to SkyServer's names, GALAXY for extended and STAR for point sources) and the Galactic extinction `extinction_u..z` join the inputs, as he asked for every feature a practitioner has at training and at prediction time: both come from the object's imaging row, which exists before any spectrum.

**Assessment (AI, 2026-11-25):** refetched with `type` and `extinction_u..z`: every one of the 11 ranges returned the same rows as before (4,618,753 spectra, the same spectrum ids, no shared cell changed). On the 4,249,921 objects: `photo_type` GALAXY 2,635,130, STAR 1,614,692, UNKNOWN 99; GALAXY for 97.1% of the galaxies, STAR for 94.4% of the quasars and 94.3% of the stars; the extinctions have no missing value and are one number (correlation 1.000). `dataset check`: 0 errors, 0 warnings. Leak probe: all features AUC 0.973, the best single one `photo_type` 0.812 (then `psfMag_g` 0.791), without it 0.971; no exact copy across the split. Task probe (5 of 8 windows, log loss): LightGBM 0.247, random forest 0.261, logistic regression 0.370, the best single feature 0.601, the class shares 1.247 (before: 0.255, 0.265, 0.393, 0.615).

## Review

**Outcome:** added as `sdss_dr17_star_galaxy_quasar_1m`; the horizon is signed off as implemented and the spectra DR17 flags are dropped (issue 1, B, 2026-11-25, Andrej); the imaging's object type and the dust extinction join the inputs (issue 2, d, 2026-11-25, Andrej). 4,249,921 objects with a spectrum in SDSS DR17 whose class the pipeline does not flag (`zWarning` = 0; February 2000 to March 2020), the target the spectroscopic pipeline's class (galaxy 61.60%, star 20.73%, quasar 17.68%), inputs the sky position, the camera column, the model and PSF magnitudes in five bands, the imaging pipeline's object type (`photo_type`) and the extinction in five bands; redshift, plate and fibre dropped as in `sdss_17`, the date no input. Split: eight one-year windows, 2019-2020 together, then 2018 back to 2012, each trained on every earlier spectrum (52.3% to 98.8%), no gap; metric the fallback log loss. Validity: no column leaks (all features AUC 0.973 in the leak probe, the best single one `photo_type` 0.812; missing indicators 0.50, number formats 0.52; no exact copy across the split); the one exploit, reading the test window's other rows, is closed by a protocol line. Value: on 5 of the 8 windows, untuned LightGBM 0.247 log loss, random forest 0.261, logistic regression 0.370, the best single feature 0.601, the class shares 1.247. `dataset check`: 0 errors, 0 warnings. Not built.

**Main points:** Horizon signed off (one year, no gap), the flagged spectra dropped (issue 1, B) and the imaging's object type and dust extinction added as inputs, both known to a practitioner at training and prediction time (issue 2, d); open: the DESI consistency check under issue 1.

**Record judgment:** The panel changed the definition in two places and the builder's draft in one. The spectra whose fibre carried no light are dropped by the source's own flags (18,513 UNPLUGGED, and 1,068 NODATA that the mediator found, all labelled galaxy): a class fitted to no light is a missing label, so this needed no weighing. The PSF magnitudes are added: the feature set of `sdss_17` came from the Kaggle file, not from a choice against them, and they lowered the log loss by 0.09 to 0.15 in four tests (the task probe now 0.354 against the builder's 0.489). The rest is writing in the definition: the no-gap reason (a window's length is not a gap), the number of splits an IID split would get at this size (3, not 9), the reason for merging 2019 and 2020 (eight plates of one programme), the sky position note with its cost, the re-observed objects, the 492,959 primary spectra with no photometric object, the linear baseline quoted from one run, and the protocol line against reading the test window's other rows. "Task easier" is gone from issue 1 as a reason. The record's screening named DESI DR1 as `TBD -> Yes`; it is suspended (Comments, Assessment of 2026-11-25). Retiring `sdss_17` is decided in its own review.

**Horizon:**

* **Verdict:** keep the one-year windows with no gap (medium confidence: the length follows the yearly data releases and `sdss_17`'s sign-off; no gap holds for the survey's own user, not for a public catalogue user, and the gap is costly).
* **Length:** one calendar year, the refit cadence of the data releases (DR8 January 2011, DR9 July 2012, DR10 July 2013, DR12 January 2015, DR13 July 2016, DR14 July 2017, DR15 December 2018, DR16 December 2019: every 12 to 18 months), as `sdss_17`'s windows[^hs][^h12]. Calendar years rather than release dates are our assumption.
* **Gap:** none. The user is the survey team, which has its reduced spectra within days and plans the next plates from them (the "choose targets" reading of the use case); a public user waits for the next release, whose newest spectra are 0.5 to 3.5 years old at a window's start, and a window's length is not that gap[^h10]. The split auditor measured the cost of a gap (untuned LightGBM, 300 trees, 1M training rows from the default sampler, a random 100k test rows a window, on the frame before today's changes):

  | Gap | Mean log loss | Training shares under 50% |
  |---|---|---|
  | none (implemented) | 0.450 | none |
  | 6 months | 0.495 | 2012 at 45.9% |
  | 18 months | 0.590 | 2012 at 35.5%, 2013 at 46.0% |
  | the public release at each window's start | 0.635 | 2012 at 31.9%, 2013 at 46.3% |

  Per window the 18-month gap costs 0.03 to 0.40, most in 2012 (+0.40), 2017 (+0.26) and 2013 (+0.19), where it removes the first data of a new programme (BOSS, then eBOSS). The release cutoffs of the last row are the split auditor's reading of the release papers and are not checked. "No gap" was signed off for `sdss_17` without this cost measured[^hs].
* **Time frame:** the spectra of DR17, 4 February 2000 to 24 March 2020 (the source's dates). The windows cover 2012 to March 2020, the end of BOSS and all of eBOSS: each year before 2012 would train on under half the objects (2011 at 39.4%)[^h14]. 2019 and 2020 form one window: 2020 is 8 plates of one programme (eFEDS) on 5 nights before the observatory closed for COVID-19, an atypical newest window, as decided for `sdss_17`[^hs][^h20].
* **Options:**

  | | Option | What it does | Test windows | Pro | Con |
  |---|---|---|---|---|---|
  | A | One year, no gap (implemented) | Each calendar year 2012-2018 and 2019-2020 together is tested on every earlier spectrum | 8: 62,372 to 577,180 objects (2012 scored on 500,000); train 50.2% to 98.6% | the survey team's position; every window above the half floor; `sdss_17`'s sign-off | a public catalogue user, who waits for the release, scores 0.14 to 0.19 worse on average |
  | B | One year, a 6-month gap | As A, each training side ending six months before its window | 8, as A; 2012 trains on about 46% | stands in for the planning lead (plates drilled weeks to months ahead) | +0.045 mean log loss; 2012 needs your exception to the half floor or leaves |
  | C | One year, the public release at each window's start | Each training side ends at the newest spectra public when the window opens (DR8 for 2012 up to DR14 for 2018-2019) | 8, as A; 2012 trains on about 32%, 2013 on about 46% | the position of a public astronomer using the catalogue | +0.185 mean log loss; two windows need your exception or leave; the cutoffs are not checked |
  | D | Nine windows, 2020 apart | As A, with 2019 and 2020 as separate windows | 9: 2020 alone 5,913 spectra, 2019 56,459 | one window more | the newest window is 8 plates of one programme; departs from `sdss_17`'s merge |

* **Recommendation:** A. The survey's own user has the spectra within days, and any gap of 6 months or more pushes 2012 (and at 18 months 2013) under the half floor. The cost to a public user is written into the splits comment so the choice is visible. **Decision:** sign off A, or change to B, C or D?

**Notes for the AI:** A is implemented in `_make_splits` from `WINDOW_STARTS`, `Temporal(on="date", horizon=1, horizon_unit="years", time_of="label")`. For B or C, shift each training side's end in `_make_splits` (train = dates < start - gap, or < the release cutoff of the window), add `gap`/`gap_unit` to `Temporal`, raise the 2012 (and for C 2013) exception as its own issue or drop the window, and check the release cutoffs against the DR papers first. For D, add 2020-01-01 to `WINDOW_STARTS`. On any change rewrite the splits comment and `task_summary.split`, and re-run `dataset check` and the task probe.

[^hs]: Earlier calls on `sdss_17`: the one-year windows (2026-11-12, Andrej); 2019 and 2020 as one window (its issue 7, B, 2026-11-12); "no gap" checked (2026-11-17, Andrej).
[^h12]: **SPLIT-12** (Should): the horizon is a human judgment from the source (how far ahead the actor predicts, the refit cadence); the curator signs off the horizon and the test windows of every new temporal dataset.
[^h10]: **SPLIT-10** (Should): when a label is known only some time after its row, a model refit at a window's start knows only the rows whose label had arrived; simulate that with a gap.
[^h14]: **SPLIT-14** (Must): at least 3 windows, each training on at least 50% of the data; a window under 50% is the curator's exception for that dataset, down to 30%.
[^h20]: **SPLIT-20** (Should): check whether the newest windows fall in an atypical season and widen them so most do not.

**Andrej (2026-11-25, ok):** As implemented (A).

**Resolved (2026-11-25, Andrej):** A: one calendar year, no gap, eight windows from 2019 with 2020 back to 2012, each trained on every earlier spectrum; nothing changed in the definition with the sign-off. After issue 1's drop the windows hold 52,526 (2019-2020) down to 546,222 (2012, scored on 500,000) objects and train on 98.8% down to 52.3%; a 6-month gap would put 2012 at 48.0%, an 18-month gap 2013 at 48.0% and 2012 at 37.3%. The gap costs in the table above were measured before the drop.

**Issues for Andrej:**

1. **Drop the spectra whose class DR17 flags as unreliable (`zWarning` not 0)?**

   - **Problem:**
     - Between pipeline versions, a flagged class changed 62 times as often as a clean one (26.8% against 0.43% of the same 91,063 spectra from DR12 to DR17), so the flagged labels really are unreliable.
     - After today's drop of the no-light fibres, 7.59% of the objects still carry a flag (90.9% of them SMALL_DELTA_CHI2 alone, the best class template barely ahead of the next): galaxies 5.5%, stars 8.4%, quasars 13.3%.
     - Their share grows over time, from 3.7% of the spectra before 2012 to 15-22% of the test windows from 2015, so the newer windows carry two to four times their training side's share.
   - **Background:** `zWarning` is the spectroscopic pipeline's own quality bitmask (Bolton et al. 2012; sdss4.org/dr17/algorithms/bitmasks). The target is declared as "the class the survey's spectroscopic pipeline assigned", and `sdss_17` keeps these rows only because its Kaggle file has no `zWarning` column. Today's definition already drops the spectra flagged UNPLUGGED or NODATA (19,581), whose fibre carried no light; this issue is about the rest.
   - **Effect on the task:** under A a part of each newer window's loss is label noise, and a model is scored against classes the source itself disowns; under B the test windows lose 5-22% of their objects, the ambiguous ones a deployed classifier would also be asked about, so B changes which objects are scored, not only how noisy their labels are.
   - **Experiments:**

     The same spectra in DR12 (pipeline v5_7_0) and DR17 (v5_13_2), MJD 55900-55960 (the mediator's count on the builder's files):

     | DR17 `zWarning` | Changed class from DR12 to DR17 |
     |---|---|
     | 0 (clean) | 0.43% |
     | not 0 (flagged) | 26.8% |
     | SMALL_DELTA_CHI2 | 28.3% |

     The domain practitioner's test (LightGBM, train 2014-2015, test 2016, log loss, lower is better):

     | Training rows | Clean test rows | Flagged test rows |
     |---|---|---|
     | all | 0.436 | 0.853 |
     | clean only | 0.395 | - |

     The windows as now shipped and under B, measured on the frame after today's changes:

     | Test window | Test objects | Flagged in test | Flagged in training | Test objects under B | Training share under B |
     |---|---|---|---|---|---|
     | 2019-2020 | 62,372 | 15.8% | 7.5% | 52,526 | 98.8% |
     | 2018 | 311,768 | 18.8% | 6.6% | 253,228 | 92.8% |
     | 2017 | 255,891 | 21.7% | 5.7% | 200,290 | 88.1% |
     | 2016 | 210,578 | 15.0% | 5.2% | 179,009 | 83.9% |
     | 2015 | 158,781 | 14.6% | 4.7% | 135,619 | 80.7% |
     | 2014 | 242,471 | 12.3% | 4.2% | 212,680 | 75.7% |
     | 2013 | 471,822 | 5.2% | 4.0% | 447,140 | 65.2% |
     | 2012 | 577,180 (500,000 scored) | 5.4% | 3.7% | 546,222 (500,000 scored) | 52.3% |

   - **Consistency:** no settled precedent: what you decide becomes the first case for a source's own label-quality flag. `desi_dr1_star_galaxy_quasar`, the same kind of target from another survey, is `DF: Suspended` for its label correctness (CC 2026-11-05, Myunghwan) and reopens only with "source-supported repair", which B is; the consistency check below asks what sets the two apart. `sarcoma` uses the source's reviewed labels, which leaves out uncertain types (leans B); `lung_adenocarcinoma_metastasis` keeps labels the source doubts as coded (leans A)[^z6].
   - **Panel:** the critic and the domain practitioner argue for B (the practitioner "would never train on, or validate against, spectra the pipeline flags as unreliable"); the advocate does not oppose B but disputes that it is required; the mediator leans B on the instability ratio and rules it a weighing call, not a Must.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep every flagged spectrum (implemented) | The target is the pipeline's class wherever the fibre had light, as `sdss_17` | the declared target; the test windows keep the hard, ambiguous objects a deployed model meets; no departure from `sdss_17` | 7.59% of the labels are ones the source flags, 62 times as unstable; the newer windows carry 2-4 times the training share of them; DESI's hold then needs a fact that sets SDSS apart |
     | B | Drop every flagged spectrum | `_clean` keeps `zWarning` = 0 only (4,249,919 objects) | labels the source stands behind; the repair DESI's hold names; standard practice for SDSS training sets | removes 5-22% of each test window, more of the newer ones and of quasars, so the test population changes; departs from `sdss_17` |
     | C | Keep them and ship `zWarning` as a column that is no input | As A, with the flag in the data for analysis | nothing is lost; a later scorer can filter | changes nothing in the scores; a non-input column the format does not otherwise need |

   - **Recommendation:** B, uncertain. The decisive fact is the instability: a flagged class is 62 times as likely to change with the next pipeline version, so under A part of what the newer windows score is which way the pipeline happened to break near-ties. B uses the source's own flag, not a rule of ours. A stays defensible because the target is declared as the pipeline's class and B changes which objects are tested. **Decision:** keep the flagged spectra (A), drop them (B), or keep them with the flag shipped (C)?

   **Notes for the AI:** A is implemented: `_clean` drops only `zwarning & NO_LIGHT` (UNPLUGGED, NODATA) and then the `zwarning` column. For B, drop rows with `zwarning != 0` in the same place (before the position dedup), rewrite `task_summary.row`, `predicted` (new shares) and `changes`, the no-light bullet and the window numbers in the curation notes and splits comment (the table above), add a row to the label-quality rule's Cases table, and re-run `dataset check` and the leak and task probes. For C, keep `zwarning` and declare it a non-input column if the format allows one; otherwise C is not available. Either way, answer the consistency check below and put the outcome to Myunghwan's hold on `desi_dr1_star_galaxy_quasar` as a question.

   [^z6]: **USE-5** (Must): predict what the actor would act on; check how the source built its label before accepting it. **TP-6** (Must): a better version the source itself defines replaces the current one; a fix of our own invention is not a better version (the flag is the source's). **CLEAN-15** (Must): drop rows with a missing target (the no-light spectra already dropped). principles.md, "Consistent judgement", case 2: a precedent with similar facts decided the other way by another curator.

   **Consistency check (AI, 2026-11-25): does the label-correctness bar that suspended DESI DR1's star/galaxy/quasar task apply to DR17's pipeline classes, and if not, what sets them apart?**

   - **Problem:**
     - Myunghwan suspended `desi_dr1_star_galaxy_quasar` on 2026-11-05: "Credible physical-class correctness above 90% has not been established for the intended population"; a reliable spectral fit is no verified class, and the task reopens only with independent validation or source-supported repair.
     - This dataset's target is the same kind, the SDSS pipeline's class from one template fit with the redshift, and DR17 flags 7.59% of the kept classes; `sdss_17` shipped on 2026-11-12 without the question being asked.
     - The advocate's distinguishing fact, that the target here is declared as the pipeline's class, does not hold: DESI's target is also a pipeline class (`SPECTYPE`).
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Exception for SDSS | The target is the documented pipeline class with its quality flag; recorded with that fact; DESI's hold stays on its own physical-class framing | ships as built; the task says what it predicts | the same fact may lift DESI's hold, so the double standard stays until it is put to Myunghwan |
     | b | Treat SDSS like DESI | Hold until pipeline-against-visual-inspection agreement is shown above the bar (for example from DR16Q) | one bar for both surveys | blocks the replacement of `sdss_17`, which would need the same check |
     | c | Reopen DESI to match SDSS | A documented pipeline class with its quality flag is a valid target, for both | removes the double standard | overrides another curator's decision; DESI's ease (log loss about 0.11) remains |
     | d | Amend a rule | State when a pipeline-assigned label is a valid target (documented pipeline, the source's quality flag applied), in the rule file that covers it | settles both and later surveys | a rule change for two cases |

   - **Recommendation:** d with B of issue 1: a documented pipeline class is a valid target once the source's own quality flag is applied, which is the "source-supported repair" DESI's hold names; then put it to Myunghwan as a question for DESI (c). If you keep A in issue 1, a, with the fact written down and the same question to Myunghwan. **Decision:** a, b, c or d?

   **Andrej (2026-11-25, change):** Option B: Drop every flagged spectrum.

   **Resolved (2026-11-25, Andrej):** B: `_clean` keeps only the spectra with `zWarning` = 0 (the files carry the flag), before the position dedup; the no-light drop is part of it. The choice follows the source's own quality flag, the pipeline's bitmask, not a rule of ours. 368,771 of the 4,618,753 fetched spectra leave (7.98%: 172,453 galaxies, 81,158 stars, 115,160 quasars; the 19,581 from fibres without light among them); 4,249,921 objects remain (61 repeated positions dropped, 2 of them with differing classes), galaxy 61.60%, star 20.73%, quasar 17.68%. Windows: 52,526 (2019-2020), 253,228, 200,290, 179,009, 135,619, 212,680, 447,141 and 546,222 (2012, scored on 500,000) objects, training on 98.8% down to 52.3%. `task_summary` (row, predicted, changes, fit reason), the curation notes (the flag bullet, the dedup, the sentinels, the class mix by period, the baselines) and the splits comment are rewritten; figures measured before the drop are marked so. `dataset check`: 0 errors, 0 warnings. Leak probe: all features AUC 0.972, the best single one `psfMag_g` 0.792, missing indicators and number formats 0.50, no exact copy across the split. Task probe (5 of 8 windows, log loss): LightGBM 0.255, random forest 0.265, logistic regression 0.393, the best single feature 0.615, the class shares 1.247; LightGBM ahead in every window. The consistency check above stays as written: this mark decides issue 1, not its question to Myunghwan or the rule of its option d.

2. **Add the imaging pipeline's star/galaxy `type` and the dust extinction `extinction_u..z` as inputs?**

   - **Problem:**
     - Both are legitimate inputs, from the same `PhotoObj` row as the magnitudes and known before any spectrum, but with the PSF magnitudes added today they lower the log loss by only about 0.01 more, and today's definition ships neither[^t6].
     - `type` is the photometric pipeline's rule-based call (point source when psfMag − cModelMag is at most 0.145, else extended): no label went into it, so it is not another model's score, but it is a derived class rather than a raw measurement[^t7].
     - `extinction_u..z` is the Milky Way's dust along the line of sight, the physical part of the sky position, which an expert would keep where the position mostly records which programme observed the field[^t1].
   - **Experiments:** the column auditor's fits (LightGBM, 400 trees, trained on all earlier spectra, refetched with these columns, earliest spectrum per position; log loss, lower is better):

     | Test window | Training rows | The 8 features before today | 8 + psfMag (as now) | 8 + type | 8 + psfMag, type, extinction |
     |---|---|---|---|---|---|
     | 2019-2020 | 1.04M | 0.467 | 0.353 | 0.382 | 0.347 |
     | 2018 | 0.73M | 0.433 | 0.344 | 0.364 | 0.332 |

     The last two columns against the second show what `type` and the extinction add once psfMag is in. Without psfMag, `type` alone took the domain practitioner's 2014-15 → 2016 test from 0.501 to 0.380.
   - **Panel:** the advocate and the critic both leave this to you; the domain practitioner would add both, optionally.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Neither (implemented) | The inputs stay the position, `cam_col`, the model and the PSF magnitudes | raw measurements only; the PSF magnitudes already give most of the morphology | leaves out the survey's own star/galaxy call and the dust an astronomer uses |
     | B | Add `type` | One categorical column (3 galaxy, 6 point source, rare others) | the call every SDSS catalogue user reads first | a fixed rule on the PSF magnitudes (which ship) and the cModel magnitudes; adds little once psfMag is in |
     | C | Add `extinction_u..z` | Five numeric columns | the physics of the position without the programme footprint | five near-collinear columns; a small gain |
     | D | Add both | B and C | the expert's full imaging row | the largest departure from `sdss_17`'s columns |

   - **Recommendation:** A, weakly: with the PSF magnitudes in, the rest of the measured gain is about 0.01, `type` is a rule partly on the PSF magnitudes that ship, and the extinction follows from the position. B or C is equally defensible as the expert's state. **Decision:** keep A, or add `type` (B), the extinction (C) or both (D)?

   **Notes for the AI:** add `p.type` and/or `p.extinction_u, …, p.extinction_z` to `COLS` in `download_description`, refetch the 11 ranges, rename `type` to `photo_type` (categorical in `_feature_types`), keep the extinction numeric; update `known`, the curation notes and the README; re-run `dataset check` and the leak, task and dtype probes.

   [^t6]: **USE-6** (Must): anything known at the prediction point is a legitimate input.
   [^t7]: **CLEAN-6** (Must): never build features from the labels, learned embeddings or another model's scores.
   [^t1]: **CLEAN-1** (Should): clean to the state an expert would ship.

   **Andrej (2026-11-25, discuss):** Would a practitioner have these features available at train and predict time? If yes, we should add them, otherwise not.

   **Answer (AI, 2026-11-25):** yes: both come from the object's imaging, which exists before any spectrum and for every imaged object, so a practitioner has them at training and at prediction time; by your rule they are added (d).

   * **Problem:**
     - Both sit in the object's `PhotoObj` row, the same imaging catalogue row as the model and PSF magnitudes that ship: the imaging was taken and reduced before the object was targeted for a spectrum, so neither depends on the spectrum or its class[^a6].
     - At prediction time a practitioner classifying an object without a spectrum reads the same row: SDSS's imaging catalogue gives `type` and `extinction_u..z` for every imaged object, with or without a spectrum. In the training data they come with the same join on `bestobjid` as the magnitudes, for every row; both carry the magnitudes' as-of status, DR17's imaging catalogue rather than the version an astronomer had at a window's start (`Features: Revised Later`).
     - `type` is no measurement but a fixed rule of the imaging pipeline: point source (6) when the PSF magnitude is at most 0.145 fainter than the cModel magnitude, else extended (3). No label went into it, so it is not another model's score; the PSF magnitudes ship, the cModel magnitudes do not. The shipped columns already carry most of it: LightGBM predicts it from them at 97.9% to 98.4% accuracy, and the rule in r alone with the shipped model magnitude in place of cModel agrees with it on 93.7% of the objects[^a7].
     - `extinction_u..z` is the Galactic dust reddening of the dust map at the object's position times a fixed coefficient per band: the five columns are one number (correlation 1.000; u, g, i, z at 1.855, 1.446, 0.743 and 0.553 times r). It is known for any position before any observation; the shipped position carries part of it (R² 0.51 to 0.72 from the 10 nearest training positions).
     - The domain practitioner of the panel would add both, optionally ("Optionally add `type` (as a categorical) and `extinction_u…z`. This puts the task in the state an expert would use."), and found `type` alone took most of the PSF magnitudes' gain before they shipped (0.501 to 0.380, train 2014-2015, test 2016).
   * **Experiments:** on the clean spectra (`zWarning` = 0, earliest spectrum per position, as now shipped), the two newest windows, trained on every earlier spectrum from October 2014 (the panel's refetch with these columns, MJD 56935 onward), untuned LightGBM, 400 trees, log loss, lower is better:

     | Test window | Training rows | Test rows | As shipped | + `type` | + extinction | + both |
     |---|---|---|---|---|---|---|
     | 2019-2020 | 851,124 | 52,526 | 0.2380 | 0.2329 | 0.2387 | 0.2339 |
     | 2018 | 597,896 | 253,228 | 0.2229 | 0.2186 | 0.2243 | 0.2182 |

     What the shipped columns already carry:

     | Window | `type` from the shipped columns (LightGBM accuracy) | `extinction_r` from the position (10 nearest training positions, R²) |
     |---|---|---|
     | 2019-2020 | 98.4% | 0.72 |
     | 2018 | 97.9% | 0.51 |

     `type` by class on these objects: 87.2% of the galaxies are extended, 97.0% of the quasars and 94.9% of the stars point sources.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Neither (implemented) | the inputs stay the position, `cam_col`, the model and the PSF magnitudes | raw measurements only | leaves out two columns the practitioner has at both times, against your rule |
     | b | Add `type` | one categorical column (`photo_type`: 3 extended, 6 point source, 5 objects 0) | the survey's own star/galaxy call; -0.004 to -0.005 | a rule on the PSF and cModel magnitudes, 98% recoverable from the shipped columns |
     | c | Add `extinction_u..z` | five numeric columns as the source gives them | the dust along the line of sight, the physical part of the position | one number in five columns; no gain measured (+0.001) |
     | d | Add both | b and c | the practitioner's full imaging row, as your rule asks for features available at both times; -0.004 to -0.005 | the largest departure from `sdss_17`'s columns; the extinction adds nothing measured |

   * **Recommendation:** d: both are available to the practitioner at training and at prediction time, the condition you set; the measured gain is small (`type` 0.004 to 0.005, the extinction none), so the reason is availability, not the score. b is the choice if columns that add nothing measured should stay out. **Decision:** a, b, c or d?

   [^a6]: **USE-6** (Must): anything known at the prediction point is a legitimate input.
   [^a7]: **CLEAN-6** (Must): never build features from the labels, learned embeddings or another model's scores.

   **Andrej (2026-11-25, discuss):** Reply (d): Add both

   **Resolved (2026-11-25, Andrej):** d: the query in `download_description` adds `p.type` and `p.extinction_u` to `p.extinction_z`, and the 11 ranges were fetched again (1,227 MB): every range returned the same rows as before (4,618,753 spectra, the same spectrum ids, no shared cell changed). `_clean` renames `type` to `photo_type` and decodes its codes to SkyServer's `PhotoType` names (GALAXY 2,635,130, STAR 1,614,692, UNKNOWN 99 of the 4,249,921 objects; a code outside the schema fails the load); `_feature_types` makes it categorical, the five extinctions stay numeric (none missing). `known`, `changes`, the download and source notes, a new curation bullet (what the two columns are, why they are inputs, their measured gain) and the baselines are rewritten. `dataset check`: 0 errors, 0 warnings. Leak probe: all features AUC 0.973, the best single one `photo_type` 0.812, without it 0.971, no exact copy across the split. Task probe (5 of 8 windows, log loss): LightGBM 0.247, random forest 0.261, logistic regression 0.370, the best single feature 0.601, the class shares 1.247 (before: 0.255, 0.265, 0.393, 0.615).

**Review panel:** ship after changes (mediator). Claims: 23, 21 hold, none refuted, 2 untested (the Kaggle containment, the probe numbers); two findings from the data (the unplugged fibres, the cost of the sky position). Blind review: would include, with changes; its main concern the sky position as a shortcut to the survey programme. Debate: agreed on dropping the no-light spectra, adding the PSF magnitudes, keeping no gap with a rewritten reason, keeping the position with a note and the protocol line; disputed: whether the flagged spectra must go (ruled a weighing call: issue 1) and whether the position is a leak or a shift (ruled a shift). The mediator's issue 2 (confirm no gap) is the Horizon above, its issue 3 is issue 2.

<details><summary>Mediator</summary>

**Mediator: `sdss_dr17_star_galaxy_quasar_1m`**

**Judgment record**

```text
Verdict: ship after changes.
Validity: SEL holds; USE-1 holds (approximate, Selection Bias); USE-5 open: 7.6% of rows carry a class the source flags
as unreliable (zWarning other than UNPLUGGED/NODATA), with flagged labels 62 times as unstable as clean ones (issue 1);
LEAK-10 holds (redshift, plate and fibre dropped; the DR13 as-of check is clean); LEAK-9 triggered (co-window
transductive exploit, -0.047): a protocol note; SPLIT-36 holds (L-ORDER.windows); SPLIT-14 holds (50.1% to 98.6%);
SPLIT-10: no gap kept, the reason is wrong and gets rewritten, the curator confirms with the measured cost (issue 2);
PROV-6 / TP-6: replaces sdss_17; CLEAN-11 triggered: 19,581 spectra from fibres with no light (UNPLUGGED, NODATA)
dropped in the source's own words.
Value: TP-2 holds (LightGBM beats the dummy on every split; quote one linear-gap figure); MET-1 holds (fallback log_loss).
Quality: CLEAN-1 triggered: psfMag_u..z added (repair from the origin; -0.09 to -0.15 log loss in four tests);
type and extinction_* are a weighing call (issue 3).
Weighed: position kept with a note (USE-6 shift, not a leak); cam_col kept (±0.001).
For the curator: issue 1 (zWarning ≠ 0 and the DESI hold), issue 2 (confirm no gap), issue 3 (type, extinction).
```

**Changes to make now (no decision needed)**

1. **Drop the spectra from fibres that carried no light (CLEAN-11, with the source's words; the label is then in effect missing, CLEAN-15).**
   - Add `s.zwarning` to the 11 queries and drop rows where `zwarning & (128|512) != 0`: UNPLUGGED, "fiber was unplugged or damaged", and NODATA.
   - This is 18,513 UNPLUGGED rows plus **1,068 NODATA-only rows, a new finding** (all labelled GALAXY), so 19,581 before the position dedup.
   - Both sides agreed on the UNPLUGGED part. NODATA is the same mechanism, so I add it here.
2. **Add `psfMag_u..z` and set -9999 to missing (CLEAN-1, a repair from the origin).**
   - Measured four times by two agents: log loss falls by 0.09 to 0.15.
   - No curator decision stands against it. The sdss_17 feature set (CC 2026-10-01, Lennart; issue 3, 2026-11-11, Andrej) came from removing leaks and from what the Kaggle file held, not from a choice against PSF magnitudes.
   - The domain practitioner searched the records: no precedent.
   - The values come from the same imaging and are known before any spectrum (USE-6).
   - The README should say the feature set now goes beyond sdss_17's, still as the same task (PROV-6 unchanged).
3. **`splits_comment`:**
   - Rewrite the no-gap reason. A window's length is not a gap. The user is the survey team, which has reduced spectra within days. State that a public user waits for the release: +0.045 mean log loss with a 6-month gap, +0.14 with 18 months, +0.185 at the actual release lags (split-auditor; the cutoff dates are from memory and need checking).
   - Change "the 9 an IID split would get" to 3 (SPLIT-15, SPLIT-33), and say the number of windows is limited by the training floor.
   - Give the real reason for merging 2019 and 2020: 2020 is 8 plates of one programme, before the COVID closure (SPLIT-20). "Every spectrum stays tested" is not a reason.
4. **`curation_comments` / `fit_reason` (writing; USE-8):**
   - The position note, with the per-window costs: +0.013 to +0.066, mean +0.033. Say that position records which programme's footprint an object lies in, and that it is kept as a known input (USE-6), as in sdss_17.
   - Re-observed objects: 5.6–7.7% of primary spectra from 2010 to 2020 (8–14% of quasars) belong to objects that had an earlier spectrum. Not dropped.
   - The 492,959 primary spectra with `bestobjid = 0`, which have no photometric match.
   - One linear-baseline figure taken from one run. Today 0.16, 0.185 and 0.25 come from different runs.
5. **Protocol note for the co-window exploit (LEAK-9).** A method that learns from the test window's own unlabelled rows is called out and not benchmarked.
6. **Record:**
   - Correct the DESI sibling line. It is `DF: Suspended` (CC 2026-11-05, Myunghwan), not "`TBD -> Yes`, 1".
   - In draft issue 1, remove "task easier" as a reason for B (task fidelity over separability).
   - The claim auditor's "NEGATIVE_MODEL (bit 6)" is NEGATIVE_EMISSION; bit 3 is NEGATIVE_MODEL.

**Issues for the curator, ranked**

**1. Labels the source flags as unreliable: 7.6% of rows after change 1 (validity: USE-5 Must and P5; consistency, case 2).**
- **Problem:** `zWarning ≠ 0` is set on 8.0% of spectra: 4.0% before 2012, 15–22% from 2015 on. Almost all of the rest after change 1 is SMALL_DELTA_CHI2, where the best class template barely beats the next one.
- **Decisive fact (my run, on the builder's DR12/DR17 files, 91,063 spectra):** between pipeline versions, flagged labels changed class 26.8% of the time, against 0.43% for clean ones. SMALL_DELTA_CHI2 alone changed 28.3%. So the flagged labels really are unreliable; that is no longer in dispute.
- **Critic's best case:** the task asks for the object's class. The source disowns these labels. The practitioner scores 0.436 on clean test rows against 0.853 on flagged ones. DESI was suspended for this concern, and its own way out is "source-supported repair", which B is.
- **Advocate's best case:** the target is declared as the pipeline class, and sdss_17 ships it. B removes 15–22% of the newest test windows, and a deployed model would be asked about those ambiguous objects too. B changes which objects are scored, not only how noisy the labels are.
- **Ruling:** the rules leave this open. The rows are real objects with a fitted label, not another quantity, so USE-5 does not fail on its own. It is a weighing call, and the DESI hold puts consistency in play.
- **Decide:**
  - B (drop all flagged rows) or A (keep them). My lean is B: the 62-times instability ratio.
  - What separates SDSS from DESI, using the precedent checker's options a to d. The advocate's distinguishing fact does not hold: DESI's target is also a pipeline class. If B is chosen, B is the repair the DESI hold names.
  - Ask Myunghwan whether the same reasoning reopens DESI.

**2. Confirm no gap (P4: SPLIT-10 Should; the person decides at the [ORDER.exception] step).**
- **Precedent:** Andrej checked "no gap" for sdss_17 on 2026-11-17, but its cost was never measured.
- **What is new:** the measured cost, +0.045 (6 months) to +0.185 (release lag) in mean log loss.
- **The constraint:** a gap of 6 months or more puts 2012 under the 50% floor, and 18 months puts 2013 there too. Those windows would then need a SPLIT-14 exception from the curator (30% minimum) or would be dropped.
- **Both sides:** keep no gap, for the survey-team user.
- **Decide:** whether the use case is the survey team (no gap) or the public catalogue user (a gap).

**3. `type` and `extinction_u..z` as inputs (P7: CLEAN-1, Weigh).**
- `type` is the imaging pipeline's rule-based star/galaxy call (psf − cModel > 0.145). It is not learned from labels, so CLEAN-6 does not apply. It took the log loss to 0.382 against 0.467 with psfMag absent, and adds little once psfMag is in.
- `extinction` carries the physical part of the sky position.
- **Both sides:** a curator call, not a default.
- **Decide:** add either, both or neither.

**Disputed points settled**

- **Rule for the position:** the advocate wins. LEAK-10 is about what exists at the prediction point, and position does (USE-6, LEAK-37). It hurts the score rather than leaking, so it is distribution shift. Keep it with a note (change 4). The blind reviewer and the practitioner's closing line ("drop alpha, delta") have no rule behind them beyond the score, and they go against the sdss_17 decision. No issue.
- **Rule for PSF magnitudes:** CLEAN-1 (Should) decides, with USE-6 as the reason. The remedy is the same either way: fix now.
- **Whether B is required:** not a Must. See issue 1.
- **Linear gap 0.16 vs 0.25:** different runs. Quote one (change 4).
- **"SPLIT-14 Must beats SPLIT-10":** overstated. SPLIT-14 allows a curator exception down to 30%, so a gap is possible, just costly. The weighing is issue 2.

**Task-gamer exploits**

| Exploit | Gain | Rule | Note or accepted warning | New / known | Action |
|---|---|---|---|---|---|
| Features from the test window's own unlabelled rows in the same year and sky patch | −0.047 (a lower bound; not re-measured with psfMag) | LEAK-9 (an evaluation-level leak: a model reads other test rows) | none (`accepted: {}`, no kept-on-purpose note) | new for this dataset; the rule has precedents (sepsis_prediction_1m, medical_facility_operational_data) | protocol note (change 5). Refuse the gamer's fix of adding the programme or plate as a feature (LEAK-10; sdss_17 table) and a sky-region split (sdss_17 issue, D chosen) |
| Training only on recent years beats all history | −0.026, against a random-400k baseline | not an exploit: the honest choice the row budget's default sampler (newest year back to 1M) already makes | — | known | none |
| Cross-matching positions with SkyServer | total | applies to any public dataset; not ranked | — | known in kind | none |
| The 79,075 unused 2012 rows in the kit | small, feeds exploit 1 only | LEAK-9 | — | new, minor | covered by the protocol note |

**Agreed facts**

- 4,618,684 objects after removing 69 repeated positions; galaxy 60.41%, star 20.83%, quasar 18.76%.
- 22 of the definition's claims hold. The wrong text is the gap reason, "9", and the builder report's "155" (103 objects miss all five bands).
- No copies across the split; no leak in any column; the DR13 photometry shift is at most 0.016 mag, the same for every class.
- Windows: training shares from 50.1% to 98.6%; test windows from 62,946 to 500,000 rows; every fold holds all 3 classes (smallest class 9,651).
- `zWarning` bits on the join, from my SkyServer count:
  - UNPLUGGED: 18,513 rows (GALAXY 17,948, quasar 337, star 228).
  - NODATA without UNPLUGGED: 1,068, all GALAXY.
  - Flagged labels changed class between DR12 and DR17 at 26.8%, clean ones at 0.43%.
- PSF magnitudes lower log loss by 0.09–0.15 (4 tests). Sky position raises it by 0.013–0.066 in every window.
- Gap cost: none 0.450; 6 months 0.495; 18 months 0.590; release lag 0.635.
- The task is not trivial; the metric is `log_loss` (fallback, MET-1).

**Consistency with precedent**

- **Follows sdss_17:** drops (LEAK-10), position kept, `cam_col` as a category, windows and the 2019–20 merge (its reason needs rewriting, as above), `time_of="label"`, log loss, no gap (checked by Andrej on 2026-11-17).
- **Retiring sdss_17:** follows PROV-6 / TP-6, as thyroid_discordant_archive did (2026-11-12, Andrej).
- **psfMag:** no precedent. It departs from sdss_17's columns because of a fact that sets this case apart: the source is now our own query, not the Kaggle file.
- **zWarning:** no settled precedent. Whatever the curator decides becomes the first one; add it as a Cases row.
- **DESI hold:** an open departure. Issue 1 asks for the fact that sets SDSS apart, or for B as the repair the hold names.
- **`Target: Revised Later`:** missing on sdss_17. Moot if sdss_17 is retired.

</details>

<details><summary>Claim audit</summary>

I ran a test against every claim I could check: 22 hold and none of the written claims is wrong. Two findings come from the data itself:

1. **18,513 rows (0.40%) have a class but no real spectrum.** Their fibre was not plugged in, so the pipeline fitted noise, and 97% of them came out as GALAXY. These rows cost the newest windows about 0.01 of log loss.
2. **Dropping the sky position would improve LightGBM's score by 0.013 to 0.066 in every window I fitted.** The README never mentions this, though `sdss_17`'s record documents the same effect.


**Claims table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | 4,618,684 objects; galaxy 60.41%, star 20.83%, quasar 18.76% | task_summary row / predicted | rebuilt the frame from the definition | holds | 4,618,684; 60.41 / 20.83 / 18.76 | EV-2 |
| 2 | "every primary optical spectrum with a photometric object" | task_summary row | SkyServer: `SpecObj` totals and flags | holds | all 5,112,724 rows of `SpecObj` have `sciencePrimary = 1`; the 492,959 with `bestobjid = 0` are almost all unplugged-fibre and sky spectra (sourcetype NA 336,599, SKY 56,746; zWarning set on nearly all) | PROV-1 |
| 3 | Spectra from 2000-02-04 to 2020-03-24; the nights the 11 ranges skip hold no spectrum | curation_comments, record | raw dates; a count query on SkyServer for the gaps and outside the range | holds | min and max dates as claimed; the query returned n = 0 | PROV-1 |
| 4 | 69 positions have two spectra, 0 to 5,509 nights apart (median 2,536); the class differs at 6; earliest kept | curation_comments | raw duplicates | holds | 69 / 0 / 2,536 / 5,509 / 6; the 69 also equal the duplicated `objid` count | PROV-5, LEAK |
| 5 | No copy of an object across the split (implied) | (implied) | KD-tree on sky positions at 0.5", 1", 2" and 3" | holds | 0 pairs within 0.5", 2 within 1"; at most 5 pairs straddle a window boundary at 2" (fibres on one plate are at least 55" apart, so these are separate neighbours) | PROV-6 |
| 6 | -9999 set to missing on 155 objects, 103 to 139 per band | curation_comments | NaN counts per band | holds | u 139, g 133, r 103, i 120, z 126; 155 objects, 103 of them missing all five bands (the builder report's "all five bands" is wrong, the README is right); no other sentinel, the largest magnitude is 33.8 | CLEAN |
| 7 | `rerun` is constant at 301; `cam_col` is a code with 6 values | curation_comments, `_feature_types` | raw / frame | holds | [301]; 1 to 6 | CLEAN-3 |
| 8 | Quasars 3–10% of spectra in 2000–2009, 14–17% in 2010–2013, 30–48% from 2014 | fit_reason, curation_comments | crosstab by year | holds | 2.7–10.1 / 14.4–16.7 / 30.1–48.4 | USE-8 |
| 9 | Window sizes, training shares 98.6% to 50.1%, 2012 scored on 500k drawn within classes | splits_comment | split plan | holds | every number matches; the 2012 sample has 15.4% quasars, as in all of 2012 | SPLIT, TP |
| 10 | 2019: 56,989 spectra on 72 plates; 2020: 5,957 on 8 plates over 5 nights | splits_comment | raw | holds | 56,989 / 72 (26 nights); 5,957 / 8 / 5 | SPLIT |
| 11 | DR12-to-DR17 relabel: 1,580 of 91,063 spectra (1.74%) changed class, 76% of them flagged by zWarning | record (collection facts) | recomputed from the builder's DR12 and DR17 spectrum files | holds | 1,580; 1.74%; 0.764; the transition table matches | LEAK-10 |
| 12 | Photometry moved at most 0.016 mag, the same for every class | record, curation_comments | recomputed from the builder's DR12 and DR17 photometry | holds | 5th–95th percentiles within about ±0.017 mag per band, alike across classes | LEAK-10 |
| 13 | zWarning share 8.0%: galaxy 6.2%, star 8.4%, quasar 13.3% | builder draft issue 1 | SkyServer GROUP BY | holds | 368,771 of 4,618,753; 6.2 / 8.4 / 13.3 | — |
| 14 | `predicted`: "the class the survey's spectroscopic pipeline assigned", which the task treats as the object's class | task_summary predicted | SkyServer: zWarning bit 7 (UNPLUGGED) on joined rows | **holds as written, but the object's class is missing on 18,513 rows** | 18,513 rows (0.40%) have UNPLUGGED set and median S/N 0.0 (90th percentile 0.0). Labels: GALAXY 17,948, QSO 337, STAR 228. 8,049 of the GALAXY labels sit on point sources (photometric type 6). Share of each test window: 0.87% (2019–20), 0.77%, 0.77%, 0.64%, 0.57%, 0.55%, 0.33%, 0.33% (2012), rising over time | CLEAN-15, PROV-13 |
| 15 | The sky position is a fair input known before the spectrum (implied by `known`; settled in `sdss_17`) | task_summary known | LightGBM, 500 trees, the default sampler emulated (newest years back to 1M rows), 5 windows: all features vs without position vs position alone | **known at prediction time, but it lowers the score in every window; the README does not say so** | all vs no position: 2019–20 0.476 / 0.462; 2018 0.466 / 0.446; 2016 0.514 / 0.467; 2014 0.533 / 0.514; 2012 0.329 / 0.262. Mean of the 5: 0.464 vs 0.430. Position alone is worse than the class-share dummy in 4 of 5 windows (2012: 1.92 vs 0.87). `cam_col` adds nothing (magnitudes only ≈ without position) | LEAK-10 holds; USE / writing |
| 16 | Metric: fallback `log_loss`; no source metric exists | `metric`, README Metric block | DR17 paper and SkyServer have no task (as in `sdss_17`); scored a class-share and a uniform prediction on every fold with `data_foundry.v2.metrics.score` | holds | finite on all 8 folds: class-share 0.862 to 1.335, uniform 1.0986. Every test fold holds all 3 classes (smallest: 9,651 stars in 2019–20). No scoring columns needed; the target is the source's own 3 classes | MET-1, MET-2, MET-8 |
| 17 | The date is no model input (`time_of="label"`) | known, `temporal` | feature columns as the probes see them | holds | features: alpha, delta, u, g, r, i, z, cam_col | LEAK |
| 18 | `SpecObj` is the primary spectra; photometry all primary | download_description | SkyServer `PhotoObj.mode` on the join | holds | `mode = 1` for all 4,618,753 rows | PROV |
| 19 | Redshift, plate and fibre dropped | curation_comments | frame columns | holds | not in the frame | LEAK-1 |
| 20 | "Eight windows, against the 9 an IID split would get" | splits_comment | read against `sdss_17` (3 × 3 random folds) | holds, but obscure | the comparison is with the 3 × 3 IID default; a reader without that context will not follow it | writing |
| 21 | LightGBM scores about 0.448 at the 1M budget | record baselines | my 5-window fit | consistent | the same 5 windows averaged 0.464 in my run | — |
| 22 | All 99,999 Kaggle objects are in this set | record | — | untested | the Kaggle file was not loaded; the builder and issue 8 measured it | PROV-6 |
| 23 | Probe numbers (best single feature 0.718, 1-NN 0.68) | builder report | — | untested | left to the task gamer and the probes | — |

**What I refuted or found, ranked**

**1. 18,513 rows have the class of an empty fibre (validity, P5 / target; CLEAN-15 by analogy: the object's class is in effect missing; PROV-13: the origin has the flag to repair it).**
- **What the data shows:** zWarning bit 7 (UNPLUGGED) means the fibre carried no light from the object, and median S/N is 0. The pipeline's class then defaults to GALAXY on 97% of these rows, 45% of them point sources.
- **Effect on scores:** they are 0.33% of the 2012 test window and 0.87% of 2019–20. On 2019–20 they raise LightGBM's log loss from 0.467 on the other rows to 0.478 overall; their own loss is 1.76. On 2018: 0.457 to 0.466.
- **How this changes draft issue 1:** this is a narrow subset of the zWarning question that needs no weighing. Dropping these rows removes labels that describe no object, not hard objects (the worry about option B), so the test population barely changes.
- **Mildest remedy:** add `s.zwarning` to the 11 queries, drop rows with `(zwarning & 128) != 0` (about 18.5k, documented in a bullet), and keep issue 1's wider question (all zWarning ≠ 0) open. Also worth looking at the other spectrum-quality flags in that query, e.g. NEGATIVE_MODEL (bit 6: 5,916 STAR rows).

**2. The sky position lowers the score in every window, and the definition does not say so (Weigh; writing).**
- **The facts:** the claim that position is known before the spectrum holds (LEAK-10 is fine). But under these windows, adding alpha and delta to the magnitudes makes LightGBM worse by 0.013 to 0.066 (mean 0.033, about 7% of the loss). `sdss_17` measured 0.015 on 99,999 rows and kept the feature (its record says the position "teaches the sky footprints of past programmes"). At 1M training rows the effect is up to four times larger and is the largest single effect in the task: part of the benchmark ranks which methods ignore two columns.
- **Mildest remedy:** keep the feature (the earlier decision, and task fidelity over separability), and add a curation_comments bullet with these numbers, as `sdss_17`'s record has. Raise it as a Weigh item only if the curator wants to reopen that decision now that the effect is this large.

**3. Minor wording.** The builder report says the 155 sentinel objects are "all five bands"; it is 103 of them, and the README is correct. The splits_comment's "the 9 an IID split would get" needs `sdss_17`'s 3 × 3 context to make sense.

**Untested**
- **Kaggle containment (claim 22):** needs the Kaggle file. It was measured twice upstream (issue 8 and the 2026-11-25 screening); I left it.
- **Scores beyond five windows** and the probe numbers: not rerun.

Nothing was edited in the repository.

</details>

<details><summary>Column audit</summary>

I audited all 10 columns of the cleaned frame plus the columns that were dropped. I found **no leak**. The one real problem is the opposite: the cleaning leaves out imaging columns that an astronomer always uses, and adding them cuts log loss by about a quarter. There are also two smaller points for the curator. I did not edit the repository.

**Files of the release**

The source is SkyServer's SQL search, not a set of files. The definition joins two tables: `SpecObj` (the primary spectra) and `PhotoObj` (the imaging catalogue). Two sets of rows are left out, both with a reason:
- **Repeat spectra** (`SpecObjAll` minus the primary ones): left out by the primary-spectrum rule (`sciencePrimary`), which the definition states.
- **About 494k primary spectra with no imaging match** (5,112,724 against 4,618,753): they have no features to classify with. The record's screening gives both counts; `curation_comments` implies the reason ("with a photometric object") but never gives the number. Adding it would be a small edit.

What is missing is columns, not rows: the query takes 9 of `PhotoObj`'s hundreds of columns, the same ones as the Kaggle cut (problem 1).

**Column table**

| column | meaning | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| alpha | right ascension, from the imaging | yes, before the spectrum | float, no missing values | fine, with a question (problem 2): it acts as a stand-in for the plate's sky footprint and makes temporal scores worse | LEAK-10 (by analogy with plate), USE |
| delta | declination | yes | float | as alpha | as alpha |
| u, g, r, i, z | model magnitudes (`PhotoObj.u` is an alias of `modelMag_u`; checked on SkyServer) | yes. The values carry the DR13 recalibration (2016), made without the classes; the builder found shifts of at most 0.016 mag with no difference by class | float. The -9999 sentinel is set to missing (155 objects). Missing share is at most 5 per 10,000 in every year, so no column starts or stops being recorded. The 4 to 115 values below 10 mag (saturated bright stars) and 4 to 64 above 30 mag (near-zero flux) are unusual, not impossible, so keeping them is right | fine | CLEAN-10, CLEAN-11 |
| cam_col | which of the six camera columns took the image | yes | categorical, values 1 to 6. The dtype probe flags it as `numeric_levels`; categorical is right because it is a code | fine. It adds nothing (log loss ±0.001 with or without it). Keeping it while dropping run and field ("names the image") is inconsistent, but harmless | CLEAN-14 |
| date | night of the spectrum (from MJD) | no: it arrives with the class. Declared `time_of="label"`, so it orders the split and is never an input | datetime | fine | splits |
| ObjectType | the class the spectroscopic pipeline assigned | target | category with 3 classes, stripped of whitespace | fine (label quality is the builder's zWarning issue, not mine) | — |
| redshift (dropped) | fitted together with the class | no | — | the drop is right (stars sit at z≈0, standard deviation 4.6e-4) | LEAK-10 |
| plate, fiber_ID (dropped) | spectroscopic pointing and slot | no (they encode the targeting) | — | the drop is right | LEAK-10 |
| obj_ID, spec_obj_ID, run_ID, field_ID (dropped) | identifiers | — | — | the drop is right | CLEAN-3 |
| rerun_ID (dropped) | constant 301 (checked) | — | — | the drop is right | CLEAN-5 |

I also checked for near-copies across the split: only 49 pairs of objects lie within 2″ of each other in the whole set, so there are none to speak of.

**Problems, ranked**

**1. The imaging columns of the expert state are left out (CLEAN-1 and CLEAN-22, Should; question for the curator).**
- **The claim being tested:** the task is "judging from its images alone", yet the query keeps only the Kaggle cut's columns. `PhotoObj` also holds PSF magnitudes (`psfMag_*`), the pipeline's star/galaxy type (`type`, 3 = galaxy, 6 = point source), dust extinction (`extinction_*`) and sizes. All of them come from the same images and exist before any spectrum.
- **Why they matter:** the PSF-minus-model magnitude is the standard way to separate stars from galaxies, and SDSS's own `type` is defined from it.
- **What I measured:** I re-queried SkyServer for MJD 56935 to 58932 with these columns, kept the earliest spectrum per position as the definition does, and fitted LightGBM (400 trees) trained on all earlier spectra. Log loss, lower is better:

  | Test window | Training rows | Today's 8 features | + psfMag | + type | + psfMag, type, extinction | + also petroR50_r, fracDeV_r |
  |---|---|---|---|---|---|---|
  | 2019-2020 | 1.04M | 0.467 | 0.353 | 0.382 | 0.347 | 0.343 |
  | 2018 | 0.73M | 0.433 | 0.344 | 0.364 | 0.332 | 0.327 |

- **The same pattern elsewhere:** the sdss_17 issue's DESI test found the same with Tractor's morphology type (0.128 to 0.101).
- **Why it is a question, not a fix:** Andrej fixed the features on 2026-11-11 for sdss_17, when the Kaggle file had nothing else. Now the source is our own query, so that limit is gone. Adding the columns represents the task an astronomer actually does; it does not change the task to make methods separate better.
- **Mildest remedy:** add `psfMag_u..z` (a raw measurement) to the 11 queries, re-fetch (about 5 minutes, larger CSVs), and map -9999 to missing. `type` and `extinction_*` are each a separate call:
  - `type` is a rule-based output of the imaging pipeline, not a learned score, so CLEAN-6 does not forbid it.
  - `petroR50_r` carries the -9999 sentinel too (mean -125 in my pull).
- **Consequence:** the definition would then differ from sdss_17's features. That matters for retiring sdss_17 as a version of this dataset (PROV-6), so it belongs in the sdss_17 decision.

**2. Sky position stands in for the targeting footprint and makes every window worse (question for the curator, weak).**
- **What I measured:** LightGBM, 1M most recent training rows, up to 200k test rows. Log loss with alpha and delta against without them:

  | Window | With alpha, delta | Without |
  |---|---|---|
  | 2012 | 0.352 | 0.259 |
  | 2014 | 0.534 | 0.510 |
  | 2018 | 0.442 | 0.437 |
  | 2019-2020 | 0.468 | 0.457 |

- **Why:** position alone scores 1.0 to 2.5, worse than predicting the class shares. The model learns which programme covered which part of the sky in the training years, and that does not carry over. The record's own numbers show the drift: the median declination moves from 18° (2012) to 34° (2013), and 2020 is a single patch around α≈134°, δ≈1°. This is the reason plate was dropped (LEAK-10), arriving through coordinates.
- **Why I would still keep them:** they are known at prediction, carry real physics (star density depends on galactic latitude) and hurt rather than leak.
- **Mildest remedy:** keep them and say in `fit_reason` or `curation_comments` that position mostly records which programme was active. If the curator wants to remove the trap, galactic latitude would carry the physics without the programme's footprint.
- **Two smaller notes:**
  - Adding colours (u−g and so on) helps every window by 0.01 to 0.04. The benchmark's models should find that on their own, so this is information, not a remedy (CLEAN-2).
  - Problem 1's gain was measured with alpha and delta in the base set, so position may also be holding those numbers down a little.

**3. Some test rows are objects whose class the survey already knew (fit note, weak; USE, Selection Bias).**
- **What I measured on SkyServer:** in every range from 2010 to 2020, 5.6% to 7.7% of the primary spectra belong to an object that had an earlier spectrum in `SpecObjAll`. For quasars the share is 8% to 14%. These are eBOSS and TDSS re-observations of known quasars and replacements of poorer spectra.
- **Effect:** none of this is a copy across the split. The earlier spectrum is never in the data, and the object appears once. But these objects were picked for a spectrum because of a class the survey already had, which is not the use case ("objects with images but no spectrum").
- **Mildest remedy:** one sentence in `fit_reason` with these numbers. The stronger option is to drop the rows whose object has an earlier spectrum, which needs one more query per range; I would not make it the default.

**Checked and clean:**
- No column starts or stops being recorded within the history (missing shares are near 0 in every year).
- Median magnitudes step about 3 mag fainter from 2009 to 2010. That is BOSS taking over with fainter targets, a change in which objects were picked, not in how they were recorded.
- The ordinal check does not apply (no ordinal columns).
- There is no training weight, so the weight check does not apply.
- There are no ids that encode the label and no values fitted over the whole release beyond the DR13 recalibration, which the builder already checked.

</details>

<details><summary>Split audit</summary>

**Verdict: right with notes.** I reached the same leaf the definition names. The windows meet the floor and the size rules. The reason given for "no gap" doesn't hold, and the gap changes scores a lot, so the curator has to decide it in the Horizon block.

**The tree (SPLIT-36)**
- **Collection type `Survey` → [SUR.meets]:** the use case is "choose targets for spectroscopy", which here means the targets of the next programme. The answer is *the surveyed population at a later round*, so the next step is the **Order and windows step**, keyed on the spectrum's night (MJD).
- **[ORDER.order]:** yes. The night is recorded, and the class arrives with the spectrum.
- **[ORDER.windows]:** yes. There are 8 one-year windows from 2012 on, all at or above the 50% floor.
- **[ORDER.small]:** no. The table has 4.6M rows.
- **Leaf:** **L-ORDER.windows**. This is the same leaf as `split_leaf`, the `splits_comment` and `sdss_17`, and it matches the split and tag that ship. No leaf was forced.
- **Note for the curator:** the use case's other half, "build catalogues", means objects imaged in the same years that never got a spectrum. That reading answers [SUR.meets] with the fill-in branch instead, which leads to a random or same-time split. The leaf above holds for the targeting reading, which `sdss_17` already settled with the curator. The record's measurements show the year windows are the stricter test: LightGBM log loss 0.473 against 0.315 for a random 5-fold split on 300k rows. I suggest no change.

**Checked and found sound (numbers recomputed from the definition)**
- **Windows match the comment:**

  | Window | Test rows | Training rows | Training share |
  |---|---|---|---|
  | 2019-2020 | 62,946 | 4,555,738 | 98.6% |
  | 2018 | 314,284 | | 91.8% |
  | 2017 | 257,920 | | 86.2% |
  | 2016 | 211,990 | | 81.7% |
  | 2015 | 159,730 | | 78.2% |
  | 2014 | 243,837 | | 72.9% |
  | 2013 | 474,140 | | 62.7% |
  | 2012 | 500,000 of 579,075 (capped) | 2,314,762 | 50.1% |

  - Every training side ends before its test window starts. The class mix moves with the programme: quasars are 15–17% of the test rows in 2012–13 and 30–48% from 2014.
  - No window is under the half floor, so there is no SPLIT-14 exception to raise.
  - Every test window holds far more than 33 rows.
- **Time column:** it is the night of the spectrum, which is when the label arrives (`time_of="label"`, not a model input). The pipeline reduces a spectrum within days, so no labels are still in flight at a cut. A training side ends at a window's start, so it holds no outcome that is still open.
- **Newest period:** the drop in rows per day is the survey ending, not a cut in the download.
  - 2019 has 41,475 rows in January, 13,723 in February and 1,774 in March, as eBOSS ended on 1 March 2019. There are about 17 rows in total from April to June 2019.
  - 2020 has 5,957 rows from 8 plates in February and March, before the observatory closed for COVID-19.
  - Rows per plate-night stay normal (876 and 840). The quasar share of 48% continues the eBOSS level of 2014 onward, not a selection by outcome.
- **Recurring entities:** the definition drops the 69 repeated positions, keeping the earliest spectrum. After that every photometric object appears once.
- **Plates across a window boundary:** 70 plates hold rows in two windows. That puts 15,061 test rows (0.65%) on a plate that also has earlier rows. These are different objects, and plate is not a feature, so it is harmless.
- **Training weight:** none.

**Problems, ranked**

**1. The "no gap" reason is wrong, and the gap is worth up to 0.18 log loss on average (SPLIT-10, SPLIT-12; Should, and the curator signs off).**
- The `splits_comment` says a public user "waits for the next release, which the one-year windows already stand in for". The length of a test window is not a gap: each training side ends on the window's first day. A public astronomer at a window's start only has the last data release, whose newest spectra are 0.5 to 3.5 years old.
- I fit untuned LightGBM (300 trees) per window, on 1M rows from v0.2's default sampler (newest year back), and scored it on a random 100k test rows. Lower is better:

  | Gap | Mean log loss | Training shares that fall under 50% |
  |---|---|---|
  | none (implemented) | 0.450 | none |
  | 6 months | 0.495 | 2012 at 45.9% |
  | 18 months | 0.590 | 2012 at 35.5%, 2013 at 46.0% |
  | the public release available at each window's start | 0.635 | 2012 at 31.9%, 2013 at 46.3% |

  - Per window, the 18-month gap costs 0.03 to 0.40. The largest losses are in 2012 (+0.40), 2017 (+0.26) and 2013 (+0.19), where the gap removes the first data of a new programme (BOSS, then eBOSS).
  - The release cutoffs in the last row are from my memory of the data release papers and need checking:

    | Window | Newest spectra public at its start |
    |---|---|
    | 2012 | DR8, through July 2009 |
    | 2013 | DR9, through July 2011 |
    | 2014 and 2015 | DR10, through June 2012 |
    | 2016 | DR12, through June 2014 |
    | 2017 | DR13, through May 2015 |
    | 2018 and 2019 | DR14, through May 2016 |
- **No gap is defensible for the survey's own use:** the collaboration has its reduced spectra within days and plans the next plates from them. That is the "choose targets" reading.
  - Even then there is a planning lead that nobody has measured. Plates are drilled weeks to months ahead, and eBOSS chose its targets once before the programme began.
- **Mildest remedy:** keep no gap and rewrite the reason so it names the survey-internal user, the release lag a public user faces, and the measured cost in the table above. Any gap of 6 months or more puts 2012 under the floor (and 2013 too at 18 months), so it would need dropping those windows or a SPLIT-14 exception.

**2. The comment states the wrong IID target (SPLIT-15 with SPLIT-33; text only).**
- It says "Eight windows, against the 9 an IID split would get". Two thirds of 4.6M units is far over 250,000, so an IID split gets 1 repeat of 3 folds: 3 splits. The 8 windows exceed the target.
- The "2011 window would train on 39.4%" part is right.
- **Remedy:** change "9" to "3", and say that the count is limited by the floor, not reached.

**3. The `Target: Revised Later` caveat is already recorded correctly (note, no action).** Both sides carry DR17's labels. The builder measured 1.74% of classes changed between DR12 and DR17, with no dependence on time that favours either side.

**Horizon block (for the main session)**
- **Verdict:** the length of one year stands; the gap needs the curator's decision.
- **What the source states:** the data release dates: DR8 in January 2011, DR9 in July 2012, DR10 in July 2013, DR12 in January 2015, DR13 in July 2016, DR14 in July 2017, DR15 in December 2018 (no new eBOSS spectra), DR16 in December 2019. They give a refit cadence of 12 to 18 months.
- **What we assume:**
  - the refit happens yearly on calendar years rather than on release dates;
  - the internal user, which gives no gap;
  - 2019 and 2020 merged into one window (the curator's call of 2026-11-12).
- **Time frame:** every year from 2012 on, the earliest the floor allows. The windows cover the end of BOSS and all of eBOSS. Each SDSS-I/II year before 2012 would train on under 50% (2011 at 39.4%), so none is tested.
- **Options** (the gap's effect on scores is in problem 1):

  | Length | Windows | Test window sizes | Training shares | Covers |
  |---|---|---|---|---|
  | **1 year (implemented)** | 8 | 63k to 500k (2012 capped) | 50.1% to 98.6% | BOSS 2012–14, eBOSS 2014–19 |
  | 6 months | 15 (2019 H1 plus 2020) | 63k to 389k | 50.1% to 98.6% | the same years, twice the windows |
  | 2 years | 4 (2019–20, 2017–18, 2015–16, 2013–14) | 63k to 474k | 62.7% to 98.6% | 2012 dropped or merged into 2011–12, which falls under the floor |

  - The 6-month windows step more often than any release did, and the 2-year windows step less often than releases did.
- **Recommendation:** keep the 1-year windows with no gap. Write the survey-internal user as the reason, and quote the cost of the public-release lag (+0.14 to +0.19 mean log loss, 18-month gap against release cutoffs) so the curator signs off knowing it.

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner: `sdss_dr17_star_galaxy_quasar_1m`**

**My role:** an astronomer who builds a photometric star, galaxy and quasar catalogue, or picks quasar candidates for the next season of spectroscopy, using a classifier trained on the spectra taken so far. This is the use case in `task_summary`. Published work does the same thing: Clarke et al. 2020 (A&A 639, A84) classified 111M SDSS sources that have no spectrum, and eBOSS and XDQSO picked quasar targets with classifiers trained on earlier spectra.

**Fit: **approximate**, and I agree with the declared fit**
The use case is real and the target is the right one. A spectroscopic class is the label everyone trains these classifiers on (USE-1, USE-5). Two things keep the fit approximate (USE-8):
1. The rows were already chosen for a spectrum by their colours. The definition says so.
2. The inputs leave out the imaging measurement I would always use to separate stars from galaxies. That is finding 1, which is new.

**Gaps, ranked by how much they change the task**

**1. There is no morphology input (USE-6, USE-3).** This changes the task the most.
- Separating stars from galaxies in SDSS starts with morphology. The photometric pipeline's own `type` comes from psfMag − cModelMag > 0.145. Every photometric classifier in the literature takes PSF and model (or cModel) magnitudes.
- Those columns sit in the same `PhotoObj` row as `u…z`, exist before any spectrum and use the same DR13 calibration. Under USE-6 they are legitimate inputs, including the survey's own photometric `type`.
- The dataset gives only model magnitudes, so the model has to separate stars from galaxies by colour alone. No practitioner would accept that.
- **My measurement:** I queried SkyServer with the dataset's own join plus `psfMag_ugriz`, `type`, `petroR50_r`, `extinction_r` and `zwarning`, then trained untuned LightGBM on one year and tested on the next (log loss, lower is better).

  | train → test | shipped 8 features | + psfMag ×5 | ugriz + psfMag (no position) |
  |---|---|---|---|
  | 2014 → 2015 | 0.497 | 0.373 | 0.357 |
  | 2015 → 2016 | 0.517 | 0.367 | 0.340 |
  | 2014 → 2016 | 0.595 | 0.401 | 0.341 |

  - When I train on 2014 and 2015 together and test on 2016, star recall goes from 0.61 to 0.79 and accuracy from 0.79 to 0.88.
  - The photometric `type` alone gets most of that gain (0.380 against 0.501).
  - About 3% of DESI's measured objects also give a large morphology gain (the issue's table: MORPHTYPE 0.101 against 0.128).
- **Caveats:** these are one-year training sides, not the 1M default sampler. The rows are close to the shipped rows but not identical (no position dedup). The size of the effect is still far beyond noise in all three pairs.
- **Precedent:** none. No `sdss_17`, `sdss_dr17` or `desi` record mentions PSF magnitudes or morphology, and `sdss_17` inherited its columns from the Kaggle query. Adding the columns is cheap because the 11 queries are already in `download_description`.
- **Recommendation:** add `psfMag_u…z` to the queries. Optionally add `type` (as a categorical) and `extinction_u…z`. This puts the task in the state an expert would use. It does not change the task to make methods separate better: it supplies the inputs the actor really has.

**2. Sky position (`alpha`, `delta`) mostly records which targeting programme covered a field, not physics.** Medium.
- In the table above, position plus `cam_col` makes the next-year score *worse* than ugriz alone: 0.497 against 0.473, 0.517 against 0.455, and 0.595 against 0.458.
- The reason is that the programme footprints, such as eBOSS areas and the deep quasar fields, change from year to year.
- An expert would keep only what position means physically: Galactic latitude (star density) and extinction, which `extinction_*` gives directly.
- I would not remove position on my own authority. It is known at prediction time, and a model that misuses it pays for that in the score. The README should name it as a programme proxy that the year split punishes.
- `cam_col` is a camera slot with no astrophysical meaning. Removing it has no effect (0.498 against 0.497). I would drop it, at low priority.

**3. Labels flagged by `zWarning` (builder's draft issue 1).** Medium.
- I would never train on, or validate against, spectra the pipeline flags as unreliable. Standard practice is `zWarning == 0`, and DESI's own filter is `ZWARN = 0`.
- In 2016, 15.6% of test spectra are flagged.
- **My measurement (train 2014–15, test 2016):**
  - The model scores 0.436 on clean test rows and 0.853 on flagged ones.
  - Training on clean rows only improves the clean test rows to 0.395.
- So the flagged rows inflate the loss, and their share grows in later windows (4% before 2012, 17–22% from 2017). That turns part of the windows' difficulty into label noise.
- I support option B: fetch `s.zwarning` and drop the flagged rows. When I measured the same 2014–15 → 2016 case, the flagged share was 19% of galaxies, 13% of quasars and 13% of stars. That is not strongly tilted by class, so B removes noise more than it reshapes the classes.

**4. The test population is still spectroscopic targets, not the objects without spectra.** Known and declared.
- The objects I really classify are fainter on average than the spectroscopic galaxy limit (r < 17.77 for the main galaxy sample) and are not pre-selected by colour.
- The year split does copy one real workflow faithfully: retraining before each season's target selection.
- No change is possible here, and the `fit_reason` already says it.

**5. One row is one object, which is my unit of decision.** OK.
- The windows matching yearly data releases (DR8 to DR16) is a reasonable refit cadence.
- Keeping the date out of the inputs (`time_of="label"`) is right.

**Would I use this model?**
- With the shipped features, no. It confuses 39% of stars, and 15% of objects predicted as quasars are galaxies. A catalogue built that way would not be credible next to Clarke et al. or the photometric `type`.
- With PSF magnitudes added, and trained and scored on spectra with `zWarning = 0`, yes as a first pass. I would trust it if its calibration held per window and if quasar purity at my fibre budget held up when the programme mix changes.

**Metric: **yes** (log loss)**
- A catalogue publishes class probabilities. Log loss is a proper scoring rule on exactly those probabilities (MET-1, MET-8).
- Quasar target selection would really be judged by purity among the top k candidates for a fibre budget (a `precision_at_k` on QSO). No source fixes k or a cost (MET-7), and class imbalance alone does not justify a PR-type metric (MET-9). So the fallback `log_loss` is the right choice, and the hard-label accuracy reported in papers is not (MET-6).
- One weakness: the class mix changes by window (quasars 14% to 48%), so part of the log loss measures how well a model tracks the shifting class priors. That reflects the real drift and is acceptable.

**What an expert would change**
1. Add `psfMag_u…z` to the query, and optionally `type` and `extinction_u…z`.
2. Fetch `zwarning` and keep only `zWarning == 0` (option B).
3. State in the README that sky position stands in for the programme footprint, and optionally drop `cam_col`.

**Sources**
- The worktree's `dataset.py`, README, the record, the builder report, `sdss_17`'s issues, `use_case.md` and `metrics.md`.
- SkyServer DR17 SQL queries run today (2014, 2015 and 2016 spectra with morphology columns; 243,838, 159,734 and 211,993 rows).
- Lupton et al. / the SDSS photometric `type` definition (psf − cModel > 0.145).
- Clarke et al. 2020, A&A 639, A84 (photometric classification of 111M SDSS sources from PSF and cModel magnitudes plus WISE).
- Bolton et al. 2012 (`zWarning`).
- Myers et al. 2015 (eBOSS quasar target selection).

The literature details are from my own knowledge; I did not search the web this run.

</details>

<details><summary>Precedent check</summary>

**Precedent check: sdss_dr17_star_galaxy_quasar_1m (precedent-checker, 2026-11-25)**

I checked 12 decisions in the definition and the builder's draft issues against the records' CC lines, the `Resolved` turns of sdss_17's `## Review`, the issue item `sdss_17`'s issues, the knowledge files (TP-6, SPLIT-14/17/20/21, LEAK-10, PROV-6) and the register's flags. **One real departure has no stated reason (finding 1). Two items need a better-written reason (findings 2 and 3). One fact disagrees between the two SDSS records (finding 4). The rest are consistent.** Andrej's sdss_17 decisions show no drift between 2026-11-11 and 2026-11-19, and no exception is on its third use.

**Findings**

**1. Departs without a stated reason: a pipeline-class target is shipped here, but held on DESI DR1 by another curator for its label correctness**
- **Precedent:** `desi_dr1_star_galaxy_quasar`, **CC (2026-11-05, Myunghwan)**, now `DF: Suspended`.
  - The task is the same one: star, galaxy or quasar from photometry, the target the spectroscopic pipeline's class.
  - The reason he gave: "Credible physical-class correctness above 90% has not been established for the intended population … do not continue qualification or build."
  - The AI Assessment the same day: do not "equate a reliable spectral fit with a verified physical class". It would reopen only with "independent label validation or source-supported repair".
- **This case:** the same kind of target, built and recommended for shipping. The record, the definition and today's issue never take up that bar.
  - The record's sibling line calls DESI "`TBD -> Yes`, 1: another survey". It leaves out the suspension and its reason.
  - Issue 10 rejects DESI on other grounds (easier, no time structure).
  - sdss_17 (shipped 2026-11-12, Andrej) never faced the bar either: its 9 resolved issues contain no "correctness", "visual inspection" or "physical class".
- **What could set SDSS apart, none of it written down:**
  - `task_summary.predicted` defines the target as "the class the survey's spectroscopic pipeline assigned", not a physical class.
  - SDSS publishes visual-inspection catalogues, for example the DR16Q superset. I did not open them, so this is not verified.
  - DR17's `zWarning` is a quality flag the source itself defines.
- **Why it matters for the draft review:** this bears directly on the builder's issue 1. The DESI hold names "source-supported repair" as a way out, and also says a reliable fit (ZWARN = 0) alone is not a verified class.

The draft for the record's `## Review`:

> **Consistency check (AI, 2026-11-25): does the label-correctness bar that suspended DESI DR1's star/galaxy/quasar task apply to DR17's pipeline classes, and if not, what sets them apart?**
>
> * **Problem:**
>   - Myunghwan suspended `desi_dr1_star_galaxy_quasar` on 2026-11-05: "Credible physical-class correctness above 90% has not been established for the intended population"[^cons]. A reliable spectral fit is no verified class, it said, and the task reopens only with independent validation or source-supported repair.
>   - This dataset's target is the same kind: the SDSS pipeline's class from one template fit with the redshift (Bolton et al. 2012). DR17 flags 8.0% of these classes as unreliable (`zWarning` ≠ 0; 13.3% of quasars), and 1.74% of the classes changed between DR12 and DR17. `sdss_17` shipped on 2026-11-12 without this question being asked.
>   - Ship DR17's classes as they are, set a bar for both, or hold both?
> * **Options:**
>
>   | | Option | Pro | Con |
>   |---|---|---|---|
>   | a | Exception for SDSS: the target is defined as the pipeline's class, not the physical class, and the DR17 paper and SkyServer document the pipeline and its `zWarning`. Recorded with that fact; DESI's hold stays on its own physical-class framing | ships as built; the task says what it predicts | DESI's target is the pipeline's `SPECTYPE` too, so the same fact may lift its hold |
>   | b | Treat SDSS like DESI: hold until pipeline-against-visual-inspection agreement is shown above the bar (for example from DR16Q) | one bar for both surveys | blocks the replacement of `sdss_17`; `sdss_17` would need the same check |
>   | c | Reopen DESI's hold to match SDSS: a documented pipeline class with its quality flag is a valid target | removes the double standard | overrides another curator's decision; DESI's ease (log loss 0.11) remains |
>   | d | Amend: state when a pipeline-assigned label is a valid target (documented pipeline, source quality flag applied or shipped), in the rule file that covers it | settles both and later surveys | a rule change for two cases |
>
> * **Recommendation:** a, written down with its fact, and the same fact offered to Myunghwan's hold (c as a question to him). If the curator wants a bar, d with B of issue 1 (drop `zWarning` ≠ 0) as the source-supported repair.
>
> [^cons]: principles.md, "Consistent judgement", case 2: a precedent with similar facts decided the other way, by another curator. **TP-6** (Must): a valid task stays; a better version the source itself defines replaces it, and a fix of our own invention does not.

**2. Issue 1 (`zWarning`, recommendation B): no settled precedent, so whatever the curator decides becomes the first one**
- **Closest cases:**
  - DESI's planned filter in today's issue 10 notes ("filter … ZWARN 0", from the DR1 page's "useful spectra"). The AI proposed it the same day, but it is not decided. Recommendation B is consistent with it.
  - sdss_17 kept these rows only because the Kaggle file has no `zWarning` column. That is a constraint, not a decision, so B departing from sdss_17 has a stated fact: the column is now available.
  - `lung_adenocarcinoma_metastasis`: label doubts the source names are kept as coded and never relabelled. B drops rows rather than relabelling them, so this case is near but not the same.
  - `sarcoma`: uses the study's own reviewed labels, which excluded uncertain types. This is the source's own quality control and leans toward B.
  - TP-6: a fix of our own invention such as "dropping near-ties" is not a better version. `zWarning` is defined by the source, so B passes TP-6 only if that is said explicitly.
- **To fix in the draft:**
  - The builder lists "task easier" among B's effects. That must not appear as a reason (task fidelity over separability). The reason is label reliability alone.
  - The issue should cite the DESI hold (finding 1).
  - After the decision, add a row to the relevant rule's Cases table.

**3. Merging 2019 and 2020: follows sdss_17 issue 7, B (Resolved 2026-11-12, Andrej), but the fact behind it has changed**
- **Then:** the merge rested on a 2020 window of 141 test spectra, with a standard error of 0.083 (SPLIT-17, SPLIT-20).
- **Now:** the 2020 window holds 5,957 spectra, 42 times as many.
  - What still holds: 8 plates of one programme (eFEDS) before the COVID closure. Issue 8 measured a standard error of 0.061 for that window alone, and SPLIT-20 calls for widening an atypical newest window.
  - So the merge is still consistent with its reason.
- **The problem is the written reason:** the splits comment justifies the merge by "every spectrum stays tested", which nine windows would also do.
  - It should name the 8 plates and the atypical newest window instead.
  - Separately, the builder's 9-window alternative is a fair question for the curator and is not decided by precedent.

**4. A collection fact disagrees between siblings**
- **The fact:** this record adds `Target: Revised Later`, measured on DR12 against DR17. sdss_17 lacks the tag although its labels are the same DR17 classes.
- **When it matters:** it does not matter if issue 10's B (retire sdss_17) is taken. If the curator keeps sdss_17 (A), both records should carry the tag.

**Consistent with precedent**

| Decision | Precedent |
|---|---|
| Redshift, plate and fibre dropped | sdss_17, CC 2026-10-01 (Lennart), 2026-11-11 (Andrej) |
| Date orders the split but is no model input (`time_of="label"`) | sdss_17 issue 6, A, 2026-11-12 |
| `cam_col` as a category | sdss_17, 2026-10-31 (Lennart) |
| Fallback log loss | sdss_17, MET-1, 2026-10-21 |
| `Selection Bias` marker, approximate fit | sdss_17 |
| Eight windows; no 2011 window, which would train on 39.4% | sdss_17 issue 9, A, 2026-11-19 (there 40.4%) |
| 2012 test window capped at a random 500,000 drawn within the classes | fugaku_hpc_job_failure_1m (`sample_temporal_splits`, `stratify_on`) |
| Training sides left whole, sub-sampled by the default sampler | the row-budget rule of 2026-11-12, as issue 10's notes say |
| One spectrum per position, the earliest | sdss_17 kept the first in file order; the earliest is stricter and gives its reason |
| `Features: Revised Later` (DR13 recalibration) kept after an as-of check | LEAK-10, as for tunisian_fraud_detection_challenge (2026-11-05, Lennart) |
| Replace sdss_17 and retire it as a `Duplicate` | PROV-6 / TP-6, as thyroid_discordant_archive / thyroid_discordant (2026-11-12, Andrej; the old record was retired the same day, after his question) |

The register's `opposite_outcomes` flag on PROV-6 (1 keep, 5 exclude) holds no pair with this case: retiring the cut is on the majority side.

</details>

<details><summary>Blind review</summary>

I would include this dataset, with changes: drop `alpha`, `delta` and probably `cam_col`, and describe the temporal split as a test of shift between survey programmes, not of deployment over time.

**What the task is**

The table holds the SDSS DR17 objects that got an optical spectrum. The features are five-band photometry (`u g r i z`), sky position (`alpha`, `delta`) and camera column (`cam_col`). The target, `ObjectType`, is the class the spectroscopic pipeline assigned: GALAXY 60.4%, STAR 20.8%, QSO 18.8%. `date` is the spectrum's observation date. Spectroscopic redshift, plate, fiber and spec ID are absent, which matters: redshift alone almost settles the class (it is what makes the well-known 100k Kaggle "Stellar Classification SDSS17" version easy, around 97% accuracy).

The use is real. Classifying stars, galaxies and quasars from photometry is what surveys do for the billions of objects that never get a spectrum, and their spectroscopic samples are used to train those classifiers. The values look like genuine SDSS data:
- There are no duplicate positions, even when rounded to 0.36 arcsec, so repeat spectra appear to have been removed.
- Class medians make physical sense: QSOs have a flat spectrum (u−r ≈ 0.7) and galaxies are red (u−r ≈ 2.8).
- Missing values are few (about 35 per band) and appear to be former −9999 sentinels already turned into NaN.

There is plenty of signal and it is not trivial. LightGBM reaches 0.89–0.90 accuracy on a random split and 0.82 on a temporal split, against 0.605 and 0.476 for predicting the majority class. With 4.6M rows, size is no issue.

**Concerns, most serious first**

1. **Sky position is a shortcut to the survey programme, and it hurts under the temporal split.**
   - Position alone (`alpha`, `delta`, `cam_col`) gives 0.630 accuracy against 0.605 for the majority class on a random split. On the temporal split it gives 0.470, slightly below the 0.476 majority rate.
   - Adding these columns to the magnitudes helps a little on a random split (0.892 vs 0.886) but costs a lot on the temporal one: accuracy drops from 0.821 to 0.770, and log-loss rises from 0.51 to 0.58.
   - The model is learning which sky areas each programme observed (SEGUE star fields, eBOSS quasar fields), not anything about the object. A classifier used on the whole sky could not rely on that.
   - `cam_col` (which of the camera's six columns imaged the object) is an instrument detail with no physical meaning.
   - Change: drop `alpha`, `delta` and `cam_col`, or at least note the issue in the documentation.

2. **The temporal split measures shift between survey programmes.** The class mix swings with the programme running at the time:

   | Years | Programme | Class mix |
   |---|---|---|
   | 2000–06 | SDSS-I/II Legacy | about 65–79% GALAXY |
   | 2007–09 | SEGUE | STAR rises to 48% / 59% / 89% |
   | 2010–13 | BOSS | about 70% GALAXY |
   | 2014–20 | eBOSS | QSO at 35–49% |

   - The test windows, mostly 2015 onward, contain far more quasars than the training data (training is about 13% QSO overall).
   - So test windows score how well a model copes with a change in which objects were targeted. That is a valid test, but a different one from "predict the next batch from the same process".
   - Change: keep the split, but describe it as shift between programmes. Expect scores to vary a lot across the 8 windows. A random or sky-grouped split is a reasonable alternative.

3. **The spectroscopic targets were pre-selected by colour.** Each programme picked which objects to observe using colour cuts aimed at a particular class. The table is therefore not representative of "all photometric objects", and classifying within those targets is partly re-learning the cuts. This is normal for SDSS-trained classifiers and not a reason to exclude, but it limits how far the results carry over to real use.

4. **Smaller preparation points.**
   - Colours (u−g, g−r, and so on) are not included. Tree models gain slightly from them (0.897 vs 0.886), so leaving them out is acceptable.
   - 26 rows have identical magnitudes in all five bands. This is negligible, though it may be leftover duplicates or placeholder values.
   - About 50 values per band are outside the usual 12–29 mag range: faint ends up to 31–32 mag and bright ones down to 6.5–10 mag. These are probably saturated or very faint measurements. They are harmless, but could be filtered.
   - `ObjectType` is correctly stored as categorical, and `date` is correctly kept out of the features.
   - No training weight is assigned, which is fine.

**What I could not check**

- **The exact query:** which magnitude type (model, PSF or petrosian), whether rows were restricted to primary spectra, and whether spectra with redshift warnings were removed. I could not see the SQL, and I did not open or confirm any of the source links.
  - If spectra with warnings were kept, part of the labels are unreliable: a small fraction of SDSS pipeline classes are wrong. Filtering on the redshift-warning flag (`zWarning = 0`) would be worth doing.
  - Whether the magnitudes are model or PSF magnitudes changes how separable stars and galaxies are.
- **The sample:** I worked on the 1M-row sample, not the full 4.6M rows.
- **The splits:** I scored one 80/20 temporal cut, with the test period starting 2015-10-07, not the actual 8 windows.

</details>

<details><summary>Task gamer</summary>

The task can be gamed only a little: no row copies, ordering or format artefacts carry the label. The one exploit that works uses the test window's own composition, cutting log-loss by about 0.047 (10%).

All numbers are mean `log_loss` over the 8 test windows, lower is better. Every model was trained on a random 400k-row sample of its training set (the full sets have 2.3M–4.6M rows); test sets were scored in full. The baseline (an untuned LightGBM on the 8 shipped features) scores **0.4737**. Adding a column of random numbers moved the mean to 0.4728–0.4744 and each window by up to about ±0.005; that is the noise level for the gains below.

**Exploits**

| # | Exploit | Script | Honest score | Exploited score | Gain (per split, range) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| 1 | Co-window sky context: features built from the unlabelled rows observed in the same year within the same sky patch, including the test window's own rows | the gamer's feature script | 0.4737 (baseline) / 0.4482 (recent-3-years) | 0.4268 / 0.4166 (with recent-3-years training) | −0.047 vs baseline (per window: −0.102 to +0.007; 7 of 8 better, r5f0 slightly worse); −0.032 vs recent-3-years | Mostly no (see below) | Give the targeting program or plate as a real feature, or test on held-out sky regions |

**Mechanism.** The class mix changes a great deal from year to year: QSO share of the test windows runs from 15% (2012) to 48% (2019). The shift follows the survey programs (eBOSS QSO plates, ELG plates). For each row, the features describe its 30 nearest neighbours in the same year: their mean colours and magnitude, their share of blue (u−g < 0.6) objects, how close they sit, and how many lie within a plate radius (1.49°). For a test row, those neighbours are the other test rows. These features carry no label, and fitted alone they score 0.918, close to a model that only knows the class shares. Their value is in telling the model which program a sky patch was observed under, which corrects the photometric model per window. The gains are largest in 2017 (r2f0, −0.10) and 2012 (r7f0, −0.10).

**Judgement.** A deployed classifier would know a plate's target list once the plate is designed. It would not know the set of objects whose spectra end up dated in the same calendar year, and that is how the benchmark builds its windows. The decisive fact is whether the use case runs at plate design (the gain is then partly signal) or at photometric target selection (the gain is then an exploit).

**Mildest fix.** Ship the targeting program or survey (e.g. SDSS-I legacy, BOSS, eBOSS) as a feature, which is known before the spectrum. That makes the transductive proxy redundant and the honest model much stronger. Alternatively, split by sky region as well as by time.

A smaller caveat on the same features: only 500,000 of the 579,075 rows from 2012 are in that test window. The other 79,075 rows are in neither training nor test, and my co-window features for 2012 also used them, a small extra.

**Flaw that hurts an honest model**

| Flaw | Honest choice | Baseline | Honest score | Gain |
|---|---|---|---|---|
| Training includes SDSS-I/II years (QSO share 9–11%) whose targeting no longer matches the test years | Train only on the last 3 years before each window | 0.4737 | 0.4482 (last 5 years: 0.4660) | −0.026 on average; better on 7 of 8 windows (−0.06 on r6f0, −0.05 on r2f0); worse on r5f0 (2014): 0.5447 vs 0.5107 |

Every split trains on all rows from 2000 onward, so early surveys with a different target mix dominate the training set. A model at the prediction point would rightly weight recent programs, and doing so is honest. The fix to the task is to cap the training history (for example the last 3–5 years), or to supply the program id so that old rows stop misleading the model.

**Attacks that found nothing**

- **Value formats:** magnitudes carry 5 decimals and positions 12–13 at the same rate in every class. About 300 rows have missing magnitudes, spread across all classes. There are pile-up values (u = 24.635 in 11k rows, mostly stars, and z = 22.827) that look like zero-flux magnitudes; these are real physics a model sees anyway, not an artefact. `cam_col` class rates are flat (59–61% galaxies).
- **Row order:** rows are sorted by date and shuffled within each date. Next-row label agreement is 0.5493, against 0.5492 after a shuffle within each date. Position within a date has the same distribution for all three classes.
- **Copies across the split:** no two rows lie within 1″ of each other, except 2 pairs, so the data was de-duplicated by object. Only 4,840 rows have a neighbour within 3″, and they share its label 76% of the time. Only 103 rows have duplicated photometry. There is nothing to look up.
- **Labels of nearby training rows:** the share of each class among the 30 nearest training rows makes things worse, 0.5266 against 0.4737.
- **Re-estimating the test class mix from the test predictions (EM):** much worse, 0.745. The photometric model is badly miscalibrated under this shift and over-estimates the QSO share (0.65–0.77 against true 0.30–0.48 on windows r0f0–r4f0).
- **Weight, scaled or ranked columns, columns from after the prediction point:** there is no training weight, and no columns standardised over all rows. Redshift, plate, MJD (the observation date) and fiber (the leaky columns in the Kaggle "SDSS17" version) are absent.

**Public file lookup.** Matching alpha/delta against SkyServer's SpecObj table (DR17) would return each row's class. That works for any public dataset and is not ranked here.

**Not checked**

- I did not tune the per-row neighbourhood features or try other radii, so the 0.047 gain is a lower bound.
- I did not run a classifier separating training from test rows.
- I did not test whether some test plates are re-observations of sky fields already in training.

Web search found only Kaggle notebooks for the 100k-row SDSS17 version and no leak threads that apply here ([Stellar classification overview](https://lana7am.github.io/Stellar_Classification/about.html), [arXiv 2503.09220](https://arxiv.org/pdf/2503.09220)).

</details>

<details><summary>Advocate</summary>

**Advocate's opening brief: `sdss_dr17_star_galaxy_quasar_1m`**

**Position:** ship it. The split, the target and the metric are right as they are. Two fixes are cheap and both come from the source itself: add the PSF magnitudes, and drop the 18,513 spectra from unplugged fibres. Neither fix changes the task, so neither is a reason to hold the dataset. Every other open point needs only a rewritten comment.



**1. Validity holds: no leak, and the data is what it claims (P4 and P5 above everything else; LEAK-10 Must, PROV-1)**
- **Evidence:**
  - The claim auditor tested 22 claims. All 22 hold and none of the written claims is wrong.
  - The columns that carry the label are gone: redshift, plate and fibre were dropped, and the date is no model input (`time_of="label"`; claims 17 and 19).
  - The as-of check on the DR13 recalibration is clean: photometry moved at most 0.016 mag, the same for every class (claim 12). The column auditor found no leak in any column.
  - The task gamer found no exploit in copies, row order, value formats or the labels of nearby training rows.
  - After the position dedup no object appears twice: 0 pairs lie within 0.5", and at most 5 pairs straddle a window boundary at 2".
  - SkyServer returned the same 4,618,753 rows again on 2026-11-25.
- **Why it matters most:** validity outranks everything the other side can raise. No panelist found a validity failure that cannot be fixed inside the definition.

**2. This is the source's own better version of a task that already ships (TP-6 Must, PROV-6 Must)**
- **Evidence:**
  - The query is the Kaggle cut's own query without its `TOP 100000`. It has the same 18 columns, all 99,999 Kaggle objects, and 46 times the rows.
  - Under the v0.2 row budget, untuned LightGBM scores 0.448 here against 0.494 on the cut's rows. It beats logistic regression in all 8 windows.
  - The test windows grow from 1,076–11,044 spectra to 62,946–500,000 (`sdss_17`'s issues). Issue 8 measured that the standard error of a model gap halves.
- **Rule:** TP-6 says a better version the source itself defines replaces the current one. That is what this dataset is. The precedent checker finds the retirement of `sdss_17` on the majority side of PROV-6 and parallel to `thyroid_discordant_archive` (2026-11-12, Andrej).
- **What it answers:** any wish to keep `sdss_17` instead, or to ship both.

**3. The split mirrors the application, and adding a gap would break a Must (SPLIT-14 Must over SPLIT-10 Should)**
- **Evidence:**
  - The split auditor walked the decision tree on its own and reached the leaf the definition names, L-ORDER.windows.
  - Every window trains on at least 50.1% of the rows (2012). Every training side ends before its window starts. No labels are still in flight at a cut, because the pipeline reduces a spectrum within days.
  - The split is also the harder test: 0.473 on the year windows against 0.315 on a random split.
- **Concessions:**
  - The written reason for having no gap is wrong. A window's length is not a gap.
  - "the 9 an IID split would get" should read 3.
- **Mildest remedy:** keep no gap. Rewrite the reason so it names the survey-internal user, the collaboration that plans the next plates from spectra reduced within days. State the cost a public user faces (+0.14 to +0.19 mean log loss) so the curator signs off knowing it.
- **Why no gap wins:** any gap of 6 months or more puts 2012 under the 50% floor, and 18 months puts 2013 under it too (split auditor). That is SPLIT-14, a Must, against SPLIT-10, a Should. Adding a gap would cost windows or need an exception; fixing the comment costs a few lines.

**4. It is worth benchmarking, and the metric fits the decision (P6; TP-2 Should, MET-1 Must)**
- **Evidence:**
  - LightGBM about 0.45 against logistic regression 0.70 and the class shares 1.19. The best model beats the dummy on 100% of splits.
  - Every test fold holds all three classes; the smallest class count is 9,651.
  - The domain practitioner endorses log loss: a catalogue publishes class probabilities, and no source fixes a fibre budget that a top-k metric would need (MET-7).
- **The task gamer's one exploit:** features built from the test window's own unlabelled rows, worth −0.047. It is transductive. A deployed model would not have it when it selects targets from photometry, which is our use case, and a per-row model never sees it.
  - The mildest remedy is a note, by analogy with the weak transductive leak tension (LEAK-30: keep with a note).
  - The gamer's own fix, shipping the targeting programme or plate as a feature, would undo the plate drop that LEAK-10 requires. It must be refused.
- **"Training on the last 3 years is better":** the default sampler already draws the newest year back to 1M rows, so the benchmark does this by construction.

**5. The missing PSF magnitudes are real, and the fix keeps the dataset (CLEAN-1 Should, P7; USE-6 Must allows the inputs)**
- **Concession:** this is the panel's strongest finding, and I do not dispute it.
  - The column auditor measured that adding `psfMag_u…z` lowers log loss from 0.467 to 0.353 (2019–2020) and from 0.433 to 0.344 (2018).
  - The domain practitioner measured 0.12–0.19 lower log loss in three year-to-year tests.
  - Both say every SDSS star/galaxy separation starts from the PSF-minus-model magnitude.
- **Why it does not block shipping:**
  - It is a quality gap at P7, not a validity failure. The task as shipped is valid, and TP-6 says a valid task stays.
  - The features were fixed for `sdss_17` only because the Kaggle file had nothing else. Our own query removes that limit, so this is a repair from the origin: the first step of the remedy ladder.
  - It is cheap and safe: add five columns to the 11 queries, refetch in about 5 minutes, and map −9999 to missing. The target, split and metric stay as they are, so it represents the real task better rather than changing it to make methods separate better.
- **What I would keep out of the default:** `type` and `extinction_*` should each be a separate curator call. `type` is the imaging pipeline's own rule-based class, and USE-6 allows it as an input, but it should not ride in silently.

**6. Label quality: drop the unplugged fibres; keep the pipeline class as the target (CLEAN-15 Must by analogy, PROV-13 Must; TP-6 against the DESI precedent)**
- **Concession:**
  - 18,513 rows (0.40%) have zWarning bit 7 (UNPLUGGED) set and a median S/N of 0.0. Their labels describe no object; 97% default to GALAXY.
  - They cost the newest windows about 0.01 log loss.
  - **Remedy:** add `s.zwarning` to the queries and drop rows with `zwarning & 128`. The flag is the source's own, so this is a repair from the origin (PROV-13), not a fix of our own invention (TP-6).
- **The wider question (8.0% of rows flagged):** this is a weighing call, not a block.
  - Option B, dropping every flagged row, passes TP-6 because SDSS defines the flag. The practitioner backs it, and the flags are not strongly tilted by class (19% of galaxies, 13% of quasars, 13% of stars in 2016).
  - Keeping the rows is also defensible. The target is defined as "the class the survey's spectroscopic pipeline assigned", and that is the label every photometric classifier trains on (USE-5).
  - Either way the dataset ships. "Task easier" must not be given as the reason for B; the reason is label reliability.
- **The DESI precedent** (`desi_dr1_star_galaxy_quasar` suspended on 2026-11-05, Myunghwan, because physical-class correctness was not established). The fact that sets this case apart, to be recorded:
  - This task's target is declared as the pipeline class, not the physical class.
  - The same target already ships in `sdss_17` (Andrej, 2026-11-12).
  - Dropping UNPLUGGED, and optionally all of zWarning ≠ 0, is exactly the "source-supported repair" the DESI hold names as its way out.
  - I agree with the precedent checker's recommendation: option (a), and put the same fact to Myunghwan's hold as a question.

**7. Keep the sky position; document what it does (USE-6 Must; the 2026-11-11 decision; task fidelity over separability)**
- **Evidence:**
  - Position is known before any spectrum, so USE-6 makes it a legitimate input.
  - It hurts rather than leaks. Position alone scores worse than the class shares, and adding it costs 0.013–0.066 log loss (claim auditor).
  - `sdss_17` measured the same effect and the curator kept the feature.
- **Why not drop it:**
  - Dropping a known input because it makes scores worse is changing the task to make methods separate better, which the curator has ruled out.
  - Whether a method learns to discount a programme's footprint under drift is part of what the benchmark should measure. The blind reviewer's drop has no rule behind it beyond the score.
- **Mildest remedy:** a `curation_comments` bullet with the per-window numbers, saying position mostly records which targeting programme was active.
  - `cam_col` changes scores by ±0.001; keep it, as in `sdss_17`.
  - The repeat-observation share (5.6–7.7% of spectra) and the ~494k primary spectra without a photometric match go into `fit_reason` and `curation_comments` as sentences.



**Judgment record (the advocate's reading):**
```text
Verdict: ship after small changes.
Validity: LEAK-10 holds (redshift, plate, fibre dropped; as-of check clean); SPLIT-14 holds, so no gap
(SPLIT-10 reason rewritten); PROV-6 / TP-6: replaces sdss_17; PROV-13: UNPLUGGED rows dropped from the source's own flag.
Value: TP-2 holds (gap over linear 0.25); MET-1 holds (fallback log_loss).
Quality: CLEAN-1, add psfMag_u..z (repair from origin, cheap).
Weighed: zWarning ≠ 0 (B or keep); position kept with a note; transductive co-window exploit noted.
For the curator: zWarning option; type/extinction; DESI consistency (a).
```

</details>

<details><summary>Critic</summary>

I argue that `sdss_dr17_star_galaxy_quasar_1m` should **ship only after changes**. Nothing found is a leak, and the task is real. But about 18.5k labels describe no object, the inputs leave out the measurement an astronomer always uses, and the split comment gives a wrong reason for its biggest choice.

**Critic's opening brief: `sdss_dr17_star_galaxy_quasar_1m`**

**1. 18,513 rows carry the class of an empty fibre (validity: P5, target)**
- **Problem:** these rows have zWarning bit 7 (UNPLUGGED) set, and their median S/N is 0.0. The fibre carried no light from the object, so the pipeline fitted noise. 97% of them come out as GALAXY, and 8,049 of those GALAXY labels sit on point sources.
- **Effect:** these labels describe no object, so in effect the object's class is missing. Their share rises over time, from 0.33% of the 2012 test window to 0.87% of 2019–20. On 2019–20 they raise LightGBM's log loss from 0.467 to 0.478, and their own log loss is 1.76. This is noise in the label, not a hard object.
- **Evidence:** claim-auditor, claim 14 and finding 1. The 18,513 come from a SkyServer query on the joined rows.
- **Rules:** CLEAN-15 (Must; the target is in effect missing) and PROV-13 (Must; the origin has the flag that allows the repair). TP-6 is not in the way, because the flag is the source's own definition, not a fix we invented.
- **Remedy (fix the definition):** add `s.zwarning` to the 11 queries and drop the rows where `(zwarning & 128) != 0`. Document it in one bullet. Nothing needs weighing here, so this should not wait for the wider zWarning call in point 2.

**2. The wider zWarning question is still open, and the record does not face the DESI hold (validity: P5 and USE-5; consistency)**
- **Problem:** DR17 flags 8.0% of the classes as unreliable: galaxies 6.2%, stars 8.4%, quasars 13.3%. The flagged share grows from 4.0% before 2012 to 15–22% from 2015, so the newer test windows carry 3 to 5 times the training sides' share.
- **Effect:** part of the windows' difficulty is label noise.
  - The domain practitioner's test (train 2014–15, test 2016): the model scores 0.436 on clean test rows and 0.853 on flagged ones.
  - 76% of the labels that changed between DR12 and DR17 carry the flag.
  - The practitioner would never train on or validate against flagged spectra.
- **Inconsistency:** Myunghwan suspended `desi_dr1_star_galaxy_quasar` on 2026-11-05 for exactly this concern, physical-class correctness. The record calls DESI "`TBD -> Yes`" and leaves out the suspension (precedent-checker, finding 1).
- **Rules:** USE-5 (Must; predict what the actor acts on), P5, and principles.md "Consistent judgement", case 2.
- **Remedy (curator call):**
  - Take the builder's option B: drop zWarning ≠ 0, with label reliability as the only reason. "Task easier" must come out of the builder's text, under the rule of task fidelity over separability.
  - Put the precedent-checker's consistency check about DESI into the `## Review` either way.

**3. The morphology an expert always uses is missing (P3: USE-6's "why"; P7: CLEAN-1, Should)**
- **Problem:** the task is "judging from its images alone", yet the inputs are only the Kaggle cut's 9 columns. `PhotoObj` holds the PSF magnitudes in the same row, and the photometric `type` is defined from PSF minus cModel magnitude. Both exist before any spectrum and carry the same DR13 calibration.
- **Effect:** the benchmark asks for a star/galaxy split by colour alone, which no practitioner does. The practitioner would not use the shipped model: 39% of stars are confused.
- **Evidence:** two agents measured this independently, on the definition's own join. Log loss, lower is better:

  | Test | Shipped features | + psfMag |
  |---|---|---|
  | 2019–20 window | 0.467 | 0.353 |
  | 2018 window | 0.433 | 0.344 |
  | 2014 → 2015 | 0.497 | 0.373 |
  | 2015 → 2016 | 0.517 | 0.367 |

  Sources: column-auditor problem 1; domain-practitioner, gap 1.
- **Why the earlier decision does not bind:** the features were fixed for sdss_17 on 2026-11-11 because the Kaggle file had no other columns. Our own query removes that limit. No record ever decided on PSF magnitudes; the domain-practitioner searched and found none.
- **Not separability:** USE-6's reason is that dropping an input known at the prediction point changes the task. Leaving these out does exactly that.
- **Remedy (fix the definition):** add `psfMag_u…z` to the 11 queries and map −9999 to missing. `type` (categorical) and `extinction_*` are optional and up to the curator.

**4. The "no gap" reason is wrong, and the gap is the largest unlabelled choice in the split (P4: SPLIT-10 and SPLIT-12, Should; the curator signs off on the horizon)**
- **Problem:** the splits comment says a public user "waits for the next release, which the one-year windows already stand in for". The window length is not a gap: every training side ends on the window's first day.
- **Effect:** a gap changes mean log loss a lot:

  | Gap | Mean log loss |
  |---|---|
  | none (shipped) | 0.450 |
  | 6 months | 0.495 |
  | 18 months | 0.590 |
  | public release available at each window's start | 0.635 |

  Evidence: split-auditor, problem 1.
- **Remedy (a note, not a re-split):** keep no gap. Give the real reason: the survey-internal user gets reduced spectra within days. Quote the cost of the public-release lag so the curator signs off knowing it. A gap of 6 months or more would push 2012 below the training floor.

**5. Sky position works as a proxy for the targeting programme and hurts every window, and the README never says so (P3/P4 notes; Weigh)**
- **Evidence:**
  - Adding `alpha` and `delta` worsens log loss by 0.013 to 0.066 in every window, a mean of 0.033 (claim auditor). The column-auditor and the blind reviewer measured the same direction.
  - Position alone scores worse than predicting the class shares.
  - At 1M training rows the effect is up to four times sdss_17's 0.015.
- **This is the reason plate was dropped, returning through the coordinates (LEAK-10 by analogy).** Even so, I do not ask to drop the columns: they are known at prediction, and task fidelity comes before separability.
- **Remedy (a note):** add a curation_comments bullet with the numbers, as sdss_17's record has, and name galactic latitude as the curator's alternative. Dropping `cam_col` is optional: it changes log loss by at most ±0.001 (column-auditor) and has no physical meaning.

**6. The fit_reason leaves out two selection facts (P3: USE-8, note)**
- **Re-observed objects:** 5.6–7.7% of the primary spectra from 2010 to 2020 belong to objects with an earlier spectrum, and 8–14% of quasars. These objects were targeted because the survey already knew their class, which is the opposite of the use case, "objects with images but no spectrum" (column-auditor, problem 3).
- **Same-window exploit:** features built from the test window's own unlabelled rows lower mean log loss by 0.047 (task-gamer). It works because a calendar year of spectra marks the active programme.
- **Remedy (a note):** one sentence for each in `fit_reason` / `curation_comments`, with the numbers. Dropping the re-observed objects is not needed.

**7. Wrong or weak text in the definition (writing)**
- The splits comment says "the 9 an IID split would get". The IID target here is 3 (SPLIT-15 with SPLIT-33). Change "9" to "3" and say the window count is limited by the training floor.
- The 2019–2020 merge is justified by "every spectrum stays tested", which nine windows would do too. Name the real reason instead: 2020 is 8 plates of one programme before the COVID closure, an atypical newest window (SPLIT-20).
- The 494k primary spectra with no photometric match are implied but never counted in `curation_comments` (column-auditor).
- The builder report says all 155 sentinel objects are missing all five bands; only 103 are. The README is correct.

**Judgment record**
- **Verdict:** ship after changes. Point 1 is required. Points 2 and 3 are curator calls I argue for. Points 4–7 are notes.
- **Validity:**
  - CLEAN-15 / PROV-13 triggered: fixed by dropping the UNPLUGGED rows.
  - USE-5 open: the zWarning ≠ 0 rows, and the DESI consistency check.
  - LEAK-10 holds.
  - SPLIT-10's reason is wrong; the choice of no gap stands.
- **Value:** TP holds, with a gap of 0.16 over the linear model.
- **Quality:** CLEAN-1 departure (no PSF magnitudes) to be fixed; under USE-6's reason it reaches the task itself.
- **Weighed:** position − (note); `cam_col` neutral.

No file was edited.

</details>

<details><summary>Advocate's rebuttal</summary>

**Advocate's rebuttal: `sdss_dr17_star_galaxy_quasar_1m`**

**Where we stand:** the critic and I reach the same verdict, "ship after changes", and we ask for the same changes in the definition. We disagree on two things only:
- the rule behind point 5;
- how firmly point 2 should push option B.

I concede everything else.

**Critic 1: the 18,513 UNPLUGGED rows. Conceded in full.**
- This was my point 6 too. The facts:
  - median S/N is 0.0;
  - 97% of these rows are labelled GALAXY, and 8,049 of those sit on point sources;
  - their share of the test windows rises from 0.33% to 0.87%.
- The rules are CLEAN-15 (Must) and PROV-13 (Must). The flag is the source's own, so TP-6 does not stand in the way.
- **What follows:** this is required before shipping and does not wait for the wider zWarning call. Add `s.zwarning` to the 11 queries and drop the rows where `(zwarning & 128) != 0`.
- The claim auditor's side note goes into the `## Review` as a question, not as a drop: NEGATIVE_MODEL, bit 6, is set on 5,916 STAR rows.

**Critic 2: the wider zWarning question and DESI. Partly conceded.**
- **Conceded: the record leaves out the DESI suspension.** It calls DESI "`TBD -> Yes`". That is wrong and must be corrected. The consistency check goes into the `## Review` whichever way the curator decides (principles.md, "Consistent judgement", case 2).
- **Conceded: "task easier" must come out of the builder's text** as a reason for option B, under the rule of task fidelity over separability.
- **Disputed: that USE-5 makes B a Must.** It is still a weighing call. Two facts:
  - The target is declared as the pipeline class, which is what photometric classifiers train on. The same target ships today in `sdss_17` (Andrej, 2026-11-12).
  - A deployed model never sees zWarning. The flagged objects are ones it would be asked about. B removes 15–22% of the newest windows, against 4% of the early training years. That changes which objects get scored, not only how much noise their labels carry.
- **What I accept:** B is defensible on label reliability. The practitioner shows it is not strongly tilted by class: 19% of galaxies, 13% of quasars, 13% of stars. The 76% flag rate among the DR12→DR17 relabels shows those labels really are noisy.
- I don't oppose B. I oppose calling it required. The curator should choose with both numbers in front of them:
  - log loss 0.436 on clean rows against 0.853 on flagged rows;
  - the share of each window that B removes.
- The dataset ships either way.

**Critic 3: the PSF magnitudes. Conceded, and I join the call to fix it before shipping.**
- Four independent measurements show 0.09–0.15 lower log loss, and the Kaggle-file reason for the old feature set no longer holds.
- The critic reads the gap as reaching USE-6, not only CLEAN-1. Whichever rule we cite, the remedy is the same: add `psfMag_u…z` and map −9999 to missing. So I don't argue the label.
- We agree that `type` and `extinction_*` are separate calls for the curator.

**Critic 4: the reason for no gap. Conceded.**
- This was my point 3. Keep no gap: SPLIT-14 (Must) wins over SPLIT-10 (Should), because any gap of 6 months or more pushes 2012 below the training floor.
- Rewrite the reason around the survey-internal user, who gets reduced spectra within days.
- Quote the cost a public user faces, so the curator signs off knowing it: mean log loss 0.450 → 0.495 → 0.590 → 0.635 (no gap, 6 months, 18 months, public-release lag).

**Critic 5: sky position. I agree with the remedy but dispute the rule.**
- The critic calls position "the reason plate was dropped, returning through the coordinates (LEAK-10 by analogy)". That analogy does not hold:
  - Plate and fibre were dropped because they are **not known** for an object without a spectrum. The column auditor's entry for them reads "no (they encode the targeting)".
  - Position **is** known from the imaging, before any spectrum.
  - A leak helps scores. Position hurts them in every window, by 0.013–0.066.
- That makes it distribution shift under USE-6, not a LEAK-10 matter. This matters for the record: tagging it as a leak would invite someone later to drop it on a Must.
- **What follows is unchanged:** keep `alpha` and `delta`, and add a `curation_comments` bullet with the per-window numbers. Galactic latitude can be named as an option for the curator.
- `cam_col`: keep it, as in `sdss_17`. It moves log loss by ±0.001.

**Critic 6: re-observed objects and the same-window exploit. Conceded as notes.**
- One sentence each in `fit_reason` / `curation_comments`, with the numbers:
  - 5.6–7.7% of primary spectra belong to objects with an earlier spectrum (8–14% of quasars);
  - the same-window exploit is worth −0.047, and it is transductive (LEAK-30 tension: keep with a note).
- Both sides agree the re-observed objects should not be dropped.
- I keep my refusal of the gamer's fix: shipping plate or programme as a feature would undo the LEAK-10 drop.

**Critic 7: the text fixes. All conceded.**
- Change "9" to "3" for the IID window count, and say the training floor limits the number of windows.
- Give the real reason for merging 2019 and 2020 (SPLIT-20): 2020 is 8 plates of one programme before the COVID closure, an atypical newest window.
- Count the ~494k primary spectra without a photometric match in `curation_comments`. That is 492,959 with `bestobjid = 0`, almost all unplugged-fibre and sky spectra (claim auditor, claim 2).
- Correct the builder report: 103 sentinel objects, not 155, are missing all five bands. The README is already right.

**Joint position for the mediator**
- **Required:**
  - drop the UNPLUGGED rows;
  - add `psfMag_u…z`;
  - make the text fixes in points 4, 6 and 7;
  - add the position note;
  - correct the record's description of DESI.
- **Curator calls:** zWarning ≠ 0 (option B or keep); `type` and `extinction_*`; consistency with DESI.
- **Disputed:** only whether position is labelled LEAK-10 (critic) or USE-6 shift (me), and whether B is weighed (me) or argued for as near-required (critic).

No file was edited.

</details>

<details><summary>Critic's rebuttal</summary>

I accept the advocate's points 1, 2, 3, 5 and 7. I dispute part of point 6, and one figure and one remedy in point 4.

**Critic's rebuttal: `sdss_dr17_star_galaxy_quasar_1m`**

The two briefs agree on the two fixes: add `psfMag_u…z` and drop the UNPLUGGED rows. They also agree that every remaining point needs only a note. The real dispute is whether all zWarning ≠ 0 rows can be kept. My answer is no, because of the DESI precedent.

**Advocate 1: validity holds. **Conceded, with one correction.****
- I found no leak, and nothing on the panel contradicts the as-of check or the dedup.
- "None of the written claims is wrong" overstates it, by the advocate's own point 3:
  - The no-gap reason in the splits comment is wrong.
  - "9" should read "3".
  - The builder report says 155 objects are missing all five bands. The real count is 103 (column-auditor).
- These are text errors, not validity failures.

**Advocate 2: this replaces `sdss_17` (TP-6, PROV-6). **Conceded.****
I never argued for keeping `sdss_17` or shipping both.

**Advocate 3: no gap; SPLIT-14 outweighs SPLIT-10. **Conceded.****
This is my point 4 with the same remedy: keep no gap, rewrite the reason, and quote the +0.14–0.19 cost of the public release lag. We also agree on "9" → "3".

**Advocate 4: worth benchmarking, log loss is the right metric. **Conceded on the verdict, disputed on two details.****
- **The gap over the linear model:**
  - The builder's checklist says 0.16 (its checklist).
  - Line 25 of the same report gives LightGBM 0.489 against linear 0.674 on 5 of 8 splits.
  - The advocate's 0.25 compares an all-window LightGBM mean with a linear number from another run.
  - TP-2 passes either way. The README and the judgment record should quote one measured figure from one run.
- **LEAK-30, the note on the same-window exploit:** agreed, it stays a note. That is my point 6. I also agree that shipping plate or the targeting programme as a feature must be refused.
- **The sampler covers "train on the last 3 years":** conceded.

**Advocate 5: add the PSF magnitudes. **Conceded.****
- I never called this a block. My remedy was "fix the definition", which is the advocate's remedy too.
- I agree that `type` and `extinction_*` each need their own curator call.
- One small point: the advocate files this under P7 quality, but the reason it matters is USE-6. Without PSF magnitudes the model must separate stars from galaxies by colour alone, and no practitioner does that, so the gap reaches the task itself. That is why I ask for it as a definition fix, not an optional cleanup.

**Advocate 6: drop UNPLUGGED; for the rest, keeping the rows "is also defensible". **First part conceded, second part disputed.****
- **UNPLUGGED (bit 7):** we agree.
- **Keeping the other flagged rows (7.6%):** I dispute that this is defensible.
  - **USE-5 (Must):** the actor is an astronomer who picks targets by their true class.
    - The task question (`task_summary.question`) asks about the object: "Is a sky object a galaxy, a star or a quasar". It does not ask what the pipeline said.
    - The pipeline itself marks these 7.6% as unreliable.
    - A model scored against labels the source disowns is not scored on what the actor acts on.
    - The domain practitioner would not train on flagged spectra or validate against them.
  - **The fact the advocate offers to set this apart from DESI does not do so:**
    - The advocate says the target here is the pipeline class. DESI's target is also a pipeline class, `SPECTYPE` (DESI record).
    - The advocate says the same target ships in `sdss_17`. DESI was screened as "the same target and the same photometric classification task as sdss_17", and it was suspended anyway.
    - So neither fact separates the two cases. The hold's concern is that a pipeline class may differ from the physical class. That concern applies to SDSS as much as to DESI.
  - **What does set this case apart:** the hold names its own way out, "source-supported repair ... for a specified cohort" (DESI record). Dropping every zWarning ≠ 0 row, using SDSS's own flag, is that repair. Dropping only UNPLUGGED leaves 7.6% of rows that the source calls unreliable, and the precedent-checker's option (a) is then hard to defend.
  - **Under "Consistent judgement", case 2:**
    - Option B is consistent with Myunghwan's hold.
    - Option "keep" would need a fact that sets this case apart. None has been shown.
  - The class balance the advocate cites (19% / 13% / 13% in 2016) argues for B: dropping the flagged rows removes noise without reshaping the classes.
- **What I ask for:**
  - Option B as the recommended default, given for label reliability only. "Task easier" must come out of the text.
  - Either way, the DESI consistency question goes into `## Review` with the reasoning above, not with the pipeline-class argument.
  - I agree that the same question goes to Myunghwan's hold.

**Advocate 7: keep sky position with a note. **Conceded.****
This matches my point 5. Keeping `cam_col` is fine. The repeat-observation share and the ~494k primary spectra without a photometric match go in as sentences, as both briefs say.

**Where things stand**
- **Required:** drop the UNPLUGGED rows and add `psfMag_u…z`.
- **Curator calls:**
  - zWarning ≠ 0: I argue for B and the advocate leaves it open. The DESI consistency check tips it to B unless the curator names a fact that sets this case apart.
  - Whether to add `type` and `extinction_*`.
- **Notes, agreed by both sides:** the gap reason, 9 → 3, the reason for merging 2019–20, the position numbers, the transductive exploit, the re-observed objects, the 494k spectra without a photometric match, the 103 vs 155 count, and one linear-baseline figure.

I edited no files.

</details>

## Reference

Abdurro'uf, Accetta K., Aerts C., et al. (2022). The Seventeenth Data Release of the Sloan Digital Sky Surveys: Complete Release of MaNGA, MaStar, and APOGEE-2 Data. The Astrophysical Journal Supplement Series 259(2):35. https://doi.org/10.3847/1538-4365/ac4414

Blanton M. R., Bershady M. A., Abolfathi B., et al. (2017). Sloan Digital Sky Survey IV: Mapping the Milky Way, Nearby Galaxies, and the Distant Universe. The Astronomical Journal 154(1):28. https://doi.org/10.3847/1538-3881/aa7567

Bolton A. S., Schlegel D. J., Aubourg É., et al. (2012). Spectral Classification and Redshift Measurement for the SDSS-III Baryon Oscillation Spectroscopic Survey. The Astronomical Journal 144(5):144. https://doi.org/10.1088/0004-6256/144/5/144
