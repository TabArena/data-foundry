from __future__ import annotations

import numpy as np
import pandas as pd


def run_all_checks(
    *,
    data: pd.DataFrame,
    classification: bool,
    target_feature: str,
    print_report: bool = True,
    duplicate_column_check: bool = True,
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
    duplicate_column_check: bool
        Whether to check for duplicate columns. Default is True.
    """
    from scipy import stats

    # Set display options to show all rows and columns
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)
    pd.set_option("display.max_colwidth", None)

    # Validate inputs
    if target_feature not in data.columns:
        raise ValueError(f"target_feature '{target_feature}' is not in the DataFrame.")

    # Display high-level overview
    print("\n#### Dataset Overview")
    print(f"Rows: {len(data):,}")
    print(f"Columns: {data.shape[1]}")

    # Keep a small sample head (this is small memory)
    df_head = data.head(5)

    # Feature summary: dtype, missing counts, unique counts, example values
    # Use views/series from the original DataFrame where possible to avoid copies
    dtypes = data.dtypes
    n_missing = data.isna().sum()
    pct_missing = (n_missing / len(data) * 100).round(2)
    n_unique = data.nunique()

    summary = pd.DataFrame(
        {
            "dtype": dtypes,
            "n_missing": n_missing,
            "pct_missing": pct_missing,
            "n_unique": n_unique,
        }
    )

    # Collect up to 10 example values for each column
    def get_examples(col: pd.Series, n: int = 10) -> str:
        # get most frequent non-null values
        most_common_vals = col.dropna().value_counts().head(n).index
        processed_vals = []

        for v in most_common_vals:
            display_val = v
            # Use isinstance checks to avoid misusing pandas dtype helpers on types
            if isinstance(v, (int, float, np.number)):
                if isinstance(v, float) and round(v, 4) != 0:
                    display_val = round(v, 4)
            processed_vals.append(str(display_val))

        return ", ".join(processed_vals)

    # Apply column-wise; apply returns a Series view when possible
    summary["examples"] = data.apply(get_examples)
    summary["dtype"] = summary["dtype"].astype("string")
    summary = summary.sort_values(["dtype", "pct_missing"], ascending=[True, False]).reset_index()

    # Free some temporarily held Series that are now in `summary`
    del dtypes, n_missing, pct_missing, n_unique

    # Detailed statistics for numeric features
    numeric_stats = "No numeric features to summarize."
    numeric_cols = data.select_dtypes(include=[np.number])
    if numeric_cols.shape[1] > 0:
        # describe() will create a small summary; keep only needed columns
        numeric_stats = numeric_cols.describe().T
        numeric_stats = numeric_stats[["count", "mean", "std", "min", "max"]]

    # We can drop numeric_cols reference now to release memory
    if "numeric_cols" in locals():
        del numeric_cols

    # Detailed statistics for non-numeric (categorical or object) features
    cat_stats = "No categorical/object features to summarize."
    cat_cols = data.select_dtypes(exclude=[np.number])
    MAX_LEN = 67

    def truncate_value(v, max_len=MAX_LEN):
        if pd.isna(v):
            return "<NA>"
        s = str(v)
        return s if len(s) <= max_len else s[: max_len - 3] + "..."

    if cat_cols.shape[1] > 0:
        frames = []
        n = len(data)

        # Iterate column names to avoid copying whole DataFrame where possible
        for col in cat_cols.columns:
            vc = data[col].value_counts(dropna=False).head(5)

            df_col = vc.rename_axis("value").reset_index(name="count")
            df_col["value"] = df_col["value"].map(truncate_value)
            df_col["pct"] = (df_col["count"] / n * 100).round(2)
            df_col["rank"] = range(1, len(df_col) + 1)
            df_col["column"] = col

            frames.append(df_col[["column", "rank", "value", "count", "pct"]])

        cat_stats = pd.concat(frames, ignore_index=True).set_index(["column", "rank"]).sort_index()

        # drop temporary structures
        del frames

    # drop cat_cols reference
    if "cat_cols" in locals():
        del cat_cols

    # Target distribution (classification task)
    if classification:
        target_counts = data[target_feature].value_counts(dropna=False)
        target_pct = (target_counts / len(data) * 100).round(2)
        target_df = pd.DataFrame({"count": target_counts, "pct": target_pct})
    else:
        # Work directly on the target series to avoid copies
        target_series = data[target_feature]
        y_missing_count = target_series.isna().sum()

        # Drop NA in place by creating view via .loc on non-null mask
        y = target_series[target_series.notna()].astype(float)
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

        # cleanup target-related temporaries
        del target_series, y, y_log, y_pos

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
    print("Get row duplicates...")
    total_dups = data.duplicated().sum()
    pct_dups = total_dups / len(data) * 100
    # Fixed bug: use data.duplicated (was data.data.duplicated)
    dups_wo_target = data.duplicated(subset=[c for c in data.columns if c != target_feature]).sum()
    pct_dups_wo_target = dups_wo_target / len(data) * 100

    print("\n#### Duplicate Report")
    print(f"Total duplicate rows: {total_dups} ({pct_dups:.2f}% of dataset)")
    print(f"Duplicate rows ignoring target: {dups_wo_target} ({pct_dups_wo_target:.2f}% of dataset)")

    if duplicate_column_check:
        print("Get column duplicates...")
        # --- Efficient duplicate column check (hash-based) ---
        # Compute hash fingerprint per column without copying whole DataFrame
        col_hashes = data.apply(lambda s: pd.util.hash_pandas_object(s, index=False).sum())

        # Group columns by hash
        hash_groups = col_hashes.groupby(col_hashes).groups

        duplicate_cols = []

        # Verify equality within hash groups (protect against rare collisions)
        for group in hash_groups.values():
            group_cols = list(group)
            if len(group_cols) > 1:
                base = group_cols[0]
                for c in group_cols[1:]:
                    if data[base].equals(data[c]):
                        duplicate_cols.append(c)

        n_dup_cols = len(duplicate_cols)
        pct_dup_cols = n_dup_cols / data.shape[1] * 100

        print(f"Duplicate columns: {n_dup_cols} ({pct_dup_cols:.2f}% of columns)")
        if n_dup_cols > 0:
            print("Duplicate column names:")
            for col in duplicate_cols:
                print(f"  - {col}")

        # cleanup
        del col_hashes, hash_groups, duplicate_cols

    # cleanup remaining temporaries (do not delete returned objects)
    # Keep numeric_stats and cat_stats as they may be returned/printed

    print("\nData quality checks completed.")
    return df_head, summary, numeric_stats, cat_stats, target_df
