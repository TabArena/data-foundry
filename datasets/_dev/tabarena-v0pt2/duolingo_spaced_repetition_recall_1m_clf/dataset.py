"""Duolingo session-performance classification, Data Foundry v2. Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    SplitPlan,
    TaskSummary,
    Temporal,
    TemporalSplits,
)


class DuolingoSpacedRepetitionRecall1mClf(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Given N exercises on a word and prior practice, will this session achieve at least 75% correct?",
        use_case="A language-learning application estimates session performance given an exercise count and prior practice. This version reports the chance of reaching a curator-selected 75% accuracy criterion, for example to show the likelihood of meeting a session performance goal. The source does not establish this cutoff as mastery or as its deployed decision rule.",
        row="One learner-word lesson or practice session in Duolingo's six-language historical logs, 28 February to 12 March 2013.",
        predicted="Probability of a session achieving at least 75% correct: positive when 4 times the correct count is at least 3 times the exercise count, including exact 75%. This summarizes the same observed performance as the original fraction but does not estimate its conditional mean.",
        known="The supplied session exercise count N (session_seen), course, lexical tag, prior exposure and correct-answer counts, elapsed time and recorded clock context. The archive records realized N, not a documented planned count. Clock consistency is curator-accepted; start/completion semantics remain unverified. Each test prediction uses the fixed training-side model and that row alone; other test rows cannot enter preprocessing, features or inference.",
        split="Three later one-day test windows with earlier training and a one-day gap; learners may recur. Each window uses 1M train and 111,111 test records, approximately 90/10 after sampling. The target-dependent canonical ordering can change sampled records when this target replaces the fraction, so old diagnostic scores are not copied as qualification.",
        changes="Replace expected-fraction regression with probability of reaching at least 75% session accuracy. The label is coarsened, not filtered. AUROC evaluates binary probability rankings; diagnostic classifiers train with binary log loss. Retain numerical session_seen, equal record weights, eight predictors and the temporal-only 90/10 protocol. The cutoff is curator-selected, not source-defined.",
        fit="approximate",
        fit_reason="Session performance includes learning and feedback within practice. The count is realized rather than proven preassigned; the task conditions on it without a causal fixed-count claim. Start/completion timestamps and reporting latency remain unverified. The one-day gap is an accepted conservative approximation, not a proven delay bound.",
    )
    unique_name = "duolingo_spaced_repetition_recall_1m_clf"
    version_of = "duolingo_spaced_repetition_recall"
    version_comment = "Apply the same temporal windows to the full release, then keep 1M earlier training and 111,111 later test rows per window using the shared benchmark sampling order. This curator-selected cap gives approximately 90/10 after sampling; it does not reproduce the paper's single file-order cutoff. Keep the used-row union. All learners are eligible; learner IDs are excluded from features."
    year = "2016"
    domain = "education"
    source = "Other"
    source_url = "https://doi.org/10.18653/v1/P16-1174"
    license = "CC BY-NC 4.0"
    download_description = """
        Obtain settles.acl16.learning_traces.13m.csv.gz, file 3091087, from version 1.0 of
        https://doi.org/10.7910/DVN/N8XJME and place it in local-data-warehouse/duolingo_spaced_repetition_recall/.
        Official data API: https://dataverse.harvard.edu/api/access/datafile/3091087.
        Use the X-Dataverse-key header if authentication is needed, without saving a token in URLs or source code.
        Verify MD5 0a1cae5eb7ad4b0bd9c0de91d74fcced and 379004009 bytes.
    """
    bibtex = r"""
        @inproceedings{settles-meeder-2016-trainable,
          title = {A Trainable Spaced Repetition Model for Language Learning},
          author = {Settles, Burr and Meeder, Brendan},
          booktitle = {Proceedings of the 54th Annual Meeting of the Association for Computational Linguistics},
          pages = {1848--1858}, year = {2016}, doi = {10.18653/v1/P16-1174},
          url = {https://aclanthology.org/P16-1174/}
        }
    """
    curation_comments = """
        We start with settles.acl16.learning_traces.13m.csv.gz, Harvard Dataverse version 1.0, file 3091087.

        - Prediction contract: estimate session performance conditional on supplied session_seen N and prior/context inputs. The archive records realized N, not a verified preassigned count. This is an approximate conditional logged-process task, not a causal test of assigning N. Source clock start/completion semantics and label arrival remain unverified under the curator-accepted recorded-clock approximation.
        - Practical purpose and changed estimand: the former regression estimated E[K/N | X,N], expected fraction correct. This curator-selected version estimates P(K/N >= 0.75 | X,N), the chance that the same session meets a specified accuracy criterion. Both concern session performance, but one does not recover the other. The binary version discards within-class score detail; it does not remove denominator dependence. At N=1,2,3 this criterion equals all-correct; at N=4, 3/4 is positive. No rows are removed for having a particular outcome.
        - Label construction: use original integer session_correct K and session_seen N to define Yes if 4*K >= 3*N, No otherwise. Exact 75% is positive. Verify the published p_recall equals K/N, remove identity-aware source copies before coarsening, and drop p_recall, session_correct and opaque IDs from model data. Numerical session_seen remains a conditioning input, not a label by itself. Coarsening before source-copy removal could collapse distinct events; source-copy removal precedes it here.
        - Training and evaluation: diagnostics fit binary-log-loss classifiers and score roc_auc, with log loss also reported. Benchmark methods retain their own training objective. AUROC evaluates ranking of this binary event, not expected fraction, probability calibration or accuracy at a fixed action threshold. Equal weight per existing record; no exercise/denominator weighting, class balancing or label smoothing. The 75% outcome cutoff is not a threshold on predicted probabilities.
        - Meaning of 75%: Myunghwan selected this performance criterion after bounded >=75% and all-correct diagnostics. It is not a source-defined mastery convention or deployed rule; the source originally predicts a quantitative session proportion. Do not present a changed target as only a metric swap or choose the task solely for a larger numerical gap. Current qualification uses the final definition's own samples and source-label leak checks.
        - Identity-aware deduplication removes 81 exact source profiles with user_id retained, then excludes learner identity. The source lexeme_id is opaque; lexeme_string is a lexical and morphological tag, not free prose. No current correct count or fraction remains as a predictor. All learners remain eligible across temporal folds; prior summaries are allowed, not a cold-start claim.
        - Convert Unix timestamp to UTC-referenced datetime, retained as context and split key. Sort actual timestamps by the base class, not approximate source file order. Three March 12/11/10 2013 one-day windows use expanding history with a one-day gap; newest day is partial, ending 16:14:57 UTC. A custom wrapper only supplies train_cap=1000000 and test_cap=111111. The same full-source eligibility rule remains; the original paper's single file-order 90/10 cut is not literally reproduced.
        - Counter consistency from prior full-source verification: both prior counters match preceding history plus the preceding session in 98.18% of 6,992,475 strictly later visible learner-word pairs; exposure and correct counters decrease in 0.328% and 0.305%. Causes are unknown. Keep source histories rather than reconstructing left-truncated history. These observations do not demonstrate current-outcome leakage.
        - Source and limits: 83.886% of raw sessions are all correct and 58.937% have one exercise. Keep all genuine outcomes. Paper/archive first-90% mean recall differs, 0.859 versus 0.896172; historical paper scores are not reproduced results for this archive. The 2016 ACL paper/code predate this Dataverse deposit released 2017-12-14. The source added lexeme_string to the release; original experiments used lexeme_id.
        - Curator decisions (Myunghwan, latest 2026-11-03): selected inclusive >=75% session-performance classification and AUROC while preserving the practical performance-estimation purpose; this supersedes the earlier fraction/RMSE choice. Keep numerical session_seen, equal records, temporal-only windows, one-day gap, 1M/111111 caps and no learner reservation. The curator selected the formulation after seeing exploratory outer-window results. Model iteration selection uses inner validation, but these inspected dates are not a pristine confirmatory test of the formulation choice. No automated cutoff sweep was used. Final inclusion, warning acceptance and build/commit remain separate decisions.
        - Metric provenance: Settles and Meeder (2016), section 4.1, deliberately use MAE for strength displays and AUC/half-life correlation for ranking; source AUC rounds proportions and is not this >=75% label. Use binary roc_auc as the fallback for the curator-defined event, not as a claim to reproduce source evaluation. The source display-MAE criterion answers a different quantitative target (MET-1, MET-2, MET-8, MET-11).
        - Potential leak, kept on purpose (LEAK-9, an evaluation leak): fit preprocessing and the model on this split's training rows only, freeze learned state, and predict each test session from its own eight supplied covariates. No feature, model step or update may use other test rows, test-block statistics, future histories or held-out labels from another split. Batching is allowed only when each prediction is invariant to adding, removing, reordering or changing unrelated test rows; equal timestamps grant no ordering access. A later test row's history_correct can reveal an earlier session's correct count: a feature-only same-test successor attack recovers 3.32-5.18% of test labels at 99.97-100% precision, increasing the frozen honest model's AUROC by 0.0210-0.0349 across three windows. These are evaluation leaks; each row's own prior histories remain legitimate. The benchmark must check methods against this protocol and exclude test-block learning. Downstream enforcement is required, not established by a dataset check or this build.
        - Final scientific review (2026-11-03, Myunghwan): approved inclusion as implemented with the documented conditional realized-N, clock/label-arrival, source-history, short-period and exploratory-selection limitations. The practical purpose is session-performance estimation via probability of achieving at least 75%, not expected fraction correct or source-defined mastery. Issue 6 is closed; there are no check warnings to accept. Build, commit and publication require a separate request.
    """
    target = "session_accuracy_at_least_75"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason="Source checked: Settles and Meeder (2016), section 4.1, https://aclanthology.org/P16-1174.pdf uses MAE for quantitative strength displays and AUC/half-life correlation for ranking. Myunghwan selects probability of at least 75% session accuracy, a new binary performance summary; source MAE and rounded-proportion AUC do not score this label. Use binary roc_auc fallback (MET-2/MET-8/MET-11), equal records, with no fixed probability action threshold. This changes the target and evaluation, not merely the scale of the old regression error."
    )
    temporal = Temporal(on="timestamp", horizon=1, horizon_unit="days", gap=1, gap_unit="days")
    splits_comment = "Three newest calendar-day test windows, March 12/11/10 2013, with expanding earlier history and a one-day training gap. All learners are eligible and may recur; no learner holdout. Actual timestamps are sorted, with all training clocks strictly before each test window minus the gap. Use the standard temporal windows and shared benchmark sampling order on the full source, with curator-selected caps of 1M train and 111,111 test rows per window (approximately 90/10). Keep the used-row union. A custom split wrapper only supplies the smaller test cap; no temporal eligibility or learner partition changes. Learner ID and the current correct count are excluded from predictors. The newest day is partial; daily cadence and label-delay bounds remain accepted approximations, not verified source facts. Fit on the training side only and predict each test row from its own covariates with frozen model state; no other test rows, future histories, test-block statistics or held-out labels from another split may enter a prediction."

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(
            raw_dir / "settles.acl16.learning_traces.13m.csv.gz",
            dtype=dict.fromkeys(
                ("user_id", "lexeme_id", "lexeme_string", "learning_language", "ui_language"), "category"
            ),
        )

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        assert raw["session_seen"].gt(0).all()
        assert np.allclose(raw["p_recall"], raw["session_correct"] / raw["session_seen"], rtol=0, atol=5e-7)
        assert raw["p_recall"].between(0, 1).all()
        # Remove copies while original fraction and learner identity still distinguish source events.
        df = raw.drop(columns=["lexeme_id"]).drop_duplicates().copy()
        # Integer comparison includes exact 75%, without a floating-point boundary decision.
        df[self.target] = (4 * df["session_correct"] >= 3 * df["session_seen"]).map({False: "No", True: "Yes"})
        df = df.drop(columns=["user_id", "session_correct", "p_recall"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        del df
        return FeatureTypes(categorical=["learning_language", "ui_language", "lexeme_string"], datetime=["timestamp"])

    def _make_splits(self, df: pd.DataFrame) -> SplitPlan:
        from data_foundry.v2.splits import sample_temporal_splits

        windows = TemporalSplits(window=1, unit="days", n_windows=3, gap=1).splits(df, "timestamp")
        for folds in windows.values():
            for train, _test in folds.values():
                assert len(train) >= len(df) / 2, "Full-source training history floor violated"
        reduced, splits, _ = sample_temporal_splits(
            df,
            windows,
            train_cap=1_000_000,
            test_cap=111_111,
            random_state=self.SPLIT_RANDOM_STATE,
        )
        return SplitPlan(df=reduced, splits=splits)

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        del df
        return [
            Decision(
                title="Session performance criterion",
                why="Coarsen observed session accuracy into the curator-selected inclusive 75% event; retain N, exclude outcome ingredients, and preserve the conditional performance-estimation meaning.",
                evidence=pd.DataFrame(
                    {
                        "measure": ["source rows", "learners", "lexemes", "source fraction = 0", "source fraction = 1"],
                        "value": [
                            len(raw),
                            raw["user_id"].nunique(),
                            raw["lexeme_id"].nunique(),
                            int(raw["p_recall"].eq(0).sum()),
                            int(raw["p_recall"].eq(1).sum()),
                        ],
                    }
                ),
            )
        ]
