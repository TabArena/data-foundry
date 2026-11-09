"""Curated dataset definition for `early_learning_predictors` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    FeatureTypes,
    Grouping,
    Metric,
    Source,
    TaskSummary,
    decode,
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
    "gr_ecd": ["almost none", "0-25%", "25-50%", "50-75%", "almost all"],
    "obs_booknumber": [
        "none or almost none",
        "less than 50",
        "50-100 books",
        "100-250 books",
        "more than 250 books",
    ],  # open-ended
    "obs_condition_equipment": [
        "bad (mostly broken and unused)",
        "okay (some in working condition)",
        "fine (mostly in working condition)",
        "very good",
    ],
    "obs_infrastructure": [
        "strong state of disrepair",
        "moderate signs of disrepair",
        "minor signs of disrepair",
        "well maintained",
    ],
    "obs_material_display": [
        "no, there is nothing against the walls",
        "yes, but of poor quality and not relevant to the age group",
        "yes, of average quality and relevant to the age group",
        "yes, stimulating and appropriate",
    ],
    "plan": [
        "no",
        "yes, details provided for the main activities in the week",
        "yes, details provided for the activities each day",
    ],
    "pqa_assessment_observation": [
        "inadequate: no observation record, or the observation book is not in regular use",
        "basic: a regular observation record/book with some written indication of remedial activities",
        "good: many and varied observations of children's progress and a range of activities to remediate difficulties/facilitate holistic development",
    ],
    "pqa_assessment_systematic": [
        "inadequate: there is no systematic child assessment",
        "basic: assessments done at least twice a year, using a standard format, and filed for reference",
        "good: assessments using a standard format updated regularly, children with difficulties assessed more often",
    ],
    "pqa_curriculum_balance": [
        "inadequate: either free play or whole group activities predominate",
        "basic: both free play and whole group activities each day and some small group times",
        "good: substantial free play indoors and outdoors, story, music and ring time daily and regular small group teaching",
    ],
    "pqa_curriculum_plan": [
        "inadequate: no evidence of planning used to organise learning activities",
        "basic: planning books and the playroom reflect a planned and integrated approach",
        "good: plans are applied, taking into account children's interests and developmental appropriateness",
    ],
    "pra_adequacy_materials": ["inadequate", "somewhat adequate", "adequate", "good", "excellent"],
    "pra_cotlands_support": ["neutral", "very satisfied", "extremely satisfied"],
    "pra_cotlands_visits": ["1 time", "4 times", "more than 10 times"],  # open-ended
    "pra_education": [
        "below Grade 12/matric",
        "matric/National Senior Certificate",
        "certificate",
        "diploma",
        "undergraduate degree",
        "postgraduate degree",
    ],
    "pra_engaged": ["seldom", "sometimes", "often"],
    "pra_free_play": ["30 minutes or less", "up to 1 hour", "up to 2 hours", "more than 3 hours"],  # open-ended
    "pra_free_play_outdoor": ["30 minutes or less", "up to 1 hour", "up to 2 hours", "up to 3 hours"],
    "pra_grade": ["school not attended", "grade 8", "grade 9", "grade 10", "grade 11", "grade 12"],
    "pra_letcee_support_cluster": ["not satisfied", "neutral", "very satisfied", "extremely satisfied"],
    "pra_letcee_support_coach": ["not satisfied", "neutral", "very satisfied"],
    "pra_motivate_mentoring": ["disagree strongly", "disagree a little", "agree a little", "agree strongly"],
    "pra_motivate_recognition": ["disagree strongly", "disagree a little", "agree a little", "agree strongly"],
    "pra_motivate_support": ["disagree strongly", "disagree a little", "agree a little", "agree strongly"],
    "pra_ntataise_attendance": ["5 times", "7 times", "8 times", "9 times", "more than 10 times"],  # open-ended
    "pra_ntataise_support": ["slightly satisfied", "neutral", "very satisfied", "extremely satisfied"],
    "pra_ntataise_visits": [
        "2 times",
        "3 times",
        "4 times",
        "5 times",
        "7 times",
        "8 times",
        "more than 10 times",
    ],  # open-ended
    "pra_tuc_support": ["not satisfied", "neutral", "very satisfied", "extremely satisfied"],
    "pra_tuc_visits": [
        "1 time",
        "2 times",
        "4 times",
        "5 times",
        "7 times",
        "10 times",
        "more than 10 times",
    ],  # open-ended
    "pri_covid_staff_salaries": [
        "no, not able to pay them at all",
        "no, had to reduce their salaries",
        "yes, salaries have remained the same",
    ],
    "pri_education": [
        "below Grade 12/matric",
        "matric/National Senior Certificate",
        "certificate",
        "diploma",
        "undergraduate degree",
        "postgraduate degree",
    ],
    "pri_fees_paid_proportion": [
        "none of the parents",
        "only a few parents",
        "about half of the parents",
        "most parents, but not all",
        "all parents",
    ],
    "pri_food_parents_afternoon": ["none", "some", "all"],
    "pri_food_parents_breakfast": ["none", "some", "all"],
    "pri_food_parents_lunch": ["none", "some", "all"],
    "pri_food_parents_morning": ["none", "some", "all"],
    "pri_parents_activities": ["no, no one", "yes, only one or two", "yes, some parents", "yes, most parents"],
    "pri_parents_contact": ["no, no one", "yes, only one or two", "yes, some parents", "yes, most parents"],
    "pri_parents_frequency": ["never", "annually", "quarterly", "monthly", "weekly"],
    "pri_registered_dsd": ["not registered", "in process", "conditionally registered", "fully registered"],
    "pri_registered_partial": ["not registered", "in process", "conditionally registered", "fully registered"],
    "pri_registered_programme": ["not registered", "in process", "conditionally registered", "fully registered"],
    "pri_same_language": [
        "none of the children",
        "less than half of the children",
        "more than half of the children",
        "all children",
    ],
    "pri_separate": [
        "no, all ages learning and playing together",
        "yes, grouped by age but using the same space",
        "yes, grouped by age and divided into different rooms",
    ],
    "pri_staff_employed": [
        "less than half of the number of previous years",
        "more than half of the number of previous years",
        "about the same number as previous years",
        "more staff than previous years",
    ],
    "pri_support_dbe": ["never", "once", "twice", "three times", "more than three times"],  # open-ended
    "pri_support_dsd": ["never", "once", "twice", "three times", "more than three times"],  # open-ended
    "pri_support_frequency": ["once a year", "once a term", "once a month", "once a week"],
    "pri_support_municipality": ["never", "once", "twice", "three times", "more than three times"],  # open-ended
    "pri_support_ngo": ["never", "once", "twice", "three times", "more than three times"],  # open-ended
    "rating": [
        "no books at all",
        "lack of books, few books, or dated books",
        "lots of books but not clearly used",
        "lots of books and clearly used",
    ],
    "teacher_emotional_appropriate": ["not true", "sometimes true", "often true"],
    "teacher_emotional_confidence": ["not true", "sometimes true", "often true"],
    "teacher_emotional_independent": ["not true", "sometimes true", "often true"],
    "teacher_emotional_selfstarter": ["not true", "sometimes true", "often true"],
    "teacher_emotional_understand": ["not true", "sometimes true", "often true"],
    "teacher_social_assistance": ["none of the time", "a little of the time", "most of the time", "all of the time"],
    "teacher_social_cooperate": ["none of the time", "a little of the time", "most of the time", "all of the time"],
    "teacher_social_ideas": ["none of the time", "a little of the time", "most of the time", "all of the time"],
    "teacher_social_initiative": ["none of the time", "a little of the time", "most of the time", "all of the time"],
    "teacher_social_nonaggressive": ["none of the time", "a little of the time", "most of the time", "all of the time"],
    "teacher_social_peers": ["none of the time", "a little of the time", "most of the time", "all of the time"],
    "teacher_emotional_adjust": ["not true", "sometimes true", "often true"],
    "child_stunted": ["Severely stunted", "Moderately stunted", "Normal"],
    "pra_salary": [
        "R0",
        "less than R500 per month",
        "R500 – R749",
        "R750 – R999",
        "R1000 – R1249",
        "R1250 – R1499",
        "R1500 – R1999",
        "R2000 – R2499",
        "R2500 – R2999",
        "R3000 – R3499",
        "R3500 – R3999",
        "R4000 – R4449",
        "R5000 – R5999",
        "more than R6000",
    ],
    "pra_cotlands_attendance": ["1 time", "more than 10 times"],
    "pra_lesedi_support": ["neutral", "very satisfied"],
    "pra_letcee_clubsupport": ["neutral", "very satisfied"],
}


# The codebook's words for coded columns, decoded in `_clean` after the codes that mean unknown are missing
# (CLEAN-12; the curator's rule of 2026-11-01).
CODE_LABELS = {
    "gr_ecd": {"0": "almost none", "1": "0-25%", "2": "25-50%", "3": "50-75%", "4": "almost all"},
    "obs_booknumber": {
        "1": "none or almost none",
        "2": "less than 50",
        "3": "50-100 books",
        "4": "100-250 books",
        "5": "more than 250 books",
    },
    "obs_condition_equipment": {
        "1": "bad (mostly broken and unused)",
        "2": "okay (some in working condition)",
        "3": "fine (mostly in working condition)",
        "4": "very good",
    },
    "obs_infrastructure": {
        "1": "strong state of disrepair",
        "2": "moderate signs of disrepair",
        "3": "minor signs of disrepair",
        "4": "well maintained",
    },
    "obs_material_display": {
        "0": "no, there is nothing against the walls",
        "1": "yes, but of poor quality and not relevant to the age group",
        "2": "yes, of average quality and relevant to the age group",
        "3": "yes, stimulating and appropriate",
    },
    "plan": {
        "0": "no",
        "1": "yes, details provided for the activities each day",
        "2": "yes, details provided for the main activities in the week",
    },
    "pqa_assessment_observation": {
        "0": "inadequate: no observation record, or the observation book is not in regular use",
        "1": "basic: a regular observation record/book with some written indication of remedial activities",
        "2": "good: many and varied observations of children's progress and a range of activities to remediate difficulties/facilitate holistic development",
    },
    "pqa_assessment_systematic": {
        "0": "inadequate: there is no systematic child assessment",
        "1": "basic: assessments done at least twice a year, using a standard format, and filed for reference",
        "2": "good: assessments using a standard format updated regularly, children with difficulties assessed more often",
    },
    "pqa_curriculum_balance": {
        "0": "inadequate: either free play or whole group activities predominate",
        "1": "basic: both free play and whole group activities each day and some small group times",
        "2": "good: substantial free play indoors and outdoors, story, music and ring time daily and regular small group teaching",
    },
    "pqa_curriculum_plan": {
        "0": "inadequate: no evidence of planning used to organise learning activities",
        "1": "basic: planning books and the playroom reflect a planned and integrated approach",
        "2": "good: plans are applied, taking into account children's interests and developmental appropriateness",
    },
    "pra_adequacy_materials": {
        "1": "inadequate",
        "2": "somewhat adequate",
        "3": "adequate",
        "4": "good",
        "5": "excellent",
    },
    "pra_cotlands_support": {"3": "neutral", "4": "very satisfied", "5": "extremely satisfied"},
    "pra_cotlands_visits": {"1": "1 time", "4": "4 times", "11": "more than 10 times"},
    "pra_education": {
        "1": "below Grade 12/matric",
        "2": "matric/National Senior Certificate",
        "3": "certificate",
        "4": "diploma",
        "5": "undergraduate degree",
        "6": "postgraduate degree",
    },
    "pra_engaged": {"1": "seldom", "2": "sometimes", "3": "often"},
    "pra_free_play": {"1": "30 minutes or less", "2": "up to 1 hour", "3": "up to 2 hours", "5": "more than 3 hours"},
    "pra_free_play_outdoor": {
        "1": "30 minutes or less",
        "2": "up to 1 hour",
        "3": "up to 2 hours",
        "4": "up to 3 hours",
    },
    "pra_grade": {
        "0": "school not attended",
        "8": "grade 8",
        "9": "grade 9",
        "10": "grade 10",
        "11": "grade 11",
        "12": "grade 12",
    },
    "pra_letcee_support_cluster": {
        "1": "not satisfied",
        "3": "neutral",
        "4": "very satisfied",
        "5": "extremely satisfied",
    },
    "pra_letcee_support_coach": {"1": "not satisfied", "3": "neutral", "4": "very satisfied"},
    "pra_motivate_mentoring": {
        "1": "disagree strongly",
        "2": "disagree a little",
        "3": "agree a little",
        "4": "agree strongly",
    },
    "pra_motivate_recognition": {
        "1": "disagree strongly",
        "2": "disagree a little",
        "3": "agree a little",
        "4": "agree strongly",
    },
    "pra_motivate_support": {
        "1": "disagree strongly",
        "2": "disagree a little",
        "3": "agree a little",
        "4": "agree strongly",
    },
    "pra_ntataise_attendance": {
        "5": "5 times",
        "7": "7 times",
        "8": "8 times",
        "9": "9 times",
        "11": "more than 10 times",
    },
    "pra_ntataise_support": {
        "2": "slightly satisfied",
        "3": "neutral",
        "4": "very satisfied",
        "5": "extremely satisfied",
    },
    "pra_ntataise_visits": {
        "2": "2 times",
        "3": "3 times",
        "4": "4 times",
        "5": "5 times",
        "7": "7 times",
        "8": "8 times",
        "11": "more than 10 times",
    },
    "pra_tuc_support": {"1": "not satisfied", "3": "neutral", "4": "very satisfied", "5": "extremely satisfied"},
    "pra_tuc_visits": {
        "1": "1 time",
        "2": "2 times",
        "4": "4 times",
        "5": "5 times",
        "7": "7 times",
        "10": "10 times",
        "11": "more than 10 times",
    },
    "pri_covid_staff_salaries": {
        "0": "no, not able to pay them at all",
        "1": "no, had to reduce their salaries",
        "2": "yes, salaries have remained the same",
    },
    "pri_education": {
        "1": "below Grade 12/matric",
        "2": "matric/National Senior Certificate",
        "3": "certificate",
        "4": "diploma",
        "5": "undergraduate degree",
        "6": "postgraduate degree",
    },
    "pri_fees_paid_proportion": {
        "0": "none of the parents",
        "1": "only a few parents",
        "2": "about half of the parents",
        "3": "most parents, but not all",
        "4": "all parents",
    },
    "pri_food_parents_afternoon": {"0": "none", "1": "some", "2": "all"},
    "pri_food_parents_breakfast": {"0": "none", "1": "some", "2": "all"},
    "pri_food_parents_lunch": {"0": "none", "1": "some", "2": "all"},
    "pri_food_parents_morning": {"0": "none", "1": "some", "2": "all"},
    "pri_parents_activities": {
        "0": "no, no one",
        "1": "yes, only one or two",
        "2": "yes, some parents",
        "3": "yes, most parents",
    },
    "pri_parents_contact": {
        "0": "no, no one",
        "1": "yes, only one or two",
        "2": "yes, some parents",
        "3": "yes, most parents",
    },
    "pri_parents_frequency": {"0": "never", "1": "weekly", "2": "monthly", "3": "quarterly", "4": "annually"},
    "pri_registered_dsd": {
        "1": "fully registered",
        "2": "conditionally registered",
        "3": "in process",
        "4": "not registered",
    },
    "pri_registered_partial": {
        "1": "fully registered",
        "2": "conditionally registered",
        "3": "in process",
        "4": "not registered",
    },
    "pri_registered_programme": {
        "1": "fully registered",
        "2": "conditionally registered",
        "3": "in process",
        "4": "not registered",
    },
    "pri_same_language": {
        "1": "all children",
        "2": "more than half of the children",
        "3": "less than half of the children",
        "4": "none of the children",
    },
    "pri_separate": {
        "0": "no, all ages learning and playing together",
        "1": "yes, grouped by age but using the same space",
        "2": "yes, grouped by age and divided into different rooms",
    },
    "pri_staff_employed": {
        "1": "more staff than previous years",
        "2": "about the same number as previous years",
        "3": "more than half of the number of previous years",
        "4": "less than half of the number of previous years",
    },
    "pri_support_dbe": {"0": "never", "1": "once", "2": "twice", "3": "three times", "4": "more than three times"},
    "pri_support_dsd": {"0": "never", "1": "once", "2": "twice", "3": "three times", "4": "more than three times"},
    "pri_support_municipality": {
        "0": "never",
        "1": "once",
        "2": "twice",
        "3": "three times",
        "4": "more than three times",
    },
    "pri_support_ngo": {"0": "never", "1": "once", "2": "twice", "3": "three times", "4": "more than three times"},
    "pri_support_frequency": {"1": "once a year", "2": "once a term", "3": "once a month", "4": "once a week"},
    "rating": {
        "0": "no books at all",
        "1": "lack of books, few books, or dated books",
        "2": "lots of books but not clearly used",
        "3": "lots of books and clearly used",
    },
    "teacher_emotional_appropriate": {"0": "not true", "1": "sometimes true", "2": "often true"},
    "teacher_emotional_confidence": {"0": "not true", "1": "sometimes true", "2": "often true"},
    "teacher_emotional_independent": {"0": "not true", "1": "sometimes true", "2": "often true"},
    "teacher_emotional_selfstarter": {"0": "not true", "1": "sometimes true", "2": "often true"},
    "teacher_emotional_understand": {"0": "not true", "1": "sometimes true", "2": "often true"},
    "teacher_social_assistance": {
        "1": "none of the time",
        "2": "a little of the time",
        "3": "most of the time",
        "4": "all of the time",
    },
    "teacher_social_cooperate": {
        "1": "none of the time",
        "2": "a little of the time",
        "3": "most of the time",
        "4": "all of the time",
    },
    "teacher_social_ideas": {
        "1": "none of the time",
        "2": "a little of the time",
        "3": "most of the time",
        "4": "all of the time",
    },
    "teacher_social_initiative": {
        "1": "none of the time",
        "2": "a little of the time",
        "3": "most of the time",
        "4": "all of the time",
    },
    "teacher_social_nonaggressive": {
        "1": "none of the time",
        "2": "a little of the time",
        "3": "most of the time",
        "4": "all of the time",
    },
    "teacher_social_peers": {
        "1": "none of the time",
        "2": "a little of the time",
        "3": "most of the time",
        "4": "all of the time",
    },
    "teacher_emotional_adjust": {"0": "not true", "1": "sometimes true", "2": "often true"},
    "gr_1_tt": {
        "1": "all children at school every day",
        "4": "alternate days of the week",
        "5": "10-day cycle (3 days one week, 2 days the following week)",
    },
    "grade_r": {"0": "no", "1": "yes, and I was able to see them", "2": "yes, but I was not able to see them"},
    "obs_building": {
        "1": "conventional, brick or block with tile or zinc roof",
        "2": "traditional, mortar or mud walls with zinc or thatch roof",
        "3": "shipping container",
        "4": "prefab building",
        "5": "informal housing (shack)",
    },
    "obs_cooking_census": {
        "0": "none",
        "1": "electricity",
        "2": "gas",
        "5": "paraffin",
        "6": "coal or wood",
        "97": "other",
    },
    "obs_heating_census": {
        "0": "none",
        "1": "electricity",
        "2": "gas",
        "4": "solar",
        "5": "paraffin",
        "6": "coal or wood",
        "97": "other",
    },
    "obs_lighting_census": {
        "0": "none",
        "1": "electricity",
        "2": "gas",
        "3": "candles",
        "4": "solar",
        "5": "paraffin",
        "97": "other",
    },
    "obs_water": {
        "1": "tap water in the building",
        "2": "tap water on-site, outside the building",
        "3": "public or communal tap off-site",
        "4": "bore-hole water on-site",
        "5": "rain water tank on-site",
        "97": "other",
    },
    "pra_class_language": {
        "1": "Afrikaans",
        "2": "English",
        "3": "isiNdebele",
        "4": "isiXhosa",
        "5": "isiZulu",
        "6": "Sepedi",
        "7": "Setswana",
        "8": "Sesotho",
        "9": "Siswati",
        "10": "Tshivenda",
        "11": "Xitsonga",
    },
    "pra_job": {"1": "principal/matron", "2": "supervisor", "3": "practitioner/teacher", "4": "assistant practitioner"},
    "pra_previous": {
        "1": "working in another school/ECD programme",
        "2": "self-employed",
        "3": "in school/studying",
        "4": "not employed, but looking for work",
        "5": "working in another industry/sector",
        "97": "other",
    },
    "pra_shape": {"1": "rectangle", "2": "L-shaped", "3": "circle"},
    "pri_bank": {"1": "yes", "2": "no, principal uses his/her own bank account"},
    "pri_facilities": {
        "1": "school",
        "2": "the ECD programme",
        "3": "religious institution",
        "4": "community centre",
        "5": "not-for-profit organisation",
        "6": "municipality",
        "7": "other government institution (not municipality)",
        "8": "the person in charge of the programme",
        "9": "another private individual",
        "10": "private business",
        "97": "other",
    },
    "pri_land": {
        "1": "school",
        "2": "the ECD programme",
        "3": "religious institution",
        "4": "community centre",
        "5": "not-for-profit organisation",
        "6": "municipality",
        "7": "other government institution (not municipality)",
        "8": "the person in charge of the programme",
        "9": "another private individual",
        "10": "private business",
        "97": "other",
        "11": "communal land (traditional)",
    },
    "pri_kitchen": {
        "0": "no kitchen or meal preparation area",
        "1": "yes, separated from the children",
        "2": "no, not separated from the children",
    },
    "pri_location": {
        "1": "in someone's house",
        "2": "in the garage of someone's house",
        "3": "at a church/mosque/place of worship",
        "4": "at a community hall/centre",
        "5": "a municipal building",
        "6": "an ECD centre",
        "97": "other",
    },
    "pri_meal_prep": {
        "1": "a cook employed by the programme",
        "2": "volunteers/someone from the community",
        "3": "EPWP worker",
        "5": "practitioners",
        "97": "other",
    },
    "pra_agency_choice": {
        "1": "agree with the 1st statement much more than with the 2nd",
        "2": "agree with the 2nd statement much more than with the 1st",
        "3": "agree with both statements equally",
        "4": "disagree with both statements equally",
    },
    "pra_agency_explore": {
        "1": "agree with the 1st statement much more than with the 2nd",
        "2": "agree with the 2nd statement much more than with the 1st",
        "3": "agree with both statements equally",
        "4": "disagree with both statements equally",
    },
    "pra_agency_learn": {
        "1": "agree with the 1st statement much more than with the 2nd",
        "2": "agree with the 2nd statement much more than with the 1st",
        "3": "agree with both statements equally",
        "4": "disagree with both statements equally",
    },
    "pra_agency_order": {
        "1": "agree with the 1st statement much more than with the 2nd",
        "2": "agree with the 2nd statement much more than with the 1st",
        "3": "agree with both statements equally",
        "4": "disagree with both statements equally",
    },
    "pra_agency_play": {
        "1": "agree with the 1st statement much more than with the 2nd",
        "2": "agree with the 2nd statement much more than with the 1st",
        "3": "agree with both statements equally",
        "4": "disagree with both statements equally",
    },
    "pra_agency_questions": {
        "1": "agree with the 1st statement much more than with the 2nd",
        "2": "agree with the 2nd statement much more than with the 1st",
        "3": "agree with both statements equally",
        "4": "disagree with both statements equally",
    },
    "pra_agency_understand": {
        "1": "agree with the 1st statement much more than with the 2nd",
        "2": "agree with the 2nd statement much more than with the 1st",
        "3": "agree with both statements equally",
        "4": "disagree with both statements equally",
    },
    "pra_salary": {
        "0": "R0",
        "1": "less than R500 per month",
        "2": "R500 – R749",
        "3": "R750 – R999",
        "4": "R1000 – R1249",
        "5": "R1250 – R1499",
        "6": "R1500 – R1999",
        "7": "R2000 – R2499",
        "8": "R2500 – R2999",
        "9": "R3000 – R3499",
        "10": "R3500 – R3999",
        "11": "R4000 – R4449",
        "12": "R5000 – R5999",
        "13": "more than R6000",
    },
    "pra_cotlands_attendance": {"1": "1 time", "11": "more than 10 times"},
    "pra_lesedi_support": {"3": "neutral", "4": "very satisfied"},
    "pra_letcee_clubsupport": {"3": "neutral", "4": "very satisfied"},
    "pri_internet_source": {"1": "ADSL/LAN cable", "2": "Wi-Fi router"},
    "pri_mobile": {"1": "based at a specific location", "2": "moves from place to place"},
    "pra_gender": {"1": "male", "2": "female"},
}


# Scores and ratings with no words per level: numbers, as the source ships them (CLEAN-14).
SCORES = [
    "quintile",
    "pra_class_space_2",
    "pra_satisfaction_support",
    "ses_cat",
    "ses_proxy",
    "teacher_familiarity_with_child",
    "teacher_selfcare_total",
]


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
    domain = "education"
    sources = (
        Source(
            role="publication",
            platform="Other",
            url="https://www.datafirst.uct.ac.za/dataportal/index.php/catalog/962",
            license="Creative Commons CC-BY (Attribution-only) License",
            year="2024",
            bibtex="""
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
            """,
        ),
    )
    download_description = r"""
        No automatic download possible!

        mkdir -p local-data-warehouse/early_learning_predictors
        Go to https://www.datafirst.uct.ac.za/dataportal/index.php/catalog/962/get-microdata., create an account, download the data files and move them to local-data-warehouse/early_learning_predictors. Next, run:

        unzip local-data-warehouse/early_learning_predictors/elom-tb5i-2016-2023-v1-csv.zip -d local-data-warehouse/early_learning_predictors \
        && mv local-data-warehouse/early_learning_predictors/elom-tb5i-2016-2023-v1-csv/* local-data-warehouse/early_learning_predictors \
        && rm local-data-warehouse/early_learning_predictors/elom-tb5i-2016-2023-v1-csv.zip \
        && rm -r local-data-warehouse/early_learning_predictors/elom-tb5i-2016-2023-v1-csv
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
        - `language_match` ("Assessment language matches home", DataFirst V1328; 1 for 14,813 children, 0 for 6) holds
          the enumerator's reason in place of the answer in 16 rows. Each reason explains why the child was assessed in
          another language than at home (English at an English school or on the principal's request, a child who
          answers in Sesotho where the parents speak Zulu), so they are a "no": 0 (2026-11-01, CLEAN-11; Lennart asked
          to find out what they mean rather than keep them as categories).
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
        - The ward ships as the national ward code `id_ward_best` (8 digits, 569 wards), a category, in place of
          `ward_best`, the ward's number within its municipality (2026-11-05, Lennart, GitHub issue #48, CLEAN-14):
          as a number `ward_best` read as an order of places that does not exist, and 101 numbers stood for 569
          wards (ward 4 of Steve Tshwete is 83103004, ward 4 of Dr JS Moroka 83106003). The ward is a location, kept
          like the municipality, district and province, not an id of the data collection like the other `id_`
          columns. A ward holds 1 to 18 facilities (median 3, 28.5% hold one); the split groups by facility.
          The survey's sampling cluster `id_cluster_original` (430 clusters, also a median of 3 facilities) stays
          dropped: it exists only in the 2021 round (5,222 children), so it is a unit of that survey's sample design
          and marks the round, which we drop as `data_year`; the ward is a place a new facility has too, recorded in
          the 2020-2022 rounds (2026-11-05, Lennart).
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
        - Ordinal scales (2026-10-30, the curator's marks of 2026-10-31 and 2026-11-01, CLEAN-14): 86 columns are
          ordered categories in the order of the source's codebook (`ORDINAL_LEVELS`); 66 of them decoded from the
          source's codes into its words (`CODE_LABELS`, 2026-11-01); codes that mean unknown are missing (CLEAN-10).
        - Codes decoded (2026-11-01, CLEAN-12, CLEAN-14; the curator's rule: a code whose codebook says in words what
          each level is carries the words, a score without them is a number): 66 ordered codes carry their codebook's
          words (`CODE_LABELS`), in the same order; 27 unordered codes carry their words: `gr_1_tt`, `grade_r`,
          `obs_building`, `obs_cooking_census`, `obs_heating_census`, `obs_lighting_census`, `obs_water`,
          `pra_class_language`, `pra_job`, `pra_previous`, `pra_shape`, `pri_bank`, `pri_facilities`, `pri_land`,
          `pri_kitchen`, `pri_location`, `pri_meal_prep`, `pra_agency_choice`, `pra_agency_explore`, `pra_agency_learn`,
          `pra_agency_order`, `pra_agency_play`, `pra_agency_questions`, `pra_agency_understand`, `pri_internet_source`,
          `pri_mobile`, `pra_gender`; 7 scores with no words per level are numbers (`SCORES`): `quintile`,
          `pra_class_space_2`, `pra_satisfaction_support`, `ses_cat`, `ses_proxy`, `teacher_familiarity_with_child`,
          `teacher_selfcare_total`.
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
        # the enumerator's reason why the assessment was not in the home language, written in place of a 0 (notes)
        answer = df["language_match"]
        df["language_match"] = answer.where(answer.isin(["0", "1"]) | answer.isna(), "0")
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
        # the 2021 survey's sampling cluster: present only in that round, so it marks the round (curation notes)
        leaky_cols += ["id_cluster_original"]
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
                # the ward's number within its municipality: the same number names different wards;
                # the national ward code `id_ward_best` ships in its place (curation notes)
                "ward_best",
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
        # codes the codebook leaves without words, or a question that did not apply (CLEAN-10)
        df = set_missing(
            df,
            {
                "pra_cotlands_visits": [0.0],
                "pra_free_play": [0.0],
                "pra_free_play_outdoor": [0.0],
                "obs_water": [0.0],
                "pri_bank": [0.0],
            },
        )
        # the codebook's words for its codes (CLEAN-12)
        df = decode(df, CODE_LABELS)
        # scores with no words per level are numbers (CLEAN-14)
        df[SCORES] = df[SCORES].astype("object").apply(pd.to_numeric)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            ordinal=ORDINAL_LEVELS,
            categorical=(
                "pri_mobile",
                "pri_internet_source",
                "pra_agency_understand",
                "pra_agency_questions",
                "pra_agency_play",
                "pra_agency_order",
                "pra_agency_learn",
                "pra_agency_explore",
                "pra_agency_choice",
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
                # the national ward code, a location like the municipality (curation notes)
                "id_ward_best",
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
