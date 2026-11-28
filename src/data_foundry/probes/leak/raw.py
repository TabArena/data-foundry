"""The raw state before ``_clean`` (probes 10, 18, 19, 20, 21): the target in the source's row order, cells filled by
interpolation, the rows ``_clean`` removed, the columns it dropped, and copies before deduplication.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from data_foundry.probes.leak.core import profile_codes, say, score


def straight_line_fills(values: pd.Series) -> pd.Series:
    """Cells on a straight line between the cells above and below, in the order given: a cell whose step from the row
    above equals its step to the row below (and is not zero), in a run of two or more such cells, or alone when the
    step is finer than 0.01. Gaps filled by linear interpolation leave this trace; so do runs of round values by
    chance (92, 91, 90, 89), which only the values themselves can tell apart.
    """
    v = values.astype(float)
    step_in, step_out = v.diff(), -v.diff(-1)
    hit = ((step_in - step_out).abs() < 1e-6 * v.abs().clip(lower=1)) & (step_in.abs() > 1e-9)
    run_size = hit.groupby((hit != hit.shift()).cumsum()).transform("size")
    finer = (step_in * 100 - (step_in * 100).round()).abs() > 1e-6
    return hit & ((run_size >= 2) | finer)


def fill_counts(raw: pd.DataFrame, target: str, *, min_cells: int = 5) -> dict[str, dict[str, int]]:
    """Per numeric column of ``raw``, in its row order, the cells of ``straight_line_fills`` counted per target value;
    the columns with at least ``min_cells`` of them, most first.
    """
    out = {}
    for col in raw.columns:
        if col == target or not pd.api.types.is_numeric_dtype(raw[col]) or raw[col].nunique() <= 5:
            continue
        hit = straight_line_fills(raw[col])
        if hit.sum() >= min_cells:
            out[col] = {str(k): int(n) for k, n in hit.groupby(raw[target]).sum().items()}
    return dict(sorted(out.items(), key=lambda kv: -sum(kv[1].values())))


def row_order(y: pd.Series, problem_type: str) -> dict:
    """Probe 10, the target by row position in the source's order: ``y`` is the target of the rows in their raw order.

    A classification target gets the next-row label match against chance (the sum of the squared class shares, with
    a z score) and the largest gap between a class's share in a tenth of the rows and overall; a regression target
    the Spearman correlation with the position and the lag-1 autocorrelation. Rows sorted or blocked by the target
    show up here, and shuffled rows give chance. ``flag``: z of 5 or more, a gap of 0.1 or more, or a correlation of
    0.1 or more in size. A source in time order shows autocorrelation by nature: read it against the time column.
    """
    y = y.reset_index(drop=True)
    n = len(y)
    out: dict = {"rows": n}
    if problem_type == "regression":
        v = pd.to_numeric(y, errors="coerce")
        out["spearman_position"] = float(pd.Series(np.arange(n), dtype=float).corr(v, method="spearman"))
        out["lag1_autocorrelation"] = float(v.autocorr(lag=1)) if n > 2 else float("nan")
        sizes = [abs(out["spearman_position"]), abs(out["lag1_autocorrelation"])]
        out["flag"] = bool(np.nanmax(sizes) >= 0.1) if not np.all(np.isnan(sizes)) else False
        return out
    labels = y.astype(str).where(y.notna())
    shares = labels.value_counts(normalize=True)
    chance = float((shares**2).sum())
    values = labels.to_numpy()
    both = pd.notna(values[1:]) & pd.notna(values[:-1])
    match = float((values[1:][both] == values[:-1][both]).mean()) if both.any() else float("nan")
    se = float(np.sqrt(chance * (1 - chance) / max(int(both.sum()), 1)))
    tenth = np.minimum(np.arange(n) * 10 // max(n, 1), 9)
    by_tenth = pd.crosstab(tenth, labels, normalize="index")
    gap = float((by_tenth - shares.reindex(by_tenth.columns)).abs().to_numpy().max()) if len(by_tenth) else 0.0
    out.update(next_row_match=match, chance=chance, z=(match - chance) / se if se else float("nan"))
    out["largest_tenth_gap"] = gap
    out["flag"] = bool((se and out["z"] >= 5) or gap >= 0.1)
    return out


def removed_rows(raw_y: pd.Series | None, kept: np.ndarray, problem_type: str) -> dict:
    """Probe 19, the rows ``_clean`` removed: ``kept`` marks each raw row that reaches the curated frame (booleans in
    raw order); ``raw_y`` is the raw table's target column, or None when it has none of that name.

    Gives the counts and, with ``raw_y``, the target of the removed rows against the kept ones, unlabelled rows
    counted apart: the class shares (``flag`` at a gap of 0.1 or more), or the medians and the mean shift in
    standard deviations of all labelled rows (``flag`` at 0.5 or more). A filter that removes rows by their outcome (an
    extreme target, one class) selects on the label: CLEAN-11 and USE-7 say when that is right.
    """
    kept = np.asarray(kept, dtype=bool)
    out: dict = {"raw_rows": len(kept), "kept": int(kept.sum()), "removed": int((~kept).sum())}
    if raw_y is None or kept.all():
        return out
    raw_y = raw_y.reset_index(drop=True)
    labelled = raw_y.notna().to_numpy()
    out["removed_unlabelled"] = int((~kept & ~labelled).sum())
    gone, stay = ~kept & labelled, kept & labelled
    if not gone.any():
        out["flag"] = False
        return out
    if problem_type == "regression":
        v = pd.to_numeric(raw_y, errors="coerce")
        a, b = v[gone], v[stay]
        sd = float(v[labelled].std())
        out.update(removed_median=float(a.median()), kept_median=float(b.median()))
        out["mean_shift_sd"] = float((a.mean() - b.mean()) / sd) if sd else float("nan")
        out["flag"] = bool(abs(out["mean_shift_sd"]) >= 0.5) if sd else False
        return out
    labels = raw_y.astype(str)
    removed_shares = labels[gone].value_counts(normalize=True)
    kept_shares = labels[stay].value_counts(normalize=True)
    classes = removed_shares.index.union(kept_shares.index)
    gaps = (removed_shares.reindex(classes, fill_value=0) - kept_shares.reindex(classes, fill_value=0)).abs()
    out["removed_shares"] = {str(k): round(float(v), 4) for k, v in removed_shares.items()}
    out["kept_shares"] = {str(k): round(float(v), 4) for k, v in kept_shares.items()}
    out["largest_share_gap"] = float(gaps.max())
    out["flag"] = bool(gaps.max() >= 0.1)
    return out


def dropped_column_proxies(
    columns: pd.DataFrame,
    y: pd.Series,
    pairs: list,
    *,
    regression: bool,
    n_jobs: int = 8,
    max_columns: int = 50,
    weight: np.ndarray | None = None,
) -> dict:
    """Probe 20, the raw columns the definition drops, each alone against the shipped target (untuned LightGBM, scored
    as ``score``, with the training ``weight`` when the task has one) on ``pairs``: ``columns`` holds them aligned with
    ``y``, row by row of the curated frame.

    A dropped identifier, later measurement or outcome field that scores well alone says what the definition kept out;
    compare it with the kept features alone (``run``). Strings and booleans are scored as categories and a datetime as
    its time stamp; at most ``max_columns`` columns, in the raw table's order. Returns ``{column: score}``, best first
    (None when the fit fails), and ``skipped``, the columns over the limit.
    """
    scores: dict = {}
    for col in list(columns.columns)[:max_columns]:
        x = columns[col]
        if pd.api.types.is_datetime64_any_dtype(x):
            x = (x - x.min()).dt.total_seconds()
        elif not pd.api.types.is_numeric_dtype(x) or pd.api.types.is_bool_dtype(x):
            x = x.astype("string").astype("category")
        try:
            scores[col] = round(score(x.to_frame(), y, pairs, regression=regression, n_jobs=n_jobs, weight=weight), 4)
        except (ValueError, TypeError) as err:  # a column LightGBM cannot read is reported, not fatal
            scores[col] = None
            say(f"dropped column {col}: not scored ({type(err).__name__})")
    ranked = dict(sorted(scores.items(), key=lambda kv: -1.0 if kv[1] is None else -kv[1]))
    return {"scores": ranked, "skipped": max(0, columns.shape[1] - max_columns)}


def raw_copies(raw: pd.DataFrame, target: str | None) -> dict:
    """Probe 21, exact copies in the raw table, before ``_clean`` drops or deduplicates anything: the rows equal in
    every column but the target and the identifiers (a column whose values are all distinct, which would make every
    row unique), their groups, the groups holding more than one label, and the full-row copies.

    Set against probe 5 on the curated frame: copies the definition removed, or the source's own repeats it kept
    (LEAK-16 to LEAK-21).
    """
    has_target = target is not None and target in raw.columns
    inputs = raw.drop(columns=[target]) if has_target else raw
    ids = [c for c in inputs.columns if len(inputs) > 1 and inputs[c].nunique(dropna=False) == len(inputs)]
    inputs = inputs.drop(columns=ids)
    codes = profile_codes(inputs)
    sizes = pd.Series(codes).value_counts()
    repeated = sizes[sizes > 1]
    out: dict = {
        "raw_rows": len(raw),
        "rows_with_input_copy": int(repeated.sum()),
        "copy_groups": len(repeated),
        "identifiers_left_out": ids,
    }
    if has_target:
        labels = raw[target].reset_index(drop=True).astype(str).where(raw[target].reset_index(drop=True).notna())
        several = labels.groupby(codes).nunique(dropna=False)
        out["groups_with_several_labels"] = int((several.reindex(repeated.index) > 1).sum())
        out["full_row_copies"] = int(len(raw) - len(np.unique(profile_codes(raw))))
    return out


def _order_line(order: dict) -> str:
    flag = " - flag" if order["flag"] else ""
    if "next_row_match" in order:
        return (
            f"row order (probe 10), the target in the raw order: next-row label match {order['next_row_match']:.3f} "
            f"against chance {order['chance']:.3f} (z {order['z']:.1f}); largest class-share gap by tenth of the rows "
            f"{order['largest_tenth_gap']:.3f}{flag}"
        )
    return (
        f"row order (probe 10), the target in the raw order: Spearman with the position "
        f"{order['spearman_position']:.3f}, lag-1 autocorrelation {order['lag1_autocorrelation']:.3f}{flag}"
    )


def _removed_line(removed: dict) -> str:
    line = f"rows `_clean` removed (probe 19): {removed['removed']:,} of {removed['raw_rows']:,}"
    if "removed_unlabelled" in removed:
        line += f" ({removed['removed_unlabelled']:,} unlabelled)"
    if "largest_share_gap" in removed:
        line += (
            f"; class shares removed {removed['removed_shares']} against kept {removed['kept_shares']}, "
            f"largest gap {removed['largest_share_gap']:.3f}"
        )
    elif "mean_shift_sd" in removed:
        line += (
            f"; target median removed {removed['removed_median']:.4g} against kept {removed['kept_median']:.4g}, "
            f"mean shift {removed['mean_shift_sd']:+.2f} SD"
        )
    return line + (" - flag" if removed.get("flag") else "")


def _copies_line(copies: dict) -> str:
    line = (
        f"raw copies (probe 21): {copies['rows_with_input_copy']:,} of {copies['raw_rows']:,} rows share their "
        f"inputs with another row, in {copies['copy_groups']:,} groups"
    )
    if copies.get("identifiers_left_out"):
        line += f" (identifiers left out: {copies['identifiers_left_out'][:5]})"
    if "groups_with_several_labels" in copies:
        line += (
            f", {copies['groups_with_several_labels']:,} of them with more than one label; "
            f"{copies['full_row_copies']:,} full-row copies"
        )
    return line


def raw_lines(result: dict) -> list[str]:
    """The report lines of the raw-state probes (``data-foundry probe leak --raw``), from their results by name."""
    lines = []
    if result.get("row_order"):
        lines.append(_order_line(result["row_order"]))
    if result.get("removed_rows"):
        lines.append(_removed_line(result["removed_rows"]))
    dropped = result.get("dropped_columns")
    if dropped:
        top = dict(list(dropped["scores"].items())[:8])
        more = f"; {dropped['skipped']} more not scored" if dropped["skipped"] else ""
        lines.append(f"each dropped raw column alone (probe 20): {top}{more}")
    if result.get("raw_copies"):
        lines.append(_copies_line(result["raw_copies"]))
    return lines
