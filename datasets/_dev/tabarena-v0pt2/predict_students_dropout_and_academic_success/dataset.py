"""Curated dataset definition for `predict_students_dropout_and_academic_success` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset


class PredictStudentsDropoutAndAcademicSuccess(AbstractCuratedDataset):
    # Dataset
    unique_name = "predict_students_dropout_and_academic_success"
    year = "2021"
    domain = "education"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5MC89"
    license = "CC BY 4.0"
    download_description = """
        We download the data from the UCI repository and uzip it to a predefined folder.

        mkdir -p local-data-warehouse/predict_students_dropout_and_academic_success/ && wget -P local-data-warehouse/predict_students_dropout_and_academic_success/ https://archive.ics.uci.edu/static/public/697/predict+students+dropout+and+academic+success.zip && unzip local-data-warehouse/predict_students_dropout_and_academic_success/predict+students+dropout+and+academic+success.zip -d local-data-warehouse/predict_students_dropout_and_academic_success/  && rm local-data-warehouse/predict_students_dropout_and_academic_success/predict+students+dropout+and+academic+success.zip
    """
    bibtex = r"""
        @inproceedings{martins2021early,
          title={Early prediction of student’s performance in higher education: A case study},
          author={Martins, M{\'o}nica V and Tolledo, Daniel and Machado, Jorge and Baptista, Lu{\'\i}s MT and Realinho, Valentim},
          booktitle={Trends and Applications in Information Systems and Technologies: Volume 1 9},
          pages={166--175},
          year={2021},
          organization={Springer}
        }
    """
    curation_comments = """
        - We renamed the target variable and fixed some typos in the feature names.
        - We reversed the ordinal encoding of all categorical features.
        - We removed whitespaces and special characters from the feature names.
    """

    # Task
    target = "AcademicOutcome"
    problem_type = "multiclass_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        data = pd.read_csv(raw_dir / "data.csv", sep=";")
        return data

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        data = raw
        target_feature = "AcademicOutcome"
        data = data.rename(
            columns={
                "Target": target_feature,
                "Daytime/evening attendance	": "Daytime/evening attendance",
            }
        )
        maps = {
            "International": {1: "yes", 0: "no"},
            "Marital status": {
                1: "single",
                2: "married",
                3: "widower",
                4: "divorced",
                5: "facto union",
                6: "legally separated",
            },
            "Application mode": {
                1: "1st phase - general contingent",
                2: "Ordinance No. 612/93",
                5: "1st phase - special contingent (Azores Island)",
                7: "Holders of other higher courses",
                10: "Ordinance No. 854-B/99",
                15: "International student (bachelor)",
                16: "1st phase - special contingent (Madeira Island)",
                17: "2nd phase - general contingent",
                18: "3rd phase - general contingent",
                26: "Ordinance No. 533-A/99, item b2) (Different Plan)",
                27: "Ordinance No. 533-A/99, item b3 (Other Institution)",
                39: "Over 23 years old",
                42: "Transfer",
                43: "Change of course",
                44: "Technological specialization diploma holders",
                51: "Change of institution/course",
                53: "Short cycle diploma holders",
                57: "Change of institution/course (International)",
            },
            "Course": {
                33: "Biofuel Production Technologies",
                171: "Animation and Multimedia Design",
                8014: "Social Service (evening attendance)",
                9003: "Agronomy",
                9070: "Communication Design",
                9085: "Veterinary Nursing",
                9119: "Informatics Engineering",
                9130: "Equinculture",
                9147: "Management",
                9238: "Social Service",
                9254: "Tourism",
                9500: "Nursing",
                9556: "Oral Hygiene",
                9670: "Advertising and Marketing Management",
                9773: "Journalism and Communication",
                9853: "Basic Education",
                9991: "Management (evening attendance)",
            },
            "Daytime/evening attendance": {1: "daytime", 0: "evening"},
            "Previous qualification": {
                1: "Secondary education",
                2: "Higher education - bachelor's degree",
                3: "Higher education - degree",
                4: "Higher education - master's",
                5: "Higher education - doctorate",
                6: "Frequency of higher education",
                9: "12th year of schooling - not completed",
                10: "11th year of schooling - not completed",
                12: "Other - 11th year of schooling",
                14: "10th year of schooling",
                15: "10th year of schooling - not completed",
                19: "Basic education 3rd cycle (9th/10th/11th year) or equiv.",
                38: "Basic education 2nd cycle (6th/7th/8th year) or equiv.",
                39: "Technological specialization course",
                40: "Higher education - degree (1st cycle)",
                42: "Professional higher technical course",
                43: "Higher education - master (2nd cycle)",
            },
            "Nacionality": {
                1: "Portuguese",
                2: "German",
                6: "Spanish",
                11: "Italian",
                13: "Dutch",
                14: "English",
                17: "Lithuanian",
                21: "Angolan",
                22: "Cape Verdean",
                24: "Guinean",
                25: "Mozambican",
                26: "Santomean",
                32: "Turkish",
                41: "Brazilian",
                62: "Romanian",
                100: "Moldova (Republic of)",
                101: "Mexican",
                103: "Ukrainian",
                105: "Russian",
                108: "Cuban",
                109: "Colombian",
            },
            "Mother's qualification": {
                1: "Secondary Education - 12th Year of Schooling or Eq.",
                2: "Higher Education - Bachelor's Degree",
                3: "Higher Education - Degree",
                4: "Higher Education - Master's",
                5: "Higher Education - Doctorate",
                6: "Frequency of Higher Education",
                9: "12th Year of Schooling - Not Completed",
                10: "11th Year of Schooling - Not Completed",
                11: "7th Year (Old)",
                12: "Other - 11th Year of Schooling",
                14: "10th Year of Schooling",
                18: "General commerce course",
                19: "Basic Education 3rd Cycle",
                22: "Technical-professional course",
                26: "7th year of schooling",
                27: "2nd cycle of the general high school course",
                29: "9th Year of Schooling - Not Completed",
                30: "8th year of schooling",
                34: "Unknown",
                35: "Can't read or write",
                36: "Can read without having a 4th year of schooling",
                37: "Basic education 1st cycle (4th/5th year) or equiv.",
                38: "Basic Education 2nd Cycle",
                39: "Technological specialization course",
                40: "Higher education - degree (1st cycle)",
                41: "Specialized higher studies course",
                42: "Professional higher technical course",
                43: "Higher Education - Master (2nd cycle)",
                44: "Higher Education - Doctorate (3rd cycle)",
            },
            "Father's qualification": {
                1: "Secondary Education - 12th Year of Schooling or Eq.",
                2: "Higher Education - Bachelor's Degree",
                3: "Higher Education - Degree",
                4: "Higher Education - Master's",
                5: "Higher Education - Doctorate",
                6: "Frequency of Higher Education",
                9: "12th Year of Schooling - Not Completed",
                10: "11th Year of Schooling - Not Completed",
                11: "7th Year (Old)",
                12: "Other - 11th Year of Schooling",
                13: "2nd year complementary high school course",
                14: "10th Year of Schooling",
                18: "General commerce course",
                19: "Basic Education 3rd Cycle",
                20: "Complementary High School Course",
                22: "Technical-professional course",
                25: "Complementary High School Course - not concluded",
                26: "7th year of schooling",
                27: "2nd cycle of the general high school course",
                29: "9th Year of Schooling - Not Completed",
                30: "8th year of schooling",
                31: "General Course of Administration and Commerce",
                33: "Supplementary Accounting and Administration",
                34: "Unknown",
                35: "Can't read or write",
                36: "Can read without having a 4th year of schooling",
                37: "Basic education 1st cycle",
                38: "Basic Education 2nd Cycle",
                39: "Technological specialization course",
                40: "Higher education - degree (1st cycle)",
                41: "Specialized higher studies course",
                42: "Professional higher technical course",
                43: "Higher Education - Master (2nd cycle)",
                44: "Higher Education - Doctorate (3rd cycle)",
            },
            "Mother's occupation": {
                0: "Student",
                1: "Representatives of Legislative/Executive Bodies",
                2: "Specialists in Intellectual/Scientific Activities",
                3: "Intermediate Level Technicians and Professions",
                4: "Administrative staff",
                5: "Personal Services, Security and Safety Workers and Sellers",
                6: "Farmers and Skilled Workers",
                7: "Skilled Workers in Industry/Construction/Craftsmen",
                8: "Installation and Machine Operators",
                9: "Unskilled Workers",
                10: "Armed Forces Professions",
                90: "Other Situation",
                99: "(blank)",
                122: "Health professionals",
                123: "Teachers",
                125: "ICT Specialists",
                131: "Intermediate science and engineering technicians",
                132: "Health technicians",
                134: "Legal/social/cultural technicians",
                141: "Office workers",
                143: "Finance/statistics workers",
                144: "Other administrative support",
                151: "Personal service workers",
                152: "Sellers",
                153: "Personal care workers",
                171: "Skilled construction workers",
                173: "Printing/jewelers/artisans",
                175: "Food/woodworking workers",
                191: "Cleaning workers",
                192: "Unskilled agriculture workers",
                193: "Unskilled construction workers",
                194: "Meal preparation assistants",
            },
            "Father's occupation": {
                0: "Student",
                1: "Representatives of Legislative/Executive Bodies",
                2: "Specialists in Intellectual/Scientific Activities",
                3: "Intermediate Level Technicians and Professions",
                4: "Administrative staff",
                5: "Personal Services, Security and Safety Workers and Sellers",
                6: "Farmers and Skilled Workers",
                7: "Skilled Workers in Industry/Construction/Craftsmen",
                8: "Installation and Machine Operators",
                9: "Unskilled Workers",
                10: "Armed Forces Professions",
                90: "Other Situation",
                99: "(blank)",
                101: "Armed Forces Officers",
                102: "Armed Forces Sergeants",
                103: "Other Armed Forces personnel",
                112: "Directors of administrative services",
                114: "Hotel/catering services directors",
                121: "Physical sciences/engineering specialists",
                122: "Health professionals",
                123: "Teachers",
                124: "Finance/administration specialists",
                131: "Intermediate science technicians",
                132: "Health technicians",
                134: "Legal/social/cultural technicians",
                135: "ICT technicians",
                141: "Office workers",
                143: "Finance/statistics workers",
                144: "Other administrative support",
                151: "Personal service workers",
                152: "Sellers",
                153: "Personal care workers",
                154: "Security personnel",
                161: "Market-oriented farmers",
                163: "Subsistence farmers",
                171: "Skilled construction workers",
                172: "Metal workers",
                174: "Electricians",
                175: "Food/craft workers",
                181: "Machine operators",
                182: "Assembly workers",
                183: "Vehicle drivers",
                192: "Unskilled agriculture workers",
                193: "Unskilled construction workers",
                194: "Meal preparation assistants",
                195: "Street vendors",
            },
            "Displaced": {1: "yes", 0: "no"},
            "Educational special needs": {1: "yes", 0: "no"},
            "Debtor": {1: "yes", 0: "no"},
            "Tuition fees up to date": {1: "yes", 0: "no"},
            "Gender": {1: "male", 0: "female"},
            "Scholarship holder": {1: "yes", 0: "no"},
        }
        for column, mapping in maps.items():
            data[column] = data[column].map(mapping)
        # More renaming
        data = data.rename(columns={"Nacionality": "Nationality"})
        data.columns = [
            c.replace(" ", "_").replace(")", "").replace("(", "").replace("'", "").replace("/", "")
            for c in data.columns
        ]
        as_cat_type = [
            "Marital_status",
            "Application_mode",
            "Course",
            "Daytimeevening_attendance",
            "Previous_qualification",
            "Nationality",
            "Mothers_qualification",
            "Fathers_qualification",
            "Mothers_occupation",
            "Fathers_occupation",
            "Displaced",
            "Educational_special_needs",
            "Debtor",
            "Tuition_fees_up_to_date",
            "Gender",
            "Scholarship_holder",
            "International",
            target_feature,
        ]
        data[as_cat_type] = data[as_cat_type].astype("category")
        df = data
        return df
