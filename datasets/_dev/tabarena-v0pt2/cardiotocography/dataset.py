"""Curated dataset definition for `cardiotocography` (data-foundry v2). Evidence: README.md."""

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
)

# The ordinal scales, lowest level first, from the source's codebook (curation notes; the README lists
# them). An open-ended level holds everything beyond it.
ORDINAL_LEVELS = {
    "Tendency": ["left asymmetric", "symmetric", "right asymmetric"],
    "NSP": ["normal", "suspect", "pathologic"],
}


# The codebook's words for coded columns, decoded in `_clean` after the codes that mean unknown are missing
# (CLEAN-12; the curator's rule of 2026-11-01).
CODE_LABELS = {
    "Tendency": {"-1": "left asymmetric", "0": "symmetric", "1": "right asymmetric"},
}


class Cardiotocography(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=("Is the fetal state in a segment of a fetal heart-rate recording normal, suspect or pathologic?"),
        use_case=(
            "For example, during fetal monitoring, software flags the recording segments that expert obstetricians "
            "would call suspect or pathologic, so that a clinician looks at them."
        ),
        row=(
            "One segment of a fetal cardiotocography exam (fetal heart rate and uterine contractions): 2,070 segments"
            " of 335 exam files from January 1995 to June 1998, overlapping within an exam. The place is not stated in"
            " the definition."
        ),
        predicted=(
            "The fetal state three expert obstetricians agreed on: normal (78%), suspect (14%) or pathologic (8%)."
        ),
        known=(
            "Measures computed automatically from the segment: baseline heart rate, accelerations, fetal movements, "
            "contractions, four kinds of decelerations, short- and long-term variability, and the shape of the "
            "heart-rate histogram."
        ),
        split=(
            "Later exams are held out: three nine-month windows from October 1996 to June 1998, each trained on all "
            "earlier exams, as monitoring software trained on past exams meets new ones. An exam's segments share its "
            "date, so they stay on one side."
        ),
        changes=(
            "We keep the exam date and split by it, and drop the 56 segments whose date is an unset clock (1980). We "
            "drop the file names, the segment positions, the constant column DR, the 10-class pattern label and the "
            "other expert labels."
        ),
        fit="direct",
        fit_reason=(
            "The measures come from the segment itself and the label is the experts' reading of it, as a monitoring "
            "aid would see them. The label is a judgement, not the baby's outcome, and its class mix changes between "
            "1996 and 1997 (suspect 14% to 1%, pathologic 4% to 13%) for a reason the source does not give, so the "
            "newest windows test a shift."
        ),
    )

    # Dataset
    unique_name = "cardiotocography"
    domain = "medical & healthcare"
    sources = (
        Source(
            role="publication",
            platform="UCI",
            url="https://doi.org/10.24432/C51S4N",
            license="CC BY 4.0",
            year="2010",
            bibtex="""
                @misc{campos2010cardiotocography,
                  author       = {Campos, D. and Bernardes, J.},
                  title        = {{Cardiotocography}},
                  year         = {2000},
                  howpublished = {UCI Machine Learning Repository},
                  note         = {{DOI}: https://doi.org/10.24432/C51S4N}
                }
            """,
        ),
    )
    download_description = """
        wget https://archive.ics.uci.edu/static/public/193/cardiotocography.zip && unzip cardiotocography.zip && rm cardiotocography.zip && mkdir -p local-data-warehouse/cardiotocography && mv CTG.xls local-data-warehouse/cardiotocography
    """
    curation_comments = """
        We use the data from UCI and the 3 class problem of predicting NSP as it is more medical relevant.

        - Each row is a segment (sample `b` to `e`) of one exam file, and 1,706 of the 1,774 consecutive segment pairs within a file overlap, so the rows of a file must stay together. Each file has one exam date, so a split by date keeps them together.
        - Split by exam date (2026-11-11, Andrej; SPLIT-32, SPLIT-14): the "Raw Data" sheet dates every exam, January 1995 to June 1998, and the labels shift between 1996 and 1997 (suspect 14% to 1% of the segments, pathologic 4% to 13%). Monitoring software meets later exams, so we keep `Date` as `exam_date` and test three nine-month windows (details in the splits comment). Trained on earlier exams, untuned LightGBM's log loss on the two newest windows is 1.825 and 1.608, against 0.498 and 0.444 when trained on as many segments of all years (Slurm job 1365902). Whether the shift lies in the experts' reading, in which exams were sent, or in the program's measures is not documented.
        - 56 segments of 17 files (name stems `Mrsa`, `Moar`, `Mag`, `Caft`, `Cs`) carry the date 1980-01-04, an unset clock; we drop them, since they have no usable date.
        - The earlier split by a patient key inferred from the file names (176 keys for 352 files) is replaced by the date split, and the key leaves the frame. An earlier exam of a test segment's patient stem is in training for 20% of the oldest window's segments and 0% to 1% of the other two; files merged under one stem agree on the label no more than chance (55% against 57%), so this leaks nothing.
        - We drop the start and end index of the segment within the recording, which describe the file, not the fetal state.
        - `DR` (repetitive decelerations) is 0 in every row, so we drop it (constant column).
        - We drop all other columns that represent the label.
        - Ordinal scales (2026-10-30, the curator's marks of 2026-10-31 and 2026-11-01, CLEAN-14): 1 column is ordered
          categories in the order of the source's codebook (`ORDINAL_LEVELS`); 1 of them decoded from the source's codes
          into its words (`CODE_LABELS`, 2026-11-01).
        - Codes decoded (2026-11-01, CLEAN-12, CLEAN-14; the curator's rule: a code whose codebook says in words what
          each level is carries the words, a score without them is a number): 1 ordered codes carry their codebook's
          words (`CODE_LABELS`), in the same order.
        - The target (2026-11-01, CLEAN-25): `NSP` ships its classes as words, normal < suspect < pathologic (CTG.xls,
          sheet Description: 'NSP | Normal=1; Suspect=2; Pathologic=3').
    """

    # Task
    target = "NSP"
    problem_type = "multiclass_classification"
    metric = Metric.fallback(
        reason=(
            "UCI page defines no task metric; the SisPorto 2.0 paper describes the analysis program and "
            "expert agreement, not a prediction benchmark."
        ),
    )
    temporal = Temporal(
        on="exam_date",
        splits=TemporalSplits(window=9, unit="months", cutoffs=("1996-10-01", "1997-07-01", "1998-04-01")),
    )
    splits_comment = """
        Monitoring software trained on past exams meets later ones: three test windows of nine months by exam date, newest first, April to June 1998 (224 segments of 14 files; normal 182, suspect 5, pathologic 37), July 1997 to March 1998 (305 segments of 26 files; normal 255, suspect 0, pathologic 50) and October 1996 to June 1997 (307 segments of 27 files; normal 252, suspect 46, pathologic 9). Each trains on all earlier dated exams, 89%, 74% and 60% of the 2,070 segments, without a gap: the label is the experts' reading of the stored trace, available when the exam is classified. The exams fall on 47 dates; the windows hold 9, 9 and 4 of them, and the newest ends early, because the data ends on 1998-06-06. The labels shift between 1996 and 1997 (suspect 14% to 1%, pathologic 4% to 13%), so the newest windows hold few or no suspect segments and largely test the shift: untuned LightGBM's log loss is 1.825 and 1.608 on the two newest windows, against 0.498 and 0.444 trained on as many segments of all years (Slurm job 1365902). An exam's segments overlap and share its date, so they stay on one side.
    """
    accepted_check_warnings = {
        "meta_time_horizon_mismatch": "The exams fall on 47 dates and the data ends on 1998-06-06, so the newest "
        "nine-month window (from 1998-04-01) holds exams of 6 April to 6 June 1998 only; the windows are nine "
        "calendar months.",
        "splits_test_class_missing": "The July 1997 to March 1998 window holds no suspect segment (normal 255, "
        "pathologic 50): the experts' suspect share falls from 14% of the segments in 1996 to 1% in 1997, the shift "
        "the date split is chosen to test (2026-11-11, Andrej). Every train side holds all three classes, and log "
        "loss is defined on the classes a fold holds.",
    }

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        # Read excel file
        df = pd.read_excel(raw_dir / "CTG.xls", sheet_name="Raw Data")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # -- Remove rows that are not data rows from Excel sheet
        # Drop first row, which is missing in the Excel sheet
        df = df.drop(index=0).reset_index(drop=True)
        # Drop last three rows as they are also corrupted
        df = df.drop(index=df.index[-3:]).reset_index(drop=True)
        # the exam date is the time column; 1980-01-04 is an unset clock (56 segments of 17 files), no usable date
        df["exam_date"] = pd.to_datetime(df["Date"])
        df = df[df["exam_date"] != pd.Timestamp("1980-01-04")].reset_index(drop=True)
        df = df.drop(
            columns=[
                "FileName",
                # Duplicat of LB
                "LBE",
                # Non-feature information
                "b",
                "e",
                "Date",
                "SegFile",
                # constant (0 in every row)
                "DR",
                # Classes
                "A",
                "B",
                "C",
                "D",
                "E",
                "AD",
                "DE",
                "LD",
                "FS",
                "SUSP",
                "CLASS",
            ]
        )
        # the codebook's words for its codes (CLEAN-12)
        df = decode(df, CODE_LABELS)
        # the target's classes in words (CLEAN-25): the source's class names
        df = decode(df, {self.target: {"1": "normal", "2": "suspect", "3": "pathologic"}})
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            ordinal=ORDINAL_LEVELS,
            datetime=["exam_date"],
        )
