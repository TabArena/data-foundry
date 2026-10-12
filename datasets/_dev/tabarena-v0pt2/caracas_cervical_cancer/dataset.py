"""Curated dataset definition for `caracas_cervical_cancer` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, drop_columns

SCREENING_TESTS = ["Hinselmann", "Schiller", "Citology"]
"""The three screening results besides the biopsy: outcomes of the same work-up, not features."""

SOURCE_FILLS = {
    "Smokes (years)": 1.266972909,
    "Smokes (packs/year)": 0.5132021277,
    "Hormonal Contraceptives (years)": 2.282200521,
}
"""Values the source filled in before release (the only answers with more than three decimals): unknown durations."""

RENAME = {
    "Age": "age",
    "Number of sexual partners": "number_of_sexual_partners",
    "First sexual intercourse": "age_first_sexual_intercourse",
    "Num of pregnancies": "number_of_pregnancies",
    "Smokes": "smokes",
    "Smokes (years)": "smokes_years",
    "Smokes (packs/year)": "smokes_packs_per_year",
    "Hormonal Contraceptives": "hormonal_contraceptives",
    "Hormonal Contraceptives (years)": "hormonal_contraceptives_years",
    "IUD": "iud",
    "IUD (years)": "iud_years",
    "STDs": "stds",
    "STDs (number)": "stds_number",
    "STDs:condylomatosis": "std_condylomatosis",
    "STDs:vaginal condylomatosis": "std_vaginal_condylomatosis",
    "STDs:vulvo-perineal condylomatosis": "std_vulvo_perineal_condylomatosis",
    "STDs:syphilis": "std_syphilis",
    "STDs:pelvic inflammatory disease": "std_pelvic_inflammatory_disease",
    "STDs:genital herpes": "std_genital_herpes",
    "STDs:molluscum contagiosum": "std_molluscum_contagiosum",
    "STDs:HIV": "std_hiv",
    "STDs:Hepatitis B": "std_hepatitis_b",
    "STDs:HPV": "std_hpv",
    "STDs: Number of diagnosis": "stds_number_of_diagnoses",
    "STDs: Time since first diagnosis": "stds_years_since_first_diagnosis",
    "STDs: Time since last diagnosis": "stds_years_since_last_diagnosis",
    "Dx:Cancer": "dx_cancer",
    "Dx:CIN": "dx_cin",
    "Dx:HPV": "dx_hpv",
    "Dx": "dx",
    "Biopsy": "biopsy",
}
"""Source column -> name without colons, spaces or brackets (LightGBM refuses colons in feature names)."""


class CaracasCervicalCancer(AbstractCuratedDataset):
    # Dataset
    unique_name = "caracas_cervical_cancer"
    year = "2017"
    domain = "medical & healthcare"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5Z310"
    license = "CC BY 4.0"
    download_description = """
        We download the data from UCI (dataset 383, Cervical Cancer (Risk Factors)). The zip holds one file,
        risk_factors_cervical_cancer.csv (858 rows, 36 columns; unanswered questions are "?").

        mkdir -p local-data-warehouse/caracas_cervical_cancer
        wget -P local-data-warehouse/caracas_cervical_cancer https://archive.ics.uci.edu/static/public/383/cervical+cancer+risk+factors.zip
        unzip local-data-warehouse/caracas_cervical_cancer/cervical+cancer+risk+factors.zip -d local-data-warehouse/caracas_cervical_cancer
        rm local-data-warehouse/caracas_cervical_cancer/cervical+cancer+risk+factors.zip
    """
    bibtex = """
        @inproceedings{fernandes2017transfer,
          title={Transfer Learning with Partial Observability Applied to Cervical Cancer Screening},
          author={Fernandes, Kelwin and Cardoso, Jaime S. and Fernandes, Jessica},
          booktitle={Pattern Recognition and Image Analysis (IbPRIA 2017)},
          series={Lecture Notes in Computer Science},
          volume={10255},
          pages={243--250},
          year={2017},
          publisher={Springer},
          doi={10.1007/978-3-319-58838-4_27}
        }
        @article{fernandes2018supervised,
          title={Supervised deep learning embeddings for the prediction of cervical cancer diagnosis},
          author={Fernandes, Kelwin and Chicco, Davide and Cardoso, Jaime S. and Fernandes, Jessica},
          journal={PeerJ Computer Science},
          volume={4},
          pages={e154},
          year={2018},
          doi={10.7717/peerj-cs.154}
        }
        @misc{fernandes2017cervical,
          title={Cervical Cancer (Risk Factors)},
          author={Fernandes, Kelwin and Cardoso, Jaime and Fernandes, Jessica},
          year={2017},
          howpublished={UCI Machine Learning Repository},
          doi={10.24432/C5Z310}
        }
    """
    curation_comments = """
        We start with risk_factors_cervical_cancer.csv from UCI: 858 patients of the gynecology service at Hospital Universitario de Caracas (2012-2013), with their answers to a risk-factor questionnaire and four test results.

        - Prediction point: the patient's questionnaire answers, before any result of her screening work-up is known, the creators' setting "where only behavioral and demographic information is observable" (Fernandes et al. 2018, Results).
        - The target is the biopsy (55 positive of the 750 patients kept). We drop the other three test results (Hinselmann, Schiller, Citology): they come from the same work-up (decision table).
        - We read "?" as a missing value: patients "decided not to answer some questions for privacy concerns" (2018, Dataset).
        - We drop the 108 patients who did not answer the hormonal-contraceptive question: their test results look unrecorded rather than negative. None of them has a positive biopsy, Hinselmann or Schiller result, where 11.8 are expected (binomial P = 4e-6), yet the routine cytology finds 2 and their answers show no lower risk (decision table).
        - We set the values the source filled in before release (`SOURCE_FILLS`) to missing. They are the only answers with more than three decimals in their columns, all in rows that answered "yes": the answer is known, the duration is not.
        - `stds_number_of_diagnoses` is 0 for every patient who skipped the STD questions; we set it to missing for them.
        - We drop the flags for cervical condylomatosis and AIDS: no patient has either.
        - The STD-type flags and the previous-diagnosis flags (`dx_*`) stay binary categorical columns: they are multi-label (43 patients have two to four STD types).
        - We rename the columns without colons, spaces and brackets (LightGBM refuses colons in feature names). `dx` and the `dx_*` flags are the previous cervical diagnoses of the 2017 Table 1, history rather than the diagnosis of this work-up (12 of the 18 patients with `dx_cancer` have a negative biopsy).
        - We keep the 22 rows (2.9%) whose answers repeat another row's: coarse answer profiles of young patients, not adjacent in the file. Recombining the answers at random among patients of the same age and history gives 20 repeats on average, so they are different women (decision table).
        - Note: a label-free distance to the nearest other patient gives ROC AUC 0.70, above the untuned models (random forest 0.68). It follows the number of nonzero answers (Spearman 0.57), so we read it as the risk load of the questionnaire, not as generated data (the generated-data probe finds no rule leaves).
        - Anomaly: a few answers contradict each other (2 patients report a first intercourse after their current age, 5 have a `dx_*` flag set while `dx` is 0). Kept as recorded: we cannot tell which answer is wrong.
    """

    # Task
    target = "biopsy"
    problem_type = "binary_classification"

    accepted_check_warnings = {
        "dataset_duplicate_rows": "The 21 exact copies (2.8%) are coarse answer profiles of young patients with "
        "short histories, not adjacent in the file; recombining answers at random among patients of the same age "
        "and history gives as many repeats (20 on average, 16-25), so they are different women and stay.",
    }

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        # "?" marks a question the patient did not answer
        return pd.read_csv(raw_dir / "risk_factors_cervical_cancer.csv", na_values="?")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # values the source filled in before release: the answer is yes, the duration unknown
        for col, value in SOURCE_FILLS.items():
            df[col] = df[col].mask((df[col] - value).abs() < 1e-6)
        # the count of STD diagnoses is 0 by default for patients who skipped the STD questions
        df["STDs: Number of diagnosis"] = df["STDs: Number of diagnosis"].astype(float).mask(df["STDs"].isna())
        # patients who skipped the contraceptive question: their test results look unrecorded, not negative
        df = df[df["Hormonal Contraceptives"].notna()]
        # the other three test results come from the same work-up as the biopsy: outcomes, not features
        df = drop_columns(df, SCREENING_TESTS)
        # never positive: 0 or unanswered in every row
        df = drop_columns(df, ["STDs:cervical condylomatosis", "STDs:AIDS"])
        df = df.rename(columns=RENAME)
        df[self.target] = df[self.target].map({0: "negative", 1: "positive"})
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # yes/no answers and diagnosis flags; counts, ages and years stay numeric
        binary = ["smokes", "hormonal_contraceptives", "iud", "stds", "dx_cancer", "dx_cin", "dx_hpv", "dx"]
        return FeatureTypes(categorical=[c for c in df.columns if c in binary or c.startswith("std_")])

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        answered = raw["Hormonal Contraceptives"].notna()
        kept = raw[answered]
        tests = pd.DataFrame(
            {
                test: {
                    "patients with a positive result": int(kept[test].sum()),
                    "of them with a positive biopsy": int(kept["Biopsy"][kept[test] == 1].sum()),
                    "positive biopsies with a negative result": int(kept["Biopsy"][kept[test] == 0].sum()),
                }
                for test in SCREENING_TESTS
            }
        )
        tests.index.name = "patients kept"
        grouped = raw.groupby(answered.map({True: "answered (kept)", False: "not answered (dropped)"}))
        by_answer = pd.DataFrame({"patients": grouped.size()})
        for test in [*SCREENING_TESTS, "Biopsy"]:
            by_answer[f"{test} positive"] = grouped[test].sum()
            by_answer[f"{test} rate"] = grouped[test].mean().round(3)
        by_answer.index.name = "hormonal-contraceptive question"
        features = [c for c in df.columns if c != self.target]
        repeated = df.duplicated(subset=features, keep=False)
        profiles = df[repeated].groupby(features, dropna=False, observed=True)[self.target].nunique()
        duplicates = pd.Series(
            {
                "rows repeating another row's answers": int(df.duplicated(subset=features).sum()),
                "profiles with copies": len(profiles),
                "profiles whose copies differ in the biopsy": int((profiles > 1).sum()),
                "youngest patient with a copy (age)": int(df.loc[repeated, "age"].min()),
                "oldest patient with a copy (age)": int(df.loc[repeated, "age"].max()),
            },
            name="count",
        )
        duplicates.index.name = "repeated answer profiles"
        return [
            Decision(
                "The other three test results are dropped",
                "Hinselmann, Schiller and cytology are results of the same screening work-up as the biopsy and "
                "targets in IbPRIA 2017; as features they turn risk assessment into reading the colposcopy.",
                tests,
            ),
            Decision(
                "Patients who skipped the contraceptive question are dropped",
                "None of them has a positive biopsy, Hinselmann or Schiller result, while their answers show no "
                "lower risk and the routine cytology still finds 2: their examination results look unrecorded, "
                "not negative.",
                by_answer,
            ),
            Decision(
                "Repeated answer profiles are kept",
                "The copies are young patients with short histories, not adjacent in the file: plausibly "
                "different women with the same coarse answers.",
                duplicates,
            ),
        ]
