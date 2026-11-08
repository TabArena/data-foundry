# dementia_prediction

**Outcome:** added. In the working copy since the migration; a scan of 2026-11-08 for units with unequal numbers of
rows (raised on boreal_postfire_lichen_biomass's issue 7) found that the log loss counts a person once per visit, 1 to
5 times, while the use case is a first visit. Resolved on 2026-11-08: each person counts once in the log loss
(issue 1).

**Main points:** Open: none. Resolved on 2026-11-08: each person counts once in the log loss, weighted by 1 over the
person's visits (issue 1).

**Issues for Lennart:**

1. **Count each person once in the log loss, score only the first visits, or each visit, as now?**

   * **Problem:**
     - A row is one visit, and the 150 people of OASIS-2 have 1 to 5 visits each (91 two, 43 three, 13 four or five), so a person seen five times counts five times in the log loss.
     - The use case is a first visit at a memory clinic, but follow-up visits of test people are scored as if each were a first visit, and each visit has its own rating (31 people change it).
     - Should each visit weigh 1 over its person's number of visits, so that each person counts once, or should only each test person's first visit count?
   * **Background:**
     - 370 visits of 150 people (the 3 visits rated moderate dementia are dropped, all of them follow-ups); a test fold
       holds about 50 people and 112 to 138 visits.
     - The inputs differ between visits (age, the cognitive test score, the MRI measures), and so can the rating; a
       model gives each visit its own prediction, and the weight changes only how much each visit counts.
     - The first visit is OASIS-2's visit 1, which the definition drops as a feature and would keep as a scoring
       column only; every person has one among the shipped rows. At first visits the ratings are 57% no dementia, 35%
       very mild and 9% mild, against 56%, 33% and 11% over all visits.
   * **Rules:** the use case decides what one prediction is and at which unit the score counts[^dp-unit]. Neither
     weight follows from the inputs, so B and C accept the check's warning with a reason the rules do not name yet (a
     weight that gives each unit one vote), as for pancreatic_cancer_mouse_detection[^dp-weight].
   * **Effect on the task:** per visit, people followed longer weigh more, and with them the follow-ups, rated mild a
     little more often (13% of the 220 follow-ups against 9% of the first visits); per person, each person counts once;
     first visits only, the score asks exactly what the use case asks, on less than half the test rows. Training keeps
     every visit under all three.
   * **Experiments:** 8 untuned predictors (two logistic regressions, random forest, extra trees, two LightGBM, kNN and
     the class shares) on the 60 shipped splits, re-run on 2026-11-08 for option C (the scan's first 30 splits give
     about the same taus for B: 0.94 per split, lowest 0.71, 1.0 for the mean). Kendall tau measures how far two orders of the models agree, 1 when they are the same.
     - Per person against per visit: tau 0.94 per split on average (lowest 0.71) and 1.0 for the ranking by the mean
       over the splits; the same best model on 56 of 60 splits.
     - First visit only against per visit: tau 0.87 per split (lowest 0.57) and 0.93 for the ranking by the mean
       (extra trees and the strong logistic regression swap, 0.750 and 0.751); the same best model on 49 of 60 splits,
       on 48 to 52 scored visits per fold.
     - The logistic regression leads under all three (log loss 0.62 per visit, 0.67 per person, 0.59 on first
       visits).
   * **Consistency:**
     - boreal_postfire_lichen_biomass counts each plot once since 2026-11-08[^dp-boreal]; there every input belongs
       to the plot, here none of the visit's measurements do.
     - The same scan raised superconductivity (per composition) and pancreatic_cancer_mouse_detection (per mouse).
     - sepsis_survival_minimal_clinical_records and wids_diabetes_mellitus score each admission of a returning patient
       per row (each admission a decision); here the use case is a first visit.
   * **Panel:** none; raised by the one-vote-per-unit scan of 2026-11-08 (boreal_postfire_lichen_biomass issue 7).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Per visit (implemented) | log loss over all visits | every rated visit scored; nothing changes | a person counts by the number of visits, 1 to 5; follow-ups scored as first visits |
     | B | Each person counts once | log loss weighted by 1 over the person's visits, a scoring column for the metric only; log loss first gets an optional weight input | one vote per person, the clinic's unit; ranks models as per visit (tau 1.0 for the mean) | a framework change; the check's warning accepted with a reason the rules do not name yet; follow-ups still scored as first visits |
     | C | First visit only | weight 1 on each test person's first visit and 0 on the follow-ups, from OASIS-2's visit number, for scoring only; same framework change as B | scores exactly the first-visit use case; one vote per person | 48 to 52 scored visits per fold instead of 112 to 138, a noisier score; the same framework change |

   * **Recommendation:** B: the clinic acts once per person, and B keeps every visit in the score; C if the score
     should match the first-visit framing exactly, at the cost of more than half the scored rows. **Decision:** A, B or
     C?

   **Notes for the AI:** on B or C: (1) `log_loss` takes no `weight` today; give it an optional row weight in
   `src/data_foundry/v2/metrics.py` (scikit-learn's `sample_weight`, `optional_inputs=("weight",)`,
   `weighted_definition` so the unweighted spec stays unchanged), with a test; one change serves
   asp_potassco_classification too if its issue 5 goes that way; (2) in `_clean`, before `Visit` is dropped, add
   `person_weight` (B: `1.0 / df.groupby("Subject ID")["Subject ID"].transform("size")`, after the moderate visits are
   dropped) or `first_visit_weight` (C: `(df["Visit"] == 1).astype(float)`), declared as a `ScoringColumn(...,
   role="weight", used_by="log_loss")`; (3) `Metric.fallback(reason=..., inputs={"weight": ...})`, the reason naming
   the weighting; no `sample_weight`; (4) accept `task_metric_weight_without_sample_weight` with the reason used for
   pancreatic_cancer_mouse_detection (a design weight of the score that gives each person one vote, SPLIT-23; not an
   amount at risk, MET-15; not a survey weight, MET-16); (5) on C, the `fit_reason` sentence "Follow-up visits of test
   people are scored as if each were a first visit" goes, and the task summary's `split` says only first visits are
   scored; on B, the grouping's definition adds that each person counts once; (6) `dataset check`, the CC line, a
   CHANGELOG entry, a Cases row in metrics.md. On A: a note that a person counts by the number of visits (tau 0.94 per
   split against one vote per person). The re-run: `one_vote_scan/apply_2026-11-08/dementia_first_visit.py` in the
   exposure review's run folder.

   [^dp-unit]: **SPLIT-23** (Must): the source's use case, cited, decides what one prediction is (a row, or a whole
     group). **MET-1** (Must): the declared metric scores the real task, at the unit the actor acts on.
   [^dp-weight]: **MET-15** (Must): a metric weight that is a function of the features needs no sample weight, and
     the bundle check `task_metric_weight_without_sample_weight` is then accepted with that reason; a realized amount
     at risk is also the training weight. A weight that gives each unit one vote and does not follow from the inputs
     is not named.
   [^dp-boreal]: boreal_postfire_lichen_biomass, issue 7, Lennart, 2026-11-08: "Option B: Each plot counts once."

   **Lennart (2026-11-08, change):** Option B: Each person counts once.

   **Resolved (2026-11-08, Lennart):** B, each person counts once. `log_loss` got an optional `weight` input, and the
   log loss is weighted by `person_weight`, 1 over the person's number of visits, a scoring column for the metric only
   with no training weight (Lennart's rule of 2026-11-08: a one-vote weight is for scoring only; training with it
   measured -0.004 log loss, within noise). Follow-up visits stay scored as if each were a first visit, at one vote
   per person; the notes, the metric's reason and the record say so.
