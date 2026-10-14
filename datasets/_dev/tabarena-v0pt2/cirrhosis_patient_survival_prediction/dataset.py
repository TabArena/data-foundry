"""Curated dataset definition for `cirrhosis_patient_survival_prediction` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, TaskSummary, drop_columns

FIVE_YEARS = 5 * 365.25  # days; N_Days is whole days, so an event on day 1,826 or earlier is within 5 years
LAST_TRIAL_ID = 312  # IDs 1-312 are the trial patients, 313-418 the patients outside the trial


def _cohort(raw: pd.DataFrame) -> pd.DataFrame:
    """Per patient: the event within 5 years, 5 years of follow-up, and whether the study could follow them 5 years."""
    event = raw["Status"].isin(["D", "CL"]) & raw["N_Days"].le(FIVE_YEARS)
    followed = raw["N_Days"].ge(FIVE_YEARS)
    # IDs follow the order of registration within the trial and within the other patients, and follow-up ended at
    # the July 1986 analysis: when anyone registered at or after a patient was followed 5 years, so could they be
    newest_first = raw.sort_values("ID", ascending=False, kind="stable")
    covered = newest_first.groupby(newest_first["ID"].le(LAST_TRIAL_ID))["N_Days"].cummax().ge(FIVE_YEARS)
    return pd.DataFrame({"event": event, "followed": followed, "covered": covered.reindex(raw.index)})


class CirrhosisPatientSurvivalPrediction(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "Will a patient with primary biliary cirrhosis die or receive a liver transplant within 5 years of "
            "registration?"
        ),
        use_case=(
            "When a patient with primary biliary cirrhosis is referred, a hepatologist estimates the risk of death "
            "or transplant in the next years from routine findings, to decide whether and when to evaluate the "
            "patient for a liver transplant. Dickson et al. (1989) built the Mayo risk model on this cohort for that "
            "decision."
        ),
        row=(
            "One patient referred to the Mayo Clinic with primary biliary cirrhosis and registered from 1974 to about "
            "mid-1981, early enough to be followed 5 years before the July 1986 analysis: 304 patients, 238 in a "
            "drug trial and 66 outside it."
        ),
        predicted=(
            "Whether the patient died or received a liver transplant within 5 years (1,826 days) of registration: "
            "107 of 304 did (35%), 103 deaths and 4 transplants."
        ),
        known=(
            "Age, sex, the trial drug (D-penicillamine or placebo; missing outside the trial), physical signs (fluid "
            "in the abdomen, enlarged liver, spider veins, swelling), blood and urine tests (bilirubin, cholesterol, "
            "albumin, copper, liver enzymes, triglycerides, platelets, clotting time) and the histologic stage, all "
            "taken at registration. Patients outside the trial lack the signs and several tests."
        ),
        split=(
            "Random patients, stratified by the outcome, so the test data stands for new patients referred to the "
            "same clinic in the same years."
        ),
        changes=(
            "The source is a survival study with the time to death, transplant or the end of follow-up. We turn it "
            "into a 5-year outcome: we keep the patients registered early enough to be followed 5 years, drop 5 lost "
            "to follow-up before then, and drop the follow-up time and status."
        ),
        fit="approximate",
        fit_reason=(
            "The outcome, its 5-year horizon and the findings at registration match the decision. The patients were "
            "treated 1974-1986, before ursodeoxycholic acid became the standard drug and while transplants were rare "
            "(4 of 107 events), so the data stand for an earlier treatment era. The registration year shows no trend "
            "in the label (ROC AUC 0.52), so a random split fits."
        ),
    )

    # Dataset
    unique_name = "cirrhosis_patient_survival_prediction"
    year = "1991"
    domain = "medical & healthcare"
    source = "Other"  # the Mayo Clinic PBC trial data (Fleming and Harrington 1991); UCI 878 is a later copy
    source_url = "https://www.mayo.edu/research/documents/pbchtml/doc-10027635"
    license = "CC BY 4.0"  # stated on UCI 878, the copy we download
    download_description = """
        We get the UCI data.

        wget https://archive.ics.uci.edu/static/public/878/cirrhosis+patient+survival+prediction+dataset-1.zip && unzip cirrhosis+patient+survival+prediction+dataset-1.zip && rm cirrhosis+patient+survival+prediction+dataset-1.zip && mkdir -p local-data-warehouse/cirrhosis_patient_survival_prediction && mv cirrhosis.csv local-data-warehouse/cirrhosis_patient_survival_prediction/
    """
    bibtex = """
        @article{dickson1989prognosis,
          title={Prognosis in primary biliary cirrhosis: model for decision making},
          author={Dickson, E Rolland and Grambsch, Patricia M and Fleming, Thomas R and Fisher, Lloyd D and Langworthy, Alice},
          journal={Hepatology},
          volume={10},
          number={1},
          pages={1--7},
          year={1989},
          publisher={Wiley Online Library}
        }
    """
    curation_comments = """
        We start with the UCI copy (878) of the Mayo Clinic PBC data (Fleming and Harrington 1991, appendix D): 418 patients, 312 in the D-penicillamine trial and 106 outside it who agreed to be followed.

        - The source is a survival study: N_Days runs from registration to death, liver transplant or the July 1986 analysis, and Status says which. The label is death or transplant within 5 years (5 * 365.25 days, so day 1,826 or earlier), the transplant-free survival that the GLOBE score predicts (Lammers et al. 2015, Gastroenterology), against 5 years of follow-up without either.
        - We keep only the patients registered early enough for 5 years of follow-up, up to about mid-1981. A later patient could enter only with an early death or transplant (25 of the 109 did, the rest are censored), so keeping them would select on the outcome.
        - The data have no registration date. IDs follow the registration order within the trial and within the other patients, so a patient counts as registered in time when someone registered at or after them in the same group was followed 5 years.
        - We drop the 5 patients lost to follow-up before 5 years. 304 patients remain, 107 with the event (103 deaths, 4 transplants).
        - We drop ID, and N_Days and Status, which define the label.
        - The other columns are the baseline values taken at registration (the follow-up visits are in the separate pbcseq file), so all stay. The 66 patients outside the trial have no drug, ascites, hepatomegaly, spiders, copper, alkaline phosphatase or SGOT; these stay missing.
        - Until 2026-10-14 the task regressed the log time to death over the 161 patients who died. That is right truncation: a patient registered in 1982-84 entered only with a death within about 3 years (median 1.86 years, against 3.98 for 1974-76), so the label partly measured the calendar window.
    """

    # Task
    target = "death_or_transplant_within_5y"
    problem_type = "binary_classification"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "cirrhosis.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        cohort = _cohort(df)
        # a patient registered too late for 5 years of follow-up could only enter with an early event
        keep = cohort["covered"] & (cohort["event"] | cohort["followed"])
        df = df.loc[keep]
        df["death_or_transplant_within_5y"] = cohort.loc[keep, "event"].astype(int)
        df = drop_columns(df, ["ID", "N_Days", "Status"])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "Drug",
                "Ascites",
                "Hepatomegaly",
                "Spiders",
                "Edema",
                "Stage",
                "Sex",
            ],
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        cohort = _cohort(raw)
        outcome = pd.Series("censored before 5 years (dropped)", index=raw.index)
        outcome.loc[cohort["followed"]] = "followed 5 years without event"
        outcome.loc[cohort["event"]] = "death or transplant within 5 years"
        registered = cohort["covered"].map(
            {True: "early enough for 5 years of follow-up (kept)", False: "too late (dropped)"}
        )
        table = pd.crosstab(registered.rename("registered"), outcome.rename("outcome"), margins=True)
        return [
            Decision(
                title="Only patients registered early enough to be followed 5 years",
                why=(
                    "Follow-up ended in July 1986 for everyone, so a patient registered after about mid-1981 could "
                    "only be seen with an event within 5 years, never without one. Keeping them would add positives "
                    "chosen by their outcome."
                ),
                evidence=table,
            )
        ]
