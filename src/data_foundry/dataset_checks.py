from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats


def run_all_checks(
    *,
    data: pd.DataFrame,
    classification: bool,
    target_feature: str,
    print_report: bool = True,
):
    """Run a suite of common checks on tabular data to surface potential issues.

    This function prints a comprehensive summary of a dataset, including basic
    statistics, feature-level information, missing values, unique values,
    example values and duplicate ratios. It also reports target class counts
    when performing classification.

    Parameters
    ----------
    data : pandas.DataFrame
        The dataset to evaluate.
    classification : bool
        Whether the task is classification. If True, the function will display
        the distribution of the target classes.
    target_feature : str
        Name of the target variable.
    print_report : bool
        Whether to print the report to the console. Default is True.
    """
    # Set display options to show all rows and columns
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)
    pd.set_option("display.max_colwidth", None)

    # FIMXE: remove or add later again...
    # # pd.set_option("display.expand_frame_repr", False)
    # if get_ipython() is not None:
    #     from IPython.display import HTML, display
    #
    #     display(HTML("<style>div.jp-OutputArea-output pre {white-space: pre;}</style>"))
    #     display(HTML("<style>div.output_area pre {white-space: pre;}</style>"))

    # Validate inputs
    if target_feature not in data.columns:
        raise ValueError(f"target_feature '{target_feature}' is not in the DataFrame.")

    # Display high-level overview
    print("\n#### Dataset Overview")
    print(f"Rows: {len(data):,}")
    print(f"Columns: {data.shape[1]}")

    df_head = data.head(5)
    # Feature summary: dtype, missing counts, unique counts, example values
    summary = pd.DataFrame(
        {
            "dtype": data.dtypes,
            "n_missing": data.isna().sum(),
            "pct_missing": (data.isna().mean() * 100).round(2),
            "n_unique": data.nunique(),
        }
    )

    # Collect up to 10 example values for each column
    def get_examples(col: pd.Series, n: int = 10) -> str:
        # get most frequent non-null values
        most_common_vals = col.dropna().value_counts().head(n).index
        processed_vals = []

        for val in most_common_vals:
            if pd.api.types.is_numeric_dtype(type(val)):
                if pd.api.types.is_float_dtype(type(val)) and round(val, 4) != 0:
                    val = round(val, 4)
            processed_vals.append(str(val))

        return ", ".join(processed_vals)

    summary["examples"] = data.apply(get_examples)
    summary["dtype"] = summary["dtype"].astype("string")
    summary = summary.sort_values(
        ["dtype", "pct_missing"], ascending=[True, False]
    ).reset_index()

    # Detailed statistics for numeric features
    numeric_stats = "No numeric features to summarize."
    numeric_cols = data.select_dtypes(include=[np.number])
    if not numeric_cols.empty:
        numeric_stats = numeric_cols.describe().T
        numeric_stats = numeric_stats[["count", "mean", "std", "min", "max"]]

    # Detailed statistics for non-numeric (categorical or object) features
    cat_stats = "No categorical/object features to summarize."
    cat_cols = data.select_dtypes(exclude=[np.number])
    MAX_LEN = 67

    def truncate_value(v, max_len=MAX_LEN):
        if pd.isna(v):
            return "<NA>"
        s = str(v)
        return s if len(s) <= max_len else s[: max_len - 3] + "..."

    if not cat_cols.empty:
        frames = []
        n = len(data)

        for col in cat_cols.columns:
            vc = data[col].value_counts(dropna=False).head(5)

            df_col = vc.rename_axis("value").reset_index(name="count")
            df_col["value"] = df_col["value"].map(truncate_value)
            df_col["pct"] = (df_col["count"] / n * 100).round(2)
            df_col["rank"] = range(1, len(df_col) + 1)
            df_col["column"] = col

            frames.append(df_col[["column", "rank", "value", "count", "pct"]])

        cat_stats = (
            pd.concat(frames, ignore_index=True)
            .set_index(["column", "rank"])
            .sort_index()
        )

    # Target distribution (classification task)
    if classification:
        target_counts = data[target_feature].value_counts(dropna=False)
        target_pct = (target_counts / len(data) * 100).round(2)
        target_df = pd.DataFrame({"count": target_counts, "pct": target_pct})
    else:
        y_missing_count = data[target_feature].isna().sum()
        y = pd.Series(data[target_feature]).dropna().astype(float)
        nonpos_pct = (y <= 0).mean() * 100

        # log transform choice
        if (y > 0).all():
            y_log = np.log(y)
            log_type = "log"
        else:
            y_log = np.log1p(y)
            log_type = "log1p"

        # basic shape stats
        skew_y = stats.skew(y, bias=False)
        skew_log = stats.skew(y_log, bias=False)

        var_y = y.var()
        var_log = y_log.var()

        # distribution check on positive values only
        y_pos = y[y > 0]
        if len(y_pos) >= 30:
            # exponential
            _, scale = stats.expon.fit(y_pos)
            ll_exp = np.sum(stats.expon.logpdf(y_pos, scale=scale))
            aic_exp = 2 * 1 - 2 * ll_exp  # 1 param: scale

            # lognormal
            s, _, scale = stats.lognorm.fit(y_pos)
            ll_logn = np.sum(stats.lognorm.logpdf(y_pos, s=s, scale=scale))
            aic_logn = 2 * 2 - 2 * ll_logn  # 2 params: s, scale

            dist_hint = "lognormal" if aic_logn < aic_exp else "exponential"
        else:
            aic_exp = aic_logn = np.nan
            dist_hint = "insufficient_data"

        target_df = pd.DataFrame(
            {
                "y_missing_count": [y_missing_count],
                "non_positive_pct": [round(nonpos_pct, 2)],
                "skew_y": [round(skew_y, 3)],
                "skew_log": [round(skew_log, 3)],
                "var_y": [round(var_y, 3)],
                "var_log": [round(var_log, 3)],
                "log_used": [log_type],
                "aic_exponential": [round(aic_exp, 1)],
                "aic_lognormal": [round(aic_logn, 1)],
                "dist_hint": [dist_hint],
            }
        )

    if print_report:
        print("\n#### Sample Rows")
        print(df_head)
        print("\n#### Feature Summary")
        print(summary)
        print("\n#### Numeric Feature Statistics")
        print(numeric_stats)
        print("\n#### Categorical Feature Statistics")
        print(cat_stats)
        print("\n#### Target Distribution")
        print(target_df)

    # Duplicate checks
    total_dups = data.duplicated().sum()
    pct_dups = total_dups / len(data) * 100
    dups_wo_target = data.drop(columns=[target_feature]).duplicated().sum()
    pct_dups_wo_target = dups_wo_target / len(data) * 100

    print("\n#### Duplicate Report")
    print(f"Total duplicate rows: {total_dups} ({pct_dups:.2f}% of dataset)")
    print(
        f"Duplicate rows ignoring target: {dups_wo_target} ({pct_dups_wo_target:.2f}% of dataset)"
    )
    print("\nData quality checks completed.")

    return df_head, summary, numeric_stats, cat_stats, target_df
