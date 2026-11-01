"""Dtype probes: is each column typed by its meaning, a count or a measured quantity numeric and a code categorical?

A count typed categorical loses its order, and its high values become rare levels that preprocessing drops or merges
(bank_marketing's `campaign`, contacts 1-63, shipped as 48 levels); a code typed numeric gets an order it does not
have. The values alone cannot tell the two apart: a label-encoded city and a count of calls are both small integers.
So the probes list the columns where the dtype disagrees with the values, the column's name or the source's codebook,
and the meaning decides (CLEAN-14 of ``cleaning_features.md``). They are tooling-independent: ``column_table`` takes
a pandas frame and, optionally, a codebook (column name -> type and description), and returns one row per categorical
or numeric column:

* ``n_values``; for a categorical column ``numeric_share`` (the share of its levels that are numbers) and
  ``other_levels`` (up to five levels that are not: in a column of counts often proxy missing codes such as `.b` or
  `-3`, CLEAN-10); for the numeric levels or values ``value_min``, ``value_max`` and ``integer``; for numeric levels
  ``rank_corr``, Spearman's rho of each level with how often it occurs: about -1 for a count, whose frequencies fall
  as the value grows.
* ``codebook_type`` and ``codebook_description``: the source's type and words for the column, matched by name (lower
  case, letters and digits only; a codebook name of at least three characters that starts exactly one column's name,
  up to a separator, also matches it, as UCI's `N-073` matches qsar_biodeg's `N073_chemical_substructure`).

Flags, strongest first (``FLAG_ORDER``); "mostly numbers" is a ``numeric_share`` of at least ``MOSTLY``:

* ``quantity_words``: categorical with more than two levels, at least half of them numbers, and the codebook's
  description or the column's name reads like a count or an amount ("number of", "how many", "frequency of",
  "quantity of", "amount of"; name parts such as `num`, `count`, `cnt`, `amount`, `expense`).
* ``codebook_numeric``: categorical, mostly numbers, numeric in the codebook (UCI ``Integer`` or ``Continuous``,
  OpenML ``numeric``). UCI types coded answers as ``Integer`` too (online shoppers' `Browser`, website_phishing's
  -1/0/1 answers), so it is a question, not a verdict.
* ``codebook_categorical``: numeric with more than two values, categorical in the codebook (UCI ``Categorical``,
  OpenML ``nominal``): a code typed as a number, or an ordinal scale or bins typed numeric on purpose.
* ``count_like``: categorical, mostly numbers, at least ``MIN_LEVELS`` integer levels starting at 0 or 1 with every
  integer of the first ``MIN_LEVELS`` present, and ``rank_corr`` at most ``RANK_CORR``. Codes numbered by frequency
  (alfa_battle's label-encoded cities) look the same.
* ``code_name``: numeric with more than two integer values, and a name part that names a code (`id`, `code`, `zip`,
  `postcode`).
* ``numeric_levels``: categorical with more than two levels, mostly numbers, and no stronger flag. Most are codes (zip
  codes, ICD-9 codes, label-encoded ids), but a count whose codebook says nothing plain lands here too: qsar_biodeg's
  `C026` (atom-centred fragments R--CX--R, 0 to 12).

``codebook_from_uci`` and ``codebook_from_openml`` read a codebook from the two APIs' JSON (``fetch_codebook`` gets
it from a source link). An ordinal scale (a grade, binned ranges, survey answers) is no count: it is decided case by
case, categorical by default (CLEAN-14).
"""

from __future__ import annotations

import json
import re
import urllib.request

import numpy as np
import pandas as pd

MIN_LEVELS = 10
RANK_CORR = -0.5
MOSTLY = 0.9
FLAG_ORDER = (
    "quantity_words",
    "codebook_numeric",
    "codebook_categorical",
    "ordinal_like",
    "open_end",
    "count_like",
    "code_name",
    "numeric_levels",
)
QUANTITY_WORDS = re.compile(
    r"\b(numbers? of|counts? of|how many|how much|frequency of|quantity of|amount of|no\. of)\b", re.IGNORECASE
)
QUANTITY_NAME_PARTS = {"nb", "num", "number", "count", "counts", "cnt", "freq", "times", "amount", "qty", "expense"}
CODE_NAME_PARTS = {"id", "code", "zip", "zipcode", "postcode", "postal"}
OPEN_LEVEL = re.compile(
    r"^\s*(<=?|>=?|≤|≥)\s*\$?\d|\d\s*\+\s*$|\d\s*<=?\s*$|\d+\s*plus\b|^(gt|lt|ge|le|less|below|above|over|under)\s*\d"
    r"|\b(or more|and more|or over|and over|or older|and older|more than|less than|fewer than)\b",
    re.IGNORECASE,
)
OPEN_WORDS = re.compile(r"\b(or more|and more|and over|or over|more than|or older|and older)\b", re.IGNORECASE)
RANGE_LEVEL = re.compile(r"^\s*[\[(]?\s*\$?\d[\d,.]*\s*(-|\u2013|~|/|to)\s*\$?\d[\d,.]*\s*[\])%]?\s*$", re.IGNORECASE)
SCALE_WORDS = re.compile(
    r"\b(low|medium|high|none|mild|moderate|severe|never|rarely|seldom|sometimes|often|frequently|always|usually|"
    r"poor|fair|good|excellent|average|slight|minor|major|strongly|agree|disagree|daily|weekly|monthly|primary|"
    r"secondary|tertiary|ex|gd|ta|fa|po)\b",  # the last five: Ames-style quality codes (excellent ... poor)
    re.IGNORECASE,
)
ORDINAL_WORDS = re.compile(r"\b(ordinal|ordered|grade[sd]?|stage|scale|severity|degree)\b", re.IGNORECASE)
NUMERIC_TYPES = {"integer", "continuous", "numeric", "real"}
CATEGORICAL_TYPES = {"categorical", "nominal"}


def _norm(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", str(name).lower())


def _name_parts(name: str) -> set[str]:
    """The parts of a column name, split at non-letters and at camel case (`numCalls` -> num, calls)."""
    spaced = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", str(name))
    return {p for p in re.split(r"[^a-z0-9]+", spaced.lower()) if p}


def _starts_with_name(column: str, key: str) -> bool:
    """Whether ``column``'s letters and digits start with ``key`` and a separator (or the end) follows them."""
    seen = 0
    for i, char in enumerate(str(column).lower()):
        if not char.isalnum():
            continue
        if seen == len(key) or char != key[seen]:
            return seen == len(key) and not str(column)[i - 1].isalnum()
        seen += 1
    return seen == len(key)


def match_codebook(columns: list[str], codebook: dict[str, dict]) -> dict[str, dict]:
    """The codebook entry of each column that has one: the same name once normalised, else a unique prefix."""
    by_norm = {_norm(name): entry for name, entry in codebook.items() if _norm(name)}
    out = {c: by_norm[_norm(c)] for c in columns if _norm(c) in by_norm}
    for key, entry in by_norm.items():
        if len(key) < 3:
            continue
        hits = [c for c in columns if c not in out and _starts_with_name(c, key)]
        if len(hits) == 1:
            out[hits[0]] = entry
    return out


def _level_counts(series: pd.Series) -> tuple[pd.Series, list]:
    """How often each value that is a number occurs, indexed by the value as a float, and the categorical levels that
    are no number.
    """
    counts = series.value_counts(dropna=True)
    counts = counts[counts > 0]
    if not isinstance(series.dtype, pd.CategoricalDtype):
        return pd.Series(counts.to_numpy(), index=np.asarray(counts.index, dtype=float)), []
    values = [_as_number(level) for level in counts.index]  # not pd.to_numeric: it crashed on some string levels
    numbers = [v is not None for v in values]
    others = [level for level, ok in zip(counts.index, numbers, strict=True) if not ok]
    index = np.asarray([v for v in values if v is not None], dtype=float)
    return pd.Series(counts.to_numpy()[numbers], index=index), others


def _as_number(level: object) -> float | None:
    """A category level as a number, or None when it is no finite number."""
    try:
        value = float(level)
    except (TypeError, ValueError):
        return None
    return value if np.isfinite(value) else None


def column_table(
    df: pd.DataFrame, *, exclude: list[str] | tuple[str, ...] = (), codebook: dict[str, dict] | None = None
) -> pd.DataFrame:
    """One row per categorical or numeric column of ``df`` not in ``exclude``, with its flags; see the module."""
    columns = [c for c in df.columns if c not in set(exclude)]
    matched = match_codebook(columns, codebook or {})
    rows = []
    for col in columns:
        s = df[col]
        categorical = isinstance(s.dtype, pd.CategoricalDtype)
        if not categorical and (not pd.api.types.is_numeric_dtype(s) or pd.api.types.is_bool_dtype(s)):
            continue
        entry = matched.get(col, {})
        counts, others = _level_counts(s)
        row = {
            "column": col,
            "dtype": str(s.dtype),
            "n_values": int(s.nunique(dropna=True)),
            "numeric_share": None,
            "other_levels": [str(level) for level in others[:5]],
            "ordered": bool(s.cat.ordered) if categorical else None,
            "open_levels": [str(x) for x in s.cat.categories if OPEN_LEVEL.search(str(x))][:5] if categorical else [],
            "range_levels": sum(bool(RANGE_LEVEL.search(str(x))) for x in s.cat.categories) if categorical else 0,
            "scale_levels": sum(bool(SCALE_WORDS.search(str(x))) for x in s.cat.categories) if categorical else 0,
            "value_min": None,
            "value_max": None,
            "integer": None,
            "rank_corr": None,
            "codebook_type": entry.get("type"),
            "codebook_description": entry.get("description"),
        }
        if categorical:
            row["numeric_share"] = round(len(counts) / max(len(counts) + len(others), 1), 3)
        if len(counts):
            values = pd.Series(counts.index)
            row["value_min"], row["value_max"] = float(values.min()), float(values.max())
            row["integer"] = bool((values == values.round()).all())
            if categorical and len(counts) >= 3:
                rho = values.corr(pd.Series(counts.to_numpy(), dtype=float), method="spearman")
                row["rank_corr"] = None if pd.isna(rho) else round(float(rho), 3)
        row["flags"] = _flags(row, counts, categorical=categorical)
        rows.append(row)
    return pd.DataFrame(rows)


def _flags(row: dict, counts: pd.Series, *, categorical: bool) -> list[str]:
    ctype = str(row["codebook_type"] or "").lower()
    description = str(row["codebook_description"] or "")
    several = row["n_values"] > 2
    if categorical:
        return _categorical_flags(row, counts, ctype, description, several=several)
    flags = []
    if several and ctype in CATEGORICAL_TYPES:
        flags.append("codebook_categorical")
    if several and row["integer"] and _name_parts(row["column"]) & CODE_NAME_PARTS:
        flags.append("code_name")
    return flags


def _categorical_flags(row: dict, counts: pd.Series, ctype: str, description: str, *, several: bool) -> list[str]:
    flags = ["open_end"] if row["open_levels"] or OPEN_WORDS.search(description) else []
    if row["ordered"]:  # typed ordinal on purpose: only an open end is worth naming
        return flags
    levels = row["open_levels"] or row["range_levels"] or row["scale_levels"] >= 2
    if several and (levels or ORDINAL_WORDS.search(description) or OPEN_WORDS.search(description)):
        flags.insert(0, "ordinal_like")
    words = QUANTITY_WORDS.search(description) or _name_parts(row["column"]) & QUANTITY_NAME_PARTS
    mostly = row["numeric_share"] >= MOSTLY
    if several and words and row["numeric_share"] >= 0.5:
        flags.append("quantity_words")
    if several and mostly and ctype in NUMERIC_TYPES:
        flags.append("codebook_numeric")
    if mostly and row["integer"] and len(counts) >= MIN_LEVELS:
        start = row["value_min"]
        head = {start + i for i in range(MIN_LEVELS)}
        if start in (0, 1) and head <= set(counts.index) and (row["rank_corr"] or 0) <= RANK_CORR:
            flags.append("count_like")
    if not flags and several and mostly:
        flags.append("numeric_levels")
    return flags


def flagged(table: pd.DataFrame) -> pd.DataFrame:
    """The rows of ``column_table`` with a flag, strongest flag first."""
    if table.empty:
        return table
    ranked = table.assign(_rank=table["flags"].map(lambda f: min(map(FLAG_ORDER.index, f), default=len(FLAG_ORDER))))
    return ranked[ranked["_rank"] < len(FLAG_ORDER)].sort_values(["_rank", "column"]).drop(columns="_rank")


def codebook_from_uci(payload: dict) -> dict[str, dict]:
    """Column name -> ``{"type", "description"}`` from the UCI API's JSON (``api/dataset?id=<id>``). When the variable
    table has no names (qsar_biodeg), the numbered lines of the free-text variable information are read instead
    ("26) N-073: Ar2NH / Ar3N / Ar2N-Al / R..N..R"), with no type.
    """
    data = payload.get("data") or {}
    out = {}
    for v in data.get("variables") or []:
        name = (v.get("name") or "").strip()
        if name:
            out[name] = {"type": v.get("type"), "description": v.get("description")}
    if not out:
        info = (data.get("additional_info") or {}).get("variable_info") or ""
        for m in re.finditer(r"^\s*\d+\)\s*([^:\n]+?):\s*(.+?)\s*$", info, re.MULTILINE):
            out[m.group(1)] = {"type": None, "description": m.group(2)}
    return out


def codebook_from_openml(payload: dict) -> dict[str, dict]:
    """Column name -> ``{"type", "description"}`` from OpenML's feature list (``api/v1/json/data/features/<id>``)."""
    features = (payload.get("data_features") or {}).get("feature") or []
    return {f["name"]: {"type": f.get("data_type"), "description": None} for f in features}


def codebook_api_url(url: str) -> str | None:
    """The API address of the codebook behind a UCI or OpenML dataset link, or None for another source."""
    m = re.search(r"archive\.ics\.uci\.edu/(?:dataset|static/public)/(\d+)", url)
    if m:
        return f"https://archive.ics.uci.edu/api/dataset?id={m.group(1)}"
    m = re.search(r"openml\.org/(?:d/|search\?.*?\bid=|api/v1/(?:json/)?data/(?:features/)?)(\d+)", url)
    if m:
        return f"https://www.openml.org/api/v1/json/data/features/{m.group(1)}"
    return None


def fetch_codebook(url: str, *, timeout: float = 30) -> dict[str, dict]:
    """The codebook of a UCI or OpenML dataset link (one request), or an empty dict for another source."""
    api = codebook_api_url(url)
    if api is None:
        return {}
    with urllib.request.urlopen(api, timeout=timeout) as response:  # noqa: S310 - a fixed https address
        payload = json.loads(response.read())
    return codebook_from_uci(payload) if "uci.edu" in api else codebook_from_openml(payload)
