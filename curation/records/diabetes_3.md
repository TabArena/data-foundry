---
unique_name: diabetes_3
name: Diabetes
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
priority: 1
tags:
- Tiny Data
- 'Samples: Over Time'
- 'Time: Lost'
- 'Target: Fixed Delay'
- Clinical Study
collections:
- TabSTAR
original_source: Website
year: '2002'
collection_period: Unknown
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.1214/009053604000000067
- https://hastie.su.domains/Papers/LARS/diabetes.data
v2_path: datasets/_dev/tabarena-v0pt2/diabetes_3/dataset.py
source_row: 785
type_adapter_id: curation-record-v1
---

## Comments

scikit-learn toy dataset

Unclear if too trivial?

Let us use the version of the data without normalization and the correct headers.

The original source of the data is supposedly from the same group as the referenced paper. Unclear in general, but should be fine as it is used so much

**Assessment (AI, 2026-10-07):** The data traces to Efron et al. (2004) and Hastie's LARS page (since 2002, with the headers `age sex bmi map tc ldl hdl tch tg glu y`). It does not look like the paper's "442 diabetes patients": read as fasting glucose in mg/dL, `glu` runs 58-124 (mean 91), so none reaches 126. No source gives the clinic, the units or how the response is measured (criterion 4E, against the accepted unclear source). Not trivial: on all 60 splits the best single feature, chosen on the training side, reaches R^2 0.30 against 0.49 for the best of least squares, ridge and a random forest, and stays below them on every split. Suggest dropping `Trivial`.

**Assessment (AI, 2026-10-20):** priority 1 for the review of the added dataset: gap -, use case -, source -, shape -, risk - (Issue 1: response, units and cohort undocumented; maybe not diabetics; alternative is to retire). A classic tiny regression (442 rows) used everywhere, but the cohort and the target are undocumented; it adds little beyond a familiar toy benchmark.

**Assessment (AI, 2026-10-20):** re-check by the review panel: ship after changes, once the curator rules on USE-5 (the mediator; otherwise `No`, `No Good Target`). No leak, the random split is right, and the task is not trivial (the best single feature stays below least squares, ridge and a random forest on 60 of 60 splits, by at least 0.08); the definition now has `fit="approximate"` with the gap named. Open: no source says what the label measures, nor the clinic, the units or the inclusion rule, so whether USE-5 is met is the curator's reading or an amendment, decided with mobile_churn (Review issue 1). Under PROV-8 the source links would be the DOI and the LARS page, with OpenML 44223 as the copy scaled over all rows; the `Trivial` marker has no proof (both are record-field rows in the Review). Priority 1: gap -, use case -, source +, shape -, risk - (use case: the fit is approximate and the decision is ours; source: a peer-reviewed paper and the authors' page; shape: 442 patients; risk: the label's quantity is undocumented and USE-5 is open).

CC (2026-10-21, Lennart): on the USE-5 question (Review issue 1): "In general, I would like to keep the data and just mark it as approximate, and we can case-by-case decide the details." USE-5 amended: a label from a named publication whose construction is undocumented may ship with fit approximate and a note naming the gap; kept as defined.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback rmse — the LARS paper illustrates variable selection, no held-out score.

CC (2026-10-26, Lennart): the record's fields as the definition has them. source_links: the paper's DOI and the authors' file on Trevor Hastie's LARS page (PROV-8). The earlier links are copies: OpenML 44223 (https://www.openml.org/d/44223) ships the features scaled over all 442 rows, and https://www4.stat.ncsu.edu/~boos/var.select/diabetes.html is a later copy. The `Trivial` marker is removed (TP-4: the best single feature, chosen on the training side, stays below least squares, ridge and a random forest on all 60 shipped splits, mean R^2 0.31 against 0.48).

CC (2026-10-26, Lennart): verdict ship.

CC (2026-11-17, Andrej): the declared split (random, 20x3 folds, `ForcedIIDFromTemporal`) is checked: the split decision tree, walked without the current split, reaches the split it ships (blind split walk).

CC (2026-11-18, Andrej): the forced tag stays (Review issue 1, A; stationarity reasoning, SPLIT-32 as amended today): no reason to take later samples as interchangeable. With the target undocumented there is no domain mechanism to rest ASR on.

## Review

**Outcome:** added. Stationarity reasoning of 2026-11-18: the definition reaches the forced step with no time to measure; decided below (issue 1, A, 2026-11-18).

**Main points:** Task gamer (blind, 2026-11-27): nothing gamed. Ridge RMSE 55.11 (50.0 to 61.0 over 60 splits; a random column adds 0.20) beats untuned boosting (59.03); row position, ranks over all rows, neighbouring rows' labels and number formats change it by at most 0.36, against a split spread of about 4; no duplicate rows, 1-NN no better than the mean (77.9 against 77.2); a format-only model is worse than the mean. The features ship in raw units, so the scaling leak of the scikit-learn copy does not apply. Re-audited on 2026-11-27: nothing to decide. The values are raw, not standardised (age 19-79, glucose 58-124), so read as mg/dL no glucose reaches the diabetes threshold of 126, as the definition says. The derived columns hold (the Friedewald LDL matches on 438 of 442 rows), the number formats carry no target signal, and the best method beats the best single feature on all 60 splits. The sex codes have no sourced mapping; HDL and blood pressure fit 1 = female and 2 = male, but that is an inference, so keeping them unlabelled is right. Earlier: `ForcedIIDFromTemporal` stays (issue 1, A, 2026-11-18). Nothing is left open.

**Issues for Andrej:**

1. **Keep `ForcedIIDFromTemporal`, or tag `AssumedStationaryRelation`?**

   * **Problem:**
     - Time: Lost: Efron et al. 2004 (LARS) baseline visits, clinic, period and inclusion undocumented; no date, no trend in file order.
     - Use: A physician predicts one-year progression at a baseline visit for future patients, decades after collection.
     - Mechanism: Baseline BMI, blood pressure and lipids to an undocumented progression score; neither the response's measurement nor the cohort is known, so no mechanism can be named.
   * **Background:** similar datasets[^asr].

     | Similar dataset or source | What was measured | Verdict | Why similar |
     |---|---|---|---|
     | diabetes_130_us | nine encounter-order windows 1999-2008 vs random folds | small shift: LightGBM ROC AUC 0.654 vs 0.662 (first stays 0.625 vs 0.643) | hospital outcome from routine clinical data over a decade |
     | Davis SE et al., 'Calibration drift in regression and machine learning models for acute kidney injury', JAMIA 2017;24(6):1052-1061 (literature, cited from memory: check) | VA hospital models over 9 years | discrimination stable, calibration drifted | routine-lab clinical risk model used years after fitting |

   * **For a stationary use case:**
     - BMI, BP and lipids are physical/physiological measurements.
   * **Against:**
     - the response is undocumented, so no mechanism can be argued.
     - diabetes treatment and diagnostic thresholds changed since the late 1990s.
     - period and span unknown.
   * **Earlier views:**
     - CC 2026-11-17 (Andrej): random 20x3 ForcedIIDFromTemporal checked by blind walk.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `ForcedIIDFromTemporal` (implemented) | The folds stay; the Time basis line names the reasoning below | Claims only what is known | The split stands for later samples only as far as the use case is stationary |
     | B | `AssumedStationaryRelation` | The folds stay; you give the reason (eight words or more) | Documents why random folds stand for later samples | the response is undocumented, so no mechanism can be argued; diabetes treatment and diagnostic thresholds changed since the late 1990s |

   * **Recommendation:** A, with the target undocumented there is no domain mechanism to rest ASR on. Confidence: high. **Decision:** A or B?

   [^asr]: **SPLIT-32** (Should; amended 2026-11-18, Andrej): "where it holds none, the review reasons whether the use case can be taken as stationary, from the domain's mechanism and from similar datasets ..., where the AI offers `AssumedStationaryRelation` with a recommendation for a person to decide." `AssumedStationaryRelation` keeps the forced split's folds and replaces only the tag; its line opens `AssumedStationaryRelation (<person>, <date>): <reason>`.

   **Andrej (2026-11-18, ok):** as implemented.

   **Resolved (2026-11-18, Andrej):** A, as implemented: the forced tag stays; the `Time basis:` line gives the reasoning (With the target undocumented there is no domain mechanism to rest ASR on.)

## Reference

@article{efron2004least,
  title={Least angle regression},
  author={Efron, Bradley and Hastie, Trevor and Johnstone, Iain and Tibshirani, Robert},
  year={2004}
}
