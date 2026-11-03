---
unique_name: kepler_dr24_tce_vetting
name: Kepler Q1-Q17 DR24 threshold-crossing events with Autovetter training labels
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- AI-Filled (Verify)
original_source: GOV Website
year: '2015'
domain: physics & astronomy
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://doi.org/10.1088/0004-637X/806/1/6
- https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=q1_q17_dr24_tce
- https://exoplanetarchive.ipac.caltech.edu/docs/API_tce_columns.html
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: NASA's Kepler Q1-Q17 DR24 threshold-crossing events with the Autovetter's training labels (planet candidate, astrophysical false positive, non-transiting phenomenon), the table a random forest was built on; it fills the empty physics and astronomy domain, but how the labels relate to the diagnostic columns, and the light-curve CNNs later trained on the same signals, need a look.
- Source: NASA Exoplanet Archive (IPAC/Caltech for NASA), table `q1_q17_dr24_tce`, documented at API_tce_columns.html (117 database columns in 13 groups: transit fit, stellar parameters, trapezoid fit, weak-secondary test, light-curve and pixel vetting statistics, ghost diagnostic, rolling-band histogram, bootstrap, Autovetter outputs). Counts from the scout's TAP query (2026-10-30, not repeated): 20,367 TCEs on 12,669 stars, 15,737 labelled (PC 3,600, AFP 9,596, NTP 2,541), 4,630 UNK. The method paper is McCauliff et al. 2015 (ApJ 806, 6; arXiv 1408.1496) on the Q1-Q12 TCEs ("18,406 transit-like features"); the DR24 Autovetter catalog applies it later (its own document not read). `av_training_set`: "If the TCE was included in the training set, the training label encodes what is believed to be the "true" classification."
- Use case: after the pipeline flags a periodic signal, the vetting team decides whether it becomes a planet candidate for follow-up; McCauliff et al. (abstract): "Vetting candidate signals manually by inspecting light curves and other diagnostic information is a labor intensive effort", so a classifier on the attributes does it. Fit direct. Regime grouped by star (several TCEs per KIC target; USE-10); Kepler data of 2009-2013.
- Siblings and duplicates: `kepler_koi_disposition` and `tess_toi_disposition` (candidates of this run: the KOI table's confirmed versus false-positive disposition, and TESS's TOI table; same mission family with other units and labels, PROV-7, though the curator may want one Kepler task); `first_principles_kepler` (No, AHDS: six planets fit by Kepler's third law); `apokasc3_red_giant_mass` (another Kepler-derived candidate, another task). External collections: none found.
- Better data: from the gap scout for physics and astronomy, listed next to `first_principles_kepler` as a related task, not as better data for it.
- Papers and pages: McCauliff et al. 2015 (random forest, "overall error rate of 5.85%"); Shallue and Vanderburg 2018 (AJ 155, 94) trained a CNN on the light curves of Kepler TCEs and report that "98.8% of the time it ranks plausible planet signals higher than false-positive signals"; that they used these DR24 labels is from memory, to verify.
- Metric: McCauliff et al. report an overall and a per-class error rate, threshold metrics without a fixed decision (MET-6), so the fallback `log_loss` for three classes (MET-8); a binary planet-candidate framing would take `roc_auc`.
- Risks for /add-dataset: drop the Autovetter outputs (`av_pred_class`, `av_vf_*`, `av_pp_*`; LEAK-10); the AFP and NTP labels came from TCERT and other diagnostics, so some vetting statistics may have set the label (SEL-5, LEAK-10; read the Autovetter document); SEL-12 and SEL-13: the attributes are fits and statistics computed from light curves and pixel data, and a CNN on the light curves is the later state of the art, so check that tabular models stay competitive on this table (the field's own tool here was a random forest; transit depth, period and centroid offsets read as measurements under SEL-15); UNK rows go.
- Priority: gap + (physics & astronomy has 0 accepted, multiclass is thin), use case +, source + (NASA archive with column documentation and a method paper), shape + (15,737 labelled TCEs, over 100 numeric attributes, grouped by star), risk - (labels and diagnostics; the light-curve modality).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through a related task next to `first_principles_kepler`; the gap scout for physics and astronomy.
- as published: Threshold-crossing events (periodic transit-like signals) on Kepler target stars: 20,367 TCEs on 12,669 stars x 158 columns; 15,737 labelled (PC 3,600, AFP 9,596, NTP 2,541) on 9,865 stars, 4,630 ...; target: av_training_set: planet candidate (PC), astrophysical false positive (AFP) or non-transiting phenomenon (NTP); PC labels from TCERT dispositions, AFP and NTP ...; access: open.
- Why: NASA mission data with a paper-defined three-class task that the source solved with a random forest on these attributes (a tabular tool); expert labels; open archive table | The real, decision-bearing task on Kepler orbital data (period, transit fit, stellar parameters); the record's Kepler's-third-law fit (6 ...
- Adds: Multiclass (thin, 24 of 173) in physics and astronomy (0 accepted); grouped by star (several TCEs per KIC star). Risks: drop the av_* model outputs (av_pred_class, vote fractions, posteriors); check which diagnostic columns TCERT read to set the label (leak); the data is dated (2009-2013) although the task continues ...
