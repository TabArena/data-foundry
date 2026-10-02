"""Curated dataset definition for `polish_companies_bankruptcy` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import arff
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset


class PolishCompaniesBankruptcy(AbstractCuratedDataset):
    # Dataset
    unique_name = "polish_companies_bankruptcy"
    year = "2010"
    domain = "finance"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5F600"
    license = "CC BY 4.0"
    download_description = """
        We download the data from the UCI repository and uzip it to a predefined folder.

        mkdir -p local-data-warehouse/polish_companies_bankruptcy/ && wget -P local-data-warehouse/polish_companies_bankruptcy/ https://archive.ics.uci.edu/static/public/365/polish+companies+bankruptcy+data.zip && unzip local-data-warehouse/polish_companies_bankruptcy/polish+companies+bankruptcy+data.zip -d local-data-warehouse/polish_companies_bankruptcy/ && rm local-data-warehouse/polish_companies_bankruptcy/polish+companies+bankruptcy+data.zip
    """
    bibtex = r"""
        @article{zikeba2016ensemble,
          title={Ensemble boosted trees with synthetic features generation in application to bankruptcy prediction},
          author={Zi{\k{e}}ba, Maciej and Tomczak, Sebastian K and Tomczak, Jakub M},
          journal={Expert systems with applications},
          volume={58},
          pages={93--101},
          year={2016},
          publisher={Elsevier}
        }
    """
    curation_comments = """
        - We only use data from year 5 (5year.arff), because it is the newest data and the target is bankruptcy status after only 1 year.
        - We created semantically meaningful feature names.
        - We removed duplicates.
        - Anomaly: the data contains a lot of features created by feature engineering.
    """

    # Task
    target = "company_bankrupt"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        with open(raw_dir / "5year.arff") as f:
            data = arff.load(f)
        df = pd.DataFrame(data["data"], columns=[x[0] for x in data["attributes"]])
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        target_feature = self.task_metadata.target_column_name
        df.columns = [
            "net_profit_to_total_assets",
            "total_liabilities_to_total_assets",
            "working_capital_to_total_assets",
            "current_assets_to_short_term_liabilities",
            "liquidity_days_ratio",
            "retained_earnings_to_total_assets",
            "ebit_to_total_assets",
            "book_value_equity_to_total_liabilities",
            "sales_to_total_assets",
            "equity_to_total_assets",
            "extended_profit_to_total_assets",
            "gross_profit_to_short_term_liabilities",
            "gross_profit_plus_depreciation_to_sales",
            "gross_profit_plus_interest_to_total_assets",
            "liabilities_days_ratio",
            "gross_profit_plus_depreciation_to_total_liabilities",
            "total_assets_to_total_liabilities",
            "gross_profit_to_total_assets",
            "gross_profit_to_sales",
            "inventory_days_ratio",
            "sales_growth_ratio",
            "operating_profit_to_total_assets",
            "net_profit_to_sales",
            "three_year_gross_profit_to_total_assets",
            "equity_minus_share_capital_to_total_assets",
            "net_profit_plus_depreciation_to_total_liabilities",
            "operating_profit_to_financial_expenses",
            "working_capital_to_fixed_assets",
            "log_total_assets",
            "net_liabilities_to_sales",
            "gross_profit_plus_interest_to_sales",
            "current_liabilities_days_ratio",
            "operating_expenses_to_short_term_liabilities",
            "operating_expenses_to_total_liabilities",
            "sales_profit_to_total_assets",
            "total_sales_to_total_assets",
            "current_assets_minus_inventories_to_long_term_liabilities",
            "constant_capital_to_total_assets",
            "sales_profit_to_sales",
            "liquid_assets_to_short_term_liabilities",
            "liabilities_to_adjusted_operating_profit",
            "operating_profit_to_sales",
            "receivables_plus_inventory_turnover_days",
            "receivables_days_ratio",
            "net_profit_to_inventory",
            "current_assets_minus_inventory_to_short_term_liabilities",
            "inventory_days_cost_ratio",
            "ebitda_to_total_assets",
            "ebitda_to_sales",
            "current_assets_to_total_liabilities",
            "short_term_liabilities_to_total_assets",
            "short_term_liabilities_days_cost_ratio",
            "equity_to_fixed_assets",
            "constant_capital_to_fixed_assets",
            "working_capital_absolute",
            "gross_margin",
            "adjusted_liquidity_ratio",
            "total_costs_to_total_sales",
            "long_term_liabilities_to_equity",
            "inventory_turnover_ratio",
            "receivables_turnover_ratio",
            "short_term_liabilities_days_ratio",
            "sales_to_short_term_liabilities",
            "sales_to_fixed_assets",
            target_feature,
        ]
        df[target_feature] = df[target_feature].map({"1": "Yes", "0": "No"})
        # conflicting duplicates drop (without target column)
        df = df.drop_duplicates(
            subset=[c for c in df.columns if c != self.task_metadata.target_column_name], keep=False
        )
        return df
