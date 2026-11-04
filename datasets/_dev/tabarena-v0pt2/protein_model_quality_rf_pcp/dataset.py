"""RF-PCP GDT_TS quality regression."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Grouping, Metric, TaskSummary


def protein_key(name: str) -> str:
    """Recover a source protein identifier without using features or labels."""
    casp = re.match(r"(?i)casp\d+_(T\d+)_", name)
    if casp:
        return "casp:" + casp[1].upper()
    patterns = (
        r"(?i)(?:ROSETTA|rosetta62)_([0-9][a-z0-9]{3})",
        r"(?i)John2002__([0-9][a-z0-9]{3})",
        r"(?i)fisa_(?:casp3_)?([a-z0-9]{4})",
        r"(?i)lattice_ssfit_([0-9][a-z0-9]{3})",
        r"(?i)4state_reduced_([0-9][a-z0-9]{3})",
        r"(?i)lmds_([0-9][a-z0-9]{3})",
    )
    for pattern in patterns:
        match = re.match(pattern, name)
        if match:
            identity = match[1].lower()
            return ("legacy:" if identity == "smd3" else "pdb:") + identity
    raise ValueError(f"Unrecognized protein identity: {name}")


class RfPcp(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="What fraction of reference residues aligns within the source's four GDT distance tolerances?",
        use_case=(
            "A structural-biology researcher ranks the candidate models generated for one protein before the "
            "experimental reference is available, to choose which to refine; scored by the correlation per protein."
        ),
        row=(
            "One of 95,094 protein-structure candidate rows in the author's mixed CASP5-10 and classic-decoy "
            "release; 4,893 explicitly named native reference structures are excluded from this candidate population."
        ),
        predicted="Fractional GDT_TS at 1, 2, 4 and 8 angstrom tolerances; higher is better.",
        known=(
            "Candidate-structure total solvent-accessible area, cumulative aliphatic C-beta distances, empirical "
            "energy, secondary-structure score, sequence length and aliphatic pair count."
        ),
        split=(
            "Whole canonical protein identities are held out. Protein identities are verified for "
            "342 CASP targets: 339 organizer links and three sequence checks. No alias overlaps a classic target."
        ),
        changes=(
            "Exclude explicitly named native references; recover target keys; retain the original GDT_TS "
            "scale and all six supplied descriptors. Myunghwan selected GDT_TS after comparing all three targets."
        ),
        fit="approximate",
        fit_reason=(
            "The original task predicts quality before the experimental reference is known. The historical mix "
            "of model generators and unresolved descriptor and alignment conventions limit interpretation."
        ),
    )
    unique_name = "protein_model_quality_rf_pcp"
    raw_data_from = "protein_model_quality_rf_pcp"
    year = "2014"
    domain = "biology & life sciences"
    source = "Other"
    source_url = "https://sourceforge.net/projects/rf-pcp/files/"
    license = "No dataset licence stated in the author archive or inspected release listing"
    download_description = """
        Download the author's RF-PCP-DataSet.zip from
        https://downloads.sourceforge.net/project/rf-pcp/RF-PCP-DataSet.zip and extract its three CSVs under
        local-data-warehouse/protein_model_quality_rf_pcp/.
        Archive SHA256: d7d057c1f8043f7289fdbeed7cc36c26086650afc3e4ce7d8ad1228c09baef17.
        This candidate reads RF-PCP-Full-dataset.csv. The two other CSVs are retained as source evidence.
    """
    bibtex = """
        @article{rana2015rfpcp,
          title={Quality assessment of modeled protein structure using physicochemical properties},
          author={Rana, Prashant Singh and Sharma, Harish and Bhattacharya, Mahua and Shukla, Anupam},
          journal={Journal of Bioinformatics and Computational Biology},
          volume={13}, number={2}, pages={1550005}, year={2015},
          doi={10.1142/S0219720015500055}
        }
    """
    curation_comments = """
        - Prediction point: after generating a candidate structure, before its experimental reference is available.
        - Curator decision (2026-10-29, Myunghwan): Include GDT_TS as a historical tabular
          benchmark with the documented descriptor uncertainties. Source year 2014 and the
          identity-based exclusion of 4,893 native references are accepted; retain 95,094 rows
          and the three documented ambiguous zero-RMSD cases. Preserve source values and the
          historical approximate fit; no modern-generator or protein-family claim is made.
        - On five identical protein-held-out folds, Ridge RMSE is 0.19318568 and training-side-selected
          LightGBM RMSE is 0.17894541, a 7.37% RMSE reduction. The slight difference from TM-score's
          7.14% is not evidence of a significant advantage or maximum future improvement.
          All nine-fold qualification results remain applicable after exact frame/fold equivalence checks.
        - The author archive has 99,987 complete rows. Exclude 4,893 IDs beginning native_ or ending _native.pdb
          because this candidate
          population scores generated structures. Preserve zero-error generated models; do not filter on labels.
          Myunghwan approved this identity-based native-row exclusion. Two retained perfect-label
          IDs, casp5_T0156_1nxj.nNh1.pdb and ROSETTA_1aa2_1aa2h2.pdb, may be reference-like but their identities
          are unverified. Retain CASP10_T0676_HOMER_TS2.pdb: zero matched RMSD and low global scores can reflect
          limited alignment coverage; no label repair is supported by the source evidence.
        - Predict GDT_TS in its supplied scale. Remove both alternative outcome columns and the structure ID
          from predictors. All six released descriptors remain numeric. No target transform or clipping.
        - Source Sections 2.2 and 2.3 define RMSD in angstroms and TM/GDT as fractional scores. Area is absolute
          solvent-accessible surface area; ED sums aliphatic C-beta distances; PN counts aliphatic residue pairs.
          SS compares STRIDE with PSIPRED. Its equation counts agreement but the prose says mismatch; retain the
          supplied number without complementing it. Some scores exceed the modeled-structure sequence length;
          source coverage versus full-sequence alignment is unverified. No native-reference leakage is demonstrated.
          The retrieved archive has no feature-generation code; row-level generation was not reconstructed.
        - ED is a sum of pair distances over the PN pairs, and PN is fixed by the sequence (constant within protein
          and sequence length in 1,146 of 1,249 cells). A sum over one or more pairs cannot be 0, and a sum over no
          pairs cannot be positive, so ED = 0 with PN > 0 (71 rows) and PN = 0 with ED > 0 (63 rows) become missing
          and the rows stay (CLEAN-11; Lennart, 2026-11-04). Each of those rows has a same-protein, same-length
          sibling with the value positive.
        - Energy is signed in the release despite absolute-sum prose; retain signs and extreme finite values.
          Neither a large magnitude nor a negative energy is itself proof of a recording error or leakage.
        - Protein keys come from source filenames. CASP keys use T identifiers, case-normalized; classic sets use
          native PDB accessions, conservatively merging chain variants and collections. Legacy smd3 is distinct.
          The required, hash-verified protein_aliases.json merges six verified same-protein components across PDB
          accessions and collections (14 source keys become six groups), using RCSB sequences and UniProt identity.
          No key is inferred by feature clustering or target values.
        - Official CASP pages map 339 observed targets to experimental PDB accessions, none shared with classic
          targets. Three further identities are confirmed by exact sequences and retain original keys, with no
          colliding aliases. This is not a sequence-family split.
        - The metric (Lennart, 2026-11-04; exception to MET-5): `mean_group_pearsonr` on `protein_id`, the
          correlation within each protein averaged over proteins, as CASP scores quality assessment per target. The
          paper reports RMSE, correlation, R2 and tolerance accuracy side by side; pooled RMSE rewards a protein's
          typical quality, and each protein's true mean, which orders no candidate, beats LightGBM on it (0.134
          against 0.188). Each test fold holds 148-149 proteins with a median of 103-113 candidates, none under 5.
        - `Energy` stays as supplied (Lennart, 2026-11-04): the extreme positive values (up to 7e11) are ProSEE's
          output for unminimized models whose atoms overlap, continuous with the rest and carrying signal (mean GDT_TS
          0.339 against 0.398), so unusual rather than impossible (CLEAN-11). `SS` has no bound the source gives.
        - Outdated (Lennart, 2026-11-04): six global descriptors of 2002-2012 server models; since CASP15 the
          standard is the predictor's own confidence (pLDDT). Kept as a small grouped biology task, with no new features.
        - First release is the August 2014 source archive; the paper appeared online in December 2014 and in 2015.
          The year denotes the first release, not the paper's issue year. No source metadata is overwritten silently.
    """
    target = "GDT"
    problem_type = "regression"
    metric = Metric.from_context(
        "mean_group_pearsonr",
        reason=(
            "The use case ranks the candidate structures of one target, as CASP's quality assessment scores it per "
            'target (CASP10: "the two assessment approaches show different qualities of the methods and we use both of '
            'them"). Rana et al. (DOI 10.1142/S0219720015500055) report RMSE, correlation, R2 and tolerance accuracy '
            "side by side. Pooled RMSE does not score the decision: each protein's true mean, which orders no candidate, "
            "beats LightGBM on it (0.134 against 0.188). Exception to MET-5 (Lennart, 2026-11-04)."
        ),
        inputs={"group": "protein_id"},
    )
    grouping = Grouping(
        on="protein_id",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition=(
            "A group collects candidates for one canonical protein. CASP uses T identifiers and classic "
            "decoys use native PDB identifiers. Source Section 2.2 defines quality relative to experimental structure; "
            "Evaluation holds out target proteins. Verified same-protein accession aliases are merged. "
            "Cross-source alias completeness is an open qualification issue, not established by the group checks."
        ),
    )
    splits_comment = """
        Default repeated three-fold grouped evaluation with seed 4267. All rows of each recovered target key stay
        together, including verified same-protein accession aliases. The selected GDT task and preserved target alternatives share test groups;
        membership is verified explicitly.
        All 342 CASP identities are verified; three retain source IDs. Sequence-family independence is not claimed.
    """
    accepted_check_warnings = {}

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "RF-PCP-Full-dataset.csv")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        is_reference = raw["PDB-ID"].str.startswith("native_") | raw["PDB-ID"].str.endswith("_native.pdb")
        df = raw.loc[~is_reference].copy()
        df["protein_id"] = df["PDB-ID"].map(protein_key)
        mapping_bytes = (self.folder / "protein_aliases.json").read_bytes()
        expected = "6ca86a5b32cad72d6795dd629f99be918115be0eb9bba5b87fb32746d437c187"
        if hashlib.sha256(mapping_bytes).hexdigest() != expected:
            raise ValueError("RF-PCP grouping requires the reviewed protein identity map")
        aliases = json.loads(mapping_bytes)
        df["protein_id"] = df["protein_id"].map(lambda key: aliases.get(key, key))
        df = df[["Area", "ED", "Energy", "SS", "SL", "PN", self.target, "protein_id"]]
        # A sum of distances over one or more pairs is positive, and no pairs give no distance (CLEAN-11).
        no_distance, no_pairs = df["ED"].eq(0) & df["PN"].gt(0), df["PN"].eq(0) & df["ED"].gt(0)
        df.loc[no_distance, "ED"] = float("nan")
        df.loc[no_pairs, "PN"] = float("nan")
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["protein_id"])
