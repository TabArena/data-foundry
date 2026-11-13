"""Curated dataset definition for `sarcoma_methylation_classification` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import gzip
from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, Metric, TaskSummary

MATRICES = {
    "450k": "GSE140686_GPL13534_matrix_processed.txt.gz",
    "EPIC": "GSE140686_GPL21145_matrix_processed.txt.gz",
}
"""GEO's processed matrices, one per array type: a probe x (beta, detection p) table per sample."""

PROBE_FILTERS = (
    "filter/xy_11551probes.vh20151030.txt",
    "filter/snp_7998probes.vh20151030.txt",
    "filter/amb_3965probes.vh20151030.txt",
    "filter/epicV1B2_32260probes.vh20160325.txt",
)
"""The probe lists of the Heidelberg classifier's training code (Capper et al. 2018, `mnp_training`), whose counts are
the paper's: probes on the X and Y chromosomes, probes with a common SNP at or near the CpG, probes that do not map
uniquely, and 450k probes missing from the EPIC array."""

CLASS_PREFIX = "methylation class "

CLASS_FAMILIES = {
    "chondrosarcoma (group A)": "chondrosarcoma (family)",
    "chondrosarcoma (group B)": "chondrosarcoma (family)",
    "chondrosarcoma (IDH group A)": "chondrosarcoma (IDH) (family)",
    "chondrosarcoma (IDH group B)": "chondrosarcoma (IDH) (family)",
}
"""The four subgroups of conventional chondrosarcoma that only the clustering separates (Supplementary Data 2:
category 2, all 60 cases histologically conventional chondrosarcoma), shipped as the source's two methylation class
families, whose scores the classifier adds up (SEL-4)."""

SITE_TYPOS = {
    "Soft tisse": "Soft tissue",
    "abomen": "abdomen",
    "thracic wall": "thoracic wall",
    "pevic girdle": "pelvic girdle",
}
"""Misspelt parts of Supplementary Data 1's `Site` (2, 3, 2 and 1 cases), each the same place as its spelt form."""


def clean_site(site: pd.Series) -> pd.Series:
    """`Site` with its parts stripped and joined by ", ", the typos fixed and "lower, limbs" read as "lower limbs".

    Trailing spaces and missing separators split one place into two levels; no two distinct places merge.
    """

    def one(value: str) -> str:
        parts = [part.strip() for part in value.split(",")]
        parts = [SITE_TYPOS.get(part, part) for part in parts if part]
        text = ", ".join(parts).replace("lower, limbs", "lower limbs")
        return text

    return site.map(one, na_action="ignore")


def reference_labels(sd1: pd.DataFrame) -> pd.DataFrame:
    """Supplementary Data 1 indexed by GEO's sample name (`REFERENCE_SAMPLE n`), with the class without its prefix."""
    labels = sd1.set_index("ID")
    assert labels.index.is_unique
    assert labels["Methylation Class Name"].str.startswith(CLASS_PREFIX).all()
    # The source writes "Ewing's sarcoma" with an acute accent (U+00B4) for the apostrophe.
    labels["class"] = labels["Methylation Class Name"].str.removeprefix(CLASS_PREFIX).str.replace("\u00b4", "'")
    return labels


def sample_names(path: Path) -> list[str]:
    """The reference cases' names in the header of a processed matrix."""
    with gzip.open(path, "rt") as handle:
        header = [name.strip('"') for name in handle.readline().rstrip("\n").split("\t")]
    return [name for name in header if name.startswith("REFERENCE_SAMPLE ")]


class SarcomaMethylationClassification(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "Which methylation class, the tumour type a DNA-methylation classifier assigns, does a bone or soft-tissue "
            "tumour belong to, judged from its methylation profile and where it grew?"
        ),
        use_case=(
            "A pathologist uploads a sarcoma's methylation array to a classifier at diagnosis and uses the class to "
            "confirm, refine or revise the histological diagnosis; the source runs such a classifier, and in its "
            "validation 29 of 59 cases where the two disagreed were revised in favour of the class."
        ),
        row=(
            "One tumour of the source's reference set: 1,077 cases, one per patient, the dated ones profiled from 2013 "
            "to 2019 on two array types and sent by 31 centres and studies, 28 of them non-tumour control tissue."
        ),
        predicted=(
            "Its methylation class, one of 63: 60 tumour classes, most of them one WHO tumour type (chordoma the "
            "largest with 59 cases, ten classes of 7), and 3 kinds of control tissue."
        ),
        known=(
            "The methylation levels of 405,842 CpG sites in the tumour's DNA, the tumour's site (and its tissue: "
            "bone, soft tissue, skin, viscera, intracranial), and whether it is a primary tumour, a recurrence or a "
            "metastasis."
        ),
        split=(
            "Random patients, so the test data stands for new patients' tumours, mostly from centres the training "
            "data has seen: without its centre in training a tumour scores about 0.8 log loss against 0.24. A split "
            "by centre would leave about 74 test tumours per fold with no training tumour of their class."
        ),
        changes=(
            "Four chondrosarcoma subgroups that only the clustering separates are merged into the source's two class "
            "families; the histological diagnosis, the referring centre and the DNA material are not inputs."
        ),
        fit="approximate",
        fit_reason=(
            "The inputs are what the classifier sees at diagnosis, but the reference cases are prototypical (a "
            "quarter of the later validation cases reached no class, and 'no match' cannot be scored here), some "
            "classes were designated by clustering these same profiles, and the array type follows the class (31 "
            "of 63 classes on one type only)."
        ),
    )

    # Dataset
    unique_name = "sarcoma_methylation_classification"
    year = "2020"
    domain = "medical & healthcare"
    # GEO series GSE140686 (public 2020-03-01) and the paper's supplementary tables (Nature Communications, 2021)
    source = "Other"
    source_url = "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE140686"
    license = (
        "No licence stated on GEO for GSE140686; the paper and its supplementary data are CC BY 4.0; the probe lists "
        "of mnp_training are MIT"
    )
    download_description = """
        We download GEO's processed matrices of GSE140686 (minfi `preprocessIllumina` per sample, 2019-11-19; the
        450k matrix 1.6 GB, the EPIC matrix 3.3 GB), the paper's Supplementary Data 1 (the class of each reference
        case) and 2 (the class table), and the four probe lists the paper's filter counts come from (the training
        code of the Heidelberg brain tumour classifier, github.com/mwsill/mnp_training, pinned to commit ece7262).
        We leave out the IDATs (`GSE140686_RAW.tar`, 18 GB) and the signal-intensity matrices (10 GB).

        mkdir -p local-data-warehouse/sarcoma_methylation_classification/filter
        cd local-data-warehouse/sarcoma_methylation_classification
        GEO=https://ftp.ncbi.nlm.nih.gov/geo/series/GSE140nnn/GSE140686/suppl
        wget $GEO/GSE140686_GPL13534_matrix_processed.txt.gz $GEO/GSE140686_GPL21145_matrix_processed.txt.gz
        ESM=https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-020-20603-4/MediaObjects
        wget $ESM/41467_2020_20603_MOESM4_ESM.xlsx $ESM/41467_2020_20603_MOESM5_ESM.xlsx
        MNP=https://raw.githubusercontent.com/mwsill/mnp_training/ece7262015b896d31078d8125091c83c06158d59/filter
        for f in xy_11551probes.vh20151030.txt snp_7998probes.vh20151030.txt amb_3965probes.vh20151030.txt \\
            epicV1B2_32260probes.vh20160325.txt; do wget -P filter $MNP/$f; done
    """
    bibtex = """
        @article{koelsche2021sarcoma,
          title={Sarcoma classification by {DNA} methylation profiling},
          author={Koelsche, Christian and Schrimpf, Daniel and Stichel, Damian and Sill, Martin and Sahm, Felix and
                  Reuss, David E. and Blattner, Mirjam and Worst, Barbara and Heilig, Christoph E. and Beck, Katja
                  and others},
          journal={Nature Communications},
          volume={12},
          number={1},
          pages={498},
          year={2021},
          doi={10.1038/s41467-020-20603-4}
        }
    """
    curation_comments = """
        We start with GEO's processed beta matrices of GSE140686 (450k and EPIC) and the paper's Supplementary Data 1 (Koelsche et al. 2021), which gives the methylation class of each of the 1,077 reference cases.

        - Prediction point: a bone or soft-tissue tumour has been profiled on a methylation array at diagnosis, and the model assigns its methylation class from the profile, the site and the manifestation. The histological diagnosis is not an input.
        - Rows: the 1,077 reference cases (485 on 450k, 592 on EPIC), one per patient ("All samples of the reference and validation set are from individual/different patients", Methods); GEO's sample names are Supplementary Data 1's `ID` for all 1,077. GEO's 428 validation cases are left out: their labels are institutional diagnoses and the classifier's own calls (Supplementary Data 3).
        - Target: the methylation class. The classes come from "Unsupervised clustering, respecting the minimal number of seven cases per group" of examined, molecularly tested cases; Supplementary Data 2 places 48 tumour classes as one WHO entity, 8 as a subgroup, 3 as combining entities, 3 as not WHO entities. The four subgroups of conventional chondrosarcoma (60 cases, one histology) are told apart by the clustering alone, and the paper's cross-validation errors "predominantly occurred" among them and three classes with BCOR alterations; they ship as the source's two class families (18 and 42 cases), whose scores the classifier adds up (SEL-4). The other subgroup and non-WHO classes stay, each defined outside the clustering too (a BCOR or CIC fusion, a MYOD1 or DICER1 mutation, retained H3K27 trimethylation, a histological subtype). 63 classes; the ten of 7 cases (2 or 3 per test fold) are 6.5% of the test rows and carry 12% of a random forest's log loss (3 folds) and 20% of a logistic regression's (9 folds). The classes of 9 cases or fewer are 15.8% of the rows and carry 27% to 40% of the loss, above the 22% kept for sarcoma (TP-8).
        - Controls: the three classes of non-tumour tissue (blood 10, skeletal muscle 8, reactive tissue 10) stay, as the classifier has them for samples with too little tumour; the blood controls are EDTA blood, not tissue. The clinical columns recognise them: all 28 lack `manifestation`, and a missing manifestation with one of three sites flags the 28 and 4 tumours; every reactive-tissue control is a missing manifestation with site `Soft tissue, trunk, paraspinal` (10 of 10). Format features built on this (missing values, exact 0 and 1 betas) moved a logistic regression's log loss from 0.1119 to 0.1116, inside the noise (LEAK-13).
        - Features: GEO's beta values, processed per sample (minfi `preprocessIllumina`); the paper's later correction for array and material over all samples (limma `removeBatchEffect`) is not in them, so no value depends on another case's (LEAK-30 does not apply). GEO holds the same 408,768 CpG probes for both arrays, none on X or Y, against the paper's 428,230; we drop the 2,926 on the paper's filter lists (1,681 near a common SNP, a germline genotype; 1,283 that do not map uniquely; 38 on both), which leaves 405,842. No probe is constant or a copy of another, no two tumours are identical, and the closest pairs (Pearson 0.98 to 0.99) are blood controls. Stored as float32 (7 significant digits; the arrays measure about 3).
        - Missing and exact values: 18,544 betas in 7,255 probes are missing (at most 232 in a tumour), mostly on one array type, and stay missing; their pattern alone scores macro ROC AUC 0.81 against 0.996 for the betas. Exact betas of 0 and 1 (0.47%, where background correction sets a channel to zero) are more frequent on 450k and frozen samples, and their pattern alone scores 0.75 to 0.84 (the leak probes' number format). Every case went through the same processing, so both follow the array, the material and the value, not a recording by class (LEAK-13); kept.
        - Clinical columns: `site`, `site_tissue` and `manifestation` ship as categories, known when the tumour is sent. `site` is Supplementary Data 1's site with its parts stripped of spaces and joined by ", " and four misspellings fixed (`Soft tisse`, `abomen`, `thracic wall`, `pevic girdle`), which leaves 186 places for the 197 spellings, 88 missing; `Blood` is the 10 blood controls. Four femurs are listed under upper limbs (`Bone, limbs, upper limbs, femur`) and stay as written. `site_tissue` is its first part (bone, soft tissue, skin, visceral, intracranial, lymph node, blood). `manifestation` is primary, recurrence or metastasis, missing for the 28 controls and 28 tumours. Dropped: `Diagnosis` (the histology that, with the clustering, set the class), `Supplier` (31 centres and studies; 18 classes take 90% or more from one), `Batch` (the array date), `DNA` (its `EDTA blood` is the blood control class, and it disagrees with GEO's material for 51 cases), the tumour cell content (estimated from the profile by a model), `IDAT` and `Colour`.
        - Potential leak, kept on purpose: the betas give the array type away (ROC AUC 1.00, logistic regression, 3 folds), and 31 of the 63 classes are on one array type only (313 cases). The shortcut is small: EPIC tumours of the two-array classes put 0.044 of their probability on EPIC-only classes, 450k tumours 0.024 (9 folds). Revisit with the IDATs. The record carries `Class-dependent Recording` for it.
        - Anomaly: Supplementary Data 2's group sizes differ by one case from Supplementary Data 1's counts for three classes (malignant peripheral nerve sheath tumour 27 against 26, solitary fibrous tumour 27 against 26, mesenchymal chondrosarcoma 9 against 8); the shipped classes are Supplementary Data 1's.
        - Note: 40 arrays (35 + 5) are also in the Heidelberg CNS tumour series (cns_tumor_methylation_classification), with the same Sentrix IDs: 35 in GSE90496 (`REFERENCE_SAMPLE` 717, 721, 722, 725, 727, 729, 730, 731, 741, 744, 748, 755, 756, 759, 788, 798, 800 to 807, 811, 814, 820, 971, 973, 976, 977, 979 to 982) and 5 in GSE109379 (580, 600, 750, 939, 972): 10 schwannomas, 9 solitary fibrous tumours, 8 chordomas, 9 melanomas and 4 Ewing sarcomas, all from Heidelberg and Tübingen neuropathology. The tasks differ (PROV-7); dropping them here would cut melanoma from 12 cases to 3.
    """

    splits_comment = """
        IID over patients, stratified on the class: one tumour per patient, and the classifier types new patients' tumours. The larger hidden group is the referring centre (`Supplier`, 31 centres and studies, dropped): removing all tumours of a test tumour's centre from training raises its log loss to 0.80 against 0.235 for removing as many random tumours of the same classes (about +0.57, from +0.09 to +1.5 by centre; the comparison scores only tumours whose class keeps a training tumour, so it is approximate). Grouping by centre gives 0.86 against 0.18 under IID, but leaves about 74 test tumours per fold whose class has no training tumour, as 18 classes take 90% or more of their cases from one centre; so the split stays IID and the scores hold for a new patient of a known centre more than for a new lab. The array slide sits inside the centre: 740 of the 1,077 tumours share an array slide (Sentrix chip) with a tumour of their class, which a new patient's tumour never does. Removing a test fold's slide mates from training costs 0.019 more log loss than removing as many random tumours of the same classes (logistic regression; 0.057 for 5 nearest neighbours; 6 folds each), so the scores are slightly optimistic. Grouping by slide would leave about 13 test tumours per fold whose class has no training tumour.
    """

    # Task
    target = "methylation_class"
    problem_type = "multiclass_classification"
    metric = Metric.fallback(
        reason=(
            "The paper reports for its cross-validation 'an estimated error rate of 1.95% for raw scores and 0.65% "
            "for calibrated scores and a multi-class area under receiver operating characteristic curve of 0.99 and a "
            "Brier score of 0.05' (Methods, Classifier development): three metrics side by side, none named as the "
            "criterion (MET-5). The calibrated-score cut-off of 0.9 decides whether a case gets a class at all, not "
            "which one, so it fixes no threshold metric (MET-7). GEO and the classifier's site define none."
        ),
    )

    prepared_raw_files = ("reference_betas.parquet",)

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        # The two matrices are 4.9 GB of gzipped text; their reference cases' beta columns are joined on the probe
        # once and kept probe by sample (a parquet file of 1,077 columns; one of 400,000 columns would not be).
        import pyarrow as pa
        import pyarrow.csv as pacsv
        import pyarrow.parquet as pq

        blocks = []
        for file in MATRICES.values():
            with gzip.open(raw_dir / file, "rt") as handle:
                header = [name.strip('"') for name in handle.readline().rstrip("\n").split("\t")]
            # Each beta column is followed by its "Detection Pval" column; the names repeat, so name them apart.
            names = [
                f"{header[i - 1]} detection p" if name == "Detection Pval" else name for i, name in enumerate(header)
            ]
            betas = [name for name in names if name.startswith("REFERENCE_SAMPLE ") and not name.endswith(" p")]
            table = pacsv.read_csv(
                raw_dir / file,
                read_options=pacsv.ReadOptions(column_names=names, skip_rows=1, block_size=1 << 26),
                parse_options=pacsv.ParseOptions(delimiter="\t"),
                convert_options=pacsv.ConvertOptions(
                    include_columns=[names[0], *betas],
                    column_types={name: pa.float64() for name in betas} | {names[0]: pa.string()},
                ),
            )
            block = table.to_pandas().set_index(names[0])
            assert block.index.is_unique, file
            blocks.append(block)
        assert blocks[0].index.equals(blocks[1].index), "the two matrices hold different probes"
        betas = pd.concat(blocks, axis=1)
        betas.index.name = "probe"
        pq.write_table(pa.Table.from_pandas(betas, preserve_index=True), raw_dir / "reference_betas.parquet")

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame | pd.Series]:
        import pyarrow.parquet as pq

        return {
            "betas": pq.read_table(raw_dir / "reference_betas.parquet").to_pandas(),  # probe x sample
            "sd1": pd.read_excel(raw_dir / "41467_2020_20603_MOESM4_ESM.xlsx", engine="openpyxl"),
            "sd2": pd.read_excel(raw_dir / "41467_2020_20603_MOESM5_ESM.xlsx", engine="openpyxl", header=1),
            "platform": pd.Series(
                {name: platform for platform, file in MATRICES.items() for name in sample_names(raw_dir / file)}
            ),
            "filters": pd.Series(
                {probe: file for file in PROBE_FILTERS for probe in (raw_dir / file).read_text().split()}
            ),
        }

    def _clean(self, raw: dict[str, pd.DataFrame | pd.Series]) -> pd.DataFrame:
        betas = raw["betas"]
        labels = reference_labels(raw["sd1"])
        # 1. One row per reference case: GEO's sample name is Supplementary Data 1's `ID` (all 1,077 match, and so do
        #    the IDAT names).
        assert set(betas.columns) == set(labels.index)
        # 2. The probes: GEO's 408,768 minus the 2,926 on the paper's filter lists (SNP and non-unique probes; GEO
        #    holds none on X or Y and none missing from EPIC).
        probes = betas.index[~betas.index.isin(raw["filters"].index)]
        # 3. The features: the betas as GEO publishes them, one row per case, stored as float32.
        features = betas.loc[probes].T.astype(np.float32)
        # 4. The clinical columns known at diagnosis; the diagnosis, the supplier, the batch, the DNA material and the
        #    purity estimate are left out (curation notes).
        clinical = labels.loc[features.index, ["Site", "Manifestation"]].rename(columns=str.lower)
        clinical["site"] = clean_site(clinical["site"])
        clinical.insert(1, "site_tissue", clinical["site"].str.split(", ").str[0])
        # 5. The target: the methylation class, with the four conventional-chondrosarcoma subgroups as their families.
        target = labels.loc[features.index, "class"].replace(CLASS_FAMILIES).rename(self.target)
        return pd.concat([target, clinical, features], axis=1)

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["site", "site_tissue", "manifestation"])

    def _decisions(self, raw: dict[str, pd.DataFrame | pd.Series], df: pd.DataFrame) -> list[Decision]:
        labels = reference_labels(raw["sd1"])
        sd2 = raw["sd2"]
        category = pd.Series(
            sd2.iloc[:, 4].to_numpy(), index=sd2.iloc[:, 0].str.removeprefix(CLASS_PREFIX).to_numpy(), name="category"
        )
        platform = raw["platform"].reindex(labels.index)
        classes = (
            pd.DataFrame(
                {
                    "source class": labels["class"],
                    "shipped as": labels["class"].replace(CLASS_FAMILIES),
                    "array": platform,
                }
            )
            .groupby(["shipped as", "source class"])["array"]
            .value_counts()
            .unstack(fill_value=0)
        )
        classes["category (Supplementary Data 2)"] = category.reindex(classes.index.get_level_values(1)).to_numpy()
        merged = classes.loc[sorted(set(CLASS_FAMILIES.values()))]
        n_probes = len(raw["betas"])
        dropped = raw["filters"][raw["filters"].index.isin(raw["betas"].index)].value_counts()
        probes = pd.DataFrame(
            {"probes": [n_probes, *dropped.to_numpy(), n_probes - int(dropped.sum())]},
            index=pd.Index(
                ["in GEO's matrices (both arrays)", *[f"dropped: on {f}" for f in dropped.index], "kept"],
                name="step",
            ),
        )
        by_array = classes.groupby(level=0)[["450k", "EPIC"]].sum()
        single = by_array[(by_array == 0).any(axis=1)]
        arrays = pd.DataFrame(
            {
                "classes": [len(by_array), int((by_array["EPIC"] == 0).sum()), int((by_array["450k"] == 0).sum())],
                "cases": [int(by_array.to_numpy().sum()), int(single["450k"].sum()), int(single["EPIC"].sum())],
            },
            index=pd.Index(["all", "on the 450k array only", "on the EPIC array only"], name="shipped classes"),
        )
        return [
            Decision(
                title="Target: four chondrosarcoma subgroups shipped as the source's two class families",
                why=(
                    "The four subgroups of conventional chondrosarcoma come from the clustering alone (category 2 "
                    "of Supplementary Data 2; all 60 cases are histologically conventional chondrosarcoma), and the "
                    "paper's cross-validation errors 'predominantly occurred' between them and among three classes "
                    "with BCOR alterations. The classifier adds their scores up into two methylation class families, "
                    "the IDH-mutant subgroups and the others, which ship as the classes (SEL-4)."
                ),
                evidence=merged,
            ),
            Decision(
                title="Probes: GEO's matrices minus the paper's SNP and non-unique probe lists",
                why=(
                    "GEO's two matrices hold the same 408,768 CpG probes, already without the X and Y probes and "
                    "the 450k probes missing from EPIC; the paper also removed probes near a common SNP (the "
                    "patient's genotype) and probes that do not map uniquely, with the lists of the Heidelberg "
                    "classifier's training code."
                ),
                evidence=probes,
            ),
            Decision(
                title="Array type follows the class",
                why=(
                    "The array type is not a column, but the betas give it away, and half the classes were profiled "
                    "on one array type only. A model can lean on the array; the curation notes give the size of "
                    "that shortcut."
                ),
                evidence=arrays,
            ),
        ]
