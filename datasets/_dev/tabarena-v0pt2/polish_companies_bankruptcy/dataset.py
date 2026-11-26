"""Curated dataset definition for `polish_companies_bankruptcy` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import arff
import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Metric, Source, TaskSummary, TimeBasis


class PolishCompaniesBankruptcy(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a Polish company go bankrupt within a year of its financial statement?",
        use_case=(
            "For example, a lender or investor reads a company's annual financial statement and assesses the risk "
            "that it goes bankrupt within a year, to decide on credit or investment."
        ),
        row=(
            "One financial statement of a Polish company from the Emerging Markets Information Service, from the "
            "fifth year of the source's forecasting period (5,790 statements); bankrupt companies are from 2000-2012,"
            " operating ones from 2007-2013."
        ),
        predicted="Whether the company is bankrupt one year after the statement (7.0% are).",
        known=(
            "27 financial ratios of the statement, rebuilt from one set of amounts by the same rule for every "
            "statement: debt, equity, liquidity, working capital, gross profit, turnover and size."
        ),
        split="Random statements; the file has no dates.",
        changes=(
            "We use only the source's fifth-year file (bankruptcy one year later) and drop duplicate rows. The "
            "bankrupt and the operating companies were extracted in separate runs that recorded some items "
            "differently, so we rebuild 27 of the 64 ratios from one set of amounts for every statement, drop the "
            "other 37 and round every value to 4 significant digits."
        ),
        fit="approximate",
        fit_reason=(
            "The ratios come from the statement and the label follows a year later, as in use, and the rebuilt ratios "
            "no longer show which extraction run a statement came from, except through company size. But the "
            "bankrupt and the surviving companies were taken from different periods (2000-2012 against 2007-2013) "
            "and the file has no dates, so part of the signal may be the period rather than the company."
        ),
    )

    # Dataset
    unique_name = "polish_companies_bankruptcy"
    domain = "finance"
    sources = (
        Source(
            role="publication",
            platform="UCI",
            url="https://doi.org/10.24432/C5F600",
            license="CC BY 4.0",
            year="2016",
            bibtex=r"""
                @article{zikeba2016ensemble,
                  title={Ensemble boosted trees with synthetic features generation in application to bankruptcy prediction},
                  author={Zi{\k{e}}ba, Maciej and Tomczak, Sebastian K and Tomczak, Jakub M},
                  journal={Expert systems with applications},
                  volume={58},
                  pages={93--101},
                  year={2016},
                  publisher={Elsevier}
                }
            """,
        ),
    )
    download_description = """
        We download the data from the UCI repository and uzip it to a predefined folder.

        mkdir -p local-data-warehouse/polish_companies_bankruptcy/ && wget -P local-data-warehouse/polish_companies_bankruptcy/ https://archive.ics.uci.edu/static/public/365/polish+companies+bankruptcy+data.zip && unzip local-data-warehouse/polish_companies_bankruptcy/polish+companies+bankruptcy+data.zip -d local-data-warehouse/polish_companies_bankruptcy/ && rm local-data-warehouse/polish_companies_bankruptcy/polish+companies+bankruptcy+data.zip
    """
    curation_comments = """
        - We only use the fifth-year file (5year.arff): its label is bankruptcy one year after the statement, the horizon a lender decides on (Andrej, 2026-11-26). The five yearly files are one panel of the same companies a year apart, without a company id: a statement's sales over its sales growth equal the sales of one statement of the previous file, and 5,603 of the 5,790 statements of 5year (97%) have the same company's statement in 4year. The other files are longer horizons (two to five years) with less signal once the extraction runs below are removed (ROC AUC 0.61-0.75 against 0.79-0.84 for 5year on the rebuilt ratios, measured 2026-11-05), and pooling them would need a company key the source does not give.
        - We removed duplicate statements (every copy of a statement whose 64 ratios repeat).
        - Extraction runs (Andrej, 2026-11-26): the source collected the bankrupt companies (2000-2012) and the operating ones (2007-2013) in separate runs over EMIS, and each run wrote some items by its own conventions: multi-year items copied from one year or missing, total sales or total costs in place of sales, liabilities without a third item, operating profit coded 0, items copied into others, working capital in whole units. On the published 64 ratios, 10 label-free flags of these conventions alone reach ROC AUC 0.964 (LightGBM, the 9 shipped splits) against 0.955 for the ratios.
        - We therefore rebuild every kept ratio from one set of amounts per statement, by the same label-free rule for every row, in units of total assets: sales from the ratios over sales (the median of four implied figures; the source's sales-to-assets ratio holds total sales over total costs in one record format), liabilities as total assets minus equity, current assets from the current ratio and short-term liabilities, inventory and receivables from their day ratios, cash from the net-liabilities ratio, working capital in absolute units as working capital over assets times total assets. 27 ratios stay under their source names; 37 are dropped: the multi-year items (retained earnings, sales growth, three-year gross profit), total sales and total costs over sales, the long-term liability ratios, operating profit and its ratios, profit on sales, extended profit, equity minus share capital, and the ratios on net profit, operating expenses, cost of sales and depreciation, and two whose definition cannot be reproduced from the other columns. Every column is rounded to 4 significant digits, since rebuilt values carry more digits than the source's 5; infinities are missing.
        - Result (2026-11-26): within one class, a model no longer tells the record formats or the missing history apart beyond company size (out-of-fold ROC AUC, LightGBM / logistic regression: operating companies of the reference format against the zero-coded one 0.53 / 0.57, bankrupt companies with against without history 0.53 / 0.54; the reference format against the larger-company format 0.84 / 0.84 with the two size columns, 0.64 / 0.62 without; as published 0.98-1.00 each). On the 9 shipped splits the rebuilt table scores ROC AUC 0.797 (LightGBM) and 0.811 (logistic regression), against 0.955 and 0.924 for the published ratios and 0.729 and 0.777 for the two size columns alone; the bankrupt companies without history score as the others (0.54 / 0.52, as published 0.96 / 0.87). No relation between two or three columns holds at rates that differ by format or class by more than 0.084.
        - The rebuild makes 42 sets of statements identical (84 rows, one set with both labels): their source rows differ only in dropped ratios, mostly the cost items.
        - The bankrupt and the operating companies still come from different periods (the Selection Bias marker), and the file has no dates.
        - We created semantically meaningful feature names.
        - Anomaly: every feature is a ratio the source engineered from the statement; the raw amounts are not published.
    """
    split_leaf = "L-FORCED.random"
    time_basis = TimeBasis(
        "ForcedIIDFromTemporal",
        """
        the statements come from several years, and the file has no dates, so the
        time is lost and part of the signal may be the period. A dated release would test statements later than those
        used for training. Not taken as stationary (Andrej, 2026-11-18): The class/period confounding is explicit in
        the source, and bankruptcy-ratio relations are documented as non-stationary across economic periods.
        """,
    )

    # Task
    target = "company_bankrupt"
    problem_type = "binary_classification"
    metric = Metric.source(
        "roc_auc",
        original="AUC (area under the ROC curve)",
        reference="Zieba, Tomczak & Tomczak, Ensemble boosted trees with synthetic features generation in application to bankruptcy prediction, Expert Systems with Applications 58 (2016) 93-101",
        definition="ROC AUC of bankrupt vs not, per forecasting-year file.",
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        with open(raw_dir / "5year.arff") as f:
            data = arff.load(f)
        df = pd.DataFrame(data["data"], columns=[x[0] for x in data["attributes"]])
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        target_feature = self.task_metadata.target_column_name
        df = raw.copy()
        df.columns = [*(f"X{k}" for k in range(1, 65)), target_feature]
        # conflicting duplicates drop (without target column), on the source's 64 ratios
        df = df.drop_duplicates(subset=[c for c in df.columns if c != target_feature], keep=False)
        x = df.drop(columns=[target_feature]).astype(float)
        out = _rebuild(x)
        out[target_feature] = df[target_feature].map({"1": "Yes", "0": "No"})
        return out


def _significant(v: pd.Series, digits: int = 4) -> pd.Series:
    """Round to ``digits`` significant digits (the source writes 5; rebuilt values carry more)."""
    a = v.to_numpy(dtype=float)
    with np.errstate(all="ignore"):
        scale = 10.0 ** (digits - 1 - np.floor(np.log10(np.abs(a))))
        r = np.round(a * scale) / scale
    return pd.Series(np.where(np.isfinite(a) & (a != 0), r, np.where(a == 0, 0.0, np.nan)), index=v.index)


def _rebuild(x: pd.DataFrame) -> pd.DataFrame:
    """The 27 ratios rebuilt from one set of amounts per statement, by the same label-free rule for every row.

    ``Xk`` is UCI attribute k. Amounts are in units of total assets. Format F2 (``X9`` holds total sales over total
    costs, and the ratios over sales use another figure): one of the four sales figures the ratios over sales imply
    differs from ``X9`` by more than 0.2%, or ``X9 * X58`` is 1 within 0.2%. Sales are the median of the usable
    implied figures, ``X9`` where none is usable outside F2.
    """
    with np.errstate(all="ignore"):
        implied = pd.concat([x.X1 / x.X23, x.X18 / x.X19, x.X35 / x.X39, x.X63 * x.X51], axis=1)
        usable = pd.concat(
            [
                (x.X1.abs() > 1e-3) & (x.X23.abs() > 1e-3),
                (x.X18.abs() > 1e-3) & (x.X19.abs() > 1e-3),
                (x.X35.abs() > 1e-3) & (x.X39.abs() > 1e-3),
                x.X63.notna() & x.X51.notna() & (x.X51.abs() > 1e-4),
            ],
            axis=1,
        )
        implied = implied.where(usable.to_numpy()).replace([np.inf, -np.inf], np.nan)
        other_sales = ((implied.div(x.X9, axis=0) - 1).abs() > 2e-3).sum(axis=1) >= 1
        f2 = other_sales | ((x.X9 * x.X58 - 1).abs() < 2e-3)
        sales = implied.median(axis=1)
        sales = sales.where(sales.notna() | f2, x.X9)
        tl = 1 - x.X10  # liabilities as total assets minus equity
        ca = x.X4 * x.X51
        wc = ca - x.X51
        fa = 1 - ca
        inv = x.X20 * sales / 365
        rec = x.X44 * sales / 365
        cash = x.X2 - x.X30 * sales
        cols = {
            "total_liabilities_to_total_assets": tl,
            "working_capital_to_total_assets": wc,
            "current_assets_to_short_term_liabilities": x.X4,
            "book_value_equity_to_total_liabilities": x.X10 / tl,
            "sales_to_total_assets": sales,
            "equity_to_total_assets": x.X10,
            "gross_profit_to_short_term_liabilities": x.X18 / x.X51,
            "total_assets_to_total_liabilities": 1 / tl,
            "gross_profit_to_total_assets": x.X18,
            "gross_profit_to_sales": x.X18 / sales,
            "inventory_days_ratio": x.X20,
            "working_capital_to_fixed_assets": wc / fa,
            "log_total_assets": x.X29,
            "net_liabilities_to_sales": (tl - cash) / sales,
            "liquid_assets_to_short_term_liabilities": (ca - inv - rec) / x.X51,
            "receivables_plus_inventory_turnover_days": (inv + rec) * 365 / sales,
            "receivables_days_ratio": x.X44,
            "current_assets_minus_inventory_to_short_term_liabilities": (ca - inv) / x.X51,
            "current_assets_to_total_liabilities": ca / tl,
            "short_term_liabilities_to_total_assets": x.X51,
            "equity_to_fixed_assets": x.X10 / fa,
            "working_capital_absolute": wc * 10**x.X29,
            "inventory_turnover_ratio": sales / inv,
            "receivables_turnover_ratio": sales / rec,
            "short_term_liabilities_days_ratio": x.X51 * 365 / sales,
            "sales_to_short_term_liabilities": sales / x.X51,
            "sales_to_fixed_assets": sales / fa,
        }
    out = pd.DataFrame(cols, index=x.index).replace([np.inf, -np.inf], np.nan)
    return out.apply(_significant)
