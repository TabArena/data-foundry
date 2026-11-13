"""Curated dataset definition for `aegis_bronchial_airway_lung_cancer` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import gzip
import sqlite3
import tarfile
import tempfile
from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, TaskSummary, decode, drop_columns

SERIES_MATRIX = "GSE66499_series_matrix.txt.gz"
# The Bioconductor annotation of the array; its featureSet table types every transcript cluster.
ANNOTATION = "pd.hugene.1.0.st.v1_3.14.1.tar.gz"
ANNOTATION_DB = "pd.hugene.1.0.st.v1/inst/extdata/pd.hugene.1.0.st.v1.sqlite"
# Cluster types that measure the lab's reagents and the background, not the patient: control->affx (spike-ins) and
# control->bgp->antigenomic (background probes).
CONTROL_TYPES = ("control->affx", "control->bgp->antigenomic")
# Sample fields of the series matrix kept next to the expression values (the others are the same on every array).
SAMPLE_FIELDS = {
    "!Sample_title": "title",
    "!Sample_geo_accession": "gsm",
}
N_PATIENTS = 639  # "298 patients from AEGIS 1 and 341 from AEGIS 2" (the series summary)


class AegisBronchialAirwayLungCancer(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "Does a current or former smoker with a suspicious lung lesion have lung cancer, judging from gene "
            "activity in cells brushed from the airway during bronchoscopy?"
        ),
        use_case=(
            "When bronchoscopy for a suspicious lesion does not give a diagnosis, the pulmonologist uses an airway "
            "gene-expression classifier to choose between further invasive tests, such as a surgical biopsy, and a "
            "more conservative diagnostic approach (Silvestri et al. 2015)."
        ),
        row=(
            "One patient of the AEGIS-1 and AEGIS-2 trials (639 current or former smokers who had a bronchoscopy for "
            "suspected lung cancer at 28 centres), with one microarray of the cells brushed from the mainstem bronchus."
        ),
        predicted=(
            "Whether the patient was diagnosed with lung cancer (76% were), from the bronchoscopy or within 12 months "
            "of follow-up."
        ),
        known=(
            "The patient's sex and the activity of about 33,000 transcript clusters (gene-level microarray values) in "
            "the brushed cells; not the age, smoking history or lesion size the clinician also has."
        ),
        split="Random patients, standing for new patients examined the same way.",
        changes=(
            "We keep one array per patient (the first of the 2 to 4 arrays of 23 patients), drop the 102 control "
            "clusters of spike-ins and background, and drop 554 transcript clusters that repeat another cluster's "
            "probes exactly."
        ),
        fit="approximate",
        fit_reason=(
            "The cells are brushed before the bronchoscopy's result, but the rows are all bronchoscopy patients, "
            "while the test is used when the bronchoscopy gives no diagnosis; that subgroup cannot be cut (its result "
            "is not released), so the score is on a broader, likely more cancer-heavy population. Age, which the "
            "source's classifier used, is not in the release."
        ),
    )

    # Dataset
    unique_name = "aegis_bronchial_airway_lung_cancer"
    year = "2015"
    domain = "medical & healthcare"
    source = "GOV Website"
    source_url = "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE66499"
    license = "Public Domain"
    download_description = """
        The series matrix of GEO GSE66499 (the RMA values and the sample characteristics):

        mkdir -p local-data-warehouse/aegis_bronchial_airway_lung_cancer && wget -P local-data-warehouse/aegis_bronchial_airway_lung_cancer https://ftp.ncbi.nlm.nih.gov/geo/series/GSE66nnn/GSE66499/matrix/GSE66499_series_matrix.txt.gz

        The array annotation pd.hugene.1.0.st.v1 3.14.1 (Bioconductor), for the type of each transcript cluster:

        wget -P local-data-warehouse/aegis_bronchial_airway_lung_cancer https://bioconductor.org/packages/release/data/annotation/src/contrib/pd.hugene.1.0.st.v1_3.14.1.tar.gz

        The CEL files (GSE66499_RAW.tar, 2.8 GB, https://ftp.ncbi.nlm.nih.gov/geo/series/GSE66nnn/GSE66499/suppl/GSE66499_RAW.tar) are not read by the definition; the curation checks used their scan dates and raw intensities.
    """
    bibtex = """
        @article{silvestri2015bronchial,
          title={A Bronchial Genomic Classifier for the Diagnostic Evaluation of Lung Cancer},
          author={Silvestri, Gerard A. and Vachani, Anil and Whitney, Duncan and Elashoff, Michael and Porta Smith, Kate and Ferguson, J. Scott and Parsons, Ed and Mitra, Nandita and Brody, Jerome and Lenburg, Marc E. and Spira, Avrum and {AEGIS Study Team}},
          journal={New England Journal of Medicine},
          volume={373},
          number={3},
          pages={243--251},
          year={2015},
          doi={10.1056/NEJMoa1504601}
        }
    """
    curation_comments = """
        We start with the series matrix of GEO GSE66499 (Veracyte, public 2015-05-17): 680 arrays (Affymetrix Human Gene 1.0 ST, GPL6244) of 639 patients, the "RMA normalization" values of 33,297 transcript clusters, and the sample characteristics tissue, gender and cancer_yes_no.

        - The prediction point is the bronchoscopy: the airway cells are brushed from the mainstem bronchus during the procedure, before its result and before the final diagnosis, which came from the bronchoscopy or from up to 12 months of follow-up (Whitney et al. 2015). Every feature (the expression values and the sex) exists then.
        - Patients and arrays: the titles (A1_0001_2 is AEGIS-1, patient 0001, second array) give 639 patients, AEGIS-1 298 (220 cancer, 78 benign) and AEGIS-2 341 (267, 74), as the series summary states. 23 patients have 2 to 4 arrays (41 extra arrays), 22 of them benign and all in AEGIS-1; their label and sex agree across arrays. The series describes "680 CEL files from 639 BEC specimens", and the CEL headers date them: in every such patient the scan date rises with the array number, the first arrays scanned from 2010-11-23 to 2011-06-21, the later ones from 2011-02-24 to 2011-08-19, beside other patients' first arrays: later hybridisations of the same specimen. They correlate 0.984 to 0.996 with each other (any two arrays of different patients: 0.953 to 0.990, 1st to 99th percentile). We keep each patient's first array (LEAK-17, USE-11): the test is run once per specimen, and all 680 rows would have given 22 benign patients two to four training rows each.
        - The target is `cancer_yes_no` (Y or N) as words, `lung_cancer` Yes (487, 76.2%) or No (152). The diagnosis comes from the bronchoscopy or from follow-up until a final diagnosis or for 12 months (Whitney et al. 2015); the 639 patients are those who "met the criteria for inclusion" (Silvestri et al. 2015, abstract).
        - Inputs: the 33,297 transcript clusters of the series matrix (the core-level transcript clusters of GPL6244, named by their IDs) and `sex` (the `gender` characteristic, Male or Female). The recorded sex agrees with the level of the ten most variable chromosome-Y clusters on all 680 arrays (male minimum 7.5, female maximum 6.0, log2), a check that the arrays and the records belong together. `tissue` (BEC specimen on every array) is dropped. The trial (AEGIS-1 or AEGIS-2) is not kept: a new patient belongs to neither, and the two trials ran over overlapping years (ClinicalTrials.gov: AEGIS-1, NCT01309087, January 2009 to May 2013; AEGIS-2, NCT00746759, February 2010 to February 2015).
        - 102 control clusters leave by their type in pd.hugene.1.0.st.v1 (3.14.1): the 57 `control->affx` clusters (bacterial, poly-A and ERCC spike-ins, reagents added in the lab) and the 45 `control->bgp->antigenomic` background clusters. They measure the processing run, not the patient: the spike-ins alone score ROC AUC 0.621 (L2 logistic regression, 3 repeats of 3-fold CV), as much as the scan day alone (0.62), the background clusters 0.487. The normgene clusters (exon and intron controls) stay: they measure the sample.
        - 227 clusters have no type in pd.hugene.1.0.st.v1 (no featureSet entry with a type): their meaning is unknown; they stay.
        - 557 transcript clusters measure exactly the probes of another cluster (974 clusters in 417 sets of identical probes, 129 of the dropped copies on chromosome 6, 46 on chromosome Y), so their values are identical: the first of each set by ID is kept. 3 of the 557 copies are control clusters, already dropped above; 554 leave here and 32,641 clusters ship.
        - Not in the release: age, smoking history (pack-years, current or former), lesion size and the bronchoscopy's own result. The source's classifier combines age with gene-expression estimates of sex, smoking status and pack-years (Whitney et al. 2015), so a model here works without the one clinical input it used.
        - The values: the series matrix holds RMA values, quantile-normalised and summarised over many arrays at once (LEAK-30). From the CEL files and the Bioconductor annotation pd.hugene.1.0.st.v1 (3.14.1), a numpy re-implementation of oligo's RMA reproduces them per cohort (mean absolute difference 0.036 log2 for AEGIS-2, 0.090 for AEGIS-1) far better than over all 680 arrays (0.143 for both), and worse when AEGIS-1 is split by its processing years (0.112 and 0.146): the values match RMA run once per cohort, AEGIS-1 perhaps together with arrays not deposited (the looser fit). The cohorts' value distributions differ (median 7.29 against 7.07 log2).
        - Potential leak, kept on purpose: RMA over all arrays of a cohort puts each test array into the quantile reference and the probe effects every training value is computed with (LEAK-30). Measured on the 639 kept arrays (2 repeats of 3-fold CV, our RMA per cohort): fitting RMA on the training arrays alone, then normalising each test array to the training reference and summarising it with the training probe effects, changes the values by 0.02 to 0.03 log2 on average and the ROC AUC by -0.0006 for L2 logistic regression (SD 0.0012 over 6 folds, higher with the leak on 2 of 6) and +0.0018 for LightGBM (SD 0.021, 3 of 6). Kept as the source published it (Lennart, 2026-10-19, on the sibling: a scaling over all rows is no strong leak). The CEL files would allow a rebuild, but a per-sample one needs a reference frozen outside the data (fRMA's vectors for this array, an R package), and the measured effect is nil; revisit if a frozen reference becomes easy to use from Python.
        - Scan batches (from the CEL headers) are unbalanced in the label: the share benign of the kept arrays runs from 6% (2011-06-21, 18 arrays) to 65% (2010-12-06, 26 arrays), and the scan day alone, target-encoded on the training side, scores ROC AUC 0.62 out of fold. The models do not use it: on the same out-of-fold predictions their ROC AUC within scan days is as high as over all patients (L2 logistic regression 0.768 against 0.748, LightGBM 0.674 against 0.671; three repeats of 3-fold CV). The expression values tell some scan days apart (one day against the rest: ROC AUC 0.67 to 0.91). Keeping each patient's last array instead gives the same picture (scan day alone 0.56).
        - The split is random over patients (the default 3-fold protocol), not AEGIS-1 for training and AEGIS-2 for testing: the source trained its classifier on 299 other AEGIS-1 patients not in this deposit (Whitney et al. 2015) and validated it on both cohorts, and two cohorts that ran over overlapping years are two groups, a transfer test between two processing runs rather than the use case's new patients (splits.md, few groups). The transfer costs little: trained on AEGIS-1 and tested on AEGIS-2, L2 logistic regression scores ROC AUC 0.769 (0.799 on the AEGIS-2 patients of random folds), the other way 0.723 (0.691 on AEGIS-1's); LightGBM 0.638 and 0.652 (0.737 and 0.590).
        - Metric: ROC AUC is the criterion the source's classifier was built by: Whitney et al. 2015 assess accuracy by the AUC, estimate it by cross-validation in training and keep the gene clusters that give "the best AUC" (Statistical methods, Results); Silvestri et al. 2015 report it for the locked classifier in each cohort (0.78 in AEGIS-1, 0.74 in AEGIS-2), beside sensitivity, specificity and negative predictive value at the classifier's own cut-off (the abstract; the NEJM full text was not read).
        - No missing values, no duplicate rows. GEO places no restrictions on the use of its data (NCBI's disclaimer); the licence is written as Public Domain, as for `lung_cancer_epithelial_genexp`.
        - The patients come from 28 centres, a plausible hidden group, but the release has no centre id, so a split by centre cannot be tested; its nearest proxies (scan day, scan month, cohort) show no drop in score (random 0.728, by scan day 0.734, by scan month 0.705, L2 logistic regression).
        - Sibling: `lung_cancer_epithelial_genexp` (GSE4115, Spira et al. 2007) is the same task of the same research line on 187 other patients and another array (PROV-4: another cohort, its own dataset).
    """

    # Task
    target = "lung_cancer"
    problem_type = "binary_classification"
    metric = Metric.source(
        "roc_auc",
        original="ROC curve AUC",
        reference="https://pmc.ncbi.nlm.nih.gov/articles/PMC4434538/ (Whitney et al. 2015, Statistical methods)",
        definition="ROC AUC of the predicted probability of a lung cancer diagnosis, over all patients of a test fold",
    )
    splits_comment = """
        The default protocol, random patients (20 repeats of 3 folds), one array per patient. The source validated its
        locked classifier, trained on 299 other AEGIS-1 patients, on each cohort separately; the two cohorts are not
        used as training and test here, as they are concurrent trials processed in two runs, not a stand-in for new
        patients (curation notes).
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        # The series matrix: the sample fields (lines starting with "!Sample_") and the expression table, one column
        # per array, one row per transcript cluster.
        fields: dict[str, list[str]] = {}
        with gzip.open(raw_dir / SERIES_MATRIX, "rt") as f:
            for line in f:
                if line.startswith("!series_matrix_table_begin"):
                    break
                if not line.startswith("!Sample_"):
                    continue
                key, *values = line.rstrip("\n").split("\t")
                values = [v.strip('"') for v in values]
                if key == "!Sample_characteristics_ch1":
                    # "tissue: ...", "gender: ...", "cancer_yes_no: ..." on three lines of the same key
                    name = values[0].split(": ", 1)[0]
                    assert all(v.startswith(name + ": ") for v in values), name
                    fields[name] = [v.split(": ", 1)[1] for v in values]
                elif key in SAMPLE_FIELDS:
                    fields[SAMPLE_FIELDS[key]] = values
            expr = pd.read_csv(f, sep="\t", index_col=0, comment="!", dtype={"ID_REF": str})
        expr.index = expr.index.astype(str)
        meta = pd.DataFrame(fields)
        assert list(expr.columns) == list(meta["gsm"]), "arrays out of order"
        # The control clusters (CONTROL_TYPES) leave here, by their type in the array annotation.
        expr = expr.drop(index=[i for i in _control_clusters(raw_dir) if i in expr.index])
        values = expr.T.reset_index(drop=True)
        values.columns.name = None
        return pd.concat([meta, values], axis=1)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # 1. The cohort, the patient and the array from the title: A1_0001_2 is AEGIS-1, patient 0001, second array;
        #    a title without a suffix is a patient's only array.
        parts = df["title"].str.extract(r"^(A[12])_(\d{4})(?:_(\d))?$")
        assert parts[[0, 1]].notna().all().all(), "unparsed title"
        df["patient"] = parts[0] + "_" + parts[1]
        df["array"] = parts[2].fillna("1").astype(int)
        assert (df.groupby("patient")[["cancer_yes_no", "gender"]].nunique() == 1).all().all()

        # 2. One array per patient, the first: 23 patients (22 benign, all in AEGIS-1) have 2 to 4 arrays, the
        #    later ones hybridised on later dates; the use case makes one prediction per specimen (LEAK-17, USE-11).
        df = df[df["array"] == 1]
        assert df["patient"].is_unique
        assert len(df) == N_PATIENTS

        # 3. The target in words (CLEAN-25): "Yes" is a lung cancer diagnosis.
        df = decode(df, {"cancer_yes_no": {"Y": "Yes", "N": "No"}})
        df = df.rename(columns={"cancer_yes_no": self.target, "gender": "sex"})

        # 4. Identifiers and the constant tissue leave; the trial (AEGIS-1 or AEGIS-2, in the title) is not kept.
        df = drop_columns(df, ["title", "gsm", "patient", "array", "tissue"])

        # 5. Transcript clusters whose probes are exactly another cluster's carry identical values: keep the first.
        clusters = [c for c in df.columns if c.isdigit()]
        copies = df[clusters].T.duplicated(keep="first")
        return drop_columns(df, list(copies[copies].index))

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["sex"])


def _control_clusters(raw_dir: Path) -> list[str]:
    """The IDs of the transcript clusters whose type in the array annotation is one of CONTROL_TYPES."""
    with tempfile.TemporaryDirectory() as tmp:
        with tarfile.open(raw_dir / ANNOTATION) as tar:
            member = tar.getmember(ANNOTATION_DB)
            member.name = "annotation.sqlite"
            tar.extract(member, tmp, filter="data")
        con = sqlite3.connect(Path(tmp) / "annotation.sqlite")
        try:
            rows = con.execute(
                "SELECT DISTINCT f.transcript_cluster_id FROM featureSet f JOIN type_dict t ON f.type = t.type "
                "WHERE t.type_id IN (?, ?)",
                CONTROL_TYPES,
            ).fetchall()
        finally:
            con.close()
    ids = sorted(str(r[0]) for r in rows)
    assert len(ids) == 102, len(ids)  # 57 control->affx, 45 control->bgp->antigenomic
    return ids
