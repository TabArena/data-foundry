"""Curated dataset definition for `eryhemato_squamous_disease` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, TaskSummary


class EryhematoSquamousDisease(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=("Which of six scaly red skin diseases does a patient have, judged from the clinical examination?"),
        use_case=(
            "A dermatologist examines a patient with red, scaly skin and makes a differential diagnosis among six "
            "similar diseases before taking a biopsy, the first of the source's two steps."
        ),
        row=(
            "One patient diagnosed with one of the six diseases at the Department of Dermatology, Gazi University, "
            "Ankara (366 patients, published 1998; period not stated)."
        ),
        predicted=(
            "The diagnosis: psoriasis (31%), seborrheic dermatitis, lichen planus, pityriasis rosea, chronic "
            "dermatitis or pityriasis rubra pilaris (5%)."
        ),
        known=(
            "Ten clinical findings graded 0 to 3 (redness, scaling, definite borders, itching, the Koebner "
            "phenomenon, polygonal and follicular papules, and involvement of the mouth, knees and elbows, and "
            "scalp), family history and age."
        ),
        split="Random patients.",
        changes=(
            "We drop the 22 findings from the biopsy and keep the clinical examination; with the biopsy the task is "
            "close to solved."
        ),
        fit="approximate",
        fit_reason=(
            "The clinical findings come before the biopsy and the label is the confirmed diagnosis, so the task is "
            "the differential the source describes; it is small and old. The patients look selected (93% of those "
            "with lichen planus have mouth lesions, about half in another clinic's series, and all with pityriasis "
            "rubra pilaris are aged 7 to 22), which makes these two diseases easier to recognise than in a clinic."
        ),
    )

    # Dataset
    unique_name = "eryhemato_squamous_disease"
    year = "1998"
    domain = "medical & healthcare"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5FK5P"
    license = "CC BY 4.0"
    download_description = """
        We take the original data from UCI.

        wget https://archive.ics.uci.edu/static/public/33/dermatology.zip && unzip dermatology.zip && rm dermatology.zip dermatology.names
        mkdir -p local-data-warehouse/eryhemato_squamous_disease && mv dermatology.data local-data-warehouse/eryhemato_squamous_disease/
    """
    bibtex = r"""
        @article{guvenir1998learning,
          title={Learning differential diagnosis of erythemato-squamous diseases using voting feature intervals},
          author={G{\"u}venir, H Altay and Demir{\"o}z, G{\"u}l{\c{s}}en and Ilter, Nilsel},
          journal={Artificial intelligence in medicine},
          volume={13},
          number={3},
          pages={147--165},
          year={1998},
          publisher={Elsevier},
          doi={10.1016/S0933-3657(98)00028-1}
        }
    """
    curation_comments = """
        We start with the data from UCI.

        - We keep only the clinical features: the 10 clinical findings graded 0 to 3, family history and age. The source describes two steps: "Patients were first evaluated clinically with 12 features. Afterwards, skin samples were taken for the evaluation of 22 histopathological features." With the 22 histopathological features the task is close to solved (a logistic model reaches macro ROC AUC 0.999 and 97% accuracy on the shipped splits); the task here is the clinical differential before the biopsy (macro ROC AUC 0.98, 87% accuracy), where seborrheic dermatitis, pityriasis rosea and chronic dermatitis are the hard cases.
        - We encode all features but age as categorical, since they are ordinal features in nature.
        - We ensure missing values in age are encoded as NaN.
        - Note: `class` keeps the source's codes: 1 psoriasis, 2 seborrheic dermatitis, 3 lichen planus, 4 pityriasis rosea, 5 chronic dermatitis, 6 pityriasis rubra pilaris.
        - Note: the patients look selected. 93% of those with lichen planus have mouth lesions, against 56% of 91 biopsy-confirmed patients in another clinic's series (Samreen A, Luqman N, Asgher R, Khalid M, Shaheen JA. Frequency of oral involvement in cutaneous lichen planus patients. J Pak Assoc Dermatol. 2021;31(3):454-458. doi:10.66344/jpad.v31i3.1817). All 20 with pityriasis rubra pilaris are aged 7 to 22, though the disease is most common in adults; the source calls it "a children's disease".
        - Note: one psoriasis patient has age 0, the only patient younger than 7. It may be an infant or a stand-in for an unknown age (the source marks 8 unknown ages with "?"); we keep it.
    """

    # Task
    target = "class"
    problem_type = "multiclass_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        feature_names = [
            "erythema",
            "scaling",
            "definite borders",
            "itching",
            "koebner phenomenon",
            "polygonal papules",
            "follicular papules",
            "oral mucosal involvement",
            "knee and elbow involvement",
            "scalp involvement",
            "family history",
            "melanin incontinence",
            "eosinophils in the infiltrate",
            "PNL infiltrate",
            "fibrosis of the papillary dermis",
            "exocytosis",
            "acanthosis",
            "hyperkeratosis",
            "parakeratosis",
            "clubbing of the rete ridges",
            "elongation of the rete ridges",
            "thinning of the suprapapillary epidermis",
            "spongiform pustule",
            "munro microabcess",
            "focal hypergranulosis",
            "disappearance of the granular layer",
            "vacuolisation and damage of basal layer",
            "spongiosis",
            "saw-tooth appearance of retes",
            "follicular horn plug",
            "perifollicular parakeratosis",
            "inflammatory monoluclear inflitrate",
            "band-like infiltrate",
            "age",
            "class",
        ]
        df = pd.read_csv(raw_dir / "dermatology.data", header=None, names=feature_names)
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        clinical = [
            "erythema",
            "scaling",
            "definite borders",
            "itching",
            "koebner phenomenon",
            "polygonal papules",
            "follicular papules",
            "oral mucosal involvement",
            "knee and elbow involvement",
            "scalp involvement",
            "family history",
            "age",
        ]
        df = raw[[*clinical, self.target]].copy()
        df["age"] = df["age"].replace("?", np.nan).astype(float)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # age is numeric, and has some missing values
        return FeatureTypes(categorical=[c for c in df.columns if c not in ("age", self.target)])
