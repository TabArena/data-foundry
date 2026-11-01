"""Curated dataset definition for `hiva_agnostic` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Metric, TaskSummary


class HivaAgnostic(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Is a chemical compound active against HIV in a laboratory screen?",
        use_case=(
            "For example, a drug-discovery team ranks untested compounds by computer and decides which to send to the"
            " laboratory screen."
        ),
        row=(
            "One compound of the US National Cancer Institute's AIDS antiviral screen, as prepared for the 2007 "
            "Agnostic Learning vs. Prior Knowledge challenge (its 3,845 training and 384 validation compounds)."
        ),
        predicted="Whether the compound is active in the screen (3.52% are).",
        known=(
            "1,429 anonymous yes/no descriptors of the molecule's structure (the challenge's 1,617 without the 188 that "
            "copy another)."
        ),
        split="Random compounds, so the test data stands for other compounds of the same screen.",
        changes=(
            "We add the challenge's 384 validation compounds, whose labels it released, and drop the descriptors that "
            "copy another."
        ),
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
    data_tags = ("Anonymized",)
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
        - The target is binary, as the challenge made it: the screen's three classes (active, moderately active, inactive) were "brought back to a two-class classification problem (active vs. inactive)" (challenge description, copied on OpenML 1039); 149 of the 4,229 compounds are active.
        - We use the challenge's training (3,845 compounds, 135 active) and validation compounds (384, 14 active; labels in ValidAgnos.zip), as `hiva.param` lists them. The test labels (38,449 compounds) were never released. The validation compounds were added on 2026-10-14.
        - We drop the 188 descriptors that copy an earlier one; until 2026-10-14 a fixed list dropped 99 of them. 23 compounds repeat another's descriptors, always with the same label (3 of them across training and validation), and stay.
          Why they stay (checked 2026-10-21 against the challenge's prior-knowledge release, which gives the same 4,229 compounds as structures with their NCI NSC numbers, in another order): every compound has its own NSC number, so no compound is entered twice. Of the 4,156 structures that RDKit reads, 7 repeat another's exact structure under a new NSC number, 9 ignoring stereochemistry and 19 counting salt forms of one parent. That is fewer than the 23 repeated descriptor vectors, so at least 4 of the 23 are different compounds that the 1,617 binary descriptors cannot tell apart. The two releases share no key, so the 23 cannot be matched one by one. All 46 rows are inactive.
    """

    # Task
    target = "CompoundActive"
    problem_type = "binary_classification"
    metric = Metric.source(
        "balanced_accuracy",
        original="BER (balanced error rate) = 0.5*(b/(a+b) + c/(c+d)); final ranking by test BER; AUC also reported (= 1-BER for hard predictions)",
        reference="https://www.agnostic.inf.ethz.ch/evaluation.php ; Guyon et al. 2007 IJCNN, doi 10.1109/IJCNN.2007.4371065",
        definition="mean of per-class recall on active vs inactive (balanced_accuracy = 1 - BER), on hard predictions",
    )

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        # The challenge's training and validation compounds; it never released the test labels
        df = pd.concat(
            [pd.read_csv(raw_dir / f"HIVA/hiva_{part}.data", header=None, sep=" ") for part in ("train", "valid")],
            ignore_index=True,
        )
        y = pd.concat(
            [
                pd.read_csv(raw_dir / "HIVA/hiva_train.labels", header=None),
                pd.read_csv(raw_dir / "Agnostic/hiva_valid.labels", header=None),
            ],
            ignore_index=True,
        )
        return {"df": df, "y": y}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        df, y = raw["df"], raw["y"]
        df.columns = [f"molecule_structure_property_{i + 1}" for i in range(len(df.columns))]
        # Remove trailing whitespace column
        df = df.drop(columns=["molecule_structure_property_1618"])
        # Drop the descriptors that copy an earlier one (188 of 1,617)
        df = df.loc[:, ~df.T.duplicated().to_numpy()]
        df["CompoundActive"] = y[0]
        return df.astype("category")
