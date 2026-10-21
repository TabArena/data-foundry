# The metric that scores a task

Part 6b of the curation rules, under P6 (worth benchmarking) in [principles.md](principles.md), after
[task_probes.md](task_probes.md): a TP rule wins a conflict with a MET rule of the same strength. The rules of earlier
parts win over this file's rules in a conflict; within this file a rule wins over the rules below it of the same
strength. How to weigh, exceptions and amendments: [principles.md](principles.md).

Which metric a dataset declares, where it comes from, and how the data is made to fit it. The curator's aim (Lennart,
2026-10-21): "keep the best metric for the task that would have been used in practice". The metric the source used is
evidence of that, strong for a competition and weak for a paper that reported accuracy because it was the field's
habit. The rules come from the curator's decisions of 2026-10-21 and the metric sweep of that day over all 173
definitions of the TabArena v0.2 working copy (it proposed the source's metric for 106, a stand-in for 12 and the
fallback for 55; 21 of the 106 are accuracy, which these rules send back to the curator).

**Why this rank.** A metric problem never excludes a dataset: every task can be scored by a fallback, so a wrong
metric is always fixed in the definition and never reaches the remedy of exclusion that a validity problem (P1-P5) can.
It also follows the higher parts and never leads them. The use case (P3) says what the metric has to measure, and the
split (P4) follows the application: a metric is matched to the split, and the split is changed for a metric only when
the use case asks for the same change (MET-2).

The evidence base, cited by short name:

* **Provost et al. 1998**: F. Provost, T. Fawcett, R. Kohavi, "The case against accuracy estimation for comparing
  induction algorithms", ICML 1998 (the reading of D. Page's CS 760 course,
  <https://pages.cs.wisc.edu/~dpage/cs760/roc.pdf>). Accuracy assumes equal error costs and a known target class
  distribution, which most real tasks and most benchmark releases do not have (a stratified or re-balanced sample
  does not show the natural distribution); on ten UCI datasets no learner's ROC curve dominated, so an accuracy
  comparison picks a model that is better at one operating point only; without costs and class distribution, no
  single threshold number supports a strong claim, while ROC analysis holds for every cost and prior.
* **Vickers & Elkin 2006**: A. Vickers, E. Elkin, "Decision curve analysis: a novel method for evaluating prediction
  models", Medical Decision Making 26(6):565-574. The threshold probability p_t at which a patient opts for treatment
  states how they weigh a false positive against a false negative; the net benefit at p_t is
  TP/n - FP/n x p_t / (1 - p_t), and a model's value is read over the range of thresholds that are reasonable for
  the decision. (Paywalled here: read from the abstract and the method's well-known formula.)
* **Gneiting & Raftery 2007**: T. Gneiting, A. Raftery, "Strictly proper scoring rules, prediction, and estimation",
  JASA 102(477):359-378. A strictly proper scoring rule (log loss, the Brier score) has its unique optimum at the true
  predictive distribution, so it rewards honest probabilities; it is a loss that can be tailored to the problem at
  hand. A probability scored by a proper rule serves every later threshold and cost. (Paywalled here: read from the
  abstract and the paper's well-known results.)
* **McDermott et al. 2024**: M. McDermott, H. Zhang, L. Hansen, G. Angelotti, J. Gallifant et al., "A closer look at
  AUROC and AUPRC under class imbalance", NeurIPS 2024, <https://arxiv.org/abs/2401.06091>. AUPRC is not in general
  better than AUROC under class imbalance: AUROC weighs every mis-ordered positive-negative pair the same, AUPRC
  weighs the mistakes among the highest scores more, which favours gains in subpopulations with more positives and
  can widen disparities; the claim that AUPRC suits imbalance is mostly repeated without a source.

## Rules

### What the metric measures

**MET-1 (Must).** The declared metric scores the real task: the decision of the use case (USE-1), at the unit the
actor acts on, the way a practitioner would have chosen a model for it in practice. Look before falling back: the
competition's evaluation page, the task description, the paper that defined the task (which may be later than the
data's first publication: TableShift for anes_voting_2026, Chicco & Jurman 2020 for
sepsis_survival_minimal_clinical_records), and record where you looked. Every definition declares a metric with its
origin (MET-11); none is left to a silent default.

**MET-2 (Must).** Match the data, the metric and the real task. Before declaring a metric, check on the shipped data
that:
* its unit of evaluation exists in our data: per row, per patient, per customer, per era, per week, per instance;
* every input it needs ships as a column and is never a feature (a group, a time, a weight, an onset hour), and the
  test fold holds what the metric reads: whole patient stays for a per-patient utility, several eras or weeks per
  window for a per-era correlation or a slope over weeks, enough positives for the top k, every class the cost
  matrix names;
* the metric means on our task what it meant on the source's: same target, same classes, same class balance. A task
  we changed (classes merged or dropped, a balanced sample replaced by the full release, duplicates removed) keeps
  the source's metric only when its meaning survives the change.

When the data falls short, adapt the data first if the use case agrees (ship the column, keep whole groups in a test
fold, scale a fixed k to the fold); otherwise declare a stand-in or the fallback. The split is never changed for a
metric against the use case (P4 wins; [splits.md](splits.md)). Cases: sepsis_prediction_1m (the 500k row cap trims
3,371 rows from a test fold and can cut a stay's hours; the challenge's utility needs whole stays),
home_credit_default_stability_1m (about 9 weeks per test window for a weekly slope), coil_2000 (k = 800 of 4,000
becomes the top 20% of each fold), emscad and taiwanese_bankruptcy_prediction (the paper's accuracy was on a 1:1
sample; the release is 4.6% and 3.2% positive), naticusdroid_android_permissions_dataset (balanced with 75%
duplicates in the paper, 35% positive after we dropped them).

**MET-3 (Must).** The declared metric is computed on the scale the source scored. Ship the target on that scale: a
transform the definition applied for modelling (log1p of a skewed target) is undone when the source's metric is
defined on the raw scale, because a metric on another scale is another metric (MAE on a log target is close to a
median relative error, not an error in hectares). Keep a transformed target only when the transform is how the metric
is defined: RMSLE is RMSE on log1p(y), so a log1p target with `rmse` is the source's RMSLE, and declaring `rmsle` on
it logs the target twice. "If the goal is to use the transform only for scoring we can keep it that way, but generally
speaking we can adapt the data to these needs" (Lennart, 2026-10-21). Cases: forest_fires (MAD in hectares, target
shipped as log1p), allstate_claims_severity (MAE on the raw loss, target shipped logged), mercari_price_suggestion
and pkdd_15_taxi_trip_time_prediction_ii_1m (RMSLE as RMSE on log1p), santander_transaction_value (`rmsle` on a log1p
target, a definition bug).

### Whose metric to trust

**MET-4 (Should).** A competition's leaderboard metric is the source's metric: declare it. The organisers chose it for
their decision and every team optimised it (Kaggle, Zindi, DrivenData, PhysioNet/CinC, KDD Cup, an industrial
challenge). It is overruled only by MET-2 or on evidence that it is biased or wrong for the use case, from the source
(a metric the forum shows was gamed) or measured on the shipped splits, written in the notes with its numbers. A
competition that scored hard labels has fixed that the decision is a hard label, so its threshold metric (F1, a cost
matrix) is kept: methods choose their threshold on the training side. Cases: zillow_prize, mercari_price_suggestion,
amex_non_iid_1m, african_credit_scoring_challenge, force_2020.

**MET-5 (Should).** A paper's metric is the source's metric only when it is one deliberate choice: the paper names it
as the criterion it ranks, tunes or selects models by, or argues why it fits the decision. A paper that reports
several metrics side by side (accuracy, precision, recall, F1, AUC) without naming the one that decides has no unique
original: declare the fallback, and list the reported metrics in the reason. "If papers report multiple metrics, they
did not have a unique one and then we should fall back" (Lennart, 2026-10-21). A headline number in the abstract is
not by itself a deliberate choice. Cases: gallstone_disease and early_stage_diabetes_risk_prediction (accuracy with
precision, recall, F-measure: fallback), forest_fires (MAD and RMSE, ranked by MAD: kept), labour_inspection_compliance
(Sec. 6.5 argues precision at the median score is "the most important statistic": a deliberate choice).

**MET-6 (Should).** A threshold metric (accuracy or error rate, balanced accuracy, NER or BER, F1, precision, recall,
precision at k, a misclassification cost) is declared from a paper only when the source fixes the decision (the
threshold, the k, or the cost matrix) and the task acts on hard decisions at that point. Without them a hard-label
score measures the threshold a method happened to pick (0.5 by default) as much as the model, assumes equal costs and
the test class balance (Provost et al. 1998), and is coarse on small folds. Most papers on UCI-era data report
accuracy because the field did, not because the decision called for it: "In many cases, like all that used accuracy,
the author did not know better" (Lennart, 2026-10-21). Be critical, judge each case by the use case, and declare the
fallback when the paper's threshold metric is a habit. Competitions fall under MET-4. Cases: ljubljana_breast_cancer,
heart_disease_cleveland, clock_protein_toxicity, credit_approval (accuracy or error rate, no threshold or costs:
fallback proposed), covertype (a single deliberate accuracy, hard labels per map cell: kept, proposed).

**MET-7 (Should).** When the source fixes a cost matrix, a single treatment threshold or a k from its decision, declare
that metric (`cost_matrix`, `precision_at_k`): the costs are the use case. A threshold probability p_t at which an
actor acts states the relative harm of a false positive and a false negative, odds p_t / (1 - p_t) (Vickers & Elkin
2006), so the net benefit at one fixed p_t is a cost matrix. Score the mean cost per row, not the total, since our
folds differ in size from the source's test file. The cost is scored on hard labels (the method picks its threshold),
or on probabilities turned into the decision of least expected cost (for two classes, predict positive above
c_fp / (c_fp + c_fn)); the definition says which. Never invent a cost or a threshold: a source that gives a range of
costs or thresholds (a decision curve, cost ratios 1 to 5) fixes no single one, so its task is scored by a
threshold-free metric. Cases: credit_g (Statlog's 5:1 matrix), aps_failure (IDA 2016: 10 per false alarm, 500 per
missed failure), force_2020 (12 x 12 penalty matrix), taiwanese_bankruptcy_prediction (cost ratios 1 to 5: no single
matrix).

### What to prefer for the same goal

**MET-8 (Should).** For the same goal, prefer the probabilities. When no threshold metric is fixed (MET-6, MET-7) or
the source has no unique metric (MET-5), score classification by a strictly proper scoring rule or a ranking metric:
the fallback, `roc_auc` for binary and `log_loss` for multiclass tasks, `rmse` for regression. A strictly proper rule
is optimised only by the true probabilities (Gneiting & Raftery 2007), and a probability serves any threshold and cost
a user later picks; ROC AUC holds for every cost and class prior (Provost et al. 1998). A source that scores
calibration together with hard-label accuracy (Detrano 1989's reliability and percent correctly classified) asked for
probabilities. "Probabilities are often better metrics for the same goal" (Lennart, 2026-10-21).

**MET-9 (Should).** Class imbalance alone is no reason for the area under the precision-recall curve over ROC AUC
(McDermott et al. 2024). AUROC weighs every mis-ordered positive-negative pair the same; AUPRC weighs the errors among
the highest scores and moves with the prevalence (its floor is the positive share). Declare `average_precision` when
the source chose it as its criterion and the decision acts only on the top of the ranking (the few cases a team can
follow up); when the source fixes how many it acts on, `precision_at_k` says it directly (MET-7). An AUPRC whose
positive class is the majority, or whose floor is near its ceiling on our folds, resolves models poorly: evidence to
overrule it (MET-5, MET-4). Cases: sepsis_survival_minimal_clinical_records (PR AUC on the 92.6% majority class, floor
0.926, best 0.966: fallback proposed).

**MET-10 (Weigh).** Factors on a borderline call between the source's metric and the fallback:
* the source's track record: a competition > a paper that argues its metric > a paper that reports one metric > a
  paper that reports several;
* the resolution on our folds: a hard-label score on a few dozen test units moves in steps of a few percent (musk: 34
  molecules per fold);
* the ceiling: a metric near its best for every method no longer tells methods apart;
* whether our task is still the source's (MET-2): changed classes or balance weaken the source's claim.

### How to declare it

**MET-11 (Must).** Every metric has one origin, and the notes name the original whenever the declared metric is not
exactly it:
* **source**: what the source scored, computed on our data. A metric that ranks every pair of models the same by
  identity counts (RMSE on log1p(y) for RMSLE; ROC AUC for a binary normalized Gini, which is 2 x AUC - 1); the
  `definition` says the identity.
* **stand-in**: the source has a unique metric that cannot be computed on our data (inputs not published, a task we
  changed), and the closest computable metric replaces it; it names the original and why the original cannot be
  computed, and the closeness is measured on the shipped splits where possible (pooled Pearson within 0.0002 of
  per-era CORR, numerai_v5_2_1m).
* **context** (Lennart, 2026-10-21, diamonds): the source defines no metric, but the task makes one obvious, so the
  default would score the wrong thing; the reason says why (a price's error matters relative to the price, so
  `rmsle` on the price in dollars). Only when the context is clear; otherwise the fallback.
* **fallback**: the source defines no metric, or none the task would use in practice (MET-5, MET-6, MET-9), and the
  task makes none obvious; roc_auc, log_loss or rmse by problem type. The reason says where we looked and, when we
  rejected the source's metric, which one and why.
* For a multiclass task, prefer log loss to a multiclass ROC AUC (one-vs-rest or one-vs-one averages): an average of
  binary rankings does not score the class probabilities a decision uses (Lennart, 2026-10-21,
  biogeographical_ancestry_prediction).

**MET-12 (Must).** Standard metrics carry their standard, scikit-learn style names (`roc_auc`, `log_loss`, `mae`,
`f1_weighted`, `average_precision`). A custom metric gets a general name for what it computes (`cost_matrix`,
`precision_at_k`, `weighted_pearsonr`, `mean_group_pearsonr`, `gini_stability`,
`normalized_early_detection_utility`), never a dataset's or a competition's name; the dataset's parts (the matrix,
k, the weights, the time offsets) are its parameters. One metric has one spelling across the collection. Cases:
force_2020's `force_2020_penalty_matrix` and amex_non_iid_1m's `amex_metric` renamed to general names.

**MET-13 (Must).** A custom metric is shipped with the dataset that needs it, as a reference implementation in the
shared metric library, in the same change. It is the fastest well-tested code available: a statistics library where
it covers the metric, otherwise vectorised array code, or for a competition whose official code is slow, the faster
versions posted in its discussions, checked. It is tested to equal the official implementation on random inputs (to
1e-9 or exactly), on one case computed by hand, and timed on 1M rows. A metric only one definition holds is never
shipped: a reader of the files could not compute it. How in Data Foundry:
[definitions.md](../../knowledge-data-foundry/references/definitions.md), "Metrics".

## Patterns

| The source | Declare | Rules |
|---|---|---|
| A competition's leaderboard metric, computable on our data | it (`Metric.source`) | MET-4 |
| A competition's metric that needs inputs we cannot ship | the closest computable (`stand_in`) | MET-2, MET-11 |
| A paper's one deliberate metric that suits the decision | it | MET-5 |
| A paper reporting accuracy, precision, recall, F1, AUC | the fallback | MET-5 |
| A paper's accuracy, no threshold, no costs | the fallback, unless the use case acts on hard labels at equal costs | MET-6, MET-8 |
| A cost matrix or one treatment threshold fixed by the source | `cost_matrix` (mean cost per row) | MET-7 |
| A range of costs or thresholds | the fallback | MET-7 |
| A metric on the raw scale, a target shipped transformed | ship the raw target | MET-3 |
| RMSLE | a log1p target with `rmse` | MET-3, MET-11 |
| No metric anywhere | the fallback, with where we looked | MET-1, MET-11 |

## Cases

Precedents: how a rule was applied. They never change a rule; an exception is listed with the fact that set it apart.
The rows marked `proposed` come from the metric sweep of 2026-10-21 (`local-data-warehouse/_runs/2026-10-21_metrics/`)
and wait for the curator; the others are decided.

| Rule | Dataset | Decision | Decisive evidence | Kind |
|---|---|---|---|---|
| MET-4 | zillow_prize | `mae`, the competition's metric (2026-10-21) | Kaggle scored MAE on logerror; RMSE had been kept as the house default; 0.38% of the rows (absolute logerror above 1) hold 49.9% of the squared error | applied |
| MET-4, MET-12 | amex_non_iid_1m | `gini_top_capture` (top 4%, negatives weighted 20), per customer | the competition's M = 0.5 (G + D); the dataset-named `amex_metric` renamed; the official pandas code is slow on 460k customers | proposed |
| MET-4, MET-6 | african_credit_scoring_challenge | `f1`, the competition's metric (2026-10-21) | Zindi scored F1 on submitted labels; ROC AUC had been kept as the house default | applied |
| MET-4, MET-7, MET-12 | force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition | `cost_matrix` with the competition's penalty matrix (2026-10-21) | a published 12 x 12 penalty matrix over hard labels (11 x 11 after Basement was dropped); no standard metric ranks the same | applied, renamed from `force_2020_penalty_matrix` |
| MET-4 | digicow_farmer_training_adoption_challenge | `log_loss` (2026-10-21) | Zindi's rubric (log loss 0.75, ROC AUC 0.25 over the 7-, 90- and 120-day targets) scores targets the task does not ship; on the shipped 7-day target log loss carries 0.65 of 0.80 | applied |
| MET-11 | porto_seguro | `roc_auc` for the normalized Gini (2026-10-21) | for a binary target the normalized Gini is 2 x ROC AUC - 1, so the two rank models the same | applied |
| MET-2, MET-11 | numerai_v5_2_1m | `pearsonr` standing for per-era CORR (2026-10-21); `mean_group_pearsonr` on the `era` scoring column proposed | pooled Pearson within 0.0002 of CORR per model, Kendall tau 0.89-0.93 with its ranking; `era` ships, so the original is computable | applied, proposed |
| MET-3, MET-11 | mercari_price_suggestion | `rmse` on the log1p price, the source's RMSLE | Kaggle scored RMSLE; the target is already log1p, so RMSE on it equals RMSLE on the price | proposed |
| MET-3, MET-5 | forest_fires | `mae` on the burned area in hectares, the target shipped raw | Cortez & Morais 2007 report MAD and RMSE and rank by MAD (SVM with 4 weather inputs, MAD 12.71; the mean predictor has the best RMSE); MAE on the shipped log1p target would be another metric | proposed |
| MET-5 | gallstone_disease | fallback `roc_auc` | Esen et al. 2024 report accuracy, precision, recall, F-measure and AUC; accuracy is the headline, none is named as the criterion | proposed |
| MET-6 | ljubljana_breast_cancer | fallback `roc_auc` | every 1986-1988 paper reports accuracy only, without costs or a threshold; 30% recurrence on 286 rows | proposed |
| MET-6, MET-8 | heart_disease_cleveland (and _hungary, _va_long_beach) | fallback `roc_auc` | Detrano 1989 scores reliability (calibration in the large) and percent correctly classified: two criteria, one of them about probabilities | proposed |
| MET-7 | credit_g | `cost_matrix` (bad as good costs 5, good as bad costs 1) | Statlog's cost matrix in german.doc and the Statlog book's average cost; from probabilities, the Bayes decision is p(bad) > 1/6 | proposed |
| MET-7 | aps_failure | `cost_matrix` (false alarm 10, missed failure 500), mean per row | the IDA 2016 challenge scored total cost on its 16,000-row test file; ROC AUC is at 0.99 | proposed |
| MET-2, MET-7 | taiwanese_bankruptcy_prediction | fallback `roc_auc` | Liang et al. 2016: average accuracy on a 1:1 sample (the release is 3.2% bankrupt) and a cost with ratios 1 to 5: no single matrix | proposed |
| MET-9 | sepsis_survival_minimal_clinical_records | fallback `roc_auc`, PR AUC named as the original | Chicco & Jurman 2020's "principal indicator" is PR AUC with Alive (92.6%) as positive: floor 0.926, best 0.966 | proposed |
| MET-2, MET-12 | sepsis_prediction_1m | `normalized_early_detection_utility` with `Patient_ID` and `Hour` as scoring columns, after the data checks | the PhysioNet/CinC 2019 utility is per patient and hour around onset; the 500k cap trims 3,371 rows from a test fold and can cut a stay: check every test stay is whole and the onset hour is derivable; renamed from `PhysioNet2019UtilityFunction` | proposed |

## In Data Foundry

How a definition declares the metric (`Metric.source`, `Metric.stand_in`, `Metric.fallback`), the scoring columns and
the spec in the container, and how to add a custom metric to `src/data_foundry/v2/metrics.py` and test it:
[definitions.md](../../knowledge-data-foundry/references/definitions.md), "Field mapping" and "Metrics".
