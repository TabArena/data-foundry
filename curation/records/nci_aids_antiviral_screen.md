---
unique_name: nci_aids_antiviral_screen
name: NCI DTP AIDS Antiviral Screen data (aids_conc_may04, with the AIDO99SD structure file)
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 4
tags:
- Non-IID (Grouped)
collections:
- ChemPile
original_source: GOV Website
year: '2004'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://wiki.nci.nih.gov/display/NCIDTPdata/AIDS+Antiviral+Screen+Data
- https://dtp.cancer.gov/databases_tools/bulk_data.htm
- '# MoleculeNet HIV, a processed copy (41,127 compounds, binary), Wu et al. 2018'
- https://doi.org/10.1039/C7SC02664A
v2_path: datasets/_dev/tabarena-v0pt2/nci_aids_antiviral_screen/dataset.py
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

CC (2026-11-02, Lennart): "Make it binary following the default usage of the field" (review page, issue 1). The
screen's confirmed active and confirmed moderately active merge into one active class against confirmed inactive,
the target the 2007 HIVA challenge, MoleculeNet, OGB's `ogbg-molhiv` and ChemPile all define on this file, and the
metric follows it from the `log_loss` fallback to `roc_auc` (MET-4). CLEAN-17 permits the merge because the
convention is established and the merge is tested; the Cases row is in `cleaning_features.md`.

CC (2026-11-02, Lennart): "Yes retire it as described" (review page, issue 2): `hiva_agnostic` retires as a
duplicate of this release (PROV-6).

**Assessment (AI, 2026-11-02):** applied. 41,140 compounds, 1,404 active (3.4%), target `active_in_screen` (Yes/No,
Yes the event), `roc_auc` from the context; the ordered typing of the three conclusions is gone (CLEAN-25: a binary
target is not ordered). The merge keeps 7 compounds the three-class framing dropped as conflicting (concluded CA
under one NSC number and CM under another), so the LEAK-20 conflict set falls from 46 compounds / 119 rows to 39 /
104. The potency scale the two active classes form stays in decision table 2, with the selectivity-index
measurement. `dataset check` clean (0 errors, 0 warnings, 27 checks); the scaffold groups, the close-analog shares
and the NSC-batch numbers were re-measured on the new frame and the definition's prose now quotes those. Two things
for you: the record still reads `suggestion: TBD -> Yes` and `WIP (Triage)` because you left the verdict box empty
on the review page, and the priority rationale's gap clause ("the collection's one multiclass molecule task") no
longer holds, so priority 4 may want a second look — `international_stroke_trial_outcome` is the other open
multiclass-against-binary framing, flagged 2026-10-31.

CC (2026-11-02, Lennart): issue 4 as implemented (review page): the charge code read as +1 stands (PROV-13; our
structures differ from MoleculeNet's and OGB's on the 690 repaired compounds, a problem of that copy, PROV-15), and
the NSC submission-batch dependency stays disclosed in `splits_comment` rather than split away (SPLIT-30).

**Assessment (AI, 2026-11-02):** the declared metric was marked "as declared" on the page while it was still the
`log_loss` fallback of the three-class target; issue 1 replaced it with `roc_auc`, so the mark is read as a check of
the old declaration and the new one waits for the curator's confirmation in issue 1. Probes on the merged target
(task, leak; 5 and 3 splits): no flag; random forest ROC AUC 0.817, LightGBM 0.806, the best single feature 0.641;
grouping the NSC batches away as well moves ROC AUC from 0.802 to 0.800 (fold spread 0.012 to 0.025).

CC (2026-11-02, Lennart): on the fit (review page, issue 3): "it might be direct with the binary task now?"

**Assessment (AI, 2026-11-02):** it is, and more plainly than before. The critic's case for `approximate` rested on
one fact, that the CA/CM boundary is nowhere published (USE-8, the `differentiated_thyroid_cancer_recurrence`
precedent). Merging CA and CM takes that boundary out of the label, so the argument has nothing left to apply to.
What the binary label rests on is the active against inactive line, and that one is published: Weislow et al. 1989
gives the operational rule ("If a test substance shows at least 30% protection against virus-induced cytopathic
effects in the host cells, the microculture XTT antiviral assay is repeated"), which is where the word "confirmed"
comes from, and the source's own files show the line is sharp, with only 83 of 42,038 inactive compounds (0.2%) ever
reaching an EC50 against 84.6% of CA and 40.7% of CM. So `fit="direct"` now holds on a published definition alone;
the mediator's selectivity-index measurement stays in the notes as evidence about the three-class framing, not as the
support for the fit. `qsar_oral_toxicity` stays distinguished: there an external set of untested chemicals exists and
shows the test rows are closer to training than the chemicals a screener meets, and here no such set exists. The
analog share is not what separates them (oral is approximate at 16.3%, this is direct at 15.5%); the external set is.
`fit_reason` is unchanged, since it never rested on CA/CM.

CC (2026-11-02, Lennart): `ship` on the review page of 2026-11-02, with the declared metric marked as declared. The
dataset is accepted as the definition now stands: the binary `active_in_screen` of the curator's mark of the same
day, scored with `roc_auc`, on splits grouped by Bemis-Murcko scaffold. This is also the curator's verification of
the AI screening of 2026-10-31, which had never been through the screening queue: `TBD -> Yes` becomes `Yes` and
`AI (UNVERIFIED)` gives way to the curator's name. The claim stays until the work reaches `main`.

**Assessment (AI, 2026-11-02):** this closes issue 1 of the review page, which asked for the metric to be confirmed
once the target changed. The page keeps one timestamp per record and none per mark, so it does not say whether the
metric was marked again in this round or the mark carried over from the first; what it does say is that the `ship`
verdict was given on a page that declared `roc_auc` with origin `context`, and the confirmation is read from the
verdict. Say so if that is wrong and the metric should go back to `log_loss`.

`roc_auc` is declared from the context, not from the source (MET-4 by analogy; the DTP page names no metric at all).
It is what MoleculeNet, OGB's `ogbg-molhiv` and ChemPile score on this label, and what a screening team reads, since
the model ranks compounds for the next plate; it is unmoved by the 3.4% base rate, where the 2007 HIVA challenge's
balanced error rate would need a threshold none of them fixes. The caveat that travels with it is in the metric's own
reason: reading the source's charge code as the +1 it means leaves our structures different from MoleculeNet's, and
OGB's built on it, on 690 compounds, so a score here is close to but not literally the `ogbg-molhiv` leaderboard's.
This is the collection's first `Metric.from_context` on a classification task; the fourteen before it are all RMSLE
on a price. For a binary target `roc_auc` is also the plain fallback (MET-8), so nothing hangs on the origin except
that the reason records the three benchmarks that score this label, which is why it is declared that way. With the
verdict the last open issue closes and the folder's `REVIEW.md` goes; the review panel's reports stay in the run
folder of 2026-11-01, and what they settled is in the definition's `curation_comments` and in the assessments above.
The practitioner's second caveat, that the library is the compounds the DTP held by 1999 and a prospective hit rate
on a modern deck would be lower, moved into `curation_comments` rather than going with the file.

**Assessment (AI, 2026-11-02):** `priority` stays at 4, but the reason it rested on is gone. It read partly on this
being the collection's one multiclass molecule task, and the binary target removes that gap: `priority_factors.py`
now measures the thin values among the 98 accepted definitions as the domains education, insurance and physics &
astronomy, the problem type multiclass and the regime none, so chemistry, binary and grouped are all common. On
selection.md's arithmetic the factor line is now gap -, use case 0, source +, shape +, risk - (the duplicate is
retired and the panel recommends ship), which gives 2 or 3; the screening of 2026-10-31 wrote 3 and `/add-dataset`
wrote 4 on 2026-11-01, so the number already sat a step above its line before the merge. No record's priority has
been revisited at a review ship (sarcoma, 2026-10-22, changed its problem type and kept 3), so the number is left
for the curator. `international_stroke_trial_outcome`, the other open multiclass-against-binary framing (flagged
2026-10-31), is the sibling to decide the same way.

CC (2026-11-02, Lennart): on the priority after the binary merge removed the multiclass gap it partly rested on:
"4 is ok". It stays at 4; the corrected factor line is in the assessment above.
