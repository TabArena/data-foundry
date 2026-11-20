---
unique_name: seismic_bumps
name: seismic-bumps
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
- WIP (Triage)
claimed_by: Andrej
suggestion: No (Retired)
decision_markers:
- Too Small
tags:
- Non-IID (Temporal)
- 'Samples: Over Time'
- 'Time: Inferred'
- 'Target: Later'
- 'Entities: Recur'
- Database Snapshot
original_source: UCI
year: '2013'
domain: industry & manufacturing
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
source_links:
- https://doi.org/10.24432/C5W902
notebook_path: datasets/beyond_iid/old_iid/seismic_bumps/seismic_bumps.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/seismic_bumps/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-09-30, Lennart): **Retired: the honest split is temporal, and as a temporal task the data is too small.** Each row is one 8-hour shift of one longwall in the Wesola coal mine and the label is a bump above 10^4 J in the next shift (ARFF header; Sikora & Wrobel 2010, Archives of Mining Sciences 55(1), Sec. 2.1: data "aggregated in the hourly and shift periods", "prediction horizon amounted to one ... shift"; Sec. 4.1: "consecutive shifts"). The file is in shift order: row t's label equals "row t+1 recorded a bump >= 10^4 J" in 2,583 of 2,583 consecutive pairs (0.877 when shuffled), and the sequence is non-stationary (positive rate per tenth of the file 0.04, 0.28, 0.13, 0.01, ...). The shipped IID shuffle lets training see every period (ROC AUC 0.75 IID vs about 0.6 forward; leak audit 2026-09-24). Following our temporal convention (as many splits as an IID task of this size, 10 x 3 = 30, never less than 50% of the data for training), all test windows come from the newest half, which holds only 49 of the 170 positives: 30 windows of 43 shifts have 0-5 positives each (6 have none). Even 3 or 2 windows (14-26 positives each) give ROC AUC intervals of about +-0.1 to +-0.14 per window. The UCI file (2,584 shifts, threshold 10^4 J) is a later export than the paper's (1,961 shifts from longwalls SC508 and SC503, threshold 5*10^5 J). TabArena v0.1 dataset.

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Temporal Tabular.

forecasting seismic bumps in a coal mine from longwalls in a Polish mine; used for clusterting. 

Description highlights practical importance of the taskl. each row contains a summary statement about seismic activity in the rock mass within one shift (8 hours). If decision 
attribute has the value 1, then in the next shift any seismic bump with an energy higher than 10^4 J was 
registered. Hence, the task might be time-invariant.

Potential issue: Temporal

Lennart: temporal data

Andrej: unsure whether the features are extracted from time-series. even if yes, they are extracted from 8h windows and I think this is rather a tabular task. BUT: Temporal correlations need to be investigated. unsure whether the extracted features are time-invariant

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `aaia16_coal_mine_seismic_hazard` (TBD -> Yes, priority 4). Each is screened in its own record; this record's verdict stays the curator's.

**Assessment (AI, 2026-11-19):** collection facts and type, set for the v0.2 definition (the record predated them): `Samples: Over Time` (each row is one 8-hour shift of a longwall, predicted at the shift's end; the ARFF header: "each row contains a summary statement about seismic activity in the rock mass within one shift"); `Time: Inferred` (no date or shift number in the file; the file order is the shift order: row t's label equals "row t+1 recorded a bump of 10^4 J or more" (`nbumps4` to `nbumps89` > 0, equally `maxenergy` >= 10^4) in 2,583 of 2,583 consecutive pairs); `Target: Later` (the label is the next shift's outcome, known one shift after the row, the same delay for every row); `Entities: Recur` (all rows come from two longwalls, ARFF header "Data come from two of longwalls", with no longwall id). Collection type `Database Snapshot`: a monitoring system's shift records released as one extract with no date per row and the order rebuilt from the file (SPLIT-34 rule 2; panel data needs the release to identify the unit, rule 1, and it does not).

**Assessment (AI, 2026-11-19):** review panel (full): ship after changes if kept. Applied without a decision: the LEAK-9 protocol line (the next test row holds a row's label), `shift_order` no input (`time_of="label"`), the notes' numbers (positives per tenth, the energy drops, the preparation stretch 906-1104), the proxy target and missing longwall id in `fit_reason`, AAIA'16 in the metric reason. Signal without `shift_order` at 84 shifts: ROC AUC TabPFN 0.579 p 0.095; log loss passes (p 0.048) but its gain is the window's level only.

CC (2026-11-20, Andrej): no overlapping windows toward the target (Review issue 5, A).

CC (2026-11-20, Andrej): Review issue 1, A: monthly test windows stay; the cadence is our assumption, and a model refit every day did not beat the window's model on the windows measured, so the monthly window does not penalise the models.

CC (2026-11-20, Andrej): Review issue 2, A: ROC AUC stays the metric; log loss, average precision and the Brier score follow each window's bump rate, and recall at an alarm share needs a budget the source does not give.

CC (2026-11-20, Andrej): Review issue 4, B: test windows of 84 shifts (four weeks of the measured 21-shift week), 15 windows of 1-10 bumps, each trained on 51.1% or more of the shifts; the window length and the 50% floor stop more than 15 of the target 30.

CC (2026-11-20, Andrej): Review issue 3, A: seismic_bumps is kept although no tuned method beats shuffled labels at p < 0.05 under ROC AUC on the 84-shift windows (TabPFN p 0.095); a weak shift-level signal is the task, and the only public shift-level seismic set stays.

## Review

**Outcome:** added on 2026-11-19 on your note to issue 1: retired as `Too Small` on 2026-09-30 and reopened the same day, as the rule it rested on changed. The v0.2 definition is written and passes `dataset check`; the review panel is running, and its issues will follow here.

**Main points:** The panel's changes are made (the test-row protocol line, `shift_order` no input, the notes' numbers, the proxy target). Open: the metric (issue 2), keep or `No Signal` (issue 3, turns on issue 2), the window length (issue 4), overlapping windows (issue 5).

**Issues for Andrej:**

1. **Reinstate seismic_bumps as a temporal task, now that few bumps per window no longer make it `Too Small`?**

   * **Problem:**
     - The retirement rested on the old reading of TP-9: 30 windows of 43 shifts in the newest half held 0-5 bumps each (6 none), and few positives per window counted against the task.
     - Since 2026-11-19 few positives in a window are part of the task; only a window without a bump breaks ROC AUC, and it is widened or its cut moved[^tp9].
     - Windows of 86 shifts (about four weeks at three shifts a day) give 15 windows, each training on half the shifts or more and holding 1-7 bumps; the target an IID split would get is 30[^split15].
   * **Details:**
     - 2,584 shifts in shift order (row t's label is a bump of 10^4 J or more in shift t+1), 170 bumps, 49 of them in the newest half; the bump rate moves by tenth of the file (0.04, 0.28, 0.13, 0.01, ...), so the split stays temporal.

       | Windows | Count | Shifts each | Bumps each | Windows without a bump |
       |---|---|---|---|---|
       | 43 shifts (the retired layout) | 30 | 43 | 0-5 | 6 |
       | 86 shifts, about four weeks | 15 | 86 | 1-7 | 0 |
       | 129 shifts, about six weeks | 10 | 129 | 2-10 | 0 |
       | cuts moved until each holds a bump | 30 | 33-97 | 1-4 | 0 |
       | 86 shifts, with the exception down to 30% training | 21 | 86 | 0-7 | 2 |

     - A window's ROC AUC on 1-7 bumps is noisy; the mean over 15 windows is what compares models.
     - No v0.2 definition exists (the shipped copy is the old IID notebook): B or C means writing one.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep retired as `Too Small` (implemented) | No change | No new definition | Rests on a rule reading that no longer holds |
     | B | Reinstate: 15 windows of 86 shifts, newest first, each trained on all earlier shifts | A v0.2 definition with `TemporalSplits(window=86, unit="rows")`, ROC AUC; `splits_below_target` answered (15 of 30: equal windows that each hold a bump) | Every window holds a bump and trains on 50% or more; equal, label-blind windows | 15 of the target's 30; about a month a window, a refit cadence the source does not state |
     | C | Reinstate: 30 windows whose cuts move until each holds a bump (33-97 shifts) | As B with explicit cutoffs | Reaches the target | The cuts follow the labels, so windows end next to bumps: a window choice that depends on the target |

   * **Recommendation:** B, the rule's reason for retiring is gone and equal windows keep the test independent of the labels. **Decision:** A, B or C?

   **Notes for the AI:** on B or C, write the v0.2 definition (raw file: UCI 266, seismic-bumps.arff; the shift order is the file order, no input), set `suggestion` and `decision_markers` back, CC line, build and `dataset check`; on A, a CC line that the retirement stands under the new rule on another ground.

   **Andrej (2026-11-19, discuss):** Do add dataset and review dataset for this dataset and add it to this html.

   **Answer (AI, 2026-11-19):** added; the review panel is running.

   * **Definition:** `datasets/_dev/tabarena-v0pt2/seismic_bumps/dataset.py`, option B's layout: windows of 86 shifts,
     newest first, each trained on all earlier shifts, no gap (the label is known at the end of the next shift), ROC
     AUC as the fallback metric. Not built into the benchmark yet.
   * **14 windows, not 15:** the file repeats two shifts three times (rows 89-90, 972-973 and 1017-1018 copy the two
     rows before them in every column), so 6 copies are dropped and 2,578 shifts remain with all 170 bumps; a 15th
     window would then train on 49.96%. The windows hold 1-7 bumps and train on 53-97% of the shifts.
   * **The order checks out:** a row's label equals "the next row has a bump of 10^4 J or more" in all 2,577 pairs.
   * **Weak signal** (tuned, mean ROC AUC over the 14 windows):

     | Model | ROC AUC | Shuffled labels |
     |---|---|---|
     | Logistic regression | 0.564 | 0.38-0.67 (p 0.29) |
     | LightGBM | 0.593 | 0.38-0.58 (p 0.048) |
     | TabPFN 3.5 | 0.637 | 0.40-0.55 (5 shuffles) |
     | seismic energy alone, untrained | 0.645 | |

   * **Questions from the build** (window length, the 15th window, the shift order as an input, the weak signal, the
     metric) go to the panel and come back here as issues.

   **Andrej (2026-11-19, discuss):** Which metric do we use? Rethink the metric from the use case perspective and depending on which metric makes sense, think about whether it is fine to have splits without positives.

   **Answer (AI, 2026-11-19):** ROC AUC is shipped (the binary fallback); the panel weighed it against log loss from the use case, and the choice is now issue 2. Under ROC AUC a window without a bump cannot be scored, so every window must hold one; under log loss it can be scored, but that alone gives no reason for shorter windows.

   * **What the use case asks:** the hazard service rates every shift and acts on the level it expects (destress blasting, withdrawing the crew), at a fixed action per level; the bump rate moves from 1.2% to 11.9% between 84-shift test windows. No source fixes a threshold or costs.
   * **Ruled out:** threshold metrics (balanced accuracy, sensitivity at a fixed specificity), as no threshold or cost is fixed; average precision, whose floor moves with each window's bump rate and which no source chose.
   * **Windows without a bump:** ROC AUC needs both classes in a window, so a window without a bump breaks it. Log loss scores such a window, but only on how low the model's level is there. The window length still follows the use case, and shorter windows add no test rows (the half-data floor fixes the test pool), so the panel recommends 84 shifts under either metric (issue 4).
   * **The signal under each metric** is issue 3; the window length issue 4.

   This issue's choice (reinstate, and with which windows) now rests on issues 2 to 4.

   **Andrej (2026-11-20, discuss):** I am not sure if we got the task right. Is it next day prediction? If yes, wouldn't the use case actually retrain daily? Also, would the sample size with next day prediction be 1?

   **Answer (AI, 2026-11-20):** it is next-shift prediction: each row is one 8-hour shift, rated at its end, and the label is a bump of 10^4 J or more in the next shift. A service could refit after every shift, but then each test window would be one shift, one row, which no window score can use; the source gives no refit cadence.

   * **What the source says:** the hazard is assessed per shift ("the next shift"), by the mine's monitoring systems; nothing about how often a model is refit. AAIA'16, by the same authors, released new training data about monthly.
   * **The two readings:**

     | Refit cadence | Test window | Windows | Rows per window | Scorable? |
     |---|---|---|---|---|
     | every shift | the next shift | about 1,290 | 1 | no window score (ROC AUC needs both classes; the minimum is 33 rows) |
     | every day (3 shifts) | the next day | about 430 | 3 | no, the same |
     | about monthly (implemented, 84-86 shifts) | the next four weeks | 14-15 | 84-86 | yes |

   * **A per-shift refit can be evaluated another way:** refit before every test shift, predict that one shift, and score all those single predictions together (one pooled score over the newest half, about 1,290 refits per method). That is the faithful reading of a per-shift refit, but the benchmark's protocol scores windows, not pooled single predictions, so it would need a new protocol.
   * **Does the cadence matter here?** For garments a day-old model cost Kumo-Tabular 6.5% MAE, so it can; for seismic it is not measured. A month-old model versus a refit one could be measured the same way (as for garments) before you decide.

   | | Option | What it does |
   |---|---|---|
   | A | Monthly windows (implemented) | keeps the window protocol; the cadence stays our assumption, named in `fit_reason` |
   | B | Measure first | as for garments: within each window, score shifts by a model refit up to the day before against the window's model |
   | C | A pooled per-shift evaluation | needs a protocol change in the benchmark |

   **Recommendation:** B, then A unless the measurement shows the month-old model losing clearly. **Decision:** A, B or C?

   **Andrej (2026-11-20, discuss):** Reply (B): Measure first

   **Answer (AI, 2026-11-20):** preliminary, 9 of the 15 windows: a month-old model does not lose against one refit every day: on the nine newest windows refitting every three shifts improves no model's ROC AUC and changes log loss by less than its spread, so the recommendation goes back to A.

   * **Setup:** within each 84-shift window, the window's model (trained on every shift before the window) against a model refit every 3 shifts (one day) on every shift before that day; no `shift_order` input; LightGBM (3 seeds), logistic regression, Kumo-Tabular (2 seeds).
   * **So far (the nine newest windows, 25 bumps in all, 1 to 6 per window):**

     | Model | ROC AUC, window's model | ROC AUC, daily refit | Refit better (windows) | Log loss, window's model | Log loss, daily refit | Mean gain of refit ± SD |
     |---|---|---|---|---|---|---|
     | LightGBM | 0.559 | 0.559 | 4 of 9 | 0.1520 | 0.1527 | -0.0007 ± 0.0038 |
     | Logistic regression | 0.524 | 0.514 | 1 of 9 | 0.1504 | 0.1501 | +0.0003 ± 0.0009 |
     | Kumo-Tabular | 0.582 | 0.499 | 1 of 8 | 0.1567 | 0.1540 | +0.0028 ± 0.0076 |

   * **Reading:** no model gains from the daily refit in ROC AUC; in log loss the gains sit well inside one SD across windows. Unlike garments (Kumo-Tabular -6.5% MAE from a day-old model), the cadence does not show here; the monthly window does not penalise the models. The scores themselves are near chance at 1 to 6 bumps per window, which is issue 3's question, not the cadence's.
   * **Still running:** the six older windows (the full run reports a paired test over all 15); this turn is updated when it ends.

   **Recommendation:** A (monthly windows, the cadence named in `fit_reason` with this measurement), unless the six older windows reverse it. **Decision:** A, B or C?

   **Andrej (2026-11-20, discuss):** In this case, I decide for monthly windows

   **Resolved (2026-11-20, Andrej):** A: monthly windows stay; a daily refit did not beat the window's model on the windows measured (ROC AUC refit better in 1-4 of 9 windows per model; log loss gains within one SD). `fit_reason` names the cadence as our assumption with this measurement once the run over all 15 windows ends; the window length itself (84 or 86 shifts) is issue 4.

   **Answer (AI, 2026-11-20):** the refit test over all 15 windows confirms the preliminary reading: a model refit every day never beats the window's model in ROC AUC, and its log-loss gains are not significant.

   | Model | ROC AUC, window's model / daily refit | Refit better (of 15) | Wilcoxon p | Log loss, window's model / daily refit | Refit better (of 15) | Wilcoxon p |
   |---|---|---|---|---|---|---|
   | LightGBM | 0.553 / 0.555 | 8 | 0.80 | 0.1720 / 0.1685 | 10 | 0.33 |
   | Logistic regression | 0.535 / 0.523 | 3 | 0.04 (refit worse) | 0.1695 / 0.1683 | 10 | 0.14 |
   | Kumo-Tabular | 0.592 / 0.509 | 3 | 0.006 (refit worse) | 0.1672 / 0.1643 | 10 | 0.19 |

   The monthly windows decided under this issue stand; the definition's splits comment now gives these numbers.

   [^tp9]: **TP-9** (Must): count the positives per test window and report them; few positives are part of the task; only a window without a positive under a ranking metric is widened or its cut moved (SPLIT-16).

   [^split15]: **SPLIT-15** (Must for the newest window, Should for the others): the number of windows aims at the splits an IID split of the data would get, SPLIT-33's count for two thirds of all scored units; fewer are accepted, never under three.

2. **Metric: ROC AUC (the fallback) or log loss?**

   * **Problem:**
     - The service acts on an absolute hazard level, while the bump rate moves tenfold between test windows (1.2% to 11.9%); ROC AUC ranks shifts within a window and cannot see whether the level follows the month's hazard; log loss scores the probability itself[^met8].
     - No source fixes a threshold or costs: the ARFF header reports accuracy, balanced accuracy, sensitivity and specificity side by side, so threshold metrics are out[^met6]; the same authors chose ROC AUC for the same shift-level decision in the AAIA'16 challenge (Janusz et al. 2016).
     - Measured (issue 3): under log loss all of the models' gain is each window's level, not which shifts are dangerous; under ROC AUC the gain inside a window is weak.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | `roc_auc`, the binary fallback (implemented) | No change; the metric reason cites AAIA'16 | The field's own choice for this decision; window scores compare across bump rates | Cannot see the level, the main variation here |
     | B | `log_loss`, chosen from the use case | `Metric` from context, with ROC AUC named as the alternative weighed | Scores the absolute probability a fixed alarm level acts on; a strictly proper rule | The first binary log loss chosen from context; window scores depend on the bump rate; its whole signal is the window's level |

   * **Recommendation:** A, because the source fixes no threshold, the field's competition chose to rank, and the task asks which shift is dangerous; take B only if you would have chosen it before seeing the numbers of issue 3. **Decision:** A or B?

   **Andrej (2026-11-20, discuss):** What exactly do you mean with window scores depend on the bump rate? and its whole signal is the window's level?

   **Answer (AI, 2026-11-20):** two plain points about log loss here.

   * **"Window scores depend on the bump rate":** log loss is low wherever bumps are rare, whatever the model. A model that predicts the right overall rate scores about 0.06 in a window with 1% bumps and about 0.37 in one with 12% bumps. So averaging log loss over windows mixes easy (quiet) and hard (active) months, and a window's score says more about how many bumps it held than about the model. ROC AUC has no such pull: a model that ranks no better than chance scores 0.5 in every window.
   * **"Its whole signal is the window's level":** the models beat the constant in log loss, but all of that gain is getting each window's overall bump rate right (quiet months low, active months high), not ranking which shifts inside a window are dangerous. The test: replace each model's per-shift predictions by its own average for that window; that flat prediction scores as well as the model or better (0.1661 against 0.1673 for logistic regression, 0.1665 against 0.1684 for LightGBM). So under log loss the task rewards knowing the month's hazard level, while the decision the service makes is about the next shift.

   This is why ROC AUC (issue 2, A) is recommended: it scores the ranking of shifts within a window, the part the service acts on.

   **Andrej (2026-11-20, discuss):** Could another metric be even better?

   **Answer (AI, 2026-11-20):** not clearly: every candidate either shares log loss's pull toward the month's bump rate or needs an alarm budget the source does not give; ROC AUC stays the closest fit to "which shift is dangerous".

   | Metric | What it scores | Here (1-10 bumps per window, rate 1.2-11.9%) | Fit |
   |---|---|---|---|
   | ROC AUC (implemented) | the ranking of shifts within a window | chance is 0.5 in every window; noisy with 1-2 bumps, but defined | ranks the next shift, the service's decision |
   | Average precision (PR AUC) | how high the bump shifts rank, from the top | chance equals the window's bump rate, so window scores move tenfold with the rate, as log loss does; with one bump it is 1 / its rank | the alarm view, but even noisier |
   | Log loss (B) | the probability itself | measured: all of the models' gain is each window's level | the level, not the shift |
   | Brier score | the probability, squared error | the same pull toward the window's rate as log loss, milder on confident misses | as log loss |
   | Recall at a fixed alarm share (say the top 10% of shifts) | bumps caught under an alarm budget | needs a budget; the source gives none (it reports sensitivity and specificity side by side) | a threshold metric, ruled out without costs |

   * A metric that would be better than ROC AUC needs one of two things this source lacks: a stated alarm budget (then recall at that share) or costs of a missed bump against a false alarm (then expected cost).
   * The noise of a few bumps per window hits every ranking metric alike; it is issue 3's question (keep or `No Signal`), not the metric's.

   **Recommendation:** A (ROC AUC), unchanged. **Decision:** A or B?

   **Andrej (2026-11-20, ok):** Agree.

   **Resolved (2026-11-20, Andrej):** A: ROC AUC, the binary fallback, stays; no other metric fits better without an alarm budget or costs the source does not give. The metric reason cites AAIA'16.

   [^met8]: **MET-8** (Must): without a source metric, a binary task falls back to ROC AUC; a metric chosen from the use case's context needs a clear context.

   [^met6]: **MET-6** (Must): several metrics reported side by side without a threshold or costs are no deliberate choice of one.

3. **Keep, or retire as `No Signal`?**

   * **Problem:**
     - With `shift_order` no input and 84-shift windows, no model beats its shuffled training labels at p < 0.05 under ROC AUC; both sides of the panel agreed before the run that this layout decides and that a p of 0.05 to 0.16 goes to you[^tp2].
     - Under log loss two model families beat all 20 shuffles, but all of their gain is each window's bump level.
   * **Experiments:** tuned on a temporal inner split, 20 shuffles of the training labels; 15 windows of 84 shifts.

     | Metric | Method | Score | Shuffled | p |
     |---|---|---|---|---|
     | ROC AUC | TabPFN 3.5 | 0.579 | 0.444-0.611 | 0.095 |
     | ROC AUC | logistic regression | 0.588 | 0.402-0.608 | 0.19 |
     | ROC AUC | LightGBM | 0.548 | 0.374-0.568 | 0.24 |
     | log loss (constant 0.1771) | logistic regression | 0.1673 | 0.1752-0.1802 | 0.048 (all below) |
     | log loss | LightGBM | 0.1684 | 0.1756-0.1810 | 0.048 (all below) |
     | log loss | TabPFN 3.5 | 0.1675 | 0.1765-0.1798 | 0.048 (all below) |
     | log loss | each model's own window mean as a constant | 0.1661 / 0.1665 | | |

     The 86-shift windows of the first build give TabPFN ROC AUC 0.583, p 0.048 (a sensitivity check only); with `shift_order` as an input the earlier run passed (LightGBM 0.593, p 0.048), but that column is no input.
   * **Background:** the source calls seismic hazard "the hardest detectable and predictable of natural hazards", and its 14 classifiers reach balanced accuracy 0.50-0.69; precedents: clock_protein_toxicity retired at p 0.16, forest_fires kept at p 0.02; one raw feature (the geophone energy) scores 0.645 untrained, but it was picked on the test rows, so it is no proof of `Trivial`.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | Under ROC AUC: an exception at p 0.095 with this reason; under log loss: step 1 passes, the level-only gain is noted | The source's own decision; a weak signal is what the field expects; 15 windows of 1-10 bumps resolve only large gains | Under ROC AUC no method shows a signal at p < 0.05; under log loss the signal is the window's level only |
     | B | Retire as `No Signal` | `No` / `No Signal`, the folder removed in a retirement PR | What the agreed threshold gives under ROC AUC | Loses the only public shift-level seismic set; aaia16 is not built |

   * **Recommendation:** none: this is the call both sides left to you; with issue 2 A it is an exception either way, with issue 2 B the rule keeps it. **Decision:** A or B?

   **Andrej (2026-11-20, ok):** Did you test with the new monthly windows?

   **Answer (AI, 2026-11-20):** yes: the table above is the 84-shift layout you chose in issue 4 (15 windows, 1-10 bumps each), with `shift_order` no input. The 86-shift windows of the first build are only the sensitivity line under the table (TabPFN p 0.048).

   | Windows | TabPFN ROC AUC | p (20 shuffles) |
   |---|---|---|
   | 84 shifts, 15 windows (issue 4, B) | 0.579 | 0.095 |
   | 86 shifts, 14 windows | 0.583 | 0.048 |

   Your `ok` keeps the dataset (A) on p 0.095 under ROC AUC (issue 2, A), the exception the issue describes. **Decision:** confirm A?

   **Andrej (2026-11-20, ok):** Agree.

   **Resolved (2026-11-20, Andrej):** A: kept as a curator's exception under ROC AUC (TabPFN 0.579 against shuffled training labels, p 0.095 on the 84-shift windows): the source calls seismic hazard among the hardest to predict, a weak signal is what the field expects, and 15 windows of 1-10 bumps resolve only large gains.

   [^tp2]: **TP-2** (Should): a signal exists when a tuned method beats the same pipeline on shuffled labels; otherwise `No Signal`.

4. **Window length: 84 shifts (four measured weeks) instead of 86?**

   * **Problem:**
     - 86 shifts rested on "three shifts a day" without a check; the split auditor measured a 21-row weekly cycle (18 coal-getting and 3 preparation shifts) in rows 150-905, so four weeks are 84 rows; the source states no refit cadence, and AAIA'16 released data about monthly[^split12].
     - At 84 shifts: 15 windows, 1-10 bumps each (49), every one on 51.1% training or more; the 15th-window question (49.96% at 86) disappears.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | 86 shifts, 14 windows (implemented) | No change | No rebuild | Not four weeks; rests on an unchecked cadence |
     | B | 84 shifts, 15 windows | `TemporalSplits(window=84, unit="rows", min_train_fraction=0.5)` | Four measured weeks; one more window | The weekly cycle is not visible after row 1105, where the test windows lie |

   * **Recommendation:** B, chosen on the measured week, not on the scores (86 gives TabPFN p 0.048, 84 p 0.095). **Decision:** A or B?

   **Andrej (2026-11-20, change):** Option B: 84 shifts, 15 windows.

   **Resolved (2026-11-20, Andrej):** B: `TemporalSplits(window=84, unit="rows", min_train_fraction=0.5)`: 15 windows of four measured weeks, 1-10 bumps each (49 in all), trained on 51.1% to 96.7% of the shifts; `splits_below_target` accepted (15 of 30: the window length and the 50% floor; no overlap, issue 5); `fit_reason` names the monthly cadence as our assumption with the daily-refit measurement. `dataset check`: 0 errors; open warnings: the sequential `shift_order` (the time column, no input) and few bumps per window (the task, issue 3). Not rebuilt.

   [^split12]: **SPLIT-12** (Should): the use case sets the window length, step, gap and time unit, named in the splits comment.

5. **Overlapping windows toward the target of 30?**

   * **Problem:** the target for 2,578 shifts is 30 windows; 84-shift windows moved by 42 give about 29, but they count one test pool twice, and the use case gives no reason for them[^split15].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | No overlap (implemented) | 14 or 15 windows | Separate evaluations | Half the target |
     | B | 84 shifts, step 42 | About 29 windows | Near the target | Each test shift scored twice; no use-case reason |

   * **Recommendation:** A. **Decision:** A or B?

   **Andrej (2026-11-20, ok):** As implemented (A).

   **Resolved (2026-11-20, Andrej):** A: no overlapping windows; each test shift is scored once.

   [^split15]: **SPLIT-15** (Must for the newest window, Should for the others): aim at SPLIT-33's count, accept fewer, never under three; overlapping windows are only offered.

**Review panel:** ship after changes, if you keep it (mediator). Tier full, 2026-11-19: claim, column and split auditors, domain practitioner, blind reviewer and task gamer (both outside the repository, via `claude -p` on Slurm), precedent checker, advocate and critic with one rebuttal each, mediator; the editor pass is the main session's. Claims: 25, 21 hold, 2 refuted (note numbers, fixed), 2 untested (the 2010 paper). Blind review: include with changes (few positives, `shift_order` no input, the dropped rows explained). Task gamer: the next test row gives a row's label (ROC AUC 1.000): an evaluation leak, fixed with the protocol line (LEAK-9). Agreed: the protocol line, `shift_order` no input, 84 shifts, the number fixes, the proxy target in `fit_reason`. Disputed: keep or `No Signal` (issue 3), which turns on the metric (issue 2).

<details><summary>Mediator</summary>

**Mediator report: `seismic_bumps` (full panel, 2026-11-19)**

**Judgment record**

```text
Verdict: ship after changes, if the curator keeps it on the signal question, which depends on the metric.
Validity: SEL holds; USE-1 holds (approximate: the source's own use, destress blasting and withdrawing crews; the target a proxy, a bump of 10^4 J or more, not a rockburst); LEAK-9 triggered, evaluation level only, fixed with a protocol line; LEAK-19 fixed (6 export copies dropped); SPLIT-16 and TP-9 hold (no test window without a bump at 84 shifts); SPLIT-14 holds (15 windows, at least 51.1% training); SPLIT-15 below target (15 of 30), accepted with the reason; SPLIT-12 needs the curator's sign-off on the window length.
Value: TP-2 step 1 borderline under roc_auc (TabPFN p 0.095 at 84 shifts, the run both sides agreed would decide); passes clearly under log_loss (LR and LightGBM beat all 20 shuffles), but all of that gain is the window's bump level. TP-4: no proof (genergy picked on the test rows; the feature picked on each training side scores 0.470). TP-10 leg 1 holds (persistence 0.488).
Quality: number and wording fixes; proxy target and missing longwall id in fit_reason.
Weighed: real use case +, source states weak signal +, small single-mine export -, aaia16 larger data for the same task - (supersession would depart from selection.md "Small or dated").
For the curator: metric; keep or No Signal; window length; overlapping windows (optional).
```

**Decisive new measurement: TP-2 step 1 under log loss** (no `shift_order`, tuned by log loss on the temporal inner split, 20 shuffles; Slurm jobs 1397775/1397776; `panel/scratch/mediator/signal_logloss.py`)

| Windows | Method | Mean log loss | Shuffled | p | Windows better than the constant | Brier p |
|---|---|---|---|---|---|---|
| 84 shifts (15) | best constant (training bump share) | 0.1771 | | | | |
| 84 | LR | 0.1673 | 0.1752-0.1802 | 0.048 (all 20 below) | 12/15 | 0.048 |
| 84 | LightGBM | 0.1684 | 0.1756-0.1810 | 0.048 (all 20 below) | 10/15 | 0.286 |
| 42 shifts (30, 6 without a bump) | LR | 0.1678 | 0.1753-0.1808 | 0.048 | 19/30 | 0.048 |
| 42 | LightGBM | 0.1683 | 0.1745-0.1809 | 0.048 | 20/30 | 0.048 |

Where the log-loss gain comes from (84-shift windows, `decomp.py`):

| | LR | LightGBM |
|---|---|---|
| Best constant (training bump share) | 0.1771 | 0.1771 |
| The model | 0.1673 | 0.1684 |
| The model's own window mean as a constant for that window | 0.1661 | 0.1665 |
| A constant at the window's true bump rate (oracle) | 0.1558 | 0.1558 |
| The model moved to the window's true rate | 0.1568 | 0.1575 |
| Spearman, window mean prediction vs bump rate (15 windows) | 0.44 | 0.30 |

All of the log-loss signal is the window's level: each model's own window-mean constant scores better than the model. The models track which periods are quiet (mean predictions 0.03-0.10 against window rates 0.012-0.119); the previous 84 shifts' bump rate does worse than the constant (0.1787), so the level comes from the features, not recency.

**Changes to make now:** the LEAK-9 protocol line (the "rows ship shuffled" claim was false: temporal tasks are sorted by their time column); `shift_order` no input (`time_of="label"`, as wine_quality and labour_inspection_compliance); number and wording fixes (positives per tenth, the energy drops, the preparation stretch rows 906-1104, "adjacency proven"); fit_reason (proxy target, no longwall id, next shift's type not given); metric reason cites AAIA'16; after the verdict: TP-9/SPLIT-16 Cases rows, accepted warnings.

**For the curator:** M1 metric (lean roc_auc: the source fixes no threshold, the field's competition chose to rank, and log loss would keep the task for a monthly level signal while the task asks about the shift; log loss only if chosen before seeing these numbers); M2 keep or No Signal (under roc_auc p 0.095, between clock_protein_toxicity retired at 0.16 and forest_fires kept at 0.02; under log_loss step 1 passes and step 2 is the curator's call on a level-only gain); M3 sign off 84 shifts (measured four weeks); M4 overlapping windows (no).

**Consistency:** followed: the reopening (TP-9, SPLIT-16 amended; lung_adenocarcinoma_metastasis); rebuilt-order leaf, no gap (wine_quality, labour_inspection_compliance); LEAK-9 protocol line (loan_default_prediction_imperial_college, spanish_motor_coverage, medical_facility_operational_data); copy drop (LEAK-19); `shift_order` no input; roc_auc fallback (gallstone_disease, ljubljana_breast_cancer). Departures: log_loss by `context` would be the first binary one (the tenfold drift of the bump rate under a fixed alarm threshold would be the distinguishing fact); keeping under roc_auc at p 0.095 is an exception with a stated reason. Cross item: the tree's wording on whether a rebuilt order is an input differs between sibling leaves (separate rule question).

</details>

<details><summary>Claim audit</summary>

**Claim auditor (seismic_bumps, 2026-11-19)**
Bottom line: no deciding claim failed; 2 descriptive numbers wrong; Sikora & Wrobel 2010 claims untested. No models fitted. Scripts panel/scratch/claim-auditor/c1-c4.py.
Holds: 2,584x19, 170 pos (6.6%); label(t) = row t+1 bump >=1e4 J, 2583/2583 both definitions (chance 0.877; lag-1 autocorr log genergy 0.851 vs -0.01 shuffled; chain may be true by construction, shows export order); 6 copies exactly rows 89-90, 972-973, 1017-1018, all class 0, AB AB blocks with identical gdenergy (LEAK-19); after drop 2,578 rows, 2577/2577, no positive lost; nbumps6/7/89 all zero; ratings (seismic a/b; seismoacoustic a/b/c; ghazard a/b/c; W 1663/N 921); 14 windows of 86, bumps 4,1,2,6,4,1,3,2,3,5,7,4,5,1 (48), train 0.533-0.967, 15th 0.4996; target 30; no gap (train ends at test_start-1 in all folds); use case quote ("reduce a risk of rockburst (e.g. by distressing shooting) or withdraw workers"); nbumps4/5/maxenergy describe previous shift; no feature-vector duplicates across split; metric: UCI names none, header table Acc/BAcc/spec/sens for 14 classifiers under stratified 10x10 CV, no threshold (MET-5/6/8); ROC AUC computable every fold (dummy 0.5); licence CC BY 4.0, DOI 10.24432/C5W902, year 2013; signal numbers reproduce (LR p 5/.. ; LightGBM no shuffle >= 0.593, max 0.584; genergy 0.645, 13/14 windows >0.5, paired +0.0075 SE 0.0207, 8/14); collection facts/type.
Refuted (minor, wording): (8) "genergy drops about tenfold near row 820": 600-820 vs 820-1040 is 2.3x; tenfold near rows 350-390 (449k -> 50k, 8.9x), another 3.9x step near 720-740 -> reword. (7) positives per tenth: shipped data 11,72,33,2,3,8,15,8,11,7 (not 10,72,34,...) -> replace.
Approximate: "rows 940-1120 almost only preparation": 91% N; block starts ~40 rows earlier (900-1080: 99%); longest N run 199.
Untested: Sikora & Wrobel 2010 (MET-5 ranking criterion, horizon quote, 1,961 shifts SC508/SC503 at 5e5 J in Lennart's CC); 3-shifts-a-day cadence (WWW in 1,338/2,582 trigrams, W runs up to 92, N up to 199; hedged); protocol line "rows ship shuffled and are scored one by one" not checked against the harness; gdenergy/gdpuls not reproducible (<=4.8%).
Minor: record issue 1 Problem/Options still say "15 windows"; definition ships 14.

</details>

<details><summary>Column audit</summary>

**Column auditor (seismic_bumps, 2026-11-19)**
Verdict: no data leak, no must-fix cleaning. All features describe the shift just ended. Scripts: panel/scratch/column-auditor/.
`shift` describes the current shift (bumps by own shift 1.18 vs 0.29; by prev/next row 1.11 vs 0.41).
Columns all fine: seismic (only a/b; window AUC 0.483), seismoacoustic (a/b/c; c 48 rows), shift, genergy (level break ~row 850: medians 30k-820k -> 3k-40k), gpuls, gdenergy/gdpuls (do not reproduce from file's 8 previous rows, <=4.9%; implied mean vs trailing mean Spearman 0.77 vs -0.04 shuffled -> order right, GMax own history), ghazard (high first at row 1,692, all No), nbumps (= band sum in 2,576/2,578), nbumps2-5 (nbumps4/5, maxenergy>=1e4 = previous row's label: fine as input, LEAK-34/LEAK-44), energy, maxenergy; nbumps6/7/89 constant dropped (CLEAN-5); shift_order = file position with gaps, question; target fine.
Dedup drops any repeated row, not only adjacent pairs; same result here (cosmetic).
Problems:
1. Within-window leak (P4, LEAK-9 Should, evaluation level): label = next test row's nbumps4/5; sorting test rows by shift_order gives 1,190/1,204 test labels exactly, ROC AUC 1.000 in all 14 windows untrained. curation_comments note ("rows ship shuffled ... a model sees it only by learning from the test block") understates it; CLEAN-23 says temporal rows sorted by time index, contradicts "ship shuffled". Not a data leak. Mildest remedy: rewrite the LEAK-9 protocol line to name the mechanism; dropping shift_order removes the exact key (a chain might still be matched via gdenergy/gdpuls).
2. shift_order as input (curator): row count, not the actor's date; runs through two longwalls and a stoppage (rows ~850-1100); test values always beyond training. With/without: TabPFN 0.637/0.583, LGBM 0.593/0.588, LR 0.564/0.579. Defensible by actor test; with 1 argues for option B (drop).
3. Next shift's type not an input (curator, CLEAN-19): bump rate 9.4% next coal-getting vs 1.5% preparation (current 9.2% vs 1.9%). Only if the plan fixes W/N in advance; may be recorded after the fact. Don't add without source.
4. Level break / two longwalls (P7, note): all test windows (row 1,380 on) in the later regime; add that to the note.
5. Minor: nbumps > band sum in 2 rows; nbumps5 header wording; unused levels declared correctly.
Dtype probe 0/16 flagged, agreed.

</details>

<details><summary>Split audit</summary>

**Split auditor (seismic_bumps, 2026-11-19)**
Verdict: right, with notes. Temporal on file order, expanding train, no gap; leaf Temporal · rebuilt order (also readable as panel data with two unidentified longwalls -> same leaf). Step ③ conditional until the curator signs off the window length (SPLIT-12). Scripts panel/scratch/split-auditor/a1-a5.py (pandas only).
1. Window length: 86 is not four weeks; data gives 4 weeks = 84. Rows 150-905 follow a 21-row cycle (18 coal-getting + 3 preparation = 6 working days + maintenance day at 3 shifts/day): autocorr of preparation flag 0.37 lag 21, 0.32/42, 0.36/63, 0.38/84; lags 18-19, 23: 0.02-0.07. Whole file 0.29 at 21 vs 0.23-0.24 at 20/22. 86 = twice the retired 43.
| Length | Meaning | Windows | Bumps | No bump | Min train | Next back |
| 42 | 2 wk | 30 | 0-5 | 6 | 51.1% | 49.5% |
| 63 | 3 wk | 20 | 0-6 | 2 | 51.1% | 48.7% |
| 84 | 4 wk (measured) | 15 | 1-10 | 0 | 51.1% | 47.9% |
| 86 | implemented | 14 | 1-7 | 0 | 53.3% | 49.96% |
| 91 | calendar month | 14 | 0-9 | 1 | 50.6% | 47.1% |
| 126 | 6 wk | 10 | 2-9 | 0 | 51.1% | 46.2% |
Remedy TemporalSplits(window=84): 15 windows >=51.1%, 1-10 bumps, 49 total; splits comment gives the measured cycle; monthly cadence stays our assumption. Horizon block: length assumed, cadence unstated; one-shift horizon stated by source.
2. Two longwalls likely sequential, meeting at the 199-shift preparation stretch rows 906-1104 (~66 days, energy down ~10x, face relocation).
| Segment | Rows | Bump rate | Med genergy | Med gpuls | Coal share | 21-cycle |
| 0-149 | 150 | 0.7% | 75,800 | 291 | 40% | - |
| 150-905 | 756 | 15.3% | 56,120 | 408 | 73% | yes |
| 906-1104 | 199 | 0.5% | 4,310 | 27 | 0% | - |
| 1105-2583 | 1,479 | 3.5% | 20,760 | 423 | 71% | no (runs of 18-40 prep shifts every ~160-170 rows) |
All test windows in the second segment; ~116 of 170 bumps in the first. Note it (test covers later longwall only); do not group (SPLIT-25, unconfirmed, 2 groups). Label chain proves file adjacency, not time continuity. Paper names SC508/SC503.
3. "Checked against time": chain + regime shifts show adjacency only; the 21-row weekly cycle (rows 150-905) is the calendar check, put it in splits_comment; unshown for the second segment.
4. shift_order input: keep (actor test; monotone shift count = prediction time; stands for longwall/phase). Tree wording inconsistent: DB Snapshot rebuilt-order leaf "no input when it comes with the target" vs sibling leaves "a rebuilt order ... is no input"; here target derived from order. Raise as cross item. TabPFN 0.637 vs 0.583 must not decide.
5. 15th window at 49.96%: not recommended; moot at 84.
6. Count below target 30 (10x3): 15 at 84 (14 at 86); stops: length + floor. Options: 84 stepped by 42 (~29, if overlap admitted); 30% exception (windows without bump appear); 2-week windows forbidden shortening.
7. Pass: no gap (SPLIT-10); time column = end of rated shift; newest window complete (4 bumps, 4.7%); last raw row label unverifiable; copy drop exact (rows 89,90,972,973,1017,1018, training region, no bump lost); TP-9 ok; within-window next-row leak "documented and harmless under per-row scoring".

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner (seismic_bumps, 2026-11-19)**

Fit approximate (agrees with fit="approximate"); real use case, no No Good Target.
Paper retry failed (Sikora & Wrobel 2010 unreachable); AAIA'16 summary (Janusz et al. 2016, FedCSIS, doi 10.15439/2016F560) read in full.

1. Inputs: all shipped inputs held at shift end. Missing: next shift's type (planned; next coal-getting 156/1,662 bumps = 9.4% vs preparation 14/915 = 1.5%; next-shift type alone ROC AUC 0.646 all / 0.582 newest half; current shift type 0.637 / 0.603), longwall id, face advance; history beyond one shift.
2. Target: bump >= 1e4 J next shift is a proxy for increased activity, not rockburst (header: "not connected with accurate rockburst prediction"); median maxenergy 3e4 J, 12 shifts >= 1e5 J, none >= 1e6 J; USCB counts >= 1e5 J as high-energy; AAIA'16 warning level 5e4 J over 8 h. Name proxy in fit_reason; not a retirement reason.
3. Rows = shift-end decisions; later-on-earlier testing is what the actor faces. 195-shift preparation-only run (rows 906-1104) = relocation/stoppage, always in training.
4. Use: supplement only; best model ties genergy (TabPFN 0.637 vs 0.645). Newest half: top 20% genergy alarms catch 21/49 bumps; alarming every coal-getting shift (72%) catches 45/49.
5. Metric: keep roc_auc; source fixes no threshold/costs (MET-5..8 -> fallback); AAIA'16 by the same authors chose AUC -> add to metric.reason (MET-11). Gap: calibration under drifting rate (0.8%-28% per tenth) unscored; AP no basis.

Gaps ranked: (1) next-shift type + longwall id missing; (2) proxy target; (3) no calendar: coal runs 1-61 shifts, prep 1-40 + one of 195, "86 shifts = 4 weeks" uncheckable; (4) expert ratings carry nothing (0.483/0.501/0.512; coarse a/b, d never), AAIA'16 experts score 0.92.
Cadence: none stated; AAIA'16 released data about monthly; supports 86 shifts as about a month.
Weak signal expected: header "hardest detectable"; its 14 classifiers balanced accuracy 0.50-0.69 under IID CV; AAIA'16 high AUC mostly between-site; genergy 0.681 within coal-getting, 0.508 within preparation.
Changes: maybe add next row's shift as "planned next shift" (measure, own decision item); proxy + missing longwall in fit_reason; cite AAIA'16 AUC in metric reason; weigh option D (aaia16 the better version; keep this as small single-mine variant or supersede once aaia16 built).
Scripts: panel/scratch/domain-practitioner/tools/.

</details>

<details><summary>Blind review</summary>

**Verdict: include with changes.** This is the real UCI seismic-bumps data with a correct target, honest features and a sensible time-ordered split. But the test set has few positives, `shift_order` must not be used as a feature, and the 6 removed rows need an explanation.

**What the task is.** Each row summarises one 8-hour shift at a longwall in a Polish coal mine. The target is whether a high-energy bump (above 10⁴ J) happens in the *next* shift. The source says: "'1' means that high energy seismic bump occurred in the next shift ('hazardous state')." A mine's hazard-assessment staff would make this call at the end of each shift, to decide on precautions, staffing or destressing. It is a real use, and every feature describes the previous shift or the 8 shifts before it.

**Concerns, most to least serious**

1. **Too few positives in the test windows to score reliably.**
   - 170 of 2,578 rows are positive (6.6%). The positives cluster early: rows 200–600 have positive rates of 26% and 18.5%, while rows 800 onward run at 0.5–7%.
   - I simulated 14 expanding windows starting at 30% of the rows. The tested rows carry a base rate of only 3.0%, about 54 positives in total, or roughly 4 per window. Some windows will have 0–2 positives, so AUC per window is undefined or very noisy.
   - Signal is modest. LightGBM scored AUC 0.66 and average precision 0.051 over the temporal windows, against a base rate of 0.030. Random 5-fold CV gave AUC 0.77, so drift is real and the temporal split is the right choice.
   - Change: use fewer, larger windows (for example 4–5), or pool predictions across windows before scoring. Report AUC or log-loss rather than accuracy.

2. **`shift_order` must be excluded from the features.**
   - It is a row index. Under a time split, a model can only extrapolate on it. Including it moved AUC from 0.66 to 0.69, which is likely by chance, not real signal.
   - `task.md` does not say whether it is a feature or only the column that orders the split.
   - Change: keep it only for ordering the split.

3. **Six rows dropped without explanation.**
   - The UCI source lists 2,584 rows. Here `shift_order` skips 89, 90, 972, 973, 1017 and 1018: three pairs of consecutive rows.
   - The remaining table has no duplicates.
   - Change: document why they were removed, or restore them.

4. **Two longwalls are mixed with no identifier.**
   - The source says "Data come from two of longwalls located in a Polish coal mine." There is no longwall column, and the source does not say how rows are ordered.
   - The ordering does look like a true time sequence. The label of row *t* equals "next row has `maxenergy` ≥ 1e4" in 2,577 of 2,577 cases, with no exceptions, and likewise "next row has `nbumps4` + `nbumps5` > 0".
   - The `shift` column, however, has runs of up to 195 identical values. That is odd if shifts were a strict rotation and may point to a block or longwall boundary.
   - The big level change around rows 200–600 (`genergy` rolling mean about 600k there, versus about 20–50k later) may be the other longwall or a different stage of mining.
   - Change: note this in the task description. The time split itself is fine.

5. **Labels can be read off the next row (no direct leak).**
   - Because each label is a deterministic function of the next row's features, a model that could see neighbouring rows would trivially solve the task.
   - Row-wise tabular models cannot, and the temporal split exposes at most one boundary row per window. So this is not leakage for this benchmark.
   - Change: do not use random-split CV, and do not add lagged or "next" features.

6. **Preparation is otherwise fine.**
   - The constant-zero columns `nbumps6`, `nbumps7` and `nbumps89` are already dropped.
   - The categoricals are typed correctly. `seismic` only has the levels "lack" and "low" hazard, out of the four in the source, which is plausible.
   - There are no missing values, and the values are physically plausible: `gdenergy` and `gdpuls` are percentage deviations, so negative values are expected.
   - The energy columns are heavy-tailed (`genergy` reaches 2.6M), which is harmless for tree models.
   - No training-weight column is defined, and none is needed.

**What I could not check**
- Why the 6 rows were removed. I did not download the raw UCI ARFF file to compare it row by row.
- Which rows belong to which longwall, and the actual calendar dates.
- Whether the label threshold (10⁴ J) matches the mine's operational definition beyond the UCI description.

</details>

<details><summary>Task gamer</summary>

**Verdict:** the task can be gamed completely. Each row's label is exactly whether the next row's `maxenergy` is at least 10⁴ J, and the next shift's row sits in the same test window. A one-line rule scores AUC 1.000 on all 14 splits, against 0.60 for the honest baseline.

Scripts: `work/run.py` (models and rules), `work/extra.py` (format, duplicate and gap checks). Scores are mean ROC AUC over the 14 shipped temporal windows (86 test rows each, 1–7 positives per window).

| # | Exploit | Script | Honest score | Exploited score | Gain (per split, range) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| 1 | Next row's `maxenergy` (or `energy`, or `nbumps4+nbumps5`) used as the score, or added as a feature (lead over the whole table) | run.py | 0.602 (LGBM) / 0.577 (with lag features) | 1.000 | +0.40 mean; +0.07 to +0.98 per split | No. That value is the next shift's measurement, which is exactly the outcome being predicted. | Split so no unit's next row is scorable with it: score one row per window, or score each test row with only the rows up to it. Or shuffle row order within each test window and drop `shift_order` from the test features. |
| 1b | Same rule restricted to rows inside the test window (the last test row has no next row) | run.py | 0.602 | 0.994 | +0.39; one split 0.91, the rest 1.00 | No | Same |
| 1c | Next row's `energy` alone (no `maxenergy`) | run.py | 0.602 | 0.999 | +0.40 | No | Same |

**Mechanism.** Each row is one 8-hour shift. Its features describe that shift, and the label is "a bump above 10⁴ J happens in the *next* shift". Rows are stored in time order (`shift_order`), so row i+1's `maxenergy` is the event row i is asked to predict. The crosstab of the label against `maxenergy(i+1) ≥ 10⁴` is perfectly diagonal (2408/0, 0/170), and `nbumps4+nbumps5 > 0` on the next row gives the same diagonal. This holds even across the 6 rows the preparation removed (shift_order 89, 90, 972, 973, 1017, 1018, all class "No"). The test windows are contiguous blocks of 86 consecutive shifts, so 85 of the 86 test rows have their answer in another test row. The split's `side` and the row order are enough to rebuild the lead. A model deployed at the end of shift i cannot see shift i+1.

**Mildest fix.** Make the next row unusable at test time: shuffle each test window and withhold `shift_order` from the test features. The answer still sits in the next row, though, and `genergy`/`gpuls` follow smooth trajectories, so the order could be rebuilt. The robust fix is to score row by row and give the model only the rows up to the prediction point.

**Not exploits (signal a deployed model has):**
- The current row's `maxenergy ≥ 10⁴` is the previous row's label. It raises P(y=1) from 0.061 to 0.135, and the model already has it as a feature.
- Lag features of earlier shifts are legitimate. They did not help: 0.577 vs 0.602, within noise.

**Flaws that hurt an honest model.** None confirmed. The positive rate falls over time (training 6.7–8.9%, test windows 1.2–8.1%). Dropping `shift_order` scored 0.567 and adding lag features 0.577. Both sit inside the noise band, so neither choice clearly beats the baseline.

**Noise check.** Adding one random column to the baseline gives means of 0.552, 0.657 and 0.610 over three seeds. Per-split AUCs swing wildly: window r1 has one positive and scores between 0.02 and 0.55. Any honest gain below about ±0.05 is noise here. The leak's +0.40 is far outside that.

**Attacks that found nothing:**
- **Exact duplicate feature rows across the split:** 0.
- **Formats:**
  - `energy` and `maxenergy` are multiples of 100 in 100% of class-0 rows and 99.4% of class-1 rows.
  - `genergy` ends in 00 for 10.4% of class-0 rows and 12.4% of class-1 rows. Nothing usable.
- **No columns are scaled or ranked over the whole table**, and the task has no weight.
- **`shift_order` as a feature:** it slightly helps (0.602 vs 0.567 without it, within noise). It is the legitimate time index and reflects the falling positive rate.

**Web.** UCI and OpenML confirm that each row is one shift and that the class refers to the next shift. They do not say the rows are consecutive in time, and I found no published discussion of the leak. The kit has 6 fewer rows than the published file (2408 vs 2414 class 0); those rows were dropped without breaking the chain. Looking rows up in the published file would also work, but that is not a flaw of the task.

**Not checked:**
- A train-vs-test adversarial classifier. It is moot given the leak.
- Whether the data mixes two longwalls, as the source describes. The single unbroken lead chain suggests it is one sequence, or at least sorted that way.

Sources: [UCI seismic-bumps](https://archive.ics.uci.edu/dataset/266/seismic+bumps), [OpenML 1500](https://api.openml.org/d/1500), [OpenML 45562](https://api.openml.org/d/45562), [datahub README](https://r2.datahub.io/clu849xgz0005ic08loiq97jq/main/raw/data/seismic-bumps/README.md)

</details>

<details><summary>Precedents</summary>

**Precedent checker (seismic_bumps, 2026-11-19)**
| Decision | Verdict | Precedents |
|---|---|---|
| Reopen (few bumps not Too Small) | consistent | TP-9/SPLIT-16 amended; lung_adenocarcinoma_metastasis (5 positives per fold kept, 11-11); rosbank1. Housekeeping: TP-9/SPLIT-16 Cases rows still list seismic as the Too Small example |
| Leaf Temporal · rebuilt order, no gap | consistent | SPLIT-22 case, wine_quality, labour_inspection_compliance, mercedes; LEAK-9 protocol note per bank_marketing |
| Issue 1 window 86 shifts | departs, weak reason | siblings set length by count (mercedes 320 for 9, wine 292/295, loan_default 5,000, labour 1/6); "four weeks at 3 shifts/day" contradicted by data (W/N breaks 3-a-day cycle at 2,234 positions); sounder reason SPLIT-17 (coffee_rating): 30x43 and 14x86 test the same newest half |
| Issue 1 option D (label-placed cuts) | con too strong | TP-9/SPLIT-16 prescribe moving a cut until it holds a positive |
| Issue 2 14 vs 15th at 49.96% | consistent either way | ashrae_1m 49.47%, anes 49.2% (Lennart, CC); 30% exception adds little (tenths 4-5: 2 and 3 bumps) |
| Issue 3 shift_order input | DEPARTS, no distinguishing fact | labour file_row (11-12 Andrej issue 4 B: no input), wine_quality file_position (11-13 Andrej: "a row's place in an exported file is not something the grader holds"); order kept as input only for source-issued ids / dated order (mercedes, loan_default, bank_marketing) |
| Issue 4 weak signal keep | consistent | TP-2 step 1 passes (LightGBM p 0.048, TabPFN above 5 shuffles; forest_fires p 0.02 counted); step 2 keeps (bank_marketing 0.586, acquire 0.654, hr_analytics 0.62-0.63) |
| Issue 4 coupled to issue 3 | precision | without shift_order no method beats shuffles at p<0.05 (LR 0.10, LGBM 0.10, TabPFN not run): decide 3 first, then TabPFN without shift_order, 20 shuffles |
| Issue 4 B No Signal | would depart now | two methods beat shuffles |
| Issue 4 C Trivial / genergy tie | would depart from TP-4; tie overstated | genergy picked as best of >=6 features on test windows (TP-2 last sentence); train-chosen feature 0.470; ratings 0.48-0.51 -> like thyroid_discordant, aps_failure; unlike ljubljana (NPI), sepsis |
| Issue 4 D superseded by aaia16 | would depart | selection.md "Small or dated" (body_density, hepatitis_c_egypt); aaia16 screening calls it another release (PROV-4) |
| Issue 5 roc_auc fallback | consistent | MET-5/6 (gallstone, ljubljana, heart_disease) |
| 6 copies dropped | consistent | LEAK-18/19 (wine, audiology); _clean drops all duplicates, correct here (exactly 6) |
| SEL-10/TP-10 not addressed | gap, low | features hold target's last observation; TP-10 leg 1: beat persistence / recent bump rate; no persistence ROC AUC computed (rain_in_australia; stock, appliances retired) |

Reflection prompt for issue 3 (recommendation b: time_of="label", orders split only, like wine_quality; then rerun TabPFN without shift_order, 20 shuffles). Options a keep as exception / b like wine / c reopen wine+labour / d amend the time-column rule.
Wording: issue 1 reason -> SPLIT-17; issue 4 "Decisive" bullet should call genergy tie a same-rows screen; C names TP-4, D names selection.md.

</details>

<details><summary>Advocate</summary>

**Advocate opening brief (seismic_bumps): ship with four wording fixes and one input change**
1. Next-row read = evaluation leak (LEAK-9, Should, P4): conceded fact (2,577/2,577; 1.000 reading the neighbour). Not a data leak (features known at shift end; deployed model cannot see t+1). Harness: Data Foundry hands out positions only (src/data_foundry/v2/splits.py); scoring is the external harness's ("a recommendation; the harness decides", schema.py); order_rows sorts temporal tasks by time column (v2/preprocessing.py; CLEAN-23 Must) so test rows arrive in shift order with shift_order. Concession: note "rows ship shuffled and are scored one by one" is false, rewrite. LEAK-9: fix in scoring or a protocol line, not the data; a method learning from the test block is called out. Precedents: loan_default_prediction_imperial_college (Andrej 11-10, next test row lifts Gini 0.20->0.63, kept with protocol line), spanish_motor_coverage (Andrej 11-09), medical_facility_operational_data (Lennart 11-05, MAE 13.85->6.83). LEAK-9 has no severity grade. Shuffling test rows breaks CLEAN-23; order rebuildable via genergy/gpuls anyway. Remedy: standard protocol line in curation_comments and splits_comment.
2. Real use case (source's own: destress shooting / withdraw workers); order proven (chain, 21-shift cycle); cleaning checks out; proxy target named in fit_reason, no retirement.
3. TP-2 step 1 passes: LightGBM 0.593 (p 0.048, 20 shuffles), TabPFN 0.637 above all 5 shuffles (0.395-0.545); step 2 keeps (bank_marketing 0.586, acquire 0.654, hr_analytics 0.62-0.63); source expects weak. Concession: without shift_order LR/LGBM p 0.10, TabPFN (0.583) not shuffled -> run TabPFN without shift_order vs 20 shuffles on Slurm before sign-off.
4. Not Trivial (TP-4): genergy same-rows screen of >=6 features; train-chosen feature 0.470; ratings 0.48-0.51; no published rule.
5. Not Too Small (TP-9): all windows hold a bump; 14 >= 3; lung_adenocarcinoma precedent. Window: set 84 (measured 4 weeks): 15 windows, 1-10 bumps, 49, >=51.1% train.
6. TP-10 leg 1 answered by panel/probes/baselines.txt: persistence (current shift's own bump >=1e4 J = last label) mean ROC AUC 0.488 over 14 windows vs models 0.59-0.64 (LGBM 0.605 baseline, TabPFN 0.637).
7. aaia16 supersession departs (selection.md Small or dated; PROV-4). Concedes issue 3 B (shift_order no input) per wine/labour. Wording fixes: tenfold drop near 350-390 (2.3x at 820); positives per tenth 11,72,33,2,3,8,15,8,11,7; record issue 1 says 15 windows; note test windows in later regime; cite AAIA'16 AUC in metric reason (MET-11).
Remedies mildest first: protocol line; wording; shift_order no input; window 84; TabPFN without shift_order vs 20 shuffles.

</details>

<details><summary>Advocate's rebuttal</summary>

**Advocate rebuttal (seismic_bumps)**
Concedes critic 1, 2, 4, 5, 6; 7 agrees. Point 3: accepts rule and ladder, disputes procedure:
(a) fix the window before reading results: 84 chosen now on the measured cycle; the 84 run decides; 86 only a sensitivity check (choosing the passing window = a choice on test rows; TP-2 last sentence, EV-1).
(b) one threshold for all families: TP-2 states none; panel precedent p < 0.05 vs 20 shuffles (forest_fires p 0.02 counted); clock_protein_toxicity retired at p 0.16; p 0.05-0.16 goes to the curator as close to the line, not automatic retirement.
(c) report shuffle spread: 1-10 bumps per window, shuffled means 0.38-0.67 (LR); 14-15 windows cannot detect gains under ~0.1; a narrow miss = data cannot show the signal, for step-2 weighing.
Keep sources: source's use (crew withdrawal, destress blasting); TP-2 step 2; bank_marketing 0.586, hr_analytics 0.62-0.63.
Joint state: fixes agreed (protocol line, time_of="label", window 84, number corrections, fit_reason and segment notes); verdict on TP-2 step 1 for the 84 run at p<0.05 vs 20 shuffles: any family passes -> keep (step 2, gain + spread in notes); none -> No Signal; 0.05-0.16 -> curator's call.

</details>

<details><summary>Critic</summary>

**Critic opening brief (seismic_bumps): ship only with changes; point 3 may become No Signal**
1. Protocol line false (LEAK-9): order_rows/order_positions (src/data_foundry/v2/preprocessing.py) stable-sorts temporal containers by shift_order; 85/86 test rows have label in next test row; gamer 1.000; column auditor 1,190/1,204, 1.000 all windows. Split auditor's "harmless" holds only if the protocol forbids reading other test rows. Remedy: protocol line as loan_default / spanish_motor (each test row from training rows + own features; method reading other test rows called out); still needed after dropping shift_order (order rebuildable via genergy/gdenergy).
2. shift_order no input: leaf "no input when it comes with the target" (order checked from the label chain); labour file_row 11-12, wine file_position 11-13; actor holds date, not row number; counts across 199-shift stoppage and two longwalls; test values beyond training range. Remedy Temporal(on="shift_order", time_of="label").
3. Without shift_order no method passes TP-2 step 1 yet: LR 0.564/0.579 p 0.10; LGBM 0.593/0.588 p 0.10; TabPFN 0.637/0.583 shuffles not run. Untrained screen: genergy 0.645 (13/14), coal flag 0.592, genergy x coal 0.674 (same-rows, not TP-4 proof). Remedy: decide 2, then TabPFN + LightGBM without shift_order, 20 shuffles each; none beats -> No Signal ladder; else keep under TP-2 step 2 with a note.
4. Window 84 not 86 (SPLIT-12/15): measured 21-row cycle; 15 windows, 1-10 bumps, >=51.1%; caveat cycle invisible after row 1105.
5. Wrong numbers: positives per tenth (11,72,33,2,3,8,15,8,11,7); tenfold drop 350-390 (2.3x at 820); prep stretch rows 906-1104 (199) not 940-1120; record issue 1 says 15 windows; "ship shuffled".
6. fit_reason / notes: proxy target (header: "not connected with accurate rockburst prediction"; median bump maxenergy 3e4 J, none 1e6); tests cover later segment only (row 1380+; ~116/170 bumps before row 906). No exclusion reasons.
7. Nothing found: persistence 0.488, trailing rates 0.32-0.48; aaia16 supersession departs (selection.md, PROV-4); next-shift type no source (CLEAN-19); reopening, copy drop, roc_auc, no gap consistent.

</details>

<details><summary>Critic's rebuttal</summary>

**Critic rebuttal (seismic_bumps)**
Agrees on nearly all remedies; one point open: TP-2 step 1 without shift_order (jobs 1397641/1397642).
Agreed changes in order: (1) protocol line (LEAK-9) in notes + splits_comment, worded as loan_default; (2) shift_order time_of="label" (wine, labour); (3) window 84 (15 windows, 1-10 bumps, >=51.1%); (4) wording fixes (positives per tenth, energy drop, prep stretch, "15 windows" in record, test windows in later regime); (5) proxy target in fit_reason; (6) metric reason cites AAIA'16 AUC (not checked by critic); (7) sign off only after the no-shift_order check.
Per point: 1 concede; 2 mostly concede, but "order proven" -> "adjacency proven; calendar cadence shown only for rows 150-905; all test windows after row 1380" (SPLIT-12, wording); 3 DISPUTE: passing numbers are with shift_order, which the advocate concedes is no input; without it LR 0.579 p 0.10, LGBM 0.588 p 0.10, TabPFN 0.583 untested; if none beats 20 shuffles at either length -> defining-column ladder No Signal, not keep under step 2 (step-2 precedents passed step 1 first); 4 concede (genergy x coal 0.674 same-rows screen, fact for a note); 5 concede; 6 concede (persistence 0.488); 7 concede.

</details>

<details><summary>Signal run without shift_order</summary>

**Decisive run: TP-2 step 1 without shift_order (jobs 1397643/1397644, 2026-11-19)**
The panel's signal script (tuned on a temporal inner split, last 20% of each train side; same pipeline on shuffled training labels, 20 shuffles each; windows newest first, every window >= 50% training). p = (shuffles >= real + 1) / 21.
| Method | 84 shifts (15 windows): mean ROC AUC | p | 86 shifts (14 windows): mean ROC AUC | p |
| LR | 0.588 | 0.19 (shuffles 0.596, 0.608, 0.589 above) | 0.579 | 0.24 |
| LightGBM | 0.548 | 0.24 | 0.588 | 0.095 |
| TabPFN 3.5 | 0.579 | 0.095 (one shuffle 0.611 above) | 0.583 | 0.048 (max shuffle 0.578) |
Shuffled means range: 84 LR 0.402-0.608, LGBM 0.374-0.568, TabPFN 0.444-0.611; 86 LR 0.398-0.692, LGBM 0.365-0.588, TabPFN 0.386-0.578.
Agreed beforehand (advocate rebuttal, critic rebuttal): the 84-shift run decides; 86 only a sensitivity check; threshold p < 0.05 vs 20 shuffles; 0.05-0.16 = curator's call, stated as such; none passes -> No Signal (critic).

</details>

## Reference

See some of the papers on UCI
