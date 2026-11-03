---
unique_name: early_sepsis_mortality_transcriptome
name: Early sepsis whole-blood RNA-seq with in-hospital mortality and SOFA (GSE185263, Baghela et al. 2022)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
tags:
- AI-Filled (Verify)
- Tiny Data
- Many features
original_source: Other
year: '2022'
domain: medical & healthcare
problem_type: Binary Classification
source_links:
- https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE185263
- https://pubmed.ncbi.nlm.nih.gov/35027333/
- https://github.com/BoevaLab/GeneICL
- http://arxiv.org/abs/2610.08694
- https://ftp.ncbi.nlm.nih.gov/geo/series/GSE185nnn/GSE185263/suppl/GSE185263_raw_counts.csv.gz
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: whole-blood RNA-seq at first presentation of 348 patients with early sepsis (four emergency rooms and one ICU) with in-hospital death (52 of 345 per the run) and SOFA at 24 hours; a real triage question, but about 20,000 or more gene columns on 345 patients, with about 10 deaths per test fold.
- Source: Baghela et al. (Hancock lab, University of British Columbia), "Predicting sepsis severity at first clinical presentation: The role of endotypes and mechanistic signatures", EBioMedicine 2022 (doi 10.1016/j.ebiom.2021.103776, PMID 35027333, PMC8808161); GEO GSE185263, public 2022-01-10, Illumina (GPL16791), one supplementary file `GSE185263_raw_counts.csv.gz`. As published: "Blood RNA-Seq and clinical data were collected from 348 patients in four emergency rooms (ER) and one intensive-care-unit (ICU), and 44 healthy controls"; the GEO sample characteristics: disease state, age, sex, collection location (country), collection site (emergency room or ICU), "sofa 24h post admisssion", "in hospital mortality" (Survived or not). Raw counts, one column per sample.
- Use case: the emergency or ICU physician at first presentation triages a patient with suspected sepsis (escalation, ICU admission, antibiotics) from a blood draw: "The severity and endotype signatures ... providing a method to triage early sepsis patients" (abstract); fit approximate (a research RNA-seq profile stands in for a signature test, and in-hospital death has no fixed horizon). Regime: IID over patients, or grouped by collection site (five sites; the ICU cohort differs); a new hospital leans to grouped, but 52 deaths over five sites leave few positives per site.
- Siblings and duplicates: no other record holds GSE185263 (grep for the accession and GeneICL); the clinical sepsis records `sepsis_survival_minimal_clinical_records`, `sepsis_prediction`, `mimic_iv`, `eicu_collaborative_research_database` are other sources and features. From the same benchmark: `target_pediatric_relapse_transcriptome`, `beataml2_ex_vivo_drug_response`. External collections: GeneICL (Bohl, Theus, Wissel, Boeva, arXiv 2610.08694, 2026: 80 bulk-transcriptome outcome tasks; its sepsis-mortality task, n = 345, per the run).
- Better data: from the curator's Zotero collection (item 300, GeneICL); no search for better data in this run.
- Papers and pages: Baghela 2022 (signatures for severity and mortality with "accuracy/AUC of 77-80%"); GeneICL 2026; GEO lists two later PubMed ids (36690713, 37090709; not read).
- Metric: none deliberate: the paper reports accuracy and AUC together ("accuracy/AUC of 77-80%", abstract); fallback `roc_auc` (MET-1, MET-5, MET-6); inputs none.
- Risks for /add-dataset: `Too Small` risk (52 deaths among 345, about 10 per test fold of five, fewer per site; TP-5); a gene table far wider than its rows (width is no reason to drop, CLEAN-22; normalise per sample, not with size factors fit over all samples, LEAK-30); drop the 44 controls, and SOFA for a mortality target (measured after the sample, LEAK-10); check how GeneICL got 345 of 348 (patients without an outcome); site and ER/ICU as features or groups.
- Priority: gap 0 (medical & healthcare and binary are not thin), use case 0 (approximate fit), source + (GEO with a peer-reviewed paper), shape 0 (345 patients), risk - (few deaths per fold, TP-5).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 300: "GeneICL: A Tabular Foundation Model for Bulk Transcriptomics".
- as published: patients: 392 samples = 348 sepsis patients (266 sampled in four emergency rooms, 82 in one ICU) + 44 healthy controls; sites Australia 113, Netherlands 104, Toronto 82, Colombia 73, Vancouver 20 ...; target: in-hospital mortality (binary, 52 of 345 died); alternative: SOFA score 24 h after admission (regression); access: open.
- Why: Real multi-site prospective cohort, open in GEO, with the outcome measured after the sample; GeneICL's sepsis-mortality task (n=345).
- Adds: A sepsis-prognosis task from the blood transcriptome, next to the clinical sepsis records (sepsis_survival_minimal_clinical_records, mimic_iv); five sites allow a grouped split. Small: 52 deaths.
