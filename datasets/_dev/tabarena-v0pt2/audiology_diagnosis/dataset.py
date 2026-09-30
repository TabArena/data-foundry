"""Curated dataset definition for `audiology_diagnosis` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset


class AudiologyDiagnosis(AbstractCuratedDataset):
    # Dataset
    unique_name = "audiology_diagnosis"
    year = "1987"
    domain = "medical & healthcare"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5TP4R"
    license = "CC BY 4.0"
    download_description = """
        We get the data from UCI.
        wget https://archive.ics.uci.edu/static/public/8/audiology+standardized.zip && unzip audiology+standardized.zip && rm audiology+standardized.zip audiology.standardized.names && mkdir -p local-data-warehouse/audiology_diagnosis && mv audiology.standardized.data audiology.standardized.test local-data-warehouse/audiology_diagnosis/
    """
    bibtex = """
        @incollection{bareiss1990protos,
          title={Protos: An exemplar-based learning apprentice},
          author={Bareiss, E Ray and Porter, Bruce W and Wier, Craig C},
          booktitle={Machine learning},
          pages={112--127},
          year={1990},
          publisher={Elsevier}
        }
    """
    curation_comments = """
        We start with the data from UCI and merge train and test data.

        - We drop the ID column as it is uninformative here.
        - The target label contains groups of labels with specifications. We merge labels into groups that represent general a diagnosis. We create 3 labels: "normal", "cochlear", "other". There is likely a much better way to partition these labels, but this is most reasonable partitioning for an acutal task, going from names and my limited domain knowledge about the various diagnoses.
        - We drop duplicated rows as they might introduce too much information leakage for such small data and are likely not natural but rather an artifact of the limited number of features.
        - We remove one constant column (history_fullness).
    """

    # Task
    target = "diagnosis"
    problem_type = "multiclass_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        columns = [
            "age_gt_60",
            "air",
            "airBoneGap",
            "ar_c",
            "ar_u",
            "bone",
            "boneAbnormal",
            "bser",
            "history_buzzing",
            "history_dizziness",
            "history_fluctuating",
            "history_fullness",
            "history_heredity",
            "history_nausea",
            "history_noise",
            "history_recruitment",
            "history_ringing",
            "history_roaring",
            "history_vomiting",
            "late_wave_poor",
            "m_at_2k",
            "m_cond_lt_1k",
            "m_gt_1k",
            "m_m_gt_2k",
            "m_m_sn",
            "m_m_sn_gt_1k",
            "m_m_sn_gt_2k",
            "m_m_sn_gt_500",
            "m_p_sn_gt_2k",
            "m_s_gt_500",
            "m_s_sn",
            "m_s_sn_gt_1k",
            "m_s_sn_gt_2k",
            "m_s_sn_gt_3k",
            "m_s_sn_gt_4k",
            "m_sn_2_3k",
            "m_sn_gt_1k",
            "m_sn_gt_2k",
            "m_sn_gt_3k",
            "m_sn_gt_4k",
            "m_sn_gt_500",
            "m_sn_gt_6k",
            "m_sn_lt_1k",
            "m_sn_lt_2k",
            "m_sn_lt_3k",
            "middle_wave_poor",
            "mod_gt_4k",
            "mod_mixed",
            "mod_s_mixed",
            "mod_s_sn_gt_500",
            "mod_sn",
            "mod_sn_gt_1k",
            "mod_sn_gt_2k",
            "mod_sn_gt_3k",
            "mod_sn_gt_4k",
            "mod_sn_gt_500",
            "notch_4k",
            "notch_at_4k",
            "o_ar_c",
            "o_ar_u",
            "s_sn_gt_1k",
            "s_sn_gt_2k",
            "s_sn_gt_4k",
            "speech",
            "static_normal",
            "tymp",
            "viith_nerve_signs",
            "wave_V_delayed",
            "waveform_ItoV_prolonged",
            "indentifier",
            "diagnosis",
        ]
        df = pd.read_csv(raw_dir / "audiology.standardized.data", header=None, names=columns, na_values="?")
        df = pd.concat(
            [df, pd.read_csv(raw_dir / "audiology.standardized.test", header=None, names=columns, na_values="?")],
            ignore_index=True,
        )
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        as_cat_type = list(df)
        df[as_cat_type] = df[as_cat_type].astype("category")
        cochlear_classes = [
            "cochlear_age_and_noise",
            "cochlear_age_plus_poss_menieres",
            "cochlear_noise_and_heredity",
            "cochlear_poss_noise",
            "cochlear_unknown",
            "possible_menieres",
            "mixed_cochlear_age_fixation",
            "mixed_cochlear_age_otitis_media",
            "mixed_cochlear_age_s_om",
            "mixed_cochlear_unk_discontinuity",
            "mixed_cochlear_unk_fixation",
            "mixed_cochlear_unk_ser_om",
            "cochlear_age",
            "mixed_poss_noise_om",
        ]
        normal_classes = ["normal_ear"]
        other_classes = [
            "acoustic_neuroma",
            "bells_palsy",
            "conductive_discontinuity",
            "conductive_fixation",
            "mixed_poss_central_om",
            "otitis_media",
            "poss_central",
            "possible_brainstem_disorder",
            "retrocochlear_unknown",
        ]

        def map_to_diagnosis(x):
            if x in cochlear_classes:
                return "cochlear"
            if x in normal_classes:
                return "normal"
            if x in other_classes:
                return "other"
            raise ValueError(f"Unknown diagnosis class: {x}")

        df["diagnosis"] = df["diagnosis"].apply(map_to_diagnosis).astype("category")
        df = df.drop(
            columns=[
                "indentifier",
                "history_fullness",  # constant column
            ]
        )
        df = df.drop_duplicates()
        return df
