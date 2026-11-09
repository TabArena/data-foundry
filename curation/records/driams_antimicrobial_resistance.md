---
unique_name: driams_antimicrobial_resistance
name: 'DRIAMS: Database of Resistance Information on Antimicrobials and MALDI-TOF Mass Spectra'
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 3
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
- Many features
original_source: Other
year: '2021'
domain: medical & healthcare
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.5061/dryad.bzkh1899q
- https://doi.org/10.1038/s41591-021-01619-9
- https://datadryad.org/dataset/doi:10.5061/dryad.bzkh1899q
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

**Assessment (AI, 2026-11-08):** size check for the large-datasets review: the paper's tasks are one table per species and drug of 2,631 to 4,961 DRIAMS-A spectra x 6,000 bins (one drug over all species: about 26,500 to 30,500 spectra), not 300,000 rows, and the one site with case ids and dates is an 86 GB download; the call stands, priority 3.
- As published: Dryad doi:10.5061/dryad.bzkh1899q, version of 2025-08-19 (version 12), CC0; four archives `DRIAMS_A.tar.gz` 86.16 GB, `DRIAMS_B.tar.gz` 3.69 GB, `DRIAMS_C.tar.gz` 12.43 GB, `DRIAMS_D.tar.gz` 42.56 GB and a README, 144.84 GB in all (Dryad API). Each archive has `raw`, `preprocessed`, `binned_6000` (one text file per spectrum) and `id` (yearly metadata tables with the species and one column per antimicrobial). The preprint (bioRxiv 10.1101/2020.07.30.228411 v2, posted 2021-07-12; Results and Online Methods): 303,195 spectra and 768,300 resistance labels of 803 species; DRIAMS-A University Hospital Basel, 11/2015-08/2018, 145,341 spectra, 71 antimicrobials; DRIAMS-B Canton Hospital Basel-Land 01-06/2018; DRIAMS-C Canton Hospital Aarau 01-08/2018; DRIAMS-D Viollier 01-06/2018, 7,771 spectra with 7,720 resistance profiles. The bins are processed: square root, Savitzky-Golay smoothing, SNIP baseline, TIC, then 3 Da bins from 2,000 to 20,000 Da. The label is 1 for resistant or intermediate, "as both types of samples prevent the application of the antibiotic".
- The task's table: one row per spectrum of one species with one drug's label, the paper's main scenarios (Supplemental Table 5, all workstations): S. aureus oxacillin 3,790, E. coli ceftriaxone 4,961, K. pneumoniae ceftriaxone 2,860, about 8-10% resistant. The paper excludes the hospital-hygiene workstation, leaving 3,411, 4,302 and 2,631 (computed). A drug table over all species is larger: ceftriaxone 26,545 and ciprofloxacin 30,543 DRIAMS-A spectra (Supplemental Table 2), with the species as an input. Inputs: the 6,000 bins (a spectrum in the processed state), plus the species in a multi-species table. DRIAMS-A's id tables carry `case_no`, `acquisition_date` and `workstation` (the metadata columns the authors' maldi-learn loader expects), so a temporal split with cases as groups fits there (SPLIT-13). For B, C and D "no information regarding clinical cases was provided" (Online Methods).
- Access: the binned spectra and the id tables come only inside the full archives, so a DRIAMS-A build downloads 86 GB (B alone is 3.7 GB). CC0, no data-use agreement. The Dryad API's file download answered "Unauthorized, must have current bearer token" and the web link gave a script a 403, so a build needs a Dryad API token or a browser download.
- Changes the call: the size is per task, not per database: thousands of rows and 6,000 features per species-drug table. One fact for /add-dataset: hospital-hygiene samples are grown on "selective media containing antibiotics, enabling the growth of resistant strains only", and a classifier recognises the workstation from the spectrum (Supplemental Table 5), so the definition follows the paper and drops them (a route of mostly one class that models recognise, LEAK-39). The paper's own split is random, "stratified by both antimicrobial class and patient case number", 10 repeats, with a temporal check on May-August 2018. The priority stays 3: gap 0, use case +, source +, shape +, risk - (the 86 GB build, a choice of tasks).
- Not checked: the sizes of `binned_6000` and `id` inside each archive (nothing downloaded); the id-table columns on a file (taken from the loader's code); the counts in the Nature Medicine version (the preprint was read); the spectra per site for B and C.

CC (2026-11-08, Lennart): accepted for adding (`Yes`) in the screening review of the large candidates (most rows, most features).
