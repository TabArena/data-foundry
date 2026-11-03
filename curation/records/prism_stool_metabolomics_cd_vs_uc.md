---
unique_name: prism_stool_metabolomics_cd_vs_uc
name: MW-ST001000-CD-UC (PRISM Stool Metabolomics CD vs UC)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
tags:
- AI-Filled (Verify)
- Tiny Data
- Many features
collections:
- TabBench-Bio
original_source: Other
year: '2018'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
source_links:
- https://doi.org/10.1038/s41564-018-0306-4
- https://www.metabolomicsworkbench.org/data/DRCCMetadata.php?StudyID=ST001000
- https://arxiv.org/abs/2609.07441
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: Crohn's disease against ulcerative colitis from untargeted stool metabolomics of 121 PRISM patients (Franzosa et al.); a documented cohort, but a tiny cut the benchmark chose (the paper classified IBD against controls, and three classes), from patients already diagnosed and treated.
- Source: Franzosa et al., "Gut microbiome structure and metabolic activity in inflammatory bowel disease", Nature Microbiology 4:293-305 (online 2018-12-10; doi 10.1038/s41564-018-0306-4), Broad Institute and MGH. Data: Metabolomics Workbench ST001000 (released 2019-04-17; the REST summary gives the licence as CC BY-NC-ND, the TabBench-Bio registry says CC BY 4.0): 220 stool samples (factors: CD 88, UC 76, control 56) in four LC-MS analyses (AN001878 HILIC-pos, AN001879 HILIC-neg, AN001880 C18-neg, AN001881 C8-pos); the paper counts 8,869 clustered features over the four methods. PRISM, the discovery cohort, is 155 subjects (68 CD, 53 UC, 34 non-IBD controls); the Dutch validation cohort 65 (20 CD, 23 UC, 22 controls). As TabBench-Bio ships it (registry `MW-ST001000-CD-UC`, live registry only, not the paper's Table 4): AN001880 alone, 121 PRISM patients x 2,121 features, target 1 = CD, 0 = UC, log1p, with the controls and the validation cohort left out.
- Use case: a gastroenterologist telling CD from UC in a patient with IBD; in practice endoscopy, histology and imaging settle it, and the stool metabolome is a research biomarker. The paper's PRISM samples are cross-sectional, from clinic patients already diagnosed, with antibiotics, immunosuppressants, mesalamine and steroids modelled as covariates (Methods), so the features carry the treatment. Fit approximate; regime IID (one sample per subject), with the validation cohort as a possible second site.
- Siblings and duplicates: no other record of PRISM, ST001000 or IBD metabolomics (grep by name, accession and disease). External collections: TabBench-Bio (live registry and leaderboard snapshot of 2026-10-23).
- Better data: a candidate of the benchmark TabBench-Bio (the run searched no further).
- Papers and pages: Franzosa et al. (Results; Methods); https://www.metabolomicsworkbench.org/data/DRCCMetadata.php?StudyID=ST001000; TabBench-Bio (Kreuer et al. 2026, arXiv 2609.07441).
- Metric: the paper scored IBD against control by AUC with random forests ("ranging from 0.86 to 0.92") and the three-way CD/UC/control call by percent correct (64-65% within PRISM); it reports no CD-against-UC classifier, so none found for this cut. TabBench-Bio ranks classification by macro-F1 (Sec. 3.5), a threshold metric without a fixed threshold (MET-6). Fallback `roc_auc`; inputs none.
- Risks for /add-dataset: drug metabolites can give the diagnosis away (mesalamine is first-line for UC; LEAK-10, USE-3: set the prediction point, then decide on annotated drug features); which task to ship: the source's own IBD-against-control (155 subjects, or 220 with the validation cohort) or the three classes over all four analyses, rather than the benchmark's cut (SEL-8, TP-6); one of four analyses only; no batch or plate metadata (registry note); 121 rows, 53 UC, about 10 per test fold (TP-5 holds).
- Priority: gap 0 (medical, binary), use case 0 (approximate, no actor named), source + (paper and repository), shape 0 (121 rows), risk - (treatment in the features).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 121 x 2,121; target: diagnosis (68 CD / 53 UC).
- Why: Crohn's disease vs ulcerative colitis from untargeted stool metabolomics (PRISM cohort, C18-negative table AN001880)
- Notes: Not in the paper's table: in the live registry and leaderboard (snapshot 2026-10-23). Franzosa et al. 2019; the external 43-person validation cohort is left out.
