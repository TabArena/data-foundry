"""Curated dataset definition for `taiwanese_bankruptcy_prediction` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, Source, TaskSummary


class TaiwaneseBankruptcyPrediction(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a listed Taiwanese company go bankrupt?",
        use_case=(
            "For example, a lender or investor screens companies on their published financial ratios and decides "
            "whether to extend credit or invest."
        ),
        row=(
            "One company-year, as the file's structure suggests (the source does not say), of the Taiwan Economic "
            "Journal's data for 1999-2009 (6,819 rows)."
        ),
        predicted=(
            "Whether the company went bankrupt under the Taiwan Stock Exchange's rules (3.2%); the time between the "
            "ratios and the bankruptcy is not stated."
        ),
        known=(
            "The company's financial ratios: profitability, margins, growth, per-share figures, liquidity, debt, "
            "turnover and cash flow."
        ),
        split="Random companies of the whole period, as the years are not given.",
        fit="approximate",
        fit_reason=(
            "The ratios are what a lender sees, but the source states neither the year of each row nor the gap "
            "between the statements and the bankruptcy, so the random split stands in for scoring companies before "
            "they fail. The rows repeat by company over the years and the bankrupt label recurs one block (likely a "
            "year) apart, so a company's other years sit on both sides of the random split."
        ),
    )

    # Dataset
    unique_name = "taiwanese_bankruptcy_prediction"
    domain = "finance"
    sources = (
        Source(
            role="publication",
            platform="UCI",
            url="https://doi.org/10.24432/C5004D",
            license="CC BY 4.0",
            year="2020",
            bibtex="""
                @article{liang2016financial,
                  title={Financial ratios and corporate governance indicators in bankruptcy prediction: A comprehensive study},
                  author={Liang, Deron and Lu, Chia-Chi and Tsai, Chih-Fong and Shih, Guan-An},
                  journal={European journal of operational research},
                  volume={252},
                  number={2},
                  pages={561--572},
                  year={2016},
                  publisher={Elsevier}
                }
            """,
        ),
    )
    data_tags = ("ForcedIIDFromTemporal",)
    download_description = """
        We download the data from the UCI repository and uzip it to a predefined folder.

        mkdir -p local-data-warehouse/taiwanese_bankruptcy_prediction/ && wget -P local-data-warehouse/taiwanese_bankruptcy_prediction/ https://archive.ics.uci.edu/static/public/572/taiwanese+bankruptcy+prediction.zip && unzip local-data-warehouse/taiwanese_bankruptcy_prediction/taiwanese+bankruptcy+prediction.zip -d local-data-warehouse/taiwanese_bankruptcy_prediction/ && rm local-data-warehouse/taiwanese_bankruptcy_prediction/taiwanese+bankruptcy+prediction.zip
    """
    curation_comments = """
        - We map binary Bankrupt column to yes/no
        - We rename the features to be shorter and have no special characters.
        - We drop the constant column "Net_Income_Flag".
        - We drop two duplicated features (same values as other features).
        - Anomaly: the paper introducing the dataset has more features, but these do not seem to be in the dataset.
        - Potential leak, kept on purpose: 67 of the 91 non-binary numeric columns have a minimum of exactly 0 and a maximum of exactly 1 over the 6,819 companies, a min-max scaling over all rows that UCI does not document; the Taiwan Economic Journal's raw data are commercial. Kept (Lennart, 2026-10-19): a scaling over all rows is no strong leak, and data often come this way; revisit if unscaled data appear.
        - Anomaly: the data is temporal but all features are time-invariant. This might still have a latent, non-verifiable temporal component, which we ignore for our predictive IID task.
        - Source gap (2026-11-11, Andrej; PROV-2, USE-8): Liang et al. (2016, Sec. 3.1) describe 239 bankrupt and 239
          matched companies of similar size and industry, each with at least three years of complete public data
          before the crisis and with 95 financial ratios and 95 corporate governance indicators. The UCI release
          differs (6,819 rows, 220 bankrupt, 3.2%; the ratios only), and how it was drawn is not documented. Neither
          UCI nor the paper states how long before the bankruptcy the ratios were taken, so the prediction point is
          unknown: if the ratios came from the year of the failure, the task recognises failing companies rather than
          forecasting them. Recording check on the v0.2 frame (untuned LightGBM, 9 splits): debt ratio plus net worth
          over assets equals 1 in every row of both classes; unscaled values above 1 in a 0-1 column occur in 82% of
          the surviving and 91% of the bankrupt rows (mostly turnover ratios) and alone reach ROC AUC 0.64; coarser
          precision reaches 0.51. So both classes follow one recording convention (unlike
          polish_companies_bankruptcy, where such markers reach 0.955-0.964).
        - Company-years (2026-11-11, Andrej; SPLIT-8): the raw file is not shuffled and repeats its rows at a regular
          period of 26 to about 200 rows: one period after a row, its closest match lies below the 1st percentile of
          random-pair distances for 34% of rows against 13-17% at other offsets. The bankrupt label recurs at that
          period: 69% of the 220 bankrupt rows have another bankrupt row within three rows one period later, against
          21-25% at other offsets (about 20% by chance). So the rows look like company-years ordered by industry and
          year, but no company id or year exists to rebuild them. Under random folds a test row whose rebuilt chain
          has a bankrupt row in training is bankrupt in 10.5% of cases against 1.0% otherwise. ROC AUC, 5 folds x 3
          repeats on the UCI file: random split LightGBM 0.941, kNN (k = 25) 0.884; grouped by rebuilt chains 0.939
          and 0.881; grouped by 10 contiguous file segments 0.934 (sd 0.031) and 0.877. The chains miss most bankrupt
          runs, so the grouped scores bound the leak loosely. Kept with the random split and this note.
        - Time basis: ForcedIIDFromTemporal: listed Taiwanese companies of 1999-2009, used to screen later statements;
          no row carries its year or company. The raw file repeats its rows at a regular period (26 to about 200
          rows; one period after a row its closest match lies below the 1st percentile of random-pair distances for
          34% of rows, 13-17% at other offsets), so the rows look like company-years ordered by industry and year,
          but no block can be dated (Time: Lost). Leak test across the split: a company's other years sit on the
          other side, and 69% of bankrupt rows have a bankrupt row one period later (21-25% at other offsets);
          grouping on rebuilt chains or on file segments moves ROC AUC from 0.941 to 0.939 and 0.934 (LightGBM).
          Years and company ids would allow a split by time. Not tested: later years and companies not seen in
          training.
    """

    # Task
    target = "Bankrupt"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason="Liang et al. 2016 report average accuracy and Type I / II errors on a 1:1 sample (the release is 3.2% bankrupt, MET-2), and a cost with ratios 1 to 5: no single matrix (MET-7). roc_auc is the binary fallback (also reported).",
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/data.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df.columns = [
            "Bankrupt",
            "ROA_C_Before_Interest_Depreciation",
            "ROA_A_Before_Interest_After_Tax",
            "ROA_B_Before_Interest_Depreciation_After_Tax",
            "Operating_Gross_Margin",
            "Realized_Sales_Gross_Margin",
            "Operating_Profit_Rate",
            "PreTax_Net_Interest_Rate",
            "AfterTax_Net_Interest_Rate",
            "NonIndustry_Income_Expenditure_Revenue",
            "Continuous_Interest_Rate_After_Tax",
            "Operating_Expense_Rate",
            "R&D_Expense_Rate",
            "Cash_Flow_Rate",
            "InterestBearing_Debt_Interest_Rate",
            "Tax_Rate_A",
            "Net_Value_Per_Share_B",
            "Net_Value_Per_Share_A",
            "Net_Value_Per_Share_C",
            "Persistent_EPS_Last_4_Seasons",
            "Cash_Flow_Per_Share",
            "Revenue_Per_Share",
            "Operating_Profit_Per_Share",
            "Net_Profit_Before_Tax_Per_Share",
            "Realized_Sales_Gross_Profit_Growth_Rate",
            "Operating_Profit_Growth_Rate",
            "AfterTax_Net_Profit_Growth_Rate",
            "Regular_Net_Profit_Growth_Rate",
            "Continuous_Net_Profit_Growth_Rate",
            "Total_Asset_Growth_Rate",
            "Net_Value_Growth_Rate",
            "Total_Asset_Return_Growth_Rate",
            "Cash_Reinvestment_Percent",
            "Current_Ratio",
            "Quick_Ratio",
            "Interest_Expense_Ratio",
            "Total_Debt_to_Net_Worth",
            "Debt_Ratio_Percent",
            "Net_Worth_to_Assets",
            "LongTerm_Fund_Suitability_Ratio_A",
            "Borrowing_Dependency",
            "Contingent_Liabilities_to_Net_Worth",
            "Operating_Profit_to_PaidIn_Capital",
            "Net_Profit_Before_Tax_to_PaidIn_Capital",
            "Inventory_Accounts_Receivable_to_Net_Value",
            "Total_Asset_Turnover",
            "Accounts_Receivable_Turnover",
            "Average_Collection_Days",
            "Inventory_Turnover_Rate",
            "Fixed_Assets_Turnover_Frequency",
            "Net_Worth_Turnover_Rate",
            "Revenue_Per_Person",
            "Operating_Profit_Per_Person",
            "Allocation_Rate_Per_Person",
            "Working_Capital_to_Total_Assets",
            "Quick_Assets_to_Total_Assets",
            "Current_Assets_to_Total_Assets",
            "Cash_to_Total_Assets",
            "Quick_Assets_to_Current_Liability",
            "Cash_to_Current_Liability",
            "Current_Liability_to_Assets",
            "Operating_Funds_to_Liability",
            "Inventory_to_Working_Capital",
            "Inventory_to_Current_Liability",
            "Current_Liabilities_to_Liability",
            "Working_Capital_to_Equity",
            "Current_Liabilities_to_Equity",
            "LongTerm_Liability_to_Current_Assets",
            "Retained_Earnings_to_Total_Assets",
            "Total_Income_to_Total_Expense",
            "Total_Expense_to_Assets",
            "Current_Asset_Turnover_Rate",
            "Quick_Asset_Turnover_Rate",
            "Working_Capital_Turnover_Rate",
            "Cash_Turnover_Rate",
            "Cash_Flow_to_Sales",
            "Fixed_Assets_to_Assets",
            "Current_Liability_to_Liability",
            "Current_Liability_to_Equity",
            "Equity_to_LongTerm_Liability",
            "Cash_Flow_to_Total_Assets",
            "Cash_Flow_to_Liability",
            "CFO_to_Assets",
            "Cash_Flow_to_Equity",
            "Current_Liability_to_Current_Assets",
            "Liability_Assets_Flag",
            "Net_Income_to_Total_Assets",
            "Total_Assets_to_GNP_Price",
            "NoCredit_Interval",
            "Gross_Profit_to_Sales",
            "Net_Income_to_Stockholders_Equity",
            "Liability_to_Equity",
            "DFL",
            "Interest_Coverage_Ratio",
            "Net_Income_Flag",
            "Equity_to_Liability",
        ]
        df["Bankrupt"] = df["Bankrupt"].map({0: "No", 1: "Yes"})
        df = df.drop(
            columns=[
                "Net_Income_Flag",
                "Current_Liability_to_Liability",
                "Current_Liability_to_Equity",
            ]
        )
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # Liability_Assets_Flag (1 when liabilities exceed assets) is a yes/no flag: categorical (CLEAN-14)
        del df
        return FeatureTypes(categorical=["Liability_Assets_Flag"])
