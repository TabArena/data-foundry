---
unique_name: eryhemato_squamous_disease
name: dermatology
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Selection Bias
tags:
- Tiny Data
- 'Samples: Over Time'
- 'Time: Lost'
collections:
- TabArena Reject
original_source: UCI
year: '1998'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://github.com/EpistasisLab/pmlb/blob/master/datasets/dermatology/metadata.yaml
- https://doi.org/10.24432/C5FK5P
notebook_path: datasets/beyond_iid/new_iid/eryhemato_squamous_disease/eryhemato_squamous_disease.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/eryhemato_squamous_disease/dataset.py
source_row: 753
type_adapter_id: curation-record-v1
---

## Comments

Looks like an old but reasonable task

If we use the Histopathological, this means we assume the patient may or may not be given a biopsy

CC (2026-10-06, Lennart): Changed to the clinical features only after the task-probe review (flag `solved`). The source evaluates in two steps: "Patients were first evaluated clinically with 12 features. Afterwards, skin samples were taken for the evaluation of 22 histopathological features." With all 34 features the task is close to solved (logistic regression: macro ROC AUC 0.999, 97% accuracy on the 60 shipped splits; BeyondArena's best log loss 0.044), so v0.2 asks for the diagnosis before the biopsy: the 11 clinical findings, family history and age. Same six classes. On the shipped splits this gives macro ROC AUC 0.98 and 87% accuracy for logistic regression (log-loss skill +0.76; random forest +0.72, LightGBM +0.65), with seborrheic dermatitis, pityriasis rosea and chronic dermatitis as the hard cases, which is the differential the source describes. No probe flags on the rebuilt container. One pair of patients shares all clinical findings with different diagnoses.

**Assessment (AI, 2026-10-14):** The count above is off by one: the clinical features are 10 findings graded 0 to 3 (erythema to scalp involvement), family history and age, the source's 12 clinical features (UCI variable list); the definition keeps exactly these.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback log_loss — Guevenir et al. 1998 report cross-validated accuracy of VFI5 without costs between the six diagnoses, and we use the 12 clinical features only (MET-6).

**Assessment (AI, 2026-10-27):** evidence for the Selection Bias marker of PR #16, checked on dermatology.data: 67 of the 72 lichen planus patients (93%) have oral mucosal involvement and none of the other 294 patients do, against 19% to 63% in clinic series of cutaneous lichen planus (56% of 91 biopsy-confirmed patients, https://jpad.com.pk/index.php/jpad/article/view/1817; 19% of 131, https://diposit.ub.edu/dspace/handle/2445/171919). All 20 pityriasis rubra pilaris patients are aged 7 to 22. The rows look like typical cases of each disease rather than a clinic's patients. The definition's fit_reason does not name this yet.

CC (2026-10-27, Lennart): fit approximate (was direct): a dermatologist's lichen planus patients do not show the selection of these rows, so it is a known gap (USE-8, amended on the review of PR #16); the Selection Bias marker stays.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 10 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `erythema`, `scaling`, `definite borders`, `itching`, `koebner phenomenon`, `polygonal papules`, `follicular papules`, `oral mucosal involvement`, `knee and elbow involvement`, `scalp involvement` (the README lists their levels).

CC (2026-11-01, Lennart): the decode rule (a code whose codebook says in words what each level is carries the words; a score without them is a number): 10 scores are numbers (erythema, scaling, definite borders, itching, koebner phenomenon, polygonal papules, follicular papules, oral mucosal involvement and more).

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target ships its class names.

CC (2026-11-05, Lennart): GitHub issue #48 review: the 10 clinical scores 0-3 ship as numbers (the source names only the two ends of the scale); `_feature_types` declares only `family history` categorical. The declared metric (log_loss fallback) is checked.

**Assessment (AI, 2026-11-05):** the 2026-11-01 decoding made the scores numbers in `_clean`, but a blanket `_feature_types` (every column but age categorical) cast them back to unordered categories; found by GitHub issue #48. A test now checks that every `SCORES` column ships numeric.

CC (2026-11-11, Andrej): BeyondArena v0.2 review page, eryhemato_squamous_disease:
- Issue 3 (`change`, option B / the answer's a): the random split stays and is tagged `ForcedIIDFromTemporal`, with a `Time basis:` bullet carrying the measured cost. Shuffling does not remove the file's two recording paths: it gives every test patient training patients of its own part, worth 0.08 to 0.15 in log loss (logistic regression on a random mix of both parts 0.536 and 0.345, against 0.688 and 0.425 trained on as many patients of the other part alone; the part as a feature adds 0.014, a made-up part 0.001). Read as two collection periods, too few for three windows.
- Issue 1 (`ok`): ship the clinical-only task as defined; no change.
- Issue 2 (`discuss`, no note): the ten graded findings already ship as numbers, as the decode rule of 2026-11-01 and the definition's notes ask; nothing left to apply.
- `dataset check` passed (0 errors, 0 warnings, 1 info: the known pair with the same findings and different diagnoses).
- The review moved from the folder's file into this record's `## Review` section.

## Review

**Outcome:** added. The AI recommends shipping it after one type fix: the ten graded clinical findings ship as
unordered categories, although the definition's own notes and the curator's rule of 2026-11-01 make them numbers
(issue 2). Reviewed on 2026-11-04 without a review panel, from the record, the earlier experiments and a model
run on the shipped data. Validity: the diagnosis of six scaly red skin diseases from the source's 12 clinical features,
before the skin biopsy, the first of the two steps the source describes; the label is the biopsy diagnosis, so the
signs that mark lichen planus and pityriasis rubra pilaris are not circular (Andrej's audit, 2026-10-20). The patients
look selected (`Selection Bias`, fit `approximate` since Lennart's call of 2026-10-27). Value: TabPFN beats logistic
regression on 59 of 60 shipped splits (log loss 0.320 against 0.371), 55 of 60 on the three hard classes alone. A
model run used the 34-feature BeyondArena table with the biopsy findings, so its spread does not carry over.
Quality: the ten findings typed as unordered categories (issue 2); one patient aged 0, kept with a note. Weighed: a
stage the source describes and a clear model ranking +, a selected, small and old cohort -.

**Main points:** All settled: ship the clinical-only task with the ten graded findings as numbers (issues 1 and 2,
resolved 2026-11-05); the random split is tagged forced from temporal with the measured cost of the file's two parts
(issue 3, resolved 2026-11-10).

**Record judgment:** valid. Settled by CC 2026-10-06 (Lennart: clinical features only), CC 2026-10-20 (Andrej: keep,
selection named in the fit), CC 2026-10-27 (Lennart: fit approximate, the marker stays) and CC 2026-11-01 (Lennart: the
ten scores are numbers, the target ships its class names). Lennart's comment of 2026-10-06 says one pair of patients
shares all clinical findings with different diagnoses; without age it is 38 patients in 10 groups (the bundle check
counts one pair because age breaks the other ties).

**Issues for Andrej:**

1. **Ship in TabArena v0.2 as defined?**

   * **Problem:**
     - Polygonal papules or mouth involvement mark all 72 lichen planus patients and no one else, and follicular
       papules mark pityriasis rubra pilaris, so two of six classes follow from one sign each.
     - The patients look selected: 93% of the lichen planus patients have mouth involvement against 19% to 63% in
       clinic series, and all 20 pityriasis rubra pilaris patients are aged 7 to 22.
     - Your audit of 2026-10-20 found neither a reason to exclude nor to change the setup; ship it?
   * **Background:** the source evaluates in two steps: "Patients were first evaluated clinically with 12 features.
     Afterwards, skin samples were taken for the evaluation of 22 histopathological features." With the biopsy
     findings the task is close to solved (logistic regression macro ROC AUC 0.999), so v0.2 keeps the ten clinical
     findings graded 0 to 3, family history and age (CC 2026-10-06, Lennart)[^1a]. The label is the diagnosis after
     the biopsy, and the marking signs are seen before it, so no feature is the criterion that assigns the label.
     Lichen planus is a disease of the skin and mouth with flat, angular bumps (polygonal papules); pityriasis rubra
     pilaris shows bumps around hair follicles (follicular papules).
   * **Effect on the task:** two classes are easier than in a dermatologist's clinic, where many lichen planus
     patients have no mouth lesions and pityriasis rubra pilaris is most common in adults. The model comparison rests
     on the three hard classes (seborrheic dermatitis, pityriasis rosea, chronic dermatitis), the differential the
     source describes.
   * **Experiments:** on the 60 shipped splits (20 repeats of 3 folds), clinical features only: TabPFN 3.5 log loss
     0.320 and accuracy 0.895, logistic regression 0.371 and 0.871; TabPFN better on 59 of 60 splits, and on 55 of 60
     on the three hard classes alone. Lichen planus and pityriasis rubra pilaris carry 2.7% of TabPFN's log loss.
     Without age, 38 patients in 10 groups share all clinical findings with different diagnoses; they carry 31% to
     36% of the loss and both models score about 1.1 on them, and the TabPFN to logistic regression gap is the same
     without them (6.2 against 6.4 per fold), so they set a floor on the loss, not the ranking.
   * **Consistency:** this dataset is the worked example of the selection-bias pattern: a concern flag, the verdict
     stays, the gap is named in `fit_reason`, and the fit is approximate when the real setting lacks the
     selection[^1b]. The stage before the biopsy follows the rule that a task with measurements from a later stage is
     offered at the stage the source describes[^1c].
   * **Sources:** Güvenir HA, Demiröz G, Ilter N. Learning differential diagnosis of erythemato-squamous diseases
     using voting feature intervals. Artif Intell Med. 1998;13(3):147-165. doi:10.1016/S0933-3657(98)00028-1. UCI
     page: https://doi.org/10.24432/C5FK5P. Clinic series: Samreen A, Luqman N, Asgher R, Khalid M, Shaheen JA.
     Frequency of oral involvement in cutaneous lichen planus patients. J Pak Assoc Dermatol. 2021;31(3):454-458
     (56% of 91 biopsy-confirmed patients; https://jpad.com.pk/index.php/jpad/article/view/1817); 19% of 131 in
     https://diposit.ub.edu/dspace/handle/2445/171919.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Ship (implemented) | 366 patients, 12 clinical features, six diagnoses, random split, log loss; `Selection Bias` and fit `approximate` | the source's own pre-biopsy stage; models separate on 59 of 60 splits | selected cases make two classes easy; small and old |
     | B | Discuss | the verdict stays open | room for a point the audit missed | none found since the audit |

   * **Recommendation:** A, ship, once issue 2 is applied: no exclusion reason survived the audit, and the selection
     is named in the fit. **Decision:** ship (A), or discuss (B)?

   [^1a]: **TP-6** (Must): keep two questions apart, is the task valid and is it the best version; **USE-4** (Must):
     when the features include measurements from a stage after the decision the task models, offer the task at the
     stage the source describes.
   [^1b]: Selection bias (selection.md, "Selection bias"; Andrej 2026-10-20, Lennart 2026-10-27): mark it
     `Selection Bias`, the verdict is usually still `Yes`; name the gap in `fit_reason`; **USE-8** (Must): the fit is
     approximate when the real-world setting of the use case does not share the bias.
   [^1c]: **USE-4** (Must), case row: eryhemato_squamous_disease offered on the 12 clinical features, before the skin
     biopsy (applied).

   **Resolved (2026-11-05, Andrej):** ship (A), once issue 2 is settled.

   **Andrej (2026-11-11, ok):**

   **Resolved (2026-11-11, Andrej):** A again; issue 2 is settled, so the clinical-only task ships as defined. The
   definition is unchanged by this mark.

2. **Type the ten graded findings as numbers, as the notes and the decode rule say?**

   * **Problem:**
     - `_clean` turns the ten findings graded 0 to 3 into numbers, as the curation notes and your rule of 2026-11-01
       say, but `_feature_types` still declares every column except age categorical, so they ship as unordered
       categories (the README lists them as `category`).
     - An unordered category drops the order the source gives the grades ("0 indicates that the feature was not
       present, 3 indicates the largest amount possible, and 1, 2 indicate the relative intermediate values").
     - Type them as numbers?
   * **Background:** the decode rule of 2026-11-01 makes a score with no words per level a number, and lists this
     dataset's ten findings among the columns that "are numbers again"[^2a]. Pull request #37 added the conversion in
     `_clean` but left `_feature_types` as the notebook migration wrote it. Of the 16 definitions with such a list of
     scores, this is the only one whose README shows them as categories (checked 2026-11-04).
   * **Effect on the task:** with 244 training patients per split, a model has to learn each grade of each finding as
     a separate level instead of reading more redness or more scaling as more of the same sign, which a dermatologist
     does.
   * **Experiments:** in the ordinal experiment of 2026-10-30 (LightGBM, a linear model and TabPFN 3.5 on the shipped
     splits), the grades in order lowered LightGBM's error against unordered categories by 31% on this dataset, the
     largest gain of 55 datasets; TabPFN gained less, as it handles unordered categories well.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Unordered categories (implemented) | the ten findings ship as unordered categories | none found | contradicts the notes and the decode rule; loses the order the source states |
     | B | Numbers | the ten findings ship as numbers 0 to 3; `family history` stays categorical | follows the source's codebook, the notes and the rule; one line in `_feature_types` | the checksum changes; a rebuild |
     | C | Ordered categories | the ten findings ship as ordered categories 0 < 1 < 2 < 3 | keeps the order without spacing | the form of 2026-10-30 that the rule of 2026-11-01 reversed |

   * **Recommendation:** B, numbers: the decode rule already decided it, and only the type declaration was missed.
     **Decision:** numbers (B), keep the categories (A), or ordered categories (C)?

   **Notes for the AI:** on B, set `_feature_types` to `FeatureTypes(categorical=["family history"])`, run
   `dataset check`, and confirm in the README that the ten `SCORES` columns are numeric and `family history` is
   categorical; the CHANGELOG entry names the fix. On C, declare `ordinal={c: [0, 1, 2, 3] for c in SCORES}` and drop
   the conversion note.

   [^2a]: **CLEAN-14** (Should; amended 2026-11-01, Lennart): a score or rating with no words per level is a number;
     its case row lists "the ten 0-3 findings" of eryhemato_squamous_disease as numbers again (applied). **CLEAN-12**
     (Should): a code whose codebook says in words what each level is carries the words; a code without them stays as
     shipped.

   **Andrej (2026-11-05, discuss):** Why do you recommend B although the bullets in C are clearly ordered categories?

   **Answer (AI, 2026-11-05):**

   * **Your question:** the grades are clearly ordered, so why numbers (B) rather than ordered categories (C)?
   * **Found:**
     - Both keep the order; they differ in whether the steps count as equal. A number says 2 is twice 1 and the step
       from 2 to 3 is the step from 1 to 2; an ordered category says only 0 < 1 < 2 < 3.
     - The source describes one intensity scale with words only at its ends: "0 indicates that the feature was not
       present, 3 indicates the largest amount possible, and 1, 2 indicate the relative intermediate values". No level
       has a name of its own (no "mild", "marked"), which is what makes a code an ordered category under the type rule.
     - The type rule of 2026-11-01 (Lennart) settles that case: a score or rating with no words per level, or words
       only at its two ends, is a number; a code the source names in words, level by level, ships as the words,
       ordered when the scale is[^b1]. Its Cases row names these ten findings among the 54 columns that "are numbers
       again". C is the form of 2026-10-30, which that rule reversed for scores like these.
     - So B is not a judgment that the grades lack an order; it applies the rule written for exactly this kind of
       scale. Choosing C here would be an exception to that rule, or an amendment that moves all 54 such columns (16
       definitions) back to ordered categories.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | B | Numbers | the ten grades ship as 0 to 3; `family history` categorical | follows the source's scale and the type rule; the same form as the other 53 scored columns | assumes equal steps between grades |
     | C | Ordered categories, as an exception | the ten grades as 0 < 1 < 2 < 3 here only; a dated exception line naming what sets them apart | no spacing assumed | differs from the other scores under the same rule, with no fact that sets these apart found |
     | D | Ordered categories, rule amended | every score with words only at its ends becomes an ordered category (54 columns, 16 definitions) | one form for all graded findings | reverses the rule of 2026-11-01; 16 definitions change |

   * **Recommendation:** B, as before: the rule decided this form for graded scores with words only at the ends, and
     these ten are one of its named cases. **Decision:** numbers (B), ordered here only (C), or amend the rule (D)?

   [^b1]: **CLEAN-14** (Should; amended 2026-11-01, Lennart): the decode table in cleaning_features.md, rows "a code
     the source names in words, level by level" (the words, ordered when the scale is) and "a score or rating with no
     words per level, or words only at its two ends" (a number).

   **Lennart (2026-11-05, change):** Option B: Numbers.

   **Resolved (2026-11-05, Lennart):** B, on GitHub issue #48 (#52). The 10 scores ship as numbers; `_feature_types`
   declares only `family history` categorical, the contradicting note is gone, and a test checks that every `SCORES`
   column ships numeric.

   **Andrej (2026-11-11, discuss):**

   **Answer (AI, 2026-11-11):** Nothing is left to decide here and nothing was re-measured: the ten graded findings
   ship as numbers, which is what the definition's own notes and the decode rule of 2026-11-01 ask for.

   * `_feature_types` declares only `family history` categorical; `erythema`, `scaling`, `definite borders`,
     `itching`, `koebner phenomenon`, `polygonal papules`, `follicular papules`, `oral mucosal involvement`,
     `knee and elbow involvement` and `scalp involvement` ship numeric, and a test checks it.
   * The source names only the ends of the scale ("0 indicates that the feature was not present, 3 indicates the
     largest amount possible, and 1, 2 indicate the relative intermediate values"), which is why they are numbers
     rather than ordered categories with named levels.
   * If the mark meant something else, say which part; as it stands the issue can be closed.

3. **Time basis: the file's two parts score apart: name the random split forced from temporal?**

   * **Problem:**
     - The 12 clinical findings and the diagnosis describe the patient at one examination and the file keeps no date, but it has two parts: rows 1 to 169 in mixed order and rows 170 to 366 mostly in runs of one diagnosis, with another case mix (seborrheic dermatitis 41 against 20 patients, psoriasis 44 against 68).
     - The clinical findings tell the two parts apart (random forest ROC AUC 0.70, against 0.54 from the diagnosis alone), and a model trained on one part scores worse on the other than one trained on as many patients of both (logistic regression log loss 0.381 against 0.318 on the second part, 0.696 against 0.479 on the first), so if the parts are two periods of collection, the relation between findings and diagnosis moved between them.
     - Keep the random split as a `StationaryRelation`, tag it `ForcedIIDFromTemporal` with the measured cost, or split by file part?
   * **Background:**
     - What moves within a diagnosis: in the second part, psoriasis patients have itching graded 0.84 lower and the Koebner phenomenon (new lesions where the skin is injured) 0.77 lower on the 0 to 3 scale; pityriasis rosea patients itching 0.61 and Koebner 0.90 lower and definite borders 0.64 higher. That fits another examiner, another period, or cases added by diagnosis.
     - The 8 missing ages come in two runs of four consecutive rows (rows 34 to 37 and 263 to 266), so within each part the order looks like the order of recording; the source (Güvenir et al. 1998, not readable here) and the UCI page say nothing about the order or the period.
     - The record's facts, `Samples: Over Time` and `Time: Lost`, still fit: the parts are not dates. By the rule's questions the diagnosis is a present state, which would make a `StationaryRelation`, but the rule counts a change in practice or recording as time reaching the target, and two parts are too few for three windows, which makes the split forced[^3a].
   * **Experiments:** the raw UCI file, the 12 clinical features of the v0.2 task, untuned logistic regression and random forest (Slurm job 1366170):
     - Telling the parts apart (5 x 5-fold, random forest): ROC AUC 0.704 from the findings, 0.735 with the diagnosis added, 0.539 from the diagnosis alone.
     - Each part's patients in 3 folds (5 seeds), trained on the other part (169 or 197 patients) or on as many patients drawn from both parts outside the test fold: on the second part, logistic regression log loss 0.381 against 0.318 (worse on 14 of 15 folds), random forest 0.527 against 0.400 (15 of 15); on the first part, 0.696 against 0.479 (15 of 15) and 0.651 against 0.572 (12 of 15). Accuracy falls by 0.01 to 0.04.
     - The time probe of 2026-11-06 flagged the order: consecutive rows share the diagnosis 42% of the time against 20% by chance, all of it in the second part (14% in rows 1 to 169, 66% after).
   * **Effect on the task:** under the random split both parts sit on both sides, so a model learns each part's grading; if the parts are periods, a dermatologist's new patients come from a later one, and the random split flatters every model by 0.06 to 0.22 in log loss.
   * **Unknown:** whether the parts are two periods, two examiners, or one series extended by diagnosis; the authors (Güvenir, İlter) would know.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random split, `StationaryRelation` (implemented) | the shipped split; once PR #50 is in, the tag and a `Time basis:` line | the diagnosis is read at the examination | the measurement contradicts it: the relation moves between the file's parts |
     | B | Random split, `ForcedIIDFromTemporal` | the shipped split; the tag and a `Time basis:` line with the two parts and the measured cost[^3b] | states what the random split hides; keeps 60 splits over all 366 patients | reads the file's parts as periods, which the source does not state |
     | C | Split by file part | train on one part, test on the other | tests the shift directly | two groups make one shift test, not a benchmark split[^3c]; the boundary is estimated from the order, not recorded |

   * **Recommendation:** B: the relation measurably moves between the two parts, and two parts cannot give the windows a temporal split needs, so the random split stays as a forced one with its cost written down. If you read the parts as another examiner rather than another time, A with the shift named. **Decision:** A, B or C?

   **Notes for the AI:** on B, once PR #50 is in: `data_tags = ("ForcedIIDFromTemporal",)` and a curation bullet `- Time
   basis: ForcedIIDFromTemporal: patients examined over a period the source does not state (published 1998); the file
   keeps no date but has two parts, rows 1 to 169 in mixed order and rows 170 to 366 mostly in runs of one diagnosis.
   The clinical findings tell them apart (random forest ROC AUC 0.70; 0.54 from the diagnosis alone), and trained on one
   part, logistic regression's log loss on the other is 0.381 and 0.696, against 0.318 and 0.479 trained on as many
   patients of both parts (Slurm job 1366170). Read as two collection periods, too few for three windows; dates of
   examination would allow a split by period.` On A, `data_tags = ("StationaryRelation",)` and the same facts with the
   curator's reason. C needs a column from the raw row order and a grouping with two groups; not drafted. No
   `splits_comment` change on A or B.

   [^3a]: **SPLIT-32** (Should): time affects the target when the target, how often it occurs, or its relation to the
     features moves with the period (a change in practice or recording among the examples); when it does and the time
     is lost or too short for three windows, the split is forced. A present state read through a relation that time
     does not move is a `StationaryRelation`.
   [^3b]: **SPLIT-8** (Must): a task temporal in nature or by its use case whose release cannot give the windows ships
     in the closest regime, tagged as forced from temporal, with the cost measured against the valid windows where the
     data has any, after a leak test across the split; the definition says what a timestamp would change.
   [^3c]: Weighed factor "Only a few groups" (splits.md): with only a few groups, a grouped split is a domain-shift test
     between them rather than prediction for unseen entities. **SPLIT-24** (Must): group on a true group id or on one
     constructed exactly from the data.

   **Andrej (2026-11-06, discuss):** After shuffling the samples, can models still exploit the different recording
   paths?

   **Answer (AI, 2026-11-09):** Yes: shuffled, every test patient has training patients from its own part, and that is
   worth 0.08 to 0.15 in log loss; keep the random split, tagged forced from temporal with these numbers (a)?

   * **Problem:**
     - On the shipped splits, logistic regression scores one part's test patients at log loss 0.536 against 0.688 (rows
       1 to 169) and 0.345 against 0.425 (rows 170 to 366) when it trains on a random mix of both parts, as the random
       split does, rather than on as many patients of the other part alone (better on 57 and 54 of 60 splits).
     - What it gains is each part's grading, not its case mix, and it does not get all of it: told the part, the model
       improves by another 0.014 (53 of 60 splits), while a made-up part with the same diagnoses per part gives 0.001.
     - `StationaryRelation` (A) is closed anyway since your rule of 2026-11-06: it needs a measurement on dates, and
       this file has none[^3p].
   * **Experiments:** the shipped task (12 clinical features, 60 random splits), each patient's part traced from its
     raw row, untuned logistic regression (LR), random forest (RF) and LightGBM, log loss (Slurm job 1373758):
     - Each part's test patients, by what the model trained on. The first three columns train on the same number of
       patients (104 to 120, the smaller part's training rows); the last on the whole training side:

       | Test patients | Own part only | Random mix of both | Other part only | All 244 |
       |---|---|---|---|---|
       | rows 1 to 169, LR | 0.508 | 0.536 | 0.688 | 0.462 |
       | rows 170 to 366, LR | 0.304 | 0.345 | 0.425 | 0.288 |
       | rows 1 to 169, RF | 0.579 | 0.602 | 0.694 | 0.564 |
       | rows 170 to 366, RF | 0.390 | 0.430 | 0.559 | 0.366 |
       | rows 1 to 169, LightGBM | 0.896 | 1.016 | 1.248 | 0.819 |
       | rows 170 to 366, LightGBM | 0.536 | 0.651 | 0.825 | 0.450 |

     - The mix beats the other part on 57 and 54 of 60 splits (LR), 53 and 60 (RF), 49 and 43 (LightGBM). At the same
       size, the own part alone beats the mix (LR on 37 and 45 of 60): the other part's patients hurt when they replace
       own-part patients, and help when added (all 244 beat the own part alone).
     - The part as a feature: LR 0.369 to 0.355 (better on 53 of 60), RF 0.457 to 0.437 (52), LightGBM 0.620 to 0.598
       (42). A made-up part, drawn within each diagnosis so it has the real part's diagnoses: LR 0.367 (34 of 60), RF
       0.448, LightGBM 0.611. With the part flipped on the test patients, the LR with the part loses 0.061 (worse on
       all 60 splits). Terms for each finding by part add nothing more (LR 0.363).
     - The case mix alone: the diagnosis shares of the patient's own part predict no better than the overall shares
       (log loss 1.687 against 1.687). Itching and Koebner shuffled within each part, so that they still mark the part
       and say nothing else, do worse than dropped (LR 0.545 against 0.533, worse on 51 of 60); dropping both costs
       0.164, so their value is clinical.
     - For scale: TabPFN beats LR by 0.051 (issue 1).
   * **Effect on the task:** shuffling does not remove the two recording paths; it hands every test patient training
     patients of its own path, so the random split scores a model on practices it has seen. A dermatologist's new
     patients come from a third practice (another examiner or a later period). If it differs as much as the two parts
     do, a model loses about the gap between the mix and the other part; trained on both parts it may lose less, which
     the file cannot test.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Random split, `ForcedIIDFromTemporal` | the issue's B, its `Time basis:` line with the numbers measured on the shipped splits (notes below)[^3q] | says what the random split rewards: each part's own grading; keeps 60 splits over all 366 patients | reads the file's parts as periods, which the source does not state |
     | b | Split by file part | the issue's C: train on one part, test on the other | scores the shift a new practice brings | two groups make one shift test, not a benchmark split[^3r]; the boundary is estimated from the order |
     | c | Random split, no prototype | a `Time basis:` line naming the two parts and the cost, no tag | claims no period, for the reading of two examiners | `dataset check` keeps noting the missing basis; the rule gives a forward use case with its time lost the forced tag[^3p] |

   * **Recommendation:** a, unchanged: the measurement shows what B assumed, that the random split rewards learning
     each part's grading, and A is closed. **Decision:** a, b or c?

   **Notes for the AI:** on a, once PR #50 is in: `data_tags = ("ForcedIIDFromTemporal",)` and a curation bullet `- Time
   basis: ForcedIIDFromTemporal: patients examined over a period the source does not state (published 1998); the file
   keeps no date but has two parts, rows 1 to 169 in mixed order and rows 170 to 366 mostly in runs of one diagnosis.
   The clinical findings tell them apart (random forest ROC AUC 0.70; 0.54 from the diagnosis alone). The random split
   puts both parts on both sides, so each test patient has training patients of its own part: on the shipped splits,
   logistic regression's log loss on one part's patients is 0.536 and 0.345 when it trains on a random mix of both
   parts, against 0.688 and 0.425 when it trains on as many patients of the other part alone; told the part, it
   improves by another 0.014, and the case mix of the parts adds nothing (Slurm job 1373758). Read as two collection
   periods, too few for three windows; dates of examination would allow a split by period.` On c, no tag and the same
   facts in a `Time basis:` line that says why no prototype fits. No `splits_comment` change.

   [^3p]: **SPLIT-32** (Should; Andrej, 2026-11-06): a `StationaryRelation` is always measured on a dated source; where
     time is lost it cannot be, and a forward use case takes the forced tag. A change in practice or recording among
     the examples counts as time reaching the target.
   [^3q]: **SPLIT-8** (Must): a task temporal in nature or by its use case whose release cannot give the windows ships
     in the closest regime, tagged as forced from temporal, with the cost measured where the data allows, after a leak
     test across the split; the definition says what a timestamp would change.
   [^3r]: Weighed factor "Only a few groups" (splits.md): with only a few groups, a grouped split is a domain-shift test
     between them rather than prediction for unseen entities.

   **Resolved (2026-11-10, Andrej):** B, which is the 2026-11-09 Answer's option a: the random split stays,
   `data_tags = ("ForcedIIDFromTemporal",)`, and the `Time basis: ForcedIIDFromTemporal:` bullet in `curation_comments`
   carries the numbers measured on the shipped splits (mix 0.536 and 0.345 against the other part 0.688 and 0.425, the
   part as a feature 0.014; Slurm job 1373758). No `splits_comment` change; record facts unchanged.

   **Andrej (2026-11-11, change):** Reply (a): Random split, ForcedIIDFromTemporal
   Option B: Random split, ForcedIIDFromTemporal.
   After shuffling the samples, can models still exploit the different recording paths?

   **Resolved (2026-11-11, Andrej):** B (the 2026-11-09 Answer's a), and carried out on this branch:
   `data_tags = ("ForcedIIDFromTemporal",)` and the `Time basis: ForcedIIDFromTemporal:` bullet with the measured
   numbers are in the definition; the random split and `splits_comment` are unchanged, and `dataset check` passes
   (0 errors, 0 warnings; the one info is the known pair of patients sharing all clinical findings). On the question:
   yes, shuffling does not remove the two recording paths, it hands every test patient training patients of its own
   path, which is worth 0.08 to 0.15 in log loss (mix 0.536 and 0.345 against the other part alone 0.688 and 0.425;
   the part as a feature adds 0.014 on top, a made-up part 0.001; Slurm job 1373758). That is what the tag now says.

## Reference

@article{guvenir1998learning,
  title={Learning differential diagnosis of erythemato-squamous diseases using voting feature intervals},
  author={G{\"u}venir, H Altay and Demir{\"o}z, G{\"u}l{\c{s}}en and Ilter, Nilsel},
  journal={Artificial intelligence in medicine},
  volume={13},
  number={3},
  pages={147--165},
  year={1998},
  publisher={Elsevier}
}
