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
- 'Samples: No Time Dimension'
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

CC (2026-11-11, Andrej): review marks on both issues; the state they ask for is the one this record already carries, so nothing changed beyond the review itself.

- Issue 1 (change, no note): the retirement stands. `suggestion: No (Retired)`, `v2_path` cleared, no folder in the working copy.
- Issue 2 (change, "Option C: Trivial."): `Trivial` is the marker, beside `Outdated`, `Not Representative`, `No Good Target (yet)` and `Selection Bias`. Its proof is the CC line of 2026-11-10: the unfitted textbook rule on the audiogram (air-bone gap or a tympanogram that is not type A, then abnormal air conduction or any pattern code) assigns 194 of the 195 cases, accuracy 0.995 against 0.968 for the best model, and the audiologist holds the audiogram when the type is assigned (TP-4, SEL-5).
- The review moved from the folder's `REVIEW.md` (the folder is gone; the file was still in the other working copy) into this record's `## Review` section.

## Review

**Outcome:** added; recommended `No (Retired)` (`Trivial`). The 195 cases of the audiology collection used to teach the
Protos expert system (UCI, 1987), with Lennart's target of 2026-10-06: the type of hearing loss (normal 19,
sensorineural 142, conductive or mixed 34). Reviewed without a panel, from the gathered evidence: the record, the
earlier checks of 2026-10-14 and model runs on the shipped BeyondArena data. The AI recommends retiring it,
as Andrej argued on 2026-10-14; the disagreement waits for Lennart. Validity: the type of hearing loss is defined by
the audiogram and the tympanogram, which are features read at the same visit; the five defining tests alone reach
accuracy 0.903 against 0.938 for all 65 features, and the case history alone, the only version with a decision before
testing, predicts nothing beyond the majority class (SEL-5, LEAK-4; issue 1). Value: no probe flag since the
redefinition, linear model log-loss skill +0.81, best single feature +0.45; on the earlier shipped target a
hand-written list of the textbook definitions beat all 40 benchmark methods (log loss 0.092 against 0.266). Quality: a
teaching collection with 19 normal ears (`Selection Bias`). Weighed: a traced source and a field convention against a
label that its own defining tests spell out.

**Main points:** Retired (2026-11-05); marker `Trivial` since 2026-11-10: an unfitted textbook rule on the audiogram beats every model (issue 2, resolved; PR #57).

**Record judgment:** valid source, circular label. The record holds both sides: Lennart's redefinition (CC
2026-10-06) and Andrej's objection (CC 2026-10-14). The suggestion is `Yes (Disagreement)` and the folder stays until
the two agree. The data-scouting run of 2026-10-31 screened `hbdc_audiogram_air_bone_gap` (AI-filled, unverified): it
predicts bone conduction and the air-bone gap from the air-conduction audiogram, a different task without this
circularity, and its data are on request only.

**Issues for Andrej:**

1. **Retire because the type of hearing loss is read off the tests that define it?**

   * **Problem:**
     - The target is the type of hearing loss (normal, sensorineural, or conductive or mixed), and audiology defines
       that type by the audiogram and the tympanogram, which are features of the same visit.
     - The five defining tests alone reach accuracy 0.903 against 0.938 for all 65 features, while the case history
       alone, the only version with a decision before testing, predicts nothing beyond the majority class.
     - Retire the dataset, or keep Lennart's redefinition of 2026-10-06?
   * **Background:** a gap between the air-conduction and the bone-conduction thresholds (the air-bone gap) means a
     conductive part, sound blocked in the outer or middle ear; raised thresholds without a gap mean a sensorineural
     loss of the inner ear or the nerve; the tympanogram measures how the eardrum moves and is abnormal with a
     middle-ear problem. These tests are the columns `airBoneGap`, `air`, `bone`, `boneAbnormal` and `tymp`. The
     source's 24 diagnoses cannot be the target: 16 have 4 or fewer cases, and the four large cochlear ones are
     spelled out by two history answers, age over 60 and noise exposure (139 of 147 cases)[^1b]. The three types are
     the field's standard grouping, which a target the definition builds needs[^1c].
   * **Effect on the task:** a model learns the textbook rule, which an audiologist who has the audiogram and the
     tympanogram applies directly. What the rule leaves over (46 sensorineural cases with `air` normal, 11 conductive
     or mixed cases without a gap) reads as coarse coding of a 1987 teaching set rather than signal.
   * **Experiments:**
     - Andrej's check (CC 2026-10-14; 5-fold logistic regression on the 195 cases; majority class 0.728): the five
       defining tests 0.903 accuracy (balanced 0.805), all 65 features 0.938 (0.850), the case history alone 0.728
       (0.355). `airBoneGap` = t is conductive or mixed in 23 of 23 cases, an abnormal `tymp` in 33 of 34, and a
       depth-3 tree on the defining tests learns the rule.
     - Lennart's probes on the rebuilt container (CC 2026-10-06): no flags; linear model log loss 0.14 against 0.76
       for the class shares (skill +0.81), the best single feature `tymp` +0.45, so no single column matches the
       model[^1d].
     - Model runs on the shipped BeyondArena data (the earlier target cochlear / normal / other, 199 rows,
       20 x 3 splits): a hand-written decision list of the textbook definitions (retrocochlear signs, then an air-bone
       gap with normal bone conduction, then a normal audiogram) scored log loss 0.092, against 0.266 for the best of
       40 benchmark methods and 0.283 for TabPFN 3.5; the same list learned per split as a small tree, 0.140. That is
       the earlier target, not the one v0.2 ships, but the pattern is the same: the label follows the tests.
   * **Curators:** Lennart (CC 2026-10-06): the grouping is the field's standard one, and any label of this data is
     partly read off its tests. Andrej (CC 2026-10-14): that is why no fair task is left.
   * **Consistency:** follows central_international_medical_college_and_hospital_health_risk_prediction (its label,
     the NEWS2 chart, computed from the vitals it ships: retired as `Trivial` on 2026-10-12). It differs from
     eryhemato_squamous_disease (kept 2026-10-20), where two classes follow one sign each but the label is the
     biopsy, an independent measurement taken after the signs. biomechanical_orthopaedic_prediction carries the same
     objection, also open.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the redefinition (implemented) | 195 cases, three types, all 65 findings; fit approximate | the field's standard grouping; the model beats the best single feature (+0.81 against +0.45) | five defining tests give 0.903 of the 0.938 accuracy; the rest looks like coding noise |
     | B | Retire | `No (Retired)` with `Trivial`; the folder leaves the working copy | no task whose signal is its label's definition | the only hearing-loss dataset leaves; overturns Lennart's redefinition |
     | C | The type from the case history only | the stage before testing: history answers as the only features | no circular feature | predicts nothing beyond the majority class (balanced accuracy 0.355) |

   * **Recommendation:** B: the label is read off five of its features, and the version without them carries no
     signal[^1a]; the call waits for Lennart's reply to the CC of 2026-10-14. **Decision:** keep (A), retire (B) or
     the history only (C)?

   **Notes for the AI:** on B, once Lennart agrees: `suggestion: No (Retired)`, marker `Trivial` (keep
   `No Good Target (yet)`), a dated CC line, the folder removed from the working copy with a CHANGELOG entry and
   `v2_path` cleared, as for the retirements of 2026-10-12. Until then do not remove the folder. On A:
   `suggestion: Yes`, remove `No Good Target (yet)`, and a CC line naming the reason. C is a new definition (the
   history columns only) and needs `dataset check` and the task probes.

   [^1a]: **SEL-5** (Must): a label the source computes with a published, deterministic rule from the columns: drop
     the rule's inputs when the rest still makes a real task; when the inputs are the whole task, it is `Trivial`.
   [^1b]: **LEAK-4** (Must): when a definition changes the target, check the shipped label with a depth-2 or depth-3
     tree on its defining columns, which shows whether the target is a rule. Cases: audiology_diagnosis.
   [^1c]: **TP-7** (Must): a target the definition builds uses an established convention of the field, and each
     candidate is tested for classes per fold, signal and how rule-like the label is. Cases: audiology_diagnosis.
   [^1d]: **TP-4** (Must): `Trivial` needs proof: the raw feature, chosen on each split's training side, has to match
     or beat the methods fold by fold.

   **Andrej (2026-11-05, change):** Retire and clearly articulate the reason.

   **Answer (AI, 2026-11-05):**

   * **Applied:** the record is `No (Retired)`, with a CC line giving the reasons: the type of hearing loss is read off
     five of its features (accuracy 0.903 of 0.938), and the case history alone, the stage before testing, gives only
     the majority class (0.728). `year` is 1987. The folder stays until this file is committed, as for the other
     retirements.
   * **Open, the marker:** option B named `Trivial`, which needs the fold-by-fold proof that one raw feature matches the
     methods[^a1]. On the target v0.2 ships the best single feature reaches skill +0.45 against +0.81 for a linear model,
     and the decision list that beat all 40 methods ran on the earlier target. Where the test failed or was never run,
     `Trivial` was removed (thyroid_discordant, 2026-10-22; heart_disease_switzerland, a `No` record, 2026-10-27).
     What sets audiology apart?

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | `Trivial` after the test | run the textbook decision list on the v0.2 splits fold by fold against the methods; add `Trivial` if it matches | the marker names the reason, with its proof | needs the benchmark's tuned results on the v0.2 target, which do not exist yet |
     | B | `No Good Target / Scientific Discovery` | add it for "no signal before testing, the definition after it"; drop `No Good Target (yet)`; keep `Outdated`, `Not Representative`, `Selection Bias` | every marker carries its proof; no test needed | the marker does not name the circular label (the CC line does) |
     | C | Amend the rule | a label the field defines from columns of the table is `Trivial` without the fold-by-fold test when the rest carries no signal | names the reason; covers biomechanical_orthopaedic_prediction too | a rule change for two cases |

   * **Recommendation:** B: the reason is written in the record, and a marker should not claim a test that did not run.
     **Decision:** A, B or C?

   [^a1]: **TP-4** (Must): `Trivial` needs proof: the raw feature, chosen on each split's training side, has to match
     or beat the methods fold by fold.

   **Resolved (2026-11-05, Andrej):** `No Good Target / Scientific Discovery` (option B), under the new rule that a label the field defines by measurements that ship as columns is no prediction target (SEL-19); `Trivial` is not why it retires. The record, the folder's removal and the rule are in PR #57.

   **Resolved (2026-11-11, Andrej):** his mark of today (change, no note) confirms the retirement, which is carried on
   this branch: `suggestion: No (Retired)`, `v2_path` cleared and no folder in the working copy. The marker that
   carries it is issue 2's.

2. **Which marker under your ladder for a label read off its defining columns: `No Good Target`, `No Signal` or `Trivial`?**

   * **Problem:**
     - An unfitted textbook rule on the audiogram assigns 194 of the 195 cases (accuracy 0.995), ahead of every model
       (best 0.968), and the audiologist has the audiogram when the type is assigned, so `Trivial` has its proof[^2b].
     - With the audiogram dropped, the 11 case-history answers keep a small real signal, but reassessed from scratch
       that task has no decision behind it, since the audiogram is the routine first test of any hearing complaint.
     - Which marker carries the retirement, or does the history-only task come back?
   * **Background:**
     - The ladder: drop the defining columns and test the rest; the rest useless is `No Signal`, too few features left
       is `No Good Target / Scientific Discovery`, the defining columns at hand at the decision with a simple rule giving
       the label is `Trivial`; when the rest still carries signal it is kept and the new task reassessed from scratch.
       It replaces PR #57's rule that the field's definition is not `Trivial`[^2c].
     - With the five defining tests removed, the other audiogram codes (`m_sn_gt_1k` and the like name the type) still
       give accuracy 0.84, so the audiogram as a whole is the defining measurement.
     - The case history beats the class shares (log loss 0.713 against 0.762) and 20 shuffled runs (p = 0), at the
       majority class in accuracy; PR #57, the record's CC line and the CHANGELOG say it "gives only the majority
       class", which holds for accuracy only.
     - The rule: conductive or mixed when there is an air-bone gap or the tympanogram is not type A; otherwise
       sensorineural when air conduction is abnormal or any of the audiogram's 40 pattern codes (`m_sn_gt_2k`,
       `notch_4k` and the like) is set; otherwise normal. Its one error is a sensorineural case called conductive.
     - The first version of the rule, without the pattern codes, reached 0.764 (balanced accuracy 0.892): it was right
       on all 34 conductive or mixed and all 19 normal ears, and called normal the 45 sensorineural ears whose coarse
       air-conduction code reads normal. Every one of those 45 has a pattern code set, and no normal ear has one.
   * **Experiments:** the 195 cases of v0.2, 5-fold x 5 repeats, best of logistic regression, random forest and gradient
     boosting (Slurm job 1374813; the rules, `rule_check.py`):

     | Features | Accuracy | Balanced accuracy | Log loss |
     |---|---|---|---|
     | All 61 | 0.968 | 0.957 | 0.111 |
     | Audiogram codes only (50) | 0.966 | 0.966 | 0.114 |
     | The five defining tests | 0.907 | 0.834 | 0.208 |
     | All but those five | 0.839 | 0.678 | 0.444 |
     | Case history only (11) | 0.739 | 0.376 | 0.713 |
     | Case history, shuffled labels (best of 20) | | | 0.759 |
     | Class shares | 0.728 | 0.333 | 0.762 |
     | Textbook rule, gap and tympanogram, then air conduction (no fitting) | 0.764 | 0.892 | |
     | Textbook rule, gap and tympanogram, then air conduction or any pattern code (no fitting) | 0.995 | 0.998 | |

   * **Effect on the task:** none on the retirement; the marker and the CC line change.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | `No Good Target / Scientific Discovery` (implemented), new reason | CC line: with the audiogram dropped, 11 history answers remain, too few to carry the type of hearing loss; "majority class" corrected to the small signal | the reassessed history task has no decision | does not name what the rule shows: the shipped label is a lookup on the audiogram |
     | B | `No Signal` | marker swapped | names that nothing usable is left | the history beats both the class shares and shuffled labels, so the marker's own test fails |
     | C | `Trivial` | marker swapped for `No Good Target`; CC line: the unfitted rule assigns 194 of 195 cases, ahead of every model; the history task, reassessed, has no decision | the ladder's branch for inputs at hand at the decision, with its proof | the rule reads 45 columns, though only as "any pattern code set" |
     | D | History-only task | un-retire: the 195 cases, the 11 history answers, the same three types | no defining column; a real if small signal | accuracy at the majority class; no decision is taken on the history before the audiogram |

   * **Recommendation:** C: an unfitted rule on the audiogram, which the audiologist holds when assigning the type,
     beats every model; the history-only task, reassessed from scratch, has no decision, so it does not come back[^2b].
     **Decision:** A, B, C or D?

   **Notes for the AI:** on D, revert the retirement in PR #57 and drop the 50 audiogram codes in `_clean`; on A to C, in PR #57 (on C, `Trivial` replaces `No Good Target / Scientific Discovery` with
   the rule and its 0.995 in the CC line): the record's CC line and the CHANGELOG entry say the history shows a
   small signal (log loss 0.713 against 0.762) instead of "the majority class"; the case rows in `selection.md`,
   `leak_checks.md` and `task_probes.md` the same; the rule text is the ladder, folded into the deterministic-rule rule
   (Andrej, 2026-11-10). Evidence:
   `~/claude_jobs/sel19_reassess/` (`run.py`, `results.json`, job 1374813; `rule_check.py`).

   [^2b]: **TP-2** (Should): a real signal beats shuffled labels on the split the use case needs; `No Signal` when the
     methods stay within them. **TP-4** (Must): `Trivial` needs proof that one raw feature or a simple rule matches the
     methods fold by fold.
   [^2c]: **SEL-19** (Must, PR #57, to be folded into **SEL-5**): a label the field defines by measurements that ship as
     columns is no prediction target; marker `No Good Target / Scientific Discovery`, not `Trivial`.

   **Resolved (2026-11-10, Andrej):** `Trivial` (option C), in chat: if nothing learnable from the data beats a textbook rule not fitted on it, the data cannot be used for prediction. In PR #57 (commit 43a0aee9): the marker and a CC line in the record, TP-4 and SEL-5 amended, the case rows and the CHANGELOG; the history wording corrected.

   **Andrej (2026-11-11, change):** Option C: Trivial.

   **Resolved (2026-11-11, Andrej):** C, confirmed and already carried by this branch: `decision_markers` hold
   `Trivial` beside `Outdated`, `Not Representative`, `No Good Target (yet)` and `Selection Bias`, and the record's CC
   line of 2026-11-10 gives the proof (the unfitted textbook rule on the audiogram assigns 194 of 195 cases, accuracy
   0.995, against 0.968 for the best model; the history-only task, reassessed, has no decision behind it). Nothing
   further to apply here; the folder is gone and the review now lives in this record.

## Reference

@incollection{bareiss1990protos,
  title={Protos: An exemplar-based learning apprentice},
  author={Bareiss, E Ray and Porter, Bruce W and Wier, Craig C},
  booktitle={Machine learning},
  pages={112--127},
  year={1990},
  publisher={Elsevier}
}
