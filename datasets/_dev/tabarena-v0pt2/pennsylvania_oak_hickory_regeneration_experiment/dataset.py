"""Curated dataset definition for `pennsylvania_oak_hickory_regeneration_experiment` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, Grouping, Metric, TaskSummary, drop_columns

# The columns of `DataCJFR.csv` we keep, as published, and their names here. The file's names differ from the ones
# its README lists (`SEED21_COUNT_OVER_6IN` is the README's `COUNT21`); the 2014 values are the pre-treatment inventory.
RENAME = {
    "STUDY_AREA": "state_forest",
    "FENCE": "fence",
    "LIME": "lime",
    "HERB": "herbicide",
    "SEED14_COUNT_OVER_6IN": "seedlings_over_6in_2014",
    "SEED14_AGG_HT_OVER_6IN": "aggregate_height_over_6in_2014_m",
    "SEED14_COUNT_W_UNDER_6IN": "seedlings_all_heights_2014",
    "SEED14_AGG_HT_W_UNDER_6IN": "aggregate_height_all_heights_2014_m",
    "PH14": "soil_ph_2014",
    "AL": "soil_al_2014",
    "MN": "soil_mn_2014",
    "KALA_VOL_M3_14": "mountain_laurel_volume_index_2014",
}
# Measured after the 2014 inventory (LEAK-10): the 2021 values and the 2014-2021 changes (the target, its other
# measures and its differences), the 2016 soil pH (after lime), the 2016 canopy photo (after herbicide), basal area
# averaged over 2014-2021 and mountain laurel volume averaged over the post-treatment surveys.
AFTER_PREDICTION_POINT = [
    "SEED21_AGG_HT_W_UNDER_6IN",
    "DELTA_AGG_HT_UNDER_6IN",
    "SEED21_COUNT_W_UNDER_6IN",
    "DELTA_COUNT_UNDER_6IN",
    "SEED21_AGG_HT_OVER_6IN",
    "DELTA_AGG_HT_OVER_6IN",
    "DELTA_COUNT_OVER_6IN",
    "PH16",
    "LOGIT_CANOPY_OPEN16",
    "AVG_BA_m2_ha",
    "AVG_POST_TRT_KALA_VOL_M3_1621",
]
TARGET_COUNT = "SEED21_COUNT_OVER_6IN"


class PennsylvaniaOakHickoryRegenerationExperiment(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "How many tree seedlings of any species taller than 15 cm will a small plot in an oak-hickory stand of "
            "two central Pennsylvania state forests hold seven years after its pre-treatment inventory, given that "
            "inventory and the treatment planned for it (deer fence, lime, herbicide, a combination or none)?"
        ),
        use_case=(
            "For example, a state forester planning regeneration treatments forecasts how many seedlings a plot will "
            "hold seven years after a planned deer fence, lime or herbicide, from the pre-treatment inventory of "
            "seedlings, mountain laurel and soil; the data shows the treatment's effect only weakly. The funders (the "
            "Pennsylvania Game Commission and DCNR's Bureau of Forestry) state a management aim; no prediction user "
            "is named."
        ),
        row=(
            "One microplot 3.3 m across at one of 24 randomly chosen sites in the Rothrock and Bald Eagle state "
            "forests (261 microplots, 9 to 11 per site), with the treatment combination it received in 2014-2015."
        ),
        predicted=(
            "The number of tree seedlings over 15 cm (6 in) tall on the microplot in 2021, seven years after the "
            "inventory, of any tree species, red maple and black birch included (the deposit has no species split); "
            "shipped as log(1 + count) and scored on the count; 18% of the microplots have none."
        ),
        known=(
            "The state forest, the treatment combination, the 2014 seedling counts and aggregate heights (over 15 cm "
            "and at all heights), a 2014 mountain laurel cover-height index and, for most microplots, the 2014 soil "
            "pH, aluminium and manganese."
        ),
        split=(
            "Whole sites are held out, so a test microplot stands for a new site in the Rothrock or Bald Eagle state "
            "forest where no plot was followed, over the same 2014-2021 years; every treatment combination is in "
            "training at other sites."
        ),
        changes=(
            "We predict the 2021 count rather than the paper's 2014-2021 change, drop the values measured after the "
            "treatments (2016 soil pH and canopy, basal area and laurel volume averaged over later years), and split "
            "by site."
        ),
        fit="approximate",
        fit_reason=(
            "A forester acts on oak and hickory, but all tree species are counted; one microplot per treatment per "
            "site weakly identifies the treatment's effect, applied per plot, not per stand; no overstory, deer "
            "impact or fern cover; two forests and one 2014-2021 cohort, so training and test share the years' "
            "weather, deer and seed crops, which a later cohort's forecast would not."
        ),
    )

    # Dataset
    unique_name = "pennsylvania_oak_hickory_regeneration_experiment"
    year = "2024"
    domain = "biology & life sciences"
    source = "Other"  # the Dryad deposit of Begley-Miller et al. (2024), published 2024-09-25
    source_url = "https://doi.org/10.5061/dryad.z8w9ghxnk"
    license = "CC0 1.0"  # stated on the Dryad deposit
    data_tags = ("ForcedGroupedFromTemporal",)
    download_description = """
        The data is the Dryad deposit doi:10.5061/dryad.z8w9ghxnk (version of 2024-09-25, CC0). Dryad's per-file API answers 401 without a token and its web download answers 403 to scripts, but the version download of its API redirects without a token to a zip of both files; their SHA-256 digests equal those Dryad lists (checked 2026-11-01).
        mkdir -p local-data-warehouse/pennsylvania_oak_hickory_regeneration_experiment && cd local-data-warehouse/pennsylvania_oak_hickory_regeneration_experiment
        curl -L -o dryad_z8w9ghxnk_v20240925.zip https://datadryad.org/api/v2/versions/318677/download
        unzip dryad_z8w9ghxnk_v20240925.zip  # DataCJFR.csv and README.md
        sha256sum DataCJFR.csv  # c183bbab24a4564e71129772d38092a724fb58acc3352e3d0485b25d9de2c11b
    """
    bibtex = r"""
        @article{begleymiller2024complex,
          title = {Complex interactions of deer herbivory, soil chemistry, and competing vegetation explain oak--hickory forest tree regeneration in central {Pennsylvania}, {USA}},
          author = {Begley-Miller, Danielle and Diefenbach, Duane R. and Domoto, Emily J. and Drohan, Patrick J. and Jones, Phillip and McDill, Marc E. and Rosenberry, Christopher S. and Sabo, Autumn E. and Wallingford, Bret D.},
          journal = {Canadian Journal of Forest Research},
          volume = {54},
          number = {11},
          pages = {1367--1375},
          year = {2024},
          doi = {10.1139/cjfr-2024-0034},
          note = {Data: \url{https://doi.org/10.5061/dryad.z8w9ghxnk}, CC0}
        }
    """
    curation_comments = """
        We start with `DataCJFR.csv` from the Dryad deposit of Begley-Miller et al. (2024), version of 2024-09-25 (261 microplots, 28 columns), fetched through Dryad's API; its SHA-256 equals Dryad's digest.
        - Prediction point: the full vegetation inventory of a site in 2014, before the treatments. Fences and lime went in "in the summer of 2014 (27 May-14 Aug) immediately following a full vegetation inventory", the herbicide "following the 2015 summer vegetation monitoring season" (17-28 Aug 2015; Sec. 2.2 as reproduced in the Dryad methods). The treatment combination is the decision, so it is an input; the target is the 2021 survey, seven years on. The paper's text beyond the methods on Dryad was not read (the publisher answers automated requests with a bot check).
        - Anomaly: the deposit's README describes its file only in part (PROV-2; a measurement on the file outranks the codebook, EV-2). The file has 28 columns under other names, against the 21 the README announces (22 described). Seven file columns have no README entry: `PH16`, `AL` and five all-height columns (the 2014 and 2021 counts and aggregate heights with the under-6-in class, and the change in that count); `PRE_TRT_ALL_COMP_VOL` is described and not in the file. Names were matched by content: each 2014-2021 change equals the 2021 value minus the 2014 value in every row (aggregate heights to the 0.1 m rounding), and the two all-height 2014 inputs are read by an identity: each stem beyond the over-6-in count adds 0.0762 m of aggregate height, the midpoint of the 0-6 in class, in every row (to the rounding). The file holds 261 microplots and 2 empty rows, which we drop; the README's "262 rows (first-row headers)" counts the header, so it agrees with the methods' "n = 261". Three control microplots are missing (site 137 number 3, site 149 numbers 2 and 3).
        - Target: `log1p_seedlings_over_6in_2021` is log(1 + `SEED21_COUNT_OVER_6IN`), the README's `COUNT21`: the tree seedlings (woody stems at most 2.54 cm at breast height) taller than 6 in (0.15 m) on the 3.30 m microplot in 2021. The crews counted "any live, arborescent, woody species" (Sec. 2.3), so red maple and black birch, common at these sites (Sec. 2.1), count the same as oak and hickory; the deposit has no species split (USE-5, USE-8; named in `fit_reason`). Not the paper's response, "the change between 2014 and 2021" (Sec. 2.4): the forester acts on the regeneration that will be there (USE-5), and with the 2014 count as an input the level and the change carry the same information (on the count, an error on one is the same error on the other). The count rather than the aggregate height (`SEED21_AGG_HT_OVER_6IN`, zero in the same 48 microplots): the abundance a regeneration tally counts, where the aggregate height is an index built from class midpoints. Logged as a skewed count (skew 2.93, 0.43 after log1p; median 4, maximum 154; CLEAN-16); the metric inverts it and scores the count (MET-3).
        - Note: 48 of 261 microplots (18.4%) have no seedling over 6 in in 2021, an observed absence. The zero is the most frequent value only just (38 microplots hold one seedling), and it follows the inventory: 39% of the microplots with none over 6 in in 2014 have none in 2021, against 12% of the others. So the zeros look like the low end of the count more than a regime of their own.
        - Dropped as measured after the prediction point (LEAK-10): every 2021 value and 2014-2021 change (`SEED21_*`, `DELTA_*`); `PH16`, the 2016 soil pH after lime (mean 4.27 on limed against 3.12 on unlimed treated microplots); `LOGIT_CANOPY_OPEN16`, canopy openness photographed in 2016, after the herbicide; `AVG_BA_m2_ha`, basal area averaged over the 2014-2021 surveys, so it carries overstory change up to the outcome year; `AVG_POST_TRT_KALA_VOL_M3_1621`, mountain laurel volume averaged over the surveys after the herbicide. The README's `BA` and `CANOPY` have no 2014 counterpart in the file, so no lag is possible.
        - Kept the 2014 soil values (`soil_ph_2014`, `soil_al_2014`, `soil_mn_2014`): they do not differ between limed and unlimed microplots (Mann-Whitney p = 0.51, 0.92, 0.24; see Decisions), and with site fixed effects and all three flags lime moves the 2014 pH by +0.05 (95% CI -0.02 to +0.12) against +1.18 for the 2016 pH (review panel, 2026-11-01). Sec. 2.4 adds that "soil pH varied among microplots both before and after treatment". So the 2014 samples were taken before the lime. They are missing in 72 microplots: all 69 controls at positions 2 to 4, sampled only "when time allowed" (Sec. 2.3), so in this file time never allowed, and 3 at site 140; kept missing (not caused by the outcome).
        - Anomaly: `AL` is not described; we read it as 2014 extractable aluminium because it is missing in exactly the microplots where `PH14` and `MN` are and does not differ between limed and unlimed plots. Its unit is not stated. `MN` is stated in cmol(+)/kg, which is implausible: the maximum, 206, would be 5.7% of the soil's mass; mg/kg fits the values (1.7 to 206), not checked with the lab (PROV-2). Both shipped as published.
        - Note: `mountain_laurel_volume_index_2014` (`KALA_VOL_M3_14`, the README's `PRE_TRT_KALA_VOL`) is the midpoint of the percent-cover class times the top of the height class in m. The README reports it in m3, but 78 of 261 values exceed the 15.4 m3 an 8.55 m2 microplot holds up to 1.8 m, so it is an index, and its name says so (PROV-2).
        - Dropped as identifiers or copies: `UID` (equal to `PLOT` x 100 + `SUBPLOT` in every row); `SUBPLOT`, the microplot's number (1 to 4 controls, 5 always the fence, 6 to 11 the other six combinations at random), which a new stand does not have and whose treatment content the three flags carry (CLEAN-3); `TRT`, the treatment code, one to one with the three flags in every row (CLEAN-5). `PLOT` is the site and becomes the group column `site` (its first digit is the forest).
        - The flags `fence`, `lime` and `herbicide` are Yes/No categories (CLEAN-14); `state_forest` stays (Rothrock 7.9-9.2 deer/km2, Bald Eagle 2.8-3.3 in 2018-2019, Sec. 2.1), known for any stand.
        - Note: the fence alone is always microplot 5 (Sec. 2.2), so fence against control is not randomised over positions; the other six combinations are randomised over microplots 6 to 11, and every combination appears once per site. The fences were "maintained yearly at the time of data collection, except in 2020" (Sec. 2.2), so `fence` records the assignment, not seven years of exclusion.
        - No duplicate rows.
        - Probes (2026-11-03, untuned, the forest-stratified splits, 60): random forest R^2 0.29 on the log1p target (LightGBM 0.23, kNN 0.15, ridge 0.14; with the site means shuffled across sites at most 0.03) and RMSE 16.9 seedlings on the count, better than the mean count (23.3) on 56 of 60 splits. On the earlier unstratified splits (2026-11-01, 30): better than the mean count on 30 of 30, than the back-transformed mean of log1p on 24 of 30, and than the mean on the log scale on 28 of 30; the treatment flags add R^2 0.018 (paired SE 0.003, positive on 93% of splits), the change in log count ranging from +0.48 under the fence alone to -0.37 under herbicide alone. On stocking calls at held-out sites (SILVAH's thresholds, a diagnostic only), no untuned model beats carrying the 2014 count forward (review panel), so the treatment's effect is weakly identified (named in `fit_reason`). The 2014 count of the same seedlings is the strongest single input (R^2 0.22 alone), the natural core of the task. Held out by site, LightGBM loses R^2 0.14 against random microplots; site means hold 52% of the target's variance.
        - Note: the metric is RMSE on the count, which one or two dense sites per fold decide (MET-10): one test site of 8 holds a median 47% of the random forest's squared error (up to 72%; stratified splits), and 9 of 60 test folds hold no microplot with 69 or more seedlings. A linear model fit on log1p can score in the thousands after the inverse (ridge: count RMSE 2,543 over 30 splits), from a few extrapolated predictions (review panel, 2026-11-01). RMSE kept (CC 2026-11-02, Andrej): the fallback, AIC read as an in-sample model choice, not a score of predictions; not RMSLE and not the Poisson deviance nantucket_sound_sea_duck_aerial_survey_counts takes for its source's likelihood criterion.
    """

    # Task
    target = "log1p_seedlings_over_6in_2021"
    problem_type = "regression"
    metric = Metric.fallback(
        reason=(
            "The source tests treatments: Sec. 2.4 (reproduced in the Dryad methods) fits GLMMs of the 2014-2021 "
            "change in seedling count and aggregate height on the three treatments and ranks them by AIC, an "
            "in-sample model-selection criterion; no prediction error on new sites is reported there. The paper's "
            "results could not be read (the publisher answers automated requests with a bot check)."
        ),
        target_transform="log1p",
    )
    grouping = Grouping(
        on="site",
        labels="per_sample",
        prediction_unit="row",
        context="all_rows",
        definition="""
            One group is a sampling site: one of 24 locations drawn at random from 100 in the Rothrock and Bald Eagle state forests, a network of 11 plots within 110 x 52 m (Sec. 2.1-2.2), with 9 to 11 microplots in the file. Microplots of a site share soil, overstory and deer pressure; the authors include "Site ... as a random intercept effect to account for potential similarities among microplots within a sampling site" (Sec. 2.4). The use case is a stand that has not been followed: its whole pre-treatment inventory is known when predicting (context "all_rows"), none of its outcomes. Each microplot is one prediction.
        """,
    )
    stratify_on = "state_forest"
    accepted_check_warnings = {
        "task_stratify_on_regression": (
            "`state_forest` is a discrete feature with two values, one per site: the site folds are balanced on the "
            "forest so every training side has both (Andrej, 2026-11-03, issue 2)."
        ),
    }
    splits_comment = """
        Grouped splits on the site, stratified by state forest (CC 2026-11-03, Andrej, issue 2): all microplots of a site stay on one side, and every test fold holds 3-5 sites of each forest, so each training side has both forests, as a model built from the study would. A test fold stands for 8 stands never followed, each with every treatment combination once beside 2-4 controls. Forced grouped: the real task forecasts a later cohort, which one cohort cannot test. The test sites are new sites of the Rothrock and Bald Eagle state forests, all followed over the same 2014-2021 years, so the score does not cover other forests or later years. Stricter than the source, which fits all 24 sites with site as a random effect.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "DataCJFR.csv", encoding="utf-8-sig")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # 1. The two empty rows at the end of the file
        df = raw.dropna(how="all").copy()
        # 2. The site is the group; the treatment flags get readable labels
        df["site"] = df["PLOT"].astype(int).map("site_{:03d}".format)
        for col in ["FENCE", "LIME", "HERB"]:
            df[col] = df[col].map({"Y": "Yes", "N": "No"})
        # 3. The target: the 2021 count of seedlings over 6 in, logged (the metric scores the count)
        df[self.target] = np.log1p(df[TARGET_COUNT])
        # 4. Drops: values measured after the 2014 inventory (LEAK-10), the raw target, identifiers and the
        #    treatment code (a copy of the three flags)
        df = drop_columns(df, [*AFTER_PREDICTION_POINT, TARGET_COUNT, "UID", "PLOT", "SUBPLOT", "TRT"])
        return df.rename(columns=RENAME)

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=["site", "state_forest", "fence", "lime", "herbicide"],
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        from scipy.stats import mannwhitneyu

        data = raw.dropna(how="all")
        treated = data[data["TRT"] != "C"]  # lime was randomised among microplots 6-11 (and 5 is never limed)
        rows = []
        for col in ["PH14", "AL", "MN", "PH16"]:
            limed = treated.loc[treated["LIME"] == "Y", col].dropna()
            unlimed = treated.loc[treated["LIME"] == "N", col].dropna()
            rows.append(
                {
                    "column": col,
                    "mean, limed": round(limed.mean(), 2),
                    "mean, unlimed": round(unlimed.mean(), 2),
                    "Mann-Whitney p": f"{mannwhitneyu(limed, unlimed).pvalue:.2g}",
                    "missing (all microplots)": int(data[col].isna().sum()),
                }
            )
        soil = pd.DataFrame(rows).set_index("column")

        count14, count21 = data["SEED14_COUNT_OVER_6IN"], data[TARGET_COUNT]
        zeros = pd.DataFrame(
            {
                "microplots": [len(data), int((count14 == 0).sum()), int((count14 > 0).sum())],
                "2021 count = 0": [
                    int((count21 == 0).sum()),
                    int((count21[count14 == 0] == 0).sum()),
                    int((count21[count14 > 0] == 0).sum()),
                ],
                "2021 count = 1": [
                    int((count21 == 1).sum()),
                    int((count21[count14 == 0] == 1).sum()),
                    int((count21[count14 > 0] == 1).sum()),
                ],
            },
            index=["all", "2014 count = 0", "2014 count > 0"],
        )
        return [
            Decision(
                "The 2014 soil values are pre-treatment, the 2016 pH is not",
                "Lime was randomised over the treated microplots, so a soil value sampled before the lime does not "
                "differ between limed and unlimed ones. PH14, AL and MN do not; PH16 does, by 1.2 pH units, and is "
                "dropped with the other post-treatment columns (LEAK-10).",
                soil,
            ),
            Decision(
                "The zeros of the 2021 count",
                "The target's zero (no seedling over 6 in) is its most frequent value only just, and it follows the "
                "2014 inventory, so it reads as the low end of the count rather than a separate regime.",
                zeros,
            ),
        ]
