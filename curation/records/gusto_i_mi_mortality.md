---
unique_name: gusto_i_mi_mortality
name: GUSTO-I trial patient data (30-day mortality after acute myocardial infarction), as distributed in the R package predtools
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
domain: medical & healthcare
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.1161/01.cir.91.6.1659
- https://cran.r-project.org/package=predtools
- https://github.com/resplab/predtools/blob/master/R/gusto.R
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: patient data of the GUSTO-I trial (40,830 patients with acute MI, enrolled 1990-1993) with death by day 30 and the admission predictors of the published Lee et al. model; a large, real clinical prediction task, with an unclear release path of the patient file (predtools gives "Internet" as its source).
- Source: the GUSTO-I trial and its 30-day mortality model: Lee, Woodlief, Topol, Weaver, Betriu, Col, Simoons, Aylward, Van de Werf, Califf, "Predictors of 30-day mortality in the era of reperfusion for acute myocardial infarction. Results from an international trial of 41,021 patients", Circulation 91(6):1659-1668 (1995, https://doi.org/10.1161/01.cir.91.6.1659). The patient file ships in the R package predtools (resplab, UBC; https://cran.r-project.org/package=predtools): "Anonymized data from the gusto trial", "A data frame with 40830 rows and 29 variables", documenting only `day30`, `sho`, `hig`, `dia` and `hrt`, with "@source Internet" (https://github.com/resplab/predtools/blob/master/R/gusto.R).
- Use case: at admission for an acute MI the cardiologist estimates the risk of death from age, systolic blood pressure, Killip class, heart rate and infarct location (together "about 90% of the prognostic information" in the abstract) and history; the paper's model "accurately estimated the likelihood of death" and names no decision; fit direct for a risk estimate at admission, though care has moved from thrombolysis to primary PCI since (`Outdated` to weigh); regime IID (a trial cohort of 15 countries; region could group).
- Siblings and duplicates: `mic` (`Yes`, 1,700 Krasnoyarsk patients with complications and the lethal outcome: the same quantity among others, another source, PROV-4); `smart_vascular_events` (another Steyerberg case-study cohort, a different task). No other GUSTO record (searched gusto, predtools, clinicalpredictionmodels). External collections: none known.
- Better data: no new search; found as better data for `mic`.
- Papers and pages: Lee et al. 1995 (abstract read on Europe PMC); Steyerberg, Clinical Prediction Models, the chapter 22 page (https://www.clinicalpredictionmodels.org/extra-material/chapter-22, moved here from source_links as related work, PROV-12: "The GUSTO-I trial provided data for a prediction model developed by Kerry Lee et al at Duke Clinical Research Institute"; it offers the subsamples sample2, sample4 and sample5, not the full file); the predtools documentation.
- Metric: none found as one criterion (the abstract reports chi-square statistics per predictor and no c-index; the full text not read); fallback `roc_auc` (MET-5, MET-8). Inputs: none.
- Risks for /add-dataset: the file's provenance (PROV-2: who released the patient-level data, Duke or the Steyerberg book, is unconfirmed; 40,830 rows against 41,021 enrolled needs a note); 24 of the 29 columns are undocumented in predtools (map them to the paper's predictors); the thrombolytic arm, if the file holds it, is randomised and known at admission; 30-day death about 7%, so about 2,860 deaths.
- Priority: gap 0 (medical, binary and IID are not thin), use case 0 (the paper names the estimate, not the decision), source + (Circulation paper of a documented trial), shape + (40,830 patients, mixed types), risk 0 (the file's release path is a PROV-2 note, not a leak or an unclear target).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `mic`.
- as published: 40,830 patients, 29 variables (predtools documentation); trial enrolment 1990-1993 in 15 countries; target: day30: death within 30 days (binary); access: open.
- Why: The same quantity as mic's lethal outcome (death after an MI, predicted from admission data: history, examination, ECG location), with features of the same kind.
- Adds: 24 times the patients (40,830 against 1,700) from many countries instead of one Krasnoyarsk hospital. Not newer (1990-1993 against 1992-1995), binary death instead of mic's cause of death and complications. Provenance caveat (PROV-2): the trial is well traced, but predtools gives the file's source as 'Internet'; who ...
