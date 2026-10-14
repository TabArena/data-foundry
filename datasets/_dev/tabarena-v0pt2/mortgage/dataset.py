"""Curated dataset definition for `mortgage` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    TaskSummary,
    Temporal,
    TemporalSplits,
    drop_columns,
)

STATUS = {0: "active", 1: "default", 2: "payoff"}
"""The source's `status_time` codes ("Default (1), payoff (2), and nondefault/nonpayoff (0)") and our labels."""

LOAN_KEY = ["id", "orig_time", "balance_orig_time"]
"""A loan: a borrower id with its origination period and original balance (a few ids hold two mortgages)."""

LOAN_STATE = ["balance_time", "interest_rate_time"]
"""The loan's own state on a row, replaced by its value at the loan's previous observation (the LTV is recomputed)."""

MACRO_LAGS = {"hpi_time": 2, "gdp_time": 2, "uer_time": 1}
"""Quarters back to the newest value of each macro column that is published when a quarter starts. The house price
index of a quarter's last month and a quarter's GDP growth come out one to two months after the quarter ends, the
unemployment rate of a quarter's first month in its second month."""

REAL_ESTATE_FLAGS = {
    "REtype_CO_orig_time": "condominium",
    "REtype_PU_orig_time": "planned_urban_development",
    "REtype_SF_orig_time": "single_family",
}
"""The one-hot real-estate flags of the data page; a row with none of them set is `other`."""


def deduplicated(raw: pd.DataFrame) -> pd.DataFrame:
    """The raw rows with period 51's doubled records removed, keeping the event copy where two copies differ only in
    the status.
    """
    record = [c for c in raw.columns if c not in ("default_time", "payoff_time", "status_time")]
    return raw.sort_values("status_time", ascending=False, kind="stable").drop_duplicates(subset=record)


class Mortgage(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a mortgage default, be paid off, or stay active in the coming quarter?",
        use_case=(
            "At the start of each quarter, a lender scores every mortgage it holds for whether, during the quarter, "
            "it defaults, is paid off or stays active, as in the book's own out-of-time backtest."
        ),
        row=(
            "One US mortgage in one quarter, for 50,000 borrowers observed from 2000 Q2 to 2015 Q1 (Credit Risk "
            "Analytics, Baesens et al. 2016)."
        ),
        predicted=(
            "The loan's status at the end of the quarter: active (93.29%), paid off (4.27%) or defaulted (2.44%)."
        ),
        known=(
            "The quarter, the loan's dates (origination, first observation, maturity) and terms at origination "
            "(balance, rate, loan-to-value, credit score, property type, investor), its balance, rate and "
            "loan-to-value at the previous quarter, and unemployment, GDP growth and house prices as published by the"
            " quarter's start."
        ),
        split=(
            "Each test window is one quarter (2014 Q3, 2014 Q4, 2015 Q1), trained on every earlier quarter; a test "
            "loan's earlier quarters are in training, as for a lender scoring the loans it holds."
        ),
        changes=(
            "We use each loan's balance, rate and loan-to-value of the previous quarter and the economic figures as "
            "published by the quarter's start; the source's own-quarter values partly record the event or come out "
            "later."
        ),
        fit="direct",
        fit_reason=(
            "Everything the model sees is known when the quarter starts, the outcome falls within the quarter, and "
            "later quarters are tested, as in the book's backtest."
        ),
    )

    # Dataset
    unique_name = "mortgage"
    year = "2016"
    domain = "finance"
    source = "Other"
    source_url = "http://www.creditriskanalytics.net/datasets-private2.html"
    license = (
        "Use only in conjunction with the Credit Risk Analytics textbooks; commercial use prohibited (the agreement "
        "on the book's download form, http://www.creditriskanalytics.net/datasets.html). Note: the site's terms "
        '(http://www.creditriskanalytics.net/terms.html) say "You must not: Republish material from Credit Risk '
        'Analytics [...] Redistribute content from Credit Risk Analytics".'
    )
    download_description = """
        We download mortgage_csv.rar from the data page of the book "Credit Risk Analytics" (Baesens, Roesch and
        Scheule, Wiley 2016) and extract mortgage.csv from it. The book's site asks for a name and an agreement on
        http://www.creditriskanalytics.net/datasets.html before it shows the data page; the file link itself needs no
        login. Any RAR extractor works (unrar from https://www.rarlab.com, unar, 7z, bsdtar). The page also offers the
        data in two SAS formats (mortgage_9.4.rar, mortgage_earliersas.rar).

        mkdir -p local-data-warehouse/mortgage
        wget -O local-data-warehouse/mortgage/mortgage_csv.rar http://www.creditriskanalytics.net/uploads/1/9/5/1/19511601/mortgage_csv.rar
        unrar x local-data-warehouse/mortgage/mortgage_csv.rar local-data-warehouse/mortgage/
        rm local-data-warehouse/mortgage/mortgage_csv.rar

        sha256 of mortgage_csv.rar: 1ce1c9be8d9a86edef040ca54c392bbfd609354a852507db63f20776a0b88924
        sha256 of mortgage.csv: f8e819eb02a3bfb575d927c878e921faf6c0751e2e19056100e7e9dee76cc1a8 (68,397,638 bytes)
    """
    bibtex = r"""
        @book{baesens2016credit,
          title={Credit Risk Analytics: Measurement Techniques, Applications, and Examples in {SAS}},
          author={Baesens, Bart and R{\"o}sch, Daniel and Scheule, Harald},
          publisher={John Wiley \& Sons},
          address={Hoboken, NJ},
          year={2016},
          isbn={978-1-119-14398-7},
          doi={10.1002/9781119449560}
        }
    """
    curation_comments = """
        We start with mortgage.csv from the data page of the book Credit Risk Analytics (Baesens, Roesch and Scheule 2016): one row per loan and period for 50,000 US mortgage borrowers.

        - Prediction point: the start of each quarter. A lender scores every loan it still holds for whether, during the quarter, the loan defaults, is paid off or stays active.
        - Target: `status`, the source's `status_time`, as `default`, `payoff` and `active` (the competing-risks form of the R Companion, chapter 11); we drop its indicator columns `default_time` and `payoff_time`. Loans that leave the panel without an event keep their last row `active` as recorded.
        - The loan's balance, interest rate and LTV come from its previous observation (`*_lag_1`): on an event row the row's own state partly records the event (decision table), and the previous state is what the lender knows (garments_worker_productivity precedent).
        - The macro columns hold the predicted quarter's own values (as the book's PD models use them), published during or after it. We use the newest values published when the quarter starts: unemployment one quarter back, GDP growth and the house price index two quarters back (decision table).
        - `LTV_time_lag_1` follows the source's formula with the previous balance and the index two quarters back. `hpi_orig_time` is published two quarters after origination; until then it is missing and the LTV keeps the house value at origination.
        - Period 51 is doubled for 312 loans: we drop the exact copies and, where two copies differ only in the status, keep the payoff copy (the loan leaves the panel).
        - An origination interest rate, original balance or current interest rate of 0 becomes missing (89,990, 270 and 25 rows); the source's `LTV_time` is missing on exactly the zero-balance rows.
        - We drop `id`, the borrower id in file order. A few ids hold two mortgages, so a loan is an id with its origination period and original balance; this key only finds a loan's previous observation.
        - The three real-estate flags (at most one set per row) become one category `real_estate_type`, `other` where none is set.
        - Note: `time`, `orig_time`, `first_time` and `mat_time` stay period numbers; the periods are quarters from 2000 Q2 to 2015 Q1.
        - Kept as recorded: origination fields that change within a loan, interest rates above 25% (44 rows) and LTVs above 300% (38 rows).
        - Duplicate rows kept (58 of 622,177 rows without `id`): they come from 8 pairs of borrower ids with the same origination profile, mostly separate loans on the same terms.
        - Note: unlike the book's retired HMEQ data (homeq_default_prediction), the loans show no generation artefacts (label-free nearest-neighbour distance: ROC AUC 0.58 for default, HMEQ 0.92).
        - Split: temporal, one quarter per window, like the book's out-of-time backtest (splits comment).
        - Note: the task probes flag `drift_baseline`. The task stays (task_probes.md rule 2): LightGBM trained on the full train side beats the previous quarter's class shares in each window (period 60: log loss 0.1195 against 0.1251).
    """

    # Task
    target = "status"
    problem_type = "multiclass_classification"

    # Splits
    splits_comment = """
        The book's own out-of-time backtest fits on the periods before 60 and tests on period 60 (R Companion code,
        chapter 13, "Backtesting PD at level 1": `mortgage[mortgage$time < 60, ]` against
        `mortgage[mortgage$time > 59, ]`). We simulate a model that is refit every quarter and scores the loans active
        in the next one: 3 test windows of one period each, periods 60, 59 and 58 (2015 Q1, 2014 Q4 and 2014 Q3; newest
        first), each trained on all earlier periods. A test quarter's loans have their earlier quarters in train
        (99.4-99.9% of the test rows), as for a lender scoring the loans it holds. The status of a quarter is known
        when the next one starts, so every training label is known at the cutoff and there is no gap.
    """
    temporal = Temporal(
        on="time",
        splits=TemporalSplits(window=1, unit="unique", n_windows=3),
        horizon=1,  # one period, a quarter
        horizon_unit="steps",
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "mortgage.csv")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # Period 51 is doubled for 312 loans: keep one row per record, and the event copy where the two copies differ
        # only in the status.
        df = deduplicated(raw)

        # Number the loans (an id with its origination period and original balance) before the zeros become missing.
        df["loan"] = df.groupby(LOAN_KEY, sort=False).ngroup()

        # Proxy missing values: an origination rate, original balance or current rate of 0.
        for column in ["Interest_Rate_orig_time", "balance_orig_time", "interest_rate_time"]:
            df[column] = df[column].mask(df[column] == 0)

        # The loan's balance and rate at its previous observation, in place of the row's own state.
        df = df.sort_values(["loan", "time"], kind="stable")
        df[LOAN_STATE] = df.groupby("loan", sort=False)[LOAN_STATE].shift(1)

        # The macro values as published when the quarter starts (the source holds one value per period).
        assert (df.groupby("time")[list(MACRO_LAGS)].nunique() == 1).all().all()
        macro = df.groupby("time")[list(MACRO_LAGS)].first()
        for column, lag in MACRO_LAGS.items():
            df[column] = (df["time"] - lag).map(macro[column])

        # The LTV of the previous balance, by the source's formula (balance over the value at origination moved with
        # the house price index) with the index as published. The origination quarter's index is published two
        # quarters later; until then it is missing and the house keeps its value at origination.
        published = df["time"] - df["orig_time"] >= 2
        df["hpi_orig_time"] = df["hpi_orig_time"].where(published)
        index_change = (df["hpi_time"] / df["hpi_orig_time"]).where(published, 1.0)
        house_value = df["balance_orig_time"] / (df["LTV_orig_time"] / 100) * index_change
        df["LTV_time"] = df["balance_time"] / house_value * 100
        lagged = [*LOAN_STATE, "LTV_time"]
        df = df.rename(
            columns={**{c: f"{c}_lag_1" for c in lagged}, **{c: f"{c}_lag_{k}" for c, k in MACRO_LAGS.items()}}
        )

        # The one-hot real-estate flags as one category, in place of the first flag.
        flags = list(REAL_ESTATE_FLAGS)
        df[flags[0]] = np.select(
            [df[flag] == 1 for flag in flags], list(REAL_ESTATE_FLAGS.values()), default="other"
        ).astype(object)
        df = df.rename(columns={flags[0]: "real_estate_type"})

        # The target: the status of the period, with readable labels.
        df["status_time"] = df["status_time"].map(STATUS)
        df = df.rename(columns={"status_time": self.target})
        return drop_columns(df, ["id", "loan", "default_time", "payoff_time", *flags[1:]])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["real_estate_type"])

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        # How the row's own balance moves on event rows against the loan's previous row.
        frame = deduplicated(raw).sort_values([*LOAN_KEY, "time"], kind="stable")
        ratio = frame["balance_time"] / frame.groupby(LOAN_KEY, sort=False)["balance_time"].shift(1)
        rows = frame.assign(ratio=ratio)[ratio.notna()]
        rows = rows.assign(
            period=np.where(rows["time"] >= 58, "periods 58-60", "periods 2-57"),
            status=rows["status_time"].map(STATUS),
        )
        table = rows.groupby(["period", "status"]).agg(
            rows=("ratio", "size"),
            zero_balance=("balance_time", lambda s: f"{(s == 0).mean():.2%}"),
            balance_down_over_5pct=("ratio", lambda s: f"{(s < 0.95).mean():.1%}"),
            balance_unchanged=("ratio", lambda s: f"{(s == 1).mean():.1%}"),
        )
        windows = df[df["time"] >= 58].groupby("time")[self.target].value_counts().unstack()
        windows.index.name = "test period"
        own = raw.groupby("time")[list(MACRO_LAGS)].first()
        used = df.groupby("time")[[f"{c}_lag_{k}" for c, k in MACRO_LAGS.items()]].first()
        macro = pd.concat([own.add_suffix(" (own quarter)"), used], axis=1).loc[[60, 59, 58]].round(3)
        macro.index.name = "test period"
        return [
            Decision(
                "A loan's balance, LTV and rate come from its previous observation",
                "On an event row the row's own balance records the event (a paid-off or sharply reduced balance, a "
                "balance left unchanged by the missed payments that make a default). At the start of a quarter a "
                "lender knows the loan's state at its previous observation.",
                table,
            ),
            Decision(
                "Temporal split: three quarters, each trained on all earlier quarters",
                "The book's backtest trains on the periods before 60 and tests on period 60; a lender scores the loans "
                "it holds, so a test quarter's loans have their earlier quarters in train.",
                windows,
            ),
            Decision(
                "Macro values as published when the quarter starts",
                "The source's macro columns hold the quarter's own values (the house price index of its last month, "
                "the unemployment rate of its first month, its GDP growth), published during or after the quarter. "
                "The model sees the unemployment rate one quarter back and the GDP growth and house price index two "
                "quarters back.",
                macro,
            ),
        ]
