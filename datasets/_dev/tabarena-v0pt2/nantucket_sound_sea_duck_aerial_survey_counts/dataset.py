"""Curated dataset definition for `nantucket_sound_sea_duck_aerial_survey_counts` (data-foundry v2). Evidence: README.md."""

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
    TaskSummary,
    drop_columns,
)

SPECIES_GROUP = "LTDU"  # long-tailed duck, one of the source's three groups (COEI, SCOT, LTDU); see curation_comments
WINTER_LABELS = {2003: "2003/04", 2004: "2004/05", 2005: "2005/06"}
GRID_M = 1500.0  # the side of a segment of the source's grid (504 cells on a 24 x 24 lattice)
RENAME = {
    "x": "utm19n_easting_m",
    "y": "utm19n_northing_m",
    "length": "transect_km",
    "time": "day_of_winter",
    "SSTw": "sst_winter_mean_c",
    "SSTm": "sst_month_c",
    "SSTrel": "sst_month_relative_c",
    "SBT": "bottom_temp_summer_c",
    "chla": "chlorophyll_a_mg_m3",
    "cdom": "cdom_absorbance",
    "meanphi": "sediment_grain_size_phi",
    "depth": "seabed_elevation_m",
    "d2land": "distance_to_land_km",
    "SAR": "seafloor_surface_area_ratio",
    "tidebmean": "tidal_velocity_bottom_mean_m_s",
    "tidesd": "tidal_velocity_sd_m_s",
    "strat": "stratification_log10",
    "NAOw": "nao_winter",
    "ferry": "ferry_route_within_1km",
}


class NantucketSoundSeaDuckAerialSurveyCounts(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "How many long-tailed ducks on the water does an aerial survey count in its strip through a 1.5 km square "
            "of Nantucket Sound on a winter survey day, for a square the survey flights did not cover?"
        ),
        use_case=(
            "After the last of three winters of aerial surveys (spring 2006), an analyst fills in the long-tailed "
            "ducks in the parts of Nantucket Sound the plane did not fly on each survey day, from the seabed, the "
            "ocean and that day's counts elsewhere. The source models the Sound this way for planners siting "
            "offshore wind farms or protected areas, though its maps show a seasonal density per square."
        ),
        row=(
            "One 1.5 km x 1.5 km segment of the source's grid on one survey day, that is the strip about 180 m wide "
            "flown through it: 7,751 segment-days of 30 surveys in the winters 2003/04 to 2005/06, over 454 of the "
            "grid's 504 segments."
        ),
        predicted=(
            "The number of long-tailed ducks counted on the water in that strip (flying birds are left out), shipped "
            "on a log scale and scored on the count. 57.1% of the segment-days have none; the others hold a median of "
            "7, and counts of 100 or more (3.6% of them) hold 45% of the ducks, up to 3,000."
        ),
        known=(
            "The segment's position and seabed (elevation, sediment grain, seafloor relief, tidal currents, distance "
            "to land, a ferry route), ocean colour and modelled sea temperatures, the winter and its NAO index, the "
            "day of the winter and the length of strip flown."
        ),
        split=(
            "Whole north-south transects (columns of the source's 1.5 km grid) are held out with all their survey "
            "days, as the field validates (BOEM 2018-010, Sec. 2.5.6), so a test square stands for a line the plane "
            "did not fly; the other transects flown that day are in training."
        ),
        changes=(
            "We took the long-tailed duck from the source's three species groups, rebuilt the authors' table from "
            "their unscaled covariates (their analysis files standardise every column over all rows), and hold out "
            "whole transects, where the source fitted on all rows."
        ),
        fit="approximate",
        fit_reason=(
            "One daytime strip count on one survey day stands for the seasonal density per square that planners read "
            "off the source's maps, and for this species it misses most of the birds, which are largely absent from "
            "the Sound by day (Allison, Perkins & Perry 2009, MMS 2009-020). The strip length is known for a test "
            "row, where a map sets 1.5 km."
        ),
    )

    # Dataset
    unique_name = "nantucket_sound_sea_duck_aerial_survey_counts"
    year = "2019"  # the Dryad deposit of 2019-02-15, the first publication of the segment table (PROV-9)
    domain = "biology & life sciences"
    source = "Other"  # Dryad, the data deposit of Smith et al. (2019)
    source_url = "https://doi.org/10.5061/dryad.1vm20t6"
    license = "CC0 1.0"  # stated on the Dryad deposit and its Zenodo mirror
    data_tags = ("Spatial",)
    download_description = """
        The Dryad deposit doi:10.5061/dryad.1vm20t6 (2019-02-15) answers automated downloads with 401 (its API needs a bearer token), its web download with 403 and its version route with 405 (too large for zip generation). Dryad's own mirror on Zenodo, record 4932958, carries the same DOI and the same four files; its md5 of the archive equals Dryad's own file listing. We take Data/ducks&environment.RData from NanSound_Ecol&Evol.zip (990 MB; the other files are the README and two fitted-model archives, Results_ltdu.zip and Results_scot.zip) and export its two data frames to CSV with pyreadr; in R, load() and write.csv(env.segs, row.names = FALSE) give the same values.

        mkdir -p local-data-warehouse/nantucket_sound_sea_duck_aerial_survey_counts/rdata && cd local-data-warehouse/nantucket_sound_sea_duck_aerial_survey_counts
        curl -L -o NanSound_Ecol_Evol.zip 'https://zenodo.org/api/records/4932958/files/NanSound_Ecol&Evol.zip/content'
        md5sum NanSound_Ecol_Evol.zip
        # 6c4e32882f86b3b0d22c46805b8067d6  NanSound_Ecol_Evol.zip
        unzip -p NanSound_Ecol_Evol.zip 'NanSound_Ecol&Evol/Data/ducks&environment.RData' > rdata/ducks_and_environment.RData
        uvx --from pyreadr==0.5.7 --with pandas==3.0.6 python -c "import pyreadr; r = pyreadr.read_r('rdata/ducks_and_environment.RData'); r['env.segs'].to_csv('env_segs.csv', index=False); r['obs.final'].to_csv('obs_final.csv', index=False)"
        sha256sum rdata/ducks_and_environment.RData env_segs.csv obs_final.csv
        # 456f2407cd729fab8f30b0ce042fd3f8ea513dbc61876bfd7d7d7d356015530b  rdata/ducks_and_environment.RData
        # 742072e9673a2ea6768c471e7f12d15a22d7803fb547da62a42265941c9c3784  env_segs.csv
        # 2765785c79296b99ceab6f778a111c4b86ebc0b645deb8d16b399ccf5ad8595a  obs_final.csv
    """
    bibtex = """
        @misc{smith2019nantucketdata,
          title = {Data from: Modeling spatiotemporal abundance of mobile wildlife in highly variable environments using boosted {GAMLSS} hurdle models},
          author = {Smith, Adam D. and Hofner, Benjamin and Lamb, Juliet S. and Osenkowski, Jason and Allison, Taber and Sadoti, Giancarlo and McWilliams, Scott and Paton, Peter},
          year = {2019},
          publisher = {Dryad},
          doi = {10.5061/dryad.1vm20t6},
          howpublished = {\\url{https://doi.org/10.5061/dryad.1vm20t6}},
          note = {Data of Smith et al. (2019), Ecology and Evolution 9:2346-2364, doi:10.1002/ece3.4738}
        }
    """
    curation_comments = """
        We start with the data frames env.segs (the 504 segments x 30 survey dates, with the transect length flown and the covariates of Table 1) and obs.final (counts per segment, date and species group) in Data/ducks&environment.RData of the Dryad deposit of Smith et al. (2019), taken from its Zenodo mirror and exported to CSV.

        - Prediction point: after the last survey of 2005/06 (spring 2006), when the source fitted one model on all 30 surveys and drew its maps; for each survey day, the long-tailed ducks in the squares the plane did not fly. Known then are the covariates of the source's Table 1 (the 2002-2006 ocean-colour means and the 2003-2005 tidal means included), the winter, the day and the strip length. Distribution mapping, as the source describes it, uses such models "to predict utilization of un-sampled areas or time periods based on biophysical habitat features" (Introduction); the decision it names is siting: "marine spatial planners must carefully consider the most appropriate information to use when deciding, for example, where to place marine protected areas or offshore wind energy developments" (Sec. 4.2).
        - Survey days, not map dates: the source's maps give every segment "predicted on 10 evenly-spaced dates from 15 November through 1 April in each winter" (Figs. 4-6), which are not survey days, and planners read the seasonal value per square. The task fills in a surveyed day, whose level the model learns from the other squares flown that day, as the field validates such models (BOEM 2018-010, Sec. 2.4: the survey as a random effect; Sec. 2.5.6: cross-validation stratified by transect). On the block splits the survey day's training mean alone reaches R^2 0.13 on log1p, against 0.18 for untuned LightGBM, and LightGBM without the winter, the day, the NAO index and the monthly sea temperatures -0.001 (9 splits). A new square on a date not in training (segments and survey dates held out together) scores -0.077, below the training mean (-0.007; review panel).
        - Regime: grouped, not the temporal split the screening proposed (later winters from earlier ones). The regime follows the source's maps of the surveyed winters; it never forecasts a later one ("Since additional test data were not available for our study area, we used a pseudo R2 measure of the explained variation", Sec. 2.5). A forecast of a later winter fails TP-10 leg 1, so a temporal task would be `No` under SEL-10: trained on 2003/04-2004/05 and tested on the three parts of 2005/06, neither the covariates nor a segment's own past predict it (best untuned model R^2 0.04 on log1p, the segment's past mean 0.025; RMSE on the count 105.9 against 106.6 for the past mean).
        - Group: the transect column (`transect_column`), a column of the source's 1.5 km grid, along which the plane flies north-south (Sec. 2.1.2); 24 columns, built exactly from the coordinates (SPLIT-24). The field validates by holding out whole transects (BOEM 2018-010, Sec. 2.5.6), and the curator chose the field's practice (Andrej, 2026-11-03, review issue 1: "We should definitely use what the field uses"). Single held-out segments kept their neighbours on the same flight line, flown minutes apart, in training (95% of test rows had a square flown the same day within 1.5 km; without only those neighbours R^2 on log1p fell from 0.251 to 0.177); 3 x 3 blocks of the grid were the panel's alternative. On the declared metric, the mean Poisson deviance, untuned LightGBM with a Poisson loss explains 4.2% of the training mean's deviance under transect columns (0.8% to 12.8%, above the mean on 9 of 9 folds of 3 repeats), against 7.9% under 3 x 3 blocks (review, 2026-11-03).
        - Target: the long-tailed duck (LTDU), one of the three groups the source models apart, chosen on all rows, test folds included (the Decision). On the earlier 3 x 3 block splits untuned LightGBM reached R^2 0.18 on log1p for it and -0.08 for the common eider, which has 75.1% zeros ("no eiders were detected in 75% of segment observations", Sec. 2.2) and counts up to 30,000. The scoters pool four codes (SUSC, WWSC, BLSC, UNSC in R/create_final_data.R; "we pooled all scoter observations", Sec. 2.1.2) and reach 0.20 on log1p, but one raft of 70,000 holds 67% of their squared deviation from the mean on the count. Long-tailed duck: 57.1% zeros; the other counts have a median of 7, counts of 100 or more (3.6% of them) hold 45% of the ducks, up to 3,000, and the 10 largest counts hold 84% of the squared deviation. Shipped as log1p, scored on the count (`target_transform="log1p"`).
        - The counts are of ducks on the water, the quantity a habitat map wants. The same flights' raw sightings are archived at NOAA NCEI (accession 0115356, dataset MassAudNanAerial, 39,559 records, August 2002 to March 2006), and the deposit equals NCEI's in-strip long-tailed duck count minus the birds marked flying on 3,609 of the 3,612 segment-days with the species in either (the daily ratio is 1.000 on every day of 2003/04 and 2004/05 but one, 0.996). NCEI has no behaviour field for 2005/06; there the deposit lacks two flocks, 711 ducks on 2006-02-08 and 800 on 2006-03-06 (zero bullet), probably flying birds, not shown. NCEI holds 7 more winter survey days (2004/05: 2; 2005/06: 5), which the paper's "30 ... standardized aerial strip-transect surveys" (Sec. 2.1.2) leave out without a stated reason; they are not in the deposit and not added.
        - Daytime use only: the team that flew these surveys wrote that they were flown "during daylight hours when the vast majority of LTDUs are absent from the Sound" (Allison, Perkins & Perry 2009, MMS 2009-020). The counts miss the night roosting and the dawn and dusk commute that the species' siting question at Horseshoe Shoal was about; a reason for `fit="approximate"`, not a change to the data.
        - A zero is a flown strip without a long-tailed duck on the water; the authors "assumed our survey design led to a low incidence of false zeros" (Sec. 2.2), though "our survey methods did not address potential undercounting of individuals that were diving during flyovers" (Sec. 2.1.2). One known gap: NCEI places 800 long-tailed ducks on transect 11-10 on 2006-03-06 (13:04-13:06, one position, all in segment 329), which are in no deposit row and not in the authors' own sighting table (GIS/Survey/obs_poly.dbf); the segment holds a zero that day. The sightings share one position, so no rule locates the rest of that pass, and the rows stay (LEAK-25).
        - Rows: the segment-days with a transect length above 0, with a zero where obs.final has no long-tailed duck, as the authors build their model data (`subset(env.segs, length > 0)` and the zero fill in R/model_ltdu.R): 7,751 rows, the 30 surveys of the paper (13, 10 and 7 per winter). The 50 segments never flown and the 7,369 segment-days not flown are no rows.
        - Covariates from env.segs as the authors computed them (R/create_final_data.R), unscaled. Their per-species files (data_ltdu.Rda) standardise every continuous column over all 7,751 rows (`scale()` in R/model_ltdu.R), so we rebuild the table from env.segs (PROV-13; LEAK-30 avoided).
        - Dropped: `xkm` and `ykm`, the coordinates minus their medians over the grid, in km (exact copies of the easting and northing); the segment number, an id of 454 levels that no test fold has seen, replaced by the group column; the date. The winter and the day of the winter, the source's own covariates (Table 1), give the date (the day takes 28 values over the 30 dates), and a winter spans two calendar years, so we keep these parts, as the source does, rather than the date. The authors' effort covariate `obs_window` (2 x 91.44 m x the length) is not built: `transect_km` holds it.
        - `transect_km` is the length of strip flown in the segment (0.002 to 3.18 km; above about 1.6 km, 94 rows, where a transect crossed the segment twice; 353 rows below 0.3 km, kept as the authors kept them). The count grows with it: an exposure, a feature as in the family's call of 2026-10-30.
        - `seabed_elevation_m` is the source's `depth`, the seabed's elevation relative to mean high water, -21.4 to -1.5 m ("lower values = deeper water", Table 1); renamed so that the name matches the sign, values kept.
        - `sst_month_relative_c` is the month's sea temperature minus its mean over the 504 segments of that month (R/create_final_data.R): a statistic of the temperature field, known for every segment, not of the counted rows.
        - Note: `sst_winter_mean_c` (November to March) and `nao_winter` (December to March) take months after a survey day, `chlorophyll_a_mg_m3` and `cdom_absorbance` are geometric means of the monthly composites from July 2002 to March 2006, and the tidal velocities and stratification are 2003-2005 means (Table 1): all known in spring 2006, not for a map made during a winter. `nao_winter` has one value per winter (-0.09, 0.38, -0.87), a recoding of `winter`; both are covariates of Table 1.
        - Metric: the mean Poisson deviance on the count, predictions floored at 0.01 ducks, a stand-in for the source's out-of-bag likelihood (CC 2026-11-02, Andrej: the deviance here, wadden_sea_sibes_macoma_abundance and pennsylvania_oak_hickory_regeneration_experiment keep RMSE; this source names one count-likelihood criterion, theirs do not). Under RMSE, one to four of about 2,600 test rows per split hold half the squared deviation from the training mean (one or two on 8 of the 9). On the block splits the training mean scores 64.37, untuned LightGBM on log1p 64.30 and LightGBM with a Poisson loss 64.41, though the log1p fit's back-transformed predictions sum to 28% of the observed test total and the Poisson fit's to 68%. Under the mean Poisson deviance (predictions floored at 0.01) the Poisson fit is 9.8% below the training mean on 9 of 9 splits and the tree fits on log1p 13% to 15% above it (review panel, 8 untuned fits).
    """

    # Task
    target = "log1p_long_tailed_duck_count"
    problem_type = "regression"
    metric = Metric.stand_in(
        "mean_poisson_deviance",
        original=(
            "the out-of-bag negative log-likelihood of the boosted GAMLSS hurdle model, by which Smith et al. (2019) "
            "stop the boosting (Sec. 2.3.2), and the pseudo R2 on that likelihood they report (Sec. 2.5: 'Since "
            "additional test data were not available for our study area, we used a pseudo R2 measure of the "
            "explained variation')"
        ),
        reason=(
            "Both score a predictive distribution, which a point prediction does not give; the comparison of "
            "predicted and counted totals per survey (Fig. 8) is a plot, not a score, and the deposit's README "
            "defines no metric. The mean Poisson deviance on the count in the strip is the count likelihood of a "
            "predicted mean, the closest score a point prediction allows (curator, 2026-11-02). RMSE on the count "
            "could not tell a fit whose predicted totals are 28% of the observed from the training mean (64.30 "
            "against 64.37), where the deviance ranks the calibrated Poisson fit 9.8% below the mean on 9 of 9 "
            "splits. Predictions below 0.01 ducks count as 0.01, so a model that predicts none still scores."
        ),
        reference="Smith et al. 2019, Ecology and Evolution 9:2346-2364, https://doi.org/10.1002/ece3.4738, Sec. 2.3.2",
        params={"min_prediction": 0.01},
        target_transform="log1p",
    )
    grouping = Grouping(
        on="transect_column",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a transect column: a column of the source's 1.5 km grid over Nantucket Sound, flown north-south (24 columns), its key each segment's column counted from the grid's south-west cell, exact from the coordinates. Held out with all its survey days, a column stands for a transect the plane did not fly, the unit the field holds out to validate its models (BOEM 2018-010, Sec. 2.5.6). The other transects flown on the same day stay in training, so the day's level is learnable from them. The source fitted on all rows and validated in sample (Smith et al. 2019, Sec. 2.5). Each segment-day is one prediction.
        """,
    )
    splits_comment = """
        Default grouped splits on `transect_column`, whole north-south transects of the source's 1.5 km grid with all their survey days, as the field validates (BOEM 2018-010, Sec. 2.5.6; Andrej, 2026-11-03). A test column stands for a transect the plane did not fly; the other transects flown that day are in training, so the model learns the day's level from them. On the mean Poisson deviance a Poisson LightGBM beats the training mean on 9 of 9 folds of 3 repeats (4.2% of its deviance explained). Grouped rather than temporal: the regime follows the source's maps of the surveyed winters; a forecast of a later winter fails TP-10 leg 1, so a temporal task would be `No` under SEL-10 (curation_comments).
    """

    accepted_check_warnings = {
        "task_target_value_dominant": (
            "57.1% zeros: observed absences, a flown strip without a long-tailed duck on the water (Andrej, "
            "2026-11-03: a valid zero-inflated regression task)."
        ),
    }

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        return {
            "env": pd.read_csv(raw_dir / "env_segs.csv"),
            "obs": pd.read_csv(raw_dir / "obs_final.csv"),
        }

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        env, obs = raw["env"], raw["obs"]
        assert not env.duplicated(["seg", "date"]).any()
        assert not obs.duplicated(["seg", "date", "group"]).any()

        # 1. The flown segment-days (transect length above 0), as the authors' model scripts subset them.
        df = env[env["length"] > 0].copy()

        # 2. The target: long-tailed ducks counted in the strip; a flown segment-day without a record is a zero.
        ltdu = obs[obs["group"] == SPECIES_GROUP].set_index(["seg", "date"])["count"]
        key = pd.MultiIndex.from_frame(df[["seg", "date"]])
        assert key.isin(ltdu.index).sum() == len(ltdu)  # every count falls on a flown segment-day
        count = pd.Series(ltdu.reindex(key).to_numpy(), index=df.index).fillna(0.0)
        df[self.target] = np.log1p(count)

        # 3. The group: the transect column, each segment's column on the source's grid counted from its south-west
        #    cell (the offsets are whole multiples of 1.5 km); the plane flies the columns north-south.
        col = (df["x"] - env["x"].min()) / GRID_M
        row = (df["y"] - env["y"].min()) / GRID_M
        assert np.allclose(col, col.round())
        assert np.allclose(row, row.round())
        df["transect_column"] = "c" + col.round().astype(int).astype(str).str.zfill(2)

        # 4. Readable names and labels.
        df = df.rename(columns=RENAME)
        df["winter"] = df["winter"].map(WINTER_LABELS)
        df["ferry_route_within_1km"] = df["ferry_route_within_1km"].map({0: "no", 1: "yes"})

        # 5. The segment number (an id unseen in every test fold); copies: xkm and ykm are the coordinates shifted and
        #    in km, the date is the winter plus the day.
        return drop_columns(df, ["seg", "xkm", "ykm", "date"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["transect_column", "winter", "ferry_route_within_1km"])

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        env, obs = raw["env"], raw["obs"]
        flown = env.loc[env["length"] > 0, ["seg", "date"]]
        rows = []
        for group, name in [("LTDU", "long-tailed duck"), ("SCOT", "scoters (4 codes)"), ("COEI", "common eider")]:
            counts = flown.merge(obs[obs["group"] == group], on=["seg", "date"], how="left")["count"].fillna(0.0)
            deviation = (counts - counts.mean()) ** 2
            rows.append(
                {
                    "group": name,
                    "segment-days": len(counts),
                    "share zero": round(float((counts == 0).mean()), 3),
                    "mean": round(float(counts.mean()), 1),
                    "max": int(counts.max()),
                    "share of squared deviation in the largest": round(float(deviation.max() / deviation.sum()), 3),
                    "share of squared deviation in the 10 largest": round(
                        float(deviation.nlargest(10).sum() / deviation.sum()), 3
                    ),
                }
            )
        return [
            Decision(
                title="The long-tailed duck as the target",
                why=(
                    "The source models three groups apart. We take the long-tailed duck for its signal on held-out "
                    "blocks (untuned LightGBM R^2 0.18 on log1p, the eider -0.08) and its fewer zeros (57% against "
                    "75% for the eider). The scoters reach 0.20 on log1p, but one raft of 70,000 holds 67% of their "
                    "squared deviation, so an error on their count comes down to one row. The eider's largest counts "
                    "dominate less than the long-tailed duck's. Chosen on all rows, test folds included."
                ),
                evidence=pd.DataFrame(rows).set_index("group"),
            )
        ]
