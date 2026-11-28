"""Curated dataset definition for `lung_cancer_epithelial_genexp` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from data_foundry.definition import (
    AbstractCuratedDataset,
    FeatureTypes,
    Grouping,
    Metric,
    Source,
    TaskSummary,
    TimeBasis,
)

# GEO characteristic -> column: the clinical findings known at the bronchoscopy (Beane et al. 2008's clinical model);
# never bronch_status, subjective_assessment, biomarker_score, cancer_status or sample_id
CLINICAL = {
    "age": "age",
    "gender": "sex",
    "race": "race",
    "smoking_status": "smoking_status",
    "packyears": "pack_years",
    "presence_of_hemopytsis": "haemoptysis",
    "presence_of_lymphadenopathy": "lymphadenopathy",
    "mass_size_greater_than_3cm": "mass_over_3cm",
}


class LungCancerEpithelialGenexp(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "Does a smoker with suspected lung cancer have it, judging from gene activity in cells brushed from the "
            "airway?"
        ),
        use_case=(
            "During bronchoscopy for suspected lung cancer, a pulmonologist brushes cells from the normal-looking "
            "airway and uses their gene expression to judge whether the patient has cancer and needs further invasive"
            " tests (Spira et al. 2007)."
        ),
        row=(
            "One smoker undergoing bronchoscopy for suspected lung cancer (163 patients of the extended GEO release "
            "GSE4115 whose arrays passed the authors' quality control)."
        ),
        predicted=(
            "Whether the patient was finally diagnosed with lung cancer (48% were); the time to the final diagnosis "
            "is not stated."
        ),
        known=(
            "The measured activity of about 22,000 gene probes (Affymetrix microarrays) in the brushed airway cells, "
            "and 8 clinical findings known before the brushing: age, sex, race, smoking status, pack-years, coughing "
            "up blood, and from the chest CT a mass over 3 cm and enlarged lymph nodes."
        ),
        split=(
            "Grouped by scan period: the arrays fall into six periods of their scan order (about half a year of scans "
            "each), and a test period is never in training, so a model meets arrays of a period it has not seen."
        ),
        changes=(
            "We use the extended release of 192 patients, not the paper's 129, and drop the 5 without a diagnosis "
            "and the 24 arrays that failed the authors' quality control. The split holds out whole scan periods "
            "(sixths of the sample number, which follows the scan order). The 8 clinical findings join the "
            "expression; the bronchoscopy's own result and the study's later risk rating stay out."
        ),
        fit="direct",
        fit_reason=(
            "The sample is taken at the bronchoscopy, before the diagnosis is known, and the clinical findings are "
            "there at that point too; a held-out patient is a new one. The clinical findings predict better than the "
            "expression, which adds a little to them. The task is small, with 163 patients and far more genes than "
            "patients."
        ),
    )

    # Dataset
    unique_name = "lung_cancer_epithelial_genexp"
    domain = "medical & healthcare"
    sources = (
        Source(
            role="publication",
            platform="GOV Website",
            url="https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE4115",
            license="Public Domain",
            year="2006",
            bibtex="""
                @article{spira2007airway,
                  title={Airway epithelial gene expression in the diagnostic evaluation of smokers with suspect lung cancer},
                  author={Spira, Avrum and Beane, Jennifer E and Shah, Vishal and Steiling, Katrina and Liu, Gang and Schembri, Frank and Gilman, Sean and Dumas, Yves-Martine and Calner, Paul and Sebastiani, Paola and others},
                  journal={Nature medicine},
                  volume={13},
                  number={3},
                  pages={361--366},
                  year={2007},
                  publisher={Nature Publishing Group US New York}
                }
            """,
        ),
    )
    download_description = """
        We download the original gene expression data from the GEO records.

        mkdir -p local-data-warehouse/lung_cancer_epithelial_genexp/ && wget -P local-data-warehouse/lung_cancer_epithelial_genexp/ https://ftp.ncbi.nlm.nih.gov/geo/series/GSE4nnn/GSE4115/matrix/GSE4115_series_matrix.txt.gz && gzip -d local-data-warehouse/lung_cancer_epithelial_genexp/GSE4115_series_matrix.txt.gz
    """
    curation_comments = """
        - We start with an extended dataset of 192 patients. The original reference uses 129 samples as "Individuals without final diagnoses as of May 2005 were excluded from this primary dataset". We remove 5 samples without a clear label ("Smoker with suspect lung cancer Sample"), yielding a dataset of 187 samples.
        - Quality control (2026-11-13, Andrej): we drop the 24 arrays for which GEO gives no clinical characteristics, leaving 163 (78 cancer). The series says "23 of these samples were then filtered for quality control reasons", and these 24 correlate worse with the median profile (median 0.93 against 0.98), so they are most likely the arrays the authors removed; GEO gives no list. They were 19 cancer and 5 not (79%, against 48% among the rest; Fisher exact p = 0.004), all from the submission of 2006-01-29, so a failed array mostly meant cancer, and with the clinical findings in, trees read their empty fields as cancer. Kept as test-only rows they would cost every model 0.05 to 0.13 ROC AUC, scored as no cancer as a block, and a clinic never reads an array that failed its quality control.
        - We use "Sample_title" from the metadata as labels for the prediction task.
        - Scan period (2026-11-12, Andrej): each title carries a sample number (56 to 328), which is the scan order. The CEL files of 31 arrays survive in linked GEO copies (28 in GSE19027), and their scan dates, April 2003 to January 2006, follow the number at Spearman 0.997. We cut the rank of the number among the 163 kept arrays into six periods of 27 or 28 arrays (`scan_period`, the split's group) and do not ship the number itself.
        - Clinical findings (2026-11-13, Andrej): the 8 findings GEO gives for 163 arrays join the expression: `age`, `sex`, `race`, `smoking_status`, `pack_years`, `haemoptysis`, `lymphadenopathy` (hilar or mediastinal nodes over 1 cm on the chest CT) and `mass_over_3cm` (on the chest CT), the variables of the clinical model of Beane et al. 2008 (Cancer Prevention Research 1(1):56-64, https://doi.org/10.1158/1940-6207.CAPR-08-0011). They are known at the bronchoscopy, and none is the diagnosis, which came from pathology or follow-up. On the 163 arrays and the grouped splits (logistic regression, ROC AUC): clinical only 0.819, expression only 0.744, both 0.834 (expression adds +0.015, SE 0.006; +0.036 on the 118 non-diagnostic bronchoscopies); untuned LightGBM 0.800, 0.742 and 0.767. All 8 are complete for the 163 kept arrays.
        - Left out on purpose: `bronch_status`, whether this bronchoscopy's cytopathology gave the diagnosis (40 of 78 cancers, 5 of 85 others), which arrives after the brushing and is the diagnosis for half the cancers; `subjective_assessment`, a risk rating made for the study afterwards by three pulmonologists blinded to the outcome (ROC AUC 0.897 alone), which no clinic records; `biomarker_score`, the 80-gene predictor fitted on the labels; `cancer_status` and `sample_id`, the label and the title's number.
        - Potential leak, kept on purpose: GSE4115 holds RMA values, which quantile-normalise all arrays processed together, so a sample's values depend on the others (per-sample medians vary by an SD of only 0.053 log2 over 187 samples); there are no CEL files to redo it per sample. Kept (Lennart, 2026-10-19): a scaling over all rows is no strong leak, and data often come this way; revisit if raw arrays appear.
    """
    split_leaf = "L-FORCED.periods"
    time_basis = TimeBasis(
        "ForcedGroupedFromTemporal",
        """
        the arrays were scanned over almost three years in the order of their sample number. Arrays of one period share a scan signature (within each class the expression tells the later from the earlier arrays at ROC AUC 0.90 to 0.98), and the cancer share moves from 4% to 70% between periods, so random folds let a model read a period's cancer share: held-out periods score 0.05 to 0.14 ROC AUC lower than random folds at equal training size (on all 187 arrays, before the quality-control drop; on the 163 kept ones older-to-newer halves score 0.05 (LR) and 0.10 (LightGBM) below random halves). Forward windows cannot be scored with 163 arrays (three windows of 27; on the 187 arrays the oldest of three windows of 31 ranked below chance whatever trained), so whole periods are held out, and training includes later periods. The relation itself did not drift measurably: 56 training arrays near the test period or far from it score the same (LR +0.003, LightGBM +0.008). Not tested: patients scanned after every training array, as a forward window would test.
        """,
    )

    # Task
    accepted_check_warnings = {
        "groups_test_groups_few": (
            "Six scan periods by design (2026-11-12, Andrej): the 163 arrays cannot form forward windows of a "
            "usable size, and periods of about half a year of scans keep each period's scan signature on one "
            "side; each test fold holds 54 or 55 arrays. Two periods per test fold is what six periods allow; "
            "each fold still scores 54 or 55 arrays one by one. The signal carries across held-out periods: on "
            "the 163 arrays with the clinical findings, untuned LightGBM (ROC AUC 0.668 to 0.917, mean 0.793) and "
            "logistic regression (0.650 to 0.905, mean 0.769) beat chance on all 14 test pairs that occur (run of "
            "2026-11-13). The repeats reuse the same pairs, so the spread across repeats is descriptive."
        ),
    }
    target = "DiagnosedCancer"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason=(
            "Spira et al. 2007 report accuracy with sensitivity and specificity of the 80-gene predictor "
            "(83/80/84%); the clinical claim rests on sensitivity and NPV, no single metric or threshold. "
            "roc_auc is the binary fallback."
        ),
    )

    # Splits: whole scan periods held out
    grouping = Grouping(
        on="scan_period",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a scan period: a sixth of the arrays in the order of the sample number in their GEO titles
            (27 or 28 arrays), which follows the scan dates (April 2003 to January 2006, from the CEL headers of 31
            arrays in linked GEO copies). The arrays of one period share a scan signature and the cancer share differs
            between periods (4% to 70%), so a random split lets a model read the period's share. A pulmonologist
            brushes a new patient's airway after every array a model was trained on, and the release cannot form
            forward windows of a usable size, so whole periods are held out (forced from temporal). The source's
            authors recruited the patients from January 2003 to April 2005 at four medical centres and validated on a
            set collected prospectively from June 2005 to January 2006 at five (Spira et al. 2007; Beane et al. 2008).
            Each array is one prediction, made from its own expression.
        """,
    )
    splits_comment = """
        Stratified grouped 3-fold cross-validation over the six scan periods with 20 repeats: each test fold holds two
        whole periods (54 or 55 arrays), and no period sits on both sides. The periods by sample number among the 163
        arrays that passed quality control: 56-98 (28 arrays, scanned April-May 2003, 4% cancer), 99-139 (27, October
        2003, 41%), 140-177 (27, March-April 2004, 59%), 181-226 (27, July-December 2004, 70%), 228-273 (27,
        February-March 2005, 63%) and 274-328 (27, May 2005 to January 2006, 52%; most of the prospective five-centre
        set); the scan months are those of the dated arrays in each range. Six periods allow at most 15 distinct test
        pairs (14 occur over the 20 repeats), so the repeats recur and fold scores spread wider than under random folds
        (fold SD about 0.09 ROC AUC against 0.05). Grouping replaced random patients on 2026-11-12 (Andrej):
        random folds scored 0.05 to 0.14 ROC AUC higher than held-out periods at equal training size
        (curation notes).
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "GSE4115_series_matrix.txt", sep="\t", comment="!", index_col=0).T
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # read labels
        with open(self.raw_dir / "GSE4115_series_matrix.txt") as f:
            for line in f:
                if line.startswith("!Sample_title"):
                    labels = [t.strip('"') for t in line.strip().split("\t")[1:]]
                    break
        df["DiagnosedCancer"] = pd.Series(labels, index=df.index)

        def resolve_label(label):
            if label.startswith("Smoker diagnosed with cancer Sample"):
                return "Yes"
            if label.startswith("Smoker NOT diagnosed with cancer Sample"):
                return "No"
            if label.startswith("Smoker with suspect lung cancer Sample"):
                return np.nan
            raise ValueError(f"Unknown label: {label}")

        sample_number = df["DiagnosedCancer"].str.extract(r"Sample (\d+)$", expand=False).astype(int)
        df["DiagnosedCancer"] = df["DiagnosedCancer"].apply(resolve_label)
        # the 8 clinical findings known at the bronchoscopy
        chars = {}
        with open(self.raw_dir / "GSE4115_series_matrix.txt") as f:
            for line in f:
                if line.startswith("!Sample_characteristics_ch1"):
                    cells = [c.strip('"') for c in line.rstrip("\n").split("\t")[1:]]
                    field = next((c.split(": ", 1)[0] for c in cells if ": " in c), None)
                    if field in CLINICAL:
                        chars[CLINICAL[field]] = [c.split(": ", 1)[1] if ": " in c else np.nan for c in cells]
        clin = pd.DataFrame(chars, index=raw.index)
        # remove suspected cancer samples, and the 24 arrays GEO gives no clinical data for (the quality-control
        # failures: "23 of these samples were then filtered for quality control reasons"; 19 of them cancer)
        keep = df["DiagnosedCancer"].notna() & clin.notna().all(axis=1)
        df, clin, sample_number = df[keep].copy(), clin[keep].copy(), sample_number[keep]
        # scan period: the sixth of the sample number's rank among the kept arrays (the number is the scan order)
        rank = sample_number.rank(method="first").astype(int).to_numpy() - 1
        df["scan_period"] = pd.Series((rank * 6) // len(df) + 1, index=df.index).map("period_{}".format)
        for col in ("age", "pack_years"):
            clin[col] = pd.to_numeric(clin[col])
        clin["sex"] = clin["sex"].map({"M": "male", "F": "female"})
        clin["race"] = clin["race"].map({"CAU": "Caucasian", "OTHER": "other"})
        for col in ("haemoptysis", "lymphadenopathy", "mass_over_3cm"):
            clin[col] = clin[col].map({"0": "no", "1": "yes"})
        return pd.concat([df, clin[list(CLINICAL.values())]], axis=1)

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=(
                "scan_period",
                "sex",
                "race",
                "smoking_status",
                "haemoptysis",
                "lymphadenopathy",
                "mass_over_3cm",
            ),
        )
