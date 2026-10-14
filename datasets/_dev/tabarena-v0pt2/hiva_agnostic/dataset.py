"""Curated dataset definition for `hiva_agnostic` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, TaskSummary


class HivaAgnostic(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Is a chemical compound active against HIV in a laboratory screen?",
        use_case=(
            "For example, a drug-discovery team ranks untested compounds by computer and decides which to send to the"
            " laboratory screen."
        ),
        row=(
            "One compound of the US National Cancer Institute's AIDS antiviral screen, as prepared for the 2007 "
            "Agnostic Learning vs. Prior Knowledge challenge (its 3,845 training compounds)."
        ),
        predicted="Whether the compound is active in the screen (3.51% are).",
        known=("1,617 anonymous yes/no descriptors of the molecule's structure, without the duplicated ones."),
        split="Random compounds, so the test data stands for other compounds of the same screen.",
        fit="direct",
        fit_reason=(
            "The features come from the structure alone, as for an untested compound, and the test compounds are "
            "unseen. The descriptors are anonymous, so their meaning cannot be checked."
        ),
    )

    # Dataset
    unique_name = "hiva_agnostic"
    year = "2007"
    domain = "chemistry & material science"
    source = "Other"
    source_url = "https://www.agnostic.inf.ethz.ch"
    license = "Public Domain"
    download_description = """
        We download the dataset from the challenge platform into predefined folder:

        mkdir -p local-data-warehouse/hiva_agnostic/ && wget -P local-data-warehouse/hiva_agnostic/ https://www.agnostic.inf.ethz.ch/datasets/DataAgnos/HIVA.zip && wget -P local-data-warehouse/hiva_agnostic/ https://www.agnostic.inf.ethz.ch/datasets/ValidAgnos.zip && unzip local-data-warehouse/hiva_agnostic/HIVA.zip -d local-data-warehouse/hiva_agnostic/ && unzip local-data-warehouse/hiva_agnostic/ValidAgnos.zip -d local-data-warehouse/hiva_agnostic/ && rm local-data-warehouse/hiva_agnostic/HIVA.zip && rm local-data-warehouse/hiva_agnostic/ValidAgnos.zip
    """
    bibtex = """
        @inproceedings{guyon2007agnostic,
          author={Isabelle Guyon and Amir Saffari and Gideon Dror and Gavin Cawley},
          booktitle={2007 International Joint Conference on Neural Networks},
          title={Agnostic Learning vs. Prior Knowledge Challenge},
          year={2007},
          pages={829-834},
          doi={10.1109/IJCNN.2007.4371065}
        }
    """
    curation_comments = """
        - The target is binary, as the challenge made it: the screen's three classes (active, moderately active, inactive) were "brought back to a two-class classification problem (active vs. inactive)" (challenge description, copied on OpenML 1039); 135 of the 3,845 training compounds are active.
        - We use only the challenge's training file. The download also fetches the validation labels the challenge released afterwards (hiva_valid.labels, 384 compounds, 14 active), but they are not used; the challenge site offers no test labels.
    """

    # Task
    target = "CompoundActive"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        # train data
        df = pd.read_csv(raw_dir / "HIVA/hiva_train.data", header=None, sep=" ")
        y = pd.read_csv(raw_dir / "HIVA/hiva_train.labels", header=None)
        return {"df": df, "y": y}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        df, y = raw["df"], raw["y"]
        df.columns = [f"molecule_structure_property_{i + 1}" for i in range(len(df.columns))]
        # Remove trailing whitespace column
        df = df.drop(columns=["molecule_structure_property_1618"])
        target_feature = "CompoundActive"
        df[target_feature] = y[0]
        df = df.astype("category")
        # Drop duplicated columns
        df = df.drop(
            columns=[
                "molecule_structure_property_710",
                "molecule_structure_property_1079",
                "molecule_structure_property_1398",
                "molecule_structure_property_1024",
                "molecule_structure_property_829",
                "molecule_structure_property_1615",
                "molecule_structure_property_724",
                "molecule_structure_property_732",
                "molecule_structure_property_410",
                "molecule_structure_property_509",
                "molecule_structure_property_1035",
                "molecule_structure_property_811",
                "molecule_structure_property_686",
                "molecule_structure_property_1386",
                "molecule_structure_property_59",
                "molecule_structure_property_1493",
                "molecule_structure_property_542",
                "molecule_structure_property_1500",
                "molecule_structure_property_376",
                "molecule_structure_property_765",
                "molecule_structure_property_970",
                "molecule_structure_property_1011",
                "molecule_structure_property_1127",
                "molecule_structure_property_701",
                "molecule_structure_property_1114",
                "molecule_structure_property_1390",
                "molecule_structure_property_1194",
                "molecule_structure_property_925",
                "molecule_structure_property_797",
                "molecule_structure_property_1373",
                "molecule_structure_property_1223",
                "molecule_structure_property_1457",
                "molecule_structure_property_1342",
                "molecule_structure_property_1314",
                "molecule_structure_property_1272",
                "molecule_structure_property_1322",
                "molecule_structure_property_1576",
                "molecule_structure_property_633",
                "molecule_structure_property_1430",
                "molecule_structure_property_574",
                "molecule_structure_property_519",
                "molecule_structure_property_937",
                "molecule_structure_property_734",
                "molecule_structure_property_320",
                "molecule_structure_property_1344",
                "molecule_structure_property_175",
                "molecule_structure_property_544",
                "molecule_structure_property_533",
                "molecule_structure_property_746",
                "molecule_structure_property_1104",
                "molecule_structure_property_1138",
                "molecule_structure_property_322",
                "molecule_structure_property_402",
                "molecule_structure_property_757",
                "molecule_structure_property_784",
                "molecule_structure_property_1472",
                "molecule_structure_property_1599",
                "molecule_structure_property_791",
                "molecule_structure_property_1205",
                "molecule_structure_property_1031",
                "molecule_structure_property_1074",
                "molecule_structure_property_1455",
                "molecule_structure_property_1475",
                "molecule_structure_property_287",
                "molecule_structure_property_748",
                "molecule_structure_property_1175",
                "molecule_structure_property_1191",
                "molecule_structure_property_1582",
                "molecule_structure_property_264",
                "molecule_structure_property_1050",
                "molecule_structure_property_554",
                "molecule_structure_property_1449",
                "molecule_structure_property_1140",
                "molecule_structure_property_407",
                "molecule_structure_property_1341",
                "molecule_structure_property_1124",
                "molecule_structure_property_1049",
                "molecule_structure_property_1325",
                "molecule_structure_property_667",
                "molecule_structure_property_851",
                "molecule_structure_property_1523",
                "molecule_structure_property_525",
                "molecule_structure_property_1208",
                "molecule_structure_property_1556",
                "molecule_structure_property_933",
                "molecule_structure_property_1356",
                "molecule_structure_property_1209",
                "molecule_structure_property_964",
                "molecule_structure_property_989",
                "molecule_structure_property_1028",
                "molecule_structure_property_1458",
                "molecule_structure_property_842",
                "molecule_structure_property_1468",
                "molecule_structure_property_1419",
                "molecule_structure_property_1367",
                "molecule_structure_property_112",
                "molecule_structure_property_699",
                "molecule_structure_property_796",
                "molecule_structure_property_478",
            ]
        )
        return df
