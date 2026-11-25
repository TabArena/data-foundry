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
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

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

## Reference

Abdurro'uf, Accetta K., Aerts C., et al. (2022). The Seventeenth Data Release of the Sloan Digital Sky Surveys: Complete Release of MaNGA, MaStar, and APOGEE-2 Data. The Astrophysical Journal Supplement Series 259(2):35. https://doi.org/10.3847/1538-4365/ac4414

Blanton M. R., Bershady M. A., Abolfathi B., et al. (2017). Sloan Digital Sky Survey IV: Mapping the Milky Way, Nearby Galaxies, and the Distant Universe. The Astronomical Journal 154(1):28. https://doi.org/10.3847/1538-3881/aa7567

Bolton A. S., Schlegel D. J., Aubourg É., et al. (2012). Spectral Classification and Redshift Measurement for the SDSS-III Baryon Oscillation Spectroscopic Survey. The Astronomical Journal 144(5):144. https://doi.org/10.1088/0004-6256/144/5/144
