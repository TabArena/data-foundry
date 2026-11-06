"""Curated dataset definition for `bemtpl97` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import hashlib
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
    decode,
    drop_columns,
)

# The 2019 copy's names and codes as the author's 2020 release (and the boosting paper) write them.
RELEASE_NAMES = {
    "EXP": "expo",
    "NCLAIMS": "nclaims",
    "COVERAGE": "coverage",
    "AGEPH": "ageph",
    "BM": "bm",
    "POWER": "power",
    "AGEC": "agec",
    "FUEL": "fuel",
    "USE": "use",
    "FLEET": "fleet",
    "PC": "postcode",
    "LONG": "long",
    "LAT": "lat",
}
RELEASE_CODES = {"COVERAGE": {"TPL": "TPL", "PO": "TPL+", "FO": "TPL++"}, "FLEET": {"N": "0", "Y": "1"}}


class Bemtpl97(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How many claims per year insured will a motor-insurance policyholder make?",
        use_case=(
            "For example, an EU motor insurer prices a third-party liability policy today: before quoting the yearly "
            "premium, its actuary estimates the policyholder's expected claims per year insured from the rating "
            "factors the insurer may use, learned here from a Belgian portfolio of 1997. Since 21 December 2012 EU "
            "law bars sex as a rating factor (CJEU C-236/09, Test-Achats), so the model does not see it."
        ),
        row="One of 163,231 policyholders of a Belgian motor-insurance portfolio observed in 1997, as first published in 2019.",
        predicted=(
            "Claims per year insured: the claims of 1997 (0 to 5) divided by the share of 1997 insured. Each "
            "policyholder counts in proportion to that share, in training and scoring."
        ),
        known=(
            "At policy start the insurer knows the policyholder, vehicle, coverage and municipality; sex is left out, "
            "as EU insurers may no longer price on it. The share of 1997 insured is no input: it is shorter when a "
            "policy started or was surrendered during the year, often after a claim, so it is the rate's denominator "
            "and each policyholder's weight."
        ),
        split=(
            "Random policyholders are held out, representing comparable unseen customers of the same year; the "
            "portfolio has no dates, so no later year can be held out."
        ),
        changes=(
            "We divide the claim count by the share of 1997 insured and weight each policyholder by that share, as "
            "the source's models do with an offset. We keep every policyholder of the first public copy, and exclude "
            "the identifier, the municipality name, the same-period outcome fields and the policyholder's sex."
        ),
        fit="approximate",
        fit_reason=(
            "The insurer prices today, but the data is one undated year of a 1997 portfolio, so random policyholders "
            "of 1997 stand in for today's customers, whose rating factors and claim rates may differ. Sex is left "
            "out, as today's tariff must leave it out."
        ),
    )

    unique_name = "bemtpl97"
    year = "2019"
    domain = "insurance"
    source = "GitHub"
    source_url = "https://github.com/katrienantonio/PE-pricing-analytics/tree/0b279c433de7c8ef46ebf0a33cd70ebd76d2af9e"
    license = (
        "No licence stated by the 2019 course repository; CASdatasets declares GPL (>= 2) for the 2020 release of "
        "the same portfolio; insurer-specific terms not verified"
    )
    data_tags = ("Spatial", "ForcedIIDFromTemporal")
    download_description = """
        Download the first public copy of the portfolio (2019, all 163,231 policies), a tab-separated text file.
        mkdir -p "${DATA_FOUNDRY_WAREHOUSE:-local-data-warehouse}/bemtpl97"
        curl -L --fail "https://raw.githubusercontent.com/katrienantonio/PE-pricing-analytics/0b279c433de7c8ef46ebf0a33cd70ebd76d2af9e/data/P%26Cdata.txt" -o "${DATA_FOUNDRY_WAREHOUSE:-local-data-warehouse}/bemtpl97/P&Cdata.txt"
        Expected SHA-256: 90915897ec158f5e54f54ef1bbdbf9ce415d3fb29bd60aaa7f159b7b2a418aff.
        From the repository root, set DATA_FOUNDRY_DATASETS_ROOT=datasets/_dev/tabarena-v0pt2.
    """
    bibtex = r"""
        @misc{Antonio2019PricingAnalytics,
          author = {Antonio, Katrien},
          title = {PE-pricing-analytics: Pricing analytics in R, course material},
          year = {2019},
          howpublished = {\url{https://github.com/katrienantonio/PE-pricing-analytics}},
          note = {First public copy of the portfolio, data/P\&Cdata.txt (163,231 policies), added on 26 September
                  2019; commit 0b279c433de7c8ef46ebf0a33cd70ebd76d2af9e}
        }
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
        We start with data/P&Cdata.txt of [katrienantonio/PE-pricing-analytics](https://github.com/katrienantonio/PE-pricing-analytics/tree/0b279c433de7c8ef46ebf0a33cd70ebd76d2af9e) commit 0b279c433de7c8ef46ebf0a33cd70ebd76d2af9e, the first public copy (2019, all 163,231 policies), read with exact float parsing; its column names, coverage labels (PO as TPL+, FO as TPL++) and fleet codes (N and Y as 0 and 1) become those of the author's 2020 release (superseded 2026-11-05: until then we started with data/beMTPL97.rda from CASdatasets commit 227fb56b8734bdb7c0327a41180e01d2ddaeaf26, the release's 163,212 rows, equal as a parsed table to the author's mtpl_data.rds).

        - Prediction point: the quotation at policy start. [Binning manuscript](https://roelverbelen.netlify.app/publication/binning/binning.pdf), Sec. 2, p. 4: "The risk factors are registered at the start of the policy period and remain constant during this period". The quotation is today's, by an EU insurer (CC below on sex).
        - Target: nclaims_per_year = nclaims / expo, the claims per year insured (MET-14), with expo as the row weight of the metric and the training weight (`sample_weight`, MET-15) and never a feature (LEAK-41). nclaims (0 to 5, no cap) leaves the frame as a part of the target, and _clean checks that nclaims_per_year x expo gives it back. We drop the identifier ID, the same-period outcomes AMOUNT and AVG (the release's amount and average; the 2019 copy has no claim column), and TOWN, the municipality name, which has one value per postcode and is not in the release.
        - Exposure (LEAK-41, MET-15; issue 1, resolved 2026-11-06): expo, the share of 1997 the policy was in force (one day to one year), is shorter for policyholders "who started the policy in the course of the year or surrendered the policy before the end of the year" ([arXiv:1904.10890v3](https://arxiv.org/pdf/1904.10890v3), Sec. 4.1). A start is known at quotation, a surrender (often after a claim) is not, and without dates the two cannot be told apart. As a free feature it gained 0.0036 to 0.0041 of mean Poisson deviance over a proportional offset (16 to 18% of untuned LightGBM's skill; 0.0039 on the 163,231 rows without sex, 9 folds), part-year policies claimed about 1.4 times the offset model's expected count, and at the quote (every policy priced for a full year) the free model was 0.0002 to 0.0011 worse than the offset model and never better, its claims coming in 1.08 times its price. expo now ships as the rate's denominator and each row's weight, the source's offset model. With the background of month-end ends and first-of-month starts removed, the excess starts claim 0.094 a year and full years 0.126, so true starts show no excess claims and little legitimate signal goes with the feature.
        - Metric: the source's mean Poisson deviance, by which it tunes and compares its frequency models ([arXiv:1904.10890v3](https://arxiv.org/pdf/1904.10890v3), Sec. 3.2 Eq. 5, Algorithm 3, Sec. 4.5; treeML.Rmd lines 641-657 score nclaims against frequency times expo), here on the rate weighted by expo: sum(w*d)/sum(w) equals the source's count deviance of the expected count expo x rate times n/sum(expo) of the scored rows (about 1.12), so models rank as by the source's metric on every fold (MET-11, origin source). Floor 1e-4 claims per year on the predicted rate (MET-13 as amended on 2026-11-06; the rule of 2026-11-04, "in pratice we would also clip to a reasonable number", two orders below the smallest plausible rate, on the scale the metric scores); a NaN or infinite prediction raises.
        - Dtypes: coverage is ordered, TPL < TPL+ < TPL++ (plus limited, then comprehensive material damage; CLEAN-14); fuel, use, fleet and postcode are nominal; the rest stay numeric. sex stays by curator choice, for research on a 1997 tariff (superseded 2026-11-05: sex leaves the features, CC below; it was nominal).
        - Copies kept: each row is a distinct source policyholder; the 133 extra exact rows and 35 conflicting profiles are coarse rating profiles that coincide (the IID hidden-group probe found none, though 147,308 rows were too sparse to compare; superseded 2026-11-05: 176 extra exact rows and 50 rows with a conflicting profile on the 163,231 rows without sex, and the probe again found none, 155,120 rows too sparse).
        - Selection by the release: the manuscript has 163,231 policies, 19 of them with an average claim cost above EUR 81,000 (Sec. 3.2, p. 11). The release is the 2019 copy of those 163,231 rows minus exactly these 19 (all claimants, 21 claims, 0.1% of all claims), the other rows identical and in the same order; the boosting paper evaluates on the 163,212. No further filter (superseded 2026-11-05: the 19 are restored, CC below, so no selection by claim cost remains).
        - Split forced IID from temporal (ForcedIIDFromTemporal, SPLIT-8): an insurer fits on past policy years and prices the next, but the portfolio is one undated year and its raw order (the 2019 copy's and the release's alike) is sorted by postcode, so no row-order window exists and the cost cannot be measured. A later year would test the drift of claim frequency; recover one if a release has it.
        - Year 2019: the first public copy is data/P&Cdata.txt in [katrienantonio/PE-pricing-analytics](https://github.com/katrienantonio/PE-pricing-analytics/tree/0b279c433de7c8ef46ebf0a33cd70ebd76d2af9e), added on 26 September 2019 with all 163,231 policies; we download the author's 2020 release of the 163,212 through CASdatasets (superseded 2026-11-05: we download this 2019 copy). The observation year is 1997. CASdatasets declares GPL (>= 2); the 2019 course repository states no licence; the insurer's terms are not stated.
        - CC (2026-11-05, Lennart): all 163,231 policies of the first public copy ship (issue 2, b; PROV-8, USE-5), not the release's 163,212, which leave out the 19 policies whose average claim cost exceeds EUR 81,000. Re-verified on 2026-11-05: the 2019 copy minus exactly its 19 rows with AVG above 81,000 equals the release row by row in the same order, every value equal to the 15 digits of the text file; the 19 hold 21 claims. The restored rows remove the selection by claim cost, so the record needs no `Selection Bias` marker for it. They are 19 rows more than the boosting paper evaluates on.
        - CC (2026-11-05, Lennart): sex leaves the features (issue 3, a). The actor is an EU insurer pricing today, and the Test-Achats ruling (CJEU C-236/09, 1 March 2011, in force for new contracts from 21 December 2012) bars sex as a rating factor: "We make this special case here as we would try to understand how good such models would be in the current world, and they would not be able to use sex". The 1997 portfolio stays the data, priced as an insurer would today, so the fit stays approximate. Sex carried 0.0004 of mean Poisson deviance (0.0002 to 0.0007 per fold, better in 9 of 9; 1.6% of the skill; untuned LightGBM-Poisson, 9 folds, 163,231 rows). With both changes the model scores 0.5279 against the training mean's 0.5520 (was 0.5274 against 0.5517: 4.4% skill each). The tension is a row in principles.md; home_credit_default_risk (CODE_GENDER) and credit_card_clients_default (SEX) keep sex, not reviewed yet.
        - CC (2026-11-06, Lennart): issue 1 resolved by its option B as the rate with a sample weight (option A of https://github.com/TabArena/data-foundry/issues/51): the target is the claims per year insured, expo the weight of the metric and of training and never a feature (LEAK-41, MET-14, MET-15), the floor 1e-4 a year (MET-13). Supersedes Myunghwan's calls of 2026-10-23 ("Retain expo ... Do not annualize, bin, clip, weight") and 2026-10-26 ("expo as a predictor") and the floor of 2026-11-04 (1e-6 on the expected count): the conditional measurement came later (+0.0043, 17% of the skill; never better at quotation), the source itself scores with an offset, and with the weight, dividing does not inflate short records. The built container 01a18ad7 is superseded.
    """

    target = "nclaims_per_year"
    problem_type = "regression"
    metric = Metric.source(
        "mean_poisson_deviance",
        original="Mean Poisson deviance of observed claims against expected observed-period claim counts",
        reference="https://github.com/henckr/treeML/blob/2ee8accc6df49168bd865cdf49efa1b7a5c8f4de/treeML.Rmd#L641-L657",
        params={"min_prediction": 1e-4},
        inputs={"weight": "expo"},
        definition=(
            "2*sum(w*(y*log(y/mu)-y+mu))/sum(w) over the claims per year y and the predicted rates mu, w = expo (the "
            "share of 1997 insured); zero y log term is zero; mu below 1e-4 claims per year counts as 1e-4. Equals the "
            "source's mean count deviance of the expected counts expo*mu times n/sum(expo) of the scored rows (about "
            "1.12)"
        ),
    )
    scoring_columns = (
        ScoringColumn(
            column="expo",
            role="weight",
            used_by="mean_poisson_deviance",
            description=(
                "the share of 1997 the policy was in force (one day to one year), realized: shorter when the policy "
                "started or was surrendered during the year, a surrender often after a claim. The rate's denominator; "
                "each row's weight in the metric and in training; never a feature"
            ),
        ),
    )
    sample_weight = "expo"
    accepted_check_warnings = {
        "task_target_value_dominant": (
            "The 144,936 zero rates are policyholders without a claim in 1997, not censoring or missing-value "
            "placeholders: claim frequency on all policyholders, including nonclaimants."
        ),
    }
    splits_comment = """
        Default IID protocol: random 3-fold cross-validation repeated 3 times for this population, with the
        benchmark split seed 4267 after the base class's content ordering and shuffle with seed 42.
        Each row is a distinct policyholder; test customers are unseen, while municipalities may recur.
        This evaluates comparable customers within the historical portfolio, not future years or insurers.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        path = raw_dir / "P&Cdata.txt"
        expected = "90915897ec158f5e54f54ef1bbdbf9ce415d3fb29bd60aaa7f159b7b2a418aff"
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError("P&Cdata.txt does not match the pinned 2019 copy")
        raw = pd.read_csv(path, sep="\t", float_precision="round_trip")
        if len(raw) != 163_231:
            raise ValueError(f"Expected the 163,231 policies of the 2019 copy, got {len(raw):,}")
        return raw

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        if not raw["ID"].is_unique:
            raise ValueError("Expected one row per policyholder")
        if raw["EXP"].isna().any() or not raw["EXP"].between(1 / 365 - 1e-12, 1).all():  # 15 digits in the text
            raise ValueError("Expected observed exposure between one day and one year")
        if raw.groupby("PC")["TOWN"].nunique().max() != 1:
            raise ValueError("Expected one municipality name per postcode")
        df = drop_columns(raw, ["ID", "AMOUNT", "AVG", "TOWN", "SEX"])
        df = decode(df, RELEASE_CODES).rename(columns=RELEASE_NAMES)[list(RELEASE_NAMES.values())]
        # Claims per year insured, weighted by the share of 1997 insured (MET-14, MET-15): the count leaves the frame as
        # a part of the target, and expo stays only as the weight scoring column, never a feature (LEAK-41).
        df["nclaims_per_year"] = df["nclaims"] / df["expo"]
        if not np.allclose(df["nclaims_per_year"] * df["expo"], df["nclaims"], rtol=0, atol=1e-9):
            raise ValueError("Expected nclaims_per_year x expo to give back nclaims")
        return drop_columns(df, ["nclaims"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            ordinal={"coverage": ["TPL", "TPL+", "TPL++"]},  # TPL, plus limited, plus comprehensive damage
            categorical=["fuel", "use", "fleet", "postcode"],
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        features = df.drop(columns=[self.target, "expo"])  # the weight is no feature
        evidence = pd.Series(
            {
                "policyholders in the 2019 copy": len(raw),
                "distinct source IDs": raw["ID"].nunique(),
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
                "coincide naturally; no person-level duplication is established, so every row is kept.",
                evidence,
            )
        ]
