"""Curated dataset definition for `eucalyptus` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import hashlib
import io
from pathlib import Path

import arff
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, Metric, TaskSummary


class Eucalyptus(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="What is a measured eucalyptus trial record's soil-conservation Utility category?",
        use_case=(
            "For example, a forestry assessor considers a suggested Utility category when assigning a "
            "soil-conservation rating to a eucalyptus trial record, using its already recorded site, species, "
            "growth and condition measurements."
        ),
        row=(
            "One released site/replicate/species/seedlot trial record from the North Island. The source describes "
            "replicated plantings, but does not establish the exact biological aggregation of each exported row."
        ),
        predicted=(
            "The released Utility label (none, low, average, good or best), from a binned 0-5 "
            "soil-conservation rating; exact row-level conversion remains unverified."
        ),
        known="Already recorded trial/site context, species and seedlot identity, growth, survival and condition.",
        split="Random records from the represented trial population; sites and planting material can recur.",
        changes=(
            "Myunghwan (2026-10-26) selected measured records: remove only rows jointly missing Vig, "
            "Ins_res, Stem_Fm, Crown_Fm and Brnch_Fm. This leaves 667 of 736 records and removes Mor, Wen "
            "and the 1986 cohort; all 19 predictors and all five Utility classes remain. Three species codes are corrected from ma to mn as the source prescribes, and one impossible diameter becomes missing."
        ),
        fit="approximate",
        fit_reason=(
            "This implements the accepted assessment-time task. The preparation report specifies utility cut "
            "points; original rating construction, missing-rating conversion, exact row aggregation and "
            "prediction-time chronology remain unresolved."
        ),
    )

    unique_name = "eucalyptus"
    year = "Unverified"
    domain = "environmental science & climate"
    source = "Other"
    source_url = "https://researchcommons.waikato.ac.nz/entities/publication/3541f4de-ee18-496a-aa5d-1233afbf66d4"
    license = None
    data_tags = ("Spatial",)
    accepted_check_warnings = {
        "meta_license_unknown": (
            "Curator accepted the unknown original-data license as a documented metadata gap on 2026-10-21. "
            "Keep license=None; mirror software and repository paper-use terms do not establish a data license."
        ),
        "meta_dataset_year": (
            "Curator accepted the unverified first public release year as a documented metadata gap on 2026-10-21. "
            "Keep year='Unverified'; the related 1991 paper and 1996 preparation report do not prove release date."
        ),
    }
    download_description = """
        We use the category_encoders mirror of the agricultural eucalyptus ARFF, whose header attributes
        the data to Bruce Bulloch. Thomson and McQueen's 1996 Waikato preparation report, Section 4
        (printed pp. 17-29; PDF pp. 20-32), documents the forestry data and utility categorization.
        Its five class counts match this release; exact row-by-row correspondence to historical files,
        first public release and original-data license remain unverified. The mirror's software
        license does not establish rights to the original data.

        mkdir -p local-data-warehouse/eucalyptus
        curl --fail --location 'https://raw.githubusercontent.com/scikit-learn-contrib/category_encoders/78f3165cfdd8e6761e96eaa465e5e661bde9a990/examples/benchmarking_large/datasets/arff-datasets-master/agridata/eucalyptus.arff' -o local-data-warehouse/eucalyptus/eucalyptus.arff
        echo 'a8cd5b3206b4c57964678cd8f9b77d4e4f1b87474b8a34ccd94cfb0ec4bb2e02  local-data-warehouse/eucalyptus/eucalyptus.arff' | sha256sum --check

        With DATA_FOUNDRY_WAREHOUSE set, put eucalyptus/eucalyptus.arff under that warehouse instead.
    """
    bibtex = """
        @techreport{ThomsonMcQueen1996Agricultural,
          author = {Thomson, Kirsten and McQueen, Robert J.},
          title = {Machine learning applied to fourteen agricultural datasets},
          institution = {University of Waikato},
          number = {96/18},
          year = {1996},
          month = {September},
          url = {https://researchcommons.waikato.ac.nz/entities/publication/3541f4de-ee18-496a-aa5d-1233afbf66d4},
          note = {Section 4, pp. 17--29 (PDF pp. 20--32), visually read from the scanned report;
                  exact first data release and original-data license unverified}
        }
    """
    curation_comments = """
        We start with the 736-row, hash-pinned category_encoders eucalyptus ARFF.

        - Prediction point: assessment time, using already recorded site, species, growth and condition to
          suggest the released soil-conservation Utility class. The parent forestry study describes joint
          measurements, not a verified ordering before a separately pending rating. This is the curator's
          accepted approximate task, not planting-time selection or new-location prediction.
        - Myunghwan (2026-10-26) selected measured records: drop only rows jointly missing Vig, Ins_res,
          Stem_Fm, Crown_Fm and Brnch_Fm, before splitting and without reading the target. This removes 69
          of 736 rows, leaving 667: none 111, low 107, average 130, good 214, best 105. Mor/Wen and the 1986
          cohort disappear; the sample no longer represents the complete release. Keep all 19 predictors.
        - Keep none as a meaningful class. Thomson and McQueen (1996), section 4, printed pp.20-21, gives
          the five New_Utility cut points. Original numeric-rating conversion, missing-rating handling and
          the exact 5.00 boundary remain unverified. Bulk = DBH * DBH * Ht is a separate target, not a Utility formula.
        - Apply the preparation report's explicit species correction ma to mn (printed p.22) to three
          retained records. Set the one DBH value 42085 cm to missing: a diameter of 420.85 m is impossible,
          and no verified replacement is available. Retain its row; do not guess a decimal correction.
          All other retained cell values are unchanged. Raw bytes and removed-row identities remain archived.
        - Keep Latitude categorical as approved, along with Abbrev, Rep, Locality, Map_Ref, Sp and PMCno.
          The report treats latitude as enumerated and rejects numeric seedlot ordering. The only 82__32
          latitude occurs in the removed Wen rows; this is a selection consequence, not a geographic repair.
          Rep=22 remains unresolved. Year is planting context, not an annotation timestamp.
        - Retain 20 repeats of three stratified random folds, seed 4267, within represented measured trials.
          Sites, replicates and planting material can recur. Recompute the deterministic frame and folds after
          source-cell repairs; fresh qualification uses the regenerated memberships, not historical predictions.
        - Fresh train-only fixed-model diagnostics on 30 of 60 repaired-frame folds give log loss 0.896
          logistic, 0.974 forest and 1.462 LightGBM versus prior 1.567; logistic/forest win 30/30, LightGBM 21/30.
          No task flags. All 417 fresh pipelines and 447 prediction arrays were independently audited. These
          are adapted untuned probes, not benchmark rankings: training-only imputation/scaling/one-hot inputs
          for all families, with internal single-feature selection. Old feature-version scores are historical.
        - Diagnostic permutation AUC is 0.499; no label shortcut was demonstrated. No exact predictor copies
          cross the 60 folds; one pair of near-identical replicates crosses 28 folds. Seed-0 Abbrev-held-out
          LightGBM loss is 2.177 versus matched random 1.670, reinforcing the represented-trial limitation.
          Diagnostic feature-removal choices use test AUC and are descriptive, not an unbiased removal policy.
          Secondary AUC cannot substitute for log loss; three auxiliary group tests have undefined AUC.
        - Use multiclass log loss as the fallback: the preparation report, printed pp.21-25, reports error rates
          and tree sizes without fixed operational costs. No label transformation, class merge, weighting or
          extra row filter applies. Original annotation chronology, biological row aggregation and exact
          correspondence to historical plots remain unverified.
        - Keep the accepted unknown first-release year and original-data licence qualifications. The 1991
          forestry paper and 1996 preparation report are evidence of the research, not proof of data-release date
          or an original-data licence. Mirror software terms do not supply that licence.
    """

    target = "Utility"
    problem_type = "multiclass_classification"
    metric = Metric.fallback(
        reason=(
            "Thomson and McQueen (1996), Section 4, printed pp. 21-25 (PDF pp. 24-28), "
            "reports classification error and tree size, without fixed operational costs or a decision threshold. "
            "The parent forestry study (Bulloch, Method pp. 13-14) defines subjective usefulness ratings, "
            "not a probability-scoring criterion. Use multiclass log loss under MET-6/8. "
            "Preparation report: https://researchcommons.waikato.ac.nz/bitstreams/"
            "b676db41-cdc8-4afb-a000-db3bd56bff1c/download"
        )
    )
    splits_comment = """
        Recommended stratified random three-fold cross-validation, with the base class's repeat count and seeds
        (20 repeats for 667 measured records). Test records are additional observations from the represented trial population.
        Sites, replicates, species and seedlots can recur across train and test; dependencies among trials remain
        a limitation. This is an assessment-time task, not evaluation on entirely new locations or future plantings.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        content = (raw_dir / "eucalyptus.arff").read_bytes()
        assert hashlib.sha256(content).hexdigest() == (
            "a8cd5b3206b4c57964678cd8f9b77d4e4f1b87474b8a34ccd94cfb0ec4bb2e02"
        ), "Raw ARFF differs from the pinned release."
        parsed = arff.load(io.StringIO(content.decode("utf-8")))
        return pd.DataFrame(parsed["data"], columns=[attribute[0] for attribute in parsed["attributes"]])

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # Curator selection avoids benchmarking a recording convention; labels never select rows.
        subjective = ["Vig", "Ins_res", "Stem_Fm", "Crown_Fm", "Brnch_Fm"]
        df = raw.loc[~raw[subjective].isna().all(axis=1)].copy()
        # The preparation report explicitly identifies ma as an erroneous species code.
        df["Sp"] = df["Sp"].replace({"ma": "mn"})
        # Preserve the record without inventing the true value of an impossible diameter.
        df.loc[df["DBH"].eq(42085.0), "DBH"] = float("nan")
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=("Abbrev", "Rep", "Locality", "Map_Ref", "Latitude", "Sp", "PMCno"))

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        subjective = ["Vig", "Ins_res", "Stem_Fm", "Crown_Fm", "Brnch_Fm"]
        missing = raw[subjective].isna().all(axis=1)
        labels = ["none", "low", "average", "good", "best"]
        counts = pd.DataFrame(
            {
                "all_records": raw[self.target].value_counts().reindex(labels, fill_value=0),
                "retained_records": df[self.target].value_counts().reindex(labels, fill_value=0),
                "removed_joint_missing": raw.loc[missing, self.target].value_counts().reindex(labels, fill_value=0),
            }
        )
        return [
            Decision(
                title="Remove only the curator-selected joint-missing records; retain all five classes",
                why=(
                    "Myunghwan (2026-10-26) selected measured records to avoid predicting a recording convention. "
                    "The five-predictor all-missing rule removes 69 records before splitting; no label selects rows. "
                    "Keep none as a meaningful class. Original annotation/recording chronology remains unverified."
                ),
                evidence=counts,
            ),
            Decision(
                title="Retain trial identities and categorical Latitude",
                why=(
                    "Codes describe the represented trial population. Rep and PMCno are identifiers; Latitude is "
                    "the released category. Random splits evaluate additional records within that population."
                ),
                evidence=df[["Abbrev", "Rep", "Map_Ref", "Latitude", "Sp", "PMCno"]]
                .nunique()
                .rename("observed_nonmissing_categories"),
            ),
        ]
