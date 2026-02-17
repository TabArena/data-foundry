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
    # Performance tuning for very large DataFrames
    sample_threshold: int = 1_000_000,
    sample_frac: float = 0.1,
    sample_random_state: int = 0,
):
    """Run a suite of common checks on tabular data to surface potential issues.

    This function prints a comprehensive summary of a dataset, including basic
    statistics, feature-level information, missing values, unique values,
    example values and duplicate ratios. It also reports target class counts
    when performing classification.

    For very large DataFrames, you can set `sample_threshold` and `sample_frac`
    to run the heavier, approximate computations (example values, top category
    frequencies, numeric summaries and distribution fitting) on a random
    sample. Missing-value counts, duplicate detection and exact target class
    counts are always computed on the full dataset.

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
    sample_threshold : int
        If len(data) > sample_threshold, heavy computations use a random sample.
        Default 1_000_000 (disabled for smaller datasets).
    sample_frac : float
        Fraction of rows to sample for heavy computations when sampling is used.
    sample_random_state : int
        Random state used for sampling reproducibility.
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

    # Decide whether to sample for heavy operations
    n_rows = len(data)
    use_sampling = sample_frac is not None and n_rows > sample_threshold and 0.0 < sample_frac < 1.0
    sample_df = data.sample(frac=sample_frac, random_state=sample_random_state) if use_sampling else data

    # Display high-level overview
    cols = list(data.columns)

    print("\n#### Dataset Overview")
    print(f"Rows: {n_rows:,}")
    print(f"Columns: {len(cols)}")

    # Keep a small sample head (this is small memory)
    df_head = data.head(5)

    # Feature summary: dtype, missing counts, unique counts, example values
    # For very large DataFrames avoid creating full intermediate DataFrames
    dtypes = data.dtypes  # small

    # Compute missing and unique counts per-column without creating a full isna() DataFrame
    n_missing = pd.Series(index=cols, dtype=int)
    n_unique = pd.Series(index=cols, dtype=int)
    for c in cols:
        s = data[c]
        n_missing[c] = int(s.isna().sum())
        # keep pandas default behavior for nunique (dropna=True)
        n_unique[c] = int(s.nunique())

    pct_missing = (n_missing / n_rows * 100).round(2)

    summary = pd.DataFrame(
        {
            "dtype": dtypes,
            "n_missing": n_missing,
            "pct_missing": pct_missing,
            "n_unique": n_unique,
        }
    )

    # Helper that extracts examples from a Series; uses sample_df for heavy ops when sampling
    def get_examples_from_series(s: pd.Series, n: int = 10) -> str:
        s_for = s if not use_sampling else s.loc[s.index.isin(sample_df.index)]
        vc_index = s_for.dropna().value_counts().head(n).index
        vals = []
        for v in vc_index:
            # avoid expensive dtype checks on the whole Series; handle numeric formatting here
            display_v = (round(v, 4) if round(v, 4) != 0 else 0.0) if isinstance(v, float) and not np.isnan(v) else v
            vals.append(str(display_v))
        return ", ".join(vals)

    # Build examples per-column (avoids DataFrame.apply which can allocate)
    examples = {}
    for c in cols:
        examples[c] = get_examples_from_series(data[c])

    summary["examples"] = pd.Series(examples)
    summary["dtype"] = summary["dtype"].astype("string")
    summary = summary.sort_values(["dtype", "pct_missing"], ascending=[True, False]).reset_index()

    # Free some temporarily held Series that are now in `summary`
    del dtypes, n_missing, pct_missing, n_unique, examples

    # Detailed statistics for numeric features computed per-column; use sample_df for heavy ops when enabled
    numeric_stats = "No numeric features to summarize."
    numeric_cols = [c for c in cols if np.issubdtype(data[c].dtype, np.number)]
    if numeric_cols:
        stats_rows = {}
        for c in numeric_cols:
            s_full = data[c]
            s_for = s_full if not use_sampling else s_full.loc[s_full.index.isin(sample_df.index)]
            cnt = s_for.count()
            stats_rows[c] = {
                "count": float(cnt),
                "mean": float(s_for.mean()) if cnt > 0 else np.nan,
                "std": float(s_for.std()) if cnt > 0 else np.nan,
                "min": float(s_for.min()) if cnt > 0 else np.nan,
                "max": float(s_for.max()) if cnt > 0 else np.nan,
            }
        numeric_stats = pd.DataFrame.from_dict(stats_rows, orient="index")
        numeric_stats = numeric_stats[["count", "mean", "std", "min", "max"]]

    # Detailed statistics for non-numeric (categorical or object) features
    cat_stats = "No categorical/object features to summarize."
    cat_cols = [c for c in cols if c not in numeric_cols]
    MAX_LEN = 67

    def truncate_value(v, max_len=MAX_LEN):
        if pd.isna(v):
            return "<NA>"
        s = str(v)
        return s if len(s) <= max_len else s[: max_len - 3] + "..."

    if cat_cols:
        frames = []
        n = n_rows if not use_sampling else len(sample_df)
        for col in cat_cols:
            s_col = data[col]
            s_for = s_col if not use_sampling else s_col.loc[s_col.index.isin(sample_df.index)]
            vc = s_for.value_counts(dropna=False).head(5)
            df_col = vc.rename_axis("value").reset_index(name="count")
            df_col["value"] = df_col["value"].map(truncate_value)
            df_col["pct"] = (df_col["count"] / n * 100).round(2)
            df_col["rank"] = range(1, len(df_col) + 1)
            df_col["column"] = col
            frames.append(df_col[["column", "rank", "value", "count", "pct"]])
        if frames:
            cat_stats = pd.concat(frames, ignore_index=True).set_index(["column", "rank"]).sort_index()
        del frames

    # Target distribution (classification task) - always exact on full data
    if classification:
        target_counts = data[target_feature].value_counts(dropna=False)
        target_pct = (target_counts / n_rows * 100).round(2)
        target_df = pd.DataFrame({"count": target_counts, "pct": target_pct})
    else:
        # Work directly on the target series to avoid copies; for distribution fitting, use sample_df when enabled
        target_series = data[target_feature]
        y_missing_count = int(target_series.isna().sum())

        y_full = target_series[target_series.notna()].astype(float)
        y = y_full if not use_sampling else y_full.loc[y_full.index.isin(sample_df.index)]
        nonpos_pct = float((y <= 0).mean() * 100) if len(y) > 0 else 0.0

        # log transform choice
        if (y > 0).all():
            y_log = np.log(y)
            log_type = "log"
        else:
            y_log = np.log1p(y)
            log_type = "log1p"

        # basic shape stats computed on Series
        skew_y = float(stats.skew(y, bias=False)) if len(y) > 0 else np.nan
        skew_log = float(stats.skew(y_log, bias=False)) if len(y_log) > 0 else np.nan

        var_y = float(y.var()) if len(y) > 0 else np.nan
        var_log = float(y_log.var()) if len(y_log) > 0 else np.nan

        # distribution check on positive values only
        y_pos = y[y > 0]
        if len(y_pos) >= 30:
            _, scale = stats.expon.fit(y_pos)
            ll_exp = np.sum(stats.expon.logpdf(y_pos, scale=scale))
            aic_exp = 2 * 1 - 2 * ll_exp  # 1 param: scale

            s_fit, _, scale = stats.lognorm.fit(y_pos)
            ll_logn = np.sum(stats.lognorm.logpdf(y_pos, s=s_fit, scale=scale))
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
        del target_series, y_full, y, y_log, y_pos

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
    total_dups = int(data.duplicated().sum())
    pct_dups = total_dups / n_rows * 100 if n_rows > 0 else 0.0
    # Duplicate rows ignoring target
    cols_wo_target = [c for c in cols if c != target_feature]
    dups_wo_target = int(data.duplicated(subset=cols_wo_target).sum())
    pct_dups_wo_target = dups_wo_target / n_rows * 100 if n_rows > 0 else 0.0

    print("\n#### Duplicate Report")
    print(f"Total duplicate rows: {total_dups} ({pct_dups:.2f}% of dataset)")
    print(f"Duplicate rows ignoring target: {dups_wo_target} ({pct_dups_wo_target:.2f}% of dataset)")

    if duplicate_column_check:
        print("Get column duplicates...")
        # Compute a hash fingerprint per column in a memory-friendly loop
        # (pd.util.hash_pandas_object applied per-series)
        col_hashes = pd.Series(index=cols, dtype="uint64")
        for c in cols:
            col_hashes[c] = int(pd.util.hash_pandas_object(data[c], index=False).sum())

        # Group columns by hash value
        hash_groups = col_hashes.groupby(col_hashes).groups

        duplicate_cols = []
        for group in hash_groups.values():
            group_cols = list(group)
            if len(group_cols) > 1:
                base = group_cols[0]
                for c in group_cols[1:]:
                    if data[base].equals(data[c]):
                        duplicate_cols.append(c)

        n_dup_cols = len(duplicate_cols)
        pct_dup_cols = n_dup_cols / len(cols) * 100 if len(cols) > 0 else 0.0

        print(f"Duplicate columns: {n_dup_cols} ({pct_dup_cols:.2f}% of columns)")
        if n_dup_cols > 0:
            print("Duplicate column names:")
            for col in duplicate_cols:
                print(f"  - {col}")

        # cleanup
        del col_hashes, hash_groups, duplicate_cols

    # cleanup remaining temporaries (do not delete returned objects)

    print("\nData quality checks completed.")
    return df_head, summary, numeric_stats, cat_stats, target_df
