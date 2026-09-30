"""Curated dataset definition for `mic` (data-foundry v2). Evidence: report.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class Mic(AbstractCuratedDataset):
    # Dataset
    unique_name = "mic"
    year = "2020"
    domain = "medical & healthcare"
    source = "UCI"
    source_url = "https://archive.ics.uci.edu/dataset/579/myocardial+infarction+complications"
    license = "CC BY 4.0"
    download_description = """
        We download the data from the UCI repository and uzip it to a predefined folder.

        mkdir -p local-data-warehouse/mic/ && wget -P local-data-warehouse/mic/ https://archive.ics.uci.edu/static/public/579/myocardial+infarction+complications.zip && unzip local-data-warehouse/mic/myocardial+infarction+complications.zip -d local-data-warehouse/mic/ && rm local-data-warehouse/mic/myocardial+infarction+complications.zip
    """
    bibtex = """
        @article{golovenkin2020trajectories,
          title={Trajectories, bifurcations, and pseudo-time in large clinical datasets: applications to myocardial infarction and diabetes data},
          author={Golovenkin, Sergey E and Bac, Jonathan and Chervov, Alexander and Mirkes, Evgeny M and Orlova, Yuliya V and Barillot, Emmanuel and Gorban, Alexander N and Zinovyev, Andrei},
          journal={GigaScience},
          volume={9},
          number={11},
          pages={giaa128},
          year={2020},
          publisher={Oxford University Press}
        }
    """
    curation_comments = """
        - There are 12 possible targets and four possible time moments to predict the targets for this dataset. We use the categorical target as it summarizes the other possible targets. Furthermore, we use the last possible time point for prediction to utilize all available data.
        - We treat "?" as missing values.
        - We dropped the "id" column.
        - We reversed the ordinal encoding of the target feature.
    """

    # Task
    target = "LET_IS"
    problem_type = "multiclass_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/MI.data", na_values="?")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df.columns = [
            "ID",
            "AGE",
            "SEX",
            "INF_ANAM",
            "STENOK_AN",
            "FK_STENOK",
            "IBS_POST",
            "IBS_NASL",
            "GB",
            "SIM_GIPERT",
            "DLIT_AG",
            "ZSN_A",
            "nr_11",
            "nr_01",
            "nr_02",
            "nr_03",
            "nr_04",
            "nr_07",
            "nr_08",
            "np_01",
            "np_04",
            "np_05",
            "np_07",
            "np_08",
            "np_09",
            "np_10",
            "endocr_01",
            "endocr_02",
            "endocr_03",
            "zab_leg_01",
            "zab_leg_02",
            "zab_leg_03",
            "zab_leg_04",
            "zab_leg_06",
            "S_AD_KBRIG",
            "D_AD_KBRIG",
            "S_AD_ORIT",
            "D_AD_ORIT",
            "O_L_POST",
            "K_SH_POST",
            "MP_TP_POST",
            "SVT_POST",
            "GT_POST",
            "FIB_G_POST",
            "ant_im",
            "lat_im",
            "inf_im",
            "post_im",
            "IM_PG_P",
            "ritm_ecg_p_01",
            "ritm_ecg_p_02",
            "ritm_ecg_p_04",
            "ritm_ecg_p_06",
            "ritm_ecg_p_07",
            "ritm_ecg_p_08",
            "n_r_ecg_p_01",
            "n_r_ecg_p_02",
            "n_r_ecg_p_03",
            "n_r_ecg_p_04",
            "n_r_ecg_p_05",
            "n_r_ecg_p_06",
            "n_r_ecg_p_08",
            "n_r_ecg_p_09",
            "n_r_ecg_p_10",
            "n_p_ecg_p_01",
            "n_p_ecg_p_03",
            "n_p_ecg_p_04",
            "n_p_ecg_p_05",
            "n_p_ecg_p_06",
            "n_p_ecg_p_07",
            "n_p_ecg_p_08",
            "n_p_ecg_p_09",
            "n_p_ecg_p_10",
            "n_p_ecg_p_11",
            "n_p_ecg_p_12",
            "fibr_ter_01",
            "fibr_ter_02",
            "fibr_ter_03",
            "fibr_ter_05",
            "fibr_ter_06",
            "fibr_ter_07",
            "fibr_ter_08",
            "GIPO_K",
            "K_BLOOD",
            "GIPER_NA",
            "NA_BLOOD",
            "ALT_BLOOD",
            "AST_BLOOD",
            "KFK_BLOOD",
            "L_BLOOD",
            "ROE",
            "TIME_B_S",
            "R_AB_1_n",
            "R_AB_2_n",
            "R_AB_3_n",
            "NA_KB",
            "NOT_NA_KB",
            "LID_KB",
            "NITR_S",
            "NA_R_1_n",
            "NA_R_2_n",
            "NA_R_3_n",
            "NOT_NA_1_n",
            "NOT_NA_2_n",
            "NOT_NA_3_n",
            "LID_S_n",
            "B_BLOK_S_n",
            "ANT_CA_S_n",
            "GEPAR_S_n",
            "ASP_S_n",
            "TIKL_S_n",
            "TRENT_S_n",
            "FIBR_PREDS",
            "PREDS_TAH",
            "JELUD_TAH",
            "FIBR_JELUD",
            "A_V_BLOK",
            "OTEK_LANC",
            "RAZRIV",
            "DRESSLER",
            "ZSN",
            "REC_IM",
            "P_IM_STEN",
            "LET_IS",
        ]
        df = df.drop(
            columns=[
                "ID",
                "FIBR_PREDS",
                "PREDS_TAH",
                "JELUD_TAH",
                "FIBR_JELUD",
                "A_V_BLOK",
                "OTEK_LANC",
                "RAZRIV",
                "DRESSLER",
                "ZSN",
                "REC_IM",
                "P_IM_STEN",
            ]
        )
        target_feature = "LET_IS"
        df[target_feature] = df[target_feature].map(
            {
                1: "cardiogenic_shock",
                0: "alive",
                2: "pulmonary_edema",
                3: "myocardial_rupture",
                4: "progress_congestive_heart_failure",
                5: "thromboembolism",
                6: "asystole",
                7: "ventricular_fibrillation",
            }
        )
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "SEX",
                "INF_ANAM",
                "STENOK_AN",
                "FK_STENOK",
                "IBS_POST",
                "IBS_NASL",
                "GB",
                "SIM_GIPERT",
                "DLIT_AG",
                "ZSN_A",
                "nr_11",
                "nr_01",
                "nr_02",
                "nr_03",
                "nr_04",
                "nr_07",
                "nr_08",
                "np_01",
                "np_04",
                "np_05",
                "np_07",
                "np_08",
                "np_09",
                "np_10",
                "endocr_01",
                "endocr_02",
                "endocr_03",
                "zab_leg_01",
                "zab_leg_02",
                "zab_leg_03",
                "zab_leg_04",
                "zab_leg_06",
                "O_L_POST",
                "K_SH_POST",
                "MP_TP_POST",
                "SVT_POST",
                "GT_POST",
                "FIB_G_POST",
                "ant_im",
                "lat_im",
                "inf_im",
                "post_im",
                "IM_PG_P",
                "ritm_ecg_p_01",
                "ritm_ecg_p_02",
                "ritm_ecg_p_04",
                "ritm_ecg_p_06",
                "ritm_ecg_p_07",
                "ritm_ecg_p_08",
                "n_r_ecg_p_01",
                "n_r_ecg_p_02",
                "n_r_ecg_p_03",
                "n_r_ecg_p_04",
                "n_r_ecg_p_05",
                "n_r_ecg_p_06",
                "n_r_ecg_p_08",
                "n_r_ecg_p_09",
                "n_r_ecg_p_10",
                "n_p_ecg_p_01",
                "n_p_ecg_p_03",
                "n_p_ecg_p_04",
                "n_p_ecg_p_05",
                "n_p_ecg_p_06",
                "n_p_ecg_p_07",
                "n_p_ecg_p_08",
                "n_p_ecg_p_09",
                "n_p_ecg_p_10",
                "n_p_ecg_p_11",
                "n_p_ecg_p_12",
                "fibr_ter_01",
                "fibr_ter_02",
                "fibr_ter_03",
                "fibr_ter_05",
                "fibr_ter_06",
                "fibr_ter_07",
                "fibr_ter_08",
                "GIPO_K",
                "GIPER_NA",
                "TIME_B_S",
                "R_AB_1_n",
                "R_AB_2_n",
                "R_AB_3_n",
                "NA_KB",
                "NOT_NA_KB",
                "LID_KB",
                "NITR_S",
                "NOT_NA_1_n",
                "LID_S_n",
                "B_BLOK_S_n",
                "ANT_CA_S_n",
                "GEPAR_S_n",
                "ASP_S_n",
                "TIKL_S_n",
                "TRENT_S_n",
            ],
        )
