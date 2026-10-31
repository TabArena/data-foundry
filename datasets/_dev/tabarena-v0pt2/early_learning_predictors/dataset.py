"""Curated dataset definition for `early_learning_predictors` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    FeatureTypes,
    Grouping,
    Metric,
    TaskSummary,
    drop_columns,
    set_missing,
)

# The ordinal scales, lowest level first, from the source's codebook (curation notes; the README lists
# them). An open-ended level holds everything beyond it.
ORDINAL_LEVELS = {
    "child_years_in_programme": ["1st year in the programme", "2nd year in programme", "3rd year in programme"],
    "pqa_curriculum_literacy": [
        "Inadequate: Few appropriate language activities. E.g. Practitioner rarely reads",
        "Basic: Some of the following language/literacy activities – daily story, some ap",
        "Good: Daily story with active child participation and discussion. E.g. children",
    ],
    "pqa_curriculum_ncf": [
        "Inadequate: No evidence that programme supports NCF aims.",
        "Basic: Learning programme focuses on some of the ELDAs and is mostly development",
        "Good: Learning programme used covers all the ELDAs and activities are developmen",
    ],
    "pqa_curriculum_numeracy": [
        "Inadequate: Few or no appropriate maths activities, staff do not show children h",
        "Basic: Some practitioner initiated and directed maths activities including numbe",
        "Good: Frequent number songs, rhymes, games. Children encouraged to count objects",
    ],
    "pqa_environment_accessible": [
        "Inadequate: Few or no materials are accessible to children.",
        "Basic: Some materials are easily accessible for children.",
        "Good: All materials are laid out so that children can easily access them.",
    ],
    "pqa_environment_appropriate": [
        "Inadequate: Many materials are not appropriate for the developmental level and i",
        "Basic: Most materials match the developmental level and interests of children 4",
        "Good: Materials provide for a range of developmental levels and interests includ",
    ],
    "pqa_environment_areas": [
        "Inadequate: There are no or fewer than 3 organised learning areas.",
        "Basic: Three learning areas set out for children to play in (alone or with other",
        "Good: There are 4 or more learning areas arranged so children can use them, quie",
    ],
    "pqa_environment_open": [
        "Inadequate: No open ended materials.",
        "Basic: At least 1 example of open ended materials in each of 2 learning areas.",
        "Good: At least 2 examples of open ended materials in each of 3 learning areas.",
    ],
    "pqa_environment_outdoor": [
        "Inadequate: Few or no outdoor equipment/opportunities.",
        "Basic: Some outdoor equipment to promote different kinds of movement.",
        "Good: A variety of small and large equipment to promote different kinds of movem",
    ],
    "pqa_environment_variety": [
        "Inadequate: Insufficient materials in any or all areas. E.g. children have to wa",
        "Basic: Some materials for all learning areas. E.g. children don’t have to wait b",
        "Good: Enough and variety of materials in all learning areas - more than 2 activi",
    ],
    "pqa_relationships_acknowledge": [
        "Inadequate: Staff do not use encouragement to acknowledge children’s efforts or",
        "Basic: Staff sometimes use encouragement (at least 2 instances observed with 2 d",
        "Good: Staff regularly use encouragement to acknowledge individual children’s eff",
    ],
    "pqa_relationships_discipline": [
        "Inadequate: No positive discipline observed or expectations may not be age appropriate.",
        "Basic: No harsh methods used, control maintained, expectations age appropriate.",
        "Good: Effective use of non-punitive methods, staff apply rules consistently, children supported to solve conflicts for themselves, express how they are feeling.",
    ],
    "pqa_relationships_peers": [
        "Inadequate: Children are discouraged from interacting (e.g. not allowed to choos",
        "Basic: Peer interaction encouraged (e.g. free choice of who to play with), negat",
        "Good: Staff help children develop good social behaviours, provide activities tha",
    ],
    "pqa_relationships_staff": [
        "Inadequate: Staff are not responsive to or involved with children (ignore or jus",
        "Basic: Friendly atmosphere, some positive interactions and response to individua",
        "Good: Frequent positive interaction, warm contact, relaxed and pleasant atmosphe",
    ],
    "pqa_teaching_choice": [
        "Inadequate: Staff direct how children use materials and carry out activities (e.",
        "Basic: Children make at least 2 choices independent of practitioner direction ab",
        "Good: Children make 3 or more choices during playtime (independent of practition",
    ],
    "pqa_teaching_engagement": [
        "Inadequate: Staff do not engage to support and extend children’s learning. Inter",
        "Basic: Staff engage with one or two children to extend their learning using one",
        "Good: Staff regularly engage to extend children’s learning using a variety of te",
    ],
    "pqa_teaching_participation": [
        "Inadequate: In large group activities staff do not ask children to offer ideas o",
        "Basic: Children sometimes contribute or participate at own developmental levels",
        "Good: Children contribute their own ideas and participate at own developmental l",
    ],
    "pqa_teaching_questions": [
        "Inadequate: No open ended questions to extend children’s thinking (only one word",
        "Basic: Some questions to encourage children to reflect on an activity or idea. E",
        "Good: Many questions to encourage children to reflect on actions and ideas in mu",
    ],
    "pqa_teaching_support": [
        "Inadequate: Staff do not support children to do things for themselves or encoura",
        "Basic: Practitioner sometimes supports children to do things for themselves and",
        "Good: Practitioner regularly supports children to do things for themselves and t",
    ],
    "quintile": [1.0, 2.0, 3.0, 4.0, 5.0],
    "gr_ecd": [0.0, 1.0, 2.0, 3.0, 4.0],
    "obs_booknumber": [1.0, 2.0, 3.0, 4.0, 5.0],  # open-ended
    "obs_condition_equipment": [1.0, 2.0, 3.0, 4.0],
    "obs_infrastructure": [1.0, 2.0, 3.0, 4.0],
    "obs_material_display": [0.0, 1.0, 2.0, 3.0],
    "plan": [0.0, 2.0, 1.0],
    "pqa_assessment_observation": [0.0, 1.0, 2.0],
    "pqa_assessment_systematic": [0.0, 1.0, 2.0],
    "pqa_curriculum_balance": [0.0, 1.0, 2.0],
    "pqa_curriculum_plan": [0.0, 1.0, 2.0],
    "pra_adequacy_materials": [1.0, 2.0, 3.0, 4.0, 5.0],
    "pra_class_space_2": [1.0, 2.0, 3.0, 4.0, 5.0],
    "pra_cotlands_support": [3.0, 4.0, 5.0],
    "pra_cotlands_visits": [0.0, 1.0, 4.0, 11.0],  # open-ended
    "pra_education": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
    "pra_engaged": [1.0, 2.0, 3.0],
    "pra_free_play": [0.0, 1.0, 2.0, 3.0, 5.0],  # open-ended
    "pra_free_play_outdoor": [0.0, 1.0, 2.0, 3.0, 4.0],
    "pra_grade": [0.0, 8.0, 9.0, 10.0, 11.0, 12.0],
    "pra_letcee_support_cluster": [1.0, 3.0, 4.0, 5.0],
    "pra_letcee_support_coach": [1.0, 3.0, 4.0],
    "pra_motivate_mentoring": [1.0, 2.0, 3.0, 4.0],
    "pra_motivate_recognition": [1.0, 2.0, 3.0, 4.0],
    "pra_motivate_support": [1.0, 2.0, 3.0, 4.0],
    "pra_ntataise_attendance": [5.0, 7.0, 8.0, 9.0, 11.0],  # open-ended
    "pra_ntataise_support": [2.0, 3.0, 4.0, 5.0],
    "pra_ntataise_visits": [2.0, 3.0, 4.0, 5.0, 7.0, 8.0, 11.0],  # open-ended
    "pra_satisfaction_support": [1.0, 2.0, 3.0, 4.0, 5.0],
    "pra_tuc_support": [1.0, 3.0, 4.0, 5.0],
    "pra_tuc_visits": [1.0, 2.0, 4.0, 5.0, 7.0, 10.0, 11.0],  # open-ended
    "pri_covid_staff_salaries": [0.0, 1.0, 2.0],
    "pri_education": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
    "pri_fees_paid_proportion": [0.0, 1.0, 2.0, 3.0, 4.0],
    "pri_food_parents_afternoon": [0.0, 1.0, 2.0],
    "pri_food_parents_breakfast": [0.0, 1.0, 2.0],
    "pri_food_parents_lunch": [0.0, 1.0, 2.0],
    "pri_food_parents_morning": [0.0, 1.0, 2.0],
    "pri_parents_activities": [0.0, 1.0, 2.0, 3.0],
    "pri_parents_contact": [0.0, 1.0, 2.0, 3.0],
    "pri_parents_frequency": [0.0, 4.0, 3.0, 2.0, 1.0],
    "pri_registered_dsd": [4.0, 3.0, 2.0, 1.0],
    "pri_registered_partial": [4.0, 3.0, 2.0, 1.0],
    "pri_registered_programme": [4.0, 3.0, 2.0, 1.0],
    "pri_same_language": [4.0, 3.0, 2.0, 1.0],
    "pri_separate": [0.0, 1.0, 2.0],
    "pri_staff_employed": [4.0, 3.0, 2.0, 1.0],
    "pri_support_dbe": [0.0, 1.0, 2.0, 3.0, 4.0],  # open-ended
    "pri_support_dsd": [0.0, 1.0, 2.0, 3.0, 4.0],  # open-ended
    "pri_support_frequency": [1.0, 2.0, 3.0, 4.0],
    "pri_support_municipality": [0.0, 1.0, 2.0, 3.0, 4.0],  # open-ended
    "pri_support_ngo": [0.0, 1.0, 2.0, 3.0, 4.0],  # open-ended
    "rating": [0.0, 1.0, 2.0, 3.0],
    "ses_cat": [1.0, 2.0, 3.0, 4.0, 5.0],
    "ses_proxy": [1.0, 2.0, 3.0, 4.0, 5.0],
    "teacher_emotional_appropriate": [0.0, 1.0, 2.0],
    "teacher_emotional_confidence": [0.0, 1.0, 2.0],
    "teacher_emotional_independent": [0.0, 1.0, 2.0],
    "teacher_emotional_selfstarter": [0.0, 1.0, 2.0],
    "teacher_emotional_understand": [0.0, 1.0, 2.0],
    "teacher_familiarity_with_child": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0],
    "teacher_selfcare_total": [1.0, 2.0, 3.0, 4.0],
    "teacher_social_assistance": [1.0, 2.0, 3.0, 4.0],
    "teacher_social_cooperate": [1.0, 2.0, 3.0, 4.0],
    "teacher_social_ideas": [1.0, 2.0, 3.0, 4.0],
    "teacher_social_initiative": [1.0, 2.0, 3.0, 4.0],
    "teacher_social_nonaggressive": [1.0, 2.0, 3.0, 4.0],
    "teacher_social_peers": [1.0, 2.0, 3.0, 4.0],
    "teacher_emotional_adjust": [0.0, 1.0, 2.0],
    "child_stunted": ["Severely stunted", "Moderately stunted", "Normal"],
}


class EarlyLearningPredictors(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "What score will a preschool child at a facility not seen before reach on a standard early learning test?"
        ),
        use_case=(
            "The source asks which features of early learning programmes predict better outcomes, a study looking "
            "back. As a prediction, for example, a programme funder estimates the scores of children at a new "
            "facility from facility, staff and family surveys, to find children at risk without a full assessment."
        ),
        row=(
            "One child aged 50 to 69 months assessed at an early learning facility in South Africa, 2016 to 2023 "
            "(DataDrive2030 merged surveys, 18,874 children); a few children per facility."
        ),
        predicted=(
            "The child's total score on the Early Learning Outcomes Measure: 23 items over five areas (gross and fine"
            " motor development, numeracy, cognition and executive function, literacy and language)."
        ),
        known=(
            "739 features: the child's age, sex, birth date, grant, stunting, languages and years in the programme; "
            "the facility's registration, staff, building, equipment and observed practice; teacher and parent "
            "questionnaires. Many are missing for whole survey rounds."
        ),
        split=(
            "Whole facilities are held out, so the test data stands for facilities never surveyed; the source's "
            "competition split children at random."
        ),
        changes=(
            "We drop the parts and other versions of the score, another child assessment, the home-learning survey "
            "(mostly missing), the survey year, the assessor's id and the timers of the data collection, and split by "
            "facility."
        ),
        fit="approximate",
        fit_reason=(
            "The source's question is explanatory. As a forecast, some surveys were made after the assessment, and the "
            "rows mix survey rounds with different questions."
        ),
    )

    # Dataset
    unique_name = "early_learning_predictors"
    year = "2024"
    domain = "education"
    source = "Other"
    source_url = "https://www.datafirst.uct.ac.za/dataportal/index.php/catalog/962"
    license = "Creative Commons CC-BY (Attribution-only) License"
    download_description = r"""
        No automatic download possible!

        mkdir -p local-data-warehouse/early_learning_predictors
        Go to https://www.datafirst.uct.ac.za/dataportal/index.php/catalog/962/get-microdata., create an account, download the data files and move them to local-data-warehouse/early_learning_predictors. Next, run:

        unzip local-data-warehouse/early_learning_predictors/elom-tb5i-2016-2023-v1-csv.zip -d local-data-warehouse/early_learning_predictors \
        && mv local-data-warehouse/early_learning_predictors/elom-tb5i-2016-2023-v1-csv/* local-data-warehouse/early_learning_predictors \
        && rm local-data-warehouse/early_learning_predictors/elom-tb5i-2016-2023-v1-csv.zip \
        && rm -r local-data-warehouse/early_learning_predictors/elom-tb5i-2016-2023-v1-csv
    """
    bibtex = """
        @dataset{DataDrive2030_2024_elom_thrivebyfive,
            author       = {{DataDrive2030}},
            title        = {ELOM and Thrive by Five Index 2016--2023, Merged Data},
            version      = {1},
            year         = {2024},
            address      = {Cape Town},
            publisher    = {DataDrive2030},
            note         = {[dataset]. Producer: DataDrive2030; Distributor: DataFirst},
            doi          = {10.25828/WG0D-Y909},
            url          = {https://doi.org/10.25828/WG0D-Y909}
        }
    """
    curation_comments = """
        - The data is collected for predictive analytics to find major drivers of early learning outcomes. Nevertheless, predictive performance matters and the data could also be used for identifying at risk children.
        - The data consists of different subsets that were collected at different times. Sometimes the target was even collected before the predictors. Although the data is collected over time, the task is cross-sectional. Therefore, we drop most date features, after checking whether relevant information was already extracted.
        - We use a grouped split based on id_facility to reflect a potential deployment scenario where we want to predict for a new facility. Note that a date (year) is available, but the data collection is conducted per facility so we don't use a time-based split.
        - The target score ELOM is continuous, but decisions are made based on cutoffs to identify at-risk children. We keep the task as regression, to maintain the most information.
        - Note: The data consists of different age groups, for which the ELOM score is computed differently. While under these circumstances a multi-class target using the given cutoffs might be a valid choice, the age is given  as a feature and therefore, we assume that a model can be expected to learn patterns for subgroups.
        - The data is collected from several sources, including direct assessments, teacher questionnaires, parent surveys and facility data. The data is collected by different enumerators across different facilities. The target is from a separate tool (see further information below).
        - We drop all columns which are components or alternative versions of the target, to avoid leakage.
        - We drop all samples with a missing target.
        - Due to most samples having missing values, we drop all "HOME LEARNING ENVIRONMENT DATA" features. This mostly aligns with the Zindi challenge, except that the features hle_ind, quintile_used, and ses_proxy were kept. We keep the latter two, because they are not missing for all samples and are derived from other; not-HLE features.
        - We drop all features with 100% missing values and one unique value.
        - Cleaning of 2026-10-30 (CLEAN-5, CLEAN-14): `child_stunted`'s "Normal HAZ" (2016-2022) and "Normal" (2023) are
          one level spelled two ways, merged as "Normal"; `pra_dob` is a date (`%d%b%Y`); `pri_calc_time_open` and
          `pri_calc_time_close` ("HH:MM") are present only where the hour and minute columns are and equal to them, so
          they are dropped, as is `certificate_registration_npo`, a copy of `certificate_register`; 26 columns of the
          enumerators' free text (the "other" answers and the explanations of flagged measurements) are strings.
          `language_match` holds 0, 1 and 12 explanations in place of a 0 or 1 (16 rows); it stays a category, as the
          explanations do not say which answer they replace.
        - `.a` and `.b` are Stata's extended missing values, exported to the CSV as text (2,388 and 29 cells after the
          target filter, only in the 2020-2022 rounds). They occur only where the question was asked (all 40 `.a` of
          the DSD subsidy amount are programmes that receive it), while a skipped question is blank, so they are
          unanswered questions; the source does not say which code is which. They become missing values. The 46
          columns that held them are counts, rand amounts per month, a year and a timer in minutes, `numeric` in the
          source's codebook: they are numbers, no longer categories (CLEAN-10, CLEAN-14; issue #36). The timer,
          `teacher_duration`, is dropped (below).
        - We drop all indicator columns.
        - We drop some repeated columns, such as age_group_label.
        - Because all features could generally be available at prediction time, even if would not be ideal effort-wise, we keep all features that don't leak the target or are otherwise problematic.
        - We transform all date columns to datetime.
        - Additional description of the target: The ELOM 4 & 5 Years Assessment Tool measures whether preschool children are on track for their age in key areas of development. It is a standardised tool that measures performance across five key developmental domains for children aged 50 to 59 months and 60 to 69 months. The scoring assesses a child in 23 items, across five domains, namely: gross motor development, fine motor development, emergent numeracy and mathematics, cognition and executive functioning, and emergent literacy and language. These five domains form part of the direct assessment.
        - Note: We keep some features that were not in the zindi challenge, such as the teacher and parent questionnaires, because they are potentially predictive and could be available at prediction time. Moreover, some columns present in the zindi challenge (like latitude and longitude) are not available.
        - Note: The data consists of a few subsets with partially distinct features collected. This might not represent a real task, but we don't know for sure, so we keep all samples.
        - The assessor's id (`id_enumerator`) is a control variable of the data collection rather than a factor that
          should be used for prediction, so we drop it with the other ids, although it is predictive and explains
          noise in the target.
        - We drop `teacher_duration`, the minutes the teacher's socio-emotional rating form was open (DataFirst's
          codebook: "Teacher SEF duration in minutes"): a timer of the data collection, like the three `duration_elom`
          timers dropped above, not a property of the child, the teacher or the facility. It exists only in the
          2020-2022 rounds (26% of the children); 39% of its values are 0 (93% in the 2020 round, 50% in 2021, 28% in
          2022) and 1.4% exceed a day, up to 29 days. Its Spearman correlation with the score is -0.06, and what signal
          it has follows the round (the 0-minute forms, mostly of 2020, score 50.1 against 48.1 overall), which we drop
          as `data_year` (2026-10-30, Lennart).
        - Note: There are strong patterns of missingness within the data, due to different uses of various tools and measurements across subgroups
        - Anomaly: Many missing values
        - Feature families by column name (from the v1 exploration, counted 2026-10-22 on the cleaned data, 745 columns; a column can match more than one): pri 258, obs 161, pra 149, count_ 74, pqa 35, child 25, teacher 22. 576 columns are also in the Zindi train file, 136 more are pra/pqa/pri/obs columns not in it, and 33 others are new (among them the target, child_total_elom; Zindi calls it target). 102 Zindi columns are not in our data, among them latitude, longitude, the ward, municipality and province ids and the date columns. 80% of the cells are missing and every row has a missing value.
        - Anomaly: This is a highly underspecified task, leaving a lot of data cleaning to the user/model.
        - Ordinal scales (2026-10-30, the curator's marks of 2026-10-31, CLEAN-14): 89 columns are ordered categories in
          the order of the source's codebook (`ORDINAL_LEVELS`); 69 of them were shipped as numbers; codes that mean
          unknown are missing (CLEAN-10).
    """

    # Task
    target = "child_total_elom"
    problem_type = "regression"
    metric = Metric.source(
        "rmse",
        original="Root Mean Squared Error (Zindi error_metric root_mean_squared_error)",
        reference=(
            "https://zindi.africa/competitions/datadrive2030-early-learning-predictors-challenge (API field error_metric)"
        ),
        definition="RMSE of the child's total ELOM score.",
    )
    grouping = Grouping(
        on="id_facility",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is an early learning facility; its rows are the children assessed there with the ELOM tool, a few per facility. The question is "which features of an early learning programme predict better learning outcomes for children" (DataDrive2030, Zindi), and the programme features are facility-level, so a random split would let a model recognise facilities. Each child is one prediction, for a facility not seen in training; the Zindi split was random by child.
        """,
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "elom-tb5i-2016-2023-v1.csv", low_memory=False)
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.loc[~df["child_total_elom"].isna()]
        df["child_stunted"] = df["child_stunted"].replace({"Normal HAZ": "Normal"})  # 2016-2022 and 2023 spellings
        # Stata's extended missing values `.a` and `.b`, exported as text, made 46 numeric columns text (curation notes)
        coded = [col for col in df.columns if df[col].isin([".a", ".b"]).any()]
        df[coded] = df[coded].replace({".a": None, ".b": None}).apply(pd.to_numeric)
        leaky_cols = [col for col in df.columns if "result" in col]
        leaky_cols += [col for col in df.columns if "domain" in col]
        leaky_cols += [col for col in df.columns if "child_score" in col]
        leaky_cols += [col for col in df.columns if "child_total_elom_w2" in col]
        leaky_cols += [col for col in df.columns if "_w2" in col]
        leaky_cols += [
            col for col in df.columns if "_sef" in col
        ]  # other test, but also a time-consuming child assessment like ELOM
        leaky_cols += [
            "child_total_elom_cuts",
            "duration_elom",
            "duration_elom_sef",
            "duration_elom_hle",
            "child_sample_wgt",
        ]
        leaky_cols += ["id_cluster_original"]  # leaks with school-based split
        leaky_cols += [
            "child_observe_total",
            "child_observe_attentive",
            "child_observe_concentrated",
            "child_observe_diligent",
            "child_observe_interested",
        ]  # Unsure but likely leak the target
        leaky_cols += ["data_year", "language_assessment"]  # Also collected with the target
        df = df.drop(columns=leaky_cols)
        indicator_cols = [
            "child_id",
            "id_enumerator",
            "id_enumerator_hle",
            "id_prov_best",
            "audit_ind",
            "id_ward_best",
            "child_conditions",
            "calc_test_hour",
            "teacher_gender",
            "count_aftercare",
            "saspri_datazone_quintile",
            "id_dc_best",
            "id_enumerator_hle",
            "id_facility_hle",
            "id_mn_best",
            "id_prov_best",
            "id_team",
            "id_ward_best",
            "data_source",
            "sef_ind",
            "pra_ind",
        ]
        df = df.drop(columns=indicator_cols)
        hle_cols = [col for col in df.columns if "hle_" in col or "_hle" in col]
        df = df.drop(columns=hle_cols)
        df = df.loc[:, df.isna().mean() < 1]
        df = df.loc[:, df.nunique() > 1]
        df = drop_columns(
            df,
            [
                # dates
                "child_date",
                "child_enrolment_date",
                "obs_date",
                "pqa_date",
                "pra_date",
                "pri_date",
                "teacher_date",
                # repeats `child_age_group`
                "age_group_label",
                # "HH:MM" text, present only where the hour and minute columns are, and equal to them
                "pri_calc_time_open",
                "pri_calc_time_close",
                # a copy of `certificate_register` in every row
                "certificate_registration_npo",
                # how long the teacher's rating form was open: a timer of the data collection (curation notes)
                "teacher_duration",
            ],
        )
        # codes outside a scale that mean unknown, and states outside it placed as missing (CLEAN-10,
        # CLEAN-14): don't know, refused, not asked, other
        df = set_missing(
            df,
            {
                "child_years_in_programme": ["Don't know"],
                "gr_ecd": [5.0],
                "pra_education": [97.0],
                "pra_grade": [14.0],
                "pra_satisfaction_support": [0.0],
                "pri_parents_activities": [97.0],
                "pri_parents_contact": [97.0],
                "pri_parents_frequency": [97.0],
                "pri_registered_dsd": [5.0],
                "pri_registered_partial": [5.0],
                "pri_registered_programme": [5.0],
                "pri_support_frequency": [97.0],
            },
        )
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            ordinal=ORDINAL_LEVELS,
            categorical=(
                # answer codes stored as numbers (building, water and energy source, owner, language, job; point 4)
                "gr_1_tt",
                "grade_r",
                "obs_building",
                "obs_cooking_census",
                "obs_heating_census",
                "obs_lighting_census",
                "obs_water",
                "pra_class_language",
                "pra_job",
                "pra_previous",
                "pra_shape",
                "pri_bank",
                "pri_facilities",
                "pri_kitchen",
                "pri_land",
                "pri_location",
                "pri_meal_prep",
                "programme",
                "child_gender",
                "child_age_group",
                "child_attends",
                "child_grant",
                "child_has_sibling",
                "child_stunted",
                "child_languages",
                "child_spectacles",
                "child_years_in_programme",
                "dc_best",
                "language_match",
                "mn_best",
                "phase_natemis",
                "pre_covid",
                "prov_best",
                "certificate_register",
                "certificate_registration_partial",
                "certificate_registration_program",
                "facility_type",
                "health",
                "library_access",
                "obs_access",
                "obs_access_disability_0",
                "obs_access_disability_1",
                "obs_access_disability_2",
                "obs_access_disability_3",
                "obs_access_disability_4",
                "obs_access_disability_5",
                "obs_access_disability_6",
                "obs_accessible",
                "obs_area",
                "obs_area_0",
                "obs_area_1",
                "obs_area_2",
                "obs_area_3",
                "obs_area_4",
                "obs_area_5",
                "obs_area_6",
                "obs_area_7",
                "obs_area_8",
                "obs_books",
                "obs_books_age",
                "obs_cooking_1",
                "obs_cooking_2",
                "obs_cooking_3",
                "obs_cooking_4",
                "obs_cooking_5",
                "obs_cooking_6",
                "obs_cooking_7",
                "obs_electricity_working",
                "obs_equipment_0",
                "obs_equipment_1",
                "obs_equipment_2",
                "obs_equipment_3",
                "obs_equipment_4",
                "obs_equipment_5",
                "obs_fence",
                "obs_fencing_play_area",
                "obs_firstaid",
                "obs_gate",
                "obs_handwashing_0",
                "obs_handwashing_1",
                "obs_handwashing_2",
                "obs_handwashing_3",
                "obs_handwashing_97",
                "obs_handwashing_friendly",
                "obs_hazard",
                "obs_hazard_0",
                "obs_hazard_1",
                "obs_hazard_2",
                "obs_hazard_3",
                "obs_hazard_4",
                "obs_hazard_5",
                "obs_hazard_6",
                "obs_hazard_7",
                "obs_hazard_8",
                "obs_hazard_97",
                "obs_heating_1",
                "obs_heating_2",
                "obs_heating_3",
                "obs_heating_4",
                "obs_heating_5",
                "obs_heating_6",
                "obs_heating_7",
                "obs_heating_8",
                "obs_lighting_1",
                "obs_lighting_2",
                "obs_lighting_3",
                "obs_lighting_4",
                "obs_lighting_5",
                "obs_lighting_6",
                "obs_lighting_8",
                "obs_materials",
                "obs_materials_0",
                "obs_materials_1",
                "obs_materials_10",
                "obs_materials_11",
                "obs_materials_12",
                "obs_materials_13",
                "obs_materials_14",
                "obs_materials_15",
                "obs_materials_16",
                "obs_materials_17",
                "obs_materials_18",
                "obs_materials_19",
                "obs_materials_2",
                "obs_materials_20",
                "obs_materials_3",
                "obs_materials_4",
                "obs_materials_5",
                "obs_materials_6",
                "obs_materials_7",
                "obs_materials_8",
                "obs_materials_9",
                "obs_materials_97",
                "obs_menu_compliance",
                "obs_menu_display",
                "obs_menu_same",
                "obs_outdoor",
                "obs_potable",
                "obs_safety_0",
                "obs_safety_1",
                "obs_safety_10",
                "obs_safety_2",
                "obs_safety_3",
                "obs_safety_4",
                "obs_safety_5",
                "obs_safety_6",
                "obs_safety_7",
                "obs_safety_8",
                "obs_safety_9",
                "obs_shared",
                "obs_space",
                "obs_toilet",
                "obs_toilet_0",
                "obs_toilet_1",
                "obs_toilet_2",
                "obs_toilet_3",
                "obs_toilet_4",
                "obs_toilet_5",
                "obs_toilet_6",
                "obs_toilet_7",
                "obs_toilet_8",
                "obs_toilet_97",
                "obs_toilet_clean",
                "obs_toilet_paper",
                "obs_toilet_size_chemical_1",
                "obs_toilet_size_disability_1",
                "obs_toilet_size_disability_2",
                "obs_toilet_size_disability_3",
                "obs_toilet_size_flush_1",
                "obs_toilet_size_flush_2",
                "obs_toilet_size_flush_3",
                "obs_toilet_size_pit_1",
                "obs_toilet_size_pit_2",
                "obs_toilet_size_pit_3",
                "obs_toilet_size_septic_2",
                "obs_toilet_size_septic_3",
                "obs_toilet_size_ventilation_1",
                "obs_toilet_size_ventilation_2",
                "obs_toilet_size_ventilation_3",
                "obs_toilets_children",
                "obs_toilets_gender",
                "obs_water_running",
                "position_other",
                "position_other_reason",
                "pqa_class",
                "pqa_class_age_1",
                "pqa_class_age_2",
                "pqa_class_age_3",
                "pqa_class_age_4",
                "pqa_class_age_5",
                "pqa_class_age_6",
                "pqa_curriculum_literacy",
                "pqa_curriculum_ncf",
                "pqa_curriculum_numeracy",
                "pqa_environment_accessible",
                "pqa_environment_appropriate",
                "pqa_environment_areas",
                "pqa_environment_open",
                "pqa_environment_outdoor",
                "pqa_environment_variety",
                "pqa_relationships_acknowledge",
                "pqa_relationships_discipline",
                "pqa_relationships_peers",
                "pqa_relationships_staff",
                "pqa_teaching_choice",
                "pqa_teaching_engagement",
                "pqa_teaching_participation",
                "pqa_teaching_questions",
                "pqa_teaching_support",
                "pra_clearance_ncp",
                "pra_clearance_police",
                "pra_cohort_0",
                "pra_cohort_1",
                "pra_cohort_2",
                "pra_cohort_3",
                "pra_cohort_4",
                "pra_cohort_5",
                "pra_cohort_6",
                "pra_gender",
                "pra_groupings_1",
                "pra_groupings_2",
                "pra_groupings_3",
                "pra_groupings_4",
                "pra_groupings_5",
                "pra_language",
                "pra_learnership",
                "pra_materials_donated",
                "pra_materials_kit",
                "pra_materials_library",
                "pra_materials_makefind",
                "pra_ncf_trainer_1",
                "pra_ncf_trainer_2",
                "pra_ncf_trainer_3",
                "pra_ncf_trainer_4",
                "pra_ncf_trainer_5",
                "pra_ncf_trainer_97",
                "pra_ncf_training",
                "pra_on_time",
                "pra_online_training",
                "pra_online_training_details",
                "pra_paid",
                "pra_parent_meeting",
                "pra_parent_same_attendance",
                "pra_plan_4yrs_1",
                "pra_plan_4yrs_2",
                "pra_plan_4yrs_3",
                "pra_plan_4yrs_4",
                "pra_plan_4yrs_97",
                "pra_plan_5yrs_1",
                "pra_plan_5yrs_2",
                "pra_plan_5yrs_3",
                "pra_plan_5yrs_4",
                "pra_plan_5yrs_5",
                "pra_plan_5yrs_97",
                "pra_plan_approved",
                "pra_plan_ncf",
                "pra_plans_0",
                "pra_plans_1",
                "pra_plans_2",
                "pra_plans_3",
                "pra_qualification_0",
                "pra_qualification_1",
                "pra_qualification_2",
                "pra_qualification_3",
                "pra_qualification_4",
                "pra_qualification_5",
                "pra_qualification_6",
                "pra_qualification_7",
                "pra_qualification_97",
                "pra_special_referrals",
                "pra_special_training",
                "pra_training_0",
                "pra_training_1",
                "pra_training_2",
                "pra_training_3",
                "pra_training_4",
                "pra_training_5",
                "pra_training_6",
                "pri_aftercare",
                "pri_attendance_usual",
                "pri_clinic_travel_1",
                "pri_clinic_travel_2",
                "pri_clinic_travel_3",
                "pri_clinic_travel_4",
                "pri_clinic_travel_5",
                "pri_clinic_travel_97",
                "pri_confirm_subsidy",
                "pri_covid_awareness",
                "pri_covid_awareness_1",
                "pri_covid_awareness_2",
                "pri_covid_awareness_3",
                "pri_covid_awareness_4",
                "pri_covid_awareness_97",
                "pri_covid_fund_applied",
                "pri_covid_fund_received",
                "pri_covid_precautions",
                "pri_covid_precautions_1",
                "pri_covid_precautions_2",
                "pri_covid_precautions_3",
                "pri_covid_precautions_4",
                "pri_covid_precautions_5",
                "pri_covid_precautions_6",
                "pri_covid_precautions_97",
                "pri_dsd_conditional_1",
                "pri_dsd_conditional_10",
                "pri_dsd_conditional_2",
                "pri_dsd_conditional_3",
                "pri_dsd_conditional_4",
                "pri_dsd_conditional_5",
                "pri_dsd_conditional_6",
                "pri_dsd_conditional_7",
                "pri_dsd_conditional_8",
                "pri_dsd_conditional_9",
                "pri_dsd_conditional_97",
                "pri_dsd_previous",
                "pri_dsd_unregistered_1",
                "pri_dsd_unregistered_10",
                "pri_dsd_unregistered_11",
                "pri_dsd_unregistered_12",
                "pri_dsd_unregistered_13",
                "pri_dsd_unregistered_2",
                "pri_dsd_unregistered_3",
                "pri_dsd_unregistered_4",
                "pri_dsd_unregistered_5",
                "pri_dsd_unregistered_6",
                "pri_dsd_unregistered_7",
                "pri_dsd_unregistered_8",
                "pri_dsd_unregistered_9",
                "pri_dsd_unregistered_97",
                "pri_expenseother",
                "pri_fees",
                "pri_fees_exceptions",
                "pri_fees_exceptions_other",
                "pri_fees_free",
                "pri_firstaid",
                "pri_food_donation",
                "pri_food_donor_1",
                "pri_food_donor_2",
                "pri_food_donor_3",
                "pri_food_donor_4",
                "pri_food_donor_97",
                "pri_food_guidance",
                "pri_food_type_0",
                "pri_food_type_1",
                "pri_food_type_2",
                "pri_food_type_3",
                "pri_food_type_4",
                "pri_food_type_5",
                "pri_funding_1",
                "pri_funding_2",
                "pri_funding_3",
                "pri_funding_4",
                "pri_funding_5",
                "pri_funding_6",
                "pri_funding_7",
                "pri_funding_97",
                "pri_funding_donations",
                "pri_funding_food",
                "pri_funding_none",
                "pri_funding_salary_0",
                "pri_funding_salary_1",
                "pri_funding_salary_2",
                "pri_funding_salary_3",
                "pri_funding_salary_4",
                "pri_funding_salary_97",
                "pri_garden",
                "pri_health_0",
                "pri_health_1",
                "pri_health_2",
                "pri_health_3",
                "pri_health_4",
                "pri_health_5",
                "pri_health_97",
                "pri_holidays",
                "pri_internet",
                "pri_internet_user_1",
                "pri_internet_user_2",
                "pri_internet_user_3",
                "pri_internet_user_4",
                "pri_language",
                "pri_library",
                "pri_library_material_1",
                "pri_library_material_10",
                "pri_library_material_11",
                "pri_library_material_12",
                "pri_library_material_2",
                "pri_library_material_3",
                "pri_library_material_4",
                "pri_library_material_5",
                "pri_library_material_6",
                "pri_library_material_7",
                "pri_library_material_8",
                "pri_library_material_9",
                "pri_meal_1",
                "pri_meal_2",
                "pri_meal_3",
                "pri_meal_4",
                "pri_meals",
                "pri_money_1",
                "pri_money_2",
                "pri_money_3",
                "pri_money_97",
                "pri_network",
                "pri_network_type_1",
                "pri_network_type_2",
                "pri_network_type_3",
                "pri_network_type_97",
                "pri_precovid_attendance",
                "pri_qualification_0",
                "pri_qualification_1",
                "pri_qualification_2",
                "pri_qualification_3",
                "pri_qualification_4",
                "pri_qualification_5",
                "pri_qualification_6",
                "pri_qualification_7",
                "pri_qualification_97",
                "pri_records_0",
                "pri_records_1",
                "pri_records_2",
                "pri_records_3",
                "pri_records_4",
                "pri_records_5",
                "pri_refrigerator",
                "pri_registered_cipc",
                "pri_registered_health",
                "pri_registered_npo",
                "pri_school",
                "pri_staff_changes_reasons_1",
                "pri_staff_changes_reasons_2",
                "pri_staff_changes_reasons_3",
                "pri_staff_changes_reasons_4",
                "pri_staff_changes_reasons_5",
                "pri_staff_changes_reasons_6",
                "pri_staff_changes_reasons_97",
                "pri_subsidy",
                "pri_support",
                "pri_support_provider_1",
                "pri_support_provider_2",
                "pri_support_provider_3",
                "pri_support_provider_4",
                "pri_support_provider_5",
                "pri_support_provider_97",
                "pri_transport",
                "pri_zoning",
                "professionals_practitioners",
                "sanitation_educators_1",
                "sanitation_educators_2",
                "sanitation_educators_3",
                "sanitation_learners",
                "urban",
                "teacher_emotional_met",
                "teacher_selfcare_met",
                "teacher_social_met",
                # yes/no questions by their name (CLEAN-14)
                "pra_breadwinner",
                "pra_letcee_club",
                "pri_funding_subsidy",
            ),
            # enumerators' free text: the "other" answers and the explanations of flagged measurements
            string=(
                "healthother",
                "obs_handwashingother",
                "obs_materialsother",
                "obs_water_running_none",
                "obs_waterother",
                "pra_class_size_large",
                "pra_class_space_large",
                "pra_class_space_small",
                "pra_education_other",
                "pra_ncf_trainerother",
                "pra_plan_4yrs_other",
                "pra_plan_5yrs_other",
                "pra_qualification_other",
                "pri_covid_awareness_other",
                "pri_covid_precautions_other",
                "pri_dsd_conditional_other",
                "pri_dsd_unregistered_other",
                "pri_food_donorother",
                "pri_funding_salaryother",
                "pri_fundingother",
                "pri_landother",
                "pri_moneyother",
                "pri_qualificationother",
                "pri_reason_register_year",
                "pri_staff_changes_reasonsother",
                "pri_support_providerother",
            ),
            datetime={"child_dob": "%d%b%Y", "pra_dob": "%d%b%Y"},
        )
