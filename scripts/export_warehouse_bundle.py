"""Create a zip archive of all curated dataset folders referenced in _tmp_state_paths.py."""

from __future__ import annotations

import os
import sys
import zipfile
from pathlib import Path

from tqdm import tqdm

# Resolve paths relative to the data-foundry root
SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent

sys.path.insert(0, str(ROOT_DIR / "datasets" / "beyond_iid"))
from _tmp_state_paths import GROUPED, NEW_IID, OLD_IID, TEMPORAL

WAREHOUSE = ROOT_DIR / "local-data-warehouse"
BUNDLE_NAME = "beyond_iid_data_bundle"
OUTPUT_ZIP = WAREHOUSE / (BUNDLE_NAME + ".zip")


all_paths = OLD_IID + NEW_IID + TEMPORAL + GROUPED
print(f"Total URIs to export: {len(all_paths)}")

missing = []
with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zf:
    for uri in tqdm(all_paths, desc="Zipping datasets"):
        src_dir = WAREHOUSE / uri
        if not src_dir.is_dir():
            raise ValueError(f"Expected directory not found: {src_dir}")
        for f in sorted(os.listdir(src_dir)):
            full = src_dir / f
            if full.is_file():
                zf.write(full, arcname=str(Path(BUNDLE_NAME) / uri / f))

size_mb = OUTPUT_ZIP.stat().st_size / 1024 / 1024
print(f"\nCreated: {OUTPUT_ZIP}")
print(f"Size: {size_mb:.1f} MB")
print(f"Datasets: {len(all_paths)}")
