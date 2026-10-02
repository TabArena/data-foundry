"""Curated dataset definition for `cardiotocography` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Grouping, anonymize_ids


class Cardiotocography(AbstractCuratedDataset):
    # Dataset
    unique_name = "cardiotocography"
    year = "2010"
    domain = "medical & healthcare"
    source = "UCI"
    source_url = "10.24432/C51S4N"
    license = "CC BY 4.0"
    download_description = """
        wget https://archive.ics.uci.edu/static/public/193/cardiotocography.zip && unzip cardiotocography.zip && rm cardiotocography.zip && mkdir -p local-data-warehouse/cardiotocography && mv CTG.xls local-data-warehouse/cardiotocography
    """
    bibtex = """
        @misc{campos2010cardiotocography,
          author       = {Campos, D. and Bernardes, J.},
          title        = {{Cardiotocography}},
          year         = {2000},
          howpublished = {UCI Machine Learning Repository},
          note         = {{DOI}: https://doi.org/10.24432/C51S4N}
        }
    """
    curation_comments = """
        We use the data from UCI and the 3 class problem of predicting NSP as it is more medical relevant.

        - We transform the file names into patient IDs to indicate the sub-group of samples recorded from the same patient.
        - Each row is a segment (sample `b` to `e`) of one exam file, and 1,706 of the 1,774 consecutive segment pairs within a file overlap, so the rows of a file must stay together. The patient ID above the file is our guess, no source documents it: we strip the trailing number of a named file (`Aast_1` ... `Aast_14` -> `Aast`), each numbered file (`S0001027.dat`) stays alone. This gives 176 IDs for 352 files; 61 IDs merge 2 to 14 files and 10 span exam dates 50 to 1,139 days apart, so a stem is likely initials and may hold two women or two pregnancies. Merging too much only makes the split stricter; a woman under two IDs (similar stems such as `Mcslr`/`Mcslrc`, or a numbered file) would put her separate exams on both sides, but never overlapping segments.
        - The raw data has dates and the start and end index of the recording. We drop these as they are not relevant for the predictive task and would not be available for test samples.
        - We drop all other columns that represent the label.
    """

    # Task
    target = "NSP"
    problem_type = "multiclass_classification"
    grouping = Grouping(
        on="patient_id",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a patient, as far as the file names identify one; its rows are segments of her CTG exams, each classified by three expert obstetricians (UCI). Each segment is one prediction, made from that segment alone. The segments of one exam overlap, so an exam's rows must stay together; the patient key above the exam is a heuristic on the file names (curation notes).
        """,
    )

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
        df["FileName"] = (
            df["FileName"]
            .str.replace(r"\.[^.]+$", "", regex=True)
            .pipe(lambda s: s.where(s.str.fullmatch(r"S\d+"), s.str.replace(r"(_?\d+)$", "", regex=True)))
        )
        # stable anonymous ids (random uuid4 ids changed the data and the grouped splits on every run)
        df["patient_id"] = anonymize_ids(df["FileName"])
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
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "patient_id",
            ],
        )
