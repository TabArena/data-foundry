"""Curated dataset definition for `covertype` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes


class Covertype(AbstractCuratedDataset):
    # Dataset
    unique_name = "covertype"
    year = "1998"
    domain = "environmental science & climate"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C50K5N"
    license = "CC BY 4.0"
    data_tags = ("Spatial",)
    download_description = """
        We download the data from UCI.

        wget https://archive.ics.uci.edu/static/public/31/covertype.zip && unzip covertype.zip && rm old_covtype.info covtype.info covertype.zip  && gunzip covtype.data.gz
        mkdir -p local-data-warehouse/covertype && mv covtype.data local-data-warehouse/covertype/
    """
    bibtex = """
        @article{blackard1999comparative,
          title={Comparative accuracies of artificial neural networks and discriminant analysis in predicting forest cover types from cartographic variables},
          author={Blackard, Jock A and Dean, Denis J},
          journal={Computers and electronics in agriculture},
          volume={24},
          number={3},
          pages={131--151},
          year={1999},
          publisher={Elsevier}
        }
    """
    curation_comments = """
        We start with the data from UCI.

        We create a special version of the dataset to avoid leakage. This version consists only of three 3 classes and 3 (spatial) wilderness areas. The investigation of Covertype shows that the dataset comprises multiple wilderness areas (Rawah, Comanche Peak, Neota, Cache la Poudre) that can be treated as subgroups but are not strictly IID, with wilderness area and soil type encoded as one-hot categorical features. Although TabRed argues for a time split to reflect a real task, the dataset lacks both explicit time and precise spatial (e.g., GNSS) features, leaving only area identifiers, which implicitly encode collection time and location; consequently, IID splits would introduce temporal or spatial leakage. Additional issues include transformed features in the OpenML/TALENT version that leak test distribution, incorrect column order in the UCI release, and evidence from EDA that class distributions differ across areas, confirming the dataset’s grouped nature where cover type characteristics strongly depend on area. The only robust strategy is a spatially motivated grouped split by area; however, because some classes appear only in specific areas, the dataset is restricted to classes present in the three largest areas and evaluated using leave-one-area-out grouped splits.

        Other steps:
        - We add the column names in the correct way.
        - We reverse the one-hot encoding of the Wilderness_Area and Soil_Type features, and add human-readable descriptions for these features. Moreover, we add the climatic and geologic zones categorical features for each soil type based on the codes.
        - We reverse the ordinal encoding of the class name.
    """

    # Task
    target = "Cover_Type"
    problem_type = "multiclass_classification"
    group_on = "Wilderness_Area"
    group_labels = "per_sample"

    # Splits
    splits_comment = """
        We create stratified grouped 3-fold split, always leaving one area out of the training data.
    """

    accepted_check_warnings = {
        "splits_test_over_budget": "One leave-one-area-out test fold holds a whole wilderness area of 257,015 rows, "
        "3% over the 250k budget; capping it would cut the area the fold tests on.",
    }

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        columns = [
            "Elevation",
            "Aspect",
            "Slope",
            "Horizontal_Distance_To_Hydrology",
            "Vertical_Distance_To_Hydrology",
            "Horizontal_Distance_To_Roadways",
            "Hillshade_9am",
            "Hillshade_Noon",
            "Hillshade_3pm",
            "Horizontal_Distance_To_Fire_Points",
            "Wilderness_Area1",
            "Wilderness_Area2",
            "Wilderness_Area3",
            "Wilderness_Area4",
            "Soil_Type1",
            "Soil_Type2",
            "Soil_Type3",
            "Soil_Type4",
            "Soil_Type5",
            "Soil_Type6",
            "Soil_Type7",
            "Soil_Type8",
            "Soil_Type9",
            "Soil_Type10",
            "Soil_Type11",
            "Soil_Type12",
            "Soil_Type13",
            "Soil_Type14",
            "Soil_Type15",
            "Soil_Type16",
            "Soil_Type17",
            "Soil_Type18",
            "Soil_Type19",
            "Soil_Type20",
            "Soil_Type21",
            "Soil_Type22",
            "Soil_Type23",
            "Soil_Type24",
            "Soil_Type25",
            "Soil_Type26",
            "Soil_Type27",
            "Soil_Type28",
            "Soil_Type29",
            "Soil_Type30",
            "Soil_Type31",
            "Soil_Type32",
            "Soil_Type33",
            "Soil_Type34",
            "Soil_Type35",
            "Soil_Type36",
            "Soil_Type37",
            "Soil_Type38",
            "Soil_Type39",
            "Soil_Type40",
            "Cover_Type",
        ]
        df = pd.read_csv(raw_dir / "covtype.data", header=None, names=columns)
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # --- Wilderness mapping (from "Wilderness_Area{k}" -> code + name) ---
        WILDERNESS_NAME = {
            1: "Rawah Wilderness Area",
            2: "Neota Wilderness Area",
            3: "Comanche Peak Wilderness Area",
            4: "Cache la Poudre Wilderness Area",
        }
        # --- Soil mapping (Study Code -> USFS ELU code + description) ---
        SOIL = {
            1: (2702, "Cathedral family - Rock outcrop complex, extremely stony."),
            2: (2703, "Vanet - Ratake families complex, very stony."),
            3: (2704, "Haploborolis - Rock outcrop complex, rubbly."),
            4: (2705, "Ratake family - Rock outcrop complex, rubbly."),
            5: (2706, "Vanet family - Rock outcrop complex complex, rubbly."),
            6: (2717, "Vanet - Wetmore families - Rock outcrop complex, stony."),
            7: (3501, "Gothic family."),
            8: (3502, "Supervisor - Limber families complex."),
            9: (4201, "Troutville family, very stony."),
            10: (4703, "Bullwark - Catamount families - Rock outcrop complex, rubbly."),
            11: (4704, "Bullwark - Catamount families - Rock land complex, rubbly."),
            12: (4744, "Legault family - Rock land complex, stony."),
            13: (4758, "Catamount family - Rock land - Bullwark family complex, rubbly."),
            14: (5101, "Pachic Argiborolis - Aquolis complex."),
            15: (5151, "unspecified in the USFS Soil and ELU Survey."),
            16: (6101, "Cryaquolis - Cryoborolis complex."),
            17: (6102, "Gateview family - Cryaquolis complex."),
            18: (6731, "Rogert family, very stony."),
            19: (7101, "Typic Cryaquolis - Borohemists complex."),
            20: (7102, "Typic Cryaquepts - Typic Cryaquolls complex."),
            21: (7103, "Typic Cryaquolls - Leighcan family, till substratum complex."),
            22: (7201, "Leighcan family, till substratum, extremely bouldery."),
            23: (7202, "Leighcan family, till substratum - Typic Cryaquolls complex."),
            24: (7700, "Leighcan family, extremely stony."),
            25: (7701, "Leighcan family, warm, extremely stony."),
            26: (7702, "Granile - Catamount families complex, very stony."),
            27: (7709, "Leighcan family, warm - Rock outcrop complex, extremely stony."),
            28: (7710, "Leighcan family - Rock outcrop complex, extremely stony."),
            29: (7745, "Como - Legault families complex, extremely stony."),
            30: (7746, "Como family - Rock land - Legault family complex, extremely stony."),
            31: (7755, "Leighcan - Catamount families complex, extremely stony."),
            32: (7756, "Catamount family - Rock outcrop - Leighcan family complex, extremely stony."),
            33: (7757, "Leighcan - Catamount families - Rock outcrop complex, extremely stony."),
            34: (7790, "Cryorthents - Rock land complex, extremely stony."),
            35: (8703, "Cryumbrepts - Rock outcrop - Cryaquepts complex."),
            36: (8707, "Bross family - Rock land - Cryumbrepts complex, extremely stony."),
            37: (8708, "Rock outcrop - Cryumbrepts - Cryorthents complex, extremely stony."),
            38: (8771, "Leighcan - Moran families - Cryaquolls complex, extremely stony."),
            39: (8772, "Moran family - Cryorthents - Leighcan family complex, extremely stony."),
            40: (8776, "Moran family - Cryorthents - Rock land complex, extremely stony."),
        }
        CLIMATIC_ZONE = {
            1: "lower montane dry",
            2: "lower montane",
            3: "montane dry",
            4: "montane",
            5: "montane dry and montane",
            6: "montane and subalpine",
            7: "subalpine",
            8: "alpine",
        }
        GEOLOGIC_ZONE = {
            1: "alluvium",
            2: "glacial",
            3: "shale",
            4: "sandstone",
            5: "mixed sedimentary",
            6: "unspecified in the USFS ELU Survey",
            7: "igneous and metamorphic",
            8: "volcanic",
        }
        # --- Target mapping ---
        COVER_NAME = {
            1: "Spruce/Fir",
            2: "Lodgepole Pine",
            3: "Ponderosa Pine",
            4: "Cottonwood/Willow",
            5: "Aspen",
            6: "Douglas-fir",
            7: "Krummholz",
        }

        def merge_onehot(df, pattern, out_col, drop=True):
            cols = [c for c in df.columns if re.fullmatch(pattern, c)]
            X = df[cols]

            assert cols, f"No columns match {pattern}"
            assert X.notna().all().all(), f"{out_col}: contains NaNs"
            assert X.isin([0, 1]).all().all(), f"{out_col}: non-binary values found"
            s = X.sum(1)
            assert (s == 1).all(), f"{out_col}: not one-hot (row sums != 1). Bad rows: {(s != 1).sum()}"

            df[out_col] = X.idxmax(1)  # name of the active column
            return df.drop(columns=cols) if drop else df

        df = merge_onehot(df, r"Wilderness_Area\d+", "Wilderness_Area", drop=True)
        df = merge_onehot(df, r"Soil_Type\d+", "Soil_Type", drop=True)
        # Wilderness -> code + description
        w_code = df["Wilderness_Area"].str.extract(r"(\d+)$").astype("Int64")[0]
        df["Wilderness_Area"] = w_code.map(WILDERNESS_NAME)
        # Soil -> study code + ELU + description + climatic/geologic zones
        s_code = df["Soil_Type"].str.extract(r"(\d+)$").astype("Int64")[0]
        df["Soil_USFS_ELU"] = s_code.map(lambda k: SOIL[int(k)][0] if pd.notna(k) else pd.NA).astype("Int64")
        df["Soil_Type"] = s_code.map(lambda k: SOIL[int(k)][1] if pd.notna(k) else pd.NA)
        elu = df["Soil_USFS_ELU"].astype("string")
        df["Soil_ClimaticZone"] = elu.str[0].astype("Int64").map(CLIMATIC_ZONE)
        df["Soil_GeologicZone"] = elu.str[1].astype("Int64").map(GEOLOGIC_ZONE)
        df = df.drop(columns=["Soil_USFS_ELU"])
        # Target -> text label
        df["Cover_Type"] = df["Cover_Type"].map(COVER_NAME)
        # Show data distribution across wilderness areas and cover types to confirm the grouped nature of the dataset
        df.groupby(["Wilderness_Area", "Cover_Type"]).size().unstack(fill_value=0).sort_index()
        # Keep only data points that have the following classes and areas:
        allowed_classes = ["Krummholz", "Lodgepole Pine", "Spruce/Fir"]
        allowed_areas = ["Comanche Peak Wilderness Area", "Neota Wilderness Area", "Rawah Wilderness Area"]
        df = df[df["Cover_Type"].isin(allowed_classes) & df["Wilderness_Area"].isin(allowed_areas)].reset_index(
            drop=True
        )
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "Wilderness_Area",
                "Soil_Type",
                "Soil_ClimaticZone",
                "Soil_GeologicZone",
            ],
        )
