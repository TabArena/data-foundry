"""Curated dataset definition for `superconductivity` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Grouping,
    Metric,
    ScoringColumn,
    Source,
    TaskSummary,
    UnitWeight,
)


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
    task_summary = TaskSummary(
        question=("Below what temperature does a material with this chemical composition become superconducting?"),
        use_case=("A materials scientist screens candidate compositions and decides which to synthesize and measure."),
        row="One measured entry of the SuperCon database; a composition can have several entries.",
        predicted="The critical temperature, in kelvin.",
        known=(
            "81 numbers computed from the chemical formula alone (statistics of the elements' atomic properties, "
            "weighted by their shares)."
        ),
        split=(
            "Whole compositions are held out, so the test data stands for compositions never measured; other "
            "proportions of the same elements can be in training."
        ),
        changes=(
            "We group the entries by composition; with random rows, 35% of the test rows had an identical row in "
            "training. Each composition counts once in the score, where the source counts each entry."
        ),
        fit="approximate",
        fit_reason=(
            "The features come from the formula, which is all a scientist has before synthesis, and the held-out "
            "compositions match screening new ones. But every row is a known superconductor (all critical "
            "temperatures above 0 K), while most candidates do not superconduct, so a model trained here gives every "
            "candidate a critical temperature."
        ),
    )

    # Dataset
    unique_name = "superconductivity"
    domain = "physics & astronomy"
    sources = (
        Source(
            role="publication",
            platform="UCI",
            url="https://doi.org/10.24432/C53P47",
            license="CC BY 4.0",
            year="2018",
            bibtex="""
                @article{hamidieh2018data,
                  title={A data-driven statistical model for predicting the critical temperature of a superconductor},
                  author={Hamidieh, Kam},
                  journal={Computational Materials Science},
                  volume={154},
                  pages={346--354},
                  year={2018},
                  publisher={Elsevier}
                }
            """,
        ),
    )
    data_tags = ("UnseenGroup",)
    download_description = """
        We download the data from the UCI repository and uzip it to a predefined folder.

        mkdir -p local-data-warehouse/superconductivity/ && wget -P local-data-warehouse/superconductivity/ https://archive.ics.uci.edu/static/public/464/superconductivty+data.zip && unzip local-data-warehouse/superconductivity/superconductivty+data.zip -d local-data-warehouse/superconductivity/ && rm local-data-warehouse/superconductivity/superconductivty+data.zip
    """
    curation_comments = """
        - The 81 features are computed from the element shares of the chemical formula alone. `unique_m.csv` (row-aligned with `train.csv`, same critical temperatures) has each row's element counts and formula; from it we add the group column `composition` (see `composition_labels`): 15,164 compositions, 2,422 of them with 2 to 110 SuperCon entries (6,099 repeated rows). Their temperatures differ by a median standard deviation of 1.3 K, by more than 30 K for 132 compositions (other samples, phases or pressures, which the release does not record).
<<<<<<< HEAD
        - Grouped by composition since 2026-10-06 (IID before): a model like this is used for compositions without a measured temperature, and a random split gave 35% of the test rows an identical row in train. Every entry is kept (SPLIT-26), and each composition counts once in the score (Lennart, 2026-11-08, review issue 1): the RMSE weights an entry by 1 over its composition's number of entries (`composition_weight`), a scoring column for the metric only, no feature and no training weight. All 81 inputs are fixed by the composition (equal within 2,416 of the 2,422 compositions with several entries; in the other 6, formulas written at another scale such as `Au30Pd3.3Te66.6` and `Au0.3Pd0.033Te0.666`, they differ by floating-point noise, at most 3e-15 relative), so a model predicts one value per composition, and the materials scientist decides per composition which to synthesize (MET-1, MET-17). Unweighted, YBa2Cu3O7 (110 entries) counted 110 times a composition measured once, and the 2,422 compositions with several entries held 40% of the rows; weighted, the 12,742 compositions with one entry carry 84% of the weight. On the 9 shipped splits the weighted RMSE ranks 8 untuned predictors (random forest, extra trees, two LightGBM, two ridge, kNN, the training mean) like the per-entry RMSE at Kendall tau 0.98 per split on average (lowest 0.93) and 0.93 for the ranking by the mean over the splits, the same best model on 9 of 9. Not grouped by element set: a new composition is usually another proportion of known elements (a doping level), not a new family. Stanev et al. (2018) average the entries of a material instead (standard deviation below 5 K) and drop the rest; we keep the release's rows.
        - Time basis: UnseenGroup (Andrej, 2026-11-13; no prototype tag before, 2026-11-12, review issue 5). The source
          keeps its model to known chemistry: Hamidieh (2018) offers it to researchers "interested in finding high
          temperature superconductors" to "narrow their search", warns "We should not expect good predictions for
          completely new superconductors" and says it "only gives predictions for superconductors"; it scored random
          splits of 2/3 train and 1/3 test, 25 times. Holding out whole compositions stands for that question (SPLIT-34,
          the source's scope), and the catalogue's later families lie outside it. The catalogue does move with time,
          measured and recorded here: dated through the MDR SuperCon Datasheet Ver.240322 (NIMS, doi:10.48505/nims.4487,
          CC BY 4.0; 21,163 of the 21,263 rows, 99.5%), it grew in waves of families (the cuprates from 1986, MgB2 in
          2001, the iron-based superconductors from 2008). Windows by first report year (1996-2001, 2002-2008,
          2009-2019) leave 23-51% of the test compositions an element-set sibling in training, against 79-86% when the
          same compositions are held out from all years (untuned LightGBM RMSE 18.2, 14.9 and 12.6 K against 14.2, 10.0
          and 8.6 K; Slurm job 1377613). The split cannot test a family of superconductors not yet known, which the
          source leaves out.
=======
        - Grouped by composition since 2026-10-06 (IID before): a model like this is used for compositions without a measured temperature, and a random split gave 35% of the test rows an identical row in train. Every entry is kept (SPLIT-26), and each composition counts once in the score (Lennart, 2026-11-08, review issue 4, issue 1 of that round): the RMSE weights an entry by 1 over its composition's number of entries (`composition_weight`), a scoring column for the metric only, no feature and no training weight. All 81 inputs are fixed by the composition (equal within 2,416 of the 2,422 compositions with several entries; in the other 6, formulas written at another scale such as `Au30Pd3.3Te66.6` and `Au0.3Pd0.033Te0.666`, they differ by floating-point noise, at most 3e-15 relative), so a model predicts one value per composition, and the materials scientist decides per composition which to synthesize (MET-1, MET-17). Unweighted, YBa2Cu3O7 (110 entries) counted 110 times a composition measured once, and the 2,422 compositions with several entries held 40% of the rows; weighted, the 12,742 compositions with one entry carry 84% of the weight. On the 9 shipped splits the weighted RMSE ranks 8 untuned predictors (random forest, extra trees, two LightGBM, two ridge, kNN, the training mean) like the per-entry RMSE at Kendall tau 0.98 per split on average (lowest 0.93) and 0.93 for the ranking by the mean over the splits, the same best model on 9 of 9. Not grouped by element set: a new composition is usually another proportion of known elements (a doping level), not a new family. Stanev et al. (2018) average the entries of a material instead (standard deviation below 5 K) and drop the rest; we keep the release's rows.
        - Grouped by composition since 2026-10-06 (IID before): a model like this is used for compositions without a measured temperature, and a random split gave 35% of the test rows an identical row in train. Every entry is kept (SPLIT-26), and each composition counts once in the score (Lennart, 2026-11-08, review issue 1): the RMSE weights an entry by 1 over its composition's number of entries (`composition_weight`), a scoring column for the metric only, no feature and no training weight. All 81 inputs are fixed by the composition (equal within 2,416 of the 2,422 compositions with several entries; in the other 6, formulas written at another scale such as `Au30Pd3.3Te66.6` and `Au0.3Pd0.033Te0.666`, they differ by floating-point noise, at most 3e-15 relative), so a model predicts one value per composition, and the materials scientist decides per composition which to synthesize (MET-1, MET-17). Unweighted, YBa2Cu3O7 (110 entries) counted 110 times a composition measured once, and the 2,422 compositions with several entries held 40% of the rows; weighted, the 12,742 compositions with one entry carry 84% of the weight. On the 9 shipped splits the weighted RMSE ranks 8 untuned predictors (random forest, extra trees, two LightGBM, two ridge, kNN, the training mean) like the per-entry RMSE at Kendall tau 0.98 per split on average (lowest 0.93) and 0.93 for the ranking by the mean over the splits, the same best model on 9 of 9. Not grouped by element set: a new composition is usually another proportion of known elements (a doping level), not a new family. Stanev et al. (2018) average the entries of a material instead (standard deviation below 5 K) and drop the rest; we keep the release's rows.
>>>>>>> 92aa0b49 (Splitting an expanding science catalogue (SPLIT-34), replayed onto #50 and #98)
    """

    # Task
    target = "critical_temp"
    problem_type = "regression"
    metric = Metric.from_context(
        "rmse",
        reason=(
            "Original: the out-of-sample RMSE of Hamidieh 2018 (Computational Materials Science 154:346-354, "
            "doi:10.1016/j.commatsci.2018.07.052; about 9.5 K for XGBoost, R2 about 0.92 alongside), which counts "
            "each SuperCon entry. Overruled on the unit (Lennart, 2026-11-08): every input is fixed by the "
            "composition and the materials scientist decides per composition, so the RMSE of the critical "
            "temperature in K weights an entry by 1 over its composition's number of entries "
            "(`composition_weight`) and each composition counts once, as Stanev et al. (2018) count each material "
            "once. Unweighted, YBa2Cu3O7 (110 entries) would count 110 times a composition measured once."
        ),
        inputs={"weight": "composition_weight"},
    )
    scoring_columns = (
        ScoringColumn(
            column="composition_weight",
            role="weight",
            used_by="rmse",
            description=(
                "1 over the number of SuperCon entries of the row's composition (from 1/110 to 1), so that each "
                "composition counts once in the RMSE; for scoring only, never a feature or a training weight"
            ),
        ),
    )
    unit_weight = UnitWeight(column="composition_weight", unit="composition")
    grouping = Grouping(
        on="composition",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a composition: the share of each element in the chemical formula, from which the 81 features are computed. Its rows are the SuperCon entries for that composition (1 to 110), whose critical temperatures can differ (other samples, phases or pressures that the release does not record). The source predicts the critical temperature from the formula alone (Hamidieh 2018), and a model like that is used for compositions without a measured temperature, so the test compositions are new to the model. Each row is one prediction, made from the composition's features; each composition counts once in the score (`composition_weight`).
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

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Each composition counts once in the score: 1 over its number of entries (curation comments)
        df["composition_weight"] = 1.0 / df.groupby("composition")["composition"].transform("size")
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
