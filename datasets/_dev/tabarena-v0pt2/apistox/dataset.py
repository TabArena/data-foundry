"""Curated dataset definition for `apistox` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    TaskSummary,
    Temporal,
    TemporalSplits,
    drop_columns,
    rdkit_descriptors,
)

RAW_FILE = "dataset_final.csv"
"""The ApisTox main file: one row per compound, sorted by the first publication year."""

WINDOW_STARTS = (2014, 2004, 1994, 1984)
"""The first years of the four ten-year test windows, newest first."""

DROPPED_AFTER_TEST = ["ppdb_level", "toxicity_type", "source"]
"""Columns derived from the measured LD50 values or from where the label was taken (see `curation_comments`)."""

FLAGS = ["herbicide", "fungicide", "insecticide", "other_agrochemical"]
"""The agrochemical-type flags; all four at 0 is the source's "unknown" type and becomes missing."""


class Apistox(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Is a new agrochemical toxic to honey bees, before it has been tested on bees?",
        use_case=(
            "A company developing an agrochemical, or a regulator, screens a candidate compound for acute honey bee "
            "toxicity before the bee test, the use the dataset's authors name."
        ),
        row=(
            "One pesticide or related compound with a measured acute toxicity to honey bees (1,035 compounds from "
            "public databases, ApisTox 2024)."
        ),
        predicted=(
            "Whether the compound is toxic to bees: the dose that kills half of the bees is at most 11 micrograms per"
            " bee (the US EPA threshold); 29% are."
        ),
        known=(
            "The chemical structure as 199 descriptors computed from it, whether it is a herbicide, fungicide, "
            "insecticide or other agrochemical, and the year the compound first appears in the literature."
        ),
        split=(
            "Each test window is a decade of new compounds (2014-2023, 2004-2013, 1994-2003, 1984-1993), with every "
            "compound dated earlier for training, like the authors' time split."
        ),
        changes=(
            "We drop the toxicity level, the exposure route and the label's database, all recorded with or after the "
            "test; we replace the structure's text by descriptors computed from it and set the pesticide type to "
            "missing where the source marks it unknown."
        ),
        fit="approximate",
        fit_reason=(
            "The year is that of the first article PubChem links to the compound, so some compounds are dated late; "
            "the pesticide types were read in 2024, and bee tests of old compounds were often published decades "
            "later, so some training labels were not known at the cutoff."
        ),
    )

    # Dataset
    unique_name = "apistox"
    year = "2024"
    domain = "chemistry & material science"
    source = "Other"  # Zenodo, with the Scientific Data descriptor; UCI 995 only links to the Zenodo DOI
    source_url = "https://doi.org/10.5281/zenodo.11062076"
    license = "CC BY-NC 4.0"
    download_description = """
        We download the main file of ApisTox from Zenodo: version 2 of the record (13350981), the version the
        Scientific Data descriptor cites. Version 1 (https://zenodo.org/records/11062077) holds the identical file, and
        so does outputs/dataset_final.csv in https://github.com/j-adamczyk/ApisTox_dataset.

        mkdir -p local-data-warehouse/apistox && wget -O local-data-warehouse/apistox/dataset_final.csv "https://zenodo.org/records/13350981/files/dataset_final.csv?download=1"

        md5 of dataset_final.csv (as Zenodo lists it): 61ad9ef27a80987105a4cdb074eb102f
        sha256: de4b160a23601a44ac5ec5b23aae95973acba060135630a6df8f73d128baea9e
    """
    bibtex = """
        @article{adamczyk2025apistox,
          title={{ApisTox}: a new benchmark dataset for the classification of small molecules toxicity on honey bees},
          author={Adamczyk, Jakub and Poziemski, Jakub and Siedlecki, Pawe{\\l}},
          journal={Scientific Data},
          volume={12},
          number={1},
          pages={5},
          year={2025},
          doi={10.1038/s41597-024-04232-w}
        }
    """
    curation_comments = """
        We start with dataset_final.csv of ApisTox from Zenodo (record 13350981): 1,035 agrochemicals with their acute toxicity to honey bees.

        - Prediction point: a candidate agrochemical before its acute honey bee test, the authors' use case (Usage Notes). Known then are the structure, the intended use and the year the compound enters the literature, but not the LD50 values or any column derived from them.
        - Target: `toxic_to_bees` is the file's `label`, "Yes" when the LD50 is at most 11 µg per bee, the US EPA threshold (Methods, Eq. 1).
        - Dropped as recorded with or after the test: `ppdb_level` (the same LD50 cut at 1 and 100 µg), `toxicity_type` (the route with the strongest measured toxicity) and `source` (the database the label came from, which a new candidate does not have).
        - Dropped as identifiers: `name`, `CID` and `CAS`.
        - The structure: RDKit's 2D descriptors of `SMILES` as `rdkit_*` columns (`rdkit_descriptors`, RDKit 2026.03.6, pinned in the build extra), 199 of the 217, the others being constant here or a copy of another; values RDKit cannot compute (partial charges and BCUT descriptors of 107 compounds) are missing. Mean ROC AUC on the 4 windows, LightGBM / random forest: 0.79 / 0.71 with the flags and the year, 0.83 / 0.82 adding the descriptors.
        - `SMILES` dropped, as in every SMILES dataset (2026-10-14): as text (character n-grams) it adds 0.010 ROC AUC to LightGBM next to the descriptors, within the variation between windows (standard error 0.023).
        - The four agrochemical flags stay numeric 0/1. All four at 0 is the source's "'unknown' pesticide type" (Methods), so we set those 55 rows to missing. They are more often toxic (29 of 55, against 27% of the rest), and the flags were read in 2024, not at each compound's year.
        - We rename `year` to `first_publication_year`: the year of the earliest article PubChem links to the CID, else the PubChem record's creation date, so some compounds are dated late. We keep the source's years; dropping the affected compounds moves a window's ROC AUC by at most 0.044.
        - Note: salts and mixtures of one active substance are separate rows, as in the source, so some test compounds have their parent on the training side. Under a temporal split this is the substance's own history; leaving them out costs at most 0.034 ROC AUC.
        - Split: temporal on `first_publication_year`, as the authors' time split (Methods). Their recommended MaxMin split is one test set of diverse compounds, which tests interpolation, and the v2 protocol needs repeated splits.
        - Note: bee tests of old compounds were often published decades later, so a training label is not always known at the window's cutoff. Most test dates are not given, and the acute LD50 is a property of the compound.
        - Note: the task probes flag `unstable` (LightGBM, the best family with the descriptors, ROC AUC 0.82 on average, standard error of its mean skill 0.066 over the 4 windows), the spread of a small temporal task, as in consumer_complaints_1m.
        - Licence: CC BY-NC 4.0; Zenodo version 1, with the identical file, states CC BY 4.0.
    """

    # Task
    target = "toxic_to_bees"
    problem_type = "binary_classification"

    # Splits: four ten-year windows of first publication years (every year from 1950 on is in the data, so ten
    # distinct years are ten calendar years).
    temporal = Temporal(
        on="first_publication_year",
        splits=TemporalSplits(window=10, unit="unique", cutoffs=WINDOW_STARTS),
        horizon=10,
        horizon_unit="years",
    )
    splits_comment = """
        Expanding-window temporal splits on the first publication year: 4 test windows of ten years (2014-2023, 2004-2013, 1994-2003, 1984-1993), newest first; train is every compound dated before the window. The windows hold 54, 106, 118 and 173 compounds (12, 22, 19 and 33 toxic), and their train sides 95%, 85%, 73% and 56% of all compounds. A model trained on the compounds known up to a year predicts the toxicity of the compounds that appear in the next ten years. Ten years is the shortest window with 50 compounds at the newest end (2016-2023 holds 37): new compounds are few in recent years. An IID task of this size would get 10 x 3 splits, but the newest half of the data (from 1977 on) holds only 526 compounds, so four windows of about 50 or more remain.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / RAW_FILE)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.rename(columns={"year": "first_publication_year"})
        df[self.target] = df["label"].map({1: "Yes", 0: "No"})
        # All four flags at 0 means the compound has no "Agrochemical Information" section in PubChem, so its type
        # is unknown rather than "none of the four" (Methods, ECOTOX processing): a proxy missing value.
        unknown = df[FLAGS].sum(axis=1).eq(0)
        df[FLAGS] = df[FLAGS].astype("float64").where(~unknown, axis=0)
        # The structure as numbers: RDKit's 2D descriptors in place of the SMILES (data_foundry.v2.chemistry).
        df = pd.concat([df, rdkit_descriptors(df["SMILES"])], axis=1)
        # Derived from the measured LD50 values or from the database the label came from, the identifiers, the SMILES.
        return drop_columns(df, [*DROPPED_AFTER_TEST, "label", "name", "CID", "CAS", "SMILES"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # The four agrochemical flags are yes/no flags: categorical (CLEAN-14). The year stays an integer and the
        # descriptors numeric, the RDKit fragment counts too where only 0 and 1 occur; the target becomes a category.
        del df
        return FeatureTypes(categorical=["herbicide", "fungicide", "insecticide", "other_agrochemical"])

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        toxic = raw["label"].eq(1)
        dropped = pd.concat(
            {
                column: pd.DataFrame(
                    {"rows": raw[column].value_counts(), "toxic": toxic.groupby(raw[column]).sum()}
                ).sort_index(kind="stable")
                for column in DROPPED_AFTER_TEST
            },
            names=["column", "value"],
        )
        dropped["toxic share"] = (dropped["toxic"] / dropped["rows"]).round(3)

        year = df["first_publication_year"]
        is_toxic = df[self.target].eq("Yes")
        windows = pd.DataFrame(
            [
                {
                    "test years": f"{start}-{start + 9}",
                    "test compounds": int(year.between(start, start + 9).sum()),
                    "toxic in test": int((year.between(start, start + 9) & is_toxic).sum()),
                    "train compounds": int((year < start).sum()),
                    "train share": round(float((year < start).mean()), 3),
                    "toxic share in train": round(float(is_toxic[year < start].mean()), 3),
                }
                for start in WINDOW_STARTS
            ]
        ).set_index("test years")
        return [
            Decision(
                "PPDB level, toxicity route and source database dropped",
                "The PPDB level is the same LD50 cut at other thresholds, the route is the one with the strongest "
                "measured toxicity, and the source database sets how the label was made; none exists for a "
                "candidate before its test.",
                dropped,
            ),
            Decision(
                "Ten-year temporal windows on the first publication year",
                "New compounds are few in recent years, so ten years is the shortest window that holds 50 compounds "
                "at the newest end; four windows keep at least half of the compounds for training.",
                windows,
            ),
        ]
