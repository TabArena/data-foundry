"""Curated dataset definition for `gusto_i_mi_mortality` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Grouping,
    Metric,
    Source,
    SplitPlan,
    TaskSummary,
    TimeBasis,
    decode,
    drop_columns,
)
from data_foundry.v2.splits import SPLIT_RANDOM_STATE, grouped_splits

# The file's 1/2 history codes: 2 is "yes". The file labels `htn` "History of Hypertension" and `fam` "Family History
# of MI"; `pan` carries no label. Region 1 of the file is the 2,188-patient "West region" subsample of the GUSTO-I
# case studies, and its shares of code 2 equal the published shares of "yes" (hypertension history 40.4%, previous
# angina pectoris 34.0% against 34.1%, family history of MI 47.6%; Iba et al. 2021, Table 1). `prevcvd` and `prevcabg`
# follow the same coding (2 is the rarer level, 2.0% and 4.4%, with the higher death rate).
YES_NO = {1: "no", 2: "yes"}
# Whole regions in 8 folds, one repeat: every region is tested once, two regions per test fold (Andrej, 2026-11-25).
N_REGION_FOLDS = 8
FLAG = {0: "no", 1: "yes"}
# The five flags of the source's simplified models stay as released (CLEAN-22): `sho` shock (Killip III or IV), `hig`
# high risk (anterior infarct or previous MI), `ant` anterior infarct, `hyp` hypotension (systolic pressure below
# 100, 5 exceptions at 100) and `hrt` tachycardia (pulse above 80, 8 exceptions at 80).
CODE_LABELS = {
    "htn": YES_NO,
    "pan": YES_NO,
    "fam": YES_NO,
    "prevcvd": YES_NO,
    "prevcabg": YES_NO,
    "dia": FLAG,
    "sho": FLAG,
    "hig": FLAG,
    "ant": FLAG,
    "hyp": FLAG,
    "hrt": FLAG,
}


def filled_height(height: pd.Series) -> pd.Series:
    """Heights that are neither whole or half centimetres nor a converted inch value: the imputation's fills.

    The spike at 177.3 cm (957 rows, a common value of the inch grid) counts as measured.
    """
    inches = np.arange(48, 90, 0.25) * 2.54
    grid = set(np.round(inches, 1)) | set(np.floor(inches * 10 + 1e-9) / 10) | set(np.ceil(inches * 10 - 1e-9) / 10)
    h = height.round(1)
    measured = (h % 1 == 0) | np.isclose(h % 1, 0.5) | h.isin(grid) | (h == 177.3)
    return ~measured


# Killip class, the clinical grade of heart failure at presentation (I none, II rales or S3, III pulmonary oedema,
# IV cardiogenic shock).
ORDINAL_LEVELS = {"Killip": ["I", "II", "III", "IV"]}


def height_fill_table(raw: pd.DataFrame) -> pd.DataFrame:
    """Patients and 30-day deaths (%) by the look of the recorded height, on the rows that stay."""
    raw = raw[~raw.duplicated()]
    look = filled_height(raw["height"]).map({True: "filled (fraction off the grid)", False: "measured"})
    return raw.groupby(look)["day30"].agg(patients="size", died_pct=lambda d: round(d.mean() * 100, 1))


class GustoIMiMortality(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a patient presenting with an acute myocardial infarction be dead 30 days later?",
        use_case=(
            "At initial presentation with an evolving heart attack with ST elevation, within 6 hours of the onset "
            "and eligible for thrombolysis, the cardiologist estimates the patient's risk of death, which guides the "
            "choice of reperfusion therapy and of care resources (Lee et al. 1995: "
            '"Appropriate choices among alternative therapies and the use of clinical resources depend on an '
            "estimate of the patient's risk\")."
        ),
        row=(
            "One of 40,826 patients of the GUSTO-I trial (1990-1993, 1,081 hospitals in 15 countries), randomised to "
            "one of the trial's thrombolytic regimens."
        ),
        predicted="Whether the patient died within 30 days of enrolment; 7.0% did.",
        known=(
            "Age, sex, weight, the heart rate, systolic blood pressure and Killip class at presentation, the "
            "infarct's location and the number of ECG leads with ST elevation, history (earlier heart attack, "
            "angina, hypertension, diabetes, stroke, bypass surgery, smoking, family history), the source's five "
            "flags that summarise some of these (shock, hypotension, tachycardia, anterior infarct, high risk) and "
            "the assigned thrombolytic regimen."
        ),
        split=(
            "Whole regions are held out (16 regions, 8 in the US and 8 elsewhere), two per test fold, so the test "
            "data stands for the patients of a region the model has never seen; every region is tested once."
        ),
        changes=(
            "We drop the time to relief of chest pain, which the randomised treatment changes and so is measured "
            "after presentation, and the height, whose filled-in values mark patients who died. A few impossible "
            "pulse and blood pressure values become missing."
        ),
        fit="direct",
        fit_reason=(
            "Every input is recorded at presentation, before the thrombolytic acts; the outcome is fixed at day 30. "
            "The trial took the patients the decision is made for (ST elevation, within 6 hours, eligible for "
            "thrombolysis). The file lacks the source model's time to treatment. The care is that of the "
            "thrombolysis era: primary angioplasty has since become the first choice where available."
        ),
    )

    # Dataset
    unique_name = "gusto_i_mi_mortality"
    domain = "medical & healthcare"
    sources = (
        Source(
            role="publication",
            platform="Other",
            url="https://doi.org/10.1161/01.cir.91.6.1659",
            # the data's terms, stated by the repository that releases the patient file (the copy below)
            license='Free use with attribution: hbiostat.org/data states "Permission is granted to anyone wishing to use '
            'the data sets provided here. Please reference the original paper"',
            year="1995",
            bibtex="""
                @article{lee1995predictors,
                  title={Predictors of 30-day mortality in the era of reperfusion for acute myocardial infarction. Results from an international trial of 41,021 patients},
                  author={Lee, Kerry L and Woodlief, Lynn H and Topol, Eric J and Weaver, W Douglas and Betriu, Amadeo and Col, Jacques and Simoons, Maarten and Aylward, Phil and Van de Werf, Frans and Califf, Robert M},
                  journal={Circulation},
                  volume={91},
                  number={6},
                  pages={1659--1668},
                  year={1995},
                  doi={10.1161/01.cir.91.6.1659}
                }
                @article{gusto1993international,
                  title={An international randomized trial comparing four thrombolytic strategies for acute myocardial infarction},
                  author={{The GUSTO Investigators}},
                  journal={New England Journal of Medicine},
                  volume={329},
                  number={10},
                  pages={673--682},
                  year={1993},
                  doi={10.1056/NEJM199309023291001}
                }
            """,
        ),
        Source(
            role="copy",
            platform="Other",
            url="https://hbiostat.org/data/repo/gusto.rda",
            name="the patient file on the Vanderbilt Department of Biostatistics data repository",
            license='Free use with attribution: hbiostat.org/data states "Permission is granted to anyone wishing to use '
            'the data sets provided here. Please reference the original paper"',
            files=["gusto.csv"],
        ),
    )
    split_leaf = "L-PLACE.groups"
    time_basis = TimeBasis(
        "UnseenGroup",
        """
        a risk model at presentation is used at hospitals and in regions other than the ones it was built in, and the
        case study on this file validates the model built on the US patients on the patients of the other countries
        (Steyerberg and Vergouwe 2014), so whole regions are held out (16 regions). The patients were enrolled one by
        one in 1990-1993, but the file records no date and no enrolment order (its rows are sorted by age), so a
        later period at a known region is not tested, nor are later patients at all: the care of the thrombolysis
        era has changed since.
        """,
    )
    download_description = """
        The patient file gusto.rda from the Vanderbilt Department of Biostatistics data repository (served at the URL
        below, not listed in the repository's index; 595,125 bytes; the R package predtools ships the same 40,830 x 29
        table). We export it to CSV with pyreadr.

        mkdir -p local-data-warehouse/gusto_i_mi_mortality && cd local-data-warehouse/gusto_i_mi_mortality
        wget https://hbiostat.org/data/repo/gusto.rda
        sha256sum gusto.rda
        # e12bc58730894fa26f31b5b4ea963a878e855d7f2d53e47991cf8bb80b84d8e1
        uvx --from pyreadr==0.5.9 --with pandas==3.1.1 python -c "import pyreadr; pyreadr.read_r('gusto.rda')['gusto'].to_csv('gusto.csv', index=False)"
        sha256sum gusto.csv
        # 5a96c74ab43305fcaabd94a645e02c8b901c40321112e196295a64867a9b4b20
    """
    curation_comments = """
        We start with gusto.rda, the GUSTO-I patient file of the Vanderbilt Department of Biostatistics repository: 40,830 patients x 29 columns, one row per patient, 2,851 deaths by day 30 (7.0%). It is the one file of the release; the R package predtools ships the same table, and the case-study subsamples of Steyerberg's Clinical Prediction Models (the 2,188-patient West region set among them) are cuts of it.

        - Prediction point: initial presentation, before the thrombolytic acts (Lee et al. 1995: "clinical descriptors routinely collected at initial presentation"). Every kept input is recorded then; the target is death within 30 days of enrolment.
        - The file's own labels: the R file carries a `label` attribute on 15 columns (pyreadr drops it; read from the serialised file). Among them `dia` "Diabetes", `htn` "History of Hypertension", `fam` "Family History of MI", `pmi` "Previous MI", `miloc` "MI Location", `tx` "Tx in 3 groups", `sysbp` "Systolic Blood Pressure" (mmHg) and `ttr` "Time to Relief of Chest Pain > 1h". `ste` is the number of ECG leads with ST elevation; `pan` (no label) is previous angina pectoris, as the published West-region table confirms (module comment).
        - `ttr` (time to relief of chest pain over one hour, yes for 64.9%) is dropped: it is measured after presentation. Randomisation balances the baseline columns across the three arms (chi-square p 0.09 to 0.97; the count of ST leads by a rank test, 0.50), but not `ttr`: 66.3% under streptokinase, 64.6% under the combination and 62.3% under accelerated tPA (p = 3e-11), the order of the regimens' speed of reperfusion, so the treatment given at enrolment changes it. The 8-predictor model of the case-study literature includes it; at the prediction point it is not known (USE-3, LEAK-1). Kept, it would add 0.003 ROC AUC (logistic regression and LightGBM, 5-fold x 3 by region).
        - Five flags of the source's simplified models stay as released: `sho` (shock) is Killip class III or IV, `hig` (high risk) is an anterior infarct or a previous MI, `ant` is `miloc` Anterior, all exactly; `hyp` (hypotension) is systolic pressure below 100 and `hrt` (tachycardia) a pulse above 80, except 5 and 8 patients exactly at 100 and 80. None is an exact copy of another column, so none leaves for what it is (CLEAN-5, CLEAN-22), as `ARPU_SEGMENT` in expresso_churn_prediction and `dzclass` in 2_month_survival_rate_prediction stayed. They raise a logistic regression's ROC AUC by 0.003 (15 of 15 folds by region) and LightGBM's not at all (-0.001): they hand a linear model the source's cut points.
        - `tpa` is dropped: it is the treatment arm again (1 for tPA, 0 for streptokinase, blank for the combination arm), which `tx` holds. `tx` stays as an input: the arm was randomised and known at enrolment, Lee et al. include the thrombolytic among the predictors, and a model with it gives the risk under each regimen. `tx` merges the two streptokinase arms (subcutaneous or intravenous heparin) as published. Without it ROC AUC drops by 0.000 to 0.002.
        - Place codes: `regl` holds 16 regions (1,231 to 4,352 patients, 95 to 294 deaths each). Regions 1, 7, 9, 10, 11, 12, 14 and 15 hold 23,034 patients and 1,565 deaths, exactly the US cohort of Steyerberg and Vergouwe (2014); the other eight hold the 17,796 non-US patients and 1,286 deaths. Region 1 is the "West region" subsample. `grpl` (48 groups) and `grps` (121 groups) are nested in the regions but not in each other, and every `grps` group holds at least 20 deaths, every `grpl` group at least 47: groups of hospitals cut to a minimum number of events for validation studies, not places a model meets. The region is the group column (renamed `region`, never a feature); `grpl` and `grps` are dropped. Held-out regions score as random folds do (LightGBM ROC AUC 0.821 on the 8 region folds, 0.819 on random folds; group probe), and so do the finer groupings (0.823 to 0.825); training on the US and testing outside it, and the reverse, gives 0.815 (LightGBM) and 0.820 (logistic regression), inside the range of the region folds.
        - The 191 patients of the 41,021 enrolled who are not in the file are not explained by the release (Steyerberg and Vergouwe's case study uses the same 40,830). The death rates by arm in the file (7.3% for the merged streptokinase arms, 6.3% tPA, 7.0% combination) are the trial's (7.2% and 7.4%, 6.3%, 7.0%). Were all 191 dead, the death rate would be 7.4% instead of 7.0%.
        - Imputed values: Steyerberg and Vergouwe say the missing predictor values of this cohort "were filled in with a single imputation procedure considering correlations between predictor variables", so the file holds no blank and cannot show which values were filled. One pattern looks like such fills: 28 patients share every categorical and whole-number value (male, Killip I, inferior infarct, 2 ST leads, pulse 53 or 54, systolic pressure 97 or 104, never smoked, family history and no other history, time to relief over an hour) and differ only in age (31.1 to 40.7), height and weight, which move together; they come from 7 regions and all three arms, and 7 of them died (25%, against 7.0% overall). Kept as published: 0.07% of the rows, and the file cannot show which values were filled.
        - Duplicates: 4 rows repeat another row exactly, the arm and the site group included (3 sets of 2 or 3, all survivors, all in that pattern and in region 4); one row of each set stays (LEAK-19), leaving 40,826 patients and 2,851 deaths. Whether they are one patient entered twice or patients filled alike cannot be told. After the drops, 8 more rows of the pattern repeat another row (they differed only in the dropped site groups), and 2 rows share all inputs with a row of the other outcome; kept, as above.
        - Class-dependent recording (record marker `Class-dependent Recording`): the heights the source's single imputation filled in mark patients who died. 2,132 heights (5.2% of the rows) are neither whole or half centimetres nor a converted inch value (171.8, 171.3, 170.3, ...), spread less than measured heights, and 19.9% of these patients died against about 6% of the others. The gap holds in 15 of 16 regions and given everything known at presentation (age, sex, Killip class, blood pressure, pulse, infarct location, ST leads, previous MI, region: odds ratio 2.65, p = 2e-54), so the fill follows the outcome (an early death left the height unmeasured, or the outcome entered the imputation), which a model at the door cannot know (LEAK-10 through LEAK-38's conditional test). A model that spots the fills gains 0.0045 ROC AUC (LightGBM, 9 of 9 folds of the earlier 3 x 3 region folds) and a fill flag 0.007 for a regression. Milder fixes fail: the fills set to missing keep the signal (LEAK-40), and heights rounded to whole centimetres still let a model find the filled rows at ROC AUC 0.82 (LEAK-13). So `height` is dropped: it costs a logistic regression nothing (+0.0001) and tuned LightGBM 0.001 to 0.002, the leak itself; without it the filled-height rows cannot be found from the other columns (ROC AUC 0.535). The 1,026 weights of the same look carry no outcome signal (adjusted odds ratio 1.01, p = 0.91; a weight-fill flag adds 0.0000), so `weight` stays. The categorical columns may hold fills the file cannot show; the 28-row pattern above is the visible trace.
        - Impossible values set to missing (CLEAN-11, 7 cells): a pulse of 1 to 9 (4 patients, 3 of them Killip I, one with systolic pressure 180), and a pulse or systolic pressure of 0 in a Killip I patient, who is not in shock (3 patients). The other zeros stay as recorded: systolic pressure 0 in 5 patients of Killip III or IV and pulse 0 in 2 of them, all dead, an unmeasurable pressure in shock. Ages over 100 in 3 patients (108, 108, 110, whole numbers while 98.8% of ages carry a fraction) and under 25 in 26 are kept as recorded.
        - Outdated (record marker `Outdated`, SEL-18): the care is that of the thrombolysis era; primary angioplasty, stents and newer antiplatelet drugs have lowered the death rate since, while thrombolysis remains the therapy where angioplasty cannot be done in time. The task is still made today, so the fit stays direct (USE-8) and the era is a note.
        - Note: the builder's untuned task probes flagged `no_spread` (logistic regression, random forest and LightGBM ROC AUC 0.819, 0.817 and 0.820 by region, with `height` in and the five flags out); on the shipped inputs and the 8 region folds they score 0.829, 0.823 and 0.823 with no flag, and age alone 0.733 (2026-11-25). A few smooth predictors carry most of the signal (Lee et al.: five carry 90% of the prognostic information). Tuned methods separate: on the shipped inputs and the 8 region folds (2026-11-25), a logistic regression with splines reaches 0.8264 and a lightly tuned LightGBM 0.8272 against 0.8234 for a plain logistic regression (splines +0.0030, standard error 0.0008, better on 7 of 8 folds; LightGBM +0.0038, standard error 0.0014, 7 of 8; log loss 0.1997 and 0.1996 against 0.2008). Not `Trivial`: the TIMI risk score for STEMI (Morrow et al. 2000), a published score not fitted on these data, reaches 0.794 on the whole file.
        - Codes get their words: the 1/2 history codes become no/yes, `dia` and the five flags 0/1 no/yes (CLEAN-12); Killip class is an ordered category (CLEAN-14); the target `day30` becomes `death_by_day_30` (Yes/No, CLEAN-25).
    """

    # Task
    target = "death_by_day_30"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason='Lee et al. 1995 report chi-square statistics per predictor and that the model "accurately estimated '
        'the likelihood of death" (abstract; the full text could not be reached); the GUSTO-I case study on this file '
        "(Steyerberg and Vergouwe 2014, Eur Heart J, https://pmc.ncbi.nlm.nih.gov/articles/PMC4155437/) scores its "
        "models by the c statistic together with calibration in the large and the calibration slope, so no single "
        "deliberate metric (MET-5). roc_auc is the binary fallback and the c statistic the case study reports "
        "(0.813 internal, 0.812 US to non-US); log loss would also score the calibration the case study weighs."
    )
    grouping = Grouping(
        on="region",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is one of the file's 16 regions (8 in the US, 8 in the other countries; 1,231 to 4,352 patients each). A risk model at presentation is used at hospitals other than those it was built at, and the case study on this file builds its model on the US patients and validates it on the patients outside the US: "We validate these models in patients enrolled outside of the USA (n = 17 796, 1286 deaths)" (Steyerberg and Vergouwe 2014). Holding out whole regions generalises that design. Each patient is one prediction, made from their own data alone. Every region is tested once, in 8 folds of 2 regions.
        """,
    )
    splits_comment = """
        Whole regions in 8 folds, one repeat (leaf L-PLACE.groups; Andrej, 2026-11-25): each of the 16 regions is held out once, two regions per test fold, US and non-US mixed, assigned by the framework's grouped k-fold stratified by the outcome with shuffled regions and its fixed seed; each split trains on the other 14 regions. The test folds hold 4,161 to 7,789 patients and 256 to 554 deaths. One repeat of 8 folds was chosen over the protocol's 3 repeats of 3 folds, as for economic_well_being_prediction_challenge: folds of 5 or 6 regions train on 10 or 11 regions, and the repeats share most of their training regions. Measured (2026-11-25, `height` dropped, 6 draws of each design, mean ROC AUC over the folds; reference: each region held out alone): the reference gives logistic regression 0.8189, logistic regression with splines 0.8248 and lightly tuned LightGBM 0.8256, a gap of 0.0067 between LightGBM and logistic regression; 1 x 8 keeps that gap (0.0067, SD of the design's mean over draws 0.0010), 3 x 3 shrinks it to 0.0056 (SD 0.0003) and swaps the two best models by 0.0002. The file records no hospital; its finer codes (`grpl`, `grps`) are groups of hospitals cut to a minimum number of deaths for validation studies and are not used. The case study's own split (US against non-US) is two groups, too few for repeated folds; its transfer scores 0.815 to 0.820 ROC AUC (LightGBM and logistic regression, both directions), inside the range of the region folds, so the mixed folds lose nothing the source tested.
    """
    accepted_check_warnings = {
        "groups_test_groups_few": "Accepted (Andrej, 2026-11-25): a test region stands for the patients "
        "of a region the model has never seen, so two whole regions per test fold is the task (8 folds, each of the 16 "
        "regions tested once; 4,161 to 7,789 patients and 256 to 554 deaths per test fold). The signal across regions "
        "is real: the group probe scores ROC AUC 0.824 (logistic regression), 0.814 (random forest) and 0.821 "
        "(LightGBM) on the held-out regions, and LightGBM 0.821 grouped against 0.819 on random folds (2026-11-25).",
        "splits_dimensions_off_protocol": "Accepted (Andrej, 2026-11-25): 1 x 8 region folds instead of the "
        "protocol's 3 x 3. Over 6 draws each (`height` dropped, mean ROC AUC over the folds), 1 x 8 keeps the gap of "
        "lightly tuned LightGBM over logistic regression that holding out each region alone shows (0.0067 against "
        "0.0067), while 3 x 3, which trains on 10 or 11 of the 16 regions, shrinks it to 0.0056; the splits comment "
        "says why.",
    }

    def _make_splits(self, df: pd.DataFrame) -> SplitPlan:
        # One repeat of grouped k-fold over the regions, stratified by the outcome as the default protocol is
        splits = grouped_splits(
            df.reset_index(drop=True),
            n_repeats=1,
            group_on="region",
            group_labels="per_sample",
            n_folds=N_REGION_FOLDS,
            stratify_on=self.target,
            random_state=SPLIT_RANDOM_STATE,
        )
        tested = [df["region"].iloc[test].unique() for _train, test in splits[0].values()]
        assert [len(regions) for regions in tested] == [2] * N_REGION_FOLDS, tested
        assert sum(len(regions) for regions in tested) == df["region"].nunique() == 16
        return SplitPlan(splits=splits)

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "gusto.csv")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # Exact copies of a whole raw row (same age to the day, arm and site group): one row of each set stays (LEAK-19)
        copies = raw.duplicated()
        assert copies.sum() == 4
        df = drop_columns(
            raw[~copies].reset_index(drop=True),
            [
                "ttr",  # time to relief of chest pain: changed by the randomised treatment, so after presentation
                "tpa",  # the treatment arm again (blank for the combination arm); `tx` holds it
                "height",  # its filled-in values mark patients who died (LEAK-10 through LEAK-38)
                # groups of hospitals cut to a minimum number of deaths, not places
                "grpl",
                "grps",
            ],
        )
        df = df.rename(columns={"regl": "region"})
        # impossible values become missing (CLEAN-11): a pulse below 10, and a zero pulse or pressure in a patient
        # of Killip class I, who is not in shock
        killip_i = df["Killip"].eq("I")
        df["pulse"] = df["pulse"].astype(float).mask(df["pulse"].between(1, 9) | (df["pulse"].eq(0) & killip_i))
        df["sysbp"] = df["sysbp"].astype(float).mask(df["sysbp"].eq(0) & killip_i)
        assert df["pulse"].isna().sum() == 6
        assert df["sysbp"].isna().sum() == 1
        # the codebook's words for the history codes (CLEAN-12)
        df = decode(df, CODE_LABELS)
        # the target's classes in words (CLEAN-25): "Yes" is the event the task predicts
        df = decode(df, {"day30": {0: "No", 1: "Yes"}}).rename(columns={"day30": self.target})
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            ordinal=ORDINAL_LEVELS,
            categorical=[
                "region",
                "sex",
                "miloc",
                "pmi",
                "smk",
                "tx",
                "htn",
                "pan",
                "fam",
                "prevcvd",
                "prevcabg",
                "dia",
                "sho",
                "hig",
                "ant",
                "hyp",
                "hrt",
            ],
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        flags = {
            "ttr (time to relief of chest pain > 1 h)": raw["ttr"].eq(1),
            "dia (diabetes)": raw["dia"].eq(1),
            "sho (Killip III or IV)": raw["sho"].eq(1),
            "hig (anterior infarct or previous MI)": raw["hig"].eq(1),
            "htn (history of hypertension)": raw["htn"].eq(2),
            "pan (previous angina)": raw["pan"].eq(2),
            "pmi (previous MI)": raw["pmi"].eq("yes"),
        }
        by_arm = pd.DataFrame({name: flag.groupby(raw["tx"]).mean() * 100 for name, flag in flags.items()}).T
        return [
            Decision(
                title="Time to relief of chest pain dropped: the randomised treatment changes it",
                why=(
                    "Randomisation balances what is known at enrolment across the arms; `ttr` alone differs, lowest "
                    "under accelerated tPA, the regimen that reperfuses fastest (chi-square p = 3e-11 against 0.09 to "
                    "0.97 for the other inputs). So it is recorded after the thrombolytic was given, not at "
                    "presentation. Share of patients with the flag, % by arm:"
                ),
                evidence=by_arm.round(1),
            ),
            Decision(
                title="Height dropped: its filled-in values mark patients who died",
                why=(
                    "The source filled missing predictor values by a single imputation. Heights that are neither whole "
                    "or half centimetres nor a converted inch value are the fills; their patients died far more often, "
                    "in nearly every region and given everything known at presentation (odds ratio 2.65), and setting "
                    "them to missing or rounding them keeps the signal. Weights of the same look do not differ. "
                    "Patients (the 40,826 that stay) and the share who died by day 30, %:"
                ),
                evidence=height_fill_table(raw),
            ),
        ]
