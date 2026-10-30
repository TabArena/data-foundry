"""Huesken siRNA efficacy from the corrected original supplement."""

from __future__ import annotations

import itertools
import re
from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, Grouping, Metric, TaskSummary

DG = dict(
    zip(
        ("AA", "UU", "AU", "UA", "CU", "AG", "CA", "UG", "GU", "AC", "GA", "UC", "CG", "GG", "CC", "GC"),
        (
            -0.93,
            -0.93,
            -1.10,
            -1.33,
            -2.08,
            -2.08,
            -2.11,
            -2.11,
            -2.24,
            -2.24,
            -2.35,
            -2.35,
            -2.36,
            -3.26,
            -3.26,
            -3.42,
        ),
    )
)
DH = dict(
    zip(
        DG,
        (
            -6.82,
            -6.82,
            -9.38,
            -7.69,
            -10.48,
            -10.48,
            -10.44,
            -10.44,
            -11.40,
            -11.40,
            -12.44,
            -12.44,
            -10.64,
            -13.39,
            -13.39,
            -14.88,
        ),
    )
)
TD_NAMES = (
    "ends",
    "DG_1",
    "DH_1",
    "U_1",
    "G_1",
    "DH_all",
    "U_all",
    "UU_1",
    "G_all",
    "GG_1",
    "GC_1",
    "GG_all",
    "DG_2",
    "UA_all",
    "U_2",
    "C_1",
    "CC_all",
    "DG_18",
    "CC_1",
    "GC_all",
    "CG_1",
    "DG_13",
    "UU_all",
    "A_19",
)


def reverse_complement(seq):
    """Reverse-complement the RNA guide without consulting the label."""
    return seq.translate(str.maketrans("AUCG", "UAGC"))[::-1]


def descriptors(seq):
    """The 24 label-free descriptors in OligoFormer's published preprocessing."""
    pairs = [seq[i : i + 2] for i in range(18)]
    left, right = pairs[0], pairs[-1]

    def signs(pair):
        return int(pair in ("AC", "AG", "UC", "UG")) - int(pair in ("GA", "GU", "CA", "CU"))

    ends = round(DG[left] - DG[right] + (signs(left) + signs(right)) * 0.45, 2)
    enthalpy = 3.61 + sum(seq[i] in "AU" for i in (0, -1)) * 3.72 + sum(DH[p] for p in pairs)
    return (
        ends,
        DG[left],
        DH[left],
        int(seq[0] == "U"),
        int(seq[0] == "G"),
        enthalpy,
        seq.count("U") / 19,
        int(left == "UU"),
        seq.count("G") / 19,
        int(left == "GG"),
        int(left == "GC"),
        pairs.count("GG") / 18,
        DG[pairs[1]],
        pairs.count("UA") / 18,
        int(seq[1] == "U"),
        int(seq[0] == "C"),
        pairs.count("CC") / 18,
        DG[right],
        int(left == "CC"),
        pairs.count("GC") / 18,
        int(left == "CG"),
        DG[pairs[12]],
        pairs.count("UU") / 18,
        int(seq[-1] == "A"),
    )


class SirnaEfficacy(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How strongly will a candidate siRNA inhibit its target in the source's reporter assay?",
        use_case="A researcher selects siRNAs to synthesize and test for a gene without previous efficacy measurements, using the candidate guide and the known target insert sequence.",
        row="One of 2,431 siRNAs in the corrected Huesken 2005 training and test library, with a measured normalized inhibitory activity and an exact match to a published target insert.",
        predicted="The source's normalized inhibitory activity, on its published scale. Its assay controls map to 0.900 and 0.354; it is not a probability or a percentage and may exceed one.",
        known="The 19 RNA bases and two DNA overhang bases of the guide, the 57-base target window with flanks, and fixed sequence-derived descriptors. No assay result is used as an input.",
        split="Whole target genes are held out, including both inserts of the same rodent gene. Each candidate is scored individually; target gene labels are excluded from model inputs.",
        changes="Restore the 70 UBE2H rows omitted by OligoFormer's 2,361-row file; retain the original target scale and both guide overhang bases. Use categorical nucleotide positions, trimer counts and the published 24 descriptors.",
        fit="approximate",
        fit_reason="This tests pre-assay efficacy prediction within one reporter system. Transfer to endogenous expression, other cell systems, dosing or therapeutic outcomes is not established.",
    )
    unique_name = "dataset_from_uncertainty_guided_model_selection_for_tabular_foundation_models_in_biomolecule_efficacy_prediction"
    year = "2005"
    domain = "biology & life sciences"
    source = "Other"
    source_url = "https://doi.org/10.1038/nbt1118"
    license = "Not stated for the original supplementary data; publisher rights apply. No explicit redistribution license was found for the original data."
    download_description = """
        Download Huesken's corrected supplementary Tables 2 and 3, then convert with poppler pdftotext -layout:
        https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fnbt1118/MediaObjects/41587_2005_BFnbt1118_MOESM3_ESM.pdf -> table2.pdf
        https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fnbt1118/MediaObjects/41587_2005_BFnbt1118_MOESM4_ESM.pdf -> table3.pdf
        pdftotext -layout table2.pdf table2.txt
        pdftotext -layout table3.pdf table3.txt
        Place the two text inputs in this dataset's warehouse directory. Two ambiguous guide matches are resolved using the original Table 3 human/rodent membership flags, without using efficacy.
        Verified original PDF SHA256: Table 2 c33063d8621e9318f04d7c8c07ca8e5422b81b336c4a48ac664b3daf26abee8f; Table 3 4d6cbaca93d98fa738659dfaf68875af3039b2061a94aa550b0c5a5b10e83d63.
    """
    bibtex = """
        @article{huesken2005sirna,
          title={Design of a genome-wide siRNA library using an artificial neural network},
          author={Huesken, Dieter and Lange, Joerg and Mickanin, Craig and others},
          journal={Nature Biotechnology}, volume={23}, pages={995--1001}, year={2005}, doi={10.1038/nbt1118}
        }
    """
    curation_comments = """
        Start with the corrected Huesken supplementary Table 3 and target inserts in Table 2, not model-generated labels from the withdrawn early supplement.

        - Prediction point: before synthesis and the reporter assay. The candidate guide and target sequence are known; assay measurements, NAS identifiers and original train/test flags are never features (USE-3, LEAK-10).
        - All 2,431 original guide sequences and activities are retained. OligoFormer's raw copy contains 2,361 exact activity matches but omits all 70 UBE2H guides; its processed label also divides by the observed maximum, 1.341. Neither omission nor this extra scaling is carried over (PROV-13, MET-3).
        - The original Table 3 footnote specifies a linear assay-control normalization: positive control 0.900, negative control 0.354. Values above one remain measured normalized values, never clipped or called probabilities. The 2005 corrigendum (doi:10.1038/nbt1005-1315a) replaced predicted scores with these measured activities.
        - Group on the exact source species and gene symbol recovered by reverse-complement matching to Table 2. There are 30 observed gene groups in 34 published inserts; both Mmp7 inserts remain one gene group. Two ambiguous guide matches are resolved from Table 3 species flags: NAS 18412 is rodent (Rn P2rx2), NAS 19819 human (Hs P2RX3). The copy incorrectly gives NAS 18412 the human target window; it is repaired from the original, without using labels or row order (SPLIT-24, PROV-13).
        - Restore both DNA overhang bases as categorical positions, distinct from the RNA positions. The target window is 19 binding bases plus 19 flanking bases on either side. X means outside the insert; N and R retain the source's unresolved base codes in the positional features. Fixed trimer counts map N/R to X; no sequence is guessed.
        - Thermodynamic and composition descriptors use the 19 RNA bases and the fixed OligoFormer preprocessing constants. Categorical positions preserve the sequence; the redundant published one-hot encoding is left to the learner. Drop only constant and exactly duplicated feature columns, in a deterministic order (CLEAN-8). The ten explicit yes/no sequence descriptor flags are categorical; counts and continuous descriptors remain numeric (CLEAN-14). The terminal descriptor follows the inherited executable convention, round(DG[first] - DG[last] + 0.45*(sign(first)+sign(last)), 2), where sign is +1 for AC/AG/UC/UG, -1 for GA/GU/CA/CU, and 0 otherwise. This differs from the printed Li Appendix A terminal correction; DH uses -14.88 for GC rather than the printed -14.882. These fixed operational descriptors are retained, not asserted to be exact reproductions of the printed physical formula.
        - RMSE is an evidence-limited fallback: no unique original selection criterion was established in the material obtained. The generated generic fallback gloss is not proof that the original source defined no metric; the original full methods were not retrieved. See the metric reason for the actual sources checked.
        - The grouped task tests a new gene in this reporter assay. It does not certify efficacy on endogenous targets, unfamiliar experimental conditions or clinical outcomes. All original random train/test flags are discarded in favor of gene-held-out evaluation (SPLIT-4, SPLIT-5). Pooled RMSE measures activity magnitude accuracy, not demonstrated within-gene top-k selection success; no synthesis budget or decision threshold is invented.

        - CC (2026-10-26, Myunghwan): accepted the small-gene warning for this add-stage task because individual siRNAs have varying measured activities and sufficient test-row support. Even five test genes can be acceptable in this case; retain the qualified ten-gene native folds. This is a case-specific warning acceptance, not a new minimum-group rule. The separate final ship verdict was explicitly given by Myunghwan on 2026-10-28. Grouped evaluation targets an unseen species/gene ID with no measured candidates (cold start); OOD here names that unseen-entity evaluation, not a separately established shift in assay conditions.
    """
    target = "normalized_inhibitory_activity"
    problem_type = "regression"
    metric = Metric.fallback(
        reason="Checked Huesken's publisher abstract and corrected Tables 2/3, its two corrigenda, and Li et al. 2025 (arXiv:2510.02476, Tables 1-3). The later paper reports MAE and Pearson correlation side by side without one unique selection criterion. The original full methods could not be retrieved; its abstract's Pearson headline alone does not establish a deliberate unique metric (MET-5). Use regression fallback RMSE on the original published activity scale."
    )
    grouping = Grouping(
        on="target_gene",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="One group is the exact species and gene symbol of a Table 2 target insert, matched to each guide and its target context. Both inserts of Rn Mmp7 share a group. The source designed a genome-wide siRNA library; the intended use predicts individual candidate efficacy for a target gene with no measured candidates. Thirty observed genes are held out whole; guide and target sequences are known, assay labels are not.",
    )
    splits_comment = "Default repeated three-fold group protocol on whole species/gene labels; 30 genes provide 10 unseen genes per test fold. Individual siRNAs are prediction units. This replaces the original random training/test allocation and keeps the two Mmp7 inserts together. Row scoring gives larger candidate panels more weight. Repeats reuse the same thirty genes; split variation and standard errors are descriptive, not thirty independent biological experiments."
    accepted_check_warnings = {
        "groups_test_groups_few": "Accepted 2026-10-26, Myunghwan: 30 genes are sufficient for this per-siRNA continuous-activity task when test-row support is adequate; even five held-out genes can be acceptable in this case. The unchanged native folds hold ten genes and 648-942 rows, and several model families show held-out-gene signal. Repeats reuse the same genes; no universal row-count-only sufficiency rule or broader assay transfer is asserted."
    }

    def _load_raw(self, raw_dir: Path):
        inserts = []
        current = None
        for source_line in (raw_dir / "table2.txt").read_text().splitlines():
            line = source_line.replace("\f", "")
            match = re.match(r"^(Hs|Rn)\s+(\S+)\s+([ACGTRYNWSMKBDHV]+)\s+(\d+)\s*$", line)
            if match:
                current = dict(gene=match[1] + " " + match[2], sequence=match[3], length=int(match[4]))
                inserts.append(current)
            elif current and re.fullmatch(r"[ACGTRYNWSMKBDHV]+", line[14:].strip()):
                current["sequence"] += line[14:].strip()
        assert len(inserts) == 34
        assert all(len(t["sequence"]) == t["length"] for t in inserts)
        source_rows = re.findall(
            r"^\s*(\d+)\s+([ACGU]{19}[acgtu]{2})\s+(.+?)\s+([\d.]+)\s*$", (raw_dir / "table3.txt").read_text(), re.M
        )
        assert len(source_rows) == 2431
        rows = []
        for nas_id, guide, flags, activity in source_rows:
            core = guide[:19]
            binding = reverse_complement(core).replace("U", "T")
            hits = [(t, m.start()) for t in inserts for m in re.finditer("(?=" + binding + ")", t["sequence"])]
            if len(hits) > 1:
                # Original Table 3: NAS 18412 has Training Rodent, NAS 19819 Training All_Human.
                species = {"18412": "Rn", "19819": "Hs"}[nas_id]
                expected_flags = {"18412": "X           X   X   X", "19819": "X   X           X   X"}
                assert flags.strip() == expected_flags[nas_id]
                hits = [(t, pos) for t, pos in hits if t["gene"].startswith(species + " ")]
            assert len(hits) == 1, nas_id
            t, start = hits[0]
            seq = t["sequence"]
            context = (
                "X" * max(0, 19 - start) + seq[max(0, start - 19) : start + 38] + "X" * max(0, start + 38 - len(seq))
            )
            assert len(context) == 57
            rows.append(
                dict(
                    guide=guide,
                    core=core,
                    mRNA=context.replace("T", "U"),
                    target_gene=t["gene"],
                    normalized_inhibitory_activity=float(activity),
                )
            )
        df = pd.DataFrame(rows)
        assert df.core.is_unique
        assert df.target_gene.nunique() == 30
        return df

    def _clean(self, raw):
        features = {}
        for prefix, source, length in (("guide", "guide", 21), ("target_window", "mRNA", 57)):
            for i in range(length):
                features[f"{prefix}_position_{i + 1:02d}"] = raw[source].str[i].astype("category")
        for prefix, source, alphabet in (("guide", "core", "AUCG"), ("target_window", "mRNA", "AUCGX")):
            sequences = raw[source].str.replace("N", "X").str.replace("R", "X")
            for letters in itertools.product(alphabet, repeat=3):
                motif = "".join(letters)
                features[f"{prefix}_trimer_{motif}"] = sequences.str.count("(?=" + motif + ")").astype("int16")
        td = np.asarray([descriptors(seq) for seq in raw.core])
        for i, name in enumerate(TD_NAMES):
            features[f"descriptor_{name}"] = td[:, i]
        df = pd.DataFrame(features)
        df = df.loc[:, df.nunique(dropna=False) > 1]
        # These positional/descriptor equalities are representation redundancies, not label-based selection.
        df = df.loc[:, ~df.T.duplicated()]
        df[self.target] = raw[self.target]
        df["target_gene"] = raw.target_gene
        return df

    def _feature_types(self, df):
        return FeatureTypes(
            categorical=[c for c in df if "_position_" in c]
            + [
                "descriptor_" + name
                for name in ("U_1", "G_1", "UU_1", "GG_1", "GC_1", "U_2", "C_1", "CC_1", "CG_1", "A_19")
            ]
            + ["target_gene"]
        )

    def _decisions(self, raw, df):
        return [
            Decision(
                "Keep the corrected original library and assay scale",
                "Restore the omitted target gene and avoid the processed copy's data-maximum scaling.",
                raw.groupby("target_gene")[self.target].agg(["count", "min", "max"]),
            ),
            Decision(
                "Keep unknown sequence bases explicit",
                "N/R are source uncertainty and X marks insert boundaries; none is inferred from efficacy.",
                pd.Series({base: int(raw.mRNA.str.count(base).sum()) for base in "NRX"}, name="base_occurrences"),
            ),
        ]
