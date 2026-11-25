"""Curated pooled compound-protein potency from Papyrus2024.2."""

from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    Smiles,
    Source,
    SplitPlan,
    TaskSummary,
    Temporal,
    canonical_smiles,
    scaffold_groups,
)

ACTIVITY_FILE = "05.7_combined_set_without_stereochemistry.tsv.xz"
PROTEIN_FILE = "05.7_combined_set_protein_targets.tsv.xz"
TEST_WINDOWS = ((2022, 2024), (2021, 2022), (2020, 2021))
"""The test windows as half-open spans of `entry_year`, newest first (Andrej, 2026-11-24): the newest joins 2022
and 2023, because the release's last year is cut short, the other two are one year each."""
PREPARED_FILE = "05.7_high_quality_source_rows.parquet"
STRUCTURE_KEYS_FILE = "05.7_recognized_structure_keys.parquet"
ACTIVITY_MD5 = "f6dd07da52ca92029cc4cdde47c3c5cf"
PROTEIN_MD5 = "672f03fd78b73c044ff2eb7bd8373869"
SOURCE_COLUMNS = (
    "Activity_ID",
    "Quality",
    "source",
    "CID",
    "SMILES",
    "connectivity",
    "target_id",
    "Protein_Type",
    "AID",
    "doc_id",
    "Year",
    "all_doc_ids",
    "all_years",
    "type_IC50",
    "type_EC50",
    "type_KD",
    "type_Ki",
    "type_other",
    "Activity_class",
    "relation",
    "pchembl_value",
    "pchembl_value_Mean",
    "pchembl_value_StdDev",
    "pchembl_value_N",
)


def _check_md5(path: Path, expected: str) -> None:
    digest = hashlib.md5(usedforsecurity=False)
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    assert digest.hexdigest() == expected, f"Publisher checksum mismatch: {path.name}"


def _known_endpoint_rows(raw: pd.DataFrame) -> pd.Series:
    # Unknown/derived measurements have no declared shared concentration meaning; keep complete source means only.
    other = raw["type_other"].fillna("").str.contains("1", regex=False)
    recognized = pd.concat(
        [
            raw[column].fillna("").str.contains("1", regex=False)
            for column in ("type_IC50", "type_EC50", "type_KD", "type_Ki")
        ],
        axis=1,
    ).any(axis=1)
    return ~other & recognized & raw["relation"].eq("=")


def _last_document_year(value: object) -> float:
    """The newest year in a source ``all_years`` cell (the documents behind one row's mean)."""
    if not isinstance(value, str):
        return float("nan")
    years = [int(part) for part in value.replace(";", ",").split(",") if part.strip().isdigit()]
    return max(years) if years else float("nan")


def _entry_years(frame: pd.DataFrame) -> pd.Series:
    """The year each compound's measurements end: its last document year, over every row of the compound.

    A compound is a source connectivity, so chemical aliases written as different structures are one compound and
    a later alias never tests against its own earlier entry. A compound with no dated document takes the earliest
    year of the data, so it always trains and never tests.
    """
    last = frame["all_years"].map(_last_document_year)
    entry = last.groupby(frame["connectivity"], observed=True).transform("max")
    return entry.fillna(entry.min()).astype("int64")


class PapyrusBioactivity(AbstractCuratedDataset):
    """Source-mean potency for unseen chemistry across protein targets."""

    task_summary = TaskSummary(
        question="What mean log potency will a new compound have against a specified protein target?",
        use_case=(
            "For example, a medicinal chemist estimates a candidate compound's potency against a selected protein before an assay, "
            "to choose compounds for experimental follow-up. Papyrus models such compound-protein interactions."
        ),
        row=(
            "One standardized compound-protein pair in Papyrus2024.2, with an exact source mean derived only from "
            "recognized Ki, KD, IC50 or EC50 measurements. Multiple proteins and organisms remain pooled."
        ),
        predicted=(
            "The source's mean pChEMBL value, already a negative-log molar potency scale; higher is stronger. "
            "It is an average of published log measurements, not a new mean of our construction."
        ),
        known=(
            "The compound's structure and the selected protein's identity, sequence when available, organism, "
            "classification, length and mutation identity. No assay result, source potency summary or outcome history."
        ),
        split=(
            "Each compound is dated by the year its measurements end, the last document behind any of its means, and "
            "three windows are tested on the compounds whose measurements ended earlier: 2022 with 2023, then 2021, "
            "then 2020. Every protein pair of a compound goes with that year; proteins may recur."
        ),
        changes=(
            "We keep high-quality exact means composed solely of recognized potency types, join intrinsic protein "
            "metadata, remove source/provenance and outcome-derived predictors, and split by the year each "
            "compound's measurements end."
        ),
        fit="approximate",
        fit_reason=(
            "Published mean log potency combines assay types and laboratories without a fixed experimental protocol. "
            "The windows test the compounds the literature measures next, and every training label is final at its "
            "cut; the test compound's own papers are held out, but its chemical analogues need not be. Structures "
            "omit stereochemistry, and exact reported potency measurements do not represent a complete prospective "
            "screening library."
        ),
    )
    unique_name = "papyrus_bioactivity"
    sources = (
        Source(
            role="publication",
            platform="Other",
            url="https://doi.org/10.4121/16896406.v1",
            license="CC BY-SA 4.0",
            year="2021",
            bibtex="""
        @article{bequignon2023papyrus,
          title={Papyrus: a large-scale curated dataset aimed at bioactivity predictions},
                    author={Bequignon, Olivier J. M. and Bongers, Brandon J. and Jespers, Willem and IJzerman, Ad P.
          and van der Water, Bob and van Westen, Gerard J. P.},
          journal={Journal of Cheminformatics},
          volume={15},
          number={3},
          year={2023},
          doi={10.1186/s13321-022-00672-x}
        }
    """,
        ),
    )
    domain = "chemistry & material science"
    download_description = """
        The first Papyrus data publication is cited as 2021 in the 2023 paper (reference 20).
        This definition pins release 2024.2 / files05.7: https://zenodo.org/records/13987985 .
        Download these two publisher files into local-data-warehouse/papyrus_bioactivity/raw/:

        mkdir -p local-data-warehouse/papyrus_bioactivity/raw
        wget -O local-data-warehouse/papyrus_bioactivity/raw/05.7_combined_set_without_stereochemistry.tsv.xz 'https://zenodo.org/records/13987985/files/05.7_combined_set_without_stereochemistry.tsv.xz?download=1'
        wget -O local-data-warehouse/papyrus_bioactivity/raw/05.7_combined_set_protein_targets.tsv.xz 'https://zenodo.org/records/13987985/files/05.7_combined_set_protein_targets.tsv.xz?download=1'

        The commands save the filenames this definition expects. The publisher MD5 values are checked before
        preparation. The high-quality source slice is reproduced by this definition; no external script is needed.
        The release README and 05.7_additional_files.zip document schema, counts and CC BY-SA 4.0 terms.
    """
    curation_comments = """
        Papyrus2024.2/files05.7 supplies standardized non-stereochemical activities and intrinsic protein metadata.

        - Before assay, the query specifies a compound and protein. Fit transformations on training rows only;
          freeze the predictor for each query. Statistics from other held-out assay records, including externally
          preloaded held-out counts, violate this pointwise contract and must be investigated and excluded.
        - Of 59,460,216 source rows, 1,369,350 have Quality High and exact relation '='. We retain 692,017 complete
          source means composed solely of Ki, KD, IC50 or EC50; type_other contains untraceable/derived quantities.
          No measurements are selectively removed and re-averaged, no Ki-only restriction or per-protein cuts occur.
        - mean_pchembl is exactly pchembl_value_Mean: published mean log potency, with no extra log/conversion.
          557,429 labels have one measurement; 30,723 combine recognized endpoint types. Mixed assays/laboratories,
          omitted stereochemistry and the selected measured cohort make the pre-assay use case approximate.
        - The many-to-one protein join retains selected-target identity, sequence, organism, classification,
          length and mutation identity. Identity is a meaningful repeated query entity. Nine proteins/60 rows lack
          sequence. Exactly 11,732 'Unclassified protein' cells become missing; Other and partial paths remain.
        - Sequence remains a string: generic text/category handling limits representation. No learned sequence
          embedding, optional source UniRep representation or source molecular descriptors ship. Structures use
          typed canonical SMILES (CLEAN-24); salts/fragments remain published and stereo was absent in this source.
        - The canonical structure is computed once per compound. Exact copies are removed; conflicting
          canonical-pair labels leave as ambiguous copies, without averaging. The Bemis-Murcko scaffold is still
          prepared for each structure, but no longer ships as a column: it was the group key of the scaffold folds
          this definition left on 2026-11-24 and was never a model input. The source connectivity, which identifies
          chemical aliases written as different structures, dates those aliases as one compound (split note below).
        - The inherited whole-row hash ordering encoded labels: a training-only attack recovered 185/200 labels,
          independently 360/400. Disable that ordering; sort known structure/protein inputs then shuffle seed42.
          Full target perturbations leave the repaired order invariant. Source labels and fold membership stay intact.
        - The windows span all proteins; proteins and close analogues may recur across windows, and a test
          compound is new to the catalogue's record, not necessarily a new chemical series. Assay IDs, outcome
          summaries/counts, quality/endpoint flags, document provenance and the split year never enter predictors.
        - Split by the year a compound's measurements end (Andrej, 2026-11-24, issue 1 C). `entry_year` is the
          newest document year over every row of a compound (the source `all_years`), taken per source
          connectivity, so every row of a compound carries one year and aliases share it; it orders and splits the
          rows and is no model input. The source `Year`, the first interaction document, is not label availability
          (9,386 retained pairs have Year<2013 and contributing years>=2013), which is why the key is the last
          document and not the first: at every cut, no training label takes in a document from the test year or
          later (0 of 601,378, 645,094 and 681,528 training rows). 2,791 rows (1,667 compounds, 0.40%) have no
          dated document at all; they take the earliest year, 1976, so they always train. Outcome-filtered
          Papyrus++ is not used; broader source standardization is not certified independent of every label.
        - The paper reports RMSE and Pearson without one primary score. Use fallback RMSE on the unchanged log scale.
        - PROV-7: this protein-conditioned interaction task differs from fixed-target QSAR: 129,427 multi-protein
          compounds supply 365,480 rows. Measured ChEMBL overlap is 1,616 IDs/2,257 rows, including 864 same-thrombin
          pairs. Pooling or a small overlap fraction alone does not establish uniqueness. Parent/stereo equivalence
          and comprehensive sibling overlap remain unverified; no legacy QSAR task is changed.
        - Split walk (the split decision tree, SPLIT-36, from the record's collection type Expanding Science Catalogue): [CAT.next-items] the source aims at compounds the catalogue does not hold yet: yes → [CAT.entry-date] a compound's mean takes in later documents (`Target: Revised Later`), but the year its last measurement arrives, at which its label is final, is rebuilt from the documents' years: yes → [CAT.arrival] what the catalogue takes in shifts with that year (each forward window's mix of protein families is 0.15 from its training side's in total variation distance, against 0.01 for a random split; the newest window's protein classification drifts at PSI 0.41, with 2.5% of its rows in a category the training side never shows): yes → [CAT.windows] the curator's three windows train on 81.2-93.6% of the rows: yes → leaf L-CAT.entry-date, Temporal · entry date, the split this definition ships (`split_leaf`; Andrej, 2026-11-24, issue 1 C).
    """
    target = "mean_pchembl"
    problem_type = "regression"
    # Order only on known query inputs in `_clean`; the inherited whole-row content hash includes the label.
    shuffle = False
    special_features = (Smiles(column="SMILES"),)
    metric = Metric.fallback(
        reason=(
            "Bequignon et al. 2023, Bioactivity modelling/Fig.5, doi:10.1186/s13321-022-00672-x reports "
            "RMSE and Pearson correlation side by side; no unique primary regression metric. "
            "Fallback RMSE directly scores the source mean pChEMBL scale, already logarithmic."
        )
    )
    temporal = Temporal(
        on="entry_year",
        horizon=2,
        horizon_unit="years",
        time_unit="years",
        time_of="label",
    )
    split_leaf = "L-CAT.entry-date"
    splits_comment = """
        Expanding windows on the year each compound's measurements end (`entry_year`, no input), leaf
        L-CAT.entry-date of the split tree: three test windows, newest first, no gap (a published measurement is
        known when its paper appears, and the key makes every training label final at its cut). Training is every
        compound whose measurements ended before the window; rows of later years are unused by it. The windows are
        the curator's (Andrej, 2026-11-24), and `TemporalSplits` cannot state them, since one window length serves
        every cutoff: the newest window joins 2022 and 2023, because the release's last year holds a fifth of a
        usual one (ChEMBL 34 curates a paper some time after it appears), and the two before it are single years.
        Test windows (years: rows, compounds, proteins, train share): 2022-2023: 44,132, 22,792, 2,372, 93.6%;
        2021: 43,716, 24,837, 2,016, 87.3%; 2020: 42,209, 24,770, 1,860, 81.2%. The declared horizon is the newest
        window's two years; the other two windows predict one year ahead. A year is the finest step the source's
        dates give, and the use case names no refit cadence. SPLIT-33's target for 692,017 rows is 3 splits, and 3
        windows are built. All rows of a compound stay in one window; proteins recur, and a test compound may have
        a close chemical analogue in training.
    """
    prepared_raw_files = ("raw/" + PREPARED_FILE, "raw/" + STRUCTURE_KEYS_FILE)

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        directory = raw_dir / "raw"
        _check_md5(directory / ACTIVITY_FILE, ACTIVITY_MD5)
        _check_md5(directory / PROTEIN_FILE, PROTEIN_MD5)
        writer = None
        offset = 0
        selected_count = 0
        try:
            for chunk in pd.read_csv(
                directory / ACTIVITY_FILE,
                sep="\t",
                usecols=list(SOURCE_COLUMNS),
                dtype="string",
                chunksize=500_000,
            ):
                selected = chunk.loc[chunk["Quality"].eq("High")].copy()
                selected["source_row"] = pd.Series(
                    np.arange(offset, offset + len(chunk)),
                    index=chunk.index,
                ).loc[selected.index]
                offset += len(chunk)
                selected_count += len(selected)
                if not selected.empty:
                    table = pa.Table.from_pandas(selected, preserve_index=False)
                    if writer is None:
                        writer = pq.ParquetWriter(directory / PREPARED_FILE, table.schema, compression="zstd")
                    writer.write_table(table)
        finally:
            if writer is not None:
                writer.close()
        assert offset == 59_460_216, "Pinned source row count changed"
        assert selected_count == 1_369_350, "Pinned quality count changed"
        pairs = pd.read_parquet(directory / PREPARED_FILE)
        unique = pd.Series(
            pairs.loc[_known_endpoint_rows(pairs), "SMILES"].drop_duplicates().to_numpy(), dtype="string"
        )
        canonical = canonical_smiles(unique)
        canonical_unique = canonical.drop_duplicates()
        groups = scaffold_groups(canonical_unique)
        group_map = dict(zip(canonical_unique, groups, strict=True))
        keys = pd.DataFrame(
            {
                "SMILES": unique,
                "canonical_SMILES": canonical,
                "compound_scaffold": canonical.map(group_map),
            }
        )
        keys.to_parquet(directory / STRUCTURE_KEYS_FILE, index=False)

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        directory = raw_dir / "raw"
        pairs = pd.read_parquet(directory / PREPARED_FILE)
        proteins = pd.read_csv(directory / PROTEIN_FILE, sep="\t", dtype="string")
        assert proteins["target_id"].is_unique
        proteins = proteins.rename(
            columns={
                "Sequence": "protein_sequence",
                "Organism": "protein_organism",
                "Classification": "protein_classification",
                "Length": "protein_length",
            }
        )
        columns = ["target_id", "protein_sequence", "protein_organism", "protein_classification", "protein_length"]
        frame = pairs.merge(proteins[columns], on="target_id", how="left", validate="many_to_one", indicator=True)
        assert frame["_merge"].eq("both").all(), "Source target join lost a protein"
        frame = frame.drop(columns="_merge")
        keys = pd.read_parquet(directory / STRUCTURE_KEYS_FILE)
        assert keys["SMILES"].is_unique
        return frame.merge(keys, on="SMILES", how="left", validate="many_to_one")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        target = pd.to_numeric(raw["pchembl_value_Mean"], errors="coerce")
        selected = raw.loc[_known_endpoint_rows(raw) & np.isfinite(target)].copy()
        assert len(selected) == 692_017, "Pinned complete-mean eligibility changed"
        assert selected["canonical_SMILES"].notna().all()
        selected["SMILES"] = selected["canonical_SMILES"]
        selected[self.target] = target.loc[selected.index]
        # One canonical compound/protein pair must not acquire conflicting copies through representation repair.
        keys = ["SMILES", "target_id"]
        ambiguity = selected.groupby(keys, observed=True, sort=False)[self.target].transform("nunique").gt(1)
        selected = selected.loc[~ambiguity].drop_duplicates(keys)
        # The year the compound's measurements end, over the rows that ship (`temporal`, time_of="label").
        selected["entry_year"] = _entry_years(selected)
        frame = pd.DataFrame(
            {
                "SMILES": selected["SMILES"],
                "protein_id": selected["target_id"],
                "protein_sequence": selected["protein_sequence"],
                "protein_organism": selected["protein_organism"],
                "protein_classification": selected["protein_classification"],
                "protein_length": pd.to_numeric(selected["protein_length"], errors="coerce"),
                "protein_variant": selected["Protein_Type"],
                "entry_year": selected["entry_year"],
                self.target: selected[self.target],
            },
            index=selected.index,
        )
        frame["protein_length"] = frame["protein_length"].where(frame["protein_length"].gt(0))
        # This source level denotes an unknown annotation, not a biological protein class.
        frame["protein_classification"] = frame["protein_classification"].mask(
            frame["protein_classification"].eq("Unclassified protein")
        )
        # The framework's default hash sort includes the target and can be inverted after its fixed shuffle.
        # A unique structure/query key gives the same order regardless of labels or incoming raw row order; the
        # split column then orders the rows, keeping that label-independent order inside each year.
        frame = frame.sort_values(["SMILES", "protein_id"], kind="stable").sample(frac=1, random_state=42)
        return frame.sort_values("entry_year", kind="stable").reset_index(drop=True)

    def _make_splits(self, df: pd.DataFrame) -> SplitPlan:
        # The curator's windows (TEST_WINDOWS): the newest joins two years and the others are single years, which
        # one `TemporalSplits` window length cannot express. Training is every compound dated before the window,
        # and the frame is sorted by `entry_year`, so the rows of later years simply sit after the test window.
        year = df["entry_year"].to_numpy()
        splits = {}
        for repeat, (start, end) in enumerate(TEST_WINDOWS):
            train = np.flatnonzero(year < start)
            test = np.flatnonzero((year >= start) & (year < end))
            assert len(train) >= len(df) / 2, f"the window from {start} trains on less than half the rows"
            assert len(test) >= 33, f"the window from {start} tests fewer than 33 rows"
            splits[repeat] = {0: (train.tolist(), test.tolist())}
        return SplitPlan(splits=splits, df=df)

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        del df
        return FeatureTypes(
            categorical=["protein_id", "protein_organism", "protein_classification", "protein_variant"],
            string=["protein_sequence"],
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        known = _known_endpoint_rows(raw)
        counts = pd.DataFrame(
            {
                "state": [
                    "Full source",
                    "High-quality exact pairs",
                    "Recognized complete means",
                    "After representation checks",
                ],
                "rows": [59_460_216, len(raw), int(known.sum()), len(df)],
            }
        )
        return [
            Decision(
                title="Source pair means and the measured cohort",
                why=(
                    "Select complete source means with recognized measurement types; "
                    "retain pooled targets without new averaging."
                ),
                evidence=counts,
            )
        ]
