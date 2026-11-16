"""Curated dataset definition for `backblaze_hard_drive_failure_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import datetime as dt
import io
import zipfile
from pathlib import Path

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

QUARTERS = ("Q1_2025", "Q2_2025", "Q3_2025", "Q4_2025", "Q1_2026", "Q2_2026")
"""The quarterly zips read: from the first cut date (1 January 2025) to the end of the newest release (30 June 2026),
which covers the 30 days after the last cut."""

CUT_DATES = tuple(dt.date(2025 + m // 12, m % 12 + 1, 1) for m in range(17))
"""The prediction points: the first day of each month from January 2025 to May 2026. May 2026 is the last month whose
30 days after the cut lie inside the newest release (Q2 2026 ends on 30 June 2026)."""

HORIZON_DAYS = 30
"""A drive is a positive when Backblaze records it as failed within the 30 days after the cut date, the horizon of the
PAKDD 2020 Alibaba disk-failure challenge ("whether each disk will fail or not within the next 30 days")."""

ID_COLUMNS = ("date", "serial_number", "model", "datacenter", "cluster_id", "vault_id", "pod_id", "is_legacy_format")
"""The text columns of a daily file; every other column is a number (capacity, failure flag, slot, SMART values)."""


def _daily_files(raw_dir: Path) -> list[tuple[Path, str]]:
    """Every daily CSV in the quarterly zips, in date order (the macOS resource forks of Q4 2024 left out)."""
    files = []
    for quarter in QUARTERS:
        path = raw_dir / f"data_{quarter}.zip"
        with zipfile.ZipFile(path) as archive:
            names = [n for n in archive.namelist() if n.endswith(".csv") and not n.startswith("__MACOSX")]
        files += [(path, name) for name in sorted(names)]
    return files


NEAR_CONSTANT = ("smart_23_normalized",)
"""SMART columns with one value on every reported row but one, dropped as constant."""

BOOT_MAX_BYTES = 2.2e12
"""Boot drives (SSDs and 240 GB to 2 TB disks that hold a server's operating system) have a capacity of at most 2.05 TB;
every data drive holds 4 TB or more."""

VAULT_BLOCK = 20
"""A drive removed without a failure record is part of a vault migration when 20 or more data drives of its vault leave
the files within the 30 days after the same cut."""

SENTINELS = {"smart_9_raw": (0.0, 65535.0), "smart_240_raw": (65535.0,)}
"""Impossible or saturated readings set to missing: zero power-on hours on drives years old, and the 16-bit maximum
65535 in power-on and head-flying hours (a few ST8000NM0055 drives)."""


def _label_cut(snapshots: pl.DataFrame, failures: pl.DataFrame, last_seen: pl.DataFrame, cut: dt.date) -> pl.DataFrame:
    """The drives of one cut day with their outcome over the 30 days after it, and which of them stay.

    The flags, each among the drives the earlier ones leave: `boot`, a boot drive; `no_slot`, a data drive without a
    pod slot on the cut day (out of the data path); `fails_on_cut`, the failure record is the cut day itself;
    `removed_in_horizon`, no failure record and the drive's last day in the files falls before the 30th day after the
    cut; `vault_block`, a removed drive one of 20 or more removed from its vault after this cut. `fails` is a failure
    record on one of the 30 days after the cut, and `keep` marks the rows that stay. The dates are ISO strings.
    """
    day, end = cut.isoformat(), (cut + dt.timedelta(days=HORIZON_DAYS)).isoformat()
    failed = (
        failures.filter((pl.col("date") > day) & (pl.col("date") <= end))
        .select("serial_number")
        .unique(maintain_order=True)
    )
    rows = snapshots.filter(pl.col("date") == day)
    rows = rows.join(failed.with_columns(pl.lit(True).alias("fails")), on="serial_number", how="left")
    rows = rows.join(last_seen.rename({"date": "last_seen"}), on="serial_number", how="left")
    boot = pl.col("capacity_bytes") <= BOOT_MAX_BYTES
    no_slot = ~boot & pl.col("pod_slot_num").is_null()
    on_cut = ~boot & ~no_slot & (pl.col("failure") == 1)
    rows = rows.with_columns(
        pl.col("fails").fill_null(False), boot.alias("boot"), no_slot.alias("no_slot"), on_cut.alias("fails_on_cut")
    )
    eligible = ~pl.col("boot") & ~pl.col("no_slot") & ~pl.col("fails_on_cut")
    removed = eligible & ~pl.col("fails") & (pl.col("last_seen") < end)
    rows = rows.with_columns(removed.alias("removed_in_horizon"))
    block = pl.col("removed_in_horizon") & (pl.col("removed_in_horizon").sum().over("vault_id") >= VAULT_BLOCK)
    rows = rows.with_columns(block.alias("vault_block"))
    keep = eligible & (~pl.col("removed_in_horizon") | pl.col("vault_block"))
    return rows.with_columns(keep.alias("keep")).drop("last_seen")


class BackblazeHardDriveFailure1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will this hard drive be replaced as failed within the next 30 days, given its SMART readings today?",
        use_case=(
            "A cloud-storage operator's data-centre team reviews its fleet on the first of each month and decides "
            "which drives to watch, move data off or replace before they fail; Backblaze investigates a drive when "
            "one of five SMART error counters rises above zero."
        ),
        row=(
            "One data drive in service in Backblaze's data centres on the first day of a month, January 2025 to May "
            "2026 (301,000 to 345,000 drives a month, 54 models); the servers' boot drives are left out."
        ),
        predicted=(
            "Whether Backblaze records the drive as failed in the 30 days after that day; a failure is a drive "
            "replaced because it died or because its indicators said it was about to (about half each)."
        ),
        known=(
            "The drive's model, capacity and place in the data centre, and that day's SMART readings (raw and "
            "normalised), including its power-on hours and error counters."
        ),
        split=(
            "Each test window is one monthly snapshot (March, April and May 2026); training is a random million "
            "drive-months from January 2025 up to the latest snapshot whose 30 days had passed."
        ),
        changes=(
            "We built the rows and the label from Backblaze's daily logs; boot drives, drives without a slot in "
            "their server (already out of service), drives failing on the snapshot day and single drives that vanish "
            "without a failure record are left out, and drives that leave in a whole-vault migration count as not "
            "failed."
        ),
        fit="approximate",
        fit_reason=(
            "The rows, inputs and monthly refit mirror a fleet review, but the label is Backblaze's replacement "
            "record: 53% of the failures of Q3 2024 were proactive pulls on indicators that overlap the inputs, by a "
            "rule not published and at a share that varies by server type and data centre, and a few are pulls for "
            "firmware work. The five-counter rule alone ranks well below a model."
        ),
    )

    # Dataset
    unique_name = "backblaze_hard_drive_failure_1m"
    version_of = "backblaze_hard_drive_failure"
    version_comment = """
        The full table holds 17 monthly snapshots of 301,000 to 345,000 drives (5.48M rows), so each train side would hold 4.1M to 5.1M rows. We sample per test window (v2 split protocol): each window keeps all its drives (336,654 to 345,340, under the 500k budget), and its train side is a random 1M of all earlier rows outside the gap, drawn in one random order for all windows; the frame keeps only the rows a split uses. A random sample keeps every month of the training history, as in the other temporal `_1m` versions.
    """
    year = "2026"
    domain = "technology & internet"
    source = "Other"
    source_url = "https://www.backblaze.com/cloud-storage/resources/hard-drive-test-data"
    license = (
        "Backblaze Drive Stats terms (no named licence): cite Backblaze as the source; the data itself may not be sold"
    )
    data_tags = ()
    download_description = """
        Backblaze's quarterly zips of daily drive snapshots (one CSV per day), Q1 2025 to Q2 2026 (about 7.8 GB zipped):

        mkdir -p local-data-warehouse/backblaze_hard_drive_failure && cd local-data-warehouse/backblaze_hard_drive_failure
        for q in Q1_2025 Q2_2025 Q3_2025 Q4_2025 Q1_2026 Q2_2026; do wget https://f001.backblazeb2.com/file/Backblaze-Hard-Drive-Data/data_$q.zip; done
        wget https://f001.backblazeb2.com/file/Backblaze-Hard-Drive-Data/Drive_Stats_Schema_Current.csv

        The zips stay zipped; the first build reads every daily file once and writes `snapshots.parquet`, `drive_last_seen.parquet` and `failures.parquet` next to them. `data_Q4_2024.zip` was downloaded too, for a test of change features over the 30 days before a cut, and is not read.
    """
    bibtex = """
        @misc{backblaze2026drivestats,
          author = {{Backblaze}},
          title = {Hard Drive Data and Stats},
          howpublished = {\\url{https://www.backblaze.com/cloud-storage/resources/hard-drive-test-data}},
          year = {2026},
          note = {Daily drive snapshots with SMART statistics, published since February 2015},
        }
    """
    curation_comments = """
        We start with Backblaze's daily drive snapshots of 1 January 2025 to 30 June 2026 (`data_Q1_2025.zip` to `data_Q2_2026.zip`, one CSV per day with one row per drive in service).

        - Year: 2026, the release we pin (the quarterly files Q1 2025 to Q2 2026 of a growing archive, PROV-9). Backblaze has published the daily files since 4 February 2015 ("Reliability Data Set for 41,000 Hard Drives Now Open-source").
        - Prediction point: the first day of a month (17 cuts, January 2025 to May 2026), when a data-centre team reviews its fleet. One row is a data drive in that day's snapshot, with that day's values only. May 2026 is the last cut whose 30 days lie inside the release.
        - Label: `fails_within_30_days` is Yes when the drive has a failure record (`failure` = 1, written on its last day in service) on one of the 30 days after the cut (5,458 of 5,482,492 rows, 0.100%; 122 to 460 per cut). Backblaze counts a drive as failed when it is replaced as a reactive (dead) or a proactive (failing indicators) failure; drives pulled for other reasons are not failures. The 30 days follow the PAKDD 2020 Alibaba disk-failure challenge ("whether each disk will fail or not within the next 30 days"); Backblaze defines no horizon.
        - Rows left out, in this order (the decision table counts each cut):
          - Boot drives, 67,620 rows (SSDs and 240 GB to 2 TB disks that hold a server's operating system; capacity at most 2.05 TB, every data drive 4 TB or more). The files hold 32 boot-drive failure records in Q4 2024 and none from January 2025 to June 2026, while boot drives still leave the files (306 rows within 30 days of a cut), so a boot drive's No means "not recorded" (LEAK-25). Backblaze reports boot drives apart from data drives.
          - Data drives without a pod slot on the cut day, 6,353 rows (369 of them with a failure record in the 30 days, 5.8% against 0.1%, and 143 with one on the cut day). The slot goes empty when a drive is taken out of the data path, mostly as the first step of its replacement: in the daily files of Q4 2025 to Q2 2026 it is empty on 69% of failure-record days, and on slot-empty days a drive reads about 0.1M sectors a day against 340M to 460M with a slot (LEAK-10). The rule reads no label; it also takes whole-vault reporting gaps (no failures), and it makes the cohort match the drives already left out for being absent from the cut-day file. The reading is ours: Backblaze does not document an empty slot.
          - Drives whose failure record is the cut day itself, 55 rows: the snapshot is the failure record.
          - Drives that leave the files within the 30 days without a failure record and outside a vault migration, 185 rows: likely failures without a record (LEAK-25). One of SMART 5, 187, 188, 197 and 198 is above zero on 42.7% of them, against 7.7% of the kept No rows and 69.8% of the Yes rows (counted before the slot rule, on 206 drives).
        - Kept as No: the drives that leave the files within the 30 days in a block of 20 or more data drives of one vault after the same cut, 8,356 rows (4,191 on the March 2025 cut, 2,091 on January 2026, and 1,054, 900 and 120 on March, April and May 2026): vault migrations, an exit after the prediction point. Backblaze counts drives removed for other reasons as not failed, and dropping them would choose the rows by the future (LEAK-22, as framingham_heart_study_fhs keeps its competing deaths as No). An error counter is above zero on 12.4% of them, below the 22.3% of kept No rows of the same age and equal to their models' kept No rows (ST8000DM002, most of the young block drives: 31.9% against 31.9%), so they show no sign of unrecorded failures. The block rule reads no label, and every block is complete by the cut plus 30 days, so it is known at each window's refit.
        - Dropped columns: `serial_number` (the drive's id), `failure` (0 on every kept row), `is_legacy_format` (one value, written False or false), the 116 SMART columns empty or constant on the data drives (58 of them reported by boot drives only), and `smart_23_normalized` (100 on every reported row but one).
        - Kept as published: 69 SMART columns, raw and normalised values side by side, missing where a drive does not report the attribute (which attributes a drive reports depends on its maker and model); the place in the data centre (`datacenter`, `cluster_id`, `vault_id`, `pod_id`, `pod_slot_num`). Seagate's raw SMART 1, 7, 188 and 195 are bit-packed fields (SMART 188 holds three 16-bit counters; SMART 1 and 7 an error count over an operation count), kept as shipped, as Backblaze reads them; a value above zero means the same either way. `WUH721816ALE6L4` and `WDC WUH721816ALE6L4` stay two models: no drive carries both names, and only the first reports SMART 82 (a firmware or batch). Backblaze notes that `cluster_id` "is not always correct".
        - Types: `datacenter`, `cluster_id`, `vault_id` and `pod_id` are codes, so categories; `pod_slot_num` stays a number (CLEAN-14): a slot is a physical position in one server's chassis (nearby numbers are nearby slots; per-slot failure rates are flat, 0.06% to 0.15%), while `pod_id` is one of a vault's 20 servers, an index with no adjacency. Slot numbering follows the server type (26, 45 or 60 drives).
        - Set to missing: `smart_9_raw` (power-on hours) 0 on 215 rows of drives years old (none failing) and 65535 on 34 rows, and `smart_240_raw` (head-flying hours) 65535 on 30 rows: impossible or saturated 16-bit readings (CLEAN-10, CLEAN-11). The 65535 of `smart_187_raw` is a saturated error counter, a real value, and stays.
        - Not built: the change of each raw SMART counter over the 7 or 30 days before the cut. With them a regularised LightGBM scores ROC AUC 0.899, 0.918 and 0.902 on the March, April and May 2026 windows, against 0.890, 0.911 and 0.904 without (one seed, one random 1M training sample per window, on the rows before the boot, slot and vault-block rules): a gain in two windows, a loss in one. The counters are cumulative, so the snapshot already carries the drive's history, and the daily files can be used as they are.
        - Note on the label: in Q3 2024 Backblaze counted 640 reactive and 721 proactive failures (47.0% and 53.0%), the proactive ones decided on indicators ("SMART stats or file system checks", drive sentinel's read and write error threshold) that overlap the inputs. The proactive share differs by server type (Dell 73.5%, Supermicro 64.5%, Storage Pod 6.0 44.6%) and data centre (AMS 68.1%, SAC2 47.5%), which the place columns carry. The rule is not published, and the files do not say which failures were proactive. Backblaze's own triage rule, the count of SMART 5, 187, 188, 197 and 198 above zero, scores ROC AUC 0.832, 0.865 and 0.828 on the March, April and May 2026 windows against 0.871, 0.896 and 0.895 for a regularised LightGBM; 22% to 29% of the positives have all five at zero (Backblaze reported 23.3% in 2016), and among those drives the model reaches 0.66 to 0.74. The model ranks drives failing within 7 days about as well as those failing in 8 to 30 days (0.864 to 0.898 against 0.866 to 0.905, the order changing by window). These numbers come from one random 1M training sample of the same rows per window, not the shipped one, and one seed. What sets this label apart from one set by a review step on an input (xente_fraud_detection_challenge): every drive in service is monitored and a dead drive is always recorded, and the five-counter rule ranks below a model, so a No is not "not reviewed".
        - Note on the test cohort: a row is a drive in the cut day's file with a slot. Of the 1,449 drives that fail within 30 days of the three test cuts, 187 (13%; 119 in April 2026) are absent from the cut-day file and 115 are in it without a slot; both are already out of the data path (cut off by drive sentinel or under service), so the test windows hold the other 1,147 and leave out the most obvious failures, a number that swings by month.
        - Note on the training labels (SPLIT-10): the removal rule reads each drive's last day over the whole release, not as of each window's refit. 55, 121 and 74 training rows of the March, April and May windows (none positive; about 13 to 25 in a 1M train side) are kept as No because their drive reappears after the test cut, where a refit would have called it a scattered removal; 20, 13 and 3 dropped rows would be kept. None is a test row of its window. Before the boot, slot and vault-block rules the panel counted 210, 821 and 695 such rows, most in vault-wide gaps, which the vault-block rule keeps as No either way.
        - Anomaly: label noise as published. Toshiba MG08ACA16TEY drives had 64 to 76 failure records a month from July to September 2025 against 2 to 21 otherwise; Backblaze's Q3 2025 post calls them "cosmetic" failures after firmware work. They fall in training cuts only.
        - Anomaly: the December 2025 cut has 122 positives (0.037%) against 244 to 460 on the others. Replacements slow over the holidays (failure records fall to 1 to 5 a day from 16 December to 4 January, against about 8 to 15), and part of the dip is drives that vanish without a record: the November and December cuts lose 34 and 52 scattered drives, about half with an error counter. The April 2026 cut has the most (460, 0.135%), in the quarter whose failure rate Backblaze calls "the highest it's been in quite a while" (1.73%).
    """

    # Task
    target = "fails_within_30_days"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason=(
            "Backblaze publishes failure rates (annualised failure rates per model) and defines no prediction task "
            "or metric (the data page, the Drive Stats posts of Q3 2024, Q3 2025 and Q2 2026, and 'What SMART Stats "
            "Indicate Hard Drive Failures', 2016). The PAKDD 2020 Alibaba challenge scored a windowed precision, "
            "recall and F1 on hard labels for its own data, with no threshold that carries over (MET-6). roc_auc is "
            "the binary fallback (MET-8); the imbalance alone is no reason for PR AUC (MET-9). The operator acts on "
            "the top 0.1% to 1% of the fleet, a number that moves with technician capacity; on the test windows, "
            "recall in the top 0.5% and ROC AUC order four LightGBM variants differently by a few drives per window "
            "(one positive is 0.002 to 0.003 of recall), but no source fixes the share or a false-alarm cap, so "
            "roc_auc stays (MET-7)."
        )
    )

    # Splits
    splits_comment = """
        A fleet model is refit monthly and scores every drive in service on the first of the month. The three newest cuts are the test windows (1 May, 1 April and 1 March 2026, newest first), each one calendar month holding one cut. A window's train side holds the cuts whose 30 days had passed by its cut date: train cut dates lie strictly before the test cut minus 29 days, so cut + 30 days is at most the test cut, and the training labels are all known at the refit. The previous month's cut is therefore left out of the March window (February has 28 days) and kept in the April and May windows. The oldest window trains on 13 of the 17 cuts (75% of the rows). Each test window keeps all its drives (336,654 to 345,340 rows; 294 to 460 positives); each train side is a random 1M of the earlier drive-months (one random order for all windows). A drive recurs in every cut, so the test drives are known drives with earlier rows in training: the operator scores its own fleet.

        Protocol (LEAK-9): a method sees only its split's train rows and test window. Rows dated after a test window reveal its labels: a drive is recognised across months by model, place (datacenter, cluster, vault, pod, slot), capacity and power-on hours, and a drive missing from the next month's snapshot has usually failed (ROC AUC 0.993-0.996 on the March and April windows). A method that uses them is called out and not benchmarked.
    """
    temporal = Temporal(
        on="cut_date",
        splits=TemporalSplits(window=1, unit="months", n_windows=3, gap=29, gap_unit="days"),
    )
    row_budget = RowBudget(train=1_000_000, test=500_000)

    prepared_raw_files = ("snapshots.parquet", "drive_last_seen.parquet", "failures.parquet")

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        # One pass over the daily files: the full snapshot of each cut date, every drive's last day in the files, and
        # every failure record.
        snapshot_days = {d.isoformat() for d in CUT_DATES}
        snapshots, last_seen, failures = [], None, []
        for path, name in _daily_files(raw_dir):
            with zipfile.ZipFile(path) as archive:
                data = archive.read(name)
            day = Path(name).stem
            if day in snapshot_days:
                frame = pl.read_csv(io.BytesIO(data), infer_schema_length=0)
                numeric = [c for c in frame.columns if c not in ID_COLUMNS]
                snapshots.append(frame.with_columns(pl.col(c).cast(pl.Float64) for c in numeric))
            frame = pl.read_csv(
                io.BytesIO(data),
                columns=["date", "serial_number", "failure"],
                schema_overrides={"date": pl.Utf8, "serial_number": pl.Utf8, "failure": pl.Int8},
            )
            assert (frame["date"] == day).all(), f"{name}: the date column does not match the file name."
            seen = frame.select("serial_number", "date")
            last_seen = seen if last_seen is None else pl.concat([last_seen, seen])
            last_seen = last_seen.group_by("serial_number", maintain_order=True).agg(pl.col("date").max())
            failures.append(frame.filter(pl.col("failure") == 1).select("serial_number", "date"))
        pl.concat(snapshots, how="diagonal_relaxed").write_parquet(raw_dir / "snapshots.parquet")
        last_seen.sort("serial_number").write_parquet(raw_dir / "drive_last_seen.parquet")
        pl.concat(failures).sort(["date", "serial_number"]).write_parquet(raw_dir / "failures.parquet")

    def _load_raw(self, raw_dir: Path) -> dict[str, pl.DataFrame]:
        return {
            "snapshots": pl.read_parquet(raw_dir / "snapshots.parquet"),
            "last_seen": pl.read_parquet(raw_dir / "drive_last_seen.parquet"),
            "failures": pl.read_parquet(raw_dir / "failures.parquet"),
        }

    def _clean(self, raw: dict[str, pl.DataFrame]) -> pd.DataFrame:
        snapshots = raw["snapshots"]
        # The SMART columns that are empty or constant on the data drives of the cut days leave first (also to keep
        # memory down), and smart_23_normalized, 100 on every reported row but one (98, one Toshiba MG08ACA16TEY on
        # 1 February 2026). The boot drives' own SSD attributes leave with them.
        smart = [c for c in snapshots.columns if c.startswith("smart_")]
        data_drive = pl.col("capacity_bytes") > BOOT_MAX_BYTES
        n_values = snapshots.select(pl.col(c).filter(data_drive).drop_nulls().n_unique() for c in smart).row(0)
        empty = [c for c, n in zip(smart, n_values, strict=True) if n <= 1]
        snapshots = snapshots.drop(*empty, *NEAR_CONSTANT)
        frames = []
        for cut in CUT_DATES:
            rows = _label_cut(snapshots, raw["failures"], raw["last_seen"], cut)
            # Boot drives (no failure record after December 2024), data drives without a pod slot (already out of the
            # data path), drives whose failure record is the cut day itself (the snapshot is the failure record), and
            # drives that leave the files within the 30 days without a failure record outside a vault migration
            # (likely failures without a record) leave. Drives that leave in a vault block stay as No.
            rows = rows.filter(pl.col("keep"))
            frames.append(
                rows.with_columns(
                    pl.when(pl.col("fails")).then(pl.lit("Yes")).otherwise(pl.lit("No")).alias(self.target)
                )
            )
        df = pl.concat(frames, how="diagonal_relaxed").rename({"date": "cut_date"})
        # The drive's serial number (an identifier), the cut day's failure flag (0 on every kept row), the label's
        # bookkeeping and the format flag (one value, written False or false) leave.
        flags = ("fails", "boot", "no_slot", "fails_on_cut", "removed_in_horizon", "vault_block", "keep")
        df = df.drop("serial_number", "failure", *flags, "is_legacy_format")
        df = df.with_columns(
            pl.when(pl.col(c).is_in(list(values))).then(None).otherwise(pl.col(c)).alias(c)
            for c, values in SENTINELS.items()
        )
        constant = [c for c in df.columns if c.startswith("smart_") and df[c].drop_nulls().n_unique() <= 1]
        assert not constant, f"SMART columns constant on the kept rows: {constant}"
        return df.with_columns(pl.col("cut_date").str.to_date()).to_pandas()

    def _decisions(self, raw: dict[str, pl.DataFrame], df: pd.DataFrame) -> list[Decision]:
        columns = ("date", "serial_number", "failure", "capacity_bytes", "pod_slot_num", "vault_id")
        snapshots = raw["snapshots"].select(columns)
        counts = []
        for cut in CUT_DATES:
            rows = _label_cut(snapshots, raw["failures"], raw["last_seen"], cut)
            kept = rows.filter(pl.col("keep"))
            removed = rows.filter(pl.col("removed_in_horizon"))
            counts.append(
                {
                    "cut date": cut.isoformat(),
                    "drives in the snapshot": rows.height,
                    "boot drives (left out)": int(rows["boot"].sum()),
                    "data drives without a pod slot (left out)": int(rows["no_slot"].sum()),
                    "failing on the cut day (left out)": int(rows["fails_on_cut"].sum()),
                    "removed without failure, scattered (left out)": int((~removed["vault_block"]).sum()),
                    "removed without failure in a vault block (kept as No)": int(removed["vault_block"].sum()),
                    "rows kept": kept.height,
                    "failed within 30 days": int(kept["fails"].sum()),
                    "share failed (%)": round(100 * kept["fails"].mean(), 3),
                }
            )
        return [
            Decision(
                "Rows and positives per cut date",
                "Every cut date's snapshot, in the order the filters apply: boot drives, data drives without a pod "
                "slot, drives whose failure record is the cut day, and drives that leave the files within the 30 days "
                "without a failure record, dropped when scattered and kept as No when 20 or more leave one vault "
                "(a migration); then the rows kept and their positives. Holiday replacements are slow (December "
                "2025), and April 2026 is the highest month.",
                pd.DataFrame(counts),
            )
        ]

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            # The data centre, its cluster, the vault (a group of 20 pods) and the pod (one of the vault's 20
            # servers, an index with no adjacency) are codes; the slot stays a number, a physical position in one
            # server's chassis (nearby numbers are nearby slots).
            categorical=["model", "datacenter", "cluster_id", "vault_id", "pod_id"],
            datetime=["cut_date"],
        )
