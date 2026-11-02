"""Curated dataset definition for `crms_phragmites_cover` (data-foundry v2). Evidence: README.md."""

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

VEGETATION_FILE = "CRMS_Marsh_Vegetation.csv"
POREWATER_FILE = "CRMS_Discrete_Hydrographic.csv"
SOIL_FILE = "CRMS_Soil_Properties.csv"

# The species, by its currently recognised name (three spellings: the species and two subspecies).
PHRAGMITES = "Phragmites australis"
# Cover below the 1% resolution of the field sheets: "<1" (Braun-Blanquet "+") and "Solitary" ("r").
TRACE_COVER = {"<1": 0.5, "Solitary": 0.5}
# The newest complete survey season of the pinned download (2026 holds only June-July visits).
LAST_SEASON = 2025
# Soil samples are averaged over the cores' top 24 cm (six 4-cm sections).
SOIL_TOP_CM = 24
# CIMS posts soil analyses 1 to 2.5 years after sampling, so a season takes cores sampled three seasons back or earlier.
SOIL_LAG_SEASONS = 3
# Not taxa: the 2006 species list entered bare ground and open water as species.
NOT_SPECIES = {"Bare Ground", "Water"}
# No herb layer is 6 m tall; one entry reads 1,219.2 cm (40 ft) under a dominant height of 61 cm.
HERB_HEIGHT_MAX_CM = 600
# Porewater salinity against its own specific conductance: 0.35-0.66 ppt per mS/cm (1st-99th percentile); 0.57 is the
# bulk ratio. A salinity above 50 ppt at more than twice what its conductance gives is a wrong entry.
SALINITY_CHECK_PPT = 50
PPT_PER_MS_CM = 0.57

VEGETATION_COLUMNS = {
    "Station ID": "station",
    "Collection Date (mm/dd/yyyy)": "date",
    "Community": "community",
    "% Cover Total": "cover_total",
    "% Cover Herb": "cover_herb",
    "% Cover Shrub": "cover_shrub",
    "% Cover Tree": "cover_tree",
    "% Cover Carpet": "cover_carpet",
    "Average Height Dominant (cm)": "height_dominant_cm",
    "Average Height Herb (cm)": "height_herb_cm",
    "Average Height Shrub (cm)": "height_shrub_cm",
    "Average Height Tree (cm)": "height_tree_cm",
    "Average Height Carpet (cm)": "height_carpet_cm",
    "Scientific Name As Currently Recognized": "species",
    "% Cover": "cover",
    "In/Out": "in_out",
    "Latitude": "latitude",
    "Longitude": "longitude",
    "Comments": "comment",
}
# The crews' estimate for a plot inside a dense reed stand they could not enter (2012-2016), e.g. "This station is in
# a dense stand of Phragmites australis that is difficult to access so cover was estimated in 2016.  Phragmites
# cover was estimated to be 100%."
ESTIMATE_PATTERN = r"[Pp]hragmites (?:australis )?cover was estimated to be (\d+)\s*%"
NUMERIC_VISIT_COLUMNS = {
    "cover_shrub",
    "cover_tree",
    "cover_carpet",
    "height_dominant_cm",
    "height_herb_cm",
    "height_shrub_cm",
    "height_tree_cm",
    "height_carpet_cm",
    "latitude",
    "longitude",
}
SOIL_COLUMNS = {
    "Dry Soil pH (pH units)": "soil_ph",
    "Soil Salinity (ppt)": "soil_salinity_ppt",
    "Bulk Density (g/cm3)": "soil_bulk_density",
    "Organic Matter (%)": "soil_organic_matter_pct",
    "Total Nitrogen (g/kg)": "soil_total_nitrogen",
    "Total Phosphorus (mg/kg)": "soil_total_phosphorus",
}
# What the station showed at its latest visit before the season, carried as `previous_<name>`.
PREVIOUS = [
    "community",
    "cover_total",
    "cover_herb",
    "cover_shrub",
    "cover_tree",
    "cover_carpet",
    "height_dominant_cm",
    "height_herb_cm",
    "height_shrub_cm",
    "height_tree_cm",
    "height_carpet_cm",
    "species_count",
    "phragmites_cover",
    "phragmites_nearby",
    "porewater_salinity_ppt",
]


def _site(station: pd.Series) -> pd.Series:
    """The CRMS site of a station id (`CRMS0153-V51` -> `CRMS0153`)."""
    return station.str.split("-").str[0]


def _visits(veg: pd.DataFrame) -> pd.DataFrame:
    """One row per station visit (station and date), with the plot's measurements and its Phragmites record."""
    df = veg.rename(columns=VEGETATION_COLUMNS)
    df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y")
    for col in ("cover", "cover_total", "cover_herb"):
        df[col] = pd.to_numeric(df[col].replace(TRACE_COVER), errors="coerce")
    in_plot = df["in_out"].isin(["In", "Both"])
    is_phragmites = df["species"].astype("string").str.startswith(PHRAGMITES).fillna(False).astype(bool)
    # Cover is estimated inside the 4 m^2 plot only; "Out" marks a species seen near the plot, without cover.
    df["phragmites_cover"] = np.where(is_phragmites & in_plot, df["cover"], 0.0)
    df["phragmites_nearby"] = (is_phragmites & df["in_out"].isin(["Out", "Both"])).astype(int)
    df["in_plot_species"] = (df["species"].notna() & ~df["species"].isin(NOT_SPECIES) & in_plot).astype(int)
    # Every field but the species columns is one value per visit (the comment too).
    per_visit = {c: (c, "first") for c in VEGETATION_COLUMNS.values() if c not in {"station", "date", "species"}}
    per_visit.pop("cover")
    per_visit.pop("in_out")
    visits = df.groupby(["station", "date"], sort=True).agg(
        **per_visit,
        species_count=("in_plot_species", "sum"),
        phragmites_cover=("phragmites_cover", "sum"),
        phragmites_nearby=("phragmites_nearby", "max"),
    )
    return visits.reset_index()


def _porewater(hydro: pd.DataFrame) -> pd.DataFrame:
    """Porewater salinity readings (10 and 30 cm) with station, site, date and year."""
    pw = hydro.rename(
        columns={
            "CPRA Station ID": "station",
            "Date (mm/dd/yyyy)": "date",
            "Soil Porewater Specific Conductance (uS/cm)": "conductance",
            "Soil Porewater Salinity (ppt)": "salinity",
        }
    )[["station", "date", "salinity", "conductance"]]
    # Three readings (90, 71 and 57 ppt) contradict their own conductance (about 12.6, 7.1 and 5.8 ppt): missing.
    wrong = (pw["salinity"] > SALINITY_CHECK_PPT) & (pw["salinity"] > 2 * PPT_PER_MS_CM * pw["conductance"] / 1000)
    pw = pw[pw["salinity"].notna() & ~wrong].drop(columns="conductance").copy()
    pw["date"] = pd.to_datetime(pw["date"], format="%m/%d/%Y")
    pw["site"] = _site(pw["station"])
    pw["year"] = pw["date"].dt.year
    return pw


def _soil(soil: pd.DataFrame) -> pd.DataFrame:
    """Site means of the top 24 cm of the soil cores, one row per site and sampling year."""
    s = soil.rename(columns={"Station ID": "station", "Sample Date (mm/dd/yyyy)": "date", **SOIL_COLUMNS})
    s["date"] = pd.to_datetime(s["date"], format="%m/%d/%Y")
    top = pd.to_numeric(s["Sample Depth (cm)"].astype(str).str.extract(r"^(\d+)")[0], errors="coerce")
    s = s[top < SOIL_TOP_CM].copy()
    s["site"] = _site(s["station"])
    s["soil_year"] = s["date"].dt.year.astype("int64")
    return s.groupby(["site", "soil_year"], sort=True)[list(SOIL_COLUMNS.values())].mean().reset_index()


class CrmsPhragmitesCover(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "How much of a monitored 4 m^2 Louisiana coastal marsh plot will common reed (Phragmites australis) "
            "cover at its next annual survey, predicted before the season once the last season's surveys are in "
            "CIMS (they arrive over the winter)?"
        ),
        use_case=(
            "Between seasons, once the last season's surveys are in CIMS, a CPRA manager forecasts each monitored "
            "station's reed cover at next summer's survey, averaged to sites, to track spread in the western and "
            "central basins and die-back in the delta."
        ),
        row=(
            "One surveyed visit of a CRMS vegetation station in 2007-2025 (4,099 stations at 394 sites, mostly one "
            "visit a year), for stations surveyed in an earlier season."
        ),
        predicted=(
            "The percent cover of Phragmites inside the plot at that visit, 0-100; zero in 94% of the visits, "
            "mostly at stations where it was never recorded."
        ),
        known=(
            "The station's position and the visit's scheduled date (season and usual window, not the exact day), "
            "its latest earlier survey (marsh type, cover and height by layer, species count, reed in and near the "
            "plot, porewater salinity), whether a later visit found the plot in reed too dense to enter and the "
            "crew's estimate, its reed history, its site's survey and salinity that season, and soil cores "
            "published by then."
        ),
        split=(
            "Each of the nine seasons 2017-2025 is a test window, trained on every earlier season, as a model refit "
            "before each season predicts it at known stations."
        ),
        changes=(
            "We built one row per visit from the species list and joined the history, porewater and soil tables; "
            "visits whose plot was not measured leave as rows, among them 633 plots in dense reed the crews could "
            "only estimate from outside, whose estimate enters the next visit's history as its own column."
        ),
        fit="approximate",
        fit_reason=(
            "The rows and target are the program's own, but the source recommends an early warning without "
            "making a prediction, a manager acts on sites rather than 4 m^2 plots (plot and site-year RMSE rank "
            "eight models alike, Kendall tau 0.93), in the delta the reed is protected, not controlled, and CRMS "
            "does not tell the invasive lineage from the long-established noninvasive one."
        ),
    )

    # Dataset
    unique_name = "crms_phragmites_cover"
    year = "2026"  # PROV-9: a program that grows every season takes the year of the snapshot we pin
    domain = "environmental science & climate"
    source = "GOV Website"
    source_url = "https://www.lacoast.gov/crms2/"
    license = None  # none stated: the downloads carry CPRA's disclaimer and a RESTORE Council note only
    data_tags = ("Spatial",)
    download_description = """
        CPRA's bulk downloads from CIMS (Coastal Information Management System), regenerated as the program adds
        data and revises past records: the vegetation table of the zip dated 2026-10-25 (the same file as a copy of
        2026-10-18), the porewater and soil tables of 2026-11-01. A later download holds more seasons; `LAST_SEASON`
        pins 2025. SHA-256 of the three CSV files:
        CRMS_Marsh_Vegetation.csv 3cb2a0d3864263a5e697cc6966ea35bbe6ea0f86739078ef1388d4fa2cc919bd
        CRMS_Discrete_Hydrographic.csv 2408f6a2c91ab57d01912e02933ce7a5b8a45c402aca0f04470207483c019fe9
        CRMS_Soil_Properties.csv 0bf7f73b048c9c5c188c1a40ac08fa6942a4885aca82972627c772fa81deeb50

        mkdir -p local-data-warehouse/crms_phragmites_cover && cd local-data-warehouse/crms_phragmites_cover
        for t in CRMS_Marsh_Vegetation CRMS_Discrete_Hydrographic CRMS_Soil_Properties; do
            wget https://cims.coastal.la.gov/RequestedDownloads/ZippedFiles/$t.zip && unzip -o $t.zip && rm $t.zip
        done
    """
    bibtex = """
        @misc{cpra_crms_2026,
          author = {{Coastal Protection and Restoration Authority of Louisiana} and {U.S. Geological Survey}},
          title = {Coastwide Reference Monitoring System ({CRMS}): herbaceous marsh vegetation, discrete
                   hydrographic and soil properties data},
          year = {2026},
          howpublished = {\\url{https://cims.coastal.la.gov/}},
          note = {Bulk downloads CRMS\\_Marsh\\_Vegetation, CRMS\\_Discrete\\_Hydrographic and CRMS\\_Soil\\_Properties,
                  accessed 2026-10-30 and 2026-11-01}
        }
    """
    curation_comments = """
        We start with CRMS_Marsh_Vegetation.csv (594,288 species records of 75,418 plot visits at 4,619 stations of 401 sites, July 2006 to July 2026), CRMS_Discrete_Hydrographic.csv (porewater salinity) and CRMS_Soil_Properties.csv (soil cores) from CPRA's CIMS downloads.

        - Prediction point: before each survey season, once the last season is in CIMS. It arrives over the winter: in the archived CIMS downloads of 2021-2025 the previous season was 91-100% present by January-June, and the next season's first visits come in late May (no visit falls in January-April). A manager then has every survey up to the last season and forecasts each monitored station's reed cover at its visit next season, whose day is set by the station's usual window, not known exactly. Guo et al. 2026 (Ecological Applications, doi:10.1002/eap.70246; read from the USGS abstract only, the publisher answers 403) analyse these data "collected from 2006 to 2023 and spanning 390 sites across nine basins", find cover falling in the Mississippi River Delta and rising in four western and central basins, tied to soil nutrients, pH and salinity, and propose "a transferable monitoring template that integrates Phragmites cover trends (expanding/stable/declining), concurrently measured native plant cover, and key soil and pore-water indicators to flag emerging hotspots and prioritize adaptive management in other estuarine and deltaic systems"; they make no per-plot prediction. RMSE puts about 91% of its weight on the plots that already hold reed (8% of the test rows; random forest, nine windows) and a third of those lie in the delta, where the reed dies back and is protected, so the use case is the forecast of next season's cover for spread and die-back, not an early warning of new stands.
        - Row: one visit of a station in year Y with a measured plot and a measured visit of the same station in an earlier year (69,161 rows). The first visit of each station leaves: it has no survey to predict from (USE-7). The 60 station-years with two visits keep both, with the same history.
        - Target: `phragmites_cover_pct`, the summed in-plot cover of the rows whose currently recognised name starts with "Phragmites australis" (the species and two subspecies, one row per visit at most), 0 when the plot holds none. "<1" (9 reed records) and "Solitary" (3), cover below the sheets' 1% resolution, are 0.5. "Out" rows (reed seen near the plot) carry no cover by the metadata ("no estimates of cover are made for occurrences of a species outside of the sample plot"), so they count as 0 in the target and as a flag in the features.
        - Zeros: 94.1% of the rows. Structural absence dominates: in 56,208 rows the station had never seen reed in or near its plot and its site had no reed in or near its plots the season before, and 0.02% of them have reed (13 visits); when the plot had none but reed grew near it, 18.7% of 1,709 visits had reed in the plot. The zeros stay as the program records them (coded zeros are no obstacle; policy question 2 of the zero-inflated review, 2026-10-30).
        - Dropped as rows, the plots inside dense reed stands: 633 visits (2012-2016; 171 stations at 32 sites, among them CRMS0139 and CRMS0153-0163 in the Mississippi River Delta and CRMS2614, 2634, 4407, 4448 and 4626) have no measured plot (`% Cover Total` missing) and record reed only as seen outside it. Their comments explain "This station is in a dense stand of Phragmites australis that is difficult to access so cover was estimated" and give the crew's estimate ("Phragmites cover was estimated to be 100%" for 584; 70-95% for 48; 10% once), "based on an evaluation of the vegetation surrounding the plot and previous year's data", which "may not be representative". The program first published them as in-plot cover (518 of them in the archived download of November 2016, mean 98.7%) and has since moved them to "Out" with the cover fields empty (by the download of April 2021), so today's table holds no target for them and we invent none (CLEAN-15). Whether the estimates overstate is not shown: the nearest earlier measurement of the same plot averages 73.9% (median 80), and the lower covers from 2017 follow the roseau cane scale die-back ("scale present" in 95 visit comments of 2017, none before; the third decision). Their history stays: `dense_stand_since_previous` says that a visit after the latest measured one found the plot in such a stand, `dense_stand_estimate_pct` carries the crew's latest estimate there (108 rows of 106 stations, 89 of them in 2017), and the visits count in `site_share_phragmites_nearby`, as each recorded reed near the plot. `previous_phragmites_cover` stays the latest measured cover (often 2011, so `days_since_previous_visit` is long). The cost: reed is rarer among the rows of 2012-2016 (3.2-3.6% of the visits, against 6.0-7.3% with the estimates counted, 3.3-5.7% in 2007-2011 and 5.9-9.2% from 2017, when the plots were entered again), all in seasons every window trains on.
        - Dropped visits without a measured plot and without an estimate (325): not surveyed (no access in 2023, hunters, water depth, Cicuta) or an open-water plot noted only in the comment. The 2,586 visits with a total cover of 0 (open water or bare plots; 2,542 without a species in the plot) stay, with reed cover 0.
        - Dropped the 2026 visits (677, June-July only): the newest season is incomplete, so `LAST_SEASON` is 2025.
        - Features from the station's latest visit in an earlier year (`previous_*`): marsh type, total and layer covers, the dominant height and the height of each layer, the number of species in the plot, the reed cover, whether reed grew in or near the plot, and the porewater salinity measured at the station that day (mean of 10 and 30 cm; 74% of the rows). Blank layer covers and heights mean not recorded (a blank tree cover even under 6-30 m swamp canopies) and stay missing. The visit's own covers, heights, species and marsh type are co-measurements of the target (the marsh type is assigned per visit: 2,504 stations change type over time) and are not shipped.
        - Features from the station's history before the season: the highest reed cover, the number of earlier seasons with reed in the plot (`visits_with_phragmites_before` counts station-years, the latest visit of each), and whether reed was ever seen near it; and from its site in the season of that latest visit: the mean reed cover, the share of stations with reed in the plot and the share with reed in or near it, and the mean and highest porewater salinity of all the site's readings (porewater stations sampled through the year and vegetation stations).
        - Soil: for each soil variable on its own, the site's latest cores sampled three seasons before the visit's season or earlier, means over the top 24 cm of pH, salinity, bulk density, organic matter, total nitrogen and total phosphorus, the soil indicators the source names. The lag is when CIMS has them: in the archived downloads the cores of 2019-2021 reached CIMS 1 to 2.5 years after sampling, and the lag costs nothing measurable (mean window RMSE 7.050 without it, 7.054 with it; split audit). Joined per variable because pH and salinity were analysed only in the 2006-2015 cores and nitrogen and phosphorus only in 2016-2021: pH and salinity reach 85% of the rows (99.7% from 2017), bulk density and organic matter 85%, nitrogen and phosphorus 12% (none before 2019); missing stays missing.
        - Set missing, values their own records contradict (CLEAN-11): one herb height of 1,219.2 cm (40 ft) under a dominant height of 61 cm (the next highest is 549 cm), and three porewater salinities above 50 ppt (90, 71 and 57 ppt) whose specific conductance gives about 12.6, 7.1 and 5.8 ppt (porewater runs 0.35-0.66 ppt per mS/cm, 1st-99th percentile). The species count leaves out "Bare Ground" and "Water", which the 2006 species list entered as species (1,670 in-plot records).
        - TP-10, which tells a tabular task from forecasting, on the nine shipped windows (untuned models; RMSE averaged over the windows; 2026-11-01): the random forest scores 6.97 and LightGBM 7.03 (7.08 without the porewater and soil features, 7.84 without the station's own reed history), the training mean 13.9. Forecasts from the station's own reed series with nothing fitted: its last cover carried forward scores 7.75 (the random forest 10.0% lower, in 9 of 9 windows), and the best of nine per-station forecasts, an exponentially weighted mean (weight 0.7, picked on the test windows), 7.40 (5.8% lower, 8 of 9; mean paired gain 3.2 standard errors over the windows). Curves of the last cover fitted on the training seasons: a linear shrinkage 7.51 (7.2% lower, 9 of 9), a two-regime rule (0.08 where the last cover was 0, else 16 + 0.62 x the last cover; three numbers, nearly the same in every window) 7.05 (1.1%, 5 of 9, 0.9 standard errors) and an isotonic curve 7.04 (1.0%, 6 of 9; LightGBM 0.2%, 4 of 9). So leg 1 holds against the station's unfitted forecasts and not clearly against a fitted curve of its last cover; which of them is the bar is the curator's call. Leg 2 holds: every feature is known at the prediction point, and the target enters only as the last observation and trailing summaries of the station's series (its running maximum and count, and the site mean that includes the station).
        - Note: the previous reed cover is the core of the task. Alone, as a fitted curve, it reaches 98% of the best untuned family's skill (task probes on the nine windows: skill 0.731 against 0.744 for the random forest, flag `one_feature`; leak probes on three: a depth-2 tree R^2 0.752 against 0.748 for LightGBM on all features), as last season's cover is the first thing a manager reads; the raw carried-forward value loses to the models (above), so the task is not `Trivial` by TP-4.
        - Dropped: the station and site ids (the history features carry what is known of the station), the survey crew, organisation and comments (read for the estimates only), the scientific and common names as recognised and as first observed (one target species), the additional species description (a free-text note per species record, such as "shrub" or "Stressed."), the Braun-Blanquet rank (a recoding of `% Cover`: for reed, the target in another form), Group (blank in all but 161 of the 594,288 records), the plot size (4 m^2 everywhere), the sample and vegetation types (transects of natural vegetation in 99.9% of the records) and the planting counts (24 records, all 0).
        - Note: CRMS does not tell the lineages apart. Guo et al. 2026 (USGS abstract): "Louisiana supports both long-established noninvasive and (since ~2000) invasive European P. australis lineages", "but CRMS cannot distinguish them"; 15 of the 7,064 reed records name a subspecies. So the target is the cover of the species.
        - Note: the date of the visit is a feature, as the visits follow a yearly schedule (brackish and saline marshes first): its season and window are known before the season, the exact day is not, and its day-of-year pattern follows the mix of stations, not the outcome. The station's position is a feature too.
    """

    accepted_check_warnings = {
        "meta_time_horizon_mismatch": (
            "Each test window is one survey season of a calendar year (visits in May-December, 97% in "
            "June-September), so its span reads 99-203 days against the one-year horizon; the windows are calendar "
            "years (as zillow_prize and perth_house_prices)."
        ),
        "meta_license_unknown": (
            "CPRA's downloads state no licence, only its disclaimer (\"The originator makes no claims as to the data's "
            'suitability for other purposes") and a RESTORE Council note; no other licence is known (as diabetes_3 '
            "and mobile_churn)."
        ),
        "task_target_value_dominant": (
            "Zero-inflated by nature: reed covers none of the plot in 94% of the visits, 95.9% of them at stations "
            "that never had reed in or near the plot; the absence the program records, not a cap or a placeholder "
            '(Andrej, policy question 2 of the zero-inflated review, 2026-10-30: "We want to add any relevant '
            'predictive task, independent if it is zero inflated or not").'
        ),
    }

    # Task
    target = "phragmites_cover_pct"
    problem_type = "regression"
    metric = Metric.fallback(
        reason=(
            "No source metric: Guo et al. 2026 classify basin trends and relate cover to soil and porewater (USGS "
            "abstract; the full text was not reachable), and the CRMS pages and metadata define no prediction or "
            "score; RMSE on percent cover scores the forecast of next season's cover the use case names, and plot "
            "and site-year RMSE rank models alike"
        ),
    )

    # Splits: one window per survey season, the newest nine.
    temporal = Temporal(on="visit_date", splits=TemporalSplits(window=1, unit="years", n_windows=9))
    splits_comment = """
        Expanding-window temporal splits by survey season: the nine calendar years 2025 back to 2017 are the test
        windows (3,578-3,830 visits each), newest first, each trained on every visit of the earlier seasons (the 2017
        window on 51% of the rows). One season is the horizon: the network surveys once a year, and a model refit
        before a season predicts it. No gap, measured: in the archived CIMS downloads of 2021-2025 the previous season
        was 91-100% present by January-June, before the next season's first visits in late May, and so was its
        porewater (99.5-100%). The features of a test row come from earlier seasons only, the soil from cores sampled
        three seasons back or earlier, as CIMS posts soil analyses 1 to 2.5 years after sampling. The reed covers of
        2019-2023 are unchanged since first publication; those of the 2012-2016 dense-stand visits are not (in-plot
        cover in the download of November 2016, "Out" with empty cover by April 2021), so a manager predicting 2017
        read those estimates as data, which the rows carry as `dense_stand_estimate_pct`. The 2017 window holds 89
        plots measured again after the crews could not enter them in 2012-2016; they carry two thirds of its squared
        error (67% for the random forest), and without that window the random forest's margin over a fitted curve of
        the last cover falls from 1.0% to 0.7%. All nine windows stay (one atypical window of nine). Stations recur
        across the windows on purpose: the use case predicts for stations already monitored (USE-10).
    """

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        hydro_columns = [
            "CPRA Station ID",
            "Date (mm/dd/yyyy)",
            "Soil Porewater Specific Conductance (uS/cm)",
            "Soil Porewater Salinity (ppt)",
        ]
        soil_columns = ["Station ID", "Sample Date (mm/dd/yyyy)", "Sample Depth (cm)", *SOIL_COLUMNS]
        return {
            "vegetation": pd.read_csv(
                raw_dir / VEGETATION_FILE, encoding="latin-1", usecols=list(VEGETATION_COLUMNS), dtype=str
            ),
            "porewater": pd.read_csv(raw_dir / POREWATER_FILE, encoding="latin-1", usecols=hydro_columns),
            "soil": pd.read_csv(raw_dir / SOIL_FILE, encoding="latin-1", usecols=soil_columns),
        }

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        veg = raw["vegetation"].copy()
        # 0. Read as text; the columns without trace codes are plain numbers ("<1" only occurs in the three covers
        #    `_visits` converts).
        for col, name in VEGETATION_COLUMNS.items():
            if name in NUMERIC_VISIT_COLUMNS:
                veg[col] = pd.to_numeric(veg[col], errors="raise")

        # 1. One row per station visit; the reed cover is the target. A herb height no herb layer reaches is missing.
        visits = _visits(veg)
        visits["site"] = _site(visits["station"])
        visits["year"] = visits["date"].dt.year.astype("int64")
        visits["height_herb_cm"] = visits["height_herb_cm"].mask(visits["height_herb_cm"] > HERB_HEIGHT_MAX_CM)
        # 2. Visits without a measured plot leave as rows: not surveyed, or a plot inside a dense reed stand the crew
        #    could not enter (633 visits, 2012-2016; `_decisions`), whose comment holds the crew's estimate. Those keep
        #    a place in the history (steps 5 and 6). The incomplete newest season leaves too.
        estimate = pd.to_numeric(visits["comment"].str.extract(ESTIMATE_PATTERN)[0], errors="coerce")
        dense = visits[visits["cover_total"].isna() & estimate.notna() & (visits["year"] <= LAST_SEASON)].copy()
        dense["dense_stand_estimate_pct"] = estimate[dense.index].astype("float64")
        visits = visits[visits["cover_total"].notna() & (visits["year"] <= LAST_SEASON)].copy()

        # 3. Porewater salinity of each station visit (mean over the 10 and 30 cm readings of that day).
        pw = _porewater(raw["porewater"])
        station_pw = pw.groupby(["station", "date"], sort=True)["salinity"].mean().rename("porewater_salinity_ppt")
        visits = visits.merge(station_pw.reset_index(), on=["station", "date"], how="left")

        # 4. The station's latest visit of each year, with its history up to then.
        last = visits.sort_values(["station", "date"], kind="stable").groupby(["station", "year"], sort=True).tail(1)
        last = last[["station", "year", "date", *PREVIOUS]].reset_index(drop=True)
        by_station = last.groupby("station", sort=True)
        last["highest_phragmites_cover_before"] = by_station["phragmites_cover"].cummax()
        last["visits_with_phragmites_before"] = (
            last["phragmites_cover"].gt(0).astype(int).groupby(last["station"]).cumsum()
        )
        last["phragmites_nearby_before"] = by_station["phragmites_nearby"].cummax()
        history = last.rename(columns={c: f"previous_{c}" for c in [*PREVIOUS, "date", "year"]})
        history["next_year"] = (history["previous_year"] + 1).astype("int64")

        # 5. Each visit of year Y takes the station's latest visit of a year before Y (merge_asof by station).
        visits = visits.sort_values(["year", "station", "date"], kind="stable")
        history = history.sort_values(["next_year", "station"], kind="stable")
        df = pd.merge_asof(visits, history, left_on="year", right_on="next_year", by="station", direction="backward")
        df = df[df["previous_year"].notna()].copy()
        for col in ("previous_year", "previous_species_count", "visits_with_phragmites_before"):
            df[col] = df[col].astype("int64")  # the merge made them float; every kept row has a history
        df["days_since_previous_visit"] = (df["date"] - df["previous_date"]).dt.days

        # 5b. The station's latest unentered dense-stand visit of a year before Y, when it came after the latest
        #     measured visit: a flag and the crew's estimate; `previous_phragmites_cover` stays the measured one.
        dense_history = dense[["station", "date", "dense_stand_estimate_pct"]].rename(columns={"date": "dense_date"})
        dense_history["dense_next_year"] = (dense_history["dense_date"].dt.year + 1).astype("int64")
        dense_history = (
            dense_history.sort_values(["station", "dense_date"], kind="stable")
            .groupby(["station", "dense_next_year"], sort=True)
            .tail(1)
            .sort_values(["dense_next_year", "station"], kind="stable")
        )
        df = pd.merge_asof(
            df.sort_values(["year", "station", "date"], kind="stable"),
            dense_history,
            left_on="year",
            right_on="dense_next_year",
            by="station",
            direction="backward",
        )
        since_previous = df["dense_date"].gt(df["previous_date"])
        df["dense_stand_since_previous"] = since_previous.astype(int)
        df["dense_stand_estimate_pct"] = df["dense_stand_estimate_pct"].where(since_previous)

        # 6. The site in the season of that latest visit: its stations' reed, and all its porewater readings. The
        #    share with reed near the plot counts the dense-stand visits too (each recorded reed outside the plot).
        site = visits.groupby(["site", "year"], sort=True).agg(
            site_phragmites_cover_mean=("phragmites_cover", "mean"),
            site_share_with_phragmites=("phragmites_cover", lambda s: float((s > 0).mean())),
        )
        nearby = pd.concat(
            [visits[["site", "year", "phragmites_nearby"]], dense[["site", "year", "phragmites_nearby"]]]
        )
        site_nearby = nearby.groupby(["site", "year"], sort=True)["phragmites_nearby"].mean()
        site_pw = pw.groupby(["site", "year"], sort=True)["salinity"].agg(
            site_porewater_salinity_mean_ppt="mean", site_porewater_salinity_max_ppt="max"
        )
        site = (
            site.join(site_nearby.rename("site_share_phragmites_nearby"), how="left")
            .join(site_pw, how="left")
            .reset_index()
            .rename(columns={"year": "previous_year"})
        )
        df = df.merge(site, on=["site", "previous_year"], how="left")

        # 7. The site's soil cores published before the season: per soil variable (pH and salinity were analysed in
        #    the 2006-2015 cores, nitrogen and phosphorus in 2016-2021), the latest cores sampled three seasons back or
        #    earlier (merge_asof by site).
        soil = _soil(raw["soil"])
        df["soil_season"] = (df["year"] - SOIL_LAG_SEASONS).astype("int64")
        for col in SOIL_COLUMNS.values():
            one = soil.loc[soil[col].notna(), ["site", "soil_year", col]].sort_values(
                ["soil_year", "site"], kind="stable"
            )
            df = pd.merge_asof(
                df.sort_values(["soil_season", "site", "station", "date"], kind="stable"),
                one,
                left_on="soil_season",
                right_on="soil_year",
                by="site",
                direction="backward",
            ).drop(columns="soil_year")

        # 8. Readable flags; the target and the time column get their names.
        for col in ("previous_phragmites_nearby", "phragmites_nearby_before", "dense_stand_since_previous"):
            df[col] = df[col].map({1: "yes", 0: "no"})
        df = df.rename(columns={"phragmites_cover": self.target, "date": "visit_date"})
        keep = [
            "visit_date",
            "latitude",
            "longitude",
            "days_since_previous_visit",
            *[f"previous_{c}" for c in PREVIOUS],
            "highest_phragmites_cover_before",
            "visits_with_phragmites_before",
            "phragmites_nearby_before",
            "dense_stand_since_previous",
            "dense_stand_estimate_pct",
            "site_phragmites_cover_mean",
            "site_share_with_phragmites",
            "site_share_phragmites_nearby",
            "site_porewater_salinity_mean_ppt",
            "site_porewater_salinity_max_ppt",
            *SOIL_COLUMNS.values(),
            self.target,
        ]
        return df[keep]

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "previous_community",
                "previous_phragmites_nearby",
                "phragmites_nearby_before",
                "dense_stand_since_previous",
            ],
            datetime=["visit_date"],
        )

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        y = df[self.target]
        before = np.select(
            [
                df["previous_phragmites_cover"] > 0,
                df["previous_phragmites_nearby"].eq("yes"),
                df["highest_phragmites_cover_before"].gt(0) | df["phragmites_nearby_before"].eq("yes"),
                df["site_share_phragmites_nearby"].gt(0) | df["site_share_with_phragmites"].gt(0),
            ],
            [
                "1. reed in the plot at the latest visit",
                "2. none in the plot, reed near it",
                "3. reed earlier at the station, not at the latest visit",
                "4. never at the station, at its site",
            ],
            default="5. never at the station or near its site's plots",
        )
        zeros = (
            pd.DataFrame({"before": before, "with_reed": y.gt(0), "cover": y})
            .groupby("before")
            .agg(rows=("cover", "size"), share_with_reed=("with_reed", "mean"), mean_cover=("cover", "mean"))
            .round(4)
        )
        seasons = (
            df.assign(
                season=df["visit_date"].dt.year,
                with_reed=y.gt(0),
                carried_error=(y - df["previous_phragmites_cover"]) ** 2,
            )
            .groupby("season")
            .agg(
                rows=(self.target, "size"),
                share_with_reed=("with_reed", "mean"),
                mean_cover=(self.target, "mean"),
                p99_cover=(self.target, lambda s: s.quantile(0.99)),
                rmse_carried_forward=("carried_error", lambda s: float(np.sqrt(s.mean()))),
            )
            .round(3)
        )
        # The unmeasured plots: per season, how many, how many with a reed estimate in the comment, the measured reed
        # cover of the stations that have such estimates, and the visits whose comment notes the roseau cane scale.
        veg = raw["vegetation"].rename(columns=VEGETATION_COLUMNS)
        per_visit = veg.groupby(["station", "date"], sort=True).agg(
            cover_total=("cover_total", "first"), comment=("comment", "first")
        )
        reed = veg[veg["species"].astype("string").str.startswith(PHRAGMITES).fillna(False).astype(bool)]
        reed = reed[reed["in_out"].isin(["In", "Both"])]
        reed_cover = (
            pd.to_numeric(reed["cover"].replace(TRACE_COVER), errors="coerce")
            .groupby([reed["station"], reed["date"]])
            .sum()
        )
        per_visit = per_visit.join(reed_cover.rename("reed"), how="left").reset_index()
        per_visit["season"] = pd.to_datetime(per_visit["date"], format="%m/%d/%Y").dt.year
        per_visit["estimate"] = pd.to_numeric(per_visit["comment"].str.extract(ESTIMATE_PATTERN)[0], errors="coerce")
        scale = per_visit["comment"].str.contains("scale present", case=False, na=False)
        unmeasured = per_visit["cover_total"].isna()
        estimated = unmeasured & per_visit["estimate"].notna()
        stations = set(per_visit.loc[estimated, "station"])
        measured_there = per_visit[~unmeasured & per_visit["station"].isin(stations)]
        plots = (
            pd.DataFrame(
                {
                    "unmeasured_visits": unmeasured.groupby(per_visit["season"]).sum(),
                    "with_reed_estimate": estimated.groupby(per_visit["season"]).sum(),
                    "median_estimate": per_visit[estimated].groupby("season")["estimate"].median(),
                    "measured_visits_at_those_stations": measured_there.groupby("season").size(),
                    "their_mean_measured_reed_cover": measured_there["reed"]
                    .fillna(0)
                    .groupby(measured_there["season"])
                    .mean(),
                    "visits_noting_scale_present": scale.groupby(per_visit["season"]).sum(),
                }
            )
            .fillna({"unmeasured_visits": 0, "with_reed_estimate": 0, "visits_noting_scale_present": 0})
            .round(1)
        )
        return [
            Decision(
                title="Zeros by what the station showed before",
                why=(
                    "The 94% zeros are mostly structural: a station that never had reed near it, at a site without "
                    "reed nearby, almost never gains it in a year, while a plot with reed next to it often does."
                ),
                evidence=zeros,
            ),
            Decision(
                title="The target by survey season",
                why=(
                    "The test windows are seasons; the share of plots with reed and its level drift slowly. The "
                    "last column scores the previous survey's reed cover carried forward (RMSE), the raw forecast "
                    "TP-4 compares against; the fitted forecasts TP-10 weighs are in the notes."
                ),
                evidence=seasons,
            ),
            Decision(
                title="Plots without a measurement leave as rows",
                why=(
                    "From 2012 to 2016 the crews could not enter 633 plots in dense reed and wrote an estimate (mostly "
                    "100%) into the comment. The program first entered them as in-plot cover and has since moved them "
                    "to 'Out' with the cover fields empty (its comments: the estimate 'may not be representative'), so "
                    "they hold no target. Their history enters the next measured visit as a flag and the estimate, not "
                    "as the previous cover. The lower measured cover from 2017 follows the roseau cane scale die-back "
                    "(last column). Seasons 2006-2026 of the download."
                ),
                evidence=plots,
            ),
        ]
