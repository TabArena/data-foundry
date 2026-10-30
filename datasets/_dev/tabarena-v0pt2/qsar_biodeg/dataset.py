"""Curated dataset definition for `qsar_biodeg` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, TaskSummary


class QsarBiodeg(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Is a chemical readily biodegradable, judging from its molecular structure?",
        use_case=(
            "For example, a regulator or a chemical manufacturer screens a chemical's structure to decide whether it "
            "needs a ready-biodegradability test, or to rank candidates before one."
        ),
        row=(
            "One chemical with a known ready-biodegradability test result, from the data set of Mansouri et al. 2013 "
            "(1,055 chemicals)."
        ),
        predicted="Whether the chemical is readily biodegradable in the standard test; 33.7% are.",
        known=(
            "41 molecular descriptors computed from the chemical structure (counts of atoms and groups, and "
            "topological and electronic indices)."
        ),
        split=(
            "Random chemicals, so the test data stands for new chemicals; structurally similar ones can be on both "
            "sides."
        ),
        fit="direct",
        fit_reason=(
            "The descriptors come from the structure alone, which is all a screener has before testing, and the test "
            "chemicals stand for new ones."
        ),
    )

    # Dataset
    unique_name = "qsar_biodeg"
    year = "2013"
    domain = "chemistry & material science"
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
        - biodeg.csv has no header row, so we read it with `header=None` and keep the first chemical: 1,055 rows,
          356 readily biodegradable, as on UCI.
        - The counts stay numeric (CLEAN-14): atoms, groups, circuits, the frequencies of atom pairs, and the two
          atom-centred fragments `N073_chemical_substructure` (N-073: Ar2NH / Ar3N / Ar2N-Al / R..N..R, 0 to 3) and
          `C026_chemical_substructure` (C-026: R--CX--R, 0 to 12), which count the atoms of that type in the molecule.
          The definition had typed those two categorical while their meaning was unknown (found by the dtype probe,
          2026-10-30). The three presence/absence descriptors (B01[C-Br], B03[C-Cl], B04[C-Br]) are yes/no flags.
    """

    # Task
    target = "Biodegradable"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason="Mansouri et al. 2013 report error rate / NER with sensitivity and specificity, the group's house measure, without a decision threshold or costs. Original rejected: NER (balanced accuracy). roc_auc is the binary fallback."
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/biodeg.csv", sep=";", header=None)  # no header row; names set in `_clean`
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
            "N073_chemical_substructure",  # N-073: atom-centred fragment Ar2NH / Ar3N / Ar2N-Al / R..N..R, a count
            "Adjacency_LeadingEigenvalue",
            "Intrinsic_State_Pseudoconnectivity",
            "Presence_CBr_At_Dist4",
            "Sum_dO_EStates",
            "Laplace_MoharIndex2",
            "Num_RingTertiaryC",
            "C026_chemical_substructure",  # C-026: atom-centred fragment R--CX--R, a count
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
                "Presence_CBr_At_Dist4",
            ],
        )
