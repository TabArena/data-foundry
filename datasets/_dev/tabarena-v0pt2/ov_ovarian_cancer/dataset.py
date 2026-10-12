"""Curated dataset definition for `ov_ovarian_cancer` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, drop_columns

# The four omics files of MLOmics, genes x patients; all of them and the label file list the patients in one order.
OMICS = ("mRNA", "miRNA", "Methy", "CNV")
# The codes of `OV_label_num.csv`, named by the TCGA transcriptional subtypes of the same 284 patients.
SUBTYPES = {0: "Differentiated", 1: "Immunoreactive", 2: "Mesenchymal", 3: "Proliferative"}


class OvOvarianCancer(AbstractCuratedDataset):
    # Dataset
    unique_name = "ov_ovarian_cancer"
    year = "2025"
    domain = "medical & healthcare"
    source = "GitHub"  # the authors' repository shared the data from 2024, before Hugging Face and Figshare (2025)
    source_url = "https://github.com/chenzRG/Cancer-Multi-Omics-Benchmark"
    license = "CC BY 4.0"
    data_tags = ("Anonymized",)
    download_description = """
        We download the GS-OV files of the "Original" feature scale of MLOmics from its Hugging Face dataset (the
        GitHub repository's download.sh clones it), pinned to the revision of 2026-09-22. The data are also on Figshare
        (doi 10.6084/m9.figshare.28729127): its version 2 of 2025-05-25 holds the files of HF revision d7c22395
        (identical MD5), the release whose feature counts TabPFN-Wide reports. The pinned files keep a subset of its
        genes (rows) for the same patients, in the same order and with the same labels, and every gene they keep has
        the 2025 values, with two exceptions: the pinned methylation file fills the 2025 missing values (1,931 genes,
        0.2% of the cells), and the 2025 files hold two copies each of the rows named "1-Mar" and "2-Mar" (MARCH1 and
        MARCH2 turned into dates), of which the pinned files keep one.

        The authors first released the data through the GitHub repository
        (https://github.com/chenzRG/Cancer-Multi-Omics-Benchmark): from July 2024 its scripts/download.sh fetched
        Main_Dataset.zip from Dropbox (commit 60d6960 of 2024-07-24), before the Hugging Face dataset (created
        2025-04-04) and Figshare (version 1 of 2025-04-20).

        REV=74b9385f5223e6490bdec8c4a38f9b231b4f2263
        mkdir -p local-data-warehouse/ov_ovarian_cancer
        for f in mRNA miRNA Methy CNV label_num; do wget -O local-data-warehouse/ov_ovarian_cancer/OV_${f}.csv https://huggingface.co/datasets/AIBIC/MLOmics/resolve/${REV}/Main_Dataset/Classification_datasets/GS-OV/Original/OV_${f}.csv; done
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
        @article{tcga2011ovarian,
          title={Integrated Genomic Analyses of Ovarian Carcinoma},
          author={{The Cancer Genome Atlas Research Network}},
          journal={Nature},
          volume={474},
          number={7353},
          pages={609--615},
          year={2011},
          doi={10.1038/nature10166}
        }
    """
    curation_comments = """
        We start with the four omics files and the label file of GS-OV ("Original" feature scale) from MLOmics (Yang et al. 2025), Hugging Face revision 74b9385f of 2026-09-22: 284 TCGA high-grade serous ovarian cancer patients, one primary tumour sample each.

        - Prediction point: an ovarian tumour has been resected and profiled (RNA-seq for mRNA and miRNA, methylation array, SNP6 copy number), and the model assigns the transcriptional subtype that TCGA gave it (TCGA 2011).
        - Task: MLOmics releases GS-OV for "golden-standard cancer subtype classification", and TabPFN-Wide (Kolberg et al. 2025) benchmarks it with macro ROC AUC. We score log loss, the collection's metric for a multiclass task. The curation record calls the task binary; the source's labels have four classes.
        - Labels: `OV_label_num.csv` holds class codes without ids, in the patient order of the omics files. Matched by barcode to the TCGA 2011 subtypes (TCGAbiolinks, `Subtype_mRNA`), codes 0 to 3 are Differentiated, Immunoreactive, Mesenchymal and Proliferative (`SUBTYPES`); 255 of the 284 patients agree.
        - Anomaly: 29 patients (10%) have a different subtype in the TCGA 2011 assignment, spread over all pairs of classes. MLOmics does not say where its labels come from; we keep them.
        - Anonymized: the gene names do not describe the values. Many rows carry placeholder names (`ZZZ<n>`, `ZZEF<n>`), GS-OV and GS-LGG of the 2025 release carry the same name column, and the structure of real genes is absent: genes on one chromosome arm do not vary together (mean r +0.003 against +0.74 in GS-COAD), and a gene's copy number does not raise its own expression (median r -0.004 against +0.31). The values are real measurements of these patients, as the patient similarities of the four files agree. We name every feature by its omics and its row in the MLOmics file (`mRNA_00017` is row 17 of `OV_mRNA.csv`) and tag the dataset Anonymized.
        - Features: we transpose each file (genes x patients) and drop constant columns (the 3,115 mRNA rows that are zero for every patient, as TabPFN-Wide's loader does) and exact copies of an earlier column (4,753 CNV rows), keeping the first in file order. No value is missing: 48,279 features.
        - We drop the TCGA barcode, an identifier.
        - Note: the subtypes are NMF consensus clusters of an earlier microarray expression measurement of the same tumours (TCGA 2011), so the task is to recover them from the RNA-seq. The label is no rule on the shipped blocks: a depth-3 tree on the mRNA block reaches AUC 0.868, LightGBM 0.980.
        - IID: one row is one patient, and MLOmics and TabPFN-Wide split at random. Splitting by tissue source site scores like a random split (AUC 0.969 against 0.964).
    """

    # Task
    target = "subtype"
    problem_type = "multiclass_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        # one row per patient: each omics file transposed, its features prefixed with the omics
        blocks = []
        for omics in OMICS:
            block = pd.read_csv(raw_dir / f"OV_{omics}.csv", index_col=0).T
            block.columns = [f"{omics}_{name}" for name in block.columns]
            blocks.append(block)
        if not all(block.index.equals(blocks[0].index) for block in blocks):
            raise ValueError("The omics files list the patients in different orders.")
        df = pd.concat(blocks, axis=1)
        df.insert(0, "sample", df.index.to_numpy())
        # the label file has no ids: its rows follow the patient order of the omics files
        df["subtype_code"] = pd.read_csv(raw_dir / "OV_label_num.csv")["Label"].to_numpy()
        return df.reset_index(drop=True)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df[self.target] = df.pop("subtype_code").map(SUBTYPES)
        df = drop_columns(df, ["sample"])
        # the gene names do not describe the values: name each feature by its omics and its row in the MLOmics file
        renamed = {}
        for omics in OMICS:
            columns = [c for c in df.columns if c.startswith(f"{omics}_")]
            renamed |= {c: f"{omics}_{row:05d}" for row, c in enumerate(columns, start=1)}
        df = df.rename(columns=renamed)
        features = df.columns.drop(self.target)
        # constant columns (mRNA rows that are zero for every patient), and exact copies of an earlier column
        # (CNV rows with the values of an earlier row)
        constant = features[df[features].nunique() <= 1]
        features = features.drop(constant)
        copies = features[df[features].T.duplicated(keep="first").to_numpy()]
        return drop_columns(df, [*constant, *copies])
