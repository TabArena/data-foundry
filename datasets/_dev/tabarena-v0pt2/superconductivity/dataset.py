"""Curated dataset definition for `superconductivity` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, Grouping


def composition_labels(elements: pd.DataFrame) -> pd.Series:
    """One label per composition, for the rows of ``unique_m.csv`` (its element counts and formulas).

    A composition is the share of each element in the formula; the 81 features are computed from these shares, so
    rows with the same shares are the same input. The shares are compared at 6 decimals, which only removes
    floating-point noise (5 to 8 decimals give the same 15,164 compositions). This joins formulas that write one
    composition differently: in another element order (`Dy1Ir2Rh2B4`, `Dy1Rh2Ir2B4`) or scaled (`V2Zr1`,
    `V66.6Zr33.3`). A composition is labelled by its most frequent formula (ties: the first in sort order).
    """
    counts = elements.drop(columns=["critical_temp", "material"])
    shares = counts.div(counts.sum(axis=1), axis=0).round(6)
    key = pd.Series(pd.util.hash_pandas_object(shares, index=False).to_numpy(), index=elements.index)
    label = {}
    for value, formulas in elements["material"].groupby(key, sort=False):
        frequency = formulas.value_counts()
        label[value] = min(frequency.index, key=lambda formula: (-frequency[formula], formula))
    return key.map(label)


class Superconductivity(AbstractCuratedDataset):
    # Dataset
    unique_name = "superconductivity"
    year = "2018"
    domain = "physics & astronomy"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C53P47"
    license = "CC BY 4.0"
    download_description = """
        We download the data from the UCI repository and uzip it to a predefined folder.

        mkdir -p local-data-warehouse/superconductivity/ && wget -P local-data-warehouse/superconductivity/ https://archive.ics.uci.edu/static/public/464/superconductivty+data.zip && unzip local-data-warehouse/superconductivity/superconductivty+data.zip -d local-data-warehouse/superconductivity/ && rm local-data-warehouse/superconductivity/superconductivty+data.zip
    """
    bibtex = """
        @article{hamidieh2018data,
          title={A data-driven statistical model for predicting the critical temperature of a superconductor},
          author={Hamidieh, Kam},
          journal={Computational Materials Science},
          volume={154},
          pages={346--354},
          year={2018},
          publisher={Elsevier}
        }
    """
    curation_comments = """
        - The 81 features are computed from the element shares of the chemical formula alone. `unique_m.csv` (row-aligned with `train.csv`, same critical temperatures) has each row's element counts and formula; from it we add the group column `composition` (see `composition_labels`): 15,164 compositions, 2,422 of them with 2 to 110 SuperCon entries (6,099 repeated rows). Their temperatures differ by a median standard deviation of 1.3 K, by more than 30 K for 132 compositions (other samples, phases or pressures, which the release does not record).
        - Grouped by composition since 2026-10-06 (IID before): a model like this is used for compositions without a measured temperature, and a random split gave 35% of the test rows an identical row in train. Every entry is kept and scored per row. Not grouped by element set: a new composition is usually another proportion of known elements (a doping level), not a new family. Stanev et al. (2018) average the entries of a material instead (standard deviation below 5 K) and drop the rest; we keep the release's rows.
    """

    # Task
    target = "critical_temp"
    problem_type = "regression"
    grouping = Grouping(
        on="composition",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a composition: the share of each element in the chemical formula, from which the 81 features are computed. Its rows are the SuperCon entries for that composition (1 to 110), whose critical temperatures can differ (other samples, phases or pressures that the release does not record). The source predicts the critical temperature from the formula alone (Hamidieh 2018), and a model like that is used for compositions without a measured temperature, so the test compositions are new to the model. Each row is one prediction, made from the composition's features.
        """,
    )

    # Splits
    splits_comment = """
        Grouped splits on the composition: every SuperCon entry of a composition stays on one side, so a model predicts for compositions it has not seen. Compositions of the same elements in other proportions (another doping level of a known family) can be on both sides.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/train.csv")
        elements = pd.read_csv(f"{raw_dir}/unique_m.csv")
        if len(elements) != len(df) or not elements["critical_temp"].equals(df["critical_temp"]):
            msg = "unique_m.csv is no longer row-aligned with train.csv"
            raise ValueError(msg)
        df["composition"] = composition_labels(elements)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["composition"])

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        del raw
        per_composition = df.groupby("composition", observed=True)["critical_temp"].agg(["count", "std", "min", "max"])
        repeated = per_composition[per_composition["count"] > 1]
        spread = repeated["max"] - repeated["min"]
        evidence = pd.Series(
            {
                "rows": len(df),
                "compositions": len(per_composition),
                "compositions with more than one entry": len(repeated),
                "rows of those compositions": int(repeated["count"].sum()),
                "median std of their critical temperature (K)": round(float(repeated["std"].median()), 2),
                "of those, max - min above 10 K": int((spread > 10).sum()),
                "of those, max - min above 30 K": int((spread > 30).sum()),
            },
            name="value",
        )
        return [
            Decision(
                "Grouped by composition",
                "The features come from the composition alone, so the entries of one composition are identical "
                "rows; a model is used for compositions without a measured temperature, so a test composition must "
                "be new to it. A random split gave 35% of the test rows an identical row in train.",
                evidence,
            )
        ]
