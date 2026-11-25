---
unique_name: prism_stool_metabolomics_cd_vs_uc
name: MW-ST001000-CD-UC (PRISM Stool Metabolomics CD vs UC)
checked_by:
- AI (UNVERIFIED)
data_foundry_status:
- WIP (Triage)
claimed_by: Andrej
suggestion: TBD -> 2nd Tier
priority: 1
tags:
- AI-Filled (Verify)
- Tiny Data
- Many features
- Clinical Study
- 'Samples: Over Time'
- 'Time: Lost'
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

**Screening (AI, 2026-11-25):** `TBD -> 2nd Tier`, priority 1: Crohn's disease against ulcerative colitis from untargeted stool metabolomics of 121 PRISM patients (Franzosa et al.); a documented cohort, but a tiny cut the benchmark chose (the paper classified IBD against controls, and three classes), from patients already diagnosed and treated.
- Source: Franzosa et al., "Gut microbiome structure and metabolic activity in inflammatory bowel disease", Nature Microbiology 4:293-305 (online 2018-12-10; doi 10.1038/s41564-018-0306-4), Broad Institute and MGH. Data: Metabolomics Workbench ST001000 (submitted 2018-07-09, released 2019-04-17; licence CC BY-NC-ND 4.0 per the Workbench summary, while the TabBench-Bio registry says CC BY 4.0; noted, no verdict reason, EV-4): 220 stool samples (factors only `Diagnosis`: CD 88, UC 76, control 56) in four LC-MS analyses (AN001878 HILIC-pos, AN001879 HILIC-neg, AN001880 C18-neg, AN001881 C8-pos). The Workbench summary: "cross-sectional stool samples from discovery (n=155) and validation (n=65) cohorts of CD, UC, and non-IBD control subjects"; PRISM stool "collected at the MGH gastroenterology clinic", the Dutch validation subjects at home. As TabBench-Bio ships it (registry `MW-ST001000-CD-UC`, read 2026-11-25): AN001880 alone, 121 PRISM patients x 2,121 features, target 1 = CD, 0 = UC, log1p, with the controls and the validation cohort left out.
- Use case: a gastroenterologist telling CD from UC in a patient with IBD; in practice endoscopy, histology and imaging settle it, and the stool metabolome is a research biomarker. The label comes from that separate work-up (ground truth, USE-1), but it was settled before the stool was taken, and the paper models antibiotics, immunosuppressants, mesalamine and steroids as covariates, so the features carry the treatment. Fit approximate. Collection: clinic patients enrolled over time, one cross-sectional sample each, the diagnosis before the sample; no date and no recorded order in the release (the numeric `local_sample_id`s, 7122 and up, are unchecked as an order): samples over time, time lost; type `Clinical Study`.
- Split: leaf L-PLACE.random (`ForcedIIDFromGrouped`, one place, the transfer untested) because [CLI.meets] another site (the source validates on an independent Dutch cohort, "generalized well to the independent validation cohort"), [PLACE.several] no (two sites at most, PRISM and the Netherlands cohort, fail the enough-groups check; the benchmark's cut holds PRISM alone), [PLACE.units] no (one sample per subject); open: if the curator takes later patients at MGH as the use case instead, [CLI.dated] no and [ORDER.order] asks whether the sample ids give a checked order, else the forced step; whether to train on PRISM and test on the Dutch cohort as the source did (one split, SPLIT-5).
- Siblings and duplicates: no other record of PRISM, ST001000 or IBD metabolomics (grep by name, accession, author and disease; `optn_liver_waitlist_90day_mortality` matches "PRISM" only by word). External collections: TabBench-Bio (live registry and leaderboard).
- Better data: none found in a quick look; HMP2/IBDMDB (Lloyd-Price et al., Nature 2019) has stool metabolomics of about 90 participants (CD 43, UC 25, non-IBD 22, per a reanalysis), longitudinal, so fewer CD and UC subjects than PRISM's 121; no record of it.
- Papers and pages: Franzosa et al. (Results; Methods); https://www.metabolomicsworkbench.org/data/DRCCMetadata.php?StudyID=ST001000; TabBench-Bio (arXiv 2609.07441).
- Metric: the paper scored IBD against control by AUC with random forests ("ranging from 0.86 to 0.92") and the three-way CD/UC/control call by percent correct (64-65% within PRISM); it reports no CD-against-UC classifier, so none found for this cut. TabBench-Bio ranks classification by macro-F1 (Sec. 3.5), a threshold metric without a fixed threshold (MET-6). Fallback `roc_auc`; inputs none.
- Risks for /add-dataset: drug metabolites can give the diagnosis away (mesalamine is first-line for UC; LEAK-10, USE-3: set the prediction point, then decide on annotated drug features); which task to ship: the source's own IBD-against-control (155 subjects, or 220 with the validation cohort) or the three classes over all four analyses, rather than the benchmark's cut (SEL-8, TP-6); one of four analyses only; no batch or plate metadata (registry note); 121 rows, 53 UC, about 10 per test fold (TP-5 holds); the forced leaf goes to a reviewer.
- Priority: gap 0 (medical 39, binary 86, none thin), use case 0 (approximate, no actor named), source + (paper and repository), shape 0 (121 rows), risk - (treatment in the features).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 121 x 2,121; target: diagnosis (68 CD / 53 UC).
- Why: Crohn's disease vs ulcerative colitis from untargeted stool metabolomics (PRISM cohort, C18-negative table AN001880)
- Notes: Not in the paper's table: in the live registry and leaderboard (snapshot 2026-10-23). Franzosa et al. 2019; the external 43-person validation cohort is left out.
