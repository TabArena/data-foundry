"""Curated dataset definition for `wioa_employment_after_exit` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    TaskSummary,
    Temporal,
    TemporalSplits,
    drop_columns,
    set_missing,
)

# The three public use files and the exit dates (YYYYMMDD, [from, to)) each one supplies. A file holds a rolling ten
# quarters and fills the employment outcome for the exits up to four quarters before its report quarter, so the
# matured exit quarters of successive files overlap; each exit quarter is taken from the newest file that holds it
# matured, and no exit is taken twice.
SOURCE_FILES = (
    ("WIOAPerformanceRecords_PY2023Q4_PUBLIC.csv", 20220101, 20230101),
    ("WIOAPUDFPY24Q4.parquet", 20230101, 20231001),
    ("WIOAPUDFPY25Q3.parquet", 20231001, 20250401),
)
PREPARED_FILE = "wioa_exiters_q2_employment.parquet"

# Items read from the files (PIRL and calculated items of the record layout). Left out on reading, never shipped:
# the outcome items after exit (PIRL 1600-1618, 1703-1706, 1800-1805, 1814, 1900, 1901, CALC 4014-4019; CALC 4013 is
# read as the target), follow-up and post-exit services (1406, 1412, 1503), the self-service, information-only and
# reportable-individual contact dates that run past the exit (1002, 1007, 1100, 1101, 1103), employment at DWG
# completion (2002), and items that are constant, empty or copies on this population (203, 923, 920, 937,
# CALC 4006-4012, 4020, 4040, 4041, REPORT_QUARTER). The encrypted person id (100) is read for the person's history
# and dropped.
RAW_COLUMNS = (
    "PIRL105", "PIRL106", "PIRL107", "PIRL108A", "PIRL108B", "PIRL108C",
    "PIRL201", "PIRL202", "PIRL204", "PIRL205", "PIRL206", "PIRL207", "PIRL208", "PIRL209",
    "PIRL210", "PIRL211", "PIRL212", "PIRL213", "PIRL214", "PIRL215",
    "PIRL300", "PIRL301", "PIRL302", "PIRL303", "PIRL304", "PIRL305", "PIRL306", "PIRL307", "PIRL309", "PIRL310",
    "PIRL311", "PIRL312", "PIRL313", "PIRL314", "PIRL315", "PIRL316",
    "PIRL400", "PIRL402", "PIRL403", "PIRL404", "PIRL405", "PIRL406", "PIRL407", "PIRL408", "PIRL409", "PIRL410",
    "PIRL412", "PIRL413",
    "PIRL600", "PIRL601", "PIRL602", "PIRL603", "PIRL604", "PIRL701", "PIRL702", "PIRL704",
    "PIRL800", "PIRL801", "PIRL802", "PIRL803", "PIRL804", "PIRL805", "PIRL806", "PIRL807", "PIRL808",
    "PIRL900", "PIRL901", "PIRL903", "PIRL904", "PIRL905", "PIRL906", "PIRL907", "PIRL908", "PIRL909", "PIRL910",
    "PIRL911", "PIRL912", "PIRL913", "PIRL914", "PIRL916", "PIRL917", "PIRL918", "PIRL919", "PIRL921", "PIRL922",
    "PIRL930", "PIRL931", "PIRL932", "PIRL933", "PIRL934", "PIRL935", "PIRL936", "PIRL938", "PIRL939", "PIRL940",
    "PIRL1000", "PIRL1001", "PIRL1003", "PIRL1004", "PIRL1005", "PIRL1006",
    "PIRL1102", "PIRL1104", "PIRL1105", "PIRL1106", "PIRL1107", "PIRL1108", "PIRL1109", "PIRL1110", "PIRL1111",
    "PIRL1113", "PIRL1114", "PIRL1115", "PIRL1116",
    "PIRL1200", "PIRL1201", "PIRL1202", "PIRL1203", "PIRL1205", "PIRL1206", "PIRL1207", "PIRL1210", "PIRL1211",
    "PIRL1213", "PIRL1214", "PIRL1215", "PIRL1216", "PIRL1217", "PIRL1218", "PIRL1219", "PIRL1220", "PIRL1221",
    "PIRL1222",
    "PIRL1300", "PIRL1301", "PIRL1302", "PIRL1303", "PIRL1305", "PIRL1306", "PIRL1307", "PIRL1308", "PIRL1309",
    "PIRL1310", "PIRL1311", "PIRL1312", "PIRL1313", "PIRL1314", "PIRL1315", "PIRL1316", "PIRL1317", "PIRL1318",
    "PIRL1319", "PIRL1320", "PIRL1328", "PIRL1332", "PIRL1333",
    "PIRL1401", "PIRL1402", "PIRL1403", "PIRL1405", "PIRL1407", "PIRL1408", "PIRL1409", "PIRL1410", "PIRL1411",
    "PIRL1413", "PIRL1414", "PIRL1415", "PIRL1416", "PIRL1500", "PIRL1501",
    "PIRL1700", "PIRL1701", "PIRL1702",
    "PIRL1806", "PIRL1807", "PIRL1808", "PIRL1809", "PIRL1810", "PIRL1811", "PIRL1812", "PIRL1813",
    "PIRL2001", "PIRL2003", "PIRL2004", "PIRL2413", "PIRL2414", "PIRL2516", "PIRL3004", "PIRL3005", "PIRL3006",
    "PIRL3007",
    "CALC4000", "CALC4001", "CALC4002", "CALC4003", "CALC4004", "CALC4005", "CALC4013",
    "CALC4021", "CALC4022", "CALC4023", "CALC4024", "CALC4025", "CALC4026", "CALC4027", "CALC4028", "CALC4029",
    "CALC4030", "CALC4031", "CALC4032", "CALC4033", "CALC4034", "CALC4035", "CALC4036", "CALC4037", "CALC4038",
    "CALC4039",
)  # fmt: skip
# Text items (grant, project and event ids, the training provider's name, the state); the rest are numbers.
TEXT_ITEMS = (
    "PIRL105", "PIRL106", "PIRL107", "PIRL912", "PIRL919", "PIRL934", "PIRL936", "PIRL938", "PIRL1301", "PIRL2003",
    "CALC4000",
)  # fmt: skip
# Dates (YYYYMMDD), shipped as datetimes.
DATE_ITEMS = (
    "PIRL304", "PIRL306", "PIRL410", "PIRL900", "PIRL901", "PIRL906", "PIRL933",
    "PIRL1000", "PIRL1001", "PIRL1003", "PIRL1004", "PIRL1005", "PIRL1006",
    "PIRL1102", "PIRL1104", "PIRL1105", "PIRL1106", "PIRL1107", "PIRL1108", "PIRL1109", "PIRL1110", "PIRL1111",
    "PIRL1113", "PIRL1116", "PIRL1200", "PIRL1201", "PIRL1202", "PIRL1203", "PIRL1206", "PIRL1207", "PIRL1210",
    "PIRL1213", "PIRL1214", "PIRL1215", "PIRL1216", "PIRL1217", "PIRL1218", "PIRL1219", "PIRL1220", "PIRL1221",
    "PIRL1222", "PIRL1302", "PIRL1308", "PIRL1309", "PIRL1313", "PIRL1314", "PIRL1318",
    "PIRL1402", "PIRL1403", "PIRL1405", "PIRL1407", "PIRL1408", "PIRL1409", "PIRL1410", "PIRL1411", "PIRL1413",
    "PIRL1414", "PIRL1415", "PIRL1416", "PIRL1501",
    "PIRL1806", "PIRL1807", "PIRL1808", "PIRL1809", "PIRL1810", "PIRL1811", "PIRL1813",
    "PIRL2001", "PIRL2414", "PIRL2516",
)  # fmt: skip
# Numeric items wider than int16: local boards, HVRP grantees, occupation, industry and CIP codes.
WIDE_CODES = (
    "PIRL108A", "PIRL108B", "PIRL108C", "PIRL310", "PIRL311", "PIRL313", "PIRL403", "PIRL404", "PIRL405", "PIRL406",
    "PIRL1305", "PIRL1306", "PIRL1311", "PIRL1316",
)  # fmt: skip

# The frame: the Title I exits (an adult, dislocated-worker or Dislocated Worker Grant funding stream) of 2022 to
# 2024. The prepared file runs to March 2025; those exits leave the frame here (LEAK-24, see the notes).
TITLE_I_STREAMS = ("CALC4001", "CALC4002", "CALC4004")
LAST_EXIT = 20250101
# Territories whose wage records are not matched: SPRA wrote every outcome as 0 (Appendix B, PIRL 1704).
NO_WAGE_RECORDS = ("AS", "PW")
# The person's history (USE-10): the encrypted ids of these states mostly do not link across the files (Texas 22.1%
# from PY 2024 Q4 to PY 2025 Q3, Utah 63.7% from PY 2023 Q4 to PY 2024 Q4; Rhode Island 81.7%, the Northern Mariana
# Islands 74.8%, every other state 92.8% or more), and an exit of 2022 has no exit four quarters back in the files, so
# no earlier exit found there is "Unknown".
UNLINKED_IDS = ("TX", "UT")
FIRST_LOOK_BACK = pd.Timestamp("2023-01-01")

# Service, skill-gain, placement and separation dates that can fall after the exit (a first self-service after the
# exit, a supportive service or mentoring in follow-up, a skill gain reported later, a planned military separation):
# not known at the exit, so missing when later.
MASK_AFTER_EXIT = (
    "PIRL304", "PIRL1000", "PIRL1409", "PIRL1410", "PIRL1806", "PIRL1807", "PIRL1808", "PIRL1809", "PIRL1810",
    "PIRL2516",
)  # fmt: skip
# Numbers: the highest school grade completed (0-12), months with the employer of record, the altered wages of the
# three quarters before entry, the age at entry.
NUMERIC_ITEMS = ("PIRL407", "PIRL412", "PIRL1700", "PIRL1701", "PIRL1702", "CALC4039")

# SEL-1: the grounds a WIOA recipient may not base a service on (29 CFR 38.5, 38.6(b)), and the items that state or
# reveal one, leave the features last, after cleaning, so another choice of the curator edits only these lists.
# Race, Hispanic ethnicity and sex.
RACE_SEX = ("PIRL201", "PIRL210", "PIRL211", "PIRL212", "PIRL213", "PIRL214", "PIRL215")
# Age, and the youth funding, status, programme and service items that reveal an age band (WIOA Youth, Job Corps and
# YouthBuild serve ages 14 to 24 or 16 to 24; foster care youth are 24 or under).
AGE_ITEMS = (
    "CALC4039", "CALC4003", "PIRL702", "PIRL704", "PIRL905", "PIRL906", "PIRL911", "PIRL919", "PIRL1402", "PIRL1403",
    "PIRL1405", "PIRL1407", "PIRL1408", "PIRL1410", "PIRL1411", "PIRL1413", "PIRL1414", "PIRL1415", "PIRL1416",
)  # fmt: skip
# Disability, and the items that reveal it (a disabled veteran, SSI or SSDI, vocational rehabilitation, referrals to
# and from the VA's Vocational Rehabilitation and Employment).
DISABILITY_ITEMS = (
    "PIRL202", "PIRL204", "PIRL205", "PIRL206", "PIRL207", "PIRL208", "PIRL209", "PIRL939", "PIRL940",
    "CALC4021", "CALC4022", "CALC4023", "CALC4024", "CALC4025", "CALC4026", "CALC4027", "CALC4028", "CALC4029",
    "PIRL303", "PIRL602", "PIRL917", "PIRL1006", "PIRL1115", "PIRL3007",
)  # fmt: skip
# Pregnancy (sex includes it, 29 CFR 38.7) and limited English (national origin includes it, 38.9).
PREGNANCY_LEP_ITEMS = ("PIRL701", "PIRL803", "PIRL1207")
# Codes of a kept item that reveal a ground, merged into a neighbouring code: disability programmes (922 code 2) into
# other programmes, wounded, ill or injured (1114 code 3) into other reasons, and the WIOA Youth work experiences
# (1205 code 1, a summer job or internship; code 5, youth on-the-job training) into their general codes.
GROUND_CODES = {"PIRL922": {2: 1}, "PIRL1114": {3: 4}, "PIRL1205": {1: 2, 5: 7}}

# The record layout's element names, shortened, with the item number kept so each column can be looked up.
NAMES = {
    "PIRL105": "pirl105_special_project_id_1",
    "PIRL106": "pirl106_special_project_id_2",
    "PIRL107": "pirl107_special_project_id_3",
    "PIRL108A": "pirl108a_local_board_1st",
    "PIRL108B": "pirl108b_local_board_2nd",
    "PIRL108C": "pirl108c_local_board_3rd",
    "PIRL201": "pirl201_sex",
    "PIRL202": "pirl202_disability",
    "PIRL204": "pirl204_disability_sdda_services",
    "PIRL205": "pirl205_disability_lsmha_services",
    "PIRL206": "pirl206_disability_medicaid_hcbs_services",
    "PIRL207": "pirl207_disability_work_setting",
    "PIRL208": "pirl208_disability_customized_employment_services",
    "PIRL209": "pirl209_disability_financial_capability_services",
    "PIRL210": "pirl210_hispanic_latino",
    "PIRL211": "pirl211_american_indian_alaska_native",
    "PIRL212": "pirl212_asian",
    "PIRL213": "pirl213_black_african_american",
    "PIRL214": "pirl214_native_hawaiian_pacific_islander",
    "PIRL215": "pirl215_white",
    "PIRL300": "pirl300_veteran",
    "PIRL301": "pirl301_eligible_veteran_status",
    "PIRL302": "pirl302_campaign_veteran",
    "PIRL303": "pirl303_disabled_veteran",
    "PIRL304": "pirl304_date_military_separation",
    "PIRL305": "pirl305_transitioning_service_member",
    "PIRL306": "pirl306_date_covered_person_entry",
    "PIRL307": "pirl307_tap_workshop_prior_3_years",
    "PIRL309": "pirl309_hvrp_participant",
    "PIRL310": "pirl310_hvrp_grantee_1",
    "PIRL311": "pirl311_hvrp_grantee_2",
    "PIRL312": "pirl312_hvrp_reason_grantee_2",
    "PIRL313": "pirl313_hvrp_grantee_3",
    "PIRL314": "pirl314_hvrp_reason_grantee_3",
    "PIRL315": "pirl315_other_significant_barrier",
    "PIRL316": "pirl316_active_duty_military_spouse",
    "PIRL400": "pirl400_employment_status_at_entry",
    "PIRL402": "pirl402_long_term_unemployed_at_entry",
    "PIRL403": "pirl403_occupation_prior_employment",
    "PIRL404": "pirl404_industry_1st_quarter_prior",
    "PIRL405": "pirl405_industry_2nd_quarter_prior",
    "PIRL406": "pirl406_industry_3rd_quarter_prior",
    "PIRL407": "pirl407_highest_school_grade_at_entry",
    "PIRL408": "pirl408_highest_education_level_at_entry",
    "PIRL409": "pirl409_school_status_at_entry",
    "PIRL410": "pirl410_date_actual_dislocation",
    "PIRL412": "pirl412_tenure_months_at_separation",
    "PIRL413": "pirl413_msfw_designation",
    "PIRL600": "pirl600_tanf",
    "PIRL601": "pirl601_exhausting_tanf_within_2_years",
    "PIRL602": "pirl602_ssi_ssdi",
    "PIRL603": "pirl603_snap",
    "PIRL604": "pirl604_other_public_assistance",
    "PIRL701": "pirl701_pregnant_or_parenting_youth",
    "PIRL702": "pirl702_youth_needs_additional_assistance",
    "PIRL704": "pirl704_foster_care_youth",
    "PIRL800": "pirl800_homeless_at_entry",
    "PIRL801": "pirl801_ex_offender_at_entry",
    "PIRL802": "pirl802_low_income_at_entry",
    "PIRL803": "pirl803_english_language_learner",
    "PIRL804": "pirl804_basic_skills_deficient",
    "PIRL805": "pirl805_cultural_barriers",
    "PIRL806": "pirl806_single_parent",
    "PIRL807": "pirl807_displaced_homemaker",
    "PIRL808": "pirl808_eligible_msfw_status",
    "PIRL900": "pirl900_date_program_entry",
    "PIRL901": "pirl901_date_program_exit",
    "PIRL903": "pirl903_wioa_adult",
    "PIRL904": "pirl904_wioa_dislocated_worker",
    "PIRL905": "pirl905_wioa_youth",
    "PIRL906": "pirl906_date_first_youth_service",
    "PIRL907": "pirl907_incumbent_worker_training",
    "PIRL908": "pirl908_rapid_response",
    "PIRL909": "pirl909_rapid_response_additional_assistance",
    "PIRL910": "pirl910_adult_education",
    "PIRL911": "pirl911_job_corps",
    "PIRL912": "pirl912_nfjp_grant",
    "PIRL913": "pirl913_indian_native_american_programs",
    "PIRL914": "pirl914_veterans_programs",
    "PIRL916": "pirl916_vocational_education",
    "PIRL917": "pirl917_vocational_rehabilitation",
    "PIRL918": "pirl918_wagner_peyser",
    "PIRL919": "pirl919_youthbuild_grant",
    "PIRL921": "pirl921_snap_employment_training",
    "PIRL922": "pirl922_other_programs",
    "PIRL930": "pirl930_pay_for_performance",
    "PIRL931": "pirl931_registered_apprenticeship",
    "PIRL932": "pirl932_national_dwg",
    "PIRL933": "pirl933_date_first_dwg_service",
    "PIRL934": "pirl934_rapid_response_event",
    "PIRL935": "pirl935_accountability_exit_status",
    "PIRL936": "pirl936_reentry_employment_adult_grant",
    "PIRL938": "pirl938_h1b_grant",
    "PIRL939": "pirl939_disability_iep",
    "PIRL940": "pirl940_disability_section_504_plan",
    "PIRL1000": "pirl1000_date_first_self_service",
    "PIRL1001": "pirl1001_date_first_staff_assisted_service",
    "PIRL1003": "pirl1003_date_last_staff_assisted_basic_service",
    "PIRL1004": "pirl1004_date_last_career_service",
    "PIRL1005": "pirl1005_date_last_dvop_staff_assisted_service",
    "PIRL1006": "pirl1006_date_referred_va_vre",
    "PIRL1102": "pirl1102_date_last_career_guidance",
    "PIRL1104": "pirl1104_date_last_job_search_assistance",
    "PIRL1105": "pirl1105_date_last_referred_to_employment",
    "PIRL1106": "pirl1106_date_last_referred_federal_training",
    "PIRL1107": "pirl1107_date_last_placed_federal_training",
    "PIRL1108": "pirl1108_date_last_referred_federal_job",
    "PIRL1109": "pirl1109_date_last_referred_federal_contractor_job",
    "PIRL1110": "pirl1110_date_last_entered_federal_job",
    "PIRL1111": "pirl1111_date_last_entered_federal_contractor_job",
    "PIRL1113": "pirl1113_date_last_referred_other_assistance",
    "PIRL1114": "pirl1114_referred_to_jvsg",
    "PIRL1115": "pirl1115_referred_to_va_services",
    "PIRL1116": "pirl1116_date_last_other_staff_assisted_service",
    "PIRL1200": "pirl1200_date_first_individualized_service",
    "PIRL1201": "pirl1201_date_last_individualized_service",
    "PIRL1202": "pirl1202_date_employment_plan_created",
    "PIRL1203": "pirl1203_date_last_internship_work_experience",
    "PIRL1205": "pirl1205_type_of_work_experience",
    "PIRL1206": "pirl1206_date_financial_literacy_services",
    "PIRL1207": "pirl1207_date_esl_services",
    "PIRL1210": "pirl1210_date_pre_vocational_activities",
    "PIRL1211": "pirl1211_transitional_job",
    "PIRL1213": "pirl1213_date_last_dvop_individualized_service",
    "PIRL1214": "pirl1214_date_last_dvop_job_search",
    "PIRL1215": "pirl1215_date_last_dvop_referred_to_employment",
    "PIRL1216": "pirl1216_date_last_dvop_referred_federal_training",
    "PIRL1217": "pirl1217_date_last_dvop_referred_federal_job",
    "PIRL1218": "pirl1218_date_last_dvop_referred_federal_contractor_job",
    "PIRL1219": "pirl1219_date_last_dvop_other_basic_service",
    "PIRL1220": "pirl1220_date_last_dvop_career_guidance",
    "PIRL1221": "pirl1221_date_last_dvop_entered_federal_job",
    "PIRL1222": "pirl1222_date_last_dvop_entered_federal_contractor_job",
    "PIRL1300": "pirl1300_received_training",
    "PIRL1301": "pirl1301_training_provider_name",
    "PIRL1302": "pirl1302_date_entered_training_1",
    "PIRL1303": "pirl1303_training_type_1",
    "PIRL1305": "pirl1305_training_provider_cip_code",
    "PIRL1306": "pirl1306_training_occupation_code_1",
    "PIRL1307": "pirl1307_training_completed_1",
    "PIRL1308": "pirl1308_date_completed_or_withdrew_training_1",
    "PIRL1309": "pirl1309_date_entered_training_2",
    "PIRL1310": "pirl1310_training_type_2",
    "PIRL1311": "pirl1311_training_occupation_code_2",
    "PIRL1312": "pirl1312_training_completed_2",
    "PIRL1313": "pirl1313_date_completed_or_withdrew_training_2",
    "PIRL1314": "pirl1314_date_entered_training_3",
    "PIRL1315": "pirl1315_training_type_3",
    "PIRL1316": "pirl1316_training_occupation_code_3",
    "PIRL1317": "pirl1317_training_completed_3",
    "PIRL1318": "pirl1318_date_completed_or_withdrew_training_3",
    "PIRL1319": "pirl1319_individual_training_account",
    "PIRL1320": "pirl1320_pell_grant_recipient",
    "PIRL1328": "pirl1328_training_virtual_online",
    "PIRL1332": "pirl1332_postsecondary_education_during_program",
    "PIRL1333": "pirl1333_training_by_private_sector",
    "PIRL1401": "pirl1401_enrolled_secondary_education",
    "PIRL1402": "pirl1402_date_last_educational_achievement_services",
    "PIRL1403": "pirl1403_date_last_alternative_secondary_school",
    "PIRL1405": "pirl1405_date_last_youth_work_experience",
    "PIRL1407": "pirl1407_date_last_education_with_workforce_prep",
    "PIRL1408": "pirl1408_date_last_leadership_development",
    "PIRL1409": "pirl1409_date_last_supportive_services",
    "PIRL1410": "pirl1410_date_last_adult_mentoring",
    "PIRL1411": "pirl1411_date_last_guidance_counseling",
    "PIRL1413": "pirl1413_date_last_youth_entrepreneurial_training",
    "PIRL1414": "pirl1414_date_last_youth_labor_market_information",
    "PIRL1415": "pirl1415_date_last_youth_postsecondary_preparation",
    "PIRL1416": "pirl1416_date_completion_youth_services",
    "PIRL1500": "pirl1500_needs_related_payments",
    "PIRL1501": "pirl1501_date_last_rapid_response_services",
    "PIRL1700": "pirl1700_wages_3rd_quarter_before_entry",
    "PIRL1701": "pirl1701_wages_2nd_quarter_before_entry",
    "PIRL1702": "pirl1702_wages_1st_quarter_before_entry",
    "PIRL1806": "pirl1806_date_last_skill_gain_efl",
    "PIRL1807": "pirl1807_date_last_skill_gain_postsecondary_transcript",
    "PIRL1808": "pirl1808_date_last_skill_gain_secondary_transcript",
    "PIRL1809": "pirl1809_date_last_skill_gain_training_milestone",
    "PIRL1810": "pirl1810_date_last_skill_gain_skills_progression",
    "PIRL1811": "pirl1811_date_enrolled_credential_program",
    "PIRL1812": "pirl1812_school_status_at_exit",
    "PIRL1813": "pirl1813_date_completed_credential_program",
    "PIRL2001": "pirl2001_date_completion_dwg_services",
    "PIRL2003": "pirl2003_dwg_grant",
    "PIRL2004": "pirl2004_disaster_recovery_dwg",
    "PIRL2413": "pirl2413_incarcerated_at_entry",
    "PIRL2414": "pirl2414_date_released_from_incarceration",
    "PIRL2516": "pirl2516_date_postsecondary_placement",
    "PIRL3004": "pirl3004_individualized_services_virtual",
    "PIRL3005": "pirl3005_tsm_warm_handover",
    "PIRL3006": "pirl3006_tsm_housing_plan",
    "PIRL3007": "pirl3007_referred_from_va",
    "CALC4000": "state",
    "CALC4001": "calc4001_adult_funding_stream",
    "CALC4002": "calc4002_dislocated_worker_funding_stream",
    "CALC4003": "calc4003_youth_funding_stream",
    "CALC4004": "calc4004_dislocated_worker_grant",
    "CALC4005": "calc4005_wagner_peyser",
    "CALC4013": "employed_2nd_quarter_after_exit",
    "CALC4021": "calc4021_no_disability",
    "CALC4022": "calc4022_physical_chronic_health_condition",
    "CALC4023": "calc4023_physical_mobility_impairment",
    "CALC4024": "calc4024_mental_or_psychiatric_disability",
    "CALC4025": "calc4025_vision_related_disability",
    "CALC4026": "calc4026_hearing_related_disability",
    "CALC4027": "calc4027_learning_disability",
    "CALC4028": "calc4028_cognitive_intellectual_disability",
    "CALC4029": "calc4029_disability_type_not_disclosed",
    "CALC4030": "calc4030_study_toward_industry_certificate",
    "CALC4031": "calc4031_study_toward_apprenticeship_certificate",
    "CALC4032": "calc4032_study_toward_license",
    "CALC4033": "calc4033_study_toward_associate_degree",
    "CALC4034": "calc4034_study_toward_baccalaureate_degree",
    "CALC4035": "calc4035_study_toward_community_college_certificate",
    "CALC4036": "calc4036_study_toward_secondary_diploma",
    "CALC4037": "calc4037_study_toward_employment",
    "CALC4038": "calc4038_study_toward_skill_gain",
    "CALC4039": "age_at_entry",
}

# The words the record layout gives each code (PIRL 2021 schema, PY 2025 Q3 layout, Appendix A). Pure 0/1 flags keep
# 0/1 (CLEAN-14); these items have codes beyond them. The items that leave under SEL-1 keep their words here too.
YES_NO_UNDISCLOSED = {1: "Yes", 0: "No", 9: "Did not self-identify"}
YES_NO_UNKNOWN = {1: "Yes", 0: "No", 9: "Unknown"}
FUNDING = {1: "Yes, local formula", 2: "Yes, statewide", 3: "Yes, local formula and statewide", 0: "No"}
HVRP_REASON = {
    1: "Grantee no longer a DOL grantee",
    2: "Services did not meet needs",
    3: "Left the grantee's service area",
    4: "Lost touch with the counselor",
}
TRAINING_TYPE = {
    1: "On-the-job training",
    2: "Skill upgrading",
    3: "Entrepreneurial training",
    4: "ABE or ESL with training",
    5: "Customized training",
    6: "Occupational skills training",
    7: "ABE or ESL without training (TAA)",
    8: "Prerequisite training",
    9: "Registered apprenticeship",
    10: "Youth occupational skills training",
    11: "Other non-occupational-skills training",
    12: "Job readiness training with other training",
    0: "No training service",
}
SCHOOL_STATUS = {
    1: "In school, secondary or less",
    2: "In school, alternative school",
    3: "In school, postsecondary",
    4: "Not attending, no diploma (dropout)",
    5: "Not attending, secondary graduate or equivalent",
    6: "Not attending, within compulsory school age",
}
# The delivery mode, an ordered scale from in person to virtual (CLEAN-14).
VIRTUAL = {1: "Virtual or online", 2: "Mix of in-person and virtual", 0: "In-person only"}
VIRTUAL_ORDER = ("In-person only", "Mix of in-person and virtual", "Virtual or online")
CODE_LABELS = {
    "PIRL202": YES_NO_UNDISCLOSED,
    "PIRL207": {
        1: "Competitive integrated employment",
        2: "Individual supported employment",
        3: "Group supported employment",
        4: "Sheltered workshop",
        5: "Two or more settings",
        0: "Not employed",
    },
    "PIRL208": {
        1: "Discovery assessment",
        2: "Customized employment search plan",
        3: "Employer negotiation",
        4: "Secured customized employment with extended support",
        0: "No customized employment services",
    },
    "PIRL209": {1: "Benefit planning", 2: "Financial capability or asset development", 3: "Both", 0: "No"},
    "PIRL301": {1: "Yes, 180 days or less", 2: "Yes, eligible veteran", 3: "Yes, other eligible person", 0: "No"},
    "PIRL303": {1: "Yes", 2: "Yes, special disabled", 0: "No"},
    "PIRL312": HVRP_REASON,
    "PIRL314": HVRP_REASON,
    "PIRL400": {
        1: "Employed",
        2: "Employed, but notice of termination or military separation pending",
        3: "Not in labor force",
        0: "Unemployed",
    },
    "PIRL408": {
        1: "Secondary school diploma",
        2: "Secondary school equivalency",
        3: "IEP certificate of attendance or completion",
        4: "One or more years of postsecondary education",
        5: "Postsecondary technical or vocational certificate",
        6: "Associate's degree",
        7: "Bachelor's degree",
        8: "Degree beyond a bachelor's",
        0: "No educational level completed",
    },
    "PIRL409": SCHOOL_STATUS,
    "PIRL413": {1: "Seasonal farmworker", 2: "Migrant", 0: "No"},
    "PIRL601": {1: "Yes", 0: "No", 9: "Not applicable"},
    "PIRL602": {
        1: "SSI",
        2: "SSDI",
        3: "SSI and SSDI",
        4: "SSI and ticket holder",
        5: "SSDI and ticket holder",
        6: "SSI, SSDI and ticket holder",
        0: "No",
    },
    "PIRL808": {
        1: "Seasonal farmworker adult",
        2: "Migrant farmworker adult",
        3: "MSFW youth",
        4: "Dependent adult",
        5: "Dependent youth",
        0: "No",
    },
    "PIRL903": FUNDING,
    "PIRL904": FUNDING,
    "PIRL905": FUNDING,
    "PIRL907": {
        1: "Statewide or rapid response funds only",
        2: "Local formula only",
        3: "Statewide and local formula",
        4: "H-1B grant",
        5: "DWG grant",
        6: "NFJP grant",
        0: "No",
    },
    "PIRL908": YES_NO_UNKNOWN,
    "PIRL909": YES_NO_UNKNOWN,
    "PIRL911": {1: "Yes", 2: "Reportable individual", 0: "No", 9: "Unknown"},
    "PIRL914": {1: "Yes, DVOP specialist", 2: "Yes, LVER specialist", 0: "No", 9: "Unknown"},
    "PIRL916": YES_NO_UNKNOWN,
    "PIRL917": {1: "Yes, VR", 2: "VR&E", 3: "Both VR and VR&E", 0: "No", 9: "Unknown"},
    "PIRL918": {1: "Yes", 2: "Reportable individual", 0: "No"},
    "PIRL922": {1: "Yes, other WIOA or non-WIOA programs", 2: "I/DD, MH or other disability programs", 0: "No"},
    "PIRL932": {1: "Yes, NDWG participant", 2: "Reportable individual", 0: "No"},
    "PIRL935": {1: "Invalid or undisclosed SSN", 2: "Retirement", 3: "TAA under a later petition", 0: "None of these"},
    "PIRL939": {1: "Current IEP", 2: "Previous IEP", 0: "Neither"},
    "PIRL1114": {
        1: "Significant barrier to employment",
        2: "TSM in need of individualized career services",
        3: "Wounded, ill or injured, or caretaker",
        4: "Other",
        0: "Not referred",
    },
    "PIRL1115": {
        1: "VR&E",
        2: "Post 9/11 GI Bill",
        3: "Montgomery GI Bill",
        4: "Post 9/11 and Montgomery GI Bill",
        5: "Other VA services",
    },
    "PIRL1205": {
        1: "Summer employment or internship",
        2: "Employment opportunity or internship",
        3: "Pre-apprenticeship",
        4: "Job shadowing",
        5: "On-the-job training (youth)",
        6: "Transitional job",
        7: "Other work experience",
        0: "Did not participate",
    },
    "PIRL1303": TRAINING_TYPE,
    "PIRL1310": TRAINING_TYPE,
    "PIRL1315": TRAINING_TYPE,
    "PIRL1328": VIRTUAL,
    "PIRL1812": SCHOOL_STATUS,
    "PIRL2004": {
        1: "Disaster relief employment only",
        2: "Disaster relief employment and training services",
        3: "Employment and training services only",
        0: "No",
    },
    "PIRL3004": VIRTUAL,
    "PIRL3005": {
        1: "Yes, sent to the AJC by a military officer",
        2: "Yes, visited the AJC on own accord",
        3: "No, information not provided",
        0: "Not a TSM",
    },
    "PIRL3006": {1: "Yes, adequate housing plan", 2: "No adequate housing plan", 0: "Not a TSM"},
    "PIRL3007": {
        1: "VA VR&E, for labor market information",
        2: "VA VR&E, for employment services",
        3: "VA regional office",
        4: "VA medical center",
        5: "VA vocational rehabilitation funded",
        9: "VA, entity unknown",
    },
}
# Codes the layout does not list for an item: invalid, set to missing (CLEAN-11; counts in the README decision).
UNDOCUMENTED_CODES = {
    "PIRL301": [9],
    "PIRL302": [9],
    "PIRL303": [9],
    "PIRL316": [2],
    "PIRL402": [2],
    "PIRL907": [7],
    "PIRL1114": [5],
}
# Codes that only mean unknown (did not disclose or self-identify, status not known, the grantee cannot track
# enrollment) in items with no other blank: set to missing, which loses nothing (CLEAN-10). Where a blank means the
# item does not apply (PIRL 908, 909, 914, 916), "Unknown" stays a level of its own.
UNKNOWN_ONLY = {
    "PIRL300": [9],
    "PIRL801": [9],
    "PIRL805": [9],
    "PIRL806": [9],
    "PIRL910": [9],
    "PIRL918": [9],
    "PIRL932": [9],
}
# The months with the employer of record: 999 (83 years) is a fill (CLEAN-11).
TENURE_FILL = {"PIRL412": [999]}


def _decode_codes(df: pd.DataFrame, labels: dict) -> pd.DataFrame:
    """`decode`, vectorised for millions of rows: a code without a label raises, a missing value stays missing."""
    for col, mapping in labels.items():
        values = df[col].astype("float64")
        unlabelled = sorted(set(values.dropna().unique()) - {float(k) for k in mapping})
        if unlabelled:
            raise ValueError(f"Codes of {col!r} without a label: {unlabelled[:10]}")
        df[col] = values.map({float(k): v for k, v in mapping.items()}).astype("category")
    return df


def _to_dates(values: pd.Series) -> pd.Series:
    """YYYYMMDD numbers to datetimes; an impossible date becomes missing."""
    v = values.astype("float64")
    return pd.to_datetime(pd.DataFrame({"year": v // 10000, "month": v // 100 % 100, "day": v % 100}), errors="coerce")


def _quarter(dates: pd.Series) -> pd.Series:
    """A running quarter number (year * 4 + quarter - 1)."""
    return dates.dt.year * 4 + (dates.dt.month - 1) // 3


def _population(raw: pd.DataFrame) -> pd.Series:
    """The frame's rows: Title I exits before 2025, outside the territories without wage records."""
    title_i = (raw[list(TITLE_I_STREAMS)] == 1).fillna(False).any(axis=1)
    in_frame = (raw["PIRL901"] < LAST_EXIT).fillna(False)
    no_wages = raw["CALC4000"].isin(NO_WAGE_RECORDS).fillna(False)
    return title_i & in_frame & ~no_wages


def _previous_known_outcome(raw: pd.DataFrame, windows: TemporalSplits) -> pd.DataFrame:
    """The outcome of each person's latest exit at least four quarters before the row's exit quarter (USE-10).

    The person is the state and the encrypted id (PIRL 100), looked up in every exit of the prepared files. The
    outcome quarter of an exit four quarters back ended two quarters before the row's quarter, so the state's own wage
    records hold it at the row's exit; a nearer exit's outcome is not known yet. Raises when a row reads a nearer exit
    or a test row reads an exit in its gap or later.
    """
    exit_date = _to_dates(raw["PIRL901"])
    quarter = _quarter(exit_date)
    look_back = quarter - 3  # an earlier exit counts when it falls before the first day of this quarter
    look_back_end = pd.to_datetime(pd.DataFrame({"year": look_back // 4, "month": look_back % 4 * 3 + 1, "day": 1}))
    person = raw["CALC4000"].astype(str) + "|" + raw["PIRL100"].astype(str)
    rows = pd.DataFrame({"person": person, "look_back_end": look_back_end, "row": np.arange(len(raw))})
    exits = pd.DataFrame({"person": person, "previous_exit": exit_date, "previous": raw["CALC4013"].astype("float64")})
    found = pd.merge_asof(
        rows.sort_values("look_back_end", kind="stable"),
        exits.sort_values("previous_exit", kind="stable"),
        left_on="look_back_end",
        right_on="previous_exit",
        by="person",
        allow_exact_matches=False,
    ).sort_values("row", kind="stable")
    previous_exit = pd.Series(found["previous_exit"].to_numpy(), index=raw.index)
    previous = pd.Series(found["previous"].to_numpy(), index=raw.index)
    known = previous_exit.notna()
    since = (quarter - _quarter(previous_exit)).where(known)
    if (since[known] < 4).any():
        raise AssertionError("The previous known outcome reads an exit less than four quarters back.")
    step, gap = {windows.unit: windows.window}, {windows.unit: windows.gap}
    for cutoff in windows.cutoffs:
        start = pd.Timestamp(cutoff)
        in_window = (exit_date >= start) & (exit_date < start + pd.DateOffset(**step))
        if (previous_exit[in_window & known] >= start - pd.DateOffset(**gap)).any():
            raise AssertionError(f"A test row of the window from {cutoff} reads an exit in its gap or later.")
    unreadable = (raw["CALC4000"].isin(UNLINKED_IDS).fillna(False) | (exit_date < FIRST_LOOK_BACK)).to_numpy(bool)
    value = np.select(
        [(known & (previous == 1)).to_numpy(bool), (known & (previous == 0)).to_numpy(bool), unreadable],
        ["Yes", "No", "Unknown"],
        default="No earlier exit",
    )
    return pd.DataFrame(
        {"previous_known_outcome": value, "quarters_since_previous_exit": since.astype("float64")}, index=raw.index
    )


def _present(df: pd.DataFrame, items: tuple | dict) -> list[str]:
    """The shipped names of the items still in the frame."""
    return [NAMES[c] for c in items if NAMES[c] in df.columns]


class WioaEmploymentAfterExit(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "Will a person leaving a US public workforce programme (WIOA Title I adult, dislocated-worker or "
            "Dislocated Worker Grant services) be employed in the second calendar quarter after the quarter of exit?"
        ),
        use_case=(
            "For example, a WIOA Title I case manager or local workforce board, when a participant's last planned "
            "service is given, estimates the chance of employment in the second quarter after exit, to decide whom to "
            "keep in services or offer the twelve months of follow-up."
        ),
        row=(
            "One exit of one person (a period of participation) with Title I adult, dislocated-worker or Dislocated "
            "Worker Grant funding in DOL's WIOA public use files, exits from January 2022 to December 2024 in the "
            "cohort of DOL's second-quarter employment rate."
        ),
        predicted=(
            "Whether the person had unsubsidized employment in the second quarter after the exit quarter, mostly from "
            "state unemployment insurance wage records."
        ),
        known=(
            "What was recorded at entry (barriers, education, prior employment and altered prior wages), the "
            "programmes and funding streams, the services and training up to the last service, and the outcome of "
            "the person's exit a year or more before, if any."
        ),
        split=(
            "Each test window is one quarter of exits (April to December 2024); training is the exits up to nine "
            "months before it, whose outcome the state's own wage records hold when the window starts."
        ),
        changes=(
            "We combine three quarterly files, keep the Title I exits in DOL's employment-rate cohort, drop every "
            "item recorded after the exit and the items on race, ethnicity, sex, age and disability with those that "
            "reveal them, blank service dates after the exit, and add the person's previous known outcome."
        ),
        fit="approximate",
        fit_reason=(
            "DOL scores states on this outcome and decides on state aggregates; the per-person follow-up decision is "
            "ours. The file lacks whether the person was placed in a job at closure and the UI claimant status, which "
            "a case manager has, and its prior wages and codes were altered for disclosure control."
        ),
    )

    # Dataset
    unique_name = "wioa_employment_after_exit"
    year = "2026"
    domain = "social science"
    source = "GOV Website"
    source_url = "https://www.dol.gov/agencies/eta/performance/results/national"
    license = (
        "Public domain (US Government work); DOL ETA's disclaimer makes receipt of the data an agreement to use it "
        "for valid research purposes only, not to identify any individual, and to suppress published summaries of "
        "fewer than 3 individuals"
    )
    data_tags = ("Spatial",)
    download_description = """
        The WIOA Individual Performance Records public use files of the US Department of Labor, Employment and Training Administration (no login): PY 2025 Q3 from the national results page, PY 2024 Q4 and PY 2023 Q4 from its Performance Data Archive page (https://www.dol.gov/node/167922). The PY 2023 Q4 link ends in .csv and serves the unzipped CSV (5.4 GB).

        mkdir -p local-data-warehouse/wioa_employment_after_exit && cd local-data-warehouse/wioa_employment_after_exit
        wget https://www.dol.gov/media/WIOAPUDFPY25Q3.parquet
        wget https://www.dol.gov/sites/dolgov/files/ETA/Performance/pdfs/PY2025/WIOAPUDFPY24Q4.parquet
        wget https://www.dol.gov/sites/dolgov/files/ETA/Performance/pdfs/PY2023/Q4/WIOAPerformanceRecords_PY2023Q4_PUBLIC.csv
        wget "https://www.dol.gov/sites/dolgov/files/ETA/Performance/pdfs/PY2025/WIOA%20Performance%20Records%20Public%20Use%20File%20Record%20Layout%20PY2025Q3.pdf"
        wget "https://www.dol.gov/sites/dolgov/files/ETA/Performance/pdfs/PY2025/WIOA%20Performance%20Records%20Public%20Use%20File%20Disclaimer_PY2025.pdf"

        The first run writes wioa_exiters_q2_employment.parquet next to them (`_prepare_raw_files`: the matured exits of each file's range, all programmes).
    """
    bibtex = """
        @misc{dol_eta_wioa_performance_records_2026,
          title = {{WIOA} Individual Performance Records (Public Use File), {PY} 2023 {Q4}, {PY} 2024 {Q4} and {PY} 2025 {Q3}},
          author = {{U.S. Department of Labor, Employment and Training Administration}},
          year = {2026},
          howpublished = {\\url{https://www.dol.gov/agencies/eta/performance/results/national}},
          note = {Record layout: PY 2025 Q3 WIOA Performance Records Public Use File, Social Policy Research Associates, July 2026}
        }
    """
    curation_comments = """
        We start with three WIOA Individual Performance Records public use files of DOL ETA (PIRL items; record layout by Social Policy Research Associates, SPRA): PY 2023 Q4 (report quarter ending 2024-06-30), PY 2024 Q4 (2025-06-30) and PY 2025 Q3 (2026-03-31).

        - Prediction point: the last planned service of a Title I participant, when the case manager closes the case. The exit (PIRL 901: the last service that is not self-service, information-only or follow-up) is recorded once 90 days pass with no service and none planned, and is then dated back to that service (20 CFR 677.150(c)). Everything recorded at entry or during participation up to that day is known; every outcome after it is not.
        - Population: the Title I exits in DOL's second-quarter employment-rate cohort (CALC 4013 not blank: no reportable individuals, and none of the PIRL 923 exclusions such as institutionalised, medical or deceased exits, which are DOL's own denominator) with an adult, dislocated-worker or Dislocated Worker Grant funding stream (CALC 4001, 4002 or 4004). Follow-up services exist only for adult and dislocated-worker participants placed in employment (20 CFR 678.430(c), 680.150(c)); no Wagner-Peyser-only exit of PY 2025 Q3 carries a follow-up date. So the 6,425,103 cohort exits served only by Wagner-Peyser, veterans' or youth programmes leave (USE-1, USE-5; the 149,880 exits served only by youth funds are scored by DOL's Youth indicator, which counts education too). Kept: 1,023,443 exits of 2022 to 2024 (employment rate 0.719): 587,312 with adult, 474,777 with dislocated-worker and 44,472 with DWG funding; 715,100 also had Wagner-Peyser services.
        - Files: each file holds a rolling ten quarters and fills the outcome only for exits up to four quarters before its report quarter (SPRA: "Set to blank outcomes when it was too soon to report complete data"). We take the exits of 2022 from PY 2023 Q4, January to September 2023 from PY 2024 Q4 and October 2023 on from PY 2025 Q3, so each exit comes from the newest file that holds its outcome and no exit is taken twice. Where two files hold the same matured quarter the newer one revises it a little (all programmes, October 2023 to June 2024: 13,986 of 1,642,717 matched exits changed their label, 9,344 to employed). Older files on the archive page are left out: 12 quarters give three quarterly windows with the gap and more than half the rows in training.
        - Newest exits (LEAK-24): the prepared file runs to March 2025, but January to March 2025 (74,729 Title I exits) leave the frame. Their labels are DOL's first report, which later reports revise (Title I rate +0.01 to +0.72 points from the first report to the second), and Texas's wage records for calendar 2025Q3 were incomplete in PY 2025 Q3: its 2025Q1 exits read 0.398 employed in the second quarter after exit against 0.623 in the first, where every other state-quarter differs by at most a few points (SPRA's Appendix B writes "not yet available" as 0 once data are due). The test windows now hold their exits at DOL's second (October to December 2024), third and fourth report; on July to September 2024 the second report scored within 0.0002 ROC AUC of the third. Leak probe 13 still flags a mild rise of the rate of No over the newest four months pooled (z +3.2, no single month out of band): the drift of the rate (0.747 in 2022Q1, 0.700 in 2023Q4, 0.689 in 2024Q4) plus at most the second report's lag on October to December 2024 (about 0.5 points of rate, all programmes). Revisit with PY 2025 Q4, which brings January to March 2025 to its second report: move the windows forward a quarter if Texas's 2025Q3 wages are complete there.
        - Dropped: the 98 Title I exits of American Samoa (all not employed) and those of Palau (none left): Appendix B, PIRL 1704, "State reported no wages in the 2nd quarter after exit quarter ... All records were '0'", so their label records missing wage records, not employment (LEAK-39, LEAK-25).
        - Target: `employed_2nd_quarter_after_exit`, "Yes" when PIRL 1602 is 1. SPRA set it to 1 when wages in the quarter were above 0, and treated a missing or "not yet available" code as 0 once complete data were expected (Appendix B). The layout says the codes of PIRL 1600-1607 are "modified to avoid disclosing the data source"; on the PY 2025 Q3 cohort PIRL 1602 equals CALC 4013 on every row and is 1 exactly when the quarter's wages are above 0, except 45 of 2.44M employed rows (supplemental sources), so it keeps its 0/1 meaning.
        - Dropped as recorded after the exit (LEAK-10): employment, wages, occupation and industry in the quarters after exit (PIRL 1600-1618, 1703-1706), credentials (1800-1805, attainable up to a year after exit; 1814), youth placement (1900, 1901), post-exit education (1406), follow-up services (1412, 1503), employment at completion of a DWG (2002, counted over the whole exit quarter) and the calculated outcome items (CALC 4014-4019).
        - Dropped: the most recent dates of self-service, information-only and workforce-information services and of reportable-individual contact (PIRL 1002, 1100, 1101, 1103, 1007). These do not extend participation, so on the PY 2025 Q3 cohort (all programmes) the dates fall after the exit for 699k, 194k, 494k, 173k and 235k of 3.68M rows; blanking them would leave a date missing exactly when the person came back after the exit (the first self-service date, PIRL 1000, still says whether they used it before). A date after the exit carries next to no signal alone (ROC AUC 0.499 to 0.500 for each column's flag), so the drop is for the timing (LEAK-10) and costs little.
        - Dates later than the exit date are set to missing (PIRL 1000, 1409, 1410, 1806-1810, 2516, and the military separation date 304, a planned separation for 496 exits; counts in the decision below): a first self-service, a supportive service or mentoring in follow-up, a skill gain or a placement reported after the exit is not known at the exit.
        - Dropped as identifiers or copies: the encrypted person id (PIRL 100, used for the person's history below), the program year of exit (CALC 4040, from the exit date), the single-response race (CALC 4020), the category of disability (PIRL 203, spelled out by CALC 4021-4029), the reportable-individual flag and PIRL 923 (constant on this cohort), the skill-gain items CALC 4007-4012 (empty), PIRL 920 and 937 (only a placeholder) and the second and third HVRP grantees (PIRL 311 and 313, set for 1 exit each; the reasons, 312 and 314, stay). The calculated items that recode one kept item exactly go (CLEAN-5): CALC 4001 (PIRL 903 set), 4005 (PIRL 918 code 1) and 4041 (PIRL 914 code 1 or 2); CALC 4002 (from PIRL 904 or 909) and 4004 (from the DWG grant) differ from their items in 21,983 and 922 exits and stay as DOL's stream assignment.
        - Dropped (SEL-1): race (PIRL 211-215), Hispanic ethnicity (210) and sex (201). The actor is a recipient under WIOA section 188, and 29 CFR 38.6(b) bars it from giving "any aid, benefit, service, or training that is different" on the basis of race, color, religion, sex, national origin, age, disability or political affiliation; DOL's own per-person profiling model for reemployment services may not use age, race, ethnic group, sex, color, national origin or disability (UIPL 41-94). DOL's statistical adjustment model (TEGL 26-15 Attachment II) uses some of them, but on state-quarter aggregates to set state targets, not to allocate a service to a person. Dropping them costs nothing measurable (ROC AUC -0.001 to +0.005).
        - Dropped too, pending the curator's call (issue 1 of the review; SEL-1): age (CALC 4039) and disability (PIRL 202, 204-209, 939, 940, CALC 4021-4029), with the items that state or reveal them: pregnant or parenting youth (701; sex includes pregnancy, 29 CFR 38.7), English learner (803) and ESL services (1207; national origin includes limited English, 38.9), the youth funding, status, programme and service items (CALC 4003, PIRL 702, 704, 905, 906, 911, 919, 1402-1416), and the disability proxies (303 disabled veteran, 602 SSI or SSDI, 917 vocational rehabilitation, the VA VR&E referrals 1006, 1115 and 3007). Four codes of kept items that reveal a ground are merged into a neighbour: PIRL 922 code 2 (disability programmes) into 1, 1114 code 3 (wounded, ill or injured) into 4 ("Other"), and 1205 codes 1 and 5 (WIOA Youth work experience) into 2 and 7. WIOA names older individuals and individuals with disabilities as barrier groups (29 USC 3102(24)), but follow-up eligibility names neither, and a state gives the barrier groups priority by policy, not through a score. Cost on Title I: ROC AUC -0.009 to -0.011, mostly age. Kept: ex-offender status (801, 2413, 2414; a WIOA barrier group, no 29 CFR 38 ground), single parent (806), displaced homemaker (807) and cultural barriers (805), barrier groups that are no ground.
        - Added (USE-10): `previous_known_outcome` (Yes, No, No earlier exit, Unknown) and `quarters_since_previous_exit`, the outcome of the person's latest exit (state and encrypted id, any programme of the cohort) at least four quarters before the row's exit quarter, whose outcome quarter the state's own wage records hold by then; the code raises if a test row reads an exit in its gap or later. The agency knows its returning participants: in the test windows 8.9% to 11.3% of the exits have such an exit, employed at 0.76 to 0.79 after an employed one and 0.52 to 0.55 after one without (0.69 to 0.71 for the others). The ids link across the files at 92.8% or more for every state but Texas (22.1%), Utah (63.7%), the Northern Mariana Islands (74.8%) and Rhode Island (81.7%), so the exits of Texas and Utah with no earlier exit found are "Unknown" (3,105 to 4,411 per test window), as is every exit of 2022, whose look-back lies before the files. On Title I the feature added ROC AUC +0.002 to +0.007 on the returning persons (9 of 9 runs, untuned LightGBM) and nothing measurable over all exits.
        - Coded items are decoded into the layout's words (CLEAN-12); the 0/1 flags stay 0/1 categories (CLEAN-14). Codes the layout does not list for an item are set to missing (CLEAN-11; PIRL 301 code 9 in 8,543 exits, 316 code 2 in 26, 402 code 2 in 509, 907 code 7 in 28, 1114 code 5 in 26); they belong to items the PIRL 2025 schema changed, whose new values SPRA may not have mapped. PIRL 931 (registered apprenticeship) ships its codes as they are: the files hold 4 for most rows and 1-3 otherwise, not the layout's 1/0/9.
        - Codes that only mean unknown become missing where the item has no other blank, so nothing is lost (CLEAN-10): "status not known" in PIRL 300 (1,720 exits), "did not disclose" or "did not self-identify" in 801, 805 and 806 (331,371, 410,362 and 140,801), and "grantee is unable to track enrollment" in 910, 918 and 932 (406,407, 25,168 and 251,500). In 908, 909, 914 and 916 a blank means the item does not apply, so "Unknown" stays a level of its own.
        - Kept as codes: local boards (PIRL 108A-C), the state (CALC 4000), special project, grant and rapid-response event ids, and the occupation (O*NET-SOC: 403, 1306, 1311, 1316), industry (NAICS 2012: 404-406) and CIP (1305) codes, which disclosure control coarsens to a parent level beside its children; the training provider's name (PIRL 1301) ships as text. The local board code 99999 is the layout's "liable state record" and the industry code 999999 its "wages exist, industry not known" (24,659 exits in PIRL 404, employment rate 0.60), each a level of its own.
        - Ordered: the delivery mode of training and of individualized services (PIRL 1328, 3004: in person, mixed, virtual). Unordered: the highest educational level (PIRL 408) and the school status at entry and exit (409, 1812): the layout does not rank a diploma, an equivalency and an IEP certificate, and the school statuses mix attendance with attainment (CLEAN-14). The highest school grade completed (PIRL 407, 0-12) and the months with the last employer (PIRL 412) are numbers; 412's fill 999 becomes missing (none among these exits; 4 tenures longer than the person's working life stay).
        - Anomaly: the wages before entry (PIRL 1700-1702) are "randomly altered so that adjusted, rather than actual wages, are displayed"; occupation and industry codes are coarsened where fewer than 3 participants share one in a local area; exits of local areas with 50 or fewer exiters in a program year are left out (disclosure control, kept as published, PROV-3). Oklahoma is missing from the PY 2024 Q4 and PY 2025 Q3 files, so its exits are all from 2022 and none is tested. Montana's pre-entry wages are blank for 89% to 97% of its Title I exits from 2024 against 31% to 66% before (Appendix C; 865 exits).
        - Anomaly (SPLIT-20): the training rows mix three releases. Local-board codes follow each release's statewide or board coding (the same exit carries the same PIRL 108A in 68.6% of matched rows between PY 2023 Q4 and PY 2024 Q4, 85.3% between PY 2024 Q4 and PY 2025 Q3, all programmes), PIRL 108B's reporting changes too, the altered wages before entry are drawn again in each release (Spearman 0.98 to 0.99 on matched rows), and about 420 participations of one person appear in two files at a file boundary (training rows only). The local-board columns add at most 0.001 ROC AUC, so the drift moves nothing measurable.
        - Note (LEAK-25, as amended 2026-11-02): an exit without a usable SSN cannot be matched to wage records, which SPRA codes as not employed. Among these Title I exits the rule that locates such rows without the label (an invalid or undisclosed SSN, PIRL 935 code 1, and no pre-entry wage record) finds only 1,117 exits at 0.21, a mix, because SPRA fills blank pre-entry wages with 0 for adult and dislocated-worker exits; they are kept. 263,368 of the 265,653 invalid-SSN exits are New York's: its 23,465 without a positive pre-entry wage are employed at 0.32 against 0.42 for its valid SSNs, a gap part of which may be unmatched wages. The state ships as a feature, and the task keeps signal beyond it (ROC AUC within a local board 0.714 to 0.722, all programmes; the state alone 0.514 to 0.545 on Title I exits). Revisit if a later file marks unmatched exits.
        - Note: PIRL 935 code 2 "Retirement" (1,054 exits, employment rate 0.31) is an exit status without a date; a retirement a state learns after the exit would be a later value (LEAK-10, maybe; kept).
        - Note: one-day batch closures. Montana closed 10,122 exits on 2024-09-06, 7 of them Title I; among the Title I exits Texas closed 8,071 on 2022-08-31 (179 times its median day, training only), and Puerto Rico and Alabama close many on 30 June and 31 December (Puerto Rico 931 and 1,441, Alabama 594 and 527 in the April to June and October to December 2024 windows). For these the prediction at the last service is nominal; they are kept.
        - Note: the DOL disclaimer binds users of the data to research use, to identify nobody and to suppress published summaries of fewer than 3 individuals.
    """

    # Task
    target = "employed_2nd_quarter_after_exit"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason=(
            "DOL scores the employment rate in the second quarter after exit as a share of a state's exiters (the "
            "WIOA primary indicator, TEGL 26-15), with no score for a prediction per person; the statistical "
            "adjustment model of TEGL 26-15 Attachment II is a fixed-effects regression on state-quarter aggregates "
            "and reports no prediction metric. The screening found no paper predicting PIRL 1602 per person. ROC AUC "
            "scores the ranking a follow-up list needs; no source fixes a share, a capacity or a cost (follow-up "
            "reaches 0.2% to 36% of a state's Title I exits)."
        )
    )

    # Splits
    temporal = Temporal(
        on="pirl901_date_program_exit",
        splits=TemporalSplits(window=3, unit="months", cutoffs=("2024-04-01", "2024-07-01", "2024-10-01"), gap=9),
    )
    splits_comment = """
        Three test windows of one quarter of exits each: October to December 2024 (newest), July to September 2024 and April to June 2024. Each trains on the exits up to nine months before its window (a 9-month gap): 703,369, 626,808 and 541,907 exits, 68.7%, 61.2% and 53.0% of the frame. The outcome of an exit is employment in the second quarter after its exit quarter, read from the state's unemployment insurance wage records. For the newest training quarter (Q-4) that is quarter Q-2, which ended three months before the window starts, and employers report a quarter's wages within about a month of its end (the general UI reporting rule; an inference, not read in a source here), so a state refitting its model when a window starts holds these labels. A 6-month gap would admit labels of quarter Q-1, which ends as the window starts. DOL's own files fill an outcome only four quarters after the exit quarter, to take in interstate and supplemental wage matches, which turn about 0.5% to 1% of labels to employed later; a 12-month gap that waited for them would leave the oldest window below half the rows in training, and the newest training quarter is worth about +0.002 ROC AUC at equal training size (gap 9 against 12). The gap also keeps a returning person's later-measured label out of training. The exits of January to March 2024 (77,215) fall in the gap of every window and are in no split; January to March 2025 is out of the frame (see the notes).
    """

    prepared_raw_files = (PREPARED_FILE,)

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        # The three files hold 37M rows of 279 items; keep the matured exits of each file's exit range and the items
        # read below, once, with pyarrow (about 7.5M rows).
        import pyarrow as pa
        import pyarrow.compute as pc
        import pyarrow.csv as pacsv
        import pyarrow.parquet as pq

        columns = [*RAW_COLUMNS, "PIRL100"]

        def target_type(col: str) -> pa.DataType:
            if col in (*TEXT_ITEMS, "PIRL100"):
                return pa.string()
            if col in ("PIRL1700", "PIRL1701", "PIRL1702"):
                return pa.float64()
            return pa.int32() if col in (*DATE_ITEMS, *WIDE_CODES) else pa.int16()

        schema = pa.schema([(c, target_type(c)) for c in columns])

        def keep(table: pa.Table, lo: int, hi: int) -> pa.Table:
            exit_date = table["PIRL901"]
            mask = pc.and_(
                pc.is_valid(table["CALC4013"]), pc.and_(pc.greater_equal(exit_date, lo), pc.less(exit_date, hi))
            )
            return table.filter(pc.fill_null(mask, False)).select(columns).cast(schema)

        parts = []
        for name, lo, hi in SOURCE_FILES:
            if name.endswith(".parquet"):
                part = keep(pq.read_table(raw_dir / name, columns=columns), lo, hi)
            else:
                # The CSV is read as text and floats, then cast: a fractional code would fail the cast.
                read_types = {c: pa.string() if c in (*TEXT_ITEMS, "PIRL100") else pa.float64() for c in columns}
                reader = pacsv.open_csv(
                    raw_dir / name,
                    read_options=pacsv.ReadOptions(block_size=1 << 26),
                    convert_options=pacsv.ConvertOptions(
                        include_columns=columns, column_types=read_types, strings_can_be_null=False
                    ),
                )
                part = pa.concat_tables([keep(pa.Table.from_batches([batch]), lo, hi) for batch in reader])
            parts.append(part.append_column("source_file", pa.array([name] * part.num_rows, pa.string())))
        pq.write_table(pa.concat_tables(parts), raw_dir / PREPARED_FILE)

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_parquet(raw_dir / PREPARED_FILE, dtype_backend="numpy_nullable")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # 1. The person's previous known outcome, looked up in every exit of the prepared files (USE-10).
        history = _previous_known_outcome(raw, self.temporal.splits)
        # 2. The population: Title I exits before 2025, outside American Samoa and Palau.
        keep = _population(raw).to_numpy(bool)
        df = raw.loc[keep].join(history.loc[keep])
        # 3. Identifiers and bookkeeping; the second and third HVRP grantees (1 exit each); calculated items that
        #    recode one kept item exactly (CLEAN-5).
        df = drop_columns(df, ["PIRL100", "source_file", "PIRL311", "PIRL313", "CALC4001", "CALC4005"])
        # 4. Text items: an empty string is a blank item; one H-1B grant id is written in two cases.
        for col in TEXT_ITEMS:
            df[col] = df[col].replace("", pd.NA)
        # A training provider named "NA" or "n/a" is a blank written as text.
        df["PIRL1301"] = df["PIRL1301"].replace(["NA", "n/a"], pd.NA)
        df["PIRL938"] = df["PIRL938"].str.upper()
        # 5. Dates: the ones a person can reach only after the exit are not known at the exit.
        for col in MASK_AFTER_EXIT:
            df[col] = df[col].mask((df[col] > df["PIRL901"]).fillna(False))
        for col in DATE_ITEMS:
            df[col] = _to_dates(df[col])
        # 6. Codes the layout does not list (CLEAN-11), codes that only mean unknown (CLEAN-10) and the tenure fill
        #    become missing; codes that reveal a ground join a neighbour (SEL-1); then the codes become the words.
        df = set_missing(df, {**UNDOCUMENTED_CODES, **UNKNOWN_ONLY, **TENURE_FILL})
        for col, merged in GROUND_CODES.items():
            df[col] = df[col].replace(merged)
        df = _decode_codes(df, CODE_LABELS)
        # 7. The target: PIRL 1602 on DOL's employment-rate cohort (CALC 4013), 1 = employed.
        df = _decode_codes(df, {"CALC4013": {0: "No", 1: "Yes"}})
        # 8. Numbers as floats; the rest (0/1 flags and codes without words) are categories in `_feature_types`.
        for col in NUMERIC_ITEMS:
            df[col] = df[col].astype("float64")
        # 9. The grounds the actor may not base a service on, and the items that reveal them (SEL-1).
        df = drop_columns(df, [*RACE_SEX, *AGE_ITEMS, *DISABILITY_ITEMS, *PREGNANCY_LEP_ITEMS])
        return df.rename(columns=NAMES)

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        typed = {
            *_present(df, DATE_ITEMS),
            *_present(df, NUMERIC_ITEMS),
            *_present(df, CODE_LABELS),
            NAMES["PIRL1301"],
            NAMES["CALC4013"],
            "quarters_since_previous_exit",
        }
        return FeatureTypes(
            categorical=[c for c in df.columns if c not in typed],
            string=[NAMES["PIRL1301"]],
            datetime=_present(df, DATE_ITEMS),
            ordinal={NAMES[c]: list(VIRTUAL_ORDER) for c in ("PIRL1328", "PIRL3004")},
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        keep = _population(raw)
        pop = raw.loc[keep.to_numpy(bool)]
        title_i = (raw[list(TITLE_I_STREAMS)] == 1).fillna(False).any(axis=1)
        before_2025 = (raw["PIRL901"] < LAST_EXIT).fillna(False)
        steps = pd.Series(
            {
                "exits in DOL's employment-rate cohort, January 2022 to March 2025 (prepared file)": len(raw),
                "with an adult, dislocated-worker or DWG funding stream": int(title_i.sum()),
                "and an exit before 2025": int((title_i & before_2025).sum()),
                "and outside American Samoa and Palau": int(keep.sum()),
            },
            name="exits",
        )
        employed = pop["CALC4013"].astype("float64").to_numpy()
        by_file = (
            pd.DataFrame(
                {
                    "exit quarter": pd.PeriodIndex(_to_dates(pop["PIRL901"]), freq="Q").astype(str),
                    "file": pop["source_file"].to_numpy(),
                    "employed": employed,
                }
            )
            .groupby(["exit quarter", "file"], observed=True)
            .agg(exits=("employed", "size"), employment_rate=("employed", "mean"))
            .round(3)
        )
        after_exit = pd.Series(
            {col: int((pop[col] > pop["PIRL901"]).sum()) for col in MASK_AFTER_EXIT}, name="dates after the exit"
        )
        to_missing = pd.Series(
            {
                f"{col} code {codes}": int(pop[col].isin(codes).sum())
                for col, codes in {**UNDOCUMENTED_CODES, **UNKNOWN_ONLY, **TENURE_FILL}.items()
            },
            name="rows set to missing",
        )
        merged_codes = ", ".join(
            f"{col} code {code}: {int((pop[col] == code).sum())}"
            for col, merged in GROUND_CODES.items()
            for code in merged
        )
        grounds = pd.DataFrame(
            {
                "items": [", ".join(items) for items in (RACE_SEX, AGE_ITEMS, DISABILITY_ITEMS, PREGNANCY_LEP_ITEMS)]
                + [f"exits merged: {merged_codes}"],
                "status": ["dropped"]
                + ["dropped, pending the curator's call"] * 3
                + ["merged, pending the curator's call"],
            },
            index=[
                "race, Hispanic ethnicity, sex",
                "age, youth items",
                "disability, its proxies",
                "pregnancy, limited English",
                "codes merged into a neighbour",
            ],
        )
        history = (
            pd.DataFrame(
                {
                    "previous known outcome": df["previous_known_outcome"].astype(str).to_numpy(),
                    "employed": (df[self.target] == "Yes").to_numpy(),
                }
            )
            .groupby("previous known outcome")
            .agg(exits=("employed", "size"), employment_rate=("employed", "mean"))
            .round(3)
        )
        wages = pop[["PIRL1700", "PIRL1701", "PIRL1702"]]
        invalid = (pop["PIRL935"] == 1).fillna(False).to_numpy(bool)
        no_record = wages.isna().all(axis=1).to_numpy(bool)
        no_positive = ~(wages.fillna(0) > 0).any(axis=1).to_numpy(bool)
        new_york = (pop["CALC4000"] == "NY").fillna(False).to_numpy(bool)
        groups = {
            "invalid SSN": invalid,
            "invalid SSN, New York": invalid & new_york,
            "invalid SSN, no pre-entry wage record (located)": invalid & no_record,
            "invalid SSN, no positive pre-entry wage": invalid & no_positive,
            "New York, invalid SSN, no positive pre-entry wage": new_york & invalid & no_positive,
            "New York, valid SSN, no positive pre-entry wage": new_york & ~invalid & no_positive,
        }
        ssn = pd.DataFrame(
            {
                "exits": [int(m.sum()) for m in groups.values()],
                "employment_rate": [round(float(employed[m].mean()), 3) for m in groups.values()],
            },
            index=list(groups),
        )
        return [
            Decision(
                title="The population: Title I exits of 2022 to 2024",
                why=(
                    "Follow-up exists only for Title I adult and dislocated-worker exits; January to March 2025 is at "
                    "its first report with Texas's wages incomplete; American Samoa and Palau send no wages."
                ),
                evidence=steps,
            ),
            Decision(
                title="Exits by quarter and file",
                why="Each exit quarter comes from the newest file that holds its outcome; the rate is PIRL 1602.",
                evidence=by_file,
            ),
            Decision(
                title="Dates after the exit set to missing",
                why="A date later than the exit date is not known at the prediction point.",
                evidence=after_exit,
            ),
            Decision(
                title="Codes set to missing",
                why=(
                    "Codes the layout does not list (CLEAN-11), codes that only mean unknown in items with no other "
                    "blank (CLEAN-10) and the tenure fill 999."
                ),
                evidence=to_missing,
            ),
            Decision(
                title="Items dropped as grounds the actor may not base a service on",
                why=(
                    "29 CFR 38.6(b) and UIPL 41-94; race, ethnicity and sex settled, age and disability with the "
                    "items that reveal them pending the curator's call (SEL-1)."
                ),
                evidence=grounds,
            ),
            Decision(
                title="The person's previous known outcome",
                why=(
                    "The outcome of the person's latest exit at least four quarters back (USE-10); Unknown where the "
                    "ids do not link (Texas, Utah) or the look-back lies before the files (2022)."
                ),
                evidence=history,
            ),
            Decision(
                title="Exits without a usable SSN, kept",
                why=(
                    "A rule without the label locates only a mix among Title I exits (LEAK-25 as amended "
                    "2026-11-02); New York holds nearly all invalid SSNs."
                ),
                evidence=ssn,
            ),
        ]
