---
unique_name: eryhemato_squamous_disease
name: dermatology
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 3
decision_markers:
- Selection Bias
tags:
- Tiny Data
- 'Samples: Over Time'
- 'Time: Lost'
- Clinical Study
collections:
- TabArena Reject
original_source: UCI
year: '1998'
collection_period: Unknown
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://github.com/EpistasisLab/pmlb/blob/master/datasets/dermatology/metadata.yaml
- https://doi.org/10.24432/C5FK5P
- https://doi.org/10.1016/S0933-3657(98)00028-1
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

CC (2026-10-20, Andrej): Audit of the clinical-only version: no reason to exclude it or to change the splits or metric (TabPFN 3.5 vs logistic regression on the 60 shipped splits).
- Two classes follow from one sign each: polygonal papules (flat, angular bumps) or mouth involvement mark all 72 lichen planus patients and no one else, and follicular papules (bumps around hair follicles) mark pityriasis rubra pilaris. Not circular, since the label is the biopsy diagnosis and these are signs seen before it, and the model ranking is the same on the three hard classes alone (TabPFN better on 55/60 folds).
- The patients look selected: 93% of lichen planus patients have mouth involvement (56% of 91 biopsy-confirmed patients in Samreen A, Luqman N, Asgher R, Khalid M, Shaheen JA. Frequency of oral involvement in cutaneous lichen planus patients. J Pak Assoc Dermatol. 2021;31(3):454-458. doi:10.66344/jpad.v31i3.1817), and all 20 pityriasis rubra pilaris patients are aged 7 to 22, though the disease is most common in adults. This makes two classes easier than in a clinic but does not affect the model comparison.

Done (2026-10-20): `fit_reason` in `dataset.py` names the selected cases.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback log_loss — Guevenir et al. 1998 report cross-validated accuracy of VFI5 without costs between the six diagnoses, and we use the 12 clinical features only (MET-6).

**Assessment (AI, 2026-10-27):** The open questions for the curator are in the record's Review (review of the Tiny Data datasets, written from the earlier findings, no review panel); the AI recommends shipping it. Priority 4: gap +, use case + (the source describes the step before the biopsy), source +, shape -, risk +.
**Assessment (AI, 2026-10-27):** evidence for the Selection Bias marker of PR #16, checked on dermatology.data: 67 of the 72 lichen planus patients (93%) have oral mucosal involvement and none of the other 294 patients do, against 19% to 63% in clinic series of cutaneous lichen planus (56% of 91 biopsy-confirmed patients, https://jpad.com.pk/index.php/jpad/article/view/1817; 19% of 131, https://diposit.ub.edu/dspace/handle/2445/171919). All 20 pityriasis rubra pilaris patients are aged 7 to 22. The rows look like typical cases of each disease rather than a clinic's patients. The definition's fit_reason does not name this yet.

CC (2026-10-27, Lennart): fit approximate (was direct): a dermatologist's lichen planus patients do not show the selection of these rows, so it is a known gap (USE-8, amended on the review of PR #16); the Selection Bias marker stays.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels): 10 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `erythema`, `scaling`, `definite borders`, `itching`, `koebner phenomenon`, `polygonal papules`, `follicular papules`, `oral mucosal involvement`, `knee and elbow involvement`, `scalp involvement` (the README lists their levels).

CC (2026-11-01, Lennart): the decode rule (a code whose codebook says in words what each level is carries the words; a score without them is a number): 10 scores are numbers (erythema, scaling, definite borders, itching, koebner phenomenon, polygonal papules, follicular papules, oral mucosal involvement and more).

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target ships its class names.

**Assessment (AI, 2026-11-04):** reviewed for BeyondArena v0.2, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship the clinical-only differential diagnosis (no exclusion reason survived Andrej's audit, TabPFN beats LR on 59 of 60 splits) after typing the ten graded findings as numbers, which the definition still ships as unordered categories against its own notes and the decode rule. Priority 3: gap 1, use case 0, source 1, shape 0, risk -0.

CC (2026-11-05, Andrej): ship (issue 1, A) once the type of the ten graded findings (issue 2) is settled.

CC (2026-11-05, Lennart): GitHub issue #48 review: the 10 clinical scores 0-3 ship as numbers (the source names only the two ends of the scale); `_feature_types` declares only `family history` categorical. The declared metric (log_loss fallback) is checked.

**Assessment (AI, 2026-11-05):** the 2026-11-01 decoding made the scores numbers in `_clean`, but a blanket `_feature_types` (every column but age categorical) cast them back to unordered categories; found by GitHub issue #48. A test now checks that every `SCORES` column ships numeric.

CC (2026-11-18, Andrej): the split stays as shipped under SPLIT-8 as amended today (cross-dataset decision on the period count, full-information split check): the data holds two file parts, if they are periods at all, for a task of 20 repeats, which needs five, too few to hold out whole periods; the forced step goes on to the unit question: one row per patient, so random, as shipped.

CC (2026-11-18, Andrej): the forced tag stays (Review issue 7, A; stationarity reasoning, SPLIT-32 as amended today): no reason to take later samples as interchangeable. The rule lists structure in the file order as a fact against, and here it is measured as a sizeable cost.

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

**Main points:** Settled: ship the clinical-only task with the ten graded findings as numbers (issues 1, 2 and
4, resolved 2026-11-05); the random split is tagged forced from temporal with the measured cost of the file's two parts
(issue 3, resolved 2026-11-10), and the forced tag stays (issue 7, resolved 2026-11-18); issue 5 was withdrawn. Open since 2026-11-23: issue 8 (the file parts' class shares make the relation not flat: `Too Small`, or a departure).

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

2. **Type the ten graded findings as numbers, as the notes and the decode rule say?**

   * **Problem:**
     - `_clean` turns the ten findings graded 0 to 3 into numbers, as the curation notes and your rule of 2026-11-01
       say, but `_feature_types` still declares every column except age categorical, so they ship as unordered
       categories (the README lists them as `category`).
     - An unordered category drops the order the source gives the grades ("0 indicates that the feature was not
       present, 3 indicates the largest amount possible, and 1, 2 indicate the relative intermediate values").
     - Type them as numbers?
   * **Background:** the decode rule of 2026-11-01 makes a score with no words per level a number, and lists this
     dataset's ten findings among the columns that "are numbers again"[^2a]. The ordinal-scale change added the conversion in
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

   **Resolved (2026-11-05, Lennart):** B, on GitHub issue #48. The 10 scores ship as numbers; `_feature_types`
   declares only `family history` categorical, the contradicting note is gone, and a test checks that every `SCORES`
   column ships numeric.

3. **Time basis: the file's two parts score apart: name the random split forced from temporal?**

   * **Problem:**
     - The 12 clinical findings and the diagnosis describe the patient at one examination and the file keeps no date, but it has two parts: rows 1 to 169 in mixed order and rows 170 to 366 mostly in runs of one diagnosis, with another case mix (seborrheic dermatitis 41 against 20 patients, psoriasis 44 against 68).
     - The clinical findings tell the two parts apart (random forest ROC AUC 0.70, against 0.54 from the diagnosis alone), and a model trained on one part scores worse on the other than one trained on as many patients of both (logistic regression log loss 0.381 against 0.318 on the second part, 0.696 against 0.479 on the first), so if the parts are two periods of collection, the relation between findings and diagnosis moved between them.
     - Keep the random split as a `StationaryRelation`, tag it `ForcedIIDFromTemporal` with the measured cost, or split by file part?
   * **Background:**
     - What moves within a diagnosis: in the second part, psoriasis patients have itching graded 0.84 lower and the Koebner phenomenon (new lesions where the skin is injured) 0.77 lower on the 0 to 3 scale; pityriasis rosea patients itching 0.61 and Koebner 0.90 lower and definite borders 0.64 higher. That fits another examiner, another period, or cases added by diagnosis.
     - The 8 missing ages come in two runs of four consecutive rows (rows 34 to 37 and 263 to 266), so within each part the order looks like the order of recording; the source (Güvenir et al. 1998, not readable here) and the UCI page say nothing about the order or the period.
     - The record's facts, `Samples: Over Time` and `Time: Lost`, still fit: the parts are not dates. By the rule's questions the diagnosis is a present state, which would make a `StationaryRelation`, but the rule counts a change in practice or recording as time reaching the target, and two parts are too few for three windows, which makes the split forced[^3a].
   * **Experiments:** the raw UCI file, the 12 clinical features of the v0.2 task, untuned logistic regression and random forest:
     - Telling the parts apart (5 x 5-fold, random forest): ROC AUC 0.704 from the findings, 0.735 with the diagnosis added, 0.539 from the diagnosis alone.
     - Each part's patients in 3 folds (5 seeds), trained on the other part (169 or 197 patients) or on as many patients drawn from both parts outside the test fold: on the second part, logistic regression log loss 0.381 against 0.318 (worse on 14 of 15 folds), random forest 0.527 against 0.400 (15 of 15); on the first part, 0.696 against 0.479 (15 of 15) and 0.651 against 0.572 (12 of 15). Accuracy falls by 0.01 to 0.04.
     - The time probe of 2026-11-06 flagged the order: consecutive rows share the diagnosis 42% of the time against 20% by chance, all of it in the second part (14% in rows 1 to 169, 66% after).
   * **Effect on the task:** under the random split both parts sit on both sides, so a model learns each part's grading; if the parts are periods, a dermatologist's new patients come from a later one, and the random split flatters every model by 0.06 to 0.22 in log loss.
   * **Unknown:** whether the parts are two periods, two examiners, or one series extended by diagnosis; the authors (Güvenir, İlter) would know.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random split, `StationaryRelation` (implemented) | the shipped split; the tag and a `Time basis:` line | the diagnosis is read at the examination | the measurement contradicts it: the relation moves between the file's parts |
     | B | Random split, `ForcedIIDFromTemporal` | the shipped split; the tag and a `Time basis:` line with the two parts and the measured cost[^3b] | states what the random split hides; keeps 60 splits over all 366 patients | reads the file's parts as periods, which the source does not state |
     | C | Split by file part | train on one part, test on the other | tests the shift directly | two groups make one shift test, not a benchmark split[^3c]; the boundary is estimated from the order, not recorded |

   * **Recommendation:** B: the relation measurably moves between the two parts, and two parts cannot give the windows a temporal split needs, so the random split stays as a forced one with its cost written down. If you read the parts as another examiner rather than another time, A with the shift named. **Decision:** A, B or C?

   **Notes for the AI:** on B: `data_tags = ("ForcedIIDFromTemporal",)` and a curation bullet `- Time
   basis: ForcedIIDFromTemporal: patients examined over a period the source does not state (published 1998); the file
   keeps no date but has two parts, rows 1 to 169 in mixed order and rows 170 to 366 mostly in runs of one diagnosis.
   The clinical findings tell them apart (random forest ROC AUC 0.70; 0.54 from the diagnosis alone), and trained on one
   part, logistic regression's log loss on the other is 0.381 and 0.696, against 0.318 and 0.479 trained on as many
   patients of both parts. Read as two collection periods, too few for three windows; dates of
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
     raw row, untuned logistic regression (LR), random forest (RF) and LightGBM, log loss:
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

   **Notes for the AI:** on a: `data_tags = ("ForcedIIDFromTemporal",)` and a curation bullet `- Time
   basis: ForcedIIDFromTemporal: patients examined over a period the source does not state (published 1998); the file
   keeps no date but has two parts, rows 1 to 169 in mixed order and rows 170 to 366 mostly in runs of one diagnosis.
   The clinical findings tell them apart (random forest ROC AUC 0.70; 0.54 from the diagnosis alone). The random split
   puts both parts on both sides, so each test patient has training patients of its own part: on the shipped splits,
   logistic regression's log loss on one part's patients is 0.536 and 0.345 when it trains on a random mix of both
   parts, against 0.688 and 0.425 when it trains on as many patients of the other part alone; told the part, it
   improves by another 0.014, and the case mix of the parts adds nothing. Read as two collection
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
   part as a feature 0.014). No `splits_comment` change; record facts unchanged.

4. **Ship the 10 clinical scores 0 to 3 as numbers?**

   * **Problem:**
     - `_clean` turns the 10 scores into numbers (`SCORES`, the decoding of 2026-11-01), but `_feature_types` declares every column except `age` and the target categorical, so they ship as unordered categories (README: 12 categorical).
     - The notes contradict each other: "We encode all features but age as categorical, since they are ordinal features in nature" and "10 scores with no words per level are numbers".
     - Issue #48 found it and proposes an ordered category 0 < 1 < 2 < 3.
   * **Background:** The source gives words only at the two ends of the scale: "0 indicates that the feature was not present, 3 indicates the largest amount possible, and 1, 2 indicate the relative intermediate values" (`dermatology.names`, [UCI](https://doi.org/10.24432/C5FK5P))[^1].
   * **Effect on the task:** Unordered, a model cannot use that grade 2 lies between 1 and 3, and with 366 patients each grade as its own level splits the few patients further.
   * **Consistency:** The 15 other definitions with a `SCORES` list ship every listed column as a number (checked against each README's type list, 2026-11-05); this is the only one where a blanket categorical in `_feature_types` casts them back.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Unordered categories (implemented) | keeps the blanket cast of `_feature_types` | none found | the order of the grades is lost; contradicts the definition's own notes |
     | B | Numbers | `_feature_types` declares only `family history` categorical | the source names only the two ends; what the notes already say; as in the 15 other definitions | the step from 0 to 1 counts as much as from 2 to 3 |
     | C | Ordered categories 0 < 1 < 2 < 3 | the 10 scores in `FeatureTypes(ordinal=...)` | issue #48's proposal; keeps the order without a spacing | departs from the rule for a score without words per level |

   * **Recommendation:** B, the rule's form and what the 2026-11-01 decoding meant to ship. **Decision:** A, B or C?

   **Notes for the AI:** on B, `_feature_types` returns `FeatureTypes(categorical=["family history"])` (age stays
   numeric); remove the bullet "We encode all features but age as categorical, since they are ordinal features in
   nature." from `curation_comments`; on C, `FeatureTypes(ordinal={c: [0, 1, 2, 3] for c in SCORES},
   categorical=["family history"])` and a Cases row of kind `exception` under CLEAN-14. Then `dataset check`, a
   CHANGELOG entry, a CC line in the record.

   **Lennart (2026-11-05, change):** Option B: Numbers.

   **Resolved (2026-11-05, Lennart):** B. The 10 scores ship as numbers; `_feature_types` declares only `family
   history` categorical, the contradicting note is gone, and a test checks that every `SCORES` column ships numeric.

   [^1]: **CLEAN-14** (Should): a score or rating with no words per level, or words only at its two ends, is a
     number, as shipped; the test is whether the source says in words what each level is.

5. **`CrossSectional` instead of `ForcedIIDFromTemporal`?**

   * **Problem:**
     - The definition is tagged `ForcedIIDFromTemporal`, a forward use case whose time was lost[^fo-5].
     - The target is a present state measured with the features: the diagnosis, read from the clinical features of the same examination, and the use case reads it for new units at their own present[^cs-5].
     - The tag alone changes: the split stays random.
   * **Background:** the biopsy confirms the diagnosis after the examination, but it reports the disease the examination saw; the use case is the differential diagnosis, not a forecast.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Stay `ForcedIIDFromTemporal` (implemented) | the tag and its line stay | the decision stands | the tag claims a forecast the use case does not make |
     | B | `CrossSectional` | the tag and a `Time basis:` line naming the present state, the untested drift for later units and what a dated release would show | names the use case; no claim of a lost forward split | a new prototype on a decided tag |

   * **Recommendation:** B. **Decision:** A or B?

   **Notes for the AI:** on B, swap the tag, write the line, add a CC line; the split does not change.

   [^cs-5]: **SPLIT-32** (Should, 2026-11-13): a target measured together with the features, which the use case reads for new units at their own present, is `CrossSectional`, whether the dates survive or not; its line says whether the drift of the relation was measured or is untested. A label that only arrives later is no present state.
   [^fo-5]: **SPLIT-8** (Must): a forward use case without usable time ships in the closest regime, tagged forced from temporal, with a `Time basis:` line naming the reason.

   **Resolved (2026-11-13, Andrej):** withdrawn: `CrossSectional` was dropped the same day (it named no split the existing prototypes do not give: a present state used later is forced or a measured `StationaryRelation`, used within the covered time `Retrospective`). The tag stays.

7. **Keep `ForcedIIDFromTemporal`, or tag `AssumedStationaryRelation`?**

   * **Problem:**
     - Time: No date, but two file parts (rows 1-169 mixed, 170-366 in diagnosis runs) that the findings tell apart (RF ROC AUC 0.70); already measured as a cost, not as time.
     - Use: A dermatologist makes a pre-biopsy differential diagnosis for new patients, decades after the 1998 Ankara data.
     - Mechanism: Graded clinical findings (erythema, scaling, Koebner etc.) to the diagnosis: disease morphology is stable, but the grades are an examiner's reading, which differs between examiners and eras.
   * **Background:** similar datasets[^asr].

     | Similar dataset or source | What was measured | Verdict | Why similar |
     |---|---|---|---|
     | eryhemato_squamous_disease's own file parts | LR log loss on one part trained on a mix vs the other part | not flat: 0.536 -> 0.688 and 0.345 -> 0.425 | same data |
     | cardiotocography | class share by exam year | not flat by recording: suspect share 36% -> 1% | clinician-read diagnostic label; shows labelling practice drifting |

   * **For a stationary use case:**
     - disease morphology of psoriasis, lichen planus etc. does not change.
   * **Against:**
     - structure in the file order: the two parts score apart (0.536 vs 0.688 log loss)
     - features are subjective grades 0-3 by examiners (changed coding)
     - unstated period, used ~30 years later.
   * **Earlier views:**
     - Resolved 2026-11-10 (Andrej): random split tagged ForcedIIDFromTemporal with the parts' measured cost.
     - Resolved 2026-11-13 (Andrej): CrossSectional withdrawn, tag stays.
     - CC 2026-11-18 (Andrej): split stays under amended SPLIT-8, two parts too few for whole-period folds.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `ForcedIIDFromTemporal` (implemented) | The folds stay; the Time basis line names the reasoning below | Claims only what is known | The split stands for later samples only as far as the use case is stationary |
     | B | `AssumedStationaryRelation` | The folds stay; you give the reason (eight words or more) | Documents why random folds stand for later samples | structure in the file order: the two parts score apart (0.536 vs 0.688 log loss); features are subjective grades 0-3 by examiners (changed coding) |

   * **Recommendation:** A, the rule lists structure in the file order as a fact against, and here it is measured as a sizeable cost. Confidence: high. **Decision:** A or B?

   [^asr]: **SPLIT-32** (Should; amended 2026-11-18, Andrej): "where it holds none, the review reasons whether the use case can be taken as stationary, from the domain's mechanism and from similar datasets ..., where the AI offers `AssumedStationaryRelation` with a recommendation for a person to decide." `AssumedStationaryRelation` keeps the forced split's folds and replaces only the tag; its line opens `AssumedStationaryRelation (<person>, <date>): <reason>`.

   **Andrej (2026-11-18, ok):** as implemented.

   **Resolved (2026-11-18, Andrej):** A, as implemented: the forced tag stays; the `Time basis:` line gives the reasoning (The rule lists structure in the file order as a fact against, and here it is measured as a sizeable cost.)

8. **Keep the random split tagged forced from temporal, or retire the task as too small?**

   * **Problem:**
     - The shipped `Time basis:` line reads the file's two parts as two collection periods, and between them the share of seborrheic dermatitis falls from 24.3% to 10.2% (factor 2.4, chi-square p = 0.0005), which by itself makes the relation measured not flat[^dep-ery-flat].
     - A relation measured not flat is held out by whole periods or the task is `Too Small`; two parts are fewer than the five periods its 20 repeats need (four even for 3 repeats), so the rules give `Too Small`, retired or kept on the curator's call[^dep-ery-small].
     - The split tree does not list eryhemato as a departure; Lennart asked on 2026-11-23 that you make this call.
   * **Background:**
     - Class shares of the two parts, from the raw UCI file (rows 1 to 169 and 170 to 366):

       | Diagnosis | Rows 1-169 | Rows 170-366 | Factor | Chi-square p |
       |---|---|---|---|---|
       | psoriasis | 44 (26.0%) | 68 (34.5%) | 1.3 | 0.10 |
       | seborrheic dermatitis | 41 (24.3%) | 20 (10.2%) | 2.4 | 0.0005 |
       | lichen planus | 33 (19.5%) | 39 (19.8%) | 1.0 | 1.0 |
       | pityriasis rosea | 19 (11.2%) | 30 (15.2%) | 1.4 | 0.34 |
       | chronic dermatitis | 23 (13.6%) | 29 (14.7%) | 1.1 | 0.88 |
       | pityriasis rubra pilaris | 9 (5.3%) | 11 (5.6%) | 1.0 | 1.0 |

     - The cost measured on 2026-11-09 points the same way: trained on a mix of both parts, as the random split does, logistic regression's log loss is 0.536 and 0.345, against 0.688 and 0.425 trained on the other part alone.
     - The stationary-relation test itself would test one of the two parts only, a partial reading that is never the verdict; the class-share check needs no third period.
   * **Unknown:** whether the parts are two periods, two examiners, or one series extended by diagnosis (issue 3); the source does not say.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random split, `ForcedIIDFromTemporal` (implemented) | No change; the tree's departures table lists eryhemato with your reason | 60 splits; no rebuild | The line reads the parts as periods, and the rules then give `Too Small` |
     | B | `Too Small`: retire it, or keep it on your call with a CC line | The leaf the forced step gives for a relation measured not flat with too few periods | Follows the line as written | Loses a clinical differential-diagnosis task |
     | C | Random split, `ForcedIIDFromTemporal`, the line no longer reads the parts as periods | The `Time basis:` line names the parts as two examiners or a series extended by diagnosis, with the measured cost | With no periods nothing is measured, and the forced step gives this split; no departure | Rests on a reading of the file order the source does not state |

   * **Recommendation:** none from the AI beyond what the rules give as written: B while the line reads the parts as periods; C if you read them otherwise; A stays only as a departure you confirm with its reason. **Decision:** A, B or C?

   **Notes for the AI:** B: the record's suggestion `No (Retired)` with marker `Too Small` and a CC line, the folder leaves the working copy (or, kept on your call, the CC line only), and the split tree's "Retire · Too Small" names it. C: rewrite the `Time basis:` line as said, the tag unchanged. A: a departures-table row in `split_tree.md`.

   [^dep-ery-flat]: **SPLIT-32** (Should): the relation "is not flat when one period or the averaged gap is not flat for one model, or when a class share moves by a factor of two or more between two periods at chi-square p < 0.01 (the change in recording above)".
   [^dep-ery-small]: **SPLIT-32** (Should): "a relation measured not flat is held out only by whole periods, else `Too Small` (SPLIT-16)". **SPLIT-16** (Must): "where enough meaningful groups can be built to approximate the temporal split (whole periods, enough for the task's repeats, SPLIT-8), hold them out; where they cannot, the task is `Too Small`." **SPLIT-8** (Must): whole periods count only with "four periods for 3 repeats, five for 10 or 20". The split tree, ForcedFromTemporal step: "Retire · Too Small ... retired or kept only on the curator's call".

## Reference

@article{guvenir1998learning,
  title={Learning differential diagnosis of erythemato-squamous diseases using voting feature intervals},
  author={G{\"u}venir, H Altay and Demir{\"o}z, G{\"u}l{\c{s}}en and Ilter, Nilsel},
  journal={Artificial intelligence in medicine},
  volume={13},
  number={3},
  pages={147--165},
  year={1998},
  publisher={Elsevier},
  doi={10.1016/S0933-3657(98)00028-1}
}
