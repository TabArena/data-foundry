"""Curated dataset definition for `github_pull_request_acceptance_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    RowBudget,
    TaskSummary,
    Temporal,
    TemporalSplits,
    decode,
)

# The GHTorrent MySQL dump the source builds on is dated 2019-06-01; its last pull request closes on 2019-05-31.
DUMP_DATE = pd.Timestamp("2019-06-01")
# Every pull request opened before this date has at least 182 days of follow-up before the dump, so each one decided
# within DECIDED_WITHIN_DAYS of opening is in the release, in every month alike.
LAST_OPENED = pd.Timestamp("2018-12-01")
DECIDED_WITHIN_DAYS = 180

# The inputs known when the pull request is opened (the source's Table 2, timing checked against the source code of
# the MSR 2020 release, github.com/zhangxunhui/new_pullreq_msr2020, bin/pull_req_data_extraction.rb and bin/factors/).
KEEP = [
    # the contributor, as of the opening
    "first_pr",
    "core_member",
    "prev_pullreqs",
    "prior_interaction",
    "social_strength",
    "followers",
    "account_creation_days",
    # the project, as of the opening
    "project_id",
    "language",
    "project_age",
    "sloc",
    "test_lines_per_kloc",
    "test_cases_per_kloc",
    "asserts_per_kloc",
    "team_size",
    "perc_external_contribs",
    "open_issue_num",
    "open_pr_num",
    "pushed_delta",
    "fork_num",
    "stars",
    # the pull request, as opened
    "description_length",
    "commits_on_files_touched",
    "friday_effect",
]


def _history_rates(df: pd.DataFrame, keys: list[str], rate: str, count: str) -> pd.DataFrame:
    """Share merged among the pull requests of `keys` closed strictly before each row was opened, and their number.

    Only decisions made before the opening count, so a row's own outcome and the outcomes of pull requests still open
    then never enter. NaN when none was closed before.
    """
    ev = df[[*keys, "closed_at", "merged_flag"]].sort_values([*keys, "closed_at"], kind="stable")
    grouped = ev.groupby(keys, sort=False)
    ev["n_closed"] = grouped.cumcount() + 1
    ev["n_merged"] = grouped["merged_flag"].cumsum()
    ev = ev.sort_values("closed_at", kind="stable")
    query = df[[*keys, "created_at"]].assign(row=np.arange(len(df))).sort_values("created_at", kind="stable")
    out = pd.merge_asof(
        query,
        ev[[*keys, "closed_at", "n_closed", "n_merged"]],
        left_on="created_at",
        right_on="closed_at",
        by=keys,
        direction="backward",
        allow_exact_matches=False,
    ).sort_values("row", kind="stable")
    return pd.DataFrame(
        {rate: (out["n_merged"] / out["n_closed"]).to_numpy(), count: out["n_closed"].fillna(0).to_numpy()},
        index=df.index,
    )


class GithubPullRequestAcceptance1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a pull request just opened on a GitHub project be merged?",
        use_case=(
            "A project's integrator, when a pull request arrives, gauges how likely it is to be merged, to decide "
            "which of many open pull requests to review first; prioritising concurrent pull requests is a top "
            "challenge in a survey of 750 integrators (Gousios et al., ICSE 2015), and Dey and Mockus (2020) model it "
            "at opening."
        ),
        row=(
            "One pull request to the default branch of one of 10,017 GitHub projects in six languages (of the 11,229 "
            "in the release), opened from August 2010 to November 2018 and decided within 180 days (GHTorrent data, "
            "Zhang et al. 2020/2023)."
        ),
        predicted="Whether it was merged (GitHub's merge event) rather than closed without merging.",
        known=(
            "What is known when it is opened: the contributor's history in the project (earlier pull requests and "
            "how many were merged, core membership, interactions, followers), the project's size, age, popularity, "
            "workload and merge record, and the length of the pull request's title and description."
        ),
        split=(
            "Each test window is one month (September to November 2018) of newly opened pull requests of known "
            "projects; training is a random million of the pull requests opened at least a month before it."
        ),
        changes=(
            "We dropped everything recorded after the opening (review comments, CI results, who closed it, the "
            "final commits and code churn), rebuilt the merge rates from decisions made before the opening, and "
            "keep pull requests decided within 180 days, opened by November 2018."
        ),
        fit="approximate",
        fit_reason=(
            "The history features are what an integrator sees at opening, but the code change itself is missing: "
            "the release holds only its final state after review, which we dropped. Pull requests decided after 180 "
            "days or never are left out, and the label misses merges done outside GitHub's merge button."
        ),
    )

    # Dataset
    unique_name = "github_pull_request_acceptance_1m"
    version_of = "github_pull_request_acceptance"
    version_comment = """
        We sample per test window (v2 split protocol): each monthly window keeps at most 500k of its rows (it has fewer, so all), and its train side is a random 1M of the rows opened at least one month before the window (the gap), drawn in one random order for all windows; the frame keeps only the rows a split uses. The train sides hold 2,314,345 to 2,477,818 rows before sampling, so the full dataset does not fit the TabArena v0.2 budget of 1M training rows.
    """
    year = "2020"
    domain = "technology & internet"
    source = "Other"
    source_url = "https://zenodo.org/records/4837135"
    license = "CC BY 4.0"
    data_tags = ()
    download_description = """
        We download the CSV of the TSE release from Zenodo (version 4837135 of the concept record 4837134; md5 08f4868a217b8bb35dc06908ad3a05aa). The record's SQL dump is not used.

        mkdir -p local-data-warehouse/github_pull_request_acceptance && wget -O local-data-warehouse/github_pull_request_acceptance/new_pullreq.csv "https://zenodo.org/records/4837135/files/new_pullreq.csv?download=1"
    """
    bibtex = """
        @article{zhang2023pull,
          title = {Pull Request Decisions Explained: An Empirical Overview},
          author = {Zhang, Xunhui and Yu, Yue and Gousios, Georgios and Rastogi, Ayushi},
          journal = {IEEE Transactions on Software Engineering},
          volume = {49},
          number = {2},
          pages = {849--871},
          year = {2023},
          doi = {10.1109/TSE.2022.3165056},
        }
    """
    curation_comments = """
        We start with `new_pullreq.csv` (3,281,386 closed pull requests, 101 columns) from the Zenodo record of Zhang, Yu, Gousios and Rastogi (IEEE TSE 2023), the enlarged version of the dataset first released for MSR 2020 (Zhang, Rastogi and Yu; Zenodo 3922907, 2020-03-07; hence the year 2020).

        - Prediction point: the moment the pull request is opened. Every input must be known then; everything from the review (comments, commits pushed after opening, CI builds, who closed it and when) is left out (LEAK-10).
        - The source removed 2.0% of its 3,347,937 pull requests before release (66,551 rows): those with a negative first response time, CI latency, account age or project age (TSE paper, Sec. 2.3). The first two are measured after the opening; the selection is the same in every period and cannot be undone.
        - The time column `created_at` is the opening time, rebuilt as `last_close_time` (written day/month/year) minus `lifetime_minutes`, which the source code computes from the pull request's opening event to its latest close (`pull_reqs` in bin/pull_req_data_extraction.rb). `last_close_time` and `lifetime_minutes` are then dropped.
        - Dropped as recorded after the opening (LEAK-10), read from the source code: `lifetime_minutes`, `first_response_time`, `reopen_or_not`; every comment, participant and emotion field (`has_comments`, `num_comments`, `num_comments_con`, `num_code_comments`, `num_code_comments_con`, `num_participants`, `has_participants`, `part_num_code`, `core_comment`, `contrib_comment`, `inte_comment`, `other_comment`, `has_exchange`, `comment_conflict`, `perc_pos_emotion`, `perc_neg_emotion`, `perc_contrib_pos_emo`, `perc_contrib_neg_emo`, `perc_inte_pos_emo`, `perc_inte_neg_emo`, `contrib_first_emo`, `inte_first_emo`); `hash_tag` and `at_tag`, which read the description or the comments; every CI field (`ci_exists` comes from the status checks posted on the pull request, `ci_build_num`, `ci_latency`, `ci_test_passed`, `ci_failed_perc`, `ci_first_build_status`, `ci_last_build_status`).
        - Dropped as facts about the integrator, who is the user that closed the pull request and is known only then (LEAK-10): `last_closer_id`, `same_user` (the source's strongest factor), `prior_review_num` (the closer's earlier closes, counted up to the close time), `inte_affiliation`, `inte_open`, `inte_cons`, `inte_extra`, `inte_agree`, `inte_neur`, `same_country`, `same_affiliation`, `contrib_follow_integrator` and the personality differences `open_diff`, `cons_diff`, `extra_diff`, `agree_diff`, `neur_diff`.
        - Dropped as the final state of the change after review (LEAK-10): `num_commits`, `src_churn`, `test_churn`, `churn_addition`, `churn_deletion`, `files_added`, `files_deleted`, `files_changed` and `test_inclusion`. The source code counts them over every commit of the pull request at the dump (`pr_stats(pr)` with `at_open = false`; the same file has an `at_open` mode that keeps the commits made before the opening, which it uses only for `commits_on_files_touched`), so commits pushed during the review are in them, and the release cannot tell which. Their worth, the late part included: ROC AUC 0.8162 to 0.8209 in November 2018 and 0.8165 to 0.8245 in October with them added (untuned LightGBM on 600k training rows).
        - Dropped as attributes of the contributor looked up after the opening, and personal (LEAK-10; the curator may decide otherwise on the personal ones): `contrib_gender` (inferred from the name), `contrib_country` (inferred, filled in 2021 from GitHub profiles for the TSE release), `contrib_affiliation` (from the GitHub profile's company and e-mail at collection), and the five personality scores `contrib_open` to `contrib_neur` (IBM Watson on all of the user's comments in the dump, those on this pull request and later ones included).
        - Dropped: `bug_fix`, 99.3% empty (the TSE paper drops it too); the identifiers `id` (a row number of the release) and `creator_id` (the contributor's GHTorrent id, used only to rebuild the merge rates below).
        - The source's merge rates `pr_succ_rate` and `requester_succ_rate` are replaced (LEAK-7, USE-10). The source code counts as merged every earlier pull request opened before this one that was merged at any time, also after this one was opened (`pr_before_merged` and `prev_pull_requests` in bin/utils/pull_request.rb), and it counts merges by Gousios's heuristics, not by the merge event the label uses. We rebuild them from the release as the share merged (the label's definition) among the project's, and the contributor's, pull requests closed before the opening, with their numbers: `pr_succ_rate_at_open`, `project_prs_decided_before`, `requester_succ_rate_at_open`, `requester_prs_decided_before` (missing when none was decided before). They count only the pull requests in the release.
        - Kept, known at the opening by the source code: `first_pr`, `prev_pullreqs` (pull requests opened before), `core_member` (core team membership before the opening), `prior_interaction` and `social_strength` (the three months before), `followers`, `account_creation_days`, `project_age`, `team_size`, `perc_external_contribs`, `open_issue_num`, `open_pr_num`, `pushed_delta` (seconds since the project's last push), `fork_num`, `stars` (counted before the opening), `sloc` and the test densities (the base commit's tree), `commits_on_files_touched` (the commits made before the opening), `friday_effect` and `language`. `project_id` (the GHTorrent project id) stays as a category: the integrator's project is known and recurs. Untuned LightGBM scores higher without it (ROC AUC 0.8283 against 0.8189 in November 2018, 0.8259 against 0.8163 in October), a 10,000-level category it overfits; a model's limit is no reason to drop a column (EV-4).
        - Potential leak, kept on purpose: `description_length` counts the words of the title and the description as stored in GHTorrent's MongoDB dump, which keeps a pull request's latest state, so an edit made during the review would be in it. Edits are not documented for this data and cannot be located row by row; the column carries a small gain (ROC AUC 0.8189 with it, 0.8165 without, November 2018, untuned LightGBM), at most +0.0024 ROC AUC, so it stays with this note (LEAK-10, LEAK-6), as `onlinenewspopularity` and `medical_facility_operational_data` keep theirs.
        - Dropped, no code and no gain (LEAK-10): `integrator_availability`, "latest activity of the two most active integrators" (TSE paper, Table 2; added for the TSE release, whose code is not published), an hour count from 0 to 23. When it was measured cannot be checked, and it carries nothing: alone ROC AUC 0.468; 0.8188 without it against 0.8189 with it (November 2018, untuned LightGBM).
        - Dropped as counted after the merge (LEAK-10): `contrib_perc_commit`, the contributor's share of the project's commits (added for the TSE release, no published code). Among the first pull requests of contributors outside the core team, who should have almost no commits in the project yet, it is above 0 for 64.6% of the merged and 22.8% of the unmerged ones, and alone it scores ROC AUC 0.718 there: the count holds the pull request's own commits once merged. No code backs a count as of the opening. Its worth in the model: ROC AUC 0.8224, 0.8220 and 0.8087 with it against 0.8206, 0.8184 and 0.8081 without (November, October and September 2018; untuned LightGBM with 300 trees on 300k training rows), small because the merge rates carry the contributor's record.
        - Note: the label is GitHub's merge event (`merged_or_not` in the source code: a merge time exists). Merged means merged through GitHub: a pull request integrated outside it, by a squash, a cherry-pick or a merge on the command line, reads as `No` (USE-5; one reason the fit is approximate), though the source's own merge rates count many of them as merged by Gousios's heuristics.
        - Note: the projects were chosen in 2019 for having a new pull request in the three months before the dump and at least 20 closed pull requests (MSR 2020 paper, Sec. 3), so every project is one that lived on.
        - The release holds only pull requests closed by the dump, so each recent month lacks its slowest ones, which are merged less often (Decision 1: 0.902 merged among those opened in May 2019, 0.855 to 0.879 in each month of 2018). We keep the pull requests decided within 180 days of opening and opened before 2018-12-01 (LEAK-24), so every month holds all of its pull requests decided within 180 days, in training and test alike: 67,859 slower ones (2.5% of those opened by November 2018) and the 546,796 opened later leave, 2,666,723 rows stay. Left out everywhere: the pull requests decided after 180 days (3.3% of the 2016 cohort, merged 40% of the time, Decision 2) and those never decided, which the release does not hold. After the cut no recent month is out of band (leak probe 13 by month: the newest six months' share of `No` at z -0.9 to -1.3 against the 94 months before, pooled at most z -2.2, threshold 3). By quarter, the newest four pooled fall below the band (z -3.9): the share of `No` dropped from 0.15 to 0.23 per quarter in 2015-2016 to a plateau of 0.12 to 0.14 from 2017 on, and the last quarter is at 0.137, higher, where censoring would lower it. That is a drift of the level the task carries, not a cut-off at the end.
        - Dropped: 8 rows of the release identical to another in all 100 columns but the row number `id` (8 pairs, all from one account and project each, opened and closed in the same second), read as one pull request recorded twice (LEAK-18). After the drops, 25 more pairs share every shipped column: pull requests the same account (mostly a bot) opened in the same second in the same project that differ in a dropped column (commits, churn), so distinct pull requests; kept as natural repeats (LEAK-18).
        - Note: the personal attributes carry no gain on the windows (ROC AUC 0.8155 with gender, country and affiliation added, 0.8162 without, November 2018), so leaving them out costs the task nothing measurable.
        - Note: the number format alone scores ROC AUC 0.711 (leak probe 17 on the builder's frame; `social_strength` 0.65, `contrib_perc_commit` 0.63, `requester_succ_rate_at_open` 0.60). `contrib_perc_commit` is dropped above, so for it the reading below is withdrawn. The other columns are shares, and a share written with few decimals has a small denominator, a contributor with little history, which the counts carry too; the same code computes them for both classes, so we read it as the history, not a recording by class (LEAK-13). Not tested further.
        - Rows: the source collected 3,347,937 pull requests, the release holds 3,281,386, the 180-day and November-2018 cut leaves 2,666,723, and the shipped frame keeps the 1,304,081 that a split uses (each train side a random 1M, every test row).
        - Note: the 180-day window is a selection, the pull requests decided later leave; `smartshark_release_defect_prediction` meets the same end-of-data problem with a label horizon instead (a bug fixed more than a year after the release counts as none, every row stays). Both shapes are allowed (LEAK-23, LEAK-24); here a horizon would change the label to "merged within 180 days", and the slow merges would read as `No`.
        - Protocol (LEAK-9, an evaluation leak): every history count is valid at its own row's opening, but a later test row of the same project or contributor reveals an earlier one's outcome: the differences of `project_prs_decided_before` and `pr_succ_rate_at_open` (or the contributor's, the contributor rebuilt from `project_id` and the opening date minus `account_creation_days`) between consecutive test rows lift ROC AUC from 0.81-0.82 to 0.90-0.92 in all three windows (the panel's task gamer). Each test pull request is predicted from the training rows and its own features only; no feature or model step may use other test rows. The columns stay: they are what the integrator sees at the opening.
        - Note on the score: ROC AUC is pooled over all test pull requests, so it also rewards telling projects that merge often from those that do not. The project's merge rate from the training rows alone scores 0.720, 0.708 and 0.709 pooled (November, October, September 2018), `pr_succ_rate_at_open` alone 0.753, 0.750 and 0.733, LightGBM 0.813, 0.812 and 0.798; within projects with both classes (71-75% of test rows) the same LightGBM averages 0.613, 0.629 and 0.618 (300 trees on 300k training rows, the panel's mediator). Whether to score within each project is open (REVIEW.md, issue 1).
        - The target `merged` ships as `No` / `Yes` (`Yes` is merged).
    """

    # Task
    target = "merged"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason=(
            "The TSE paper scores its basic model by weighted precision, weighted recall, weighted F-score and test "
            "ROC AUC side by side (Sec. 2.4.3 and 3.1.1) with no single criterion, and the MSR 2020 data paper scores "
            "no task, so the fallback (MET-5, MET-8). No competition was held on this data."
        )
    )

    # Splits
    splits_comment = """
        Three monthly test windows of newly opened pull requests, November, October and September 2018 (newest first; 88,913, 99,992 and 80,238 rows, 12.3% to 14.2% not merged), each with a one-month gap: the train side holds the pull requests opened at least one month before the window starts. A month is the horizon of an integrator's model refit monthly. The gap stands for the decisions still pending at a refit: with it 0.27% of the newest train side's labels came after the window's start, 0.83% without it, and a model trained on the labels known at the start scores like the gap (ROC AUC 0.818 against 0.819 with the gap and 0.823 with no gap and every label final; untuned LightGBM on 600k training rows, November 2018; October 0.819, 0.816 and 0.820). Each window keeps all its rows (under the 500k test budget); each train side is a random 1M of its 2.31M to 2.48M earlier rows, drawn in one random order for all windows. The data ends with the pull requests opened in November 2018 (Decisions 1 and 2). The source's own evaluation split on the close time (the first 90% to train, TSE paper Sec. 2.4.3); we split on the opening, the prediction point. Projects recur on both sides (94-95% of each window's test rows come from a project in its full train side, before the sampling): the integrator triages new pull requests of a project they know, so its history is a legitimate input (USE-10, SPLIT-13).
    """
    temporal = Temporal(
        on="created_at",
        splits=TemporalSplits(window=1, unit="months", n_windows=3, gap=1),
    )
    row_budget = RowBudget(train=1_000_000, test=500_000)

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "new_pullreq.csv", engine="pyarrow")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # 0. Rows identical in all 100 columns but the row number `id`: one pull request recorded twice (LEAK-18).
        df = raw.drop_duplicates(subset=[c for c in raw.columns if c != "id"], keep="first").copy()
        # 1. The opening time: the latest close minus the minutes from the opening to it (source code, `pull_reqs`).
        df["closed_at"] = pd.to_datetime(df["last_close_time"], format="%d/%m/%Y %H:%M:%S")
        df["created_at"] = df["closed_at"] - pd.to_timedelta(df["lifetime_minutes"], unit="m")
        df["merged_flag"] = df["merged_or_not"].astype(int)
        # 2. Merge rates as of the opening, from decisions made before it (over every row, before the filters below).
        project = _history_rates(df, ["project_id"], "pr_succ_rate_at_open", "project_prs_decided_before")
        requester = _history_rates(
            df, ["project_id", "creator_id"], "requester_succ_rate_at_open", "requester_prs_decided_before"
        )
        df = pd.concat([df, project, requester], axis=1)
        # 3. Every month alike: pull requests opened before LAST_OPENED and decided within DECIDED_WITHIN_DAYS.
        decided_in_time = df["lifetime_minutes"] <= DECIDED_WITHIN_DAYS * 24 * 60
        df = df[(df["created_at"] < LAST_OPENED) & decided_in_time]
        # 4. Keep the inputs known at the opening, the rebuilt rates, the time and the target.
        rebuilt = [
            "pr_succ_rate_at_open",
            "project_prs_decided_before",
            "requester_succ_rate_at_open",
            "requester_prs_decided_before",
        ]
        df = df[["created_at", *KEEP, *rebuilt, "merged_or_not"]].rename(columns={"merged_or_not": self.target})
        df = decode(df, {self.target: {0: "No", 1: "Yes"}})
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=["project_id", "language", "first_pr", "core_member", "friday_effect"],
            datetime=["created_at"],
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        from sklearn.metrics import roc_auc_score

        closed = pd.to_datetime(raw["last_close_time"], format="%d/%m/%Y %H:%M:%S")
        created = closed - pd.to_timedelta(raw["lifetime_minutes"], unit="m")
        days = raw["lifetime_minutes"] / (24 * 60)
        merged = raw["merged_or_not"].astype(int)

        # 1. The release end: only pull requests closed by the dump are in it, so the newest months lose the slow ones.
        recent = created >= pd.Timestamp("2018-06-01")
        by_month = (
            pd.DataFrame(
                {"opened": created[recent].dt.strftime("%Y-%m"), "merged": merged[recent], "days": days[recent]}
            )
            .groupby("opened")
            .agg(
                rows=("merged", "size"),
                merged_share=("merged", "mean"),
                decided_after_30_days=("days", lambda d: (d > 30).mean()),
                decided_after_180_days=("days", lambda d: (d > DECIDED_WITHIN_DAYS).mean()),
            )
            .round(4)
        )
        # 2. What the cut-off leaves out: the 2016 cohort (2.4+ years of follow-up), cut the way a later month is.
        cohort = created.dt.year == 2016
        rate = merged[cohort].mean()
        cut_rows = []
        for limit in (150, 180, 240, 365):
            kept = cohort & (days <= limit)
            cut_rows.append(
                {
                    "decided within (days)": limit,
                    "share of the 2016 cohort left out": round(1 - kept.sum() / cohort.sum(), 4),
                    "merged share of those left out": round(merged[cohort & ~kept].mean(), 4),
                    "merged share kept minus all": round(merged[kept].mean() - rate, 4),
                }
            )
        # 3. The source's merge rates against the rebuilt ones, on the shipped rows.
        frame = raw[["project_id", "creator_id", "pr_succ_rate", "requester_succ_rate"]].assign(
            created_at=created, closed_at=closed, merged_flag=merged
        )
        project = _history_rates(frame, ["project_id"], "rebuilt_project", "n_project")
        requester = _history_rates(frame, ["project_id", "creator_id"], "rebuilt_requester", "n_requester")
        opened_before = frame.groupby(["project_id", "creator_id"])["created_at"].rank(method="min") - 1
        shipped = (created < LAST_OPENED) & (days <= DECIDED_WITHIN_DAYS)
        y = merged[shipped]
        auc_rows = []
        for name, values in [
            ("pr_succ_rate (source)", frame["pr_succ_rate"]),
            ("pr_succ_rate_at_open (rebuilt)", project["rebuilt_project"]),
            ("requester_succ_rate (source)", frame["requester_succ_rate"]),
            ("requester_succ_rate_at_open (rebuilt)", requester["rebuilt_requester"]),
        ]:
            auc_rows.append(
                {
                    "rate": name,
                    "ROC AUC alone (missing lowest)": round(roc_auc_score(y, values[shipped].fillna(-1)), 4),
                    "missing": int(values[shipped].isna().sum()),
                }
            )
        still_open = (opened_before - requester["n_requester"])[shipped] > 0
        auc_rows.append(
            {
                "rate": "rows whose contributor had an earlier pull request of the release still open at the opening",
                "ROC AUC alone (missing lowest)": None,
                "missing": f"{still_open.mean():.1%} ({int(still_open.sum()):,} rows)",
            }
        )
        return [
            Decision(
                "Pull requests opened by November 2018 and decided within 180 days",
                "The release holds only pull requests closed by the GHTorrent dump of 2019-06-01, so each recent "
                "month lacks its slowest pull requests, which are merged less often: the merged share rises and the "
                "share decided after 30 days falls from December 2018 on. We keep the pull requests decided within "
                "180 days of opening, opened before 2018-12-01, so every month holds the same population.",
                by_month,
            ),
            Decision(
                "What the 180-day window leaves out",
                "The 2016 cohort, followed for at least 2.4 years, cut as a month near the release end would be: "
                "the pull requests decided after 180 days are 3.3% of it and merged less than half the time, so "
                "without a common window the last test months would read about 1.4 points more merged.",
                pd.DataFrame(cut_rows),
            ),
            Decision(
                "Merge rates rebuilt from decisions made before the opening",
                "The source counts every earlier pull request that was ever merged, also those still open when this "
                "one was opened, and counts merges by Gousios's heuristics. The rebuilt rates use the label's own "
                "definition and only decisions made before the opening.",
                pd.DataFrame(auc_rows),
            ),
        ]
