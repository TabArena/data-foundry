"""Curated dataset definition for `boreal_postfire_lichen_biomass` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, Grouping, Metric, TaskSummary, drop_columns

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


def _mislocated_plots(nt: pd.DataFrame, site: pd.DataFrame) -> pd.DataFrame:
    """The NT plots whose task-sheet coordinate differs from the site sheet's by more than 0.01 degree.

    Args:
        nt: The NT lichen sheet as published.
        site: The NT site sheet as published (`Lat_start` and `Long_start` are text with a decimal comma).

    Returns:
        One row per such plot: the task sheet's `latitude`, `longitude` and `ecoprovince`, and the site sheet's
        `site_latitude` and `site_longitude`.
    """
    plots = nt.drop_duplicates("plot").set_index("plot")[["latitude", "longitude", "ecoprovince"]]
    ref = site.set_index("plot")[["Lat_start", "Long_start"]].reindex(plots.index)
    ref = ref.apply(lambda col: col.astype(str).str.replace(",", ".").astype(float))
    ref.columns = ["site_latitude", "site_longitude"]
    off = (plots["latitude"] - ref["site_latitude"]).abs().gt(0.01) | (
        plots["longitude"] - ref["site_longitude"]
    ).abs().gt(0.01)
    return plots[off].join(ref[off])


def _linked_groups(plots: pd.DataFrame) -> pd.Series:
    """One group per set of plots linked by a shared area name or by identical coordinates (exact keys only).

    Args:
        plots: One row per plot with `area_name`, `latitude` and `longitude`, in file order.

    Returns:
        The group label of each plot, numbered in file order, indexed like `plots`.
    """
    keys = [plots["area_name"], plots["latitude"].astype(str) + "," + plots["longitude"].astype(str)]
    label = pd.Series(np.arange(len(plots)), index=plots.index)
    while True:  # propagate the smallest label through both keys until nothing changes
        before = label.copy()
        for key in keys:
            label = label.groupby(key.to_numpy()).transform("min")
        if label.equals(before):
            break
    return label.rank(method="dense").astype(int).map("area_{:03d}".format)


def _repair_nt(nt: pd.DataFrame, site: pd.DataFrame) -> pd.DataFrame:
    """Repair the NT plots that `_mislocated_plots` finds, from the site sheet.

    Such a plot takes the site sheet's coordinate rounded to the task sheet's 0.01 degree grid, and the ecoprovince of
    the other plots of its site (`F1-22` of `F1-22A`) where there are any.

    Args:
        nt: The NT lichen sheet as published.
        site: The NT site sheet as published.

    Returns:
        A repaired copy of `nt`.
    """
    nt = nt.copy()
    off = _mislocated_plots(nt, site)
    rows = nt["plot"].isin(off.index)
    nt.loc[rows, "latitude"] = nt.loc[rows, "plot"].map(off["site_latitude"].round(2))
    nt.loc[rows, "longitude"] = nt.loc[rows, "plot"].map(off["site_longitude"].round(2))
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
            "test quadrats lie a median 22 km (NT) and 3.7 km (SK) from the nearest training plot."
        ),
        changes=(
            "We stack the two regional surveys, repair three plots' coordinates from the authors' site sheet, drop the "
            "authors' cover-based biomass, its presence flag and the quadrat labels, and split by burn area where the "
            "source fits models to all plots."
        ),
        fit="approximate",
        fit_reason=(
            "A real planning decision, but the label is an allometric estimate whose constant we could not check "
            "against the paper, converted differently in the two regions; rows are quadrats where the planner acts on "
            "stands; the survey is a stratified chronosequence of two regions and four ecoprovinces, with no NT burn "
            "younger than 29 years; and the age and stand type are field values, sharper than an inventory's."
        ),
    )

    # Dataset
    unique_name = "boreal_postfire_lichen_biomass"
    year = "2021"
    domain = "biology & life sciences"
    source = "Other"  # two Dryad deposits of Greuel et al. (2021), first versions 2021-02-03 (NT) and 2021-02-18 (SK)
    source_url = "https://doi.org/10.5061/dryad.t1g1jwt15"
    license = "CC0 1.0"  # both Dryad deposits and the Zenodo copies of their lichen sheets
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
    bibtex = r"""
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
    """
    curation_comments = """
        We start with `Lichen_data_NT.xlsx` (1,630 quadrats) and `Lichen_data_SK.xlsx` (380 quadrats), the quadrat sheets of the two Dryad deposits of Greuel et al. (2021), and the NT deposit's site sheet `All_site_info_NT.xlsx`, from Dryad's version downloads (NT version 5 of 2026-05-18, SK version of 2021-02-18).
        - Prediction point: a caribou habitat biologist revising a boreal caribou range plan wants the forage lichen of a stand in a burn nobody surveyed, from its location, ecoprovince, stand type and years since fire. A range needs 65% undisturbed habitat and every burn under 40 years counts as disturbed ([federal fact sheet](https://www.canada.ca/en/environment-climate-change/services/species-risk-public-registry/recovery-strategies/woodland-caribou-boreal-population-fact-sheet.html)), while NWT monitoring found that forage lichens need 45 to 70 years to recover ([CIMP](https://climatelibrary.ecc.gov.nt.ca/dataset/4bcc94fc-cb61-400e-858a-1bac4526ffcf)). The source names no actor; its results "provide a basis for estimating future caribou habitat" (Dryad abstract). The paper is CC BY 4.0, but the AI could not fetch it (Wiley 403), so the claims about it below come from the Dryad abstracts and the sheets' metadata and are unverified against the paper; the curator has been asked to read it (PROV-17).
        - The rows: Northwest Territories, "Lichen communities data collected in boreal forests from 2016-2018", "5, 1 m x 1 m quadrats at each plot"; Saskatchewan, "collected 2015-2016", "2, 2 m x 2 m quadrats at each plot" (the sheets' metadata). The sheets hold 326 NT and 190 SK plots, against the 346 and 221 of the Dryad abstracts. The 20 missing NT plots are in the deposit's `Quadrat_cover_data_NT.xlsx` (346 plots), so the authors left them out of the lichen sheet (already in its 2021 version); they stay out, since adding them back would need a target from our inferred formula. Anomaly: the 31 missing SK plots are not explained in the files.
        - Version: we ship the authors' 2022 revision of the NT sheet (Dryad version 4 of 2022-06-23, unchanged since). Against the 2021 file it drops five extra zero quadrats of plot CG2-5A, which had 10 rows, and adds the missing fifth quadrat of F6-7B (`F6-7B-6`, 0) and the constant `species` column; the other 1,629 quadrats are identical. The year stays 2021, the first publication.
        - Target: `forage_lichen_biomass_kg_ha` is the published `kgha.volperm2`, "Biomass of live lichen species, estimated by standardize live lichen volume", the pooled forage groups (C. mitis and C. arbuscula, C. rangiferina and C. stygia, C. stellaris, C. uncialis). For NT it reproduces as 12.633 x the sum of percent cover x live depth over the four forage groups (median ratio 12.6333 over the 945 quadrats with forage cover in `Quadrat_cover_data_NT.xlsx`); SK has no cover sheet. The two regions' conversions differ: the destructive samples (`Destructive_biomass_sample_*.xlsx`, 155 and 72 harvested 20 x 20 cm patches, the allometry's calibration data, not task rows) give 63.7 (NT) and 50.9 (SK) kg/ha per percent cover through the origin, and `jurisdiction` carries the offset. Chosen over the cover-based `kgha.areaperm2` because the authors' presence flag `non_zero` equals volume biomass > 0 in all 2,010 quadrats, while cover biomass > 0 differs in 2 SK quadrats (plot 2015-054).
        - Kept on kg/ha, not logged: trained on log1p and back-transformed, every probed family falls below the training mean on RMSE in kg/ha (30 shipped splits, untuned; skill against the training mean, raw against log1p: random forest +0.097 against -0.045, small LightGBM +0.103 against -0.030, means; ridge's log1p model is worse on 27 of 30 splits).
        - Dropped `kgha.areaperm2`: it is 61.934 kg/ha times the quadrat's percent cover in every row (NT on a 0.5% grid, SK on 0.1%), the same survey's measurement of the target's own cover, unknown for an unsurveyed stand (LEAK-10, a part of the target). Dropped `non_zero`, the indicator of a positive target (LEAK-10).
        - Dropped the quadrat label (`quadrat`, `plot.quadrat`: positions 0, 6, 12, 18, 24 in NT, `nw` and `se` in SK), an identifier within a plot; `species`, constant (`Cladonia spp.`, NT only); `acronym` and `acronym1`, one-to-one recodings of `ecoprovince` (CLEAN-5). Kept `ecozone` and `jurisdiction` (the published `design`), coarser levels of the ecoprovince; `jurisdiction` also marks the protocol, 1 m2 quadrats in NT and 4 m2 in SK.
        - Anomaly: plot F8-3A labels one quadrat `8` where every other plot has `6`; it is the plot's fifth quadrat, and the label is dropped anyway.
        - Repair (2026-11-01): a plot whose task-sheet coordinate differs from the authors' site sheet by more than 0.01 degree takes the site sheet's, rounded to 0.01 degree; three NT plots, 15 rows (Decisions). CG3-31A carries CG2-35A's coordinate (62.22, -116.33), 162 km from its site-mates; the site sheet puts it at 60.77, -116.56 with them, so it also takes their ecoprovince, Hay and Slave River Lowlands for Great Bear Plains (the ecozone stays Taiga plains). F13-5A and F13-5B move 7.8 and 7.9 km, from 63.03, -114.35 to 63.00, -114.21. The other 323 NT plots equal the site sheet rounded to 0.01 degree; that grid stays, since the coordinate links rest on it.
        - Every input is constant within a plot, so the quadrats of a plot share one feature vector and differ only in the target; they stay as the source's rows (SPLIT-26) and are scored one by one. A quadrat score ranks models like a stand score weighted by quadrats (Kendall tau 0.91 on the former site splits), with an NT plot weighing 5 quadrats against 2 for SK (SPLIT-23). 32.5% of the target's variance lies within identical inputs (28.8% within a plot), a floor no model can go below. Hence 532 exact duplicate rows (518 at 0: 482 quadrats of one plot and 36 of sibling plots that share every input) and the 980 rows the check counts as sharing their inputs with a row of another target (1,671 rows sit in an input group with more than one target). No feature vector occurs in two groups, so the split keeps every copy on one side (LEAK-18: few features, natural repeats).
        - Zeros: 813 of 2,010 quadrats (40.4%; NT 40.7%, SK 39.5%) have a target of 0, the presence part of the authors' hurdle model ("to account both for the heterogeneous nature of lichen presence (zero-inflation)", Dryad abstract). 811 have no forage-lichen cover; 2 in plot 2015-054 have cover but volume 0 and stay 0, as the authors' presence flag has them.
        - Note: `years_since_fire` (`TSSRF`, "Time since stand replacing fire") is the survey's stand age per plot, not a fire-map value. The 145 NT control plots (725 rows, 36%) lie in areas with "no recorded burn history" (Dryad NT methods) and carry ages of 33 to 241 years, so theirs were dated in the field (how is in the unread paper); only 26 of 110 multi-plot NT sites share one age. A planner has an inventory age or "older than the fire record". Capping the age at assumed fire-record horizons (51 years in NT, 70 in SK, our assumption) costs 0.01 to 0.03 R^2 on the shipped splits (random forest 0.007, ridge 0.024, small LightGBM 0.032; SE 0.016 to 0.021). Kept: a stand age is known at the prediction point (USE-6), and the gap is named in the fit. `stand_type` is likewise the crew's class ("Stand types, Hart et al. 2019"), where a planner has the inventory's.
        - Grouped by burn area. A group is an NT burn scar or unburned area, the plot-name prefix (`F1` of `F1-22A`; the codebook: "Plot location: Burn Scar or Unburned area -xxx"), merged with any area that shares an exact recorded coordinate: only CG2 and F2 join (CG2-4A and F2-22A/B lie about 0.5 km apart in the site sheet). Each SK plot is its own group, since SK names ("Year -xxx") carry no burn key. 216 groups, 26 NT and 190 SK; the largest, CG2 with F2, holds 200 rows (10.0%). Burn areas hold 18.4% of the NT target's sum of squares. The use case predicts for burns nobody surveyed (SPLIT-1, SPLIT-4); under the former site split, 94.3% of NT test quadrats had another site of their own burn area in training.
        - Note: a test quadrat lies a median 22.0 km from the nearest training plot in NT (2.4 km under the former site split), against 95 km for a random point in the NT study hull; in SK, split per plot, 3.7 km (15.6 km for a point in the SK hull). SK plot means (log1p) still correlate with other plots nearby (r = 0.73 under 1 km on 16 pairs, 0.42 at 2 to 5 km, about 0.2 out to 50 km), so SK stays the laxer region; between plots of different NT areas r peaks at 0.21 (5 to 10 km) and is about 0 beyond 10 km.
        - Note: ridge loses its skill under this split (-0.085 against the training mean, below it on 8 of 30 splits; +0.13 under the former site split), while the random forest keeps +0.097. Its ecoprovince effects, learned from a handful of burns (Great Bear Plains has 5 NT areas, with means from 270 to 3,453 kg/ha), do not reach a new burn: without the three region labels ridge scores +0.064. Each label is known for every stand and the source names ecoprovince as a predictor, so they stay.
        - The source's model and metric: a hurdle model whose GLM part "identified stand age, stand type and ecoprovince as significant predictors of lichen presence", and a logistic growth model of recovery (time to 50% of the asymptote, 28 to 73 years) (Dryad abstract); no prediction error is reported there, so the fallback `rmse` on kg/ha.
        - Probes (2026-11-01, untuned, the 30 shipped splits): random forest skill +0.120 against the training mean (above it on 93% of the splits), LightGBM +0.033, linear -0.075 (it swings with the fold draw); no task-probe flag, no leak-probe flag (no feature alone above the mean, no exact feature copy across the split). A random split by quadrat would give LightGBM R^2 0.440 against 0.015 by burn area.
    """

    # Task
    target = "forage_lichen_biomass_kg_ha"
    problem_type = "regression"
    metric = Metric.fallback(
        reason=(
            "The Dryad abstracts of both deposits report a hurdle model judged by the significance of its predictors "
            "and a logistic growth model of recovery time, with no prediction error. The paper (Ecosphere 12:e03481) "
            "is CC BY 4.0 but the AI could not fetch it (Wiley 403); the curator has been asked to check it for a "
            "reported prediction error. No metric is defined by the source as read."
        ),
    )
    grouping = Grouping(
        on="burn_area",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a burn scar or unburned area of the Northwest Territories (the plot-name prefix, `F1` of `F1-22A`; the codebook's "Plot location: Burn Scar or Unburned area -xxx"), merged with any area that shares an exact recorded coordinate (only CG2 and F2 join, about 0.5 km apart), with all its plots and quadrats; each Saskatchewan plot is its own group, as SK plot names carry no burn key. 216 groups: 26 NT of 10 to 200 quadrats and 190 SK of 2. The use case is a stand in a burn nobody surveyed: a range-plan biologist estimates forage across a caribou range, where most stands have no plot. Quadrats of one plot share every input, and plots of one area stand in the same burn scar or unburned area (18.4% of the NT target's sum of squares lies between areas), so all stay on one side. Stricter than the source, which fits its models to all plots. Each quadrat is one prediction.
        """,
    )
    splits_comment = """
        Grouped splits on the burn area: every plot of a burn scar or unburned area of the Northwest Territories (merged where two areas share a coordinate, only CG2 and F2) stays on one side with all its quadrats, and each Saskatchewan plot on its own, since SK plot names carry no burn key. 216 groups, 72 per test fold; test folds hold 299 to 1,028 rows, since the largest group holds 200. A test quadrat lies a median 22.0 km from the nearest training plot in NT and 3.7 km in SK, against 95 km for a random point in the NT study hull, so stands far from any survey may still be harder than the folds show, SK most. Ridge falls below the training mean on 8 of 30 splits, because ecoprovince effects learned from a handful of burns do not reach a new burn; the random forest keeps its skill.
    """

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        raw = {region: pd.read_excel(raw_dir / f"{sheet}.xlsx", sheet_name=sheet) for region, sheet in SHEETS.items()}
        raw["site"] = pd.read_excel(raw_dir / SITE_FILE, sheet_name=SITE_SHEET)
        return raw

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        # 1. Repair: the plots whose coordinate differs from the authors' site sheet by more than 0.01 degree
        nt, sk = _repair_nt(raw["NT"], raw["site"]), raw["SK"].copy()
        # 2. Stack the two regional sheets; the quadrat labels differ in type (0-24 in NT, nw/se in SK)
        nt["area_name"] = "NT:" + nt["plot"].str.split("-").str[0]  # the burn scar or unburned area, F1 of F1-22A
        sk["area_name"] = "SK:" + sk["plot"]  # SK plot names carry no burn key: each plot on its own
        df = pd.concat([nt, sk], ignore_index=True).rename(columns=RENAME)
        # 3. The group: areas linked through identical coordinates (exact keys from the data; only CG2 and F2 join)
        plots = df.drop_duplicates("plot")
        df["burn_area"] = df["plot"].map(dict(zip(plots["plot"], _linked_groups(plots), strict=True)))
        # 4. Drops: the cover-based biomass (cover x 61.934, a part of the target) and non_zero (target > 0) are
        #    LEAK-10; the plot and quadrat labels are identifiers; species is constant; acronym and acronym1 recode
        #    the ecoprovince one to one
        return drop_columns(
            df,
            [
                "kgha.areaperm2",
                "non_zero",
                "plot",
                "plot.quadrat",
                "quadrat",
                "area_name",
                "species",
                "acronym",
                "acronym1",
            ],
        )

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=["burn_area", "stand_type", "jurisdiction", "ecozone", "ecoprovince"],
        )

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        off = _mislocated_plots(raw["NT"], raw["site"])
        fixed = _repair_nt(raw["NT"], raw["site"]).drop_duplicates("plot").set_index("plot").loc[off.index]
        repaired = pd.DataFrame(
            {
                "task sheet": off["latitude"].map("{:.2f}".format) + ", " + off["longitude"].map("{:.2f}".format),
                "task sheet ecoprovince": off["ecoprovince"],
                "site sheet": off["site_latitude"].map("{:.5f}".format)
                + ", "
                + off["site_longitude"].map("{:.5f}".format),
                "km apart": _km(off["latitude"], off["longitude"], off["site_latitude"], off["site_longitude"]).round(
                    1
                ),
                "shipped": fixed["latitude"].map("{:.2f}".format) + ", " + fixed["longitude"].map("{:.2f}".format),
                "shipped ecoprovince": fixed["ecoprovince"],
            }
        )
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
                title="Three NT plots take the site sheet's coordinates",
                why=(
                    "In the task sheet CG3-31A carries CG2-35A's coordinate, 162 km from its site-mates, and F13-5A "
                    "and F13-5B sit about 8 km from where the authors' site sheet puts them. The other 323 NT plots "
                    "equal the site sheet's coordinates rounded to 0.01 degree."
                ),
                evidence=repaired,
            ),
        ]
