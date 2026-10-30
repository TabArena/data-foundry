"""Historical CPS weekly-wage estimation. Evidence: generated README.md and curation record."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, TaskSummary


class Cps88Wages(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="What weekly wage was recorded for a worker with these survey characteristics?",
        use_case=(
            "Historical estimation of unobserved wages among comparable survey respondents, approved by Myunghwan. "
            "This neither forecasts wages nor recommends pay or estimates causal effects."
        ),
        row=(
            "One of 28,155 male workers aged 18-70 in a selected March 1988 US Current Population Survey extract. "
            "The source includes Black and White workers and excludes self-employment and unpaid work."
        ),
        predicted=(
            "Weekly wage in 1992-price dollars: 1987 annual wage and salary earnings divided by weeks worked. "
            "The target is log1p(weekly wage), scored by mean absolute error on that transformed scale; expm1 recovers dollars."
        ),
        known=(
            "Education, potential work experience, ethnicity, metropolitan residence, US region and part-time "
            "status (less than 35 hours per week at the job last year)."
        ),
        split="Random survey records from the same historical population; default repeated three-fold splits.",
        changes="No rows or predictors removed; weekly wage transformed by log1p, without trimming or winsorization.",
        fit="direct",
        fit_reason=(
            "The approved task estimates a wage after the survey characteristics are available. It makes no "
            "future-cohort claim. Household and sampling-unit IDs and weights are absent, so independence "
            "under the survey design cannot be verified."
        ),
    )
    unique_name = "cps88wages"
    year = "Unknown (survey 1988)"
    domain = "social science"
    source = "Other"
    source_url = "https://doi.org/10.1007/s001810000059"
    license = "OpenML labels the release Public; a specific original-data licence is unverified."
    data_tags = ("Spatial",)
    download_description = """
        OpenML 44984 version 2 mirrors the Bierens and Ginther extract distributed as AER CPS1988.
        mkdir -p local-data-warehouse/cps88wages
        curl -fL https://data.openml.org/datasets/0004/44984/dataset_44984.pq -o local-data-warehouse/cps88wages/dataset_44984.pq
        SHA256: 823c50b089016402b8133f9f53ce391e129ec0f2a92328efdb86d701db17fd4a
    """
    bibtex = """
        @article{bierens2001quantile,
          title={Integrated Conditional Moment testing of quantile regression models},
          author={Bierens, Herman J. and Ginther, Donna K.},
          journal={Empirical Economics}, volume={26}, pages={307--324}, year={2001},
          doi={10.1007/s001810000059}
        }
    """
    curation_comments = """
        We start with OpenML 44984 version 2, checked against the AER CPS1988 CSV mirror.

        - Prediction point: survey characteristics are observed and wage is unknown to the model. Myunghwan approved
          historical estimation and ethnicity retention on 2026-10-26; no future or causal claim is intended.
        - All seven columns match the AER copy row for row; no missing cells. No respondent IDs, household IDs,
          timestamps, survey weights, annual earnings or weeks-worked predictors are released.
        - Education and potential experience are numeric; ethnicity, metropolitan residence, region and part-time
          status are nominal. The 438 negative experience values stay: age minus schooling minus six is a proxy,
          not actual years worked (AER documentation). No wage outlier is removed without evidence of error.
        - The 2,128 exact duplicate extras (7.56%) stay under Myunghwan's conditional retention decision after
          checks: 99.91% of test rows with a training profile match have a different training wage available.
          Train-only lookup rules underperform modeling; distinct identities remain unverified.
        - The source paper uses log-wage LAD fitting and ICM specification tests, not a unique held-out prediction
          scorer. Myunghwan chose log1p(wage) with absolute error on 2026-10-26,
          superseding the earlier exact-log proposal. This is context-selected scoring, not an official source score.
        - Only the target is transformed. The metric's explicit log1p scale metadata and portable implementation
          yield MAE on log1p wages, with no raw-dollar MAE, squaring, additional logging or clipping.
          Predictions are supplied on the transformed scale; negative transformed predictions are finite and scorable.
        - The survey occurred in 1988; the extract paper is from 2001. First release year and original-data licence
          remain unverified. On 2026-10-27 Myunghwan accepted the release-year uncertainty as nonblocking: survey
          year describes the data and does not affect this task. This is a local disposition, not verified release
          metadata. Original survey selection and possible disclosure controls are inherited.
    """
    target = "wage"
    problem_type = "regression"
    metric = Metric.from_context(
        "mean_absolute_log1p_error",
        reason=(
            "Myunghwan approved log1p(weekly wage) and absolute error on that scale on 2026-10-26. "
            "Relative-like errors reduce domination by high-dollar misses. "
            "The paper uses log-wage LAD fitting and specification tests, not an authenticated held-out scorer; "
            "this is a context-selected metric. Raw wages are all positive (minimum 50.05 dollars)."
        ),
        definition="mean(abs(log1p(actual weekly wage) - predicted log1p weekly wage)); no clipping",
        target_transform="log1p",
    )
    splits_comment = """
        Default IID repeated three-fold splits represent other records in this historical sample. No time axis or
        household/sampling-unit IDs are released. Demographic profiles are not verified person IDs, so matching
        profiles are not forced into groups.
    """

    accepted_check_warnings = {
        "dataset_duplicate_rows": (
            "Myunghwan permits retention if lookup does not dominate (2026-10-27). Across nine folds, "
            "99.91% of test rows with a training profile match have a different training wage available. "
            "Profile-median lookup has log1p MAE 0.4650 versus modeled 0.3909; distinct identities "
            "remain unverified. No source rows are removed."
        ),
        "dataset_conflicting_duplicate_rows": (
            "Retain differing wages for the same six coarse demographic predictors under the approved "
            "retention decision. 99.74% of repeated source profiles contain multiple wages; this is "
            "observed outcome variation, not an authenticated identity or reason to drop records."
        ),
        "meta_dataset_year": (
            "Myunghwan accepts the unknown first-release year as nonblocking (2026-10-27). "
            "The description gives survey year 1988; no verified release year is asserted."
        ),
    }

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_parquet(raw_dir / "dataset_44984.pq")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.copy()
        df["wage"] = np.log1p(df["wage"])
        # OpenML's ordered flags do not describe a ranking of these nominal responses.
        for column in ("ethnicity", "smsa", "region", "parttime"):
            df[column] = df[column].cat.as_unordered()
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["ethnicity", "smsa", "region", "parttime"])
