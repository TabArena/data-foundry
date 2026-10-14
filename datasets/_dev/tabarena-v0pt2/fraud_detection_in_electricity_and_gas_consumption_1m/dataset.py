"""Curated dataset definition for `fraud_detection_in_electricity_and_gas_consumption_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, Grouping, TaskSummary, drop_columns

CUT = "2013-01-01"
"""The prediction date: the features are the invoices before it, and the fraud labels look recorded from it on."""


def first_seen_by_quarter(raw: pd.DataFrame, events: pd.Series, *, nth: int = 1) -> pd.DataFrame:
    """Clients and fraud rate by the quarter in which a client's first event (rows where ``events``) appears; with
    ``nth`` > 1, the first invoice of the client's ``nth`` distinct meter among those rows.
    """
    rows = raw.loc[events, ["client_id", "invoice_date", "counter_number"]]
    if nth == 1:
        first = rows.groupby("client_id")["invoice_date"].min()
    else:
        starts = rows.groupby(["client_id", "counter_number"])["invoice_date"].min().reset_index()
        starts = starts.sort_values(["client_id", "invoice_date"], kind="stable")
        first = starts.groupby("client_id")["invoice_date"].nth(nth - 1)
        first = pd.Series(first.to_numpy(), index=starts.loc[first.index, "client_id"].to_numpy())
    fraud = raw.groupby("client_id")["target"].first()
    month = first.str[5:7].astype(int)
    quarter = first.str[:4] + "Q" + ((month - 1) // 3 + 1).astype(str)
    table = pd.DataFrame({"quarter": quarter.to_numpy(), "fraud": fraud.reindex(first.index).to_numpy()})
    out = table.groupby("quarter")["fraud"].agg(clients="size", fraud_rate="mean")
    out["fraud_rate"] = out["fraud_rate"].round(3)
    return out


class FraudDetectionInElectricityAndGasConsumption1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=("Will the Tunisian utility STEG find that this client commits electricity or gas meter fraud?"),
        use_case=(
            "On 2013-01-01, STEG scores each client from the client record and the invoices so far, to decide whom to"
            " inspect for meter fraud."
        ),
        row=(
            "One invoice (2005-2012) of a STEG client billed both before and after 2013, joined with the client's "
            "record; the prediction is one per client, the mean over its invoices."
        ),
        predicted=(
            "Whether STEG found the client fraudulent (7.8% of the clients billed before and after the cut); the "
            "finding falls in 2013-2019 without a date."
        ),
        known=(
            "The client's district, region, category and account creation date, and per invoice its date, tariff, "
            "meter number, status, code and type (electricity or gas), reading remarks, consumption by tier, meter "
            "readings and months covered."
        ),
        split=(
            "Whole clients are held out in three folds, so the test data stands for other clients over the same "
            "years, as in the challenge."
        ),
        changes=(
            "We cut the history at 2013-01-01, as later invoices carry traces of the inspections that set the labels,"
            " keep clients billed before and after that date, and sample 1.5M invoices by whole clients."
        ),
        fit="approximate",
        fit_reason=(
            "The finding has no date or stated horizon, and the cut date is read off the data rather than documented "
            "by STEG or Zindi."
        ),
    )

    # Dataset
    unique_name = "fraud_detection_in_electricity_and_gas_consumption_1m"
    version_of = "fraud_detection_in_electricity_and_gas_consumption"
    version_comment = """
        We sub-sample the frame (1,907,490 invoices of 83,874 clients, all before 2013) to 1.5M rows by whole clients
        (66,014, stratified on the target) and use grouped 3-fold cross-validation, so every fold trains on about 1M
        and tests on about 500k rows (v2 split protocol).
    """
    year = "2019"
    domain = "industry & manufacturing"
    source = "Zindi"
    source_url = "https://zindi.africa/competitions/fraud-detection-in-electricity-and-gas-consumption-challenge"
    license = "Zindi Competition Rules"
    data_tags = ("Spatial",)
    download_description = """
        The Zindi files need a Zindi login (train.zip holds client_train.csv and invoice_train.csv:
        https://zindi.africa/competitions/fraud-detection-in-electricity-and-gas-consumption-challenge/data). We use the
        Kaggle mirror uploaded on 2020-08-24, which holds the competition's train and test files and its sample
        submission. Its client_train.csv has the sha256 of the copy committed to GitHub on 2020-06-29
        (github.com/matzolla/STEG_fraud_detection_in_electricity_and_gaz_consumption), and its invoice_train.csv
        matches the profile printed by Zindi's starter notebook (4,476,749 x 16; 135,493 clients, 8,275 distinct
        invoice dates, 201,893 meter serials).

        uvx --from kaggle==2.2.2 kaggle datasets download mrmorj/fraud-detection-in-electricity-and-gas-consumption
        unzip fraud-detection-in-electricity-and-gas-consumption.zip client_train.csv invoice_train.csv
        rm fraud-detection-in-electricity-and-gas-consumption.zip
        mkdir -p local-data-warehouse/fraud_detection_in_electricity_and_gas_consumption
        mv client_train.csv invoice_train.csv local-data-warehouse/fraud_detection_in_electricity_and_gas_consumption/

        sha256 (2026-10-06): client_train.csv ba15926524d57058945ddccdd5bd2e1add0e00286c7940d7d8201900f2f126c3,
        invoice_train.csv 03d6b05c74962b04d40e5609644fc14166fc13270923272ac2c3de66399c7743.
    """
    bibtex = r"""
        @misc{zindi2019stegfraud,
          author       = {{Zindi} and {STEG}},
          title        = {Fraud Detection in Electricity and Gas Consumption Challenge},
          year         = {2019},
          howpublished = {\url{https://zindi.africa/competitions/fraud-detection-in-electricity-and-gas-consumption-challenge}},
          note         = {Zindi competition, first run as AI Hack Tunisia \#4 -- Predictive analytics challenge \#1 (20--22 September 2019); data from the Soci\'{e}t\'{e} Tunisienne de l'\'{E}lectricit\'{e} et du Gaz (STEG)}
        }
    """
    curation_comments = """
        We start with client_train.csv and invoice_train.csv of the Zindi challenge, from its Kaggle mirror.

        - Prediction point: on 2013-01-01, STEG scores each client from the client record and the invoices so far
          (2005 to 2012) to decide whom to inspect for meter fraud, one prediction per client as in the challenge. The
          label is STEG's per-client finding, which the data place in 2013-2019 without a date.
        - We join every invoice with its client's record on `client_id` (the source's key): one row per invoice. Only
          the train files carry labels.
        - History cut at 2013-01-01: the invoices from 2013 on carry traces of the inspections that set the labels, so
          the features are the invoices before 2013. The fraud rate of clients whose second electricity meter first
          appears in a quarter is 7.4-11.9% for each quarter of 2012 and 23.8-25.9% for each quarter of 2013, while
          the number of such events per quarter does not jump at 2013Q1 (decision table). A client-level LightGBM
          scores ROC AUC 0.848 with the full history; with the invoices before 2013 the models score 0.66-0.69. The
          cut date is read off the data; STEG and Zindi do not document it.
        - Cohort: the 83,874 clients billed both before and after the cut (6,504 frauds, 7.8%). We drop the 19,133
          clients whose last invoice is before 2013 (21 frauds, 0.11%), whose labels look unrecorded (decision table),
          and the 32,486 clients whose first invoice is from 2013 on, who have no history at the prediction point.
        - We drop the 9 exact duplicate invoices (double entries).
        - We drop `consommation_level_4`: the fourth consumption tier first appears in January 2014, so it is 0 on
          every invoice before the cut.
        - `counter_number` (the meter's serial number) is 0 on 12,555 invoices; we set it to missing. Serials repeat
          across clients, but clients that share a serial do not share labels (ROC AUC 0.51 for the other clients'
          label), so the column does not link clients across the split.
        - We rename `disrict` to `district` and `target` to `fraud` ("Yes" / "No").
        - The codes (`tarif_type`, `counter_statue`, `counter_code`, `reading_remarque`, `counter_type`, `district`,
          `client_catg`, `region`) are categorical; `invoice_date` and `creation_date` are dates. `client_id` is the
          group column, never a feature.
        - Grouped split by `client_id`; the prediction per client is the mean of its invoices' predictions (see the
          grouping definition). Zindi also scores ROC AUC on one probability per client, but with the full history.
        - Anomaly: 34 invoices (4 clients) carry `counter_statue` codes outside the documented 0-5 and 21 (3 clients)
          carry `reading_remarque` codes outside 6-9, mostly rows whose fields are shifted by one column.
          `months_number` is above 24 on 806 invoices (up to 412,509). We keep them as the source has them.
        - Anomaly: 29,121 train invoices are dated after the challenge first ran (20-22 September 2019), up to
          2019-12-07, so the dates may be shifted. The cut uses the data's dates.
        - Note: Zindi's rules forbid redistribution; the Kaggle mirror states "other".
    """

    # Task
    target = "fraud"
    problem_type = "binary_classification"
    grouping = Grouping(
        on="client_id",
        labels="per_group",
        prediction_unit="group",
        aggregation="mean",
        context="all_rows",
        definition="""
            One group is a client of STEG, the Tunisian electricity and gas utility; its rows are the client's invoices
            from 2005 to 2012 (1 to 234, median 21) with the client's record joined. The challenge asks, "Using the
            client's billing history, ... to detect and recognize clients involved in fraudulent activities", and
            scores one probability per client with ROC AUC on clients that are not in the training file (Zindi's test
            file holds 58,069 other clients over the same years). So one prediction per client, made on 2013-01-01
            from all of its invoices before that date. The group prediction is the mean of the invoices' predictions:
            the label belongs to the client, and every invoice is one observation of it. On the shipped folds,
            LightGBM fit on the training invoices scores per client ROC AUC 0.685 with the mean, 0.684 with the
            largest prediction and 0.682-0.684 with the latest date's (its ties broken by the largest or the mean),
            and the largest follows the number of invoices more (Spearman 0.31 against 0.24 for the mean, non-fraud
            clients). `last` would need a rule for ties: 50% of the clients have several invoices (electricity and
            gas) on their latest date.
        """,
    )

    # Splits
    subsample_to_budget = True
    accepted_check_warnings = {
        "splits_rows_never_tested": "The v2 protocol caps each test fold at 500k rows; the grouped folds of the 1.5M-row "
        "frame overshoot by whole clients, so 860 rows (0.06%, 31 clients) are trimmed from a test fold (2026-10-07).",
    }

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        text = {"client_id": str, "creation_date": str}
        clients = pd.read_csv(raw_dir / "client_train.csv", dtype=text)
        invoices = pd.read_csv(
            raw_dir / "invoice_train.csv",
            dtype={"client_id": str, "invoice_date": str, "counter_statue": str, "counter_type": str},
        )
        # one row per invoice with its client's record (the source's key)
        return invoices.merge(clients, on="client_id", how="left", validate="many_to_one")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.rename(columns={"disrict": "district", "target": "fraud"})
        # Cohort: clients billed both before and after the cut (ISO dates sort as text)
        first_invoice = df.groupby("client_id")["invoice_date"].transform("min")
        last_invoice = df.groupby("client_id")["invoice_date"].transform("max")
        df = df[(first_invoice < CUT) & (last_invoice >= CUT)]
        # Features: the invoices before the cut (later ones carry traces of the inspections)
        df = df[df["invoice_date"] < CUT]
        # Exact duplicate invoices (double entries)
        df = df.drop_duplicates()
        # The fourth consumption tier first appears in January 2014: 0 on every invoice before the cut
        df = drop_columns(df, ["consommation_level_4"])
        # A meter serial of 0 is no serial
        df["counter_number"] = df["counter_number"].mask(df["counter_number"] == 0)
        df["fraud"] = df["fraud"].map({1.0: "Yes", 0.0: "No"})
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "client_id",
                "tarif_type",
                "counter_statue",
                "counter_code",
                "reading_remarque",
                "counter_type",
                "district",
                "client_catg",
                "region",
            ],
            datetime={"invoice_date": "%Y-%m-%d", "creation_date": "%d/%m/%Y"},
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        del df
        first_invoice = raw.groupby("client_id")["invoice_date"].transform("min")
        last_invoice = raw.groupby("client_id")["invoice_date"].transform("max")

        billed = raw[last_invoice >= CUT]  # the clients billed from 2013, with their whole history
        elec = (billed["counter_type"] == "ELEC") & (billed["counter_number"] != 0)
        meters = first_seen_by_quarter(billed, elec, nth=2).add_prefix("second ELEC meter: ")
        status = first_seen_by_quarter(billed, billed["counter_statue"] == "5").add_prefix("counter status 5: ")
        footprints = meters.join(status, how="outer").loc["2011Q1":"2014Q4"]
        footprints.index.name = "quarter first seen"

        last_year = raw.groupby("client_id")["invoice_date"].max().str[:4]
        fraud = raw.groupby("client_id")["target"].first()
        by_last = pd.DataFrame({"last invoice year": last_year, "fraud": fraud.reindex(last_year.index)})
        by_last = by_last.groupby("last invoice year")["fraud"].agg(clients="size", frauds="sum", fraud_rate="mean")
        by_last["frauds"] = by_last["frauds"].astype(int)
        by_last["fraud_rate"] = by_last["fraud_rate"].round(4)

        cohort = raw[(first_invoice < CUT) & (last_invoice >= CUT) & (raw["invoice_date"] < CUT)]
        latest = cohort.groupby("client_id")["invoice_date"].transform("max") == cohort["invoice_date"]
        tied = cohort.loc[latest].groupby("client_id").size()
        ties = (
            f"{int((tied > 1).sum()):,} of {len(tied):,} clients ({(tied > 1).mean():.1%}) have several invoices on "
            "their latest date before the cut."
        )
        return [
            Decision(
                "The history is cut at 2013-01-01",
                "Second electricity meters and counter status 5 that first appear from 2013Q1 on go with fraud rates of "
                "21-36% per quarter, against 4-12% for the same events up to 2012Q4: traces of the inspections that "
                "set the labels. The features are the invoices before 2013.",
                footprints,
            ),
            Decision(
                "Only clients billed both before and after the cut",
                "Almost no client whose last invoice is before 2013 is a fraud, so their labels look unrecorded; a "
                "client whose first invoice is from 2013 on has no history at the prediction date.",
                by_last,
            ),
            Decision(
                "One prediction per client: the mean of its invoice predictions",
                "The challenge scores one probability per client; the mean, the largest and the latest date's "
                "predictions score the same per client, and the latest date often holds two invoices.",
                ties,
            ),
        ]
