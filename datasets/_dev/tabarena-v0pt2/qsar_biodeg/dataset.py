"""Curated dataset definition for `qsar_biodeg` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class QsarBiodeg(AbstractCuratedDataset):
    # Dataset
    unique_name = "qsar_biodeg"
    year = "2013"
    domain = "biology & life sciences"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5H60M"
    license = "CC BY 4.0"
    download_description = """
        mkdir -p local-data-warehouse/qsar_biodeg/ && wget -P local-data-warehouse/qsar_biodeg/ https://archive.ics.uci.edu/static/public/254/qsar+biodegradation.zip && unzip local-data-warehouse/qsar_biodeg/qsar+biodegradation.zip -d local-data-warehouse/qsar_biodeg/ && rm local-data-warehouse/qsar_biodeg/qsar+biodegradation.zip
    """
    bibtex = """
        @article{mansouri2013quantitative,
          title={Quantitative structure--activity relationship models for ready biodegradability of chemicals},
          author={Mansouri, Kamel and Ringsted, Tine and Ballabio, Davide and Todeschini, Roberto and Consonni, Viviana},
          journal={Journal of chemical information and modeling},
          volume={53},
          number={4},
          pages={867--878},
          year={2013},
          publisher={ACS Publications}
        }
    """
    curation_comments = """
        - We added semantic meaningful feature names.
        - Anomaly: several features are numeric-ordinal in nature but it is unclear if they are categorical features.
    """

    # Task
    target = "Biodegradable"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/biodeg.csv", sep=";")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        target_feature = "Biodegradable"
        df.columns = [
            "Laplace_Leading_Eigenvalue",
            "Weighted_Balaban_Index_Barysz_Matrix",
            "Num_Heavy_Atoms",
            "Freq_NN_At_Dist1",
            "Freq_CN_At_Dist4",
            "Num_ssssC_Atoms",
            "Num_Substituted_BenzeneC",
            "Percentage_C_Atoms",
            "Num_Terminal_PrimaryC",
            "Num_Oxygen_Atoms",
            "Freq_CN_At_Dist3",
            "Sum_dssC_EStates",
            "Weighted_HyperWiener_Index_Burden_Matrix",
            "Lopping_Centric_Index",
            "Laplace_Spectral_Moment6",
            "Freq_CO_At_Dist3",
            "Mean_Sanderson_Electronegativity",
            "Mean_Ionization_Potential",
            "Num_N_Hydrazine",
            "Num_Aromatic_Nitro_Groups",
            "Num_CRX3",
            "Weighted_Normalized_SpectralPositiveSum_Burden_Matrix",
            "Num_Circuits",
            "Presence_CBr_At_Dist1",
            "Presence_CCl_At_Dist3",
            "N073_chemical_substructure",  # no idea what this might be
            "Adjacency_LeadingEigenvalue",
            "Intrinsic_State_Pseudoconnectivity",
            "Presence_CBr_At_Dist4",
            "Sum_dO_EStates",
            "Laplace_MoharIndex2",
            "Num_RingTertiaryC",
            "C026_chemical_substructure",
            "Freq_CN_At_Dist2",
            "Num_HBond_Donors_Atoms",
            "Weighted_LeadingEigenvalue_Burden_Matrix",
            "Intrinsic_State_Pseudoconnectivity_SAvg",
            "Num_Nitrogen_Atoms",
            "Weighted_SpectralMoment6_Burden_Matrix",
            "Num_Esters",
            "Num_Halogen_Atoms",
            target_feature,
        ]
        df[target_feature] = df[target_feature].map({"RB": "Yes", "NRB": "No"})
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "Presence_CBr_At_Dist1",
                "Presence_CCl_At_Dist3",
                "N073_chemical_substructure",
                "Presence_CBr_At_Dist4",
                "C026_chemical_substructure",  # very likely categorical, but unclear
            ],
        )
