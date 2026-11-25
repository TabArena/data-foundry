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
    Source,
    TaskSummary,
    Temporal,
    TemporalSplits,
)


class DuolingoSpacedRepetitionRecall1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="From a learner's prior practice of a word, will they get more than half of its exercises right in their next session?",
        use_case="A language-learning application estimates, before a session, whether a learner will recall a word in most of its exercises, from the learner and their prior practice, as the source's own evaluation ranks it.",
        row="One learner-word lesson or practice session in Duolingo's six-language historical logs, 28 February to 12 March 2013.",
        predicted="Probability that more than half of the session's exercises on the word are right: positive when twice the correct count exceeds the exercise count. This is the source's own binary evaluation label (round of the fraction), not its conditional mean.",
        known="The learner, course, lexical tag, prior exposure and correct-answer counts, the time from the word's last practice to the end of the learner's previous lesson, and the clock, all known before the session; not the session's own exercise count, which failed lessons cut short. The timestamp marks the lesson's end, when the label exists. Each test row is predicted from the training-side model and its own inputs alone.",
        split="Three later one-day test windows with earlier training and a one-day gap; learners may recur. Each train side holds every earlier session, of which a benchmark samples 1M; each test window keeps at most 500k sessions, drawn at random. Scores of the earlier fixed draw (1M training, 111,111 test sessions) are not copied as qualification.",
        changes="Replace expected-fraction regression with the source's binary evaluation label, more than half right. The label is coarsened, not filtered. Drop the session's exercise count; keep the learner id as an input; seven source inputs plus the learner, equal record weights, temporal-only windows.",
        fit="approximate",
        fit_reason="Session performance includes learning and feedback within practice, and the label's cutoff allows fewer misses at some exercise counts than others, which the inputs do not see. The timestamp marks the lesson's end (measured), so the label exists at the recorded time; the one-day gap is a curator choice, longer than the label's delay.",
    )
    unique_name = "duolingo_spaced_repetition_recall_1m"
    sources = (
        Source(
            role="publication",
            platform="Other",
            url="https://doi.org/10.18653/v1/P16-1174",
            license="CC BY-NC 4.0",
            year="2016",
            bibtex=r"""
        @inproceedings{settles-meeder-2016-trainable,
          title = {A Trainable Spaced Repetition Model for Language Learning},
          author = {Settles, Burr and Meeder, Brendan},
          booktitle = {Proceedings of the 54th Annual Meeting of the Association for Computational Linguistics},
          pages = {1848--1858}, year = {2016}, doi = {10.18653/v1/P16-1174},
          url = {https://aclanthology.org/P16-1174/}
        }
    """,
        ),
    )
    domain = "education"
    download_description = """
        Obtain settles.acl16.learning_traces.13m.csv.gz, file 3091087, from version 1.0 of
        https://doi.org/10.7910/DVN/N8XJME and place it in local-data-warehouse/duolingo_spaced_repetition_recall/.
        Official data API: https://dataverse.harvard.edu/api/access/datafile/3091087.
        Use the X-Dataverse-key header if authentication is needed, without saving a token in URLs or source code.
        Verify MD5 0a1cae5eb7ad4b0bd9c0de91d74fcced and 379004009 bytes.
    """
    curation_comments = """
        We start with settles.acl16.learning_traces.13m.csv.gz, Harvard Dataverse version 1.0, file 3091087.

        - Prediction contract: estimate session performance before the session, from the learner's prior practice of the word and the context. The session's exercise count (session_seen) is not an input (Andrej, 2026-11-24, review issue 10 B): it is the realized count, known when the session ends, failed lessons end early (lessons under 15 exercises, 7.9% of rows, fall below 75% in 23-33% of cases), and the source's own models never use it. The recorded timestamp marks the lesson's end (the gap to the learner's next stamp grows 2.22 s per exercise of the later lesson), and the label exists at that time.
        - Practical purpose and changed estimand: the former regression estimated E[K/N | X], expected fraction correct. This version estimates P(2K > N | X), the source's own binary evaluation event (its `evaluation.r` scores `roc(round(p) ~ pp)`; R rounds 0.5 down, so exactly half is negative). Both concern session performance, but one does not recover the other. The label still depends on the exercise count (an odd count cannot split evenly), though the count is not an input. No rows are removed for having a particular outcome.
        - Label construction: use original integer session_correct K and session_seen N to define Yes if 2*K > N, No otherwise (exactly half is No, as the source rounds). Verify the published p_recall equals K/N, remove identity-aware source copies before coarsening, and drop p_recall, session_correct, session_seen and lexeme_id from model data. Coarsening before source-copy removal could collapse distinct events; source-copy removal precedes it here.
        - Training and evaluation: diagnostics fit binary-log-loss classifiers and score roc_auc, with log loss also reported. Benchmark methods retain their own training objective. AUROC evaluates ranking of this binary event, not expected fraction, probability calibration or accuracy at a fixed action threshold. Equal weight per existing record; no exercise/denominator weighting, class balancing or label smoothing. The label's cutoff on the fraction is not a threshold on predicted probabilities.
        - Label choice (Andrej, 2026-11-24, review issue 11 B): the source's own label replaces Myunghwan's 75% cutoff of 2026-11-03. Without the exercise count both labels carry the same signal (ROC AUC 0.618 and 0.619, LightGBM, three shipped windows), and the source's label needs no curator-chosen cutoff.
        - Identity-aware deduplication removes 81 exact source profiles with user_id retained. The learner id stays an input (Andrej, 2026-11-24, review issue 13 B): the application always knows its learner, 71-74% of test rows come from learners seen in training, and it adds 0.005-0.011 ROC AUC; the source's own models do not use it. The source lexeme_id is opaque and dropped; lexeme_string is a lexical and morphological tag, not free prose: the release has 19,279 lexeme_id values and 18,781 lexeme_string tags (at most 3 ids per tag). No current correct count or fraction remains as a predictor.
        - Convert Unix timestamp to UTC-referenced datetime, retained as context and split key. Sort actual timestamps by the base class, not approximate source file order. Three March 12/11/10 2013 one-day windows use expanding history with a one-day gap; newest day is partial, ending 16:14:57 UTC. The row budget: each train side holds every earlier session (9,101,009 to 11,116,635 rows, 70.8% to 86.5% of the 12,854,145, before the gap), and a benchmark samples 1M of them; each test window keeps at most 500k of its sessions (the collection's budget, 2026-11-24, Andrej, issue 12 B, which replaced the fixed draw of 1M training and 111,111 test sessions). The original paper's single file-order 90/10 cut is not reproduced.
        - Counter consistency from prior full-source verification: both prior counters match preceding history plus the preceding session in 98.18% of 6,992,475 strictly later visible learner-word pairs; exposure and correct counters decrease in 0.328% and 0.305%. Causes are unknown. Keep source histories rather than reconstructing left-truncated history. These observations do not demonstrate current-outcome leakage.
        - The release holds no first encounter of a word: history_seen is at least 1 on every row, also on each learner-word pair's first row in the release. delta matches the gap to the pair's previous logged session in 88.0% of the rows that follow one; it is longer by the 1-second rounding in 11.5% and shorter in 0.45%, where a session is missing from the log, independent of the previous outcome.
        - The lag as an input (Andrej, 2026-11-24, review issue 9 D): the timestamp marks a lesson's end, so the published delta runs from the word's last practice to this lesson's end and holds this lesson's own length, which a failed lesson cuts short. It is replaced by delta_to_previous_lesson, the time from the word's last practice to the end of the learner's previous lesson, known when this lesson starts; it is 0 where the word was practised in that previous lesson (27.6% of rows) and missing where that lesson is not in the release or comes before the last practice (15.7%). It leaves out the break before this lesson, which cannot be told apart from the lesson's length. It is built from the learner's earlier lesson times, as history_seen counts earlier sessions, and uses no label. Measured (LightGBM, three shipped days): ROC AUC 0.624-0.627 with it, 0.628-0.630 with the published delta, 0.621-0.624 with no lag.
        - Source and limits: 83.886% of raw sessions are all correct and 58.937% have one exercise. Keep all genuine outcomes. Paper/archive first-90% mean recall differs, 0.859 versus 0.896172; historical paper scores are not reproduced results for this archive. The 2016 ACL paper/code predate this Dataverse deposit released 2017-12-14. The source added lexeme_string to the release; original experiments used lexeme_id.
        - Curator decisions (Myunghwan, latest 2026-11-03): selected inclusive >=75% session-performance classification and AUROC (re-targeted to the source's round(p) on 2026-11-24, Andrej, issue 11 B); this supersedes the earlier fraction/RMSE choice. Keep numerical session_seen (dropped on 2026-11-24, Andrej, issue 10 B), equal records, temporal-only windows, one-day gap and no learner reservation; the 1M/111111 caps he approved became whole training sides under the `_1m` name on 2026-11-24 (Andrej, issue 12 B). The curator selected the formulation after seeing exploratory outer-window results. Model iteration selection uses inner validation, but these inspected dates are not a pristine confirmatory test of the formulation choice. No automated cutoff sweep was used. Final inclusion, warning acceptance and build/commit remain separate decisions.
        - Metric provenance: Settles and Meeder (2016), section 4.1, deliberately use MAE for strength displays and AUC/half-life correlation for ranking; the source's AUC is computed on round(p), this dataset's label, pooled over rows, which is the metric here. The source display-MAE criterion answers a different quantitative target (MET-1, MET-2, MET-8, MET-11). Unit of the score: pooled AUROC ranks rows across learners and lessons, while a practice scheduler ranks one learner's words; within a lesson (mean over test lessons holding both classes) LightGBM scored 0.644-0.652 with session_seen as an input, 0.581-0.590 without it, against 0.666-0.672 pooled (2026-11-21, three windows, before session_seen was dropped). The metric stays pooled AUROC; this is a note on what it measures.
        - Potential leak, kept on purpose (LEAK-9, an evaluation leak): fit preprocessing and the model on this split's training rows only, freeze learned state, and predict each test session from its own seven supplied covariates. No feature, model step or update may use other test rows, test-block statistics, future histories or held-out labels from another split. Batching is allowed only when each prediction is invariant to adding, removing, reordering or changing unrelated test rows; equal timestamps grant no ordering access. A later test row's history_correct can reveal an earlier session's correct count: a feature-only same-test successor attack recovers 3.32-5.18% of test labels at 99.97-100% precision, increasing the frozen honest model's AUROC by 0.0210-0.0349 across three windows. These are evaluation leaks; each row's own prior histories remain legitimate. The benchmark must check methods against this protocol and exclude test-block learning. Downstream enforcement is required, not established by a dataset check or this build.
        - Final scientific review (2026-11-03, Myunghwan): approved inclusion as implemented with the documented conditional realized-N, clock/label-arrival, source-history, short-period and exploratory-selection limitations. The practical purpose is session-performance estimation via probability of achieving at least 75%, not expected fraction correct or source-defined mastery. Issue 6 is closed; there are no check warnings to accept. Build, commit and publication require a separate request.
        - Split walk (the split decision tree, SPLIT-36, from the record's collection type Dated Event Log): [LOG.meets] the model meets practice sessions after the data, cases after the data → Order and windows step → [ORDER.order] the session timestamp is recorded: yes → [ORDER.windows] three one-day test windows, each training on at least half the rows: yes → leaf L-ORDER.windows, Temporal · windows on the time key, the split the definition ships (`split_leaf`; whole training sides under the collection's row budget since 2026-11-24, Andrej, issue 12 B). The gap follows the gap rules: the label's delay lies within the timestamp's resolution, which needs no gap; the gap is open for the curator.

        Apply the temporal windows to the full release; each train side holds every earlier session and a benchmark samples 1M of them; each test window keeps at most 500k sessions. This does not reproduce the paper's single file-order cutoff. All learners are eligible; the learner id is an input.
    """
    target = "session_more_than_half_correct"
    problem_type = "binary_classification"
    metric = Metric.source(
        "roc_auc",
        original="AUC of the predicted recall against round(p), pooled over sessions",
        reference="https://github.com/duolingo/halflife-regression/blob/master/evaluation.r",
    )
    temporal = Temporal(on="timestamp", splits=TemporalSplits(window=1, unit="days", n_windows=3, gap=1))
    split_leaf = "L-ORDER.windows"
    splits_comment = "Three newest calendar-day test windows, March 12/11/10 2013, with expanding earlier history and a one-day training gap. All learners are eligible and may recur; no learner holdout. Actual timestamps are sorted, with all training clocks strictly before each test window minus the gap. Use the standard temporal windows on the full source: each train side holds every earlier session (70.8% to 86.5% of the rows, before the gap), and a benchmark samples 1M of them, by default at random from the newest year before the window (all 12 days of history); each test window keeps at most 500k of its sessions, drawn at random (the collection's row budget). No learner partition. Learner ID and the current correct count are excluded from predictors. The newest day is partial (ends 16:14:57 UTC) but as full per hour as earlier days. The timestamp marks the lesson's end, so the label exists at the recorded time and the one-day gap is longer than the label's delay; the source names no refit cadence, so the daily windows are our assumption. Fit on the training side only and predict each test row from its own covariates with frozen model state; no other test rows, future histories, test-block statistics or held-out labels from another split may enter a prediction."

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
        # The source's round(p): more than half right; R rounds 0.5 down, so exactly half is No.
        df[self.target] = (2 * df["session_correct"] > df["session_seen"]).map({False: "No", True: "Yes"})
        df = df.drop(columns=["session_correct", "session_seen", "p_recall"])
        # The lag known when the lesson starts: from the word's last practice to the end of the learner's previous
        # lesson. The published delta runs to this lesson's end and so holds its length, which a failed lesson cuts
        # short. Missing where the learner's previous lesson is not in the release or precedes the last practice.
        lessons = df[["user_id", "timestamp"]].drop_duplicates().sort_values(["user_id", "timestamp"], kind="stable")
        lessons["previous_end"] = lessons.groupby("user_id", observed=True)["timestamp"].shift(1)
        df = df.merge(lessons, on=["user_id", "timestamp"], how="left", validate="many_to_one")
        lag = df["previous_end"] - (df["timestamp"] - df["delta"])
        df["delta_to_previous_lesson"] = lag.where(df["previous_end"].notna() & lag.ge(0))
        df = df.drop(columns=["delta", "previous_end"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        del df
        return FeatureTypes(
            categorical=["user_id", "learning_language", "ui_language", "lexeme_string"], datetime=["timestamp"]
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        del df
        return [
            Decision(
                title="Session performance criterion",
                why="Coarsen observed session accuracy into the source's round(p) event; exclude the exercise count and the outcome ingredients, and preserve the conditional performance-estimation meaning.",
                evidence=pd.DataFrame(
                    {
                        "measure": [
                            "source rows",
                            "learners",
                            "lexeme ids",
                            "lexeme strings",
                            "source fraction = 0",
                            "source fraction = 1",
                        ],
                        "value": [
                            len(raw),
                            raw["user_id"].nunique(),
                            raw["lexeme_id"].nunique(),
                            raw["lexeme_string"].nunique(),
                            int(raw["p_recall"].eq(0).sum()),
                            int(raw["p_recall"].eq(1).sum()),
                        ],
                    }
                ),
            )
        ]
