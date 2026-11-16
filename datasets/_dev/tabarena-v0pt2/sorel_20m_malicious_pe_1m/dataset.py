"""Curated dataset definition for `sorel_20m_malicious_pe_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import json
import mmap
import sqlite3
import struct
import zlib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    RowBudget,
    TaskSummary,
    Temporal,
    TemporalSplits,
    decode,
    drop_columns,
)

# The release's split times (config.py of github.com/sophos/SOREL-20M, in seconds since 1970, UTC): training up to
# 2018-11-30 01:49:30, validation up to 2019-01-12 07:54:00, test after it.
TRAIN_VALIDATION_SPLIT = 1543542570.0
VALIDATION_TEST_SPLIT = 1547279640.0
# The fixed sample `_prepare_raw_files` keeps: the files whose sha256 (the hash of the file's bytes, uniform over its
# range whatever the file is) begins with this hex digit, 1 in 16 of the release.
SAMPLE_PREFIX = "0"
VECTOR_FILE = "ember_v2_vectors_sha256_0.parquet"
COUNTS_FILE = "release_counts.json"
N_VALUES = 2381  # the EMBER feature version 2 vector
TAGS = ("adware", "flooder", "ransomware", "dropper", "spyware", "packed", "crypto_miner", "file_infector",
        "installer", "worm", "downloader")  # fmt: skip

# The EMBER feature version 2 layout (ember/features.py of github.com/elastic/ember, PEFeatureExtractor with
# feature_version=2: byte histogram, byte-entropy histogram, strings, general, header, section, imports, exports,
# data directories). The data directories are read by position, in the PE format's order.
DATA_DIRECTORIES = (
    "EXPORT", "IMPORT", "RESOURCE", "EXCEPTION", "SECURITY", "BASERELOC", "DEBUG", "COPYRIGHT", "GLOBALPTR", "TLS",
    "LOAD_CONFIG", "BOUND_IMPORT", "IAT", "DELAY_IMPORT", "COM_DESCRIPTOR",
)  # fmt: skip
HEADER_OPTIONAL = (
    "major_image_version", "minor_image_version", "major_linker_version", "minor_linker_version",
    "major_operating_system_version", "minor_operating_system_version", "major_subsystem_version",
    "minor_subsystem_version", "sizeof_code", "sizeof_headers", "sizeof_heap_commit",
)  # fmt: skip
# The names EMBER v2 hashes for the three one-name header fields, `str(<lief enum>).split(".")[-1]`: the names LIEF
# 0.9.0 gives them (`to_string` in src/PE/EnumToString.cpp; ember's version 2 names that LIEF version), with ARM64, which
# 0.9.0 leaves unnamed and 0.10.0 names, and "???" for a code LIEF does not name (pybind11's "???" and LIEF's
# "Out of range" hash to the same bin and sign). A file LIEF cannot parse gets the empty string in all three.
HASHED_NAMES = {
    "machine": (
        "UNKNOWN", "AM33", "AMD64", "ARM", "ARMNT", "ARM64", "EBC", "I386", "IA64", "M32R", "MIPS16", "MIPSFPU",
        "MIPSFPU16", "POWERPC", "POWERPCFP", "R4000", "RISCV32", "RISCV64", "SH3", "SH3DSP", "SH4", "SH5", "THUMB",
        "WCEMIPSV2", "INVALID", "???",
    ),
    "subsystem": (
        "UNKNOWN", "NATIVE", "WINDOWS_GUI", "WINDOWS_CUI", "OS2_CUI", "POSIX_CUI", "NATIVE_WINDOWS", "WINDOWS_CE_GUI",
        "EFI_APPLICATION", "EFI_BOOT_SERVICE_DRIVER", "EFI_RUNTIME_DRIVER", "EFI_ROM", "XBOX",
        "WINDOWS_BOOT_APPLICATION", "???",
    ),
    "magic": ("PE32", "PE32_PLUS", "???"),
}  # fmt: skip
HASHED_HEADER_COLUMNS = {
    "machine": "header_coff_machine",
    "subsystem": "header_optional_subsystem",
    "magic": "header_optional_magic",
}
# The hashed bins no name of the sampled files falls into: 0 in every file (checked on the prepared file, 2026-11-09).
CONSTANT_COLUMNS = (
    "header_characteristics_hash_1", *(f"header_dll_characteristics_hash_{i}" for i in (2, 6, 9)),
    *(f"section_entry_name_hash_{i:02d}" for i in (6, 16, 19, 24, 40, 48)),
    *(f"section_entry_props_hash_{i:02d}" for i in (1, 3, 5, 6, 7, 11, 12, 15, 16, 17, 19, 24, 26, 27, 29, 30, 31, 33,
                                                    38, 39, 41, 43, 44)),
)  # fmt: skip
FLAGS = ("general_has_debug", "general_has_relocations", "general_has_resources", "general_has_signature",
         "general_has_tls")  # fmt: skip


def vector_columns() -> list[str]:
    """The names of the 2,381 values of the EMBER feature version 2 vector, in the order of the release."""
    cols = [f"byte_histogram_{i:03d}" for i in range(256)]
    cols += [f"byte_entropy_histogram_e{h:02d}_b{b:02d}" for h in range(16) for b in range(16)]
    cols += ["strings_count", "strings_mean_length", "strings_printables"]
    cols += [f"strings_char_share_{0x20 + i:02x}" for i in range(96)]
    cols += ["strings_char_entropy", "strings_n_paths", "strings_n_urls", "strings_n_registry", "strings_n_mz"]
    cols += ["general_size", "general_vsize", "general_has_debug", "general_n_exports", "general_n_imports",
             "general_has_relocations", "general_has_resources", "general_has_signature", "general_has_tls",
             "general_n_symbols"]  # fmt: skip
    cols += ["header_coff_timestamp"] + [f"header_coff_machine_hash_{i}" for i in range(10)]
    cols += [f"header_characteristics_hash_{i}" for i in range(10)]
    cols += [f"header_optional_subsystem_hash_{i}" for i in range(10)]
    cols += [f"header_dll_characteristics_hash_{i}" for i in range(10)]
    cols += [f"header_optional_magic_hash_{i}" for i in range(10)]
    cols += [f"header_optional_{c}" for c in HEADER_OPTIONAL]
    cols += ["section_count", "section_n_zero_size", "section_n_empty_name", "section_n_read_execute",
             "section_n_write"]  # fmt: skip
    for block in ("size", "entropy", "vsize", "entry_name", "entry_props"):
        cols += [f"section_{block}_hash_{i:02d}" for i in range(50)]
    cols += [f"imports_library_hash_{i:03d}" for i in range(256)]
    cols += [f"imports_function_hash_{i:04d}" for i in range(1024)]
    cols += [f"exports_hash_{i:03d}" for i in range(128)]
    for name in DATA_DIRECTORIES:
        cols += [f"datadir_{name.lower()}_size", f"datadir_{name.lower()}_virtual_address"]
    if len(cols) != N_VALUES or len(set(cols)) != N_VALUES:
        raise ValueError(f"the EMBER v2 vector has {N_VALUES:,} distinct values, not {len(cols)}")
    return cols


# A reader of the LMDB file's main database, written out so the build needs no lmdb or msgpack package (the LMDB
# format of lmdb.h: 4,096-byte pages, a B+tree of branch and leaf pages, a value too large for its leaf page on
# overflow pages). Each value is a feature vector, serialised with msgpack as {0: [2,381 float64]} and compressed with
# zlib (the release's README).
LMDB_PAGE = 4096
MSGPACK_HEADER = b"\x81\x00\xdc" + N_VALUES.to_bytes(2, "big")
MSGPACK_VALUES = np.dtype([("marker", "u1"), ("value", ">f8")])
HEX = "0123456789abcdef"


def _lmdb_root(m: mmap.mmap) -> int:
    """The root page of the main database, from the newer of the two meta pages."""
    metas = []
    for i in range(2):
        base = i * LMDB_PAGE + 16
        if struct.unpack_from("<I", m, base)[0] != 0xBEEFC0DE:
            raise ValueError("not an LMDB file")
        txnid = struct.unpack_from("<Q", m, base + 128)[0]
        root = struct.unpack_from("<Q", m, base + 24 + 48 + 40)[0]
        metas.append((txnid, root))
    return max(metas)[1]


def lmdb_locate(m: mmap.mmap, lo: bytes, hi: bytes) -> list[tuple[bytes, int, int]]:
    """(key, byte offset of the value, its size) of every entry with ``lo <= key < hi``, in key order."""
    out: list[tuple[bytes, int, int]] = []
    stack = [_lmdb_root(m)]
    while stack:
        base = stack.pop() * LMDB_PAGE
        flags, lower = struct.unpack_from("<HH", m, base + 10)
        offsets = struct.unpack_from(f"<{(lower - 16) // 2}H", m, base + 16)
        nodes = []
        for off in offsets:
            lo16, hi16, node_flags, key_size = struct.unpack_from("<HHHH", m, base + off)
            nodes.append((bytes(m[base + off + 8 : base + off + 8 + key_size]), lo16, hi16, node_flags, base + off))
        if flags & 0x01:  # a branch page: child i holds the keys from its key (the first: from the start) to the next
            children = []
            for i, (key, lo16, hi16, node_flags, _) in enumerate(nodes):
                start = key if i else b""
                end = nodes[i + 1][0] if i + 1 < len(nodes) else None
                if start < hi and (end is None or end > lo):
                    children.append(lo16 | (hi16 << 16) | (node_flags << 32))
            stack.extend(reversed(children))
        elif flags & 0x02:  # a leaf page: the value inline, or on overflow pages (node flag F_BIGDATA)
            for key, lo16, hi16, node_flags, at in nodes:
                if lo <= key < hi:
                    data_at = at + 8 + len(key)
                    if node_flags & 0x01:
                        data_at = struct.unpack_from("<Q", m, data_at)[0] * LMDB_PAGE + 16
                    out.append((key, data_at, lo16 | (hi16 << 16)))
        else:
            raise ValueError(f"unexpected LMDB page flags {flags:#x}")
    return out


def decode_vector(m: mmap.mmap, offset: int, size: int) -> np.ndarray:
    """One feature vector as float32 (the values were float32 before msgpack wrote them as float64)."""
    raw = zlib.decompress(m[offset : offset + size])
    if raw[:5] != MSGPACK_HEADER or len(raw) != 5 + 9 * N_VALUES:
        raise ValueError("a feature vector that is not a msgpack array of 2,381 values")
    values = np.frombuffer(raw, dtype=MSGPACK_VALUES, offset=5)
    if not (values["marker"] == 0xCB).all():
        raise ValueError("a feature value that is not a float64")
    out = values["value"].astype(np.float32)
    if not (out.astype(np.float64) == values["value"]).all():
        raise ValueError("a feature value that is not a float32")
    return out


def _next(prefix: str) -> str:
    """The smallest key after every key that begins with the hex ``prefix`` (below f...f)."""
    return format(int(prefix, 16) + 1, "x").zfill(len(prefix))


def extract_vectors(lmdb_path: Path, out_path: Path, prefix: str, threads: int = 4) -> int:
    """Write the vectors of the keys that begin with ``prefix`` to a parquet file (sha256 and 2,381 float32 values).

    The key range is cut into 16 parts by the next hex digit; each part is read in the order of the file (its values
    lie anywhere in the 77 GB file) and written in key order, so the file is the same on every run. Returns the count.
    """
    import pyarrow as pa
    import pyarrow.parquet as pq

    schema = pa.schema([("sha256", pa.string())] + [(f"v{i:04d}", pa.float32()) for i in range(N_VALUES)])
    with open(lmdb_path, "rb") as handle, mmap.mmap(handle.fileno(), 0, access=mmap.ACCESS_READ) as m:

        def part(digit: str) -> tuple[list[str], np.ndarray]:
            end = prefix + HEX[HEX.index(digit) + 1] if digit != "f" else _next(prefix)
            located = lmdb_locate(m, (prefix + digit).encode(), end.encode())
            values = np.empty((len(located), N_VALUES), dtype=np.float32)
            for i in sorted(range(len(located)), key=lambda i: located[i][1]):
                values[i] = decode_vector(m, located[i][1], located[i][2])
            return [key.decode("ascii") for key, _, _ in located], values

        rows = 0
        tmp = out_path.with_suffix(".tmp")
        with pq.ParquetWriter(tmp, schema, compression="zstd") as writer, ThreadPoolExecutor(threads) as pool:
            for first in range(0, len(HEX), threads):
                for keys, values in pool.map(part, HEX[first : first + threads]):
                    arrays = [pa.array(keys, pa.string())] + [pa.array(values[:, j]) for j in range(N_VALUES)]
                    writer.write_table(pa.Table.from_arrays(arrays, schema=schema))
                    rows += len(keys)
    tmp.rename(out_path)
    return rows


def release_counts(meta_db: Path, prefix: str, n_vectors: int) -> dict:
    """Counts over the whole release for the decisions: the detection counts by label, the release's split sizes, and
    the sampled files with and without a feature vector.
    """
    con = sqlite3.connect(f"file:{meta_db}?mode=ro", uri=True)
    try:
        meta = pd.read_sql_query("select substr(sha256, 1, 1) as first, is_malware, rl_fs_t, rl_ls_const_positives "
                                 "from meta", con)  # fmt: skip
    finally:
        con.close()
    period = np.where(
        meta["rl_fs_t"] <= TRAIN_VALIDATION_SPLIT,
        "train",
        np.where(meta["rl_fs_t"] < VALIDATION_TEST_SPLIT, "validation", "test"),
    )
    detections = meta.groupby(["is_malware", "rl_ls_const_positives"]).size()
    splits = meta.groupby([period, meta["is_malware"]]).size()
    sample = meta[meta["first"] == prefix].groupby("is_malware").size()
    return {
        "detections_by_label": [[int(a), int(b), int(n)] for (a, b), n in detections.items()],
        "release_splits_by_label": [[str(a), int(b), int(n)] for (a, b), n in splits.items()],
        "sample_files_by_label": [[int(a), int(n)] for a, n in sample.items()],
        "sample_vectors": n_vectors,
        "first_seen_min_max_count": [float(meta["rl_fs_t"].min()), float(meta["rl_fs_t"].max()), len(meta)],
    }


def _hashed_pattern(name: str) -> tuple[int, int]:
    """The bin and sign scikit-learn's FeatureHasher(10, input_type="string") gives one name, as ember hashes it."""
    from sklearn.feature_extraction import FeatureHasher

    hashed = FeatureHasher(10, input_type="string").transform([[name]]).toarray()[0]
    (j,) = np.flatnonzero(hashed)
    return int(j), int(hashed[j])


def _block_patterns(block: np.ndarray) -> list[tuple[int, int]]:
    """The bin and sign of each row of a one-name block (exactly one entry of +1 or -1 per row)."""
    nonzero = block != 0
    if not (nonzero.sum(axis=1) == 1).all() or not np.isin(block[nonzero], (-1.0, 1.0)).all():
        raise ValueError("a one-name header block without exactly one entry of +1 or -1")
    j = nonzero.argmax(axis=1)
    sign = np.sign(block[np.arange(len(block)), j]).astype(int)
    return list(zip(j.tolist(), sign.tolist(), strict=True))


def decode_hashed_name(block: np.ndarray, names: tuple[str, ...]) -> list[str]:
    """A one-name field hashed into 10 signed bins turned back into the names that hash to the row's bin and sign,
    joined by " / " where several names share one ("AMD64 / ARM64"); "???" reads "unnamed".
    """
    levels: dict[tuple[int, int], list[str]] = {}
    for name in names:
        levels.setdefault(_hashed_pattern(name), []).append(name.replace("???", "unnamed"))
    patterns = _block_patterns(block)
    unknown = sorted(set(patterns) - set(levels))
    if unknown:
        raise ValueError(f"hashed header patterns that no name gives: {unknown}")
    return [" / ".join(levels[p]) for p in patterns]


class Sorel20mMaliciousPe1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "Is a Windows program file malicious, judged from its contents alone when a security vendor's telemetry "
            "first sees it?"
        ),
        use_case=(
            "A security vendor's static detector scores each Windows program the first time it meets it, without "
            "running it, and blocks or quarantines the ones it calls malicious at a low false-alarm rate; the model is "
            "refit on newer files as malware changes (SOREL-20M, Sec. 1), for example every month."
        ),
        row=(
            "One Windows program file (PE) first seen in ReversingLabs' telemetry between 1 January 2017 and 11 April "
            "2019, from the SOREL-20M release of Sophos and ReversingLabs: a fixed sixteenth of its files, those whose "
            "SHA-256 begins with 0."
        ),
        predicted=(
            "Whether Sophos labels the file malicious. In the release every malicious file has five or more antivirus "
            "detections and every benign one at most one, so files with two to four were left out; the labels were "
            "final at the release in December 2020, 20 months or more after each file was first seen."
        ),
        known=(
            "The EMBER (version 2) features computed from the file's bytes: byte and byte-entropy histograms, string "
            "statistics, file and header fields, sections, imported and exported names folded into hashed bins, data "
            "directories; and the time it was first seen."
        ),
        split=(
            "Each test window is 30 days of the release's test period (12 January to 11 April 2019), so every test "
            "file is newer than every training file; each training side is a random million of the earlier files (the "
            "oldest window: all 985,619)."
        ),
        changes=(
            "We use a fixed sixteenth of the files and test on three 30-day windows that together are the release's "
            "test set, each training on all earlier files; the hashed machine, subsystem and PE type are turned back "
            "into their names."
        ),
        fit="approximate",
        fit_reason=(
            "The features come from the file alone and exist when it is first seen, as for a deployed detector. The "
            "hour and weekday of that sighting carry ReversingLabs' feed rhythm (alone ROC AUC 0.61 to 0.63), known at "
            "arrival. But the labels follow Sophos's unpublished rules and leave out files with two to four "
            "detections, so the test holds only clear cases, and the malicious share follows the release's sampling."
        ),
    )

    # Dataset
    unique_name = "sorel_20m_malicious_pe_1m"
    version_of = "sorel_20m_malicious_pe"
    version_comment = """
        We sample twice. Before the split, `_prepare_raw_files` keeps a fixed sixteenth of the release: the files whose SHA-256 begins with 0 (the hash of the file's bytes), 1,251,351 of the 19,389,877 files with a feature vector. The hash is independent of the file, but the release's benign files of July-August 2017 and June-July 2018 came in batches favouring low SHA-256 values, so this prefix holds about 40,000 more benign training files than the average prefix: 48.9% malicious against 50.5% for the release. The test windows are unaffected (benign ratio to the other prefixes 1.00 to 1.08). A sixteenth keeps the 2,381 float32 values per file at 12 GB in memory (the whole release would take 185 GB); it leaves the two newer train sides above the 1M budget, the oldest at 985,619 files, and each test window at 77,057 to 99,209 files, under the 500k budget. Then the v2 split protocol samples per test window: each train side is a random 1M of all earlier files (one random order for all windows; the oldest window's 985,619 files are all used), and each window keeps all of its files. Every sampled file is used by some split.
    """
    year = "2020"
    domain = "technology & internet"
    source = "Other"  # Sophos's public S3 bucket, listed in the AWS Open Data registry; code and README on GitHub
    source_url = "https://registry.opendata.aws/sorel-20m/"
    license = (
        "SOREL-20M Terms and Conditions of Use (Sophos): for security research on malware detection; no "
        "redistribution of the content or of works derived from it. Code: Apache-2.0"
    )
    data_tags = ()
    download_description = """
        We download the release's index `meta.db` (3.8 GB) and the EMBER feature LMDB `ember_features/data.mdb` (76.9 GB) from Sophos's public S3 bucket; no credentials are needed. The LMDB is downloaded whole: its pages lie in the order the entries were written, so the vectors of a sample are spread over the whole file. Not needed: the 515 GB `pe_metadata` LMDB, the 8 TB of malware binaries and the 172 GB `lightGBM-features` arrays (the same values without the SHA-256 or the time). `_prepare_raw_files` then reads the sampled vectors (4 to 40 minutes).

        D=local-data-warehouse/sorel_20m_malicious_pe && mkdir -p $D/ember_features && cd $D
        aws s3 cp --no-sign-request s3://sorel-20m/09-DEC-2020/processed-data/meta.db .
        aws s3 cp --no-sign-request s3://sorel-20m/09-DEC-2020/processed-data/ember_features/data.mdb ember_features/
        # or over https: https://sorel-20m.s3.amazonaws.com/09-DEC-2020/processed-data/meta.db (and .../ember_features/data.mdb)
        # S3 ETags (MD5 of the 8 MiB parts): meta.db f1a8b94f82855126f1fc75491abb7d79-452, data.mdb d85369833ea82488bc98c1daa8fefc56-9164
    """
    bibtex = """
        @misc{harang2020sorel20m,
          title={{SOREL-20M}: A Large Scale Benchmark Dataset for Malicious {PE} Detection},
          author={Richard Harang and Ethan M. Rudd},
          year={2020},
          eprint={2012.07634},
          archivePrefix={arXiv},
          primaryClass={cs.CR},
        }
    """
    curation_comments = """
        We start with `meta.db` (per file: the SHA-256, the label `is_malware`, the first-seen time `rl_fs_t`, the detection count and 11 behaviour tags) and the LMDB `ember_features/data.mdb` (one EMBER version 2 vector per file) of the SOREL-20M release (Sophos and ReversingLabs, 9 December 2020). `_prepare_raw_files` reads the vectors of the sampled files with an LMDB reader written out in `dataset.py` (no lmdb or msgpack package). The authors' LightGBM baseline (seed 0, from the release) scores our vectors of the 8,199 test files of an exploration sample exactly as its published results do (largest difference 1e-16; ROC AUC 0.982, Fig. 5: 0.981 over five seeds), and 0.71 with the values shifted by one column.

        - The prediction point is the file's first sighting in ReversingLabs' telemetry (`rl_fs_t`, UTC, to the minute), standing for the moment a detector first meets the file. Every feature is computed from the file's bytes, which exist then; the label comes from antivirus detections and Sophos's rules later.
        - Rows: a fixed sixteenth of the release, the files whose SHA-256 begins with 0 (version comment). Files without a feature vector (335,120 of the release's 19,724,997, 3.0% of the benign and 0.4% of the malicious files; EMBER could not process them, the repository's `shas_missing_ember_features.json`) are not in the LMDB and not rows: no task row without the input (USE-7), as in the authors' splits, whose Table 1 counts (12,699,013 / 2,495,801 / 4,195,063 files) we match exactly. The paper's text gives 2,495,822 and 4,195,042, 21 files apart; its table adds up to our counts.
        - Out, as known only after the first sighting or taken from the label (LEAK-10): `rl_ls_const_positives`, the number of antivirus vendors detecting the file in ReversingLabs' telemetry ("at the time of collection", abstract), and the 11 behaviour tags (token counts parsed from the vendors' detection names). The count splits the labels without overlap: benign 0 or 1, malicious 5 or more, no file with 2 to 4 (decision below). Out too: `sha256` (an identifier, CLEAN-3) and `rl_fs_t` (now the date `first_seen`).
        - Repair (CLEAN-12): EMBER v2 hashes the machine, the subsystem and the PE type (magic) into 10 bins each, one entry of +1 or -1 per file. We turn each back into the names that hash to the file's bin and sign: the names LIEF 0.9.0 gives these fields (LIEF is the parser of EMBER v2), with ARM64 and "unnamed" for a code LIEF does not name, joined by " / " where names share one ("AMD64 / ARM64", "WINDOWS_GUI / XBOX"); missing for the 119 files LIEF could not parse (35 benign, 84 malicious; all three fields hashed the empty string). The 30 hashed columns leave.
        - Note: the other hashed blocks (the header and DLL characteristics, the section sizes, entropies and virtual sizes by section name, the entry section's name and properties, the imported libraries and functions, the exports) and the byte, byte-entropy and character histograms ship as plain numeric columns, as the authors vectorise them. Only the malicious binaries are released ("Benign files are excluded due to potential intellectual property concerns", Sec. 5, footnote 3), so this vector is the only representation of every file, and the field's detectors (the authors' LightGBM and neural network) read it as columns. They are no spectrum (CLEAN-26): no axis of a physical measurement and no field default to process them by. ember2024_malware_detection ships its version 3 vector the same way.
        - Dtypes (CLEAN-14): categorical for the decoded machine, subsystem and PE type and for the five yes/no flags (`general_has_debug`, `_relocations`, `_resources`, `_signature`, `_tls`; 0 or 1 only); the first sighting a date; numbers for the rest, float32 as the authors' vector (integers above 2^24, such as sizes, are rounded there). `header_coff_timestamp` stays a number: the compile time the file states, which a file can fake. Its 0 (1.83% of the files) and its dates after the first sighting (2.6%) are what the file states and stay as they are.
        - We drop 33 hashed bins that are 0 in every sampled file (CLEAN-5): no name of these files hashes into them (one of the header characteristics, three of the DLL characteristics, six of the entry section's name and 23 of its properties).
        - Note: `first_seen` stays a feature, as in ember2024_malware_detection: the time of arrival is known when the file arrives. Its hour and weekday alone separate the classes at ROC AUC 0.60 to 0.63 (malicious and benign files reach the telemetry at different hours); with the vector they add -0.00001 to 0.0008 ROC AUC and 0.1 to 0.4 points of the true positive rate at a 1% false positive rate (200,000 files, untuned LightGBM, 3 windows).
        - Exact copies of the vector are kept: 155 files (0.012%) share 58 vectors, none with both labels, and 0, 2 and 1 test files of the three windows have a copy among the earlier files. They are distinct files the vector cannot tell apart (LEAK-19, as hiva_agnostic and ember2024_malware_detection), too few to matter.
        - Anomaly: the share of malicious files follows the release's collection, not what a detector meets: 74-93% of the files a month from March 2017 to May 2018 (23-29% in January and February 2017), 55% in June and July 2018 and 26-40% from September 2018 on, when the weekly count rose from about 80,000 to 400,000 files. The paper does not say how the files were selected.
        - Anomaly: how the labels were set is not published ("a combination of non-public, internal information as well as a number of static rules and analyses", README FAQ). On the data they agree with a threshold on the detection count, and the files of two to four detections are missing, so the test holds clear cases only, as in EMBER and EMBER2024 (USE-5: kept, fit approximate).
        - Note: `ember2024_malware_detection` is the same task (static detection of Windows PE files) from another source, and no duplicate (PROV-4, PROV-7): VirusTotal files of 2023-2024 labelled by public engine counts, balanced per week, with the EMBER version 3 vector (2,568 values); here Sophos and ReversingLabs telemetry files of 2017-2019, labelled by Sophos, with the version 2 vector (2,381 values). The task's conventions are the same: the target `is_malicious` (No/Yes), the first sighting as the prediction point and the time column, three test windows that together are the source's test period, no gap, and the ROC AUC as the fallback metric. Both enter (principles.md, Tensions: same task, another source; Lennart, 2026-11-08).
    """

    # Task
    target = "is_malicious"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason=(
            "The paper (arXiv 2012.07634) shows ROC curves of its baselines (Figs. 4 to 6; the release's plot.py labels "
            "each with its mean ROC AUC) and asks for performance 'at lower false positive rates (1 in 1000 or below)' "
            "(Sec. 1), a range and not one operating point; plot.py also reads the true positive rate at false positive "
            "rates of 1e-5 to 1e-1, and the LightGBM baseline stops early on the log loss (lightgbm_config.json). "
            "Several criteria side by side, none named as the one that decides (MET-5), and no fixed false positive "
            "rate for a threshold metric (MET-7). The README and the AWS registry entry define no metric."
        )
    )

    temporal = Temporal(
        on="first_seen",
        splits=TemporalSplits(
            window=30, unit="days", cutoffs=("2019-01-12 07:54:00", "2019-02-11 07:54:00", "2019-03-13 07:54:00")
        ),
    )
    splits_comment = """
        We test on three 30-day windows that together are the release's test set (files first seen from 12 January 2019, 07:54 UTC, the split time of the release's config.py, to 11 April 2019), newest first: from 13 March, 11 February and 12 January, each training on every file first seen before it, so the oldest window trains on exactly the release's training and validation sets. The release has one test set of 88 days after a validation set of 43 days; 30-day windows are a monthly refit of the detector, and three windows are the fewest the protocol takes. No gap: a label waits for the antivirus detections to settle, so a detector refit at a window's start would not yet know the labels of its last weeks, but every label is final in the release (December 2020, 20 months after the last file) and the measurements show no shortcut through them: at equal training size (200,000 files, untuned LightGBM, 2 seeds) training up to the window's start instead of 30 days before it adds 0.00006 to 0.0007 ROC AUC, 0.05 to 1.3 points of the true positive rate at a 1% false positive rate and 1.3 to 3.0 points at 0.1% (6 of 6 fits, 3 windows); 0 to 2 test files a window share their exact vector with an earlier file; and no sign of labels cut by the release: the malicious share of the newest months (25% to 40%) lies in the band of the earlier ones (leak probe 13, |z| at most 2.1), its fall began in September 2018 with the fivefold rise in volume, and the malicious files of every week to the end have 21 to 23 detections on average. The release's own split has no gap either. Each test window keeps all of its 77,057 to 99,209 sampled files (under the 500k budget); each train side is a random 1M of all earlier sampled files (one random order for all windows), the oldest all of its 985,619.
    """
    row_budget = RowBudget(train=1_000_000, test=500_000)

    prepared_raw_files = (VECTOR_FILE, COUNTS_FILE)

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        # The feature vectors of the sampled files, read once from the 77 GB LMDB with 4 threads (4 minutes when the
        # file is in the page cache, about 40 from a network disk), and counts over the whole release for the decisions.
        n = extract_vectors(raw_dir / "ember_features" / "data.mdb", raw_dir / VECTOR_FILE, SAMPLE_PREFIX)
        counts = release_counts(raw_dir / "meta.db", SAMPLE_PREFIX, n)
        (raw_dir / COUNTS_FILE).write_text(json.dumps(counts, indent=1))

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        # The sampled vectors, named by the EMBER v2 layout and read batch by batch into one float32 array, and the
        # release's metadata of the same files from meta.db (joined on the sha256).
        import pyarrow.parquet as pq

        source = pq.ParquetFile(raw_dir / VECTOR_FILE)
        values = np.empty((source.metadata.num_rows, N_VALUES), dtype=np.float32)
        keys: list[str] = []
        start = 0
        for batch in source.iter_batches(batch_size=20_000):
            keys += batch.column(0).to_pylist()
            values[start : start + batch.num_rows] = np.column_stack(
                [batch.column(j).to_numpy() for j in range(1, N_VALUES + 1)]
            )
            start += batch.num_rows
        con = sqlite3.connect(f"file:{raw_dir / 'meta.db'}?mode=ro", uri=True)
        try:
            meta = pd.read_sql_query(
                "select * from meta where sha256 >= ? and sha256 < ?", con, params=(SAMPLE_PREFIX, _next(SAMPLE_PREFIX))
            )
        finally:
            con.close()
        meta = meta.set_index("sha256").loc[keys].reset_index()
        return pd.concat([meta, pd.DataFrame(values, columns=vector_columns(), copy=False)], axis=1)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # 1. The target in words, the first-seen time as a date (UTC, to the minute).
        df = decode(df, {"is_malware": {0: "No", 1: "Yes"}}).rename(columns={"is_malware": self.target})
        df["first_seen"] = pd.to_datetime(df["rl_fs_t"], unit="s")
        # 2. The three one-name header fields EMBER hashes into 10 bins each (machine, subsystem, magic) turned back
        #    into their names (CLEAN-12); missing when lief could not parse the file (the magic is then the hash of
        #    the empty string).
        magic = [f"header_optional_magic_hash_{i}" for i in range(10)]
        parsed = np.array([p != _hashed_pattern("") for p in _block_patterns(df[magic].to_numpy())])
        decoded, hashed = {}, []
        for field, column in HASHED_HEADER_COLUMNS.items():
            block = [f"{column}_hash_{i}" for i in range(10)]
            names = pd.Series(pd.NA, index=df.index, dtype=object)
            names[parsed] = decode_hashed_name(df.loc[parsed, block].to_numpy(), HASHED_NAMES[field])
            decoded[column] = names
            hashed += block
        # 3. Out: the detection count at the last scan and the 11 behaviour tags (from the vendors' detections, known
        #    only after the first sighting, and the count defines the label: LEAK-10), the first-seen time in seconds
        #    (now `first_seen`), the sha256 (an identifier, CLEAN-3) and the hashed header blocks decoded above. One
        #    drop and one concat, so the 12 GB of values are copied once. With them go the 33 hashed bins that are 0
        #    in every sampled file (CLEAN-5).
        df = drop_columns(df, ["sha256", "rl_fs_t", "rl_ls_const_positives", *TAGS, *hashed, *CONSTANT_COLUMNS])
        return pd.concat([df, pd.DataFrame(decoded, index=df.index)], axis=1)

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # Categorical: the decoded machine, subsystem and PE type, and the five yes/no flags of the general block (0 or
        # 1 only). A date: the first sighting. Every other value is a number, as the authors' vector holds it.
        return FeatureTypes(
            categorical=[*HASHED_HEADER_COLUMNS.values(), *FLAGS],
            datetime={"first_seen": None},
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        counts = json.loads((self.raw_dir / COUNTS_FILE).read_text())
        detections = pd.DataFrame(counts["detections_by_label"], columns=["is_malware", "detections", "files"])
        bands = pd.cut(detections["detections"], [-1, 0, 1, 4, 9, 19, 28], labels=["0", "1", "2-4", "5-9", "10-19",
                                                                                   "20-28"])  # fmt: skip
        table = (
            detections.assign(detections=bands, label=detections["is_malware"].map({0: "benign", 1: "malicious"}))
            .pivot_table(index="detections", columns="label", values="files", aggfunc="sum", observed=False)
            .fillna(0)
            .astype(int)
        )
        levels = pd.concat(
            {
                column: df[column].astype(object).fillna("(no PE header parsed)").value_counts()
                for column in HASHED_HEADER_COLUMNS.values()
            },
            names=["column", "name"],
        ).rename("files")
        return [
            Decision(
                title="The label is a threshold on the vendor detections, which leave",
                why=(
                    "`rl_ls_const_positives`, the number of antivirus vendors detecting a file in ReversingLabs' "
                    "telemetry 'at the time of collection' (abstract), splits the labels without overlap in all "
                    "19,724,997 files of `meta.db`: benign files have 0 or 1 detections, malicious ones 5 to 28, and no "
                    "file has 2 to 4. The count and the 11 behaviour tags parsed from the detection names are set "
                    "after the file's first sighting and define its label, so they leave (LEAK-10); the left-out grey "
                    "zone makes the test hold clear cases only."
                ),
                evidence=table,
            ),
            Decision(
                title="The hashed machine, subsystem and PE type decoded into names",
                why=(
                    "EMBER v2 hashes each of the three one-name header fields into 10 bins with one entry of +1 or -1 "
                    "per file; the names that give the file's bin and sign (LIEF 0.9.0's, with ARM64 and 'unnamed') "
                    "replace the 30 columns, joined by ' / ' where names share one. Counts in the shipped frame."
                ),
                evidence=levels.to_frame(),
            ),
        ]
