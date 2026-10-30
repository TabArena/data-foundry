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
        split="Random policyholders are held out, representing comparable unseen customers in the released portfolio.",
        changes="We keep the original claim count and exclude the identifier and other same-period outcome fields.",
        fit="approximate",
        fit_reason=(
            "Realized exposure can reflect later cancellation and is retained by explicit curator choice; "
            "its availability at policy start is unresolved. Source large-claim preprocessing is documented, "
            "but excluded identities and complete-policy removal are unverified. This task does not "
            "establish full-portfolio or future-year performance."
        ),
    )

    unique_name = "bemtpl97"
    year = "2020"
    domain = "insurance"
    source = "GitHub"
    source_url = "https://github.com/henckr/treeML/tree/2ee8accc6df49168bd865cdf49efa1b7a5c8f4de"
    license = "GPL (>= 2), declared by CASdatasets; insurer-specific terms not verified"
    data_tags = ("Spatial",)
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
        We start with data/beMTPL97.rda from CASdatasets commit 227fb56b8734bdb7c0327a41180e01d2ddaeaf26, exactly equal as a parsed table to the pinned author's mtpl_data.rds. Normalize reader-produced column labels to Python strings so sklearn recognizes feature names; their text and all values stay unchanged.

        - Prediction point: quotation/policy start is the intended application. [Binning manuscript](https://roelverbelen.netlify.app/publication/binning/binning.pdf), section 2, p. 4: "The risk factors are registered at the start of the policy period". Realized exposure is not established as known then; the fit remains approximate.
        - Curator decision (2026-10-23, Myunghwan): retain original nclaims 0-5 as numeric regression and random policyholders. The earlier RMSE choice was superseded by the 2026-10-26 decision below. No annualization, log, clipping, binning, weighting, offset or row selection. Exposure remains a predictor because longer coverage permits more claims. Drop id and the same-period outcomes claim, amount and average; nclaims is never a predictor.
        - Potential leak, kept on purpose: expo measures actual insured time, one day to one year, which can reflect later cancellation. It stays by explicit curator choice. No event/cancellation timestamps ship, so neither the probes nor the source's policy-start risk-factor description verifies quotation-time exposure. Revisit if timing records become available.
        - Keep sex for historical research by curator choice; this establishes no fairness or suitability for commercial pricing. Keep postcode nominal and both municipality coordinates. The other categories are coverage, sex, fuel, use and fleet; ages, bonus-malus, power, exposure and coordinates remain numeric.
        - Keep all 163,212 distinct source policyholders, including legitimate coarse-profile repetitions: 133 extra exact rows, 168 extra predictor-profile copies and 35 conflicting profiles involving 70 rows (35 is also the checker's excess-row statistic). Matching profiles do not establish repeated people. The IID hidden-group probe found no hit; 147,308 rows lacked enough informative tokens for its near-copy comparison, so coverage is limited.
        - Keep all 144,936 zero-claim outcomes unchanged; 5 is an observed maximum, not our cap. Source-release selection remains: the earlier manuscript has 163,231 policies and its severity analysis excludes 19 high-cost cases (section 3.2, p. 11: "For 19 records the average claim cost exceeds this threshold", EUR 81,000). The [later paper](https://arxiv.org/pdf/1904.10890v3), section 4.1, p. 14, documents large-claim exclusion. This release has 18,276 claimants, but excluded identities cannot be checked against the unavailable extraction. Apply no extra tail filter.
        - Year 2020 is the verified author data commit of 30 April 2020, not observation year 1997; earliest public distribution is unverified. CASdatasets declares GPL (>= 2); insurer-specific terms and original extraction records remain unavailable. The earlier RMSE choice is historical; the curator-selected source metric is now mean Poisson deviance on expected observed-period counts.
        - Curator decision (2026-10-26, Myunghwan): supersede only RMSE with source mean Poisson deviance. Predict expected claim count over the recorded insured period against original nclaims. Keep all released rows, expo as a predictor, and the existing IID folds; no target transform, annualization, weighting, clipping, binning or extra row filter. The score particularly penalizes near-zero means when claims occur; this is not a general preference for every small absolute error.
        - Scoring protocol (AI, 2026-10-26): require strictly positive finite expected counts for the sklearn scorer and fixed-model diagnostics. This is an implementation protocol, not an additional verbatim curator instruction. The source likelihood zero-mean limits are documented below.
        - Source score: Henckaerts et al., arXiv:1904.10890v3, sections 3.2, 4.1 and 4.5; pinned treeML.Rmd lines 641-657 defines -2 times the mean Poisson log-likelihood ratio and scores nclaims against predicted frequency times expo. Our predictions already are expected counts, so exposure is not a separate scoring input. Use 2*mean(y*log(y/mu)-y+mu), with y*log(y/mu)=0 at y=0. sklearn requires finite y>=0 and finite mu>0. The source zero-mean limit is zero at y=0 and infinity at y>0; no clipping, epsilon floor or invalid-row omission is permitted.
        - Bounded Poisson qualification, revalidated after integration: same 163,212 rows and nine original IID folds, train-only preprocessing, fixed configurations, no HPO. All predicted means are finite and strictly positive without clipping. Mean Poisson deviance: training-mean dummy 0.551734632; poisson_linear 0.547592694 (9/9 wins), poisson_lightgbm 0.528534431 (9/9 wins), poisson_forest 0.529093723 (9/9 wins), bm_only_poisson 0.549323188 (9/9 wins), expo_only_poisson 0.551113166 (9/9 wins). These saved predictions were subsequently rescored against the integrated portable source scorer after verifying identical rows and all nine folds. No model refits are implied by that integration recheck. Official RMSE task-probe flags and old tuned rankings are not reused as Poisson evidence.
        - Direct integration follow-up (2026-10-26): register the sklearn-backed source metric and use domain-valid positive means for the library's synthetic computability test. Real model predictions remain subject to the strict scorer domain; no clipping, zero-label alteration, warning waiver or failed-score omission. Retained fixed-model predictions are reused only after exact row, target, fold and source-loss checks.

    """

    target = "nclaims"
    problem_type = "regression"
    metric = Metric.source(
        "mean_poisson_deviance",
        original="Mean Poisson deviance of observed claims against expected observed-period claim counts",
        reference="https://github.com/henckr/treeML/blob/2ee8accc6df49168bd865cdf49efa1b7a5c8f4de/treeML.Rmd#L641-L657",
        definition="2*mean(y*log(y/mu)-y+mu); zero y log term is zero; finite y>=0 and expected means mu>0",
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
        return FeatureTypes(categorical=["coverage", "sex", "fuel", "use", "fleet", "postcode"])

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
