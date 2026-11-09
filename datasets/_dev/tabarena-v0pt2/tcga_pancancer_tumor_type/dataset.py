"""Curated dataset definition for `tcga_pancancer_tumor_type` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.csv as pacsv
import pyarrow.parquet as pq
from data_foundry.v2 import AbstractCuratedDataset, Decision, Metric, TaskSummary

PRIMARY_SAMPLE_TYPES = ("Primary Tumor", "Primary Blood Derived Cancer - Peripheral Blood")
"""The GDC sample types of a primary tumour: a solid primary (TCGA code 01) and the blood of the leukaemia (03)."""

PROJECT_NAMES = {
    "ACC": "Adrenocortical Carcinoma",
    "BLCA": "Bladder Urothelial Carcinoma",
    "BRCA": "Breast Invasive Carcinoma",
    "CESC": "Cervical Squamous Cell Carcinoma and Endocervical Adenocarcinoma",
    "CHOL": "Cholangiocarcinoma",
    "COAD": "Colon Adenocarcinoma",
    "DLBC": "Lymphoid Neoplasm Diffuse Large B-cell Lymphoma",
    "ESCA": "Esophageal Carcinoma",
    "GBM": "Glioblastoma Multiforme",
    "HNSC": "Head and Neck Squamous Cell Carcinoma",
    "KICH": "Kidney Chromophobe",
    "KIRC": "Kidney Renal Clear Cell Carcinoma",
    "KIRP": "Kidney Renal Papillary Cell Carcinoma",
    "LAML": "Acute Myeloid Leukemia",
    "LGG": "Brain Lower Grade Glioma",
    "LIHC": "Liver Hepatocellular Carcinoma",
    "LUAD": "Lung Adenocarcinoma",
    "LUSC": "Lung Squamous Cell Carcinoma",
    "MESO": "Mesothelioma",
    "OV": "Ovarian Serous Cystadenocarcinoma",
    "PAAD": "Pancreatic Adenocarcinoma",
    "PCPG": "Pheochromocytoma and Paraganglioma",
    "PRAD": "Prostate Adenocarcinoma",
    "READ": "Rectum Adenocarcinoma",
    "SARC": "Sarcoma",
    "SKCM": "Skin Cutaneous Melanoma",
    "STAD": "Stomach Adenocarcinoma",
    "TGCT": "Testicular Germ Cell Tumors",
    "THCA": "Thyroid Carcinoma",
    "THYM": "Thymoma",
    "UCEC": "Uterine Corpus Endometrial Carcinoma",
    "UCS": "Uterine Carcinosarcoma",
    "UVM": "Uveal Melanoma",
}
"""The 33 TCGA projects (study abbreviations) and their names on the GDC."""

CANCER_TYPES = {**PROJECT_NAMES, "COAD": "Colorectal Adenocarcinoma", "READ": "Colorectal Adenocarcinoma"}
"""The target's 32 classes: the TCGA project, with colon and rectum as one colorectal class (as TCGA and the source)."""

SEQUENCING_CENTRES = {
    "01": "Broad Institute",
    "07": "UNC",
    "13": "BCGSC",
    "31": "BCGSC",
    "41": "UNC, 2024 total-RNA re-sequencing",
    "53": "other",
}
"""The analysis centre of an RNA aliquot (TCGA barcode characters 27-28; GDC centre codes), for the route table."""

STAR_FILES = "star_counts"
"""The folder of the GDC STAR-Counts files, one sub-folder per file id (the layout `gdc-client` writes)."""


def file_table(listing: list[dict]) -> pd.DataFrame:
    """One row per STAR-Counts file of the GDC listing: project, patient, sample type and RNA aliquot."""
    rows = []
    for hit in listing:
        (case,) = hit["cases"]
        (sample,) = case["samples"]
        (aliquot,) = [
            aliquot["submitter_id"]
            for portion in sample["portions"]
            for analyte in portion["analytes"]
            for aliquot in analyte["aliquots"]
        ]
        rows.append(
            {
                "file_id": hit["file_id"],
                "file_name": hit["file_name"],
                "project": case["project"]["project_id"].removeprefix("TCGA-"),
                "patient": case["submitter_id"],
                "sample_type": sample["sample_type"],
                "aliquot": aliquot,
            }
        )
    files = pd.DataFrame(rows)
    # TCGA barcode TCGA-XX-XXXX-01A-11R-A250-07: site, vial, analyte, plate and analysis centre of the aliquot
    files["site"] = files["aliquot"].str[5:7]
    files["vial"] = files["aliquot"].str[15]
    files["analyte"] = files["aliquot"].str[19]
    files["plate"] = files["aliquot"].str[21:25]
    files["centre"] = files["aliquot"].str[26:28]
    return files


def flagged_aliquots(annotations: pd.DataFrame) -> pd.Series:
    """The RNA-seq aliquots of the PanCanAtlas sample quality annotations that do not ship, with the reason.

    Two flags of `merged_sample_quality_annotations.tsv`: `Do_not_use` (the PanCanAtlas's own exclusions: prior
    malignancies or treatment, samples outside the study protocol, failed expression QC) and
    `AWG_excluded_because_of_pathology` (the TCGA working group's pathology review rejected the sample: another type,
    no tumour, degraded RNA). Indexed by the aliquot barcode.
    """
    rna = annotations[annotations["platform"].str.contains("RNASeq", na=False)]
    do_not_use = rna["Do_not_use"].astype(str) == "True"
    pathology = rna["AWG_excluded_because_of_pathology"].astype(str) == "1.0"
    reason = pd.Series(
        np.where(do_not_use, "PanCanAtlas Do_not_use", "excluded by the working group's pathology review"),
        index=rna["aliquot_barcode"].to_numpy(),
    )
    return reason[(do_not_use | pathology).to_numpy()].groupby(level=0).first()


def exact_copy_columns(features: pd.DataFrame) -> list[str]:
    """The columns whose values copy an earlier column exactly (compared by a digest of the values)."""
    seen: set[str] = set()
    copies = []
    for column in features.columns:
        digest = hashlib.blake2b(np.ascontiguousarray(features[column].to_numpy()).tobytes()).hexdigest()
        if digest in seen:
            copies.append(column)
        seen.add(digest)
    return copies


def pancan_rna_aliquots(annotations: pd.DataFrame) -> set[str]:
    """The RNA-seq aliquots the PanCanAtlas analysed (any flag)."""
    rna = annotations[annotations["platform"].str.contains("RNASeq", na=False)]
    return set(rna["aliquot_barcode"])


def one_file_per_patient(files: pd.DataFrame, pancan: set[str]) -> pd.DataFrame:
    """Keep one primary-tumour file per patient.

    The order: the aliquot the PanCanAtlas analysed first, then the original poly-A library before the 2024 total-RNA
    re-sequencing (centre code 41), then the first vial (A before B), then the RNA analyte (R) before total RNA (T),
    then the newest plate, then the file id (only to make the choice fixed).
    """
    ranked = files.assign(
        _not_pancan=~files["aliquot"].isin(pancan),
        _resequenced=files["centre"] == "41",
        _not_r=files["analyte"] != "R",
    ).sort_values(
        ["patient", "_not_pancan", "_resequenced", "vial", "_not_r", "plate", "file_id"],
        ascending=[True, True, True, True, True, False, True],
        kind="stable",
    )
    return ranked.drop_duplicates("patient", keep="first").drop(columns=["_not_pancan", "_resequenced", "_not_r"])


def selected_files(raw: dict) -> pd.DataFrame:
    """The primary-tumour files that ship: the flagged aliquots out (`flagged_aliquots`), then one file per patient."""
    files = raw["files"]
    files = files[files["sample_type"].isin(PRIMARY_SAMPLE_TYPES)]
    files = files[~files["aliquot"].isin(flagged_aliquots(raw["annotations"]).index)]
    return one_file_per_patient(files, pancan_rna_aliquots(raw["annotations"]))


class TcgaPancancerTumorType(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Which of 32 cancer types is a tumour, judged from the gene expression of a tumour sample?",
        use_case=(
            "A pathologist or oncologist facing a cancer of unknown primary has the biopsy RNA-sequenced and uses the "
            "profile to name the most likely cancer type, which sets a site-specific treatment; the source names "
            "such cancers as a potential clinical use of its classification (Hoadley et al. 2018, Discussion)."
        ),
        row=(
            "The primary tumour of one patient of The Cancer Genome Atlas: 9,724 adult patients of 33 cancer types, "
            "collected through 695 hospital sites, one RNA-seq profile each (period not stated in the files)."
        ),
        predicted=(
            "The TCGA project the tumour was enrolled in: its cancer type as the contributing hospital's pathology "
            "diagnosed it (colon and rectum as one colorectal class), a mix of organ and histology, from 1,084 breast "
            "carcinomas down to 34 bile-duct cancers."
        ),
        known="The expression of 58,383 genes in the tumour sample (TPM from RNA sequencing), nothing clinical.",
        split=(
            "Random patients, standing for new patients' tumours. Each hospital sent one cancer type and a few types "
            "were sequenced at another centre, so the scores are optimistic for a lab whose samples come from elsewhere."
        ),
        changes=(
            "We read the GDC's per-sample files instead of the published pan-cancer matrix, which was batch-corrected "
            "over all samples, drop the samples the source's quality review flagged and keep one profile per patient."
        ),
        fit="approximate",
        fit_reason=(
            "Primary tumours of known type stand in for the metastases of unknown origin the decision is about, and "
            "the classes are TCGA projects, which split some organs by histology. Each hospital site sent one type "
            "and five types were sequenced elsewhere, so the data carry batch marks a new lab's sample lacks."
        ),
    )

    # Dataset
    unique_name = "tcga_pancancer_tumor_type"
    year = "2018"
    domain = "medical & healthcare"
    source = "GOV Website"
    source_url = "https://gdc.cancer.gov/about-data/publications/pancanatlas"
    license = (
        "NCI Genomic Data Commons open-access tier (no login): under the NIH Genomic Data Sharing policy, users do not "
        "try to identify participants and acknowledge the GDC and the dataset in publications"
    )
    download_description = """
        The open-access STAR-Counts files of the GDC (Data Release 46.0, 2026-08-10; listed on 2026-11-08) and the
        PanCanAtlas sample quality annotations (GDC PanCanAtlas publication page).

        mkdir -p local-data-warehouse/tcga_pancancer_tumor_type && cd local-data-warehouse/tcga_pancancer_tumor_type
        # 1. The listing of the 11,505 open STAR-Counts files of the 33 TCGA projects, the API's `data.hits` of every
        #    page (size 1000, from 0 to 11000) concatenated into one JSON list:
        curl -X POST https://api.gdc.cancer.gov/files -H "Content-Type: application/json" -d '{"filters": {"op": "and", "content": [{"op": "in", "content": {"field": "cases.project.program.name", "value": ["TCGA"]}}, {"op": "in", "content": {"field": "data_type", "value": ["Gene Expression Quantification"]}}, {"op": "in", "content": {"field": "analysis.workflow_type", "value": ["STAR - Counts"]}}, {"op": "in", "content": {"field": "access", "value": ["open"]}}]}, "fields": "file_id,file_name,file_size,md5sum,cases.submitter_id,cases.case_id,cases.project.project_id,cases.samples.submitter_id,cases.samples.sample_type,cases.samples.portions.analytes.aliquots.submitter_id", "format": "JSON", "size": 1000, "from": 0, "sort": "file_id:asc"}'
        #    -> gdc_files_star_counts_tcga.json
        # 2. The 10,308 primary-tumour files (sample type "Primary Tumor" or "Primary Blood Derived Cancer -
        #    Peripheral Blood"; 43.7 GB), from a gdc-client manifest of their id, file name, md5 and size:
        gdc-client download -m gdc_manifest_primary.txt -d star_counts
        # 3. The PanCanAtlas sample quality annotations (md5 05ddd2270fb1fb24fbdc2fe9bf7384e5):
        wget -O merged_sample_quality_annotations.tsv https://api.gdc.cancer.gov/data/1a7d7be8-675d-4e60-a105-19d4121bdebf
    """
    bibtex = """
        @article{hoadley2018cell,
          title={Cell-of-Origin Patterns Dominate the Molecular Classification of 10,000 Tumors from 33 Types of Cancer},
          author={Hoadley, Katherine A and Yau, Christina and Hinoue, Toshinori and Wolf, Denise M and Lazar, Alexander J and Drill, Esther and Shen, Ronglai and Taylor, Alison M and Cherniack, Andrew D and Thorsson, V{\\'e}steinn and others},
          journal={Cell},
          volume={173},
          number={2},
          pages={291--304.e6},
          year={2018},
          doi={10.1016/j.cell.2018.03.022}
        }
    """
    curation_comments = """
        We start with the GDC's open-access STAR-Counts gene expression files of the 33 TCGA projects (one file per RNA aliquot, GENCODE v36, Data Release 46.0), with the PanCanAtlas sample quality annotations (`merged_sample_quality_annotations.tsv`).

        - Prediction point: a tumour sample has been RNA-sequenced, and the model names its cancer type from the expression profile alone; no clinical field (sex, age, site of the biopsy) enters. The source names cancers of unknown primary as the clinical use of its classification (Hoadley et al. 2018, Discussion).
        - Source: the data are the GDC's per-sample STAR-Counts files of Data Release 46.0 (`tpm_unstranded`, GENCODE v36); the task, the 33 TCGA cancer types of one primary tumour each, is that of Hoadley et al. (2018, Cell). The PanCanAtlas published the 33-type collection as one resource (Hoadley et al. 2018), hence the year; its RNA matrix (`EBPlusPlusAdjustPANCAN_IlluminaHiSeq_RNASeqV2.geneExp.tsv`) was batch-corrected with EB++ over all samples, sequencing centres and platforms included (STAR Methods, "RNA Data Batch Correction"), a transductive transform. We read the GDC's per-sample re-quantification instead: STAR alignment and counts of every aliquot on its own, released by the GDC in 2022.
        - Rows: the GDC files of a primary tumour, TCGA sample type 01 (solid) or 03 (the leukaemia's blood): 10,308 files of 10,122 patients. Normals, metastases (most melanomas: SKCM keeps 103 primaries), recurrences and second primaries are not the task's sample, so the GDC's sample type filters the files (`PRIMARY_SAMPLE_TYPES`). This filter is why the melanoma class is small: most TCGA melanomas are metastases.
        - Dropped, by the source's own quality flags in the PanCanAtlas annotations (decision table): 183 files marked `Do_not_use` (a prior malignancy or its treatment, a sample outside the study protocol such as pancreatic neuroendocrine tumours in PAAD, failed expression QC) and 221 more that the TCGA working groups' pathology review excluded (`AWG_excluded_because_of_pathology`: 73 prostate samples with degraded RNA, 39 lung tumours without a clear adenocarcinoma or squamous histology, sarcomas of another type, tumours that did not arise in the organ). Their label or their RNA is in doubt by the source's own review; 398 patients leave.
        - One row per patient: 145 patients have two or three primary files (another vial, portion or sequencing run of the same tumour); copies of one tumour across the split would leak (LEAK-17), and the use case is one profile per tumour. We keep the aliquot the PanCanAtlas analysed, then the original poly-A library over the 2024 total-RNA re-sequencing, then vial A, analyte R, the newest plate (`one_file_per_patient`). 9,724 rows.
        - Features: the TPM of every GENCODE v36 gene in the file (`tpm_unstranded`, which sums to one million in every file: a per-sample scale, LEAK-30 does not apply), named `<gene name>_<Ensembl id>`, as published, not logged or filtered (a log or a cut of near-zero genes is the model's choice, and the raw TPM loses nothing); STAR's four alignment counters are no genes. We drop the 2,277 genes that are zero in every shipped tumour (the 44 Y-chromosome copies of the pseudo-autosomal genes among them); no gene copies another, so 58,383 genes ship, 44% of the cells zero. Width is no reason to cut further (CLEAN-22).
        - Target: the TCGA project as the GDC names it, with colon (COAD) and rectum (READ) adenocarcinomas merged into one colorectal class (`CANCER_TYPES`): 32 classes, from 1,084 breast carcinomas down to 34 cholangiocarcinomas (48 lymphomas, 57 carcinosarcomas, 65 chromophobe kidney tumours). Colon and rectum are one class because the two are told apart mostly by the hospital site, not the tumour (pair ROC AUC 0.78 with random patients, 0.58 with sites held out; 6% of the rows carried 23 to 30% of a linear model's log loss), TCGA studied them as one colorectal cancer and the source groups them as COAD/READ, and a cancer of unknown primary with a colorectal profile is treated as colorectal. The project is the cancer type the contributing hospital's pathology diagnosed at enrolment, so it mixes organ and histology: three kidney types, two lung types, two gliomas, oesophageal adenocarcinomas with squamous carcinomas.
        - Potential leak, kept on purpose: the sequencing route differs by class (decision table). UNC sequenced 28 types with poly-A libraries; BCGSC sequenced the oesophageal (173), stomach (388) and ovarian (411 of 416) tumours and the leukaemia (151); the 284 glioblastomas come from the Broad Institute (155), one other centre (1) and a 2024 total-RNA re-sequencing at UNC (128, Ribo-Zero libraries on a NovaSeq, GDC read-group metadata). The source removed these centre and platform effects with EB++ over all samples (STAR Methods), which we do not use (LEAK-30), and no per-sample correction exists. The route shows: within the glioblastomas a linear model tells the two routes apart at ROC AUC 0.999, and trained on total-RNA glioblastomas only it called 6% of the Broad glioblastomas glioblastoma rather than lower-grade glioma (98% the other way round, 99% with both routes in training). As shipped both glioblastoma routes are in training, and none of the 7 total-RNA tumours of other types (5 ovarian, 2 lung) was called glioblastoma (probability at most 0.024). The route lives in the gene types a poly-A library captures badly: the small non-polyadenylated RNAs alone (snRNA, snoRNA, miRNA, rRNA and the like) tell the two glioblastoma routes apart at ROC AUC 0.994, the replication histones alone at 0.998. For the four BCGSC types no such test exists, since no other type went through BCGSC: how much of their separation from their neighbours (stomach from colorectal, oesophageal from head-and-neck and lung squamous, ovarian from endometrial) is route stays unmeasured. Revisit if the GDC releases the same tumours from one centre.
        - Tissue source site and plate: kept IID with the cost in the splits comment; the sites hold one type each, so a site's handling is a weak second label within the training data. The sequencing plates do the same: 145 of the 247 plates hold one type (4,795 rows, 49%), the adrenocortical, bile-duct, carcinosarcoma and uveal melanoma tumours each sit on one plate, and two plates of one type from one site are told apart at a median ROC AUC of 0.77 (the leukaemia's 0.996).
        - Metric: the multiclass fallback `log_loss`. Macro ROC AUC saturates (0.998 to 0.999 for a linear model), log loss still spreads model families; for a pathologist, top-1 and top-3 accuracy are the readings the tissue-of-origin field reports, and both follow from the predicted probabilities.
        - Note: `treehouse_pediatric_tumor_type` re-quantifies 9,806 TCGA datasets of the same tumours (TOIL/RSEM); only its paediatric cut ships, which shares 366 TCGA tumours with this task under other labels (record assessment of 2026-11-08), so the two are distinct tasks. The TCGA records with other targets on the same tumours (`tcga_lung_histology`, `tcga_kidney_cancers`, `tcga_coad_molecular_subtype`, `sarcoma`) are distinct tasks too.
    """
    splits_comment = """
        IID over patients, stratified on the cancer type, one row per patient: a lab types the tumours of new patients (as `sarcoma`). Each of the 695 tissue source sites sent tumours of one type only, and the site shows in the profile (two sites of one type told apart at ROC AUC 0.54 to 0.96, median 0.73, over 20 types). Holding out whole sites (the leukaemia's single site split by patient) raises a linear model's log loss (PCA on 2,000 genes, 3 folds) from 0.144 to 0.195 and from 0.137 to 0.233 (two seeds). The sequencing plates are a second such batch: 145 of the 247 plates hold one type (49% of the rows), and two plates of one type from one site are told apart at a median ROC AUC of 0.77. The scores are optimistic for a lab whose samples come from hospitals not in the training data. A split by site is not shipped: one site holds the whole leukaemia class and 71 of the 78 adrenocortical carcinomas, so a fold would train on none or 7 of them.
    """

    # Task
    target = "cancer_type"
    problem_type = "multiclass_classification"
    metric = Metric.fallback(
        reason=(
            "Hoadley et al. (2018, Cell) cluster the tumours (consensus clustering of each platform, iCluster across "
            "platforms) and train no classifier of the cancer type, so the source scores no type prediction; the "
            "GDC and PanCanAtlas pages define no task. log_loss is the multiclass fallback."
        ),
    )

    prepared_raw_files = ("tpm_primary.parquet", "genes.parquet")

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        # One wide table of the TPM column of every primary-tumour file (rows: file ids, columns: Ensembl gene ids).
        listing = json.loads((raw_dir / "gdc_files_star_counts_tcga.json").read_text())
        files = file_table(listing)
        files = files[files["sample_type"].isin(PRIMARY_SAMPLE_TYPES)].sort_values("file_id", kind="stable")
        genes, values = None, []
        for file_id, file_name in zip(files["file_id"], files["file_name"], strict=True):
            table = pacsv.read_csv(
                raw_dir / STAR_FILES / file_id / file_name,
                read_options=pacsv.ReadOptions(skip_rows=1),  # the `# gene-model: GENCODE v36` line
                parse_options=pacsv.ParseOptions(delimiter="\t"),
                convert_options=pacsv.ConvertOptions(
                    include_columns=["gene_id", "gene_name", "gene_type", "tpm_unstranded"],
                    column_types={"tpm_unstranded": pa.float64()},
                ),
            ).to_pandas()
            table = table[~table["gene_id"].str.startswith("N_")]  # STAR's four alignment counters, no genes
            if genes is None:
                genes = table[["gene_id", "gene_name", "gene_type"]].reset_index(drop=True)
            assert (table["gene_id"].to_numpy() == genes["gene_id"].to_numpy()).all(), file_id  # one gene order
            values.append(table["tpm_unstranded"].to_numpy())
        matrix = np.vstack(values)
        assert np.isfinite(matrix).all()
        columns = {gene: matrix[:, i] for i, gene in enumerate(genes["gene_id"])}
        tpm = pa.table({"file_id": files["file_id"].to_numpy(), **columns})
        pq.write_table(tpm, raw_dir / "tpm_primary.parquet")
        genes.to_parquet(raw_dir / "genes.parquet", index=False)

    def _load_raw(self, raw_dir: Path) -> dict:
        listing = json.loads((raw_dir / "gdc_files_star_counts_tcga.json").read_text())
        return {
            "files": file_table(listing),
            "annotations": pd.read_csv(raw_dir / "merged_sample_quality_annotations.tsv", sep="\t", dtype=str),
            "genes": pd.read_parquet(raw_dir / "genes.parquet"),
            "tpm": pd.read_parquet(raw_dir / "tpm_primary.parquet").set_index("file_id"),
        }

    def _clean(self, raw: dict) -> pd.DataFrame:
        # 1. The primary tumours, without the flagged aliquots (`flagged_aliquots`), one file per patient.
        files = selected_files(raw)
        # 2. The features: each gene's TPM in that file, named `<gene name>_<Ensembl id without version>`.
        genes = raw["genes"]
        names = genes["gene_name"] + "_" + genes["gene_id"].str.replace(r"\.\d+", "", regex=True)
        assert names.is_unique
        df = raw["tpm"].loc[files["file_id"].to_numpy()]
        df.columns = names.to_numpy()
        # 3. The target: the TCGA project, in its GDC name, colon and rectum as one colorectal class.
        df[self.target] = files["project"].map(CANCER_TYPES).to_numpy()
        assert df[self.target].notna().all()
        # 4. Drop the genes constant over the shipped rows (zero in every tumour), then exact copies of a column.
        features = df.drop(columns=[self.target])
        constant = features.columns[features.nunique() <= 1]
        features = features.drop(columns=constant)
        df = df.drop(columns=[*constant, *exact_copy_columns(features)])
        return df

    def _decisions(self, raw: dict, df: pd.DataFrame) -> list[Decision]:
        files = raw["files"]
        primary = files[files["sample_type"].isin(PRIMARY_SAMPLE_TYPES)]
        reason = primary["aliquot"].map(flagged_aliquots(raw["annotations"]))
        kept = primary[reason.isna()]
        shipped = selected_files(raw)
        rows = pd.DataFrame(
            {
                "files": [len(primary), int((reason == "PanCanAtlas Do_not_use").sum()), len(kept), len(shipped)],
                "patients": [
                    primary["patient"].nunique(),
                    None,
                    kept["patient"].nunique(),
                    shipped["patient"].nunique(),
                ],
            },
            index=pd.Index(
                [
                    "primary-tumour files on the GDC (sample type 01, and 03 for the leukaemia)",
                    "marked Do_not_use by the PanCanAtlas, dropped",
                    "after also dropping the working groups' pathology exclusions",
                    "one file per patient (shipped rows)",
                ],
                name="step",
            ),
        ).astype("Int64")
        rows.loc["excluded by the working groups' pathology review, dropped", "files"] = int(
            (reason == "excluded by the working group's pathology review").sum()
        )
        rows = rows.iloc[[0, 1, 4, 2, 3]]
        by_class = (
            pd.crosstab(primary["project"].rename("cancer type"), reason.fillna("kept (before one per patient)"))
            .rename(index=PROJECT_NAMES)
            .loc[lambda t: t.drop(columns="kept (before one per patient)").sum(axis=1) > 0]
        )
        centre = pd.crosstab(
            shipped["project"].map(CANCER_TYPES).rename("cancer type"),
            shipped["centre"].map(SEQUENCING_CENTRES).fillna("other").rename("sequencing centre"),
        )
        centre = centre[centre.drop(columns="UNC", errors="ignore").sum(axis=1) > 0]
        n_genes = len(raw["genes"])
        n_kept = df.shape[1] - 1
        columns = pd.DataFrame(
            {"columns": [n_genes, n_genes - n_kept, n_kept]},
            index=pd.Index(
                ["genes in a GENCODE v36 file", "constant over the shipped rows or a copy, dropped", "features kept"],
                name="step",
            ),
        )
        return [
            Decision(
                title="Rows: primary tumours, the source's quality flags out, one profile per patient",
                why=(
                    "The task's sample is a primary tumour. The PanCanAtlas annotations mark aliquots not to use (a "
                    "prior malignancy or treatment, outside the study protocol, failed expression QC) and the "
                    "aliquots the TCGA working groups' pathology review excluded (another type, no tumour, degraded "
                    "RNA); both leave. A patient with several files keeps one: the aliquot the PanCanAtlas analysed, "
                    "then the original poly-A library over the 2024 total-RNA re-sequencing, then vial A, analyte R "
                    "and the newest plate."
                ),
                evidence=rows,
            ),
            Decision(
                title="The flagged primary-tumour files by cancer type",
                why="Most pathology exclusions are prostate samples with degraded RNA and lung tumours without a "
                "clear adenocarcinoma or squamous histology.",
                evidence=by_class,
            ),
            Decision(
                title="Five cancer types were sequenced away from UNC",
                why=(
                    "UNC sequenced 28 of the 33 types. BCGSC sequenced the oesophageal, stomach and ovarian tumours "
                    "and the leukaemia; the Broad Institute and a 2024 total-RNA re-sequencing at UNC hold the "
                    "glioblastomas. A model can learn such a route instead of the tumour (curation notes)."
                ),
                evidence=centre,
            ),
            Decision(
                title="Genes constant over the shipped rows are dropped",
                why="A gene with zero TPM in every shipped tumour carries nothing; no gene copies another exactly.",
                evidence=columns,
            ),
        ]
