"""Curated dataset definition for `nhanes_dxa_body_fat` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    FeatureTypes,
    Metric,
    Source,
    TaskSummary,
    Temporal,
    TemporalSplits,
    decode,
)

# The survey cycles with whole-body DXA, by the suffix of their files: the first year of each two-year cycle. NHANES ran
# no DXA in 2007-2010 and none after 2017-2018.
CYCLES = {"": 1999, "_B": 2001, "_C": 2003, "_D": 2005, "_G": 2011, "_H": 2013, "_I": 2015, "_J": 2017}
OLD_ERA = ["", "_B", "_C", "_D"]
# DEMO's cycle code (SDDSRVYR) to the cycle's first year.
SDDSRVYR_YEAR = {1: 1999, 2: 2001, 3: 2003, 4: 2005, 7: 2011, 8: 2013, 9: 2015, 10: 2017}

# DXX 2011-2018: the bone and soft-tissue invalidity code of each of the six regions (0 = valid data).
REGION_VALIDITY = [f"DXA{region}{tissue}V" for region in ("HE", "LA", "LL", "RA", "RL", "TR") for tissue in ("B", "T")]
# DXX: the status, the imputation flag of the whole-body values (DXITOT, named DXITOTST in 2005-2006), the region
# validity codes (2011-2018) and the target. Every other DXA column (regional and total fat, lean and bone mass) is an
# outcome of the same scan and is not read.
DXX_COLUMNS = ["SEQN", "_MULT_", "DXAEXSTS", "DXITOT", "DXITOTST", *REGION_VALIDITY, "DXDTOPF"]
DEMO_COLUMNS = [
    "SEQN",
    "SDDSRVYR",
    "RIDSTATR",
    "RIDEXMON",
    "RIAGENDR",
    "RIDAGEYR",
    "RIDRETH1",
    "RIDRETH3",
    "RIDEXPRG",
]
# RIDRETH3 (DEMO_G on, 2011-2018) codes non-Hispanic Asians as 6; RIDRETH1 counts them in "Other race".
RIDRETH3_ASIAN = 6

# The tape-and-scale measures taken in every cycle, renamed (BMX codebooks).
COMMON_MEASURES = {
    "BMXWT": "weight_kg",
    "BMXHT": "standing_height_cm",
    "BMXBMI": "bmi",
    "BMXLEG": "upper_leg_length_cm",
    "BMXARML": "upper_arm_length_cm",
    "BMXARMC": "arm_circumference_cm",
    "BMXWAIST": "waist_circumference_cm",
}

# Codebook words (DEMO): RIAGENDR and RIDRETH1, the same codes in every cycle; from 2011 the non-Hispanic Asians of
# RIDRETH3 get their own level (step 5 of `_clean`).
CODE_LABELS = {
    "sex": {1: "Male", 2: "Female"},
    "race_ethnicity": {
        1: "Mexican American",
        2: "Other Hispanic",
        3: "Non-Hispanic White",
        4: "Non-Hispanic Black",
        5: "Other race, including multi-racial",
    },
}


class NhanesDxaBodyFat(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "What is a person's whole-body fat percentage, as a DXA scan measures it, judging from sex, age, ethnicity "
            "and a tape and a scale?"
        ),
        use_case=(
            "A clinician, a screening programme or a gym estimates body fat, and so body-fat obesity, from weight, "
            "height and a few tape measures instead of a DXA scan, as the relative fat mass equation built on these "
            "files does (Woolcott and Bergman 2018). The tested population is aged 8-59: no one older was scanned "
            "after 2010."
        ),
        row=(
            "One person aged 8 or over examined by the US National Health and Nutrition Examination Survey in one of "
            "the eight two-year cycles with whole-body DXA (1999-2006, 2011-2018), whose whole-body percent fat CDC "
            "measured, not imputed, on a scan with every body region valid."
        ),
        predicted="The whole-body fat percentage of the DXA scan taken at the same examination.",
        known=(
            "The survey cycle, sex, age, race and ethnicity, weight, height, body-mass index, waist and upper-arm "
            "circumference, and upper-leg and upper-arm length."
        ),
        split=(
            "Each of the four newest cycles (2011-2012, 2013-2014, 2015-2016, 2017-2018) is the test data once, with "
            "every earlier cycle for training, so the test people stand for people met after the equation was fitted."
        ),
        changes=(
            "We keep only measured scans with every body region valid, the rule CDC's analysts apply to both eras, "
            "not CDC's imputed ones, and only the measures taken in every cycle (skinfolds, thigh, calf, sagittal "
            "diameter and hip were each taken in some cycles only); from 2011 non-Hispanic Asians get their own "
            "ethnicity level."
        ),
        fit="direct",
        fit_reason=(
            "The features are what a tape, a scale and a short interview give, and the label is the scan they "
            "replace. The scanner and its software changed between 1999-2006 and 2011-2018, and many of the heaviest "
            "people have no usable scan, so the sample thins the top of the range."
        ),
    )

    # Dataset
    unique_name = "nhanes_dxa_body_fat"
    domain = "medical & healthcare"
    sources = (
        Source(
            role="publication",
            platform="GOV Website",
            url="https://wwwn.cdc.gov/nchs/nhanes/dxa/dxa.aspx",
            license="Public domain (US federal government data); the NCHS data user agreement applies",
            year="2008",
            bibtex=r"""
                @misc{nchs2008nhanesdxa,
                  author       = {{Centers for Disease Control and Prevention, National Center for Health Statistics}},
                  title        = {{National Health and Nutrition Examination Survey: Dual-Energy X-ray Absorptiometry,
                                  Whole Body (DXX), 1999-2006 and 2011-2018}},
                  year         = {2008},
                  howpublished = {\url{https://wwwn.cdc.gov/nchs/nhanes/dxa/dxa.aspx}},
                  note         = {First published January 2008 (1999-2000 file); cycles 2011-2018 published March 2020}
                }
            """,
            files=("DXX*.xpt",),
        ),
        Source(
            role="part",
            platform="GOV Website",
            url="https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/BMX_J.htm",
            license="Public domain (US federal government data); the NCHS data user agreement applies",
            name="NHANES Body Measures (BMX), the same eight cycles",
            files=("BMX*.xpt",),
        ),
        Source(
            role="part",
            platform="GOV Website",
            url="https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/DEMO_J.htm",
            license="Public domain (US federal government data); the NCHS data user agreement applies",
            name="NHANES Demographics (DEMO), the same eight cycles",
            files=("DEMO*.xpt",),
        ),
    )
    download_description = """
        We download three files per survey cycle from CDC: the whole-body DXA file, the body measures and the
        demographics (8 cycles, 24 SAS transport files, 180 MB).

        mkdir -p local-data-warehouse/nhanes_dxa_body_fat && cd local-data-warehouse/nhanes_dxa_body_fat
        for ys in 1999: 2001:_B 2003:_C 2005:_D 2011:_G 2013:_H 2015:_I 2017:_J; do
          y=${ys%%:*}; s=${ys#*:}
          for f in DXX DEMO BMX; do
            wget "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/$y/DataFiles/$f$s.xpt"
          done
        done
    """
    curation_comments = """
        We start with the NHANES whole-body DXA files (DXX), joined on the participant number `SEQN` to the body
        measures (BMX) and demographics (DEMO) of the same cycle, for the eight cycles with DXA (1999-2006, 2011-2018).

        - Prediction point: the examination, once weight, height and the tape measures are taken and before (or
          instead of) a DXA scan. Every feature is recorded at that examination; the scan is taken the same day.
        - Target: `DXDTOPF`, whole-body percent fat, renamed `percent_body_fat`. Every other DXA column (regional fat,
          lean and bone mass, total fat mass) is an outcome of the same scan and is never read.
        - Measured whole-body values only, by the rule each era's release allows. 1999-2006: CDC filled missing and
          invalid scans by multiple imputation (five records per person, `_MULT_`): "Imputed values should not be
          treated as measured variables" (DXX_D). We keep the first record of people whose whole-body flag (`DXITOT`,
          `DXITOTST` in 2005-2006) is 0 and whose percent fat is the same in all five records, as DXX_D says a fully
          measured person's records are. The second test drops 90 people whose flag reads 0 but whose percent fat
          varies across the records: 80 in 2003-2004 (by up to 4.6 points) and 10 in 2005-2006, where the bone flag
          marks an imputation (by 0.1 point). 2011-2018 has no imputation: we keep completed scans (`DXAEXSTS` 1) with
          a percent fat and every region valid (the twelve bone and soft-tissue invalidity codes `DXA..BV`/`DXA..TV`
          of the six regions all 0). CDC publishes the whole-body value there also when one region of the scan is
          invalid ("If any region was coded as invalid all bone and soft tissue measurements for that region were set
          to missing", DXX_J); we drop those 893 scans (140, 148, 241 and 364 per cycle, 154 of them with the trunk
          coded "excessive x-ray noise due to morbid obesity"), as CDC's own analysts do when they compare the eras:
          "Those with any missing data during 2011–2018 did not have total body adiposity measures calculated and
          were excluded" (Stierman et al. 2021, Am J Clin Nutr 114:1495). So both eras keep a scan only when every
          region is valid: 1999-2006 imputed every scan with an invalid region, and imputed scans are dropped. This
          keeps 38,708 people: 21,768 in 1999-2006 (5,491 dropped as imputed) and 16,940 in 2011-2018 (4,671, 6,425,
          5,797, 4,875, 4,381, 4,908, 4,357 and 3,294 per cycle). `SEQN` is unique.
        - Selection Bias: pregnant women were not scanned, nor people over the table limit (300 lb in 1999-2006, 450 lb
          and 6 ft 5 in later). The heaviest people often have no usable scan, and both eras drop every scan with an
          invalid region:
          - 1999-2006: every scan with an invalid region was imputed, and imputed scans are dropped here; the heaviest
            people had most of them (76% of people with BMI 40 or more have an imputed scan, 13% below BMI 25).
          - 2011-2018: the 893 dropped scans with an invalid region (10% of the 2017-2018 cycle) have median BMI 33.6
            against 24.9 for fully valid scans; 149 of the 2017-2018 ones have the trunk coded "excessive x-ray noise
            due to morbid obesity".
          - 2011-2018: completed scans without a whole-body value grow from 4.8% of 2011-2012 to 15.6% of 2017-2018,
            and these people are heavier (median BMI 29.9 against 25.7). In 2017-2018 only 28% of examined adults aged
            20-59 with BMI 40 or more have a kept scan, against 70% of those below BMI 30 (49% and 74% if the scans
            with an invalid region were kept).
          CDC warns that "use of only the measured variables could lead to biased results" for population estimates;
          for an equation it means fewer very heavy people than a clinic meets.
        - Features: the measures taken in every cycle (weight, height, BMI, upper-leg and upper-arm length, upper-arm and
          waist circumference), sex, age in years, race and ethnicity and the cycle's first year. BMI is weight over
          height squared as CDC computes it, kept as released.
        - Left out, each because it was taken in some cycles only: thigh and calf circumference and the triceps and
          subscapular skinfolds (1999-2006 only: missing in every test row of every window), hip circumference
          (2017-2018 only: missing in every training row) and the sagittal abdominal diameter (`BMDAVSAD`, 2011-2016
          only). The diameter is the one such measure some windows hold on both sides (2013-2014 and 2015-2016, where
          it gains 0.004 and 0.012 RMSE points), but every 2017-2018 test row lacks it while 38% of that window's
          training rows carry it: there it raised the RMSE from 3.350 to 3.405 and turned the Asian rows' mean error
          from +0.58 to -0.91 points (untuned LightGBM, 5 seeds), and the newest window is the period a deployed
          equation meets. The exam's six-month period (`RIDEXMON`) is not a measurement of the person; the
          survey weights describe the sample design and are not read.
        - Race and ethnicity: `RIDRETH1`, the coding of every cycle, plus a "Non-Hispanic Asian" level from `RIDRETH3`
          for 2011-2018, when NHANES began to oversample Asian Americans. `RIDRETH1` counts them in "Other race", which
          holds 3-5% of the 1999-2006 rows and 17-25% of the 2011-2018 rows, two thirds or more of them Asian. Asians
          of 1999-2006 stay in "Other race": those cycles do not code them apart. Asians carry more fat at a given
          BMI. Measured in the 2017-2018 test window (untuned LightGBM, 5 seeds; mean error, measured minus predicted,
          for its 544 Asian people), the level moves it from +0.94 to +0.58 points.
        - Missing measures stay missing and the rows stay (0.3% to 0.9% per measure), as at an examination where one
          measure could not be taken.
        - Duplicates: no row repeats; a few rows share every feature with another person and differ in percent fat,
          natural for different people with the same rounded measures.
        - Note: the 5% shift of lean to fat mass is in both eras (DXX_D for the QDR-4500A data; DXX_G: "The NHANES BCA
          option was enabled ... this option adds 5% of lean mass to the fat mass"), so it is no break between them.
          The break is the scanner and software: a Hologic QDR-4500A in 1999-2006 (software 8.26, then Discovery 12.4
          from 2005), Hologic Discovery A with Apex in 2011-2018.
        - Ages: DXA was offered at 8-85 in 1999-2004, 8-69 in 2005-2006 and 8-59 in 2011-2018 (the documentation of each
          cycle), so the test cycles hold ages 8-59 and the older people are in training only. Children and
          adolescents are kept: the paediatric relative fat mass was built on these files (Woolcott and Bergman 2019).
        - Note: this task replaces body_density_prediction's (252 men of 1985, body density by underwater weighing) with
          another reference method for the same use case; the two scores are not comparable.
        - Metric: RMSE in percent-fat points, unweighted (fallback; the metric's reason says where we looked and why
          the survey weights are not used).
    """

    # Task
    target = "percent_body_fat"
    problem_type = "regression"
    metric = Metric.fallback(
        reason=(
            "NHANES defines no prediction task. The relative fat mass paper on these files (Woolcott and Bergman "
            "2018, Sci Rep 8:10980) chose its equation by several criteria together (R^2, RMSE, AIC, bias, accuracy, "
            "precision and simplicity) and Lee et al. 2017 (Br J Nutr 118:858) report R^2 and the standard error of "
            "estimate, so no source fixes one metric; RMSE in percent-fat points, which both report, is the regression "
            "fallback. The paper's RMSE was survey-weighted and pooled over the five imputations; ours is unweighted on "
            "measured scans, because a clinician scores the patient in front of them, not the US population."
        ),
    )

    # Splits
    split_leaf = "L-ORDER.windows"
    temporal = Temporal(
        on="survey_cycle",
        splits=TemporalSplits(window=1, unit="unique", n_windows=4),
        horizon=2,
        horizon_unit="years",
        time_unit="years",
    )
    splits_comment = """
        Leaf L-ORDER.windows: a body-fat equation is fitted on the people examined so far and used on people met later
        (the relative fat mass was developed on NHANES 1999-2004 and validated on 2005-2006, Woolcott and Bergman 2018),
        and the survey cycle orders the people. Each test window is one two-year cycle; the windows are the four newest
        cycles, newest first: 2017-2018 (3,294 people), 2015-2016 (4,357), 2013-2014 (4,908) and 2011-2012 (4,381),
        training on every earlier cycle: 35,414, 31,057, 26,149 and 21,768 people (91.5%, 80.2%, 67.6% and 56.2%).
        Every window tests on the Discovery A scanner of 2011-2018. The first three train on both eras; the 2011-2012
        window trains on the old scanner's cycles alone and so tests across the change of scanner and of sampling (the
        largest feature drift of the candidate windows, by the window statistics), a change in data collection that a
        deployed equation meets; there the "Non-Hispanic Asian" level (13.9% of the test people) has no training row,
        since 1999-2006 do not code it. Four
        windows against the nine a random split of 38,708 people would get: only eight cycles exist, and a fifth
        window, 2005-2006, would train on 43.6% of the people, below the floor of half the data. No gap: the scan and the measures are taken at the same examination, so a person's label exists when
        they are examined. The 2011-2018 values as released are CDC's re-analysis with the Apex software (every
        2011-2018 DXX file: "First Published: March 2020"); the gap rests on the same-day scan, not on release dates.
        The test cycles hold ages 8-59 only (DXA eligibility from 2011); the 60-85-year-olds of 1999-2006 train only.
    """
    accepted_check_warnings = {
        "splits_below_target": (
            "Four of the nine windows an IID split of 38,708 people would get (SPLIT-33): the release holds eight "
            "cycles, and a fifth window, 2005-2006, would train on 43.6% of the people, below the half-the-data floor "
            "(splits comment)."
        ),
    }

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        frames = []
        for suffix in CYCLES:
            dxx = pd.read_sas(raw_dir / f"DXX{suffix}.xpt", format="xport")
            dxx = dxx[[c for c in DXX_COLUMNS if c in dxx.columns]]
            bmx = pd.read_sas(raw_dir / f"BMX{suffix}.xpt", format="xport")
            demo = pd.read_sas(raw_dir / f"DEMO{suffix}.xpt", format="xport")
            demo = demo[[c for c in DEMO_COLUMNS if c in demo.columns]]
            # The DXA file lists everyone eligible for the scan (five records each in 1999-2006); the source's key.
            frame = dxx.merge(bmx, on="SEQN", how="left").merge(demo, on="SEQN", how="left")
            frame["file_suffix"] = suffix
            frames.append(frame)
        return pd.concat(frames, ignore_index=True)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # 1. One record per person: the first of the five imputation records in 1999-2006, kept only when the percent
        #    fat is the same in all five (DXX_D: a fully measured person has "5 identical records"). 90 people whose
        #    flag reads measured carry a percent fat that varies across the records (80 in 2003-2004, 10 in 2005-2006
        #    with the bone flag set), so theirs is imputed.
        old_era = df["file_suffix"].isin(OLD_ERA)
        pct = df.loc[old_era].groupby("SEQN")["DXDTOPF"]
        varies = (pct.transform("max") != pct.transform("min")) | (pct.transform("count") != pct.transform("size"))
        varies = varies.reindex(df.index, fill_value=False)
        df = df.loc[~old_era | ((df["_MULT_"] == 1) & ~varies)]
        # 2. Measured scans with every region valid, one rule for both eras: the whole-body imputation flag 0 in
        #    1999-2006 (stored as SAS's smallest float, so rounded; CDC imputed every scan with an invalid region), a
        #    completed scan in 2011-2018 whose twelve region invalidity codes are all 0, as CDC's analysts select
        #    2011-2018 scans (Stierman et al. 2021); a percent fat in both. This drops 893 completed 2011-2018 scans
        #    whose whole-body value CDC publishes despite an invalid region (140, 148, 241 and 364 per cycle).
        old_era = df["file_suffix"].isin(OLD_ERA)
        flag = df["DXITOT"].fillna(df["DXITOTST"]).round()
        all_valid = df[REGION_VALIDITY].round().eq(0).all(axis=1)
        measured = (old_era & (flag == 0)) | (~old_era & (df["DXAEXSTS"] == 1) & all_valid)
        df = df.loc[measured & df["DXDTOPF"].notna()]
        # 3. The cycle's first year, from the file read; it agrees with DEMO's cycle code.
        df = df.assign(survey_cycle=df["file_suffix"].map(CYCLES).astype("int64"))
        assert (df["SDDSRVYR"].map(SDDSRVYR_YEAR) == df["survey_cycle"]).all()
        assert not df["SEQN"].duplicated().any()
        # 4. Names and the target.
        df = df.rename(
            columns={
                "DXDTOPF": "percent_body_fat",
                "RIAGENDR": "sex",
                "RIDAGEYR": "age_years",
                "RIDRETH1": "race_ethnicity",
                **COMMON_MEASURES,
            }
        )
        # 5. The codebook's words for sex and ethnicity (CLEAN-12); from 2011, RIDRETH3's non-Hispanic Asians get their
        #    own level (before 2011 they stay in "Other race", which RIDRETH1 alone cannot split).
        df = decode(df, CODE_LABELS)
        asian = df["RIDRETH3"].eq(RIDRETH3_ASIAN)
        df["race_ethnicity"] = df["race_ethnicity"].where(~asian, "Non-Hispanic Asian")
        # 6. The features measured in every cycle, the time key and the target (curation notes for the drops, the
        #    sagittal diameter of 2011-2016 among them). BMX and DEMO code no sentinels in these columns (missing is
        #    blank); the ranges are plausible (weight 16.9 to 188.5 kg, height 105.5 to 195.1 cm, waist 32 to 176 cm),
        #    and no row repeats.
        keep = ["survey_cycle", "sex", "age_years", "race_ethnicity", *COMMON_MEASURES.values(), "percent_body_fat"]
        return df[keep]

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["sex", "race_ethnicity"])
