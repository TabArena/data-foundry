"""Curated dataset definition for `sarcoma` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, Metric, TaskSummary

OMICS = {"exp": "mRNA", "methy": "Methy", "mirna": "miRNA"}
"""The omic files of the benchmark (features x samples) and the prefix their columns get."""

REVIEWED_HISTOLOGY = {
    "STLMS": "Leiomyosarcoma",  # soft tissue
    "ULMS": "Leiomyosarcoma",  # uterine
    "DDLPS": "Dedifferentiated liposarcoma",
    # one spectrum of disease in the TCGA study and one class of the methylation classifier (Koelsche et al. 2021)
    "UPS": "Undifferentiated pleomorphic sarcoma or myxofibrosarcoma",
    "MFS": "Undifferentiated pleomorphic sarcoma or myxofibrosarcoma",
    "SS": "Synovial sarcoma",
    "MPNST": None,  # 5 patients: below 10, dropped
}
"""The reviewed types of the TCGA sarcoma study (`short_histo`), mapped to the target; None drops the type."""


def primary_tumour_profiles(raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """One row per patient with a primary-tumour sample in all three omics; the omic blocks side by side.

    The sample names are TCGA barcodes cut to the sample type (`TCGA.3B.A9HI.01`); type 01 is the primary tumour.
    """
    blocks = []
    for file, prefix in OMICS.items():
        omic = raw[file]
        primary = [c for c in omic.columns if c.split(".")[3] == "01"]
        block = omic[primary].T
        block.index = [c[:12] for c in primary]  # the patient barcode, `TCGA.3B.A9HI`
        assert block.index.is_unique, file
        block.columns = [f"{prefix}_{c}" for c in block.columns]
        blocks.append(block)
    patients = sorted(set.intersection(*(set(b.index) for b in blocks)))
    return pd.concat([b.loc[patients] for b in blocks], axis=1)


def reviewed_types(master: pd.DataFrame) -> pd.Series:
    """The expert-reviewed type (`short_histo`) of each patient of the TCGA study, indexed like the omic rows."""
    assert (master["TCGA_barcode"].str[13:15] == "01").all()
    types = pd.Series(
        master["short_histo"].to_numpy(),
        index=master["TCGA_barcode"].str[:12].str.replace("-", ".", regex=False).to_numpy(),
    )
    assert types.index.is_unique
    return types


def submitted_types(clinical: pd.DataFrame) -> pd.Series:
    """The submitted histological type of each patient's primary tumour (the clinical file), indexed like the rows."""
    primary = clinical[clinical["sampleID"].str[13:15] == "01"]
    patients = primary["sampleID"].str[:12].str.replace("-", ".", regex=False)
    types = pd.Series(primary["histological_type"].to_numpy(), index=patients.to_numpy())
    assert types.index.is_unique
    return types


class Sarcoma(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Which type of soft-tissue sarcoma is this tumour, judged from its molecular profiles?",
        use_case=(
            "A molecular pathology lab types a sarcoma from the tumour's methylation or expression profile, to support "
            "or check a hard diagnosis, as the DNA-methylation sarcoma classifier of Koelsche et al. (2021) does; "
            "TabPFN-Wide uses the task as a benchmark."
        ),
        row=(
            "The primary tumour of one patient of the TCGA sarcoma study whose type expert pathologists confirmed "
            "(201 patients; period not stated)."
        ),
        predicted=(
            "The reviewed histological type: leiomyosarcoma (40%), undifferentiated pleomorphic sarcoma or "
            "myxofibrosarcoma (one class, 30%), dedifferentiated liposarcoma (25%) or synovial sarcoma (5%)."
        ),
        known="25,910 measurements of the tumour: gene expression, DNA methylation and microRNA expression.",
        split=(
            "Random patients, so the test data stands for new patients' tumours; one hospital gives half the rows, so "
            "the scores are optimistic for a lab whose patients come from elsewhere."
        ),
        changes=(
            "The source is a clustering benchmark without a label; we add the expert-reviewed type of the TCGA study "
            "instead of the submitted diagnosis, merge the two leiomyosarcoma sites and, as the study does, "
            "undifferentiated pleomorphic sarcoma with myxofibrosarcoma, and drop the 5 nerve-sheath tumours and the "
            "array's genotype probes."
        ),
        fit="approximate",
        fit_reason=(
            "A closed set of four expert-confirmed types, profiled on three omics, stands in for a classifier that "
            "faces every referred sarcoma: the review left out uncertain cases and rarer types, so the test tumours "
            "are cleaner than a lab's, and a lab mostly has one methylation array. The source's preprocessing over "
            "all patients is a weak potential leak kept on purpose (curation notes), not a reason for the fit."
        ),
    )

    # Dataset
    unique_name = "sarcoma"
    year = "2018"
    domain = "medical & healthcare"
    # the preprocessed TCGA benchmark of the Shamir lab (Tel Aviv University); the measurements are TCGA's
    source = "Other"
    source_url = "https://acgt.cs.tau.ac.il/multi_omic_benchmark/download.html"
    license = (
        "TCGA open-access data (NCI GDC open tier); the benchmark page's footer reads 'All rights reserved'; "
        "the reviewed histology is a supplement of the TCGA publication on the GDC"
    )
    download_description = """
        We download the preprocessed TCGA sarcoma omics and the clinical data of Rappoport & Shamir (2018) from the
        benchmark page https://acgt.cs.tau.ac.il/multi_omic_benchmark/download.html (files dated 16 July 2018;
        md5 sarcoma.zip caa80f17838be76ad658a1d9581f688f, clinical.zip bf06f12bdc4244f0f5c50a78f88a5589), and the
        expert-reviewed histology of the TCGA sarcoma study (Cell 2017), `SARC_Master_Patient_Table.xlsx` from its
        GDC publication page https://gdc.cancer.gov/about-data/publications/sarc_2017 (GDC file
        20cb9a7c-28a9-49ff-9e7d-8e7af0c722d9, md5 42146699371fd1582f8f04c05a03f8f5).

        mkdir -p local-data-warehouse/sarcoma && cd local-data-warehouse/sarcoma
        wget https://acgt.cs.tau.ac.il/multi_omic_benchmark/data/sarcoma.zip
        wget https://acgt.cs.tau.ac.il/multi_omic_benchmark/data/clinical.zip
        unzip sarcoma.zip exp methy mirna && unzip clinical.zip clinical/sarcoma && rm sarcoma.zip clinical.zip
        wget -O SARC_Master_Patient_Table.xlsx https://api.gdc.cancer.gov/data/20cb9a7c-28a9-49ff-9e7d-8e7af0c722d9
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
        @article{tcga2017sarcoma,
          title={Comprehensive and Integrated Genomic Characterization of Adult Soft Tissue Sarcomas},
          author={{Cancer Genome Atlas Research Network}},
          journal={Cell},
          volume={171},
          number={4},
          pages={950--965.e28},
          year={2017},
          doi={10.1016/j.cell.2017.10.014}
        }
    """
    curation_comments = """
        We start with the sarcoma files of the multi-omic cancer benchmark of Rappoport & Shamir (2018): gene expression (`exp`), DNA methylation (`methy`, 450k array) and miRNA expression (`mirna`), plus the clinical file `clinical/sarcoma`. The label comes from the master patient table of the TCGA sarcoma study (`SARC_Master_Patient_Table.xlsx`, GDC publication page).

        - Prediction point: a primary soft-tissue sarcoma has been profiled on the three platforms, and the model assigns its histological type from these profiles; no clinical column enters.
        - Task: multiclass classification of the histological type, the subtype classification of TabPFN-Wide (Kolberg et al. 2025, Sec. 5, Table A1); typing sarcomas from molecular profiles is a diagnostic practice (Koelsche et al. 2021). The source is a clustering benchmark without a target.
        - Label: the reviewed type (`short_histo`) instead of the clinical file's submitted `histological_type`. The TCGA study confirmed 206 sarcomas by expert pathology review, excluded the others (QC failures, non-sarcomas, uncertain types) and reclassified 20 (decision table). For dedifferentiated liposarcoma the review also required a 12q15 copy-number gain in the study's own data (Cell 2017, Methods), and all 8 relabels into or out of that class follow it. The copy number is not shipped.
        - Rows: the primary tumours (TCGA sample type 01) of the 257 patients with all three omics, restricted to the 206 reviewed patients, one row per patient; the barcode is not a feature. We drop the 5 MPNST (fewer than 10), which leaves 201 rows.
        - Target: four classes, leiomyosarcoma 80, undifferentiated pleomorphic sarcoma or myxofibrosarcoma 61 (44 + 17), dedifferentiated liposarcoma 50 and synovial sarcoma 10 (3-4 per test fold). Soft-tissue and uterine leiomyosarcoma are one type, as in the clinical file: whether the tumour sits in the uterus is known before profiling, so nobody predicts it.
        - Undifferentiated pleomorphic sarcoma (UPS) and myxofibrosarcoma (MFS) are one class (Lennart, 2026-10-22): the TCGA study that supplies the label finds "MFS and UPS to be largely indistinguishable across multiple platforms" and analyses them "as a single spectrum of disease", and the DNA-methylation classifier used in diagnostics has one class for both (Koelsche et al. 2021), so the lab that types from molecular profiles acts on one class. Pathologists tell them apart from the slide, which this table does not hold. Kept apart, the pair barely separated (ROC AUC 0.60-0.66 within the pair, three runs); a random forest predicted MFS for none of the 51 MFS test rows (17 patients over three repeats); the pair, 30% of the rows, carried 51.5% of its log loss, and the merge lowers that log loss from 0.650 to 0.461.
        - Features: the three omic blocks side by side, each column prefixed with its omic (`mRNA_`, `Methy_`, `miRNA_`), with the gene names as the source wrote them through R's `make.names` and the values as shipped (mRNA and miRNA normalised per sample). We drop the 61 `Methy_rs*` columns, the array's SNP genotyping probes: the patient's germline genotype, not methylation, with no class signal (best one-vs-rest ROC AUC 0.77 among 305 tests). We drop the columns that are constant over the 201 rows and those that copy an earlier column (decision table).
        - Potential leak, kept on purpose: the benchmark's preprocessing ran over all patients, test rows included: it removed patients and features with over 20% missing values and imputed the rest by k-nearest neighbours on every omic, and kept the 5,000 methylation probes of highest variance over all 269 samples (Rappoport & Shamir 2018, Suppl. File 1). The share of imputed values is not known. Kept (Lennart, 2026-10-19) until the rebuild from the GDC's per-sample values, which should cover every block the imputation touched and drop the genotype probes too.
        - Split: IID over patients, one row each, since a lab types the tumours of new patients (splits comment; kept over a split by site, Lennart, 2026-10-22). One tissue source site holds 101 of the 201 rows and 40 of the 50 dedifferentiated liposarcomas, and holding out whole sites raises a random forest's log loss from 0.46 to 0.58 (four classes, mean of three seeds; 0.64 to 0.77 with MFS and UPS apart): a known optimism for a new lab.
        - Note: the generated-data probe flags rule leaves of dedifferentiated liposarcoma: `mRNA_MDM2.4193` alone separates the class (ROC AUC 1.000), since MDM2 sits on the 12q15 amplicon the review required. Unlike coad's copy-number block, the defining measurement is not shipped, a lab measures MDM2 at typing anyway, and the task is no rule (best single-feature skill 0.24 over 30 splits against 0.75 for the best model, four classes; 0.05 with five), so the column stays (SEL-5).
    """
    splits_comment = """
        IID over patients, stratified on the type: each patient is one row, and a lab types the tumours of new patients. One tissue source site holds 101 of the 201 rows and 40 of the 50 dedifferentiated liposarcomas, and the features carry the site weakly within a type (that site against the rest among dedifferentiated liposarcomas: ROC AUC 0.69-0.73, against 0.65 for the 95th percentile of shuffled labels). Holding out whole sites raises a random forest's log loss from 0.46 to 0.58 (mean of three seeds), so the scores are optimistic for a lab whose patients come from elsewhere.
    """

    # Task
    target = "histological_type"
    problem_type = "multiclass_classification"
    metric = Metric.fallback(
        reason=(
            "The source (Rappoport & Shamir 2018) is a clustering benchmark without a label, and the TCGA "
            "study (Cell 2017) defines no prediction metric. The task paper the definition cites, TabPFN-Wide"
            " (Kolberg et al. 2025, arXiv 2510.06162), reports AUROC and accuracy on COAD/LGG/BRCA/GBM/OV, "
            "but SARC 'is only used for attention analysis' (Table 1 caption), so no metric is defined for "
            "this task."
        ),
    )

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        raw = {file: pd.read_csv(raw_dir / file, sep=" ", index_col=0) for file in OMICS}
        raw["master"] = pd.read_excel(
            raw_dir / "SARC_Master_Patient_Table.xlsx", sheet_name=0, usecols=["TCGA_barcode", "short_histo"]
        )
        raw["clinical"] = pd.read_csv(
            raw_dir / "clinical" / "sarcoma", sep="\t", usecols=["sampleID", "histological_type"]
        )
        return raw

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        # 1. Primary tumours of the patients with all three omics (257), the omic blocks side by side.
        df = primary_tumour_profiles(raw)
        # 2. The target: the reviewed type of the TCGA study; patients outside its 206 and the 5 MPNST are dropped.
        types = reviewed_types(raw["master"]).reindex(df.index)
        unknown = set(types.dropna()) - set(REVIEWED_HISTOLOGY)
        assert not unknown, f"reviewed types without a mapping: {unknown}"
        df[self.target] = types.map(REVIEWED_HISTOLOGY).to_numpy()
        df = df[df[self.target].notna()]
        # 3. Drop the array's SNP genotyping probes (`Methy_rs*`, a germline genotype, not methylation).
        df = df.drop(columns=[c for c in df.columns if c.startswith("Methy_rs")])
        # 4. Drop the feature columns that are constant over these rows, then those that copy an earlier column.
        features = df.drop(columns=[self.target])
        constant = features.columns[features.nunique() <= 1]
        features = features.drop(columns=constant)
        duplicated = features.columns[features.T.duplicated(keep="first").to_numpy()]
        return df.drop(columns=[*constant, *duplicated])

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        patients = primary_tumour_profiles(raw).index
        reviewed = reviewed_types(raw["master"]).reindex(patients)
        table = (
            pd.DataFrame(
                {
                    "submitted (clinical file)": submitted_types(raw["clinical"]).reindex(patients).fillna("(none)"),
                    "reviewed (TCGA 2017)": reviewed.fillna("not in the reviewed 206"),
                    "shipped as": reviewed.map(REVIEWED_HISTOLOGY).fillna("(dropped)"),
                }
            )
            .value_counts()
            .rename("patients")
            .reset_index()
        )
        n_source = sum(raw[file].shape[0] for file in OMICS)
        n_snp = sum(str(probe).startswith("rs") for probe in raw["methy"].index)
        n_kept = df.shape[1] - 1
        columns = pd.DataFrame(
            {"columns": [n_source, n_snp, n_source - n_snp - n_kept, n_kept]},
            index=pd.Index(
                [
                    "omic features in the source files",
                    "SNP genotyping probes (`Methy_rs*`), dropped",
                    "constant or duplicated, dropped",
                    "features kept",
                ],
                name="step",
            ),
        )
        return [
            Decision(
                title="Target: the type confirmed by TCGA's expert pathology review",
                why=(
                    "The clinical file holds the submitted diagnosis. The TCGA sarcoma study confirmed 206 cases by "
                    "expert review, excluded the others (QC failures, non-sarcomas, uncertain types) and reclassified "
                    "20. The table pairs the two labels for the 257 patients with all three omics; the shipped type "
                    "merges the two leiomyosarcoma sites and, as the study does, UPS with MFS, and drops MPNST."
                ),
                evidence=table,
            ),
            Decision(
                title="Genotype probes, constant and duplicated columns are dropped",
                why=(
                    "The `rs` probes of the methylation array measure the patient's germline genotype, not the tumour's "
                    "methylation, and carry no class signal. Zero-only genes and miRNAs carry nothing, and an exact "
                    "copy of a column adds nothing."
                ),
                evidence=columns,
            ),
        ]
