"""Curated dataset definition for `lgg_low_grade_glioma` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, drop_columns

# Three of the four omics files of MLOmics (genes x patients; all list the patients in one order, as does the label
# file). The methylation file is left out: its profiles do not match these patients (see curation_comments).
OMICS = ("mRNA", "miRNA", "CNV")
# The codes of `LGG_label_num.csv`, named by the TCGA PanCancer Atlas classes of the same 247 patients.
SUBTYPES = {0: "IDHmut-codel", 1: "IDHmut-non-codel", 2: "IDHwt"}


class LggLowGradeGlioma(AbstractCuratedDataset):
    # Dataset
    unique_name = "lgg_low_grade_glioma"
    year = "2024"
    domain = "medical & healthcare"
    source = "GitHub"  # the authors' repository shared the data from 2024, before Hugging Face and Figshare (2025)
    source_url = "https://github.com/chenzRG/Cancer-Multi-Omics-Benchmark"
    license = "CC BY 4.0"
    data_tags = ("Anonymized",)
    download_description = """
        We download three of the four GS-LGG files of the "Original" feature scale of MLOmics (mRNA, miRNA and copy
        number; not LGG_Methy.csv) and the labels from its Hugging Face dataset (the GitHub repository's download.sh
        clones it), pinned to the revision of 2026-09-22. The data are also on Figshare
        (doi 10.6084/m9.figshare.28729127): its version 2 of 2025-05-25 holds the files of HF revision d7c22395
        (identical MD5), the release whose feature counts TabPFN-Wide reports. The pinned files keep a subset of its
        genes (rows) for the same patients, in the same order and with the same labels, and every gene they keep has
        the 2025 values (the 2025 files hold two copies each of the rows named "1-Mar" and "2-Mar", MARCH1 and MARCH2
        turned into dates; the pinned files keep one of them).

        The authors first released the data through the GitHub repository
        (https://github.com/chenzRG/Cancer-Multi-Omics-Benchmark): from July 2024 its scripts/download.sh fetched
        Main_Dataset.zip from Dropbox (commit 60d6960 of 2024-07-24), before the Hugging Face dataset (created
        2025-04-04) and Figshare (version 1 of 2025-04-20).

        REV=74b9385f5223e6490bdec8c4a38f9b231b4f2263
        mkdir -p local-data-warehouse/lgg_low_grade_glioma
        for f in mRNA miRNA CNV label_num; do wget -O local-data-warehouse/lgg_low_grade_glioma/LGG_${f}.csv https://huggingface.co/datasets/AIBIC/MLOmics/resolve/${REV}/Main_Dataset/Classification_datasets/GS-LGG/Original/LGG_${f}.csv; done
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
        @article{ceccarelli2016molecular,
          title={Molecular Profiling Reveals Biologically Discrete Subsets and Pathways of Progression in Diffuse Glioma},
          author={Ceccarelli, Michele and Barthel, Floris P and Malta, Tathiane M and others},
          journal={Cell},
          volume={164},
          number={3},
          pages={550--563},
          year={2016},
          doi={10.1016/j.cell.2015.12.028}
        }
    """
    curation_comments = """
        We start with three of the four omics files and the label file of GS-LGG ("Original" feature scale) from MLOmics (Yang et al. 2025), Hugging Face revision 74b9385f: 247 TCGA lower-grade glioma patients, one primary tumour sample each.

        - Note (2026-10-07): not recommended for the benchmark. The release is faulty in all four blocks (methylation, gene names, one mislabel; bullets below), and the label is close to a two-column rule. The folder stays until the curator decides.
        - Prediction point: a resected glioma has been profiled by RNA-seq (mRNA, miRNA) and SNP6 copy number, and the model assigns the molecular class TCGA gave the tumour (Ceccarelli et al. 2016). The IDH sequencing and the 1p/19q calls that define the classes are not in the data.
        - Task: subtype classification, as MLOmics releases it. The labels have three classes, although the curation record calls the task binary; the metric is log loss.
        - Labels: `LGG_label_num.csv` holds class codes without ids, in the patient order of the omics files. Matched by barcode to the PanCancer Atlas classes (cBioPortal), codes 0, 1 and 2 are IDHmut-codel, IDHmut-non-codel and IDHwt for 246 of the 247 patients, and we name them so.
        - Anomaly: TCGA-DU-6399 has code 2 (IDHwt), while cBioPortal and TCGAbiolinks place it with the IDH-mutant tumours. We keep the MLOmics label.
        - We leave out the methylation file `LGG_Methy.csv`: its profiles do not match these patients. The patient-similarity matrix of the mRNA profiles correlates with the miRNA (r 0.59) and copy-number ones (0.45) but not with the methylation one (-0.005, as with the patients shuffled).
        - Anonymized: the gene names of the three files do not describe their values. Thirteen mRNA columns under autosomal names separate the patients' sex at ROC AUC 0.997 to 1.000, and the genes named on 1p and 19q separate codeleted tumours no better than the others. We name every feature by its omics and its row in the MLOmics file (`mRNA_00017` is row 17 of `LGG_mRNA.csv`) and tag the dataset Anonymized.
        - Features: we transpose each file (genes x patients), drop the 4,079 mRNA rows that are zero for every patient (as TabPFN-Wide's loader does) and the 13,033 CNV rows that equal an earlier row for every patient, keeping the first. No value is missing: 21,076 features.
        - We drop the TCGA barcode, an identifier.
        - Note: close to a two-column rule. The classes are defined by the IDH mutation and the 1p/19q codeletion, a copy-number loss. A logistic regression on the best CNV column for IDHmut-codel and the best mRNA column for IDHwt (chosen on each training side) reaches log loss 0.194 (skill 0.81 over the class shares), against 0.149 (skill 0.85) for an L2 logistic regression on all 21,076 features. Removing a block does not help.
        - IID split: one row is one patient, as in MLOmics and TabPFN-Wide; a split by tissue source site scores like a random one.
    """

    # Task
    target = "subtype"
    problem_type = "multiclass_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        # one row per patient: each omics file transposed, its features prefixed with the omics
        blocks = []
        for omics in OMICS:
            block = pd.read_csv(raw_dir / f"LGG_{omics}.csv", index_col=0).T
            block.columns = [f"{omics}_{name}" for name in block.columns]
            blocks.append(block)
        if not all(block.index.equals(blocks[0].index) for block in blocks):
            raise ValueError("The omics files list the patients in different orders.")
        df = pd.concat(blocks, axis=1)
        df.insert(0, "sample", df.index.to_numpy())
        # the label file has no ids: its rows follow the patient order of the omics files
        df["subtype_code"] = pd.read_csv(raw_dir / "LGG_label_num.csv")["Label"].to_numpy()
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
