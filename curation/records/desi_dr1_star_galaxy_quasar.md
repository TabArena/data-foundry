---
unique_name: desi_dr1_star_galaxy_quasar
name: DESI Data Release 1 (spectroscopic classes with Legacy Surveys DR9 photometry)
checked_by:
- Myunghwan
data_foundry_status:
- 'DF: Suspended'
suggestion: TBD -> Yes
priority: 1
decision_markers:
- Selection Bias
original_source: Website
year: '2025'
domain: physics & astronomy
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://data.desi.lbl.gov/doc/releases/dr1/
- https://data.desi.lbl.gov/public/dr1
- https://ui.adsabs.harvard.edu/abs/2026AJ....171..285D
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 18.7M spectroscopically classified stars, galaxies and quasars with Legacy Surveys photometry, a newer and far larger source for the photometric task of `sdss_17`; the targets were picked per class by colour cuts.
- Source: DESI Collaboration (Abdul Karim et al.), "Data Release 1 of the Dark Energy Spectroscopic Instrument", arXiv:2503.14745 (2025-03-18), AJ 171, 285 (2026); data at data.desi.lbl.gov/public/dr1 under CC BY 4.0 ("Use of DESI data requires including the citation and acknowledgment text", DR1 page). As published: Main Survey useful spectra of 18,659,804 unique targets, 13,049,402 galaxies, 1,553,713 quasars, 4,056,689 stars, observed May 2021 to June 2022 (DR1 page); the redshift catalogue (`zpix-SURVEY-PROGRAM.fits`, `zall-pix`) holds `SPECTYPE`, `Z`, `ZWARN`, `TARGET_RA/DEC`, `FLUX_G/R/Z/W1/W2` with inverse variances, `FIBERFLUX_*`, `EBV`, `MORPHTYPE`, `SHAPE_R`, `SERSIC`, Gaia magnitudes, `PARALLAX`, `PMRA/PMDEC`, the target bits and spectroscopic quality columns (desidatamodel).
- Use case: an imaging survey classifies objects that have photometry but no spectrum as star, galaxy or quasar for a catalogue or for follow-up (ours; the release names no prediction task); fit approximate, as for `sdss_17`. Regime IID following `sdss_17` (kept IID after a plate-grouping test, CC 2026-10-01); sky regions (HEALPix) are a candidate group.
- Siblings and duplicates: `sdss_17` (`Yes`, `Selection Bias`, SDSS DR17 photometry) and its Kaggle copy `stellar_classification_dataset_sdss17`: another survey, so no duplicate (PROV-4); `desi_bgs_photometric_redshift` is a photo-z regression on DESI's bright galaxies, another task from the same survey (PROV-7); `happy_teddy_sdss_photo_z`, `sdss_mpajhu_bpt_class` are other SDSS tasks. External collections: none found.
- Better data: found as better data for `sdss_17`; no further search this round.
- Papers and pages: the DESI DR1 paper and documentation; desidatamodel for the catalogue columns.
- Metric: none found (DR1 page, data model; a data release, not a task); fallback `log_loss` (MET-1, MET-8); inputs none.
- Risks for /add-dataset: targets were chosen per class by colour cuts (the BGS, LRG, ELG, QSO and MWS programmes), so the target bits (`DESI_TARGET`, `BGS_TARGET`, `MWS_TARGET`, `SCND_TARGET`, `SV*_TARGET`), `PRIORITY_INIT`, `NUMOBS_INIT`, `FA_TARGET` and `OBJTYPE` encode the class and go, with `Z`, `ZERR`, `ZWARN`, `DELTACHI2`, `TSNR2_*`, `COADD_*` and the fibre columns, which exist only after the spectrum (LEAK, USE-3); `Selection Bias` as for `sdss_17`: the class sits close to the targeting programme, so check the task is not trivial within it (TP-4); Tractor shape columns (`MORPHTYPE`, `SHAPE_R`, `SERSIC`) are fits to the image, a SEL-13 call for the curator (the `sdss_17` definition kept position and magnitudes only); 18.7M rows need a subsample.
- Priority: gap + (physics & astronomy has no accepted dataset; multiclass is thin), use case 0 (ours), source + (collaboration paper and data model), shape + (millions of objects, fluxes, Gaia astrometry), risk - (colour-cut selection, many target and post-spectrum columns to drop): 3.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `sdss_17`.
- as published: 18,659,804 unique main-survey objects with useful spectra: 13,049,402 galaxies, 1,553,713 quasars, 4,056,689 stars; photometry from the Legacy Surveys DR9 Tractor catalogue (g, r, z, WISE W1/W2 ...; target: Spectroscopic class SPECTYPE (STAR, GALAXY, QSO), the same three classes as sdss_17; access: open.
- Why: Same target and the same photometric classification task as sdss_17's v2 definition (position and broadband magnitudes, redshift and plate dropped), from a newer spectroscopic survey
- Adds: Two orders of magnitude more labelled objects (subsample for the benchmark), newer data, infrared WISE bands that help separate quasars from stars. Same risk as sdss_17: targets were picked by colour cuts (Selection Bias); the DESI target bits and tile/fibre columns encode the class and must be dropped. A newer ...

CC (2026-11-05, Myunghwan): Carry forward the explicit defer decision for the proposed physical STAR/GALAXY/QSO task. Credible physical-class correctness above 90% has not been established for the intended population; preserve the investigation and do not continue qualification or build under the current decision.

**Assessment (AI, 2026-11-05):** The prior disposition saved TBD -> Yes at priority 1; carry those values forward with DF: Suspended. Source studies show class-dependent failures in selected pipeline populations. The 20 selected visual-model cases are diagnostic evidence, not a representative global error-rate estimate or independently validated replacement labels. Do not describe a reported failure rate within a source-selected subset as a global label-accuracy result, or equate a reliable spectral fit with a verified physical class. Reopen with applicable independent label validation or source-supported repair meeting the stated requirement for a specified cohort and an explicit galaxy/AGN/QSO mapping. A materially changed target or population remains a curator choice. The hold is not a permanent scientific rejection or a new metric/split decision.
