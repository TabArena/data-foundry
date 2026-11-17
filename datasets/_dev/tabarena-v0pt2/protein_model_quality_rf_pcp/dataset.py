"""RF-PCP GDT_TS quality regression."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Grouping, Metric, Source, TaskSummary


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
            "A structural-biology researcher ranks all candidate models generated for one protein, best to worst, "
            "before the experimental reference is available; scored by the correlation within each protein."
        ),
        row=(
            "One of 94,083 protein-structure candidate rows in the author's mixed CASP5-10 and classic-decoy "
            "release; 4,893 explicitly named native reference structures and the rosetta62 set's 1,011 relaxed native "
            "structures are excluded from this candidate population."
        ),
        predicted="Fractional GDT_TS at 1, 2, 4 and 8 angstrom tolerances; higher is better.",
        known=(
            "Candidate-structure total solvent-accessible area, cumulative aliphatic C-beta distances, empirical "
            "energy, secondary-structure score, the candidate's residue count and aliphatic pair count. The residue "
            "count is fixed per target in CASP6-9 and acts as the target's length; in CASP10 it is the candidate's "
            "own length and varies within all 67 targets."
        ),
        split=(
            "Whole canonical protein identities are held out. Protein identities are verified for "
            "342 CASP targets: 339 organizer links and three sequence checks. No alias overlaps a classic target."
        ),
        changes=(
            "Exclude explicitly named native references and relaxed natives; recover target keys; retain the "
            "original GDT_TS scale and all six supplied descriptors. Myunghwan selected GDT_TS after comparing all "
            "three targets."
        ),
        fit="approximate",
        fit_reason=(
            "The original task predicts quality before the experimental reference is known. Left out are inputs the "
            "researcher would have: the generating server and its own model rank, the decoy set, the target's full "
            "length. 64% of rows are classic decoy sets, several merged within one protein, and CASP10 descriptors "
            "follow another convention than CASP5-9; alignment conventions are unresolved."
        ),
    )
    unique_name = "protein_model_quality_rf_pcp"
    domain = "biology & life sciences"
    sources = (
        Source(
            role="publication",
            platform="Other",
            url="https://sourceforge.net/projects/rf-pcp/files/",
            license="No dataset licence stated in the author archive or inspected release listing",
            year="2014",
            bibtex="""
                @article{rana2015rfpcp,
                  title={Quality assessment of modeled protein structure using physicochemical properties},
                  author={Rana, Prashant Singh and Sharma, Harish and Bhattacharya, Mahua and Shukla, Anupam},
                  journal={Journal of Bioinformatics and Computational Biology},
                  volume={13}, number={2}, pages={1550005}, year={2015},
                  doi={10.1142/S0219720015500055}
                }
            """,
        ),
    )
    data_tags = ("UnseenGroup",)
    download_description = """
        Download the author's RF-PCP-DataSet.zip from
        https://downloads.sourceforge.net/project/rf-pcp/RF-PCP-DataSet.zip and extract its three CSVs under
        local-data-warehouse/protein_model_quality_rf_pcp/.
        Archive SHA256: d7d057c1f8043f7289fdbeed7cc36c26086650afc3e4ce7d8ad1228c09baef17.
        This candidate reads RF-PCP-Full-dataset.csv. The two other CSVs are retained as source evidence.
    """
    curation_comments = """
        - Prediction point: after generating a candidate structure, before its experimental reference is available.
        - Curator decision (2026-10-29, Myunghwan): Include GDT_TS as a historical tabular
          benchmark with the documented descriptor uncertainties. Source year 2014 and the
          identity-based exclusion of 4,893 native references are accepted; retain 95,094 rows
          (superseded 2026-11-05: 94,083 rows, the 1,011 relaxed natives leave too, CC below)
          and the three documented ambiguous zero-RMSD cases. Preserve source values and the
          historical approximate fit; no modern-generator or protein-family claim is made.
        - Models differ on the declared metric (TP-3): on the nine shipped splits, untuned LightGBM scores 0.322 and
          ridge 0.272, LightGBM higher in all nine (2026-11-05, without the relaxed natives; 0.355 against 0.294 with
          them, review panel 2026-11-04). The earlier five-fold comparison
          (ridge RMSE 0.19318568 against LightGBM 0.17894541, 7.37%) was measured for the RMSE fallback and is
          historical.
        - The author archive has 99,987 complete rows. Exclude 4,893 IDs beginning native_ or ending _native.pdb
          because this candidate
          population scores generated structures. Preserve zero-error generated models; do not filter on labels.
          Myunghwan approved this identity-based native-row exclusion. Two retained perfect-label
          IDs, casp5_T0156_1nxj.nNh1.pdb and ROSETTA_1aa2_1aa2h2.pdb, may be reference-like but their identities
          are unverified. Retain CASP10_T0676_HOMER_TS2.pdb: zero matched RMSD and low global scores can reflect
          limited alignment coverage; no label repair is supported by the source evidence.
        - CC (2026-11-05, Lennart): `grouping.context="all_rows"` (issue 5, B; SPLIT-23, USE-6; as sat11_hand_algo_runtime): the researcher holds all of a target's candidates when ranking them, so a model may compare a candidate with the other candidates of its protein. A model that does so (each descriptor's z-score and rank within its protein, the group size) scored 0.517 against 0.355 on the frame with the relaxed natives and 0.483 against 0.322 without them; that use is legitimate now, not an exploit. huesken_sirna_efficacy is reopened to follow (issue 9, A).
        - CC (2026-11-05, Lennart): the rosetta62 set's 1,011 relaxed natives leave by identity (issue 4, B; USE-7 via
          CLEAN-11), like the 4,893 named natives. Their IDs (`rosetta62_<pdb>_rn<pdb>.out.N.pdb`, matched on
          `_rn<pdb>.out.`) sit in the folder `relaxed_natives/` of the set's own archive (Zenodo 48780): the
          experimental structure energy-minimised, which exists only once the reference is known. The pattern matches
          only these 1,011 rosetta62 rows, none of the three zero-RMSD rows above; they held 8 of the 10 GDT_TS = 1
          rows and the best candidate in 55 of the 56 rosetta62 proteins. 94,083 rows and 445 proteins remain, each
          rosetta62 protein with at least 99 de novo decoys.
        - Predict GDT_TS in its supplied scale. Remove both alternative outcome columns and the structure ID
          from predictors. All six released descriptors remain numeric. No target transform or clipping.
        - Source Sections 2.2 and 2.3 define RMSD in angstroms and TM/GDT as fractional scores. Area is absolute
          solvent-accessible surface area; ED sums aliphatic C-beta distances; PN counts aliphatic residue pairs.
          SS compares STRIDE with PSIPRED. Its equation counts agreement but the prose says mismatch; retain the
          supplied number without complementing it. 5,620 scores exceed the row's sequence length and 5,414 the
          largest length in their protein; source coverage versus full-sequence alignment is unverified. No native-reference leakage is demonstrated.
          The retrieved archive has no feature-generation code; row-level generation was not reconstructed.
        - ED is a sum of pair distances over the PN pairs, and PN is fixed by the sequence (constant within protein
          and sequence length in 1,143 of 1,245 cells). A sum over one or more pairs cannot be 0, and a sum over no
          pairs cannot be positive, so ED = 0 with PN > 0 (71 rows) and PN = 0 with ED > 0 (60 rows) become missing
          and the rows stay (CLEAN-11; Lennart, 2026-11-04). 129 of the 131 rows have a same-protein, same-length
          sibling with the value positive (counts of 2026-11-05, without the relaxed natives); the other two
          (CASP10_T0692_FALCON-TOPO_TS5.pdb and CASP10_T0716_sysimm_TS4.pdb) are the only rows of their length in a
          protein whose other rows are positive.
        - SL counts the residues of the candidate model. In CASP6-9 and the ROSETTA, John2002 and rosetta62 sets it
          is constant within every target, so it acts as the target's length; in CASP10 it varies within all 67
          targets (and within 2 of 37 CASP5 targets and 12 classic-set proteins), so it measures the candidate's
          coverage of a GDT_TS normalised by the target's length. On the CASP10 targets of the shipped splits,
          ranking by SL alone scores 0.50 on the metric and a row-only LightGBM 0.05 (review panel, 2026-11-04;
          the same without the relaxed natives, 2026-11-05).
          The full file has 2,259 CASP10 rows that the paper's validation file lacks (66 of 67 targets, median
          GDT_TS 0.238 against 0.441).
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
          correlation within each protein averaged over proteins, because the use case ranks one protein's
          candidates. The paper reports RMSE, correlation, R2 and tolerance accuracy side by side; pooled RMSE rewards
          a protein's typical quality, and each protein's true mean, which orders no candidate, beats LightGBM on it
          (0.124 against 0.187 on the nine shipped splits, 2026-11-05; 0.134 against 0.188 with the relaxed natives).
          The correlation stands in for the top-1 GDT_TS loss (the best candidate's GDT_TS
          minus the picked one's) that CASP11-14 use to score picking a model; both rank three test models the same
          way (review panel, 2026-11-04). A protein whose candidates all get the same prediction scores 0; a protein
          whose GDT_TS does not vary would be left out, and there is none (the library's rule since 2026-11-05).
          Each test fold holds 148-149 proteins with a median of 102-108 candidates,
          at least 13. In the 19 proteins merged across decoy collections (26% of rows), the score partly rewards
          telling the collections apart, about +0.01 on the fold mean.
        - `Energy` stays as supplied (Lennart, 2026-11-04): the extreme positive values (up to 7e11) are ProSEE's
          output for unminimized models whose atoms overlap, continuous with the rest and carrying signal (mean GDT_TS
          0.339 against 0.398), so unusual rather than impossible (CLEAN-11). `SS` has no bound the source gives.
        - CC (2026-11-12, Andrej): the split stays by protein ("I go back to by split by protein", issue 11, which
          answers issue 10; SPLIT-34): a split by CASP round was weighed and is not built. Windows by round score
          within 0.03 of a same-size protein split on CASP8 and CASP9 and 0.03 to 0.07 lower on CASP7; CASP10 scores
          about 0 under any split that trains on the earlier rounds, a change of descriptor convention rather than
          time (splits_comment).
        - Outdated (Lennart, 2026-11-04): six global descriptors of 2002-2012 server models; since CASP15 the
          standard is the predictor's own confidence (pLDDT). Kept as a small grouped biology task, with no new features.
        - First release is the August 2014 source archive; the paper appeared online in December 2014 and in 2015.
          The year denotes the first release, not the paper's issue year. No source metadata is overwritten silently.
        - Time basis: UnseenGroup (Andrej, 2026-11-13; `Timeless` before): the use case ranks the candidates of a
          protein whose structure is not known, so the split holds out whole proteins. A candidate's GDT against its
          reference is fixed once both exist; windows by CASP round score within 0.03 of the protein split on CASP8 and
          CASP9. It cannot test candidates from later prediction methods (the descriptors come from 2002-2012 server
          models).
    """
    target = "GDT"
    problem_type = "regression"
    metric = Metric.from_context(
        "mean_group_pearsonr",
        reason=(
            "The use case ranks the candidate structures of one target, so each target is scored on its own (CASP10's "
            "quality assessment reports per-target and pooled correlation side by side). The per-target correlation "
            "stands in for the top-1 GDT_TS loss of picking the best model and ranks models the same way. Rana et al. "
            "(DOI 10.1142/S0219720015500055) report RMSE, correlation, R2 and tolerance accuracy side by side. Pooled "
            "RMSE does not score the decision: each protein's true mean, which orders no candidate, beats LightGBM on "
            "it (0.124 against 0.187). A protein whose predictions are all equal scores 0 instead of being left out, "
            "so declining to rank a protein earns nothing over a guess. Exception to MET-5 (Lennart, 2026-11-04)."
        ),
        inputs={"group": "protein_id"},
    )
    grouping = Grouping(
        on="protein_id",
        labels="per_sample",
        prediction_unit="row",
        context="all_rows",
        definition=(
            "A group collects candidates for one canonical protein. CASP uses T identifiers and classic "
            "decoys use native PDB identifiers. Source Section 2.2 defines quality relative to experimental structure; "
            "Evaluation holds out target proteins. Verified same-protein accession aliases are merged. "
            "Cross-source alias completeness is an open qualification issue, not established by the group checks. "
            "A target's candidates are in hand together when they are ranked (CASP releases a target's server models "
            "at once), so a model may see all rows of a test protein (`all_rows`)."
        ),
    )
    splits_comment = """
        Default repeated three-fold grouped evaluation with seed 4267. All rows of each recovered target key stay
        together, including verified same-protein accession aliases. The selected GDT task and preserved target alternatives share test groups;
        membership is verified explicitly.
        All 342 CASP identities are verified; three retain source IDs. Sequence-family independence is not claimed.
        The source's own files train on CASP5-9 and the classic sets and validate on CASP10. Forward windows by CASP
        round (train on all earlier rows, untuned LightGBM, per-protein correlation) score CASP8 0.339, CASP9 0.484
        and CASP10 0.009; through CASP9 they match the grouped folds within 0.04 (2026-11-05, without the relaxed
        natives; 0.340, 0.483, 0.016 and 0.03 with them), so the rounds show no drift, and
        CASP10's low score comes from its other descriptor convention (the SL note), not from time. The grouped
        split is kept (Andrej, 2026-11-12: "I go back to by split by protein").
    """
    accepted_check_warnings = {}

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "RF-PCP-Full-dataset.csv")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        is_reference = raw["PDB-ID"].str.startswith("native_") | raw["PDB-ID"].str.endswith("_native.pdb")
        # rosetta62's relaxed natives (the archive's relaxed_natives/ folder) are references too (USE-7 via CLEAN-11).
        is_relaxed_native = raw["PDB-ID"].str.contains(r"_rn[0-9a-z]{4}\.out\.", regex=True)
        df = raw.loc[~(is_reference | is_relaxed_native)].copy()
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
