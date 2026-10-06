"""Curated dataset definition for `audiology_diagnosis` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


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
        - We drop duplicated cases (the same findings and the same original diagnosis; 27 of 226) as they are likely not natural but rather an artifact of the coarse, categorical findings, and would put copies of one case on both sides of a split.
        - The 24 original diagnoses cannot be a target at this size: 16 of them have 4 or fewer cases. Each name combines the site of the hearing loss with its cause (`mixed_cochlear_age_otitis_media`: a mixed loss, its cochlear part from age, its conductive part from otitis media). We use the site, grouped as the standard distinction in audiology between a hearing loss with and without a conductive part (the air-bone gap): "normal" (normal_ear), "sensorineural" (the cochlear diagnoses, possible_menieres, and the retrocochlear acoustic_neuroma and retrocochlear_unknown) and "conductive_or_mixed" (the conductive diagnoses, otitis_media and every mixed diagnosis). The four standard types (conductive and mixed apart) would leave 10 conductive cases, 3-4 per test fold.
        - We drop the cases whose diagnosis is not a type of hearing loss: bells_palsy (a facial-nerve diagnosis) and the central diagnoses possible_brainstem_disorder and poss_central (3 cases after the duplicates).
        - We do not use the cause as the target: among the cochlear diagnoses it is spelled out by two history findings (age_gt_60 and history_noise agree with cochlear_age, cochlear_age_and_noise, cochlear_poss_noise or cochlear_unknown in 139 of 147 cases).
        - We remove the columns that are constant after these steps: history_fullness, and the brainstem-test findings bser, viith_nerve_signs and waveform_ItoV_prolonged, which only the dropped cases had (bser is also recorded for one kept case).
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
        df = raw.drop(columns=["indentifier"]).drop_duplicates()
        sensorineural = [
            "cochlear_age",
            "cochlear_age_and_noise",
            "cochlear_age_plus_poss_menieres",
            "cochlear_noise_and_heredity",
            "cochlear_poss_noise",
            "cochlear_unknown",
            "possible_menieres",
            "acoustic_neuroma",
            "retrocochlear_unknown",
        ]
        conductive_or_mixed = [
            "conductive_discontinuity",
            "conductive_fixation",
            "otitis_media",
            "mixed_cochlear_age_fixation",
            "mixed_cochlear_age_otitis_media",
            "mixed_cochlear_age_s_om",
            "mixed_cochlear_unk_discontinuity",
            "mixed_cochlear_unk_fixation",
            "mixed_cochlear_unk_ser_om",
            "mixed_poss_central_om",
            "mixed_poss_noise_om",
        ]
        not_a_hearing_loss_type = ["bells_palsy", "possible_brainstem_disorder", "poss_central"]

        def hearing_loss(x):
            if x == "normal_ear":
                return "normal"
            if x in sensorineural:
                return "sensorineural"
            if x in conductive_or_mixed:
                return "conductive_or_mixed"
            raise ValueError(f"Unknown diagnosis class: {x}")

        df = df[~df["diagnosis"].isin(not_a_hearing_loss_type)].copy()
        df["diagnosis"] = df["diagnosis"].apply(hearing_loss)
        # Constant after the steps above: the brainstem-test findings were recorded only for the dropped cases.
        df = df.drop(columns=["history_fullness", "bser", "viith_nerve_signs", "waveform_ItoV_prolonged"])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=[c for c in df.columns if c != self.target])
