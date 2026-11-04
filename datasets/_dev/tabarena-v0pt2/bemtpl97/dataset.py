"""Curated dataset definition for `bemtpl97` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, Metric, TaskSummary, drop_columns


class Bemtpl97(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How many claims will a motor-insurance policyholder make during their insured period?",
        use_case=(
            "For example, an actuary studies risk differentiation before quoting a policy, using historical "
            "policyholders to estimate the number of claims during a customer's insured period."
        ),
        row="One of 163,212 distinct policyholders in a released Belgian motor-insurance portfolio observed in 1997.",
        predicted="Expected claims during the observed insured period; labels are original nclaims (observed 0-5).",
        known=(
            "The source describes policyholder, vehicle, coverage, claim-history and municipality characteristics "
            "at policy start. This benchmark additionally supplies realized insured duration, whose availability "
            "at quotation is unresolved. Exposure is the fraction of the year actually insured; longer coverage "
            "gives more opportunity for claims."
        ),
        split=(
            "Random policyholders are held out, representing comparable unseen customers of the same year; the "
            "release has no dates, so no later year can be held out."
        ),
        changes="We keep the original claim count and exclude the identifier and other same-period outcome fields.",
        fit="approximate",
        fit_reason=(
            "The policies carry no dates, so random policyholders of 1997 stand in for the next year's customers an "
            "insurer prices. Realized exposure is kept on purpose, although it can reflect a cancellation later in "
            "the year. The release's selection: the 19 policies whose average claim cost exceeds EUR 81,000 (0.1% "
            "of 18,295 claimants) are most likely removed."
        ),
    )

    unique_name = "bemtpl97"
    year = "2020"
    domain = "insurance"
    source = "GitHub"
    source_url = "https://github.com/henckr/treeML/tree/2ee8accc6df49168bd865cdf49efa1b7a5c8f4de"
    license = "GPL (>= 2), declared by CASdatasets; insurer-specific terms not verified"
    data_tags = ("Spatial", "ForcedIIDFromTemporal")
    download_description = """
        Download the CASdatasets copy, identical as a parsed table to the author's treeML release.
        Install rdata==1.1.0 and its dependencies in the environment used to run this definition.
        mkdir -p "${DATA_FOUNDRY_WAREHOUSE:-local-data-warehouse}/bemtpl97"
        curl -L --fail https://raw.githubusercontent.com/dutangc/CASdatasets/227fb56b8734bdb7c0327a41180e01d2ddaeaf26/data/beMTPL97.rda -o "${DATA_FOUNDRY_WAREHOUSE:-local-data-warehouse}/bemtpl97/beMTPL97.rda"
        Expected SHA-256: 955a821a7a693bf18076c425e4d5a5a99889f3c89e1fbd99eca6239c11e963a6.
        From the repository root, set DATA_FOUNDRY_DATASETS_ROOT=datasets/_dev/tabarena-v0pt2.
    """
    bibtex = r"""
        @misc{Henckaerts2020TreeMLData,
          author = {Henckaerts, Roel},
          title = {treeML: Motor third party liability insurance portfolio and code},
          year = {2020},
          howpublished = {\url{https://github.com/henckr/treeML}},
          note = {Data file mtpl\_data.rds added on 30 April 2020; commit 2ee8accc6df49168bd865cdf49efa1b7a5c8f4de}
        }
        @misc{Henckaerts2020Boosting,
          author = {Henckaerts, Roel and Côté, Marie-Pier and Antonio, Katrien and Verbelen, Roel},
          title = {Boosting insights in insurance tariff plans with tree-based machine learning methods},
          year = {2020},
          eprint = {1904.10890},
          note = {Version 3, 2 March 2020; accompanying author data release cited separately}
        }
    """
    curation_comments = """
        We start with data/beMTPL97.rda from CASdatasets commit 227fb56b8734bdb7c0327a41180e01d2ddaeaf26, equal as a parsed table to the pinned author's mtpl_data.rds; column labels become Python strings.

        - Prediction point: the quotation at policy start. [Binning manuscript](https://roelverbelen.netlify.app/publication/binning/binning.pdf), Sec. 2, p. 4: "The risk factors are registered at the start of the policy period and remain constant during this period".
        - Target: the original nclaims, 0 to 5, as a count regression on every policyholder; no annualization, cap, weight or offset. We drop id and the same-period outcomes claim, amount and average.
        - Potential leak, kept on purpose: expo, the share of 1997 the policy was in force (one day to one year), is shorter when the policyholder "surrendered the policy during the year" (p. 4), so it can record a later cancellation. It stays as the exposure the source puts into the expected count; a Poisson fit on log(expo) alone scores 0.5470 against the training mean's 0.5517 (nine folds). Revisit if policy dates become available.
        - Metric: the source's mean Poisson deviance of nclaims against the predicted expected count, by which it tunes and compares its frequency models ([arXiv:1904.10890v3](https://arxiv.org/pdf/1904.10890v3), Sec. 3.2 Eq. 5, Algorithm 3, Sec. 4.5; treeML.Rmd lines 641-657 score nclaims against frequency times expo). Exposure enters through the prediction, so it is neither a weight nor a scoring column. A predicted mean below 1e-6 counts as 1e-6 (Lennart, 2026-11-04: "in pratice we would also clip to a reasonable number"): one day of exposure at a 3% claim frequency is about 1e-4, so the floor sits two orders below the smallest plausible mean; a NaN or infinite prediction raises.
        - Dtypes: coverage is ordered, TPL < TPL+ < TPL++ (plus limited, then comprehensive material damage; CLEAN-14); sex, fuel, use, fleet and postcode are nominal; the rest stay numeric. sex stays by curator choice, for research on a 1997 tariff.
        - Copies kept: each row is a distinct source policyholder; the 133 extra exact rows and 35 conflicting profiles are coarse rating profiles that coincide (the IID hidden-group probe found none, though 147,308 rows were too sparse to compare).
        - Selection by the release: the manuscript has 163,231 policies, 19 of them with an average claim cost above EUR 81,000 (Sec. 3.2, p. 11); the release has 163,212, so it most likely dropped those 19. No further filter.
        - Split forced IID from temporal (ForcedIIDFromTemporal, SPLIT-8): an insurer fits on past policy years and prices the next, but the release is one undated year, so the cost cannot be measured. A later year would test the drift of claim frequency; recover one if a release has it.
        - Year 2020: the author's data commit of 30 April 2020, the earliest public copy found; the observation year is 1997. CASdatasets declares GPL (>= 2); the insurer's terms are not stated.
    """

    target = "nclaims"
    problem_type = "regression"
    metric = Metric.source(
        "mean_poisson_deviance",
        original="Mean Poisson deviance of observed claims against expected observed-period claim counts",
        reference="https://github.com/henckr/treeML/blob/2ee8accc6df49168bd865cdf49efa1b7a5c8f4de/treeML.Rmd#L641-L657",
        params={"min_prediction": 1e-6},
        definition="2*mean(y*log(y/mu)-y+mu); zero y log term is zero; finite y>=0; mu below 1e-6 counts as 1e-6",
    )
    accepted_check_warnings = {
        "task_target_low_cardinality": (
            "The curator explicitly confirmed regression on the original claim count, observed from 0 to 5. "
            "The target measures a numeric number of claims; it is not binned into classification labels."
        ),
        "task_target_value_dominant": (
            "The 144,936 zero labels are observed zero claims, not censoring or missing-value placeholders. "
            "The curator accepted claim-count regression on all released policyholders, including nonclaimants."
        ),
    }
    splits_comment = """
        Default IID protocol: random 3-fold cross-validation repeated 3 times for this population, with the
        benchmark split seed 4267 after the base class's content ordering and shuffle with seed 42.
        Each row is a distinct released policyholder; test customers are unseen, while municipalities may recur.
        This evaluates comparable customers within the selected historical portfolio, not future years or insurers.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        import rdata

        path = raw_dir / "beMTPL97.rda"
        expected = "955a821a7a693bf18076c425e4d5a5a99889f3c89e1fbd99eca6239c11e963a6"
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError("beMTPL97.rda does not match the pinned public release")
        return rdata.read_rda(path)["beMTPL97"]

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        if not raw["id"].is_unique:
            raise ValueError("Expected one released row per policyholder")
        if raw["expo"].isna().any() or not raw["expo"].between(1 / 365, 1).all():
            raise ValueError("Expected observed exposure between one day and one year")
        return drop_columns(raw.rename(columns=str), ["id", "claim", "amount", "average"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            ordinal={"coverage": ["TPL", "TPL+", "TPL++"]},  # TPL, plus limited, plus comprehensive damage
            categorical=["sex", "fuel", "use", "fleet", "postcode"],
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        features = df.drop(columns=[self.target])
        evidence = pd.Series(
            {
                "released policyholders": len(raw),
                "distinct source IDs": raw["id"].nunique(),
                "retained rows": len(df),
                "extra identical cleaned rows": df.duplicated().sum(),
                "rows in repeated predictor profiles": features.duplicated(keep=False).sum(),
                "extra predictor-profile copies": features.duplicated().sum(),
            },
            name="count",
        )
        return [
            Decision(
                "Preserve distinct policyholders with repeated coarse profiles",
                "The source documents unique policyholders. Coarse characteristics and zero-heavy outcomes can "
                "coincide naturally; no person-level duplication is established, so every released row is kept.",
                evidence,
            )
        ]
