---
unique_name: fermi_4fgl_dr4_source_classes
name: 'Fermi-LAT 14-year Source Catalog (4FGL-DR4): classes of associated gamma-ray sources'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Selection Bias
tags:
- AI-Filled (Verify)
original_source: GOV Website
year: '2023'
domain: physics & astronomy
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://doi.org/10.3847/1538-4365/ab6bcb
- https://fermi.gsfc.nasa.gov/ssc/data/access/lat/14yr_catalog/
- https://arxiv.org/abs/2307.12546
- https://arxiv.org/abs/2201.11184
- https://heasarc.gsfc.nasa.gov/W3Browse/fermi/fermilpsc.html
- https://arxiv.org/abs/2510.08654
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: NASA's Fermi-LAT 14-year catalog (4FGL-DR4) with measured spectral and variability fits and a class for about two thirds of its 7,194 sources, a real astronomy multiclass task in a domain with no accepted dataset; the labelled sources are brighter than the unassociated ones the task is for, the class set is still to choose, and `fermi_lat_4fgl_source_class` (screen_63) records the same catalog and target.
- Source: the Fermi-LAT collaboration; 4FGL by Abdollahi et al., ApJS 247:33 (2020, https://doi.org/10.3847/1538-4365/ab6bcb), with the incremental releases DR3 (arXiv 2201.11184, still the method reference) and DR4 (arXiv 2307.12546, "Please cite both documents"). FSSC page (https://fermi.gsfc.nasa.gov/ssc/data/access/lat/14yr_catalog/): gll_psc_v35.fit (revision 4 of 2024-07-24; first DR4 release 2023-07-24), "7194" sources, data of 2008-08-04 to 2022-08-02; the HEASARC table fermilpsc mirrors it (7,195 there and in arXiv 2510.08654). As published: one row per source with position and error ellipses, detection significance, fluxes and energy flux, Spectrum_Type (PowerLaw, LogParabola, PLSuperExpCutoff) and the fit parameters, band fluxes, variability, Data_Release (the release that added the source) and the association columns; target CLASS1 (upper case identified, lower case associated). Class counts from the run's Assessment (HEASARC, 2026-10-30, not recounted): 4,772 associated or identified (bcu 1,623, bll 1,490, fsrq 820, psr 320, others), 2,423 unassociated.
- Use case: an astronomer picks unassociated gamma-ray sources for follow-up (radio pulsar searches, optical spectroscopy of blazar candidates) by their predicted class, as the ML papers on the catalog do (arXiv 2510.08654: "Identification of Gamma Ray Pulsar Candidates in the Fermi-LAT 4FGL-DR4 Unassociated Sources"); the catalog names no decision, and FSSC warns that associations "are not in general to be taken as firm identifications"; fit approximate: the labelled sources are brighter and better localised than the unassociated targets (`Selection Bias`, as on `sdss_17`); regime IID over sources, or temporal by Data_Release (train on DR1-DR3 sources, test on those added in DR4), to decide (SPLIT-3).
- Siblings and duplicates: `fermi_lat_4fgl_source_class` (unscreened, screen_63, from the curator's Zotero collection): the same catalog file and the same CLASS1 target, a duplicate record (PROV-4), so one of the two stays; `sdss_17` (`Yes`) and `happy_teddy_sdss_photo_z` (`TBD -> Yes`, screening): other astronomy tasks, no overlap; `alerce_ztf_light_curve_classes`: light curves of another survey. External collections: none in our vocabulary.
- Better data: no new search; found through the gap scout for physics and astronomy.
- Papers and pages: Abdollahi et al. 2020 (4FGL); the DR3 and DR4 documents (not read beyond the FSSC and HEASARC pages); Pathania et al. 2025 (arXiv 2510.08654, abstract read: random forest and XGBoost on DR4, no metric in the abstract); the earlier ML literature on 3FGL and 4FGL unassociated sources (not read).
- Metric: none found (the FSSC page, the HEASARC description and the abstract of arXiv 2510.08654 name none; full texts not read), so the fallback `log_loss` for the multiclass task, `roc_auc` for a binary framing such as pulsar against AGN (MET-1, MET-8). Inputs: none.
- Risks for /add-dataset: the class set (bcu is a blazar of unknown subtype; many tiny classes such as nov, glc, sfr to merge or drop, TP-5); the association columns (ASSOC1/2, the association probabilities, CLASS2, the counterpart names) are label-side and go (LEAK); the spectral model may be chosen by the known class (pulsars fitted with a super-exponential cutoff), so Spectrum_Type and which fit columns are filled may give the label away (`Class-dependent Recording`, LEAK-13 to LEAK-15, to check against the DR3 document); label noise in the lower-case associations; mostly numeric columns; about 4,800 labelled rows.
- Priority: gap + (physics & astronomy has no accepted dataset; multiclass is thin), use case 0 (named by papers on the catalog, but the fit is approximate), source + (NASA mission catalog with ApJS papers), shape + (about 4,800 labelled sources, dozens of measured columns, a release order), risk - (the class set and class-dependent spectral models to settle; a duplicate record of this run).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the gap scout for physics and astronomy.
- as published: Gamma-ray point sources: 7,195 sources (HEASARC fermilpsc, 2026-10-30), of which 4,772 associated or identified (bcu 1,623, bll 1,490, fsrq 820, pulsars 320, others) and 2,423 unassociated; spectral ...; target: Source class CLASS1, for example pulsar vs AGN, or BL Lac vs FSRQ among blazars; access: open.
- Why: NASA mission catalog with measured spectral fits (SEL-15) and an established ML task (RF and XGBoost on DR4, arXiv 2510.08654; earlier on 3FGL); open
- Adds: Multiclass astronomy; a temporal angle across releases (3FGL, DR1 to DR4: sources associated later). Risks: lowercase associations are positional and 'not in general to be taken as firm identifications' (FSSC), so label noise; bcu is a blazar of unknown subtype; numeric features only; about 4,800 labelled rows

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: the same 4FGL catalog and target (`fermi_lat_4fgl_source_class`; PROV-4). The curator keeps one, or both as distinct tasks.
