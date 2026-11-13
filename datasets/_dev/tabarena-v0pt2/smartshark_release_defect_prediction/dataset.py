"""Curated dataset definition for `smartshark_release_defect_prediction` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, Grouping, Metric, TaskSummary, decode

# The label window: a file counts as defective when a validated bug that was in it at the release is fixed within
# this many days after the release (curation notes, the target bullet).
LABEL_HORIZON_DAYS = 365
# A file's age in days, with the release day, dates the file's birth to the day and so links a file to itself in the
# next release (the review panel's task gamer); ages are kept in whole months and the release by its year.
DAYS_PER_MONTH = 30.4375
# Every project of the source had activity in Jira and Git after this date (the paper's Table 3), so its data runs at
# least to here and a release whose label window closes by then is fully followed up.
FOLLOW_UP_END = pd.Timestamp("2018-01-01")
DATA_DIR = "release-level-data"


class SmartsharkReleaseDefectPrediction(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "Which source files of a new release of a Java project will need a bug fix within a year, for a project "
            "whose own defect history the model has not seen?"
        ),
        use_case=(
            "At a release, the quality-assurance team of an open-source Java project decides which files to review "
            "or test first, from the code, its static-analysis warnings and its recent changes (the source scores "
            "this by the cost of quality assurance against the cost of defects)."
        ),
        row=(
            "One production Java file in one release of one of 38 Apache projects (280 releases from 2005 to 2016; "
            "test files excluded by the source), measured at the release commit."
        ),
        predicted=(
            "Whether a bug that was already in the file at the release, validated by hand as a bug and linked to the "
            "file, was fixed in the file within a year after the release (3.6% of files); for 16.8% of them the bug was "
            "already reported in Jira at the release."
        ),
        known=(
            "About 3,260 measures of the file at the release: code size, complexity and coupling of its "
            "classes and methods with their spread, syntax-tree counts, static-analysis warnings, and the changes, "
            "authors, refactorings and linked issues of the six months before; the release year."
        ),
        split=(
            "Whole projects are held out, all their releases together, so the test data stands for a project whose "
            "defect history the model has never seen, as in the source's own experiment."
        ),
        changes=(
            "We count only bugs fixed within a year of the release, keep the releases whose year closed by 2018 and "
            "not before the project's first linked fix, and drop constant and duplicated measures."
        ),
        fit="approximate",
        fit_reason=(
            "The features are what the project has at the release and the label a validated bug present at it, but "
            "the one-year window is ours, the test projects are always unseen ones and the score pools the files "
            "of several releases where the team ranks one release's files."
        ),
    )

    # Dataset
    unique_name = "smartshark_release_defect_prediction"
    year = "2021"
    domain = "technology & internet"
    source = "Other"  # the authors' Zenodo replication kit, the first release of this data
    source_url = "https://doi.org/10.5281/zenodo.5675024"
    license = "Apache-2.0"  # Zenodo: "All materials are licensed under the Apache 2.0 License (see LICENSE file)"
    download_description = """
        The release-level archive of the authors' replication kit on Zenodo (doi 10.5281/zenodo.5675024, 616 MB, md5 e81b745db794beecfcabd4e8cff14036); the archive DO_NOT_USE_release-level-data.tar.gz (6M-SZZ labels) is not used, as the authors ask.
        mkdir -p local-data-warehouse/smartshark_release_defect_prediction && cd local-data-warehouse/smartshark_release_defect_prediction
        wget -O release-level-data.tar.gz https://zenodo.org/api/records/5675024/files/release-level-data.tar.gz/content
        wget -O README https://zenodo.org/api/records/5675024/files/README/content
        wget -O LICENSE https://zenodo.org/api/records/5675024/files/LICENSE/content
        wget -O Replication-Notebook.ipynb https://zenodo.org/api/records/5675024/files/Replication-Notebook.ipynb/content
        tar xzf release-level-data.tar.gz   # release-level-data/<project>-<version>{_aggregated.csv,.json,_bug_fixes.json}
    """
    bibtex = """
        @article{herbold2022problems,
          title = {Problems with {SZZ} and features: An empirical study of the state of practice of defect prediction data collection},
          author = {Herbold, Steffen and Trautsch, Alexander and Trautsch, Fabian and Ledel, Benjamin},
          journal = {Empirical Software Engineering},
          volume = {27},
          number = {2},
          pages = {42},
          year = {2022},
          doi = {10.1007/s10664-021-10092-4}
        }
    """
    curation_comments = """
        We start with the 398 files `<project>-<version>_aggregated.csv` of release-level-data.tar.gz (the authors' replication kit, IND-JLMIV+R labels), each release dated from its `<project>-<version>.json`: 154,271 file-release rows of 38 projects, 2001-07-14 to 2018-08-17, 4,189 numeric features (the paper says 4,198; the ISSUE block has 63 columns, not 72).

        - Prediction point: the release commit. Static measures are taken on it, change, refactoring and issue counts on the six months before it (Sec. 5.1; the kit's `mynbou` walks back from the release commit), so every feature exists at the release.
        - Target: the source calls a file defective when a bug whose inducing changes all precede the release is fixed after it, however much later (Sec. 4.1). Fixes come late (median 234 days; for releases of 2006-2011, 55% of defective files fixed within a year, 74% within two), so the releases before the 2018-2019 collection lost bugs not yet fixed: 3.5% defective in 2017 and 2.0% in 2018 against 4-9% before (LEAK-24). We count a bug when its fix in the file (the file's own fixing commit from `<release>_bug_fixes.json`; the date in the issue column's name, the issue's last fixing commit, where the JSON has none) falls within 365 days of the release, so every release has the same follow-up. The file's own commit labels 31 more rows defective than the issue's date would (4,074 against 4,043). The label is a bug present at the release and fixed within the year, not one found after it: 16.8% of the defective rows' bugs were already reported in Jira at the release.
        - Cohort: dropped are 56 releases whose year closes after 2018-01-01 (35,390 rows; every project was active after that date, Table 3) and 62 whose year closed before their project's first fix linked to an issue (5,815 rows; 53 Apache Commons releases of 2001-2010, 8 of JSPWiki of 2001-2006, Giraph 0.1.0): no fix of theirs could be recorded (LEAK-25). Left: 113,066 rows, 280 releases of 38 projects, 2005-09-12 to 2016-12-31, 3.6% defective (2.3% to 5.9% by year).
        - Not split by release date: a bug labels a file in every release from its inducing change to its fix, so 2014, 2015 and 2016 windows trained on all earlier releases give 19%, 8% and 22% of their test positives the same file labelled by the same bug in training (SPLIT-9); the one-year gap that removes it leaves 28%, 36% and 53% of the rows for training (SPLIT-14). The split is by project, the source's cross-project design.
        - Dropped: `file` (the path), the release name, `imports` (imported classes, dropped by the source's notebook too; it names the project's own packages), 478 columns constant on the kept rows and 452 exact copies of an earlier column (annotation, enum and interface aggregates that coincide when a file has at most one such member). 3,259 measures and the release year remain; the year is known at the release (USE-6), though the source does not use it.
        - Ages rounded: `MOSER_age` and `MOSER_weighted_age` (days since the file's first and weighted commit) are kept in whole months and the release date by its year (`release_year`). Release day minus age in days dates each file's birth to the day, which links 81% of rows to the same file in the project's next release, whose change and issue counts fall inside the label window: ROC AUC 0.787 to 0.839, up in 9 of 9 splits (review panel's task gamer, LEAK-10). The rounding does not stop the link: matching on the file's syntax-tree and size profile within the project, with the birth month and a later year, still finds a next-release row for 77% of rows and gains 0.046 (0.788 to 0.834, up in 9 of 9 splits; noise 0.002), since unchanged files keep their profile.
        - Protocol (LEAK-9): a method predicts each row from the training rows and that row's own features. Linking a test row to the same file in a later release of its project (whose change, bug-fix and issue counts cover the months after the release, inside the label window) is no feature step: it gains 0.046 ROC AUC, and a method that does it is called out and not benchmarked.
        - Anomaly: the `_gini` aggregates lie in [-2, 0], `mynbou`'s formula (aggregation.py) without the usual scale: -2 for one value, -1 for two values one of them 0 (`SM_method_numpar_gini`, 9.9% of rows). Kept as published.
        - Duplicate rows kept: 2,021 (1.8%) copy another row exactly (distinct small files of one release, median 14 logical lines), 4,332 (3.8%) when the date is left aside (also files unchanged between releases); all copies stay within a project, none crosses a split. 26 rows in 9 groups hold both labels, a real ambiguity (LEAK-18, LEAK-20).
        - Note: size carries most of the signal, as in the defect literature: file size alone (`SM_file_lloc`, logical lines) reaches ROC AUC 0.783 pooled, as untuned LightGBM, and 0.821 averaged within release against 0.811 (261 releases, 9 splits; review panel's claim audit).
        - Note: the `ISSUE_<priority>_<type>` counts read the linked issues' priority and type as Jira held them at collection (2018-2019), not at the release; a change after the release cannot be traced in the kit (a weak LEAK-10; the best single one, `ISSUE_major_bug`, reaches ROC AUC 0.626).
        - Note: `ISSUE_*_improvment` counts issues of the Jira type "wish", the name the source's `mynbou` gives that type (its constants.py); it is not a misspelt "improvement", which has its own columns.
        - Note: 279 release dates for 280 releases, against 398 releases in the kit: the cohort drops 118 releases (56 at the right end, 62 at the left), and `santuario-java-1.0.0` and `santuario-java-1.2` share one release commit date (2010-09-11).
        - Note: better data for `jm1` (NASA MDP, 21 static measures of one C program, 2004), which keeps its verdict; `eclipse_bug_data_zimmermann` is kept for later. SmartSHARK's later database releases cover more projects, but release-level files exist only for these 398 releases.
    """

    # Task
    target = "defect_within_1y"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason=(
            "The paper (Sec. 5.2, 5.9) scores each test release by recall, precision, F1 and the lower and upper "
            "bounds of a cost ratio between quality assurance and defects, with the effort in logical lines of code; "
            "it ranks by no single one, the bounds give a range of cost ratios rather than one, and F1, precision and "
            "recall need a threshold the paper does not fix (Gaussian naive Bayes at its default). The replication "
            "notebook computes the same set"
        ),
    )
    grouping = Grouping(
        on="project",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is an Apache project with all its releases. The source's experiment is cross-project: "We then use all data from projects other than the release for training, the data from the release itself for testing" (Herbold et al. 2022, Sec. 5.9), the setting of a team without defect data of its own. Holding out whole projects also keeps every release of a file on one side: a bug labels a file in every release between its inducing change and its fix, so a file's earlier release in training would hand over the label of its later one. Each row is one prediction, made from that file's measures at its release.
        """,
    )
    splits_comment = """
        Grouped splits on the project: all releases of a project stay on one side, so a model ranks the files of a project whose defect history it has never seen, as in the source's cross-project experiment. The source tests one release at a time and trains on all releases of the other projects; our folds pool several held-out projects, and the paper's filter (releases with at least 100 files and five defective files) is not applied, since a small release is still a decision.
    """
    prepared_raw_files = ("release_level_files.parquet",)

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        # One table of the 398 per-release CSV files, with each release's date (from its JSON) and each file's
        # earliest bug fix: the file's own fixing commit from `<release>_bug_fixes.json`, for the issues the file's
        # columns after `BUGFIX_count` (named `<issue>_<severity>_<fix date>`) mark; the column date (the issue's
        # last fixing commit) where the JSON has no commit for that file.
        frames = []
        for path in sorted((raw_dir / DATA_DIR).glob("*_aggregated.csv")):
            release = path.name.removesuffix("_aggregated.csv")
            df = pd.read_csv(path, sep=";", low_memory=False)
            bugs_at = df.columns.get_loc("BUGFIX_count")
            issues = df.columns[bugs_at + 1 :]
            fixed = pd.to_datetime([name.rsplit("_", 2)[2] for name in issues]).to_numpy(dtype="datetime64[ns]")
            hit = df[issues].to_numpy() > 0
            first = pd.Series(pd.NaT, index=df.index, dtype="datetime64[ns]")
            for j in np.argsort(fixed, kind="stable")[::-1]:  # latest first, so the earliest fix is written last
                first[hit[:, j]] = fixed[j]
            names = np.array([name.rsplit("_", 2)[0] for name in issues])
            per_file = {
                e["file"]: {b["name"]: pd.Timestamp(b["bugfix_commit_date"]) for b in e["bug_fixes"]}
                for e in json.loads((raw_dir / DATA_DIR / f"{release}_bug_fixes.json").read_text())
                if e["bug_fixes"]
            }
            for i in np.flatnonzero(hit.any(axis=1)):
                own = per_file.get(df.at[i, "file"], {})
                dates = [own.get(n, fixed[j]) for j, n in enumerate(names) if hit[i, j]]
                first.iat[i] = min(dates)
            # the JSON ends with `"release_date": "YYYY-MM-DD hh:mm:ss"`; read its tail only (the files hold 4-30 MB)
            with (raw_dir / DATA_DIR / f"{release}.json").open("rb") as fh:
                fh.seek(-300, 2)
                date = re.search(r'"release_date":\s*"([^"]+)"', fh.read().decode()).group(1)
            out = df.iloc[:, : bugs_at + 1].copy()
            out.insert(0, "release", release)
            out.insert(1, "release_date", pd.Timestamp(date))
            out["first_bug_fix"] = first
            frames.append(out)
        pd.concat(frames, ignore_index=True).to_parquet(raw_dir / "release_level_files.parquet")

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_parquet(raw_dir / "release_level_files.parquet")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # 1. The project is the release name without its version (`commons-lang-3.7` -> `commons-lang`).
        df["project"] = df["release"].str.replace(r"-[0-9][^-]*$", "", regex=True)
        # 2. The target: a validated bug in the file at the release, fixed within the horizon after it.
        window_end = df["release_date"] + pd.Timedelta(days=LABEL_HORIZON_DAYS)
        df[self.target] = (df["first_bug_fix"] <= window_end).astype(int)
        # 3. The cohort: the window closes by the end of follow-up, and not before the project's first linked fix.
        recorded_from = df.groupby("project")["first_bug_fix"].transform("min")
        df = df[(window_end <= FOLLOW_UP_END) & (window_end >= recorded_from)]
        # 4. Identifiers, the source's label columns and the imports list leave.
        df = df.drop(columns=["release", "file", "imports", "BUGFIX_count", "first_bug_fix"])
        # 4b. Ages in whole months and the release by its year, so no row dates a file's birth to the day (LEAK-10).
        for col in ("MOSER_age", "MOSER_weighted_age"):
            df[col] = np.floor(df[col] / DAYS_PER_MONTH).astype(int)
        df.insert(df.columns.get_loc("release_date"), "release_year", df["release_date"].dt.year)
        df = df.drop(columns="release_date")
        # 5. Constant and exact-duplicate measures on the kept rows (CLEAN-5), the first of each copy kept.
        features = [c for c in df.columns if c not in (self.target, "project", "release_year")]
        constant = [c for c in features if df[c].nunique(dropna=False) <= 1]
        kept = [c for c in features if c not in constant]
        values = {c: df[c].to_numpy(dtype=float).tobytes() for c in kept}
        seen: dict[bytes, str] = {}
        copies = [c for c in kept if seen.setdefault(values[c], c) != c]
        df = df.drop(columns=constant + copies)
        return decode(df, {self.target: {0: "No", 1: "Yes"}})

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["project"])

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        # The source's label (any later fix) against the one-year label, by release year, and what the cohort keeps.
        year = raw["release_date"].dt.year
        window_end = raw["release_date"] + pd.Timedelta(days=LABEL_HORIZON_DAYS)
        within = raw["first_bug_fix"] <= window_end
        project = raw["release"].str.replace(r"-[0-9][^-]*$", "", regex=True)
        recorded_from = raw["first_bug_fix"].groupby(project).transform("min")
        kept = (window_end <= FOLLOW_UP_END) & (window_end >= recorded_from)
        table = pd.DataFrame(
            {
                "rows": raw.groupby(year).size(),
                "releases": raw.groupby(year)["release"].nunique(),
                "defective, any later fix (source)": (raw["BUGFIX_count"] > 0).groupby(year).mean().round(3),
                "defective, fixed within a year": within.groupby(year).mean().round(3),
                "rows kept": kept.groupby(year).sum(),
                "releases kept": raw.loc[kept, "release"].groupby(year[kept]).nunique(),
                "kept: defective within a year": within[kept].groupby(year[kept]).mean().round(3),
            }
        ).fillna({"releases kept": 0, "kept: defective within a year": "none kept"})
        table.index.name = "release year"
        return [
            Decision(
                "A one-year label window, and the releases followed up for it",
                "The source counts a bug however long after the release it was fixed, so the releases just before "
                "the 2018-2019 collection lose the bugs not yet fixed. Counting fixes within a year gives every "
                "release the same follow-up. Left out: releases whose year closes after 2018-01-01, and releases "
                "whose year closed before the project's first fix linked to an issue (no fix of theirs could be "
                "recorded).",
                table,
            ),
        ]
