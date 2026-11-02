"""Curated dataset definition for `rand_health_insurance_experiment_doctor_visits` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import io
import struct
from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Grouping,
    Metric,
    TaskSummary,
    drop_columns,
)

# Columns of randdata.dta that are derived from other columns (statsmodels' randhie page documents lpi and fmde).
DERIVED = [
    "logc",  # ln(coins + 1), but 0 for plans 2-4 (coins 100) and ln(96) for plan 13 (coins 0); `plan` is kept
    "lpi",  # ln(max(1, participation incentive)); `pioff` is kept
    "fmde",  # ln(max(1, mdeoff / (0.01 coins))) with 95 for plan 13; 0 for plans 1-4 and the free plan 11
    "linc",  # log(income + 1)
    "lfam",  # log(family size)
    "lnum",  # equal to lfam
    "child",  # age under 18
    "fchild",  # female x child
    "xghindx",  # ghindx with its missing values filled in
    "binexp",  # meddol > 0
    "lnmeddol",  # log(meddol)
]

# Values the extract filled in with one mean per site or site group (disea: 2,072 of the 2,074 children under 14).
FILLS = {
    "disea": {1: 13.7319, 2: 11.8427, 3: 9.9673, 4: 9.9673, 5: 10.5763, 6: 10.5763},
    "mhi": {1: 74.3683, 2: 81.3527, 3: 83.3914, 4: 83.3914, 5: 77.4003, 6: 77.4003},
    "educdec": {1: 12.3251, 2: 12.7567, 3: 11.3874, 5: 10.9698, 6: 10.6277},
}
HEALTH_FLAGS = ["hlthg", "hlthf", "hlthp"]

RENAME = {
    "year": "study_year",
    "coins": "coinsurance_rate",
    "idp": "individual_deductible_plan",
    "mdeoff": "max_dollar_expenditure",
    "pioff": "participation_incentive",
    "tookphys": "took_baseline_physical",
    "xage": "age",
    "educdec": "education_of_decision_maker",
    "num": "family_size",
    "mhi": "mental_health_index",
    "disea": "chronic_disease_index",
    "physlm": "physical_limitation",
    "ghindx": "general_health_index",
    "outpdol": "outpatient_spending",
    "drugdol": "drug_spending",
    "suppdol": "supplies_spending",
    "mentdol": "psychotherapy_spending",
    "inpdol": "inpatient_spending",
    "meddol": "medical_spending",
    "totadm": "hospital_admissions",
    "inpmis": "inpatient_charges_missing",
    "mentvis": "psychotherapy_visits",
    "mdvis": "md_visits",
    "notmdvis": "non_md_visits",
}

TARGET = "medical_spending_next_year"
NEWHOUSE_1989 = "https://pmc.ncbi.nlm.nih.gov/articles/PMC4192960/"


def read_stata_110(path: Path) -> pd.DataFrame:
    """Read randdata.dta, a Stata 7 file (format 110) that pandas does not read.

    Format 110 differs from format 111 (Stata 7 SE, which pandas reads) here only in the type codes: every one of the
    45 columns is a 4-byte float, coded ``f`` (102) in format 110 and 254 in format 111. Header: version, byte order,
    file type, padding, the variable count (2 bytes), the observation count (4 bytes), an 81-byte label and an 18-byte
    time stamp, then one type byte per variable.
    """
    buf = bytearray(path.read_bytes())
    n_vars = struct.unpack("<H", bytes(buf[4:6]))[0]
    types_at = 10 + 81 + 18
    assert buf[0] == 110, "expected a Stata format-110 file"
    assert buf[1] == 2, "expected little-endian byte order"
    assert set(buf[types_at : types_at + n_vars]) == {102}, "expected only float columns"
    buf[0] = 111
    buf[types_at : types_at + n_vars] = bytes([254]) * n_vars
    return pd.read_stata(io.BytesIO(bytes(buf)), convert_categoricals=False)


def first_years(raw: pd.DataFrame) -> pd.DataFrame:
    """One row per person, the first study year on file, in person-id order."""
    return raw.sort_values(["zper", "year"], kind="stable").drop_duplicates("zper")


def family_ids(persons: pd.DataFrame) -> pd.Series:
    """Families as runs of consecutive person ids with the same site, plan and income, indexed by person id."""
    key = persons[["site", "plan", "income"]]
    return pd.Series((key != key.shift()).any(axis=1).cumsum().to_numpy(), index=persons["zper"].to_numpy())


def unasked_children(persons: pd.DataFrame) -> pd.Series:
    """Persons under 14 at entry with a filled `physlm` and no self-rated health flag: never asked."""
    filled = persons["physlm"].notna() & ~persons["physlm"].isin([0.0, 1.0])
    no_flag = persons[HEALTH_FLAGS].sum(axis=1) == 0
    return persons.loc[(persons["xage"] < 14) & filled & no_flag, "zper"]


class RandHealthInsuranceExperimentDoctorVisits(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "How much will a person under 65 spend on medical care next year, given this year's visits and spending, "
            "their health at enrolment and their insurance plan?"
        ),
        use_case=(
            "A payer sets next year's capitation payment per enrollee of a health maintenance organisation; Newhouse "
            "et al. (1989) used these data to measure how well prior use and health measures predict a person's "
            "annual spending, as adjusters of Medicare's per-enrollee payment (the AAPCC)."
        ),
        row=(
            "One person in one study year of the RAND Health Insurance Experiment (six US sites, 1974-1982, ages 0 "
            "to 63) whose next study year is on file too: 14,214 person-years of 5,638 persons in 2,258 families, "
            "from Cameron and Trivedi's person-year extract."
        ),
        predicted=(
            "The person's medical spending in the next study year, in dollars: all medical services except dental and "
            "outpatient mental health care (outpatient care, drugs, supplies, hospital stays). 23% of the years have "
            "none."
        ),
        known=(
            "This year's doctor and other visits, hospital admissions and spending by type; age, sex, race and family "
            "size; health at enrolment (self-rated health, health indexes, chronic disease, physical limitation); the "
            "site and the insurance plan (coinsurance, deductible, out-of-pocket cap, the experiment's participation "
            "payment)."
        ),
        split=(
            "Whole families are held out, so the test data stands for enrollees outside the sample a formula is "
            "calibrated on, each with their own past year known. The test years are the same study years as the "
            "training years: the extract has no calendar years, so next year's change is not tested."
        ),
        changes=(
            "We pair each person-year with the person's next year and predict that year's spending; we drop the "
            "derived copies of columns and the family income, whose timing cannot be checked; we set the values the "
            "extract filled in (race, physical limitation, chronic disease, mental health, the decision maker's "
            "education, and self-rated health for children never asked) to missing; and we drop 52 years whose "
            "hospital charges are missing."
        ),
        fit="approximate",
        fit_reason=(
            "The source's own question on its own data, but a 1970s experiment: enrollees under 65 randomised to "
            "plans, 1970s prices and care, health at enrolment only (the paper also used an exit examination), no "
            "claims diagnoses and no welfare flag, which payment formulas use, and no calendar years, so the drift "
            "between calibrating a formula and using it is not tested."
        ),
    )

    # Dataset
    unique_name = "rand_health_insurance_experiment_doctor_visits"
    year = "1995"
    domain = "medical & healthcare"
    source = "Other"
    source_url = "https://doi.org/10.3886/ICPSR06439.v1"
    license = (
        'Public domain (statsmodels\' randhie page: "This is in the public domain."); ICPSR 6439 lists no access '
        "restriction"
    )
    data_tags = ("Spatial", "ForcedGroupedFromTemporal")
    download_description = """
        mkdir -p local-data-warehouse/rand_health_insurance_experiment_doctor_visits
        wget -O local-data-warehouse/rand_health_insurance_experiment_doctor_visits/randdata.dta \\
            http://cameron.econ.ucdavis.edu/mmabook/randdata.dta
        # sha256 8364cf9e53e32c794bcf0313a1590adcedf4e0526ba792884c7978cde169a628 (downloaded 2026-10-30).
        # A copy: Cameron and Trivedi's "Authors' extract" of the RAND Health Insurance Experiment (data page
        # http://cameron.econ.ucdavis.edu/mmabook/mmadata.html, Microeconometrics, 2005, pp. 553-6 and 671-4), cut from
        # the experiment's public-use files, ICPSR 6439 (first released 1995-06-05).
    """
    bibtex = """
        @misc{newhouse1995randhie,
          author = {Newhouse, Joseph P.},
          title = {{RAND} Health Insurance Experiment [in Metropolitan and Non-Metropolitan Areas of the United
                   States], 1974--1982},
          howpublished = {Inter-university Consortium for Political and Social Research, ICPSR 6439},
          year = {1995},
          doi = {10.3886/ICPSR06439.v1},
          note = {Person-year extract randdata.dta from A. C. Cameron and P. K. Trivedi (2005), Microeconometrics:
                  Methods and Applications, Cambridge University Press}
        }
    """
    curation_comments = """
        We start with randdata.dta, Cameron and Trivedi's person-year extract of the RAND Health Insurance Experiment
        (20,190 rows x 45 columns, 5,912 persons, study years 1 to 5). The experiment's public-use files it was cut
        from, ICPSR 6439, need a login and have not been read (403 on 2026-11-01). The name says doctor visits, the
        screening's first target; the target is next-year medical spending, and the visit counts are features.

        - Prediction point: the end of a study year. The target is the person's medical spending in the next study
          year (`meddol` of year t + 1), the dependent variable of Newhouse et al. 1989 (Health Care Financing Review
          10(3), "Dependent variables": "Our major interest was to estimate or predict annual expenditures for medical
          care services in constant dollars. The unit of analysis was the person-year [...] virtually all medical
          services other than dental and outpatient mental health services"). `meddol` equals outpatient + drugs +
          supplies + inpatient spending in 20,188 of 20,190 rows.
        - Reading: pandas does not read Stata format 110, so `_load_raw` changes the version byte and the type codes
          (all 45 columns are 4-byte floats) to format 111; the 10 columns of statsmodels' own conversion of the file
          (its `randhie` dataset) equal ours in all 20,190 rows.
        - Rows: each person-year paired with the same person's next study year, 14,266 pairs of 5,639 persons; the
          273 persons without two consecutive years drop out. As in the source, the first year is never a target:
          "we did not use those in their first year of participation because we did not have comparable prior-use
          data for them" (Newhouse et al., "Source of data").
        - Dropped rows: the 52 pairs whose target year has `inpmis` = 1 ("missing any inpatient charges"): every one
          had a hospital admission, and the recorded spending lacks part of its inpatient charges (68 of the 80 such
          person-years record some; median $264), so it is not the task's quantity.
        - Features: year t's visits, admissions and spending by type, the family size and age that year, and the
          baseline columns. The source's prior-use adjusters are "whether there was any outpatient
          expenditure, whether there was any inpatient expenditure, and the logarithms of outpatient and inpatient
          expenditures"; we ship the amounts and counts they come from.
        - Not features: the target year's other outcomes and its eligible fraction. The fraction is below 1 for 37
          targets, each the person's last year on file, 19 of them in study year 2, before any planned end: the year
          is cut short by what happens in it (deaths, exits), so it is not a period known when a payment is set. The
          37 rows stay unannualised (a payer bears these costs); they average $2,408 against $172 and hold 5.6% of the
          target's sum of squares. Year t's eligible fraction (`time`) is dropped as constant: all 45 partial years
          are a person's last year on file, never a year t.
        - Group: the family, rebuilt in `_clean` as runs of consecutive person ids (`zper`) with the same site, plan
          and income: 2,258 families in the shipped rows, at most 10 persons and 33 rows. The out-of-pocket cap and
          the participation incentive, outside the key, take one value in 99.8% and 99.5% of the 1,407 families of two
          or more; adjacent families that share an income are merged, which holds more together, not less. `zper`
          leaves the table: its leading digit is the site and its numbers run in family order.
        - `income` is dropped: its label is cut off ("income based on annual income r..."), it takes one value in all
          of a person's years, it is not the income the out-of-pocket cap was set from (cap / income varies within a
          plan), and it holds one site-mean fill per site (563 persons). Whether it averages later years cannot be
          checked (LEAK-10); the ICPSR 6439 codebook would settle it. Dropping it moved R2 by 0.0004 at most.
        - Dropped as derived copies: `logc` (ln(`coins` + 1), but coded 0 for plans 2-4 and ln(96) for plan 13),
          `lpi` (ln(max(1, incentive))), `fmde` (ln(max(1, `mdeoff` / (0.01 `coins`))) with 95% for plan 13, 0 for
          plans 1-4 and the free plan), `linc`, `lfam`, `lnum`, `child` (age under 18), `fchild`, `binexp` (`meddol` >
          0), `lnmeddol` and `xghindx` (`ghindx` with filled-in values). We keep the raw quantities and `plan`.
        - `hlthg`, `hlthf`, `hlthp` become one `self_rated_health` (excellent when none is set; at most one is set in
          every row). For children under 14 at entry with a filled `physlm`, no flag set means never asked: 346 of
          these 371 children read excellent, against 65% of the other children, so for them it is missing.
        - Missing values restored (Decision 1): the extract filled gaps with one mean per site or site group. `black`
          (81 persons, 0.511 at site 6) and `physlm` (433 persons) hold fractional values in a 0/1 flag; `disea` holds
          four site-group constants for 2,387 persons (2,072 of the 2,074 children), `mhi` four for 1,133 persons and
          `educdec` five for 68. All become missing (a mean over rows that include the test persons; the pipeline
          imputes); with the income drop this moved R2 by under 0.001. `general_health_index` is missing for every
          person of site 1 and for 5-9% elsewhere: kept missing.
        - Note: `chronic_disease_index` is 100 x the count of chronic diseases / the length of the list, to one
          decimal: 23 diseases at site 1, 29 elsewhere, so one scale (a share of the list). The health measures change
          instrument at age 14 (the 38-item mental health index is for adults; `general_health_index`, an adult
          scale, is present for 71% of the rows under 14); age is a feature.
        - Note: the plan columns are the experiment's randomised treatment. A payer knows an enrollee's cost sharing
          (coinsurance, deductible, out-of-pocket cap), and Newhouse et al. regress expenditures on plan first, so they
          stay. `coinsurance_rate` follows the file's coding, which its own `logc` and `fmde` contradict for the
          deductible plans: plan 13 (the individual deductible plan of sites 2-6) is coded 0 where they code 95%, plans
          2-4 are coded 100 where `logc` codes 0. `plan`, a category, is the reliable identity. The participation
          incentive is a payment of the experiment no payer makes; it is known at enrolment and stays.
        - Note: all ages are kept (31% of the rows are under 14); Newhouse et al. keep persons 14 or older "because our
          measures of health status are different for persons of younger ages", while a capitation covers children.
          They also keep only persons who completed the study and its exit examination; requiring completion would
          select on the future, and the extract has no exit examination.
        - Note: the target ships in dollars, not logged. The metric is R2 in dollars and a capitation pays the mean; a
          model fit on logs would need a retransformation (the source uses Duan's smearing estimator). The extract's
          price base is not stated on the data page.
        - Note: 22.7% of the target years are 0 (no medical spending that year); the maximum is $39,182 and the SD
          four times the mean ($726 against $178), so the R2 of a fold moves with its few largest stays: the largest
          row alone holds 41-44% of the sum of squares of each of the 3 test folds that hold it. Newhouse et al.
          estimate the maximum R2 for total expenditure at 14.5% ("Results").
    """

    # Task
    target = TARGET
    problem_type = "regression"
    metric = Metric.source(
        "r2",
        original=(
            "Efron's R2 of annual medical expenditure, 1 - sum((y - yhat)^2) / sum((y - ybar)^2), reported as a share "
            "of the maximum R2 after removing the plan-only R2"
        ),
        reference=f"{NEWHOUSE_1989} (Methods, Estimation methods, eq. 3)",
        definition=(
            "1 - SS_res / SS_tot of next-year medical spending in dollars. The paper's share, ((R2(b) - R2(plan)) / "
            "(1 - R2(plan))) / max R2, increases with R2(b) on a fixed sample, so it ranks models the same."
        ),
    )
    grouping = Grouping(
        on="family_id",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a family: a run of consecutive person ids (`zper`) with the same site, plan and income, the
            values a family shares (2,258 families, 1 to 10 persons, up to 33 rows, one per person and consecutive
            pair of study years). A capitation formula is calibrated on one population and applied to enrollees
            outside it (Newhouse et al. 1989, Introduction: "Medicare pays the HMO an amount per enrollee that is based
            on Medicare payments per fee-for-service beneficiary in the county"), with each enrollee's previous year
            as an input. New enrollees join as families, so the test families are new and their past year is in the
            features. Members of a family share the plan and their spending is correlated (Newhouse et al., "Source of
            data": "a husband's and wife's utilization could be expected to be correlated"), and the baseline columns
            are constant within a person, so a random split would let a model recognise persons and their families.
            Holding families together instead of persons moves R2 within the spread over repeats (ridge 0.0870
            against 0.0866 over 20 repeats, random forest 0.0860 against 0.0889 over 6; SD of the repeat means 0.006).
        """,
    )
    splits_comment = """
        Grouped 3-fold splits by family (`family_id`), forced from temporal (SPLIT-8): every year of a family stays on
        one side. A payer calibrates its formula on past years and applies it to the next, but the extract has study
        years 1 to 5 and no calendar years (the six sites started at different dates). Test windows by the target's
        study year keep at least half the rows for training only for year 4 (76.4% of the rows train) and year 5
        (88.2%; year 3 would train on 38.4%), where SPLIT-14 asks for three windows, and years 4 and 5 hold only the
        5-year enrollees. On those windows untuned random forest / ridge reach R2 0.151 / 0.127 (year 4) and 0.112 /
        0.111 (year 5), against 0.131 / 0.127 and 0.093 / 0.107 on the same rows of these folds (mean of 3 repeats),
        so the forced split is no more optimistic than the valid windows. A release with calendar years (ICPSR 6439,
        or the sites' start dates) should get a temporal split. A leak test across the folds finds none: no feature row
        recurs across the split, a person-level key (baseline values and birth cohort) links 0.2% of test rows to
        training, and the training side's mean target of the test row's site and study year adds nothing (LightGBM
        -0.004, ridge +0.000 R2; a placebo cell mean -0.000). Shipped forced on the curator's call (Andrej,
        2026-11-02: "Forced group splits should be fine").
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return read_stata_110(raw_dir / "randdata.dta")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.astype("float64")
        for col in ["zper", "year", "site", "plan"]:
            df[col] = df[col].astype("int64")

        # The group: families rebuilt from the raw income before it is dropped (a grouping column, never a feature).
        persons = first_years(df)
        df["family_id"] = df["zper"].map(family_ids(persons))
        unasked = unasked_children(persons)

        # Values the extract filled in (a mean per site or site group) become missing again.
        for col in ["black", "physlm"]:
            df[col] = df[col].where(df[col].isin([0.0, 1.0]))
        for col, by_site in FILLS.items():
            df[col] = df[col].mask((df[col] - df["site"].map(by_site)).abs() < 1e-3)

        # Self-rated health: three flags against the omitted category "excellent"; missing for children never asked.
        assert (df[HEALTH_FLAGS].sum(axis=1) <= 1).all()
        rating = np.select(
            [df["hlthp"] == 1, df["hlthf"] == 1, df["hlthg"] == 1], ["poor", "fair", "good"], default="excellent"
        )
        df["self_rated_health"] = pd.Series(rating, index=df.index).where(~df["zper"].isin(unasked))
        # `income`: the label is cut off and its timing cannot be checked (LEAK-10).
        df = drop_columns(df, [*DERIVED, *HEALTH_FLAGS, "income"])

        # Pair each person-year with the same person's next study year: its spending is the target.
        nxt = df[["zper", "year", "meddol", "inpmis"]].rename(columns={"meddol": TARGET, "inpmis": "next_inpmis"})
        nxt["year"] = nxt["year"] - 1
        df = df.merge(nxt, on=["zper", "year"], how="inner", validate="one_to_one")

        # A target year with missing inpatient charges records only part of the year's spending.
        df = df.loc[df["next_inpmis"] == 0]
        # The eligible fraction of year t is 1 in every pair: all 45 partial years are a person's last year on file.
        # `zper` encodes the site and the family order; the family id replaces it as the group.
        df = drop_columns(df, ["next_inpmis", "time", "zper"])
        return df.rename(columns=RENAME)

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "site",
                "plan",
                "individual_deductible_plan",
                "took_baseline_physical",
                "black",
                "female",
                "physical_limitation",
                "self_rated_health",
                "inpatient_charges_missing",
            ],
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        persons = first_years(raw)
        rows = []
        for col in ["black", "physlm"]:
            filled = persons.loc[~persons[col].isin([0.0, 1.0])]
            for (site, value), n in filled.groupby(["site", col]).size().items():
                rows.append(
                    {"column": RENAME.get(col, col), "site": int(site), "value": f"{value:.4f}", "persons": int(n)}
                )
        for col, by_site in FILLS.items():
            for site, value in by_site.items():
                n = int(((persons[col] - value).abs() < 1e-3).loc[persons["site"] == site].sum())
                rows.append({"column": RENAME[col], "site": site, "value": f"{value:.4f}", "persons": n})
        unasked = persons.loc[persons["zper"].isin(unasked_children(persons))]
        for site, n in unasked.groupby("site").size().items():
            rows.append({"column": "self_rated_health", "site": int(site), "value": "excellent", "persons": int(n)})
        return [
            Decision(
                title="Values the extract filled in set to missing",
                why=(
                    '`black` and `physlm` are yes/no flags (statsmodels: physlm is "1 if the person has a physical '
                    "limitation\"), yet a few persons per site hold one fractional value: a mean the extract's makers "
                    "filled in. `disea`, `mhi` and `educdec` hold one constant per site or site group, each close to "
                    "the observed mean there; the `disea` constant is held by 2,072 of the 2,074 children under 14. "
                    'Self-rated health reads "excellent" (no flag set) for 346 children under 14 at entry with a '
                    "filled `physlm`: never asked. All become missing, and the pipeline imputes."
                ),
                evidence=pd.DataFrame(rows),
            )
        ]
