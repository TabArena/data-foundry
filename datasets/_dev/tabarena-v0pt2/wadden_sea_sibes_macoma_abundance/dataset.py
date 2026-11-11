"""Curated dataset definition for `wadden_sea_sibes_macoma_abundance` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import scipy.io
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Grouping,
    Metric,
    ScoringColumn,
    Source,
    TaskSummary,
    drop_columns,
)
from scipy.spatial import cKDTree

MACOMA_SIBES_ID = 59  # Macoma balthica in species.csv (sibes_id 59, aphia_id 880017)
TELLINOIDEA_SIBES_ID = 339  # tellinoids below 3 mm, Macoma balthica included (species.csv remark)
SEDIMENT = ["median_grain_size", "percentage_mud"]
NEIGHBOURS = 8  # other stations of the survey year the sediment is interpolated from
METRES_PER_DEGREE = np.array([66_700.0, 111_200.0])  # longitude and latitude at 53.3 N
VAKLODINGEN_RELEASE = b"vaklodingen_release20260303"  # the `id` of the 40 Rijkswaterstaat tiles downloaded
VAKLODINGEN_TILES = [
    "122_2120",
    "122_2322",
    "123_1716",
    "123_1918",
    "123_2120",
    "123_2322",
    "124_1514",
    "124_1716",
    "124_1918",
    "124_2120",
    "125_1514",
    "125_1716",
    "125_1918",
    "126_1312",
    "126_1514",
    "126_1716",
    "126_1918",
    "127_1312",
    "127_1514",
    "127_1716",
    "128_1312",
    "128_1514",
    "129_1312",
    "129_1514",
    "130_1312",
    "131_1312",
    "132_1110",
    "132_1312",
    "133_1110",
    "133_1312",
    "134_1110",
    "134_1312",
    "135_1110",
    "135_1312",
    "136_1312",
    "136_1514",
    "137_1514",
    "137_1716",
    "138_1514",
    "138_1716",
]


def station_elevation_series(tile_dir: Path, stations: pd.DataFrame) -> pd.DataFrame:
    """Every vaklodingen survey of the 20 m cell that holds each station: one row per station and survey.

    Args:
        tile_dir: Folder with the downloaded `vaklodingenKB<tile>.nc` files (netCDF 3).
        stations: One row per `sampling_station_id` with its `x` (longitude) and `y` (latitude).

    Returns:
        Columns `sampling_station_id`, `survey` (the survey's date stamp, mostly a nominal 1 January of the survey
        year, from the source's file names) and `elevation_m_nap` (metres above NAP), from the cell whose centre lies
        within 15 m of the station (a cell is 20 m wide).
    """
    out = []
    for tile in VAKLODINGEN_TILES:
        nc = scipy.io.netcdf_file(tile_dir / f"vaklodingenKB{tile}.nc", "r", mmap=False)
        assert nc._attributes["id"] == VAKLODINGEN_RELEASE, nc._attributes["id"]
        var = nc.variables
        cells = np.c_[var["lon"].data.ravel(), var["lat"].data.ravel()] * 1e-7 * METRES_PER_DEGREE
        dist, cell = cKDTree(cells).query(stations[["x", "y"]].to_numpy() * METRES_PER_DEGREE)
        inside = dist < 15.0
        z = var["z"].data.reshape(var["z"].data.shape[0], -1)[:, cell[inside]].astype(float)
        z[np.abs(z) > 1e30] = np.nan  # the fill value: the cell was not surveyed that time
        survey = pd.to_datetime(var["time"].data.astype(float), unit="D")
        nc.close()
        frame = pd.DataFrame(z, index=survey, columns=stations["sampling_station_id"].to_numpy()[inside])
        # dropna: pandas 3's stack() keeps the unsurveyed (NaN) cells that pandas 2's dropped, and merge_asof in
        # _clean would then take an unsurveyed survey as the latest one (40.7% of the samples without elevation)
        out.append(frame.stack().dropna().rename("elevation_m_nap").rename_axis(["survey", "sampling_station_id"]))
    series = pd.concat(out).reset_index()
    return series.groupby(["sampling_station_id", "survey"], as_index=False)["elevation_m_nap"].mean()


def interpolate_sediment(samples: pd.DataFrame) -> pd.DataFrame:
    """Sediment at each sample from the 8 nearest other stations of its survey year, by inverse squared distance.

    The station itself is never a source, a station sampled twice in a year counts once (its mean), samples without
    sediment are no source, and distances below 50 m count as 50 m.
    """
    out = pd.DataFrame(np.nan, index=samples.index, columns=SEDIMENT)
    for _, rows in samples.groupby(samples["date"].str[:4]):
        src = rows.dropna(subset=SEDIMENT).groupby("sampling_station_id")[["x", "y", *SEDIMENT]].mean()
        tree = cKDTree(src[["x", "y"]].to_numpy() * METRES_PER_DEGREE)
        dist, idx = tree.query(rows[["x", "y"]].to_numpy() * METRES_PER_DEGREE, k=NEIGHBOURS + 1)
        own = src.index.to_numpy()[idx] == rows["sampling_station_id"].to_numpy()[:, None]
        weight = 1.0 / np.maximum(dist, 50.0) ** 2
        weight[own] = 0.0
        weight[~own.any(axis=1), NEIGHBOURS] = 0.0  # the station has no sediment of its own: the 8 nearest
        values = src[SEDIMENT].to_numpy()[idx]
        out.loc[rows.index] = (weight[..., None] * values).sum(axis=1) / weight.sum(axis=1, keepdims=True)
    return out


class WaddenSeaSibesMacomaAbundance(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "How many Baltic tellins (Macoma balthica, a small clam) live per square metre at a place on the Dutch "
            "Wadden Sea mudflats that was not sampled, in a survey year already run?"
        ),
        use_case=(
            "An ecologist or a Wadden Sea manager draws the abundance map of a past survey: the density of this key "
            "shorebird prey over the intertidal flats between the survey's stations, which the source maps for "
            "habitat-directive, quality-status and impact assessments; no source names a decision taken on the map."
        ),
        row=(
            "One fauna sample (one core on foot, two cores bulked from a boat, a single boat core in 39 samples) at "
            "one SIBES survey station on one day, June to October 2008-2022 (59,044 samples at 5,092 stations of "
            "the NIOZ survey, most of them sampled in 13-15 of the 15 years)."
        ),
        predicted=(
            "The number of Baltic tellins per square metre found in the sample, shipped on a log scale (log1p) and "
            "scored on the density itself. 56.0% of the samples hold none."
        ),
        known=(
            "The position, its tidal basin and named flat, the survey's date, the sediment's median grain size and "
            "mud content interpolated from the nearest other stations of that year's survey, and the flat's "
            "elevation from Rijkswaterstaat's latest depth survey of the place."
        ),
        split=(
            "Whole stations are held out with all their years, so a test station stands for a place between the "
            "stations of a survey already run; its neighbours about 500 m away, the same year's survey and the later "
            "surveys are in training, as for a map of a past survey drawn from the whole archive."
        ),
        changes=(
            "We built the zeros from the sample list, interpolated the sediment from neighbouring stations, joined "
            "the elevation from Rijkswaterstaat's depth surveys, dropped the 2008 samples without any fauna record "
            "(0.6%) and those with unidentified tellinoid spat (0.1%), and left out how a sample was taken (by boat "
            "or on foot, core area, grid or random station)."
        ),
        fit="approximate",
        fit_reason="The decision the map serves is not named.",
    )

    # Dataset
    unique_name = "wadden_sea_sibes_macoma_abundance"
    domain = "biology & life sciences"
    sources = (
        Source(
            role="publication",
            platform="Other",  # NIOZ's data repository (DAS), the first publication of the survey data
            url="https://doi.org/10.25850/nioz/7b.b.ug",
            license="CC BY-SA 4.0",  # stated on the NIOZ dataset page
            year="2024",  # a yearly growing release: the year of the pinned snapshot, version 6 of 2024-12-21 (PROV-9)
            bibtex="""
                @misc{bijleveld2024sibes,
                  title = {{SIBES} dataset, version 6},
                  author = {Bijleveld, Allert Imre and Tacoma, Marten and Koolhaas, Anita},
                  year = {2024},
                  publisher = {NIOZ Royal Netherlands Institute for Sea Research},
                  doi = {10.25850/nioz/7b.b.ug},
                  howpublished = {\\url{https://doi.org/10.25850/nioz/7b.b.ug}},
                  note = {Data descriptor: Bijleveld et al. (2025), SIBES: Long-term and large-scale monitoring of intertidal macrozoobenthos and sediment in the Dutch Wadden Sea, Scientific Data 12:239, doi:10.1038/s41597-025-04540-9}
                }
                @misc{rijkswaterstaat2026vaklodingen,
                  title = {Vaklodingen: bathymetry and topography measurements along the {D}utch coast},
                  author = {{Rijkswaterstaat}},
                  year = {2026},
                  publisher = {Deltares OpenEarth},
                  howpublished = {\\url{https://opendap.deltares.nl/thredds/catalog/opendap/rijkswaterstaat/vaklodingen/catalog.html}},
                  note = {Release vaklodingen\\_release20260303}
                }
            """,
        ),
    )
    data_tags = ("Spatial",)
    download_description = """
        We download version 6 (published 2024-12-21) of the SIBES dataset from the NIOZ data repository (doi:10.25850/nioz/7b.b.ug). The repository replaces the files with each yearly release (the newest three years stay embargoed), so a later download holds more years than these 2008-2022.
        mkdir -p local-data-warehouse/wadden_sea_sibes_macoma_abundance && cd local-data-warehouse/wadden_sea_sibes_macoma_abundance
        B=https://doi.nioz.nl/dataset/95a5d109-1c31-4f1c-b6af-e0ef3892d83b/resource
        curl -L -o samples.csv $B/fb62c1db-4f16-4753-a5ce-6f48f3dcbf7c/download/samples.csv
        curl -L -o biota.csv $B/21c5c418-0165-4361-b65b-a59877897677/download/biota.csv
        curl -L -o species.csv $B/5de9ee94-8025-4dd7-b462-b4b937ae0068/download/species.csv
        Version 6 has sha256 2d5faefe... (samples.csv), 8d762310... (biota.csv) and 067bcbf2... (species.csv); other sums mean a newer release.
        The elevation comes from Rijkswaterstaat's vaklodingen (bathymetry and topography of the Dutch coast and Wadden Sea on a 20 m grid, one survey of each area every few years), as the 40 netCDF tiles that hold the stations, from Deltares' OpenEarth THREDDS server (release `vaklodingen_release20260303`, about 2.9 GB; no login). The netCDF files state "can be used freely for research purposes provided that the following source is acknowledged: Rijkswaterstaat"; data.overheid.nl lists Rijkswaterstaat's bathymetry under CC0 1.0.
        mkdir -p vaklodingen && cd vaklodingen
        V=https://opendap.deltares.nl/thredds/fileServer/opendap/rijkswaterstaat/vaklodingen
        for t in 122_2120 122_2322 123_1716 123_1918 123_2120 123_2322 124_1514 124_1716 124_1918 124_2120 125_1514 125_1716 125_1918 126_1312 126_1514 126_1716 126_1918 127_1312 127_1514 127_1716 128_1312 128_1514 129_1312 129_1514 130_1312 131_1312 132_1110 132_1312 133_1110 133_1312 134_1110 134_1312 135_1110 135_1312 136_1312 136_1514 137_1514 137_1716 138_1514 138_1716; do curl -L -o vaklodingenKB$t.nc $V/vaklodingenKB$t.nc; done
        The sha256 of the 40 sums (`sha256sum *.nc | sha256sum`) is 3935cf21...; the definition asserts the release id of every tile.
    """
    curation_comments = """
        We start with samples.csv and biota.csv of the SIBES dataset, version 6 (NIOZ, 2024-12-21): 59,463 core samples from 2008-2022 at 5,105 stations of the Dutch Wadden Sea flats.

        - Prediction point: a place on the flats between the stations of a survey already run, for the source's map of that year (the model was used "to make predictions for sites where only environmental data are available", Lyashevska et al. 2016, Abstract). Known then are the position, tidal basin and flat, the survey's date (each area is sampled "during the same period each year", descriptor; a test sample given the day of the nearest training station of its year scores the same, R^2 within 0.001), the sediment from a map, as "the covariate must be known everywhere in the study area" (Lyashevska et al., Materials and Methods), and the elevation, the paper's third covariate, which the release does not hold.
        - Sediment: the grain size and mud content measured in a jar at the visit, just before the fauna core, are replaced by values interpolated from the 8 nearest other stations of the same survey year, weighted by 1/distance^2 (below 50 m counted as 50 m). The measured values scored R^2 0.012-0.018 higher on log1p in three untuned model families (9 of 9 shipped folds), a gain a place without a sample cannot have (USE-3). The interpolated values (correlation 0.82 for mud, 0.88 for grain size with the measured ones) still help a smooth model (+0.035 R^2 for a spline ridge over no sediment), so they replace the columns rather than leave (LEAK-7, CLEAN-19), and they fill 2008, when sediment was taken on a 1000-m grid (measured in 747 of the 3,450 kept 2008 samples).
        - Elevation (CC 2026-11-02, Andrej: "Join it if it is available"): `elevation_m_nap`, metres above NAP (about mean sea level), of the 20 m cell that holds the station in the latest Rijkswaterstaat vaklodingen survey whose date stamp (mostly a nominal 1 January of the survey year, from the source's file names) is on or before the sample's date (median 2.7 years earlier, 98.0% within 6 years; 5 samples have no earlier survey and stay missing). 19.3% of the samples take a survey stamped 1 January of their own year, which may have been made after the sample; that stays, as the bed is not set by the tellins and the map of a past survey is drawn from the whole archive, later surveys included (splits comment). Elevation sets how long a flat lies dry and is, with mud, a main factor of tellin habitat; a map maker has it for every place. It is a separate survey of the bed, not of the visit, so it exists at an unsampled place (USE-3). Untuned LightGBM R^2 on log1p 0.343 to 0.376 (+0.033, 9 of 9 shipped folds), a spline ridge 0.210 to 0.293, and RMSE on the density 872.8 to 863.9 (lower in 9 of 9).
        - Target: Macoma balthica (sibes_id 59), the paper's species, in individuals per m2. biota.csv lists only taxa present, "Zero values can be obtained by combining the files 'biota.csv' and 'samples.csv'" (Bijleveld et al. 2025, Table 4): a zero is no tellin in the sample (56.0%). Shipped as log1p, scored on the density (`target_transform="log1p"`). Numbers, not biomass: numbers are the paper's quantity, and the release holds biomass per taxon and sample but no size classes, so the part a bird can eat cannot be built.
        - 769 samples have no fauna record of any taxon: empty cores, or fauna never entered. The descriptor's Table 1 counts them among the processed samples (its yearly counts equal the samples.csv rows) and says an unprocessed sample "did not lead to an entry in the database". 342 are from 2008, 9.0% of that year against 0.2-1.5% in each later year, at stations empty on 2.8% of their 2009-2022 visits (0.77% for all samples of those years): dropped, located by the year, not by the core (LEAK-25). The 427 of 2009-2022 stay as zeros, by the Table 4 recipe.
        - Dropped the 71 samples with Tellinoidea (sibes_id 339, 2015-2022): tellinoids below 3 mm are classified at the superfamily level, which "Includes ... Macoma balthica" (species.csv), so their Macoma count is a lower bound (CLEAN-15). All 71 go, not only the 29 without Macoma, so the rule reads another taxon's record, not the label. The 12 samples with Tellininae (3-5 mm) and no Macoma stay as zeros: "So far, only Macomangulus tenuis and Fabulina fabula were found" (species.csv).
        - Six 2022 sample ids appear twice in samples.csv with two different sediment measurements (149.8 and 47.2 um in one) and one fauna record: one row kept, and neither measurement is a source of the interpolation.
        - Dropped how the sample was taken, `sampling_type` (grid or random station), `platform` (boat or on foot) and `total_surface_m2` (the core area, set by the platform), and `sample_id`: an unsampled place has no visit (USE-3), and the density is already per m2. The other taxa of the sample are measured with the target and are not inputs.
        - Note: held for training rows only, not shipped (cross-dataset item of 2026-11-09, Andrej): what each sample measured at its visit, which a place between the stations lacks: the sediment measured in the jar (`median_grain_size`, `percentage_mud`, in 55,776 of the release's 59,463 samples; it enters only as the interpolation for other samples), how the sample was taken (`sampling_type`, `platform`, the core area `total_surface_m2`), and the rest of biota.csv for the sample, the 170 other taxa and the tellins' biomass (`afdm_m2`). They are known for the sampled stations when the map is fit, but not for a place it predicts. They would need a training-only role, which the format does not have yet (MET-14, LEAK-41, MET-16), so they stay out for now.
        - Exposure (MET-14, MET-15, USE-3; 2026-11-06): the effort behind a count is the core area, planned by the platform (two boat cores of 0.0173 m2 together, one core of 0.0177 m2 on foot; CV 1.4% over the shipped rows), and, for samples with many individuals, a subsample fraction the lab picks after seeing the sample and does not release ("For the species and samples that contained many individuals, a subsample was selected and analyzed", descriptor). The source folds both into `abundance_m2`, "standardized for differences in sampled surface area and subsampling" (descriptor, Table 4), so the target is a density: 2,480 of the 25,974 positive counts per core (density x core area, 9.55%) are more than 0.02 from a whole number. The 608 below one tellin per core (on a 0.1 lattice, mostly in samples poor in fauna) are not explained by the area or the subsample correction, which can only raise a count; the descriptor documents fractional counts only for polychaete fragments, so their cause is unknown; they ship as published with this note, and NIOZ is not asked for now (CC 2026-11-08, Lennart; Review issue 7). They are 1.0% of the rows, at small densities (median about 29 per m2), which the RMSE on the density does not feel. No count is released, so MET-14's check that the target times the core area rebuilds the count has nothing to rebuild; the source's density ships as it is. The map predicts the density of each place, an equal-area cell, so the task scores it unweighted and declares no sample weight (the equal-area clause of LEAK-41's time-on-risk row in the leak rules, 2026-11-08, with noaa_afsc_bottom_trawl_survey_cpue); the core area is no feature, as an unsampled place has no core (above), and a Poisson deviance on the count per core would not be a likelihood for counts that are not whole.
        - Note: 117 station-days hold two samples, a grid and a random sample at the same coordinates (log1p correlation 0.53). With the interpolated sediment the two share every feature (the duplicate rows the checks report); both are kept, in one fold through the station.
        - Note: for lack of funding, many 2017 and 2018 samples were processed years later (descriptor, Table 1: 2,831 and 2,274 processed then; version 6 holds 4,139 and 4,140), and Tellininae occur almost only in 2018. Bivalvia sp. ("Parts of individuals", 874 samples) is kept: no species list ties it to Macoma.
        - Metric (Andrej, 2026-11-10, review issue 8, option C): the per-year normalised RMSE on the density, `mean_group_normalized_rmse` over the 15 survey years: each year's RMSE on the density (after the inverse of log1p) divided by the standard deviation of that year's true densities, averaged over the years, so each survey's map counts once. The original is RMSE on the density pooled over the years, the fallback kept on 2026-11-02 (CC, Andrej) since the source names no single criterion. Pooled, a few dense spat patches decide it (up to 99,780 per m2): 2014 holds 75.5% of the squared deviation of the density (the yearly standard deviation runs from 93 per m2 in 2008 to 2,899 in 2014) and the 10 densest samples 58.0%. Within a year a fixed divisor ranks models as RMSE does, so only the equal weight per year is ours; within a year a few cores still weigh most (a year's 10 densest samples hold a median 55% of its squared deviation, 25% to 82%). On 2026-11-09 (8 untuned models, the 9 shipped splits, 3 seeds) the pooled RMSE and the per-year score agreed only at Kendall tau 0.51 (0.36 to 0.71 per split): LightGBM fit by squared error on the density beat the constant pooled but not per year (a difference of +0.013, SE 0.015), and LightGBM with a Tweedie loss was first under both. Task probe on the new score (2026-11-10, untuned, fit on log1p, 5 of the 9 splits): random forest 0.962, LightGBM 0.967, linear 1.005, the dummy (the training mean of log1p, back-transformed) 1.046, where 1 is each year's own mean density; the random forest beats the dummy on 5 of 5 splits by 0.084 (SE 0.005); no flag. `survey_year`, the year of `date` as text, is the metric's group, a scoring column and never a feature; `date` stays a feature. Every fold holds every year, since whole stations are held out with all their years. On the pooled RMSE (before 2026-11-10): an untuned LightGBM fit on log1p explains R^2 0.33 of log1p but 0.01 of the density (9 shipped folds, before the elevation was joined). Back-transformed, it puts the mean density of a tidal basin in a year at a median 0.19 of the observed (143 basin-years with at least 100 test samples, one repeat), yet its RMSE is only 4% above that of a Tweedie fit on the density (879.7 against 847.1, the training mean 883.9; the Tweedie fit wins in 9 of 9 folds). RMSE kept (CC 2026-11-02, Andrej): the fallback, as the source names no single criterion; nantucket_sound_sea_duck_aerial_survey_counts takes the mean Poisson deviance as a stand-in for its source's one likelihood criterion.
        - Note (CC 2026-11-06, Lennart): 39 samples are a single boat core of 0.00866 m2, which the data descriptor does not describe (from a boat "two cores ... combined area of 0.0173 m2", on foot "a single core of 0.0177 m2"): 20 in 2008, 9 in 2010 and 10 in 2009-2019, each at its own station (32 grid, 7 random). 79.5% hold no tellin, against 60.6% in the same stations' 452 other samples and 67.2% in the two-core boat samples of the same year and basin; one tellin in such a core is 115.5 per m2, against 57.7 in two, and halving the area of a random scatter at those rates gives 77.8% and 82.0% zeros. Kept (CLEAN-11: unusual, not wrong): the source standardised their density for the area, they are 0.07% of the rows, and the zeros a small core adds are the chance part of a zero that the next note names.
        - Note: a core of 0.017 m2 can miss tellins where the habitat suits them ("even when environmental conditions are perfectly suitable, it is possible to encounter no animals in the core", Lyashevska et al. 2016, Introduction), so a zero mixes unsuitable habitat and chance.
        - CC (2026-11-06, Lennart): decision D13 of the exposure study (#51; review issue 6): the 39 single boat cores stay, with the note above, and the notes name the effort the density folds in (the core area and the subsample fraction, chosen after the sample is seen and not released). No earlier call covered them: the definition has kept them without a note since the review panel of 2026-11-01, which counted them and raised nothing; the exposure study of 2026-11-05 found that the descriptor does not describe them and measured their zeros (79.5% against 57.4% for two-core boat samples).
        - CC (2026-11-10, Andrej): review issue 8, "Reply (b): Per-year normalised RMSE (C)": the score is `mean_group_normalized_rmse` over the survey years on the density, each survey's map one vote, in place of the pooled RMSE of 2026-11-02.
        - CC (2026-11-09, Andrej): review issue 9, A as implemented, "Go ahead" on the consistency check's (a): the elevation stays the latest vaklodingen survey stamped on or before the sample's date, though the map of a past survey could also take a later one. The reason: the survey nearest in time would move the elevation by a median 0.08 m (90th percentile 0.30 m, for the 49.7% of the samples it changes), about the median 0.07 m between two successive surveys of a cell, too little to move a settled join.
    """

    # Task
    target = "log1p_macoma_per_m2"
    problem_type = "regression"
    metric = Metric.from_context(
        "mean_group_normalized_rmse",
        reason=(
            "The use case is the map of one past survey, and Lyashevska et al. 2016 (Materials and Methods, "
            "Cross-validation) check such a map within one year, by several measures side by side with no single "
            "criterion (MET-5); the SIBES descriptor and data page define no metric. The original is RMSE on the "
            "density pooled over the 15 survey years, the fallback kept on 2026-11-02 (Andrej); pooled, 2014, the year "
            "of the dense spat patches, holds 75.5% of the squared deviation and decides the ranking. Each year's RMSE "
            "on the density over the spread of its true densities, averaged, keeps RMSE within a year (a fixed divisor "
            "ranks models as RMSE does) and gives each survey's map one vote (Andrej, 2026-11-10)."
        ),
        inputs={"group": "survey_year"},
        target_transform="log1p",
    )
    scoring_columns = (
        ScoringColumn(
            column="survey_year",
            role="group",
            used_by="mean_group_normalized_rmse",
            description=(
                "the survey year, the year of `date` as text (15 years, 2008-2022): the metric divides each year's "
                "RMSE on the density by the spread of its true densities and averages the 15; never a feature, and "
                "`date` stays a feature"
            ),
        ),
    )
    accepted_check_warnings = {
        "task_target_value_dominant": (
            "56.0% zeros: samples without a Baltic tellin (Andrej, 2026-11-03: zero-inflated targets are natural for these tasks and a core challenge)."
        ),
    }
    grouping = Grouping(
        on="station",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a SIBES sampling station, a fixed position on the 500 m grid or a random station placed on a gridline at a random distance from a grid station, revisited every year (5,092 stations, most sampled 13-15 times in 2008-2022). Held out with all its years, a station stands for a place on the flats without a fauna sample, which is where the map is wanted: "the model was used to make predictions for sites where only environmental data are available" (Lyashevska et al. 2016, Abstract). Their leave-one-out cross-validation over the stations of one year is the analogue; holding a station out in every year is stricter, as a model cannot use the station's own record (R^2 0.343 against 0.378 when the station's other years stay in training, untuned LightGBM before the elevation was joined). Each sample is one prediction.
        """,
    )
    splits_comment = """
        Default grouped splits on the station: every sample of a station, in all years, stays on one side, so a test station is a place without a fauna sample. Its neighbouring stations and the other stations of the same survey year are in training, as for a map drawn between the stations of a survey. The moment is a map of a past survey drawn from the whole archive, so the later surveys are in training too; they add rows, not the test year's outcome: trained only on the years up to its own, a test year scores R^2 0.317 on log1p, against 0.299 on as many random training rows (untuned LightGBM, one repeat). The test is somewhat stricter than a map: a test sample lies a median 500 m from the nearest training station of its year, a map pixel 195 m from the nearest station. Grouped rather than temporal: the use case maps a surveyed year between stations, not a future year (SPLIT-3); expanding yearly windows score R^2 0.16-0.33. Leak test across the split (CC 2026-11-02, Andrej): no test row has a feature copy in training; merging stations within 50, 100 or 250 m into one group moves R^2 from 0.377 by +0.000, -0.002 and -0.006, so no nearby station is a hidden copy; 6.8% of the test rows have a training sample of their year within 100 m, against 14.5% of map pixels; no input is built from another row's outcome. Removing the test year's training rows costs R^2 0.085, as many random rows 0.002 (9 of 9 splits): the score leans on the same survey's other stations, which is the map's own input, not a leak.
    """

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        return {
            "samples": pd.read_csv(raw_dir / "samples.csv"),
            "biota": pd.read_csv(raw_dir / "biota.csv"),
            "species": pd.read_csv(raw_dir / "species.csv"),
            "elevation": station_elevation_series(
                raw_dir / "vaklodingen",
                pd.read_csv(raw_dir / "samples.csv").drop_duplicates("sampling_station_id"),
            ),
        }

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        samples, biota, species = raw["samples"].copy(), raw["biota"], raw["species"]
        assert species.loc[species["sibes_id"] == MACOMA_SIBES_ID, "name"].tolist() == ["Macoma balthica"]
        assert species.loc[species["sibes_id"] == TELLINOIDEA_SIBES_ID, "name"].tolist() == ["Tellinoidea"]

        # 1. Six sample ids occur twice with conflicting sediment values: one row each, no sediment source.
        twice = samples["sample_id"].duplicated(keep=False)
        samples.loc[twice, SEDIMENT] = np.nan
        samples = samples.drop_duplicates("sample_id", keep="first")

        # 2. A place without a sample has the sediment interpolated from the year's other stations (USE-3).
        interpolated = interpolate_sediment(samples)
        samples["interpolated_median_grain_size_um"] = interpolated["median_grain_size"]
        samples["interpolated_mud_percent"] = interpolated["percentage_mud"]

        # 3. Elevation: the station's 20 m cell in the latest vaklodingen survey whose date stamp (mostly a nominal
        # 1 January of the survey year) is on or before the sample's date.
        samples["day"] = pd.to_datetime(samples["date"])
        latest = pd.merge_asof(
            samples.reset_index().sort_values("day", kind="stable"),
            raw["elevation"].sort_values("survey", kind="stable"),
            left_on="day",
            right_on="survey",
            by="sampling_station_id",
            direction="backward",
        ).set_index("index")
        samples["elevation_m_nap"] = latest["elevation_m_nap"]
        samples = samples.drop(columns="day")

        # 4. 2008 samples without any fauna record are located by the year, not by the core (LEAK-25): dropped.
        # Later ones are counted as processed by the descriptor (Table 1) and stay as zeros (Table 4).
        no_record = ~samples["sample_id"].isin(biota["sample_id"])
        samples = samples[~(no_record & samples["date"].str.startswith("2008"))]

        # 5. Tellinoidea below 3 mm include Macoma: its count in those samples is a lower bound (CLEAN-15).
        tellinoid = biota.loc[biota["sibes_id"] == TELLINOIDEA_SIBES_ID, "sample_id"]
        samples = samples[~samples["sample_id"].isin(tellinoid)]

        # 6. The target: Macoma per m2, zero where the sample has no Macoma row (descriptor, Table 4).
        macoma = biota[biota["sibes_id"] == MACOMA_SIBES_ID].groupby("sample_id")["abundance_m2"].sum()
        density = samples["sample_id"].map(macoma).fillna(0.0)
        samples[self.target] = np.log1p(density)

        # 7. Names; the station is the group column.
        df = samples.rename(
            columns={
                "sampling_station_id": "station",
                "tidal_basin_name": "tidal_basin",
                "tidal_flat_name": "tidal_flat",
                "x": "longitude",
                "y": "latitude",
            }
        )
        df["station"] = df["station"].astype(str)
        df["survey_year"] = df["date"].str[:4]  # the metric's group (one vote per survey's map), never a feature

        # 8. The visit's own sediment and how the sample was taken are no property of an unsampled place (USE-3).
        return drop_columns(df, ["sample_id", "sampling_type", "platform", "total_surface_m2", *SEDIMENT])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=["station", "tidal_basin", "tidal_flat", "survey_year"],  # survey_year: the metric's group
            datetime={"date": "%Y-%m-%d"},
        )

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        samples, biota = raw["samples"].drop_duplicates("sample_id"), raw["biota"]
        in_taxon = {
            name: samples["sample_id"].isin(biota.loc[biota["sibes_id"] == sibes_id, "sample_id"])
            for name, sibes_id in [("macoma", MACOMA_SIBES_ID), ("tellinoidea", TELLINOIDEA_SIBES_ID)]
        }
        table = pd.DataFrame(
            {
                "year": samples["date"].str[:4].astype(int),
                "without_fauna_record": ~samples["sample_id"].isin(biota["sample_id"]),
                "with_tellinoidea": in_taxon["tellinoidea"],
                "tellinoidea_without_macoma": in_taxon["tellinoidea"] & ~in_taxon["macoma"],
            }
        )
        by_year = table.groupby("year").agg(
            samples=("year", "size"),
            without_fauna_record=("without_fauna_record", "sum"),
            with_tellinoidea=("with_tellinoidea", "sum"),
            tellinoidea_without_macoma=("tellinoidea_without_macoma", "sum"),
        )
        by_year["share_without_record"] = (by_year["without_fauna_record"] / by_year["samples"]).round(3)
        kept_year = pd.to_datetime(df["date"]).dt.year
        by_year["kept"] = kept_year.value_counts().reindex(by_year.index)
        by_year["macoma_zero_share_kept"] = (df[self.target] == 0).groupby(kept_year).mean().round(3)
        return [
            Decision(
                title="2008 samples without any fauna record dropped, later ones kept as zeros",
                why=(
                    "A sample with no row in biota.csv is an empty core or a sample whose fauna was never entered. "
                    "The descriptor's Table 1 counts every such sample among the processed ones, and an unprocessed "
                    "sample leaves no entry. 2008 has 9.0% of them against 0.2-1.5% in each later year, so the year "
                    "locates unrecorded samples without reading the core (LEAK-25); the later ones stay as zeros."
                ),
                evidence=by_year[
                    ["samples", "without_fauna_record", "share_without_record", "kept", "macoma_zero_share_kept"]
                ],
            ),
            Decision(
                title="Samples with Tellinoidea dropped",
                why=(
                    "SIBES counts tellinoids below 3 mm at the superfamily level, Macoma balthica included "
                    "(species.csv), so in these samples the Macoma count is a lower bound (CLEAN-15)."
                ),
                evidence=by_year.loc[
                    by_year["with_tellinoidea"] > 0, ["with_tellinoidea", "tellinoidea_without_macoma"]
                ],
            ),
        ]
