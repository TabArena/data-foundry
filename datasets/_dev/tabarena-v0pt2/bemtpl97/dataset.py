"""Curated dataset definition for `bemtpl97` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, Metric, TaskSummary, decode, drop_columns

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
        question="How many claims will a motor-insurance policyholder make during their insured period?",
        use_case=(
            "For example, an EU motor insurer prices a third-party liability policy today: before quoting, its "
            "actuary estimates how many claims the policyholder will make during the insured period from the rating "
            "factors the insurer may use, learned here from a Belgian portfolio of 1997. Since 21 December 2012 EU "
            "law bars sex as a rating factor (CJEU C-236/09, Test-Achats), so the model does not see it."
        ),
        row="One of 163,231 policyholders of a Belgian motor-insurance portfolio observed in 1997, as first published in 2019.",
        predicted="Expected claims during the observed insured period; labels are original nclaims (observed 0-5).",
        known=(
            "At policy start the insurer knows the policyholder, vehicle, coverage and municipality; sex is left out, "
            "as EU insurers may no longer price on it. The share of 1997 insured is supplied, though its availability "
            "at quotation is unresolved: it is shorter when a policy started or was surrendered during the year, and "
            "per insured year part-year policies claim 1.6 to 2.3 times as often as full-year ones."
        ),
        split=(
            "Random policyholders are held out, representing comparable unseen customers of the same year; the "
            "portfolio has no dates, so no later year can be held out."
        ),
        changes=(
            "We keep the original claim count and every policyholder of the first public copy, and exclude the "
            "identifier, the municipality name, the same-period outcome fields and the policyholder's sex."
        ),
        fit="approximate",
        fit_reason=(
            "The insurer prices today, but the data is one undated year of a 1997 portfolio, so random policyholders "
            "of 1997 stand in for today's customers, whose rating factors and claim rates may differ. Sex is left "
            "out, as today's tariff must leave it out. Realized exposure is kept on purpose, although it can reflect "
            "a cancellation later in the year."
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
        - Target: the original nclaims, 0 to 5, as a count regression on every policyholder; no annualization, cap, weight or offset. We drop the identifier ID, the same-period outcomes AMOUNT and AVG (the release's amount and average; the 2019 copy has no claim column), and TOWN, the municipality name, which has one value per postcode and is not in the release.
        - Potential leak, kept on purpose: expo, the share of 1997 the policy was in force (one day to one year), is shorter for policyholders "who started the policy in the course of the year or surrendered the policy before the end of the year" ([arXiv:1904.10890v3](https://arxiv.org/pdf/1904.10890v3), Sec. 4.1). A start is known at quotation, a surrender (often after a claim) is not, and without dates the two cannot be told apart. The source puts exposure into the expected count in proportion (an offset with slope 1); here it is a free feature. Given the other features and a proportional offset, part-year policies claim about 1.4 times the expected count, and using expo freely instead of as an offset gains 0.0036 to 0.0041 of mean Poisson deviance, 16 to 18% of untuned LightGBM's skill over the training mean (3 and 9 folds; superseded 2026-11-05: 0.0039 on the 163,231 rows without sex, 0.0033 to 0.0047 per fold, 16% of the skill, 9 folds; the same run on the old frame gave 0.0040, 0.0036 to 0.0044; out of fold, a LightGBM offset model gives part-year policies 1.41 times the expected count on both frames). Revisit if policy dates become available.
        - Metric: the source's mean Poisson deviance of nclaims against the predicted expected count, by which it tunes and compares its frequency models ([arXiv:1904.10890v3](https://arxiv.org/pdf/1904.10890v3), Sec. 3.2 Eq. 5, Algorithm 3, Sec. 4.5; treeML.Rmd lines 641-657 score nclaims against frequency times expo). Exposure enters through the prediction, so it is neither a weight nor a scoring column. A predicted mean below 1e-6 counts as 1e-6 (Lennart, 2026-11-04: "in pratice we would also clip to a reasonable number"): one day of exposure at a 3% claim frequency is about 1e-4, so the floor sits two orders below the smallest plausible mean; a NaN or infinite prediction raises.
        - Dtypes: coverage is ordered, TPL < TPL+ < TPL++ (plus limited, then comprehensive material damage; CLEAN-14); fuel, use, fleet and postcode are nominal; the rest stay numeric. sex stays by curator choice, for research on a 1997 tariff (superseded 2026-11-05: sex leaves the features, CC below; it was nominal).
        - Copies kept: each row is a distinct source policyholder; the 133 extra exact rows and 35 conflicting profiles are coarse rating profiles that coincide (the IID hidden-group probe found none, though 147,308 rows were too sparse to compare; superseded 2026-11-05: 176 extra exact rows and 50 rows with a conflicting profile on the 163,231 rows without sex, and the probe again found none, 155,120 rows too sparse).
        - Selection by the release: the manuscript has 163,231 policies, 19 of them with an average claim cost above EUR 81,000 (Sec. 3.2, p. 11). The release is the 2019 copy of those 163,231 rows minus exactly these 19 (all claimants, 21 claims, 0.1% of all claims), the other rows identical and in the same order; the boosting paper evaluates on the 163,212. No further filter (superseded 2026-11-05: the 19 are restored, CC below, so no selection by claim cost remains).
        - Split forced IID from temporal (ForcedIIDFromTemporal, SPLIT-8): an insurer fits on past policy years and prices the next, but the portfolio is one undated year and its raw order (the 2019 copy's and the release's alike) is sorted by postcode, so no row-order window exists and the cost cannot be measured. A later year would test the drift of claim frequency; recover one if a release has it.
        - Year 2019: the first public copy is data/P&Cdata.txt in [katrienantonio/PE-pricing-analytics](https://github.com/katrienantonio/PE-pricing-analytics/tree/0b279c433de7c8ef46ebf0a33cd70ebd76d2af9e), added on 26 September 2019 with all 163,231 policies; we download the author's 2020 release of the 163,212 through CASdatasets (superseded 2026-11-05: we download this 2019 copy). The observation year is 1997. CASdatasets declares GPL (>= 2); the 2019 course repository states no licence; the insurer's terms are not stated.
        - CC (2026-11-05, Lennart): all 163,231 policies of the first public copy ship (issue 2, b; PROV-8, USE-5), not the release's 163,212, which leave out the 19 policies whose average claim cost exceeds EUR 81,000. Re-verified on 2026-11-05: the 2019 copy minus exactly its 19 rows with AVG above 81,000 equals the release row by row in the same order, every value equal to the 15 digits of the text file; the 19 hold 21 claims. The restored rows remove the selection by claim cost, so the record needs no `Selection Bias` marker for it. They are 19 rows more than the boosting paper evaluates on.
        - CC (2026-11-05, Lennart): sex leaves the features (issue 3, a). The actor is an EU insurer pricing today, and the Test-Achats ruling (CJEU C-236/09, 1 March 2011, in force for new contracts from 21 December 2012) bars sex as a rating factor: "We make this special case here as we would try to understand how good such models would be in the current world, and they would not be able to use sex". The 1997 portfolio stays the data, priced as an insurer would today, so the fit stays approximate. Sex carried 0.0004 of mean Poisson deviance (0.0002 to 0.0007 per fold, better in 9 of 9; 1.6% of the skill; untuned LightGBM-Poisson, 9 folds, 163,231 rows). With both changes the model scores 0.5279 against the training mean's 0.5520 (was 0.5274 against 0.5517: 4.4% skill each). The tension is a row in principles.md; home_credit_default_risk (CODE_GENDER) and credit_card_clients_default (SEX) keep sex, not reviewed yet.
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
            "The curator accepted claim-count regression on all policyholders, including nonclaimants."
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
        return decode(df, RELEASE_CODES).rename(columns=RELEASE_NAMES)[list(RELEASE_NAMES.values())]

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            ordinal={"coverage": ["TPL", "TPL+", "TPL++"]},  # TPL, plus limited, plus comprehensive damage
            categorical=["fuel", "use", "fleet", "postcode"],
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        features = df.drop(columns=[self.target])
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
