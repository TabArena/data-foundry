"""Curated dataset definition for `cesnet_quic22_service_classification_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import gzip
import re
import zipfile
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    RowBudget,
    TaskSummary,
    Temporal,
    TemporalSplits,
    drop_columns,
)

if TYPE_CHECKING:
    import pandas as pd

ZIP_NAME = "cesnet-quic22.zip"
SAMPLE_FILE = "flows_sample.parquet"
COUNTS_FILE = "flow_counts.parquet"

SAMPLE_ONE_IN = 20
"""The fixed hash sample `_prepare_raw_files` keeps: a flow whose SplitMix64 hash of its `ID` is 0 modulo 20."""

CHUNK_BYTES = 256 * 1024 * 1024
"""The size of the blocks of a decompressed daily CSV parsed at a time."""

PPI_LENGTH = 30
"""The packet sequences hold the first 30 packets of a flow (the flow exporter's default)."""

HIST_BINS = 8
"""Each packet histogram has 8 logarithmic bins: 0-15, 16-31, 32-63, 64-127, 128-255, 256-511, 512-1024, >1024."""

# The release's columns, in the order of every daily CSV's header.
COLUMNS = (
    "ID",
    "SRC_IP",
    "DST_IP",
    "DST_ASN",
    "SRC_PORT",
    "DST_PORT",
    "PROTOCOL",
    "QUIC_VERSION",
    "QUIC_SNI",
    "QUIC_USERAGENT",
    "TIME_FIRST",
    "TIME_LAST",
    "DURATION",
    "BYTES",
    "BYTES_REV",
    "PACKETS",
    "PACKETS_REV",
    "PPI_LEN",
    "PPI_DURATION",
    "PPI_ROUNDTRIPS",
    "APP",
    "CATEGORY",
    "FLOW_ENDREASON_IDLE",
    "FLOW_ENDREASON_ACTIVE",
    "FLOW_ENDREASON_OTHER",
    "PPI",
    "PHIST_SRC_SIZES",
    "PHIST_DST_SIZES",
    "PHIST_SRC_IPT",
    "PHIST_DST_IPT",
)
INT_COLUMNS = (
    "ID",
    "DST_ASN",
    "SRC_PORT",
    "DST_PORT",
    "PROTOCOL",
    "BYTES",
    "BYTES_REV",
    "PACKETS",
    "PACKETS_REV",
    "PPI_LEN",
    "PPI_ROUNDTRIPS",
)
FLOAT_COLUMNS = ("DURATION", "PPI_DURATION")
BOOL_COLUMNS = ("FLOW_ENDREASON_IDLE", "FLOW_ENDREASON_ACTIVE", "FLOW_ENDREASON_OTHER")
TIME_COLUMNS = ("TIME_FIRST", "TIME_LAST")
# The packet sequence's three lists, in the order the release stores them, and our column prefixes.
PPI_PARTS = (("ipt", "ppi_ipt_"), ("dir", "ppi_dir_"), ("size", "ppi_size_"))
# The four histograms and our column prefixes (the TMA 2023 paper's names, Fig. 3).
HISTOGRAMS = {
    "PHIST_SRC_SIZES": ("psize_bin", ""),
    "PHIST_DST_SIZES": ("psize_bin", "_rev"),
    "PHIST_SRC_IPT": ("ipt_bin", ""),
    "PHIST_DST_IPT": ("ipt_bin", "_rev"),
}

RENAME = {
    "DST_IP": "dst_ip",
    "DST_ASN": "dst_asn",
    "SRC_PORT": "src_port",
    "DST_PORT": "dst_port",
    "QUIC_VERSION": "quic_version",
    "TIME_FIRST": "time_first",
    "DURATION": "duration",
    "BYTES": "bytes",
    "BYTES_REV": "bytes_rev",
    "PACKETS": "packets",
    "PACKETS_REV": "packets_rev",
    "PPI_LEN": "ppi_len",
    "PPI_DURATION": "ppi_duration",
    "PPI_ROUNDTRIPS": "ppi_roundtrips",
    "APP": "service",
}


def ppi_columns() -> list[str]:
    """The 90 columns of the packet sequence: inter-packet times, directions and sizes of packets 1 to 30."""
    return [f"{prefix}{i:02d}" for _, prefix in PPI_PARTS for i in range(1, PPI_LENGTH + 1)]


def histogram_columns() -> list[str]:
    """The 32 columns of the four packet histograms, named as in the TMA 2023 paper (`psize_bin1`, `ipt_bin8_rev`)."""
    return [f"{prefix}{i}{suffix}" for prefix, suffix in HISTOGRAMS.values() for i in range(1, HIST_BINS + 1)]


def _splitmix64(x: np.ndarray) -> np.ndarray:
    """SplitMix64 of unsigned 64-bit integers: a fixed hash, the same on every machine and parser block."""
    x = x.astype(np.uint64)
    with np.errstate(over="ignore"):
        x = x + np.uint64(0x9E3779B97F4A7C15)
        x = (x ^ (x >> np.uint64(30))) * np.uint64(0xBF58476D1CE4E5B9)
        x = (x ^ (x >> np.uint64(27))) * np.uint64(0x94D049BB133111EB)
        x = x ^ (x >> np.uint64(31))
    return x


def _parse_block(data: bytes, *, header: bool):
    """Parse a block of whole CSV lines of one daily file; every field as text."""
    import polars as pl

    return pl.read_csv(
        data,
        has_header=header,
        new_columns=None if header else list(COLUMNS),
        schema=None if header else dict.fromkeys(COLUMNS, pl.String),
        infer_schema=False,
    )


def _type_sample(frame):
    """Type the kept rows: numbers, times and flags; the packet sequence and the histograms as one column per value.

    The packet values are 32-bit floats (sizes up to 1,500 bytes and times in milliseconds are exact), missing beyond
    the flow's first packets; the histogram counts are 32-bit integers.
    """
    import polars as pl

    frame = frame.with_columns(
        *[pl.col(c).cast(pl.Int64, strict=True) for c in INT_COLUMNS],
        *[pl.col(c).cast(pl.Float64, strict=True) for c in FLOAT_COLUMNS],
        *[pl.col(c).replace_strict({"True": True, "False": False}, return_dtype=pl.Boolean) for c in BOOL_COLUMNS],
        *[pl.col(c).str.to_datetime("%Y-%m-%dT%H:%M:%S%.f", time_unit="us", strict=True) for c in TIME_COLUMNS],
    )
    # PPI is "[[times], [directions], [sizes]]": one list per part, as long as the flow's first packets (at most 30).
    parts = pl.col("PPI").str.strip_prefix("[[").str.strip_suffix("]]").str.split("], [")
    exprs = []
    for k, (_, prefix) in enumerate(PPI_PARTS):
        values = parts.list.get(k).str.split(", ").list.eval(pl.element().filter(pl.element() != "").cast(pl.Int64))
        exprs += [
            values.list.get(i, null_on_oob=True).cast(pl.Float32).alias(f"{prefix}{i + 1:02d}")
            for i in range(PPI_LENGTH)
        ]
    for name, (prefix, suffix) in HISTOGRAMS.items():
        values = pl.col(name).str.strip_prefix("[").str.strip_suffix("]").str.split(", ").cast(pl.List(pl.Int64))
        exprs += [values.list.get(i).cast(pl.Int32).alias(f"{prefix}{i + 1}{suffix}") for i in range(HIST_BINS)]
    frame = frame.with_columns(exprs)
    lengths = [parts.list.get(k).str.split(", ").list.len() for k in range(len(PPI_PARTS))]
    return frame.with_columns(pl.concat_list(lengths).alias("ppi_list_lengths")).drop(["PPI", *HISTOGRAMS], strict=True)


class CesnetQuic22ServiceClassification1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "Which of 102 web services (Google Search, YouTube, Instagram, a Czech news site, ...) is behind this "
            "encrypted QUIC connection, judged from its traffic without reading its handshake?"
        ),
        use_case=(
            "An internet provider's flow monitoring labels each exported flow record of a QUIC connection on its "
            "backbone with the web service behind it, for traffic reporting, accounting and auditing flows whose "
            "server name it cannot read (Encrypted Client Hello hides it, or it is faked), without decrypting the "
            "connection's first packet; for example with a model refit every few days on the flows whose server "
            "name it could still read."
        ),
        row=(
            "One QUIC connection to a server on port 443 (a flow record, exported when idle for 65 s or after 5 "
            "minutes) on the backbone of CESNET2, the Czech research and education network of about half a million "
            "users, 31 October to 27 November 2022; a fixed 1-in-20 sample of the release's 140M service flows, of "
            "which this version uses 2.5M."
        ),
        predicted=(
            "The web service, from the connection's server name mapped by the authors' list of each service's "
            "domains (102 services; flows of other services are left out)."
        ),
        known=(
            "The sizes, directions and gaps of the first 30 packets; the bytes and packets each way, the duration "
            "and why the record ended; histograms of all packet sizes and gaps; the QUIC version; the client port; "
            "the server's address and network (autonomous system); the start time."
        ),
        split=(
            "Each test window is one of the last three 4-day periods (16 to 27 November 2022), up to 500,000 flows "
            "each; training is a random million of all earlier flows."
        ),
        changes=(
            "We leave out the server name and the user agent (both read from the decrypted handshake), the flows of "
            "services outside the 102, and the client's address; the packet lists become one column per packet and "
            "value, and the times are Prague time."
        ),
        fit="approximate",
        fit_reason=(
            "The flow records, features and server-name labels are what such a monitor exports. Gaps: a closed world "
            "(flows of services outside the 102 are left out, so no unknown service is tested); the class mix is the "
            "release's per-service sampling, not the network's; one network over four weeks."
        ),
    )

    # Dataset
    unique_name = "cesnet_quic22_service_classification_1m"
    version_of = "cesnet_quic22_service_classification"
    version_comment = """
        We sample twice. Before the split, `_prepare_raw_files` keeps a fixed 1-in-20 hash sample of the release's 153,226,273 flows (the SplitMix64 hash of each flow's unique `ID`, so the sample is the same on every run and parser block): 7,663,274 flows, 7,026,437 of the 102 services after `_clean`. Then the v2 split protocol samples per test window: each 4-day window keeps at most 500k of its 684k to 1.29M flows, and its train side is a random 1M of all earlier flows (4.19M to 6.17M), stratified on the service and drawn in one random order for all windows; the frame keeps only the rows a split uses. The 1-in-20 sample changes no expected class share and leaves every window and train side above its budget.

        Departure: the definitions guide asks that a temporal frame is not sampled before the split (a Should); we sample it because the 28 daily files hold 153M flows (89 GB unpacked) that no build can hold. The hash sample keeps every day and every service at the same rate: the class shares of the sample match the release's per window (chi-square over 102 classes, p 0.35 to 0.99 on the test windows and train sides).
    """
    year = "2022"
    domain = "technology & internet"
    source = "Other"
    source_url = "https://doi.org/10.5281/zenodo.7409923"
    license = "CC BY 4.0"
    data_tags = ()
    download_description = """
        We download the release from Zenodo (record 10728760 of 2024-02-29, the latest version of concept 7409923; its zip is the same file as in the first version of 2022-12-07: 20,952,008,298 bytes, md5 2d52ad44ddb22645a3464634fc54bb9c) and `servicemap.csv` (md5 89b5080480db4be0c31bbbbdedd62451). `_prepare_raw_files` reads the 28 daily CSVs from the zip without unpacking it.

        mkdir -p local-data-warehouse/cesnet_quic22_service_classification && cd local-data-warehouse/cesnet_quic22_service_classification && wget -O cesnet-quic22.zip "https://zenodo.org/records/10728760/files/cesnet-quic22.zip?download=1" && wget -O servicemap.csv "https://zenodo.org/records/10728760/files/servicemap.csv?download=1"
    """
    bibtex = """
        @article{luxemburk2023cesnetquic22,
          author = {Luxemburk, Jan and Hynek, Karel and {\\v{C}}ejka, Tom{\\'a}{\\v{s}} and Luka{\\v{c}}ovi{\\v{c}}, Andrej and {\\v{S}}i{\\v{s}}ka, Pavel},
          title = {{CESNET-QUIC22}: A large one-month {QUIC} network traffic dataset from backbone lines},
          journal = {Data in Brief},
          volume = {46},
          pages = {108888},
          year = {2023},
          doi = {10.1016/j.dib.2023.108888},
        }
    """
    curation_comments = """
        We start with `cesnet-quic22.zip` from Zenodo (10.5281/zenodo.7409923): 28 daily CSVs with 153,226,273 QUIC flows of the CESNET2 backbone, 31 October to 27 November 2022, each labelled with a web service from its SNI domain (Luxemburk et al., Data in Brief 2023).

        - Prediction point: the flow record is exported (the connection idle for 65 s, or 5 minutes of activity), and the monitor labels the record (for reporting, accounting and audit, not inline enforcement) with a service from what it reads without decrypting the handshake: the packet sizes, directions and gaps, the flow's counters and histograms, the QUIC version in the clear header, the ports and the server's address. The labels it trains on come from the server names it can still read; a test flow's own server name is not an input. Potential leak, kept on purpose: the flow's counters (`duration`, bytes and packets each way), `flow_end_reason` and the packet histograms exist only once the flow ends, which the export point allows; at a point right after the first 30 packets, without these whole-flow columns and `time_first`, a LightGBM scores mean log loss 0.260 against 0.220 with the shipped features (3 windows, review panel's task gamer).
        - Download: the whole release (all four weeks are training history for the windows). `_prepare_raw_files` reads the 28 daily files once and keeps a fixed 1-in-20 hash sample of the flows by their unique `ID` (7,663,274 flows; no `ID` repeats in it), plus the count of all flows per hour and service for the window table (version comment).
        - Rows: the 102 services of the authors' list. We drop the three background classes (`google-background`, `facebook-background`, `default-background`: 8.3% of the release, sampled 1 in 15), the flows of other services that the data article keeps "for open-world scenarios" (Sect. 3.1); the evaluation paper trains and scores on the 102 services (Table I, 102 outputs in its appendix) and names unknown classes as a limitation (Sect. VI).
        - We drop `QUIC_SNI`, the server name the label is mapped from by `servicemap.csv` (each of the 36,948 names in the sample maps to one class), and `QUIC_USERAGENT` (0.2% of the flows), read like it from the decrypted first packet, which the use case does not read (LEAK-10). `CATEGORY` is a function of the service and leaves.
        - We drop the flow `ID` and the client's address (`SRC_IP`, anonymised by Crypto-PAn per the data article) (CLEAN-3), and `TIME_LAST`, the start plus `DURATION` (within 30 microseconds).
        - Constant over the task rows (CLEAN-5): `PROTOCOL` (17, UDP), `DST_PORT` (443, the authors' filter), the first packet's direction (+1, client to server) and gap (0 ms), and the smallest size bin of both histograms (no packet under 16 bytes; 6 of the 7.0M sampled server-side counts are 1 to 3, none in the shipped frame).
        - The packet sequence ships as published, one numeric column per packet and value (`ppi_ipt_02` to `ppi_ipt_30` in milliseconds, `ppi_dir_02` to `ppi_dir_30` as +1 client to server and -1 server to client, `ppi_size_01` to `ppi_size_30` in bytes of UDP payload), as the paper's LightGBM reads it ("each packet position in PSTATS as a separate feature", Sect. IV-B); positions past the flow's packet count (`ppi_len`, 2 to 30; 59% of the flows have fewer than 30) are missing, where the paper's CNN pads with zeros. We do not scale, clip or zero out any position (the paper's preprocessing and its no-handshake variant are modelling choices). The directions `ppi_dir_02` to `ppi_dir_30` stay numbers (+1 / -1), a named exception to CLEAN-14's rule that a code is a category: the field's sequence models multiply the sizes by the sign, and the numbers are lossless. The library has no special-feature kind for a packet sequence yet, so it is not declared as one; revisit when one lands.
        - The four packet histograms (8 logarithmic bins of sizes and gaps per direction over the whole flow) ship as 30 count columns named as in the paper (`psize_bin2` to `psize_bin8`, `psize_bin2_rev` ..., `ipt_bin1` to `ipt_bin8_rev`); a direction's size bins sum to its packet count.
        - The three exclusive end-reason flags become `flow_end_reason` (idle timeout 99.5%, active timeout 0.45%, other 0.04%) (CLEAN-12). The QUIC version, a 32-bit code written in decimal, is its hex code (`0x1` 90.0%, version 1; `0xfaceb002`, `0xfaceb001`, `0xfaceb00e`, the versions of Meta's QUIC stacks (mvfst); `0xff00001d`, IETF draft 29; names from the QUIC working group's versions list), categorical; so are the destination address and its autonomous system number (CLEAN-14). The client port stays a number, as in tls_os_fingerprinting_masaryk_1m.
        - Potential shortcut, kept on purpose: the server's address (`dst_ip`, 8,255 addresses among the sampled service flows, 3.4% IPv6) and its autonomous system (`dst_asn`, 487) stay as categories. The monitor sees both in the clear at the prediction point (USE-6), and the paper names a lookup of addresses as a classifier of its own (its "IP baseline", 68.68% accuracy, Table I) and an ensemble with it as future work (Sect. VII); its ML models leave the address out. The address is no label construction (the label comes from the server name; 16.7% of the addresses serve several services, and they carry 62.9% of the flows), but it is the strongest input: a LightGBM on 100k sampled training flows scores log loss 0.507 and 0.544 on the newest and oldest windows without either column, 0.497 and 0.534 with the network, and 0.195 and 0.192 with the address and the network (accuracy 86.1% to 94.4%, macro recall 60.0% to 81.5%; one fit per window, 100k test flows). 99.9% of a window's flows go to an address seen before it. Revisit if the benchmark should measure the side-channel task of the paper's models (drop both columns).
        - The release's times are UTC: each daily file runs from 23:00 UTC of the day before (local midnight) and flows peak at 9 to 12 UTC. We ship `time_first` in Prague time (UTC+1 for every flow), so the windows are the operator's days.
        - Note: the services were sampled at collection, each at its own rate (the top 5% 1 in 15, the bottom 60% not at all; data article Sect. 3.4), so the class mix is softened against the network's. The score uses the release's mix, unweighted (metric reason); the counts before sampling ship with the release.
        - Anomaly: the first two days (31 October, 1 November) hold about half the flows of the later Mondays and Tuesdays, at every hour of the day (3.3M each, against 7.4M to 7.9M), which the source does not explain; they are training history only.
        - Repairs (CLEAN-11): 57 sampled flows (61 cells of `ppi_ipt_03` to `ppi_ipt_30`) hold negative inter-packet gaps down to -4 ms, impossible (most likely packets reordered at capture), set to missing; `dst_asn` 65535 (a reserved number, most likely a failed lookup; 1 sampled flow) is set to missing.
        - Note: 29,987 sampled flows (0.43%) last longer than the 300 s active timeout, up to 360 s, and 8 have a packet-sequence duration a few milliseconds above the flow's; kept as released.
        - Note: rare services stay (TP-8): the stratified 500k test windows hold about 15 to 24 flows of their rarest service (livescore in the oldest window, uber in the two newest), and the ten rarest services hold 0.08% of a test window's flows and 1.5% of a LightGBM's log loss (oldest window, 100k training flows, with the address). No exact copies: over all shipped columns no two of the 2.5M rows are equal. Forced past the default cell budget, the pure-value check finds six server addresses and one network held by a single service (Instagram's 157.240.30.63, Spotify's 35.186.224.25, Google's public resolvers 8.8.8.8 and 8.8.4.4 for `dns-doh`, Apple's network 36183 for `apple-privaterelay`, ...): dedicated servers, the address's signal.
        - Note: the task is not trivial (TP-4) and not solved, though the task probe flags `solved` on its macro ROC AUC (0.998 for LightGBM, an average of 102 one-against-the-rest scores): on the declared log loss LightGBM scores 0.202, a random forest 0.677, a linear model 0.772, the class shares 3.542 (3 shipped windows, 100k rows per side, LightGBM with a minimum child weight of 1: the untuned default diverged to 24.7). The best single feature is the address (1.041), and the address as a lookup of each server's earlier services scores 0.83 to 0.86 (68.5% to 70.3% accuracy, the paper's IP baseline: 68.68%).
        - Note: the leak probes find no shortcut beyond the address (stable LightGBM, 20k rows per side, 3 windows): all features macro ROC AUC 0.984, without the address 0.966, the first packets' sizes alone 0.82 to 0.86; the missing indicators (0.582) and the number format (0.649) only repeat the flow's packet count. No test flow has an exact copy in its train side. Probe 13 sees the YouTube share rise on the last weekend (26-27 November), the weekly cycle every earlier weekend shows (6.5% to 7.0% of the flows on weekend days, 4.5% to 5.1% on working days from 2 November), not censoring: the label is set when the connection starts.
    """

    # Task
    target = "service"
    problem_type = "multiclass_classification"
    metric = Metric.fallback(
        reason=(
            "The evaluation paper (Luxemburk, Hynek, Čejka, 'Encrypted traffic classification: the QUIC case', TMA "
            "2023, Sect. IV and V, Tables I and II) reports accuracy, provider-level accuracy, macro F1 and macro "
            "recall side by side and names none as the criterion (MET-5); all four score hard labels without a "
            "threshold or costs (MET-6), and its footnote 2 says accuracy and F1 depend on the per-service sampling "
            "of the release, while recall does not. The data article (Data in Brief 2023) and the Zenodo page define "
            "no metric. The score is the release's class mix, unweighted (MET-16): the sampling ratios are a design "
            "weight of the collection, and the task is not a population estimate. The class mix comes from the "
            "source's per-service sampling, so it does not carry over to a network (TMA footnote 2)."
        )
    )

    # Splits
    splits_comment = """
        We use each of the last three 4-day periods (16 to 19, 20 to 23 and 24 to 27 November 2022, Prague days of the flow's first packet) as a test window, newest first, and all earlier flows as train data; the horizon is 4 days. The evaluation paper trains one model on the first week and tests it on each of the next three (TMA 2023, Sect. IV-V), which trains on 21% of the service flows and scores one model on three periods. SPLIT-14 asks for at least three windows that each train on at least half of the data: weekly windows cannot give them (the week of 14 November trains on 49.2% of the 140M service flows, the week of 7 November on 21.4%), and four days is the widest length that can (the windows train on 59.7%, 69.4% and 87.8%; five days would leave the oldest at 47.3%). A refit every few days is a plausible cadence for a monitor that labels its training flows from the server names it can still read, and the paper's own drift (Google's certificate change in the second week) built up within days. No gap: the label is the server name of the connection's own first packet, known when the flow record is exported. Each window keeps at most 500k of its flows and each train side is a random 1M of all earlier flows (one random order, stratified by the service), drawn from the fixed 1-in-20 sample of the release.

        Notes: 31 October and 1 November are a capture break (half the flows of later days at every hour, a different class mix: Instagram about 10% of the flows against about 4.5% later); they are training history only, and dropping them gains a LightGBM 0.007 to 0.012 log loss, near noise, so they stay. The oldest test window (16 to 19 November) holds the Czech public holiday of 17 November and the bridge day after it, so its class mix leans to a weekend's. Shifts of the release's per-service sampling rates over the month show as drift. Training on only the last 8 days before a window gains about 0.03 log loss: the training history is the participant's choice.
    """
    temporal = Temporal(on="time_first", splits=TemporalSplits(window=4, unit="days", n_windows=3))
    row_budget = RowBudget(train=1_000_000, test=500_000)

    prepared_raw_files = (SAMPLE_FILE, COUNTS_FILE)

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        # One pass over the 28 daily CSVs inside the zip (a gzip file each), block by block: the fixed 1-in-20 hash
        # sample of the flows (by `ID`), typed, and the number of all flows per hour of their start and service.
        import polars as pl

        samples, counts = [], []
        with zipfile.ZipFile(raw_dir / ZIP_NAME) as zf:
            names = sorted(n for n in zf.namelist() if re.search(r"/flows-\d{8}\.csv\.gz$", n))
            for name in names:
                with zf.open(name) as member, gzip.open(member) as handle:
                    header = handle.readline().decode().strip().split(",")
                    if tuple(header) != COLUMNS:
                        msg = f"{name}: unexpected header {header}"
                        raise ValueError(msg)
                    rest = b""
                    while True:
                        buf = handle.read(CHUNK_BYTES)
                        data = rest + buf
                        if buf:
                            cut = data.rfind(b"\n") + 1
                            data, rest = data[:cut], data[cut:]
                        else:
                            rest = b""
                        if not data.strip():
                            if not buf:
                                break
                            continue
                        block = _parse_block(data, header=False)
                        counts.append(
                            block.group_by(
                                [pl.col("TIME_FIRST").str.slice(0, 13).alias("hour"), "APP"], maintain_order=True
                            )
                            .len()
                            .with_columns(pl.col(pl.String).cast(pl.Categorical))
                        )
                        ids = block["ID"].cast(pl.UInt64, strict=True).to_numpy()
                        keep = (_splitmix64(ids) % np.uint64(SAMPLE_ONE_IN)) == 0
                        # The kept rows' text goes to categories: a filtered text column would hold the whole block.
                        kept = _type_sample(block.filter(pl.Series(keep))).with_columns(
                            pl.col(pl.String).cast(pl.Categorical), pl.lit(name.split("/")[-1]).alias("file")
                        )
                        samples.append(kept)
                        if not buf:
                            break
        sample = pl.concat(samples, how="vertical").with_columns(pl.col(pl.Categorical).cast(pl.String))
        sample.sort(["TIME_FIRST", "ID"], maintain_order=True).write_parquet(raw_dir / SAMPLE_FILE)
        count = (
            pl.concat(counts)
            .with_columns(pl.col(pl.Categorical).cast(pl.String))
            .group_by(["hour", "APP"], maintain_order=True)
            .agg(pl.col("len").sum())
        )
        count.sort(["hour", "APP"]).write_parquet(raw_dir / COUNTS_FILE)

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        import pyarrow.parquet as pq

        text = ["SRC_IP", "DST_IP", "QUIC_VERSION", "QUIC_SNI", "QUIC_USERAGENT", "APP", "CATEGORY", "file"]
        return pq.read_table(raw_dir / SAMPLE_FILE, read_dictionary=text).to_pandas()

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        import numpy as np

        # Guard: each of the three packet lists is as long as the packet count the release gives (PPI_LEN).
        lengths = np.stack(raw["ppi_list_lengths"].to_numpy())
        assert (lengths == raw["PPI_LEN"].to_numpy()[:, None]).all()
        df = raw.rename(columns=RENAME)

        # 1. Rows: the flows of the 102 services. The three background classes (Google, Facebook and other services
        #    outside the authors' list) are for open-world studies; the paper's task is the 102 services.
        df = df[~df["service"].astype("string").str.endswith("-background")].copy()

        # 2. The time of the first packet: the release writes UTC (each daily file runs from 23:00 UTC of the day
        #    before, local midnight); we ship Prague time, UTC+1 for every flow (summer time ended on 30 October
        #    2022 at 01:00 UTC, before the first flow), so the days of the windows are the operator's days.
        df["time_first"] = df["time_first"].dt.tz_localize("UTC").dt.tz_convert("Europe/Prague").dt.tz_localize(None)

        # 3. The flow's end reason: three exclusive flags (exactly one is set on every flow) as one category.
        reasons = df[["FLOW_ENDREASON_IDLE", "FLOW_ENDREASON_ACTIVE", "FLOW_ENDREASON_OTHER"]].to_numpy()
        assert (reasons.sum(axis=1) == 1).all()
        df["flow_end_reason"] = np.array(["idle timeout", "active timeout", "other"])[reasons.argmax(axis=1)]

        # 4. The QUIC version, a 32-bit code the release writes in decimal, in hex as the protocol writes it (0x1 is
        #    QUIC version 1, 0xff00001d draft 29, 0xfaceb00x the versions of Meta's QUIC stacks, mvfst).
        # 4b. Repairs: negative inter-packet gaps (61 cells, packets reordered at capture) and the reserved network
        #     number 65535 (a failed lookup) become missing (CLEAN-11).
        ipt = [c for c in df.columns if c.startswith("ppi_ipt_")]
        df[ipt] = df[ipt].mask(df[ipt] < 0)
        df["dst_asn"] = df["dst_asn"].astype("Int64").mask(df["dst_asn"] == 65535)
        df["quic_version"] = df["quic_version"].astype("string").map(lambda v: hex(int(v)), na_action="ignore")

        # 5. Columns that leave:
        #    - the server name (SNI), which the label is mapped from, and the user agent, read like it from the
        #      decrypted first packet; the service category, a function of the label (LEAK-10);
        #    - the flow id and the client's anonymised address (CLEAN-3); the end time, the start plus `duration`;
        #    - the constants: the protocol (UDP), the server port (443, the authors' filter), the first packet's
        #      direction (client to server) and gap (0), the smallest size bin of both directions (no packet under
        #      16 bytes; 6 server-side counts of 1 to 3 in the 7.0M sampled flows, none in the shipped frame) (CLEAN-5); the end-reason flags (step 3) and the list lengths of the guard.
        return drop_columns(
            df,
            [
                "QUIC_SNI",
                "QUIC_USERAGENT",
                "CATEGORY",
                "ID",
                "SRC_IP",
                "TIME_LAST",
                "PROTOCOL",
                "dst_port",
                "ppi_dir_01",
                "ppi_ipt_01",
                "psize_bin1",
                "psize_bin1_rev",
                "FLOW_ENDREASON_IDLE",
                "FLOW_ENDREASON_ACTIVE",
                "FLOW_ENDREASON_OTHER",
                "ppi_list_lengths",
                "file",
            ],
        )

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=["dst_ip", "dst_asn", "quic_version", "flow_end_reason"],
            datetime=["time_first"],
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        import pandas as pd

        counts = pd.read_parquet(self.raw_dir / COUNTS_FILE)
        # The hour of the first packet, UTC in the release, as the Prague day (UTC+1 for every flow; `_clean`).
        counts["day"] = (pd.to_datetime(counts["hour"], format="%Y-%m-%dT%H") + pd.Timedelta(hours=1)).dt.floor("D")
        counts["background"] = counts["APP"].str.endswith("-background")
        service = counts[~counts["background"]]
        total = service["len"].sum()

        # The window designs: weekly windows (the paper's test weeks) against the shipped 4-day windows.
        designs = []
        for design, starts, days in (
            ("weekly (the paper's test weeks)", ("2022-11-21", "2022-11-14", "2022-11-07"), 7),
            ("4 days (shipped)", ("2022-11-24", "2022-11-20", "2022-11-16"), 4),
        ):
            for start in starts:
                begin = pd.Timestamp(start)
                end = begin + pd.Timedelta(days=days)
                designs.append(
                    {
                        "design": design,
                        "test window": f"{begin:%d %b} to {end - pd.Timedelta(days=1):%d %b %Y}",
                        "service flows in the window": int(
                            service.loc[service["day"].between(begin, end, "left"), "len"].sum()
                        ),
                        "train share of all service flows": round(
                            float(service.loc[service["day"] < begin, "len"].sum() / total), 3
                        ),
                    }
                )
        windows = pd.DataFrame(designs)

        # The background classes against the 102 services, per week of the flow's start.
        counts["week"] = counts["day"].dt.isocalendar().week.astype(int)
        background = counts.pivot_table(index="week", columns="background", values="len", aggfunc="sum")
        background.columns = ["flows of the 102 services", "background flows (3 classes)"]
        background["background share"] = (background.iloc[:, 1] / background.sum(axis=1)).round(3)
        return [
            Decision(
                "Test windows of four days",
                "SPLIT-14 asks for three windows that each train on at least half of the data; weekly windows over "
                "four weeks leave the second and third newest week below it, four days is the widest length that keeps "
                "three windows above it (counts of all 140M service flows of the release, by the Prague day of the "
                "flow's first packet).",
                windows,
            ),
            Decision(
                "Background flows left out",
                "The three background classes hold flows of services outside the authors' 102, for open-world "
                "studies; the paper's classifiers are trained and scored on the 102 services only (counts of the "
                "release by ISO week of the flow's first packet).",
                background,
            ),
        ]
