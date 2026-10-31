"""Curated dataset definition for `regensburg_pediatric_appendicitis` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, TaskSummary, set_missing

# The ordinal scales, lowest level first, from the source's codebook (curation notes; the README lists
# them). An open-ended level holds everything beyond it.
ORDINAL_LEVELS = {
    "Ketones_in_Urine": ["no", "+", "++", "+++"],
    "RBC_in_Urine": ["no", "+", "++", "+++"],
    "WBC_in_Urine": ["no", "+", "++", "+++"],
    "Peritonitis": ["no", "local", "generalized"],
    "Appendicolith": ["no", "suspected", "yes"],
    "Perforation": ["no", "not excluded", "suspected", "yes"],
    "Appendicular_Abscess": ["no", "suspected", "yes"],
    "Appendix_Wall_Layers": ["intact", "partially raised", "raised"],
    "Perfusion": ["no", "hypoperfused", "present", "hyperperfused"],
}


class RegensburgPediatricAppendicitis(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Is a child's appendicitis complicated (gangrenous, perforated or abscessed)?",
        use_case=(
            "For example, a paediatric surgeon, after the examination, blood tests and ultrasound of a child with "
            "suspected appendicitis, judges how severe it is, to choose between surgery and conservative treatment."
        ),
        row=(
            "One child admitted with abdominal pain and suspected appendicitis to the Children's Hospital St. Hedwig "
            "in Regensburg, Germany, 2016-2021, who had an ultrasound (763 children)."
        ),
        predicted=(
            "Whether the appendicitis was complicated (15.07%); the rest, among them children without appendicitis, "
            "count as uncomplicated."
        ),
        known=(
            "Age, sex, height and weight, symptoms and examination signs, body temperature, blood and urine tests, "
            "two clinical appendicitis scores, and the ultrasound findings (appendix diameter, free fluid, wall "
            "layers, perfusion, signs of perforation or abscess, and others)."
        ),
        split=("Random children, so the test data stands for other children of the same hospital and years."),
        changes=(
            "We keep the children who had an ultrasound and drop the diagnosis, the surgeon's management decision and"
            " the length of stay."
        ),
        fit="approximate",
        fit_reason=(
            "The features are known at the decision, but the curators suspect some of them leak the severity and "
            "could not rule it out; ultrasound signs of perforation or abscess come close to the label's own "
            "definition. How severity was set for children not operated on is not stated."
        ),
    )

    # Dataset
    unique_name = "regensburg_pediatric_appendicitis"
    year = "2023"
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

        - The data first appeared on Zenodo (v1.0, 2023-02-23, five days before the paper's preprint), hence source
          Other; UCI 938 is a copy that names the Zenodo DOI as its source.
        - Note, for this dataset is was hard to choose the label given the tabular data. We picked "Severity" in the end. "Diagnosis" is a noisy ground truth for all cases but the ones that had surgery. It was either deterministically determined by the AS score, or during surgery. "Management" reflects the decision and opinion of senior pediatric surgeon. Only "Severity" represents a ground truth as all cases that were server, were either clearly servery or did not even have appendicitis.
         - Warning: We tried to clean the data as good as possible but we suspect it might still contain some features leaking the severity, but we lack the medical expertise to identify them. Thus, I would not be surprised if we had to remove this dataset later again.
        - The data contains string data, but only for a very small number of patients and the text is often seemingly very useless. The features add most likely no value, but we keep them in for the pipeline/model to ignore if needed.
        - We drop the few patients that did not have an ultrasound to avoid them being leaking due to missing features.
        - Ordinal scales (2026-10-30, the curator's marks of 2026-10-31, CLEAN-14): 9 columns are ordered categories in
          the order of the source's codebook (`ORDINAL_LEVELS`).
        - `Appendix_Wall_Layers` (2026-10-31, CLEAN-14): the codebook's "regular / irregular" (Zenodo Data Summary); the
          labels translate the German record of the 2021 release (intact = intakt, raised = aufgehoben, the layering
          lost; partially raised = partly lost), so intact < partially raised < raised. `upset` (1 child) is irregular
          in the authors' code but of unknown degree: missing.
        - `Perfusion` (2026-10-31, CLEAN-14): the codebook's scale is the amount of blood flow (unremarkable /
          hypoperfused / hyperperfused), but this file has no `unremarkable`: the 16 children linked to the 2021
          release with `unremarkable` are blank here, so a blank also means unremarkable. `no` (no flow, 3 children)
          and `present` (flow without a grade, 1) are not in the codebook; ordered by flow as no < hypoperfused <
          present < hyperperfused, `present`'s place is our reading (the authors' code groups `no` with hypoperfused
          and `present` with hyperperfused).
    """

    # Task
    target = "Severity"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason=(
            "Marcinkevics et al. 2024 report AUROC and AUPR side by side per target; neither is named as the "
            "criterion. roc_auc is the binary fallback."
        ),
    )

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
        # irregular wall layers of unknown degree, off the scale (CLEAN-14)
        df = set_missing(df, {"Appendix_Wall_Layers": ["upset"]})
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            ordinal=ORDINAL_LEVELS,
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
