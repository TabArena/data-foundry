"""Curated dataset definition for `tls_os_fingerprinting_masaryk_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import re
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    RowBudget,
    ScoringColumn,
    TaskSummary,
    Temporal,
    TemporalSplits,
    UnitWeight,
    drop_columns,
)

ZIP_NAME = "flows_dataset_anonymized.zip"
PREPARED = "flows_all.parquet"

# The release's column names (one header for all 120 hourly CSVs) and ours.
RENAME = {
    "Date flow start": "flow_start",
    "Date flow end": "flow_end",
    "Src IPv4": "src_ip",
    "sPort": "src_port",
    "Dst IPv4": "dst_ip",
    "dPort": "dst_port",
    "SYN size": "syn_size",
    "TCP win": "tcp_window",
    "TCP SYN TTL": "syn_ttl",
    "TLS SNI": "tls_sni",
    "TLS SNI length": "tls_sni_length",
    "TLS Client Version": "tls_client_version",
    "Client Cipher Suites": "tls_cipher_suites",
    "TLS Extension Types": "tls_extension_types",
    "TLS Extension Lengths": "tls_extension_lengths",
    "TLS Elliptic Curves": "tls_elliptic_curves",
    "TLS EC Point Formats": "tls_ec_point_formats",
    "HTTP Host": "http_host",
    "HTTP UA OS": "http_ua_os",
    "HTTP UA OS MAJ": "http_ua_os_major",
    "HTTP UA OS MIN": "http_ua_os_minor",
    "HTTP UA OS BLD": "http_ua_os_build",
    "SSH Client Version": "ssh_client_version",
    "SSH Client Application": "ssh_client_application",
    "SSH Client Encryption": "ssh_client_encryption",
    "SSH Client MAC": "ssh_client_mac",
    "SSH Client Compression": "ssh_client_compression",
    "Session ID": "session_id",
    "Ground Truth OS": "os",
}
INT_COLUMNS = ("sPort", "dPort", "SYN size", "TCP win", "TCP SYN TTL", "TLS SNI length", "Session ID")
DATE_COLUMNS = ("Date flow start", "Date flow end")

# GREASE values (RFC 8701): two equal bytes of the form 0x?A, sent at random by a client to keep servers tolerant.
GREASE = re.compile(r"^([0-9a-f])a\1a$")
# The probe stores each list as fixed-width little-endian 16-bit fields, padded to the end with one filler value.
LIST_PADDING = {
    "tls_cipher_suites": "0000",
    "tls_extension_types": "ffff",
    "tls_extension_lengths": "ffff",
    "tls_elliptic_curves": "0000",
}


def _decode_id_list(blob: str, padding: str, *, as_int: bool = False) -> str:
    """One packed list of the probe as comma-separated values: the 16-bit IDs in hex (big-endian, as the TLS
    registries write them) or the lengths in decimal, the trailing padding removed and GREASE values named. A
    padding value before the end is a real value (one client offers the cipher suites 0x0000 to 0x0007).
    """
    if len(blob) % 4:
        msg = f"A packed TLS list must hold whole 16-bit fields: {blob!r}."
        raise ValueError(msg)
    fields = [blob[i : i + 4].lower() for i in range(0, len(blob), 4)]
    while fields and fields[-1] == padding:
        fields.pop()
    values = []
    for field in fields:
        value = field[2:4] + field[0:2]  # little-endian to big-endian
        if as_int:
            values.append(str(int(value, 16)))
        else:
            values.append("GREASE" if GREASE.match(value) else value)
    return ",".join(values)


def _decode_point_formats(code: str) -> str:
    """The EC point formats field, a 4-byte number, as its list of formats: the bytes before the first 0xFF filler
    (16777215 = 0x00FFFFFF is [0]); all filler (4294967295) is the empty list: the client sent no such extension.
    """
    value = int(code)
    formats = []
    for byte in value.to_bytes(4, "big"):
        if byte == 0xFF:
            break
        formats.append(str(byte))
    return ",".join(formats) if formats else ""


def _map_categories(s: pd.Series, fn) -> pd.Series:
    """Apply `fn` to each distinct value of a categorical column (a many-to-one map is allowed)."""
    cats = s.cat.categories
    mapped = np.array([fn(c) for c in cats], dtype=object)
    uniques, inverse = np.unique(mapped, return_inverse=True)
    codes = s.cat.codes.to_numpy()
    new_codes = np.where(codes >= 0, inverse[np.maximum(codes, 0)], -1)
    return pd.Series(pd.Categorical.from_codes(new_codes, categories=uniques), index=s.index, name=s.name)


class TlsOsFingerprintingMasaryk1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "Which operating system (Android, iOS, Mac OS, Windows or Windows Phone) runs on the device behind this "
            "Wi-Fi session, read from one of its connections' flow records?"
        ),
        use_case=(
            "A university's network security team runs flow monitoring on its campus Wi-Fi and records the operating "
            "system of each device per Wi-Fi session, for its inventory of the systems on the network, from what the "
            "flow monitor reads of the device's connections; for example, the model is refit twice a day on the "
            "flows labelled so far."
        ),
        row=(
            "One TCP connection whose SYN packet the flow monitor saw (a flow record of up to 5 minutes) from a "
            "device on Masaryk University's Eduroam Wi-Fi, 12 to 16 July 2019: 13.3M of the release's 18.7M flows, "
            "of which this version samples 2.5M."
        ),
        predicted=(
            "The device's operating system as the authors derived it from the host name the device gave the "
            "university's DHCP server when it connected (five classes)."
        ),
        known=(
            "The SYN packet's size, window and time to live, the ports, the flow's start and duration, and when "
            "present the TLS ClientHello (version, offered ciphers, extensions, curves, point formats, server name), "
            "the host of a plain-text HTTP request and the SSH client's software and algorithms."
        ),
        split=(
            "Each test window is one of the last three half-days (15 July noon to 16 July midnight), up to 500,000 "
            "flows each; training is a random million of all earlier flows. Each Wi-Fi session carries the same "
            "weight in a window's score (before the window is sampled to 500k flows)."
        ),
        changes=(
            "We keep the flows with TCP SYN fields, drop the User-Agent's OS fields (the device's own statement of "
            "its OS) and the addresses, decode the packed TLS lists into protocol IDs, set impossible or filler "
            "values to missing, and weight each flow by 1 over its session's flows in the half-day."
        ),
        fit="approximate",
        fit_reason=(
            "The inputs are what a flow monitor reads in the clear, and the windows follow a refit. Gaps: every test "
            "device already has its DHCP label, standing in for the unlabelled devices the model would serve; those "
            "host names are editable on Windows and name no OS version; the unit is a session per half-day, not a "
            "device; one network over five days; no Linux."
        ),
    )

    # Dataset
    unique_name = "tls_os_fingerprinting_masaryk_1m"
    version_of = "tls_os_fingerprinting_masaryk"
    version_comment = """
        We sample per test window (v2 split protocol): each half-day test window keeps at most 500k of its 1.08M to 2.06M task flows, and its train side is a random 1M of all earlier task flows (8.2M to 11.4M), drawn in one random order for all windows and stratified by the target; the frame keeps only the rows a split uses (2.5M). A random draw over the whole history keeps both weekdays and the weekend in every train side.
    """
    year = "2019"
    domain = "technology & internet"
    source = "Other"
    source_url = "https://doi.org/10.5281/zenodo.3461771"
    license = "CC BY 4.0"
    data_tags = ()
    download_description = """
        We download the release from Zenodo (record 3461771 of 2019-09-26, one zip of 700,767,981 bytes, md5 ebb0f2c0117193e43d9089d613748c7f); `_prepare_raw_files` reads its 120 hourly CSVs from the zip.

        mkdir -p local-data-warehouse/tls_os_fingerprinting_masaryk && wget -O local-data-warehouse/tls_os_fingerprinting_masaryk/flows_dataset_anonymized.zip "https://zenodo.org/records/3461771/files/flows_dataset_anonymized.zip?download=1"
    """
    bibtex = """
        @misc{lastovicka2019tlsdataset,
          author = {La{\\v{s}}tovi{\\v{c}}ka, Martin and {\\v{S}}pa{\\v{c}}ek, Stanislav and Velan, Petr and {\\v{C}}eleda, Pavel},
          title = {Dataset Using {TLS} Fingerprints for {OS} Identification in Encrypted Traffic},
          year = {2019},
          publisher = {Zenodo},
          doi = {10.5281/zenodo.3461771},
          howpublished = {\\url{https://doi.org/10.5281/zenodo.3461771}},
        }
    """
    curation_comments = """
        We start with `flows_dataset_anonymized.zip` from Zenodo (10.5281/zenodo.3461771): 120 hourly CSVs with 18,708,983 flow records of Masaryk University's Eduroam devices, 12 to 16 July 2019, each enriched with its Wi-Fi session and the OS from the DHCP logs (Laštovička et al., "Using TLS Fingerprints for OS Identification in Encrypted Traffic", NOMS 2020, Sect. IV).

        - Prediction point: a flow record is exported (at the connection's end, or after 5 minutes of activity: every duration stops at 300 s), and the monitoring system labels it with the OS of the device behind it from what the flow monitor read in the clear: the TCP SYN packet, the TLS ClientHello, a plain-text HTTP host, an SSH banner. The device's identity (its address, its session) is not an input.
        - We keep the 13,309,494 flows (71.1%) that carry the TCP SYN fields (size, window, TTL), the inputs of the paper's TCP/IP method, which "depends on network and transport layer information" (Sect. VI.A); the other 5.4M (UDP, or TCP whose SYN the probe did not see) carry only ports and times (USE-7). The TLS flows are among them, but for 1,662 of 9,515,666.
        - We drop the four HTTP User-Agent OS fields (`HTTP UA OS`, `MAJ`, `MIN`, `BLD`): a code the probe parses from a plain-text User-Agent, the device's own statement of its OS. Where it names an OS (4.1% of the task flows; 65535 means unknown) it names the label's majority class for 96.5% of them, and the paper's User-Agent method scores 0.9764 accuracy (Table III); its ML methods use the User-Agent as their training label (Sect. V.B). The task is the OS from encrypted traffic, the paper's aim (LEAK-10).
        - We drop the source address (the device's anonymised address, one per session, reused across sessions and devices: 1,724 of 6,165 addresses carry several OS labels over the five days) and the session id, identifiers of the device (CLEAN-3). The source address alone scores macro ROC AUC 0.921 on the shipped splits: it names the device, not its stack. The session id gives the session weight and an opaque id of the session's half-day (`session_window`, the unit of the weight, never a feature), and leaves.
        - We drop the destination address, the server's address under Crypto-PAn: an opaque id of 138,681 values, 79,163 of them seen by one session only (the device's own peers). Next to the server names (SNI and HTTP host) it adds nothing consistent: as a category it moves a LightGBM's session-weighted log loss by -0.0023, -0.0009 and +0.0023 on the three shipped windows (31 leaves; -0.0011, -0.0001, -0.0016 with 4 leaves). 22.4% of the task flows carry neither name; its gain on them alone was not measured (CLEAN-3).
        - The flow's end time becomes `flow_duration_s` (end minus start, 0 to 300 s); the start stays as `flow_start`.
        - The probe stores each TLS list as fixed-width little-endian 16-bit fields padded at the end (cipher suites: the first 8, padded with 0000; extension types and lengths: 28 slots, padded with ffff; supported groups: the first 8, padded with 0000), shipped as hex strings (`4a4a0113...`). We decode them into comma-separated IDs as the TLS registries write them (`GREASE,1301,1302,1303,c02b,...`; lengths in decimal), drop the trailing padding (a padding value inside a list stays: one client offers the ciphers 0x0000 to 0x0007), and name the GREASE values (RFC 8701: 0x0a0a, 0x1a1a, ..., 0xfafa, drawn at random by Chrome-based clients for each connection) `GREASE`, as JA3 fingerprints ignore them: the extension type lists fall from 8,243 to 469 distinct values, the cipher lists from 402 to 311 (CLEAN-12).
        - `tls_ec_point_formats` is a 4-byte number whose bytes up to the first 0xff are the formats (16777215 = 0x00ffffff is `0`, 66303 is `0,1,2`, 131071 is `0,1`); 4294967295, all filler, is no extension (`none`, 764,225 flows, none of whose extension lists holds 0x000b).
        - An empty list is `none` where the ClientHello was parsed (its version is known): no extensions (SSLv3, old TLS clients: 2,823 flows), no supported groups (12,130). Where the version is missing the lists are all filler, so the probe parsed no ClientHello: missing (3,829 flows), as are the 94 empty cipher lists of SSLv2 ClientHellos, whose cipher specs the probe does not parse.
        - We drop `ssh_client_version`, constant (2.0) over the task flows (CLEAN-5). The other four SSH fields stay, filled on 186 or 187 flows: columns leave for what they are, not for how few rows hold them (CLEAN-22).
        - Dtypes: the source port is numeric (its range differs by OS: 63.7% of Android flows fall in 32768-49151, 0.1% of Windows flows); the destination port is categorical, a service code (443, 5223 for Apple push, 5228 for Google push; the ten most common hold 96.9% of the rows) (CLEAN-14). The SYN size, window and TTL are numeric, as in the paper (it rounds the TTL up to a power of two, which we leave to the models), and so is the SNI length. The TLS version and the ID lists (cipher suites, extension types, supported groups, point formats) are categorical, as the paper encodes every TLS field (Sect. V.A); the server names (SNI, HTTP host) and the extension lengths (11,601 distinct lists, lengths that vary per connection) are strings.
        - The SYN size is the IP packet's length, at least 40 bytes for an IPv4 TCP SYN: 328 task flows (300 of them Windows) hold 2 to 34 bytes, set to missing with the rows kept (CLEAN-11). The SNI length is 0, the probe's filler, on the 3,829 task flows where no ClientHello was parsed (its version missing); set to missing like the lists (CLEAN-10).
        - `tls_client_version` is the ClientHello's legacy version, so TLS 1.3 clients show as TLSv1.2 (paper Sect. III): 49% of the shipped TLSv1.2 rows offer TLS 1.3 (extension 0x002b). The release cuts the SNI at 64 bytes (5,998 task flows); `tls_sni_length` keeps the full length.
        - Note: the SNI and the HTTP host stay: the paper's "specific domains" method reads them (0.8659 accuracy, Table III), and a monitor sees them in the clear at the prediction point (USE-6); alone, as text, the SNI scores macro ROC AUC 0.776 and the HTTP host 0.533 (leak probe, 3 shipped splits).
        - Note: the paper trains on the first day and tests on the other four (Sect. V.B); we use three half-day windows instead (splits comment).
        - Anomaly: the labels come from the host names in the DHCP logs, which "works well for Apple and Google operating systems", while the Windows host name "is readily editable" (Sect. V.C). The release has five classes and no Linux or other OS, although Fig. 4 gives 1.48% Linux and 0.07% other; its shares (Google 39.93%, Apple 30.03%, Microsoft 28.49%) are not the release's flow shares (Android 37.9%, Apple 22.1%, Windows and Windows Phone 39.9%), and the paper does not say what they count.
        - Anomaly: the label disagrees with the TCP stack for some sessions: 141 of 3,154 Windows sessions (260,552 flows, 5.0% of the Windows flows) send most SYNs with a TTL from 64, the start value of Linux, Apple and Android stacks (Windows starts at 128), and 24 Mac OS and 7 Android sessions send most with one from 128. The 141 look like real Windows hosts whose TTL arrives at 64 or less (a host setting or a hop that rewrites it): 137 never send a SYN with a TTL above 64, 205,630 of their 260,552 flows carry the Windows stack's SYN pair (size 52, window 64240), and 103 of them send a User-Agent with the Windows code. Kept as labelled, since a relabelling from the features would be ours.
        - Anomaly: a few busy sessions hold many flows: the largest Windows session has 578,764 task flows (4.3%), the ten largest 12.0%, all Windows; Windows has 39.5% of the flows and 7.0% of the sessions. The score weights each flow by 1 over its session's flows in the half-day (`session_weight`), so Windows holds 23-38% of a test window's flows but 6-8% of its weight. The unit is a session in a half-day, not a device: the paper counts 45,602 sessions of 11,962 devices (MAC addresses, which the release does not hold), so a device with several sessions counts several times. Every test device is one the DHCP host name already labels; the model stands in for the devices whose host names say nothing, which the release cannot contain (USE-8).
        - Note: 0.7% of the test flows have an exact copy in their train side among the numeric and categorical inputs, all with the same label; with the server names and times none has (leak probe 5, the 3 shipped splits). They are distinct connections with the same fingerprint, kept (LEAK-18). Over all columns the shipped frame has 84 duplicate rows (9 with another label), kept for the same reason. Forced past the default cell budget, the pure-value check finds three TLS fingerprints held by Android alone (41,051 to 51,655 shipped flows each, 99.7% to 100%): cipher and extension lists of an Android TLS library, the signal the task rests on.
        - Note: the times are as released, the clock of the flow probe; the hourly files are named by the same hours (the first file also holds 9,263 task flows that started in the last ten minutes of 11 July, kept in the training history).
        - Note: `period`, the flow's start floored to 12 hours, is only the key of the half-day windows: `TemporalSplits` has no hours unit (library gap). It adds nothing beyond `flow_start`, is one value per test window that training never holds, and a naive model that reads both times as numbers loses 0.015 to 0.018 of session-weighted log loss on the shipped windows. It goes once the windows can be cut on `flow_start` in hours (CLEAN-19).
        - Note: the unit weight's check allows a sampled unit's weights to sum to less than 1 under a row budget (library change of 2026-11-09): the weight is computed on all task flows before each window is sampled.
        - Note: the task is not trivial (TP-4): the best single feature (`syn_size`) scores 0.282 session-weighted log loss against 0.133 for a random forest and 0.144 for LightGBM on all features (task probe, 3 shipped windows). The prior of the train side's flows scores 1.43; the prior of its sessions, the honest null for this weighted score, 1.08.
    """

    # Task
    target = "os"
    problem_type = "multiclass_classification"
    metric = Metric.fallback(
        reason=(
            "The paper (Laštovička et al., NOMS 2020, Sect. VI.B, Table III) reports accuracy, precision, recall and "
            "F-score, micro-averaged over the OS names, side by side, with none named as the criterion (MET-5), on "
            "hard labels without a threshold or costs (MET-6); the Zenodo page defines no metric. Each Wi-Fi session "
            "carries the same weight in each test window: a flow weighs 1 over its session's task flows in the "
            "half-day (`session_weight`), since the inventory decides per device, while the paper scores every flow "
            "and one session holds up to 578,764 of them (MET-17). The score's class balance is therefore per "
            "session: Windows holds 23-38% of a test window's flows but 6-8% of its weight, and `validation_weight` "
            "returns the column a validation loss is weighted by alike. The weight moves the ranking of close models: "
            "among 9 to 10 competitive LightGBM fits per window, 17 of 36, 19 of 45 and 19 of 36 pairs swap order "
            "between the per-flow and the per-session score, and the best per flow is never the best per session. "
            "The weight is not a training weight; a model fitted with it scores between 0.008 worse and 0.12 better "
            "than one fitted without it, depending on the model and the encoding."
        ),
        inputs={"weight": "session_weight"},
    )
    scoring_columns = (
        ScoringColumn(
            column="session_weight",
            role="weight",
            used_by="log_loss",
            description=(
                "1 over the number of task flows of the row's Wi-Fi session in the row's half-day, computed on all "
                "task flows, so each session carries the same weight in a test window's log loss before the window "
                "is sampled to 500k flows; its unit is `session_window`; for scoring and validation only, never a "
                "feature or a training weight"
            ),
        ),
    )
    unit_weight = UnitWeight(column="session_weight", unit="session_window")

    # Splits
    splits_comment = """
        We use each of the last 3 half-days (15 July 12:00 to 16 July 24:00, the clock of the release) as a test window, newest first, and all earlier flows as train data; the time key `period` is the flow's start floored to 12 hours, so one window is one step (horizon 1 step, 12 hours). The paper trains on the first day and tests on the other four (Sect. V.B), which trains on 18.8% of the task flows; SPLIT-14 asks for at least three windows on at least half of the data, which daily windows over five days cannot give (the third newest day trains on 35.6%), so we cut half-days: the windows train on 61.7%, 77.2% and 85.3% of the task flows, and a refit twice a day is a plausible cadence for a monitoring system. No gap: the label is known when the device connects (the DHCP request at the session's start), before any of its flows. 16 to 21% of a window's flows belong to a session with flows before the window (6 to 12% of its sessions): the network's devices recur, as they do for the monitoring system. Removing the test window's sessions from its train side worsens the window's score by 0.001 to 0.002 (0.006 to 0.012 on those sessions' own rows), so a model recognises a recurring session only a little. The training flows still open at a cutoff (at most 0.05% of a train pool) are kept: their label was known at connection, and their duration is an input, not the outcome. Trained on the paper's history (a random 1M of day 1) instead, LightGBM scores 0.136 on the same windows against 0.112 with the expanding history: the shipped task is easier than the paper's protocol by the drift over the days. Each window keeps at most 500k of its flows and each train side is a random 1M of all earlier flows (one random order for all windows, stratified by the OS).
    """
    temporal = Temporal(
        on="period",
        splits=TemporalSplits(window=1, unit="unique", n_windows=3),
        horizon=1,
        horizon_unit="steps",
    )
    row_budget = RowBudget(train=1_000_000, test=500_000)

    prepared_raw_files = (PREPARED,)

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        # The 120 hourly CSVs of the zip, in the order of their names, as one parquet file: numbers and dates typed,
        # every other field kept as the release's text. Reading only; no row or column is removed here.
        import polars as pl

        frames = []
        with zipfile.ZipFile(raw_dir / ZIP_NAME) as zf:
            names = sorted(n for n in zf.namelist() if n.endswith("_ground_truth.csv"))
            for name in names:
                frame = pl.read_csv(zf.read(name), infer_schema=False)
                frame = frame.with_columns(
                    *[pl.col(c).cast(pl.Int64, strict=True) for c in INT_COLUMNS],
                    *[pl.col(c).str.to_datetime("%Y-%m-%d %H:%M:%S%.3f", strict=True) for c in DATE_COLUMNS],
                )
                frames.append(frame)
        pl.concat(frames, how="vertical").write_parquet(raw_dir / PREPARED)

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        import pyarrow.parquet as pq

        path = raw_dir / PREPARED
        names = pq.read_schema(path).names
        text = [c for c in names if c not in INT_COLUMNS and c not in DATE_COLUMNS]
        # Text fields as categories: 18.7M rows with few distinct values per field.
        return pq.read_table(path, read_dictionary=text).to_pandas()

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.rename(columns=RENAME)

        # 1. Rows the use case never sees (USE-7): a flow without the TCP SYN fields (UDP, or a SYN the probe missed).
        df = df[df["syn_size"].notna()].copy()
        # An IPv4 TCP SYN is at least 40 bytes (20 IP + 20 TCP): a smaller size is impossible, the row stays (CLEAN-11).
        df["syn_size"] = df["syn_size"].where(df["syn_size"] >= 40)
        # The destination port is a service code (categorical, see `_feature_types`): whole numbers, not floats.
        df["dst_port"] = df["dst_port"].astype("Int64")

        # 2. The HTTP User-Agent OS fields leave (the device's own statement of its OS); the addresses are identifiers;
        #    the end time becomes the duration.
        df["flow_duration_s"] = (df["flow_end"] - df["flow_start"]).dt.total_seconds()
        df = drop_columns(
            df,
            ["http_ua_os", "http_ua_os_major", "http_ua_os_minor", "http_ua_os_build", "src_ip", "dst_ip", "flow_end"],
        )

        # 3. The packed TLS lists decoded into the protocol's IDs (CLEAN-12).
        for col, padding in LIST_PADDING.items():
            as_int = col == "tls_extension_lengths"
            df[col] = _map_categories(df[col], lambda b, p=padding, a=as_int: _decode_id_list(b, p, as_int=a))
        df["tls_ec_point_formats"] = _map_categories(df["tls_ec_point_formats"], _decode_point_formats)
        # An empty list is "none" where the ClientHello was parsed (its version is known): the client sent
        # no such extension (SSLv3, old TLS clients). A cipher list is never empty in a ClientHello, so an empty one,
        # like any list without a parsed version, was not read by the probe and is missing.
        parsed = df["tls_client_version"].notna()
        for col in [*LIST_PADDING, "tls_ec_point_formats"]:
            empty = df[col].astype("string").eq("").fillna(False).to_numpy()
            df[col] = df[col].cat.add_categories(["none"])
            df.loc[empty & parsed.to_numpy(), col] = "none"
            df.loc[empty & ~parsed.to_numpy(), col] = np.nan
            df[col] = df[col].cat.remove_unused_categories()
        df.loc[df["tls_cipher_suites"].eq("none").fillna(False), "tls_cipher_suites"] = np.nan
        # Without a parsed ClientHello the SNI length's 0 is the probe's filler, like the lists (CLEAN-10).
        df["tls_sni_length"] = df["tls_sni_length"].where(parsed)

        # 4. Constant over the task rows (every SSH client offers version 2.0).
        df = drop_columns(df, ["ssh_client_version"])

        # 5. The time key of the windows (half-days), the session weight (1 over the session's flows per half-day) and
        #    its unit, the (session, half-day) pair numbered in a random order, so it encodes neither time nor session.
        df["period"] = df["flow_start"].dt.floor("12h")
        unit = df.groupby(["session_id", "period"], sort=False)
        df["session_weight"] = 1.0 / unit["session_id"].transform("size")
        codes = unit.ngroup().to_numpy()
        df["session_window"] = np.random.default_rng(0).permutation(codes.max() + 1)[codes]
        df = drop_columns(df, ["session_id"])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "dst_port",
                "tls_client_version",
                "tls_cipher_suites",
                "tls_extension_types",
                "tls_elliptic_curves",
                "tls_ec_point_formats",
                "ssh_client_application",
                "ssh_client_encryption",
                "ssh_client_mac",
                "ssh_client_compression",
            ],
            string=["tls_sni", "http_host", "tls_extension_lengths"],
            datetime=["flow_start", "period"],
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        task = raw[raw["SYN size"].notna()]
        ua = task["HTTP UA OS"].astype("string").fillna("(none)")
        ua_table = pd.crosstab(ua, task["Ground Truth OS"].astype("string"))
        ua_table = ua_table.loc[ua_table.sum(axis=1).sort_values(ascending=False, kind="stable").index].head(8)

        period = task["Date flow start"].dt.floor("12h")
        newest = sorted(period.unique())[-3:]
        rows = []
        for start in newest:
            window = task[period == start]
            flows = window.groupby("Ground Truth OS", observed=True).size()
            sessions = window.groupby("Ground Truth OS", observed=True)["Session ID"].nunique()
            for os_name in flows.index:
                rows.append(
                    {
                        "test window": str(start),
                        "os": os_name,
                        "flows": int(flows[os_name]),
                        "flow share": round(flows[os_name] / flows.sum(), 3),
                        "sessions": int(sessions[os_name]),
                        "session share": round(sessions[os_name] / sessions.sum(), 3),
                    }
                )
        return [
            Decision(
                title="The User-Agent's OS fields leave",
                why=(
                    "The probe parses the OS from a plain-text HTTP User-Agent, the device's own statement of its "
                    "OS. Where it names one (any code but 65535, unknown) it names the label's majority class for "
                    "96.5% of the flows; the four fields are dropped. Task flows by the OS code and the label."
                ),
                evidence=ua_table,
            ),
            Decision(
                title="Each session carries the same weight per test window",
                why=(
                    "A few busy Windows sessions hold a large share of the flows (one has 578,764), while most "
                    "sessions are phones. Each flow weighs 1 over its session's flows in the half-day "
                    "(`session_weight`, unit `session_window`), so the log loss gives every session of a window the "
                    "same weight before the window is sampled. Flows and sessions by class in the three test "
                    "windows, before sampling."
                ),
                evidence=pd.DataFrame(rows),
            ),
        ]
