"""Curated dataset definition for `glioblastoma` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision

COHORT_FILES = ("exp", "methy", "mirna")
"""The omic files of the benchmark (features x samples); its patients have a primary tumour in all three."""

FEATURE_FILES = {"methy": "Methy", "mirna": "miRNA"}
"""The omic files whose values are features, and the prefix their columns get. The expression file (`exp`) only
selects the patients: the label is computed from expression."""


def primary_samples(omic: pd.DataFrame) -> dict[str, str]:
    """Patient barcode (`TCGA.02.0001`) -> the column of its primary tumour (TCGA sample type 01, `TCGA.02.0001.01`)."""
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


def expression_subtypes(clinical: pd.DataFrame) -> pd.Series:
    """The expression subtype of each patient's primary tumour, indexed like the omic rows (`TCGA.02.0001`)."""
    primary = clinical[clinical["sampleID"].str[13:15] == "01"]
    patients = primary["sampleID"].str[:12].str.replace("-", ".", regex=False)
    subtypes = pd.Series(primary["GeneExp_Subtype"].to_numpy(), index=patients.to_numpy())
    assert subtypes.index.is_unique
    return subtypes


class Glioblastoma(AbstractCuratedDataset):
    # Dataset
    unique_name = "glioblastoma"
    year = "2018"
    domain = "medical & healthcare"
    # the preprocessed TCGA benchmark of the Shamir lab (Tel Aviv University); the measurements are TCGA's
    source = "Other"
    source_url = "https://acgt.cs.tau.ac.il/multi_omic_benchmark/download.html"
    license = "TCGA open-access data (NCI GDC open tier); the benchmark page's footer reads 'All rights reserved'"
    download_description = """
        We download the preprocessed TCGA glioblastoma omics and the clinical data of Rappoport & Shamir (2018) from
        the benchmark page https://acgt.cs.tau.ac.il/multi_omic_benchmark/download.html (files dated 16 July 2018;
        md5 gbm.zip 676039134f118857ed4211c9c7d851aa, clinical.zip bf06f12bdc4244f0f5c50a78f88a5589).

        mkdir -p local-data-warehouse/glioblastoma && cd local-data-warehouse/glioblastoma
        wget https://acgt.cs.tau.ac.il/multi_omic_benchmark/data/gbm.zip
        wget https://acgt.cs.tau.ac.il/multi_omic_benchmark/data/clinical.zip
        unzip gbm.zip exp methy mirna && unzip clinical.zip clinical/gbm && rm gbm.zip clinical.zip
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
        We start with the glioblastoma files of the multi-omic cancer benchmark of Rappoport & Shamir (2018): gene
        expression (`exp`), DNA methylation (`methy`, the 5,000 most variable probes of the Illumina 27k array) and
        miRNA expression (`mirna`), plus the clinical file `clinical/gbm` (the TCGA clinical matrix of UCSC Xena). The
        authors' preprocessing (dropping patients and features with over 20% missing values, k-nearest-neighbour
        imputation, the choice of probes) uses all patients but no label.

        - Prediction point: a primary glioblastoma has been profiled by DNA methylation and miRNA arrays, and the model
          assigns the expression subtype that its gene expression would get. No clinical column enters.
        - Task: subtype classification as in TabPFN-Wide (Kolberg et al. 2025, Sec. 5), whose loader takes
          `GeneExp_Subtype` from the clinical file. The source is a clustering benchmark without a target, and the
          curation record says binary classification, but the paper's task has four classes. The paper scores AUROC and
          accuracy; we keep log loss, the collection's metric for a multiclass task.
        - We drop the expression block, as sdss_17 drops `redshift`: the subtypes are assigned from gene expression of
          the same tumours (Brennan et al. 2013; Verhaak et al. 2010). The Verhaak class gene sets scored on `exp`
          reproduce 216 of the 274 labels, and a logistic regression on the four set scores (log loss 0.645) beats
          LightGBM on all 17,576 omic columns (0.693). Without the block the task is to predict the expression subtype
          from two other measurements.
        - Rows: primary tumours (TCGA sample type 01) of the patients with all three omics, as the benchmark does
          (`only.primary=T` in its `benchmark.R`): 274 patients, all with a subtype. The expression file selects them
          and adds no column. The barcode is not a feature.
        - Target: `expression_subtype`, the `GeneExp_Subtype` of the patient's primary tumour (four classes; decision
          table).
        - Features: the methylation and miRNA blocks side by side in the source order, each column prefixed with its
          omic (`Methy_`, `miRNA_`), values as shipped. We drop constant columns and columns that copy an earlier one
          (none at present): 5,534 features.
        - Split: IID over patients, as in TabPFN-Wide. The tissue source site (the second field of the barcode) goes
          with the subtype (Cramer's V 0.22), but holding out whole sites leaves a random forest as it is (macro ROC AUC
          0.873 on random folds, 0.880 by site), so we keep the split by patient.
    """

    # Task
    target = "expression_subtype"
    problem_type = "multiclass_classification"

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        # The expression file only selects the patients: its header (and one row) is enough.
        raw = {"exp": pd.read_csv(raw_dir / "exp", sep=" ", index_col=0, nrows=1)}
        raw |= {file: pd.read_csv(raw_dir / file, sep=" ", index_col=0) for file in FEATURE_FILES}
        raw["clinical"] = pd.read_csv(raw_dir / "clinical" / "gbm", sep="\t", usecols=["sampleID", "GeneExp_Subtype"])
        return raw

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        # 1. The benchmark's patients (a primary tumour in all three omics, 274); methylation and miRNA side by side.
        df = cohort_profiles(raw)
        # 2. The target: the expression subtype (every one of these patients has one).
        df[self.target] = expression_subtypes(raw["clinical"]).reindex(df.index).to_numpy()
        df = df[df[self.target].notna()]
        # 3. Drop the feature columns that are constant over these rows, then those that copy an earlier column
        #    (none at present; kept so that a change of the rows cannot leave such columns behind).
        features = df.drop(columns=[self.target])
        constant = features.columns[features.nunique() <= 1]
        features = features.drop(columns=constant)
        duplicated = features.columns[features.T.duplicated(keep="first").to_numpy()]
        return df.drop(columns=[*constant, *duplicated])

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        del df
        subtypes = expression_subtypes(raw["clinical"]).reindex(cohort_profiles(raw).index)
        counts = subtypes.fillna("no subtype").value_counts().rename("patients").rename_axis("subtype")
        return [
            Decision(
                title="Target: the expression subtype of the clinical file; the expression block is not a feature",
                why=(
                    "TabPFN-Wide classifies the glioblastoma subtype (`GeneExp_Subtype`); all 274 patients with a "
                    "primary tumour in the three omics have one. The subtypes are assigned from gene expression, so "
                    "the expression block only selects the patients."
                ),
                evidence=counts.to_frame(),
            )
        ]
