---
unique_name: desi_dr1_star_galaxy_quasar
name: DESI Data Release 1 (spectroscopic classes with Legacy Surveys DR9 photometry)
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 3
decision_markers:
- Selection Bias
tags:
- AI-Filled (Verify)
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
v2_path: datasets/_dev/tabarena-v0pt2/desi_dr1_star_galaxy_quasar_1m/dataset.py
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

CC (2026-11-08, Lennart): accepted for adding (`Yes`) in the screening review of the large candidates (most rows, most features).

**Assessment (AI, 2026-11-09):** the same task from another survey as `sdss_17`, not better data for it (principles.md, Tensions, "Same task, another source"): SDSS has the u and i bands, DESI adds two infrared bands, Gaia astrometry and image morphology, and the targeting rules differ, so both enter. This corrects the "better data" reading of 2026-10-31; the reason is also in the definition's notes and in `sdss_17`'s record.

**Assessment (AI, 2026-11-09):** review panel (full): ship after changes (made: fit_reason names the ZWARN cohort and the label's disagreement with DESI's DR1 quasar catalogue in both directions, USE-8; fibre fluxes of unmeasured bands and SERSIC of point sources set missing, CLEAN-10; parallax and proper motions without a Gaia DR2 match blanked, LEAK-10 weak, CLEAN-21; the notes' LightGBM numbers re-run with early stopping, EV-1; the SEL-13/SEL-15 fact against magic_gamma_telescope; sdss_17 the same task from another survey); disputed: USE-5 and TP-6, the label (keep Redrock's class with the note, or relabel from DESI's quasar catalogue: the critic, and the advocate after the rebuttal, for its additions only; the mediator for the note, since DESI's quasar class follows the targeting class); for the curator: issue 1. Priority 3: gap +, use case 0, source +, shape +, risk - (gap: physics & astronomy and multiclass are thin among the accepted definitions; use case: ours, the fit approximate; risk: the label at the galaxy/quasar boundary is open, issue 1).
