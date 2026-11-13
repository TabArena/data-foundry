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
priority: 3
decision_markers:
- Selection Bias
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: Other
year: '2021'
domain: physics & astronomy
required_split:
- Temporal (NON-IID)
problem_type: Multiclass Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://skyserver.sdss.org/dr17/SearchTools/sql
- https://www.sdss4.org/dr17/
- https://doi.org/10.3847/1538-4365/ac4414
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

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
