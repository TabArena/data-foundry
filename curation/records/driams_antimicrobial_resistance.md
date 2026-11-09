---
unique_name: driams_antimicrobial_resistance
name: 'DRIAMS: Database of Resistance Information on Antimicrobials and MALDI-TOF Mass Spectra'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
- Many features
- Spectral Data
original_source: Other
year: '2021'
domain: medical & healthcare
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.5061/dryad.bzkh1899q
- https://doi.org/10.1038/s41591-021-01619-9
- https://datadryad.org/dataset/doi:10.5061/dryad.bzkh1899q
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: more than 300,000 clinical MALDI-TOF spectra from four Swiss laboratories linked to more than 750,000 resistance results, with a treatment decision the paper names; binned spectra as features (the `micro_mass` precedent) and a heavy build.
- Source: Weis, Cuénod, Rieck, Borgwardt & Egli, "DRIAMS: Database of Resistance Information on Antimicrobials and MALDI-TOF Mass Spectra", Dryad 10.5061/dryad.bzkh1899q (2021-11-01; updated 2025-08-19, "A new DRIAMS_C.tar.gz File was uploaded to remove some corrupt information"; CC0 per the Dryad API), with Weis et al., "Direct antimicrobial resistance prediction from clinical MALDI-TOF mass spectra using machine learning", Nature Medicine (January 2022). As published: four archives, DRIAMS-A (University Hospital Basel, 86 GB), B (Canton Hospital Basel-Land, 3.7 GB), C (Canton Hospital Aarau, 12.4 GB), D (Viollier AG, 42.6 GB), each with `raw`, `preprocessed`, `binned_6000` ("binning along the mass-to-charge-ratio axis with a bin size of 3Da, resulting in 6000 feature bins") and an `id` folder whose metadata holds "species and antimicrobial resistance corresponding to each spectra" (Dryad description).
- Use case: "current culture-based techniques can take up to 72 hours to generate results"; a "retrospective clinical case study of 63 patients found that implementing this approach would have changed the clinical treatment in nine cases" (abstract): the microbiologist and the treating physician choose or narrow the antibiotic when the species identification comes back, before the susceptibility test; fit direct. Regime temporal (isolates arrive over time) with patients as groups inside (SPLIT-13); the paper's own split not read.
- Siblings and duplicates: `micro_mass` (`Yes`, species identification from 571 MALDI-TOF spectra) shares the instrument and the binned form, not the task (PROV-7); `amr_uti_antibiotic_resistance` (resistance from health records), `cryptic_mtb_drug_resistance` (genomes) and `bacteria_id_raman` are other resistance or identification tasks. No other record of DRIAMS (grep: driams, maldi). External collections: none found; maldi-learn is the authors' loader.
- Better data: found as a related task next to `micro_mass`; no further search this round.
- Papers and pages: Weis et al. 2022 (Nature Medicine); the Dryad README; github.com/BorgwardtLab/maldi-learn.
- Metric: the abstract reports ROC AUCs "of 0.80, 0.74 and 0.74" for S. aureus, E. coli and K. pneumoniae, the paper's headline; other measures in the full text not read. `roc_auc`, also the fallback (MET-5, MET-8); inputs none.
- Risks for /add-dataset: one target per drug and species, so a choice of tasks to ship (the paper's scenarios: S. aureus, E. coli, K. pneumoniae against their key drugs); 6,000 spectral bins per row (`Many features`; SEL-15 weighs raw bins against, the `micro_mass` precedent keeps them); several isolates per patient (a patient or case id in `id` to confirm, SPLIT-24); 145 GB of archives of which only `binned_6000` and `id` are needed (`Needs extensive data wrangling`); resistance from each laboratory's routine testing, so methods and breakpoints may differ by site and year (CLEAN).
- Priority: gap 0 (medical & healthcare, binary, temporal not thin), use case + (the paper names the treatment decision), source + (Nature Medicine and Dryad), shape + (thousands of spectra per common species, a time and site structure), risk - (spectral bins, heavy build, tasks to choose): 3.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through a related task next to `micro_mass`.
- as published: more than 300,000 MALDI-TOF spectra with more than 750,000 antimicrobial resistance phenotypes from four Swiss institutions (DRIAMS-A Basel university hospital, B Basel-Land, C Aarau, D Viollier); ...; target: resistant or susceptible for a given antimicrobial on a given clinical isolate (one binary target per drug); access: open.
- Why: same domain, instrument and data shape as micro_mass (MALDI-TOF spectra of bacterial isolates, vectorized to fixed bins, grouped by species or isolate), but a different task with a named clinical decision and a published benchmark; the micro_mass precedent shows binned spectra are in scope here
- Adds: for micro_mass itself no larger species-identification set was found whose labels are independent of the spectra (routine labs label spectra with the instrument vendor's own matching software, which makes the target near-circular); DRIAMS keeps the modality and brings a target that is measured separately from the ...
