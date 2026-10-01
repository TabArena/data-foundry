"""Curated dataset definition for `dementia_prediction` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Grouping


class DementiaPrediction(AbstractCuratedDataset):
    # Dataset
    unique_name = "dementia_prediction"
    year = "2010"
    domain = "medical & healthcare"
    source = "Other"
    source_url = "https://doi.org/10.17632/tsy6rbc5d4.1"
    license = "CC BY NC 3.0"
    data_tags = ("WrongDomain",)
    download_description = """
        We get the data from Mendeley version of another paper (https://www.sciencedirect.com/science/article/pii/S2352914819300917?via%3Dihub).

        wget https://data.mendeley.com/public-files/datasets/tsy6rbc5d4/files/b4978a7c-df15-46b2-be69-891d4935b652/file_downloaded && mv file_downloaded oasis_longitudinal_demographics.xlsx && mkdir -p local-data-warehouse/dementia_prediction && mv oasis_longitudinal_demographics.xlsx local-data-warehouse/dementia_prediction/
    """
    bibtex = """
        @article{marcus2010open,
          title={Open access series of imaging studies: longitudinal MRI data in nondemented and demented older adults},
          author={Marcus, Daniel S and Fotenos, Anthony F and Csernansky, John G and Morris, John C and Buckner, Randy L},
          journal={Journal of cognitive neuroscience},
          volume={22},
          number={12},
          pages={2677--2684},
          year={2010},
        }
    """
    curation_comments = """
        We start with the data from Mendeley.

        - CDR and Group are both the same target variable. CDR is the Clinical Dementia Rating (0 = no dementia, 0.5 = very mild AD, 1 = mild AD, 2 = moderate AD), which determines the group variable. 31 of the 150 subjects change their rating across visits (the 'Converted' group). We make this a task to predict for a patient (at any given time point of a scan) their dementia rating. The rating is ordinal but discrete, so we treat it as a classification problem (not regression). We drop cases with moderate_AD (n=3), as we do not have enough data on this class to include them in our prediction task.
        - We drop the group variable (Nondemented / Demented / Converted, derived from the ratings over the visits) and the time of the scan (visit number, MR delay). We predict each visit's rating from the subject's sex, age, years of education (EDUC), socioeconomic status (SES, 19 missing), the Mini-Mental State Examination score of the same visit (MMSE, 2 missing; a separate cognitive test, not derived from the rating) and three measures from the visit's MRI scan: estimated total intracranial volume (eTIV), normalized whole-brain volume (nWBV) and the atlas scaling factor (ASF, which is 1755 / eTIV, kept as in the source).
        - We also drop the constant hand column.
    """

    # Task
    target = "CDR"
    problem_type = "multiclass_classification"
    grouping = Grouping(
        on="Subject ID",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a subject of OASIS-2: older adults scanned on two or more visits at least a year apart, each visit with its own clinical dementia rating (Marcus et al. 2010). Each visit is one prediction, made from that visit alone, for a subject not seen in training: a first-visit framing, since a follow-up visit would know the earlier ratings. The source defines no prediction task.
        """,
    )

    # Splits
    splits_comment = """
        We create stratified grouped 20-repeated 3-fold split. This creates ca. 50 group members (ca. 120-150 samples) per test set.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_excel(raw_dir / "oasis_longitudinal_demographics.xlsx")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.drop(
            columns=[
                "MRI ID",
                "Visit",
                "MR Delay",  # uninformative time information
                "Group",  # leak
                "Hand",  # constant
            ]
        )
        # 0 = no dementia, 0.5 = very mild AD, 1 = mild AD, 2 = moderate AD)
        df["CDR"] = df["CDR"].replace({0.5: "very_mild_AD", 1: "mild_AD", 2: "moderate_AD", 0: "no_dementia"})
        df = df[df["CDR"] != "moderate_AD"]
        df = df.sample(frac=1, random_state=42).sort_values(by=["Subject ID"], kind="stable").reset_index(drop=True)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["M/F", "Subject ID"])


# MIGRATE: the v1 notebook did not shuffle; v2 shuffles IID/grouped data (set `shuffle = False` if the order matters)
