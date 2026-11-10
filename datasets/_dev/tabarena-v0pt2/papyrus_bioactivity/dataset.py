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
    Grouping,
    Metric,
    Smiles,
    TaskSummary,
    canonical_smiles,
    scaffold_groups,
)

ACTIVITY_FILE = "05.7_combined_set_without_stereochemistry.tsv.xz"
PROTEIN_FILE = "05.7_combined_set_protein_targets.tsv.xz"
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


def _alias_safe_scaffolds(frame: pd.DataFrame) -> pd.Series:
    # The source connectivity identifies chemical aliases even when their tautomer scaffolds differ.
    pairs = frame[["connectivity", "scaffold"]].drop_duplicates()
    aliases = pairs.loc[pairs["connectivity"].duplicated(keep=False)]
    parent: dict[str, str] = {}

    def root(group: str) -> str:
        while group in parent:
            group = parent[group]
        return group

    for _, rows in aliases.groupby("connectivity", sort=False, observed=True):
        roots = {root(group) for group in rows["scaffold"]}
        representative = min(roots)
        for group in roots - {representative}:
            parent[group] = representative
    return frame["scaffold"].replace({group: root(group) for group in parent})


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
            "Chemical scaffolds are held out across all proteins. The test compounds are from unseen chemical series; "
            "proteins may recur. This is structural generalization, not a prospective chronological evaluation."
        ),
        changes=(
            "We keep high-quality exact means composed solely of recognized potency types, join intrinsic protein "
            "metadata, remove source/provenance and outcome-derived predictors, and hold out compound scaffolds."
        ),
        fit="approximate",
        fit_reason=(
            "Published mean log potency combines assay types and laboratories without a fixed experimental protocol. "
            "Scaffold holdout tests new chemistry; it does not establish that historical training labels "
            "preceded test dates. Structures omit stereochemistry, and exact reported potency measurements "
            "do not represent a complete prospective screening library."
        ),
    )
    unique_name = "papyrus_bioactivity"
    year = "2021"
    domain = "chemistry & material science"
    source = "Other"
    source_url = "https://doi.org/10.4121/16896406.v1"
    license = "CC BY-SA 4.0"
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
    bibtex = """
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
        - Canonical structure/scaffold is computed once per compound. Exact copies are removed; conflicting
          canonical-pair labels leave as ambiguous copies, without averaging. Three source-connectivity aliases
          include two crossing scaffold keys: union those components by recorded identity, without labels.
        - The inherited whole-row hash ordering encoded labels: a training-only attack recovered 185/200 labels,
          independently 360/400. Disable that ordering; sort known structure/protein inputs then shuffle seed42.
          Full target perturbations leave the repaired order invariant. Source labels and fold membership stay intact.
        - Scaffold groups span all proteins; proteins and close analogs may recur across folds. Assay IDs,
          outcome summaries/counts, quality/endpoint flags, document provenance and years never enter predictors.
        - Year is the first interaction document, not complete label availability: 9,386 retained pairs have Year<2013
          but contributing years>=2013. This is not temporal evaluation. Any temporal variant must establish all
          training outcomes collected before test prediction. Outcome-filtered Papyrus++ is not used; broader
          source standardization is not certified independent of every label.
        - The paper reports RMSE and Pearson without one primary score. Use fallback RMSE on the unchanged log scale.
        - PROV-7: this protein-conditioned interaction task differs from fixed-target QSAR: 129,427 multi-protein
          compounds supply 365,480 rows. Measured ChEMBL overlap is 1,616 IDs/2,257 rows, including 864 same-thrombin
          pairs. Pooling or a small overlap fraction alone does not establish uniqueness. Parent/stereo equivalence
          and comprehensive sibling overlap remain unverified; no legacy QSAR task is changed.
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
    grouping = Grouping(
        on="scaffold",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition=(
            "One group is a compound Bemis-Murcko scaffold across all protein targets. Ringless compounds and "
            "compounds in a scaffold exceeding 10% of unique compounds are individually grouped by structure. "
            "The molecular scaffold default (SPLIT-31) models new chemical series before assay; the source's "
            "pooled PCM models motivate the protein-conditioned target, not a both-endpoint holdout."
        ),
    )
    splits_comment = """
        Default grouped folds hold out whole compound scaffolds across all proteins. A compound and every one of its
        compound-protein outcomes remain on one side. Proteins may be present on both sides; some sparse targets may
        occur only in test. The scaffold share is computed over unique compounds, not their number of measured targets.
        Scaffold components connected by the same source compound connectivity are joined, so aliases cannot cross.
        Sorted one-to-one numeric scaffold codes are used only inside the default splitter to avoid slow text
        membership checks; the published scaffold values and default folds are unchanged.
        The frame is ordered by canonical structure and protein identity then shuffled with seed42, independently
        of labels. The source also reports random and temporal splits; this tests structural generalization only.
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
        selected["scaffold"] = selected["compound_scaffold"]
        selected["scaffold"] = _alias_safe_scaffolds(selected)
        selected[self.target] = target.loc[selected.index]
        # One canonical compound/protein pair must not acquire conflicting copies through representation repair.
        keys = ["SMILES", "target_id"]
        ambiguity = selected.groupby(keys, observed=True, sort=False)[self.target].transform("nunique").gt(1)
        selected = selected.loc[~ambiguity].drop_duplicates(keys)
        frame = pd.DataFrame(
            {
                "SMILES": selected["SMILES"],
                "protein_id": selected["target_id"],
                "protein_sequence": selected["protein_sequence"],
                "protein_organism": selected["protein_organism"],
                "protein_classification": selected["protein_classification"],
                "protein_length": pd.to_numeric(selected["protein_length"], errors="coerce"),
                "protein_variant": selected["Protein_Type"],
                "scaffold": selected["scaffold"],
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
        # A unique structure/query key gives the same order regardless of labels or incoming raw row order.
        return frame.sort_values(["SMILES", "protein_id"], kind="stable").sample(frac=1, random_state=42)

    def _make_splits(self, df: pd.DataFrame):
        # GroupKFold shuffles sorted unique keys. One-to-one sorted codes preserve those exact folds while
        # avoiding NumPy's quadratic object-string membership path on hundreds of thousands of scaffold keys.
        coded = df.assign(scaffold=pd.Categorical(df["scaffold"], categories=sorted(df["scaffold"].unique())).codes)
        plan = self.default_splits(coded)
        plan.df = df
        return plan

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        del df
        return FeatureTypes(
            categorical=["protein_id", "protein_organism", "protein_classification", "protein_variant"],
            string=["protein_sequence", "scaffold"],
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
