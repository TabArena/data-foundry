"""Curated dataset definition for `seismic_bumps` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    FeatureTypes,
    Metric,
    Source,
    TaskSummary,
    Temporal,
    TemporalSplits,
    decode,
    drop_columns,
)
from scipy.io import arff

# The hazard assessments' codes in the words of the ARFF header, lowest level first (CLEAN-12, CLEAN-14).
HAZARD_LEVELS = ["lack of hazard", "low hazard", "high hazard", "danger state"]
HAZARD_CODES = dict(zip(["a", "b", "c", "d"], HAZARD_LEVELS, strict=True))
CODE_LABELS = {
    "seismic": HAZARD_CODES,
    "seismoacoustic": HAZARD_CODES,
    "ghazard": HAZARD_CODES,
    "shift": {"W": "coal-getting", "N": "preparation"},
}


class SeismicBumps(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a high-energy seismic bump (10^4 J or more) occur at a coal-mine longwall in the next shift?",
        use_case=(
            "For example, the mine's rock-burst prevention service assesses the seismic hazard of a longwall at the end "
            "of each 8-hour shift and, where it expects a strong bump in the next one, orders destress blasting or "
            "withdraws the crew from the threatened area (the source's stated use)."
        ),
        row=(
            "One 8-hour shift at a longwall of a Polish hard-coal mine, summarised by its monitoring systems (2,578 "
            "shifts in shift order after six copied rows are dropped; the file has no dates, and the shifts come from "
            "two longwalls without a longwall id)."
        ),
        predicted=(
            "Whether any seismic bump of 10^4 J or more is registered in the next shift (6.6% of shifts), known when "
            "that shift ends."
        ),
        known=(
            "The shift just ended: whether it was a coal-getting or a preparation shift, the hazard ratings of the "
            "seismic, seismoacoustic and most active geophone's methods, that geophone's energy and pulse count and "
            "their deviations from the eight shifts before, and the number and energy of the bumps registered by "
            "energy band."
        ),
        split=(
            "Later shifts: 15 test windows of 84 consecutive shifts (four weeks of the 21-shift week measured in the "
            "file) over the newest half, each trained on all earlier shifts."
        ),
        changes=(
            "We drop six rows that repeat the two shifts before them, and three bump counts (10^6 J and above) that "
            "are zero in every shift; the codes of the hazard ratings and the shift type become their words."
        ),
        fit="approximate",
        fit_reason=(
            "Later shifts are tested on earlier ones, but the order is rebuilt without dates, the two longwalls cannot "
            "be told apart, and the monthly refit cadence is our assumption (a daily refit did not beat it). The "
            "target is a proxy: a bump of 10^4 J or more stands for raised seismic activity, not a rockburst."
        ),
    )

    # Dataset
    unique_name = "seismic_bumps"
    domain = "industry & manufacturing"
    sources = (
        Source(
            role="publication",
            platform="UCI",
            url="https://doi.org/10.24432/C5W902",
            license="CC BY 4.0",
            year="2013",
            bibtex="""
                @article{sikora2010application,
                  title={Application of rule induction algorithms for analysis of data collected by seismic hazard monitoring systems in coal mines},
                  author={Sikora, Marek and Wr{\\'o}bel, {\\L}ukasz},
                  journal={Archives of Mining Sciences},
                  volume={55},
                  number={1},
                  pages={91--114},
                  year={2010}
                }
            """,
        ),
    )
    data_tags = ()
    download_description = """
        We download the ARFF file from the UCI repository (dataset 266); the zip holds only seismic-bumps.arff.

        wget https://archive.ics.uci.edu/static/public/266/seismic+bumps.zip && unzip seismic+bumps.zip && rm seismic+bumps.zip
        mkdir -p local-data-warehouse/seismic_bumps && mv seismic-bumps.arff local-data-warehouse/seismic_bumps/
    """
    curation_comments = """
        We start with seismic-bumps.arff from UCI (2,584 shifts, 18 features and the class; the release's only file).

        - Prediction point: the end of a shift. Its features summarise that shift (the ARFF header's "previous shift"
          is the shift before the prediction), and the label is a bump of 10^4 J or more in the next shift (ARFF
          header; Sikora & Wrobel 2010, Archives of Mining Sciences 55(1), Sec. 2.1, prediction horizon one shift).
        - Shift order: the file has no dates or shift numbers, but its order is the shift order: row t's label equals
          "row t+1 registered a bump of 10^4 J or more" (`nbumps4` to `nbumps89` above zero, equally `maxenergy` of
          10^4 J or more) in 2,583 of 2,583 consecutive pairs (SPLIT-22). That proves the rows are adjacent shifts; the
          calendar is shown only for rows 150-905, where the shift types follow a 21-row week (18 coal-getting and 3
          preparation shifts, three shifts a day; autocorrelation of the preparation flag 0.37 at lag 21). We keep the
          file position as `shift_order` before any row is dropped and split on it. It is no model input
          (`Temporal(..., time_of="label")`): it is a row's place in an exported file, not a date the service holds,
          as for wine_quality and labour_inspection_compliance.
        - Six rows are copies of the two shifts before them (rows 89-90, 972-973 and 1017-1018 of the file repeat rows
          87-88, 970-971 and 1015-1016 in every column, all without a bump). Two consecutive real shifts cannot repeat
          the geophone's energy, pulses and their 8-shift deviations exactly, so they are export copies; we drop the
          second copy (LEAK-19). The shift-order check holds after the drop (2,577 of 2,577 pairs); no positive is
          lost (170 of 2,578, 6.6%).
        - `nbumps6`, `nbumps7` and `nbumps89` (bumps of 10^6 J and above) are zero in every shift: dropped as
          constant. `nbumps4` and `nbumps5` stay: they and `maxenergy` record bumps of the class's energy in the
          shift just ended, which the service knows when it predicts the next one.
        - Codes decoded to the header's words (CLEAN-12): the hazard ratings `seismic`, `seismoacoustic` and
          `ghazard` (a lack of hazard, b low hazard, c high hazard, d danger state; ordered, CLEAN-14; d never occurs)
          and `shift` (W coal-getting, N preparation).
        - Two longwalls: the header says the data come from two longwalls of the mine; the file has no longwall id and
          the shift-order check runs through the whole file, so the two are not separable. The geophone energy drops
          about ninefold near rows 350-390 and fourfold near rows 720-740, and rows 906-1104 are 199 consecutive
          preparation shifts at low energy, most likely a move of the face between the two longwalls (not confirmed by
          the source); every test window lies after them, where the bump rate is about a quarter of the earlier one
          (116 of the 170 bumps fall before row 906). The paper's data (1,961 shifts of longwalls SC508 and
          SC503, threshold 5 x 10^5 J) differ from this later export (Lennart's CC of 2026-09-30).
        - Potential leak, kept on purpose: inside a test window, a test row's label is the next test row's bump count
          and energy (83 of every 84 test rows; reading the next row scores ROC AUC 1.000 in every window). The rows
          reach a method in shift order (temporal tasks are sorted by their time column). Protocol (LEAK-9): each test
          shift is predicted from the training rows and its own features only; no feature or model step may use other
          test rows, and a method that reads them is called out and not benchmarked.
        - The target (CLEAN-25): `class` renamed to `bump_next_shift`, "Yes" (1, a hazardous state) the event.
        - Metric: the UCI page names none; the ARFF header reports accuracy, balanced accuracy, specificity and
          sensitivity side by side for 14 classifiers under stratified 10 x 10 cross-validation, each at its own
          default threshold, with no threshold or costs fixed (MET-5, MET-6). The full text of Sikora & Wrobel 2010
          was not reachable (journal archive and BazTech); `roc_auc` is the binary fallback (MET-8).
        - Better data for the same task may exist: `aaia16_coal_mine_seismic_hazard` (AAIA'16 challenge, screened in
          its own record).
    """

    # Task
    target = "bump_next_shift"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason=(
            "The UCI page (dataset 266) names no metric. The ARFF header's results table reports accuracy, balanced "
            "accuracy, specificity and sensitivity side by side for 14 classifiers (stratified 10 x 10 CV), each at its "
            "default threshold, with no threshold or cost matrix fixed: no unique, deliberate metric (MET-5, MET-6). "
            "The full text of Sikora & Wrobel 2010 (Archives of Mining Sciences 55(1)) could not be retrieved. "
            "roc_auc is the binary fallback (MET-8); the same authors chose AUC for the same shift-level decision in "
            "the AAIA'16 challenge (Janusz et al. 2016, FedCSIS, doi 10.15439/2016F560)."
        ),
    )

    # Splits
    splits_comment = """
        Leaf (SPLIT-36): Database Snapshot -> new cases that arrive one by one -> the arrival order rebuilt from the
        data and checked (the file order; each row's label equals the next row's recorded bump in 2,577 of 2,577
        pairs) -> at least three windows of the use case's size -> Temporal · rebuilt order. The bump rate moves
        strongly along the order (positives per tenth of the shipped rows 11, 72, 33, 2, 3, 8, 15, 8, 11, 7), so later shifts
        are tested on earlier ones; another mine or a new longwall's first weeks stay untested. Each test window is a run
        of 84 consecutive shifts (`shift_order`), trained on every earlier shift (SPLIT-11); the windows walk back from
        the newest and do not overlap (Andrej, 2026-11-20). Window length (SPLIT-12): four weeks of
        the file's measured week, a monthly refit of the service's model (Andrej, 2026-11-20). The
        shift types of rows 150-905 follow a 21-row week (18 coal-getting and 3 preparation shifts, three a day;
        autocorrelation of the preparation flag 0.37 at lag 21, 0.38 at lag 84), so four weeks are 84 shifts; the cycle
        is not visible after row 1105, where the test windows lie. The source states no refit cadence; the monthly
        cadence remains our assumption (Andrej, 2026-11-20): within each of the 15 windows,
        a model refit every day (every 3 shifts) on all earlier shifts did not beat the window's model (ROC AUC refit
        better in 3-8 of 15 windows per model, worse on average for logistic regression and Kumo-Tabular; log loss
        better in 10 of 15, p 0.14-0.33, not significant). With no dates there is no season or month to choose between, so the windows walk back
        (SPLIT-15). Target: 30 windows (SPLIT-33 for two thirds of 2,578 shifts); 15 are reached: 84-shift windows
        within the newest half (1,289 shifts) fit 15 times. What stops more: the window length and the 50% floor
        (SPLIT-14). Every window holds a bump (1 to 10, 49 in all; TP-9, SPLIT-16), and each trains on 51.1% to 96.7%
        of the shifts. No gap: the label (a bump in the next
        shift) is known when that shift ends, which is the prediction point of the next row, so the label of the
        last training row is known when the first test row is rated (one step of the order, SPLIT-10). `shift_order`
        orders the split and is no input. Protocol (LEAK-9): each test shift is predicted from the training rows and its
        own features only; a method that reads other test rows (whose next row holds a row's label) is called out.
    """
    temporal = Temporal(
        on="shift_order",
        time_of="label",
        splits=TemporalSplits(window=84, unit="rows", min_train_fraction=0.5),
    )
    accepted_check_warnings = {
        "splits_below_target": (
            "15 of the 30 windows an IID split of this size would get: windows of four weeks (84 shifts) fit 15 times "
            "within the newest half, so the window length and the 50% training floor stop more; overlapping windows "
            "are not used, so each test shift is scored once (Andrej, 2026-11-20)."
        ),
    }

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        data, _ = arff.loadarff(raw_dir / "seismic-bumps.arff")
        df = pd.DataFrame(data)
        for col in df.columns:
            if df[col].dtype == object:
                df[col] = df[col].str.decode("utf-8")
        # the file position is the shift order (see the curation notes); kept before any row is dropped
        df["shift_order"] = range(len(df))
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # 1. Six export copies: rows that repeat the two shifts before them in every column (LEAK-19); the first
        #    copy stays. `shift_order` differs between copies, so compare the source's columns.
        source_cols = [c for c in df.columns if c != "shift_order"]
        df = df[~df.duplicated(subset=source_cols, keep="first")]
        # 2. Bump counts of 10^6 J and above: zero in every shift.
        df = drop_columns(df, ["nbumps6", "nbumps7", "nbumps89"])
        # 3. Codes to the ARFF header's words (CLEAN-12); the target's classes in words (CLEAN-25).
        df = decode(df, CODE_LABELS)
        df = df.rename(columns={"class": self.target})
        df = decode(df, {self.target: {"0": "No", "1": "Yes"}})
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=["shift"],
            ordinal=dict.fromkeys(("seismic", "seismoacoustic", "ghazard"), HAZARD_LEVELS),
        )
