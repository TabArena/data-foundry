"""Curated economic well-being prediction task (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.bundle_checks import CheckResult
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    SplitPlan,
    TaskSummary,
    Temporal,
    decode,
    drop_columns,
)

CODE_LABELS = {"urban_or_rural": {"R": "Rural", "U": "Urban"}}

PERIOD_ENDS = {
    "ghsl_built_1990_to_2000": 2000,
    "ghsl_built_2000_to_2014": 2014,
    "ghsl_not_built_up": 2014,
}
LAND_COVER = (
    "landcover_crops_fraction",
    "landcover_urban_fraction",
    "landcover_water_permanent_10km_fraction",
    "landcover_water_seasonal_10km_fraction",
)
TEST_YEARS = (2016, 2015, 2014)


class EconomicWellBeingPredictionChallenge(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="What is a survey cluster's wealth index in a later year and an unseen country?",
        use_case=(
            "An agency estimates historical local wealth where survey coverage is missing, to inform geographic "
            "targeting of support. A model trained on earlier surveys is evaluated on later surveys in another country."
        ),
        row="One survey-cluster observation in the released training file: 21,454 rows, 18 countries, 1994–2016.",
        predicted=(
            "The source's cluster-average, asset-related wealth index, from zero to one with higher values "
            "indicating greater wealth. It describes the survey year, not future income."
        ),
        known=(
            "Proposed inputs are the released survey year, urban/rural context, settlement history, water, population "
            "density, nighttime lights and distances. The represented years of water, population and lights remain "
            "unresolved. Known future settlement intervals are masked; survey-time alignment is not fully verified."
        ),
        split=(
            "Temporal × unseen-country evaluation: sixteen country-year tests in 2014–2016. Each model trains "
            "only on earlier years and excludes every "
            "row from its test country. Thus both year and country differ from training."
        ),
        changes=(
            "We mask explicit future settlement periods and their not-built residual, omit four temporally "
            "unmapped land-cover snapshots, and impose forward-year country exclusions. We keep all rows and labels."
        ),
        fit="approximate",
        fit_reason=(
            "The source's target formula, cross-survey harmonization and several covariate epochs are not "
            "documented. Myunghwan accepts calendar-year timing as an approximation; same-year endpoints are allowed. "
            "Later reconstructions "
            "of past states are allowed, but unknown represented epochs are not certified safe."
        ),
    )

    unique_name = "economic_well_being_prediction_challenge"
    year = "2021"
    domain = "social science"
    source = "Zindi"
    source_url = "https://zindi.world/competitions/aims-data-science-hackathon"
    license = "CC BY-SA 4.0"
    data_tags = ("Spatial",)
    download_description = """
        Obtain Train.csv from the Economic Well-Being Prediction Challenge data page:
        https://zindi.world/competitions/economic-well-being-prediction-challenge/data
        Place it at local-data-warehouse/economic_well_being_prediction_challenge/Train.csv.
        The inspected curator-provided file is 5,829,604 bytes; SHA-256
        caf159ff5c84630ca3ec61793ab362073cfed396e348ecca12f60f4d13efa93c.
        Login or acceptance of the source terms may be needed. An independent publisher checksum is unavailable.
        No other competition files are read. The original AIMS task and the public rerun describe the same task;
        no byte-for-byte comparison against the original AIMS download has been made.
    """
    bibtex = r"""
        @misc{Zindi2021EconomicWellBeing,
          author = {{Zindi} and {AIMS} and {Microsoft}},
          title = {AIMS Data Science Hackathon and Economic Well-Being Prediction Challenge},
          year = {2021},
          howpublished = {\url{https://zindi.world/competitions/aims-data-science-hackathon}},
          note = {Public Economic Well-Being challenge rerun on Zindi}
        }
    """
    curation_comments = """
        We start with the curator-provided Train.csv from Zindi's Economic Well-Being Prediction Challenge.

        - Prediction point: estimate a survey-year index using proposed same-year or earlier-state inputs and a model fitted to earlier survey years from other countries. This annual reconstruction permits same-calendar-year epoch endpoints; ordering against actual interviews cannot be verified. Some represented epochs remain unresolved. Myunghwan permits later-created measurements of past states (2026-10-31) and resolved the timing review using calendar-year approximation (2026-11-02). Exact feature epochs remain unverified.
        - Target: Myunghwan accepted prediction of the supplied source index with approximate fit when approving ship (2026-11-02). Retain all 21,454 supplied labels unchanged. They are a cluster-average wealth index on 0–1, not currency or a poverty probability. Exact survey instruments, construction, harmonization and reference normalization remain unverified; do not attribute a particular survey programme or PCA formula.
        - Temporal repair: mask ghsl_built_1990_to_2000 before 2000 and ghsl_built_2000_to_2014 before 2014. Also mask ghsl_not_built_up before 2014: its through-2014 residual can reconstruct the combined future construction from the other fractions. Only calendar-year precision is available: through-2000 and through-2014 fields remain on their endpoint-year rows. In 2014 tests the two 2014-ending fields are missing throughout training but observed in test, an intentional coverage change.
        - Omit four landcover_* columns: the source links a 2015–2019 product without saying which epoch was sampled. This is future state for pre-2015 rows, and we cannot assign a safe epoch to later rows. No replacement historical extraction was available; preserve the original raw file for repair.
        - Potential leak, unresolved: retain population density, nighttime lights and water under Myunghwan's instruction to keep columns absent established leakage. Their represented epochs are unknown; population products have several historical epochs. Source searches and repeated-location checks do not establish temporal safety. If later-state content is established, mask affected years or replace with historical values; omit an unrepaired field. Later production alone is no exclusion.
        - Year-comparison check (2026-11-02): water, population and light means vary in all 52 consecutive observed-year comparisons within 18 countries. The fixed 2000–2014 construction layer also varies in all 52 because survey years can sample different clusters. Five exact distance-signature groups span 1994–1995 (25 rows), with all 14 numeric geographic inputs unchanged; these are location proxies, not verified cluster IDs. This check cannot date the source layers. Myunghwan resolved issue 1 with year-level approximation; an established actual later-state measurement would still require repair.
        - Decode the source’s R/U urban_or_rural codes to Rural/Urban categorical labels (CLEAN-12, current main). Meanings are unchanged; unknown codes raise. Keep it as a category: the source starter notebook explicitly uses it. Generic metadata boilerplate does not identify this field as prohibited. Country and ID are used only to construct and verify splits, then removed from the model frame; year remains a numeric time input. No country/year frequency encodings or full-data statistics are added.
        - Keep all rows and numeric scales. Original labels are unique, and repeated predictor profiles are not established collection errors. Country exclusion prevents same-country repeats crossing a split. Zero numeric measurements remain zero; the source documents no alternative missing-code convention.
        - Evaluation: temporal × unseen-country, as explicitly confirmed by Myunghwan (2026-11-02). The sixteen tests are each observed country-year cell in 2014–2016. Every training side uses strictly earlier years, excludes the test country entirely and exceeds half the full sample. This adds a future-time requirement to the source's unseen-country task. Training sides overlap; country-year tests are not independent repeated samples.
        - Candidate-specific override of SPLIT-3 (Myunghwan, 2026-11-02; preserved 2026-11-05): temporal × unseen-country is the explicitly accepted future-year survey-gap task in an unseen country. Either single-regime substitution changes that task (USE-1, Must, P3); this is a higher-ranked use-case override, not an ordinary waiver of a Must. The global rule is unchanged.
        - Temporal limitation: survey year orders label content. Target harmonization using future actual states cannot be ruled out. Label publication dates are absent, a limitation on literal historical deployment claims rather than an extra acceptance gate for this retrospective task. These are open limits, not accepted warnings or cleared leakage findings.
    """

    target = "Target"
    problem_type = "regression"
    metric = Metric.source(
        "rmse",
        original="Root Mean Squared Error",
        reference="https://zindi.world/competitions/economic-well-being-prediction-challenge",
    )
    temporal = Temporal(on="year", horizon=1, horizon_unit="years")
    splits_comment = """
        Joint temporal × unseen-country evaluation: one test for each country observed in 2016, 2015 and 2014,
        newest year first, countries alphabetically within each year. For test country c in year t, training
        contains every row with year < t and country != c; test contains country == c and year == t.
        The backend stores Temporal metadata; the custom memberships enforce both chronology and whole-country
        exclusion. This is a joint evaluation regime. Each country-year test is stored as one temporal repeat with one fold. No test-country history is
        available to the learner. Country and opaque ID are dropped after index construction. All training
        sides exceed 50% of the original rows. Earlier rows are retained for training; not every row is tested.
        Annual survey content is ordered; publication delays remain unknown. The one-year horizon describes
        the test window, not an outcome follow-up duration. These tests share training data and countries.
    """
    accepted_check_warnings = {}

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "Train.csv", dtype={"ID": "str", "country": "str", "urban_or_rural": "str"})

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.copy()
        for column, end in PERIOD_ENDS.items():
            df.loc[df["year"] < end, column] = np.nan
        return decode(drop_columns(df, list(LAND_COVER)), CODE_LABELS)

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["country", "urban_or_rural"], string=["ID"])

    def _make_splits(self, df: pd.DataFrame) -> SplitPlan:
        splits = {}
        for test_year in TEST_YEARS:
            countries = sorted(df.loc[df["year"] == test_year, "country"].unique())
            for country in countries:
                train = np.flatnonzero((df["year"] < test_year) & (df["country"] != country))
                test = np.flatnonzero((df["year"] == test_year) & (df["country"] == country))
                if not len(test) or len(train) < len(df) / 2:
                    raise ValueError("A country-year split lacks the declared support")
                splits[len(splits)] = {0: (train.tolist(), test.tolist())}
        return SplitPlan(splits=splits, df=df.drop(columns=["country", "ID"]))

    def _extra_checks(self, container) -> list[CheckResult]:
        source = self.df
        bad = []
        for repeat, folds in container.experiment_metadata.splits.items():
            for fold, (train, test) in folds.items():
                tr, te = source.iloc[train], source.iloc[test]
                if tr["year"].max() >= te["year"].min() or set(tr["country"]) & set(te["country"]):
                    bad.append((repeat, fold))
        wrong_cells = {
            column: int(source.loc[source["year"] < end, column].notna().sum()) for column, end in PERIOD_ENDS.items()
        }
        if bad or any(wrong_cells.values()):
            return [CheckResult("economic_valid_time_country_error", "error", f"Bad splits {bad}, cells {wrong_cells}")]
        return [
            CheckResult(
                "economic_valid_time_country_verified",
                "info",
                "All explicit future-period cells masked; all 16 tests strictly later and wholly country-disjoint. "
                "Unspecified feature epochs remain unverified; annual endpoint alignment does not establish interview-time order.",
            )
        ]

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        masking = pd.DataFrame(
            [
                {"column": column, "period_end": end, "masked_rows": int((raw["year"] < end).sum())}
                for column, end in PERIOD_ENDS.items()
            ]
        )
        source = self.df
        plan = self.make_splits(source)
        support = []
        for repeat, folds in plan.splits.items():
            train, test = folds[0]
            support.append(
                {
                    "test": repeat,
                    "year": int(source.iloc[test]["year"].min()),
                    "country": str(source.iloc[test]["country"].iloc[0]),
                    "train_rows": len(train),
                    "test_rows": len(test),
                    "country_overlap": len(set(source.iloc[train]["country"]) & set(source.iloc[test]["country"])),
                }
            )
        return [
            Decision(
                "Remove explicit future-state information", "Mask by represented period, not production date.", masking
            ),
            Decision(
                "Future-year prediction in an unseen country",
                "Every country-year test excludes all country history.",
                pd.DataFrame(support),
            ),
        ]
