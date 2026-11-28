---
unique_name: duolingo_spaced_repetition_recall
name: Duolingo spaced repetition learning traces (Settles and Meeder, ACL 2016)
checked_by:
- Myunghwan
- Andrej
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
priority: 2
tags:
- Non-IID (Temporal)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Varying Delay'
- 'Entities: Recur'
- Dated Event Log
original_source: Other
year: '2016'
collection_period: 28 Feb 2013 - 12 Mar 2013
domain: education
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.18653/v1/P16-1174
- https://doi.org/10.7910/DVN/N8XJME
- https://github.com/duolingo/halflife-regression
v2_path: datasets/_dev/tabarena-v0pt2/duolingo_spaced_repetition_recall_1m/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: 12.9 million Duolingo student-word practice traces (two weeks of 2013) with the share recalled in the session as the target, from the paper of the half-life regression model Duolingo deployed to schedule practice; education is thin, but the signal is weak (best MAE 0.128 against 0.175 for a constant) and the features are few.
- Source: Settles and Meeder, "A Trainable Spaced Repetition Model for Language Learning", ACL 2016 (doi 10.18653/v1/P16-1174); data on Harvard Dataverse (doi 10.7910/DVN/N8XJME, a 361 MB gzipped CSV), code on GitHub duolingo/halflife-regression (MIT licence for the code; the scout notes CC BY-NC 4.0 for the data, not checked). As published: "two weeks of Duolingo log data, containing 12.9 million student-word lesson and practice session traces" (Sec. 4.1); 12 columns `p_recall`, `timestamp`, `delta` (seconds since the word was last practised), `user_id`, `learning_language`, `ui_language`, `lexeme_id`, `lexeme_string`, `history_seen`, `history_correct`, `session_seen`, `session_correct` (README).
- Use case: the app predicts the probability that a learner recalls each word, which drives the strength meters and the choice of words to practise (Sec. 4.1: "Since the strength meters in Duolingo's interface are based on model predictions, we use MAE"; "Since our model is used to prioritize words for practice, we use AUC"); the paper deployed the model in "the production system" in two controlled user experiments (Sec. 4). Fit direct. Regime temporal: "using the first 90% for training and remaining 10% for testing" (Sec. 4.1), with learners on both sides of the cut.
- Siblings and duplicates: `assistments` (`TBD -> 2nd Tier`, knowledge tracing with per-attempt leaks) and `riiid_answer_correctness` (unscreened, next-answer correctness on EdNet): learner models on other platforms, no duplicate (searched Duolingo, spaced repetition, knowledge tracing). External collections: none found.
- Better data: from the gap scout for education; no further search this round.
- Papers and pages: the ACL paper (text read, Secs. 3 and 4, Table 2); the Dataverse record; the GitHub README (`evaluation.r` computes MAE, AUC and Spearman correlation).
- Metric: the paper reports MAE, AUC and the half-life correlation "for a comprehensive comparison" (Sec. 4.1, Table 2), three with a reason each and no single criterion, so the fallback `rmse` (MET-5, MET-8); inputs none.
- Risks for /add-dataset: `p_recall` is `session_correct` / `session_seen`, so both go (LEAK); the target is a share of a few exercises, mostly 1 (training mean 0.859, Table 2); a weak signal (the best AUC 0.538, Table 2; TP-2, keep if real); `lexeme_id` has a high cardinality and `lexeme_string` is a morphological tag string; 12.9M rows need a cap; data from 2013; the decision is a prioritisation of words, which the curator may read as ranking (SEL-9), while the task as published is a per-word recall regression.
- Priority: gap + (education), use case + (the paper names the deployed uses), source + (ACL paper, Dataverse and code), shape + (12.9M traces, categorical and numeric, temporal, learners), risk - (a weak signal and few features).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the gap scout for education.
- as published: about 13 million student-word lesson traces x 12 columns: p_recall, timestamp, delta since last practice, user_id, learning and UI language, lexeme id and tag, history_seen, history_correct, ...; target: p_recall, the share of exercises in the session where the word was recalled correctly (session_seen and session_correct are its inputs and must be dropped); access: open.
- Why: a documented, open dataset of a company's deployed model, with the paper's metrics (MAE, AUC)
- Adds: a large learning-analytics regression task grouped by user with a time order; few features, and close to knowledge tracing (see the assistments record, kept as 2nd Tier), so a weaker hit

**Retained local curation history (2026-11-05):** The following dated discussion and curator choices predate this main refresh; their dates and attribution remain historical.

CC (2026-11-02, Myunghwan): proceed to add-dataset following screening review. Qualify the original continuous session-recall proportion at session start using prior information and chronological evaluation. Current-session counts are not predictors. Do not silently replace the target with ranking, binary single-answer correctness, inferred memory half-life, or cold-start evaluation. This accepts investigation, not final inclusion, a scope exception, or a build/commit. Independent precedent checking found this consistent; timing, scope and empirical validity remain subject to actual-data qualification.

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: 12.9 million Duolingo student-word practice traces (two weeks of 2013) with the share recalled in the session as the target, from the paper of the half-life regression model Duolingo deployed to schedule practice; education is thin, but the signal is weak (best MAE 0.128 against 0.175 for a constant) and the features are few.
- Source: Settles and Meeder, "A Trainable Spaced Repetition Model for Language Learning", ACL 2016 (doi 10.18653/v1/P16-1174); data on Harvard Dataverse (doi 10.7910/DVN/N8XJME, a 361 MB gzipped CSV), code on GitHub duolingo/halflife-regression (MIT licence for the code; the scout notes CC BY-NC 4.0 for the data, not checked). As published: "two weeks of Duolingo log data, containing 12.9 million student-word lesson and practice session traces" (Sec. 4.1); 12 columns `p_recall`, `timestamp`, `delta` (seconds since the word was last practised), `user_id`, `learning_language`, `ui_language`, `lexeme_id`, `lexeme_string`, `history_seen`, `history_correct`, `session_seen`, `session_correct` (README).
- Use case: the app predicts the probability that a learner recalls each word, which drives the strength meters and the choice of words to practise (Sec. 4.1: "Since the strength meters in Duolingo's interface are based on model predictions, we use MAE"; "Since our model is used to prioritize words for practice, we use AUC"); the paper deployed the model in "the production system" in two controlled user experiments (Sec. 4). Fit direct. Regime temporal: "using the first 90% for training and remaining 10% for testing" (Sec. 4.1), with learners on both sides of the cut.
- Siblings and duplicates: `assistments` (`TBD -> 2nd Tier`, knowledge tracing with per-attempt leaks) and `riiid_answer_correctness` (unscreened, next-answer correctness on EdNet): learner models on other platforms, no duplicate (searched Duolingo, spaced repetition, knowledge tracing). External collections: none found.
- Better data: from the gap scout for education; no further search this round.
- Papers and pages: the ACL paper (text read, Secs. 3 and 4, Table 2); the Dataverse record; the GitHub README (`evaluation.r` computes MAE, AUC and Spearman correlation).
- Metric: the paper reports MAE, AUC and the half-life correlation "for a comprehensive comparison" (Sec. 4.1, Table 2), three with a reason each and no single criterion, so the fallback `rmse` (MET-5, MET-8); inputs none.
- Risks for /add-dataset: `p_recall` is `session_correct` / `session_seen`, so both go (LEAK); the target is a share of a few exercises, mostly 1 (training mean 0.859, Table 2); a weak signal (the best AUC 0.538, Table 2; TP-2, keep if real); `lexeme_id` has a high cardinality and `lexeme_string` is a morphological tag string; 12.9M rows need a cap; data from 2013; the decision is a prioritisation of words, which the curator may read as ranking (SEL-9), while the task as published is a per-word recall regression.
- Priority: gap + (education), use case + (the paper names the deployed uses), source + (ACL paper, Dataverse and code), shape + (12.9M traces, categorical and numeric, temporal, learners), risk - (a weak signal and few features).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the gap scout for education.
- as published: about 13 million student-word lesson traces x 12 columns: p_recall, timestamp, delta since last practice, user_id, learning and UI language, lexeme id and tag, history_seen, history_correct, ...; target: p_recall, the share of exercises in the session where the word was recalled correctly (session_seen and session_correct are its inputs and must be dropped); access: open.
- Why: a documented, open dataset of a company's deployed model, with the paper's metrics (MAE, AUC)
- Adds: a large learning-analytics regression task grouped by user with a time order; few features, and close to knowledge tracing (see the assistments record, kept as 2nd Tier), so a weaker hit

**Assessment (AI, 2026-11-02):** added provisionally as duolingo_spaced_repetition_recall_1m for review, not built. The official v1.0 archive has 12,854,226 rows, 115,222 learners and 19,279 lexemes. Standard temporal budgeting yields 2,596,122 used rows and seven predictors in three one-day windows with 1M train/500k test each and a provisional one-day gap. Fit is approximate: session correctness includes within-session practice and feedback, clock/start/end timing and label latency are unverified, and prior counters have small continuity anomalies. Neither leakage nor an adequate latency bound is established. The paper assigns MAE to display prediction; provisional RMSE instead scores expected session performance, a curator choice. The source file training mean 0.896172 differs from the paper's 0.859, so historical scores do not establish current value. Table 2's best AUC is Leitner 0.542; HLR is 0.538. The Riiid sibling is screened, superseding the older discovery wording. Completed actual-data evidence and the independent panel belong in the definition review. Priority 4: gap + (education), use case + (documented strength estimates), source + (publisher/archive), shape + (large temporal table), risk - (timing, metric and counter uncertainties).

**Assessment (AI, 2026-11-02):** completed add-stage qualification and full independent ten-role panel, including one advocate/critic rebuttal each and final review editing. Recommendation ship after changes, with shipping held for unresolved prepractice clock availability and the metric decision; training-label maturity remains unverified, separate from the Should-level daily/partial-day simulation. Fixed chronological inner selection yields full-budget LightGBM RMSE 0.266211/0.267808/0.268566 versus mean 0.269600/0.271136/0.272381, modest positive signal on all three windows. An MAE-appropriate quantile model predicts constant one throughout each test fold; this ties median MAE 0.103155/0.104112/0.104691, not proof that every MAE model is trivial. No demonstrated current-outcome leakage; six-feature probe profile overlap 0.014%, full seven-input profiles including time zero. Final dataset check has zero errors and one unaccepted genuine-endpoint warning. Source timing facts cannot be made true by approval; source MAE versus expected-fraction RMSE is a separate weighing call. No build, commit or final ship decision. This completed evidence supersedes the earlier provisional priority4: official-factor measurement over163accepted definitions finds no thin education/regression/temporal coverage; bounded static-domain fallback handles two unrelated pinned-runtime QSAR import incompatibilities. Priority 2: gap - (no measured thin coverage), use case - (fit approximate, no direct-fit point), source + (original publisher/archive), shape + (large mixed temporal table), risk - (timing and metric unresolved).

CC (2026-11-02, Myunghwan): prediction-time inputs do not matter much provided timestamp is consistent; refit time is less concerning. Clarified: later dates and learner-disjoint in the same holdout. Stick to current record level with no special weighting; the metric concern is the target's quantized fractions induced by exercise counts, not exercise weighting. This is partial review, not a final ship decision or endpoint-warning acceptance.

**Assessment (AI, 2026-11-02):** independent consistency review supports applying conditional timing acceptance while retaining unverified source semantics. The new grouped custom split imposes calendar chronology and global learner exclusion; user_id is genuine group metadata, never a predictor. Equal-record RMSE remains provisional; session-equal fractional cross-entropy is under comparison. Historical recurring-learner temporal scores and exploratory exercise-weighted diagnostics do not qualify the changed holdout. Requalification and focused independent review are in progress.

**Assessment (AI, 2026-11-02):** applied and requalified Myunghwan's joint later-date and learner-disjoint holdout with equal record weights. The frame has 1,752,858 rows, seven predictors and 55 observed fraction values. An independent full-source rebuild reproduces every value and index; 70,766 training learners and 8,824 test learners have zero overlap. Each of three windows trains on one million rows and tests 133,517, 223,084 or 205,718 rows. Exact deduplication removes 81 full raw record copies, without merging distinct learners or denominator records. New full-budget model diagnostics show a small positive signal on every window: mean RMSE is 0.26534 for the constant baseline, 0.26345 for RMSE training and 0.26274 for fractional cross-entropy training. Predictions are constrained for these diagnostics; the standard RMSE scorer itself is unchanged. The MAE-trained diagnostic predicts one throughout each test fold. Numeric regression losses can score a quantized fraction's conditional mean without assuming continuous noise or classifying its support values. Source MAE remains a deliberate criterion; the final metric is undecided. Checks have zero errors and two unaccepted warnings: genuine target dominance and the calendar layout rather than generic grouped cross-validation. The complete focused panel preserves the settled timing acceptance, equal-record weighting and combined holdout. A local group-probe adapter scores only actual test indices; the original helper's invalid all-row learnability run was canceled and excluded. No replacement metric, denominator weights, warning acceptance, ship verdict, build or commit is inferred.

CC (2026-11-02, Myunghwan): the current session_seen-driven fraction artifacts do not make sense as the final task. Either include session_seen and predict the count-dependent values, or simplify the target to be less sensitive, for example accuracy above 70%. This explicitly authorizes investigating both task repairs; no alternative or final cutoff is selected. Equal record weighting and the combined later-date/learner-disjoint holdout remain in force.

**Assessment (AI, 2026-11-02):** investigated both repairs on the exact qualified frame and outer indices; all 15 candidate score rows independently reproduce within 7.08e-15. Adding realized session_seen changed mean RMSE from 0.26345 to 0.26301 under the frozen earlier model configuration, a conditional/oracle diagnostic rather than evidence the final count is known before practice. The paper describes adaptive lesson continuation, so a genuine count-availability contract is required for a prospective conditional task. The illustrative strict >70% label is positive in 86.79% of raw and 86.89% of prepared records. Without current count as a feature, its fixed-configuration classifier reaches mean ROC-AUC 0.61497 and log loss 0.37289 versus prior baseline 0.38224. Coarsening does not eliminate denominator dependence: for 1–3 encounters it requires all correct, whereas 3/4 passes. Recommend the binary direction for the original before-practice goal if a meaningful operational success criterion is chosen. No final target, threshold, added predictor, source-convention claim or ship decision is inferred. The former metric-only recommendation is superseded; the saved definition is retained as baseline evidence pending task choice.

CC (2026-11-02, Myunghwan): “70% was only illustrative. I wanna check both directions”. Investigate both the session_seen-conditioned count/fraction direction and simpler outcomes; no route, cutoff or final metric is selected. Equal record weights and the joint later-date/learner-disjoint holdout remain settled.

**Assessment (AI, 2026-11-02):** completed both extended checks and independent verification of all 30 primary scores and 240 denominator subgroups (maximum primary discrepancy 1.11e-16). Given realized n, a supported count distribution improves mean record-level count log loss 0.45425 to 0.44272 versus an n-only empirical baseline, with little exact-count mode accuracy gain. Inner-selected beta-binomial is slightly worse in outer log loss than binomial on all windows; no extra-dispersion benefit or outer selection is claimed. This explicitly conditional task retains the realized-count availability limitation and would need an appropriate output/scoring contract. Without current n, strict majority, illustrative above-70% and all-correct events reach mean AUC 0.61696, 0.61497 and 0.63740 and improve their own prior log-loss baselines on every window. These are distinct events; neither their scores nor simple names choose operational meaning. Coarsening reduces precision but retains count dependence and practice-policy effects. The prior binary preference is superseded by this balanced evidence. The saved definition remains baseline only; no final task, threshold, metric, warning acceptance, build or ship decision is inferred.

CC (2026-11-02, Myunghwan): “OK let's stick to the original target and RMSE. And put num_seen as the predictor.” Preserve p_recall=session_correct/session_seen and use source session_seen as the numerical count predictor. This selects scalar expected accuracy conditional on supplied N, as discussed, with equal record weights and the combined later-date/learner-disjoint holdout. Source display MAE is consciously not adopted for this conditional mean-score task. No binary threshold, warning acceptance, final ship, build or commit is inferred.

**Assessment (AI, 2026-11-02):** independent precedent review supports applying the selected fraction+N task and RMSE without repeating settled formulation, metric, timing, weighting or holdout questions. The archive contains realized N; retain a conditional score-prediction interpretation and do not claim verified preplanned count availability or a causal effect of assigning N. Added session_seen to the definition; session_correct and learner ID remain outside model inputs. Affected checks and evidence-alignment verification follow before final review.

**Assessment (AI, 2026-11-02):** applied and rechecked the selected original p_recall target, RMSE and session_seen predictor for conditional expected session accuracy given N. The canonical frame has 1,753,189 rows, eight predictors and 60 observed fraction values. Adding N changes content-based ordering and row-budget sampling, so earlier +N predictions were not reused; affected leak, task and corrected group probes and paired fixed-configuration L2 trees were rerun. Mean RMSE is 0.265349 for the training mean, 0.265029 for the N-only mean, 0.263399 for paired trees without N and 0.262986 with N. No outer-selected configuration or metric, denominator weighting, endpoint filtering or binary threshold. Final checks have zero errors and the same two unaccepted warnings. Focused independent review preserves the chosen conditional realized-N interpretation, source-MAE departure and settled clock/holdout decisions. Only the genuine-target and layout warning dispositions and overall inclusion remain human choices. Build/commit not authorized. Priority 2: gap - (prior collection check found no measured thin coverage), use case - (conditional logged-process approximation), source + (traceable publisher archive), shape + (large mixed table), risk - (modest signal and unverified source timing details).

CC (2026-11-02, Myunghwan): “let's just do the temporal split only. no learner holdout”. This supersedes the earlier joint learner/date partition. Keep the original p_recall target, numerical session_seen predictor and equal-record RMSE. All learners are eligible for earlier training and later test windows; learner identity stays excluded from predictors. Retain three newest one-day windows and the one-day gap. Genuine-target warning acceptance, final inclusion and build/commit are not inferred.

**Assessment (AI, 2026-11-02):** independent consistency review supports applying the newer temporal-only choice without repeating earlier learner-transfer questions. Implemented standard temporal windows with source identity retained only during exact-record deduplication, then removed. Prior joint-split scores remain historical; actual data/splits, affected checks, probes and model evidence are being regenerated. The conditional realized-N and accepted recorded-clock limitations remain explicit.

**Assessment (AI, 2026-11-02):** completed temporal-only requalification after Myunghwan removed the learner holdout. The regenerated source-fraction task has 2,596,123 rows, eight predictors including session_seen and 55 observed fraction values. All three windows have one million earlier training and 500,000 later test rows with a one-day gap; no learner reservation or learner-ID predictor remains. Learner identity is retained only during duplicate removal and dropped afterward. New affected probes and model fits replace prior joint-split evidence; no historical predictions reused. Mean RMSE is 0.271519 for the training mean, 0.271083 for the N-only mean, 0.268116 for paired trees without N and 0.267615 with N. Inner iteration selection uses earlier dates and a one-day gap, without a learner restriction or outer tuning. Zero check errors and one unaccepted genuine-target warning remain; the grouped-layout warning is mechanically resolved, not human-accepted. Focused independent review retains the supplied-realized-N, clock, source-history and short-period limitations. Issue 5 closes; only issue 4 and overall inclusion remain human choices. No build/commit. Priority 2: gap - (prior collection check found no measured thin coverage), use case - (conditional logged-process approximation), source + (traceable publisher archive), shape + (large mixed temporal table), risk - (modest signal and unverified source timing details).

CC (2026-11-02, Myunghwan): reduce test rows to the original task's 90/10 ratio; confirmed “yes 90/10 ratio. I think original task is like that” after clarification of 111,111 test rows per 1M training rows. Retain temporal-only evaluation without a learner holdout, three latest one-day windows and the one-day gap, original fraction, numerical session_seen and equal-record RMSE. This is a cap ratio after sampling, not literal reproduction of the source's single file-order split. No genuine-target warning acceptance, final inclusion or build/commit inferred.

**Assessment (AI, 2026-11-02):** independent consistency review supports the smaller cap within the standard 500k ceiling. A dataset-local wrapper uses the same standard temporal windows and sampler with test_cap=111111; horizon and gap remain explicitly declared. Verify exact training/preprocessing equality and new-test subset correspondence before any row-level prediction reuse; otherwise refit. Recompute new holdout scores and affected bounded probes. The N-only baseline averages training fractions separately for each N, with equal record weights and no other features.

**Assessment (AI, 2026-11-02):** applied and requalified the curator-selected 1M train / 111,111 test rows per unchanged temporal window, approximately 90/10 after sampling. The package has 1,429,456 rows, eight predictors and 51 observed fraction values, with no learner holdout, the original p_recall target, numerical session_seen and equal-record RMSE. Raw ordered training values and each new test record map exactly to the preceding package, but lexical categories shrink from 15,289 to 13,639; strict prediction reuse was rejected and all affected fits/probes rerun. Mean RMSE is 0.271510 for the global training mean, 0.271079 for the N-only training mean, 0.268031 for paired trees without N and 0.267535 with N. The N-only baseline is an equal-record training-fraction mean by N, not a count or all-correct target; unseen N falls back to the global training mean. Zero errors and one genuine-target warning; no old aggregate metrics copied. Focused independent review preserves the conditional realized-N, accepted clock/history/short-period limitations and deliberate source-MAE departure. The numeric cap ratio is not literal reproduction of the source's single file-order cut. Only warning 4 and final inclusion remain unmarked; no build/commit. Priority 2: gap - (prior collection check found no measured thin coverage), use case - (conditional logged-process approximation), source + (traceable publisher archive), shape + (large mixed temporal table), risk - (modest signal and unverified source timing details).

CC (2026-11-03, Myunghwan): "yes, let's do this way." selects the proposed inclusive >=75% session-accuracy classification evaluated with AUROC. Further instruction: "and make it very clearly about this change -- not ruining the practical meaning (estimating the perf) while varying the loss/target". Preserve session-performance estimation conditional on supplied numerical session_seen N and prior/context inputs. The selected summary changes from expected fraction E[K/N|X,N] to probability P(K/N>=0.75|X,N), not merely its evaluation metric. The 75% criterion is explicit curator direction, not a documented source mastery convention; this task-specific choice supersedes the skill's default established-convention preference without claiming a general rule amendment. Retain equal-record treatment, temporal-only three one-day windows and one-day gap, 1M/111111 caps, no learner holdout or outcome filtering. The classifier framing has its own _clf identity and replaces the active regression framing; prior bytes/results remain historical evidence. Diagnostic classifiers use binary log loss for training, roc_auc for benchmark evaluation, and log loss for secondary diagnosis. AUROC does not assess calibration or recover expected accuracy. No final inclusion, build/commit or warning acceptance inferred.

**Assessment (AI, 2026-11-03):** applied and qualified the inclusive 75% session-performance classifier as duolingo_spaced_repetition_recall_1m_clf, replacing the active regression framing. The practical purpose remains estimating session performance given N and prior context. The estimand changes from expected fraction E[K/N|X,N] to event probability P(K/N>=0.75|X,N); diagnostics train binary log loss and evaluation uses roc_auc. The criterion is curator-selected, not source-defined mastery. Eight predictors retain numerical realized session_seen; source fraction, current correct count and opaque IDs are excluded. Source-copy removal precedes coarsening, with no outcome filtering or exercise weighting. Three temporal one-day windows retain a one-day gap, 1M training / 111,111 test records and no learner holdout. Native checks report zero errors and warnings; task probes have no flags and source-label/binary leakage checks are complete. The final 1,429,456 rows have 86.75% Yes. Changing the target changed actual sampled records despite identical index-array hashes, so all affected models and probes ran fresh. Mean AUROC: constant 0.500000, N-only binary rate 0.596148, classifier without N 0.622571, classifier with N 0.663756. The full model beats N-only on AUROC and log loss in every window. Independent column, split and numerical audits, mediator and cold editor support the package. The regression warning closes through retargeting, not acceptance; issue 6 concerns final inclusion only. Realized-N conditioning, source-clock/arrival uncertainty, imperfect histories and short coverage remain limits. Formulation choice followed exploratory outer-window evidence, not pristine confirmation. No final inclusion, build/commit or peer transfer is inferred. Priority 2: gap - (no measured thin-coverage bonus), use case - (conditional logged-process approximation), source + (traceable publisher archive), shape + (large mixed temporal table), risk - (timing and criterion/generalization limits).

**Assessment (AI, 2026-11-03):** rationale requested by Myunghwan, synthesized from the recorded discussion: retain practical session-performance estimation while changing the summary from expected fraction to the probability of achieving at least 75%. Small exercise counts create quantized, N-dependent fractions, and the earlier regression package had about 84% perfect scores; full-model RMSE gains were modest. This did not invalidate regression. The coarser event retains all records and numerical N, sacrifices within-class score detail and gives measured ranking signal beyond the binary N-only baseline (current mean AUROC 0.663756 versus 0.596148, with log-loss gains on every window). The 75% criterion is a curator-selected performance goal, not source-defined mastery or a denominator-invariant outcome. AUROC gains are not directly comparable to RMSE reductions, and explored dates are not untouched confirmation. Detailed rationale is in the definition review. Preparing review-added-datasets does not mark final inclusion or authorize build/commit.

CC (2026-11-03, Myunghwan): "yes" to the recommendation to include the completed >=75% session-performance classification with its documented limitations, after confirmation that final inclusion was the sole remaining decision. Ship as implemented; issue 6 accepted as implemented. Retain numerical realized session_seen, equal record weights, AUROC and the temporal-only 90/10 protocol. The output is probability of reaching at least 75%, not expected accuracy; the criterion is curator-selected. Realized-N conditioning, uncertain clock/label arrival, imperfect histories, short 2013 coverage and exploratory formulation selection remain explicit limits, not verified source facts. This is scientific inclusion only; no build, commit, push, publication or claim release is authorized.

**Assessment (AI, 2026-11-03):** independent decision/precedent review found the final inclusion consistent with the completed qualification and prior explicit task choice; no new reflection question is needed. Recorded the actual ship verdict and issue-6 acceptance on their original exact native review identity, preserved the closed review and full panels in local evidence, and removed the now-empty canonical the Review. The approved definition and record retain all limitations. A native documentation recheck will verify identical data, category metadata, labels, metric and six split arrays; no models or probes need repeating for an approval note. The claim and WIP (DF) state remain pending later authorized integration; DF: Yes and release are not applied.

**Assessment (AI, 2026-11-03):** final approval follow-through is complete. Native recheck reports zero errors and warnings, with byte-identical serialized data, category/label state and all six train/test index arrays. AUROC and the scientific settings are unchanged, so existing models/probes remain applicable. Issue 6 is closed and no scientific decisions remain. The exact approval and application history are preserved on the original native snapshot. Ready for a separately requested build; no build, commit, publication or claim release performed.

CC (2026-11-03, Myunghwan): requested build and local commits for the approved Duolingo >=75% session-performance classification. Retain the accepted definition, numerical session_seen, equal record weights, AUROC and temporal-only 1M/111111 protocol. The follow-up training-size diagnostic supports retaining 1M rows for the current classifier. This request authorizes build/reproducibility verification and local repository commits; push, publication, merge and claim release remain separate.

**Assessment (AI, 2026-11-03):** completed the requested build as `01a1a36f-3f9a-72b9-8bd1-47d1a96fa6fc`, checksum `v2:18d351606c00ca77ce5f6707c1d477305d0e183492e0e8d05160bf28109285bb`, from clean source commit `7c1928bb7cb5da99bf21b04727790c2269366c7e`. The format-2 container contains 1,429,456 rows and eight predictors with the accepted temporal 1M/111111 protocol. Zero build errors or warnings; saved reload and checksum verification passed. All values, category levels/codes and six split arrays match the approved data, and the loaded container reproduces the saved model AUROCs. A check using only the single traced source gzip reproduces the checksum; a local raw-input backup was verified. The separate training-size diagnostic supports retaining 1M rows for this fixed LightGBM setup (mean AUROC 0.663756 versus 0.624079 for three 100k random draws per window, or 0.628121 at matched boosting rounds); it does not claim the optimum for every model family. No scientific decision remains. Record status and claim remain pending later authorized integration; no push, publication or claim release is performed.

CC (2026-11-05, Myunghwan): repeat add-dataset, review-added-datasets and build-commit against updated main using our past decisions; ask only when new input is needed.

CC (2026-11-03, Myunghwan): the declared metric roc_auc is checked: the curator explicitly selected AUROC for the inclusive >=75% event, then accepted inclusion as implemented. This faithful short form retains the original dated choice; it is not a new metric mark on a refreshed snapshot.

**Assessment (AI, 2026-11-05):** current-main participant review and independent refutation demonstrate a same-test successor-counter exploit: 3.32-5.18% label recovery at 99.97-100% precision, raising the frozen honest AUROC by 0.0210-0.0349 across three windows. This is new measured evaluation leakage, distinct from previously accepted uncertainty in source histories. Applied the current LEAK-9 protocol correction, following the November 5 medical-facility and fremtpl2 precedents: preserve valid own-row histories and all eight predictors, require train-only fitting and current-row predictions, forbid other test rows/future histories and test-block learning. Benchmark method checking remains required in BENCHMARK_CHANGES_TODO; no downstream enforcement is claimed. Past target, AUROC, numerical N, equal weights, temporal windows/gap/caps and inclusion decisions remain in force. No new curator acceptance or exception is invented.

**Assessment (AI, 2026-11-05):** review panel (focused current-main recheck): ship after the routine protocol correction, now applied; disputed: whether the new future-counter attack requires dropping legitimate histories or new human input (settled by current LEAK-9 and the medical-facility/sepsis precedents in favor of own-row predictions and required benchmark method checks); for the curator: no open issue, historical issue 6 retained and new issue 7 closed as an agent-owned policy repair. Exact data, category state and all six split arrays match the approved package; the current empty special_features metadata field explains the initial framework-only checksum change. Fresh native checks have zero errors/warnings and task probes no flags. The lexical ordinal-like dtype flag is refuted by the source meaning. Priority 2: gap - (no established thin-coverage bonus), use case - (conditional logged-process approximation), source + (publisher/archive), shape + (large mixed temporal table), risk - (timing/generalization limitations and required benchmark protocol enforcement).

**Assessment (AI, 2026-11-05):** repeated current-main build complete: format-2 container `01a1adef-2da5-75af-9a38-674925897d45` from clean source commit `8429113143096b5f196312d7cca1089cb18197ab`. Zero errors/warnings; saved reload and reproduction from the sole traced raw input pass. All approved values, categories, labels and six split arrays are unchanged, and saved model AUROCs reproduce. The current checksum includes the updated schema and explicit own-row protocol; it is not expected to equal the historical pre-protocol checksum. The review preserves dated human decisions and resolved history; no new scientific decision remains. Required downstream method checks for test-block learning remain in BENCHMARK_CHANGES_TODO; this build does not certify them. Source/build commits stay local and the claim remains pending integration.

CC (2026-11-05, Myunghwan): after the review procedures were updated, requested another add-dataset -> review-added-datasets -> build-commit cycle using our past decisions, asking for input only if something new is needed. This retains the previously approved task, metric, inputs, weighting, temporal evaluation and inclusion; it explicitly authorizes the repeated local build and commits. Original review marks remain on their original source identity.

**Assessment (AI, 2026-11-05):** review panel (focused qualification repeat): retain ship as implemented; disputed: none; for the curator: no open issue. The reviewed source is 9048f36a, matching the previous scientific/probe code and procedures; package versions are unchanged. Fresh definition and API checks report 27 checks with zero errors/warnings. Exact frame/category/label state and all six arrays match prior approval, and twelve saved AUROCs independently reproduce; prior probes, participant/refutation and batch-invariance evidence are explicitly retained as dated executions, not claimed as new runs. The known future-counter evaluation leak remains governed by the own-row protocol and pending downstream method checking. Priority 2: gap - (no established thin-coverage bonus), use case - (conditional logged-process approximation), source + (publisher/archive), shape + (large mixed temporal table), risk - (timing/generalization limitations and required benchmark enforcement).

**Assessment (AI, 2026-11-05):** current rule wording clarification: TP-7's established-convention condition is Must, stronger than the historical phrase "default established-convention preference". The inclusive 75% criterion is retained under Myunghwan's explicit task-specific direction and current request to reuse it, not a source convention or a claim that every TP-7 condition is satisfied. No general rule amendment or new curator exception is inferred; historical attributed CC text is preserved.

**Assessment (AI, 2026-11-05):** qualification refresh build complete: format-2 container `01a1ae4b-07ce-7d55-b885-f6b11cb52d72` from clean source `90e77a7ccbaadc25d903a32e255298f7ca31694a`. Checksum `v2:c20f832bb366fbe3e87b547b5ddf83cca1c5877f6d3f4e7bd16c1d9a25b6e6e3` matches the preceding accepted build exactly. Zero errors/warnings; saved reload and reproduction from the sole traced raw input pass. Approved values, category/label state, all six split arrays and saved model scores are unchanged. Native current review records the latest explicit retention instruction while preserving original approval marks. No new scientific decision remains. Benchmark-side own-row method checking remains required and unverified; local build/source commits and claim remain pending integration.

**Compatibility follow-up (AI, 2026-11-16):** The accepted 1M/111111 training/test caps remain unchanged. Current main removed the legacy temporal sampler signature and resolves only budget-suffix variants; this definition still needs sampler/name/raw-folder migration and requalification before a new build. The historical review, inclusion decision and build evidence are preserved; this rebase does not grant a new scientific exception.

**Assessment (AI, 2026-11-16; compatibility repair):** Use the plain definition name `duolingo_spaced_repetition_recall` for the already approved custom capped temporal protocol. The `_1m` suffix now selects automatic collection sampling, which retains full training history and is incompatible with custom splits. Preserve the accepted capped-training draw explicitly, then use the current test-sampling API. This is a compatibility repair, without changing target, inputs, metric, temporal windows, label-availability filtering or intended row membership. Historical build/source identities remain preserved; fresh build and exact data/split comparisons are recorded separately when complete.

**Assessment (AI, 2026-11-16; verified compatibility build):** Built the canonical `duolingo_spaced_repetition_recall` definition from clean source `a6a4ac56259a656b235696d1e74d0a8c36f68f68` as format 2 UUID `01a1e3a8-8cac-768b-9020-b03d7cb94769`, checksum `v2:8c78ceb1edbf5b54d0dbbe689e14fcc84fc1f0a6bea2db3f488d6135b0d192ab`. The 1,429,456 rows, every value/dtype/category and row order, target, features, metric and all ordered train/test arrays exactly match the previously accepted container. Preserve the approved fixed training draw and test caps; use eligible history after label-availability filtering, before sampling, for the temporal training-floor check. Saved reload/checksum verification and a separate check using only traced inputs both pass with zero errors or warnings. The regenerated card records the canonical name and current build. Original build/source commits and resolved scientific decisions remain preserved. No model refit or new scientific exception is inferred; required downstream method checks and previously accepted limitations remain in force.

**Assessment (AI, 2026-11-21):** collection facts set from the split audit: one row per learner-word session with its own Unix timestamp; the outcome is known when the session ends; learners and learner-word pairs recur (about 54% of rows follow an earlier session of the same pair).

**Assessment (AI, 2026-11-21):** review panel (full re-check): ship after changes; disputed: session_seen under LEAK-10's span clause or LEAK-41 (settled: span clause, both conditions measured, wording conflict to a cross-dataset item), the gap (SPLIT-10, settled: no gap as an application, not fugaku's exception), the windows (SPLIT-15, settled: every other day), TP-7 remedy (round(p) measured more rule-like in N, to the curator); for the curator: issues H and 8-12. Wording fixed in the definition: timestamp = lesson end, label exists then; lexeme counts 19,279 ids / 18,781 strings; pooled vs within-lesson AUROC note. Priority 2: gap - (no measured thin coverage), use case - (fit approximate, realized N), source + (publisher archive, code read), shape + (large temporal table), risk - (curator cutoff against TP-7, spans the outcome cuts on a minority of rows).

CC (2026-11-24, Andrej): "Option B: _1m, full training sides." (issue 12 B): the dataset ships as `duolingo_spaced_repetition_recall_1m`; each train side holds every earlier session and a benchmark samples 1M of them; the custom fixed draw is dropped; the collection's row budget applies (at most 500k test sessions per window), so the earlier 111,111 test cap and the 90/10 ratio no longer hold. Windows, the one-day gap and the target are unchanged.

**Assessment (AI, 2026-11-24):** applied issue 12 B and re-checked the definition: 0 errors, 0 warnings, 28 checks. The frame has 12,854,145 sessions; the training sides hold 11,116,635 / 10,067,081 / 9,101,009 rows (86.5% / 78.3% / 70.8%) for the test days 12/11/10 March, whose 642,626 / 1,094,884 / 1,049,554 sessions are sampled to 500,000 each (Yes 86.8% / 86.6% / 86.7%); the container holds 12,116,635 rows. Task probe on the new splits: LightGBM AUROC 0.634, random forest 0.601, session_seen alone 0.597, linear 0.549, dummy 0.500; LightGBM beats the dummy on all 3 splits; no flags. Not built.

CC (2026-11-24, Andrej): review issue 10, B: `session_seen` is dropped as a leak ("Under this formulation session_seen is clearly a leak and needs to be dropped"); the task is decided before the session from seven inputs.

CC (2026-11-24, Andrej): the declared horizon (one-day windows, a one-day gap, windows on 12, 11 and 10 March) is checked, as implemented (A).

CC (2026-11-24, Andrej): review issue 8, as implemented (A): the three newest days stay the test windows ("We have Sunday and two week days, this is fine").

CC (2026-11-24, Andrej): review issue 11, B: the label is the source's round(p), more than half of the session's exercises right, with the source's pooled ROC AUC; this replaces Myunghwan's 75% cutoff of 2026-11-03.

CC (2026-11-24, Andrej): review issue 13, B: `user_id` is a categorical input; the application knows its learner.

CC (2026-11-25, Andrej): review issue 9, D: the published delta is replaced by the time from the word's last practice to the end of the learner's previous lesson, known when the lesson starts.

CC (2026-11-25, Andrej): the declared split (three one-day windows on 12, 11 and 10 March, a one-day gap, whole earlier training sides; leaf L-ORDER.windows) is checked, as implemented.

CC (2026-11-25, Andrej): verdict ship; nothing open in the review. The build is stale until rebuilt.

CC (2026-11-25, Andrej): the value in the Outcome is corrected. The task probe's ROC AUC of 0.547-0.552 understates the task: the probe trains on the newest 200k rows of each training side, which hold only 11% of the test learners. Measured on the final features (LightGBM, a fixed 200k test sample per day):

| Training rows | Learner id | 10 Mar | 11 Mar | 12 Mar | Test learners seen in training |
|---|---|---|---|---|---|
| Newest 200k (the probe's cap) | yes | 0.586 | 0.587 | 0.585 | 11% |
| Random 1M | yes | 0.631 | 0.632 | 0.628 | 70% |
| Whole side (9-11M) | no | 0.638 | 0.639 | 0.637 | 73% |
| Whole side (9-11M) | yes | 0.651 | 0.654 | 0.649 | 73% |

## Review

**Outcome:** added as `duolingo_spaced_repetition_recall_1m`. Ship: the full re-check of 2026-11-21 kept the data and the task; the curator's decisions of 2026-11-24 and 2026-11-25 reshaped its label and inputs. Label: the source's own, more than half of the session's exercises right, scored with the source's pooled ROC AUC (issue 11 B), in place of the 75% cutoff. Inputs, all known before the session: the clock, two languages, the word, the learner (`user_id`, issue 13 B), two history counts and `delta_to_previous_lesson`, the time from the word's last practice to the end of the learner's previous lesson (issue 9 D); the realized exercise count `session_seen` is dropped as a leak (issue 10 B). Split: one-day windows on 12, 11 and 10 March with a one-day gap (H A, issue 8 A); each training side holds every earlier session (86.5%, 78.3%, 70.8% of the rows) and test days keep at most 500k sessions (issue 12 B). Validity: the timestamp is the lesson's end, so the label exists at it; a later test row's practice counters can reveal an earlier row's result, which predicting each test row from its own inputs keeps closed (issue 7). Value: LightGBM on the whole training side scores ROC AUC 0.649-0.654 with the learner id and 0.637-0.639 without (2026-11-25); the task probe's 0.547-0.552 comes from its cap of the newest 200k training rows, which hold only 11% of the test learners. `dataset check`: 0 errors, 0 warnings. Nothing open.

**Main points:** No open decision. Not a decision: the build is stale after this round's changes.


**Record judgment:** The record and definition agree. Issues 1-5 stay closed, their discussion kept in the comments. Issues 6 and 7 are settled. The full re-check of 2026-11-21 opens the horizon (H) and issues 8-12: the gap, the windows, `delta`, the realized count, the 75% cutoff against the rule on built targets, and the `_1m` name (settled 2026-11-24, B). The notes keep the known limits: N is the realized count, the source's practice counters are imperfect, the log covers 12 days of 2013, and the target was chosen after seeing test-window scores; the timestamp is now measured as the lesson's end. The target is the chance of reaching 75%, not the expected fraction correct.

**Horizon:**

* **Verdict:** keep one-day windows (medium confidence); drop the gap (medium confidence), since the label exists at the recorded time and the newest day is complete.
* **Length:** no source names a horizon or a refit cadence. The paper's own evaluation is one cut in file order (the first 90% of rows train, the last 10% test), about the newest 1.1 days (11 March 13:45 to 12 March 16:14, measured 2026-11-24), so one day is close to the source's own test span; a daily refit is our assumption[^x21d1].
* **Gap:**
  - The target is the session's own score, known when the session ends; the timestamp marks the lesson's end (measured 2026-11-21: the gap to the next stamp grows by 2.22 s per exercise of the later lesson, 0.96 s per exercise of the earlier), so the label exists at the recorded time and a cut on `timestamp` needs no gap for the label: the delay is within the time column's resolution (a second), the case in which the split tree's gap rules set none[^x24t1].
  - The newest day is as complete as a later read of it would be (about 42-45k rows an hour against about 43.7k on 10 March, estimated) and its share of recalls is unchanged (86.8% against 86.5-86.8%), so no selection by the outcome shows at the release end: the measured case in which the rules need no gap[^x21d2].
  - The one-day gap (Myunghwan, 2026-11-02/03) predates the rule that measurements decide the gap; with the 1M training cap it costs no training rows, only the newest day of history.
  - Rows that share a timestamp stay on one side under every option: each cut falls at a midnight, and tied rows share the same second.
* **Time frame:** 28 February 18:28 to 12 March 16:14 UTC 2013, the whole release (Harvard Dataverse v1.0), about 1.1M sessions a day; the newest day is partial. The three newest days are our choice (see the issue on the windows).
* **Options:**

  | | Option | What it does | Test windows | Pro | Con |
  |---|---|---|---|---|---|
  | A | One day, one-day gap (implemented) | Tests 12/11/10 March; training ends a full day before each test day starts | 3 windows, 111,111 rows tested each; train 86.5% / 78.3% / 70.8% before the cap | safe whatever the clock means; signed off before | gap far longer than the label delay; drops the newest day of history; tests 1-2 days ahead |
  | B | One day, one-hour gap | `gap=1, gap_unit="hours"`; same test days | 3 windows, 111,111 rows tested each; train just under 95.0% / 86.5% / 78.3% | closest to a refit that takes an hour | the hour rests on a refit latency no source names; the label itself exists at the stamp |
  | C | Two days, no gap | Tests 11-12, 9-10, 7-8 March | 3 windows, 111,111 rows tested each (sampled from about 1.7-2.1M); train 86.5% / 70.8% / 53.4% | each window holds a weekend day or two weekdays | the third window is near the floor[^x21d3]; no source points to two days |
  | D | One day, no gap | Same test days; training ends at the test day's midnight | 3 windows, 111,111 rows tested each; train 95.0% / 86.5% / 78.3% (measured 2026-11-24) | the label exists at the stamp and the newest day is complete; uses the newest day of history; closest to the source's ungapped cut | departs from the gap Myunghwan signed off; shares to re-measure before the build |

* **Recommendation:** D: the stamp is the lesson's end, so the label exists when the row is recorded, and the newest day is measured complete, which is the case in which the rules need no gap; it applies the rule, as melbourne_housing_market and lt_vehicle_loan_default_prediction did, and needs no exception; the one hour of B rests on a refit latency no source names. Decide with the windows (issue 8). **Decision:** keep A, or change to B, C or D?

**Notes for the AI:** For D, set `Temporal(on="timestamp", horizon=1, horizon_unit="days")` and `TemporalSplits(window=1, unit="days", n_windows=3)` (gap 0), with the step the windows issue chooses. For B, `gap=1, gap_unit="hours"` in both. On any change, rewrite the gap sentences in `task_summary.split`, `fit_reason`, the curation note on the three one-day windows and the splits comment (the source names no refit cadence; the label exists at the stamp; tied stamps stay on one side); rebuild only on the curator's ask; re-check the floor (the assert in `_make_splits`). The shares in the table are measured (`dataset windows duolingo_spaced_repetition_recall --window 1 --unit days --gap 0` and `--gap 1`, 2026-11-24); re-measure only for a gap not in the table. On any option, the splits comment gives the training shares before the cap (the README's 0.7 is of the sampled frame) and the count 3 against SPLIT-15's target of 3 (SPLIT-33's count for two thirds of the scored rows); the split tree's leaf is `L-ORDER.windows`, which a `splits_comment` may cite by its ID. Do not cite fugaku_hpc_job_failure as the basis for no gap: its no-gap is a recorded exception made where a selection by the outcome was measured. On any option, also set `split_leaf = "L-ORDER.windows"` (cross-dataset item, Andrej 2026-11-24: every definition names its leaf with its split decision); every option keeps three windows with at least half the rows in training, so none needs the windows exception.

[^x21d1]: **SPLIT-12** (Should): the horizon, the refit cadence, the gap and the time unit come from the use case and the source; the splits comment names each, or says the source is silent and what is assumed. The split tree's windows check: where the use case and the source are silent, a person sets them, so the daily windows stand on the curator's sign-off.
[^x21d2]: **SPLIT-10** (Should): a gap of about the label delay; "No gap is needed where the collection covers what the gap guards against and the measurements show neither: ... the newest period is as complete as a later read of it" (amended 2026-11-04/05, Lennart; cases melbourne_housing_market, lt_vehicle_loan_default_prediction). Here an application, not an exception.
[^x24t1]: Split tree (2026-11-24): Dated event log, the model meets cases after the data [LOG.meets] → Order and windows step on the recorded timestamp [ORDER.order], three one-day windows that keep half the rows [ORDER.windows] → **Temporal · windows on the time key** [L-ORDER.windows], the split shipped. Its gap rules (**SPLIT-10**, Should): "no gap where the delay is within the time column's resolution (a date: one day) or a written exception holds".
[^x21d3]: **SPLIT-14** (Must): every window trains on at least half the rows, down to 30% only as the curator's exception.

**Andrej (2026-11-24, ok):** As implemented (A).

**Resolved (2026-11-24, Andrej):** A, as implemented: one-day test windows (12, 11 and 10 March) with a one-day gap, training ending a full day before each test day. No change to the definition.

**Issues for Myunghwan:**

6. **Include the selected conditional session-performance task?**

   - **Problem:** Whether to include the completed conditional >=75% session-performance classifier with its documented limitations.
   - **Background:** The target, AUROC, numerical N, equal record weights and temporal-only protocol were already selected by Myunghwan.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Include as implemented (implemented) | Retain the approved task and documented limitations | Preserves the selected performance-estimation purpose | Approximate logged-process interpretation and short coverage remain |
     | B | Leave out | Exclude this candidate | Avoids its stated limitations | Discards the approved large temporal education task |

   - **Recommendation:** A, following the actual November 3 inclusion decision. **Decision:** already settled.

   **Resolved (2026-11-03, Myunghwan):** Answered exactly "yes" to including the completed task with its limitations; accepted as implemented. The original ship and issue-6 marks remain on their original review identity. The November 5 request carries these choices forward, without assigning a new snapshot to the old marks.

7. **Predict each session without reading later test-session histories?**

   - **Problem:** A later held-out session's history counters reveal an earlier session's result when a model can inspect the test block.
   - **Effect on the task:** Reading future test covariates gives information unavailable at the earlier session's prediction point.
   - **Experiments:** Independent feature-only matching within each full 111111-row test window reconstructs 3.32-5.18% of labels at 99.97-100% precision; adding this to frozen honest predictions increases AUROC by 0.0210-0.0349 across all three windows.
   - **Consistency:** Current policy separates test-block evaluation leakage from valid own-row history and applies a benchmark-checked prediction-access contract, as for the medical-facility and sepsis tasks.[^protocol]
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Fixed training state and current row only (implemented) | Keep eight predictors; prohibit other test rows, future histories, test-block fitting/statistics and cross-split held-out labels | Preserves legitimate prior history and all approved data/splits; follows current policy | Benchmark must audit each method and exclude test-block learning |
     | B | Remove history_correct and requalify | Ship seven predictors and remove derived accuracy-history features | Blocks the demonstrated counter-difference formula | Loses legitimate signal: bounded raw-model AUROC drops 0.0072-0.0131; changes the approved predictor set |

   - **Recommendation:** A, the routine current-policy remedy that retains the approved task. **Decision:** no new human mark is required for this protocol correction; downstream enforcement remains a benchmark obligation.

   **Resolved (2026-11-05, AI):** Applied the current general evaluation-leak rule and its existing precedents: explicit train-only fitting, frozen state and current-row-only prediction in the definition, plus the benchmark method-checking TODO. Batched computation is allowed only when each prediction is invariant to changes in unrelated test rows. This records an agent-owned correction, not new curator acceptance or verified downstream enforcement.

   [^protocol]: LEAK-9 (Should, amended 2026-11-05) fixes evaluation leaks in scoring or a protocol the benchmark checks; LEAK-7 favors the smallest valid repair; LEAK-34 protects legitimate prior history. See the current `medical_facility_operational_data` issue-7 decision and `sepsis_prediction_1m` snapshot contract. No dataset-specific exception or general rule amendment is introduced here.

11. **Keep the curator's 75% cutoff, or re-target to the source's own label or to the source fraction?**

   - **Problem:**
     - The definition builds the target (at least 75% of a session's exercises correct), and the cutoff is Myunghwan's choice, not a convention of the source or the field.
     - The rule on built targets asks for an established convention without exception, so the earlier acceptance (2026-11-03) does not cover it[^x21tp1].
     - The source's own evaluation binarises the same fraction as `round(p)`, positive when more than half the exercises are right, and on this data that label depends more on the count than the 75% label does.
   - **Background:** the publisher's `evaluation.r` computes `roc(round(p) ~ pp)` on the per-session predictions that `experiment.py` writes ([duolingo/halflife-regression](https://github.com/duolingo/halflife-regression), read 2026-11-21); R rounds 0.5 to 0, so the label is `2K > N` (K correct of N). Myunghwan asked for a target less sensitive to the count (CC 2026-11-02) and chose the 75% cutoff on 2026-11-03.
   - **Effect on the task:** under either label the chance of Yes depends on N through how many misses the cutoff allows; under `round(p)` it swings with the parity of N, so a model scores by learning that rule, not the learner.
   - **Experiments:** label rate by N on lessons of 15 or more exercises and mean recall by N on all lessons (full release); the gain of N under each label is in issue 10's table (all rows +0.040 for 75% against +0.071 for `round(p)`):

     | N | Rows (15+ lessons) | P(Yes), 75% | P(Yes), round(p) | Mean recall (all lessons) |
     |---|---|---|---|---|
     | 1 | 6.77M | 0.898 | 0.898 | 0.884 |
     | 2 | 2.53M | 0.834 | 0.834 | 0.910 |
     | 3 | 1.32M | 0.777 | 0.979 | 0.918 |
     | 4 | 0.63M | 0.959 | 0.959 | 0.917 |
     | 5 | 0.31M | 0.934 | 0.994 | 0.914 |
     | 6 | 0.14M | 0.907 | 0.989 | 0.915 |

     Mean recall is flat from N = 2, so the jumps in P(Yes) are the cutoffs' construction, not learning.
   - **Consistency:** audiology_diagnosis is the only case (classes merged by a convention of the field); no case has a source convention that is more rule-like than the curator's cutoff.
   - **Panel:** advocate and critic both conceded re-targeting to `round(p)` before the measurement, the critic on condition it be verified first; the mediator, after the measurement, leans keeping 75%.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep 75% (implemented) | Target unchanged; stands only with the clause on curator cutoffs put to the rules across datasets | keeps the settled task; the label depends less on N | needs a rule change made for one dataset so far; the cutoff stays a curator choice |
     | B | Re-target to round(p) | Yes when 2K > N, the publisher's own evaluation label; probes and fits rerun | follows the source's convention, as the rule asks | nearly doubles N's share of the score; P(Yes) swings with the parity of N; reverses Myunghwan's choice |
     | C | Source fraction, N as trials | Target `p_recall` with the count as the number of trials in the loss and the metric; no built target | no cutoff at all | reverses the switch from the fraction (CC 2026-11-03); the count becomes a weight the outcome cuts on 7.9% of rows; the metric changes |

   - **Recommendation:** B together with issue 10's B (changed 2026-11-24): without the count the two labels carry the same signal (ROC AUC 0.618 and 0.619), so the 75% cutoff's advantage, a label less tied to the count, no longer matters, while round(p) is the source's own label and needs no change to the rule on built targets. A if the count stays as an input. **Decision:** keep 75% (A), or re-target to B, C or D?

   **Notes for the AI:** The rule question (amend TP-7 for a curator-chosen cutoff) is a cross-dataset item; the clause proposed there: "A curator cutoff on a fraction the source records stands without a convention when the source's own binarisation is tested beside it on how rule-like the label is in the denominator, and the cutoff is less so; the definition names both labels and the test. Cases: duolingo_spaced_repetition_recall." For A, once that item is decided, add to the "Meaning of 75%" curation bullet: "The source's own evaluation binarises as round(p), 2K > N (evaluation.r); on lessons of 15+ exercises it makes the label more rule-like in N (P(Yes) 0.834 at N = 2, 0.979 at N = 3; N's AUROC gain +0.071 against +0.040 for 75%), so the 75% cutoff is kept." Add a CC line. For B: `df[self.target] = (2 * df["session_correct"] > df["session_seen"]).map({False: "No", True: "Yes"})`; update `target` name, question, predicted, use_case, changes, the label-construction bullet and the metric reason; rerun the leak and task probes. For C: target `p_recall`, regression with `session_seen` as trials; this needs the weight decision under LEAK-41 first.

   [^x21tp1]: **TP-7** (Must): "When the definition builds the target itself (merged or dropped classes), use an established convention, test each candidate (classes per test fold after dropping duplicates, signal, how rule-like the label is), and run the leak probes on the source's labels too." Case: audiology_diagnosis. A Must has no exceptions.

   **Andrej (2026-11-24, discuss):** I have troubles to understand why the task was designed that way. Why do we even use binary classification and not regression if there is a numerical target?

   Also, please explain to me what kinds of tasks the source approached, whic htargets and metrics where used, and why they were ruled out in favor of the current task definition?

   **Answer (AI, 2026-11-24):** the binary label was not forced by the data: the record has no fact that rules the source's fraction out, and measured, the fraction depends least on the exercise count of the three targets. A plain regression on the fraction is a fourth option (d below), and the recommendation moves to it.
   - **What the source did** ([Settles and Meeder 2016, Sec. 3.3 and 4](https://aclanthology.org/P16-1174.pdf); code [duolingo/halflife-regression](https://github.com/duolingo/halflife-regression), `experiment.py` and `evaluation.r`, read 2026-11-24):

     | | Offline evaluation on this log (Sec. 4.1, Table 2) | User experiments (Sec. 4.3-4.4, Table 4) |
     |---|---|---|
     | Unit | one learner-word session | learners in the live app, six weeks |
     | Target | p = share of the session's exercises on the word answered correctly (K/N); for the half-life term also h = -Δ / log2(p), worked out from p and the lag Δ, not observed | daily retention: share of learners who come back the next day (any activity, lessons, practice) |
     | Inputs | lag Δ, the prior seen/correct counters (as sqrt(1 + count)), the lexeme tag, a bias; logistic regression adds Δ; no model uses the session's own count N | n/a |
     | Models | half-life regression (4 variants: with or without lexeme tags and the h term), Leitner and Pimsleur (fixed formulas), logistic regression (2 variants), constant p = 0.859 | HLR against Leitner, then HLR without lexeme tags against HLR, as the app's scheduler |
     | Training loss | squared error on p, plus 0.01 x squared error on h, plus L2 (Sec. 3.3); p is clipped to [0.0001, 0.9999], h to 15 minutes - 274 days | n/a |
     | Metrics | MAE on p ("the strength meters ... are based on model predictions"); AUC "to help evaluate these rankings" (words to practise): in `evaluation.r` `roc(round(p) ~ pp)` on one row per session, so Yes when p > 0.5 (R rounds 0.5 down); half-life correlation: Spearman between predicted and worked-out h (`experiment.py`'s own `spearmanr` is in fact Pearson); no single metric is named as deciding | change in daily retention (%) |
     | Split | file order: first 90% train, last 10% test (measured: the test part runs 11 March 13:45 to 12 March 16:14) | randomised groups |
     | Best results | MAE 0.128 (HLR) against 0.175 (constant); AUC 0.538 (HLR), 0.542 (Leitner); half-life correlation 0.201 (HLR) | HLR: practice -7.3%, others n.s.; without lexemes: +1.7% to +12.0% |

     The user experiments are not in the data. Of the offline task, the half-life is no target of its own: given p and Δ (an input) it is a formula, and on the 83.9% of sessions with p = 1 it is set by the clips (Δ x 6,931 days, capped at 274 days whenever the lag is over about an hour).
   - **How the task as shipped came about** (from `## Comments`):

     | Date, who | Choice | Reason as recorded |
     |---|---|---|
     | 2026-10-31, AI (screening) | target `p_recall`, metric RMSE | the paper reports MAE, AUC and the half-life correlation side by side, none named as deciding, so the fallback metric[^x24r1] |
     | 2026-11-02, Myunghwan | keep "the original continuous session-recall proportion", no current-session counts as inputs | none beyond following the source |
     | 2026-11-02, Myunghwan | "Stick to current record level with no special weighting" | "the metric concern is the target's quantized fractions induced by exercise counts, not exercise weighting" |
     | 2026-11-02, Myunghwan | look into a binary target | "the current session_seen-driven fraction artifacts do not make sense as the final task. Either include session_seen and predict the count-dependent values, or simplify the target to be less sensitive, for example accuracy above 70%"; then "70% was only illustrative. I wanna check both directions" |
     | 2026-11-02, Myunghwan | fraction, RMSE, N as an input | "OK let's stick to the original target and RMSE. And put num_seen as the predictor."; the source's MAE "consciously not adopted" |
     | 2026-11-02, Myunghwan | temporal windows only; 1M / 111,111 rows | "let's just do the temporal split only. no learner holdout"; "yes 90/10 ratio. I think original task is like that" |
     | 2026-11-03, Myunghwan | at least 75% correct, AUROC | "yes, let's do this way." to a proposal the record does not keep; "make it very clearly about this change -- not ruining the practical meaning (estimating the perf) while varying the loss/target" |
     | 2026-11-03, AI (rationale he asked for) | same | "Small exercise counts create quantized, N-dependent fractions, and the earlier regression package had about 84% perfect scores; full-model RMSE gains were modest. This did not invalidate regression." |
     | 2026-11-03, Myunghwan | ship as implemented | "yes" to inclusion |

   - **Why the fraction was not shipped, as far as the record says:** only the two lines above: Myunghwan found the count-driven fraction values not to "make sense", and the AI rationale names the quantised values, the 84% of perfect sessions and the small RMSE gain, while saying none of them makes regression invalid. Why 75% and not 70% or all-correct, the record does not say; it calls the cutoff "curator-selected", "not a documented source mastery convention".
   - **Why the source's MAE was not taken:** not stated in the record beyond "consciously not adopted". Measured now: MAE rewards the median, and the median of p is 1. On this release's file-order test (the paper's cut), predicting 1 for every session scores MAE 0.104, the training mean 0.174 (the paper's constant: 0.175), HLR reported 0.128. The paper gives its mean as 0.859 against 0.896 here; with 0.859 the constant 1 would score about 0.141, so whether it beat HLR on the paper's own data is not established. On the data we ship it wins on every test day, and the record's MAE-trained model predicted 1 throughout (2026-11-02)[^x24r2].
   - **Measured on the release** (12,854,145 rows after removing copies; test days with the one-day gap, all rows of the day):

     | N (exercises of the word) | Rows | Share of rows | Mean p | p = 1 | p = 0 | P(Yes), 75% | P(Yes), round(p) |
     |---|---|---|---|---|---|---|---|
     | 1 | 7.58M | 58.9% | 0.884 | 0.884 | 0.116 | 0.884 | 0.884 |
     | 2 | 2.64M | 20.5% | 0.910 | 0.830 | 0.010 | 0.830 | 0.830 |
     | 3 | 1.36M | 10.6% | 0.918 | 0.776 | 0.001 | 0.776 | 0.979 |
     | 4 | 0.66M | 5.1% | 0.917 | 0.710 | 0.000 | 0.959 | 0.959 |
     | 5 | 0.32M | 2.5% | 0.914 | 0.647 | 0.000 | 0.932 | 0.993 |
     | 6 | 0.14M | 1.1% | 0.915 | 0.597 | 0.000 | 0.903 | 0.988 |
     | 7+ | 0.15M | 1.2% | 0.915 | 0.501 | 0.000 | 0.921 | 0.998 |
     | all | 12.85M | 100% | 0.896 | 0.839 | 0.071 | 0.867 | 0.892 |

     | Target | Share of its variance N alone explains |
     |---|---|
     | fraction p | 0.3% |
     | at least 75% (shipped) | 1.7% |
     | round(p) (source's AUC label) | 2.4% |

     | Test day | Rows | p = 1 | Distinct p | RMSE: training mean | RMSE: mean by N | MAE: training mean | MAE: constant 1 |
     |---|---|---|---|---|---|---|---|
     | 12 March | 642,626 | 83.8% | 53 | 0.2698 | 0.2694 | 0.1735 | 0.1033 |
     | 11 March | 1,094,884 | 83.7% | 56 | 0.2719 | 0.2715 | 0.1746 | 0.1047 |
     | 10 March | 1,049,554 | 83.7% | 51 | 0.2729 | 0.2724 | 0.1750 | 0.1049 |

     - The mean of p is flat from N = 2 (0.910-0.918); the count changes how the scores spread (more 1s at N = 1, more in-between values at larger N), not their mean. RMSE scores the conditional mean, so the quantised values do not get in its way; a cutoff turns that spread into jumps of P(Yes), which is where N's 1.7% and 2.4% come from.
     - 59% of rows have N = 1, where p is 0 or 1: there, RMSE on p is the Brier score of a yes/no answer.
     - Model fits on the fraction already in the record (2026-11-02, same three days, one-day gap, 1M / 111,111 rows, LightGBM): RMSE 0.271510 training mean, 0.271079 mean by N, 0.268031 trees without N, 0.267535 with N. N adds 0.0005; under the 75% label it adds 0.040 AUROC of the 0.166 above chance (issue 10's table). The gain over the mean is small (1.5% of RMSE); a small score alone decides nothing[^x24r3].
   - **What a regression on p changes:** the target is bounded in [0, 1] with 84% of rows at 1, 7% at 0 and 9% in between; no target is built, so the rule on built targets does not apply and needs no amendment; the metric (RMSE) is not the source's MAE, for the measured reason above; equal record weights stay (Myunghwan, 2026-11-02); the realized-count question (issue 10) stays, smaller, since N carries little of this target.
   - **Options** (B and C as above; d is new):

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Keep 75% (implemented, A) | Target unchanged | the settled task; less rule-like in N than round(p) | fails the rule on built targets unless it is amended for this one dataset; N explains 1.7% of the label against 0.3% of the fraction; the cutoff's number has no recorded reason |
     | b | Re-target to round(p) (B) | Yes when 2K > N | the source's AUC label | most rule-like in N (2.4%; P(Yes) 0.776 at N = 3 under 75%, 0.979 under round(p)) |
     | c | Fraction, N as trials (C) | `p_recall` with N as the trial count in loss and metric | no cutoff; weighs a session by its exercises | needs the weight decision first; reverses "no special weighting" (2026-11-02) |
     | d | Fraction, equal weights, RMSE, N as input (new) | Target `p_recall` (K/N), regression, RMSE; inputs as shipped; `problem_type` regression | the source's own target and its training loss (squared error); no built target, no rule change; the task Myunghwan chose on 2026-11-02; N explains least; fits measured (RMSE 0.2675 against 0.2715) | reverses the switch of 2026-11-03; MAE, the source's display metric, is replaced by RMSE (on this data MAE rewards predicting 1 everywhere); signal small in RMSE units; leak and task probes, check and fits to rerun |

   - **Recommendation:** d: the record gives no fact against the source's fraction, the regression avoids the rule failure that option a needs an amendment for, and on this data the cutoff adds the very dependence on N it was meant to remove (1.7% of the label's variance against 0.3% of the fraction's). It reverses Myunghwan's choice, so it is his and yours to make. **Decision:** keep 75% (a), or change to b, c or d?

   **Notes for the AI:** For d: `target = "p_recall"`, `problem_type = "regression"`, `Metric.fallback` RMSE with the reason (the paper reports MAE, AUC and the half-life correlation side by side; on this release MAE is won by the constant 1: 0.103-0.105 on the test days against 0.173-0.175 for the training mean); in `_clean` keep `p_recall` (computed as `session_correct / session_seen`), drop the label line; rewrite `task_summary` (question, predicted, use_case, changes), the label, metric and "Meaning of 75%" curation bullets and the metric reason; rerun the check, the leak and task probes and the fits; issue 10's numbers are measured on the 75% label and need redoing under d.

   [^x24r1]: **MET-5** (Should): "A paper that reports several metrics side by side ... without naming the one that decides has no unique original: declare the fallback, and list the reported metrics in the reason."
   [^x24r2]: **MET-2** (Must): "Match the data, the metric and the real task." The display of a recall probability needs a prediction near the mean, which MAE does not reward here.
   [^x24r3]: **TP-2** (Should): a signal is judged in two steps, only the first a test; the record's own wording elsewhere: "the score's size never decides".

   **Andrej (2026-11-24, discuss):** Is mae really off just because median of 1? Ultimately this is just a heavy tailed regression distribution and models should still improve?

   **Answer (AI, 2026-11-24, evening):** under MAE, no: measured, no model improves on predicting 1; under squared error, yes, a little. Untuned LightGBM on the fraction, the shipped inputs (with and without the exercise count), trained on 1M rows of each shipped training side (one run):

     | Test day | MAE, always 1 | MAE, LightGBM trained on MAE | RMSE, training mean | RMSE, LightGBM trained on squared error | Same, without the exercise count |
     |---|---|---|---|---|---|
     | 12 March | 0.1033 | 0.1033 | 0.2698 | 0.2668 | 0.2674 |
     | 11 March | 0.1047 | 0.1047 | 0.2719 | 0.2686 | 0.2691 |
     | 10 March | 0.1049 | 0.1049 | 0.2729 | 0.2691 | 0.2697 |

   - Why MAE fails here: a model trained on MAE predicts the median of the fraction given the inputs, and with 83.9% of sessions all correct that median is 1 for nearly every kind of session; the model collapses to the constant, so MAE cannot tell models apart. It is not the heavy tail itself but the mass at 1.
   - Under squared error the fraction is a usable target, and models do improve on the mean on every day, but by little: about 2% of the variance explained (RMSE 0.2668 against 0.2698). The exercise count adds 0.0006 of it.
   - For comparison, the binary 75% label as shipped: LightGBM ROC AUC 0.634 against 0.5 for the dummy, ahead on every split (the `_1m` task probe of today).
   - So option d (the fraction with RMSE) is a valid target with a weak signal, and the source's MAE is ruled out by measurement. The recommendation of earlier today (d) was made before this run; given the stronger signal of the binary labels, the choice is between a, b and d on how much signal the benchmark needs, and between a and b on the cross-dataset item on a curator's own cutoff. Recommendation: a or b over d; the issue stays open.

   **Answer (AI, 2026-11-24, later):** the two binary labels side by side, as Andrej asked in chat (one run on the 12,854,145 deduplicated sessions; untuned LightGBM on 1M rows of each training side, shipped inputs; means over the three test days, which agree to 0.003):

     | | 75% label (shipped) | round(p), more than half right (the source's AUC label) |
     |---|---|---|
     | Yes share, all sessions | 86.7% | 89.2% |
     | Yes share by exercises, 1 / 2 / 3 / 4 / 5 / 6 / 7+ | 0.884 / 0.830 / 0.776 / 0.959 / 0.932 / 0.903 / 0.921 | 0.884 / 0.830 / 0.979 / 0.959 / 0.993 / 0.988 / 0.998 |
     | Variance the exercise count explains | 1.7% | 2.4% |
     | No rows per test day | 85,027-146,455 | 68,577-118,346 |
     | ROC AUC, LightGBM, all inputs | 0.660 | 0.693 |
     | ROC AUC, LightGBM, without the exercise count | 0.618 | 0.619 |
     | ROC AUC, the exercise count alone | 0.596 | 0.628 |
     | Log loss: training share → LightGBM | 0.392 → 0.374 | 0.342 → 0.318 |

   - The labels agree on 97.5% of sessions; they differ only where 50% < p < 75% (319,393 sessions Yes under round(p), No under 75%).
   - Without the exercise count both labels carry the same learnable signal (0.618 against 0.619). round(p)'s higher AUC comes from the exercise count: with 3, 5 or more exercises almost every session is Yes under round(p) (an odd count cannot split evenly), so the count alone reaches 0.628.
   - So round(p) is the more rule-like label (the count decides more of it), the 75% label the one whose signal rests less on the count; both clearly beat the fraction under any loss (2% of the variance).

   **Andrej (2026-11-24, discuss):** So what do you recommend? round to align with the source, or are the arguments for 0.75 more convincing?

   **Answer (AI, 2026-11-24, evening):** round(p), together with dropping the count (issue 10 B).
   - The case for 75% rested on the count as an input: with the count, round(p) lets a model score by the count's parity (the count alone reaches ROC AUC 0.628 under round(p), 0.596 under 75%).
   - Without the count, that advantage is gone: both labels reach the same ROC AUC (0.619 and 0.618) on the same inputs, and agree on 97.5% of sessions.
   - round(p) is what the source evaluates (`roc(round(p) ~ pp)` in its evaluation code), so it meets the rule on built targets as written; 75% would need that rule amended for this dataset alone (the open cross-dataset item on a curator's own cutoff, which then lapses).
   - The fraction itself (option d) stays out: under MAE no model beats predicting 1, under squared error models explain about 2% of the variance.

   **Andrej (2026-11-24, change):** Option B: Re-target to round(p).

   **Resolved (2026-11-24, Andrej):** B, applied: the label is Yes when 2K > N (more than half of the session's exercises right; exactly half is No, as the source's R rounding gives), target `session_more_than_half_correct`; the metric is the source's own pooled ROC AUC on round(p) (`Metric.source`, its `evaluation.r`), no longer a fallback; the question, use case, prediction, changes, the estimand, label-construction and label-choice bullets and the decision table follow. `dataset check`: 0 errors, 0 warnings. Task probe: ROC AUC 0.555 (linear) / 0.552 (LightGBM) against 0.500, ahead on 3 of 3 days, flags `no_spread` and `drift_baseline` (questions for the tuned benchmark). The cross-dataset item on a curator's own cutoff lapses with it.

10. **Keep the realized exercise count now that failed lessons are seen to end early?**

   - **Problem:**
     - `session_seen` is the realized count of exercises, kept as an input (Myunghwan, 2026-11-02/03) without a claim that it is planned.
     - The count is a span the outcome can cut: lessons under 15 exercises (7.9% of rows) fall below 75% accuracy in 23-33% of cases against 0.9% of 20-exercise lessons, so many of them are failed lessons that ended early.
     - On those rows "given N exercises" does not hold, while on full lessons N is set before the outcome.
   - **Effect on the task:** for a minority of rows the count is partly a result of the session, not an input to it[^x21col3].
   - **Experiments:** LightGBM, 1M training rows, 111,111 test rows per shipped day, mean of the 3 windows; lesson = learner and timestamp, its size (the sum of `session_seen`) a diagnostic only, never a feature; gain of N = AUROC with the 8 shipped inputs minus AUROC without `session_seen` (higher is better), for the shipped label and the source's `round(p)` label of issue 11:

     | Test rows | Rows per window | 75% label: with N / without / gain | round(p) label: with N / without / gain |
     |---|---|---|---|
     | all | 111,111 | 0.666 / 0.626 / +0.040 | 0.700 / 0.630 / +0.071 |
     | lessons under 15 exercises (the outcome can cut N) | 9,140 | 0.622 / 0.615 / +0.007 | 0.649 / 0.607 / +0.042 |
     | lessons of 15 or more (the outcome did not cut N) | 101,971 | 0.668 / 0.621 / +0.047 | 0.700 / 0.625 / +0.076 |
     | 15 or more, and N of 2 or more | 44,405 | 0.683 / 0.615 / +0.068 | 0.777 / 0.628 / +0.149 |

     The count keeps its worth on the full lessons the outcome did not cut and adds little where failure cuts it, so the truncation is not where its score comes from; that worth is the label's construction (how many misses the cutoff allows at each N, issue 11), since mean recall is flat from N = 2 (issue 11's table). Mistakes do not add repeats of a word[^x21col5].
   - **Consistency:** the keep (2026-11-02/03) predates the rule on weights and rate denominators (2026-11-06) and the clause on spans the outcome can cut (2026-11-08); noaa_storm_events_damage kept its Flash Flood durations with a note giving their worth on the rows the outcome did not draw; bank_marketing's `campaign` is set apart, recorded after its prediction point, where here the curator placed the prediction point after N is set. Whether the rule on weights and rate denominators also reaches a count the label is built from is a wording question across datasets, raised separately[^x21col4].
   - **Panel:** the advocate reads it under the span clause and keeps it with a note; the critic reads it under the rule on rate denominators and drops it; the blind review, without our notes, would drop it or redefine the target; the mediator finds both conditions of the span clause measured and leans keep.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the count with a note (implemented) | To add: a `Potential leak, kept on purpose:` note giving its worth on full and short lessons | keeps the settled conditional task; worth measured on the rows the outcome did not draw | the count is partly drawn by the outcome on 7.9% of rows |
     | B | Drop `session_seen` | 7 predictors (0.626 AUROC); the task becomes before practice | no input drawn by the outcome | reverses a settled curator choice; the label still depends on the count |

   - **Recommendation:** B (changed 2026-11-24): the source never uses the count as an input, it is known only when the session ends and cut short by failure on 7.9% of rows, and with issue 11's B the labels lose nothing without it (ROC AUC 0.618 and 0.619 without the count); A only if the 75% label stays. **Decision:** keep A, or change to B?

   **Notes for the AI:** For A, add to the "Prediction contract" bullet: "Potential leak, kept on purpose: failed lessons end early (lessons under 15 exercises, 7.9% of rows, fall below 75% accuracy in 23-33% of cases against 0.9% at the standard 20), so on those rows N is cut short by the outcome; N adds +0.047 AUROC on lessons of 15 or more, which the outcome did not cut, and +0.007 on lessons under 15 (LightGBM, mean of the three shipped windows, 2026-11-21)"; add a CC line. For B, drop `session_seen` in `_clean` and rewrite the question, `known` and the contract bullet. Evidence: the mediator's experiment of 2026-11-21 (panel).

   [^x21col3]: **LEAK-10** (Must), the span clause (a count of attempts the outcome can end); **USE-8** (Must): the fit names how closely the rows, the features, the label's timing and the split mirror the use case.
   [^x21col5]: At N = 3, all three answers are right in 0.766 of lessons against 0.683 if answers were independent at the mean recall (binomial), so a mistake does not bring the same word back within the lesson.
   [^x21col4]: **LEAK-10** (Must), second clause, says a column used as a weight or as a rate's denominator is **LEAK-41**'s (Must), whose own scope is weights (the metric's row weight, the training weight, a rate target's denominator); this task has no weight and a binary target, so by its own text LEAK-41 does not reach `session_seen`. The wording question goes to the cross-dataset items, not to this dataset.

   **Andrej (2026-11-24, discuss):** Is it valid to use the count as a feature and did the source allow it? Can we somehow adapt it to make sure there are no leaks?

   **Answer (AI, 2026-11-24, evening):** not fully valid, and the source does not use it; the clean adaptation is to drop it.
   - The source: none of its models (half-life regression, Leitner, Pimsleur, logistic regression) takes `session_seen` as an input; its features are the history counts (`history_seen`, `history_correct`), the lag and the word. The count enters only as the denominator of the fraction it predicts.
   - When it is known: the count is the realized number of exercises of the word in the session, known when the session ends, after the outcome; failed lessons end early (7.9% of rows), so there it is partly the outcome.
   - Adapting it: the planned count (the lesson's design) is not in the data; keeping only full lessons (15 or more exercises) would remove the cut rows but change the population the task covers; a count bucket keeps the same dependence. None removes the problem without changing the task, so dropping it (B) is the clean form.
   - What it costs: without the count, ROC AUC 0.618 (75% label) and 0.619 (round(p)) against 0.660 and 0.693 with it; most of the count's worth is the label's construction (how many misses each cutoff allows at each count), not the learner.

   **Andrej (2026-11-24, discuss):** Is it possible to identify the sessions that were terminated early? If we would be able to do that, would we then be able to use the feature because then it would be the real no. of exercises planned for the session?

   **Answer (AI, 2026-11-24, night):** not cleanly, and even where it can, using the count stays a leak. Measured on the 12,854,145 sessions, a lesson taken as one learner at one timestamp (901,059 lessons; its size the sum of its counts):

     | Lesson size (exercises) | Share of rows | Yes (75% label) | Accuracy in the lesson |
     |---|---|---|---|
     | 1-9 | 4.0% | 76.3% | 80.2% |
     | 10-14 | 3.9% | 77.7% | 83.1% |
     | 15-19 | 6.7% | 84.7% | 90.3% |
     | exactly 20 | 5.6% | 86.8% | 92.5% |
     | 21-25 | 10.6% | 87.1% | 91.0% |
     | 26 or more | 69.2% | 88.0% | 90.9% |

   - There is no planned length to compare with: only 11% of lessons have exactly 20 exercises, and most rows sit in sessions of 26 or more (practice sessions, or several lessons at one timestamp). Short lessons are less accurate, the trace of early stops, but a short lesson can also be a short practice by design, so an early stop is not identifiable row by row.
   - Where it could be identified, each use leaks: dropping the short lessons removes the rows richest in failure (Yes 76-78% against 87-88%), a selection by the outcome; blanking the count there makes the missing value say "failed lesson"; and a lesson is known to be full only after it ends.
   - The count of a full lesson would be the planned count, but the planned count itself is not in the data. The recommendation stays B: drop the count.

   **Andrej (2026-11-24, chat):** Under this formulation session_seen is clearly a leak and needs to be dropped.

   **Resolved (2026-11-24, Andrej):** B, applied. `_clean` drops `session_seen` with the outcome ingredients; the question, use case, `known`, `changes`, `fit_reason`, the prediction-contract, estimand and label-construction bullets and the decision table now describe a task decided before the session from seven inputs (clock, lag, two languages, the word, two history counts); measurements taken with the count are dated as such. The 75% label is unchanged (issue 11 open). `dataset check`: 0 errors, 0 warnings. Task probe: LightGBM ROC AUC 0.571, ahead of the dummy on 3 of 3 days, flag `drift_baseline` (a question for the tuned benchmark).

9. **Keep `delta` as recorded, now that it runs to the end of the current lesson?**

   - **Problem:**
     - Lesson timestamps mark the lesson's end, so `delta` runs from the previous practice's end to this lesson's end and includes this lesson's own length[^x21col1].
     - A lesson the learner fails ends early: 20-exercise lessons are below 75% accuracy in 0.9% of cases, lessons of 7-10 exercises in 32.8%.
     - For the 24.4% of rows practised in the learner's previous lesson (74% of them under 15 minutes), `delta` therefore partly records how this lesson went.
   - **Background:** `timestamp`, a datetime feature, is stamped at the lesson's end too; it holds the lesson's length, minutes, inside a day-level time.
   - **Effect on the task:** a feature the task calls known at session start holds a span the outcome can end[^x21col2].
   - **Experiments:** LightGBM, 1M training rows and 111,111 test rows per window, the three shipped windows (AUROC, higher is better):

     | Variant | Mean of 3 windows | Test rows with delta under 15 min (30% of them) |
     |---|---|---|
     | Shipped | 0.6652 | 0.6858 |
     | Delta floored at 15 min | 0.6627 | 0.6779 |
     | No delta | 0.6578 | 0.6765 |

     The floored variant keeps only the spans the outcome cannot draw (every break of 15 minutes or more), so its row against the no-delta row is the worth `delta` keeps on the rows the outcome did not draw. At one exercise, delta under 15 minutes ranks the label at AUC 0.566; the gap before the previous lesson, known at the start, at 0.541.
   - **Consistency:** the source's own model (half-life regression) uses this `delta`; noaa_storm_events_damage blanked the spans the outcome alone draws and kept the rest with a note giving its worth; unlike bank_marketing's `campaign`, recorded after its prediction point, most of `delta` (the break before the lesson) lies before the prediction point.
   - **Panel:** the column audit (2026-11-21) measured this on the full release; advocate and critic both recommend A.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep with a note (implemented) | `delta` as published; to add: a kept-on-purpose note with its worth on both parts | the source's feature, as in the paper; keeps worth on the spans the outcome did not draw | on the 24.4% of rows practised in the learner's previous lesson, `delta` is largely this lesson's own length |
     | B | Floor `delta` at 15 minutes | Every delta below 900 s becomes 900 | removes the current lesson's length from all back-to-back rows | also removes the legitimate break; costs 0.0025 AUROC |
     | C | Drop `delta` | 7 predictors | no span stamped at the lesson's end | costs 0.0074 AUROC; removes the source's core spacing variable |

   - **Recommendation:** A: the outcome draws the span only through lessons that end early, a minority of rows; `delta` keeps its worth on the spans the outcome did not draw; and the features cannot tell which short deltas a failure cut. **Decision:** keep A, or change to B or C?

   **Notes for the AI:** For A, add a curation bullet: "Potential leak, kept on purpose: `timestamp` marks the end of a lesson, so `delta` for words practised in the learner's previous lesson includes the current lesson's length, which a failed lesson cuts short; delta under 15 minutes is worth 0.0023-0.0028 AUROC (0.008 on its rows), and the spans of 15 minutes or more, which the outcome does not draw, keep about 0.005 (0.6627 with delta floored at 15 minutes against 0.6578 without delta, mean of the three shipped windows). `timestamp` is stamped at the lesson's end too: it holds the lesson's length, minutes, inside a day-level time."; amend `task_summary.known` and `fit_reason`. For B, `df["delta"] = df["delta"].clip(lower=900)` in `_clean`. Rebuild only when asked. Evidence: the column audit of 2026-11-21 (panel).

   [^x21col1]: The gap between a learner's consecutive lesson stamps grows by 2.22 s per exercise of the later lesson and 0.96 s per exercise of the earlier one; its 5th percentile rises from 20 to 178 s with the later lesson's size and from 20 to 59 s with the earlier one's.
   [^x21col2]: **LEAK-10** (Must), the clause on a span whose start or end the outcome can draw: the rest stays with a note giving its worth only when the outcome draws a minority of the spans and the span keeps its worth on the rows the outcome did not draw; the size of the worth alone never decides (2026-11-08, Lennart, on noaa_storm_events_damage).

   **Andrej (2026-11-24, discuss):** Can we somehow reconstruct the true time since the word was last practiced by looking at the user id and the last sessions that are not in the same period?

   **Answer (AI, 2026-11-24, night):** partly, and the part we can rebuild is free of the leak; added as option D. The lesson's start is not recorded, but the end of the learner's previous lesson is, and it is known when this lesson starts: the time from the word's last practice to that previous end is a lag the outcome cannot touch. It leaves out the break between the two lessons, which cannot be separated from this lesson's own length. Measured on the full release (one run; LightGBM with the learner, round(p) label, no exercise count; ROC AUC):

     | | Value |
     |---|---|
     | Rows where it is defined | 84.3% (missing where the learner's previous lesson is before the release, 4.8% of rows where the release misses a lesson) |
     | Rows where it is zero (word practised in the learner's previous lesson) | 27.6% |
     | What `delta` adds on top (the break plus this lesson's length), median / 90th percentile | 408 s / 23.5 h |
     | ROC AUC, `delta` as shipped / the rebuilt lag / no lag, 12 March | 0.628 / 0.624 / 0.621 |
     | Same, 11 March | 0.630 / 0.627 / 0.624 |
     | Same, 10 March | 0.629 / 0.627 / 0.622 |

     The rebuilt lag keeps about half of what the lag is worth, without the part the lesson's length adds.

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | D | Rebuild the lag from the learner's previous lesson | Replace `delta` by the time from the word's last practice to the end of the learner's previous lesson (`user_id`, timestamps), missing where that lesson is not in the release | no part of it is drawn by the outcome; keeps about half of the lag's worth | a built feature; missing on 15.7% of rows; drops the break before this lesson |

   - Recommendation, changed: D, since the shipped `delta` mixes in the lesson's own length, which a failed lesson cuts short; A only if the source's exact feature matters more than that leak.

   **Andrej (2026-11-25):** In this case I go with your recommendation D.

   **Resolved (2026-11-25, Andrej):** D, applied: `_clean` replaces `delta` by `delta_to_previous_lesson`, the time from the word's last practice to the end of the learner's previous lesson (0 where the word was practised in that lesson, missing where that lesson is not in the release or precedes the last practice); `known` and a curation bullet say so. `dataset check`: 0 errors, 0 warnings. Task probe: ROC AUC 0.552 (linear) / 0.547 (LightGBM) against 0.500, ahead on 3 of 3 days, flags `no_spread` and `drift_baseline` as before.

8. **Keep the three newest days as test windows, or spread them over the history?**

   - **Problem:**
     - The windows are the three days just before the release end (12, 11 and 10 March), and the splits comment gives no reason for that choice.
     - The rules now prefer windows spread over the eligible history and ask for a reason when walking back from the newest[^x21d4].
     - Test days back to 8 March keep more than half the rows for training under either gap the Horizon block weighs (53.4% with the one-day gap, 62.6% with none, measured 2026-11-24).
   - **Effect on the task:** the three windows are Sunday, Monday and Tuesday of one week; a spread set (12, 10 and 8 March) would test Tuesday, Sunday and Friday. Every window trains on 1M sampled rows either way.
   - **Experiments:** no model run (the rules choose windows on data statistics, not scores); `dataset windows` on the full file, 2026-11-24 (training share of all rows before the cap). Every day has the same share of Yes (86.4-86.9% on the test day against 86.5-86.9% on its training side) and no feature drifts from the training side (largest population stability index 0.002-0.010, `delta`), so the days differ by weekday only:

     | Test day | Train share, one-day gap | Train share, no gap | Weekday |
     |---|---|---|---|
     | 12 Mar | 86.5% | 95.0% | Tue (partial) |
     | 11 Mar | 78.3% | 86.5% | Mon |
     | 10 Mar | 70.8% | 78.3% | Sun |
     | 9 Mar | 62.6% | 70.8% | Sat |
     | 8 Mar | 53.4% | 62.6% | Fri |

   - **Consistency:** the windows were signed off on 2026-11-02, before the rule on choosing windows (2026-11-10); delivery_eta, aeolus_rebuilt and nyc_taxi_trip_duration took spread windows under it (Lennart, 2026-11-10); maps_router_eta kept its newest windows for a history with no other set above the floor, which does not hold here.
   - **Panel:** advocate and critic both recommend B; the split audit of 2026-11-05 checked the bounds and the floor only, not this choice.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Three newest days (implemented) | 12/11/10 March; the splits comment gets the reason | longest histories; no rebuild of the windows | adjacent days; no Friday or Saturday; walking back needs a reason the rules accept |
     | B | Every other day | 12/10/8 March | spread over the eligible days, as the rules prefer; Friday, Sunday and Tuesday | the oldest window nearer the floor (53.4% with the one-day gap, 62.6% with none); rebuild of the windows |

   - **Recommendation:** B: the rules prefer spread windows and every window of 12/10/8 March keeps more than half the rows for training, so nothing forces the walk back from the newest; it adds a Friday; delivery_eta, aeolus_rebuilt and nyc_taxi_trip_duration took spread windows the same way. **Decision:** keep the three newest days (A), or change to B?

   **Notes for the AI:** For B, `TemporalSplits(window=1, unit="days", n_windows=3, step=2)`, or the chosen days as `cutoffs=("2013-03-12", "2013-03-10", "2013-03-08")` as definitions.md declares a choice of windows, with the gap the Horizon decision sets (and the same gap in `Temporal`); the shares are measured (table); update `task_summary.split`, the curation note on the windows and the splits comment ("Tested days 12, 10 and 8 March 2013, every other day: Tuesday, Sunday and Friday, each with more than half the rows before it"). For A, append to the splits comment the reason the curator gives. Add a CC line either way.

   [^x21d4]: **SPLIT-15** (Must for the newest window, Should for the others): the newest window is always tested; prefer windows in other years, seasons, months, weeks or days over those just before the newest; walking back from the newest needs its reason (amended 2026-11-10, Lennart and Andrej).

   **Andrej (2026-11-24, ok):** There is no reason to believe that using earlier than the three newest date is in any way more diverse. We have Sunday and two week days, this is fine.

   **Resolved (2026-11-24, Andrej):** A, as implemented: the three newest days (12, 11 and 10 March) stay the test windows; they hold a Sunday and two weekdays. No change to the definition.

12. **Ship as `duolingo_spaced_repetition_recall_1m` with full training sides and a 1M / 111,111 row budget?**

   - **Problem:**
     - Since the house decision of 2026-11-10 (Lennart, issue #70), training sides keep every row and a set over the row budget ships under a `_1m` name, the benchmark drawing its training rows.
     - This definition draws 1M training rows itself under a plain name (an AI repair of 2026-11-16), and the record's first name was `duolingo_spaced_repetition_recall_1m` (2026-11-02).
     - fugaku_hpc_job_failure keeps the same kind of fixed draw for a fact this dataset lacks: its 384-dimension embedding makes a whole training side about 36 GB.
   - **Background:** this release is about 12.9M rows of 9 columns (8 inputs and the target), like aeolus_rebuilt_1m (13.7M rows); with 12 days of history the default draw (random 1M of the newest year before the window) draws the way today's fixed draw does, at random from every earlier row, though not the same rows, and Myunghwan's "retain 1M rows" (CC 2026-11-03) becomes the budget; the 111,111 test cap stays in the budget.
   - **Effect on the task:** none on what is scored; the container holds whole training sides and the name changes.
   - **Consistency:** 18 `_1m` folders follow the house decision; fugaku_hpc_job_failure keeps its cap with its size fact as the written reason.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Plain name, fixed 1M draw (implemented) | `_make_splits` draws 1M training rows per window; the budget samples the test side only | no rename or rebuild; the protocol Myunghwan signed off | departs from the 18 `_1m` sets with no fact that sets it apart; custom split code |
     | B | `_1m`, full training sides | Rename to `duolingo_spaced_repetition_recall_1m`; drop the custom draw; row budget 1M train / 111,111 test | follows the house convention; standard split code | rename of folder, class name and `v2_path`; rebuild |

   - **Recommendation:** B: nothing in this dataset sets it apart from the other sets over the row budget, and the fixed draw is the one fugaku keeps only for its embedding size. **Decision:** keep A, or change to B (decide with fugaku_hpc_job_failure)?

   **Notes for the AI:** For B: `unique_name = "duolingo_spaced_repetition_recall_1m"`, rename the folder, set the record's `v2_path`; `row_budget = RowBudget(train=1_000_000, test=111_111)`; replace the custom `_make_splits` draw by the standard temporal split (keep the floor assert), so each train side holds every earlier row; rewrite `task_summary.split`, the cap curation note, the trailing note and the splits comment ("each train side holds every earlier session; a benchmark samples 1M of them, by default at random from the newest year before the window"); the Outcome then opens "added as `duolingo_spaced_repetition_recall_1m`". Rebuild only when asked. fugaku keeps its cap with the embedding-size reason written in its splits comment.

   **Answer (AI, 2026-11-24):** fugaku_hpc_job_failure's issue 5 was marked C (`_1m` with whole training sides) on 2026-11-24, but that version does not pass `dataset check` on our largest nodes (its whole training sides hold 24.0M rows with 384 embedding coordinates each), so fugaku's issue 5 is open again with options. This dataset's 12.9M rows of 9 columns have no such size; options and recommendation stand.

   **Andrej (2026-11-24, change):** Option B: _1m, full training sides.

   **Resolved (2026-11-24, Andrej):** B applied. The folder, class and `unique_name` are now `duolingo_spaced_repetition_recall_1m` (record `v2_path` set; the record file keeps its name). The custom fixed 1M training draw is gone. The definition declares the standard windows (`Temporal(on="timestamp", splits=TemporalSplits(window=1, unit="days", n_windows=3, gap=1))`), so the horizon and the one-day gap stay as they are while the Horizon item is open. `split_leaf = "L-ORDER.windows"` is set. The framework's own floor check replaces the hand-written assertion, which the definition validator refuses beside declared windows. Each train side holds every earlier session: 11,116,635 / 10,067,081 / 9,101,009 rows (86.5% / 78.3% / 70.8%) for 12/11/10 March. A benchmark samples 1M of them. The collection's budget applies to the test side: each test day's 642,626 / 1,094,884 / 1,049,554 sessions are sampled to 500,000, because a definition in the collection cannot declare a budget of its own. So the 111,111 test cap of this option and the 90/10 ratio (CC 2026-11-02) no longer hold. The rewritten texts are `task_summary.split`, the row-budget curation note, the curator-decisions note, the split walk, the trailing note and the splits comment. The test that pinned the old draw (`tests/test_curated_temporal_compatibility.py`) is removed. Check: 0 errors, 0 warnings; README regenerated. Task probe: LightGBM 0.634 AUROC, beats the dummy on all 3 splits, no flags. Not built.

13. **Add the learner (`user_id`) back as an input?**

   - **Problem:**
     - The definition drops `user_id` (115,222 learners), but the app that predicts a learner's session always knows who the learner is.
     - It was dropped for a split that held whole learners out of training ("user_id is genuine group metadata, never a predictor", 2026-11-02); the same day that split was replaced by time windows in which learners recur, and the exclusion stayed without a new reason[^x24d1].
     - 71-74% of the test rows come from learners who are in training, so the learner is a known entity of the task.
   - **Background:**
     - The source does not use it: `experiment.py` of duolingo/halflife-regression reads `user_id` but builds features only from the history counts (`right`, `wrong`), the lag (`t`, logistic regression only), a bias and one indicator per word; `user_id` goes only into the prediction files written for evaluation. Its models are per word and history, not per learner.
     - The domain practitioner of 2026-11-21: "learner identity or a learner's past accuracy: I always have it"; the task gamer found no gain from rebuilding each learner's previous outcomes from the released rows.
   - **Experiments:** untuned LightGBM without the exercise count (issue 10 B), 1M rows of each training side, one run; ROC AUC:

     | Test day | Test rows of learners in training | 75% label: no learner / `user_id` | round(p): no learner / `user_id` |
     |---|---|---|---|
     | 12 March | 72.3% | 0.618 / 0.622 | 0.618 / 0.628 |
     | 11 March | 74.2% | 0.619 / 0.625 | 0.620 / 0.630 |
     | 10 March | 71.5% | 0.617 / 0.623 | 0.618 / 0.629 |

     A learner's past accuracy over all words, computed on the training side, was also tried but was built with the training rows' own outcomes, so its score (0.579-0.586) is not usable; a correct version uses only each learner's earlier sessions.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep it dropped (implemented) | No learner input | the source's feature set; no high-cardinality id | the model cannot use who the learner is, which the app knows; the original reason is gone |
     | B | Add `user_id` as a categorical input | The anonymised learner id as a category; learners recur across the windows | an input the actor holds; +0.005 to +0.010 ROC AUC; tests how methods handle a 115k-level id | beyond the source's features; a learner new to the test day gets no benefit (26-29% of test rows) |
     | C | Add a learner history feature | The learner's accuracy over all words in earlier sessions, from earlier rows only and from the training side for test rows (the evaluation protocol) | the learner's ability as a number, also for learners with few rows | a built feature to get right and verify; not measured correctly yet |

   - **Recommendation:** B: the learner is an input the deployed app always has, the reason it was dropped no longer applies, and it adds measurable signal; C only after a correct measurement. **Decision:** keep A, or change to B or C?

   **Notes for the AI:** On B, keep `user_id` in `_clean` (drop it from the drop list) and add it to the categorical features; update `known`, the identity bullet of `curation_comments` and the splits comment; rerun the check, the task and leak probes. On C, build the feature from strictly earlier sessions of the learner (cumulative correct over seen, all words), from training rows only for test rows; measure it before shipping.

   [^x24d1]: Record CC of 2026-11-02 (Myunghwan): "This supersedes the earlier joint learner/date partition. ... All learners are eligible for earlier training and later test windows; learner identity stays excluded from predictors."

   **Andrej (2026-11-24, change):** Option B: Add user_id as a categorical input.

   **Resolved (2026-11-24, Andrej):** B, applied: `user_id` stays in the frame as a categorical input (115,222 learners); `known`, the identity bullet and the closing note say so. Checked with issue 11 B in the same run: 0 errors, 0 warnings.

**Review panel:** ship after changes (mediator, 2026-11-21, full re-check). Applied without a decision: the timestamp marks the lesson's end and the label exists then, in `known`, `fit_reason`, the prediction-contract bullet and the splits comment; both lexeme counts (19,279 ids, 18,781 strings) in the notes and the decision table; the pooled against within-lesson AUROC note on the metric; the copy counts of the 2026-11-05 report (81 / 91 / 79 without timestamp) are stale, 164 / 199 / 191 test rows today, no exploit either way; no definition text states them. Left: `stratify_on` in the README, and the column audit's row and counter wording. Advocate and critic agreed, for the curator to decide: no gap (H), windows every other day (issue 8), `delta` kept with a note (issue 9). Disputed: `session_seen`, kept with a note as a span the outcome can cut (advocate, mediator) or dropped as a rate's denominator (critic; issue 10); the 75% cutoff, where both first conceded the source's own label and the mediator, after measuring it, leans keep (issue 11). For the curator: H and issues 8-12; issues 6-7 stay resolved. Claim audit: no validity claim refuted; three stale (timestamp, copy counts, lexeme count), two untested. Blind review, without our notes: include with changes; main concern `session_seen` (issue 10). Task gamer: one exploit, the known later-row counters (issue 7). The domain practitioner's learner prior (an expanding past-accuracy rate per learner) is an added feature, not a fix, and changes no decision. Earlier panels (2026-11-02, 2026-11-05): ship; their sections below are dated.

<details><summary>Mediator (2026-11-21)</summary>

**Mediator: duolingo_spaced_repetition_recall (2026-11-21)**

Inputs read: claim audit, domain practitioner, precedent checker, advocate and critic openings and
rebuttals, blind review, task gamer, column audit (`pr59_columns/findings/duolingo.md` + scripts), fugaku's column
audit and precedent-checker report, check.log (28 checks, 0 errors), the record's `## Review` (Horizon, issues 6-10),
`dataset.py`, README, principles.md, LEAK-6/9/10/41, SPLIT-10/15, TP-7, definitions.md "Larger than the row budget".
New: one run and the publisher's evaluation code read from GitHub.

**Judgment record**

```text
Verdict: ship after changes.
Validity: SEL holds; USE-1 holds (fit approximate, USE-8; prediction point conditional on N by curator choice);
  LEAK-9 triggered, fixed (own-row protocol, issue 7); LEAK-10 span clause triggered on session_seen and delta:
  both conditions now measured for each (minority drawn by the outcome; worth kept on the rows it did not draw),
  so keep-with-note is open, the curator's case-by-case call; LEAK-41 does not reach session_seen by its own text
  (no weight, no rate target), but LEAK-10's pointer reads wider: a rule-wording question;
  SPLIT-10: no gap needed (label exists at the stamp, newest day complete); SPLIT-14 holds; SPLIT-15 newest holds.
Value: TP-3, TP-4 hold (LightGBM - linear +0.153); TP-7 fails as shipped (curator cutoff, no convention, a Must):
  the source's own binarisation exists (round(p)) but measures more rule-like in N.
Quality: stale wording (clock "unverified", copy counts, stratify_on), delta note numbers, metric unit note.
Weighed: source +, size +, use-case fit approximate -, label's dependence on N -.
For the curator: TP-7 remedy (validity-adjacent Must); session_seen keep-with-note vs drop; LEAK-10/41 wording;
  gap; windows; _1m with fugaku.
```

**Decisive experiment: N's gain on full-length lessons**

LightGBM as in the column audit (400 trees, 1M random training rows before the one-day gap, 111,111 random test rows
per shipped day). Lesson = learner + timestamp; lesson size = sum of `session_seen`, a diagnostic only, never a
feature. "Gain of N" = AUROC with the 8 shipped features minus without `session_seen`. Mean of 3 windows (min-max of
the gain in brackets). Script and log: the run folder
(`full_lessons.py`, `1401968.log`).

| Test rows | Rows/window | Label 75% (shipped): with N / without / gain | Label round(p): with N / without / gain |
|---|---|---|---|
| all | 111,111 | 0.666 / 0.626 / **+0.040** (0.038-0.041) | 0.700 / 0.630 / **+0.071** (0.068-0.074) |
| lessons under 15 exercises (outcome can cut N) | 9,140 | 0.622 / 0.615 / +0.007 (0.005-0.009) | 0.649 / 0.607 / +0.042 |
| lessons of 15+ (outcome did not cut N) | 101,971 | 0.668 / 0.621 / **+0.047** (0.044-0.049) | 0.700 / 0.625 / +0.076 |
| 15+ and N >= 2 | 44,405 | 0.683 / 0.615 / +0.068 | 0.777 / 0.628 / +0.149 |
| lessons of 18-22 (standard 20) | 15,989 | 0.690 / 0.627 / +0.063 | 0.763 / 0.641 / +0.122 |

Label rate by N on lessons of 15+ (full release):

| N | rows | P(Yes), 75% | P(Yes), round(p) |
|---|---|---|---|
| 1 | 6.77M | 0.898 | 0.898 |
| 2 | 2.53M | 0.834 | 0.834 |
| 3 | 1.32M | 0.777 | 0.979 |
| 4 | 0.63M | 0.959 | 0.959 |
| 5 | 0.31M | 0.934 | 0.994 |
| 6 | 0.14M | 0.907 | 0.989 |

Reading:
- N keeps its worth on the rows the outcome did not draw: +0.047 on full lessons, more than on all rows; on the short
  lessons, where failure cuts N, it adds only +0.007. The truncation is not where N's score comes from.
- That worth is the label's construction: P(Yes | N) jumps with how many misses the cutoff allows at each N, while mean
  recall is flat from N = 2 (0.910-0.918, blind review). It is a TP-7 / USE-8 matter, not a leak.
- round(p) nearly doubles N's share (+0.071; +0.149 on N >= 2): under it P(Yes) swings by the parity of N (0.834 at
  N = 2, 0.979 at N = 3).

Publisher's convention, read 2026-11-21 (github.com/duolingo/halflife-regression): `evaluation.r` computes
`roc(round(p) ~ pp)` on the `.preds` file, one row per session (`experiment.py` writes `inst.p` = pclip(p_recall),
`%.4f`; the per-exercise `dump_detailed_predictions` is commented out). R's `round(0.5)` is 0, so the label is
p > 0.5, i.e. `2K > N`. The critic's condition (verify before re-targeting) is met; the result is above.

**Changes to make now (no decision needed)**

1. Replace "start/completion semantics remain unverified" and "label-delay bounds remain accepted approximations" in
   `task_summary.known`, `fit_reason`, the Prediction contract bullet and `splits_comment` with the measured fact:
   the stamp marks the lesson's end and the label exists then (column audit; claim 24). EV-2.
2. Copy counts without timestamp: 164 / 199 / 191 (claim 18). README `stratify_on`: either pass it to
   `sample_temporal_splits` or drop it from the metadata (claim 22; the balance holds in effect: 0.8670 vs 0.8677).
   Lexeme count: name `lexeme_id` 19,279 vs `lexeme_string` 18,781. EV-7.
3. Metric unit note (both sides agree; MET-2 note, not a change of metric): pooled AUROC ranks rows across learners;
   the scheduler ranks one learner's words; shipped model within-lesson 0.644-0.652, without N 0.581-0.590, N alone
   0.611-0.615.
4. `timestamp` is a datetime feature stamped at the lesson's end, like `delta` (issue 9): mention it in issue 9's
   note (a lesson's length, minutes, inside a day-level time).
5. The record's `Outcome` / `Main points` say "No new curator decision remains" and list the one-day gap and caps as
   unchanged: stale once issues 8-10 and the items below are open (editor).

**Open issues in the record**

| # | Verdict | What, why |
|---|---|---|
| H | **revise** | Add option "No gap" and recommend it. The stamp is the lesson's end, the label exists at it, the newest day is complete (42-45k rows/hour, recall share unchanged): SPLIT-10's "no gap is needed where ... the newest period is as complete as a later read of it". It is an application of SPLIT-10 (cases melbourne_housing_market, lt_vehicle_loan_default_prediction), not an exception. Do not cite fugaku as the basis: its no-gap is a recorded *exception* to SPLIT-10, made where a selection by the outcome was measured (fugaku precedent report, finding 1). The one hour of option B rests on an assumed refit latency no source names (SPLIT-12). Keep tied stamps on one side. Window training shares change: re-measure with `dataset windows`. Decide with issue 8. |
| 6 | keep | Settled (Resolved 2026-11-03). |
| 7 | keep | Settled. The gamer's exploit #1 is the known successor leak; its gain (+0.022 to +0.035) matches the note (+0.021 to +0.035). Exploit #2 adds nothing beyond #1. No new issue. |
| 8 | **revise** | Drop "spreading buys little" (a claim about scores, which SPLIT-15 does not accept; unmeasured) and the maps_router_eta precedent (its reason, "no other choice", does not hold: 12/10/8 March fits the floor). Recommend B (every other day; 12/10/8 under no gap: Tue, Sun, Fri, about 62% training for 8 March, estimated), as delivery_eta, aeolus_rebuilt, nyc_taxi_trip_duration (Lennart, 2026-11-10). Both advocate and critic agree. Re-state the shares for the gap chosen in H. |
| 9 | **revise** (keep A) | Add to the note the worth on the rows the outcome did not draw: floored delta 0.6627 vs no delta 0.6578 (about +0.005), as the span clause asks; drop "the worth is small" as a reason (X4) and state the mechanism contrast with bank_marketing `campaign`: most of `delta` lies before the prediction point. Add `timestamp` (change 4). Both sides agree on A. |
| 10 | **revise** | Replace the experiments with the decisive experiment (table above) and the consistency line ("not a new rule" is wrong: the keep predates LEAK-41, 2026-11-06, and the span clause, 2026-11-08). Problem: the count is a span the outcome cuts on 7.9% of rows. Options A keep with a `Potential leak, kept on purpose:` note giving +0.047 on lessons of 15+ and +0.007 on lessons under 15; B drop (7 predictors, 0.626 AUROC). The LEAK-41 reach goes to its own item (new issue 2), not into this one. Recommendation A (see below). |

**New issues for the curator (each one decision)**

1. **TP-7: keep the 75% cutoff, re-target to the source's `round(p)`, or amend TP-7?** (Must; rank first)
   - Problem: the definition builds the target; 75% is curator-chosen with no convention (record "Current rule
     wording"). A Must has no exceptions, so the AI assessment of 2026-11-05 does not cover it.
   - Evidence: the publisher's AUC uses `round(p)` = `2K > N` (read above). But TP-7 also tests "how rule-like the
     label is", and on that test round(p) is worse: N's gain +0.071 against +0.040, P(Yes) 0.834 at N = 2 vs 0.979 at
     N = 3. Myunghwan chose the binary target to make it "less sensitive" to the count (CC 2026-11-02).
   - Options: A re-target to round(p) (the convention the rule asks for; doubles the N artefact; reruns of probes);
     B keep 75% and amend TP-7 (e.g. a curator cutoff on the source's fraction, tested against the source's own
     binarisation, when it is less rule-like in the count); C back to the source fraction (no built target, so TP-7 is
     not triggered; reverses CC 2026-11-03).
   - Advocate and critic both conceded A before this measurement; it changes the case. Mediator lean: B, because the
     measurement shows A worsens the very artefact the curator chose the cutoff to reduce. Decision needed:
     Myunghwan's (task owner) with Andrej's on the amendment.
2. **LEAK-10's pointer to LEAK-41: does "a rate's denominator" cover the denominator of a rate the label thresholds?**
   (rule wording; cross item)
   - Exact text: LEAK-10 (second clause) and LEAK-6 say "A column the task uses as a weight or as a rate's denominator
     is LEAK-41's, never kept with a note." LEAK-41's own scope: "A column the task uses as a weight (the metric's
     row weight, the training weight, a rate target's denominator) whose value is set or cut after the prediction
     point is never a model input". LEAK-10's span clause names "a count of attempts".
   - Settled by the text: LEAK-41 narrows LEAK-10 only within its own scope, and that scope is weights; this task has
     no weight and its target is a binary event, not a rate. So LEAK-41 does not reach `session_seen`, and the span
     clause governs (advocate). The critic's reading rests on the pointer's wider words; the two sentences disagree,
     which only an amendment fixes.
   - Options: A narrow the pointer to "a rate target's denominator" (matches LEAK-41 and its cases, all exposures);
     B widen LEAK-41 to any denominator of a rate the target is built from (then issue 10 becomes drop, whatever it
     scores). Lean A: the mechanism LEAK-41 guards (the cut carries the outcome) is measured small here (+0.007 on the
     cut rows), and its remedy (rate target with N as weight) was turned down by the curator.
3. **`_1m` and the training cap: ship as `duolingo_spaced_repetition_recall_1m` with full training sides, budget
   train 1M / test 111,111?** (house convention, decide with fugaku_hpc_job_failure)
   - Problem: since issue #70 (Lennart, 2026-11-10) train sides keep every row and over-budget sets are `_1m`; this
     definition draws 1M itself under a plain name, through an AI repair (2026-11-16). The record's first name was
     `duolingo_spaced_repetition_recall_1m` (Assessment 2026-11-02).
   - What sets the pair apart: fugaku's 384-d embedding makes a whole training side about 36 GB (its precedent report,
     finding 3), a fact for an exception. Duolingo has none: about 11M rows of 9 columns, like aeolus_rebuilt_1m
     (13.7M rows). With a 12-day history the default sampler (newest year, random N) draws the same distribution as
     today's fixed draw, and Myunghwan's "retain 1M rows" (CC 2026-11-03) becomes the budget's N. The 111,111 test cap
     stays in the container (the budget caps the test side; the check fires only above it).
   - Options: A `_1m`, full training sides, `RowBudget(train=1M, test=111,111)`; B keep the fixed draw with a written
     exception (no distinguishing fact here). Lean A for duolingo; fugaku keeps its cap with the embedding-size fact
     written as the reason (or follows A if Andrej prefers one rule for both).

**Disputes settled or handed over**

| Point | Advocate | Critic | Outcome |
|---|---|---|---|
| session_seen: LEAK-41 or LEAK-10 span clause | span clause; measure first | LEAK-41 via LEAK-10's pointer; drop | Text: span clause (LEAK-41's scope is weights); wording conflict to new issue 2. Measured: both span-clause conditions hold (7.9% of rows cut; +0.047 on full lessons). Keep-with-note is open; the curator decides (issue 10), lean A. |
| N = 1 tie (0.636 vs 0.634) | says nothing about N >= 2 | N's worth is the label | Both right: full-lesson N >= 2 gain +0.068 is real but is the cutoff's construction (new issue 1). |
| TP-7 remedy | round(p) | round(p), verify first | Verified; measured worse on TP-7's rule-likeness test; to curator (new issue 1). |
| Gap | no gap | no gap | Agreed; H revised. Basis SPLIT-10 application, not fugaku. |
| Windows | B | B | Agreed; issue 8 revised. |
| delta | A + number | A + number | Agreed; issue 9 revised. |
| _1m | curator, with fugaku | curator, with fugaku | New issue 3; duolingo has no size fact. |
| Metric unit | note | note (rate target would settle it) | Note now (change 3). |

**Agreed facts**

- Data genuine (every blind-review sample row in the public file; MD5, rows, licence CC BY-NC 4.0 reproduced).
- Stamp = lesson end (gap to next stamp +2.22 s per exercise of the later lesson); label exists at the stamp; newest
  day complete.
- Failed lessons end early: lessons under 15 exercises are 7.9% of rows, 20-30% of them with 4+ wrong answers vs 3% at
  20. Mistakes do not add repeats of a word (3/3 at N = 3 in 0.766 vs 0.683 binomial).
- Successor exploit (issue 7) +0.02 to +0.035, closed by the own-row protocol; no other exploit.
- Checks 0 errors; floor 86.5 / 78.3 / 70.8%; LightGBM - linear +0.153 (SE 0.011); without N 0.628 pooled.
- delta includes the current lesson's length on 24.4% of rows; worth: short deltas 0.0023-0.0028, other deltas about
  0.005.

**Consistency with precedent**

- Gap: follows SPLIT-10's measured no-gap cases (melbourne, lt_vehicle); fugaku is a different case (exception with
  measured selection) and is not cited as the basis.
- Windows: follows delivery_eta / aeolus_rebuilt / nyc_taxi (B); maps_router_eta set apart by its 40-day history.
- session_seen keep (if A): follows noaa_storm_events_damage Flash Flood (span clause, worth on undrawn rows measured);
  set apart from bank_marketing `campaign` (recorded after the prediction point, which here the curator placed after N
  is set) and from the LEAK-41 exposure family (no weight, no rate target). If the curator takes new issue 2 B, drop.
- delta: noaa Flash Flood, consistent.
- Issue 7: medical_facility, fremtpl2, loan_default_prediction_imperial_college, consistent.
- TP-7: audiology_diagnosis is the only case (re-target on a field convention); no precedent for a source convention
  that is more rule-like than the curator's cutoff, hence a curator call.
- `_1m`: 18 `_1m` folders follow issue #70; duolingo has no fact to depart; fugaku has one (embedding size).

</details>

<details><summary>Advocate (2026-11-21)</summary>

**Advocate opening: duolingo_spaced_repetition_recall (2026-11-21)**

**Position:** ship. The data, the use case, the split and the value hold. Two problems are real: `session_seen` (issue 10) and the curator-chosen 75% cutoff (TP-7). Both have a fix in the definition that keeps the dataset, so neither is a reason to exclude it (remedy ladder). The gap, the windows, `delta` and the naming are value or quality calls, not validity failures.

Inputs read: the record's `## Review` (Horizon, issues 6-10), the claim audit, domain practitioner, precedent check, blind review, task gamer, the column audit (`pr59_columns/findings/duolingo.md`), check.log, leak.log, task.log, dtype. No group.log in the run folder.

**1. Real data, a real actor, a real decision (P2, P3: USE-1, PROV)**

- The claim audit reproduces every number of the record on the full release: file id, MD5, size, CC BY-NC 4.0, row counts, p_recall = K/N (error 4.7e-13), dedup 81, collection period. No claim was refuted on validity.
- The blind reviewer, without our notes, found the data genuine (every sample row matches the public file) and the task real: the scheduler ranks words for practice, and the paper evaluates with AUC for that reason. Its verdict was "include with changes", not exclude.
- The domain practitioner rates the fit approximate, not none. Recurring learners tested on later days match the scheduler's case (SPLIT-13).

**2. Honest evaluation: checks pass, the one exploit is closed by protocol (P4: SPLIT-14, LEAK-9)**

| Check | Result |
|---|---|
| Bundle checks | 28 run, 0 errors, 0 warnings |
| Floor (SPLIT-14, Must) | train share 86.5 / 78.3 / 70.8% |
| Exact feature copies across sides | 0.2% of test rows, same label 0.1% |
| Newest day censored? (probe 13) | no: rows and rate of No within the band (abs(z) < 3) |
| Task gamer's exploits | one: a later test row's counters give away 3-5% of labels (+0.02 to +0.035 AUROC) |

- The exploit is an evaluation leak through other test rows. LEAK-9 (Should, amended 2026-11-05) fixes it with a checked own-row protocol, which the definition already states (issue 7, resolved). Precedents: medical_facility_operational_data (issue 7 A), spanish_motor_insurance (LEAK-9 row, Andrej 2026-11-09).
- The gamer found the other strong effects (session context, `timestamp`) honest.

**3. Worth benchmarking (P6: TP-3, TP-4)**

| Family (task probe, 3 windows) | ROC AUC | Skill over dummy |
|---|---|---|
| LightGBM | 0.641 | +0.282 (beats dummy on 3/3) |
| Random forest | 0.600 | +0.201 |
| Single feature (`session_seen`) | 0.596 | +0.192 |
| Linear | 0.565 | +0.129 |

- The spread LightGBM minus linear is +0.153 (paired SE 0.011): the task separates methods. This answers the blind reviewer's "every method within 0.01", which came from a 200k sample without `session_seen`.
- Not trivial (TP-4): a depth-3 tree reaches 0.599 against 0.641; no feature alone exceeds 0.596.
- The low ceiling is the source's own: the paper says its AUC values "may seem low" because recall is noisy. Noise is a property of the task, not a flaw.

**4. `session_seen` (issue 10): LEAK-10's span clause governs, and its mildest outcome keeps the dataset**

- What LEAK-41 (Must) covers: "a column the task uses as a weight (the metric's row weight, the training weight, a rate target's denominator)". This task ships no weight and no rate target: equal records and a binary label (CC 2026-11-02/03, Myunghwan). Its cases (fremtpl2, bemtpl97, frempl, pricing_game) are all exposures of a rate task. Reading it onto a thresholded label stretches the text. That would be an amendment (option c), not an application.
- What applies is LEAK-10's span clause (a count the outcome can cut short). Its first condition holds: the outcome cuts the count only in failed lessons, about 8% of rows (column audit). For the other rows the lesson generator sets N. The task gamer tested whether mistakes add repeats of a word: they do not (at N=3, 3/3 in 0.766 of rows against 0.683 binomial; 1/3 in 0.024 against 0.038). Mean recall rises with N, the opposite of an error-driven count.
- Its second condition (worth on the rows the outcome did not draw) is not measured yet. This is the open gap, and it is measurable: lesson size from the raw file as a diagnostic, N's gain on lessons of 15+ exercises.
- Mildest remedy, in order: (1) measure; if the gain holds on full lessons, keep with a `Potential leak, kept on purpose:` note giving that number (noaa Flash Flood precedent). (2) If it does not, or the curator reads LEAK-41 as covering the label's denominator, drop N (issue 10 B). That is a definition fix: without N the model still reaches 0.628 pooled AUROC (domain practitioner) against 0.5, so the dataset ships either way.
- The practitioner's point that much of N's worth is the label's dependence on N is true. It is also the estimand the curator chose on purpose ("P(K/N >= 0.75 | X, N)", CC 2026-11-03). It bears on USE-8's fit (approximate), which the record already says.

**5. The 75% cutoff (TP-7, Must): a real departure, fixed by the source's own convention or an amendment**

- I concede: TP-7 asks for an established convention, a Must has no exceptions, and the record says the 75% is curator-selected (record "Current rule wording").
- The source does binarize its target. The publisher's evaluation code computes AUC on `round(p)` (record, claim table: "Publisher AUC code uses `round(p)`"). That is a convention of the source for this exact quantity.
- The two labels agree on N = 1 and 2 (59% of rows have N = 1) and differ only where accuracy lies from 50% to below 75% at N >= 3.
- Mildest remedy: re-target to the source's `round(p)` label, or amend TP-7 for a cutoff on a source fraction tested against the source's own (the AI assessment of 2026-11-05 already tested 75% against all-correct). Either keeps the dataset. This is the curator's choice; it was settled twice by Myunghwan.

**6. Gap and windows (Horizon, issue 8): conservative as shipped, no Must at stake**

- The one-day gap is longer than needed. It loses the newest day of history, but with the 1M training cap it costs no training rows (Horizon block). It breaks no Must. SPLIT-10 is a Should, and the measurement (stamp = lesson end, newest day complete) allows a shorter gap.
- I support the precedent checker's no-gap option (fugaku_hpc_job_failure, same curator, 2026-11-03), or B. Both are definition changes and a rebuild, not exclusion.
- Windows: SPLIT-15 is a Must only for the newest window, which is tested. For the others both A (with its written reason) and B (12/10/8 March, about 54% or 62% train) pass the floor. I take B if the curator wants consistency with delivery_eta; the dataset ships either way.

**7. `delta`, naming and wording: quality fixes (P7; LEAK-10 note)**

- `delta` (issue 9): keep with a note, as noaa_storm_events_damage's Flash Flood (Lennart, 2026-11-08). Most of the span lies before the prediction point; the note adds its worth on the rows the outcome did not draw: floored delta 0.6627 against no delta 0.6578.
- `_1m` naming: a house convention (issue #70), not validity. The fixed 1M draw has a curator reason (90/10, CC 2026-11-02). Rename it if the curator wants it aligned with fugaku_hpc_job_failure; no Must is at stake.
- Stale wording to fix: "start/completion unverified" (refuted: the stamp is the lesson's end), the copy counts without timestamp (now 164 / 199 / 191), the "lexemes" count (lexeme_id 19,279 vs lexeme_string 18,781).

**Judgment record**

```text
Verdict: ship after changes.
Validity: SEL holds; USE-1 holds (fit approximate, USE-8); LEAK-9 triggered, fixed (own-row protocol);
  LEAK-10 span clause triggered on session_seen and delta: delta kept with a note; session_seen kept with a note
  if its worth holds on full lessons, else dropped; SPLIT-14 holds; SPLIT-15 newest window holds.
Value: TP-3 holds (spread +0.153); TP-4 holds; TP-7 departure: re-target to round(p) or amend.
Quality: wording fixes; _1m naming optional.
For the curator: issue 10 (session_seen, measure first), TP-7 remedy, gap (no gap or B), windows (A or B).
```

</details>

<details><summary>Advocate rebuttal (2026-11-21)</summary>

**Advocate rebuttal: duolingo_spaced_repetition_recall (2026-11-21)**

**Where we stand:** the critic and I agree the task is real, no exclusion is due, and points 4-7 are fixes. We
disagree only on how far LEAK-41 reaches and which remedy for `session_seen` is the mildest. On TP-7 I concede.

| # | Critic's point | Answer |
|---|---|---|
| 1 | `session_seen` breaks LEAK-41 / USE-3 | partly concede: drop N unless its worth on full lessons is measured and holds; dispute the rate-target remedy as the default |
| 2 | 75% cutoff breaks TP-7 | concede; add a milder fix (the source's `round(p)`) |
| 3 | pooled AUROC vs within-session decision | concede a note; dispute a Must failure |
| 4 | one-day gap rests on a refuted reason | concede: no gap |
| 5 | three adjacent days need a reason | concede: B |
| 6 | fixed 1M draw under a plain name | concede it needs a curator line; not validity |
| 7 | stale or incomplete notes | concede all |

**1. `session_seen`**

- **Conceded:**
  - The span clause's second condition (worth on the rows the outcome did not draw) was never measured. Without it,
    LEAK-10 gives no note.
  - The curator's prediction point was first "session start, current-session counts are not predictors" (CC
    2026-11-02). The keep predates LEAK-41 and the cut evidence.
  - So as shipped, N cannot stay unexamined.
- **Disputed: the prediction point.** The later CC of the same day ("put num_seen as the predictor") and the CC of
  2026-11-03 ("conditional on supplied numerical session_seen N") move it on purpose. It now sits after the lesson plan
  is set. For about 92% of rows the generator sets N before any answer. The task gamer's binomial test shows mistakes do
  not add repeats of a word. USE-3 holds at that point. The open question is the 8% of failed lessons, which is
  LEAK-10's question.
- **Disputed: the N=1 tie as evidence.** On N=1 rows N is constant, so no model can gain from it there. The tie (0.636
  vs 0.634) says nothing about N's worth on full lessons with N ≥ 2. That is the number the span clause needs.
- **Disputed: LEAK-41's reach.** Its text names "a weight (the metric's row weight, the training weight, a rate
  target's denominator)". This task ships no weight and no rate target. Its four cases are all exposures of rate
  tasks. Applying it to the cutoff of a binary label is an amendment (precedent check, option c), which the curator
  may make, but it is not the present rule.
- **Disputed: the remedy order.** Shipping `p_recall` with N as weight re-targets the task. It also restores the
  regression and the weights that Myunghwan turned down (CC 2026-11-02 "no special weighting"; CC 2026-11-03 chose the
  binary label). Dropping N (issue 10 B) is the milder fix on the ladder: drop, not re-target. It still ships: 0.628
  pooled AUROC without N against 0.5.
- **My position:** measure N's gain on lessons of 15+ exercises (lesson size from the raw file, as a diagnostic only).
  If it holds, keep with a `Potential leak, kept on purpose:` note, or the curator amends LEAK-41 explicitly. Otherwise
  drop N. The rate target is the curator's option, not the default.

**2. TP-7**

- **Conceded:** a Must, no convention, and an AI assessment is no curator exception. A Must has no exceptions at all
  (principles, "Exceptions and amendments"), so the critic's "record a TP-7 exception" is not available either. Only a
  re-target or an amendment works.
- **Added remedy:** the source's evaluation code binarizes with `round(p)` (record claim table). That is a convention of
  the source for this quantity. It agrees with 75% at N = 1 and 2 and differs only at N ≥ 3 with accuracy from 50% up
  to 75%. It keeps the binary task Myunghwan chose, so it is milder than the rate target.
- **Disputed:** "with N it becomes free score". If N is a valid input (point 1), the event's dependence on N is a
  property of the event, not a leak. It inflates the score, but the score's size never decides (X4). The
  label-construction worry is TP-7's, and the re-target answers it.

**3. Metric**

- **Conceded:** the note should name the unit mismatch, with the practitioner's within-lesson numbers.
- **Disputed: a Must failure.** The source's own AUC is pooled over all rows: the paper reports it that way, and the
  publisher's code computes it so. A within-lesson score needs a lesson key the data does not ship (no `user_id`). A
  note is the right remedy. A change of metric follows only if the curator takes the rate target.

**4. Gap**

- **Conceded:** I already supported no gap (fugaku_hpc_job_failure). Keep tied stamps on one side.
- **Small correction:** the gamer's +0.002 / +0.010 / +0.001 trains on all earlier rows, so it measures more than the
  gap alone.

**5. Windows**

- **Conceded:** "spreading buys little" is a claim about scores, and SPLIT-15 does not take it. B (12/10/8 March, or
  12/9/7 under no gap) is the consistent choice. Decide it with the gap.

**6. Training cap and name**

- **Conceded:** no curator line approves the plain name. The 90/10 CC predates issue #70. Decide with
  fugaku_hpc_job_failure. This is a convention question; it changes no validity verdict.

**7. Notes**

- **Conceded, all:**
  - The "unverified" timestamp wording.
  - The `delta` worth on rows the outcome did not draw (0.6627 vs 0.6578).
  - The stale copy counts (164 / 199 / 191).
  - `stratify_on`: pass it to the sampler, or drop it from the README.

**Net verdict**

```text
Verdict: ship after changes (both sides: no exclusion).
Validity: session_seen: measure worth on full lessons, then keep with a note or drop (curator; LEAK-41 reach is an
  amendment question); TP-7: re-target to round(p) or amend (curator).
Split: no gap; windows B.
Quality: notes fixed; _1m decided with fugaku.
```

</details>

<details><summary>Critic (2026-11-21)</summary>

**Critic opening brief: duolingo_spaced_repetition_recall (2026-11-21)**

**Position:** do not ship as defined. The task is real (Duolingo's practice scheduler, Settles & Meeder 2016), so no
exclusion. But its strongest input breaks a Must, the target it then predicts is a curator cutoff without the
exception a Must needs, and the split and documentation carry reasons that no longer hold. Changes below, mildest first
within each point.

Evidence read: claim audit, domain practitioner, precedent check, blind review (clean_room), task gamer
(participant_kit), column audit (`pr59_columns/findings/duolingo.md`), record `## Review` (Horizon, issues 6-10),
check.log (0 errors), leak.log, task.log, dtype.log. All probe logs are present now; three phase A agents ran before
they arrived.

**1. `session_seen` is the label's denominator, cut by the outcome, and after the prediction point (validity; LEAK-41 Must, USE-3 Must)**

- **Problem:** the label is `4*K >= 3*N`; N (`session_seen`) is the denominator of that rate. The column audit found
  failed lessons end early: lessons under 15 exercises (7.9% of rows) have at least four wrong answers in 20-30% of
  cases, against 3% at the standard 20 (issue 10). The source README defines N as "times the user saw the word during
  this lesson", and the paper says a lesson "continues until the student masters" its words. The curator's own
  prediction point (CC 2026-11-02: "at session start using prior information ... Current-session counts are not
  predictors") puts N after it.
- **Effect on the task:** the model scores the label's construction, not recall. Practitioner's run:

  | Variant | Pooled AUROC (mean of 3 days) | Within-lesson AUROC | AUROC on N=1 rows |
  |---|---|---|---|
  | shipped 8 features | 0.670 | 0.644-0.652 | 0.636 |
  | without `session_seen` (session start) | 0.628 | 0.581-0.590 | 0.634 |
  | `session_seen` only | 0.598 | 0.611-0.615 | 0.500 |

  Within a lesson N alone ranks the label better than every input known at session start; on N=1 rows, where N
  cannot help, the two models tie. The leak probe and task probe agree: `session_seen` is the best single feature on
  all 3 splits (0.595-0.596), and the blind reviewer, with none of our notes, made this its first concern.
- **Rule:** LEAK-41 (Must): a rate target's denominator "whose value is set or cut after the prediction point is never
  a model input, whatever it scores". The LEAK-10 span clause would allow a note only if the span keeps its worth on the
  rows the outcome did not draw; that was never measured, and "the size of the worth alone never decides".
  Precedent: bank_marketing `campaign`, dropped once the prediction point was set before the campaign (Lennart,
  2026-11-08). The keep (Myunghwan, 2026-11-02/03) predates LEAK-41 (2026-11-06) and the cut evidence (2026-11-21).
- **Remedy:** the remedy the LEAK-41 case table gives for a denominator whose cut cannot be located row by row: ship the source's rate
  `p_recall` with `session_seen` as its weight scoring column and sample weight, never a feature (fremtpl2, bemtpl97,
  frempl). Milder alternative that keeps the binary label: drop `session_seen` (issue 10 B). Either reverses a curator
  choice, so it goes to Myunghwan; keeping N needs a written exception naming the higher-ranked Must, and none exists.

**2. The 75% target is a curator cutoff with no convention and no recorded exception (validity; TP-7 Must)**

- **Problem:** TP-7 asks a target the definition builds to use an established convention. The 2026-11-05 assessment
  already says the cutoff is "not ... a blanket satisfaction of TP-7". It means "all correct" at N=1-3 and "one miss
  allowed" at N>=4.
- **Effect on the task:** P(Yes) is 0.885 / 0.830 / 0.775 / 0.962 for N = 1-4 while mean raw recall is flat from N=2
  (0.910 / 0.918 / 0.917; blind review on the full 12.9M). No scheduler acts on this event (practitioner); the source
  predicts the proportion. Without N (point 1) this artefact becomes label noise; with N it becomes free score.
- **Rule:** TP-7 (Must); USE-8 (fit approximate). Only TP-7 precedent: audiology_diagnosis, rebuilt on a field
  convention.
- **Remedy:** point 1's rate target removes the cutoff. If the binary label stays, record a TP-7 exception with its
  fact (quantised fractions at N=1-3, CC 2026-11-02/03) as a curator line, not an AI assessment.

**3. The metric ranks across learners; the decision ranks words within one learner's session (value; MET-2 Must, MET-8 Weigh)**

- **Problem:** pooled AUROC compares rows of different learners and days. The scheduler ranks one learner's words at one
  moment (practitioner, NEW).
- **Effect:** the shipped model's within-lesson AUROC (0.644-0.652) is 0.02 below its pooled score, and N carries most
  of the within-lesson ranking (point 1).
- **Remedy:** mildest is a note naming the unit mismatch. If point 1's rate target is taken, binomial log loss on
  `p_recall` with N as weight is the source's quantity under a proper rule (MET-8) and settles this too.

**4. The one-day gap rests on a reason the column audit refuted (split; SPLIT-10 Should, tree leaf)**

- **Problem:** the gap was set because start or end of the stamp was "unverified". Measured 2026-11-21: the stamp is
  the lesson's end, the label exists at it, and the newest day is complete. The Horizon block then recommends one hour
  on an assumed refit latency that no source names; the tree leaf "Temporal · arrival date" asks for no gap.
- **Evidence:** precedent check finding 1 (fugaku_hpc_job_failure, same curator, 2026-11-03: no gap once completion is
  exact; melbourne_housing_market, lt_vehicle_loan_default_prediction). Task gamer: closing the gap raises the honest
  score by +0.002 / +0.010 / +0.001.
- **Remedy:** add "no gap" to the Horizon options and recommend it, keeping tied stamps on one side.

**5. The three adjacent newest days need a reason that holds (split; SPLIT-15 Should)**

- **Problem:** issue 8 cites maps_router_eta, which kept the newest weeks because nothing else fitted. Here 12/10/8
  March fits the floor (about 54% with the one-day gap, about 62% with none). Lennart spread windows wherever feasible
  on 2026-11-10 (delivery_eta, aeolus_rebuilt, nyc_taxi_trip_duration). "Spreading buys little" is a claim about scores,
  which SPLIT-15 does not accept as a reason, and it was not measured.
- **Remedy:** option B (every other day), decided with point 4; or A with a reason of its own written in the splits
  comment.

**6. The training cap is fixed inside the container under a plain name (convention; definitions.md row budget)**

- **Problem:** since issue #70 (Lennart, 2026-11-10/12) the train side keeps all earlier rows and an over-budget set is
  `<name>_1m`. This definition draws 1M training rows itself and dropped `_1m` through an AI compatibility repair
  (2026-11-16), not a curator line. The 90/10 approval (CC 2026-11-02) predates #70.
- **Remedy:** `_1m` with the collection's budget, test cap 111,111 kept as the curator's choice if the API allows;
  decide together with fugaku_hpc_job_failure.

**7. Notes that are refuted or incomplete (quality; EV, LEAK-10 span clause)**

- `task_summary.known`, `fit_reason` and the "Prediction contract" note still say start/completion is unverified;
  refuted (claim audit 24, column audit). Use the column audit's wording.
- Issue 9's `delta` note gives only the worth of short deltas (0.0023-0.0028); the span clause needs the worth on rows
  the outcome did not draw: floored delta 0.6627 against none 0.6578 (precedent check finding 4). Issue 9 A itself I do
  not contest.
- Copy counts without timestamp (81 / 91 / 79) are stale: 164 / 199 / 191 today (claim audit 18).
- README `stratify_on` is not passed to the sampler; the class balance holds in effect only (claim audit 22).
- Remedy: fix the wording; no rebuild needed for the text alone.

**Not argued**

- The successor-row exploit (issue 7): settled under LEAK-9 with the own-row protocol; I have no new evidence.
- Weak signal: LightGBM beats the dummy on 3 of 3 splits by +0.141 skill (task.log); a real small signal is a keep
  (TP-2).
- Licence CC BY-NC 4.0 is verified and is the house norm question, not this dataset's.
- The blind reviewer's "unexplained 11% subset" is the documented 1M / 111,111 cap.

</details>

<details><summary>Critic rebuttal (2026-11-21)</summary>

**Critic rebuttal: duolingo_spaced_repetition_recall (2026-11-21)**

**Where we stand:** we agree on more than we disagree. Neither of us asks for exclusion, and both of us ship after
changes. One real dispute is left: whether `session_seen` may stay with a note (point 4). On TP-7 I accept the
advocate's `round(p)` remedy, on one condition.

| Advocate point | Reply |
|---|---|
| 1. Real data, actor, decision | Concede |
| 2. Honest evaluation, exploit closed by protocol | Concede |
| 3. Worth benchmarking | Concede, with one caveat |
| 4. `session_seen` under LEAK-10, not LEAK-41 | Dispute |
| 5. TP-7: re-target to `round(p)` or amend | Concede the remedy, with one condition |
| 6. Gap and windows | Concede |
| 7. `delta`, naming, wording | Concede `delta` and wording; partly dispute naming |

**1. Real data, a real actor, a real decision: concede**

The claim audit refutes no claim on validity, and the blind reviewer matched every sample row to the public file. I
never argued exclusion.

**2. Honest evaluation: concede**

The successor exploit is settled by the own-row protocol (LEAK-9, issue 7). The checks show 0 errors, and probe 13
shows no censoring at the release end.

**3. Worth benchmarking: concede, with one caveat**

- The LightGBM-minus-linear spread of +0.153 (paired SE 0.011) answers the blind reviewer's "within 0.01". TP-3 and
  TP-4 hold.
- Caveat: the single-feature baseline is `session_seen` on all 3 splits (0.596). Part of the spread is therefore the
  label's dependence on N.
- Without N there is still a real signal: 0.628 pooled AUROC against 0.5 (practitioner). The value holds
  under my remedy too.

**4. `session_seen` falls under LEAK-10's span clause, not LEAK-41: dispute**

**Scope.**
- LEAK-41 names "a rate target's denominator". The label here is `4K >= 3N`, a cutoff on the rate K/N, so N is still
  that rate's denominator. Thresholding the rate does not remove N from the target's definition.
- LEAK-10 sends this case to LEAK-41 itself: "A column the task uses as a weight or as a rate's denominator is
  LEAK-41's, never kept with a note." The wording is "a rate's denominator", not only a rate target's.
- So keep-with-a-note under the span clause is not open for this column. Reading LEAK-41 narrowly would need the
  amendment (option c), not the other way round.

**Mechanism.**
- I concede the gamer's finding: mistakes do not add repeats of a word (at N=3, 3/3 in 0.766 of rows against 0.683
  binomial).
- That test does not touch the cut the column audit found: whole lessons end early when they fail. In lessons under 15
  exercises, 20-30% have at least four wrong answers, against 3% at the standard 20. A truncated lesson gives each word
  fewer exposures.
- The gamer's evidence and the cut are two different mechanisms. Only the cut makes N partly an outcome.

**Worth.**
- The advocate's plan to measure N's gain on full lessons only is good evidence, and I support running it.
- It cannot decide the question, because LEAK-41 applies "whatever it scores", and the span clause adds "the size of
  the worth alone never decides".
- The evidence we have already says what that worth mostly is. On N=1 rows, where N cannot help, the model with N
  scores 0.636 and the session-start model 0.634. Within a lesson, N alone (0.61) beats every input known at session
  start (0.58-0.59).

**Estimand.**
- The 11-03 CC chose P(K/N >= 0.75 | X, N) on purpose. It predates LEAK-41 (11-06) and the cut evidence (11-21).
- A curator choice made before a Must existed is a reason to ask Myunghwan again, not a fact that satisfies the Must.

**Common ground.** The advocate's fallback, drop N (issue 10 B), is a fix in the definition, and the dataset ships
either way. We differ only on which remedy comes first: I put dropping N (or the weight remedy) first; the advocate
puts measure-and-note first.

**5. TP-7: concede the `round(p)` remedy, with one condition**

- I concede that `round(p)` is a better remedy than a recorded exception. The paper's AUC is defined on correctly
  versus incorrectly recalled words (§4.1, read in `clean_room/work/web/paper.txt`). The record's earlier claim table
  (line 430) says the publisher's evaluation.r uses `round(p)`.
- Condition: this round's claim audit did not re-read evaluation.r; its released experiment.py has no AUC. Verify
  evaluation.r before re-targeting. Also note that R's `round(0.5)` is 0, so the label means p > 0.5, and 1/2 is a
  No.
- The new label still depends on N: 1/1, 2/2 and at least 2/3 are a Yes. So it does not reopen point 4; it only
  narrows the artefact.
- Amending TP-7 for one dataset (the advocate's other option) I still oppose, while a source convention exists.

**6. Gap and windows: concede**

- SPLIT-10 and SPLIT-15 (beyond the newest window) are Shoulds, and I never claimed a Must there.
- We agree on no gap (the fugaku precedent), and on B for the windows, or A with a reason that holds.

**7. `delta`, naming and wording: concede `delta` and wording, partly dispute naming**

- `delta`: concede A, with the note giving 0.6627 against 0.6578.
- Wording: agreed, plus the "lexemes" count the advocate adds.
- Naming, partly disputed: the 90/10 CC (2026-11-02) is the curator's reason for the 111,111 test cap. It gives no
  reason to fix a 1M training draw against issue #70's "N is recorded, not applied". The switch to the plain name was
  an AI repair. I agree it is no Must, so it is the curator's call, decided together with fugaku.

**No new points**

No new fact came up, so I add no new points.

</details>

<details><summary>Claim audit (2026-11-21)</summary>

**Claim audit: duolingo_spaced_repetition_recall (duolingo), 2026-11-21**

**Result:** no claim refuted on validity. Nearly every number the definition and its record state comes out the same on the full release. Three claims are stale or worded too strongly, and two could not be tested.

**How it was tested:** One run ran `claims.py` on the full raw file and on the definition's own `make_splits()` and `to_container()`. Script and log are in the run folder. The Dataverse API, the halflife-regression GitHub history and the 2016 README were read as well.

**Probe outputs:** the run folder holds only `precedent/`. There is no check.log, README_check.md, leak/, task/, dtype/ or group.log, so I could not read the dataset check or the probes.

**Claims table**

| # | Claim | Where | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | File 3091087, v1.0, MD5 0a1cae5e…, 379,004,009 bytes, CC BY-NC 4.0, deposited 2017-12-14 | download_description, sources, curation note | Dataverse versions API | holds | all match; released 2017-12-14T19:47Z | SRC |
| 2 | p_recall = K/N | `_clean` assert, label note | max abs error | holds | 4.7e-13 | - |
| 3 | 83.886% of sessions all correct; 58.937% have N=1 | curation note "Source and limits" | raw counts | holds | 0.838864; 0.589371 | - |
| 4 | Mean recall of the archive's first 90% is 0.896172 | same | file-order first 90% | holds | 0.8961722 | - |
| 5 | The paper's mean is 0.859 | same | paper Table 2 | **untested** | no PDF text tool on the box (no pdftotext, pypdf or poppler) | - |
| 6 | Deduplication removes 81 profiles, with user_id kept | curation note | count duplicates with and without lexeme_id and user_id | holds; "identity-aware" changes nothing | 81 in every variant | - |
| 7 | lexeme_string is a morphological tag, not prose | curation note | contents of the categories | holds | 100% carry `<…>` tags; at most 81 chars; 18,781 strings for 19,279 ids (at most 3 ids per string); 462 strings occur in more than one course | - |
| 8 | The source added lexeme_string to the release; original experiments used lexeme_id | curation note | 2016 repo README and experiment.py at 2ed77ed8 (2016-06-07) | holds as the README states it; nuance below | README: "Only the lexeme_id column was used in our original experiments"; the released experiment.py builds lexeme features from `lexeme_string` | - |
| 9 | At N=1,2,3 the label is the same as all-correct; at N=4, 3/4 counts as positive | curation note | Yes share vs all-correct share by N | holds | N=1-3 equal (0.884, 0.830, 0.776); N=4: 0.959 Yes vs 0.710 all-correct | - |
| 10 | Counters match the previous session in 98.18% of 6,992,475 later pairs; seen and correct counters decrease in 0.328% and 0.305% | curation note | sort by user, lexeme, time; compare consecutive rows | holds | 6,992,475; 0.98177; 0.00328; 0.00305 | - |
| 11 | No missing cells; no history_correct > history_seen | record review | count | holds | 0; 0; also history_seen ≥ 1 everywhere | - |
| 12 | Collection period 28 Feb – 12 Mar 2013; newest day partial, ends 16:14:57 UTC | record front matter, curation note | timestamp min/max | holds | 2013-02-28 18:28:01 to 2013-03-12 16:14:57; test day 1 covers 17 hours | - |
| 13 | Sorted by the actual timestamp, not by file order | curation note | monotonicity check | holds | raw file not sorted (1.75% of steps go backwards); shipped frame sorted | - |
| 14 | 1,429,456 rows, 8 features, 1M train / 111,111 test per window, about 90/10 | README, task_summary.split | rebuild | holds | 1,429,456 rows; 8 features; every fold 1,000,000 / 111,111 | - |
| 15 | Test windows 12, 11, 10 March with a one-day gap; training ends before test start minus the gap | splits_comment | min and max times per side | holds | train ends 23:59:57–59 two days earlier; gap 1 day plus 1–7 s | SPLIT-10 |
| 16 | Every window trains on at least half the rows | `_make_splits` assert, issue 8 | population train share | holds | 0.8648 / 0.7832 / 0.7080 (issue 8's 86.5 / 78.3 / 70.8) | SPLIT-14 |
| 17 | No full-feature copies across train and test | record review "Exact cross-side copies" | merge on all 8 features | holds | 0 in every fold | LEAK |
| 18 | Without timestamp, copies match the training set 81 / 91 / 79 times | same | merge on 7 features | **stale** | 164 / 199 / 191 test rows today | - |
| 19 | About 54% of rows follow an earlier session of the same learner-word pair | Assessment 2026-11-21 | consecutive same-pair rows | holds | 0.544 | SPLIT-32 |
| 20 | Metric: roc_auc fallback, computable on every fold | metric, README | `scorer` on a constant and a random prediction per fold; class counts | holds | 0.5 constant; 0.494–0.498 random; about 96.3k positive and 14.8k negative per fold | MET-2 |
| 21 | Source metrics: MAE for display, AUC with rounded p, half-life correlation (§4.1) | metric reason | paper §4.1 and released experiment.py | **partly untested** | experiment.py computes MAE and correlation only (`spearmanr` is in fact Pearson), with no AUC; I could not read the paper's AUC definition (see 5) | MET-1 |
| 22 | The test sample keeps the window's class balance (README `stratify_on`) | README | test vs window Yes share | holds in effect | 0.8670 vs 0.8677; 0.8665 vs 0.8662; 0.8667 vs 0.8667. `sample_temporal_splits` is called without `stratify_on`, so the README field does not drive it | - |
| 23 | The task is not trivial: N alone does not give the answer | implied (TP-4) | univariate AUC per test fold | holds | session_seen 0.526–0.530; per-N training base rate 0.595–0.597; historical accuracy 0.572–0.577; LightGBM 0.665 (issue 9) | TP-4 |
| 24 | "Start/completion semantics remain unverified" | task_summary.known, fit_reason, first curation note | column audit measurement | **refuted** (KNOWN) | the stamp is the lesson's end: the gap to the next stamp grows 2.22 s per exercise of the later lesson (record Horizon block, issue 9 footnote) | LEAK-10 |
| 25 | The successor attack recovers 3.32–5.18% of labels and adds 0.021–0.035 AUROC | LEAK-9 curation note, issue 7 | - | **untested** | not re-run; the protocol remedy is settled | LEAK-9 |

**Refuted and untested claims, ranked**

1. **The timestamp semantics are called "unverified" (claim 24; KNOWN, refuted).**
   - The column audit measured that the stamp marks the lesson's end.
   - `task_summary.known`, `fit_reason` and the "Prediction contract" note still say start or completion is unverified.
   - This also bears on the tag `Target: Varying Delay`. Measured from the stamp, the label exists at the recorded time, as the Horizon block says. The tag still holds if the prediction point is the lesson's start, which the question's "Given N exercises … will this session achieve" implies. The record should then say so, as the `bank_marketing`-style reading of a count the outcome stops.
   - Mildest remedy: the wording the column audit already gives in its doc fixes. This goes with issues 9 and 10 and adds no new issue.
2. **The source-metric description is only partly verified (claim 21; NEW, minor; MET-1).**
   - The released code has no AUC.
   - The fallback stands either way: no source metric scores a ≥75% label.
   - Mildest remedy: none needed, unless a reviewer with PDF tools finds that §4.1 does not define AUC on rounded p. Then drop "rounded-proportion AUC" from the reason.
3. **The cross-side copy counts without timestamp are stale (claim 18; NEW, cosmetic).**
   - 81 / 91 / 79 do not reproduce; today's sampled rows give 164 / 199 / 191 test rows.
   - The conclusion, no exploit, does not depend on the count.
   - Mildest remedy: refresh the numbers, or say they come from an earlier sample.
4. **The paper's 0.859 is untested (claim 5)** and **the successor-attack size is untested (claim 25).** Neither changes a decision.

**Nuances, not refutations**

- **lexeme_string vs lexeme_id (claim 8):**
  - The 2016 README says only lexeme_id was used in the original experiments. The public experiment.py builds the lexeme features from lexeme_string.
  - The data itself was first published in 2016 (S3, alongside the code); the 2017-12-14 date is the Dataverse re-deposit.
  - The curation note is literally right.
- **Dropping lexeme_id:** this merges up to 3 ids into one string (498 distinctions are lost). It does not change the deduplication count (81 either way).
- **Decision evidence row "lexemes":** it counts lexeme_id (19,279), while the model sees lexeme_string (18,781).

**Not refuted, with what was tested**

- Every number in the record's limits and counter bullets.
- The row and fold sizes, the gap, the floor and the class balance.
- The 8-feature list: timestamp, delta, learning_language, ui_language, lexeme_string, history_seen, history_correct, session_seen. Neither session_correct nor p_recall is in it.
- The metric's computability on every fold.
- The source file's identity and licence.

</details>

<details><summary>Domain practitioner (2026-11-21)</summary>

**Domain practitioner: duolingo_spaced_repetition_recall (2026-11-21)**

I am the person who runs the practice scheduler in a language-learning app. When a learner opens a practice session, I pick which words go into it. I want the words whose recall has dropped the most (Settles & Meeder 2016, half-life regression; it also drives the per-skill strength meters).

**Fit: approximate.** The inputs and the population are the real logs. But the target is a session score that depends on N. The curator chose the 75% cutoff, and nothing in the source or the product acts on it. N is only known after the session.

**Inputs at my decision point (USE-3, USE-6)**

| Input | Do I have it when I choose the words? | Status |
|---|---|---|
| history_seen, history_correct, lexeme_string, languages | yes | fine |
| delta | mostly. It runs to the lesson's end, so it includes the current lesson's length (24% of rows) | KNOWN, issue 9 |
| timestamp | I have the session start, not the end | KNOWN (column audit) |
| session_seen (N) | **no.** The lesson generator and the learner's mistakes set it during the session, and failed lessons end early | KNOWN, issue 10 (settled keep, 11-02/03) |
| learner identity or a learner's past accuracy | **I always have it.** The data drops it, and the learner's past accuracy across all words is not a feature | NEW, minor |

**Target (USE-5, USE-1)**

- What I act on is the recall probability of one word now: rank the words, then practise the lowest ones. The source predicts the proportion p (MAE) and ranks by it. HLR's prediction is p = 2^(-delta/h).
- P(K/N >= 0.75 | N) mixes two events. At N=1-3 it means "all correct", and 59% of rows have N=1. At N >= 4 one miss is allowed. No scheduler acts on this event. The cutoff is curator-selected (TP-7: no established convention). KNOWN, a settled curator choice.
- Would I use this model? Only by ignoring N. I would score each word without N, or at N=1, which amounts to predicting first-exposure recall. So the shipped model's N-dependence, worth about 0.04 AUROC, is signal I could not use at decision time.

**Row and test (USE-10)**

- One row is one learner-word inside one session. My decision is the ranking of one learner's words at one moment.
- Learners recur, and the temporal test on later days with known learners matches my case (I schedule for existing users). Fine.

**Metric (MET-1, MET-2, MET-8)**

**Partly.** Pooled AUROC ranks rows across all learners and sessions. My decision ranks words within one learner's session (the unit I act on, MET-2).

First result of my run (LightGBM, 1M train, about 111k test rows sampled as whole lessons, test day 12 March):

| Variant | Pooled AUROC | Mean within-lesson AUROC | AUROC on N=1 rows |
|---|---|---|---|
| shipped 8 features | 0.666 | 0.652 | 0.632 |

- 4,803 test lessons hold both classes, covering 72% of the rows.
- The run also tests "no session_seen" and "session_seen only" on all three days. It was still running at hand-back.
- Log: the run folder
- Script: `.../domain-practitioner/actor.py`

The metric I would choose (NEW, weighed, not a Must breach): AUROC within learner-session, or log loss on per-exposure recall. That is MET-8: a probability scored by a proper rule, which is the source's quantity.

**What an expert would change (ranked)**

1. Drop session_seen and predict at session start (issue 10 B). Better still, predict p_recall itself as the target: binomial log loss with N as the trial count and not as a feature. That is the HLR task, and it removes the N-defined label. KNOWN direction; reverses a curator decision.
2. Score ranking within the unit I act on, the learner-session, as well as pooled. NEW.
3. Add a learner prior: an expanding past-accuracy rate per learner, computed on training rows only. A practitioner always has it. NEW, minor.
4. Delta to session start (issue 9). KNOWN.

**Sources**

- Settles & Meeder 2016 (ACL, doi 10.18653/v1/P16-1174), via the record's section 4.1 notes. The PDF did not extract here; the product use is from my own knowledge of the paper.
- github.com/duolingo/halflife-regression README for the column definitions.
- The record's issues 9 and 10, and the run folder.
- Missing: check.log, README_check.md and the leak/task/dtype/group probe outputs were not present in the run folder (only `precedent/`).

**Addendum: full results of my run (arrived after hand-back)**

LightGBM with 1M training rows, scored on about 111k test rows per day, sampled as whole lessons. "Within-lesson AUROC" is the mean over the 4.8k test lessons that hold both classes (72% of rows).

| Variant | Pooled AUROC (12/11/10 Mar) | Within-lesson AUROC | AUROC on N=1 rows |
|---|---|---|---|
| shipped 8 features | 0.666 / 0.672 / 0.672 (mean 0.670) | 0.652 / 0.648 / 0.644 | 0.636 |
| no session_seen (session start) | 0.625 / 0.628 / 0.632 (mean 0.628) | 0.590 / 0.583 / 0.581 | 0.634 |
| session_seen only | 0.598 / 0.602 / 0.593 (mean 0.598) | 0.612 / 0.615 / 0.611 | 0.500 |

Reading (NEW, supports items 1 and 2 of the ranked changes):

- **Within a learner's lesson, N alone ranks the label better than every input I hold at session start (0.61 against 0.58-0.59).** Most of the ranking that the 75% label rewards inside a lesson is the label's own dependence on N: at N=1 to 3 it means all correct, at 4 or more one miss is allowed.
- **On N=1 rows the shipped model and the session-start model score the same (0.636 against 0.634).** N=1 rows are the label I would act on (first-exposure recall). There, prior knowledge carries all the signal and N adds nothing.
- So the pooled lead of the shipped model (+0.042) measures the label's construction, not the recall prediction I would use.
- Lessons on the test days hold a median of 8 words (upper quartile 22).

</details>

<details><summary>Precedent check (2026-11-21)</summary>

**Precedent check: duolingo_spaced_repetition_recall (2026-11-21)**

Inputs: `decision_register.py --json` (5,933 decisions; register at
the run folder; no register flag names this
dataset), the record (CC lines, issues 6-10, Horizon block), `dataset.py`, the column-audit summary
(the run folder), the Cases tables of splits.md, leak_checks.md and task_probes.md,
split_tree.md (Dated event log), definitions.md (row budget). The check/probe outputs (check.log, leak/, task/, dtype/,
group.log) were not in the run folder when I looked, so I did not
read them. I fitted no models.

**Summary**

| # | Decision | Verdict | Precedents | New/Known |
|---|---|---|---|---|
| 1 | Horizon: recommend a one-hour gap (B) | departs, no reason given: the precedents and the tree leaf point to no gap, and the options leave it out | fugaku_hpc_job_failure (Myunghwan 11-03), melbourne_housing_market, lt_vehicle_loan_default_prediction, SPLIT-10 amendment, tree leaf "Temporal · arrival date" | NEW |
| 2 | Issue 8: keep the three newest days (rec. A) | departs, no reason given: the reason it cites from maps_router_eta does not hold here | delivery_eta, aeolus_rebuilt, nyc_taxi_trip_duration (all B, Lennart 11-10); maps_router_eta (A, 11-11, "no other choice") | NEW (the issue's consistency line) |
| 3 | Issue 10: keep realized `session_seen` (rec. A) | departs, no reason given; may break a Must (LEAK-41) | bank_marketing `campaign` dropped (Lennart 11-08); LEAK-41 + exposure family (fremtpl2, bemtpl97, frempl, pricing_game); LEAK-10 span clause | NEW |
| 4 | Issue 9: keep `delta` with a note (rec. A) | consistent (noaa Flash Flood); the note is missing one number | noaa_storm_events_damage Flash Flood (Lennart 11-08); bank_marketing `campaign` / heart_failure `time` set apart | NEW (small) |
| 5 | Train side capped inside the container, plain name instead of `_1m` | departs from the house convention, with a pre-convention reason only (shared with fugaku) | issue #70 (Lennart 11-10), v0.2 budget (Lennart 11-12); 18 `_1m` folders, nyc_taxi_trip_duration_1m | NEW |
| 6 | Curator-chosen 75% cutoff (TP-7) | departs from a Must, with a stated reason (curator direction) and no recorded exception or amendment | audiology_diagnosis (only TP-7 case) | KNOWN (AI assessment 2026-11-05) |
| 7 | Issue 7: own-row protocol, `history_correct` kept | consistent | medical_facility_operational_data (Lennart 11-05), loan_default_prediction_imperial_college f615/f617 (Andrej 11-10), fremtpl2 (11-05) | KNOWN |
| 8 | Temporal split, no learner holdout, learners recur | consistent | SPLIT-13; tree: Dated event log → forward → a case arrives | KNOWN |
| 9 | One-day window length | consistent (the source's own test span, SPLIT-12) | medical_facility_operational_data (source horizon), SPLIT-12 family row | KNOWN |
| 10 | ROC AUC fallback, equal weights, dedup before coarsening | consistent | MET fallback; no contrary precedent found | KNOWN |

**Findings**

**1. Horizon gap: the precedents point to no gap, and the options leave it out (NEW)**

- Measured on 2026-11-21: the stamp marks the lesson's end, so the label exists at the stamp. The column audit says:
  "zero gap label-safe; option B's session-length assumption not needed".
- The tree's question is whether the delay is "longer than the time column's smallest recorded step (a timestamp: its
  resolution)". Measured from the stamp, the delay is zero, so the leaf is **Temporal · arrival date** (no gap). The
  Horizon block's B says "a gap of about the delay, as the tree's leaf asks", which does not fit what was measured.
- SPLIT-10 as amended (Lennart, 11-04/05): measurements decide, and no gap is needed where the newest period is as
  complete as a later read of it. The block measured exactly that: the newest day has normal rows per hour and an
  unchanged positive share.
- The closest precedent is the same curator on a sibling: fugaku_hpc_job_failure (Myunghwan, 2026-11-03), "no
  additional fixed embargo after exact recorded-completion filtering: precise timestamps permit use of completed
  outcomes at live refit". Also melbourne_housing_market and lt_vehicle_loan_default_prediction: no gap once measured.
- The one hour is a refit latency we assume. SPLIT-10 and SPLIT-12 accept a planning gap only where the use case has
  one, and I found no precedent for a gap justified by refit latency.
- Rows of one lesson share a stamp. With no gap the cut still has to keep tied stamps on one side; the Notes already
  ask for that check.

Reflection prompt (issue shape):

> **Gap: should the options include no gap, as on fugaku_hpc_job_failure?**
>
> - **Problem:**
>   - The stamp marks the lesson's end and the label exists then (measured 2026-11-21); the newest day is complete.
>   - Under these facts fugaku_hpc_job_failure (2026-11-03, Myunghwan) shipped with no gap, and the tree's leaf is
>     "Temporal · arrival date", no gap.
>   - The recommended one hour rests on an assumed refit latency that no source names.
> - **Options:**
>
>   | | Option | Pro | Con |
>   |---|---|---|---|
>   | a | No gap; the splits comment says the stamp marks the lesson's end, measured | follows fugaku and the tree leaf; trains on the most recent day | only safe because the end-of-lesson stamp was measured |
>   | b | One hour (current recommendation), with the assumed latency written down as the reason | a margin against clock error | no measurement asks for it; departs from fugaku |
>   | c | Keep the one-day gap (implemented) | signed off before | the reason ("start/completion unverified") no longer holds |
>
> - **Recommendation:** a.
>
> [^g]: SPLIT-10 (amended 2026-11-04/05), SPLIT-12; split_tree.md, Dated event log, "a case arrives".

**2. Issue 8: the "short history" reason does not fit this release (NEW)**

- After the SPLIT-15 amendment (2026-11-10), Lennart chose spread windows every time spreading was feasible:
  delivery_eta ("Every other week", 11-10), aeolus_rebuilt (holidays, July, March, 11-10) and nyc_taxi_trip_duration
  (Memorial Day week, a week in April, 11-10). blogfeedback (Andrej, 11-03) took more windows.
- The issue cites maps_router_eta as the precedent for keeping the newest windows. Its CC (Lennart, 11-11) gives the
  reason "the 40 days leave no other choice: a fourth whole week would train on about a quarter". Duolingo does have
  another choice: option B (12/10/8 March) keeps every window above 50% (8 March about 54% with the one-day gap).
- Under finding 1 the train shares also go up. With no gap, a test on 8 March trains on about 62% (the rows before
  8 March, the issue's own table) and 7 March on about 54% (Horizon option C). That leaves room for 12/10/8 or 12/9/7.
- Part of the rec. A reasoning, "spreading buys little within one fortnight", is a claim about scores. SPLIT-15 bases
  the choice on use case and data statistics, never a model's score, and nothing was measured for it here.
  delivery_eta's release was also short (weeks) and still went to B.

Reflection prompt:

> **Windows: spread them, as on delivery_eta, or keep the newest three with a reason of their own?**
>
> - **Problem:**
>   - delivery_eta, aeolus_rebuilt and nyc_taxi_trip_duration (Lennart, 2026-11-10) moved to spread windows wherever
>     the floor allowed; maps_router_eta kept the newest weeks only because nothing else fitted.
>   - Here 12/10/8 March fits the floor (about 54% with the one-day gap, about 62% with none).
> - **Options:**
>
>   | | Option | Pro | Con |
>   |---|---|---|---|
>   | a | Keep A, with a fact that sets it apart, e.g. a daily refit use case that only cares about the days just after a refit (SPLIT-15's "use case that only cares about the weeks after a refit") | no rebuild of windows | the use case states no refit cadence (the Horizon block calls it assumed) |
>   | b | Every other day (12/10/8, or 12/9/7 under no gap) | follows delivery_eta; adds Friday/Saturday | oldest window near the floor under the one-day gap |
>   | c | Reopen delivery_eta to match A | — | no fact supports it |
>
> - **Recommendation:** b, decided together with the gap (finding 1).
>
> [^w]: SPLIT-15 (amended 2026-11-10), SPLIT-14.

**3. Issue 10: the realized count is the label's denominator and the outcome cuts it short (NEW)**

- Issue 10's consistency line says "settled as a realized count ...; this is new evidence ..., not a new rule". The
  settlement (Myunghwan, 2026-11-02/03) came before three rules and cases that now cover this mechanism:
  - LEAK-41 (Must, 2026-11-06/08): "A column the task uses as a weight or ... a rate target's denominator whose value
    is set or cut after the prediction point is never a model input, whatever it scores". The label is
    `4*K >= 3*N`, a cutoff on the rate K/N. N is its denominator, and failed lessons cut it short (new on 11-21).
  - The LEAK-10 span clause (2026-11-08): "A span (a duration, a count of attempts) whose start or end the outcome ...
    can draw" may stay with a note only when the source's rule lets the outcome draw a minority of spans and the span
    keeps its worth on the rows the outcome did not draw. "The size of the worth alone never decides."
  - bank_marketing `campaign` (Lennart, 2026-11-08): this campaign's calls, ended by the outcome. It was kept with a
    note on 11-06, then dropped once the prediction point was set before the campaign. The add-dataset skill names it
    as the example of `Target: Varying Delay`, the tag this record carries.
- The duolingo record set the prediction point at session start (CC 2026-11-02: "at session start using prior
  information ... Current-session counts are not predictors"), then added N as a predictor ("put num_seen as the
  predictor"). The facts on the cut point the same way as bank_marketing.
- Rec. A argues that "the truncation touches a minority of rows". That covers the first half of the span clause. The
  second half (worth on rows the outcome did not draw) is not measured: the 0.041 AUROC is over all rows, and most of
  it is the label's own dependence on N.
- The exposure family under LEAK-41 has one more remedy, which issue 10 does not offer: ship the rate with N as its
  weight, never as a feature (fremtpl2, bemtpl97, frempl). That is the old regression with weights, which Myunghwan
  turned down (equal weights). So the realistic options are to drop N or to keep it as an exception.
- The 0.041 is "most of it the label's own dependence on N". LEAK-41 asks for the score of a model on the weight alone
  next to the gain. This record has it: N-only AUROC 0.596 against 0.664 for the full model.

Reflection prompt:

> **Keep the realized exercise count, though LEAK-41 bars a denominator that the outcome cuts short?**
>
> - **Problem:**
>   - `session_seen` is the denominator of the label (4K >= 3N), and failed lessons end early (lessons under 15
>     exercises, about 8% of rows, 23-33% below 75%).
>   - bank_marketing's `campaign`, a count the outcome stops, was dropped (Lennart, 2026-11-08), and LEAK-41 (a Must)
>     keeps a cut denominator out of the inputs "whatever it scores".
>   - The keep (Myunghwan, 2026-11-02/03) predates both.
> - **Options:**
>
>   | | Option | Pro | Con |
>   |---|---|---|---|
>   | a | Keep N as an exception, with its fact: the app sets N before the session for the ~92% of rows in full-length lessons, and the task is conditional on N by the curator's design (USE-8 fit approximate); measure the worth of N on full-length lessons only and put it in the note | keeps the settled task | an exception to a Must needs a higher-ranked Must; none is named |
>   | b | Drop N (issue 10 B) | follows bank_marketing and LEAK-41 | reverses a settled curator choice; the label still depends on N |
>   | c | Amend LEAK-41/LEAK-10 for a count that is the label's denominator and is mostly fixed by design | settles the rule for later cases | a rule change on one case |
>
> - **Recommendation:** ask Myunghwan. b is the reading that follows the rules. If he keeps N, record a with the
>   measured worth on full lessons.
>
> [^n]: LEAK-41 (Must), LEAK-10 (span clause, amended 2026-11-08, X4), USE-8.

**4. Issue 9 (`delta`): consistent, with one number missing from the note (NEW, small)**

- Rec. A follows noaa_storm_events_damage's Flash Flood duration (Lennart, 2026-11-08). There the outcome draws a
  minority of the spans, the rows it drew cannot be told apart, and the span keeps its worth elsewhere, so it was kept
  with a note.
- What sets it apart from bank_marketing `campaign` and heart_failure `time` (dropped): most of `delta`, the break
  before the lesson, lies before the prediction point. Only the current lesson's length lies after it, and that is a
  large share only for back-to-back rows. The issue should state this contrast.
- The span clause wants the note to give the worth on the rows the outcome did not draw. The table already holds it:
  floored delta 0.6627 against no delta 0.6578, about 0.005 AUROC from deltas of 15 minutes or more. The proposed note
  gives only the worth of short deltas (0.0023-0.0028). Add the other number.
- The rec's "the worth is small" should not carry the decision (X4: "the size of the worth alone never decides"). The
  mechanism argument already does.

**5. Training cap applied in the container, plain name instead of `_1m` (NEW)**

- Convention (definitions.md, issue #70, Lennart 2026-11-10; v0.2 budget, Lennart 2026-11-12):
  - "The train side keeps every row available to it ... N is recorded, not applied."
  - A v0.2 dataset whose splits have a side over the budget "is the version named `<name>_1m`".
  - The test cap is the collection's 500k.
- The definition draws 1M training rows itself in `_make_splits`, caps test at 111,111 and ships under the plain name.
  The AI's compatibility repair (2026-11-16, CHANGELOG) gives the reason: "Plain names support custom capped splits;
  the collection's `_1m` suffix selects automatic sampling of full training history."
- The curator's approval of the caps (Myunghwan, CC 2026-11-02, "90/10 ratio") predates issue #70. No curator line
  approves the switch from `_1m` to a plain name. That was an AI repair.
- fugaku_hpc_job_failure (also Myunghwan) has the same departure. These two are the only v0.2 definitions with a
  hand-rolled train cap among the 18 `_1m` folders and the rest. A third would make an amendment due.
- The smaller test cap has its own stated reason (90/10, CC 11-02). The capped train side has none beyond keeping the
  old draw.

Reflection prompt:

> **Ship as `duolingo_spaced_repetition_recall_1m` with full training history, as every other over-budget v0.2 set does?**
>
> - **Problem:**
>   - Since issue #70 (Lennart, 2026-11-10) the train side keeps all earlier rows and the benchmark samples N.
>   - This definition and fugaku_hpc_job_failure fix a 1M training draw in the container under a plain name, through
>     an AI compatibility repair (2026-11-16), not a curator line.
> - **Options:**
>
>   | | Option | Pro | Con |
>   |---|---|---|---|
>   | a | Keep the fixed draw as an exception, its fact: the 90/10 ratio Myunghwan chose to match the source (CC 11-02) | keeps the approved container byte-identical | the ratio also holds after the benchmark's own sampling; departs from 16+ `_1m` sets |
>   | b | `_1m` with the collection's budget; test cap 111,111 kept as a curator choice if the API allows, else 500k | follows the convention; the sampling can be studied | rebuild; the training rows change |
>   | c | Amend the convention to allow a fixed train draw | — | reverses issue #70's reason (models may see more history) |
>
> - **Recommendation:** b, decided together with fugaku_hpc_job_failure.
>
> [^b]: definitions.md "Larger than the row budget" (issue #70; Lennart 2026-11-10, 2026-11-12).

**6. 75% cutoff vs TP-7 (KNOWN)**

- TP-7 (Must): a target the definition builds uses "an established convention". The AI assessment of 2026-11-05 says
  the 75% is curator-selected, "not ... a blanket satisfaction of TP-7, or a general rule amendment".
- The cutoff is therefore a departure from a Must, with a stated reason but no higher-ranked Must. Under "Consistent
  judgement" case 1, the remedy is an exception with its fact, or an amendment.
- The only TP-7 precedent, audiology_diagnosis, rebuilt the target on a field convention. I found no precedent of a
  curator cutoff on a continuous target.
- Option (a) for the curator: the source's fraction is quantized by N (mostly 1 to 3 exercises), so no
  fraction-scale target is meaningful (CC 11-02), and the cutoff was tested against all-correct. Record that as the
  exception's fact. Low priority: it was settled twice by Myunghwan.

**Consistent (no prompt)**

- Issue 7, the own-row protocol with `history_correct` kept: same shape as loan_default_prediction_imperial_college
  f615/f617 (Andrej, 2026-11-10, kept with a protocol line), medical_facility_operational_data (Lennart, 11-05) and
  fremtpl2 (11-05). spanish_motor_insurance_coverage_level_2022_2024 removed a history instead, but there a renewal's
  prior-year claims are not the row's own legitimate history. Not a conflict.
- Temporal split with recurring learners: SPLIT-13 (known entities are the use) and the Dated event log leaf.
- One-day windows: the source's single cut tests about the newest 1.3 days. Following the source's test span matches
  medical_facility_operational_data (SPLIT-12). The weekly windows of delivery_eta and nyc_taxi were their sources'
  periods, so no conflict.
- The record's `Target: Varying Delay` tag fits: the add-dataset skill defines it as "a count or a length that the
  outcome stops", which is what issues 9 and 10 found.

**No drift found**

Myunghwan's one-day gap on duolingo (11-02/03) and his no-embargo decision on fugaku (11-03) look opposite. They were
consistent on the facts known then: duolingo's clock meaning was unverified, fugaku's was exact. The 11-21 measurement
removes that difference (finding 1).

</details>

<details><summary>Blind review (2026-11-21)</summary>

**Blind review: Duolingo half-life regression traces, target `session_accuracy_at_least_75`**

**Verdict: include with changes.** The data is real and the task is real (scheduling vocabulary review). As prepared, though, the strongest feature, `session_seen`, is not known when the prediction is made, and much of its signal comes from the 0.75 threshold rather than from memory. Drop `session_seen` from the features, or redefine the target, and state the weak-signal ceiling.

**What the task is**
Duolingo's student model estimates, before a lesson or practice session, how likely a student is to recall each word. It uses that estimate to rank words for practice and to set the skill "strength meters". Settles & Meeder (ACL 2016) say: "Since our model is used to prioritize words for practice, we use AUC to help evaluate these rankings." So the use is real: the scheduler makes the prediction when it picks the next session's words.

**Concerns, most serious first**

**1. `session_seen` is unknown at prediction time and is mechanically tied to the target**
- The README defines it as "times the user saw the word/lexeme during this lesson/practice". It describes the session whose outcome is being predicted.
- The paper says "Each lesson continues until the student masters all of the target words being taught in the session". The number of exposures therefore depends on the student's errors, so it is partly an outcome.
- The binary target is `p_recall >= 0.75`, with p = correct/seen. That means 1/1 for one exposure, 2/2 for two, 3/3 for three, and only 3/4 for four. The threshold alone moves the base rate:

| session_seen | P(target = Yes), sample | mean raw p_recall, full 12.9M |
|---|---|---|
| 1 | 0.885 | 0.884 |
| 2 | 0.830 | 0.910 |
| 3 | 0.775 | 0.918 |
| 4 | 0.962 | 0.917 |
| 5 | 0.935 | 0.914 |

  The raw recall rate is flat from 2 exposures up, but the binarized target swings by 19 points. That is an artefact of the threshold, not memory.
- Effect on scores (temporal split, 3 two-day windows, 200k-row sample, AUC; log loss shows the same pattern):

| features | LogReg AUC (w0/w1/w2) | LightGBM AUC (w0/w1/w2) |
|---|---|---|
| history only (delta, history_seen/correct, languages) | 0.604 / 0.604 / 0.596 | 0.593 / 0.596 / 0.589 |
| + lexeme_string | – | 0.600 / 0.599 / 0.595 |
| + session_seen | 0.654 / 0.655 / 0.651 | 0.649 / 0.649 / 0.649 |
| session_seen alone | 0.596 / 0.594 / 0.600 | 0.596 / 0.594 / 0.600 |
| prior (log loss) | 0.394 / 0.384 / 0.393 | |

  `session_seen` on its own carries as much AUC as all the history features together.
- **Change:** drop `session_seen` from the features. If it is kept as a "planned session length", the target must not depend on it. Options are a target of `session_correct == session_seen` (perfect recall) with a note, or a regression on `p_recall`, the paper's target, weighted by `session_seen`.

**2. Weak signal, and the model ranking may not separate methods**
- Without `session_seen`, the best AUC is about 0.60 and log loss gains only 0.006–0.009 over the prior. Linear LR matches or beats LightGBM.
- The paper reports similar ceilings: "AUC of 0.5 implies random guessing ... so the AUC values here may seem low. This is due in part to an inherently noisy prediction".
- Noise is a legitimate property, but a benchmark gains little from a task on which every method scores within about 0.01 AUC.
- **Change:** keep the task only if the panel accepts a low-ceiling task. Report it so the low numbers are expected.

**3. The user identity was removed, and the split ignores users**
- The raw data has `user_id` (115,222 users). The sample holds 55,287 users with a median of 2 rows each.
- Student ability is the main source of variation that the scheduler actually knows, through each user's history over all words. Without the user id or any user-level aggregates, the task models only word-level history.
- Under the temporal split, the same students appear in training and test. This is consistent with deployment (a known student going forward), so it is not a leak. But because the id has been dropped, a "student" model cannot be built either.
- **Change:** consider adding user-level history aggregates known before the session (the user's past accuracy over all words). Do not add the raw id.

**4. The prepared table is an unexplained 11% subset**
- The raw file on Dataverse has 12,854,226 rows. `task.md` gives 1,429,456 rows for the prepared table.
- Every one of the 200,000 sample rows matches a raw row exactly. The target agrees with `p_recall >= 0.75` on 100% of them.
- The distributions of delta, history and session_seen match the raw data, and so does the language mix. The subset looks random, but the selection rule is not stated.
- Random row sampling also breaks sessions apart. A raw session holds a median of 8 word-rows and a mean of 14, and these rows share user and timestamp. That is harmless for a temporal split.
- **Change:** document how the 1.43M rows were chosen.

**5. Licence**
- The Dataverse terms say: "This work is released under the Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)".
- The GitHub repository's MIT licence covers the code only.
- **Change:** confirm that NC data is allowed in the benchmark.

**6. Minor preparation points**
- `lexeme_string` is a category with about 8.7k levels in the sample. More than 97% of test rows' lexemes appear in training, so this is fine. The string has structure (surface/lemma<POS><tags>) that a parsed POS column would expose; optional.
- `history_correct` is at least 1 in every raw row, including rows with `history_seen` = 1. The traces evidently start after a first correct exposure. This is a property of the source, not of the preparation.
- The timestamp span is 2013-02-28 to 2013-03-12, 12 days. Three test windows over 12 days are acceptable, but they show no drift; the AUCs are flat across windows.
- `task.md` names no weight column, so I did not judge one. If weights are added, `session_seen` is the natural weight for a regression on `p_recall`.

**Data is genuine**
- Every sample row matches the public 12.9M-row file.
- The values are plausible: delta from 1 s to 467 days, history counts up to 13.5k (heavy users), and no missing values.

**What I could not check**
- I could not run the paper's HLR method itself, and I did not read the paper's exact Table 2 figures; my PDF text extraction was crude. The quoted sentences are from the paper.
- I do not know how the 1.43M subset or the three test windows were defined. I used my own windows: test periods 03-07–08, 03-09–10 and 03-11–12, each trained on all earlier rows.
- All models ran on the 200k sample, not on the full 1.43M rows.
- I did not test whether `session_seen` is fixed in advance for practice sessions, as opposed to lessons. Only the lesson behaviour is documented.

</details>

<details><summary>Task gamer (2026-11-21)</summary>

**Task gamer report: duolingo_spaced_repetition_recall**

**Verdict:** the task can be gamed only a little. One real exploit exists: a later row of the same user and word gives away the exact session outcome. It covers 3–5 % of test rows and adds +0.02 to +0.035 AUC over the baseline. The other large effects (`session_seen`, session context) are information a deployed model would have.

Setup: LightGBM, 300 trees, lr 0.1, 63 leaves, n_jobs=2, no tuning, no weight. Splits are the 3 shipped day windows (test = 10, 11, 12 March 2013). Each training set is 1M rows sampled from the rows before the day ahead of the test day, so there is a one-day gap. `timestamp` is used as epoch seconds. Noise check: the baseline plus a random column moves by −0.002 to +0.003.

**Exploits**

| # | Exploit | Script | Honest score (base) | Exploited score | Gain (r0 / r1 / r2) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| 1 | Next record of the same user–word among train+test rows. Link: `ts_next − delta_next == ts`, same lexeme and languages, `history_seen_next == history_seen + session_seen`. Then `history_correct_next − history_correct` = session_correct. Used as a feature or as a rule that overwrites the prediction | work/attack.py | 0.658 / 0.650 / 0.656 | rule: 0.694 / 0.672 / 0.681; feature: 0.692 / 0.672 / 0.680 | +0.035 / +0.022 / +0.025 | No: it is the outcome, read off a later row | Coarsen `delta` (and `timestamp`) so the link no longer resolves, or split by user. Fix untested |
| 2 | #1 plus the mean linked outcome of the other words in the same session (`ts` + languages = one user's lesson). Covers 10–20 % of test rows | work/attack.py | same | 0.692 / 0.675 / 0.676 | +0.034 / +0.024 / +0.020 (no gain over #1 beyond noise) | No | same as #1 |

Against the better honest model (no `timestamp`, plus session context: 0.665 / 0.665 / 0.668), exploit #1 should still add about +0.01 to +0.03. I did not refit that combination, so this is estimated from the separate runs.

**#1 mechanism.** The data keeps every row's `history_seen` and `history_correct` before the session and `delta` since the previous view. A later row of the same user and word therefore holds the earlier row's session result as a difference. The link I built is almost exact: on the full file, 76,108 rows are linked, and the recovered label matches the true one 99.98 % of the time. Of the test rows, 5.2 % / 3.3 % / 3.6 % have their next occurrence inside train ∪ test. The coverage is low because the kit is about 11 % of the 12.9M-row source. Mildest fix: round `delta` to hours or days, and check that the link rate falls to near zero. A user-grouped split would also work, but `user_id` is not in the kit.

**Flaws that hurt an honest model**

| What is wrong | Honest choice | Baseline | Honest score | Fix to the task |
|---|---|---|---|---|
| `timestamp` is a feature, but in a forward split the trees cannot extrapolate it | drop `timestamp` | 0.658 / 0.650 / 0.656 | 0.659 / 0.659 / 0.661 (+0.001 / +0.008 / +0.004) | Optional: leave it out of the features, or keep it and document it. This is mostly a modelling choice |
| Each training set leaves out a full day between training and test, and is a 1M subsample | train on every row before the test day | same | 0.660 / 0.660 / 0.658 (+0.002 / +0.010 / +0.001) | Small: close the gap if it is not intended |
| User history is gone because `user_id` was dropped | rebuild the user's previous-session outcomes from the past links | same | 0.658 / 0.652 / 0.657 (≈0, within noise) | none needed |

**Strong features that are signal, not exploits**

- **`session_seen`** is worth 0.04 AUC: dropping it gives 0.614 / 0.603 / 0.617. Most of the effect comes from how the target is defined. "≥ 75 %" means 1/1, 2/2 or 3/3 for up to 3 views, but only 3/4 for 4 views. So P(Yes) is 0.88, 0.83, 0.78 for 1–3 views and jumps to 0.96 at 4. I tested whether mistakes cause extra views, which would make the column post-outcome. They do not:
  - 11.9 % of single-view words are wrong.
  - The linked session_correct counts are more all-correct than a binomial would give: at 3 views, 0.766 got 3/3 against 0.683 expected, and only 0.024 got 1/3 against 0.038 expected.

  So `session_seen` is not driven by errors. A deployed model would have it if the lesson plan is fixed when the lesson starts. What decides it is whether Duolingo set the number of views per word at lesson start in 2013. If it did not, the column is partly post-outcome.
- **Session context** is honest: number of words in the lesson, the other words' `session_seen`, and the mean history accuracy of the lesson's words, which proxies the dropped user id. Without `timestamp`, it gives +0.006 / +0.006 / +0.007. Most of that comes from `sess_hacc_mean`: on its own, 0.665 / 0.665 / 0.667 against 0.659 / 0.659 / 0.661. All of this is known when the lesson starts (work/attack3.py).

**Attacks that found nothing**

- **Row order:** labels of neighbouring rows within a session agree 0.795 of the time, against 0.770 if independent. That is the same user, not ordering. Position in the session plus session size scores 0.659 / 0.659 / 0.659, about the same as the baseline with `timestamp` dropped.
- **Formats:** every numeric column is a whole-number count or an epoch second, and `lexeme_string` is a fixed tag template. There is no format left to exploit.
- **Lookup in the source file:** the published file has `user_id`, `session_correct` and `p_recall`, so looking the rows up by timestamp, lexeme and history would work. This is true of any public dataset and is not ranked. I did not download it (13M rows).

**Not checked**

- Whether coarsening `delta` closes #1 without hurting the honest score.
- A train-vs-test classifier.
- Multi-hop user chains to spread the future outcome over more test rows. I expect little gain, since session mates added nothing over #1.
- The web search found no competition, no leak thread and no published critique of this table.

Scripts and logs are in work/: explore.py (1401932), attack.py (1401943), attack2.py (1401951), attack3.py (1401957), and the *_results.csv files.

</details>

<details><summary>Column audit (2026-11-21)</summary>

**duolingo column audit — full data; 2 issues (delta to lesson end; session_seen cut by failure); timestamp = lesson END (measured)**
Horizon evidence: label exists at stamp; option B's session-length assumption not needed; zero gap label-safe; newest day hourly profile matches.
Doc fixes: known/fit_reason/first bullet/splits comment: "start/completion unverified" -> "timestamp marks lesson completion, label exists then"; row: "only words seen before appear (history_seen>=1)"; counter bullet: delta = gap to pair's previous logged session 88.0%, +1s 11.5% rounding, 0.45% unlogged sessions (0.37% after Yes, 0.31% after No). Assessment: timestamp marks lesson end.

</details>

<details><summary>Qualification reuse scope and rule wording</summary>

**Qualification reuse scope:** The current focused review runs a fresh independent claim/precedent audit, mediator and editor through the updated installation. Earlier column/split, participant attack and successor-refutation reports below remain dated prior executions: exact source, package versions, values, category state, labels, scorer and six memberships verify their reuse. No new model fit, participant attack or full panel is claimed. The latest user explicitly directs retention of prior decisions; original human marks retain their original identity.

**Current rule wording:** The established-convention condition in TP-7 is a Must. This particular 75% task follows Myunghwan's explicit task-specific direction and latest instruction to retain it; the cutoff is not claimed to be a source convention, a blanket satisfaction of TP-7, or a general rule amendment. The historical attributed wording remains preserved.

</details>

<details><summary>Mediator</summary>

**Focused Duolingo mediator judgment**

2026-11-05. Base: `9048f36a1bcf7da3687fde04b18ef79cd7a1201e`. Dataset: `duolingo_spaced_repetition_recall_1m_clf`.

Verdict: ship after changes. The owner has added the explicit per-row inference protocol, demonstrated successor attack and measured size, and Duolingo benchmark-side checking TODO. I inspected those actual updated definition/record/TODO bytes. Finish the small documentation consistency changes below and native verification, then the authorized local build/commit. These are routine corrections under current LEAK-9, not a new scientific choice. Preserve the approved eight predictors, labels, weights, metric and six split arrays. This judgment does not certify downstream benchmark enforcement.

Validity: the newly demonstrated other-test-row attack is an evaluation leak (LEAK-9), requiring the protocol correction below. The evidence does not show that a row's own `history_correct` contains that row's current outcome (LEAK-10); its legitimate prior history remains protected by LEAK-34. The approved approximate conditional task and temporal regime remain intact. Value: the exact approved predictions retain mean AUROC 0.663756, versus 0.596148 for train-only N rates; fresh task probes have no flags. Quality: no new dtype repair is needed; lexical morphology is nominal, counts numerical. Weighed: the previously accepted realized-N, recorded-clock/label-arrival, imperfect-history, short-period and exploratory-selection limitations remain. For the curator: no new weighing call remains under the current general amendment and directly matching precedent.

**Changes to make now**

1. State the operational protocol in `task_summary`, `curation_comments` and `splits_comment`, so it reaches the generated README and built metadata. For each split, fit preprocessing and learned state only on that split's training rows. Freeze that state, then predict each test row from that row's supplied covariates only. No feature construction, preprocessing, model update or prediction step may use other test rows, future session histories, test-block statistics, or held-out labels from another split. Batched computation is permissible only when the prediction for a fixed row is invariant to the other test rows. Same-clock rows do not receive an invented arrival order. This is a snapshot protocol; allowing sequential test-history updates would be a separately defined protocol. Rules: LEAK-1/9, USE-3.
2. Add a `Potential leak, kept on purpose:` evaluation note naming the successor mechanism, full-fold coverage and measured gains below. Distinguish it from the already accepted source-history inconsistencies. The leak is newly found and materially measured; the old note neither disclosed nor accepted it. Rules: LEAK-6/9, EV-2/6/7.
3. Add Duolingo and this concrete mechanism to `datasets/_dev/tabarena-v0pt2/BENCHMARK_CHANGES_TODO.md`, under "Test rows predicted without the other test rows". Retain the requirement to inspect/exclude transductive methods or verify invariance to other test rows. Record this as required benchmark follow-through, not an executed check. Rules: LEAK-9, EV-7.
4. Use an AI assessment for this application of current policy; do not invent a new curator CC or a new acceptance mark. Regenerate/check metadata and README, verify exact values/categories/labels and all six split arrays, and complete the already authorized build/reload/checksum verification and local commit. A metadata checksum change is expected when protocol prose changes; do not describe it as unchanged metadata or silently replace historical identities. Rules: EV-7/8; repository build/record procedures.

Status on inspected updated bytes: the `known` summary, `Evaluation protocol (LEAK-9)` curation bullet, dated November 5 AI assessment and TODO implement the substantive correction and accurately leave downstream enforcement pending. Add the standard `Potential leak, kept on purpose (LEAK-9, an evaluation leak):` prefix to that bullet and a short own-row protocol reminder to `splits_comment`, as the medical-facility precedent does. These are cheap consistency edits; neither opens a scientific choice. Native regeneration and build are still in progress, not reported complete here.

The proposed protocol wording is: "For each split, fit preprocessing and the model only on its training rows and freeze learned state before evaluation. Predict each test session from its own supplied covariates only. No preprocessing, feature or model step may use another test row, future session histories, test-block statistics or held-out labels from another split. Batched prediction must leave each row's prediction unchanged when the other test rows change. Methods that learn from the test block are excluded from this task's benchmark."

**Issues for the curator**

None. This is conditional on implementing the corrections above. A desire to permit transductive/sequential test adaptation, change the feature set instead, or claim that unrestricted bulk predictions are valid would require a different protocol or new decision. None is requested or necessary here.

Missing executed downstream enforcement is real, but is not a new human choice for this local data build. The current amendment delegates checking to the benchmark; its exact motivating precedent already ships a written protocol with the benchmark check left on this repository's TODO. It would be inconsistent to invent an immediate harness-implementation gate for Duolingo while claiming to apply that amendment. Conversely, writing the line does not make an unchecked transductive benchmark result honest: such results remain ineligible under the protocol. Curation/build readiness and execution of compliant future benchmarks are separate factual claims.

The claim auditor's final addendum recommends issue 7 as a human choice between the protocol and dropping `history_correct`. I accept its factual refutation and its warning against inventing downstream enforcement. I do not accept that applying the current general remedy requires a fresh human mark. No distinguishing fact or contradictory current rule is identified; the amendment specifically covers this demonstrated mechanism, its motivating case already accepts the same deferred checking boundary, and LEAK-7 favors preserving valid signal. Dropping the history feature remains an optional changed task, not an equally mandatory unresolved fork. The auditor's request to present alternatives does not itself create a weighing call where current policy and direct precedent select the mildest adequate remedy. Keep the addendum as evidence and record this disagreement/resolution rather than rewriting it as unanimous initial approval.

**Agreed facts and decisive evidence**

I read the current mediator role, full review-panel procedure, principles and applicable leak/evidence rules; the current definition/record; `claim-audit.md`, `column-split-audit.md`, task/leak/dtype/check outputs; the final `participant_kit/REPORT.md` and associated evidence; and final independently authored `successor-refutation.md/json`. This is the focused tier: claim/precedent audit, column/split audit, participant gamer, independent attack refutation and mediator; a cold editor follows. There is no full-tier advocate/critic debate to imply.

The participant constructs matches without labels: same learning/UI language and lexical tag; successor clock minus its delta equals the current clock; successor prior exposures equal current prior exposures plus current N; successor correct-count minus current prior correct-count is a feasible current K. The resulting label is `4*K >= 3*N`. Every accepted successor is later than the row being predicted. Same-test-only access suffices; learner ID, future test labels, cross-fold rows and post-window records are unnecessary.

The independent refutation uses every actual 111,111-row test array and frozen, already qualified honest predictions. It rejects inconsistent candidate labels before scoring and confirms:

| Test day | Recovered rows | Coverage | Correct recovered labels | Honest AUROC | Attack AUROC | Gain |
|---|---:|---:|---:|---:|---:|---:|
| March 12 | 5,759 | 5.1831% | 5,758 (99.9826%) | 0.662491 | 0.697404 | +0.034913 |
| March 11 | 3,687 | 3.3183% | 3,687 (100%) | 0.662434 | 0.683475 | +0.021041 |
| March 10 | 3,978 | 3.5802% | 3,977 (99.9749%) | 0.666342 | 0.690257 | +0.023915 |

These are new rescoring experiments, not new model fits. The participant separately fitted 100k-train/50k-test untuned controls and found same-test-only gains of +0.036001/+0.023078/+0.025357 over its stronger honest engineering comparator. Those smaller-sample fits and bootstrap intervals must not be mixed with the full-fold frozen scores. Label recovery includes hundreds of negatives per full fold; a majority-class prediction does not explain it. Source-counter imperfections do not refute this measured route.

The current gap separates training and testing; it cannot prevent a later test row disclosing an earlier test row's outcome. Removing learner recurrence likewise does not directly address the demonstrated within-test-window channel. LEAK-9 applies because the attack reads another test row, while each counter remains prior history at its own row. This is not a conflict in which a Should overrides LEAK-10's Must: the alleged own-row post-outcome feature defect has not been demonstrated. LEAK-6 requires acting on the confirmed attack; LEAK-7 and the remedy ladder favor the valid-signal-preserving protocol fix supplied by LEAK-9.

Dropping `history_correct` blocks the tested exact K subtraction. In the participant's bounded comparison, it costs 0.00723-0.01312 AUROC for the raw control and 0.01539-0.02318 for the engineered control (also removing its derivatives). It changes approved inputs and would need fresh qualification. Under current LEAK-9 it is an optional, more destructive repair, not required. No untested alternative attack is asserted as a reason against it.

Other participant hypotheses did not establish another corrective data finding: full-feature cross-side copies are absent; descriptor lookup, formats, past-neighbor labels and row position do not establish an unavailable-outcome channel. Full-table lexical/cohort statistics gave small gains, but causal controls were not isolated, so this is not a second proven mechanism; the proposed protocol excludes test-block-derived predictors regardless. The owner's fresh raw-order adjacency flag concerns raw order removed by content ordering and actual time sorting; no shipped ordering exploit follows from that flag alone (EV-3). Dropped current fraction/count are expected label ingredients; their strong scores support their exclusion.

Current native checks report 27 passed, zero errors/warnings; fresh task probes show usable signal and no flags. The independent audits verify exact frame values, category state, labels and six split arrays against the approved package; legitimate qualification may be reused for those identical inputs. Those checks did not themselves test other-test-row access. The attack refutation supersedes any earlier broad reading of "no new leak found."

The participant additionally ran `batch_invariance.py`: for its fold-0 honest model on 50,000 fixed test rows, whole-batch versus 1,000-row chunks and 100 single-row predictions have maximum absolute difference zero (`batch_invariance.json`). This verifies that tested model's batch behavior only; it neither screens every benchmark method nor establishes a downstream guard.

**Consistency and execution boundary**

The current `medical_facility_operational_data/dataset.py` notes (lines 109-110 on this base) describe the same direction of information flow: a later row's own legitimate history reveals an earlier row's outcome. It keeps the fields, requires train-plus-own-row prediction, and records the November 5 LEAK-9 amendment and benchmark TODO. This remains accepted despite a much larger measured MAE gain. `fremtpl2/dataset.py` records the same amendment for label-free renewal information read from other rows, separately from its own-row BonusMalus repair. `sepsis_prediction_1m` forbids combining other patient hours under its snapshot task, while retaining patient-hour records; `5g_energy_consumption` explicitly makes station-hour predictions per sample and calls other-row learning transductive. These support the protocol remedy, not feature deletion or an invented learner holdout.

The decisive current implementation contract is the existing final TODO section: Data Foundry ships a protocol line and no per-row scorer; the guarantee sits in the benchmark, which must check models and exclude test-block learning. LEAK-9 is the current general amendment, not merely an old dataset-specific exception requiring renewed human approval every time it applies. The user also explicitly authorized repeating the full cycle with prior choices and local build/commit. Applying this existing remedy changes no settled target or inclusion choice.

Executed evidence here consists of inspection and synthesis of the final reports and actual current rules/definitions. I did not modify canonical source, run downstream enforcement, refit a model, build a container or create human marks. The owner must implement and verify the documentary changes and authorized build; future benchmark method checks remain pending. Preserve these boundaries in REVIEW, the record and final handoff.

</details>

<details><summary>Claim and precedent audit</summary>

**As-of scope:** The initial checksum analysis below used the byte-identical approved definition before the successor-counter finding. It attributes that initial framework-only change to special_features=[]. The final definition additionally records the own-row protocol, intentionally changing metadata again; the final native regeneration and build establish its current checksum. The successor addendum and mediator settle the later evaluation finding.

**Focused independent claim and precedent audit**

2026-11-05 UTC. Qualification source revision: `9048f36a1bcf7da3687fde04b18ef79cd7a1201e`. Dataset: `duolingo_spaced_repetition_recall_1m_clf`. Independent claim and precedent audit; no new model fitting.

Verdict: the preserved inclusion decision remains consistent. No new human decision or scientific repair is identified by this audit. The current source, frame, categories, labels, metric and six split arrays support reuse of the approved numerical qualification. The changed container checksum is entirely a current-schema metadata change, not a changed task. Final panel synthesis and build verification remain the owner's work; this report creates no new human marks.

Validity: the source and target-construction claims hold; the conditional realized-N, recorded-clock, label-arrival and source-history limitations remain explicit rather than being certified as resolved. Value: the full classifier beats the natural count-only baseline on every window; a current full task-probe run is owned by the main session, with prior exact-data qualification available. Quality: numeric counts, nominal lexical tags and No/Yes target remain consistent with the updated dtype rules. Weighed: a large, traceable education task with an approximate practical fit, short coverage and exploratory formulation-selection limits. For the curator: no reopened question from the facts inspected here.

**Scope, identities and evidence**

I read the current add-dataset panel procedure, claim-auditor and precedent-checker role files, both knowledge skills, principles/evidence and applicable use-case, split, metric, task and cleaning rules; current definition/README/record; the November 3 acceptance and its actual input/marks; the prior focused numerical and precedent audits; and the rule changes from `1964e1b2e4caa41c8a94082e028f65d4cd8b2b6b` to current main. The preserved diff is `claim-rule-changes.diff`. The historical local implementation commit `7c1928bb...` is not present in this refreshed Git object store; I used the available historical instruction commit plus the preserved actual definition/metadata/artifacts, rather than inventing a Git comparison.

The declaration SHA256 is `10e6c681a128763a081ad3ed086f5f54a21b60d77fd7b74d211b382cd1a1a06f`. The old qualification manifest records an earlier pre-approval documentation SHA (`a4298686...`), so those two definition hashes must not be described as identical. The old accepted built dataset metadata and current definition-generated dataset metadata compare exactly; task metadata differ only by the empty field described below. The data Parquet SHA256 remains `b6f104eed4cddf621d169771c84bf61e3cdb2380dd797014e9160433dcf0d596`, identical to the historical presentation frame. All six array comparisons passed independently in `claim_audit.py`, alongside the owner's stricter value/category comparisons.

Fresh independent evidence: `claim-audit-evidence.json`, executable `claim_audit.py`, `claim-source-counts.json`, executable `claim_source_counts.py`, and `claim-metric-stability.json`. The fresh decision register is `claim-register.json` / `claim-register.txt`. The column/split reviewer separately supplied `column-split-numerical.json`; source-to-selected-row lineage and the 81-copy count are inherited from the prior explicitly scoped full-source audits, not falsely presented as a new full-source alignment by this reviewer.


**Claims and attempted refutations**

Each quoted phrase below identifies a claim in current `dataset.py` task_summary/comments/splits_comment, generated README, or dated record. `Holds` means the stated, bounded claim survived the cited test; it does not mean every conceivable leak was ruled out.

| Claim and source | Refutation test actually run or inspected | Result and evidence | Rule |
|---|---|---|---|
| “One learner-word lesson or practice session”; six-language logs in late February–March 2013 (summary/README) | Reopen original paper grain; inspect fresh frame and source split audit | Holds. Paper section 4.1 describes learner-word session traces; frame has six learning languages; actual selected clocks span February 28 to March 12, newest end 16:14:57 UTC | USE-1/5, EV-2 |
| “At least 75% correct”; “4*K >= 3*N”; “Exact 75% is positive” (predicted/_clean/comments) | Independently stream all raw numeric outcomes and denominators, test integer/boundary formula against published fraction; inspect exact-data historical lineage | Holds. 12,854,226 source rows; zero bad denominators, count bounds, nonintegers or fraction mismatches. 169,363 source rows exactly 75%; zero integer-vs-fraction 75% mismatches. Prior aligned audit verified all 1,429,456 selected labels, including 18,802 exact-75% positives; current frame/labels are identical | TP-7, LEAK-4, CLEAN-1, EV-8 |
| “At N=1,2,3 this criterion equals all-correct; at N=4, 3/4 is positive” (comments) | Numeric stream checks N<=3; inspect exact integer rule for N=4 | Holds, zero N<=3 disagreements. At K=3,N=4 the implemented inequality is equality and positive | USE-5, TP-7 |
| “No rows are removed for having a particular outcome”; dedup precedes coarsening (comments/_clean) | Read actual pipeline; compare present output with approved frame and prior source-copy audit | Holds as implemented. Only source-copy removal precedes the label mapping; no binary-outcome filter or exercise weighting. Current frame has 1,240,113 Yes and 189,343 No (86.75419% Yes) | LEAK-16/19/20, CLEAN-1 |
| “83.886% ... all correct and 58.937% ... one exercise” (source-limit comment) | New full numeric raw stream | Holds: 10,782,942 all-correct / 12,854,226 = 83.88636%; 7,575,913 N=1 / 12,854,226 = 58.93714% | EV-2/7 |
| “Verify MD5 ... and 379004009 bytes” (download description) | Hash and size actual gzip | Holds exactly: MD5 `0a1cae5eb7ad4b0bd9c0de91d74fcced`, 379,004,009 bytes; SHA256 `26cf9b33f2e9b2e8aa9a8f262a017b30699ca2f625c56a12ce699d4ea7076873` matches prior qualification | PROV-8/13, EV-8 |
| “Eight predictors”; no current correct count, fraction or opaque IDs (summary/comments) | Inspect real frame schema and missing/copy counts | Holds: clock, delta, two languages, lexical tag, two history counts, N. No `p_recall`, `session_correct`, `user_id` or `lexeme_id`; no missing cells or full final-row copies | LEAK-10, CLEAN-1/14 |
| “Numerical session_seen remains a conditioning input, not a label by itself” (comments) | Inspect both outcomes within N and independently rebuild every test N-only training-rate probability | Holds. N spans integer 1–20, common N strata contain both labels; N-only baseline is each binary label's training success rate and exactly reproduces saved probabilities. It is not the former mean-fraction baseline | TP-4, LEAK-4, EV-5/9 |
| Lexical tag is nominal morphology, not prose or a severity scale (comments/_feature_types) | Inspect current dtype flag and actual lexical values against source Fig. 2/Appendix semantics | Holds. Fresh `ordinal_like` heuristic flag concerns strings such as lexical/morphology tags, not ordered severity levels. No semantic order is supplied; retain unordered category. Real counts stay numeric under updated CLEAN-14 | CLEAN-12/14/25, EV-3 |
| Three March 12/11/10 one-day windows, one-day gap, 1M/111111 per fold (split text/_make_splits) | Independently inspect six arrays, temporal boundaries, class support and source-code eligibility | Holds. Gaps 86403/86407/86401 seconds; every fold has 1,000,000 train and 111,111 test, with 14,780/14,835/14,806 negatives. Distinct training arrays, expanding eligibility. Separate source audit lower-bounds full-source train fractions at 86.48/78.32/70.80%, all above 50% | SPLIT-2/9/10/11/14, TP-5/9 |
| “Approximately 90/10 after sampling”; not the paper's single cut (summary/version/splits) | Arithmetic caps and primary paper section 4.1 | Holds. 111111/(1000000+111111) is approximately 10%; source uses one first-90%/last-10% split. Current text clearly disclaims literal reproduction | SPLIT-5/19/20, EV-2 |
| “All learners are eligible ... may recur; no learner holdout” (comments/splits) | Inspect actual split code and feature exclusions; compare prior curator input | Holds. Temporal windows receive the full cleaned source; no learner reservation exists. Recurrence is deliberate, not a cold-start claim | USE-10, SPLIT-3/13 |
| Output is P(K/N>=.75|X,N), not E[K/N|X,N]; goal is curator-selected (summary/comments/record) | Compare formulas and actual binary output, exact November 3 task-selection and approval input, and source evaluation | Holds as an approximate conditional session-performance task. The criterion is not asserted to be mastery or a deployed source rule. The two estimands are explicitly distinguished; source target is quantitative session performance | USE-1/3/5/8, TP-6/7 |
| “AUROC ... ranking ... not calibration ... or accuracy at a fixed action threshold” (training comment) | Inspect standard metric declaration, score categorical target on every fold, and current edge cases | Holds. Binary fallback `roc_auc`, no scoring columns/weights/threshold params; constant native AUROC .5 each fold. All-zero/all-one/tied probabilities are finite and permutation invariant; NaN/Inf raise ValueError | MET-2/7/8/11/12/13 |
| “Source ... MAE ... AUC/half-life correlation”; its rounded AUC is not the 75% event (metric reason) | Reopen paper section 4.1 and publisher evaluation.r | Holds. Publisher AUC code uses `round(p)`; no inclusive-75% convention is defined there. New README origin now says “no metric the task would use in practice”, fixing the earlier generic false “no metric” boilerplate | MET-1/2/5/8/11 |
| Equal records; diagnostic binary log loss with AUROC/logloss reporting; benchmark objective is its own (comments/model evidence) | Read executed model protocol; independently re-score all 12 predictions and reconstruct train-only N rates | Holds. Native scorer, independent rank-sum AUROC and manual logloss reproduce all 12 rows, maximum discrepancy 1.11e-16. Mean AUROC constant .500000, N-only .596148, without-N .622571, with-N .663756; full beats N-only in AUROC and logloss on every fold | EV-1/2/5/7/8 |
| Existing numerical qualification can be reused on refreshed main (owner claim) | Exact current frame/splits binding, current native scoring and metadata comparison | Holds for saved predictions and qualification tied to those identical inputs. No new fit was claimed. This is score reproduction, not an independent refit or proof that recorded early-stopping rounds are optimal | EV-7/8 |
| “Final scientific review ... approved inclusion ... no check warnings” (comments/record) | Read preserved exact native approval and application integrity; inspect new checks | Holds. Original snapshot `e8d965ea135d05819d8b441e64ccddb7db7abba1f8229ca7bf2ba5218a9cecd7`, version 0; actual answer “yes”, ship and issue 6 as implemented. Fresh check has 27 checks and zero errors/warnings/info. No new mark is inferred | Principles precedence, EV-7 |
| Source clock semantics, reporting latency and planned-N availability are established | Test whether the source text and code establish these stronger claims | Untested/unverified facts; current definition expressly does not claim them. Keep approximate conditional realized-N and recorded-clock wording. Source lesson adaptation supports preserving caution, not a new demonstrated leak | USE-3/8, LEAK-10, SPLIT-9/10 |
| Historical 98.18% counter consistency, counter decreases, first-90% archive/paper mean discrepancy and deposit chronology (comments) | Check historical reports, source identity and current attribution | Not newly recomputed here. Explicitly scoped as prior full-source verification; identical source identity and unchanged transform give no new contrary evidence. Counter mechanisms and start/completion timing remain unknown | PROV-16/17, EV-7/8 |
| Exploratory formulation selection was separated from inner-only model iteration selection (comments/record/model protocol) | Inspect actual dated choices, saved inner-selection audit and current wording | Holds as provenance. November 3 audit independently checked all six inner memberships/scores. This auditor re-scored primary predictions, not early-stopping traces; already inspected outer dates remain exploratory for task selection | SPLIT-4/21, EV-7/8 |
| No leak is demonstrated by current bounded screens | Inspect fresh leak JSON and supported-input scope | Holds only for tested mechanisms. Seven-feature fitted screen omits datetime; all-column exact-copy test includes the final predictors and finds zero cross-side copies. Reduced-screen matches 0.1662% and shallow depth-3 AUROC .598622 do not establish copies of full events or a label formula. Do not copy the historical reduced-screen 0.006% into the current report | LEAK-4/16, TP-4, EV-3/8 |

No current task claim is refuted. Historical screening claims about direct fit, fraction/RMSE, dropping N, single paper split or learner-disjoint evaluation are preserved history and explicitly superseded by later measured assessments and curator decisions; they must not be presented as current constraints.

**Checksum change, exactly attributed**

The accepted historical build checksum is `v2:18d351606c00ca77ce5f6707c1d477305d0e183492e0e8d05160bf28109285bb`. The current check checksum is `v2:0dadd5dcd69f149d54157ed533c07c1a83a3495446c79d655a7c7992e99b6fda`.

I independently reconstructed both using the current frame's canonical encoding and the saved historical metadata. Historical dataset metadata equal the current definition's generated dataset metadata; saved experiment metadata plus the verified identical six arrays retain the split identity. The only task metadata difference is `special_features`, absent before and now `[]` under the current schema. Hashing with the old dict exactly reconstructs the old checksum; adding only that empty field exactly reconstructs the current checksum. This is a proven metadata representation change. Do not silently edit the stored historical checksum to match it or treat it as a scientific drift requiring another approval.

**Current precedent review**

The new register contains 4,052 entries and 21 candidate flags, none naming Duolingo. The register still does not comprehensively index MET IDs and can parse numbered text in historical panel bodies as issues; absence of a flag is not the consistency finding. I read the actual closest cases and changed rules.

| Decision or changed rule | Actual precedent and current fact comparison | Finding |
|---|---|---|
| Preserve the approved approximate conditional task | `diabetes_3`, CC October 21/26: keep approximate with the undocumented-label gap named. Duolingo's label construction itself is verified; uncertainty is practical prospective interpretation | Consistent. Approval is not proof that source timing or planned N is known. No newly demonstrated availability defect was found |
| Preserve the derived 75% event, binary identity and fallback AUROC | `cirrhosis_patient_survival_prediction`, CC October 14 and November 1: explicit retargeting, binary event, No/Yes and AUROC. `nci_aids_antiviral_screen`, CC November 2: binary framing follows established field usage | Consistent with explicit target choice and metric matching, with an essential distinction: NCI/cirrhosis do not establish an educational 75% convention. Duolingo's bounded user-directed TP-7 departure was already exposed and accepted; it is not a general amendment or a false Must pass |
| TP-7 remains an established-convention Must | Actual unchanged TP-7; November 3 independent precedent report explains the specific higher-priority user instruction selecting inclusive 75% after its convention gap was shown | Preserve the existing bounded override. No third new exception or drift is established by re-running the same approved choice. Do not relabel it as a Should exception or reopen merely because the native snapshot changes |
| MET-4/5/11 changes: source standing, unique tuning criteria and context origin | New `open_soil_spectral_library` case deliberately tunes on log1p RMSE; `protein_model_quality_rf_pcp`/`huesken_sirna_efficacy` score within-group ranking; Imperial College challenge allows an overruled source metric | No opposite like-for-like case. Duolingo is a changed binary session event, not the paper's fraction target or candidate ranking within genes/proteins. Existing explicit fallback reason satisfies amended MET-11; it names the quantitative original and why it does not score this event |
| MET-13 stability tightened November 5 | New metric-library edge-case rule | Current binary AUROC passes finite constant/tied predictions, row-order permutation and invalid-prediction tests. No custom metric repair or new choice needed |
| SPLIT-9/10 now distinguish row-linked future labels from shared-code drift | `lt_vehicle_loan_default_prediction` November 5: no recurring borrower, fixed horizon and measured shared-code effect, gap 0. `alfa_battle_2_0_task_2`: own-client later-set labels filtered | Neither fact pattern demonstrates a Duolingo defect or requests changing its already-approved one-day gap. Duolingo source has recorded prior histories and realized session counts, not a retrospectively assigned borrower default label. Keep timing uncertainty explicit; do not claim a proven label-delay bound |
| SPLIT-14 now explicitly requires each window's own train side | Fresh arrays and full-source train counts | Consistent: three distinct training sides with earlier eligible histories; no frozen single model/train side across windows |
| CLEAN-12/14/25 now decode meaningful codes and preserve counts | Source lexical tags, exact counts, actual unordered No/Yes target; `bank_marketing` counts remain numerical | Consistent. Lexical morphological tags have no ordinal severity interpretation; the dtype heuristic flag is answered, not escalated into a new vote. No numeric rating or censored count was introduced |
| LEAK-9/10/13/39/40 changes: test-block exploitation, window aggregates, class-specific formats and fills | Current definition computes no whole-table covariate transform or class-specific fill; exact frame retained; current leak screen and separate task gamer attack | No new demonstrated contrary mechanism. Conditional realized N remains an explicitly accepted practical limitation; an old acceptance is not a license to conceal a newly proven leak. Task-gamer outcomes are for the separate reviewer/mediator, not pre-certified here |
| Newer curator choice replaces earlier fraction/RMSE or learner-disjoint decisions | Actual Duolingo dated CCs and exact November 3 inclusion | Consistent application of newer explicit decisions, not silent drift. Historical builds/results remain evidence, and newly authored human marks are prohibited |

No real departure without a distinguishing fact, higher-ranked new violation, or third comparable new exception was identified. No reflection prompt is warranted on this evidence. If the ongoing task-gamer or fresh task probe produces a demonstrable new validity issue, the mediator should assess that new evidence; neither a changed checksum nor a regenerated review identity is such an issue.

Primary source reread: [Settles and Meeder 2016, sections 3.3 and 4.1](https://aclanthology.org/P16-1174.pdf), and [publisher evaluation code](https://raw.githubusercontent.com/duolingo/halflife-regression/master/evaluation.r). The paper's deployed strength-display/ranking metrics concern its original quantitative output; the new event remains clearly a curator-designed performance goal. Its copyright/publication and deposit metadata are not a release authorization.

**Addendum: demonstrated successor-counter attack (new evidence, November 5)**

This addendum supersedes the opening **no new decision** conclusion only for the newly demonstrated test-block exposure below. The label, source integrity, exact frame/split identity, score reproduction, checksum explanation and previously settled scientific choices still hold. The earlier audit explicitly left the participant attack pending; its bounded seven-feature leak screens did not test this cross-row recurrence. A new human decision is now needed for issue 7's evaluation constraint or material feature removal. This reviewer changes no canonical file, acceptance mark or scientific setting.

**Mechanism and evidential status**

Read `successor_refutation.py` and `successor-refutation.json`, the owner's independent replication of the participant attack. For each fold, the code first strips the target and works only with that fold's 111,111 test rows. It matches the same learning language, interface language and lexical tag, with

```
t_next - delta_next = t_current
history_seen_next = history_seen_current + session_seen_current
K_inferred = history_correct_next - history_correct_current
```

It requires `t_next > t_current`, feasible `0 <= K_inferred <= session_seen_current`, and agreement of the inclusive-75% label among all feasible candidates for a current row. `actual_y` is attached after matching for measurement; neither actual labels nor source learner IDs nor excluded source correct counts enter the match, feasibility or accepted-prediction rule. The predictor then replaces the frozen approved honest model's probabilities only for accepted rows. Looking at the code confirms that no test label enters the matching or candidate-agreement decision. The supplied independent replication tests the actual shipped folds, not a hypothetical whole-source join.

| Fold (test date) | Reconstructed rows / 111,111 | Coverage | Correct inferred event labels | AUROC: frozen to attacked | Log loss: frozen to attacked |
|---|---:|---:|---:|---:|---:|
| 0 (March 12) | 5,759 | 5.1831% | 5,758 / 5,759 (99.9826%) | 0.662491 to 0.697404 (+0.034913) | 0.372437 to 0.352741 (-0.019696) |
| 1 (March 11) | 3,687 | 3.3183% | 3,687 / 3,687 (100%) | 0.662434 to 0.683475 (+0.021041) | 0.373293 to 0.361263 (-0.012030) |
| 2 (March 10) | 3,978 | 3.5802% | 3,977 / 3,978 (99.9749%) | 0.666342 to 0.690257 (+0.023915) | 0.371544 to 0.357934 (-0.013610) |

These figures and code inspection are strong evidence of the stated future-counter mechanism (EV-1/2/6); near-perfect classification on the linked subset and a gain over the frozen honest predictions distinguish it from ordinary recurrence or an imbalanced constant predictor. They do not establish every source learner match as correct or every counter as continuous: there are two wrong reconstructed event labels across the accepted rows, and ambiguous/infeasible candidates are excluded. A curator need not decide whether unknown counter anomalies are harmless to acknowledge this separately demonstrated evaluation shortcut.

**What this changes, and what remains settled**

The previously accepted 98.18% counter continuity and occasional decreases concerned whether source prior histories were perfectly consistent and whether they proved a current-row outcome leak. At each row's own prediction point, the preceding history remains legitimate under USE-6/10 and **LEAK-34 (Must)**. The new attack instead takes the next row's later history and reads the earlier outcome backward. Its future timestamps are measured, and its gain is measured. Calling it merely an accepted uncertainty would erase the newly demonstrated mechanism; calling every history value an intrinsic current-row leak would erase the prediction point.

The current claim “no current correct count or fraction remains as a predictor” remains literally true **within one row**. A stronger implied claim that unrestricted access to the complete test covariate block cannot disclose a row's outcome is **refuted**. The present definition does not yet state the row-access restriction needed to justify the honest row-wise evaluation. The accepted source-clock and realized-N approximations do not authorize later rows, and the one-day training gap cannot remove a successor inside the same test day. Repeating target, 75% cutoff, numerical N, equal records, dates, caps, learner recurrence or the existing gap question would not decide this mechanism.

**Current rules and closest precedents**

**LEAK-9 (Should, amended November 5)** directly addresses an evaluation leak where a model reads other test rows. It permits repair in scoring or by a protocol line the benchmark checks, instead of deleting otherwise legitimate row features. The closest actual precedent is `medical_facility_operational_data`, CC November 5, issue 7 A: future arrivals' queue features decode the current waiting-time outcome and lower MAE from 13.85 to 6.83 across all nine windows. The curator preserved the history fields with a no-other-test-row protocol and a benchmark-side model check. That mechanism is directly comparable: later rows carry realized outcome increments in otherwise legitimate histories. `sepsis_prediction`, CC October 1, similarly preserves each hour's measurements but requires causal predictions because future stay rows/record length expose the outcome. These precedents support keeping Duolingo's own-row prior counters **with a concrete evaluation restriction**, rather than rejecting the source.

The current amended LEAK-9 allows a benchmark-checked protocol line; it does not require this reviewer to invent a new scorer or certify an enforcement system that has not been demonstrated. Nor does it permit merely calling future-context cheating “out of scope” without stating the contract and how methods will be checked. **USE-3, LEAK-1/10** still forbid future information at the prediction point; **LEAK-34** does not extend its protection from past to future. **LEAK-38** is not the applicable kept-uncertainty rule: the future dates and counter mechanism are measured. **SPLIT-9** concerns unavailable training labels; here the exploit can run entirely within the test block, so increasing the train/test gap is not the demonstrated remedy. **EV-7** requires preserving the fact that honest row-wise model scores reproduce while the unrestricted participant kit permits a stronger illicit calculation.

**Repair choices for an actual curator decision**

| Choice | What it concretely fixes | Cost, validation and limits | Consistency |
|---|---|---|---|
| Preserve the eight approved predictors and require causal/row-independent prediction | Prevent the observed backward read by disallowing later test covariates when predicting an earlier row. A simple explicit contract is `prediction_i = f(training data, x_i)`, with no other test-row inputs, no fitting to the test block and no test labels. The cumulative prior histories already supplied in `x_i` stay valid | Preserve exact data and honest qualification; state the prediction point and restriction in maintained dataset/protocol notes. The benchmark must check the admitted methods for test-context use or enforce per-row access. This report has not verified such benchmark enforcement. A broader causal contract that permits earlier covariates must still prohibit later ones and test labels; it needs its own explicit check, not an assumption from sorted rows | Follows LEAK-9 and the directly comparable medical-facility/sepsis precedents; LEAK-34 protects legitimate histories |
| Drop `history_correct` and requalify the resulting seven-predictor dataset | Removes the correct-count increment used to recover K in the demonstrated attack. Without the two `history_correct` values, the exact numerator-difference identity cannot be computed from that formula | Material loss of genuine prior-success signal. Changes feature set and potentially content-based ordering/sampling, so regenerate/check the exact frame/splits and rerun affected baselines, fits and probes, including the participant attack. No residual equivalent exploit from the retained columns has been demonstrated here; do not reject this choice merely by speculating about other future information | A concrete data remedy under LEAK-7, though more destructive of approved legitimate signal than the LEAK-9 protocol remedy. It does not follow automatically from the old approval |

Recommendation: present both choices in issue 7, with **preserve histories plus an explicit benchmark-checked no-future-test-row contract** as the closest-precedent recommendation. If the curator wants protection against this measured exploit through the released columns themselves, or cannot accept the benchmark protocol obligation, dropping `history_correct` is a concrete alternative to qualify. Do not describe that drop as proven inadequate without a distinct retained-column exploit and measured evidence. Conversely, do not mark it qualified merely because the one observed formula is broken; run the affected qualification on the actual seven-feature package before accepting/building it.

A note saying that the attack is measured but allowing unrestricted future test context is not a repair for this prediction point. The next decision concerns which remedy to carry, not whether to erase the previously accepted scientific formulation. Apply no material feature deletion, changed evaluation guarantee, revised human mark or final build from this addendum alone. Preserve the original November 3 approval on its actual identity and record the new issue/decision separately.

</details>

<details><summary>Column and split audit</summary>

**Focused Duolingo column and split audit**

Verdict: retain the current definition and split, with the already accepted approximate-task limitations. New corrective findings: 0. No new human decision is requested by this audit.

This is an independent column/split contribution to the focused add-dataset recheck on 2026-11-05. It does not replace the claim, task-gamer, mediator or editor reviews. No canonical files were edited and no models were fitted. The definition is `datasets/_dev/tabarena-v0pt2/duolingo_spaced_repetition_recall_1m_clf/dataset.py`, SHA256 `10e6c681a128763a081ad3ed086f5f54a21b60d77fd7b74d211b382cd1a1a06f`, on the supplied `9048f36a` base.

I read current column-auditor/split-auditor instructions and the applicable knowledge on principles, use cases, leakage, splits, cleaning/dtypes, evidence and checks/probes. The current November 5 amendments to LEAK-9, LEAK-38 and SPLIT-9/10/14 were considered. They do not establish a previously unverified clock or delay bound. The explicit November 3 curator approval remains the authority for this task's inclusive 75% criterion, numerical N, equal record weights, temporal-only evaluation and approximate fit. CLEAN-17/TP-7's usual established-convention requirement is not reasserted as a new unanswered decision: this particular curator-selected event is explicitly authorized and accurately described as such.

**Columns and meaning**

Meanings were checked against the publisher's [data-format README](https://github.com/duolingo/halflife-regression#data-set-and-format), accessed November 5. Its descriptions of prior counters explicitly say "prior to this lesson/practice". The [paper](https://aclanthology.org/P16-1174.pdf), section 3.4 and Table 1, separately describes interaction history and lexical features. Section 2.1 describes within-session learning/feedback; section 4.1 uses historical logs. Neither establishes preassigned exercise counts or the archive's label-arrival bound.

| Column | Meaning | Known at prediction? | Observed dtype / cleaning | Verdict / rules |
|---|---|---|---|---|
| `timestamp` | Recorded session clock | Recorded-clock approximation; start/completion unverified | `datetime64[ns]`, Unix seconds converted before sorting; no coarsening | Retain with accepted timing limit; USE-8, LEAK-10, CLEAN-14/23 |
| `delta` | Seconds since previous practice of the word | Prior interval under recorded-clock assumption | `int64`; positive, not an ordinal code | Retain; USE-6, LEAK-34, CLEAN-14 |
| `learning_language` | Studied language | Context | Unordered category, 6 observed levels | Retain nominal category; CLEAN-14 |
| `ui_language` | Interface language | Context | Unordered category, 4 observed levels | Retain nominal category; CLEAN-14 |
| `lexeme_string` | Lexical/morphological tag | Exercise context | Unordered category, 13,803 observed levels | Retain; not prose or an ordinal scale; CLEAN-14, EV-3 |
| `history_seen` | Prior exposure count | Source describes prior history; imperfect continuity remains known | `int64`; quantity, not a code | Retain with accepted source-counter limit; LEAK-34, CLEAN-11/14 |
| `history_correct` | Prior correct-answer count | Same evidence and limitation as prior exposure | `int64`; never exceeds `history_seen` in the frame | Retain; LEAK-34, CLEAN-11/14 |
| `session_seen` | Realized session exercise count N | Not demonstrated preassigned; supplied conditioning variable in accepted contract | `int64`, observed 1-20; actual count, no documented open-ended top-code | Retain numerical N with accepted conditional-task limitation; USE-8, CLEAN-14 |
| `session_accuracy_at_least_75` | Inclusive event `4*K >= 3*N` | Outcome, never predictor | Unordered categorical `No`/`Yes`; Yes is the event | Correct target representation; CLEAN-25, LEAK-4 |

The current dtype probe was executed independently on the current frame through `dataset_io.from_definition`, using a supplied saved split plan. It flagged only `lexeme_string: ordinal_like` (19 levels match scale-like vocabulary). The publisher defines structured word tags, and there is no source ordering through these tags. This is a lexical false positive, resolved by meaning; an ordered category would invent an order. The four numerical predictors are counts or elapsed seconds, with no scale-code, binary-flag or open-end evidence requiring recoding. The timestamp is correctly datetime. All nine columns are typed, all cells are present, and there are no untyped object columns.

The excluded source fields are handled correctly: learner identity and opaque lexeme ID are not predictors; current `session_correct` and `p_recall` are outcome ingredients and are removed. Deduplication is identity-aware and precedes target coarsening. No fitted aggregate, imputation, whole-table scaling or learned feature is introduced by `_clean` (LEAK-10, LEAK-29, CLEAN-6/7). The current label comes from integer comparison, including exact 75%; no outcome class is filtered out.

**Exact split audit**

The saved current frame has 1,429,456 rows, eight predictors and one binary target. It is sorted by actual timestamp with a RangeIndex. All six actual split arrays were checked for bounds, uniqueness, within-window disjointness, exact requested sizes and timestamp eligibility. Their union uses every stored row. The three training arrays differ, satisfying the updated SPLIT-14 requirement for distinct earlier-history refits.

| Test day (2013) | Train rows | Test rows | Latest train timestamp | Earliest / latest test timestamp | Test Yes / No |
|---|---:|---:|---|---|---:|
| March 12 | 1,000,000 | 111,111 | March 10 23:59:58 | March 12 00:00:01 / 16:14:57 | 96,331 / 14,780 |
| March 11 | 1,000,000 | 111,111 | March 9 23:59:57 | March 11 00:00:04 / 23:59:59 | 96,276 / 14,835 |
| March 10 | 1,000,000 | 111,111 | March 8 23:59:59 | March 10 00:00:00 / 23:59:58 | 96,305 / 14,806 |

Every training clock is strictly before midnight one day before its test window, and every test clock is within the intended calendar day. The sampled train/test proportion is 90.000009% / 9.999991%. Both classes occur in every train and test side. The newest day is partial, as documented; these results do not turn it into a complete daily window.

I independently streamed all 12,854,226 source records and counted full-source training eligibility before the sampling caps: 11,116,716 / 10,067,162 / 9,101,090 rows for the newest-to-oldest windows. Even conservatively placing all 81 previously established source copies on each train side, the post-dedup training shares are at least 86.4829% / 78.3178% / 70.8021%. Thus the oldest window comfortably meets the 50% history floor; the 1M cap does not redefine eligibility (SPLIT-14). Current code constructs expanding calendar windows on full-source history and only then samples/reduces the union.

The regime matches the approved known-learner practice-stream application (USE-10, SPLIT-1/3/13, LEAK-34). Learner recurrence is allowed; no learner reservation is declared. The old learner-temporal-review group-probe output was inspected only as historical evidence: it used another regression framing and mixed learner/date restrictions, so its scores are not evidence requiring a cold-start split here. No alternative model split was run because this recheck found no contradiction in the selected regime.

**Executed checks and remaining limits**

The independent numerical check completed successfully. The measured results and their scope are reported below.

Checks included: current `dataset_io` metadata/feature interpretation; independent current dtype probe; exact pandas comparison of every frame value, dtype, category and index against approved prior `binary75-final/frame.parquet`; exact comparison of all six split arrays; split and class counts/bounds/gap/coverage; raw compressed-file SHA256; full-source denominator positivity, valid current correct counts, fraction/count agreement and history-correct <= history-seen; source eligible-history counts. There are 169,363 exact-75% source rows. The raw SHA256 still matches `26cf9b33f2e9b2e8aa9a8f262a017b30699ca2f625c56a12ce699d4ea7076873`; current frame SHA256 from the parent manifest is `b6f104eed4cddf621d169771c84bf61e3cdb2380dd797014e9160433dcf0d596`.

The parent's current native check reports 0 errors, 0 warnings, 27 passed checks; I inspected that artifact but did not rerun `dataset check`, which would rewrite its README. Fresh leak/task models belong to the parent's probe run; no fresh fitted scores are claimed here. Prior original-label and shallow-rule evidence remains applicable only with the independently verified exact frame/split identities, and is not relabeled as a newly fitted experiment.

Cannot verify: planned rather than realized N; session start/completion semantics; exact label-arrival delay; causes of the historical counter discontinuities; seasonal or modern-population generalization. The one-day gap is an accepted approximation, not proof all labels arrived before each refit. Stable test class shares cannot prove absence of censoring. The formulation was selected after exploratory outer-window inspection, so those dates are not a pristine confirmatory task-selection test. Current rules do not erase these accepted limitations, and no newly contradictory evidence was found.


</details>

<details><summary>Participant attack</summary>

**Independent participant attack report**

One confirmed finding: later held-out rows reveal earlier held-out outcomes through cumulative correct-answer counts. No test labels or public target lookup are used to construct this attack.

**Scope and baseline**

Only `task.md`, `task.json`, `data.parquet`, `splits.parquet`, the supplied scoring implementation, and the public source below informed the analysis. All authored scripts and outputs are in `work/`. No parent/project rules, curation notes, other datasets or outside code repositories were inspected. The initial LightGBM import emitted a default matplotlib configuration-path warning and created an incidental temporary cache outside the kit; no outside task/project contents were exposed. Subsequent runs place that cache in `mpl`.

All three shipped temporal splits were tested. For each, seed 481 fixes 100,000 sampled training rows and 50,000 sampled test rows. Every comparison uses those exact same rows; saved sample indices permit replay. Models are untuned LightGBM classifiers: 200 trees, 31 leaves, learning rate 0.05, seed 481, two threads. The honest baseline uses all supplied features, converts timestamp to seconds, and preserves categorical features. A stronger honest comparator adds prior accuracy, prior incorrect count, log delta, hour and weekday. These are legitimate predictors available at the stated prediction point. AUROC is computed through `score.py` using original class labels.

**Confirmed finding: successor history reconstructs current correctness**

For current row i and candidate later row j, match identical learning language, UI language and lexeme string, require:

- `timestamp_j - delta_j == timestamp_i`;
- `history_seen_j == history_seen_i + session_seen_i`;
- `timestamp_j > timestamp_i`;
- `K = history_correct_j - history_correct_i` lies between zero and `session_seen_i`.

Retain a row only when exactly one candidate survives these feature-only constraints. Reject ambiguity before reading any target labels. The inferred outcome is `4*K >= 3*session_seen_i`. Future covariates reveal K after the current session has finished, which is unavailable when its correct-answer count has not been observed. No user ID is needed. The [official data dictionary](https://github.com/duolingo/halflife-regression#data-set-and-format) describes delta as elapsed time from prior practice, the history counters as totals before current practice, and session counts as current-practice totals. This supports the reconstruction interpretation; the source was consulted for definitions only.

There are 76,093 uniquely linked rows across the complete table; reconstruction agrees with their labels on 99.982916% (13 errors). Labels are used here only to evaluate an already fixed reconstruction. To eliminate any dependence on excluded or later test windows, the main result below restricts j to the same shipped test window as i. On linked rows replace the honest engineered prediction with 0.999999 or 0.000001 according to inferred outcome; retain original model predictions elsewhere.

| Split | Honest AUC | Engineered honest AUC | Same-test successor attack AUC | Gain vs engineered | Paired bootstrap 95% interval | Linked evaluated test rows | Reconstruction accuracy |
|---|---:|---:|---:|---:|---|---:|---:|
| r0f0 | 0.630206 | 0.640320 | 0.676321 | +0.036001 | [0.033453, 0.038432] | 2,616 (5.232%) | 99.961774% |
| r1f0 | 0.626041 | 0.639688 | 0.662766 | +0.023078 | [0.021549, 0.025202] | 1,654 (3.308%) | 100.000000% |
| r2f0 | 0.630069 | 0.645489 | 0.670845 | +0.025357 | [0.023221, 0.027261] | 1,762 (3.524%) | 99.943246% |

The same-test attack gains versus the raw honest baseline are 0.046115, 0.036725 and 0.040777 respectively. Allowing successor covariates anywhere in the supplied table gives engineered-attack AUROCs 0.676321, 0.668139 and 0.677388. Thus same-test access alone establishes the finding. No successor is in the current split's training set. The gain is conditional on bulk access to future covariates; this attack is unavailable with strictly chronological per-row inference. The row bootstrap (100 replicates for the main comparison) does not account for latent user/session dependence, but the positive effect repeats in all three shipped windows.

**Other tested hypotheses**

- **Row order / IDs:** no ID columns are shipped. Timestamps are globally nondecreasing. Adding row position changes raw-baseline AUC by +0.000626, +0.001246 and -0.000233. Only the second row-bootstrap interval excludes zero. This does not establish an outcome side channel beyond supplied time.
- **Exact cross-side copies:** zero full-feature duplicates between train and evaluated test rows. Omitting timestamp produces 81, 91 and 79 matches to full training sets. Training-label mean lookup on these descriptors changes AUC by -0.000186, +0.000083 and -0.000346; all bootstrap intervals include zero. No demonstrated duplicate exploit.
- **Formats / sentinels:** generic lexeme markers, noun/verb markers, lexeme length and extreme delta flag change AUC by -0.000326, -0.000088 and +0.000682; all intervals include zero. No missing cells or impossible `history_correct > history_seen` records. Extremely long delta occurs in about 0.0096% of rows and has univariate test AUC approximately 0.5. Lexeme morphology itself is legitimate signal.
- **Inferred entities / nearest neighbors:** matching past training predecessors and blending their known label reduced all three honest AUROCs. A fixed ten-neighbor training-only comparator within language/UI/lexeme, using log prior counts, log delta, prior accuracy and exercise count, also reduced AUROC (0.622354, 0.617050, 0.621594). The confirmed attack uses future counters, rather than merely a strong nearest-neighbor predictor.
- **Training rows' futures:** 5,384, 5,518 and 5,670 sampled training rows have a unique successor in the full table. Their later records were not used as extra training labels. Temporal cutoffs have no shared training/test timestamps. The actionable issue remains held-out future counters.
- **Test statistics:** full-table lexeme frequency and same-timestamp cohort counts, added to honest engineering, gain +0.001060, +0.003264 and +0.002976. The first bootstrap interval crosses zero; the latter two do not. These combined covariates have not been isolated against a comparable causal frequency/session-context control, so deployment unavailability and mechanism are unresolved. They are not ranked as a second confirmed exploit.
- **Direct post-outcome inputs:** no `session_correct` or recall proportion is supplied. Historical counts are legitimate for the current row, and `session_seen` is explicitly conditioned on by the task. Their legitimate predictive strength is not itself a defect. The demonstrated violation is looking ahead to the next row's historical count.

**Bounded repair comparison**

Removing `history_correct` from every row prevents the demonstrated exact K-difference formula. This is a measured comparison only, not a task change or a claim that every possible future-information route is closed. For the engineered comparator, also remove prior accuracy and prior incorrect count because both derive from the removed column. All other training settings and sampled rows remain identical.

| Split | Raw model without history_correct AUC | Drop vs raw honest | Engineered model without history_correct AUC | Drop vs engineered honest |
|---|---:|---:|---:|---:|
| r0f0 | 0.622522 | 0.007683 | 0.624932 | 0.015388 |
| r1f0 | 0.612924 | 0.013117 | 0.616506 | 0.023182 |
| r2f0 | 0.622842 | 0.007227 | 0.622783 | 0.022706 |

**Evidence and replay**

Run `run_attacks.py`, then `additional_checks.py`, then `repair_comparison.py` from the kit using the supplied interpreter. All cap compute threads at two. `write_report.py` creates this report. Evidence: `scores.csv`, `evidence.json`, `additional_evidence.json`, `repair_and_noise_evidence.json`; link audit: `future_links.parquet`; exact samples and all predictions: `r*f0_samples.npz` and `r*f0_predictions.parquet`. Logs retain execution outcomes. Bootstrap intervals are exploratory conditional uncertainty checks, not population-level guarantees. More extensive tuning, hidden user identities and production inference plumbing were not checked.

The fixed r0f0 honest model is batch invariant in a direct implementation check: all 50,000 test predictions are identical between whole-batch and 1,000-row chunks; the first 100 are also identical under one-row inference (maximum absolute difference zero). See `batch_invariance.py` and `batch_invariance.json`. This establishes the property for this supplied-feature honest implementation, without auditing general benchmark submission enforcement.

</details>

<details><summary>Independent successor refutation</summary>

**Independent successor-row attack refutation**

The same-test-only successor attack replicates. It is a material new evaluation finding: later test covariates reconstruct the earlier binary outcome with 99.97-100% observed label precision on 3.32-5.18% of each full test window, and improve a frozen honest classifier on all three actual splits. The accepted imperfections in source-counter continuity do not cover or refute this future-information channel.

This report supplements and narrows the earlier `column-split-audit.md` conclusion of no newly identified corrective concerns. That audit validated individual column meaning and actual split integrity; it did not test joint access to later test rows. The new evidence does not establish that a row's own prior counter contains its own current outcome. It establishes that a later row's prior counter can disclose an earlier row's outcome to a method permitted to inspect the whole test block.

**Independent test**

Executed `successor_refutation.py`, exit 0; full results are in `successor-refutation.json` beside this report. The script is independently authored and did not read the participant attack implementation. It reads only the current saved frame/six split arrays and frozen previously qualified predictions; matching uses each actual 111,111-row test array alone. No row from another split, outside the test window or after its end is used. Learner identity, source correct counts and source fractions are unavailable to the attack.

For current row c, find later row n in the same test array such that:

1. Course, interface language and lexical tag agree.
2. `timestamp_n - delta_n == timestamp_c` exactly.
3. `history_seen_n == history_seen_c + session_seen_c`.
4. `K_inferred = history_correct_n - history_correct_c` is between zero and the current N.

Infer the event by `4*K_inferred >= 3*N_current`. A row is attacked only when every feasible matching successor agrees on this label; inconsistent candidate labels are rejected. None of these selection or inference steps reads a test label. Actual labels are used only afterward to assess precision and scores. No model is trained or tuned for this test.

| Actual fold / test day | Test rows | Accepted recoveries | Coverage | Correct labels | Label precision | Ambiguous-label rows excluded |
|---|---:|---:|---:|---:|---:|---:|
| 0 / March 12 | 111,111 | 5,759 | 5.1831% | 5,758 | 99.9826% | 1 |
| 1 / March 11 | 111,111 | 3,687 | 3.3183% | 3,687 | 100% | 0 |
| 2 / March 10 | 111,111 | 3,978 | 3.5802% | 3,977 | 99.9749% | 0 |

There are 5,761 / 3,688 / 3,979 candidate pairs before feasibility filtering. One pair in each of folds 1 and 2 implies an impossible K and is excluded. Fold 0 has exactly one current row with two candidate successors, differing both in inferred K and label; it is excluded. All accepted rows therefore have a unique candidate. Covered true negative counts are 817 / 485 / 576 and true positive counts 4,942 / 3,202 / 3,402; this is not simply predicting the majority class. There is one erroneous recovered label in folds 0 and 2, respectively, and none in fold 1.

This refutes the proposed defenses that the effect needs cross-fold data, post-window data, a learner ID, a test-label match, materially ambiguous keys, or perfect continuity across all source rows. None is needed. It does not prove exact recovery of source K on every match; binary outcome precision is what was assessed.

**Measured gain**

The control is the saved approved `classifier_with_n` prediction vector, whose current-frame and six-array identity was independently verified in the first audit. Unattacked probabilities remain byte-for-byte the same; attacked rows are replaced by their inferred 0/1 event. No fit or tuning is claimed. The prior-only version uses the current fold's training event rate elsewhere.

| Fold | Frozen honest AUROC | With successor attack | AUROC gain | Honest log loss | With attack |
|---|---:|---:|---:|---:|---:|
| 0 | 0.662491 | 0.697404 | +0.034913 | 0.372437 | 0.352741 |
| 1 | 0.662434 | 0.683475 | +0.021041 | 0.373293 | 0.361263 |
| 2 | 0.666342 | 0.690257 | +0.023915 | 0.371544 | 0.357934 |

Mean AUROC gain is about +0.026623. Even a model using only a training-prior constant plus this attack reaches AUROC 0.551862 / 0.532432 / 0.536417, against 0.5 for the constant. No confidence interval or broad model comparison is claimed by this independent check. Parent/participant confidence estimates, if reported, are separate evidence.

**Timing and remedies**

All accepted successors have a strictly later recorded timestamp than the row being scored. At that earlier row's prediction point, its later successor record has not yet happened. The publisher [data-format documentation](https://github.com/duolingo/halflife-regression#data-set-and-format) defines the counters as prior to each row's own session and delta as time since preceding practice. These semantics permit the demonstrated recurrence. The unknown start/completion meaning and reporting latency remain unknown; neither makes later-session information prospectively available for an earlier session. A one-day train/test gap cannot stop information moving backward between rows within one test window.

This mechanism falls under current **LEAK-9** (November 5 amendment): evaluation leakage when a method can read other test rows, with causal per-entity prediction/scoring or an enforced benchmark protocol as the remedy. **USE-10 / LEAK-34** still support a row's own legitimate practice history. It should not be framed as newly proving current-row `history_correct` is a post-outcome feature.

The mildest remedy is an explicit, enforceable causal inference contract: score each row using the training data and its own available covariates, or allow only previously arrived records under a defined sequential protocol. Deny every row access to later test covariates, test-fitted transformations, order statistics or aggregate state derived from those later records. Rows sharing a clock should also be handled conservatively because within-clock arrival order is unverified. A held-back streaming/per-row evaluator could enforce this; a written line requires the benchmark to actually check compliant methods, as LEAK-9 specifies. This audit has not verified that the downstream evaluator enforces it.

Dropping `history_correct` blocks this particular exact K subtraction, but removes genuine historical signal as well. It is a more destructive dataset change than enforcing causal evaluation and would require requalification of the changed feature set. It is not established as a complete solution to every future-block mechanism. Neither a new learner holdout nor wider train/test gap addresses this same-window route directly. These are analytical remedy comparisons, not a curator approval or an implemented change.

The previously accepted target, numerical realized N, equal records, history anomalies, temporal windows and exploratory formulation-selection limits remain as documented. This new test warrants a concrete evaluation-protocol follow-through; it does not authorize silent source/feature/split edits or a fresh semantic inclusion decision by this auditor.

</details>

<details><summary>Review editor</summary>

**Focused Duolingo cold editor review**

Ready for the curator after the three concrete corrections below. No further semantic issue or new human decision is identified. This is the focused review-editor role; canonical source and human marks were not modified.

I read the current editor role, writing, principles and review-file procedures, then read REVIEW.md cold. I checked its claims against dataset.py, generated README.md, the curation record and the affected BENCHMARK_CHANGES_TODO entry. The README was awaiting final regeneration during the initial inspection; the owner's later final native-check result is separate evidence, not a check executed by this editor.

**Concrete edits**

1. **Make the panel badge a recommendation.** Old: `**Review panel:** focused current-main recheck: independent claim/precedent audit, column/split audit, participant attack, independent successor refutation, mediator and editor.` New: `**Review panel:** ship after the routine protocol correction, now applied (mediator). Focused current-main recheck: independent claim/precedent audit, column/split audit, participant attack, independent successor refutation, mediator and editor.` The page takes the first sentence as the recommendation; the initial sentence was only the tier and role inventory. Keep benchmark enforcement explicitly pending in the remainder.

2. **Normalize the embedded reports to the review format.** Old examples: `# Focused Duolingo mediator judgment`, `## Changes to make now`, `### Mechanism and evidential status`. New examples: `**Focused Duolingo mediator judgment**`, `**Changes to make now**`, `**Mechanism and evidential status**`. Apply this to every report heading after the single dataset title. The current review format prohibits Markdown headings inside the panel; preserve the complete substantive reports and their disagreements while changing heading syntax.

3. **Scope the initial checksum analysis before the protocol correction.** Old unqualified opening in the claim report: `The changed container checksum is entirely a current-schema metadata change, not a changed task.` Preserve that authentic report, but precede it with: `Report scope: the opening audit and its checksum comparison describe the initial current-main refresh before the successor-counter protocol correction. At that stage, the sole task-metadata change was the empty special_features field. The final definition additionally changes protocol text; its current checksum is established by the later final regeneration/build, not by this initial comparison. The addendum records the later attack finding and the auditor's recommendation; the mediator explains the final resolution of that disagreement.` This avoids presenting the initial 0dadd checksum or schema-only explanation as the identity of the final protocol-bearing package. The record already scopes this correctly as the initial framework-only checksum change.

**Scientific and evidence assessment**

The task is intelligible without the earlier chat: predict the probability of the inclusive 75% session-performance event, conditioned on numerical realized N and legitimate prior/context inputs, with equal record weights and the retained temporal windows. It distinguishes that output from expected fraction correct and from source-defined mastery. The full record retains the reason for choosing the coarser performance summary and the fact that regression was not invalidated. Realized rather than proven planned N, uncertain start/completion and label arrival, imperfect historical counters, short 2013 coverage and exploratory formulation selection remain visible limitations.

The new finding is concrete and distinct from the accepted source-counter imperfections. Feature-only matching to a later row in the same test window reconstructs earlier outcomes. Full-window recovery of 3.32-5.18% at 99.97-100% precision and frozen-model AUROC gains of 0.0210-0.0349 are separated from the participant's newly fitted 100k/50k controls and their bootstrap intervals. Exact-data/split verification supports reuse of the approved model predictions; it is not called a new model fit. The initial bounded screens are not allowed to overrule the later independent attack replication.

The report preserves the claim auditor's proposed need for human choice and the mediator's contrary policy resolution. Current LEAK-9 and directly matching precedents support the routine train-only, own-row evaluation contract while retaining genuine history. Issue 7 closes as an AI-owned protocol correction, without attributing a new acceptance, exception or amendment to the curator. The original issue-6 inclusion and mark identity remain historical. No repeated semantic gate is needed for unchanged scientific choices.

The definition and TODO distinguish an applied documentary protocol from future benchmark method checking. Frozen fitting and own-row predictions exclude the demonstrated future-counter route; a dataset check/build does not establish downstream enforcement. The measured batch-invariance example concerns only its tested honest implementation. Neither feature deletion nor a wider gap is misrepresented as an executed or comprehensive repair.

No exposed credential or absolute host-local path was found in the inspected public review. Public source references, current-versus-historical numerical evidence and the closed issue numbering remain intelligible. No additional stylistic or speculative finding is raised.

**Review scope**

This was read-only inspection of the reviewed checkout and supplied evidence; no new models were fitted. The review relies on the explicitly observed source identities and numerical artifacts.


**Application (AI, 2026-11-05):** All three requested format and evidence-scope repairs are applied. The current native collector and page builder pass with both issues resolved; no new semantic finding is left.

</details>

<details><summary>Qualification reuse claim and precedent audit</summary>

**Focused qualification reuse claim and consistency audit**

November 6, 2026. Dataset: `duolingo_spaced_repetition_recall_1m_clf`.

Verdict: retain ship as implemented under Myunghwan's explicit current instruction to repeat the cycle using past decisions. No new scientific input is needed. This independent focused claim audit found zero new corrective findings. It does not constitute a fresh full panel, a new model fit, a new participant attack, or downstream benchmark certification.

Validity: retain the approved approximate conditional session-performance task and temporal holdouts. The documented same-test successor attack remains a demonstrated evaluation leak under LEAK-9; the implemented training-only, own-row protocol and benchmark TODO remain necessary. Value: all twelve saved model/baseline AUROCs independently reproduce on the identical current data and exact test indices. Quality: no changed scientific recipe or feature handling was found. For the curator: no new choice; all earlier limitations and required downstream method checking remain.

**Executed independent checks**

I read the installed add/review procedures, focused panel contract, both knowledge entry points, principles, current leak/metric/task/evidence rules, human-review adaptation, accepted record/definition/REVIEW, and the relevant November 3/5 decision and numerical evidence. I independently ran `claim_audit.py` independently; it exited 0. Full results are `claim-audit-evidence.json`.

The current isolated checkout begins at `f11991c8001517ad06e518bf1b4613a2cf756b46`. Its scientific source, skill and agent Git trees equal both the preserved previous checkout and reviewed source at `9048f36a1bcf7da3687fde04b18ef79cd7a1201e`. The definition remains SHA-256 `4c67e0905b680fca777f630f5cace3d65bb0ff11d41b452e1c92d66c60f9d094`. The qualification audit establishes preserved package versions and code identity. This auditor imported the identical current scientific code for its independent score check.

The newly generated 1,429,456-row frame equals the November 5 frame exactly, including index, dtypes, category values/order/codes and labels. All six train/test index arrays equal the previous arrays. The prior participant kit's full frame and all memberships also compare exactly to the new frame/arrays. Fresh frame SHA-256 is `b6f104eed4cddf621d169771c84bf61e3cdb2380dd797014e9160433dcf0d596`; source gzip SHA-256 is `26cf9b33f2e9b2e8aa9a8f262a017b30699ca2f625c56a12ce699d4ea7076873`, identical to the audited previous source. The owner-run native check reports 27 checks and zero errors, warnings or infos; its checksum `v2:c20f832bb366fbe3e87b547b5ddf83cca1c5877f6d3f4e7bd16c1d9a25b6e6e3` equals the final November 5 package. Those native-check results were read by this auditor, not rerun by this auditor.

**Claim inventory and tests**

| Claim | Source and test | Result | Rule |
|---|---|---|---|
| The task estimates the probability that a supplied-N session achieves at least 75%, preserving a session-performance purpose. | Current task summary and November 3 target-selection/inclusion CC lines; inspect actual label recipe. | Holds as the curator-selected approximate task; no source mastery claim. | USE-1/3, TP-7 |
| This event probability differs from expected fraction correct. | Current prediction/change notes and original fraction-to-event discussion; compare mathematical estimands. | Holds. No claim that AUROC recovers expected accuracy. | USE-5, MET-2 |
| One source row is a learner-word lesson/practice session; six languages and the short 2013 coverage are historical-source properties. | Unchanged source identity and prior full-source verification; current timestamp/context schema. | Reusable historical evidence; no fresh publisher lookup or new population claim. | PROV-1, EV-2/7 |
| The label includes exact 75% through `4*K >= 3*N`. | Inspect unchanged `_clean`; prior full-source count test gives zero integer/fraction comparison mismatches and 169,363 exact-75% source rows. | Holds; source-test reuse is tied to exact gzip identity. | LEAK-4, TP-7 |
| Coarsening does not filter outcomes or make the target denominator independent. | Inspect `_clean` and prior N-subgroup/label-rule evidence. | Holds; N=1,2,3 require all correct, N=4 permits 3/4. | USE-5, LEAK-4 |
| Eight predictors remain; source fraction, current correct count and opaque IDs are excluded. | Independently inspect current frame columns, recipe and types. | Holds; timestamp, delta, learning/UI language, lexical tag, prior seen/correct and session_seen only. | LEAK-10/33/34 |
| Numerical session_seen is realized rather than verified planned N. | Current source/count framing; integer dtype and observed range checked. | Holds as conditional logged-process interpretation. Planned-count availability remains unverified. | USE-3/6, EV-7 |
| Equal existing-record weights, no balancing or denominator weighting. | Unchanged definition and scorer; no scoring columns or weighting procedure. | Holds. | MET-2, CLEAN |
| The 75% criterion is curator-selected, not an established source convention. | Actual November 3 target-selection/inclusion and current reuse instruction. | Holds as task-specific user direction. TP-7's convention clause is a Must in the skill; no claim of source convention, generic exception or general amendment is made. | TP-7, instruction precedence |
| AUROC is the fallback for the changed binary event, not reproduction of paper MAE or rounded-proportion AUC. | Declared metric reason, preserved metric CC and prior source reading; independently rescore twelve saved outputs with native scorer and rank formula. | Holds; all score discrepancies below 1e-12. | MET-1/2/8/11 |
| Binary-log-loss diagnostic fitting and AUROC evaluation have different roles. | Unchanged diagnostic evidence and current training/evaluation note. | Holds; benchmark method objectives remain their own. AUROC does not certify calibration. | MET-1/2 |
| Three March 12/11/10 one-day test windows use earlier training, a one-day gap and 1M/111111 caps. | Exact six-array comparison; independently inspect per-fold clocks/support. | Holds; actual min gaps 86403, 86407 and 86401 seconds. | SPLIT-1/3/9 |
| Learners may recur; IDs are not predictors and no learner holdout is asserted. | Unchanged temporal-only recipe and actual feature inventory. | Holds; earlier grouped experiments remain historical. | USE-10, LEAK-33/34 |
| The newest day is partial and daily cadence/label-latency bounds are approximations. | Test clock range and unchanged timing notes; prior source evidence. | Holds as an explicit limit. Start/completion and reporting latency remain unverified. | USE-3, SPLIT-9, EV-7 |
| The used-row union, labels and categorical state are unchanged. | Independent exact frame/category/index and all-six-array comparisons. | Holds: 1,429,456 rows, 1,240,113 Yes and 189,343 No; no missing cells. | PROV, EV-2/8 |
| Changing a target can change actual sampled records even when positional arrays look equal. | Base shared ordering and preserved November 3 retargeting evidence. | Correct historical caution; current reuse verifies values and labels as well as positions. | EV-8, SPLIT |
| Identity-aware source-copy removal precedes label coarsening; 81 exact copies were removed in source qualification. | Unchanged recipe, source identity and previous source audit. | Reusable historical result; no new deduplication policy. | LEAK-16/19, PROV |
| Source-history continuity is imperfect without demonstrating an own-row current-outcome leak. | Previous full-source continuity test on identical raw bytes; current own-row versus successor distinction. | Reusable qualified claim. Causes and source repair remain unknown. | LEAK-10/34, EV-6/7 |
| Raw all-correct/one-exercise proportions and archive/paper mean discrepancy are disclosed. | Identical gzip and previous `claim-source-counts.json`/source audit; inspect current notes. | Reusable historical counts: 83.886% all correct and 58.937% N=1. Paper scores are not presented as reproduced archive scores. | PROV, EV-2/7 |
| The model retains useful ranking signal beyond constant and N-only controls. | Independently recompute all twelve original prediction AUROCs after exact data/split verification. | Holds for these saved diagnostics: with-N 0.662491/0.662434/0.666342; N-only 0.596707/0.597022/0.594714. No fresh fit or broad HPO claim. | TP-1/2/4, EV-8 |
| Later test-row histories can disclose earlier outcomes, with the documented gain. | Prior full-fold independent successor refutation and participant evidence; independently verify kit/frame/split identity and unchanged metric/scientific source. | Reusable demonstrated evaluation leak: 3.32-5.18% recovery at 99.97-100% precision, frozen-model gains 0.0210-0.0349. It is not merely accepted counter noise. | LEAK-6/9, EV-6/7 |
| Training-only preprocessing, frozen state and own-row inference are the current contract. | Read current summary, leak note, split note and benchmark TODO; compare LEAK-9 and medical-facility/fremtpl2 precedents. | Holds as documentary protocol; valid own-row histories are retained. Equal timestamps grant no other-row access. | LEAK-7/9/34 |
| The honest implementation's batch-invariance example proves downstream enforcement. | Prior `batch_invariance.json` and report scope; current definition/TODO. | Such a broader claim would be unsupported. Current files correctly limit evidence to the tested implementation and leave benchmark enforcement required. | LEAK-9, EV-7 |
| Past choices and original human marks are preserved; latest reuse does not create a new scientific choice. | Actual November 3 `accepted-marks.json`, historical snapshot, current `CURATOR_INPUT.md`, retained record/REVIEW and native-review contract. | Holds as retention provenance; current review must attribute its retention to the latest reuse instruction, not rebind original marks. | principles precedence, human-review contract |

**Reuse and consistency conclusion**

The exact-data guard is satisfied. Saved predictions, probes, raw/source-label checks and participant/successor findings may be retained as dated prior executions because the task, raw source, full frame/category/label state, exact memberships, scientific/probe source and scorer are unchanged. Model/probe settings remain those of their preserved original artifacts. The new current execution consists of installed native qualification plus the explicitly identified independent checks; no new attack, tuning run or full panel should be implied.

I generated the native decision register with explicit current records, working-copy root and knowledge paths. It reports 47 selected decisions of 4,069 total and zero Duolingo consistency flags. Its mechanical open-issue detection also sees historical numbered panel prose, so that count is not evidence of current unsettled issues. Actual current REVIEW and native review collection determine open marks. The matching LEAK-9 precedents retain legitimate history and require method checking in the benchmark; they do not require deleting history or inventing a new human acceptance of the leak.

TP-7's convention wording is stronger than the historical phrase "default established-convention preference". Preserve the historical attributed CC bytes. A current AI clarification may accurately say that the explicit curator-selected threshold and latest user reuse direction govern this specific task; the cutoff remains unverified as a source convention and no general rule amendment is claimed. This wording correction does not reopen the settled cutoff.

The November 3 accepted marks retain snapshot `e8d965ea135d05819d8b441e64ccddb7db7abba1f8229ca7bf2ba5218a9cecd7`, version 1; their current file SHA-256 is `b2689eb6839fcf104b3676a28c937778a224b34fe86e8b3af812c60886373292`. A new native review session can faithfully record `ship` as retention under the latest explicit request, attached to its own actual current source identity and with a note naming that provenance. This is consistent with the current no-open-issues ship default and the already accepted inclusion. It must not copy old marks and stamp them with a new fingerprint or present a new unprompted scientific approval. This audit advises that faithful recording; the owner applies and verifies the new session separately.


</details>

<details><summary>Qualification reuse mediator</summary>

**Focused qualification reuse Duolingo mediator judgment**

November 6, 2026. Dataset: `duolingo_spaced_repetition_recall_1m_clf`. Installed scientific/procedure source: `9048f36a1bcf7da3687fde04b18ef79cd7a1201e`.

Verdict: ship, retaining the previously accepted implementation under Myunghwan's explicit current instruction to repeat add/review/build using past decisions. No new curator input is needed. Finish the routine provenance wording, current native review, cold editing and authorized build verification below; none changes task meaning or reopens inclusion.

Validity: the accepted approximate conditional session-performance task and temporal holdouts remain unchanged. The demonstrated successor-counter evaluation leak remains addressed by the written train-only, frozen-state, own-row inference contract under current LEAK-9. Required future benchmark method checking is still unverified. Value: independently recomputed saved diagnostics retain mean AUROC 0.663756 versus 0.596148 for N-only training rates; these are reused predictions, not fresh model fits. Quality: the unchanged lexical ordinal-like flag is a false positive, not an ordering to impose on morphological categories. Weighed: conditional realized N, clock and label-arrival uncertainty, imperfect source histories, short 2013 coverage and exploratory formulation selection remain explicit accepted limitations. For the curator: no new choice or contradictory finding.

**Changes to make now**

1. Add a current AI clarification that TP-7's established-convention clause is a Must in the current procedure. The explicit task-specific curator instruction selecting inclusive >=75%, followed by the current instruction to reuse past decisions, governs this task. Preserve the historical attributed CC text, including its earlier "default established-convention preference" phrase; do not describe that phrase as the current rule's strength, claim that 75% is established by the source, or invent a general exception/amendment. This is a provenance correction, not a new cutoff decision (TP-7; instruction precedence; EV-7).
2. Record the current native review against the actual current files. Its `ship` retention must cite the latest request in `CURATOR_INPUT.md` and the preserved November 3 inclusion; do not copy the original marks onto a new fingerprint or call retention a newly solicited scientific approval. Original marks and their historical snapshot remain intact (principles, precedence; native human-review contract).
3. Report the current checks and dated reused evidence separately, run the cold editor, and complete the requested native build/reload/reproduction checks. The owner has corrected the initial pending status in `source-reuse.json`; it now records completed current checks. No model rerun is needed merely to manufacture freshness where exact reuse is established (EV-7/8; verification procedure).

**Issues for the curator**

None. No new input contradicts the retained decisions. Planned-count availability, exact clock start/completion meaning and label-arrival bounds remain cannot-verify, rather than being promoted to source facts by approval or reuse. Downstream enforcement remains required, rather than becoming certified by a clean local container build.

An instruction to permit test-block learning, sequential test adaptation or a changed feature/target/split would create a different task or a new conflict. None is requested. Repeating an already answered inclusion question would add no scientific decision.

**Agreed facts and evidence**

I read the current mediator role, focused panel procedure, principles, verification, relevant leak/task/evidence rules, native human-review adaptation, current definition/record/REVIEW, previous November 5 mediator and embedded panel/refutation reports, current claim audit and its numerical evidence, and current native-check/reuse manifests. This focused panel runs the claim auditor, mediator and cold editor. Previous column/split and participant work is retained as dated evidence, not claimed as a freshly executed panel. No advocate/critic debate is implied.

The owner freshly generated 1,429,456 rows with the same eight predictors, category state, labels and all six split arrays. The frame SHA-256 is `b6f104eed4cddf621d169771c84bf61e3cdb2380dd797014e9160433dcf0d596`; native checksum is `v2:c20f832bb366fbe3e87b547b5ddf83cca1c5877f6d3f4e7bd16c1d9a25b6e6e3`, matching the final November 5 package. Current native checking reports 27 checks and zero errors/warnings. The installed test run reports 2,017 passed, 286 skipped and 12 deprecation warnings; those test warnings are distinct from dataset-check warnings.

The independent claim auditor executed `claim_audit.py` successfully. It checked raw-source identity, exact current/prior/participant-kit frame and memberships, scientific/skill/agent trees, unchanged source bytes and runtime versions. All twelve saved baseline/model AUROCs independently reproduce within 1e-12. The current manifest also verifies exact native scoring. These checks support dated reuse under EV-8; they do not establish a new model fit, new attack, fresh publisher lookup or broader model optimality.

The prior full-fold successor refutation remains a demonstrated finding: later rows in the same test window recover 3.32-5.18% of earlier labels at 99.97-100% precision and improve frozen honest AUROC by 0.0210-0.0349. Current notes disclose that mechanism and size. It is a known evaluation leak this cycle, not a newly discovered own-row feature defect; unchanged counter imperfections neither explain it away nor turn it into a new finding. The exact participant-kit identity supports retaining this evidence. The earlier single-model batch-invariance check remains limited to that implementation.

**Consistency and resolution**

The current LEAK-9 amendment and medical-facility/fremtpl2 precedents retain genuine own-row history while forbidding access to other test rows and assigning method checks to the benchmark. The definition states the protocol in the task summary, leak note and split note, and the benchmark TODO retains the concrete Duolingo follow-through. Dropping `history_correct` would change approved inputs and remove honest signal; no new fact requires that more destructive remedy. The prior disagreement about needing a fresh human choice was already resolved by this general amendment and its directly matching precedent. Nothing in the installed refresh changes that resolution.

TP-7 is not treated as a general Should or waived for future datasets. The user's explicit selection is the task-specific instruction; existing candidate/source-label qualification remains dated evidence. The current claim audit reports zero Duolingo consistency flags. Neither that mechanical count nor historical numbered prose substitutes for inspecting actual open issues.

This review synthesizes supplied evidence; it does not report a new raw-data audit or model fit.

</details>

<details><summary>Qualification reuse review editor</summary>

**Focused qualification reuse cold editor**

November 6, 2026. Dataset: `duolingo_spaced_repetition_recall_1m_clf`.

Verdict: ready for the current native review once the two concrete presentation fixes below are applied. No new scientific finding, curator choice or issue 8 is needed.

**Concrete edits, most important first**

1. The panel summary currently reads: "Focused current-main recheck: independent claim/precedent audit, column/split audit, participant attack, independent successor refutation, mediator and editor." Replace it with: "The current qualification reuse focused review comprises a fresh independent claim/precedent audit, mediator and cold editor. Earlier column/split, participant-attack and successor-refutation reports remain dated prior executions, with reuse verified against unchanged source, package versions, frame/category/label state, scorer and all six split memberships. No new model fit, participant attack or full panel is claimed." Keep the recommendation's first sentence beginning `ship`, so the native recommendation badge states the current verdict. The two following standalone paragraphs headed `**Qualification reuse scope:**` and `**Current rule wording:**` must be inside a complete `<details><summary>Qualification reuse scope and rule wording</summary>` section (blank line after its opening and before its closing). The panel format permits only collapsible sections after its summary. Preserve the historical reports and the present TP-7 clarification verbatim within that section. The owner has independently proposed this same repair; applying it resolves this finding.
2. In the newly appended record assessments, replace `at9048f36a` with `at 9048f36a`, `report27 checks` with `report 27 checks`, `Priority2:` with `Priority 2:`, `gap- (` with `gap - (`, `use case- (` with `use case - (`, `source+ (` with `source + (`, `shape+ (` with `shape + (`, `risk- (` with `risk - (`, and `inclusive75%` with `inclusive 75%`. These are missing spaces in current prose, not changes to the preserved curator words or scientific rationale.

**Substantive reading**

The current task is understandable from the definition and README: estimate the probability that a learner-word session meets the inclusive 75% criterion, conditional on numerical realized N and prior/context inputs. The output differs from expected fraction correct, and the cutoff remains curator-selected rather than a source mastery convention. The current AI clarification accurately calls TP-7's established-convention condition a Must while preserving the historical attributed CC and the task-specific user direction. It does not claim a general rule amendment.

The review preserves the November 3 inclusion, original mark identity and historical discussion. The latest quoted instruction explicitly requests another cycle using past decisions. Recording a new native ship retention against the actual current files, with that instruction and the November 3 provenance in its note, is consistent with that request; copying old marks onto a fresh fingerprint would not be. Current capture/application and build remain owner follow-through, not executed editor checks.

The demonstrated future-counter attack is described as an evaluation leak. Its recovery/precision and frozen-model AUROC gains remain dated evidence; the current report does not convert independent rescoring into a new fit or attack. The definition states training-only fitting, frozen state and own-row inference, including batch invariance and exclusion of other test rows. Planned N, clock start/completion, label-arrival bounds and general population fit remain unverified. The README/definition and review correctly leave downstream method checking required. A native data build will not certify benchmark enforcement.

No interior hash heading, absolute host-local path, unresolved record-field row, new hidden curator choice or unsupported change to the target, features, weighting or splits was found in the public review. Historical disagreements and subsequently superseded recommendations remain legible as dated reports. Their preservation does not reopen the settled issues.

**Inspection and limits**

I read the installed review-editor role, review-file format, writing and principles; current definition, README, record and REVIEW; current claim audit, mediator, manifest, reuse evidence and actual latest request. This is a read-only editorial inspection. I wrote only this report, with no new experiments or scientific changes.


**Application (AI):** Both requested presentation fixes are applied. No new semantic finding or issue 8 is introduced.

</details>
