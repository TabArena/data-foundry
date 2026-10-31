---
unique_name: tess_toi_disposition
name: TESS Objects of Interest (TOI) catalog with TFOPWG dispositions
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
- https://doi.org/10.3847/1538-4365/abefe1
- https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=TOI
- https://exoplanetarchive.ipac.caltech.edu/docs/API_TOI_columns.html
- https://exofop.ipac.caltech.edu/tess/view_toi.php
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: NASA's live TESS Objects of Interest table with the follow-up working group's disposition (confirmed or known planet against false positive or false alarm), a vetting task done today in the empty physics and astronomy domain; labels arrive years after the alert and only for part of each year's TOIs, so the label timing and the refit parameters decide whether a fair split exists.
- Source: the TESS mission's TOI list, served by the NASA Exoplanet Archive (IPAC/Caltech) from the ExoFOP-TESS list ("updated about weekly"); first alerts 2018-09 (`toi_created`); catalog paper Guerrero et al. 2021, ApJS 254, 39 (arXiv 2103.12538), abstract: "We present 2,241 exoplanet candidates identified with data from the Transiting Exoplanet Survey Satellite (TESS) during its two-year prime mission". As published (archive TAP query, 2026-10-31): 8,151 TOIs; `tfopwg_disp`, "TESS Follow-up Observing Program Working Group (TFOPWG) Dispostion": CP 815, KP 606, FP 1,315, FA 100, PC 4,820, APC 490, blank 5. 36 documented columns (API_TOI_columns.html) plus uncertainty and limit columns: period, epoch, duration, depth, planet radius, insolation, equilibrium temperature, TESS magnitude, distance, stellar Teff, log g and radius, proper motion, `toi_created`, `rowupdate`. The ExoFOP table has more: follow-up observation counts, SG priorities, the TESS project's disposition, planet names, free-text comments.
- Use case: when the TESS project alerts a new TOI, the follow-up community decides which candidates get scarce ground-based telescope time; a model on the catalog parameters ranks them by the chance of being a planet. Written by the curation: no source found that defines this task on the table (the vetting models found score light curves). Fit approximate (labels exist only for followed-up TOIs). Regime temporal by `toi_created` (new alerts scored with older resolved ones), with several TOIs per star (`toipfx`) to keep together.
- Siblings and duplicates: `kepler_dr24_tce_vetting` (`TBD -> Yes`, priority 4; Kepler TCEs with Autovetter labels) and `kepler_koi_disposition` (not screened yet; Kepler KOI table) are the same vetting task family on another mission with other units and labels (PROV-7), so the curator may want one or two of the three; `first_principles_kepler` (`No`, AHDS) is unrelated in task. External collections: none found.
- Better data: found by the gap scout for physics and astronomy; no further search this round.
- Papers and pages: Guerrero et al. 2021 (abstract read); WATSON-Net (arXiv 2511.08768) takes its reference labels from the ExoFOP TOI disposition field and favoured precision over recall (search snippet, not read); ExoMiner++ (Valizadegan et al. 2025) classifies TESS signals from light curves and diagnostics.
- Metric: none found (the archive's column page, the catalog paper's abstract, the vetting papers seen, which score light-curve models), so the fallback `roc_auc` (MET-1, MET-11); inputs none.
- Risks for /add-dataset: label maturity: the resolved share by alert year (CP, KP, FP, FA) is 72% for 2019, 25% for 2021, 15% for 2023, and 2026 has 23 resolved TOIs, so a test window needs an alert cutoff and a maturity window, and the time to a disposition likely differs by class (a false positive can be ruled out faster than a planet confirmed; LEAK-22 to LEAK-26, SPLIT-9, SPLIT-10); KP rows are planets known before TESS, labelled at the alert (the label is known at the prediction point: drop them for a new-candidate task, USE-3); planet parameters are refit after the alert as sectors accrue (`rowupdate`; the ExoFOP epoch of TOI 102.01 is from 2025), so pin a snapshot and check for post-alert values (LEAK-10); never take the ExoFOP follow-up counts, SG priorities, planet names or comments; PC and APC rows are unlabelled; the parameters are fits to light curves, measurements under SEL-15, but CNNs on light curves are the field's tool, so check that tabular models stay competitive (SEL-12); a live table takes the year of the pinned snapshot (PROV-9).
- Priority: gap + (physics & astronomy has 0 accepted), use case 0 (written by the curation), source + (NASA archive with column documentation and a catalog paper), shape + (2,836 resolved TOIs over 2018-2026, about 20 measured parameters with uncertainties, a time order), risk - (censored, likely class-dependent label timing; refit parameters).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the gap scout for physics and astronomy.
- as published: Transit candidates: 8,151 TOIs x 91 columns (transit period, duration, depth, planet radius, insolation, equilibrium temperature, TESS magnitude, distance, stellar Teff, log g, radius, proper ...; target: Resolved TFOPWG disposition: planet (CP, KP) vs false positive or false alarm (FP, FA); access: open.
- Why: NASA mission catalog whose label is the outcome of follow-up observations, a task done today, with a creation date per TOI for a temporal split
- Adds: Temporal binary classification in astronomy (2018-2026). Risks: planet parameters are refined after follow-up (rowupdate), so a snapshot may carry post-follow-up information; KP marks planets known before TESS; the table is live, so a dated snapshot is needed; about 2,800 resolved rows. Same task family as ...
