"""Curated dataset definition for `american_companies_bankruptcy` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    Source,
    TaskSummary,
    Temporal,
    TemporalSplits,
    decode,
    drop_columns,
)

# The 18 items in the column order of the current CSV (commit 279e4275, April 2024), which is the header order of the
# source's split files (`dataset_paper.zip`). The July 2022 CSV holds the same values in the order of the paper's
# Table 2; `ITEMS_2022` maps each name to its column there.
ITEMS = {
    "X1": "current_assets",
    "X2": "total_assets",
    "X3": "cost_of_goods_sold",
    "X4": "total_long_term_debt",
    "X5": "depreciation_and_amortization",
    "X6": "ebit",
    "X7": "ebitda",
    "X8": "gross_profit",
    "X9": "inventory",
    "X10": "total_current_liabilities",
    "X11": "net_income",
    "X12": "retained_earnings",
    "X13": "total_receivables",
    "X14": "total_revenue",
    "X15": "market_value",
    "X16": "total_liabilities",
    "X17": "net_sales",
    "X18": "total_operating_expenses",
}
ITEMS_2022 = {  # the paper's Table 2, which names the July 2022 CSV's columns
    "current_assets": "X1",
    "cost_of_goods_sold": "X2",
    "depreciation_and_amortization": "X3",
    "ebitda": "X4",
    "inventory": "X5",
    "net_income": "X6",
    "total_receivables": "X7",
    "market_value": "X8",
    "net_sales": "X9",
    "total_assets": "X10",
    "total_long_term_debt": "X11",
    "ebit": "X12",
    "gross_profit": "X13",
    "total_current_liabilities": "X14",
    "retained_earnings": "X15",
    "total_revenue": "X16",
    "total_liabilities": "X17",
    "total_operating_expenses": "X18",
}

# The SIC divisions (SIC Manual 1987), the letters of `Division`.
SIC_DIVISIONS = {
    "A": "Agriculture, Forestry and Fishing",
    "B": "Mining",
    "C": "Construction",
    "D": "Manufacturing",
    "E": "Transportation, Communications, Electric, Gas and Sanitary Services",
    "F": "Wholesale Trade",
    "G": "Retail Trade",
    "H": "Finance, Insurance and Real Estate",
    "I": "Services",
    "J": "Public Administration",
}


def repair_decimal_points(tokens: pd.Series) -> pd.Series:
    """A token without a decimal point is the value with its point lost: three decimals, so divide by 1,000."""
    values = tokens.astype(float)
    return values.where(tokens.str.contains(".", regex=False), values / 1000)


class AmericanCompaniesBankruptcy(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "Will a US listed company file for Chapter 7 or Chapter 11 bankruptcy in the year after this annual "
            "statement?"
        ),
        use_case=(
            "A lender or investor assesses a listed company's credit risk from its latest annual statement, to "
            "decide whether to lend to it, hold it or price its debt, before a filing in the next year."
        ),
        row=(
            "One fiscal year of one company listed on the NYSE or NASDAQ, 1999 to 2018 (78,682 firm-years of 8,971 "
            "anonymised companies)."
        ),
        predicted=(
            "Whether the company files for bankruptcy in the year after the statement: the last fiscal year of a "
            "company that failed is Yes (609, 0.77%), every other year No."
        ),
        known=(
            "The statement's 17 items (assets, liabilities, debt, revenue, costs, earnings, retained earnings, "
            "market capitalisation), its fiscal year and the company's industry (SIC division and major group)."
        ),
        known_at_scoring="",
        split=(
            "Nine later fiscal years from 2008 to 2018 (not 2009 and 2017), each tested on its own and trained on "
            "every earlier year, whose labels are all known by then; most test companies have earlier years in "
            "training."
        ),
        changes=(
            "We restored the decimal points the current release lost, named the columns by the source's split "
            "files, dropped net sales (a copy of revenue), and moved the bankruptcy label from every year of a "
            "failed company to its last year, as the source defines it."
        ),
        fit="approximate",
        fit_reason=(
            "The source names credit risk assessment one year ahead, and the rows are the statements a lender "
            "reads. Approximate: no filing dates ship, so the one-year horizon cannot be verified, and a company "
            "that leaves in distress stays No; the inputs are accounting items only, of a firm set fixed by "
            "earlier papers."
        ),
    )

    # Dataset
    unique_name = "american_companies_bankruptcy"
    domain = "finance"
    sources = (
        Source(
            role="publication",
            platform="GitHub",
            url="https://github.com/sowide/bankruptcy_dataset",
            license="CC BY 4.0",
            year="2022",
            bibtex="""
                @article{lombardo2022machine,
                  title={Machine Learning for Bankruptcy Prediction in the American Stock Market: Dataset and Benchmarks},
                  author={Lombardo, Gianfranco and Pellegrino, Mattia and Adosoglou, George and Cagnoni, Stefano and Pardalos, Panos M. and Poggi, Agostino},
                  journal={Future Internet},
                  volume={14},
                  number={8},
                  pages={244},
                  year={2022},
                  publisher={MDPI},
                  doi={10.3390/fi14080244}
                }
            """,
            files=("american_bankruptcy_dataset.csv", "american_bankruptcy_dataset_2022.csv"),
        ),
    )
    data_tags = ()
    download_description = """
        mkdir -p local-data-warehouse/american_companies_bankruptcy && cd local-data-warehouse/american_companies_bankruptcy
        # the current release (commit 279e4275, 2024-04-10): decimal points lost, columns reordered, SIC columns added
        wget -O american_bankruptcy_dataset.csv https://raw.githubusercontent.com/sowide/bankruptcy_dataset/279e4275101e5df7a39e8e6b3179b66c442557f3/american_bankruptcy_dataset.csv
        # the first release (commit 7f56a80b, 2022-07-26): the same values with their decimal points, no SIC columns
        wget -O american_bankruptcy_dataset_2022.csv https://raw.githubusercontent.com/sowide/bankruptcy_dataset/7f56a80b73c2f32582fcc01d28acb6adc665ae40/american_bankruptcy_dataset.csv
    """
    curation_comments = """
        We start with `american_bankruptcy_dataset.csv` of GitHub sowide/bankruptcy_dataset at commit 279e4275 (April 2024), the data of Lombardo et al., Future Internet 14(8):244, 2022, and check its values against the same file at commit 7f56a80b (July 2022, published with the paper).

        - Files: the definition reads the current CSV (the values, and the SIC columns `Division` and `MajorGroup`, which only it has) and the July 2022 CSV (only to check the repair below). Left out: `dataset_paper.zip`, the split files of the later multimodal paper (Lombardo et al., IEEE Access 2024: one row per company with three years of items and the text of 10-K Items 1, 5 and 7; train 2001-2014, validation 2015, test 2016-2018), another task on a subset of these firm-years; it served to check the repair, the column names and the label (measured 2026-11-25, below). `README.md` and `LICENSE.md` hold no data.
        - Decimal points (`Data Quality Issue`, PROV-13): in the current CSV 914,068 of the 1,416,276 item cells (64%) lost their decimal point (C_1's total assets read 740998 in 1999 and 701.854 in 2000). Every item token without a point is divided by 1,000 (`repair_decimal_points`, on the file read as text). `_clean` asserts that the repaired values equal the July 2022 CSV in every cell, row for row, so the repair restores the published values exactly; before it, 29% to 87% of each column's cells matched. The split files agree: 6,170 of their 6,170 firm-years are found after the repair, 972 before (measured 2026-11-25).
        - Column names: the current CSV reorders the columns, so the paper's Table 2 and the Kaggle copy's names (X1 current assets, X2 cost of goods sold, X3 depreciation and amortization, X4 EBITDA, ...) are wrong for it: under them EBIT plus D&A equals EBITDA in 0.01% of rows. Table 2 names the July 2022 CSV correctly (`ITEMS_2022`), and the split files' header order names the current one (`ITEMS`); the two agree column for column. After the repair EBIT + D&A = EBITDA, cost of goods sold + gross profit = revenue, current assets <= total assets and current liabilities <= total liabilities hold in all but 3, 2, 1 and 2 rows (99.996% or more; measured 2026-11-25). `ebitda` (EBIT + D&A), `gross_profit` (revenue - cost of goods sold) and `total_operating_expenses` (revenue - EBITDA, off in 4 rows) are derived columns, kept: unlike `net_sales` they are not copies. The source states no currency unit.
        - Dropped: `net_sales` (X17), equal to `total_revenue` (X14) in every row of both releases.
        - Label (USE-5): both releases mark all 5,220 rows of the 609 failed companies `failed`, while the paper (Section 3) labels "the fiscal year before the chapter filing as 'bankruptcy' (1) for the next year. Otherwise, the company is considered healthy (0)". The target is Yes on a failed company's last fiscal year only: 609 events (0.77%). Per fiscal year they equal the paper's Table 1 counts of bankrupt firms one year later (58 in fiscal 2008 against 58 in Table 1's 2009; 36 in fiscal 2018 against 36 in 2019). The split files agree: 496 of their 502 failed rows found in the main file are a failed company's last year, none an earlier year (measured 2026-11-25). With the label as published, every year of a failed company, grouped ROC AUC falls to about 0.70 (LightGBM, measured 2026-11-25).
        - Note: the label means "bankruptcy while listed". A company that leaves the panel for any other reason (acquired, delisted, gone private; 5,675 of the 8,362 never-failed companies end before 2018) stays No, also when it left in distress and filed later. Such exits look like distress: among the No rows of the test periods 2015-2018, 2012-2014 and 2009-2011, the last year of an early exit ranks above the other No rows (ROC AUC 0.60, 0.64 and 0.58, untuned LightGBM) and makes up 11%, 19% and 13% of the top 1% of scores against about 7% of all rows (measured 2026-11-25). This is label noise every model meets alike, not a leak.
        - Note: the data has no filing dates, so a failed company whose last statement came more than a year before its filing is labelled on that last statement all the same, and for a filing soon after a fiscal year end the last statement may have been published after the filing. Neither can be checked here. A statement published after a filing would move liabilities subject to compromise out of current and long-term debt; the share of liabilities in neither stays flat on the Yes rows (median 0.060, against 0.066 the year before and 0.052 for companies that left for other reasons; measured 2026-11-25), so no sign of it shows.
        - Dropped: `company_name`, an anonymised id (`C_1` to `C_8971`) numbered roughly by first year (Spearman 0.49 with it, per company): an identifier, not a feature; `status_label`, the source of the target.
        - `fyear` is the fiscal year: the time column and a feature (the actor knows the year of the statement it scores). `Division` is decoded from the SIC letter into the division's name (SIC Manual 1987, `SIC_DIVISIONS`); every major group lies in its division's range. `MajorGroup`, the two-digit SIC major group (73 codes), is categorical: a code, not a quantity. Both SIC columns arrived with the 2024 release and are constant within each of the 8,971 companies: one lookup per company at extraction, not the industry of each year (LEAK-10). No mechanism ties a change of industry to bankruptcy, so they stay, with this note, as registry attributes stayed in tunisian_fraud_detection_challenge.
        - Anomaly: a few items are negative where an amount cannot be (current assets in 6 rows, cost of goods sold in 6, total revenue in 13); kept as recorded, since the source documents no correction.
        - Selection: the firm set is the one of the authors' earlier 10-K papers ("we consider the same companies used in [6,37] since this set of firms has been proved to be a fair approximation of the American stock market for each year", Section 3), and the paper says the bankruptcy rate "can be underestimated due to the exclusion of some companies in the past because of their small market capitalization". The panel shrinks from 5,308 firms in 1999 to 2,723 in 2018, and few new listings enter late (87 in 2017, 47 in 2018). Fiscal years 1999 to 2002, the dot-com bust, when bankruptcies of US listed companies peaked, hold only 3, 7, 10 and 17 events; they sit on training sides only. The README and the paper count 8,262 companies, the CSV 8,971 ids; the difference is not explained. The record carries `Selection Bias` for this (as polish_companies_bankruptcy).
        - Class-dependent recording checked and absent (LEAK-39): label-free recording markers (cells without a point, `.0` endings, zeros, whole numbers) reach grouped ROC AUC 0.538 alone and add nothing to the 17 items (0.858 against 0.857; measured 2026-11-25). Both classes come from one file of one extraction.
        - No duplicate company-years and no duplicate rows. 710 companies miss a year between their first and last.
        - Metric: ROC AUC, the paper's selection criterion (Section 8: "we compared all the models in terms of the AUC, and we identified the best model for both tasks using this metric. This metric was chosen for two reasons: first, due to the imbalance test set, but also because it is most commonly used in literature for this task"). The paper also questions it: a regulatory body "should not blindly trust the AUC value ... they should design and compare the ML models using the macro-F1 score and then the AUC" (Section 8.1), and "computing precision, recall for the single classes, and the macro-F1 score would better define the models' performance" (Section 9). It fixes no threshold, so a hard-label metric cannot be declared and ROC AUC stays (MET-5, MET-6). The paper scored about one sample per company of its test period (Table 4: 105 positives of 3,345 samples, 3.1%), we score every firm-year (2,723 to 3,857 a window, 0.6% to 1.5% positive), since the lender re-scores each statement: the paper's AUCs (best test 0.861) are not comparable with scores on this task.
        - Potential leak, kept on purpose (LEAK-9, an evaluation leak): a Yes row is a failed company's last row, so every row whose company has a row in the next fiscal year is No, and the shipped file holds the next year of every test year but 2018. With the true company ids, "no row in the next year" alone scores ROC AUC 0.94 to 0.97 in each of the windows 2008 to 2017; without ids, linking a row to its successor from the features (nearest neighbour within the major group) lifted mean ROC AUC from 0.867 to 0.938 on three-year test windows (+0.035 to +0.115 per window; measured 2026-11-25). One-year windows keep a test row's successor out of its own test window, not out of the file. Each test row is predicted from the training rows and its own features only; no feature or model step may use other rows of the file, and a method that reads another row of the same company is called out and not benchmarked (as for loan_default_prediction_imperial_college and spanish_motor_insurance_coverage_level_2022_2024).
    """

    # Task
    target = "bankruptcy_next_year"
    problem_type = "binary_classification"
    metric = Metric.source(
        "roc_auc",
        original="AUC (area under the ROC curve), the paper's model selection criterion (Sections 6 to 8)",
        reference="https://doi.org/10.3390/fi14080244",
    )

    # Splits
    splits_comment = """
        Nine one-year test windows, newest first: the fiscal years 2018, 2016, 2015, 2014, 2013, 2012, 2011, 2010 and 2008, each trained on every earlier fiscal year, with no gap. They hold 2,723 (2018), 3,191, 3,354, 3,504, 3,484, 3,485, 3,513, 3,625 and 3,857 (2008) firm-years with 36, 29, 33, 33, 28, 26, 25, 35 and 58 bankruptcies; the training sides hold 96.5% down to 52.3% of the 78,682 rows. The count is the 9 splits an IID split of 78,682 rows would get (SPLIT-33). Eleven years are eligible (2008 to 2018; 2007 would train on 47.3%, under the half-the-rows floor). The curator kept the first and the last eligible year, 2008 (the recession filings) and 2018, and two of the nine years between them leave: the two with the fewest bankruptcies, 2017 (21) and 2009 (23), whose scores are the noisiest; a rule on event counts, not on any model's score (SPLIT-15). They stay in the training sides of the later windows.

        Window length: one fiscal year. The source predicts one year ahead (Section 3: "predict bankruptcy at least one year before it happens") and names no refit cadence; statements are annual, so a lender refits once a year (our assumption, for the curator's sign-off), as in the other yearly panels (spanish_homeowners_motor_insurance_2010_2014, wisconsin_local_government_property_insurance_fund). Few events in a window (21 to 58) are part of the task, not a reason for wider windows (TP-9): SPLIT-14 counts the scored rows, and each window holds over 2,700. The source's own split (Sections 3 and 6: "We used data from 1999 until 2011 for training, data from 2012 until 2014 for validation and model comparison, and the remaining years from 2015 to 2018 as a test-set") is one temporal cut, not a refit cadence.

        No gap (SPLIT-10): the outcome horizon is fixed (a filing in the year after the statement) and every label is final at release, so the newest training year's labels are known before the statements of the test year are filed, and no training label is selected by its outcome. SPLIT-9's shortcut through a company's own label cannot arise: a training Yes is a company's last year, so that company has no test row. Measured at equal training size (untuned LightGBM, 3 seeds, the no-gap training side subsampled to the gapped size), the newest training year adds +0.007 ROC AUC on average over 2009-2018 (0.912 against 0.905; per window -0.013 to +0.044), no sign of a shortcut. The one residue: fiscal years that do not end in December, whose next-year filings may run past the next statements; the data carry no month, so it cannot be measured. Dropping the gap makes fiscal 2008, the recession filings of 2009 (58 events, 1.5%), an ordinary window at 52.3%.

        Companies recur: 92% to 98% of each test year's firm-years, and 301 of the windows' 303 bankruptcies, are of companies with earlier years on the training side. The use case scores listed companies a lender has seen before as well as new ones, and no company id is a feature; seen and new companies scored alike on the earlier test period 2015-2018 (ROC AUC 0.910 against 0.908).

        Protocol (LEAK-9): a test row's next fiscal year of the same company is in the file for every test year but 2018, and having one means No (ROC AUC 0.94 to 0.97 with the true ids; recovered in part from the features alone). Each test row is predicted from the training rows and its own features only; no feature or model step may use other rows of the file, and a method that reads another row of the same company is called out and not benchmarked.
    """
    split_leaf = "L-ORDER.windows"
    temporal = Temporal(
        on="fyear",
        splits=TemporalSplits(window=1, unit="unique", cutoffs=(2008, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2018)),
        horizon=1,
        horizon_unit="years",
        time_unit="years",
    )
    accepted_check_warnings = {
        "dataset_pure_feature_value": (
            "Early fiscal years (1999-2002, 99.6-99.9% No) and large sectors (Services and SIC major groups 73, 38, "
            "49, 80 and 50, about 99.5% No) against a base rate of 99.2%: year and sector base-rate effects, not "
            "leaks (review panel, 2026-11-25)."
        ),
    }

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        return {
            "current": pd.read_csv(raw_dir / "american_bankruptcy_dataset.csv", dtype=str),
            "first": pd.read_csv(raw_dir / "american_bankruptcy_dataset_2022.csv", dtype=str),
        }

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        df = raw["current"].copy()
        # 1. Restore the decimal points (curation notes) and name the items by the split files' header order.
        for column, name in ITEMS.items():
            df[name] = repair_decimal_points(df[column])
        df = df.drop(columns=list(ITEMS))
        # 2. The repaired values equal the July 2022 release, row for row and cell for cell.
        first = raw["first"]
        assert (first["company_name"].to_numpy() == df["company_name"].to_numpy()).all()
        assert (first["year"].astype(float).to_numpy() == df["fyear"].astype(float).to_numpy()).all()
        for name, column in ITEMS_2022.items():
            assert np.allclose(df[name], first[column].astype(float), rtol=1e-9, atol=1e-9), name
        # 3. The label: the last fiscal year of a failed company (curation notes).
        df["fyear"] = df["fyear"].astype(float).astype(int)
        last_year = df.groupby("company_name")["fyear"].transform("max")
        df[self.target] = ((df["status_label"] == "failed") & (df["fyear"] == last_year)).astype(int)
        df = decode(df, {self.target: {0: "No", 1: "Yes"}})
        # 4. The SIC division letter to its name; the major group stays a code.
        df = decode(df, {"Division": SIC_DIVISIONS})
        # 5. Drop the id, the published label and the copy of revenue.
        return drop_columns(df, ["company_name", "status_label", "net_sales"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["Division", "MajorGroup"])

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        current, first = raw["current"], raw["first"]
        cells = pd.DataFrame(
            {
                "column": list(ITEMS.values()),
                "cells without a point": [int((~current[c].str.contains(".", regex=False)).sum()) for c in ITEMS],
                "share equal to the 2022 release before the repair": [
                    round(float(np.isclose(current[c].astype(float), first[ITEMS_2022[n]].astype(float)).mean()), 3)
                    for c, n in ITEMS.items()
                ],
            }
        )
        year = current["fyear"].astype(float).astype(int).rename("fiscal year")
        marked = (current["status_label"] == "failed").groupby(year).sum().rename("rows marked failed")
        events = df[self.target].eq("Yes").groupby(df["fyear"].rename("fiscal year")).sum().rename("target Yes")
        label = pd.concat([marked, events], axis=1)
        return [
            Decision(
                "Decimal points restored",
                "Item tokens without a decimal point are divided by 1,000; after that every cell equals the July "
                "2022 release (asserted in `_clean`).",
                cells,
            ),
            Decision(
                "Label on the last fiscal year of a failed company",
                "The CSV marks every year of a failed company; the source labels the year before the filing. The "
                "target per fiscal year equals the paper's Table 1 one year later.",
                label,
            ),
        ]
