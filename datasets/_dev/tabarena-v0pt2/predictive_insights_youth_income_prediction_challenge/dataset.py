"""Original Youth employment task with documented source timing limitations."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, Metric, TaskSummary


class PredictiveInsightsYouthIncomePredictionChallenge(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a young South African be employed at the source's follow-up survey?",
        use_case=(
            "Youth-employment analysts estimate employment outcomes from baseline survey answers to inform support "
            "planning. This predicts observed outcomes; it does not estimate the benefit of an intervention."
        ),
        row=(
            "One labelled respondent in the original South African competition release: 4,020 source rows, "
            "4,017 after removing three exact copies apart from the identifier. The survey programme is unnamed."
        ),
        predicted=(
            "Target 1 means employed and 0 unemployed at follow-up. Both original starter notebooks describe "
            "one year after baseline; the date field's role and individual outcome dates are not authenticated."
        ),
        known=(
            "Source-described baseline labour-market status, geography and province, educational "
            "qualifications and subject-result bands, sex and citizenship flags, birth year and month, plus the survey date and redundant source round. "
            "Tenure is excluded because its missingness is conditionally outcome-linked."
        ),
        split=(
            "Repeated stratified random respondent folds, an approximation forced from a temporal task. "
            "The four survey waves do not establish three mature future windows with at least half the rows "
            "for training. Future-cohort performance is not established."
        ),
        changes=(
            "Remove the person identifier, tenure, and three exact source "
            "copies. Keep baseline-employed respondents, survey date/round context and all other source values/missing answers."
        ),
        fit="approximate",
        fit_reason=(
            "The source calls the inputs baseline and the target a one-year outcome. Yet survey dates extend "
            "to March 2023 in a June 2023 archive; those dates cannot all be baseline dates of mature one-year "
            "labels. Their role, covariate timing and follow-up selection need clarification. Date and round "
            "are retained as source context by curator decision; IID is an approximation."
        ),
    )

    unique_name = "predictive_insights_youth_income_prediction_challenge"
    year = "2023"
    domain = "social science"
    source = "Zindi"
    source_url = "https://zindi.world/competitions/predictive-insights-youth-income-prediction-challenge"
    license = (
        "Zindi competition terms: data remains property of Zindi and the competition host; "
        "redistribution to nonparticipants is prohibited. No separate open-data licence is supplied."
    )
    data_tags = ("Spatial", "ForcedIIDFromTemporal")
    download_description = """
        Sign in to Zindi at
        https://zindi.world/competitions/predictive-insights-youth-income-prediction-challenge/data
        and download the original all-files archive, subject to its terms. The curator supplied
        predictive-insights-youth-income-prediction-challenge20230621-4520-15eqo8v.zip
        (SHA256 975995c9e87e82ead4389eea9409388bfb29b398534e6396ebb92e7bd6200832).
        Extract into local-data-warehouse/predictive_insights_youth_income_prediction_challenge/.
        This definition reads only Train.csv
        (SHA256 83fe90d3ca0835ea0d274109d2c00eb71d9681fd41bf70127d687328d7dc4e4c).
        Test.csv has no labels and is retained for overlap/source checks, never treated as labelled data.
        Preserve both starter notebooks and the release manifest as original source documentation.
    """
    bibtex = r"""
        @misc{PredictiveInsights2023YouthEmployment,
          author = {{Predictive Insights and Zindi}},
          title = {Predictive Insights Youth Income Prediction Challenge},
          year = {2023},
          howpublished = {\url{https://zindi.world/competitions/predictive-insights-youth-income-prediction-challenge}},
          note = {Original June 2023 release; binary employment outcome despite the challenge name}
        }
    """
    curation_comments = """
        - Prediction point (USE-1, USE-3): the baseline interview, before follow-up employment is known, as the
          original competition and both original starter notebooks describe. The realised timing is not verified.
        - Target (USE-5, USE-8): retain original 0/1 employment labels, including respondents employed at baseline;
          no income target, initially-unemployed filter, nonresponse recoding or causal interpretation is introduced.
          All 4,020 source labels are present, but attrition, nonresponse handling and individual follow-up dates
          are not documented by the released files. Complete labels do not prove complete ascertainment.
        - Chronology: the original archive manifest was generated on 2023-06-21. Survey_date spans 2021-08-11 to
          2023-03-27, with 1,977 rows in the newest wave. Survey_date cannot be baseline for every mature one-year
          outcome in this release. It could mean follow-up, or another description could be wrong; neither is
          established. The related 2026 host hackathon's six-month account is not proof of the original horizon.
        - Calendar context (CLEAN-3, CLEAN-14, CLEAN-22; USE-3): Myunghwan requested retaining Survey_date
          as potentially useful seasonal context on 2026-10-27 and allowed redundant Round to remain.
          Survey_date is stored losslessly as a datetime; Round is a category and a deterministic function of
          date in this release, adding no information conditional on the full date. No target date, age,
          month/year feature or date backshift is fabricated. Calendar extraction belongs to the learner.
          Source-described baseline availability is retained as an explicit approximation, not proven by
          model scores. Wave association alone is not leakage evidence. Drop Person_id, a masked release ID.
        - Baseline status (USE-6): retain the labour-market status the release describes as baseline. Its
          association with later employment is legitimate if it is a baseline value; timing remains unresolved.
        - Tenure (LEAK-10; LEAK-38 conditional-test clause): independently replicated outcome-linked missingness
          within source Round and Status. In round 3 self-employment, all 10 negative labels lack tenure and all
          28 positives have it; among wage-employed respondents, 69 of 77 negatives lack it and no positive does
          (25 positives). The difference persists within geography, sex and matric strata. This is a measured
          fill-pattern concern, not proof of the actual collection time. Drop the entire tenure field; do not
          retain its missingness indicator or invent a wave-specific repair. On the earlier seventeen-input proposal's nine folds,
          fixed LightGBM ROC AUC fell from 0.7844 to 0.7370 without tenure. That difference mixes legitimate
          duration information and suspect fill; it is not an estimated amount of leakage. Removing tenure
          resolves this feature exposure only; source horizon and other mutable-feature timing stay unresolved.
        - Copies (LEAK-16, LEAK-19): three source rows are exact repeats of all non-ID fields, target included;
          remove later copies in source order. No full-source feature vector has conflicting labels. Coincident
          profiles after removing tenure remain: matching coarse answers do not establish a shared person.
          All source person IDs are unique and the official train/test person-ID sets are disjoint; masked IDs
          alone cannot authenticate longitudinal identity.
        - Cleaning (CLEAN-2, CLEAN-9, CLEAN-10, CLEAN-14): leave missing answers missing; preserve school-quintile
          code 0 because the source does not define it as missing. Treat all finite-response fields, 0/1 flags,
          birth month and mark bands as categories; birth year stays numeric. Every released non-ID
          string is a finite response or date, so no free text is discarded. Do not execute starter-model
          imputation, dummy encoding, subject-score engineering or citizenship filtering.
        - Retained coincident profiles (LEAK-18, LEAK-20): restoring date/round leaves seven extra identical
          labelled rows and three feature-profile groups with both labels. Source rows differed in the
          excluded tenure field after three complete non-ID source copies were removed. Myunghwan accepted
          natural profile coincidence on 2026-10-27 conditional on no demonstrated prediction simplification.
          Current equal-profile held-out AUC is 0.7933 versus ordinary-fold 0.7939, supplying no material
          simplification evidence in the tested model; different partitions do not estimate causal inflation.
          Equal-feature-profile grouping is a diagnostic, not an authenticated person key. Reopen retention
          if identity evidence or a measured prediction benefit establishes a duplication problem.
        - Recording quality (CLEAN-10, CLEAN-11): 1,125 retained birth months are January, including 857 with
          birth year 2000; the January share varies by survey wave. A default or anonymisation convention is
          possible, not established. Preserve these valid-looking values and school-quintile code 0 until
          a source rule supports another meaning; do not manufacture a birth day or restrict the age range.
        - CC (2026-10-27, Myunghwan): authorized completion of add-dataset for this reviewed eighteen-input task.
          Myunghwan explicitly approved final scientific inclusion on 2026-10-28. Keep Survey_date as datetime, allow redundant categorical Round,
          exclude Person_id/Tenure, retain coincident profiles under the saved conditional decision, and
          preserve source ROC AUC and repeated stratified random evaluation. Approximate fit, unresolved
          source chronology/ascertainment and round-four distribution shift remain documented limitations.
          This instruction is not final inclusion or authority for a container build, source commit or publication.
        - Access: original competition data is private under Zindi's redistribution terms; raw files and any
          derivative data remain in the local warehouse. Licensing is not a scientific rejection reason (EV-4).
    """
    # CC (2026-10-27, Myunghwan): keep coincident profiles if there is no evidence they simplify prediction.
    accepted_check_warnings = {
        "dataset_duplicate_rows": (
            "Myunghwan accepted natural profile coincidence on 2026-10-27 conditional on no demonstrated "
            "prediction simplification. After three complete source-copy removals, retaining date/round and "
            "excluding tenure leaves seven extra identical labelled profiles and three feature groups with "
            "both outcomes among 4,017 respondents. Source records differed in tenure. Preserve the natural "
            "coincidence/ambiguity under LEAK-18/20; equal-profile held-out sensitivity is a diagnostic, not "
            "an authenticated identity split. Reopen if source linkage or new performance evidence establishes "
            "a duplication benefit. Earlier sixteen-input scores are historical, not current qualification."
        ),
    }
    target = "Target"
    problem_type = "binary_classification"
    metric = Metric.source(
        "roc_auc",
        original="Area Under the Curve (ROC AUC)",
        reference=source_url,
    )
    splits_comment = """
        Repeated stratified random respondent folds follow the v2 recommendation for 4,017 rows.
        ForcedIIDFromTemporal (SPLIT-8): four survey waves and unresolved baseline/outcome dates cannot establish
        three meaningful future windows each trained on at least 50% of the data (SPLIT-14). We do not backshift
        Survey_date or invent calendar mappings. This approximation tests other respondents from represented
        cohorts, not a model deployed into future cohorts. Calendar holdouts are diagnostic sensitivity tests;
        they cannot establish a mature-label deployment protocol without authenticated observation dates.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "Train.csv", dtype={"Person_id": "string"})

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # Remove copies before metadata drops, so coarse profiles are not mistaken for repeated people.
        fields = [c for c in raw.columns if c != "Person_id"]
        df = raw.drop_duplicates(subset=fields, keep="first")
        return df.drop(columns=["Person_id", "Tenure"]).reset_index(drop=True)

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            datetime={"Survey_date": "%Y-%m-%d"},
            categorical=[
                "Round",
                "Status",
                "Geography",
                "Province",
                "Matric",
                "Degree",
                "Diploma",
                "Schoolquintile",
                "Math",
                "Mathlit",
                "Additional_lang",
                "Home_lang",
                "Science",
                "Female",
                "Sa_citizen",
                "Birthmonth",
            ],
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        cohorts = raw.groupby("Round", sort=True).agg(
            rows=("Target", "size"),
            positive=("Target", "sum"),
            first_survey_date=("Survey_date", "min"),
            last_survey_date=("Survey_date", "max"),
        )
        cohorts["positive_share"] = cohorts["positive"] / cohorts["rows"]
        return [
            Decision(
                "Survey chronology remains unresolved",
                "The archive predates one year after the newest survey dates. These dates are not authenticated "
                "baseline dates; do not construct a prospective protocol by assuming they are.",
                cohorts,
            ),
            Decision(
                "Exact source copies removed without merging coarse profiles",
                "Use every non-ID source field, including the date and target, to identify exact copies.",
                pd.DataFrame(
                    {"source_rows": [len(raw)], "retained_rows": [len(df)], "removed_copies": [len(raw) - len(df)]}
                ),
            ),
        ]
