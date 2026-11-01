---
unique_name: nci_aids_antiviral_screen
name: NCI DTP AIDS Antiviral Screen data (aids_conc_may04, with the AIDO99SD structure file)
checked_by:
- AI (UNVERIFIED)
data_foundry_status:
- WIP (Triage)
claimed_by: Lennart
suggestion: TBD -> Yes
priority: 4
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
collections:
- ChemPile
original_source: GOV Website
year: '2004'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Multiclass Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://wiki.nci.nih.gov/display/NCIDTPdata/AIDS+Antiviral+Screen+Data
- https://dtp.cancer.gov/databases_tools/bulk_data.htm
- '# MoleculeNet HIV, a processed copy (41,127 compounds, binary), Wu et al. 2018'
- https://doi.org/10.1039/C7SC02664A
v2_path: datasets/_dev/tabarena-v0pt2/nci_aids_antiviral_screen/dataset.py
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: the full NCI DTP AIDS antiviral screen (43,850 compounds with an expert conclusion CA, CM or CI; structures for 42,390), the screen that `hiva_agnostic` is a 4,229-compound anonymized cut of; a version of a shipped dataset (PROV-6), so the curator decides which one enters.
- Source: NCI Developmental Therapeutics Program, "AIDS Antiviral Screen Data" (wiki.nci.nih.gov/display/NCIDTPdata/AIDS+Antiviral+Screen+Data): the screen "has checked tens of thousands of compounds for evidence of anti-HIV activity"; results are "evaluated and placed in one of three categories": CA confirmed active, CM confirmed moderately active, CI confirmed inactive, concluded by trained staff from each dose-response curve. Files: aids_conc_may04.txt (May 2004, 43,850 compounds: NSC and conclusion), aids_ec50_may04.txt (39,365 NSCs) and aids_ic50_may04.txt (39,350 NSCs); AIDO99SD.BIN (October 1999, 42,390 structures as an MDL SD file, 2D converted to 3D with Corina, no stereochemistry). The assay: Weislow et al. 1989, J Natl Cancer Inst 81:577 (not opened). No licence stated.
- Use case: a medicinal-chemistry team decides which compounds to send to an antiviral assay, predicted from the structure (virtual screening); the source names no actor, so the fit is approximate; regime grouped on the Bemis-Murcko scaffold (SPLIT-31), as MoleculeNet and OGB split this screen.
- Siblings and duplicates: `hiva_agnostic` (`Yes`, TabArena v0.1 and BeyondArena): the 2007 Agnostic Learning vs. Prior Knowledge challenge's cut of this screen (4,229 labelled compounds, 1,617 unnamed binary descriptors, CA and CM merged); the same source and task, so a version (PROV-6), not a distinct task; Andrej's note there ("Might consider to restore it to be a 3-class problem") is what this release allows. `muv_maximum_unbiased_validation` (`TBD -> 2nd Tier`): its HIV set is a PubChem assay, not this screen. External collections: MoleculeNet HIV and OGB `ogbg-molhiv` (41,127 compounds, binary), TUDataset `AIDS` (2,000 graphs).
- Better data: found as better data for `hiva_agnostic`; no further search this round.
- Papers and pages: the DTP wiki page; Weislow et al. 1989; Wu et al. 2018, MoleculeNet, Chem Sci 9:513 (doi 10.1039/C7SC02664A; publisher page returned 403, not read); the OGB page (ogb.stanford.edu/docs/graphprop): "for ogbg-molhiv, we use ROC-AUC for evaluation", with a scaffold split; Guyon et al. 2007 for HIVA.
- Metric: `roc_auc` on active (CA or CM) against inactive, the OGB leaderboard's metric under its scaffold split (a deliberate choice, MET-4 by analogy); the HIVA challenge ranked by the balanced error rate on its own cut; inputs: the scaffold groups, computed from the structures (MET-1).
- Risks for /add-dataset: join the conclusions to the structures by NSC (42,390 of 43,850 have one); the structure file has no stereochemistry and carries salts; few actives (the share in `ogbg-molhiv` not counted here); binary or three classes is a choice (CM is "moderately active"); the EC50 and IC50 files are a regression alternative, but "computer-generated averages that may not reflect everything considered in the expert conclusions"; it holds `hiva_agnostic`'s task, so at most one of the two should ship (PROV-6); the dtp.cancer.gov bulk-data page was not reachable (expired certificate), so check the download.
- Priority: gap + (multiclass is thin, if the three conclusions are kept), use case 0, source + (NCI DTP, the class definitions on its page), shape + (43,850 compounds, scaffold groups), risk - (a version of a shipped dataset; a structure join).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `hiva_agnostic`.
- as published: 43,850 compounds in aids_conc_may04.txt (NSC number + CA/CM/CI conclusion); EC50 file 39,365 NSCs, IC50 file 39,350 NSCs; structures for 42,390 compounds in AIDO99SD.BIN; MoleculeNet HIV = 41,127 ...; target: Anti-HIV activity of a screened compound: confirmed active / confirmed moderately active / confirmed inactive (binarized as active vs inactive), from the NCI ...; access: open.
- Why: Same target and screen as hiva_agnostic: HIVA is the Agnostic Learning vs. Prior Knowledge challenge's subset of this very NCI screen (3,845 training + 384 validation compounds), given as 1,617 unnamed binary descriptors. The DTP release is the same measurement with the compounds named.
- Adds: 41,127-43,850 compounds instead of 4,229 (149 active), labels for every compound instead of a test set whose labels were never released, the original three classes (CA/CM/CI) instead of a pre-binarized target, and real structures (NSC numbers, SMILES) instead of anonymized bits, which removes the Anonymized marker ...
- A newer release of the same source as the record(s) named above (PROV-6): the curator decides which one enters.

**Assessment (AI, 2026-11-01):** the benchmark ChemPile (https://arxiv.org/abs/2505.12534) carries this record's data as "hiv": the MoleculeNet HIV processing of this screen (41,127 compounds, SMILES, active or moderately active against inactive), turned into text prompts by the ChemNLP builder `data/tabular/hiv`. `hiva_agnostic` holds the 2007 challenge subset of the same screen. Tagged ChemPile on 2026-11-01.

**Assessment (AI, 2026-11-01):** added as `datasets/_dev/tabarena-v0pt2/nci_aids_antiviral_screen/`: 41,133 compounds, the structure as a `SMILES` column (the one feature, CLEAN-24 as amended), the screen's three conclusions (CA 386, CM 1,011, CI 39,736), scaffold-grouped splits (20,772 groups), `log_loss` fallback. `dataset check` clean; the task, leak, group and dtype probes raise no flag on 5 or 9 splits (random forest macro ROC AUC 0.833, log loss 0.141, 9 of 9 above the dummy). A full review panel ran (10 agents, one rebuttal round); the mediator recommends shipping after changes, and every settled change is applied: the source's charge code read as +1 (PROV-13; 690 shipped compounds carried a hydrogen the reader invented, 2 unreadable records recovered), the target typed as an ordered scale (CLEAN-25), the metric reason corrected (MET-2), the NSC-batch dependency disclosed in `splits_comment` (SPLIT-30, LEAK-38 format), and the probes re-run on the repaired data. The curator supplied Weislow et al. 1989: it defines the assay and the 30% retest rule that gives the labels the word 'confirmed', not the CA/CM/CI criteria, so PROV-17 no longer applies; the boundary is visible in the source's released files instead (selectivity index separates CA from CM at ROC AUC 0.948 on the 387 actives with both values). Open for the curator in `REVIEW.md`: the target framing (three conclusions against the field's binary cut) and the retirement of `hiva_agnostic` (PROV-6). Priority 4: gap + (the collection's one multiclass molecule task), use case 0, source + (NCI DTP), shape + (41,133 compounds, 20,772 series), risk - (3.4% active; one feature column, so the score depends on the benchmark's encoding).
