"""Curated dataset definition for `coad_colon_adenocarcinoma` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, drop_columns

# The four omics files of MLOmics, genes x patients; all of them and the label file list the patients in one order.
OMICS = ("mRNA", "miRNA", "Methy", "CNV")
# The codes of `COAD_label_num.csv`, named by the TCGA PanCancer Atlas subtypes of the same 260 patients.
SUBTYPES = {0: "CIN", 1: "MSI", 2: "GS", 3: "HM-SNV"}


class CoadColonAdenocarcinoma(AbstractCuratedDataset):
    # Dataset
    unique_name = "coad_colon_adenocarcinoma"
    year = "2024"
    domain = "medical & healthcare"
    source = "GitHub"  # the authors' repository shared the data from 2024, before Hugging Face and Figshare (2025)
    source_url = "https://github.com/chenzRG/Cancer-Multi-Omics-Benchmark"
    license = "CC BY 4.0"
    download_description = """
        We download the GS-COAD files of the "Original" feature scale of MLOmics from its Hugging Face dataset (the
        GitHub repository's download.sh clones it), pinned to the revision of 2026-09-22. The data are also on Figshare
        (doi 10.6084/m9.figshare.28729127): its version 2 of 2025-05-25 holds the files of HF revision d7c22395
        (identical MD5), the release whose feature counts TabPFN-Wide reports. The pinned files keep a subset of its
        genes (rows) for the same patients, in the same order and with the same labels, and every gene they keep has
        the 2025 values.

        The authors first released the data through the GitHub repository
        (https://github.com/chenzRG/Cancer-Multi-Omics-Benchmark): from July 2024 its scripts/download.sh fetched
        Main_Dataset.zip from Dropbox (commit 60d6960 of 2024-07-24), before the Hugging Face dataset (created
        2025-04-04) and Figshare (version 1 of 2025-04-20).

        REV=74b9385f5223e6490bdec8c4a38f9b231b4f2263
        mkdir -p local-data-warehouse/coad_colon_adenocarcinoma
        for f in mRNA miRNA Methy CNV label_num; do wget -O local-data-warehouse/coad_colon_adenocarcinoma/COAD_${f}.csv https://huggingface.co/datasets/AIBIC/MLOmics/resolve/${REV}/Main_Dataset/Classification_datasets/GS-COAD/Original/COAD_${f}.csv; done
    """
    bibtex = """
        @article{yang2025mlomics,
          title={{MLOmics}: Cancer Multi-Omics Database for Machine Learning},
          author={Yang, Ziwei and Kotoge, Rikuto and Piao, Xihao and Chen, Zheng and Zhu, Lingwei and Gao, Peng and Matsubara, Yasuko and Sakurai, Yasushi and Sun, Jimeng},
          journal={Scientific Data},
          volume={12},
          pages={913},
          year={2025},
          doi={10.1038/s41597-025-05235-x}
        }
        @article{liu2018comparative,
          title={Comparative Molecular Analysis of Gastrointestinal Adenocarcinomas},
          author={Liu, Yang and Sethi, Nilay S and Hinoue, Toshinori and others},
          journal={Cancer Cell},
          volume={33},
          number={4},
          pages={721--735},
          year={2018},
          doi={10.1016/j.ccell.2018.03.010}
        }
    """
    curation_comments = """
        We start with the four omics files and the label file of GS-COAD ("Original" feature scale) from MLOmics (Yang et al. 2025), Hugging Face revision 74b9385f of 2026-09-22: 260 TCGA colon adenocarcinoma patients, one primary tumour sample each. We use three of the four: expression, miRNA and methylation.

        - Prediction point: a resected colon tumour has been profiled by RNA-seq (mRNA, miRNA) and the HumanMethylation450 array, and the model assigns the molecular subtype the TCGA PanCancer Atlas gave the tumour (Liu et al. 2018). The DNA measurements that define the subtypes (exome mutation counts for MSI, copy number for CIN against GS) are not used.
        - Task: MLOmics releases GS-COAD for "golden-standard cancer subtype classification"; we score it with the collection's multiclass metric, log loss. The curation record calls the task binary, but the source's labels have four classes.
        - Labels: `COAD_label_num.csv` holds class codes without ids, in the patient order of the omics files. Matched by barcode to the PanCancer Atlas subtypes (`Subtype_Selected`), codes 0, 1, 2 and 3 are GI.CIN (174), GI.MSI (48), GI.GS (34) and GI.HM-SNV (4) for all 260 patients, so we name the classes CIN, MSI, GS and HM-SNV.
        - We drop the 4 HM-SNV tumours, 1 or 2 per test fold. TCGA 2012 grouped hypermutated tumours with MSI, but Liu et al. 2018 separate the two mechanisms, so we do not merge them.
        - Features: we transpose each omics file (genes x patients) and prefix every feature with its omics (`mRNA_`, `miRNA_`, `Methy_`). We drop the 304 columns that equal an earlier column for every patient and keep the first; no column is constant and no value is missing, which leaves 36,355 features.
        - We drop the TCGA barcode, an identifier.
        - We drop the copy-number block (SNP6, `CNV_`; Lennart, 2026-10-12): copy-number changes define CIN against GS (Liu et al. 2018), so a lab that has them computes the subtype by the published procedure, and a model is needed where only expression and methylation are measured. Random forest on 6 of the shipped splits: macro ROC AUC 0.935 and log loss 0.411 with the block, 0.923 and 0.499 without it, 0.901 and 0.446 on the block alone.
        - IID split over patients: one row is one patient, and MLOmics and TabPFN-Wide split at random. Splitting by tissue source site (barcode field 2, 25 sites) scores like a random split (random forest ROC AUC 0.923 both).
        - Note: MLOmics standardised every feature of this cohort over the 260 patients, although its paper describes the "Original" scale as the genes "directly extracted from the collected omics files" (Methods; MLOmics GitHub issues #3, #7 and #9). The scaling uses no labels but includes the test rows; we keep the released values.
    """

    # Task
    target = "subtype"
    problem_type = "multiclass_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        # one row per patient: each omics file transposed, its features prefixed with the omics
        blocks = []
        for omics in OMICS:
            block = pd.read_csv(raw_dir / f"COAD_{omics}.csv", index_col=0).T
            block.columns = [f"{omics}_{name}" for name in block.columns]
            blocks.append(block)
        if not all(block.index.equals(blocks[0].index) for block in blocks):
            raise ValueError("The omics files list the patients in different orders.")
        df = pd.concat(blocks, axis=1)
        df.insert(0, "sample", df.index.to_numpy())
        # the label file has no ids: its rows follow the patient order of the omics files
        df["subtype_code"] = pd.read_csv(raw_dir / "COAD_label_num.csv")["Label"].to_numpy()
        return df.reset_index(drop=True)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df[self.target] = df.pop("subtype_code").map(SUBTYPES)
        # 4 HM-SNV tumours: too few for 3-fold cross-validation
        df = df[df[self.target] != "HM-SNV"]
        df = drop_columns(df, ["sample"])
        # the copy-number block: copy-number changes define CIN against GS, so with them a lab computes the subtype by
        # the published procedure; the task is the subtype from expression and methylation
        df = drop_columns(df, [c for c in df.columns if c.startswith("CNV_")])
        features = df.columns.drop(self.target)
        # columns constant over the kept patients, and exact copies of an earlier column
        constant = features[df[features].nunique() <= 1]
        features = features.drop(constant)
        copies = features[df[features].T.duplicated(keep="first").to_numpy()]
        return drop_columns(df, [*constant, *copies])
