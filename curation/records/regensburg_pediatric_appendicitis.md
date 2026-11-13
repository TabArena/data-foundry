---
unique_name: regensburg_pediatric_appendicitis
name: Regensburg Pediatric Appendicitis
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
- WIP (Triage)
claimed_by: Andrej
suggestion: No (Retired)
decision_markers:
- Class-dependent Recording
- No Good Target / Scientific Discovery
tags:
- Tiny Data
collections:
- New (BeyondArena)
- TabSTAR
original_source: Other
year: '2023'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.5281/zenodo.7711412
- https://archive.ics.uci.edu/dataset/938/regensburg+pediatric+appendicitis
- (https://www.openml.org/search?type=data&id=46603&sort=runs&status=active)
notebook_path: datasets/beyond_iid/new_iid/regensburg_pediatric_appendicitis/regensburg_pediatric_appendicitis.ipynb
source_row: 746
type_adapter_id: curation-record-v1
---

## Comments

Has three target variables as it seems, we likely want to use Diagnosis

The data was collected over a time horizon, but no timestamp is given. Moreover, the task does not seem to have temporal leakage given that it is across different patients in a few years (such that evolution could have had the chance to change the distribution...)

Great case of a dataset where there is a vision model and a tabular baseline (RF). Sadly, the paper does not do a good job of benchmarking the tabular models better, which might even become competitive. And the AUROCs for RF is even hidden in Table 3? I think we should include this dataset to show them how to benchmark predictive models correctly. At the same time, it is clear that for the other use cases, RF might not help

**Assessment (AI, 2026-10-14):** The data first appeared on Zenodo (Regensburg Pediatric Appendicitis Dataset v1.0, 2023-02-23, concept DOI 10.5281/zenodo.7669214; the definition downloads v1.03, 10.5281/zenodo.7711412), five days before the paper's preprint (arXiv 2302.14460). UCI 938 is a later copy whose metadata names the Zenodo DOI as its source, so the original source is Other, as in the definition. The old UCI link carried the wrong slug (`toxicity`); id 938 is this dataset.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Marcinkevics et al. 2024 report AUROC and AUPR side by side per target; neither is named as the criterion. roc_auc is the binary fallback.

CC (2026-10-27, Andrej): Keep, with one change to the data in `dataset.py` (not built). 763 children with suspected appendicitis who had an ultrasound at the Regensburg children's hospital (2016-2021); the task asks whether the appendicitis is complicated (gangrenous, perforated or abscessed: 115 children). ROC AUC (3-fold x 10): TabPFN 3.5 0.939, random forest 0.925, logistic regression 0.916.

**Changes made:**
1. **Problem:** the number format of BMI marked surgery, and through it the label, since complicated appendicitis is only found at surgery. From 2019 on BMI was typed with two decimals for 108 of 136 operated children and for 6 of 234 treated without surgery. BMI alone gives 0.56, with its format 0.76. The neutrophil share (neutrophils as % of white blood cells) is a whole number for 30% of complicated cases against 15% of the others. **Change:** BMI written to one decimal, the neutrophil share in whole percent. The number format of all columns alone drops from 0.77 to 0.58 (the rest is which cells are missing, below). The models score the same before and after: they did not use the cue.
2. **Problem:** the task description did not say how the label is set. **Change:** it says that the label comes from the tissue examination after surgery, that children treated without surgery count as uncomplicated when they did not come back, and that the label follows this hospital's practice of operating on few children (37%).
3. **Problem:** the curation comments warned, without a check, that some features might leak the severity. **Change:** the warning is replaced by the check: the ultrasound signs of perforation and abscess do not carry the score (TabPFN 3.5 0.935 without them, 0.939 with them). The comments also list the problems below.
4. Record: Andrej added as reviewer (`checked_by`).

**Problems found, not changed:**
- The label depends on the treatment: complicated cases are found only among the 284 operated children (115), none among the 479 treated without surgery, and the surgeon's decision alone ranks the label at 0.87. Kept: children treated without surgery who did not come back recovered without it, which complicated appendicitis rarely does, and the 21 who came back were operated and graded (3 complicated). So the label holds, and predicting it mirrors the real choice between operating and watching. Among operated children alone the task is harder (ROC AUC 0.78-0.81), an option if the full cohort is rejected.
- Lennart's reason to include it, that the paper does not benchmark tabular models properly, does not hold: the same group compared logistic regression, random forests and gradient boosting on 430 of these children (Marcinkevics et al. 2021) and tested them at a second hospital (Marcinkevičs, Sokol et al. 2025: severity ROC AUC 0.90 at Regensburg, 0.75 at Düsseldorf).
- Missing values follow the class (ultrasound findings filled in mostly when the report describes them; the two appendicitis scores missing for 12% of complicated cases against 4% of the others; missing values alone 0.82): they are on the record at the decision.
- Single-cell entry errors (age 0 at 164 cm, 26.9 °C, red cell count 14, haemoglobin 36 g/dL, three RDW values of 79-87%, 23.7 kg at 174 cm): they do not tell the classes apart.
- The Düsseldorf cohort (301 children, CC BY-NC 4.0) is public with the 2025 paper's code: a candidate for a separate hospital-transfer task once its columns and label definition are aligned.

References: Marcinkevics R, Reis Wolfertstetter P, Wellmann S, Knorr C, Vogt JE. Using machine learning to predict the diagnosis, management and severity of pediatric appendicitis. Front Pediatr. 2021;9:662183. doi:10.3389/fped.2021.662183. Marcinkevičs R, Sokol K, Paulraj A, Hilbert MA, Rimili V, Wellmann S, Knorr C, Reingruber B, Vogt JE, Reis Wolfertstetter P. External validation of predictive models for diagnosis, management and severity of pediatric appendicitis. Front Pediatr. 2025;13:1587488. doi:10.3389/fped.2025.1587488.

**Assessment (AI, 2026-10-27):** The open questions for the curator are in the record's Review (review of the Tiny Data datasets, written from the earlier findings, no review panel); the AI recommends shipping it. Priority 3: gap -, use case + (the source papers name the choice of surgery), source +, shape -, risk + (the format leak is fixed).
**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 7 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `Ketones_in_Urine`, `RBC_in_Urine`, `WBC_in_Urine`, `Peritonitis`, `Appendicolith`, `Perforation`, `Appendicular_Abscess` (the README lists their levels); left unordered: `Appendix_Wall_Layers` (low confidence); `Perfusion` (low confidence).

CC (2026-10-31, Lennart): marks on the review board of PR #37: Appendix_Wall_Layers ordered intact < partially raised < raised (the German record of the 2021 release; upset, 1 child, missing) and Perfusion ordered by blood flow no < hypoperfused < present < hyperperfused; a blank Perfusion also means unremarkable in this file (noted).

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found a related task: `pecarn_pediatric_head_trauma_citbi` (TBD -> Yes, priority 4). Each is screened in its own record; this record's verdict stays the curator's.

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship as defined: kept on review with BMI and the neutrophil share at measured precision (issue 1 resolved 2026-10-27); nothing open. Priority 2: gap 0, use case 0, source 1, shape 0, risk -0.

CC (2026-11-06, Andrej): retired (`No (Retired)`, `No Good Target / Scientific Discovery` beside `Class-dependent Recording`): the label is largely the surgeon's decision to operate, and the versions that remove that decision still carry the hospital's practice. The data: 763 children with suspected appendicitis and an ultrasound at the Regensburg children's hospital, 2016-2021, and whether the appendicitis was complicated (115).
- **What the label is:** a complicated appendicitis is found only at surgery, and the 479 children not operated (63%) count as uncomplicated without any tissue examination. A model trained only to predict whether the surgeon operated, which never sees the label, ranks it at ROC AUC 0.904 against 0.938 for the model trained on it; 74% of the pairs behind that score set a complicated child against one who was not operated.
- **What was tried, and what remained:**
  - 2026-10-27: BMI and the neutrophil share written at one precision, since the number format marked operated children (format-only probe 0.768 to 0.585); the label was left as it was.
  - Dropping the ultrasound signs and the clinical scores that decide surgery: still 0.924.
  - Children with appendicitis only (451): 170 children are still labelled by the decision not to operate (0.896).
  - Operated children only (284, every label from the tissue examination; 0.815, inside the 0.77-0.91 published studies report): who is operated still follows the surgeon's practice, and that practice moved within the file (32% of operated children complicated in 2016-2018, 51% later, with the share operated unchanged); the age's number format, which marks the period, still separates the classes among them (0.60), and missing values and number formats each reach 0.614. At Düsseldorf, the same group's hospital that operates 81% of its children, the same models reach 0.71 to 0.77.
- **Not changed:** `Selection Bias` was considered for the operated-only version and not added, since that version does not ship.
To do: the v2 folder leaves the working copy once its Review is committed.

## Review

**Outcome:** added. All 763 children with suspected appendicitis who had an ultrasound at the Regensburg children's
hospital (2016-2021), and whether the appendicitis was complicated (115). Reviewed without a panel, from the gathered
evidence: the record, the earlier checks of 2026-10-27 and model runs on the shipped BeyondArena data. Kept with fixes
on Andrej's review of 2026-10-27 (issue 1, resolved); the AI recommended shipping it as defined, and since Andrej's
question of 2026-11-05 recommends operated children only, the label then a tissue examination (issue 2, answer).
Validity: whether a child's appendicitis is complicated, predicted from symptoms, blood tests, scores and the
ultrasound; the label follows the treatment (complicated is only found at surgery), but children treated without surgery
are labelled by follow-up, so the label holds (USE-1); the number format that marked surgery is removed (LEAK-13). Model
runs flagged the ultrasound signs of perforation and abscess as overlapping the label's definition; the review had
measured that they do not carry the score (0.935 without them, 0.939 with them). Value: TabPFN 3.5 0.939, random forest
0.925, logistic regression 0.916 ROC AUC; on the shipped splits the 40 benchmark methods range from 0.853 to 0.935 (1 -
ROC AUC 0.147 to 0.065), TabPFN 3.5 first. Quality: class-linked missing values and single-cell entry errors kept with
notes (`Class-dependent Recording`). Weighed: a documented hospital cohort with a real surgical decision against a label
shaped by one hospital's practice.

**Main points:** Retired (2026-11-06, issue 2): the label is largely the decision to operate.

**Record judgment:** valid after repair, settled by CC 2026-10-27 (Andrej: keep, BMI and neutrophil share at
measured precision, the label's origin in the texts); the ordinal scales of PR #37 follow Lennart's marks of
2026-10-31.

**Issues for Andrej:**

1. **Ship in TabArena v0.2 as defined?**
   - Checked and settled (CC 2026-10-27, Andrej): from 2019 on BMI was typed with two decimals for 108 of 136
     operated children and 6 of 234 treated without surgery, so its format marked the label; BMI is now written to
     one decimal and the neutrophil share in whole percent, which takes the number format alone from 0.77 to 0.58
     while the models score the same. The texts say how the label is set and that it follows this hospital's
     practice (37% operated). The ultrasound signs of perforation and abscess do not carry the score (0.935 without
     them, 0.939 with them).
   - Kept on purpose: the label's dependence on treatment (the surgeon's decision alone ranks it at 0.87; the 21
     children who came back after treatment without surgery were operated and graded); missing values that follow
     the class (missing values alone 0.82), since they are on the record at the decision; single-cell entry errors
     that do not tell the classes apart.
   - Implemented: the definition as changed on 2026-10-27; 763 children, 115 complicated.
   - (a) Ship. (b) Restrict the task to operated children (284, ROC AUC 0.78 to 0.81), the alternative the review
     named if the full cohort were rejected. (c) Discuss.
   - Rule: the rule that class-specific recording conventions are harmonised (LEAK-13, Must); a use case is an
     actor, a moment and a decision (USE-1, Must): here the choice between operating and watching.
   - Precedent: gallstone_disease, kept 2026-10-21 with the same kind of format fix.
   - Recommendation: (a). Decision needed: (a), (b) or (c).

   **Resolved (2026-10-27, Andrej):** kept with the full cohort (a): BMI to one decimal and the neutrophil share in
   whole percent, the label's origin and the hospital's practice in the texts (CC 2026-10-27). The ordinal scales
   followed on 2026-10-31 (CC, Lennart). Nothing found since reopens it.

2. **Ship as defined?**

   * **Problem:**
     - Nothing open was found: the review of 2026-10-27 removed the number format that marked surgery, and the
       evidence since (model runs, whose leak flag the review had already measured) raises no new question.
   * **Experiments:** TabPFN 3.5 ROC AUC 0.939, random forest 0.925, logistic regression 0.916 (3-fold x 10); on the
     shipped splits the 40 benchmark methods range from 0.853 to 0.935; the number format alone 0.58 after the fix, most
     of it from which cells are missing, which is on the record at the decision.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Ship as defined (implemented) | 763 children, complicated appendicitis | a documented cohort and a real surgical decision | the label follows one hospital's practice |
     | B | Retire | `No (Retired)`; the folder leaves the working copy | none found | a real, repaired task leaves |

   * **Recommendation:** A. **Decision:** ship (A) or retire (B)?

   **Andrej (2026-11-05, discuss):** I am not sure whether we actually repaired the task. Performance still seems
   unrealistically good and that the label follows hospital practice is an exclusion criterion.. Go digging.

   **Answer (AI, 2026-11-05):**

   * **Problem:**
     - Not repaired: a model trained only to predict whether the surgeon operated, which never sees the complication
       label, ranks that label at ROC AUC 0.904 (TabPFN 3.5; logistic regression 0.911), against 0.938 for the model
       trained on it, because a complicated case is found only at surgery and the decision to operate follows the
       recorded features closely (the operation itself is predicted at 0.975).
     - The fix of 2026-10-27 removed a number format and left the label as it was: 479 of the 763 children (63%) count
       as uncomplicated because they were not operated and did not come back, without any tissue examination, which
       makes the label "operated, and complicated in the tissue"[^a1].
     - Among the 284 operated children, where every label is the tissue examination, the same features reach 0.815
       (TabPFN 3.5), inside the 0.77 to 0.91 that published studies report for this question; the step from there to
       0.938 is the surgeon's decision inside the label, which no column drop removes (no ultrasound and no scores:
       still 0.924).
   * **How the label is set:**
     - The source: "Appendicitis was classified as 'uncomplicated' in all conservatively treated cases. The
       'uncomplicated' category also included patients without appendicitis since none had complications during
       treatment" (2021); "Patients treated non-operatively, both with and without appendicitis, with no recurrence
       during the follow-up period were classified as uncomplicated. For patients treated operatively, classification
       was based on the histology" (2025).
     - Who is operated "reflects the decision made by a senior pediatric surgeon based on clinical, laboratory and US
       data" (2024); children "with criteria for simple appendicitis presenting clinical and sonographic improvement"
       stayed without surgery, "otherwise they underwent operation" (2021).
     - In the file: 284 operated, graded by histology (115 complicated, 169 not; 21 of them operated after coming
       back, 3 complicated); 479 not operated, all uncomplicated (170 called appendicitis by a rule on the scores and
       the appendix diameter, 309 without appendicitis).
   * **Effect on the task:** the definition's use case is the choice between surgery and watching, and for the
     children who were watched the label is that choice: a model is scored on agreeing with the surgeon, and a
     complicated appendicitis sent home would count as a correct "uncomplicated" unless the child came back; how
     many of the 479 that is cannot be checked (no tissue, and in 2021 61 of 86 children with appendicitis treated
     without surgery were reached for follow-up).
   * **Experiments** (TabPFN 3.5 unless named, 3-fold x 10 on the shipped data; feature groups 3-fold x 5; single
     findings, missing values and number formats with a small boosted-tree model, 3-fold x 5):
     - ROC AUC compares each complicated child with each other child: 74% of those pairs (479 of 648 partners) are a
       child the surgeon did not operate, ranked at 0.98 (0.986 against the 309 without appendicitis, 0.978 against
       the 170 treated without surgery); against the 169 operated uncomplicated children it is 0.811.
     - The surgery model ranks complicated above operated uncomplicated children at only 0.669: its 0.904 on the label
       is the operation. Chaining two models, the chance of surgery times the chance of a complicated finding once
       operated, gives 0.936, the same as the model trained on the label.
     - Among the uncomplicated children, the label's model scores the operated ones above the others at 0.880: what it
       learned is close to "would be operated".
     - Practice sets the number: Düsseldorf, the same group and label definition, operates 81% of its children
       (Regensburg 37%); there the authors' models reach 0.75 against 0.90 at Regensburg (2025). In our runs a model
       trained on Regensburg's 430 children of 2016-2018 ranks Düsseldorf's label at 0.807 and 0.767 among the operated,
       and one trained and tested at Düsseldorf reaches 0.769 (0.723 among the operated), against 0.934 (0.819) for
       Regensburg's 430 in the same file; the surgery model ranks the label at 0.735 there, 0.899 at Regensburg.
   * **What carries the score:**
     - The examination carries the decision: its findings alone predict the operation at 0.946 and the label at
       0.871, and leaving them out costs the surgery model 0.055; among operated children they add nothing (0.818
       with them, 0.818 without).
     - Single findings show the same: abdominal guarding (`Peritonitis`) and rebound tenderness alone predict the
       operation at 0.78 and 0.80 and the label at 0.73 and 0.76, but rank operated children at 0.52 and 0.53; the two
       clinical scores alone give 0.74 for the operation, 0.73 for the label and 0.55 among operated children.
     - The blood tests carry the severity itself: alone 0.895 on the label and 0.807 among operated children, where
       dropping them costs 0.066; CRP alone 0.85 and 0.76 (a pooled review gives CRP 0.78 for perforation).
     - The ultrasound signs of perforation and abscess were reasons to operate (no child treated without surgery had
       an abscess, 19 operated did; 2 suspected perforations against 30), but they do not carry the score: without the
       detailed ultrasound findings 0.930, without any ultrasound or scores 0.924.
   * **Recorded after or because of the decision:**
     - Length of stay, management and diagnosis are already dropped; `Peritonitis` is the examination's guarding at
       presentation ("peritonitis/abdominal guarding", 2021), not a surgical finding.
     - Unknown: the image study took "ultrasound images from admission and, if available, initial clinical course",
       and "for surgical patients, US images from the preoperative clinical course" (2024); whether the ultrasound
       columns describe the admission scan or a later scan before surgery is not stated.
     - The missing values follow the operation more than the severity: missing values alone give 0.826 on the label
       but 0.614 among operated children.
     - The practice changed over the years: among operated children 32% were complicated while ages were computed
       from the birth date (409 children, mostly 2016-2018) and 51% later, with the operated share unchanged (38% and
       36%); the age's number format, which marks the period, separates the classes among operated children at 0.60
       alone.
   * **Literature** (complicated against uncomplicated appendicitis in children, before surgery, scored on operated
     children with a tissue diagnosis):
     - 0.80 (Reismann 2019, 473 children), 0.79 (Aydin 2020), 0.77 for five severity grades (Erman 2025, 1,980), 0.87
       from blood tests and age (Akay 2026, 628), 0.92 in development and 0.91 at a second hospital for a score
       with peritoneal signs and free fluid (Ma 2026, 735 and 450).
     - On the full-cohort label of this group: 0.90 with a random forest at Regensburg (2021), 0.75 at Düsseldorf
       (2025), 0.65 to 0.78 for the image models (2024).
     - Our 0.815 among operated children sits in that range; 0.938 has no counterpart on a tissue-confirmed label, and
       the part above 0.82 comes from the pairs with children who were not operated.
   * **Consistency:** a task whose rows are those a decision let the outcome be measured for has been accepted twice:
     only granted loans have a repayment outcome, only patients sent to angiography have its result
     (`heart_disease`)[^a2]; restricting to operated children follows that, and the field's convention for this
     question[^a3].
   * **Sources:** Marcinkevics R, Reis Wolfertstetter P, Wellmann S, Knorr C, Vogt JE. Using machine learning to
     predict the diagnosis, management and severity of pediatric appendicitis. Front Pediatr. 2021;9:662183,
     https://doi.org/10.3389/fped.2021.662183. Marcinkevičs R, Reis Wolfertstetter P, Klimiene U, et al. Interpretable
     and intervenable ultrasonography-based machine learning models for pediatric appendicitis. Med Image Anal.
     2024;91:103042, https://doi.org/10.1016/j.media.2023.103042. Marcinkevičs R, Sokol K, Paulraj A, et al. External
     validation of predictive models for diagnosis, management and severity of pediatric appendicitis. Front Pediatr.
     2025;13:1587488, https://doi.org/10.3389/fped.2025.1587488 (Düsseldorf data:
     https://github.com/i6092467/pediatric-appendicitis-ml-ext). Reismann J, Romualdi A, Kiss N, et al. Diagnosis and
     classification of pediatric acute appendicitis by artificial intelligence methods: an investigator-independent
     approach. PLoS One. 2019;14(9):e0222030, https://doi.org/10.1371/journal.pone.0222030. Aydin E, Türkmen IU, Namli
     G, et al. A novel and simple machine learning algorithm for preoperative diagnosis of acute appendicitis in
     children. Pediatr Surg Int. 2020;36(6):735-742, https://doi.org/10.1007/s00383-020-04655-7. Erman A, Ferreira J,
     Ashour WA, et al. Machine-learning-assisted preoperative prediction of pediatric appendicitis severity. J Pediatr
     Surg. 2025;60(6):162151, https://doi.org/10.1016/j.jpedsurg.2024.162151. Akay MA, Kılıç ANK, Tatar OC, Varlıklı O,
     Yıldız GE. Predicting complicated appendicitis: what can machine learning add? Diagnostics (Basel).
     2026;16(16):2644, https://doi.org/10.3390/diagnostics16162644. Ma H, Ouyang J, Liu J, et al. Integration of
     clinical information for identification of gangrenous or perforated appendicitis in children: a multicenter
     retrospective cohort study with external validation. BMC Pediatr. 2026;26(1):881,
     https://doi.org/10.1186/s12887-026-07314-3. Acharya A, Markar SR, Ni M, Hanna GB. Biomarkers of acute
     appendicitis: systematic review and cost-benefit trade-off analysis. Surg Endosc. 2017;31(3):1022-1031,
     https://doi.org/10.1007/s00464-016-5109-1.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Ship as defined (implemented) | 763 children, 115 complicated; TabPFN 3.5 0.938, random forest 0.925, logistic regression 0.913 | the source's target; the largest cohort | 63% of the labels set by the decision not to operate; a surgery model that never sees the label scores 0.904; the score follows the share operated (Düsseldorf 0.75) |
     | B | Retire | `No (Retired)`; the folder leaves the working copy | no task whose label is partly the treatment | the tissue-confirmed question leaves with it |
     | C | Operated children only | 284 children, 115 complicated, every label from the tissue examination; ages written to 2 decimals; TabPFN 3.5 0.815, random forest 0.782, logistic regression 0.755 | every label measured; the question published studies ask; the signs that decide surgery add nothing (0.818 with or without); the methods spread | 284 rows; who is operated still follows practice (complicated share among them 32% early, 51% later; operated children only at Düsseldorf 0.71); the use case narrows to planning the operation; a target the source did not ship on its own |
     | D | Children with appendicitis only | 451 children, 114 complicated; drops the 309 without appendicitis; TabPFN 3.5 0.896, random forest 0.871, logistic regression 0.864 | drops the easiest pairs | 170 children still labelled by the decision not to operate; their appendicitis is itself a rule on the scores and the diameter |

   * **Recommendation:** C: every label is then a measurement, the selection is how that measurement comes to exist,
     as with granted loans, and the score lands where the literature puts this question; B if a sample chosen by the
     hospital's practice is out as well. **Decision:** C, B, or keep A?

   **Notes for the AI:** on C, in `_clean` keep `df = df[df["Management"] != "conservative"]` before the drop (284
   rows, 115 complicated; the 21 `secondary surgical` and the 1 `simultaneous appendectomy` stay, graded at surgery;
   primary surgery alone gives TabPFN 3.5 0.801), add `"Age": 2` to `MEASURED_PRECISION` (8-decimal ages mark
   2016-2018), and rewrite `task_summary`: question "Is the appendicitis of an operated child complicated (gangrenous,
   perforated or abscessed)?"; use case "For example, a paediatric surgeon, before an appendectomy, judges from the
   examination, blood tests and ultrasound whether the appendicitis is complicated, to choose the approach and plan the
   care after it" (the 2021 paper names preoperative stratification "guiding the decision between single incision vs.
   2-trocar technique"); row "one child operated for appendicitis ... who had an ultrasound (284 children)"; predicted
   "complicated in the tissue examination after surgery (40.5%)"; fit direct, `fit_reason` naming the selection (the
   use case meets the same children). `curation_comments`: the label and selection, the probes on the operated frame
   (missing values alone 0.614, number formats alone 0.614, 0.585 without the age's), the period shift. No
   `Selection Bias` marker (the selection is how the label exists); `Class-dependent Recording` stays. Then `dataset
   check`, the probes, README, a record CC line, CHANGELOG; no build. On B: record `No (Retired)` with a CC line,
   `priority` removed, the folder kept until this file is committed.

   [^a1]: No rule names hospital practice; the two that come closest. **USE-5** (Must): "Check how the source built its
     label before accepting it. [...] A label checked and found to be another quantity than the one the actor acts on
     still fails." The verification checklist's circular-features check (LEAK-4, SEL-5, TP-4): "Were every feature and
     the label read from the same source at the same time, with no gap in which a practitioner's action could differ
     from reading the label?"; here the practitioner's action sets the label for the children not operated.
   [^a2]: Selection bias, no marker when "the selection is how the label comes to exist, so every dataset of the task
     has it (only granted loans have a repayment outcome, Andrej 2026-10-15; only patients referred for angiography
     have its result, `heart_disease`)" (selection.md, Patterns, "Selection bias").
   [^a3]: **TP-7** (Must): when the definition builds the target itself, "use an established convention". **TP-6**
     (Must): "A fix of our own invention [...] is not a better version"; C drops rows whose label was never measured
     rather than inventing a label. **TP-3** (Must): "If tuned methods spread, keep the dataset." **LEAK-13** (Must):
     write every row at the precision of the measured values.

   **Andrej (2026-11-05, discuss):** Reply (B): Retire. Even after several measures tried to save the task and even
   bringing it down to 284/763 rows that could be meaningfully used, there a re still issues left. We need to retire.
   Document what we tried and why this is still not a good solution. Add the relevant decision markers

   **Resolved (2026-11-06, Andrej):** retired (B): the record is `No (Retired)` with `No Good Target / Scientific
   Discovery` beside `Class-dependent Recording`; its CC line lists what was tried (the format fix of 2026-10-27, the
   decision signs dropped, children with appendicitis only, operated children only) and what each left: the surgeon's
   decision in the label, or the practice and its period shift in the operated sample. The folder stays until this
   file is committed.

## Reference

@article{marcinkevivcs2024interpretable,
  title={Interpretable and intervenable ultrasonography-based machine learning models for pediatric appendicitis},
  author={Marcinkevi{\v{c}}s, Ri{\v{c}}ards and Wolfertstetter, Patricia Reis and Klimiene, Ugne and Chin-Cheong, Kieran and Paschke, Alyssia and Zerres, Julia and Denzinger, Markus and Niederberger, David and Wellmann, Sven and Ozkan, Ece and others},
  journal={Medical image analysis},
  volume={91},
  pages={103042},
  year={2024},
  publisher={Elsevier}
}
