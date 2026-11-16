"""Curated dataset definition for `uniform_soybean_tests_yield` (data-foundry v2). Evidence: README.md."""

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
)

TARGET = "yield_bu_acre"
# The seven daily weather variables of the release, in the order of the last axis of `inputs_weather_train.npy`
# (EvalAI 1251, "Dataset"); units from the authors' preprocessing script `Data_ts_214_days.py`.
WEATHER = ("ADNI", "AP", "ARH", "MDNI", "MaxSur", "MinSur", "AvgSur")
N_DAYS = 214  # 1 April to 31 October, the same 214 calendar days every year
OTHERS = ("maturity_group", "genotype", "state", "year", "location")
RELEASE = Path("Dataset_Competition")


def weather_columns() -> list[str]:
    """The names of the 214 x 7 daily weather columns, `<variable>_d<day>` with day 1 the 1st of April."""
    return [f"{var}_d{day:03d}" for var in WEATHER for day in range(1, N_DAYS + 1)]


class UniformSoybeanTestsYield(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "What seed yield, in bushels per acre, does a soybean line give at a trial location in a season not yet in "
            "the data, given the maturity group of its test, its pedigree group and the location's daily weather from "
            "April to October?"
        ),
        use_case=(
            "A soybean breeder or the Uniform Soybean Tests coordinator predicts each entry's yield at the locations of "
            "a season not yet in the data, from the line, the site and that season's weather taken as a given "
            "condition, to choose which lines to advance and where to test them; the model is fit on the earlier "
            "seasons' trials."
        ),
        row=(
            "One line in one test of the USDA Uniform Soybean Tests at one location in one year, 2003-2015 (US and "
            "Canada, maturity groups 00 to VIII; the 93,028 records the MLCAS2021 challenge released with yields)."
        ),
        predicted=(
            "The line's seed yield at that location and year in bushels per acre: its entry mean at the location, as "
            "the UST report prints it."
        ),
        known=(
            "The year, the location and its state or province, the maturity group of the test, an anonymized line id "
            "and its pedigree cluster, and seven daily weather variables at the location from 1 April to 31 October, "
            "taken as a given condition of the season."
        ),
        split=(
            "Whole seasons are held out: each test year is predicted by a model trained on all earlier years, so "
            "the test stands for a new season's trials, about half of them with lines never tested before."
        ),
        changes=(
            "The challenge's random split is replaced by held-out years, so a model predicts environments it has not "
            "seen instead of reading each environment's level off the other lines of it in training."
        ),
        fit="approximate",
        fit_reason=(
            "Four gaps, largest first: the breeder acts on a line's yield relative to its test's other entries and "
            "checks, but the target is the absolute yield and RMSE scores mostly each new location-year's level; the "
            "season's weather, known only at harvest, enters as a given condition, not a forecast; no test id or check "
            "flag (a location-year pools 2 to 4 maturity-group tests); no soil, planting date or management."
        ),
    )

    # Dataset
    unique_name = "uniform_soybean_tests_yield"
    year = "2021"
    domain = "biology & life sciences"
    source = "Other"  # the PLOS ONE paper's data (Shook et al. 2021), released as the MLCAS2021 challenge on EvalAI
    source_url = "https://doi.org/10.1371/journal.pone.0252402"
    license = "MLCAS2021 challenge terms: academic use; no commercial use without the organisers' permission"
    data_tags = ("Spatial",)
    download_description = """
        The MLCAS2021 Crop Yield Prediction Challenge (https://eval.ai/web/challenges/challenge-page/1251/overview)
        linked its data as one zip on Google Drive (https://drive.google.com/file/d/1DoyextA0q4mxumMAhBvqZbfZriIM9A-Y),
        which answers 404 since at least 2026-11-09; the paper's Drive folder
        (https://drive.google.com/drive/folders/1BLK56s_9z_O1DKJVGq10eKa-U5AykNY0) shows no files. We download a copy
        of the challenge zip that a participant of the University of Arizona's 2021 course INFO 529 put on CyVerse
        on 2021-10-23 (its Makefile fetches it: https://github.com/evan-mcginnis/INFO529-midterm); its files are dated
        2021-08-30, before the challenge opened, and their shapes match the challenge page (93,028 training and
        10,337 test records, 214 x 7 weather, 5,839 genotype clusters). The copy matches the authors' own files on
        GitHub (https://github.com/tryambakganguly/Yield-Prediction-Temporal-Attention, folder `data_subset/`):
        `clusterID_genotype.npy` is byte-equal to `k_means_clusters_20.npy`; the 103,365 genotype ids of the training
        and test inputs, and their (genotype, state) pairs, are the same multisets as `genotype_id_all_data.npy` and
        `state_list_all_data.csv`; 1,870 of the 2,000 rows of the authors' subset match a training record with
        identical 214-day weather, and the other 130 have their year, location and maturity group in the test inputs.
        mkdir -p local-data-warehouse/uniform_soybean_tests_yield && cd local-data-warehouse/uniform_soybean_tests_yield
        curl -O https://data.cyverse.org/dav-anon/iplant/home/evanmc/Dataset_Competition_Zip_File.zip  # sha256 e2cecf6793776eb265fab8367317fdf5d81a6c131ab14498c2af7f66dfd867e6
        unzip Dataset_Competition_Zip_File.zip  # Dataset_Competition/{Training,Test Inputs}/*.npy, clusterID_genotype.npy
    """
    bibtex = """
        @article{shook2021crop,
          title = {Crop yield prediction integrating genotype and weather variables using deep learning},
          author = {Shook, Johnathon and Gangopadhyay, Tryambak and Wu, Linjiang and Ganapathysubramanian, Baskar and Sarkar, Soumik and Singh, Asheesh K.},
          journal = {PLOS ONE},
          volume = {16},
          number = {6},
          pages = {e0252402},
          year = {2021},
          doi = {10.1371/journal.pone.0252402}
        }
    """
    curation_comments = """
        We start with the training files of the MLCAS2021 Crop Yield Prediction Challenge (EvalAI 1251): `inputs_others_train.npy` (maturity group, genotype id, state, year, location), `inputs_weather_train.npy` (214 days x 7 variables) and `yield_train.npy` for 93,028 records, plus `clusterID_genotype.npy`.

        - Prediction point: a season not yet in the data, before its trial results are compiled. The line, the maturity group of its test, its pedigree cluster, the location and the year are known before planting; the season's daily weather from 1 April to 31 October is taken as a given condition (the observed season or a scenario), not as a planting-time forecast. None of that season's yields is known, the checks and the other entries at the same location included. Nothing measured on the plot (protein, oil, lodging, height, maturity date) is in the release, and none would be allowed.
        - Source: Shook et al. (2021) converted the 26 PDF reports of the 2003-2015 Uniform Soybean Tests to spreadsheets (Material and methods: "Files from 2003-2015 USTs were downloaded as PDFs"; "Records that did not have yield data ... were removed"), matched each location-year to "the nearest grid point from a gridded 30km product (Weather.com)" and released 103,365 records; the challenge split them into 93,028 training records and 10,337 test records whose yields were never published, so only the training records ship. The paper's GitHub page points to a Google Drive folder that shows no files, and the challenge's own zip link answers 404 (2026-11-09); the copy we download is named in the download instructions. It is the authors' data: its pedigree clusters are byte-equal to the authors' `data_subset/k_means_clusters_20.npy` on GitHub, its 103,365 genotype ids (and genotype-state pairs) are the same multisets as the authors' lists, and 1,870 of the 2,000 rows of the authors' subset match a training record with identical weather (the other 130 sit in the test inputs).
        - Metric: RMSE in bu/acre, the challenge's leaderboard metric ("We will use Root Mean Square Error (RMSE) as the evaluation metric", EvalAI 1251, Evaluation; MET-4). The paper reports MAE, RMSE and R^2 side by side. What RMSE scores changes with our split: on held-out seasons it orders models by how well they guess each new location-year's level, which no feature predicts, and hardly by how they rank the lines within it. Over 13 untuned models (mean of the 6 windows 2010-2015), the order under RMSE follows the order under the error of the location-year means at Kendall tau 0.97, the order under the error within location-years at 0.33, and the order under the mean correlation within location-years at 0.38 (0.09 among the 9 competitive models); on 3 random folds of the records, as the challenge split, RMSE followed the error within location-years (tau 0.95-0.97). A location mean plus the yield trend, which cannot rank lines, ranks 3rd of 15 models and baselines under RMSE.
        - Split: the paper and the challenge split the records at random (Material and methods: "Data were randomly split into training (80%), validation (10%) and test (10%) sets"), so every test environment and every test line was also in training (all 10,337 challenge test records have a location-year and a genotype seen in its training set). On random folds of our records, untuned LightGBM with the daily weather reaches RMSE 6.68 and the same model with a location-year id in place of the weather 6.71 (one fold of three): the weather then only names the environment, whose level the other lines give away; on the held-out seasons 2010-2015 the same model scores 13.7 to 15.4. The paper's own aim is to predict "performance (for example, seed yield) in unseen and new environments" (Introduction), so we hold out whole years (`splits_comment`).
        - Note: on the held-out seasons, untuned models on all columns barely beat the training mean (task probes on the 7 windows: LightGBM RMSE 16.47 against the training mean's 16.67, ahead on 5 of 7 windows; random forest 16.81; the state alone 14.10), while simple models of the site and the line do better. The floor a method must beat (mean of the 6 windows 2010-2015): each location's mean over the earlier seasons 13.71, plus a linear yield trend 13.17, plus a shrunk effect of the line's earlier yields 13.04; with the 2009 window, 13.75, 13.31 and 13.13 over the 7 windows, and a ridge on monthly weather means in place of the trend 13.47, better only in 2009. That location mean plus a LightGBM of the residual on maturity group, pedigree cluster and year reaches 13.15; adding the weekly means of the weather raises it to 13.92 (worse on 5 of 6 windows). Beyond each location's mean and the yield trend, the weather adds nothing measurable for the models tried; on the record fields alone its effect depends on the model (a default LightGBM gains from the daily weather, 14.55 to 14.19, a regularised one loses, 14.04 to 14.76). A location-year's mean yield varies around its location's mean by 9.5 bu/acre (SD over the 1,117 location-years), and knowing each test environment's mean would leave 7.3-8.2: most of the error is the new season's level at a location. Measured with scratch scripts on the shipped windows (run of 2026-11-09), untuned, one seed.
        - Weather: shipped as published, one column per variable and day (`ADNI_d001` is 1 April, `..._d214` is 31 October): average and maximum direct normal irradiance (ADNI, MDNI), average hourly precipitation in inches (AP; on a 0.01 in/h grid, so a day with less than about 0.12 inch reads 0, and 77.6% of the days do), average relative humidity in % (ARH), and maximum, minimum and average surface temperature in degrees Fahrenheit (MaxSur, MinSur, AvgSur; "surface temperature" as the source names it, which runs hotter than 2 m air temperature: 303 location-days above 110 F, some in Minnesota and North Dakota). The series is the same for every record of a location-year (1,040 distinct series for 1,117 location-years; locations near one grid point share one). The paper averaged it to weeks (30 time steps) and Rafi et al. (2026, README of github.com/itsMustafamr/Yield) to the season's mean and SD; both are model choices, so the daily values stay.
        - Genotype: `genotype` is the release's anonymized line id (1 to 5,839, no names), kept as a category: a breeder knows which line a plot is, and 44-52% of a test year's records are of lines tested in an earlier year (LEAK-34: their earlier yields are known history). `genotype_cluster` is the challenge's K-means cluster (20 clusters) of a pedigree correlation matrix over all 5,839 lines, joined by id.
        - Protocol (LEAK-9, an evaluation leak): a method may use only the rows of a window's train indices (with their labels) and of its test indices (without labels); rows outside both, the later seasons included, are never read, also not to build features such as whether a line is entered again later. Lines entered again in a later season are the ones breeders advanced: their rows sit 1.2 to 1.8 bu/acre above their location-year's mean, the others 0.7 to 1.3 below. A flag of later presence read from the whole table lowers RMSE by 0.07 to 0.17 (about 1%; nothing in the 2015 window, which has no later season) and raises the mean correlation within location-years by 0.02 to 0.05.
        - Potential leak, kept on purpose: the pedigree clusters were fit once over all 5,839 lines, the lines of later years included. The clustering uses parentage only, never yields, and a breeder knows a new line's parents, so only the cluster boundaries carry anything of the later lines (LEAK-30, weak).
        - Maturity group: the maturity group of the test the record comes from, a number: the integer part of the relative maturity the trials are organised by; -1 is maturity group 00, the earliest (Minnesota, North Dakota, Ontario, Quebec, Manitoba, and 64 records of two Arkansas locations in 2003-2004). 215 lines (11.7% of the records) appear in two adjacent groups, a line entered in two tests. Kept as a number, not an ordered category (CLEAN-14): the groups are equal steps of relative maturity, 00 one step below 0, so a value between two groups means something.
        - State and location: `state` is the two- or three-letter code of the US state or Canadian province (quotes stripped), `location` the release's anonymized location id (159 ids, one state each, where the paper and the challenge count 150 locations), both categories.
        - Duplicates: 214 records (0.23%, in 172 groups) are exact copies of another, the yield included, and are dropped (LEAK-19): the same line, maturity group, location and year with the same yield to 0.1 bu/acre, most likely one report row converted twice; about 45 such ties would be expected by chance among the 3,618 groups of records that share every feature. Those groups (7,586 rows after the drop: one line entered twice at one location in one year, most likely in two tests of the same maturity group) keep their different yields: they are separate entries. Every copy lies within one year, so none crosses a split.
        - Anomaly: `AvgSur_d213` (30 October) equals the mean of days 212 and 214 in every row: the authors filled a missing value of that day from its neighbours (`Data_ts_214_days.py`: "Index(873) of Avg. Surface Temp is NA"). In 13,797 shipped records (14.9%; 178 of the 1,117 location-years; 13,843 of the 93,028 released records) the fill lies outside that day's minimum and maximum (`MinSur_d213`, `MaxSur_d213`), by up to 11.9 F, which an average cannot; those cells are set to missing (CLEAN-11), the others kept as released. Days with zero direct normal irradiance (2.2% of the days, in runs of at most 5) are kept as overcast days.
        - Anomaly: yields run from 0.4 to 112.4 bu/acre; the 45 records below 5 bu/acre are kept as reported (crop failures are real outcomes of a trial).
    """

    # Task
    target = TARGET
    problem_type = "regression"
    metric = Metric.source(
        "rmse",
        original="RMSE of the predicted yearly yield of each test record (bu/acre)",
        reference="https://eval.ai/web/challenges/challenge-page/1251/evaluation",
    )
    temporal = Temporal(
        on="year",
        # Explicit cutoffs: min_train_fraction with unit="unique" counts seasons, and the 2009 window trains on 6 of 13
        # seasons but 50.7% of the records.
        splits=TemporalSplits(window=1, unit="unique", cutoffs=(2015, 2014, 2013, 2012, 2011, 2010, 2009)),
        horizon=1,
        horizon_unit="years",
    )
    splits_comment = """
        Expanding-window temporal splits by year: 7 test windows of one season each (2015 back to 2009), each trained on every earlier season (2003 up to the year before), newest first; the training sides hold 50.7% to 93.1% of the records. The windows roll back while training keeps at least half of the records (the 2008 window would train on 41.2%), against the 9 folds an IID task of this size would get; the cutoffs are explicit since the library's share for a unique time value counts seasons, not records. A held-out season is a set of environments no model has seen: its weather, its locations' conditions that year, and about half of its lines (44-52% of a test season's records are of lines tested in an earlier season). The challenge's random split put every test location-year and line in training, where the same LightGBM scores RMSE 7.13 against 14.31 on held-out seasons, the weather then naming the environment. A split grouped by location-year scores 12.35-12.52 for LightGBM, about 1 bu/acre better than held-out seasons for every model tried, because the later seasons (the yield trend) and the same season's other locations are then in training, which a new season does not have; so it was not chosen. No gap: a season's yields are published in the annual UST report before the next season is harvested, and the time unit is the season.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        base = raw_dir / RELEASE
        others = np.load(base / "Training" / "inputs_others_train.npy", allow_pickle=False)
        weather = np.load(base / "Training" / "inputs_weather_train.npy", allow_pickle=False)
        yields = np.load(base / "Training" / "yield_train.npy", allow_pickle=False)
        clusters = np.load(base / "clusterID_genotype.npy", allow_pickle=False)
        assert others.shape == (93028, 5), others.shape
        assert weather.shape == (93028, N_DAYS, len(WEATHER)), weather.shape
        # (records, days, variables) -> one column per variable and day, variable-major.
        wide = weather.transpose(0, 2, 1).reshape(len(weather), -1)
        df = pd.DataFrame(others, columns=list(OTHERS))
        df["genotype_cluster"] = clusters[df["genotype"].astype(float).astype(int).to_numpy() - 1]
        df = pd.concat([df, pd.DataFrame(wide, columns=weather_columns())], axis=1)
        df[TARGET] = yields
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # 1. Types: the release stores the five record fields as text ("3.0", "\"KS\"").
        df["maturity_group"] = df["maturity_group"].astype(float)
        df["year"] = df["year"].astype(float).astype(int)
        df["state"] = df["state"].str.strip('"')
        df["genotype"] = "g" + df["genotype"].astype(float).astype(int).astype(str).str.zfill(4)
        df["location"] = "loc" + df["location"].astype(float).astype(int).astype(str).str.zfill(3)
        df["genotype_cluster"] = "c" + df["genotype_cluster"].astype(str).str.zfill(2)
        # 2. Exact copies, the yield included, are dropped. The weather is a function of the location and the year
        #    (one series per location-year), so the record fields and the yield identify a row.
        df = df.drop_duplicates(subset=[*OTHERS, "genotype_cluster", TARGET], keep="first")
        assert len(df) == 92814, len(df)
        # 3. The authors' fill of AvgSur on 30 October (the mean of days 212 and 214) is set to missing where it lies
        #    outside that day's minimum and maximum, which an average cannot.
        fill = "AvgSur_d213"
        impossible = (df[fill] < df["MinSur_d213"]) | (df[fill] > df["MaxSur_d213"])
        assert int(impossible.sum()) == 13797, int(impossible.sum())
        df.loc[impossible, fill] = np.nan
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["state", "location", "genotype", "genotype_cluster"])

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        years = sorted(df["year"].unique())
        first_line = df.groupby("genotype", observed=True)["year"].transform("min")
        rows = []
        for year in years[-7:]:
            test = df["year"] == year
            earlier = df["year"] < year
            rows.append(
                {
                    "test season": year,
                    "test records": int(test.sum()),
                    "train share of records": round(float(earlier.mean()), 3),
                    "records of lines tested earlier": round(float((first_line[test] < year).mean()), 3),
                    "records at locations seen earlier": round(
                        float(df.loc[test, "location"].isin(df.loc[earlier, "location"]).mean()), 3
                    ),
                    "location-years": int(df.loc[test, "location"].nunique()),
                }
            )
        key = [*OTHERS, "genotype_cluster"]
        counts = {
            "records released with a yield": len(raw),
            "exact copies dropped (yield included)": int(raw.duplicated(subset=[*key, TARGET]).sum()),
            "records shipped": len(df),
            "raw records sharing every feature with another": int(raw.duplicated(subset=key, keep=False).sum()),
            "shipped records sharing every feature with another (different yields kept)": int(
                df.duplicated(subset=key, keep=False).sum()
            ),
        }
        copies = pd.DataFrame({"count": list(counts.values())}, index=pd.Index(list(counts), name="records"))
        return [
            Decision(
                "Held-out seasons instead of the challenge's random split",
                "The challenge split at random, so every test location-year and line was in training and the weather "
                "only had to name the environment. A held-out season is new weather at the locations, with about half "
                "of its records from lines tested before.",
                pd.DataFrame(rows),
            ),
            Decision(
                "Exact copies dropped, records that share every feature kept",
                "Copies with the same yield to 0.1 bu/acre are most likely one report row converted twice; records "
                "with the same features and different yields are separate plots (two tests at one location).",
                copies,
            ),
        ]
