"""Convert a v1 curation notebook into a v2 dataset folder: ``dataset.py`` + ``explore.ipynb``.

Usage::

    python scripts/v2/migrate_notebook_to_v2.py datasets/_dev/tabarena-v0pt2/kick/kick.ipynb [--out DIR] [--force]

The conversion is mechanical:

* the ``DatasetMetadata(...)`` / ``PredictiveMLTaskMetadata(...)`` keyword arguments become flat class
  attributes; defaults are left out (the metric of the problem type, stratifying on a classification
  target, the regime data tags) and multi-line text is indented like code;
* the leading ``pd.read_*`` statements of the preprocessing become ``_load_raw``, the rest ``_clean``;
* list-form category casts become ``_feature_types``, and the final ``sample(frac=1, random_state=42)``
  shuffle is dropped (the base class shuffles); column drops stay in ``_clean``;
* a split cell that is the template's recommended IID/grouped split (optionally with
  ``subsample_split_to_budget``) becomes the default split; any other split code becomes ``_make_splits``;
* ``run_bundle_checks(..., ignore=[...])`` entries become ``accepted_check_warnings``;
* display-only and plotting cells move to ``explore.ipynb``.

Anything the script cannot decide is marked with a ``# MIGRATE:`` comment and listed on stdout. Run
``scripts/v2/check_equivalence.py`` afterwards: the migrated definition must give the same curated
content as the notebook.
"""

from __future__ import annotations

import argparse
import ast
import io
import json
import re
import shutil
import subprocess
import sys
import textwrap
import tokenize
from dataclasses import dataclass, field
from pathlib import Path

from data_foundry.schema import resolve_warehouse_dir

REPO = Path(__file__).resolve().parents[2]
TEMPLATE_EXPLORE = REPO / "datasets" / "_template" / "v2" / "explore.ipynb"

BOILERPLATE_MARKERS = ("run_all_checks(", "CuratedContainer(", "verify_saved_container")
DISPLAY_ONLY = re.compile(r"^(#[^\n]*\n)*\s*(df_head|summary|numeric_stats|cat_stats|target_df)\s*$")
READERS = re.compile(r"\b(pd|pl|polars|pandas)\.(read|scan)_\w+\(")
# Later code that depends on a column being categorical: a category cast cannot move past it.
DTYPE_SENSITIVE = re.compile(r"select_dtypes|\.cat\b|\.dtype|dtypes|is_categorical|CategoricalDtype")

DATASET_FIELDS = {
    "unique_name": "unique_name",
    "dataset_year": "year",
    "domain_str": "domain",
    "dataset_source": "source",
    "original_dataset_source_download_link": "source_url",
    "download_description": "download_description",
    "academic_reference_bibtex": "bibtex",
    "academic_reference_bibtex_key": "bibtex_key",
    "license": "license",
    "data_tags": "data_tags",
    "curation_comments": "curation_comments",
    "version_from_unique_name": "version_of",
    "version_comment": "version_comment",
}
TASK_FIELDS = {
    "target_column_name": "target",
    "problem_type": "problem_type",
    "objective_metric_name": "metric",
    "stratify_on": "stratify_on",
    "time_on": "time_on",
    "group_on": "group_on",
    "group_labels": "group_labels",
    "group_time_on": "group_time_on",
}
DEFAULT_METRICS = {"binary_classification": "roc_auc", "multiclass_classification": "log_loss", "regression": "rmse"}
METRIC_ALIASES = {
    "root_mean_squared_error": "rmse",
    "mean_absolute_error": "mae",
    "mean_squared_error": "mse",
    "root_mean_squared_logarithmic_error": "rmsle",
    "mean_absolute_percentage_error": "mape",
}
REGIME_TAGS = {"IID", "Non-IID", "Temporal", "Grouped", "GroupedTemporal"}
_BIBTEX_KEY = re.compile(r"@\w+\s*\{\s*([^,\s}]+)\s*,")


@dataclass
class Migration:
    """The pieces collected from one notebook."""

    unique_name: str = ""
    attrs: dict[str, object] = field(default_factory=dict)
    raw_attrs: dict[str, str] = field(default_factory=dict)  # attributes kept as source (not literals)
    comments: dict[str, str] = field(default_factory=dict)
    load_body: list[str] = field(default_factory=list)
    split_body: list[str] = field(default_factory=list)
    custom_splits: bool = False
    accepted: dict[str, str] = field(default_factory=dict)
    categorical: list[str] = field(default_factory=list)
    explore_cells: list[str] = field(default_factory=list)
    flags: list[str] = field(default_factory=list)


# --- notebook parsing ----------------------------------------------------------------------------------


def _cells(nb: dict) -> list[tuple[str, str, str]]:
    """``(section, cell_type, source)`` per cell; the section is the latest markdown heading."""
    section = "metadata"
    out = []
    for cell in nb["cells"]:
        src = "".join(cell["source"])
        if cell["cell_type"] == "markdown" and src.lstrip().startswith("#"):
            heading = src.strip().lstrip("#").strip().lower()
            for key in (
                "metadata",
                "preprocessing",
                "data checks",
                "task curation",
                "bundle checks",
                "bundle",
                "export",
            ):
                if heading.startswith(key) or (key == "metadata" and "metadata" in heading):
                    section = key
                    break
        out.append((section, cell["cell_type"], src))
    return out


def _string_continuation_lines(src: str) -> set[int]:
    """1-based line numbers that lie inside a multi-line string (after its first line)."""
    inside: set[int] = set()
    try:
        for tok in tokenize.generate_tokens(io.StringIO(src).readline):
            multiline = tok.end[0] > tok.start[0]
            if multiline and tok.type in (tokenize.STRING, getattr(tokenize, "FSTRING_MIDDLE", -1)):
                inside.update(range(tok.start[0] + 1, tok.end[0] + 1))
    except (tokenize.TokenError, IndentationError):
        pass
    return inside


def indent(src: str, prefix: str = "    ") -> str:
    """Indent code, leaving the contents of multi-line strings untouched."""
    keep = _string_continuation_lines(src)
    lines = src.split("\n")
    return "\n".join(line if (i + 1) in keep or not line.strip() else prefix + line for i, line in enumerate(lines))


def _segment(src: str, node: ast.AST) -> str:
    return ast.get_source_segment(src, node, padded=False)


def _kw(call: ast.Call, name: str) -> ast.expr | None:
    return next((k.value for k in call.keywords if k.arg == name), None)


def _names_assigned(tree: ast.AST) -> set[str]:
    names = set()
    for node in ast.walk(tree):
        targets = []
        if isinstance(node, ast.Assign):
            targets = node.targets
        elif isinstance(node, (ast.AugAssign, ast.AnnAssign, ast.For)):
            targets = [node.target]
        elif isinstance(node, ast.Delete):
            targets = node.targets
        for target in targets:
            names.update(sub.id for sub in ast.walk(target) if isinstance(sub, ast.Name))
    return names


def _mutates_df(tree: ast.AST) -> bool:
    if "df" in _names_assigned(tree):
        return True
    return any(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "df"
        and any(k.arg == "inplace" for k in node.keywords)
        for node in ast.walk(tree)
    )


def _definitions_only(tree: ast.Module) -> bool:
    """A cell of imports, assignments and function definitions (reads, lookup maps, helpers), no display."""
    kinds = (ast.Import, ast.ImportFrom, ast.Assign, ast.AnnAssign, ast.FunctionDef)
    if not tree.body or not all(isinstance(node, kinds) for node in tree.body):
        return False
    return not any(
        isinstance(node, ast.Call) and getattr(getattr(node.func, "value", None), "id", None) in ("plt", "sns")
        for node in ast.walk(tree)
    )


def _rewrite_refs(src: str) -> str:
    src = re.sub(r"f\"\{dataset_mold\.path\}/", 'f"{raw_dir}/', src)
    src = src.replace("dataset_mold.path", "raw_dir")
    src = re.sub(r"\bdataset_mold\.", "self.dataset_metadata.", src)
    src = re.sub(r"\btask_mold\.", "self.task_metadata.", src)
    # a file read relative to the notebook's folder: the definition's folder
    src = re.sub(
        r"\b(pd|pl)\.(read_\w+)\(\s*([\"'])([^\"'/{}]+\.(?:csv|tsv|xlsx|xls|parquet|json|txt|gz|zip))\3",
        r"\1.\2(self.folder / \3\4\3",
        src,
    )
    src = re.sub(r"^[ \t]*split_random_state\s*=\s*\d+[^\n]*\n", "", src, flags=re.MULTILINE)
    return re.sub(r"\bsplit_random_state\b", "self.SPLIT_RANDOM_STATE", src)


def _trailing_comments(src: str) -> dict[int, str]:
    """Line number -> the comment at the end of that line."""
    out = {}
    try:
        for tok in tokenize.generate_tokens(io.StringIO(src).readline):
            if tok.type == tokenize.COMMENT and src.split("\n")[tok.start[0] - 1][: tok.start[1]].strip():
                out[tok.start[0]] = tok.string
    except (tokenize.TokenError, IndentationError):
        pass
    return out


def _metadata(m: Migration, src: str) -> None:
    tree = ast.parse(src)
    comments = _trailing_comments(src)
    for node in tree.body:
        if not (isinstance(node, ast.Assign) and isinstance(node.value, ast.Call)):
            continue
        func = getattr(node.value.func, "id", None)
        mapping = (
            DATASET_FIELDS if func == "DatasetMetadata" else TASK_FIELDS if func == "PredictiveMLTaskMetadata" else None
        )
        if mapping is None:
            continue
        for kw in node.value.keywords:
            attr = mapping.get(kw.arg)
            if attr is None:
                m.flags.append(f"metadata field `{kw.arg}` has no v2 attribute")
                continue
            try:
                m.attrs[attr] = ast.literal_eval(kw.value)
            except ValueError:
                m.raw_attrs[attr] = _segment(src, kw.value)
                m.flags.append(f"`{attr}` is not a literal; copied as code")
            for line in range(kw.value.lineno, kw.value.end_lineno + 1):
                if line in comments:
                    m.comments[attr] = comments[line]
    m.unique_name = str(m.attrs.get("unique_name", ""))


# --- preprocessing rewrite -----------------------------------------------------------------------------


def _str_list(node: ast.AST, lists: dict[str, list[str]]) -> list[str] | None:
    if isinstance(node, ast.Name) and node.id in lists:
        return lists[node.id]
    try:
        value = ast.literal_eval(node)
    except ValueError:
        return None
    if isinstance(value, str):
        return [value]
    if isinstance(value, (list, tuple)) and all(isinstance(v, str) for v in value):
        return list(value)
    return None


def _is_df_attr_call(node: ast.AST, attr: str) -> bool:
    return isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == attr


def _category_cast(stmt: ast.stmt, lists: dict[str, list[str]]) -> list[str] | None:  # noqa: PLR0911
    """Columns of ``df[X] = df[X].astype("category")`` (or its for-loop form), else None."""
    if isinstance(stmt, ast.For) and len(stmt.body) == 1 and isinstance(stmt.target, ast.Name):
        cols = _str_list(stmt.iter, lists)
        inner = _category_cast(stmt.body[0], {stmt.target.id: ["<loop>"]})
        return cols if cols is not None and inner == ["<loop>"] else None
    if not (isinstance(stmt, ast.Assign) and len(stmt.targets) == 1 and isinstance(stmt.targets[0], ast.Subscript)):
        return None
    target, value = stmt.targets[0], stmt.value
    if not (getattr(target.value, "id", None) == "df" and _is_df_attr_call(value, "astype")):
        return None
    arg = value.args[0] if value.args else None
    if not (isinstance(arg, ast.Constant) and arg.value == "category"):
        return None
    source = value.func.value
    if not (isinstance(source, ast.Subscript) and getattr(source.value, "id", None) == "df"):
        return None
    if ast.dump(source.slice) != ast.dump(target.slice):
        return None
    return _str_list(target.slice, lists)


def _is_shuffle(stmt: ast.stmt) -> int | None:
    """The seed of ``df = df.sample(frac=1, random_state=S)[.reset_index(drop=True)]``, else None."""
    if not (isinstance(stmt, ast.Assign) and getattr(stmt.targets[0], "id", None) == "df"):
        return None
    node = stmt.value
    if _is_df_attr_call(node, "reset_index"):
        node = node.func.value
    if not _is_df_attr_call(node, "sample"):
        return None
    frac = _kw(node, "frac")
    seed = _kw(node, "random_state")
    if frac is None or ast.literal_eval(frac) != 1 or not isinstance(seed, ast.Constant):
        return None
    if getattr(node.func.value, "id", None) not in ("df", "data"):
        return None
    return seed.value


def _shuffle_source(stmt: ast.Assign) -> str:
    node = stmt.value
    if _is_df_attr_call(node, "reset_index"):
        node = node.func.value
    return node.func.value.id


def _is_noise(stmt: ast.stmt) -> bool:
    """Top-level prints and a bare trailing reset_index."""
    if (
        isinstance(stmt, ast.Expr)
        and isinstance(stmt.value, ast.Call)
        and getattr(stmt.value.func, "id", None) == "print"
    ):
        return True
    return (
        isinstance(stmt, ast.Assign)
        and getattr(stmt.targets[0], "id", None) == "df"
        and _is_df_attr_call(stmt.value, "reset_index")
        and getattr(stmt.value.func.value, "id", None) == "df"
    )


def _rewrite_load(m: Migration, src: str) -> tuple[list[str], str, str]:  # noqa: C901, PLR0912
    """Split the preprocessing into (raw variable names, `_load_raw` code, `_clean` code) and lift declarations."""
    tree = ast.parse(src)
    lines = src.split("\n")
    lists: dict[str, list[str]] = {}
    for stmt in tree.body:
        if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1 and isinstance(stmt.targets[0], ast.Name):
            value = _str_list(stmt.value, {})
            if value is not None and isinstance(stmt.value, (ast.List, ast.Tuple)):
                lists[stmt.targets[0].id] = value

    categorical, used_lists = [], set()
    remove: set[int] = set()
    replace: dict[int, str] = {}
    seeds = []
    # The leading block of imports, literal assignments and `x = pd.read_*(...)` statements: reads go to
    # `_load_raw`, the literal assignments stay at the top of `_clean`.
    reads, read_idx, prefix_literals, _n_prefix = [], [], [], 0
    for i, stmt in enumerate(tree.body):
        if isinstance(stmt, (ast.Import, ast.ImportFrom)):
            read_idx.append(i)
        elif (
            isinstance(stmt, ast.Assign)
            and len(stmt.targets) == 1
            and isinstance(stmt.targets[0], ast.Name)
            and READERS.search(_segment(src, stmt.value))
        ):
            reads.append(stmt.targets[0].id)
            read_idx.append(i)
        elif isinstance(stmt, ast.Assign) and _is_literal(stmt.value):
            prefix_literals.append(i)
        else:
            break
        i + 1
    reads = list(dict.fromkeys(reads))  # `df = read(a); df = concat([df, read(b)])` reads one frame
    if not reads:
        read_idx, prefix_literals, _n_prefix = [], [], 0
    for i, stmt in enumerate(tree.body):
        if i in read_idx:
            continue
        later = "\n".join(_segment(src, s) for s in tree.body[i + 1 :])
        cols = _category_cast(stmt, lists)
        mentioned = cols is not None and any(re.search(rf"[\"']{re.escape(c)}[\"']", later) for c in cols)
        if cols is not None and not mentioned and not DTYPE_SENSITIVE.search(later):
            categorical += cols
            remove.add(i)
            for sub in ast.walk(stmt):
                if isinstance(sub, ast.Name) and sub.id in lists:
                    used_lists.add(sub.id)
            continue
        seed = _is_shuffle(stmt)
        if seed is not None:
            seeds.append(seed)
            source = _shuffle_source(stmt)
            if source == "df":
                remove.add(i)
            else:
                replace[i] = f"df = {source}"
            continue
        if _is_noise(stmt):
            remove.add(i)

    # list variables only used by lifted statements go too
    kept_src = "\n".join(_segment(src, s) for i, s in enumerate(tree.body) if i not in remove and i not in read_idx)
    for i, stmt in enumerate(tree.body):
        if isinstance(stmt, ast.Assign) and getattr(stmt.targets[0], "id", None) in used_lists:
            name = stmt.targets[0].id
            if not re.search(rf"\b{name}\b", kept_src.replace(_segment(src, stmt), "")):
                remove.add(i)

    if seeds and any(s != 42 for s in seeds):
        m.flags.append(f"the v1 shuffle used random_state={seeds}; v2 always shuffles with 42")
    if not seeds and "time_on" not in m.attrs:
        m.flags.append(
            "the v1 notebook did not shuffle; v2 shuffles IID/grouped data (set `shuffle = False` if the order matters)"
        )
    regression = m.attrs.get("problem_type") == "regression"
    m.categorical = [c for c in dict.fromkeys(categorical) if c != m.attrs.get("target") or regression]

    def body(indices: list[int]) -> str:
        out = []
        for i in indices:
            stmt = tree.body[i]
            start = min([d.lineno for d in getattr(stmt, "decorator_list", [])] + [stmt.lineno])
            # keep comment lines directly above the statement
            while start > 1 and lines[start - 2].strip().startswith("#"):
                start -= 1
            out.append(replace[i] if i in replace else "\n".join(lines[start - 1 : stmt.end_lineno]))
        return "\n".join(out)

    # literal assignments the reads use (column names, dtypes) go to `_load_raw` as well
    read_src = "\n".join(_segment(src, tree.body[i]) for i in read_idx)
    needed = [
        i
        for i in prefix_literals
        if isinstance(tree.body[i].targets[0], ast.Name)
        and re.search(rf"\b{re.escape(tree.body[i].targets[0].id)}\b", read_src)
    ]
    load_code = body(sorted({*read_idx, *needed}))
    clean_code = body([i for i in range(len(tree.body)) if i not in remove and i not in read_idx])
    return reads, load_code, clean_code


def _is_literal(node: ast.AST) -> bool:
    try:
        ast.literal_eval(node)
    except ValueError:
        return False
    return True


# --- splits --------------------------------------------------------------------------------------------


def _is_default_split(src: str) -> bool:
    if not re.search(r"get_recommended_(iid|grouped)_splits\(", src):
        return False
    if re.search(r"^\s*df\s*=", src, flags=re.MULTILINE) and "subsample_split_to_budget" not in src:
        return False
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Call) and isinstance(node.func, (ast.Name, ast.Attribute)):
            fname = node.func.id if isinstance(node.func, ast.Name) else node.func.attr
            if fname in ("get_recommended_iid_splits", "get_recommended_grouped_splits"):
                expected = {
                    "dataset": "df",
                    "n_repeats": "n_repeats",
                    "n_splits": "n_splits",
                    "test_size": "none_or_test_size",
                }
                for arg, want in expected.items():
                    got = _kw(node, arg)
                    if got is None or ast.unparse(got) != want:
                        return False
                for arg in ("stratify_on", "group_on", "group_labels"):
                    got = _kw(node, arg)
                    if got is not None and ast.unparse(got) != f"task_mold.{arg}":
                        return False
    return True


def _splits_metadata_call(src: str) -> ast.Call | None:
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Call) and getattr(node.func, "id", None) == "PredictiveMLSplitsMetadata":
            return node
    return None


def _split_attrs(m: Migration, call: ast.Call, *, default: bool) -> None:
    for kw in ("time_horizon", "time_horizon_unit"):
        value = _kw(call, kw)
        if value is not None:
            try:
                literal = ast.literal_eval(value)
            except ValueError:
                m.flags.append(f"`{kw}` is not a literal ({ast.unparse(value)}); set it by hand")
                continue
            if literal is not None:
                m.attrs[kw] = int(literal) if kw == "time_horizon" and str(literal).isdigit() else literal
    comment = _kw(call, "splits_comment")
    if isinstance(comment, ast.Constant):
        text = str(comment.value).strip()
        if not (default and (text.startswith(("Default splits", "Recommended single")))):
            m.attrs["splits_comment"] = text


def _custom_split_body(src: str, call: ast.Call) -> str:
    """Replace the ``splits_mold = PredictiveMLSplitsMetadata(...)`` statement by a ``return SplitPlan``."""
    tree = ast.parse(src)
    stmt = next(n for n in tree.body if n.lineno <= call.lineno and call.end_lineno <= n.end_lineno)
    splits_expr = _kw(call, "splits")
    comment = _kw(call, "splits_comment")
    args = [f"splits={ast.unparse(splits_expr) if splits_expr is not None else 'splits'}", "df=df"]
    if comment is not None and not isinstance(comment, ast.Constant):
        args.append(f"comment={_segment(src, comment)}")
    lines = src.split("\n")
    before = "\n".join(lines[: stmt.lineno - 1])
    after = "\n".join(lines[stmt.end_lineno :])
    return "\n".join(part for part in (before, after) if part.strip()) + f"\nreturn SplitPlan({', '.join(args)})"


def _accepted(m: Migration, src: str) -> None:
    match = re.search(r"ignore=\[(.*?)\]", src, flags=re.DOTALL)
    if not match:
        return
    for line in match.group(1).split("\n"):
        slug = re.search(r"[\"']([a-z0-9_]+)[\"']", line)
        if slug:
            reason = line.split("#", 1)[1].strip() if "#" in line else ""
            m.accepted[slug.group(1)] = reason or "MIGRATE: state the reason"
            if not reason:
                m.flags.append(f"accepted warning `{slug.group(1)}` has no reason")


def migrate(nb_path: Path) -> Migration:  # noqa: C901, PLR0912 - one branch per cell kind
    """Collect the v2 pieces from one notebook."""
    nb = json.loads(nb_path.read_text())
    m = Migration()
    pending_split: list[str] = []
    for section, cell_type, src in _cells(nb):
        if cell_type != "code" or not src.strip():
            continue
        if any(line.lstrip().startswith(("%", "!")) for line in src.split("\n")):
            m.flags.append("a cell uses IPython magics; moved to explore.ipynb")
            m.explore_cells.append(src)
            continue
        if section == "metadata" and ("DatasetMetadata(" in src or "PredictiveMLTaskMetadata(" in src):
            _metadata(m, src)
            continue
        if "run_bundle_checks(" in src:
            _accepted(m, src)
            continue
        if DISPLAY_ONLY.match(src) or any(marker in src for marker in BOILERPLATE_MARKERS):
            continue
        tree = ast.parse(src)
        if section in ("preprocessing", "data checks"):
            (m.load_body if _mutates_df(tree) or _definitions_only(tree) else m.explore_cells).append(src)
            continue
        if section == "task curation":
            is_dims = "get_recommended_splits_dimensions" in src and "PredictiveMLSplitsMetadata(" not in src
            defines = any(isinstance(n, ast.FunctionDef) for n in tree.body)
            if is_dims or "PredictiveMLSplitsMetadata(" in src or defines or _mutates_df(tree):
                pending_split.append(src)
            else:
                m.explore_cells.append(src)
            continue
        m.flags.append(f"unclassified code cell in section {section!r}; moved to explore.ipynb")
        m.explore_cells.append(src)

    split_cells = [s for s in pending_split if "PredictiveMLSplitsMetadata(" in s]
    if len(split_cells) != 1:
        m.flags.append(f"expected one split cell, found {len(split_cells)}")
        return m
    split_src = split_cells[0]
    call = _splits_metadata_call(split_src)
    others = [s for s in pending_split if s is not split_src and "get_recommended_splits_dimensions" not in s]
    default = _is_default_split(split_src) and not others
    _split_attrs(m, call, default=default)
    if default:
        if "subsample_split_to_budget(" in split_src and not re.search(r"^#\s*df, train_idx", split_src, re.MULTILINE):
            m.attrs["subsample_to_budget"] = True
    else:
        m.custom_splits = True
        m.split_body += [s for s in pending_split if s is not split_src]
        m.split_body.append(_custom_split_body(split_src, call))
    return m


# --- rendering -----------------------------------------------------------------------------------------


def _class_name(unique_name: str) -> str:
    name = "".join(part.capitalize() for part in unique_name.split("_"))
    return name if name[:1].isalpha() else f"Dataset{name}"


def _render_value(value: object, level: str = "    ") -> str:
    """Python source for an attribute value; long or multi-line text becomes an indented triple-quoted block."""
    if isinstance(value, str) and ("\n" in value or len(value) > 90):
        body = textwrap.indent(textwrap.dedent(value.strip("\n")), level + "    ")
        body = "\n".join(line.rstrip() for line in body.split("\n"))
        if '"""' in value or body.endswith("\\"):
            return repr(value)
        prefix = "r" if "\\" in value else ""
        return f'{prefix}"""\n{body}\n{level}"""'
    if isinstance(value, list):
        return repr(tuple(value))
    return repr(value)


def _normalise_attrs(m: Migration) -> None:  # noqa: C901, PLR0912
    a = m.attrs
    problem = a.get("problem_type")
    metric = a.get("metric")
    if isinstance(metric, str):
        canonical = METRIC_ALIASES.get(metric.strip().lower(), metric.strip())
        if canonical.lower() in {*DEFAULT_METRICS.values(), "mae", "mse", "rmsle", "mape", "r2"}:
            canonical = canonical.lower()
        a["metric"] = canonical
        if canonical == DEFAULT_METRICS.get(problem):
            del a["metric"]
    classification = problem != "regression"
    if "stratify_on" in a and a["stratify_on"] == (a.get("target") if classification else None):
        del a["stratify_on"]
    for key in ("time_on", "group_on", "group_labels", "group_time_on", "version_of", "version_comment"):
        if key in a and a[key] is None:
            del a[key]
    tags = list(a.get("data_tags", ()))
    if "time_on" in a:
        regime = ["Non-IID", "Temporal"]
    elif "group_on" in a:
        regime = ["Non-IID", "GroupedTemporal" if "group_time_on" in a else "Grouped"]
    else:
        regime = ["IID"]
    if sorted(t for t in tags if t in REGIME_TAGS) == sorted(regime):
        tags = [t for t in tags if t not in REGIME_TAGS]
    a["data_tags"] = tuple(tags)
    if not a["data_tags"]:
        del a["data_tags"]
    bibtex, key = a.get("bibtex"), a.get("bibtex_key")
    if isinstance(bibtex, str) and isinstance(key, str):
        parsed = ",".join(dict.fromkeys(_BIBTEX_KEY.findall(bibtex)))
        if parsed.replace(" ", "") == key.replace(" ", ""):
            del a["bibtex_key"]


ORDER = (
    (
        "# Dataset",
        (
            "unique_name",
            "version_of",
            "version_comment",
            "raw_data_from",
            "year",
            "domain",
            "source",
            "source_url",
            "license",
            "data_tags",
            "download_description",
            "bibtex",
            "bibtex_key",
            "curation_comments",
        ),
    ),
    (
        "# Task",
        ("target", "problem_type", "metric", "stratify_on", "time_on", "group_on", "group_labels", "group_time_on"),
    ),
    ("# Splits", ("splits_comment", "time_horizon", "time_horizon_unit", "subsample_to_budget")),
)


def _function(header: str, parts: list[str], ret: str | None) -> tuple[str, list[str], list[str]]:
    imports, helpers, code = [], [], []
    for part in parts:
        tree = ast.parse(part)
        drop = set()
        for node in tree.body:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                imports.append(_segment(part, node))
                drop.update(range(node.lineno, node.end_lineno + 1))
        rest = "\n".join(line for i, line in enumerate(part.split("\n"), start=1) if i not in drop).strip("\n")
        if rest.strip():
            code.append(_rewrite_refs(rest))
    body = "\n\n".join(code)
    if "raw_dir: Path" not in header:
        # a read further down in the preprocessing: `raw_dir` is a property outside `_load_raw`
        body = re.sub(r"(?<![\w.])raw_dir\b", "self.raw_dir", body)
    if ret:
        body += f"\n{ret}"
    return header + "\n" + indent(body.strip("\n") or "pass"), imports, helpers


def render_definition(m: Migration) -> str:  # noqa: C901, PLR0912 - one branch per optional part
    """Render ``dataset.py`` text for a migration."""
    load_src = "\n\n".join(m.load_body)
    reads, load_code, clean_code = _rewrite_load(m, load_src) if load_src.strip() else ([], "", "")
    _normalise_attrs(m)

    methods, imports, helpers = [], [], []
    if reads:
        ret = f"return {reads[0]}" if len(reads) == 1 else "return {" + ", ".join(f'"{r}": {r}' for r in reads) + "}"
        fn, imp, hel = _function("def _load_raw(self, raw_dir: Path) -> pd.DataFrame:", [load_code], ret)
        methods.append(fn)
        imports += imp
        helpers += hel
        unpack = (
            f"{reads[0]} = raw"
            if len(reads) == 1
            else ", ".join(reads) + " = " + ", ".join(f'raw["{r}"]' for r in reads)
        )
        if clean_code.strip() or reads[0] != "df":
            ret = "return df"
            fn, imp, hel = _function(
                "def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:", [unpack + "\n" + clean_code], ret
            )
            if len(reads) > 1:
                fn = fn.replace("raw: pd.DataFrame", "raw: dict[str, pd.DataFrame]", 1)
            methods.append(fn)
            imports += imp
            helpers += hel
    else:
        m.flags.append("no leading read statement found; everything is in `_load_raw`")
        fn, imp, hel = _function("def _load_raw(self, raw_dir: Path) -> pd.DataFrame:", [clean_code], "return df")
        methods.append(fn)
        imports += imp
        helpers += hel
    if m.categorical:
        cols = "".join(f"\n        {c!r}," for c in m.categorical)
        methods.append(
            "def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:\n"
            f"    return FeatureTypes(\n        categorical=[{cols}\n        ],\n    )"
        )
    if m.custom_splits:
        fn, imp, hel = _function("def _make_splits(self, df: pd.DataFrame) -> SplitPlan:", m.split_body, None)
        methods.append(fn)
        imports += imp
        helpers += hel

    lines = [f'"""Curated dataset definition for `{m.unique_name}` (data-foundry v2). Evidence: report.md."""', ""]
    lines += ["from __future__ import annotations", "", "from pathlib import Path", "", "import pandas as pd"]
    seen = set()
    for imp in imports:
        if imp in seen or any(
            x in imp for x in ("matplotlib", "seaborn", "PredictiveMLSplitsMetadata", "import pandas as pd")
        ):
            continue
        seen.add(imp)
        lines.append(imp)
    v2_names = ["AbstractCuratedDataset"]
    v2_names += (["FeatureTypes"] if m.categorical else []) + (["SplitPlan"] if m.custom_splits else [])
    lines += [f"from data_foundry.v2 import {', '.join(v2_names)}", "", ""]
    for helper in dict.fromkeys(helpers):
        lines += [helper, "", ""]

    lines.append(f"class {_class_name(m.unique_name)}(AbstractCuratedDataset):")
    for title, keys in ORDER:
        block = [k for k in keys if k in m.attrs or k in m.raw_attrs]
        if not block:
            continue
        lines.append(f"    {title}")
        for key in block:
            value = m.raw_attrs[key] if key in m.raw_attrs else _render_value(m.attrs[key])
            comment = f"  {m.comments[key]}" if key in m.comments else ""
            lines.append(f"    {key} = {value}{comment}")
        lines.append("")
    if m.accepted:
        lines.append("    accepted_check_warnings = {")
        lines += [f"        {k!r}: {v!r}," for k, v in m.accepted.items()]
        lines += ["    }", ""]
    for method in methods:
        lines += [indent(method), ""]
    text = "\n".join(lines).rstrip() + "\n"
    if m.flags:
        text += "\n" + "\n".join(f"# MIGRATE: {flag}" for flag in dict.fromkeys(m.flags)) + "\n"
    return text


def render_explore(m: Migration) -> dict:
    """Render ``explore.ipynb``: the template's cells plus the notebook's exploratory cells."""
    nb = json.loads(TEMPLATE_EXPLORE.read_text())
    for cell in nb["cells"]:
        cell["source"] = [line.replace("<unique_name>", m.unique_name) for line in cell["source"]]
    if m.explore_cells:
        heading = next(i for i, c in enumerate(nb["cells"]) if "".join(c["source"]).startswith("## Exploration"))
        nb["cells"][heading] = _md("## Exploration\n\nMigrated from the v1 notebook; adapt the cells where needed.")
        new = [_code("df = ds.df.copy()  # the migrated cells below work on `df`")] + [
            _code(src.replace("dataset_mold.path", "ds.raw_dir").replace("task_mold.", "ds.task_metadata."))
            for src in m.explore_cells
        ]
        nb["cells"][heading + 1 : heading + 2] = new
    for i, cell in enumerate(nb["cells"]):
        cell["id"] = f"cell-{i}"
    return nb


def _lines(src: str) -> list[str]:
    lines = src.split("\n")
    return [line + "\n" for line in lines[:-1]] + [lines[-1]]


def _md(src: str) -> dict:
    return {"cell_type": "markdown", "id": "", "metadata": {}, "source": _lines(src)}


def _code(src: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": "",
        "metadata": {},
        "outputs": [],
        "source": _lines(src),
    }


def main(argv: list[str] | None = None) -> int:  # noqa: C901 - one branch per output step
    """Convert one notebook; see the module docstring."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("notebook", type=Path)
    parser.add_argument("--out", type=Path, help="Target folder (default: <notebook folder>/../<unique_name>).")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing dataset.py.")
    parser.add_argument(
        "--move", action="store_true", help="Move the notebook and its sibling files into a renamed folder."
    )
    args = parser.parse_args(argv)

    m = migrate(args.notebook)
    if not m.unique_name:
        print("No DatasetMetadata(unique_name=...) found.", file=sys.stderr)
        return 1
    out = args.out or args.notebook.parent.parent / m.unique_name
    out.mkdir(parents=True, exist_ok=True)
    warehouse = resolve_warehouse_dir()
    if not (warehouse / m.unique_name).exists() and "version_of" not in m.attrs:
        base = next(
            (d.name for d in sorted(warehouse.iterdir()) if d.is_dir() and m.unique_name.startswith(d.name + "_")),
            None,
        )
        if base is not None:
            m.attrs["raw_data_from"] = base
            m.flags.append(f"no warehouse folder `{m.unique_name}`; reading the raw files of `{base}` (raw_data_from)")
    definition = out / "dataset.py"
    if definition.exists() and not args.force:
        print(f"{definition} exists; pass --force to overwrite.", file=sys.stderr)
        return 1
    definition.write_text(render_definition(m))
    ruff = Path(sys.executable).parent / "ruff"
    for cmd in ([str(ruff), "check", "--fix", "-q", str(definition)], [str(ruff), "format", "-q", str(definition)]):
        subprocess.run(cmd, check=False, capture_output=True)  # noqa: S603 - the repo's own ruff on the new file
    (out / "explore.ipynb").write_text(json.dumps(render_explore(m), indent=1, ensure_ascii=False) + "\n")
    if args.move and out.resolve() != args.notebook.parent.resolve():
        # a renamed dataset (`<name>_1m`): take the v1 notebook and its sibling files along
        for item in sorted(args.notebook.parent.iterdir()):
            if item.suffix == ".ipynb" and item != args.notebook:
                continue
            shutil.move(str(item), out / item.name)
        if not any(args.notebook.parent.iterdir()):
            args.notebook.parent.rmdir()
    print(f"Wrote {definition} and {out / 'explore.ipynb'}")
    print(f"  splits: {'custom _make_splits' if m.custom_splits else 'default'}; explore cells: {len(m.explore_cells)}")
    for flag in dict.fromkeys(m.flags):
        print(f"  MIGRATE: {flag}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
