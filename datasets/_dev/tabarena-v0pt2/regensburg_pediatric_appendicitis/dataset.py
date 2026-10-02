"""Curated dataset definition for `regensburg_pediatric_appendicitis` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class RegensburgPediatricAppendicitis(AbstractCuratedDataset):
    # Dataset
    unique_name = "regensburg_pediatric_appendicitis"
    year = "2021"
    domain = "medical & healthcare"
    source = "Other"
    source_url = "https://doi.org/10.5281/zenodo.7711412"
    license = "CC-BY-NC-4.0"
    download_description = """
        We get the newest version of the tabular data from Zenodo.


        wget https://zenodo.org/records/7711412/files/app_data.xlsx?download=1
        mkdir -p local-data-warehouse/regensburg_pediatric_appendicitis && mv app_data.xlsx?download=1 local-data-warehouse/regensburg_pediatric_appendicitis/
    """
    bibtex = r"""
        @article{marcinkevivcs2024interpretable,
          title={Interpretable and intervenable ultrasonography-based machine learning models for pediatric appendicitis},
          author={Marcinkevi{\v{c}}s, Ri{\v{c}}ards and Wolfertstetter, Patricia Reis and Klimiene, Ugne and Chin-Cheong, Kieran and Paschke, Alyssia and Zerres, Julia and Denzinger, Markus and Niederberger, David and Wellmann, Sven and Ozkan, Ece and others},
          journal={Medical image analysis},
          volume={91},
          pages={103042},
          year={2024},
          publisher={Elsevier}
        }
    """
    curation_comments = """
        We start with the tabular meta-data used in the paper. We create only one task out of the dataset using one of the three available classes. We note that the main use case of the paper was image-based modelling and comparing to tabular baselines with image-to-tabular-radiometric. The authors also published the tabular data, which we use here.

        - Note, for this dataset is was hard to choose the label given the tabular data. We picked "Severity" in the end. "Diagnosis" is a noisy ground truth for all cases but the ones that had surgery. It was either deterministically determined by the AS score, or during surgery. "Management" reflects the decision and opinion of senior pediatric surgeon. Only "Severity" represents a ground truth as all cases that were server, were either clearly servery or did not even have appendicitis.
         - Warning: We tried to clean the data as good as possible but we suspect it might still contain some features leaking the severity, but we lack the medical expertise to identify them. Thus, I would not be surprised if we had to remove this dataset later again.
        - The data contains string data, but only for a very small number of patients and the text is often seemingly very useless. The features add most likely no value, but we keep them in for the pipeline/model to ignore if needed.
        - We drop the few patients that did not have an ultrasound to avoid them being leaking due to missing features.
    """

    # Task
    target = "Severity"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_excel(raw_dir / "app_data.xlsx?download=1", sheet_name=0)
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Drop samples w/o utrasounds
        df = df[df["US_Performed"] == "yes"]
        df = df.drop(
            columns=[
                # Other
                "US_Performed",  # constant after dropping other cases
                "US_Number",  # rel us_performed
                "Length_of_Stay",  # only available at discharge (so after diagnosis)
                # Other target labels Diagnosis / Management / Severity
                "Diagnosis_Presumptive",
                "Diagnosis",
                "Management",
            ]
        )
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "Sex",
                "Peritonitis",
                "Migratory_Pain",
                "Lower_Right_Abd_Pain",
                "Contralateral_Rebound_Tenderness",
                "Ipsilateral_Rebound_Tenderness",
                "Coughing_Pain",
                "Psoas_Sign",
                "Nausea",
                "Loss_of_Appetite",
                "Dysuria",
                "Stool",
                "Ketones_in_Urine",
                "RBC_in_Urine",
                "WBC_in_Urine",
                "Neutrophilia",
                "Appendix_on_US",
                "Free_Fluids",
                "Appendix_Wall_Layers",
                "Target_Sign",
                "Perfusion",
                "Surrounding_Tissue_Reaction",
                "Pathological_Lymph_Nodes",
                "Bowel_Wall_Thickening",
                "Ileus",
                "Coprostasis",
                "Meteorism",
                "Enteritis",
                "Appendicolith",
                "Perforation",
                "Appendicular_Abscess",
                "Conglomerate_of_Bowel_Loops",
            ],
            string=["Lymph_Nodes_Location", "Abscess_Location", "Gynecological_Findings"],
        )
