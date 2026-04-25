"""Dataset Insight Plots

Each function produces one self-contained figure (saved as PDF + PNG)
in the `output_plots/` directory next to this file.
"""

from __future__ import annotations

import ast
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.cm import ScalarMappable
from matplotlib.colors import LogNorm
from matplotlib.offsetbox import (
    AnchoredOffsetbox,
    HPacker,
    TextArea,
    VPacker,
)
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter, LogLocator, NullFormatter

SCRIPT_DIR = Path(__file__).parent
INPUT_CSV = SCRIPT_DIR / "warehouse_metadata.csv"
OUTPUT_DIR = SCRIPT_DIR / "output_plots"

DEFAULT_DOMAIN_COLOR = (0.35, 0.8, 1.0)
DEFAULT_DOMAIN_ALPHA = 0.9
MUTED_GREY = "#6C6C6C"

BRIGHT = sns.color_palette("bright", n_colors=10)
COLORBLIND = sns.color_palette("colorblind", n_colors=10)
FEATURE_TYPE_COLORS = {
    "Numeric": BRIGHT[0],  # blue
    "Categorical": BRIGHT[1],  # orange
    "Binary": BRIGHT[3],
    "Date/Time": BRIGHT[4], # "#FAFF19",
    "Text": BRIGHT[2],
}

FEATURE_PARTS_WITH_BINARY = [
    ("Numeric", "num_numerical_non_binary_cols", FEATURE_TYPE_COLORS["Numeric"]),
    ("Categorical", "num_categorical_non_binary_cols", FEATURE_TYPE_COLORS["Categorical"]),
    ("Binary", "num_binary_cols", FEATURE_TYPE_COLORS["Binary"]),
    ("Date/Time", "num_datetime_non_binary_cols", FEATURE_TYPE_COLORS["Date/Time"]),
    ("Text", "num_text_non_binary_cols", FEATURE_TYPE_COLORS["Text"]),
]

TASK_TYPE_COLORS = {
    "iid": COLORBLIND[0],
    "grouped": COLORBLIND[2],
    "temporal": COLORBLIND[3],
}
TASK_TYPE_LABELS = {
    "iid": "IID",
    "grouped": "Grouped",
    "temporal": "Temporal",
}
TASK_TYPE_ORDER = ["iid", "grouped", "temporal"]

PROBLEM_TYPE_LABELS = {
    "binary_classification": "Binary\nClassification",
    "multiclass_classification": "Multiclass\nClassification",
    "regression": "Regression",
    "other": "Other",
}
PROBLEM_TYPE_ORDER = ["binary_classification", "regression", "multiclass_classification"]


def set_style() -> None:
    sns.set_theme(style="whitegrid", context="paper")
    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 11,
        "axes.titlesize": 13,
        "axes.titleweight": "semibold",
        "axes.labelsize": 11,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "legend.title_fontsize": 10,
        "axes.grid": True,
        "grid.alpha": 0.35,
        "grid.linestyle": "--",
        "grid.linewidth": 0.6,
        "axes.edgecolor": "0.2",
        "axes.linewidth": 0.8,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })


set_style()


def load_data() -> pd.DataFrame:
    df = pd.read_csv(INPUT_CSV)
    duplicates = df["name"].duplicated()
    assert not duplicates.any(), (
        f"Input data has duplicate names: {df.loc[duplicates, 'name'].tolist()}"
    )
    # Hotfix missing metadata
    rossmann = df["name"] == "rossmann_store_sales"
    df.loc[rossmann, "time_horizon"] = 42
    df.loc[rossmann, "time_horizon_unit"] = "days"
    return df


def save_fig(fig: plt.Figure, name: str, subdir: str) -> None:
    out_dir = OUTPUT_DIR / subdir
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf = out_dir / f"{name}.pdf"
    png = out_dir / f"{name}.png"
    fig.savefig(pdf, bbox_inches="tight")
    fig.savefig(png, bbox_inches="tight", dpi=220)
    print(f"Saved: {subdir}/{pdf.name} / {subdir}/{png.name}")
    plt.close(fig)


# ---------------------------------------------------------------------------
# appendix_paper / domain_breakdown
# ---------------------------------------------------------------------------
def plot_domain_breakdown(
    df: pd.DataFrame,
    top_n: int | None = None,
    color: tuple[float, float, float] = DEFAULT_DOMAIN_COLOR,
    alpha: float = DEFAULT_DOMAIN_ALPHA,
) -> None:
    counts = df["domain"].value_counts()
    n_total_domains = counts.shape[0]

    if top_n is not None and top_n < n_total_domains:
        top = counts.head(top_n)
        other = counts.iloc[top_n:]
        top = pd.concat([top, pd.Series({f"Other ({len(other)} domains)": other.sum()})])
    else:
        top = counts

    labels = [
        lbl if lbl.startswith("Other") else lbl.title()
        for lbl in top.index
    ]

    fig, ax = plt.subplots(figsize=(7.0, 4.6))

    sns.barplot(
        x=top.values,
        y=labels,
        ax=ax,
        color=color,
        alpha=alpha,
        edgecolor="white",
        linewidth=0.6,
        orient="h",
    )

    ax.set_xlabel("Number of Datasets")
    ax.set_ylabel("")

    for i, v in enumerate(top.values):
        ax.text(v + max(top.values) * 0.01, i, f"{int(v)}", va="center", ha="left", fontsize=10)

    ax.set_xlim(0, max(top.values) * 1.12)
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", alpha=0.35)

    fig.tight_layout()
    save_fig(fig, name="domain_breakdown", subdir="appendix_paper")
    fig.show()


# ---------------------------------------------------------------------------
# main_paper / feature_type_stack
# ---------------------------------------------------------------------------
def plot_feature_type_stack(
    df: pd.DataFrame,
    feature_parts: list[tuple[str, str, object]] = FEATURE_PARTS_WITH_BINARY,
    sort_by_col: str ="num_numerical_non_binary_cols",
    save_name: str ="feature_type_stack_with_binary",
) -> None:
    order = (df[sort_by_col] / df["num_cols"]).sort_values().index
    shares = pd.DataFrame({
        name: df.loc[order, col] / df.loc[order, "num_cols"]
        for name, col, _ in feature_parts
    }).reset_index(drop=True)
    feature_names = [name for name, _, _ in feature_parts]
    palette = {name: color for name, _, color in feature_parts}

    long_df = (
        shares.reset_index(names="dataset_idx")
        .melt(id_vars="dataset_idx", var_name="feature_type", value_name="share")
    )

    fig, ax = plt.subplots(figsize=(6.0, 4))
    sns.histplot(
        data=long_df,
        x="dataset_idx",
        weights="share",
        hue="feature_type",
        hue_order=feature_names,
        multiple="stack",
        discrete=True,
        palette=palette,
        edgecolor="none",
        legend=False,
        ax=ax,
    )

    n = len(shares)
    ax.set_xlim(-0.5, n - 0.5)
    ax.set_ylim(0, 1)
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(["0%", "25%", "50%", "75%", "100%"])
    ax.set_xticks([])
    ax.set_xlabel("Datasets")
    ax.set_ylabel("Share of columns")

    feature_names = [*feature_names[:-2], feature_names[-1], feature_names[-2]]
    handles = [Patch(facecolor=palette[name], edgecolor="white", label=name)
               for name in feature_names]
    ax.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, -0.28),
              ncol=len(feature_names), frameon=False)
    ax.grid(axis="x", visible=False)

    fig.tight_layout()
    save_fig(fig, name=save_name, subdir="main_paper")
    fig.show()





# ---------------------------------------------------------------------------
# main_paper / dataset_year_timeline
# ---------------------------------------------------------------------------
def plot_dataset_year_timeline(df: pd.DataFrame) -> None:
    d = df.copy()
    d["dataset_year"] = d["dataset_year"].clip(lower=1985, upper=2026)

    year_min = int(d["dataset_year"].min())
    year_max = 2026
    bins = np.arange(year_min, year_max + 2)

    task_order = [t for t in TASK_TYPE_ORDER if t in d["task_type"].unique()]
    palette = {t: TASK_TYPE_COLORS[t] for t in task_order}

    fig, ax = plt.subplots(figsize=(6.0, 4))
    sns.histplot(
        data=d,
        x="dataset_year",
        bins=bins,
        hue="task_type",
        hue_order=list(reversed(task_order)),
        multiple="stack",
        palette=palette,
        edgecolor="white",
        linewidth=0.7,
        legend=False,
        ax=ax,
    )

    ax.set_xlabel("Dataset Release Year")
    ax.set_ylabel("Number of Datasets")
    ax.set_xticks(np.arange(1985, year_max + 1, 5))
    ax.set_xlim(year_min - 0.5, year_max + 1)

    handles = [Patch(facecolor=palette[t], edgecolor="white", label=TASK_TYPE_LABELS[t])
               for t in task_order]
    ax.legend(handles=handles, title="Task Type", loc="upper left", frameon=False)

    fig.tight_layout()
    save_fig(fig, name="dataset_year_timeline", subdir="main_paper")
    fig.show()


# ---------------------------------------------------------------------------
# main_paper / rows_vs_cols_scatter
# ---------------------------------------------------------------------------
def plot_rows_vs_cols_scatter(df: pd.DataFrame) -> None:
    cell_count = df["num_rows"] * df["num_cols"]
    norm = LogNorm(vmin=cell_count.min(), vmax=cell_count.max())
    cmap = sns.color_palette("flare", as_cmap=True)

    log_cells = np.log10(cell_count)
    sizes = 25 + 250 * (log_cells - log_cells.min()) / (log_cells.max() - log_cells.min())

    fig, ax = plt.subplots(figsize=(6, 4))
    sns.scatterplot(
        x=df["num_rows"],
        y=df["num_cols"],
        hue=cell_count,
        palette=cmap,
        hue_norm=norm,
        s=sizes.values,
        alpha=0.85,
        edgecolor="white",
        linewidth=0.6,
        legend=False,
        ax=ax,
    )

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Number of Rows")
    ax.set_ylabel("Number of Columns")

    sm = ScalarMappable(norm=norm, cmap=cmap)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, pad=0.02, fraction=0.045)
    cbar.set_label("Number of Cells", fontsize=10)
    cbar.ax.tick_params(labelsize=9)
    cbar.ax.minorticks_off()

    fig.tight_layout()
    save_fig(fig, name="rows_vs_cols_scatter", subdir="main_paper")
    fig.show()


# ---------------------------------------------------------------------------
# main_paper / dataset_composition_bars
# ---------------------------------------------------------------------------
def plot_dataset_composition_bars(df: pd.DataFrame, top_n_domains: int = 4) -> None:
    rows: list[tuple[str, list[tuple[str, int]]]] = []

    counts_pt = df["problem_type"].value_counts()
    pt_order = [k for k in PROBLEM_TYPE_ORDER if k in counts_pt.index]
    pt_segs = [(PROBLEM_TYPE_LABELS[k], int(counts_pt[k])) for k in pt_order]
    rows.append(("Problem", pt_segs))

    counts_tt = df["task_type"].value_counts()
    tt_order = [k for k in TASK_TYPE_ORDER if k in counts_tt.index]
    tt_segs = [(TASK_TYPE_LABELS[k], int(counts_tt[k])) for k in tt_order]
    rows.append(("Task", tt_segs))

    counts_src = df["source"].value_counts()
    named_src = ["UCI", "Kaggle"]
    named_src = [s for s in named_src if s in counts_src.index]
    others = counts_src.drop(labels=named_src, errors="ignore")
    src_segs: list[tuple[str, int]] = [
        (name, int(counts_src[name])) for name in named_src
    ]
    if len(others) > 0:
        other_label = f"Other\n(OpenML, ...)"
        src_segs.append((other_label, int(others.sum())))
    rows.append(("Source", src_segs))

    counts_dom = df["domain"].value_counts()
    top_dom = counts_dom.head(top_n_domains)
    other_dom = counts_dom.iloc[top_n_domains:]
    dom_segs: list[tuple[str, int]] = [
        (str(name).title().replace("Biology & Life Sciences", "Biology").replace(" & ", "\n& "), int(count))
        for name, count in top_dom.items()
    ]
    if len(other_dom) > 0:
        dom_segs.append((f"Other\n({len(other_dom)} domains)", int(other_dom.sum())))
    rows.append(("Domain", dom_segs))

    cmap = sns.light_palette((0.35, 0.8, 1.0), as_cmap=True)

    norm = plt.Normalize(vmin=0.0, vmax=1.0)

    fig, ax = plt.subplots(figsize=(7, 4))
    y_positions = list(range(len(rows)))[::-1]
    bar_height = 0.9

    for y, (_, segs) in zip(y_positions, rows):
        total = sum(c for _, c in segs)
        left = 0.0
        for seg_label, count in segs:
            frac = count / total
            color = cmap(norm(frac))
            ax.barh(y, frac, left=left, height=bar_height,
                    color=color, edgecolor="white", linewidth=0.8)
            if frac >= 0.05:
                ax.text(
                    left + frac / 2, y + 0.04, seg_label,
                    ha="center", va="bottom",
                    fontsize=8, color="black", fontweight="bold",
                )
                ax.text(
                    left + frac / 2, y - 0.04,
                    f"{count} ({frac * 100:.0f}%)",
                    ha="center", va="top",
                    fontsize=8, color="black", fontweight="medium",
                )
            left += frac

    ax.set_yticks(y_positions)
    ax.set_yticklabels([row_label for row_label, _ in rows], fontsize=11)
    ax.set_xlim(0, 1)
    ax.set_xlabel("Share of Datasets")
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"])
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", alpha=0.25)

    fig.tight_layout()
    save_fig(fig, name="dataset_composition_bars", subdir="main_paper")
    fig.show()


# ---------------------------------------------------------------------------
# appendix_paper / size_boxplots_by_category
# ---------------------------------------------------------------------------
def _colored_axis_label(
    ax: plt.Axes,
    parts: list[tuple[str, object]],
    axis: str = "y",
    separator: str = " / ",
    pad: float = 0.10,
) -> None:
    """Replace an axis label with multi-colored text (used as inline legend)."""
    fontsize = plt.rcParams["axes.labelsize"]
    children: list[TextArea] = []
    for i, (text, color) in enumerate(parts):
        if i > 0:
            children.append(TextArea(separator, textprops=dict(color="0.3", fontsize=fontsize)))
        children.append(TextArea(text, textprops=dict(
            color=color, fontsize=fontsize, fontweight="bold")))

    if axis == "y":
        ax.set_ylabel("")
        box = VPacker(children=children, align="center", pad=0, sep=2)
        anchor = (-pad, 0.5)
    else:
        ax.set_xlabel("")
        box = HPacker(children=children, align="baseline", pad=0, sep=2)
        anchor = (0.5, -pad)

    ab = AnchoredOffsetbox(
        loc="center", child=box, pad=0, frameon=False,
        bbox_to_anchor=anchor, bbox_transform=ax.transAxes, borderpad=0,
    )
    ax.add_artist(ab)


def plot_size_boxplots_by_category(df: pd.DataFrame) -> None:
    metric_labels = {"num_rows": "Rows", "num_cols": "Columns"}
    melted = df.melt(
        id_vars=["domain", "task_type", "problem_type"],
        value_vars=list(metric_labels.keys()),
        var_name="metric",
        value_name="value",
    )
    melted["metric"] = melted["metric"].map(metric_labels)

    palette = {"Rows": BRIGHT[0], "Columns": BRIGHT[1]}
    box_alpha = 0.55
    common_kwargs = dict(
        data=melted, hue="metric", hue_order=["Rows", "Columns"],
        palette=palette, showfliers=False, linewidth=0.8,
    )

    def _soften_boxes(ax: plt.Axes) -> None:
        for patch in ax.patches:
            fc = patch.get_facecolor()
            patch.set_facecolor((fc[0], fc[1], fc[2], box_alpha))

    # --- Domain (two horizontal boxplots: Rows and Columns) ---
    domain_counts = df["domain"].value_counts()
    domain_order = domain_counts.index.tolist()
    domain_labels = [
        f"{str(d).title()}  (n={int(domain_counts[d])})" for d in domain_order
    ]
    domain_palette = sns.color_palette("bright", n_colors=len(domain_order))

    fig, axes = plt.subplots(
        1, 2,
        figsize=(12, max(4.5, 0.42 * len(domain_order) + 1.5)),
        sharey=True,
    )
    for ax, value_col, panel_label in zip(
        axes, ["num_rows", "num_cols"], ["Number of Rows", "Number of Columns"]
    ):
        sns.boxplot(
            data=df, y="domain", x=value_col, order=domain_order,
            hue="domain", palette=domain_palette, orient="h",
            legend=False, showfliers=False, linewidth=0.8, ax=ax,
        )
        _soften_boxes(ax)
        sns.stripplot(
            data=df, y="domain", x=value_col, order=domain_order,
            color="black", alpha=0.6, size=3, jitter=0.25, ax=ax,
        )
        ax.set_xscale("log")
        ax.set_xlabel(f"{panel_label} (log scale)")
        for i in range(len(domain_order) - 1):
            ax.axhline(i + 0.5, color="0.7", linewidth=0.6, linestyle="-", zorder=0)
        ax.grid(axis="y", visible=False)

    axes[0].set_ylabel("Domain")
    axes[0].set_yticks(range(len(domain_labels)))
    axes[0].set_yticklabels(domain_labels)
    axes[1].set_ylabel("")

    fig.tight_layout()
    save_fig(fig, name="size_boxplots_by_domain", subdir="appendix_paper")
    fig.show()

    # --- Task type ---
    task_counts = df["task_type"].value_counts()
    task_order = [t for t in TASK_TYPE_ORDER if t in task_counts.index]
    task_labels = [
        f"{TASK_TYPE_LABELS[t]}\n(n={int(task_counts[t])})" for t in task_order
    ]

    fig, ax = plt.subplots(figsize=(5, 4.4))
    sns.boxplot(x="task_type", y="value", order=task_order,
                ax=ax, **common_kwargs)
    _soften_boxes(ax)
    sns.stripplot(
        data=melted, x="task_type", y="value", order=task_order,
        hue="metric", hue_order=["Rows", "Columns"],
        color="black", dodge=True, size=2.5, alpha=0.6,
        jitter=0.18, edgecolor="none", legend=False, ax=ax,
    )
    ax.set_yscale("log")
    ax.set_xlabel("Task Type")
    ax.set_ylabel("Count")
    ax.set_xticks(range(len(task_labels)))
    ax.set_xticklabels(task_labels)
    for i in range(len(task_order) - 1):
        ax.axvline(i + 0.5, color="0.7", linewidth=0.6, linestyle="-", zorder=0)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(
        handles[:2], labels[:2], title="",
        loc="lower center", bbox_to_anchor=(0.5, 1.02),
        ncol=2, frameon=False,
    )
    ax.grid(axis="x", visible=False)
    fig.tight_layout()
    save_fig(fig, name="size_boxplots_by_task_type", subdir="appendix_paper")
    fig.show()

    # --- Problem type ---
    pt_counts = df["problem_type"].value_counts()
    pt_order = [p for p in PROBLEM_TYPE_ORDER if p in pt_counts.index]
    pt_labels = [
        f"{PROBLEM_TYPE_LABELS[p]}\n(n={int(pt_counts[p])})" for p in pt_order
    ]

    fig, ax = plt.subplots(figsize=(5, 4.4))
    sns.boxplot(x="problem_type", y="value", order=pt_order,
                ax=ax, **common_kwargs)
    _soften_boxes(ax)
    sns.stripplot(
        data=melted, x="problem_type", y="value", order=pt_order,
        hue="metric", hue_order=["Rows", "Columns"],
        color="black", dodge=True, size=2.5, alpha=0.6,
        jitter=0.18, edgecolor="none", legend=False, ax=ax,
    )
    ax.set_yscale("log")
    ax.set_xlabel("Problem Type")
    ax.set_ylabel("Count")
    ax.set_xticks(range(len(pt_labels)))
    ax.set_xticklabels(pt_labels)
    for i in range(len(pt_order) - 1):
        ax.axvline(i + 0.5, color="0.7", linewidth=0.6, linestyle="-", zorder=0)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(
        handles[:2], labels[:2], title="",
        loc="lower center", bbox_to_anchor=(0.5, 1.02),
        ncol=2, frameon=False,
    )
    ax.grid(axis="x", visible=False)
    fig.tight_layout()
    save_fig(fig, name="size_boxplots_by_problem_type", subdir="appendix_paper")
    fig.show()


# ---------------------------------------------------------------------------
# appendix_paper / text_footprint_scatter
# ---------------------------------------------------------------------------
def plot_text_footprint_scatter(df: pd.DataFrame) -> None:
    text_df = df[df["num_text_cols"] > 0].copy()
    text_mean = text_df["text_char_mean"]

    norm = LogNorm(vmin=text_mean.min(), vmax=text_mean.max())
    cmap = sns.color_palette("flare", as_cmap=True)

    log_mean = np.log10(text_mean)
    sizes = 25 + 250 * (log_mean - log_mean.min()) / (log_mean.max() - log_mean.min())

    fig, ax = plt.subplots(figsize=(6, 4))
    sns.scatterplot(
        x=text_df["num_rows"],
        y=text_df["num_text_cols"],
        hue=text_mean,
        palette=cmap,
        hue_norm=norm,
        s=sizes.values,
        alpha=0.85,
        edgecolor="white",
        linewidth=0.6,
        legend=False,
        ax=ax,
    )

    ax.set_xscale("log")
    ax.set_xlabel("Number of Rows")
    ax.set_ylabel("Number of Text Columns")

    sm = ScalarMappable(norm=norm, cmap=cmap)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, pad=0.02, fraction=0.045)
    cbar.set_label("Text Length\n(Average Character Count)", fontsize=10)
    cbar.ax.tick_params(labelsize=9, which="both")

    def _fmt_plain(x: float, _: float) -> str:
        if x >= 1_000_000:
            return f"{x / 1_000_000:g}M"
        if x >= 1_000:
            return f"{x / 1_000:g}k"
        return f"{int(round(x))}"

    cbar.ax.yaxis.set_major_locator(LogLocator(base=10, numticks=15))
    cbar.ax.yaxis.set_major_formatter(FuncFormatter(_fmt_plain))
    cbar.ax.yaxis.set_minor_locator(
        LogLocator(base=10, subs=tuple(range(2, 10)), numticks=15)
    )
    cbar.ax.yaxis.set_minor_formatter(NullFormatter())

    fig.tight_layout()
    save_fig(fig, name="text_footprint_scatter", subdir="appendix_paper")
    fig.show()


# ---------------------------------------------------------------------------
# appendix_paper / categorical_cardinality_distribution
# ---------------------------------------------------------------------------
def plot_categorical_cardinality_distribution(df: pd.DataFrame) -> None:
    cards = (
        df["categorical_non_binary_cardinalities"]
        .apply(ast.literal_eval)
        .explode()
        .dropna()
        .astype(int)
    )

    fig, ax = plt.subplots(figsize=(6, 4))
    sns.histplot(
        x=cards,
        log_scale=True,
        bins=30,
        color=DEFAULT_DOMAIN_COLOR,
        alpha=DEFAULT_DOMAIN_ALPHA,
        edgecolor="white",
        linewidth=0.6,
        ax=ax,
    )

    high_card_threshold = 50
    n_high = int((cards > high_card_threshold).sum())
    pct_high = 100 * n_high / len(cards)
    ax.axvline(high_card_threshold, color="0.25", linestyle="--", linewidth=1.2)
    ax.text(
        high_card_threshold * 1.1, ax.get_ylim()[1] * 0.95,
        f"High cardinality (>{high_card_threshold})\nn={n_high} ({pct_high:.1f}%)",
        ha="left", va="top", fontsize=9, color="0.25",
    )
    ax.set_xlim(3, 1e5)
    ax.set_xticks([3, 10, 100, 1_000, 10_000, 100_000])
    ax.set_xticklabels(["3", "10", "100", "1k", "10k", "100k"])
    ax.set_xlabel(f"Cardinality (n={len(cards)} columns)")
    ax.set_ylabel("Number of Categorical Columns")
    ax.grid(axis="x", visible=False)

    fig.tight_layout()
    save_fig(fig, name="categorical_cardinality_distribution", subdir="appendix_paper")
    fig.show()


# ---------------------------------------------------------------------------
# appendix_paper / time_horizon_unit_pie
# ---------------------------------------------------------------------------
def plot_time_horizon_unit_pie(df: pd.DataFrame) -> None:
    sub = df.dropna(subset=["time_horizon_unit"]).copy()
    stats = (
        sub.groupby("time_horizon_unit")["time_horizon"]
        .agg(count="count", mean="mean")
        .sort_values("count", ascending=False)
    )
    n_total = int(stats["count"].sum())
    palette = sns.color_palette("colorblind", n_colors=len(stats))

    fig, ax = plt.subplots(figsize=(7, 4.5))
    wedges, _ = ax.pie(
        stats["count"].values,
        colors=palette,
        startangle=90,
        counterclock=False,
        wedgeprops=dict(width=0.4, edgecolor="white", linewidth=1.5),
    )
    ax.set_aspect("equal")
    ax.text(0, 0, f"N = {n_total}", ha="center", va="center",
            fontsize=18, fontweight="bold", color="0.2")

    legend_labels = [
        f"{unit}: {int(row['count'])} "
        f"({100 * row['count'] / n_total:.0f}%, avg={row['mean']:.1f})"
        for unit, row in stats.iterrows()
    ]
    ax.legend(
        wedges, legend_labels,
        loc="center left", bbox_to_anchor=(0.9, 0.5),
        frameon=False, handlelength=1.2, handleheight=1.2,
    )

    ax.grid(False)

    fig.tight_layout()
    save_fig(fig, name="time_horizon_unit_pie", subdir="appendix_paper")
    fig.show()


if __name__ == "__main__":
    df = load_data()

    # Main Paper
    plot_feature_type_stack(df)
    plot_dataset_year_timeline(df)
    plot_rows_vs_cols_scatter(df)
    plot_dataset_composition_bars(df)

    # Appendix
    plot_domain_breakdown(df)
    plot_size_boxplots_by_category(df)
    plot_text_footprint_scatter(df)
    plot_categorical_cardinality_distribution(df)
    plot_time_horizon_unit_pie(df)

