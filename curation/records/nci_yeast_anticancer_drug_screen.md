---
unique_name: nci_yeast_anticancer_drug_screen
name: 'NCI Yeast Anticancer Drug Screen datasets (April 2002 release: Stage0, Stage1, Stage2)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
original_source: GOV Website
domain: chemistry & material science
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://wiki.nci.nih.gov/display/NCIDTPdata/Yeast+Anticancer+Drug+Screen
- https://dtp.cancer.gov/databases_tools/bulk_data.htm
- '# DTP''s PubChem deposit, one assay per strain (AID 175: the mlh1 rad18 strain)'
- https://pubchem.ncbi.nlm.nih.gov/bioassay/175
- '# Simon et al. 2000, the pilot on 23 anticancer agents (related work)'
- https://pubmed.ncbi.nlm.nih.gov/10667584/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: an open NCI phenotypic screen of 87,264 compounds against DNA-repair and checkpoint mutant yeast strains (Stage0, with Stage1 and Stage2 follow-ups), a real compound-screening task with structures traceable by NSC number; the target and its unit (compound, or compound and strain) have to be chosen.
- Source: NCI DTP, "NCI Yeast Anticancer Drug Screen", April 2002 release (wiki.nci.nih.gov/display/NCIDTPdata/Yeast+Anticancer+Drug+Screen): Stage0 (stg0ftp.zip) 87,264 compounds, columns NSC, DIFFINH ("the difference between the duplicate growth inhibition measurements"), AVEINH ("the average of the duplicate growth inhibition measurements") and STRAIN; Stage1 14,837 compounds at 50 and 5 microM; Stage2 2,189 compounds at several concentrations; "active (growth inhibition of at least 70% in at least 1 strain)": Stage0 12,068 active and 75,196 inactive. PubChem holds one assay per strain, deposited by DTP on 2002-04-15 (AID 175, the mlh1 rad18 strain: 81,112 compounds tested, 10,175 active; "Compounds with inhibition of growth(giprct) >= 70% were considered active"). No licence stated. The pilot paper, Simon et al. 2000, Cancer Res 60:328 (PMID 10667584), tested 23 approved anticancer agents on the strain panel; no paper on the full screen found.
- Use case: a screening team decides which compounds to test for selective toxicity to DNA-repair-deficient cells (a stand-in for tumours with such defects, the rationale of Simon et al. 2000), predicted from the structure; no source names the decision, so the fit is approximate; regime grouped on the scaffold (SPLIT-31), with structures from DTP's open structure file or PubChem through the NSC number.
- Siblings and duplicates: none of this screen in `curation/records/` (grep for yeast anticancer, dtp, NSC); `yeast` is the UCI protein-localization set, unrelated; `yprop_4_1` (`No`, an anonymized drug-design endpoint) is the record it was found next to, not the same task. External collections: TUDataset `Yeast` and `YeastH` (79,601 graphs, 2 classes; built from the PubChem yeast assays per the page's reference, not opened).
- Better data: found as a related task next to `yprop_4_1`, not the same task; no further search this round.
- Papers and pages: the DTP wiki page; the PubChem AID 175 description; Simon et al. 2000 (abstract); Nascarella et al. 2009, Dose-Response 7:160 (hormesis in the 2,189 Stage2 compounds across 13 strains, no prediction task).
- Metric: none found (the DTP page and PubChem AID 175 define activity at 70% inhibition, no evaluation), so the fallback (`roc_auc` on active, `rmse` on AVEINH) (MET-1, MET-8); inputs none beyond the scaffold groups.
- Risks for /add-dataset: choose the unit and the target (active in any strain, one target per strain, selectivity against the wild type, or AVEINH as a regression; `Multi-target` if several); Stage1 and Stage2 hold only Stage0's actives, so the main task is Stage0; the strain names behind the STRAIN codes and the structures come from other files (PubChem or DTP), joined by NSC; duplicate-measurement noise (DIFFINH); the dtp.cancer.gov pages were not reachable (expired certificate), so check the download path.
- Priority: gap 0, use case 0 (ours), source + (the NCI DTP release, PubChem deposits), shape + (87,264 compounds), risk - (a target to define, joins for structures and strains).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through a related task next to `yprop_4_1`.
- as published: Stage0: 87,264 compounds (NSC numbers) screened in duplicate against a panel of S. cerevisiae DNA-repair and checkpoint mutant strains, columns NSC, STRAIN, AVEINH (mean growth inhibition), DIFFINH ...; target: Growth inhibition of a yeast strain by a compound (AVEINH, continuous), or active (at least 70% inhibition) in a strain / selectively active against the ...; access: open.
- Why: yprop_4_1 is drug-design data (Feng et al. 2003, J. Chem. Inf. Comput. Sci. 43:1463, four predictive-toxicology sets) with an anonymized target (oz252) and anonymized descriptors, so its endpoint cannot be named and no same-task dataset can be certified. The NCI yeast screen is a real, open compound screen in the ...
- Adds: A traceable source (NCI DTP release and a peer-reviewed screen paper), a named target and use case, real structures through NSC numbers (RDKit descriptors under CLEAN-24 instead of 251 unnamed columns), and about 10x the compounds of yprop_4_1 (87,264 against 8,885)
