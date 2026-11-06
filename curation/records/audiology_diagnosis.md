---
unique_name: audiology_diagnosis
name: Audiology
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: No (Retired)
decision_markers:
- Outdated
- Not Representative
- No Good Target (yet)
- Selection Bias
- Trivial
tags:
- Tiny Data
- Case Series
collections:
- New (BeyondArena)
- TabSTAR
original_source: UCI
year: '1987'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://archive.ics.uci.edu/dataset/8/audiology+standardized
- https://doi.org/10.24432/C5TP4R
notebook_path: datasets/beyond_iid/new_iid/audiology_diagnosis/audiology_diagnosis.ipynb
source_row: 764
type_adapter_id: curation-record-v1
---

## Comments

Feel like this is a duplicate, but I cannot find it.

Otherwise, many classes and need to check there is enough samples per class for a task, otherwise remove some

Need to check if some rules/cases come from the system in the paper or from the database

Discussion: Not a meaningful predictive task. The available data sample is highly selective and not representative. The target is to predict what kind of ear disease a person has, if any, but there are only 9% normal samples which is unrealistic in a diagnostic task. The reason is that this is a curated teaching/research case library for a case-based-reasoning system, not a consecutive clinic sample

CC (Andrej): The first target (cochlear / normal / other, 24 diagnoses collapsed to 3) was internally incoherent: `other` fused the conductive diagnoses (`airBoneGap = t`) with the retrocochlear and central ones (`airBoneGap = f`), and `bser`, the one finding that could separate the latter, was 98.5% missing. Superseded by the redefinition below.

CC (2026-10-06, Lennart): Re-defined the target after the task-probe review (flags `no_spread`, `unstable`). The 3-class merge (cochlear / normal / other) was our own, made from the diagnosis names: it put the 24 mixed losses under cochlear and lumped conductive with retrocochlear and central disorders under other. The 24 original diagnoses cannot be the target (16 have 4 or fewer cases), and dropping the rare ones does not help: the four large cochlear diagnoses are spelled out by two history findings (age_gt_60, history_noise: 139 of 147 cases). The source defines no grouping. The new target is the standard distinction between a hearing loss with and without a conductive part: normal 19, sensorineural 142, conductive_or_mixed 34 (195 cases). Duplicated cases (27) stay dropped, bells_palsy and the central diagnoses (possible_brainstem_disorder, poss_central) are dropped as not a type of hearing loss; the four types with conductive and mixed apart would leave 10 conductive cases, 3-4 per test fold. Probes on the rebuilt container: no flags; the linear model reaches log-loss skill +0.81 (log loss 0.14 against 0.76 for the class shares), the strongest single feature (`tymp`) +0.45. The label is partly read off its defining tests (a depth-3 tree reaches about 91% against 73% for the majority class), as any label of this data is.

CC (2026-10-14, Andrej): Disagreement: I think the redefined target is circular (verify-dataset rubric item 6). The type of hearing loss is defined by the audiogram and tympanogram (air-bone gap, air and bone conduction), and those tests are features. On the 195 cases (5-fold logistic regression, majority class 0.728): the five defining tests alone (`airBoneGap`, `air`, `bone`, `boneAbnormal`, `tymp`) reach accuracy 0.903 / balanced 0.805, all 65 features 0.938 / 0.850; `airBoneGap = t` is conductive_or_mixed in 23 of 23 cases, an abnormal `tymp` in 33 of 34, and a depth-3 tree on the defining tests learns the textbook rule. The only version with a decision behind it, the type before testing from the case history, carries no signal (accuracy 0.728, balanced 0.355: the majority class). What the defining tests leave over (46 sensorineural cases with `air = normal`, 11 conductive or mixed without a gap) reads as coarse coding of a 1987 teaching set, not signal a model should learn. As the CC above says, any label of this data is read off its defining tests, so no fair task is left; together with the case-library sample (19 normal ears, see Discussion), I would retire the dataset (No (Retired)).

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback log_loss — UCI page defines no metric; Protos reported classification accuracy on the 24 original diagnoses, a different target from our 3 grouped types, so no metric is defined for the shipped task.

**Assessment (AI, 2026-10-27):** The open questions for the curator are in the folder's `REVIEW.md` (review of the Tiny Data datasets, written from the earlier findings, no review panel); the AI recommends not to ship it. Priority 2: gap +, use case - (the only version with a decision behind it carries no signal), source +, shape -, risk - (the label is read off its five defining tests; recommended not to ship).
**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 6 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `air`, `ar_c`, `ar_u`, `bone`, `o_ar_c`, `o_ar_u` (the README lists their levels); their codes that mean unknown (don't know, refused, not asked) are missing in `bone` (CLEAN-10); left unordered: `speech` (a partial order).

CC (2026-11-01, Lennart): marks on the review board of PR #37: speech stays unordered (where normal sits is not documented), noted in the definition.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `hbdc_audiogram_air_bone_gap` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the folder's `REVIEW.md`. Retire: the shipped type of hearing loss is read off its five defining tests (accuracy 0.903 of 0.938), and the version before testing, from the case history, predicts nothing beyond the majority class; the disagreement waits for Lennart. Priority 2: gap 1, use case 0, source 1, shape 0, risk -1.

CC (2026-11-05, Andrej): retired (`No (Retired)`, `No Good Target / Scientific Discovery`): the type of hearing loss we ship is read off the tests that define it, and without those tests nothing is left to predict. The data is the teaching collection of the Protos expert system (195 cases, 1987); the target is Lennart's redefinition of 2026-10-06: normal, sensorineural, or conductive or mixed.
- **The label is the definition of five of its features:** audiology defines the type of loss by the audiogram (hearing thresholds by air and by bone conduction; a gap between them means a conductive part) and the tympanogram (how the eardrum moves). These tests are columns (`airBoneGap`, `air`, `bone`, `boneAbnormal`, `tymp`): alone they reach accuracy 0.903 against 0.938 with all 65 features (5-fold logistic regression, majority class 0.728); `airBoneGap` = t is conductive or mixed in 23 of 23 cases, an abnormal `tymp` in 33 of 34.
- **Before the tests there is no signal:** the case history alone, the only point where a prediction could guide which test to run, gives 0.728, the majority class (balanced accuracy 0.355).
- **Why Lennart's keep does not hold:** the three types are the field's standard grouping, but a grouping defined by columns of the same table is a lookup, not a prediction; what the textbook rule leaves over (46 sensorineural cases with a normal air-conduction code, 11 conductive or mixed cases without a gap) reads as the coarse coding of a teaching set.
Marker `No Good Target / Scientific Discovery` added: a label read off the tests that define it is no real prediction target; `Trivial` is not the reason for retiring it. `year` set to 1987, the collection's date, from the definition.

CC (2026-11-10, Andrej): marker changed to `Trivial`: a textbook rule, not fitted on these data, beats every model, so nothing learnable is left beyond what the field already writes down.
- **The rule:** conductive or mixed when there is an air-bone gap or the tympanogram is not type A; otherwise sensorineural when air conduction is abnormal or any of the audiogram's 40 pattern codes (`m_sn_gt_2k`, `notch_4k` and the like) is set; otherwise normal. It assigns 194 of 195 cases (accuracy 0.995, balanced 0.998), against 0.968 for the best of logistic regression, random forest and gradient boosting (5-fold x 5 repeats).
- **How it came about:** read on air conduction alone the rule reached 0.764: the coarse air-conduction code reads normal for 45 sensorineural ears whose high-frequency losses sit in the pattern codes, which name the type themselves; no normal ear has one set.
- **What is left without the audiogram:** the 11 case-history answers keep a small signal (log loss 0.713 against 0.762 for the class shares, outside 20 shuffled runs), so "the majority class" above holds for accuracy only; reassessed as a task of its own it has no decision, as the audiogram is the routine first test of a hearing complaint.
Marker `No Good Target / Scientific Discovery` removed. Evidence: Slurm jobs 1374813 and the rule check of 2026-11-10.

## Reference

@incollection{bareiss1990protos,
  title={Protos: An exemplar-based learning apprentice},
  author={Bareiss, E Ray and Porter, Bruce W and Wier, Craig C},
  booktitle={Machine learning},
  pages={112--127},
  year={1990},
  publisher={Elsevier}
}
