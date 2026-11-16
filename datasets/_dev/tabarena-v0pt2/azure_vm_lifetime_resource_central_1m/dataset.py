"""Curated dataset definition for `azure_vm_lifetime_resource_central_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import polars as pl
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    RowBudget,
    TaskSummary,
    Temporal,
    TemporalSplits,
)

# The trace's clock: seconds since its start, in steps of one 5-minute CPU reading (`vmcreated`, `vmdeleted`).
SLOT = 300
DAY = 86_400
# A VM is in the top class (over 24 h) once it has a reading 86,700 s after its creation; that reading is known one
# slot later, so the longest a lifetime class takes to be known is 87,000 s (24 h 10 min) after creation.
CLASS_KNOWN_WITHIN = DAY + 2 * SLOT
# The lifetime classes of Resource Central (Cortez et al. 2017, Table 3), shortest first.
LIFETIME_CLASSES = ["up to 15 min", "15 to 60 min", "1 to 24 h", "over 24 h"]
LIFETIME_EDGES = [0, 15 * 60, 3600, DAY, np.inf]
SHARE_COLUMNS = [
    "subscription_share_up_to_15min",
    "subscription_share_15_to_60min",
    "subscription_share_1_to_24h",
    "subscription_share_over_24h",
]
VMTABLE_COLUMNS = [
    "vm_id",
    "subscription_id",
    "deployment_id",
    "created",
    "deleted",
    "max_cpu",
    "avg_cpu",
    "p95_max_cpu",
    "vm_category",
    "core_bucket",
    "memory_bucket",
]
# Test windows: 864 five-minute slots (3 days). The last training slot is 24 h 10 min before a window's first slot, so
# the 289 slots between them (24 h 5 min) are the gap.
WINDOW_SLOTS = 864
GAP_SLOTS = 289


def _lifetime_class(seconds: pl.Expr) -> pl.Expr:
    return (
        pl.when(seconds <= 15 * 60)
        .then(pl.lit(LIFETIME_CLASSES[0]))
        .when(seconds <= 3600)
        .then(pl.lit(LIFETIME_CLASSES[1]))
        .when(seconds <= DAY)
        .then(pl.lit(LIFETIME_CLASSES[2]))
        .otherwise(pl.lit(LIFETIME_CLASSES[3]))
    )


def _asof_sums(rows: pl.DataFrame, events: pl.DataFrame, by: str, values: list[str], prefix: str) -> pl.DataFrame:
    """Add, per row, the sums of `values` over the events of its `by` key whose time `t` is at or before the row's."""
    cumulative = (
        events.sort([by, "t"], maintain_order=True)
        .group_by([by, "t"], maintain_order=True)
        .agg([pl.col(c).sum() for c in values])
        .with_columns([pl.col(c).cum_sum().over(by).alias(c) for c in values])
        .sort(["t", by], maintain_order=True)
    )
    out = rows.sort(["t", by], maintain_order=True).join_asof(
        cumulative, on="t", by=by, strategy="backward", check_sortedness=False
    )
    return out.with_columns([pl.col(c).fill_null(0).alias(f"{prefix}{c}") for c in values]).drop(values)


def _history_features(vm: pl.DataFrame, trace_end: int) -> pl.DataFrame:
    """One row per VM created inside the trace whose class is known at its end, with what was known at creation.

    Every count and share uses only VMs whose state was known at the row's creation slot `t`: a VM counts as created
    from the slot after its creation, as ended from the slot after its `deleted` time, and its lifetime class as known
    from `min(deleted + 300, created + 87,000)`. No VM created in the row's own slot enters a feature. VMs running
    when the trace starts (`created == 0`) count as running and, once 24 h 10 min have passed while they still ran,
    as over 24 h; their true creation time is unknown, so the 24-hour creation count is missing on the first day of a
    subscription that has them.
    """
    vm = vm.with_columns(
        pl.max_horizontal(pl.col("deleted") - pl.col("created"), pl.lit(SLOT)).alias("lifetime_seconds"),
        (pl.col("created") == 0).alias("before_trace"),
    )
    vm = vm.with_columns(
        _lifetime_class(pl.col("lifetime_seconds")).alias("lifetime_class"),
        pl.when(~pl.col("before_trace"))
        .then(pl.min_horizontal(pl.col("deleted") + SLOT, pl.col("created") + CLASS_KNOWN_WITHIN))
        .when(pl.col("deleted") >= CLASS_KNOWN_WITHIN - SLOT)
        .then(pl.lit(CLASS_KNOWN_WITHIN))
        .otherwise(None)
        .alias("class_known_at"),
    )
    vm = vm.with_columns(
        pl.when(pl.col("before_trace"))
        .then(pl.lit(LIFETIME_CLASSES[3]))
        .otherwise(pl.col("lifetime_class"))
        .alias("history_class")
    )
    rows = vm.filter((pl.col("created") > 0) & (pl.col("created") <= trace_end - (DAY + SLOT)))
    feats = rows.select("vm_id", "subscription_id", "deployment_id", pl.col("created").alias("t"))
    # The deployment's VMs created in the previous slot (t - 300), all known at t. The same slot's VMs are not counted:
    # the trace cannot order VMs within a slot, so they may arrive after this one.
    prev_slot = (
        vm.filter(~pl.col("before_trace"))
        .group_by(["deployment_id", "created"], maintain_order=True)
        .len()
        .select("deployment_id", (pl.col("created") + SLOT).alias("t"), pl.col("len").alias("deployment_vms_prev_slot"))
    )
    feats = feats.join(prev_slot, on=["deployment_id", "t"], how="left").with_columns(
        pl.col("deployment_vms_prev_slot").fill_null(0)
    )
    pre_trace_subscriptions = vm.filter(pl.col("before_trace"))["subscription_id"].unique().to_list()
    created_events = vm.select(
        "subscription_id", "deployment_id", (pl.col("created") + SLOT).alias("t"), pl.lit(1).alias("n")
    )
    ended_events = vm.select(
        "subscription_id",
        "deployment_id",
        (pl.col("deleted") + SLOT).alias("t"),
        pl.lit(1).alias("n"),
        pl.col("avg_cpu").alias("avg_cpu_sum"),
        pl.col("p95_max_cpu").alias("p95_sum"),
    )
    aged_events = vm.select("subscription_id", (pl.col("created") + DAY).alias("t"), pl.lit(1).alias("n"))
    class_events = vm.filter(pl.col("class_known_at").is_not_null()).select(
        "subscription_id",
        pl.col("class_known_at").alias("t"),
        *[(pl.col("history_class") == c).cast(pl.Int64).alias(f"c{i}") for i, c in enumerate(LIFETIME_CLASSES)],
    )
    feats = _asof_sums(feats, created_events, "subscription_id", ["n"], "sub_created_")
    feats = _asof_sums(feats, ended_events, "subscription_id", ["n", "avg_cpu_sum", "p95_sum"], "sub_ended_")
    feats = _asof_sums(feats, aged_events, "subscription_id", ["n"], "sub_aged_")
    feats = _asof_sums(feats, created_events, "deployment_id", ["n"], "dep_created_")
    feats = _asof_sums(feats, ended_events, "deployment_id", ["n"], "dep_ended_")
    feats = _asof_sums(feats, class_events, "subscription_id", [f"c{i}" for i in range(4)], "sub_known_")
    known = sum(pl.col(f"sub_known_c{i}") for i in range(4))
    ended = pl.col("sub_ended_n")
    feats = feats.select(
        "vm_id",
        "deployment_vms_prev_slot",
        pl.col("dep_created_n").alias("deployment_vms_before"),
        (pl.col("dep_created_n") - pl.col("dep_ended_n")).alias("deployment_vms_running"),
        (pl.col("sub_created_n") - pl.col("sub_ended_n")).alias("subscription_vms_running"),
        pl.when((pl.col("t") < DAY) & pl.col("subscription_id").is_in(pre_trace_subscriptions))
        .then(None)
        .otherwise(pl.col("sub_created_n") - pl.col("sub_aged_n"))
        .alias("subscription_vms_created_24h"),
        known.alias("subscription_vms_class_known"),
        *[
            pl.when(known > 0).then(pl.col(f"sub_known_c{i}") / known).otherwise(None).alias(name)
            for i, name in enumerate(SHARE_COLUMNS)
        ],
        pl.when(ended > 0)
        .then(pl.col("sub_ended_avg_cpu_sum") / ended)
        .otherwise(None)
        .alias("subscription_mean_avg_cpu"),
        pl.when(ended > 0)
        .then(pl.col("sub_ended_p95_sum") / ended)
        .otherwise(None)
        .alias("subscription_mean_p95_max_cpu"),
    )
    # Causal: the previous slot's VMs are among the deployment's VMs created before t, which are known at t.
    assert (feats["deployment_vms_prev_slot"] <= feats["deployment_vms_before"]).all()
    out = rows.select("vm_id", "created", "deleted", "core_bucket", "memory_bucket", "lifetime_class").join(
        feats, on="vm_id", how="left"
    )
    return out.sort(["created", "vm_id"], maintain_order=True)


def _observed_class(created: pd.Series, deleted: pd.Series) -> pd.Series:
    """The lifetime class as the trace shows it (cut short for a VM running at its start or end)."""
    return pd.cut(np.maximum(deleted - created, SLOT), LIFETIME_EDGES, labels=LIFETIME_CLASSES)


class AzureVmLifetimeResourceCentral1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "When a virtual machine is created in Azure, how long will it live: up to 15 minutes, up to an hour, up "
            "to a day, or longer?"
        ),
        use_case=(
            "Azure's VM scheduler can ask Resource Central for each new VM's lifetime class when it places the VM, to "
            "put VMs that end at about the same time on the same servers and to plan maintenance (Cortez et al., "
            "SOSP 2017, Sec. 4.1), as Azure's allocator later did (Barbalho et al., MLSys 2023)."
        ),
        row=(
            "One VM created in a 30-day trace of first-party Azure VMs in one region in 2019 (Azure Public Dataset "
            "V2), from its first 29 days, so every row's class is known by the trace's end."
        ),
        predicted="The VM's lifetime class, from its creation to its deletion: the four classes of Resource Central.",
        known=(
            "The VM's core and memory size class, the time of creation, how many VMs its deployment (the "
            "subscription's VMs in the region that day) created in the previous 5 minutes and before and still runs, "
            "how many VMs the subscription runs and created in the last 24 hours, and the lifetime classes and CPU use "
            "of the subscription's earlier VMs."
        ),
        split=(
            "Each of the last three 3-day periods of creations is a test window; training uses VMs created at least "
            "24 h 10 min before it, whose class was known then."
        ),
        changes=(
            "We dropped the VMs running at the trace's start or created in its last 24 hours, built the history "
            "features as of each creation (the deployment's arrivals only up to the previous 5 minutes, since the "
            "trace cannot order VMs within 5 minutes), and left out the CPU statistics and the VM category, which "
            "describe the VM's whole life."
        ),
        fit="direct",
        fit_reason=(
            "The moment, the decision and the classes are the paper's. The public trace lacks some of its inputs "
            "(service name, operating system, exact VM size), and the history spans at most the 30 days."
        ),
    )

    # Dataset
    unique_name = "azure_vm_lifetime_resource_central_1m"
    version_of = "azure_vm_lifetime_resource_central"
    version_comment = """
        The full task has 2,409,604 VMs, and the train sides of its windows hold 1.57M to 2.04M rows (65% to 85% of them). We sample per test window (v2 split protocol): each window keeps at most 500k of its rows (none holds more, so none is cut), and its train side is a random 1M of all rows it may train on, drawn in one random order for all windows; the frame keeps only the rows a split uses. The history features are computed on the full trace before sampling.
    """
    year = "2019"
    domain = "technology & internet"
    source = "GitHub"
    source_url = "https://github.com/Azure/AzurePublicDataset/blob/master/AzurePublicDatasetV2.md"
    license = "CC BY 4.0"
    download_description = """
        We download the VM, deployment and subscription tables of the Azure Public Dataset V2 (2019) from the repository's release `dataset-v2` (links in AzurePublicDatasetLinksV2.txt), not the 195 files of 5-minute CPU readings, which describe each VM's life after its creation. Only the VM table is read; the other two were checked and are not used.

        mkdir -p local-data-warehouse/azure_vm_lifetime_resource_central && cd local-data-warehouse/azure_vm_lifetime_resource_central
        B=https://github.com/Azure/AzurePublicDataset/releases/download/dataset-v2
        for f in trace_data_vmtable_vmtable.csv.gz trace_data_deployments_deployments.csv.gz trace_data_subscriptions_subscriptions.csv.gz schema.csv Azure.2019.Public.Dataset.V2.-.Trace.Analysis.ipynb; do wget "$B/$f"; done
    """
    bibtex = """
        @inproceedings{cortez2017resourcecentral,
          title = {Resource Central: Understanding and Predicting Workloads for Improved Resource Management in Large Cloud Platforms},
          author = {Cortez, Eli and Bonde, Anand and Muzio, Alexandre and Russinovich, Mark and Fontoura, Marcus and Bianchini, Ricardo},
          booktitle = {Proceedings of the 26th Symposium on Operating Systems Principles (SOSP '17)},
          pages = {153--167},
          year = {2017},
          doi = {10.1145/3132747.3132772},
        }
    """
    curation_comments = """
        We start with `vmtable.csv.gz` (2,695,548 VMs, 11 columns) of the Azure Public Dataset V2, a 30-day trace of first-party Azure VMs in one region in 2019, published in the repository in July 2019. Microsoft asks users of the trace to cite the Resource Central paper (SOSP 2017), which predicts each new VM's lifetime class for the VM scheduler.

        - The prediction point is the VM's creation: the scheduler can ask Resource Central for the VM's lifetime class when it places the VM (Sec. 4.1 of the paper: "the VM scheduler can use the lifetime predictions to co-locate VMs that are likely to terminate roughly at the same time"), as Azure's allocator later did (Barbalho et al., "Virtual Machine Allocation with Lifetime Predictions", MLSys 2023). Only what is known at that moment is a feature.
        - Note: the trace's times are seconds since its start, all on the 300 s grid of the 5-minute CPU readings (100% of `created` and `deleted`; the release does not say whether they are the first and last reading, so a VM can have lived up to 5 minutes longer or shorter). The lifetime is `max(deleted - created, 300)` s, as in Microsoft's analysis notebook of the trace, and its class follows the paper's Table 3: up to 15 min, over 15 to 60 min, over 1 to 24 h, over 24 h.
        - We drop the 227,316 VMs running at the trace's start (`created == 0`): their creation, and so their lifetime, is not in the trace.
        - We drop the 58,628 VMs created in the last 24 h 5 min of the trace (after 2,504,700 s): a VM still running at the trace's end (`deleted` = 2,591,400 s) has a class we know only once it has run over 24 h, and the ones still running would otherwise look short-lived (LEAK-24). The cut is by creation time, not by the outcome, so every kept row has its true class: each kept VM still running at the end ran over 24 h (an assert in `_clean`).
        - We drop `vm_category`: the source infers it from the periodicity of the VM's CPU readings over at least 3 days (Sec. 3.6), so it is `Unknown` for every VM that lived less than about 3 days and encodes the lifetime (LEAK-10).
        - We drop `max_cpu`, `avg_cpu` and `p95_max_cpu`: they summarise the CPU readings of the VM's whole life, after the prediction point (LEAK-10). They enter only as history, averaged over the subscription's VMs that had ended before the row's creation.
        - The deployment table's `deployment size` and the subscription table's VM count are not used: the size is the most VMs the deployment ran at once over its life (for 86.7% of the 33,205 deployments; the paper's "maximum deployment size", Sec. 3.4), and the count is taken over the whole trace, so both are known only after the prediction point (LEAK-10); the counts to date below replace them. The subscription table's first-VM time equals the earliest `created` of the subscription's VMs for every subscription, so it adds nothing.
        - We drop the encrypted VM, subscription and deployment ids after building the features: Resource Central's models use features that exist in every subscription and the subscription's history, not the id (Sec. 6.1).
        - The trace's deployment is not one Azure request: the paper regroups "the set of VMs from each subscription that are deployed to a region during a day" (Sec. 3.4), and the V2 page says "we define a 'deployment' differently than Azure in our paper". Its day has a fixed boundary at trace second 80,700, which none of the 28,208 deployments created in the trace crosses, so a VM's deployment is known at its creation. A deployment creates VMs slot after slot: 78.2% of the rows sit in a deployment that also created VMs in the previous slot, 77.8% in one that creates VMs in the next.
        - Features we build, as of the VM's creation slot `t`; Resource Central computes the same kind of feature data from the history (Sec. 4 and 6.1: "the most important attributes in determining prediction accuracy are the percentage of VMs classified into each bucket to date in the subscription"). The deployment: `deployment_vms_prev_slot`, its VMs created in the previous 5-minute slot (`t` - 300 s; an assert checks that they are among the VMs counted before `t`), `deployment_vms_before` (created in earlier slots; VMs running at the trace's start included) and `deployment_vms_running`. The deployment's VMs created in the same slot are not counted (LEAK-10): the trace cannot order VMs within a slot, so the count would include VMs that arrive up to 5 minutes later, and such arrivals carry a gain: the deployment's VMs of the next slot, added as a feature, lower log loss by 0.013 on average (LightGBM, 3 seeds in each of the 3 windows, lower in 8 of 9 fits; a random column moves it by 0.0015), while the previous slot's count scores as the same-slot count did (0.003 lower on average). Counts to date: `subscription_vms_running` (created before `t`, `deleted` at `t` or later; VMs running at the trace's start included) and `subscription_vms_created_24h` (created in the 24 h before `t`; missing before 86,400 s in the 5,687 subscriptions with VMs running at the trace's start, whose creation times are unknown: 87,870 rows, all on training sides). The subscription's lifetime classes: `subscription_vms_class_known` and the four `subscription_share_*` among the subscription's VMs whose class was known at `t` (one slot after its `deleted` time, or 24 h 10 min after its creation once it has run over 24 h; a VM running at the trace's start counts as over 24 h once it has run 24 h 10 min into the trace). `subscription_mean_avg_cpu` and `subscription_mean_p95_max_cpu`: the means of `avg_cpu` and `p95_max_cpu` over the subscription's VMs that had ended before `t`. Shares and means are missing when there is no such VM. Checked on this code: the trace cut at a slot (VMs created up to it, none ended later) gives every row created in that slot the same features as the full trace (23,436 rows at 63 slots, 12 features, 0 mismatches), and so does that cut trace without a random half of the slot's VMs (23,398 rows over two random halves, 0 mismatches), so no feature reads another VM of the row's own slot; an independent re-implementation on 3,700 rows agreed with the code before the lag, `subscription_mean_p95_max_cpu` and `subscription_vms_class_known` included.
        - `trace_hour_of_day` and `trace_day_of_week` are the hour and the day modulo 7 of the creation, as numbers (0-23 and 0-6), counted from the trace's start; the release gives neither the start's date nor its clock time. Creations follow a daily cycle and dip on days 1-2, 8-9, 15-16, 22-23 and 29 of the trace, so the day modulo 7 stands in for the weekday, a number as every weekday of the working copy (CLEAN-14).
        - `core_bucket` and `memory_bucket` are the source's size classes of the VM's virtual cores (2, 4, 8, 24, over 24) and memory in GB (2, 4, 8, 32, 64, over 64), ordered; the release does not define the class edges.
        - History: each subscription's history starts with the trace, so early rows know less of it than later ones (Resource Central's feature data spans months). The rows of the first days stay: a refit model trains on them too, and the count of known classes tells how much history a row has.
        - Duplicate rows and the unit: the VMs of one deployment created in one slot (a deployment-slot group, up to 918 VMs) share every feature and often differ in lifetime (41.7% of the groups with several VMs mix classes); they are distinct VMs and stay. 62.7% of the rows copy another row, and the rows of one slot are always on the same side of a split (0.0% of test rows have a copy in train). The score stays per VM (MET-17): the scheduler places each VM, and Resource Central's Table 4 counts per VM. The test windows hold about 4 VMs per group (281,121 / 234,507 / 241,863 VMs in 64,568 / 57,640 / 58,788 groups, newest first); groups of over 100 VMs hold 4.8 / 12.3 / 5.1% of the rows, and the over-24-h class is 5.5 / 5.1 / 5.9% of the VMs but 8.9 / 8.2 / 8.4% of the groups. Counting each group once reorders four feature-set variants of one learner at Kendall tau 0.00 / 0.33 / 1.00 against the per-VM log loss (indicative; measured with the same-slot count). Per-VM log loss weighs the short classes over the long one (up to 15 min: 42.5% of the kept VMs and 0.7% of their core-time; over 24 h: 5.7% and 79.9%); no source fixes a resource weight, so none is set (MET-7). One subscription holds 11.9-13.4% of each test window.
        - Potential leak, kept on purpose (LEAK-9, an evaluation leak): `deployment_vms_before` is cumulative, so a deployment's later test rows link to its earlier ones (with the same-slot count, the next slot's `deployment_vms_before` is this one plus the count; with the previous slot's count, a row's `deployment_vms_before` minus it is the previous slot's; matched on the size classes, 90% of the rows link), and along the chain the deaths (`deployment_vms_before` - `deployment_vms_running`) and the subscription's per-class counts (share x `subscription_vms_class_known`, an integer on 100% of the rows) reveal the current cohort's lifetimes up to 24 h ahead. A participant who reads the later test rows lowers log loss from 0.8661 to 0.7297 (regularised LightGBM; 0.169 / 0.125 / 0.115 lower per window, newest first) and from 0.9204 to 0.7409 (untuned LightGBM; 0.155 / 0.203 / 0.180 lower), a lower bound, measured with the same-slot count. The counts stay as they are, not rounded: rounding changes faithful values and still leaves a gain of 0.015. Each test VM is predicted from the training rows and its own features only; no feature or model step may use other test rows, and a method that does is called out and not benchmarked (LEAK-9 as amended 2026-11-05, as for medical_facility_operational_data).
    """

    # Task
    target = "lifetime_class"
    problem_type = "multiclass_classification"
    metric = Metric.fallback(
        reason=(
            "Resource Central (Cortez et al., SOSP 2017, Sec. 6.1, Table 4) reports for the lifetime classes the "
            "accuracy of the most likely class, the per-class precision and recall, and the precision and recall when "
            "a prediction scoring below 0.6 is withheld, side by side; it names no one metric as its criterion, and "
            "the hard-label metrics fix no cost, so the multiclass fallback (MET-5, MET-6, MET-8). The repository's "
            "V2 page and analysis notebook define no task or metric."
        )
    )

    # Splits
    temporal = Temporal(
        on="created",
        splits=TemporalSplits(window=WINDOW_SLOTS, unit="unique", n_windows=3, gap=GAP_SLOTS),
        horizon=WINDOW_SLOTS,
        horizon_unit="steps",
        gap=GAP_SLOTS,
        gap_unit="steps",
    )
    splits_comment = """
        Three test windows of 3 days each (864 five-minute creation slots; every slot of the trace has a creation, so the slots count time), the newest first, over the last 9 of the 29 days of rows. The train side of each window holds the VMs created at least 24 h 10 min before the window starts (a gap of 289 slots): a VM's lifetime class is known at most 24 h 10 min after its creation, so this is what a model refit at the window's start trains on. Without the gap the newest training VMs would be the short-lived ones, whose class is known early (the label-timing decision below). The gap also keeps `created` harmless, a trend counter whose test values lie beyond every training value: without the gap, untuned LightGBM scores log loss 1.331 on the newest window with it and 0.938 without it. The paper trains on two months and tests on the next (Sec. 6.1), which a 30-day trace cannot hold. The windows are 3 days, an exception to the source's horizon (SPLIT-12): every train side then holds 65% or more of the rows (84.7 / 76.2 / 65.2%, newest first), where 4-day windows would leave the oldest 55.2% and 4.5-day windows 50.8%. The newest window holds only high-volume days (trace days 26 to 28); the two older ones hold one low-volume day each of the trace's weekly dip (day 23, 22.8% of the middle window's rows; day 22, 23.7% of the oldest's). Each window keeps at most 500k of its rows (none is cut); each train side is a random 1M of all earlier rows (one random order for all windows). Each test VM is predicted from the training rows and its own features only; no feature or model step may use other test rows (LEAK-9: the later rows of a deployment in a test window reveal its earlier VMs' lifetimes).
    """
    row_budget = RowBudget(train=1_000_000, test=500_000)

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        vm = pl.read_csv(
            raw_dir / "trace_data_vmtable_vmtable.csv.gz",
            has_header=False,
            new_columns=VMTABLE_COLUMNS,
            schema_overrides={"core_bucket": pl.Utf8, "memory_bucket": pl.Utf8},
        )
        return vm.to_pandas()

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        vm = pl.from_pandas(raw)
        trace_end = int(vm["deleted"].max())
        # 1. Rows: VMs created inside the trace and at least 24 h 5 min before its end, with the history features as
        #    of each creation (`_history_features`). vm_category, the CPU statistics and the ids are not carried.
        df = _history_features(vm, trace_end).to_pandas()
        # 2. Every kept VM still running at the trace's end has run over 24 h, so its class is final.
        running_at_end = df["deleted"] == trace_end
        assert (df.loc[running_at_end, "lifetime_class"] == LIFETIME_CLASSES[3]).all()
        df = df.drop(columns=["vm_id", "deleted"])
        # 3. The creation's hour and day (modulo 7), counted from the trace's start.
        df["trace_hour_of_day"] = (df["created"] % DAY) // 3600
        df["trace_day_of_week"] = (df["created"] // DAY) % 7
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            ordinal={
                "core_bucket": ["2", "4", "8", "24", ">24"],
                "memory_bucket": ["2", "4", "8", "32", "64", ">64"],
                self.target: LIFETIME_CLASSES,
            },
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        trace_end = int(raw["deleted"].max())
        late = raw["created"] > trace_end - (DAY + SLOT)
        observed = _observed_class(raw["created"], raw["deleted"])
        late_state = (raw.loc[late, "deleted"] == trace_end).map({True: "running at the end", False: "ended"})
        late_table = pd.crosstab(observed[late].rename("observed lifetime class"), late_state)
        kept = (raw["created"] > 0) & ~late
        rows = pd.DataFrame(
            {
                "VMs": [len(raw), int((raw["created"] == 0).sum()), int(late.sum()), int(kept.sum()), len(df)],
            },
            index=[
                "in the trace",
                "running at its start (dropped)",
                "created in its last 24 h 5 min (dropped)",
                "kept",
                "shipped after sampling the train sides to 1M",
            ],
        )
        # Label timing: the VMs created in the 24 h 10 min before each window's start, and whether their class was
        # known at the start (they had ended, or had run over 24 h).
        slots = np.sort(df["created"].unique())
        timing = {}
        for i in range(3):
            start = int(slots[len(slots) - WINDOW_SLOTS * (i + 1)])
            near = raw[(raw["created"] > start - CLASS_KNOWN_WITHIN) & (raw["created"] < start)]
            known_at = np.minimum(near["deleted"] + SLOT, near["created"] + CLASS_KNOWN_WITHIN)
            cls = _observed_class(near["created"], near["deleted"])
            timing[f"window {i} (starts at day {start / DAY:.2f})"] = (
                (known_at <= start).groupby(cls, observed=False).mean()
            )
        timing = pd.DataFrame(timing).T.map(lambda x: f"{x:.1%}")
        category = pd.crosstab(raw["vm_category"], observed, normalize="columns").map(lambda x: f"{x:.1%}")
        return [
            Decision(
                "Rows: VMs created inside the trace, at least 24 h 5 min before its end",
                "A VM running at the trace's start has no creation in it, and a VM created near the end that is still "
                "running has no known class.",
                rows,
            ),
            Decision(
                "The dropped late VMs by their observed lifetime",
                "The VMs created in the last 24 h 5 min, by the class the trace shows and their state at the end: "
                "the ones still running would have entered the shorter classes.",
                late_table,
            ),
            Decision(
                "A gap of 24 h 10 min between train and test",
                "The share of the VMs created in the 24 h 10 min before each window's start whose lifetime class was "
                "known at the start, by class: without the gap, the newest training VMs would be the short-lived ones.",
                timing,
            ),
            Decision(
                "`vm_category` dropped: it encodes the lifetime",
                "The share of each source category within each lifetime class (all VMs, as the trace shows them): "
                "the category needs 3 days of CPU readings, so the VMs of the shorter classes are `Unknown`.",
                category,
            ),
        ]
