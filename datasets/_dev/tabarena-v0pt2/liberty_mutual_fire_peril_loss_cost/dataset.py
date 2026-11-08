"""Curated dataset definition for `liberty_mutual_fire_peril_loss_cost` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    ScoringColumn,
    TaskSummary,
    drop_columns,
)

# The policy variables the data page lists as categorical (ordinal var1, var3, var7, var8; nominal var2, var4, var5,
# var6, var9), each with "Z" for a missing value.
CATEGORICAL = [f"var{i}" for i in range(1, 10)]
TARGET = "log1p_transformed_loss_ratio"


class LibertyMutualFirePerilLossCost(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "How large will a business policy's fire loss be, relative to its total insured value, on the scale "
            "Liberty Mutual transformed it to?"
        ),
        use_case=(
            "Liberty Mutual, when it underwrites a commercial policy's fire cover, identifies the policyholder's risk "
            "exposure to tailor the coverage to the business's operation (the competition's description)."
        ),
        row=(
            "One business-insurance policy of Liberty Mutual with fire cover, perhaps one location of an account "
            "(452,061 policies, the competition's labelled half; the period and the length of the policy term are not "
            "stated)."
        ),
        predicted=(
            "The policy's fire loss as a ratio to its total insured value, transformed by the host in a way it did "
            "not disclose, shipped as its log1p and scored on the published scale; 99.74% of the policies had no loss."
        ),
        known=(
            "17 anonymised policy characteristics, among them a size measure the host uses as the score's weight, "
            "and the crime, geodemographic and weather variables of the policy's location."
        ),
        split=(
            "Random policies, as the competition split them. The file has no dates but holds several terms of many "
            "risks, so 17% to 54% of a test fold has its risk in training in another term, as when a renewal is "
            "priced; a risk's other terms carry nothing of its outcome."
        ),
        changes=(
            "We drop the row id, a nuisance column the host added and a weather column that is constant, code the "
            "host's missing level as missing, add the higher level of var4's hierarchical code, and ship the target "
            "as its log1p."
        ),
        fit="approximate",
        fit_reason=(
            "The decision is Liberty Mutual's own, but the transform of the target is not disclosed (58% of the "
            "losses exceed 1, so it is not a plain ratio of loss to insured value) and the features are anonymised; "
            "without dates, random policies stand in for the next term's policies."
        ),
    )

    # Dataset
    unique_name = "liberty_mutual_fire_peril_loss_cost"
    year = "2014"
    domain = "insurance"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/competitions/liberty-mutual-fire-peril"
    license = "Kaggle Competition Rules"
    data_tags = ("Anonymized", "Spatial", "ForcedIIDFromTemporal")
    download_description = """
        We use the train.csv of the Kaggle competition (the test half was never labelled publicly).

        kaggle competitions download -c liberty-mutual-fire-peril -f train.csv.zip && unzip train.csv.zip && rm train.csv.zip
        mkdir -p local-data-warehouse/liberty_mutual_fire_peril_loss_cost && mv train.csv local-data-warehouse/liberty_mutual_fire_peril_loss_cost/
    """
    bibtex = r"""
        @misc{LibertyMutual2014FirePerilLossCost,
          author = {{Liberty Mutual Group}},
          title  = {Liberty Mutual Group - Fire Peril Loss Cost},
          year   = {2014},
          howpublished = {\url{https://www.kaggle.com/competitions/liberty-mutual-fire-peril}},
          note   = {Kaggle competition}
        }
    """
    curation_comments = """
        We start with train.csv from the Kaggle competition (452,061 policies; the test half was never labelled publicly).

        - Prediction point: Liberty Mutual underwrites a commercial policy's fire cover, before the term. The host ships every feature in its test file, so it treats them as known then. The features are anonymised, but three checks pass. The weather block is the location's climate, not the term's weather: it stays the same in 94.6-96.9% of the consecutive terms of a risk, and the crime and geodemographic blocks never change (LEAK-10). `var13` changes at 23.1% of the terms with a loss against 28.3% of those without, so it is not updated after a loss (LEAK-38). The newest term of a risk has a loss as often as its earlier terms (0.261% against 0.292%, Fisher p 0.47), so recent losses are not missing (LEAK-24).
        - The target is the host's "transformed ratio of loss to total insured value" (data page), shipped as its log1p, `log1p_transformed_loss_ratio`, and scored on the published scale (`target_transform="log1p"`, MET-3), as in allstate_claim_prediction_challenge_1m. The transform is not disclosed, and 58% of the losses exceed 1, so the published value is not a plain ratio of loss to insured value (USE-5). The release records no term length, so the share of terms cut short is unknown and cannot be given; no feature carries a cut (`var17` is no share of a year, `var11` does not fall at loss terms), and the target is a ratio over the insured value, so it stays per contract (MET-14). 450,873 policies (99.74%) are exactly 0, the 1,188 losses run from 0.006 to 25.9 (skew 1.90 on the published scale, -0.16 on the log scale), none is negative or missing. A regularised LightGBM trained on the log1p scores 0.314 / 0.306 / 0.320 on the shipped folds, against 0.300 / 0.317 / 0.276 trained on the published scale (ahead on 2 of 3 folds, 0.313 against 0.298 on average).
        - We drop `id`: Kaggle randomised it ("We randomized the id column", forum thread 10026), and the loss rate is 0.25-0.28% in every id decile.
        - We drop `dummy`, a "Nuisance variable used to control the model, but not working as a predictor" (data page): it is `B` exactly where `var9` is `Z` (forum thread 10101), which `var9` keeps.
        - The level `Z` of `var1` to `var9` becomes missing ("Level "Z" in these variable represents a missing value", data page). These nine are categorical, as the data page lists them; the rest is numeric.
        - We add `var4_group`, the letter of `var4`: the data page says its levels "are in a hierarchical structure", the letter the higher level, and competitors split `var4` that way (forum thread 10194, "I split var4 into two values") (CLEAN-19).
        - We drop `weatherVar115`, 0 wherever present.
        - `var11` is the metric's weight ("var11 is the weight used in the weighted gini score calculation", data page) and stays a feature, and a copy, `var11_weight`, ships as the scoring column the metric reads (MET-2 as reworded on 2026-11-05: the scoring columns are the complete set of a metric's extra data; asked in PR #47's review). As a feature: the data page lists it among the "policy characteristics", the host ships it in the test file, and it behaves like the size of the risk (the decision "var11 behaves like the size of the risk"), known for train and test rows alike at underwriting (MET-2 as amended on the curator's call, Andrej, 2026-11-02). On the shipped folds `var11` as a feature gains +0.0004 (L2 on log1p) and +0.0032 (weighted by `var11`), within the fold standard deviation of about 0.04; 1/`var11` alone scores 0.071 (0.038 to 0.119), through risk selection (USE-6); `var11` is indexed by a median 1-2% a term and does not change more often going into a loss term (63.7% against 62.4% of the steps, Fisher p 0.70): a planned amount, not a realized one (LEAK-41).
        - The host "normalized" the blocks (data page): 213 of 289 numeric columns have a mean between 0.9 and 1.1. The constant is not these records' mean (177 of the 213 lie more than 10 standard errors from 1 on this half), so it comes from outside these records and carries nothing of a test row (LEAK-30); the unscaled values were never published.
        - We keep the exact copies: 28,965 rows (6.4%) equal another row in every column but `id` and `dummy` (16,981 extra copies). They are of two kinds: 11,433 extra copies have `var15` missing, so they may be terms whose age is not recorded, and 5,548 share a `var15`, so they are not terms but perhaps locations of one account. Every one of the 49 groups with a loss also holds a copy without one, and only 2 of the 1,188 losses have a copy with a loss: distinct policies the features cannot tell apart, with genuinely different outcomes (LEAK-19, LEAK-20; the decision "Exact copies"). 4.8-4.9% of the rows of a test fold have a copy in training.
        - Note: `var13` alone ranks the shipped test folds at a weighted Gini of 0.221-0.260 (ties averaged), the regularised LightGBM on the log1p target at 0.306-0.320, higher on every fold (TP-4: not trivial); the forum knew it ("target = -var13", thread 9706). Its loss rate falls from 0.41% to 0.04% over its range, like an underwriting grade, so it stays (LEAK-38).
        - Note: a test fold holds about 400 losses, so the weighted Gini of one model moves by a fold standard deviation of 0.042-0.045 (9 random or grouped folds; 0.035-0.072 within one repeat of 3 folds); differences between methods below that are fold noise (EV-8).
        - Anomaly: the location blocks are coarse: 2,588 distinct geodemographic vectors, 327 crime and 24,531 weather vectors.
    """

    accepted_check_warnings = {
        "task_metric_weight_without_sample_weight": (
            "var11, the size of the risk set at underwriting, is a feature: the metric's weight is a function of the "
            "features, so MET-15 needs no training weight (2026-11-06)."
        ),
        "task_target_value_dominant": (
            "Zero-inflated by nature: the target is 0 for the 450,873 policies (99.74%) without a fire loss; not a "
            "cap or a placeholder."
        ),
    }

    # Task
    target = TARGET
    problem_type = "regression"
    metric = Metric.source(
        "normalized_weighted_gini",
        original="Normalized weighted Gini coefficient, weights var11",
        reference="https://www.kaggle.com/competitions/liberty-mutual-fire-peril/overview/evaluation",
        inputs={"weight": "var11_weight"},
        target_transform="log1p",
    )
    scoring_columns = (
        ScoringColumn(
            column="var11_weight",
            role="weight",
            used_by="normalized_weighted_gini",
            description=(
                "a copy of var11 (the square root of a round sum insured, set at underwriting), the weight of the "
                "competition's Gini; var11 itself stays a feature"
            ),
        ),
    )
    splits_comment = """
        Default splits: random policies, as the competition split them ("The train and test sets are split randomly",
        data page), tagged as forced from temporal: an underwriter prices next term's policies, but the release has
        no dates and no risk id. The file holds consecutive terms of the same risks: 22.3% of the rows are equal to
        another in every column but `var15`, an age that steps by exactly 1 between them in 36,708 of the steps;
        47.5% when `var11` (the sum insured) may differ too, 63.9% when `var13` also may. On the shipped folds
        16.8-16.9%, 39.1-39.3% and 53.5-53.7% of the test rows have their risk in training on these three keys, and
        6.2-6.3%, 18.1-18.2% and 24.9% a later term of it (5.2% only later terms, on the first key). The risk
        carries nothing of the outcome: a risk's loss in training ranks its test terms at AUC 0.500-0.524 on every
        key, only 6 to 14 of the 1,188 losses share their risk with another loss, and taking a test risk's terms out
        of training costs no more than dropping as many random rows (paired on each fold). So the later terms in
        training are no measurable shortcut and stay (SPLIT-9; as in lending_club and avito_demand_prediction_1m).
        We read the risk as no group new data would lack: an insurer prices renewals of its own risks (SPLIT-30).
        Holding out whole risks on the first key would be partial (43.0-43.1% of the test rows keep their risk in
        training on the third) and would test every renewal as a new risk. With the policy year, the split would be
        temporal (train on earlier terms, test on the next); the year should be taken if a release has it. Shipped
        forced on the curator's call (Andrej, 2026-11-02): a forced IID split ships only when no leak is found across
        the random split, as here (the shared risk carries no outcome); how_much_did_it_rain's `No` named a measured
        leak.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "train.csv", low_memory=False)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.copy()
        # The host's transformed loss ratio on the log1p scale (the metric inverts it: target_transform="log1p").
        df.insert(df.columns.get_loc("target"), TARGET, np.log1p(df.pop("target")))
        # The host's randomised row id, and its nuisance column (a recode of var9's missing level).
        df = drop_columns(df, ["id", "dummy"])
        # The data page's missing level of the categorical policy variables.
        df[CATEGORICAL] = df[CATEGORICAL].replace("Z", np.nan)
        # The higher level of var4's hierarchical code (the letter).
        df.insert(df.columns.get_loc("var4") + 1, "var4_group", df["var4"].str[0])
        # Constant where present.
        df = drop_columns(df, ["weatherVar115"])
        # The metric's weight is also a feature: a copy ships as the scoring column the metric reads (MET-2).
        df["var11_weight"] = df["var11"]
        # Exact copies across all features stay (curation_comments, the decision "Exact copies").
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=[*CATEGORICAL, "var4_group"])

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        loss = raw["target"] > 0
        by_id = (
            loss.groupby(pd.qcut(raw["id"], 10, labels=range(1, 11)), observed=True)
            .mean()
            .mul(100)
            .round(3)
            .rename("loss rate (%)")
            .rename_axis("id decile")
        )
        dummy = pd.crosstab(raw["dummy"], raw["var9"].fillna("missing"))
        by_size = pd.DataFrame(
            {
                "policies": raw.groupby(pd.qcut(raw["var11"], 10), observed=True).size(),
                "loss rate (%)": loss.groupby(pd.qcut(raw["var11"], 10), observed=True).mean().mul(100).round(3),
                "median target of the losses": raw.loc[loss, "target"]
                .groupby(pd.qcut(raw["var11"], 10)[loss], observed=True)
                .median()
                .round(3),
            }
        ).rename_axis("var11 decile")
        features = [c for c in raw.columns if c not in ("id", "target", "dummy")]
        key = pd.util.hash_pandas_object(raw[features].astype("string").fillna("<NA>"), index=False)
        size = key.map(key.value_counts())
        copies = pd.DataFrame({"key": key, "loss": loss})[size > 1]
        per_group = copies.groupby("key")["loss"].agg(["size", "sum"])
        copy_table = pd.Series(
            {
                "rows that share all features with another row": len(copies),
                "groups of such rows": len(per_group),
                "extra copies (all but one per group)": len(copies) - len(per_group),
                "groups with a loss": int((per_group["sum"] > 0).sum()),
                "groups with a loss and a zero": int(
                    ((per_group["sum"] > 0) & (per_group["sum"] < per_group["size"])).sum()
                ),
                "losses whose group holds another loss": int(per_group.loc[per_group["sum"] > 1, "sum"].sum()),
                "losses in all": int(loss.sum()),
            },
            name="rows",
        )
        risk_columns = [c for c in features if c != "var15"]
        risk = pd.util.hash_pandas_object(raw[risk_columns].astype("string").fillna("<NA>"), index=False)
        terms = pd.DataFrame({"risk": risk, "var15": raw["var15"], "loss": loss})[risk.map(risk.value_counts()) > 1]
        steps = terms.sort_values(["risk", "var15"], kind="stable").groupby("risk")["var15"].diff().dropna()
        per_risk = terms.groupby("risk")["loss"].sum()
        terms_table = pd.Series(
            {
                "rows equal to another row in every column but var15": len(terms),
                "share of all rows (%)": round(100 * len(terms) / len(raw), 1),
                "risks (groups of such rows)": len(per_risk),
                "steps of var15 between a risk's rows (sorted) equal to 1": int((steps == 1).sum()),
                "steps equal to 0": int((steps == 0).sum()),
                "other steps": int(((steps != 0) & (steps != 1)).sum()),
                "losses in such rows": int(terms["loss"].sum()),
                "losses whose risk holds another loss": int(per_risk[per_risk > 1].sum()),
            },
            name="rows",
        )
        return [
            Decision(
                "id dropped",
                "Kaggle randomised the id (forum thread 10026), and the loss rate is flat over its deciles.",
                by_id.to_frame(),
            ),
            Decision(
                "dummy dropped",
                "The host calls dummy a nuisance variable; it is B exactly where var9 is Z (missing), which var9 keeps.",
                dummy,
            ),
            Decision(
                "var11 behaves like the size of the risk",
                "Larger var11 means more policies with a loss but a smaller ratio of loss to insured value among "
                "them, as a sum insured would; it is the metric's weight and a policy characteristic.",
                by_size,
            ),
            Decision(
                "Exact copies",
                "Rows equal in every column of the file but id and dummy; every group with a loss also holds a "
                "copy without one.",
                copy_table,
            ),
            Decision(
                "Terms of one risk",
                "Rows equal in every column but var15, which then mostly steps by 1: consecutive terms of the same "
                "risk, kept in a random split (splits_comment); losses rarely recur on a risk.",
                terms_table,
            ),
        ]
