"""Curated dataset definition for `treehouse_pediatric_tumor_type` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, Grouping, Metric, TaskSummary, anonymize_ids

CLINICAL_FILE = "GSE294351_clinical_Treehouse-Tumor-Compendium-25.01-PolyA_20250131v1.tsv.gz"
"""The compendium's clinical table: one row per RNA-seq dataset (13,359), keyed by `th_dataset_id`."""

EXPRESSION_FILE = "GSE294351_Tumor-25.01-Polya_hugo_log2tpm_58581genes_2025-02-27.tsv.gz"
"""The expression matrix: 58,581 HUGO genes (rows) x 13,359 datasets (columns), log2(TPM + 1)."""

PEDAYA_FILE = "pedaya_log2tpm.parquet"
"""The paediatric, adolescent and young-adult datasets of the matrix (`pedaya` yes), one row per dataset."""

MIN_DONORS = 10
"""A diagnosis ships as a class when at least this many donors hold it (3 or more per test fold of the grouped split)."""

NOT_GENES = ("age_at_diagnosis", "sex", "donor", "diagnosis")

SAME_TUMOUR = {
    "THR49_4750_S01": "THR30_0854_S01",
    "THR49_4752_S01": "THR30_0855_S01",
    "THR49_4754_S01": "THR30_0856_S01",
    "THR49_4765_S01": "THR30_0861_S01",
    "THR49_4774_S01": "THR30_0863_S01",
    "THR49_4775_S01": "THR30_0864_S01",
}
"""Datasets of two NCI sarcoma deposits (THR49, SRA SRP083915; THR30, dbGaP phs000768) that are one tumour.

Each pair is joined into one donor, and the THR49 copy is dropped from the rows (`shipped_cut`).

Without a shared id: each pair agrees in sex and age (within a year) and correlates at 0.9958 to 0.9973 over the
expressed genes, while no other pair of datasets of different donors in the cut passes 0.9913 (decision table).
"""


def read_clinical(raw_dir: Path) -> pd.DataFrame:
    """The clinical table as text, with the source's `unknown` and `unavailable` kept as written."""
    return pd.read_csv(raw_dir / CLINICAL_FILE, sep="\t", dtype=str, keep_default_na=False)


def patient_ids(row: pd.Series) -> list[str]:
    """Every id of the patient a dataset names; the first is always present.

    TARGET and TCGA datasets carry their barcode: the patient is TARGET's USI (`PAKSWW` of `TARGET-20-PAKSWW-03A-01R`,
    the same patient under another TARGET project code) or TCGA's `TCGA-XX-XXXX`; a Treehouse dataset id is
    `<site>_<donor>_S<sample>`, so its donor is the id without the sample. St. Jude's patient id (`SJBALL021807` of
    `SJBALL021807_D1`) and the study's own donor id link datasets of one patient across studies.
    """
    dataset = row["th_dataset_id"]
    if dataset.startswith("TARGET-"):
        ids = ["TARGET-" + dataset.split("-")[2]]
    elif dataset.startswith("TCGA-"):
        ids = [dataset[:12]]
    else:
        ids = [re.sub(r"_S\d+$", "", dataset)]
        if row["study_donor_id"] != "unavailable":
            ids.append(row["study_id"] + "|" + row["study_donor_id"])
    for text in (row["study_dataset_id"], row["study_donor_id"]):
        if match := re.match(r"SJ[A-Z]+\d+", text):
            ids.append(match.group(0))
    if dataset in SAME_TUMOUR:
        ids.append(re.sub(r"_S\d+$", "", SAME_TUMOUR[dataset]))
    return ids


def donor_key(clinical: pd.DataFrame) -> pd.Series:
    """The donor of each dataset: the datasets linked by any patient id (`patient_ids`), named by the smallest id."""
    parent: dict[str, str] = {}

    def root(key: str) -> str:
        while parent.setdefault(key, key) != key:
            key = parent[key]
        return key

    ids = [patient_ids(row) for _, row in clinical.iterrows()]
    for first, *others in ids:
        for other in others:
            a, b = root(first), root(other)
            if a != b:
                parent[max(a, b)] = min(a, b)
    return pd.Series([root(first) for first, *_ in ids], index=clinical.index)


def on_tpm_grid(values: np.ndarray) -> np.ndarray:
    """log2(TPM + 1) with the TPM rounded to RSEM's two decimals, recomputed for every value.

    RSEM writes TPM with two decimals, and every dataset of the compendium is on that grid except TCGA's and TARGET's
    (0.2% of their positive values on it; 0.0101, 0.0201, 0.0301 where the others have 0.01, 0.02, 0.03), so the low
    values alone would name the source. Rounding moves a value by at most 0.0071 (log2 units). Every value is
    recomputed, also those already on the grid (they move by less than 1e-9): recomputing only the off-grid ones
    left them with more written decimals than the rest, a new mark of the source (LEAK-13).
    """
    return np.log2(np.round(np.exp2(values) - 1, 2) + 1)


def paediatric_cut(clinical: pd.DataFrame) -> pd.DataFrame:
    """The datasets flagged `pedaya` yes, each with its donor and whether the source gives that donor two diagnoses."""
    cut = clinical[clinical["pedaya"] == "yes"].copy()
    cut["donor"] = donor_key(cut)
    cut["two_diagnoses"] = cut.groupby("donor")["disease"].transform("nunique") > 1
    return cut


def shipped_cut(cut: pd.DataFrame) -> pd.DataFrame:
    """The cut without the donors of two diagnoses and without the THR49 copies of `SAME_TUMOUR` (SPLIT-24)."""
    return cut[~cut["two_diagnoses"] & ~cut["th_dataset_id"].isin(SAME_TUMOUR)]


def diagnosis_counts(cut: pd.DataFrame) -> pd.DataFrame:
    """Datasets, donors, studies and the largest study's share per diagnosis."""
    by = cut.groupby("disease")
    table = pd.DataFrame(
        {
            "datasets": by.size(),
            "donors": by["donor"].nunique(),
            "studies": by["study_id"].nunique(),
            "largest study": by["study_id"].agg(lambda s: s.value_counts().index[0]),
            "largest study's share": by["study_id"].agg(lambda s: s.value_counts(normalize=True).iloc[0]).round(2),
        }
    )
    return table.sort_values(["donors", "datasets"], ascending=False, kind="stable")


class TreehousePediatricTumorType(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Which diagnosis does a childhood or young-adult tumour have, judged from its RNA-seq expression?",
        use_case=(
            "A molecular tumour board or pathologist confirms or revises the diagnosis of a child's or young adult's "
            "tumour from its RNA-seq profile, as the Treehouse compendia are used 'to infer molecular diagnosis' "
            "(Beale et al. 2025)."
        ),
        row=(
            "One RNA-seq dataset of one tumour sample of a patient aged 0 to 32 (3,256 datasets of 3,010 patients from "
            "37 studies: TARGET, TCGA, St. Jude and Treehouse's clinical partners, processed by one pipeline)."
        ),
        predicted=(
            "The tumour's harmonised diagnosis, one of the 27 held by 10 or more donors: acute lymphoblastic leukaemia "
            "(27%), acute myeloid leukaemia (14%), glioma (11%), osteosarcoma, neuroblastoma, Wilms tumour and 21 more."
        ),
        known="The expression of 54,571 genes as log2(TPM + 1), and the patient's age at diagnosis and sex.",
        split=(
            "Whole patients are held out, so the test data stands for new patients; most diagnoses come mostly from "
            "one or two studies, so test patients share the study, and its processing, of training patients."
        ),
        changes=(
            "We take the paediatric and young-adult cut only, drop the 84 diagnoses with fewer than 10 patients (211 "
            "datasets), 2 patients given two diagnoses and 5 tumours' second deposit, join a patient's datasets across "
            "studies, round the age "
            "down to whole years and every TPM to two decimals, removing two marks of the source study."
        ),
        fit="approximate",
        fit_reason=(
            "Tumours of settled diagnosis stand in for the uncertain case a tumour board brings, and the rare "
            "diagnoses a board meets are left out. Diagnosis and study are entangled: 11 of the 27 classes come 90% or "
            "more from one study, so a model can partly recognise the study. The diagnosis is made from scratch: the model gets no provisional diagnosis, which a "
            "board would have."
        ),
    )

    # Dataset
    unique_name = "treehouse_pediatric_tumor_type"
    year = "2025"
    domain = "medical & healthcare"
    # UCSC Treehouse Childhood Cancer Initiative, deposited on NCBI GEO with a data descriptor (Scientific Data)
    source = "Other"
    source_url = "https://doi.org/10.1038/s41597-025-05376-z"
    license = (
        "Not stated for the data: released on NCBI GEO (GSE294351) 'without access restrictions' (Beale et al. 2025); "
        "the descriptor is CC BY 4.0"
    )
    download_description = """
        The Treehouse Tumor Compendium v25.01 PolyA on NCBI GEO, series GSE294351 (public 2025-04-18): the clinical
        table (169 KB) and the expression matrix in log2(TPM + 1) over 58,581 HUGO genes (1.3 GB). The matrix of RSEM
        expected counts over 60,498 Ensembl genes in the same series is not needed.

        mkdir -p local-data-warehouse/treehouse_pediatric_tumor_type && cd local-data-warehouse/treehouse_pediatric_tumor_type
        wget https://ftp.ncbi.nlm.nih.gov/geo/series/GSE294nnn/GSE294351/suppl/GSE294351_clinical_Treehouse-Tumor-Compendium-25.01-PolyA_20250131v1.tsv.gz
        wget https://ftp.ncbi.nlm.nih.gov/geo/series/GSE294nnn/GSE294351/suppl/GSE294351_Tumor-25.01-Polya_hugo_log2tpm_58581genes_2025-02-27.tsv.gz
        # md5 8a51d75febec6ab5569bab31382428fa (clinical), 0f4adda964964f4c78e725743ce39b7d (matrix)
    """
    bibtex = """
        @article{beale2025treehouse,
          title={Consistently processed RNA sequencing data from 50 sources enriched for pediatric data},
          author={Beale, Holly C. and Learned, Katrina and Kephart, Ellen T. and Lyle, A. Geoffrey and van den Bout, Anouk and McCabe, Molly and Echandia-Monroe, Kathryn and Khare, Mansi J. and Huang, Elise Y. and Jariwala, Sneha and Antilla, Reyna and Cheney, Allison and Lee, Alex G. and Sayles, Leanne C. and Leung, Stanley G. and Vasquez, Yvonne A. and Sanders, Lauren and Haussler, David and Salama, Sofie R. and Sweet-Cordero, E. Alejandro and Vaske, Olena M.},
          journal={Scientific Data},
          volume={12},
          pages={1134},
          year={2025},
          doi={10.1038/s41597-025-05376-z}
        }
    """
    curation_comments = """
        We start with the Treehouse Tumor Compendium v25.01 PolyA on GEO (GSE294351): the clinical table and the matrix of log2(TPM + 1) over 58,581 HUGO genes, 13,359 datasets from 42 studies, all processed by the TOIL pipeline (STAR, RSEM 1.2.25, GRCh38, GENCODE 23).

        - Prediction point: a tumour of a child, adolescent or young adult has been sequenced (RNA-seq), and its diagnosis is to be confirmed or revised from the expression with the patient's age and sex; the descriptor lists "Provide diagnostic classification for individuals" among the compendium's uses (Table 5), and its abstract says the compendia are used "to infer molecular diagnosis".
        - Rows: the datasets the source flags `pedaya` yes ("pediatric, adolescent and young adult (pedaya, age <= 30)", Fig. 1; the flagged ages run from 0 to 32), 3,477 of 13,359. One dataset is "data generated from one sample"; the source merged technical replicates or kept one of them, and kept samples of one tumour "that might have different biology". The adult datasets (9,621, most of them TCGA) are left out: a tumour-type task over them is the task of `tcga_pancancer_tumor_type` (PROV-6), and only the paediatric cut is a task of its own (PROV-7). The cut still holds 366 TCGA datasets of patients aged up to 30 (336 after the class floor) and 1,337 TARGET datasets; TARGET is also the source of `target_pediatric_relapse_transcriptome`, whose target is another one.
        - Group: the donor (patient). TARGET gives no donor id for 529 of its paediatric datasets and names one patient under each project that sequenced it (`TARGET-20-PARBTV` and `TARGET-21-PARBTV`), so the donor is built from the ids: TARGET's patient code (USI), TCGA's patient barcode, the Treehouse donor id (the dataset id without its sample suffix), the study's donor id, and St. Jude's patient id where a dataset carries one; datasets that share any of these are one donor, hashed. This joins the datasets of 15 TARGET patients without a donor id (one of them, PARBTV, sequenced by two TARGET projects) and of 2 St. Jude patients in two deposits each. Six tumours deposited twice by NCI sarcoma studies (THR49 and THR30) carry no shared id; each pair has the same sex, an age within a year and a correlation of 0.9958 to 0.9973 over the expressed genes, while no other pair of datasets of different donors in the cut passes 0.9913, so the six pairs are listed in `SAME_TUMOUR` and joined (LEAK-17; decision table). They are the same tumour by similarity, not by a shared id, so the THR49 copy of each is dropped (SPLIT-24; 5 datasets, the sixth pair's donor is dropped below for its two diagnoses), as for other copies found without an id. The 4 other pairs of datasets of different donors above 0.99 (the highest 0.9914, two TCGA cervical carcinomas of women aged 24) were checked by their ids only: their TCGA patient barcodes differ, so they stay two donors (LEAK-19). 3,010 donors remain; 212 have 2 to 8 datasets.
        - Two donors the source gives two diagnoses are dropped (5 datasets): St. Jude's SJLGG065, a dysembryoplastic neuroepithelial tumour in THR11 and a glioma in THR24, and one NCI tumour, Ewing sarcoma in THR30 and CIC-rearranged sarcoma in THR49 (the class of the later study, below the floor).
        - Target: the source's harmonised diagnosis (`disease`), kept for the 27 diagnoses held by 10 or more donors (3,256 datasets). The 84 others (211 datasets; 72 have fewer than 5 datasets) are dropped: below 10 donors a class has fewer than 3 donors in some test fold of the grouped split (TP-5, TP-8), the floor sarcoma used for its MPNST. Merging them into an "other" class has no convention behind it (TP-7). The smallest classes kept are breast invasive carcinoma (10 donors), synovial sarcoma (11), dysembryoplastic neuroepithelial tumour (12) and hepatoblastoma (12).
        - Note: the source's labels are kept as written, also where one is a subtype of another or a catch-all: acute megakaryoblastic leukaemia (88 donors, 99% from St. Jude, THR24) is a type of acute myeloid leukaemia in the WHO classification and a class of its own here; `glioma` holds low- and high-grade gliomas; `lymphoma` and `supratentorial embryonal tumor NOS` are not specified further. Under the grouped split the two myeloid classes separate (4 of 452 acute myeloid leukaemia datasets predicted as the megakaryoblastic type, 7 of 93 the other way; logistic regression on 100 principal components), but holding out TARGET, which has no megakaryoblastic leukaemia, leaves 35% of its AML recognised.
        - Dropped: `icd_disease`, the ICD-O code of the diagnosis (an encoding of the target); the ids (`th_dataset_id`, `study_accession`, `study_dataset_id`, `study_donor_id`); the study (`study_id`, `source_name`), which is no property of the tumour and would let a model name the batch; `organism` and `pedaya`, constant on these rows.
        - Features: the genes as published, log2(TPM + 1) computed per dataset (each dataset's TPM sums to 1e6 within 0.002%, so no scaling over datasets: LEAK-30 holds), minus the 3,657 genes with no expression in any kept dataset and the 353 whose values copy an earlier gene's: 54,571 genes; plus the age at diagnosis and the sex. Width is no reason to drop genes (CLEAN-22).
        - Every TPM is put on RSEM's grid of two decimals (`on_tpm_grid`, LEAK-13): the datasets of every study are on it except TCGA's and TARGET's, where 0.2% of the positive values are (TPM 0.0101, 0.0201, 0.0301 where the rest have 0.01, 0.02, 0.03), so an exact low value names the source, and the source the diagnosis for several classes. Rounding moves a value by at most 0.0071 in log2 units and leaves the other studies' values as published. Every value is recomputed this way, also those already on the grid (they move by less than 1e-9): recomputing only the off-grid values had left TCGA's and TARGET's values with about 16 written decimals against 12 for the other studies, a new mark of the source (it lowered a linear model's log loss by 0.002 on top of the expression); now 98% of the positive values of both groups are written with 15 or more. The leak probe's number-format check, which counts at most 8 decimals, still scores macro ROC AUC 0.975 (0.978 before): it reads which genes are zero, which is expression, not the mark. It removes the mark, not the study's trace in the expression: on 1,500 low-expressed genes, LightGBM separates TARGET from the other studies within acute lymphoblastic leukaemia at ROC AUC 0.997 before and 0.998 after, within neuroblastoma 0.96 and 0.94.
        - Age: `unknown` (407 datasets) is missing, and every age is rounded down to whole years. TARGET writes the age with two decimals from the days at diagnosis (99% of its datasets fractional), TCGA as whole years with `.00`, most Treehouse sites as whole years and St. Jude both ways (54% fractional), so a fractional age points at the study and through it at the diagnosis: alone, it separates acute myeloid leukaemia from the rest at ROC AUC 0.71 and Wilms tumour at 0.69 (LEAK-13: one precision for every row). After the rounding the age's format says only whether it is missing (below).
        - Sex: `unknown` (311 datasets) is missing.
        - Potential leak, kept on purpose: age and sex are missing by study, not by patient (St. Jude's THR24 gives no age for 282 of its 695 datasets and no sex for 200; THR37 gives neither, THR15 and THR31 no age, THR08 no sex), and a tumour board always knows both. The missingness marks the two classes St. Jude holds alone: 89% of the acute megakaryoblastic leukaemia and 96% of the choroid plexus carcinoma datasets lack the age (88% and 89% the sex), so missing age alone scores ROC AUC 0.90 and 0.92 for them. Measured on the shipped splits (logistic regression on 100 principal components, first fold of 3 repeats): age and sex as values lower the log loss from 0.193 to 0.189, the missing indicators on top to 0.183, and for acute megakaryoblastic leukaemia from 0.365 to 0.270. Kept: both are inputs a tumour board uses (USE-6), and the gain from their missingness is 3% of the log loss; dropping age and sex removes it at the cost of their own signal.
        - Potential leak, kept on purpose: the diagnosis is entangled with the study. Of the 16 diagnoses with 30 or more donors, Wilms tumour (0.91), thyroid carcinoma (0.94), rhabdoid tumour (0.96), testicular germ cell tumour (0.98) and acute megakaryoblastic leukaemia (0.99) come 90% or more from one study, and so do six of the smaller classes, four of them from one study alone (11 of the 27 classes, 552 datasets; decision table). The expression carries the study: within a diagnosis, one study against the others separates at a median ROC AUC of 0.97 (29 pairs, 0.75 to 1.00; logistic regression on 100 principal components, out of fold by donor). Whether models use it: where a held-out study leaves 30 or more training datasets of its class, accuracy falls from 0.984 under the donor split to 0.85 with the study held out (2,345 datasets), 0.945 without TARGET's acute myeloid leukaemia; the classes held by one study cannot be scored that way. Kept: the study is no feature, a split by study removes those 11 classes from training (splits comment), and much of the signal carries across studies: with its largest study held out, glioma keeps an accuracy of 0.91 (0.98 under the donor split), medulloblastoma 1.00 (1.00), neuroblastoma 0.99 (1.00), osteosarcoma 0.99 (0.99), embryonal rhabdomyosarcoma 1.00 (1.00) and alveolar rhabdomyosarcoma 0.81 (0.85). Revisit when a cross-study variant over the classes several studies hold is wanted.
    """
    splits_comment = """
        Grouped by donor, stratified on the diagnosis: 10 repeats of 3-fold cross-validation over the 3,010 donors, so a patient's datasets (up to 8) stay on one side and the test data stands for new patients of the studies the compendium holds. A split by study would stand for a new hospital, but 11 of the 27 classes come 90% or more from one study and would leave training whenever their study is tested. Where a class keeps 30 or more training datasets, holding out its study lowers accuracy from 0.984 to 0.85 (0.945 without TARGET's acute myeloid leukaemia; logistic regression on 100 principal components), so the scores are optimistic for a hospital whose sequencing the compendium does not hold.
    """

    # Task
    target = "diagnosis"
    problem_type = "multiclass_classification"
    metric = Metric.fallback(
        reason=(
            "The source is a data descriptor (Beale et al. 2025, Scientific Data) that releases the compendium and "
            "trains no classifier; its uses (Table 5) name diagnostic classification without a metric. Comitani "
            "et al. (2023, Nature Medicine), who classify childhood cancers from RNA-seq on other data, report "
            "accuracy, precision, recall, the area under the precision-recall curve and a hierarchical similarity, "
            "tune on micro-F1 and select models on macro-F1 (full text, PMC10033451): several metrics, none chosen as "
            "the one, so the multiclass fallback."
        ),
    )
    grouping = Grouping(
        on="donor",
        labels="per_group",
        prediction_unit="row",
        context="none",
        definition="""
            One group is one donor (patient): the datasets linked by any of the patient's ids (TARGET's patient code, TCGA's patient barcode, the Treehouse donor id, the study's donor id, St. Jude's patient id) or listed in `SAME_TUMOUR`. A donor's datasets are samples of one tumour (several sites, diagnosis and relapse), all with one diagnosis, and the descriptor keeps "samples from the same tumor that might have different biology" (Beale et al. 2025). A diagnosis is made for a new patient's tumour, so whole donors are held out; each dataset is scored, as a sample is diagnosed alone.
        """,
    )

    prepared_raw_files = (PEDAYA_FILE,)

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        import pyarrow as pa
        import pyarrow.csv as pacsv

        clinical = read_clinical(raw_dir)
        datasets = clinical.loc[clinical["pedaya"] == "yes", "th_dataset_id"].tolist()
        matrix = pacsv.read_csv(
            raw_dir / EXPRESSION_FILE,
            read_options=pacsv.ReadOptions(block_size=1 << 26),
            parse_options=pacsv.ParseOptions(delimiter="\t"),
            convert_options=pacsv.ConvertOptions(
                include_columns=["Gene", *datasets], column_types={d: pa.float64() for d in datasets}
            ),
        )
        genes = matrix.column("Gene").to_pylist()
        assert len(set(genes)) == len(genes), "gene names repeat"
        values = np.column_stack([matrix.column(d).to_numpy() for d in datasets]).T  # datasets x genes
        del matrix
        frame = pd.DataFrame(values, index=pd.Index(datasets, name="th_dataset_id"), columns=genes)
        frame.to_parquet(raw_dir / PEDAYA_FILE)

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        return {"clinical": read_clinical(raw_dir), "expression": pd.read_parquet(raw_dir / PEDAYA_FILE)}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        # 1. The paediatric, adolescent and young-adult datasets and their donor (patient ids linked across studies).
        cut = paediatric_cut(raw["clinical"])
        # 2. Drop the donors the source gives two diagnoses (one tumour labelled differently by two studies) and the
        #    THR49 copies of the tumours deposited twice.
        cut = shipped_cut(cut)
        # 3. The diagnoses held by MIN_DONORS donors or more; the rarer ones are dropped.
        donors = cut.groupby("disease")["donor"].nunique()
        cut = cut[cut["disease"].isin(donors.index[donors >= MIN_DONORS])]
        # 4. Age at diagnosis in completed years (one precision for every study), sex; `unknown` is missing.
        age = pd.to_numeric(cut["age_at_dx"].replace("unknown", np.nan))
        meta = pd.DataFrame(
            {
                "age_at_diagnosis": np.floor(age).to_numpy(),
                "sex": cut["sex"].replace("unknown", np.nan).to_numpy(),
                "donor": anonymize_ids(cut["donor"]).to_numpy(),
                self.target: cut["disease"].to_numpy(),
            },
            index=cut["th_dataset_id"].to_numpy(),
        )
        # 5. The genes as published (log2(TPM + 1) per dataset), every TPM on RSEM's grid of 0.01 (TCGA and TARGET
        #    datasets are off it, a mark of their source), without the genes all zero on these rows or that copy an
        #    earlier gene.
        expression = raw["expression"].loc[meta.index]
        assert not set(expression.columns) & set(NOT_GENES), "a gene name clashes with a column of ours"
        expression = pd.DataFrame(
            on_tpm_grid(expression.to_numpy()), index=expression.index, columns=expression.columns
        )
        expression = expression.loc[:, expression.to_numpy().max(axis=0) > 0]
        expression = expression.loc[:, ~expression.T.duplicated(keep="first").to_numpy()]
        return pd.concat([expression, meta], axis=1).reset_index(drop=True)

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["sex", "donor"])

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        cut = paediatric_cut(raw["clinical"])
        table = diagnosis_counts(shipped_cut(cut))
        kept = table[table["donors"] >= MIN_DONORS]
        dropped = table[table["donors"] < MIN_DONORS]
        rest = pd.DataFrame(
            {"datasets": [dropped["datasets"].sum()], "donors": [dropped["donors"].sum()]},
            index=[f"{len(dropped)} diagnoses with fewer than {MIN_DONORS} donors (dropped)"],
        )
        # Donors of several datasets that a single id of the source would have split: by the way they were joined.
        is_target = cut["th_dataset_id"].str.startswith("TARGET-")
        by_donor = cut.groupby("donor").agg(
            datasets=("th_dataset_id", "size"),
            studies=("study_id", "nunique"),
            target_without_id=("study_donor_id", lambda s: int((is_target[s.index] & (s == "unavailable")).sum())),
            twice_deposited=("th_dataset_id", lambda s: int(s.isin(SAME_TUMOUR).any())),
            diagnoses=("disease", "nunique"),
        )
        joined = by_donor[by_donor["datasets"] > 1]
        how = np.select(
            [joined["twice_deposited"] == 1, joined["studies"] > 1, joined["target_without_id"] > 0],
            [
                "one NCI tumour deposited twice (SAME_TUMOUR)",
                "one St. Jude patient in two deposits (St. Jude patient id)",
                "one TARGET patient's datasets without a donor id (TARGET patient code)",
            ],
            default="",
        )
        joined = joined.assign(how=how)[how != ""]
        link_table = (
            joined.assign(shipped=np.where(joined["diagnoses"] > 1, "dropped: two diagnoses", "kept as one donor"))
            .groupby(["how", "shipped"])
            .agg(donors=("datasets", "size"), datasets=("datasets", "sum"))
            .reset_index()
        )
        expression = raw["expression"]
        expressed = expression.to_numpy().max(axis=0) > 0  # the genes expressed in any dataset of the cut
        pairs = []
        for copy, original in SAME_TUMOUR.items():
            a, b = expression.loc[copy].to_numpy()[expressed], expression.loc[original].to_numpy()[expressed]
            info = cut.set_index("th_dataset_id").loc[[copy, original]]
            pairs.append(
                {
                    "THR49 dataset": copy,
                    "THR30 dataset": original,
                    "correlation": round(float(np.corrcoef(a, b)[0, 1]), 4),
                    "age": " / ".join(info["age_at_dx"]),
                    "sex": " / ".join(info["sex"]),
                    "diagnoses": " / ".join(info["disease"]),
                }
            )
        return [
            Decision(
                title=f"Diagnoses held by {MIN_DONORS} or more donors ship as classes",
                why=(
                    f"With fewer than {MIN_DONORS} donors a class has fewer than 3 donors in some test fold of the "
                    "grouped 3-fold split. The table gives each diagnosis's datasets, donors and studies in the "
                    "paediatric cut, and how much of it the largest study holds: the study a model could recognise."
                ),
                evidence=pd.concat([kept, rest]),
            ),
            Decision(
                title="The donor joins a patient's datasets across studies and TARGET projects",
                why=(
                    "TARGET gives no donor id for 529 of its paediatric datasets, and its barcode names one patient "
                    "(the USI) under the code of each project that sequenced it; St. Jude's patient ids recur in "
                    "other deposits. The donor is every dataset linked by such an id. The table counts the donors "
                    "the source's donor id alone would have split; the two the source gives two diagnoses are "
                    "dropped."
                ),
                evidence=link_table,
            ),
            Decision(
                title="Six tumours deposited twice by NCI sarcoma studies: one donor each, the THR49 copy dropped",
                why=(
                    "No id links the two deposits. Each pair has the same sex and an age within a year, and "
                    "correlates over the genes expressed in the cut far above any other pair of datasets of different "
                    "donors (at most 0.9913). One pair is Ewing sarcoma in THR30 and CIC-rearranged sarcoma in "
                    "THR49, so that donor has two diagnoses and is dropped; of the other five pairs the THR49 copy is dropped (SPLIT-24), "
                    "the THR30 dataset ships."
                ),
                evidence=pd.DataFrame(pairs),
            ),
        ]
