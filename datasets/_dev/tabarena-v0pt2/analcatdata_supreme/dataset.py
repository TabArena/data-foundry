"""Curated dataset definition for `analcatdata_supreme` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision

WINDOW_END_YEAR = 1988
"""The congressional actions are counted from 1979 to the end of 1988."""

MAX_EXPOSURE_YEARS = 10
"""A decision handed down before 1979 is in the 1979-1988 window for all of its 10 years."""

INDICATORS = ["liberal", "unconstitutional", "precedent_alteration", "unanimous", "lower_court_disagreement"]
"""The 0/1 attributes of a decision."""


def _potential_exposure_years(year: pd.Series) -> pd.Series:
    """Years a decision of ``year`` is in the 1979-1988 window if Congress does not overturn it first."""
    return np.minimum(MAX_EXPOSURE_YEARS, WINDOW_END_YEAR + 1 - year)


class AnalcatdataSupreme(AbstractCuratedDataset):
    # Dataset
    unique_name = "analcatdata_supreme"
    year = "2003"
    domain = "social science"
    source = "Other"
    source_url = "https://pages.stern.nyu.edu/~jsimonof/AnalCatData/Data/"
    data_tags = ("ForcedIIDFromTemporal",)
    license = (
        "Free for scientific, educational and/or noncommercial purposes with citation of Simonoff (2003) "
        "(NOTICE in the README of the StatLib analcatdata submission)"
    )
    download_description = """
        We download supreme.csv from the data page of Simonoff's book "Analyzing Categorical Data" (2003).
        StatLib's copy of the book's data (https://lib.stat.cmu.edu/datasets/analcatdata.zip, supreme.csv dated
        2002-01-17) is byte-identical. OpenML 504, 728 and 44040 hold the same rows under other column names and
        targets.

        mkdir -p local-data-warehouse/analcatdata_supreme
        wget -O local-data-warehouse/analcatdata_supreme/supreme.csv https://pages.stern.nyu.edu/~jsimonof/AnalCatData/Data/Comma_separated/supreme.csv

        sha256 of supreme.csv: 61c847ceb3e46191790bd72acf9e3c579a94e96045e65c0a698884aff17ed217
    """
    bibtex = r"""
        @article{zorn1998analytic,
          title={An Analytic and Empirical Examination of Zero-Inflated and Hurdle {P}oisson Specifications},
          author={Zorn, Christopher J. W.},
          journal={Sociological Methods \& Research},
          volume={26},
          number={3},
          pages={368--400},
          year={1998},
          doi={10.1177/0049124198026003004}
        }
        @book{simonoff2003analyzing,
          title={Analyzing Categorical Data},
          author={Simonoff, Jeffrey S.},
          series={Springer Texts in Statistics},
          publisher={Springer},
          address={New York},
          year={2003},
          doi={10.1007/978-0-387-21727-7}
        }
    """
    curation_comments = """
        We start with supreme.csv from the data page of Simonoff's "Analyzing Categorical Data" (2003): 4,052 Supreme Court decisions handed down 1953-1988 that fell under Judiciary Committee jurisdiction in 1979-1988, collected by Zorn (1998). One row is one decision.

        - Prediction point: when a decision is handed down (for a decision before 1979, in January 1979), we predict how many congressional actions it draws in the 1979-1988 window from its five 0/1 attributes, its year and the years it has in the window. The labels of all decisions become known together, at the end of 1988.
        - IID cross-validation over the decisions, not the temporal split the record asks for (tag `ForcedIIDFromTemporal`). Every label counts actions over the same window and the newer a decision, the shorter its exposure, so a temporal test window holds exposures no training decision has: on seven two-year windows the test mean as a constant scores skill +0.033, above every model (decision table). The book models all 4,052 decisions together, so we split them at random and keep the year and the exposure as features.
        - Target: log1p of the number of actions taken (`log1p_actions_taken`), the count Zorn (1998) models; 3,882 of 4,052 decisions (95.8%) have no action, and the zeros stay. OpenML 504 and 44040 use `Log exposure` as the target, but that column is the exposure term.
        - Leak fixed: the book says the exposure is shorter where "Congress overturned a decision before 1988", so a short `Log exposure` records the outcome. All 31 decisions whose exposure is at least two years shorter than their year allows, or longer, have an action, against 4.2% of all decisions (decision table).
        - We replace `Log exposure` by the exposure the decision year implies, log(min(10, 1989 - year)) rounded to two decimals as in the file, named `log_potential_exposure`. The 76 decisions one year below their year's value get it too: 10 of them (13.2%) have an action, against 6.2% of the decisions of those years whose exposure matches, so early overturns cannot be ruled out.
        - Small but real signal, kept (task-probe rule 2): the task probes flag `no_signal` (best skill +0.016, linear, under the 0.02 floor), but regularised models beat the train mean on all 9 shipped folds (LightGBM with 4 leaves +0.021 ± 0.003, Zorn's hurdle form +0.022 ± 0.003).
        - Duplicates kept: 3,486 rows (86.0%) are exact copies of another row. Five 0/1 attributes and the year leave 446 distinct feature vectors for 4,052 different decisions, so the repeats are natural.
        - We snake-case the column names and store the five 0/1 attributes and `year_of_decision` as integers (the file writes them with two decimals).
        - Note: the window right-censors the target on purpose (a 1988 decision had one year for action, one from 1979 or earlier ten); `log_potential_exposure` is the source's control for this.
        - Note: Zorn (1998) is paywalled and was not read; the meaning of the columns comes from the book's text quoted in the record and from the column names.
    """

    # Task
    target = "log1p_actions_taken"
    problem_type = "regression"

    # One string without code indentation: `make_splits` stores `splits_comment` as written (it is not dedented).
    splits_comment = (
        "The recommended IID splits: 3-fold cross-validation with 3 repeats over all 4,052 decisions. The rows carry "
        "the decision year, but a temporal split would not be valid: every label counts the actions of the same "
        "1979-1988 window and is known only at its end, and the newer a decision, the shorter its exposure, so a "
        "test window would hold exposures no training decision has. The source fits its count models to all "
        "decisions."
    )

    accepted_check_warnings = {
        "dataset_duplicate_rows": (
            "Each row is a different Supreme Court decision; five 0/1 attributes and the year leave 446 distinct "
            "feature vectors for 4,052 decisions, so exact repeats are natural."
        ),
        "dataset_conflicting_duplicate_rows": (
            "Decisions with the same attributes and year draw different numbers of actions: the noise of the task, "
            "not a label error."
        ),
        "task_target_low_cardinality": (
            "The target is a count of actions (0 to 11, 10 distinct values) on the log1p scale; the source models "
            "it as a count (Poisson, zero-inflated and hurdle models), so regression keeps its order and scale."
        ),
        "task_target_value_dominant": (
            "Zero-inflated count: 95.8% of the decisions draw no action. The zeros are real outcomes, not a cap or "
            "a placeholder, and the excess zeros are what Zorn (1998) studies."
        ),
    }

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "supreme.csv")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # Snake-case names, in the file's column order.
        df = raw.rename(columns=lambda name: name.lower().replace(" ", "_"))
        # The file writes every value with two decimals; the indicators and the year are integers.
        df = df.astype(dict.fromkeys([*INDICATORS, "year_of_decision"], "int64"))
        # Leak: the file's exposure is shortened when Congress overturned the decision, which is the outcome. Use
        # the exposure the decision year implies instead (rounded like the file's values).
        df["log_exposure"] = np.round(np.log(_potential_exposure_years(df["year_of_decision"])), 2)
        # Target: log1p of the number of actions.
        df["actions_taken"] = np.log1p(df["actions_taken"])
        return df.rename(columns={"actions_taken": "log1p_actions_taken", "log_exposure": "log_potential_exposure"})

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        year = raw["Year of decision"].astype(int)
        acted = raw["Actions taken"] > 0
        deviation = np.exp(raw["Log exposure"]).round().astype(int) - _potential_exposure_years(year)
        kind = pd.cut(
            deviation,
            bins=[-100, -2, -1, 0, 100],
            labels=["2 or more years shorter", "1 year shorter", "as the year implies", "longer"],
        )
        exposure = pd.DataFrame(
            {
                "decisions": acted.groupby(kind, observed=False).size(),
                "with an action": acted.groupby(kind, observed=False).sum(),
            }
        )
        exposure["share with an action"] = (exposure["with an action"] / exposure["decisions"]).map("{:.1%}".format)
        exposure.index.name = "file's exposure against the year"

        # The two-year windows a temporal split would test on, from 1975-76 (the oldest with half the rows in train).
        years = df["year_of_decision"]
        acted_df = df[self.target] > 0
        exposure_years = _potential_exposure_years(years)
        rows = []
        for start in range(WINDOW_END_YEAR - 1, 1974, -2):
            in_window = years.between(start, start + 1)
            before = years < start
            rows.append(
                {
                    "decision years": f"{start}-{start + 1}",
                    "decisions": int(in_window.sum()),
                    "exposure in 1979-1988 (years)": "-".join(
                        str(v)
                        for v in sorted({int(exposure_years[in_window].min()), int(exposure_years[in_window].max())})
                    ),
                    "lowest exposure of all earlier decisions": int(exposure_years[before].min()),
                    "share with an action": f"{acted_df[in_window].mean():.1%}",
                }
            )
        windows = pd.DataFrame(rows).set_index("decision years")
        return [
            Decision(
                "`Log exposure` replaced by the exposure the decision year implies",
                "A decision Congress overturned before 1988 has a shorter exposure, so an exposure that disagrees "
                "with the year marks a decision with an action. The year-implied value is known when the decision "
                "is handed down.",
                exposure,
            ),
            Decision(
                "IID splits, not temporal windows",
                "Every label counts the actions of the same 1979-1988 window, known only at its end. A temporal "
                "window would train on labels that did not exist at its test decisions' prediction point, and from "
                "1981-82 on it would test only exposures shorter than any training decision's, so its mean moves "
                "by construction.",
                windows,
            ),
        ]
