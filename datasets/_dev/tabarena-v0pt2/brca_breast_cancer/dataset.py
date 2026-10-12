"""Curated dataset definition for `brca_breast_cancer` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision

COHORT_FILES = ("exp", "methy", "mirna")
"""The omic files of the benchmark (features x samples); its patients have a primary tumour in all three."""

FEATURE_FILES = {"methy": "Methy", "mirna": "miRNA"}
"""The omic files whose values are features, and the prefix their columns get. The expression file (`exp`) only
selects the patients: the label is computed from it."""

PAM50_NAMES = {
    "LumA": "Luminal A",
    "LumB": "Luminal B",
    "Basal": "Basal-like",
    "Her2": "HER2-enriched",
    "Normal": "Normal-like",
}


def primary_samples(omic: pd.DataFrame) -> dict[str, str]:
    """Patient barcode (`TCGA.3C.AAAU`) -> the column of its primary tumour (TCGA sample type 01, `TCGA.3C.AAAU.01`)."""
    samples = {c[:12]: c for c in omic.columns if c.split(".")[3] == "01"}
    assert len(samples) == sum(c.split(".")[3] == "01" for c in omic.columns), "two primary samples of one patient"
    return samples


def cohort_profiles(raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """One row per patient of the benchmark (a primary tumour in all three omics); the feature blocks side by side."""
    patients = sorted(set.intersection(*(set(primary_samples(raw[file])) for file in COHORT_FILES)))
    blocks = []
    for file, prefix in FEATURE_FILES.items():
        samples = primary_samples(raw[file])
        block = raw[file][[samples[p] for p in patients]].T
        block.index = patients
        block.columns = [f"{prefix}_{c}" for c in block.columns]
        blocks.append(block)
    return pd.concat(blocks, axis=1)


def pam50_calls(clinical: pd.DataFrame) -> pd.Series:
    """The PAM50 call of each patient's primary tumour, indexed like the omic rows (`TCGA.3C.AAAU`)."""
    primary = clinical[clinical["sampleID"].str[13:15] == "01"]
    patients = primary["sampleID"].str[:12].str.replace("-", ".", regex=False)
    calls = pd.Series(primary["PAM50Call_RNAseq"].to_numpy(), index=patients.to_numpy())
    assert calls.index.is_unique
    return calls


class BrcaBreastCancer(AbstractCuratedDataset):
    # Dataset
    unique_name = "brca_breast_cancer"
    year = "2018"
    domain = "medical & healthcare"
    # the preprocessed TCGA benchmark of the Shamir lab (Tel Aviv University); the measurements are TCGA's
    source = "Other"
    source_url = "https://acgt.cs.tau.ac.il/multi_omic_benchmark/download.html"
    license = "TCGA open-access data (NCI GDC open tier); the benchmark page's footer reads 'All rights reserved'"
    download_description = """
        We download the preprocessed TCGA breast cancer omics and the clinical data of Rappoport & Shamir (2018) from
        the benchmark page https://acgt.cs.tau.ac.il/multi_omic_benchmark/download.html (files dated 16 July 2018;
        md5 breast.zip 4a04ad9c49db403d95347c907ae3f866, clinical.zip bf06f12bdc4244f0f5c50a78f88a5589).

        mkdir -p local-data-warehouse/brca_breast_cancer && cd local-data-warehouse/brca_breast_cancer
        wget https://acgt.cs.tau.ac.il/multi_omic_benchmark/data/breast.zip
        wget https://acgt.cs.tau.ac.il/multi_omic_benchmark/data/clinical.zip
        unzip breast.zip exp methy mirna && unzip clinical.zip clinical/breast && rm breast.zip clinical.zip
    """
    bibtex = """
        @article{rappoport2018multi,
          title={Multi-omic and multi-view clustering algorithms: review and cancer benchmark},
          author={Rappoport, Nimrod and Shamir, Ron},
          journal={Nucleic Acids Research},
          volume={46},
          number={20},
          pages={10546--10562},
          year={2018},
          doi={10.1093/nar/gky889}
        }
    """
    curation_comments = """
        We start with the breast cancer files of the multi-omic cancer benchmark of Rappoport & Shamir (2018), gene expression (`exp`), DNA methylation (`methy`, the 5,000 most variable probes) and miRNA expression (`mirna`), plus the clinical file `clinical/breast` (the TCGA clinical matrix of UCSC Xena). The authors' filtering and imputation use all patients but no label.

        - Prediction point: a primary breast tumour has been profiled by DNA methylation and miRNA sequencing, and the model assigns the PAM50 subtype that its RNA-seq would get. No clinical column enters.
        - Task: subtype classification as in TabPFN-Wide (Kolberg et al. 2025, Sec. 5), which takes `PAM50Call_RNAseq` from the clinical file. The curation record says binary classification, but the paper's task has five classes. We keep the collection's metric for multiclass, log loss.
        - We drop the expression block, as sdss_17 drops `redshift`: PAM50 is "a 50-gene subtype predictor" (Parker et al. 2009), and `PAM50Call_RNAseq` is its call on TCGA's RNA-seq, the measurement in `exp`. With the block the task would be a lookup of 50 columns; `exp` only selects the patients (decision table).
        - Rows: primary tumours (TCGA sample type 01) of the patients with all three omics, as the benchmark does (`only.primary=T` in its `benchmark.R`). We drop the patients without a PAM50 call (decision table). TabPFN-Wide's 440 BRCA samples also hold adjacent normal samples and metastases, which the primary-tumour filter drops. One row per patient; the barcode is not a feature.
        - Target: `pam50_subtype`, the PAM50 call renamed to the usual subtype names. The Normal-like class holds 4-5 rows per test fold.
        - Features: the methylation and miRNA blocks side by side in the source order, prefixed `Methy_` and `miRNA_`, values as shipped. We drop the miRNA columns that are constant over the kept rows (all zero) and those that copy an earlier column (decision table).
        - Split: IID over patients, as in TabPFN-Wide. The tissue source site goes with the subtype (Cramer's V 0.24), but holding out whole sites does not change a random forest (macro ROC AUC 0.939 on random folds, 0.943 on folds by site), so we keep the split by patient.
        - Note: we keep the methylation probe ids. The TabPFN-Wide loader renames them to gene symbols, which gives several columns the same name.
    """

    # Task
    target = "pam50_subtype"
    problem_type = "multiclass_classification"

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        # The expression file only selects the patients: its header (and one row) is enough.
        raw = {"exp": pd.read_csv(raw_dir / "exp", sep=" ", index_col=0, nrows=1)}
        raw |= {file: pd.read_csv(raw_dir / file, sep=" ", index_col=0) for file in FEATURE_FILES}
        raw["clinical"] = pd.read_csv(
            raw_dir / "clinical" / "breast", sep="\t", usecols=["sampleID", "PAM50Call_RNAseq"]
        )
        return raw

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        # 1. The benchmark's patients (a primary tumour in all three omics, 621); methylation and miRNA side by side.
        df = cohort_profiles(raw)
        # 2. The target: the PAM50 call, with the usual subtype names; patients without a call are dropped.
        df[self.target] = pam50_calls(raw["clinical"]).reindex(df.index).map(PAM50_NAMES).to_numpy()
        df = df[df[self.target].notna()]
        # 3. Drop the feature columns that are constant over these rows, then those that copy an earlier column.
        features = df.drop(columns=[self.target])
        constant = features.columns[features.nunique() <= 1]
        features = features.drop(columns=constant)
        duplicated = features.columns[features.T.duplicated(keep="first").to_numpy()]
        return df.drop(columns=[*constant, *duplicated])

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        calls = pam50_calls(raw["clinical"]).reindex(cohort_profiles(raw).index)
        counts = (
            calls.map(PAM50_NAMES)
            .fillna("no PAM50 call (dropped)")
            .value_counts()
            .rename("patients")
            .rename_axis("PAM50 call")
        )
        n_source = sum(raw[file].shape[0] for file in FEATURE_FILES)
        columns = pd.DataFrame(
            {"columns": [n_source, n_source - (df.shape[1] - 1), df.shape[1] - 1]},
            index=pd.Index(
                [
                    "methylation and miRNA features in the source files",
                    "constant or duplicated, dropped",
                    "features kept",
                ],
                name="step",
            ),
        )
        return [
            Decision(
                title="Target: the PAM50 call; patients without one are dropped",
                why=(
                    "TabPFN-Wide classifies the PAM50 subtype (`PAM50Call_RNAseq`). Of the 621 patients with a "
                    "primary tumour in all three omics, 240 have no call."
                ),
                evidence=counts.to_frame(),
            ),
            Decision(
                title="The expression block is not a feature; constant and duplicated columns are dropped",
                why=(
                    "The PAM50 call is computed from the RNA-seq expression of 50 genes, so the expression block "
                    "only selects the patients. Zero-only miRNAs carry nothing, and an exact copy adds nothing."
                ),
                evidence=columns,
            ),
        ]
