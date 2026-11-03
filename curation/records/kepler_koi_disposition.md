---
unique_name: kepler_koi_disposition
name: 'Kepler Objects of Interest (cumulative KOI table): planet candidate vetting'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: GOV Website
domain: physics & astronomy
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://exoplanetarchive.ipac.caltech.edu/
- https://exoplanetarchive.ipac.caltech.edu/docs/API_kepcandidate_columns.html
- https://doi.org/10.3847/1538-4365/aab4f9
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: NASA's cumulative Kepler Objects of Interest table (9,564 KOIs, about 150 columns of transit fits, stellar parameters and centroid diagnostics) with the archive's disposition, a planet-vetting task in the empty physics and astronomy domain; the vetting outputs and `kepler_name` give the label away and must go, and it overlaps the Kepler TCE record of this run.
- Source: NASA Exoplanet Archive (IPAC/Caltech), the `cumulative` KOI table, columns documented at https://exoplanetarchive.ipac.caltech.edu/docs/API_kepcandidate_columns.html; catalog paper Thompson et al., "Planetary Candidates Observed by Kepler. VIII. A Fully Automated Catalog with Measured Completeness and Reliability Based on Data Release 25", ApJS 235, 38 (2018, https://doi.org/10.3847/1538-4365/aab4f9), abstract: "This catalog was created using a tool called the Robovetter which automatically vets the DR25 Threshold Crossing Events". As published (TAP query, 2026-10-31): 9,564 KOIs, 153 default columns; `koi_disposition` ("Exoplanet Archive Disposition") against `koi_pdisposition` ("Disposition Using Kepler Data"): CONFIRMED 2,748 (2,739 of them CANDIDATE by Kepler data), FALSE POSITIVE 4,839 (4,838 FALSE POSITIVE by Kepler data), CANDIDATE 1,977 (unresolved).
- Use case: a vetting team decides which transit signals are planet candidates worth scarce follow-up time; on this table the Robovetter and TCERT made that call, and confirmation came from follow-up. Fit approximate: Kepler's vetting is finished, so the table stands in for vetting a new mission's signals, and CONFIRMED depends on which candidates got follow-up. Target to choose: `koi_pdisposition` (candidate against false positive, all 9,564 labelled, the vetting decision itself) or `koi_disposition` confirmed against false positive (7,587 labelled). Regime grouped by star (`kepid`; multi-planet systems), or temporal by delivery (`koi_delivname`, `koi_vet_date`); to settle.
- Siblings and duplicates: `kepler_dr24_tce_vetting` (`TBD -> Yes`, priority 4; Kepler Q1-Q17 DR24 TCEs with Autovetter labels): a KOI is a TCE that passed vetting, so the units overlap; same mission and vetting task family with other units, another data release and other labels (PROV-7, not a duplicate), and the curator may keep one Kepler task; `tess_toi_disposition` (`TBD -> Yes`, priority 3; TESS, another mission); `first_principles_kepler` (`No`, AHDS; unrelated). External collections: a Kaggle re-upload of this table (nasa/kepler-exoplanet-search-results, 9,564 rows; from memory, not checked in this pass); the awesomedata/apd-core list entry (https://github.com/awesomedata/apd-core/tree/master/core//Physics/NASA-Exoplanet-Archive.yml) moved here from the source links (PROV-12).
- Better data: from the curator's Zotero collection (item 148, awesome-public-datasets); no further search this round.
- Papers and pages: Thompson et al. 2018 (Robovetter completeness and reliability on simulated data); the archive's column documentation and https://exoplanetarchive.ipac.caltech.edu/docs/PurposeOfKOITable.html.
- Metric: none found for a model on this table (Thompson et al. report the Robovetter's completeness and reliability, threshold rates of their own pipeline, not a criterion for this task; the archive pages state none), so the fallback `roc_auc` (MET-1, MET-6, MET-8). Inputs: none.
- Risks for /add-dataset: drop the vetting outputs `koi_score`, `koi_fpflag_nt`, `koi_fpflag_ss`, `koi_fpflag_co`, `koi_fpflag_ec`, `koi_comment` (Robovetter flags as text), `koi_disp_prov`, `koi_vet_stat`, `koi_pdisposition` when the archive disposition is the target, and `kepler_name`, which only confirmed planets carry (LEAK-10); the Robovetter is a published decision tree on metrics, few of them in this table, but the centroid offsets (`koi_dicco_*`, `koi_dikco_*`, `koi_fwm_*`) and SNR feed it, so check that the label is no rule of the shipped columns (SEL-5, TP-4); the transit fit values are measurements of a light curve (SEL-15), while a CNN on the light curves is the later tool (SEL-12, as for the sibling); confirmation favours bright stars that got follow-up (`Selection Bias` to weigh).
- Priority: gap + (physics and astronomy has 0 accepted), use case 0 (no source defines the task on this table; fit approximate), source + (archive column documentation and the DR25 catalog paper), shape + (9,564 KOIs, about 150 columns, star groups), risk - (label-giving columns to drop; overlap with `kepler_dr24_tce_vetting`).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 148: "awesomedata/awesome-public-datasets".
- as published: 9,564 KOIs x 153 columns (TAP query today): 2,748 CONFIRMED, 4,839 FALSE POSITIVE, 1,977 CANDIDATE; transit fit parameters (period, depth, duration, impact, SNR) and stellar parameters; target: koi_disposition (confirmed planet vs false positive; candidates unlabelled); access: open.
- Why: A real, documented astronomy classification with a public table and a published catalog paper; a domain the benchmark lacks.
- Adds: Astronomy. Caveats: drop the vetting outputs koi_score, koi_fpflag_* and koi_pdisposition (leaks); the features are pipeline fits to light curves (SEL-13/14 question); the TESS TOI table (7,651 TOIs, about 2,800 with a final disposition) is a newer, smaller-labelled sibling.
