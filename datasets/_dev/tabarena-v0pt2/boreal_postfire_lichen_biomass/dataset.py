"""Curated dataset definition for `boreal_postfire_lichen_biomass` (data-foundry v2). Evidence: README.md."""

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
    ScoringColumn,
    Source,
    TaskSummary,
    UnitWeight,
    drop_columns,
)

# The two regional sheets of Greuel et al. (2021), one per Dryad deposit, and their columns as published.
SHEETS = {"NT": "Lichen_data_NT", "SK": "Lichen_data_SK"}
# The NT deposit's site sheet (added on Dryad in 2026): each plot's start coordinates to about 6 decimals.
SITE_FILE, SITE_SHEET = "All_site_info_NT.xlsx", "All site info 2019-10-16"
RENAME = {
    "kgha.volperm2": "forage_lichen_biomass_kg_ha",
    "TSSRF": "years_since_fire",
    "standtype": "stand_type",
    "design": "jurisdiction",
}
# The authors' cover-based estimate of the same biomass: 61.934 kg/ha per percent of forage-lichen cover.
COVER_BIOMASS_PER_PERCENT = 61.934


def _site_coordinates(site: pd.DataFrame) -> pd.DataFrame:
    """Each NT plot's transect start from the site sheet, as numbers.

    Args:
        site: The NT site sheet as published (`Lat_start` and `Long_start` are text with a decimal comma).

    Returns:
        `site_latitude` and `site_longitude`, indexed by plot.
    """
    ref = site.set_index("plot")[["Lat_start", "Long_start"]]
    ref = ref.apply(lambda col: col.astype(str).str.replace(",", ".").astype(float))
    ref.columns = ["site_latitude", "site_longitude"]
    return ref


def _mislocated_plots(nt: pd.DataFrame, site: pd.DataFrame) -> pd.DataFrame:
    """The NT plots whose task-sheet coordinate differs from the site sheet's by more than 0.01 degree.

    Args:
        nt: The NT lichen sheet as published.
        site: The NT site sheet as published.

    Returns:
        One row per such plot: the task sheet's `latitude`, `longitude` and `ecoprovince`, and the site sheet's
        `site_latitude` and `site_longitude`.
    """
    plots = nt.drop_duplicates("plot").set_index("plot")[["latitude", "longitude", "ecoprovince"]]
    ref = _site_coordinates(site).reindex(plots.index)
    off = (plots["latitude"] - ref["site_latitude"]).abs().gt(0.01) | (
        plots["longitude"] - ref["site_longitude"]
    ).abs().gt(0.01)
    return plots[off].join(ref[off])


def _linked_groups(plots: pd.DataFrame) -> pd.Series:
    """One group per set of plots linked by a shared area name or by an identical grid coordinate (exact keys only).

    Args:
        plots: One row per plot with `area_name`, `grid_latitude` and `grid_longitude`, in file order.

    Returns:
        The group label of each plot, numbered in file order, indexed like `plots`.
    """
    keys = [plots["area_name"], plots["grid_latitude"].astype(str) + "," + plots["grid_longitude"].astype(str)]
    label = pd.Series(np.arange(len(plots)), index=plots.index)
    while True:  # propagate the smallest label through both keys until nothing changes
        before = label.copy()
        for key in keys:
            label = label.groupby(key.to_numpy()).transform("min")
        if label.equals(before):
            break
    return label.rank(method="dense").astype(int).map("area_{:03d}".format)


def _repair_nt(nt: pd.DataFrame, site: pd.DataFrame) -> pd.DataFrame:
    """Give every NT plot the site sheet's coordinates, and repair the plots that `_mislocated_plots` finds.

    Every plot takes its transect start from the site sheet as `latitude` and `longitude`. The task sheet's 0.01
    degree grid is kept as `grid_latitude` and `grid_longitude`, only to link areas that share a coordinate; a
    mislocated plot's grid value is the site sheet's rounded to 0.01 degree, and it takes the ecoprovince of the other
    plots of its site (`F1-22` of `F1-22A`) where there are any.

    Args:
        nt: The NT lichen sheet as published.
        site: The NT site sheet as published.

    Returns:
        A repaired copy of `nt` with the two grid columns added.
    """
    nt = nt.copy()
    off = _mislocated_plots(nt, site)
    rows = nt["plot"].isin(off.index)
    nt["grid_latitude"], nt["grid_longitude"] = nt["latitude"], nt["longitude"]
    nt.loc[rows, "grid_latitude"] = nt.loc[rows, "plot"].map(off["site_latitude"].round(2))
    nt.loc[rows, "grid_longitude"] = nt.loc[rows, "plot"].map(off["site_longitude"].round(2))
    ref = _site_coordinates(site)
    nt["latitude"], nt["longitude"] = nt["plot"].map(ref["site_latitude"]), nt["plot"].map(ref["site_longitude"])
    if nt[["latitude", "longitude"]].isna().any().any():
        raise ValueError("an NT plot is missing from the site sheet")
    site_name = nt["plot"].str.replace(r"[A-Z]$", "", regex=True)
    mates = nt.loc[~rows].groupby(site_name[~rows])["ecoprovince"].agg(lambda s: s.mode().iloc[0])
    nt.loc[rows, "ecoprovince"] = site_name[rows].map(mates).fillna(nt.loc[rows, "ecoprovince"])
    return nt


def _km(lat1: pd.Series, lon1: pd.Series, lat2: pd.Series, lon2: pd.Series) -> pd.Series:
    """Great-circle distance in km between two sets of coordinates in degrees."""
    p1, p2, dlon = np.radians(lat1), np.radians(lat2), np.radians(lon2 - lon1)
    return 6371.0 * np.arccos((np.sin(p1) * np.sin(p2) + np.cos(p1) * np.cos(p2) * np.cos(dlon)).clip(-1, 1))


class BorealPostfireLichenBiomass(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "How much caribou forage lichen (kg/ha) grows on the ground of a boreal stand of known type, location and "
            "time since the last stand-replacing fire, in a burn or unburned area that was not surveyed?"
        ),
        use_case=(
            "A caribou habitat biologist with the Northwest Territories government or Saskatchewan's Ministry of "
            "Environment revises a boreal caribou range plan: today every burn under 40 years counts as disturbed, "
            "while NWT monitoring found that forage lichens need 45 to 70 years to recover. From fire records and the "
            "forest inventory, the biologist estimates the forage of stands of a given type, ecoprovince and fire age "
            "in burns nobody surveyed."
        ),
        row=(
            "One ground quadrat of a survey plot (2,010 quadrats of 516 plots): five 1 x 1 m quadrats per plot in the "
            "Northwest Territories (2016-2018), two 2 x 2 m quadrats per plot in Saskatchewan (2015-2016)."
        ),
        predicted=(
            "The live biomass of the forage Cladonia lichens in the quadrat, in kg/ha, as the authors estimated it "
            "from the lichens' measured cover and height with their allometric equation; 0 in 40% of the quadrats."
        ),
        known=(
            "The years since the last stand-replacing fire, the stand type, the plot's coordinates and its "
            "ecoprovince, ecozone and jurisdiction, the same for every quadrat of a plot. The age is the survey's "
            "own, dated in the field where no fire is recorded, and the stand type the crew's class; a planner has "
            "the inventory's coarser values."
        ),
        split=(
            "Whole burn scars or unburned areas of the Northwest Territories are held out, and each Saskatchewan plot "
            "on its own (its name carries no burn key), so a test quadrat stands for a stand in a burn with no survey; "
            "test quadrats lie a median 22 km (NT) and 3.4 km (SK) from the nearest training plot."
        ),
        changes=(
            "We stack the two regional surveys, take the NT plots' coordinates from the authors' site sheet (the "
            "lichen sheet rounds them to 0.01 degree, three of them wrongly), drop the authors' cover-based biomass, "
            "its presence flag and the quadrat labels, and split by burn area where the source fits models to all plots."
        ),
        fit="approximate",
        fit_reason=(
            "The paper's own aim, a forecast of forage lichen for caribou management, but the label is an allometric "
            "estimate (one pooled equation; SK's live height taken as 0.76 of the total); rows are quadrats where the "
            "planner acts on stands; the survey is a stratified chronosequence with no NT burn younger than 29 years; "
            "and the age and stand type are field values, sharper than an inventory's."
        ),
    )

    # Dataset
    unique_name = "boreal_postfire_lichen_biomass"
    domain = "biology & life sciences"
    sources = (
        Source(
            role="publication",
            platform="Other",  # two Dryad deposits of Greuel et al. (2021), first versions 2021-02-03 (NT) and 2021-02-18 (SK)
            url="https://doi.org/10.5061/dryad.t1g1jwt15",
            license="CC0 1.0",  # both Dryad deposits and the Zenodo copies of their lichen sheets
            year="2021",
            bibtex=r"""
                @article{greuel2021predicting,
                  title = {Predicting patterns of terrestrial lichen biomass recovery following boreal wildfires},
                  author = {Greuel, Ruth J. and Degr{\'e}-Timmons, Genevi{\`e}ve {\'E}. and Baltzer, Jennifer L. and Johnstone, Jill F. and McIntire, Eliot J. B. and Day, Nicola J. and Hart, Sarah J. and McLoughlin, Philip D. and Schmiegelow, Fiona K. A. and Turetsky, Merritt R. and Truchon-Savard, Alexandre and van Telgen, Mario D. and Cumming, Steven G.},
                  journal = {Ecosphere},
                  volume = {12},
                  number = {4},
                  pages = {e03481},
                  year = {2021},
                  doi = {10.1002/ecs2.3481},
                  note = {Data: \url{https://doi.org/10.5061/dryad.t1g1jwt15} (Northwest Territories) and \url{https://doi.org/10.5061/dryad.tb2rbnzzj} (Saskatchewan), CC0}
                }
            """,
        ),
    )
    data_tags = ("Spatial",)
    download_description = """
        The data is the two Dryad deposits of Greuel et al. (2021), CC0: doi:10.5061/dryad.t1g1jwt15 (Northwest Territories, version 5 of 2026-05-18) and doi:10.5061/dryad.tb2rbnzzj (Saskatchewan, version of 2021-02-18). Dryad's per-file API answers 401 without a token, but the version download of its API redirects without a token to a zip of each version; the SHA-256 digests below equal those Dryad lists (checked 2026-11-01). The two lichen sheets are also on Zenodo, byte-identical (records 4499194 and 4552434); the NT site sheet is only on Dryad.
        mkdir -p local-data-warehouse/boreal_postfire_lichen_biomass && cd local-data-warehouse/boreal_postfire_lichen_biomass
        curl -L -o dryad_t1g1jwt15_v20260518.zip https://datadryad.org/api/v2/versions/442103/download
        curl -L -o dryad_tb2rbnzzj_v20210218.zip https://datadryad.org/api/v2/versions/105865/download
        unzip dryad_t1g1jwt15_v20260518.zip  # All_site_info_NT.xlsx, Destructive_biomass_sample_NT.xlsx, Lichen_data_NT.xlsx, Quadrat_cover_data_NT.xlsx
        unzip dryad_tb2rbnzzj_v20210218.zip  # Destructive_biomass_sample_SK.xlsx, Lichen_data_SK.xlsx
        sha256sum Lichen_data_NT.xlsx  # 03a3f3f497415fe1843d140aff621941ae2079db3437ef4186699f463d856b90
        sha256sum Lichen_data_SK.xlsx  # 74ad1fe59d2a3364e0b78f552a8b0581e8f37cd085ddcf9b222c42bcd81292a6
        sha256sum All_site_info_NT.xlsx  # 24493a7427adeecb04c694f515729d90c2a831d44ad2d8fccd453a781e7cdf6c
    """
    curation_comments = """
        We start with `Lichen_data_NT.xlsx` (1,630 quadrats) and `Lichen_data_SK.xlsx` (380 quadrats), the quadrat sheets of the two Dryad deposits of Greuel et al. (2021), and the NT deposit's site sheet `All_site_info_NT.xlsx`, from Dryad's version downloads (NT version 5 of 2026-05-18, SK version of 2021-02-18).
        - Prediction point: a caribou habitat biologist revising a boreal caribou range plan wants the forage lichen of a stand in a burn nobody surveyed, from its location, ecoprovince, stand type and years since fire. A range needs 65% undisturbed habitat and every burn under 40 years counts as disturbed ([federal fact sheet](https://www.canada.ca/en/environment-climate-change/services/species-risk-public-registry/recovery-strategies/woodland-caribou-boreal-population-fact-sheet.html)), while NWT monitoring found that forage lichens need 45 to 70 years to recover ([CIMP](https://climatelibrary.ecc.gov.nt.ca/dataset/4bcc94fc-cb61-400e-858a-1bac4526ffcf)). The source names managers, not one actor: its goal is "accurately predicting the availability of lichen forage under current and future fire regimes" (Introduction), and its relationships "support the development of the first landscape level and regional level, spatial predictions of forage lichen biomass for several boreal and barren-ground caribou herds"; "Managers should consider these regional and stand-type differences when developing strategies for caribou habitat management" (Discussion). The paper was read from the publisher's PDF (Wayback Machine copy of 2021-07-16; Andrej read the HTML on 2026-11-03).
        - The rows: Northwest Territories, "Lichen communities data collected in boreal forests from 2016-2018", "5, 1 m x 1 m quadrats at each plot"; Saskatchewan, "collected 2015-2016", "2, 2 m x 2 m quadrats at each plot" (the sheets' metadata). The sheets hold 326 NT and 190 SK plots, against the 346 and 221 of the Dryad abstracts. The 20 missing NT plots are in the deposit's `Quadrat_cover_data_NT.xlsx` (346 plots), so the authors left them out of the lichen sheet (already in its 2021 version); they stay out, since adding them back would need a target from our inferred formula. Anomaly: the 31 missing SK plots are explained neither in the files nor in the paper, whose analysis counts "n = 2014 samples across 567 sites" (Results, "Predicting lichen biomass accumulation"), close to the 2,010 quadrats here, so the missing plots may have had no quadrat data.
        - Version: we ship the authors' 2022 revision of the NT sheet (Dryad version 4 of 2022-06-23, unchanged since). Against the 2021 file it drops five extra zero quadrats of plot CG2-5A, which had 10 rows, and adds the missing fifth quadrat of F6-7B (`F6-7B-6`, 0) and the constant `species` column; the other 1,629 quadrats are identical. The year stays 2021, the first publication.
        - Target: `forage_lichen_biomass_kg_ha` is the published `kgha.volperm2`, "Biomass of live lichen species, estimated by standardize live lichen volume", the pooled forage groups (C. mitis and C. arbuscula, C. rangiferina and C. stygia, C. stellaris, C. uncialis). For NT it reproduces as 12.633 x the sum of percent cover x live depth over the four forage groups (median ratio 12.6333 over the 945 quadrats with forage cover in `Quadrat_cover_data_NT.xlsx`); SK has no cover sheet. One pooled allometry serves both regions: biomass = 0.013 x live volume (R^2 0.88 on 203 destructive samples; 12.633 is that slope in kg/ha per percent cover x cm), as "the allometric relations did not vary among ecoprovinces for the pooled Cladonia spp." (P = 0.66; Results, "Allometric equations"). SK crews measured total lichen height only; the authors took live height as 0.76 of it, "the mean ratio of live to total lichen biomass in the sorted SK samples" (Methods, "Lichen biomass allometry"), which the SK files cannot reproduce. The destructive samples (`Destructive_biomass_sample_*.xlsx`) are the allometry's calibration data, not task rows. Chosen over the cover-based `kgha.areaperm2` because the authors' presence flag `non_zero` equals volume biomass > 0 in all 2,010 quadrats, while cover biomass > 0 differs in 2 SK quadrats (plot 2015-054).
        - Kept on kg/ha, not logged, for this task's own reasons (Andrej, 2026-11-03, review issue 5): the planner needs forage in kg/ha, and trained on log1p and back-transformed, every probed family falls below the training mean on RMSE in kg/ha (30 shipped splits, untuned; skill against the training mean, raw against log1p: random forest +0.097 against -0.045, small LightGBM +0.103 against -0.030, means; ridge's log1p model is worse on 27 of 30 splits).
        - Dropped `kgha.areaperm2`: it is 61.934 kg/ha times the quadrat's percent cover in every row (NT on a 0.5% grid, SK on 0.1%), the same survey's measurement of the target's own cover, unknown for an unsurveyed stand (LEAK-10, a part of the target). Dropped `non_zero`, the indicator of a positive target (LEAK-10).
        - Dropped the quadrat label (`quadrat`, `plot.quadrat`: positions 0, 6, 12, 18, 24 in NT, `nw` and `se` in SK), an identifier within a plot; `species`, constant (`Cladonia spp.`, NT only); `acronym` and `acronym1`, one-to-one recodings of `ecoprovince` (CLEAN-5). Kept `ecozone` and `jurisdiction` (the published `design`), coarser levels of the ecoprovince; `jurisdiction` also marks the protocol, 1 m2 quadrats in NT and 4 m2 in SK.
        - Anomaly: plot F8-3A labels one quadrat `8` where every other plot has `6`; it is the plot's fifth quadrat, and the label is dropped anyway.
        - Coordinates (Andrej, 2026-11-09, review issue 9): every NT plot takes the start of its belt transect from the authors' site sheet `All_site_info_NT.xlsx` (`Lat_start`, `Long_start`, 4 to 6 decimals, text with a decimal comma), where the lichen sheet gives a 0.01 degree grid; SK's own sheet gives 12 or 13 decimals. The start places the plot, not each quadrat along the transect. For 323 NT plots the grid point lies a median 0.30 km from the site sheet's start (90th percentile 0.51 km, at most 0.59 km), and on the grid 244 of the 326 plots shared their coordinate with another plot, mostly the A and B plots of one site; in the site sheet none do. The planner knows where the stand is (USE-6), and the authors published the starts in the same CC0 deposit.
        - Repair (2026-11-01): three NT plots, 15 rows, were wrong on the grid by more than 0.01 degree (Decisions). CG3-31A carries CG2-35A's coordinate (62.22, -116.33), 162 km from its site-mates; the site sheet puts it at 60.77, -116.56 with them, so it also takes their ecoprovince, Hay and Slave River Lowlands for Great Bear Plains (the ecozone stays Taiga plains). F13-5A and F13-5B sit 7.8 and 7.9 km off, at 63.03, -114.35 against 63.00, -114.21. The grid, with these three set to the site sheet rounded to 0.01 degree, is kept only to link areas that share an exact recorded coordinate (the next bullets) and is not shipped; until 2026-11-09 it was also the shipped coordinate.
        - Every input is constant within a plot, so the quadrats of a plot share one feature vector and differ only in the target; they stay as the source's rows (SPLIT-26). Each plot counts once in the score (Lennart, 2026-11-08, review issue 7): the RMSE weights a quadrat by 1 over its plot's number of quadrats (`plot_weight`: 0.2 for the five of an NT plot, 0.5 for the two of an SK plot, so 1 per plot), a scoring column for the metric only, no feature and no training weight. A model predicts one value per plot, so the weighted MSE splits into a fixed within-plot floor plus the squared error of the plot means with each of the 516 plots counted once, and the weighted RMSE ranks models exactly like that stand score (Kendall tau 1 on all 30 shipped splits; SPLIT-23). Unweighted, the per-quadrat RMSE declared until then counted an NT plot 2.5 times an SK plot (5 quadrats against 2; NT holds 81% of the quadrats but 63% of the plots), a weighting the survey protocols set while the planner acts on stands. The two scores mostly agree: Kendall tau 0.81 per split on average (the lowest split 0.00 or 0.21, depending on the run) and 0.86 for the ranking by the mean over the splits (8 untuned predictors: random forest, extra trees, two LightGBM, two ridge, knn and the training mean); that ranking swaps only two pairs, whose difference is noise (the training mean against ridge, paired t -0.45 over the 30 splits, and against knn, t -1.14). Tau depends on the model set: with a median and a zero predictor added it is 0.84 per split and 0.91 for the ranking. 28.8% of the target's variance lies within a plot, a floor no model can go below. Hence 518 exact duplicate rows (506 at 0), all quadrats of one plot, and the 976 rows the check counts as sharing their inputs with a row of another target (1,646 rows sit in an input group with more than one target). Since the site sheet's coordinates (2026-11-09) no two plots share every input; on the 0.01 degree grid sibling plots did, which added 14 copies and raised the share within identical inputs to 32.5%. No feature vector occurs in two groups, so the split keeps every copy on one side (LEAK-18: few features, natural repeats).
        - Exposure (MET-14, MET-15; 2026-11-06): none. The lichen of a quadrat is an amount over a sampled area, which the source folds into the target: it ships the amount per unit area that MET-14 asks for (kg/ha). The sampled area, a 1 m2 quadrat in NT and a 4 m2 quadrat in SK, is a protocol constant set by `jurisdiction`, not realized, so LEAK-41 has nothing to remove; the planner decides per stand, not per sampled m2, so no exposure weight follows (MET-15). The score's `plot_weight` (above) is no exposure either: a design weight that gives each plot one vote, set by `jurisdiction`, a feature, so MET-15 asks for no training weight (2026-11-08).
        - Zeros: 813 of 2,010 quadrats (40.4%; NT 40.7%, SK 39.5%) have a target of 0, the presence part of the authors' hurdle model ("to account both for the heterogeneous nature of lichen presence (zero-inflation)", Dryad abstract). 811 have no forage-lichen cover; 2 in plot 2015-054 have cover but volume 0 and stay 0, as the authors' presence flag has them.
        - Note: `years_since_fire` (`TSSRF`, "Time since stand replacing fire") is the survey's stand age per plot, not a fire-map value. The 145 NT control plots (725 rows, 36%) lie in areas with "no recorded burn history" (Dryad NT methods) and carry ages of 33 to 241 years, so theirs were dated in the field: from four (SK) or five (NT) tree cores or disks per site, "the time since stand-replacing fire based on clusters of tree ages (<20-yr range)" and, "at sites without a clear cohort of similar-aged trees, and with no recorded fire history", "the ring count of the oldest sampled tree" (Methods, "Forest stand composition and structure"). The sites were chosen by fire-record age class (NT: 37-38 and 46-49 years after fire, and controls ">70 yr" with no recorded burn; Methods, "Site selection"); only 26 of 110 multi-plot NT sites share one age. A planner has an inventory age or "older than the fire record". Capping the age at assumed fire-record horizons (51 years in NT, 70 in SK, our assumption) costs 0.01 to 0.03 R^2 on the shipped splits (random forest 0.007, ridge 0.024, small LightGBM 0.032; SE 0.016 to 0.021). Kept: a stand age is known at the prediction point (USE-6), and the gap is named in the fit. `stand_type` is likewise the crew's class ("Stand types, Hart et al. 2019"), where a planner has the inventory's.
        - Grouped by burn area. A group is an NT burn scar or unburned area, the plot-name prefix (`F1` of `F1-22A`; the codebook: "Plot location: Burn Scar or Unburned area -xxx"), merged with any area that shares an exact recorded coordinate on the lichen sheet's 0.01 degree grid: only CG2 and F2 join (CG2-4A and F2-22A/B share 62.64, -116.25 on the grid and lie 0.28 and 0.42 km apart in the site sheet). Each SK plot is its own group, since SK names ("Year -xxx") carry no burn key. 216 groups, 26 NT and 190 SK; the largest, CG2 with F2, holds 200 rows (10.0%). Burn areas hold 18.4% of the NT target's sum of squares. The use case predicts for burns nobody surveyed (SPLIT-1, SPLIT-4); under the former site split, 94.3% of NT test quadrats had another site of their own burn area in training.
        - Note: SK burns are not recovered (Andrej, 2026-11-10, review issue 8). SK plots share burns that their names do not record: 71 of the 190 SK plots have another SK plot of the same fire year (the survey year in the name minus `TSSRF`) within 5 km, and 94 of the 190 lie inside a burn polygon of their fire year (1 year either way) in Natural Resources Canada's fire maps (the agencies' fire perimeters, NFDB, and the National Burned Area Composite, NBAC), 69 of them in 20 burns of 2 to 9 plots; with one group per plot, 88% of the SK test plots in such a burn have a burn-mate in training. The effect is small (2026-11-09; untuned random forest, LightGBM and ridge, 3 seeds, the 30 splits): burn-mates in training flatter the SK RMSE by about 5 kg/ha (2 kg/ha overall), against an SK RMSE of about 1,230 kg/ha with a fold-draw SE of about 40, and grouping by the mapped burns (shipped on 2026-11-09 only) moved no model in rank. The maps are not used: they reach only half of the SK plots (none of the 66 dated before 1945, where SK's mapped record starts), they would add about 2 GB of outside data and a shapefile reader to the build, and NFDB keeps only its current version online, so a later build could stop until the file names are updated.
        - Note: a test quadrat lies a median 22 km from the nearest training plot in NT and 3.4 km in SK (median per split, mean over the 30 splits; 2.4 km in NT under the former site split), against 95 km for a random point in the NT study hull and 15.6 km in the SK hull. SK plot means (log1p) still correlate with other plots nearby (r = 0.73 under 1 km on 16 pairs, 0.42 at 2 to 5 km, about 0.2 out to 50 km), so SK stays the laxer region; between plots of different NT areas r peaks at 0.21 (5 to 10 km) and is about 0 beyond 10 km.
        - Note: ridge loses its skill under this split (-0.085 against the training mean, below it on 8 of 30 splits, in the probes of 2026-11-01; +0.13 under the former site split), while the random forest keeps +0.097; on the container's inputs (without `plot`; 2026-11-09) ridge scores +0.008 and falls below the mean on 7 of 30, so its skill swings with the fold draw. Its ecoprovince effects, learned from a handful of burns (Great Bear Plains has 5 NT areas, with means from 270 to 3,453 kg/ha), do not reach a new burn: without the three region labels ridge scores +0.064. Each label is known for every stand and the source names ecoprovince as a predictor, so they stay.
        - The source's model and metric: a hurdle model, a binomial GLM of presence on stand age, stand type and ecoprovince and a nonlinear mixed-effects logistic growth model of biomass given presence, chosen by AICc and ANOVA; the combined model is judged in sample by "the R2 of a linear regression between measured lichen biomass and predicted lichen biomass" (Methods, "Modeling site-level mean biomass"), "a relatively weak but significant fit (R2 = 0.18, P < 0.001)" (Results, "Combined predictions"). No held-out error is reported. That R^2 is a squared correlation, blind to a biased forecast, so it cannot rank models; the task scores `rmse` on kg/ha, the planner's unit (Andrej, 2026-11-03, review issue 6: "We can keep RMSE in this case"), with each plot counted once (Lennart, 2026-11-08, review issue 7). It is declared from the context, since the fallback takes no weight.
        - Probes (2026-11-01, untuned, the 30 shipped splits): random forest skill +0.120 against the training mean (above it on 93% of the splits), LightGBM +0.033, linear -0.075 (it swings with the fold draw); no task-probe flag, no leak-probe flag (no feature alone above the mean, no exact feature copy across the split). A random split by quadrat would give LightGBM R^2 0.440 against 0.015 by burn area. On the RMSE with each plot counted once (2026-11-08), the random forest scores 1,159.8 kg/ha against the training mean's 1,250.0, better on 80% of the splits; still no task-probe flag. From 2026-11-09 the probes read the model inputs only, without `plot` (the probes before read it as a feature). On the site sheet's coordinates (2026-11-09, same folds) the random forest scores 1,164.3 against 1,250.0, better on 77% of the splits; no flag. Back on one group per SK plot (2026-11-10) the probes give these numbers again: task probe as above, no flag; group probe LightGBM R^2 0.408 on random folds against -0.035 on the burn-area folds; leak probes: no flag (no feature alone above the mean, no exact feature copy across the split).
        - Coordinates of the NT plots (2026-11-09): on the same 30 splits, the site sheet's coordinates against the grid change the random forest's RMSE by +4.2 kg/ha (SE 3.3), LightGBM's by +3.9 (SE 8.9) and ridge's by -0.4 (SE 0.1): within noise.
        - Note: held for training rows only, not shipped (cross-dataset item of 2026-11-09, Andrej): the authors measured these for the surveyed plots and quadrats, which a model could learn from, but a planner has none of them for a stand nobody surveyed. The cover-based biomass `kgha.areaperm2` (61.934 kg/ha times the quadrat's percent forage-lichen cover; Spearman 0.994 with the target in NT, 0.990 in SK) and the presence flag `non_zero` (equal to target > 0 in all 2,010 quadrats), both dropped in `_clean`. The NT ground covers of `Quadrat_cover_data_NT.xlsx` (11,627 rows: percent cover of 36 attributes such as feathermosses, litter, Sphagnum, ash and each forage-lichen group, with live and total depth for the lichens, in 1,718 quadrats of 346 plots, all 326 shipped NT plots among them; the forage-lichen covers and depths are the target's own inputs), never read. The destructive calibration samples of `Destructive_biomass_sample_NT.xlsx` and `Destructive_biomass_sample_SK.xlsx` (342 and 256 rows: 155 and 72 harvested bags from 93 and 61 plots, with cover, live and dead depth, volume and dry weight), the allometry's calibration data, never read. They would need a training-only role, which the format does not have yet (MET-14, LEAK-41 and MET-16 require the drop today).
        - CC (2026-11-09, Andrej): issue 9 (B), "Site-sheet coordinates as features": every NT plot ships its transect start from `All_site_info_NT.xlsx`; the 0.01 degree grid only links CG2 and F2 and is not shipped.
        - CC (2026-11-09, Andrej): issue 8 (B), "Burn id from the national fire polygons. Before finally adding this, ablate it and analyze the impact of this decision": the SK plots are grouped by the NFDB or NBAC burn of their fire year, implemented after the ablation; superseded on 2026-11-10 (next bullet).
        - CC (2026-11-10, Andrej): issue 8 (a), "Back to A, with the note": one group per SK plot again; the grouping by the fire maps of 2026-11-09 is removed, and its measured effect is in the notes ("SK burns are not recovered").
    """

    # Task
    target = "forage_lichen_biomass_kg_ha"
    problem_type = "regression"
    metric = Metric.fallback(
        reason=(
            "The paper judges its combined hurdle model in sample by the R2 of a regression of observed on predicted "
            "biomass (0.18; Results, 'Combined predictions'), a squared correlation that ignores a bias of the "
            "predictions, and reports no held-out error; RMSE on kg/ha, the planner's unit, is kept (Andrej, "
            "2026-11-03). Each plot counts once, since the planner acts on stands: a quadrat weighs 1 over its plot's "
            "number of quadrats (`plot_weight`: 0.2 for the five of an NT plot, 0.5 for the two of an SK plot), "
            "where unweighted the survey protocols would count an NT plot 2.5 times an SK plot (Lennart, 2026-11-08)."
        ),
        inputs={"weight": "plot_weight"},
    )
    scoring_columns = (
        ScoringColumn(
            column="plot_weight",
            role="weight",
            used_by="rmse",
            description=(
                "1 over the number of quadrats of the row's plot (0.2 for the five of an NT plot, 0.5 for the two of "
                "an SK plot), so that each plot counts once in the RMSE; for scoring only, never a feature or a "
                "training weight"
            ),
        ),
    )
    unit_weight = UnitWeight(column="plot_weight", unit="plot")
    grouping = Grouping(
        on="burn_area",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a burn scar or unburned area of the Northwest Territories (the plot-name prefix, `F1` of `F1-22A`; the codebook's "Plot location: Burn Scar or Unburned area -xxx"), merged with any area that shares an exact coordinate on the lichen sheet's 0.01 degree grid (only CG2 and F2 join, 0.3 to 0.4 km apart), with all its plots and quadrats. Each Saskatchewan plot is its own group, as SK plot names carry no burn key. 216 groups: 26 NT of 10 to 200 quadrats and 190 SK of 2. The use case is a stand in a burn nobody surveyed: a range-plan biologist estimates forage across a caribou range, where most stands have no plot. Quadrats of one plot share every input, and plots of one area stand in the same burn scar or unburned area (18.4% of the NT target's sum of squares lies between areas), so all stay on one side. Stricter than the source, which fits its models to all plots. Each quadrat is one prediction.
        """,
    )
    splits_comment = """
        Grouped splits on the burn area: every plot of a burn scar or unburned area of the Northwest Territories (merged where two areas share a coordinate, only CG2 and F2) stays on one side with all its quadrats, and each Saskatchewan plot on its own, since SK plot names carry no burn key. 216 groups, 72 per test fold; test folds hold 299 to 1,028 rows, since the largest group holds 200. A test quadrat lies a median 22 km from the nearest training plot in NT and 3.4 km in SK, against 95 km for a random point in the NT study hull, so stands far from any survey may still be harder than the folds show, SK most: SK plots of one burn can fall on both sides (94 of 190 lie inside a mapped burn of their fire year; burn-mates in training flatter the SK RMSE by about 5 kg/ha). Ridge falls below the training mean on 7 of 30 splits (untuned, the container's inputs), because ecoprovince effects learned from a handful of burns do not reach a new burn; the random forest keeps its skill.
    """

    accepted_check_warnings = {
        "dataset_duplicate_rows": (
            "518 exact copies, 506 of them at 0, all quadrats of one plot, since every input is a plot attribute. "
            "Each copy stays in one group, so no test row has a copy in training (LEAK-18: few features, natural "
            "repeats; Andrej, 2026-11-03; recounted 2026-11-09 on the site sheet's coordinates, where sibling plots "
            "no longer share every input)."
        ),
        "dataset_conflicting_duplicate_rows": (
            "Quadrats of one plot share their inputs and differ in lichen: 976 rows. 28.8% of the target's variance "
            "lies within a plot, a floor no model can go below; no two plots share every input. Each input vector "
            "stays in one group (Andrej, 2026-11-03; recounted 2026-11-09)."
        ),
    }

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        raw = {region: pd.read_excel(raw_dir / f"{sheet}.xlsx", sheet_name=sheet) for region, sheet in SHEETS.items()}
        raw["site"] = pd.read_excel(raw_dir / SITE_FILE, sheet_name=SITE_SHEET)
        return raw

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        # 1. NT coordinates from the authors' site sheet; the task sheet's grid (three plots repaired) kept for the link
        nt, sk = _repair_nt(raw["NT"], raw["site"]), raw["SK"].copy()
        # 2. Stack the two regional sheets; the quadrat labels differ in type (0-24 in NT, nw/se in SK)
        nt["area_name"] = "NT:" + nt["plot"].str.split("-").str[0]  # the burn scar or unburned area, F1 of F1-22A
        sk["area_name"] = "SK:" + sk["plot"]  # SK plot names carry no burn key: each plot on its own
        df = pd.concat([nt, sk], ignore_index=True).rename(columns=RENAME)
        # 3. The group, from exact keys only: the area name, merged where two areas share a coordinate on the NT grid
        #    (only CG2 and F2 join; SK plots carry their own coordinates, none shared)
        df["grid_latitude"] = df["grid_latitude"].fillna(df["latitude"])
        df["grid_longitude"] = df["grid_longitude"].fillna(df["longitude"])
        plots = df.drop_duplicates("plot")
        df["burn_area"] = df["plot"].map(dict(zip(plots["plot"], _linked_groups(plots), strict=True)))
        # 4. The metric's weight, 1 over the plot's number of quadrats (0.2 in NT, 0.5 in SK): each plot counts once
        #    in the RMSE; a scoring column, no feature and no training weight
        df["plot_weight"] = 1.0 / df.groupby("plot")["plot"].transform("size")
        # 5. Drops: the cover-based biomass (cover x 61.934, a part of the target) and non_zero (target > 0) are
        #    LEAK-10; the quadrat labels are identifiers (the plot stays as the unit of `plot_weight`, metadata, never
        #    a feature); species is constant; acronym and acronym1 recode the ecoprovince one to one
        return drop_columns(
            df,
            [
                "kgha.areaperm2",
                "non_zero",
                "plot.quadrat",
                "quadrat",
                "area_name",
                "grid_latitude",
                "grid_longitude",
                "species",
                "acronym",
                "acronym1",
            ],
        )

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=["burn_area", "plot", "stand_type", "jurisdiction", "ecozone", "ecoprovince"],
        )

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        off = _mislocated_plots(raw["NT"], raw["site"])
        fixed = _repair_nt(raw["NT"], raw["site"]).drop_duplicates("plot").set_index("plot")
        grid = raw["NT"].drop_duplicates("plot").set_index("plot")[["latitude", "longitude"]]
        km = _km(grid["latitude"], grid["longitude"], fixed["latitude"], fixed["longitude"])
        fixed = fixed.loc[off.index]
        repaired = pd.DataFrame(
            {
                "task sheet (grid)": off["latitude"].map("{:.2f}".format)
                + ", "
                + off["longitude"].map("{:.2f}".format),
                "task sheet ecoprovince": off["ecoprovince"],
                "site sheet (shipped)": off["site_latitude"].map("{:.6f}".format)
                + ", "
                + off["site_longitude"].map("{:.6f}".format),
                "km apart": km.loc[off.index].round(1),
                "grid for the link only": fixed["grid_latitude"].map("{:.2f}".format)
                + ", "
                + fixed["grid_longitude"].map("{:.2f}".format),
                "shipped ecoprovince": fixed["ecoprovince"],
            }
        )
        rest = km.drop(off.index)
        rows = []
        for region in SHEETS:
            frame = raw[region]
            presence = frame["non_zero"] == 1
            rows.append(
                {
                    "jurisdiction": region,
                    "quadrats": len(frame),
                    "non_zero = (volume biomass > 0)": int((presence == (frame["kgha.volperm2"] > 0)).sum()),
                    "non_zero = (cover biomass > 0)": int((presence == (frame["kgha.areaperm2"] > 0)).sum()),
                    "cover biomass / 61.934 on a 0.1% grid": int(
                        np.isclose(
                            frame["kgha.areaperm2"] / COVER_BIOMASS_PER_PERCENT * 10,
                            (frame["kgha.areaperm2"] / COVER_BIOMASS_PER_PERCENT * 10).round(),
                            atol=1e-3,
                        ).sum()
                    ),
                    "Spearman volume vs cover biomass": round(
                        frame["kgha.volperm2"].corr(frame["kgha.areaperm2"], method="spearman"), 3
                    ),
                }
            )
        return [
            Decision(
                title="The target is the volume-based biomass; the cover-based one is dropped",
                why=(
                    "The authors' presence flag follows the volume estimate in every quadrat, and the cover estimate "
                    "is a fixed multiple of the quadrat's percent cover, a part of the target."
                ),
                evidence=pd.DataFrame(rows).set_index("jurisdiction"),
            ),
            Decision(
                title="The NT plots take the site sheet's coordinates; three were wrong on the task sheet's grid",
                why=(
                    "The authors' site sheet gives each NT plot's transect start to 4 to 6 decimals, where the task "
                    f"sheet rounds to 0.01 degree: for the other {len(rest)} plots the grid point lies a median "
                    f"{rest.median():.2f} km from the start (at most {rest.max():.2f} km). On the grid CG3-31A carries "
                    "CG2-35A's coordinate, 162 km from its site-mates, and F13-5A and F13-5B sit about 8 km off. The "
                    "grid, with these three corrected, only links areas that share a coordinate and is not shipped."
                ),
                evidence=repaired,
            ),
        ]
