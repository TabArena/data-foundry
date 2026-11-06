"""Curated dataset definition for `noaa_afsc_bottom_trawl_survey_cpue` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import json
import sqlite3
import struct
from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    ScoringColumn,
    TaskSummary,
    Temporal,
    TemporalSplits,
    drop_columns,
)

# The 11 taxa, each with its FOSS species codes; the choice is explained in `curation_comments`. Three are groups of
# species the survey does not tell apart reliably: Atheresthes (arrowtooth flounder, unidentified Atheresthes to 1991,
# Kamchatka flounder) and Lepidopsetta (unidentified rock sole to 1995, northern and southern rock sole), told apart
# only later, and Hippoglossoides (flathead sole, Bering flounder, unidentified Hippoglossoides), rated moderate
# confidence in every Bering Sea catch.
TAXA = {
    "walleye pollock": (21740,),
    "Pacific cod": (21720,),
    "sablefish": (20510,),
    "Pacific halibut": (10120,),
    "rex sole": (10200,),
    "Dover sole": (10180,),
    "Greenland turbot": (10115,),
    "shortspine thornyhead": (30020,),
    "Atheresthes (arrowtooth and Kamchatka flounder)": (10110, 10111, 10112),
    "Lepidopsetta (northern and southern rock sole)": (10260, 10261, 10262),
    "Hippoglossoides (flathead sole and Bering flounder)": (10130, 10140, 10129),
}

# HAUL columns that leave: identifiers and copies of `srvy`, the end position, the tow's effort and gear, the
# vessel and the performance code (reasons in `curation_comments`).
DROPPED_HAUL_COLUMNS = [
    "hauljoin",
    "cruisejoin",
    "cruise",
    "haul",
    "station",
    "survey",
    "survey_name",
    "survey_definition_id",
    "year",
    "vessel_id",
    "vessel_name",
    "latitude_dd_end",
    "longitude_dd_end",
    "distance_fished_km",
    "duration_hr",
    "net_width_m",
    "net_height_m",
    "area_swept_km2",
    "performance",
]

# GAP's survey strata (akgfmaps `inst/extdata/afsc_bts_strata.gpkg`, layer `survey_strata`, EPSG:3338): the Gulf of
# Alaska survey (survey definition 47) was restratified for 2025, and its hauls from then on are placed in the 59
# strata of the design used from 1984 to 2023.
STRATA_FILE = "afsc_bts_strata.gpkg"
GOA_SURVEY_DEFINITION_ID = 47
GOA_OLD_DESIGN_YEAR = 1984
GOA_NEW_DESIGN_FROM = 2025
# A short tow, for the decision on the tow's effort: under this share of the median duration of its region and year
# (the standard tow is 30 minutes in the Bering Sea, 15 in the Gulf of Alaska from 1996 and the Aleutians from 1997).
SHORT_TOW = 0.75


def _read_pages(raw_dir: Path, prefix: str) -> pd.DataFrame:
    """Concatenate the `items` of the numbered FOSS JSON pages `<prefix>_NNNN.json`."""
    items: list[dict] = []
    for page in sorted(raw_dir.glob(f"{prefix}_*.json")):
        with open(page) as f:
            items.extend(json.load(f)["items"])
    return pd.DataFrame(items).drop(columns="links", errors="ignore")


def _read_goa_strata(path: Path) -> pd.DataFrame:
    """The GOA strata of the 1984 design from GAP's GeoPackage: the stratum number and its geometry blob."""
    connection = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    try:
        return pd.read_sql_query(
            "select AREA_ID as stratum, geom from survey_strata "
            "where SURVEY_DEFINITION_ID = ? and DESIGN_YEAR = ? order by AREA_ID",
            connection,
            params=(GOA_SURVEY_DEFINITION_ID, GOA_OLD_DESIGN_YEAR),
        )
    finally:
        connection.close()


def _multipolygon_rings(blob: bytes) -> list[list[np.ndarray]]:
    """The rings of a GeoPackage MULTIPOLYGON blob: per polygon, the shell first, then its holes (x, y arrays)."""
    envelope = {0: 0, 1: 32, 2: 48, 3: 48, 4: 64}[(blob[3] >> 1) & 7]
    wkb = blob[8 + envelope :]  # after the GeoPackage header: standard WKB
    order = "<" if wkb[0] == 1 else ">"
    geometry_type, n_polygons = struct.unpack_from(order + "II", wkb, 1)
    assert geometry_type == 6, geometry_type  # a two-dimensional MULTIPOLYGON
    polygons, pos = [], 9
    for _ in range(n_polygons):
        order = "<" if wkb[pos] == 1 else ">"
        (n_rings,) = struct.unpack_from(order + "I", wkb, pos + 5)
        pos += 9
        rings = []
        for _ in range(n_rings):
            (n_points,) = struct.unpack_from(order + "I", wkb, pos)
            rings.append(np.frombuffer(wkb, dtype=order + "f8", count=2 * n_points, offset=pos + 4).reshape(-1, 2))
            pos += 4 + 16 * n_points
        polygons.append(rings)
    return polygons


def _alaska_albers(latitude: np.ndarray, longitude: np.ndarray) -> np.ndarray:
    """Project degrees to NAD83 / Alaska Albers (EPSG:3338: GRS 80, parallels 55 and 65, origin 50 N 154 W), metres."""
    a, f = 6378137.0, 1 / 298.257222101
    e2 = f * (2 - f)
    e = np.sqrt(e2)

    def m(phi: np.ndarray) -> np.ndarray:
        return np.cos(phi) / np.sqrt(1 - e2 * np.sin(phi) ** 2)

    def q(phi: np.ndarray) -> np.ndarray:
        s = np.sin(phi)
        return (1 - e2) * (s / (1 - e2 * s**2) - np.log((1 - e * s) / (1 + e * s)) / (2 * e))

    phi0, phi1, phi2, lambda0 = np.radians([50.0, 55.0, 65.0, -154.0])
    n = (m(phi1) ** 2 - m(phi2) ** 2) / (q(phi2) - q(phi1))
    c = m(phi1) ** 2 + n * q(phi1)
    rho0 = a * np.sqrt(c - n * q(phi0)) / n
    rho = a * np.sqrt(c - n * q(np.radians(latitude))) / n
    theta = n * (np.radians(longitude) - lambda0)
    return np.column_stack([rho * np.sin(theta), rho0 - rho * np.cos(theta)])


def _goa_stratum_1984(latitude: pd.Series, longitude: pd.Series, strata: pd.DataFrame) -> np.ndarray:
    """The 1984-design GOA stratum that holds each position (-1 outside all; the lowest number where two touch)."""
    from matplotlib.path import Path as PolygonPath

    points = _alaska_albers(latitude.to_numpy(dtype=float), longitude.to_numpy(dtype=float))
    stratum = np.full(len(points), -1)
    for number, blob in zip(strata["stratum"].astype(int), strata["geom"]):
        inside = np.zeros(len(points), dtype=bool)
        for shell, *holes in _multipolygon_rings(blob):
            in_polygon = PolygonPath(shell).contains_points(points)
            for hole in holes:
                in_polygon &= ~PolygonPath(hole).contains_points(points)
            inside |= in_polygon
        stratum[inside & (stratum == -1)] = number
    return stratum


def _short_tows(haul: pd.DataFrame, catch: pd.DataFrame) -> pd.DataFrame:
    """Per taxon, the short tows against the mean of their stratum and year, in the cells that hold short and full tows.

    Three gaps: the share of hauls with a catch, the log1p numbers per km^2 over all hauls, and the log1p numbers per
    km^2 over the hauls with a catch (cells that hold short and full tows with a catch).
    """
    year = pd.to_datetime(haul["date_time"].str[:10], format="%Y-%m-%d").dt.year
    median = haul["duration_hr"].groupby([haul["srvy"], year]).transform("median")
    short = haul["duration_hr"] < SHORT_TOW * median
    cell = haul["srvy"] + ":" + haul["stratum"].astype(str) + ":" + year.astype(str)
    catch = catch.assign(taxon=catch["species_code"].map({c: t for t, codes in TAXA.items() for c in codes}))
    keys = [catch["hauljoin"], catch["taxon"]]
    number = catch["cpue_nokm2"].groupby(keys).sum().where(~catch["cpue_nokm2"].isna().groupby(keys).any())
    grid = pd.MultiIndex.from_product([haul["hauljoin"], list(TAXA)], names=["hauljoin", "taxon"])
    density = np.log1p(number.reindex(grid, fill_value=0.0)).unstack().reindex(index=haul["hauljoin"])
    density.index = haul.index
    rows = {}
    for taxon in TAXA:
        d = density[taxon].dropna()  # a catch weighed but not counted has no numerical CPUE
        s, c = short[d.index], cell[d.index]
        mixed = s.groupby(c).transform("any") & ~s.groupby(c).transform("all")
        d, s, c = d[mixed], s[mixed], c[mixed]
        caught = d > 0
        p, sp, cp = d[caught], s[caught], c[caught]
        mixed_p = sp.groupby(cp).transform("any") & ~sp.groupby(cp).transform("all")
        share = caught.astype(float)
        rows[taxon] = {
            "short tows": int(s.sum()),
            "share with a catch": (share - share.groupby(c).transform("mean"))[s].mean(),
            "all hauls": (d - d.groupby(c).transform("mean"))[s].mean(),
            "hauls with a catch": (p - p[mixed_p].groupby(cp[mixed_p]).transform("mean"))[mixed_p & sp].mean(),
        }
    table = pd.DataFrame(rows).T.rename_axis("taxon")
    table["short tows"] = table["short tows"].astype(int)
    return table.round(3)


class NoaaAfscBottomTrawlSurveyCpue(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "How many fish of a given groundfish species per square kilometre does a summer bottom-trawl haul catch "
            "at a place in Alaskan waters in a given survey year, given the species, the place, its depth and that "
            "year's temperatures there?"
        ),
        use_case=(
            "At each five-year review of essential fish habitat, NOAA's Alaska Fisheries Science Center fits "
            "habitat models to its trawl surveys and maps, species by species, where each managed species is "
            "abundant; the maps decide which waters are described as its essential habitat."
        ),
        row=(
            "One standard haul of AFSC's summer bottom-trawl surveys (eastern and northern Bering Sea shelf, Bering "
            "Sea slope, Gulf of Alaska, Aleutian Islands), 1982-2026, and one of 11 groundfish taxa: each haul "
            "appears once per taxon; 52% of the rows are zero catches."
        ),
        predicted=(
            "The haul's catch of the row's taxon in numbers per square kilometre swept, zero when none was caught "
            "(shipped as log1p; scored after the inverse)."
        ),
        known=(
            "The prediction is for a species at a place in a given survey year, under that year's conditions. "
            "Known: the taxon, the survey region and design stratum, the position, the date, the depth, and that "
            "year's bottom and surface temperatures at the place, given by the readings taken during the haul; not "
            "the vessel or the hour."
        ),
        split=(
            "Nine two-year windows of survey years (2025-2026 back to 2009-2010), each trained on every earlier "
            "survey: two years hold one survey of every region, and a model refit after each season is tested on "
            "the next survey cycle."
        ),
        changes=(
            "We chose 11 taxa (three of them groups the survey does not tell apart reliably), made one row per haul "
            "and taxon "
            "with zero for no catch, put the Gulf of Alaska hauls of 2025 in the strata used before that year's "
            "redesign, and left out the tow's gear and effort (the label's denominator) and the vessel and hour."
        ),
        fit="approximate",
        fit_reason=(
            "The review fits one model per species, region and life stage, with habitat layers the tables do not "
            "ship (sediment, currents, slope), and maps raster cells from long-term mean temperatures; here one "
            "table holds 11 taxa with the taxon as a feature, scored at each haul's own readings in later survey "
            "years."
        ),
    )

    # Dataset
    unique_name = "noaa_afsc_bottom_trawl_survey_cpue"
    year = "2026"
    domain = "biology & life sciences"
    source = "GOV Website"
    source_url = "https://www.fisheries.noaa.gov/foss/f?p=215:28"
    license = "Public Domain"
    data_tags = ("Spatial",)
    download_description = """
        The FOSS (Fisheries One Stop Shop) REST tables of the AFSC Groundfish Assessment Program, paged 10,000 rows at
        a time (needs curl and jq). Downloaded 2026-10-30 (HAUL, SPECIES), 2026-11-01 (CATCH of rex sole) and
        2026-11-02 (CATCH of the other 16 species codes, one query per code: FOSS refuses `$in`); FOSS is
        updated after every survey season, so a later download holds more years. The 2026 catches were not yet rated
        at download: compare with a fresh download before a build (curation notes).

        The survey strata: GAP's GeoPackage of survey strata from its R package akgfmaps (GPL >= 2; only the derived
        stratum codes ship), at a pinned commit, downloaded 2026-11-01. Only the Gulf of Alaska strata of the 1984
        design (layer `survey_strata`, `SURVEY_DEFINITION_ID` 47, `DESIGN_YEAR` 1984) are read.

        mkdir -p local-data-warehouse/noaa_afsc_bottom_trawl_survey_cpue && cd local-data-warehouse/noaa_afsc_bottom_trawl_survey_cpue
        fetch() {  # fetch <table> <file prefix> <q JSON>
            off=0; i=0
            while :; do
                f=$(printf "%s_%04d.json" "$2" "$i")
                curl -fsSG "https://apps-st.fisheries.noaa.gov/ods/foss/$1/" --data-urlencode "limit=10000" \\
                    --data-urlencode "offset=$off" --data-urlencode "q=$3" -o "$f"
                [ "$(jq .hasMore "$f")" = true ] || break
                off=$((off + $(jq '.items | length' "$f"))); i=$((i + 1))
            done
        }
        fetch afsc_groundfish_survey_haul haul '{"$orderby":{"hauljoin":"asc"}}'
        for code in 21740 21720 20510 10120 10200 10180 10115 30020 10110 10111 10112 10260 10261 10262 10130 10140 \\
                10129; do
            fetch afsc_groundfish_survey_catch "catch_$code" '{"species_code":'"$code"',"$orderby":{"hauljoin":"asc"}}'
        done
        fetch afsc_groundfish_survey_species species '{"$orderby":{"species_code":"asc"}}'
        AKGFMAPS=https://raw.githubusercontent.com/afsc-gap-products/akgfmaps/1fcc7fa598e66a13cdca95be407e1f93c11f50d3
        curl -fsSL -o afsc_bts_strata.gpkg "$AKGFMAPS/inst/extdata/afsc_bts_strata.gpkg"
        echo "1319eb3485c9ee75be96dcbfa5cba44c9d43374d1a8e6a74b7dadfdd62e6fb27  afsc_bts_strata.gpkg" | sha256sum -c
    """
    bibtex = r"""
        @misc{afsc_gap_foss_2026,
          author = {{NOAA Fisheries Alaska Fisheries Science Center, Groundfish Assessment Program}},
          title = {Fisheries One Stop Shop public data: {RACE} division bottom trawl survey data query
                   (tables {AFSC\_GROUNDFISH\_SURVEY\_HAUL}, {AFSC\_GROUNDFISH\_SURVEY\_CATCH},
                   {AFSC\_GROUNDFISH\_SURVEY\_SPECIES})},
          year = {2026},
          howpublished = {\url{https://www.fisheries.noaa.gov/foss/f?p=215:28}},
          note = {Public domain; accessed 2026-10-30 to 2026-11-02}
        }
    """
    curation_comments = """
        We start with the FOSS tables HAUL (35,561 standard hauls, 1982-2026) and CATCH of 17 species codes (201,859 positive catches) from NOAA AFSC's Groundfish Assessment Program, and with GAP's survey strata (akgfmaps), for the Gulf of Alaska strata of the 1984 design. One row per haul and taxon: 391,044 rows.

        - Prediction point: a species at a place in a given survey year, under that year's conditions. At an essential fish habitat (EFH) review, AFSC fits habitat models to the surveys up to about two years before the review (the 2017 review used 1982-2014, Laman et al. 2017, p. 5; the 2022 review 1982-2019, Laman et al. 2022, NOAA-TM-AFSC-459, p. 3), its maps stand until the next review, due "at least every 5 years" (50 CFR 600.815(a)(10), quoted in TM-459, p. 2), and the next review checks the earlier models against the surveys that followed (TM-459, p. 3). Known for the species, place and year: the taxon, the region and design stratum, the position, the date, the depth, and that year's bottom and surface temperatures there, given by the readings taken during the haul. The readings stand in for the year's temperature field, as in the same team's forecasts, which use year-specific bottom temperature kriged onto the tow locations and a 1-km grid (Barnes, Essington, Pirtle et al. 2022, Ecography e06189); the review's maps use long-term means instead ("Rasterized 38-year averages of habitat covariates", TM-459, p. 8). The readings gave no measured gain on rex sole alone: mean R^2 on log1p 0.695 with them and 0.702 without (untuned LightGBM, 3 seeds, the earlier three five-year windows), and a training-years climatology (the 10 nearest training hauls) in their place on the test hauls moves each window by -0.003 to +0.011. Position, depth and bottom temperature are the source's trawl-model covariates (TM-459, Table 3); region, stratum, date and surface temperature are ours. The review fits one model per species; here one table holds 11 taxa with the taxon as a feature (Andrej, 2026-11-02: "add species as a feature and use multiple species as samples"), in the way sat11_hand_algo_runtime ships instance and algorithm rows as an alternative to multi-target modelling.
        - Taxa (Andrej, 2026-11-02, from the AI's proposal, with flathead sole grouped on its second suggestion: "I follow your suggestions"): walleye pollock, Pacific cod, sablefish, Pacific halibut, rex sole, Dover sole, Greenland turbot, shortspine thornyhead, Atheresthes (arrowtooth flounder 10110, unidentified Atheresthes 10111, Kamchatka flounder 10112), Lepidopsetta (unidentified rock sole 10260, northern 10261 and southern rock sole 10262) and Hippoglossoides (flathead sole 10130, Bering flounder 10140, unidentified Hippoglossoides 10129). Four criteria, none a model score: the survey identified the taxon reliably over 1982-2026; the bottom trawl samples it as the survey intends; it is a managed groundfish with an EFH map; it is caught in more than one region. The three groups join species the survey does not tell apart reliably, in time or by region. Code 10111 carries Atheresthes up to 1991 (2,563 of its 2,566 catches) and arrowtooth and Kamchatka flounder start in 1992 (Laman et al. 2017, p. 7); 10260 carries rock sole up to 1995 and northern and southern rock sole start in 1996; FOSS rates flathead sole moderate confidence in every eastern and northern Bering Sea catch of 1982-2025 (12,309 of 12,576; high in the Gulf, the Aleutians and on the slope), where it is told apart from Bering flounder (4,296 catches, all in the Bering Sea, moderate or unrated). As groups, their zeros are absences. Left out: Pacific ocean perch and Atka mackerel, schooling fish off the bottom whose catch sits in a few hauls (10 hauls hold 41% and 40% of each one's squared deviation, together 79% of the variance on counts of the 22 species screened); the Alaska, Aleutian and Bering skates (named to species from 1999); big skate and giant octopus (3.7% and 6.4% of hauls); the sculpins and yellow Irish lord (no fishery). The screen of 22 species counted presence over all years, test windows included (CLEAN-8); the criteria use the identification record and the survey's design, not those counts. Presence by taxon: 12.3% (Greenland turbot) to 82.4% (walleye pollock) of hauls; the table by region is in the decisions. Untuned LightGBM on the nine windows: mean R^2 on log1p per taxon 0.44 (Greenland turbot) to 0.76 (shortspine thornyhead). Identification otherwise: every catch of 1982-2025 of the other codes is rated high confidence, except arrowtooth and Kamchatka flounder (moderate in 31% and 57%, absorbed by the group) and 1.9% of southern rock sole. The 3,968 catches of 2026 are not yet rated.
        - Zeros (52.0% of the rows; a zero-inflated target, not a cap or a placeholder): CATCH holds positive catches only (no row with zero weight), so a haul without a row for a taxon caught none of it, the source's own zero fill (gap_products documentation, "Access via API and R", sec. 10.2, "Create zero-filled data": missing CPUE set to 0 after joining HAUL and CATCH).
        - Target: numbers per square kilometre swept (`cpue_nokm2`), as the 2022 review models numerical abundance (with an area-swept offset) instead of the 2017 memo's fourth-root CPUE (TM-459, pp. 16-17), shipped as `log1p_cpue_no_km2`; a group's catch is the sum over its codes. The 127 haul and taxon rows with a catch weighed but not counted (128 catches) have no numerical CPUE and leave (CLEAN-15).
        - Hauls: all 35,561 are the survey's satisfactory hauls (every performance code is 0 or positive); the 2,659 with a positive code (satisfactory with a noted minor problem) stay, as the survey and the source use them. The code itself is dropped: recorded after the tow about the tow, and presence differs by it (rex sole on the slope 52.2% with code 0, 29.7% with a positive code; within strata 45.9% against 40.8%, so part of the gap is the tow, not the place; the decisions show the share for every taxon).
        - Effort, the survey's exposure (issue 4): the target is the catch per square kilometre swept (CPUE), into which the source folds the area swept (distance fished times net width), the rate per unit of effort (MET-14), and the score is unweighted on this density, as the review maps it over cells of equal area (MET-15). The planned effort is the standard tow, 30 minutes in the Bering Sea (median 0.50 to 0.52 h in each of its three surveys) and 15 minutes in the Gulf of Alaska from 1996 and the Aleutians from 1997 (median 0.27 h; 30 minutes before), so it reaches the models through the region and the date. The realized effort (`distance_fished_km`, `duration_hr`, `net_width_m`, `net_height_m`, `area_swept_km2`, the end position) is dropped: a place in a survey year has no tow (USE-3), and the area swept is the target's denominator (LEAK-41). As free features these columns would gain 0.0028 of the metric under an L2 fit on log1p (1.9% of untuned LightGBM's skill over the taxon means, better in 3 of the 5 windows tested) and nothing under a Poisson fit (exposure study, 2026-11-05). Only for walleye pollock does the tow length also record the catch (LEAK-10): its short tows (under 0.75 of the median duration of their region and year) lie 0.36 above the mean of their stratum and year on log1p numbers per km^2 over all hauls, against -0.36 to +0.08 for the other taxa, and on the EBS shelf its tows under 0.4 h (831) average 8.33 log1p kg per km^2 against 7.35 at full length. Where a short tow catches a taxon, the density is higher for 9 of 11 taxa by the plain means and for all 11 within their stratum and year (pollock 0.55, the others 0.00 to 0.25), which a smaller area swept explains without any stop on the catch, so the cut is claimed for pollock alone (the decision "The tow's effort is dropped"). The unweighted CPUE keeps the bias of the cut pollock tows, as NOAA's design-based index does, which averages the hauls' CPUE with equal weight in each stratum (gapindex, "Background equations").
        - Dropped, the vessel and the time of day (`date_time` kept as the date): a place in a survey year has neither; they describe the sampling event.
        - Dropped, identifiers and copies: `hauljoin` (the join key), `cruisejoin`, `cruise`, `haul`, `station` (the position columns hold the place), `survey`, `survey_name` and `survey_definition_id` (copies of `srvy`), `year` (the date's year).
        - `stratum` is built as region plus stratum number (`EBS-31`): 18 of the 128 stratum numbers are used by two surveys for different areas.
        - Anomaly, repaired: the Gulf of Alaska survey was restratified for 2025 (23 new stratum numbers, none shared with the 59 of 1990-2023), so the 431 GOA hauls of 2025, 10.2% of the newest test window, carried a stratum no training row has. They are placed in the strata of the 1984 design by their start position, with GAP's own polygons (akgfmaps `inst/extdata/afsc_bts_strata.gpkg`, layer `survey_strata`, survey definition 47, design year 1984: the same 59 numbers as FOSS; only the derived codes ship). Every 2025 haul falls inside one polygon; on the 10,878 earlier GOA hauls the join returns FOSS's stratum for 95.5% (the start position lies near a boundary for the rest). Measured on rex sole alone, with the earlier five-year windows, untuned LightGBM (3 seeds) on the newest window: R^2 on log1p 0.607 with the 2025 codes, 0.726 with the hauls placed, 0.715 without the column (on the 2025 GOA hauls -0.57, 0.51 and 0.48); the older windows score 0.723 and 0.634 with the column, 0.711 and 0.628 without. The older hauls are not mapped onto the 2025 design, which was built on survey densities that overlap the test windows.
        - `longitude_east` is the start longitude in degrees east (0-360): the Aleutian survey crosses 180 degrees (2,567 hauls west of it), where the signed longitude jumps from +180 to -180.
        - `depth_m`: in 1993-95 the depth is the headrope depth, without the net height (TM-459, p. 8), a median 1.25 m shallower at the EBS stations than from 1996 on. These are training rows in every window and stay as published.
        - Missing bottom (4.5%) and surface (2.4%) temperatures stay missing.
        - Note: the newest season is provisional. FOSS has not yet rated the 2026 catches (all 3,968 of the 11 taxa lack a `taxon_confidence`), though the 722 hauls of 2026 (44% of the newest window) match a full season (EBS 350 of 350 stations). Before a build, compare with a fresh download: if the 2026 rows change, build from the newer download or end the newest window at 2025. The lower EBS presence of rex sole in 2026 (0.169 against 0.209-0.293 in 2018-2025) alone is no reason to cut.
        - Metric: the source's RMSE on numbers per km^2, taken per taxon and given one vote per species' map (Andrej, 2026-11-02, "Let's do RMSE", then "I follow your suggestions": the AI's option (c), REVIEW.md issue 1). The review draws one EFH map per species: the places with a predicted chance of a catch of at least 5%, cut into the areas holding 95%, 75%, 50% and 25% of the species' predicted abundance (TM-459, pp. 27-28; EFH is "the area inhabited by 95% of a species' population", NMFS 2005, quoted p. 1). Pooled into one RMSE on counts, walleye pollock and rock sole held 79-93% of an untuned model's squared error in every window (pollock 34-84%), seven taxa under 1% each, and the pooled score picked LightGBM fit on raw counts, whose error per taxon is 1.72 times the taxon's spread (0.92 for LightGBM on log1p, 1.08 for each taxon's training mean). `mean_group_normalized_rmse` divides each taxon's RMSE by the spread of its true catches in the window: within a taxon a fixed divisor ranks models as RMSE does, so only the equal weight per taxon is ours. On the nine windows LightGBM on log1p scores 0.90-0.93 and beats the taxon means (1.01-1.23) in all nine; Poisson LightGBM scores 0.86-1.11. `taxon` stays a feature, and its copy `taxon_group` is the metric's group, a scoring column (MET-2 as reworded on 2026-11-05; CC below). Every taxon has a varying catch in every window, so none is left out.
        - Not shipped: the catch of other species in the same haul (unknown at a place nobody sampled, though the 2017 models used concurrent coral, sponge and sea-whip presence, p. 14), and the source's raster covariates (sediment, currents, tides, slope, ocean colour), which FOSS does not hold.
        - Note: the source fits each region and each life stage (by length) apart; FOSS's CATCH has no lengths, so the target counts all sizes, and one table holds all regions with `srvy` as a feature.
        - Anomaly: the timestamps end in "Z" but are local times (Alaska time, AKDT, in GAP's column metadata; hauls run from 05:00 to 23:00); only the date is used. The EBS shelf survey has 350 stations from 2024 (376 before).
        - CC (2026-11-06, Lennart): issue 4 resolved. `taxon` stays a feature and its copy `taxon_group` is the group the metric reads, a scoring column (MET-2 as reworded on 2026-11-05, asked in PR #47's review that day); the tow's effort stays out, the cut is claimed for walleye pollock only, and the score stays unweighted on the density (USE-3, LEAK-10, LEAK-41, MET-15). Supersedes the metric's reading of the feature `taxon` (Andrej, 2026-11-02, under MET-2 as amended then) and the note that the tow length responds to the catch, measured on pollock and read for every taxon: the exposure study of 2026-11-05 found the densities of short tows that catch a taxon higher for nearly every taxon, which a smaller area swept explains, while over all hauls only pollock's short tows stand well above their cells (+0.36 on log1p, the others -0.36 to +0.08). The scores do not change: the copy holds the same values.
    """

    # Task
    target = "log1p_cpue_no_km2"
    problem_type = "regression"
    metric = Metric.stand_in(
        "mean_group_normalized_rmse",
        original=(
            "RMSE of predicted against observed numerical abundance at the trawl stations, cross-validated, by which "
            "the 2022 EFH review selects and weights its habitat models, one model and one RMSE per species and life "
            "stage (also reported: Spearman's rho, ROC AUC, Poisson deviance explained)"
        ),
        reason=(
            "One table holds 11 taxa, so the source's RMSE per species is 11 numbers; pooled into one RMSE, walleye "
            "pollock and rock sole hold 79-93% of the squared error and the score picks the model worst for the other "
            "maps. Each taxon's RMSE over its spread, averaged, keeps the source's RMSE within a taxon (a fixed "
            "divisor ranks models as RMSE does) and gives each species' map one vote."
        ),
        reference="https://repository.library.noaa.gov/view/noaa/48659",
        definition=(
            "Per taxon, RMSE of the catch in numbers per km^2 swept over the test rows, after the inverse of log1p, "
            "divided by the standard deviation of the taxon's true catches in the window (ddof 0); the mean over the "
            "11 taxa, lower is better (equal to the mean over taxa of sqrt(1 - R^2) on counts). A taxon whose catches "
            "do not vary in a window is left out; none is in the nine windows."
        ),
        inputs={"group": "taxon_group"},
        target_transform="log1p",
    )
    scoring_columns = (
        ScoringColumn(
            column="taxon_group",
            role="group",
            used_by="mean_group_normalized_rmse",
            description=(
                "a copy of the feature taxon (11 taxa): the metric divides each taxon's RMSE by the spread of its "
                "true catches in the window and averages the 11; taxon itself stays a feature"
            ),
        ),
    )

    # Splits: nine two-year windows (one survey of every region each), each trained on every earlier survey.
    accepted_check_warnings = {
        "task_target_value_dominant": (
            "52% zeros: hauls that caught none of the row's taxon (Andrej, 2026-11-03: zero-inflated targets are natural for these tasks and a core challenge)."
        ),
    }
    temporal = Temporal(
        on="date",
        splits=TemporalSplits(window=2, unit="years", cutoffs=(2009, 2011, 2013, 2015, 2017, 2019, 2021, 2023, 2025)),
    )
    splits_comment = """
        Expanding-window temporal splits by survey year: nine test windows of two calendar years (2025-2026 back to
        2009-2010; the 2019-2020 window holds only 2019, as no survey ran in 2020), newest first, each trained on every
        earlier survey, without a gap (Andrej, 2026-11-02: "no need to do five years. Also no planning gap is
        required"). Two years is the survey cycle: since 2005 the Gulf of Alaska is surveyed in odd years and the
        Aleutians in even years, beside the yearly eastern Bering Sea shelf, so each window holds one survey of every
        region. Nine windows, as many as an IID task of this size would get folds (SPLIT-15); the oldest trains on 54% of
        the rows, and a tenth (2007-2008) would train on 49%. No gap, an exception to SPLIT-10: the 2022 review states
        no delay between a survey and its use, only the surveys it used (1982-2019, TM-459, p. 3), and FOSS held the
        hauls of the 2026 summer by 30 October 2026, so a model refit after each season has every earlier season.
        All rows of a haul share its date, so a haul's taxa stay on one side. The source scored its models on hauls
        held out at random (Laman et al. 2017, p. 16; TM-459, p. 20); the windows ask how a model holds up on the
        next survey cycle instead, as the same team tests its models by retrospective forecasts (Barnes, Essington,
        Pirtle et al. 2022, Ecography e06189), and the 2022 review "assessed the forecasting accuracy of the 2017 SDM
        approach" (TM-459, p. 3). Most test hauls are at a station seen in training (all of the eastern Bering Sea
        grid; Gulf of Alaska stations are drawn anew for each survey).
    """

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        codes = [code for taxon_codes in TAXA.values() for code in taxon_codes]
        return {
            "haul": _read_pages(raw_dir, "haul"),
            "catch": pd.concat([_read_pages(raw_dir, f"catch_{code}") for code in codes], ignore_index=True),
            "goa_strata": _read_goa_strata(raw_dir / STRATA_FILE),
        }

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        haul, catch = raw["haul"], raw["catch"]
        code_taxon = {code: taxon for taxon, codes in TAXA.items() for code in codes}
        assert set(catch["species_code"]) == set(code_taxon)
        assert not catch.duplicated(["hauljoin", "species_code"]).any()
        assert catch["hauljoin"].isin(haul["hauljoin"]).all()
        assert catch["cpue_kgkm2"].gt(0).all()
        df = haul.copy()
        # 1. The date of the haul (the clock time is local, though marked "Z"; dropped with the sampling details).
        df["date"] = pd.to_datetime(df["date_time"].str[:10], format="%Y-%m-%d")
        # 2. The GOA hauls of the 2025 design go into the strata of the 1984 design by their start position (GAP's
        #    polygons), so the column keeps one coding; then one key per survey, as numbers repeat across surveys.
        goa = df["srvy"].eq("GOA")
        redesigned = goa & df["date"].dt.year.ge(GOA_NEW_DESIGN_FROM)
        old_numbers = set(raw["goa_strata"]["stratum"].astype(int))
        assert set(df.loc[goa & ~redesigned, "stratum"]) == old_numbers
        assert not df.loc[redesigned, "stratum"].isin(old_numbers).any()
        placed = _goa_stratum_1984(
            df.loc[redesigned, "latitude_dd_start"], df.loc[redesigned, "longitude_dd_start"], raw["goa_strata"]
        )
        assert (placed >= 0).all(), "a GOA haul of the 2025 design lies outside every 1984 stratum"
        df.loc[redesigned, "stratum"] = placed
        df["stratum"] = df["srvy"] + "-" + df["stratum"].astype(str)
        # 3. Longitude in degrees east, continuous across 180 degrees in the Aleutians.
        df["longitude_east"] = df["longitude_dd_start"] % 360
        df = df.rename(columns={"latitude_dd_start": "latitude"})
        # 4. One row per haul and taxon, zero-filled (the source's recipe): a group's catch is the sum over its
        #    species codes, and a catch weighed but not counted leaves its row, as it has no numerical CPUE (CLEAN-15).
        catch = catch.assign(taxon=catch["species_code"].map(code_taxon))
        keys = [catch["hauljoin"], catch["taxon"]]
        cpue = catch["cpue_nokm2"].groupby(keys).sum()
        cpue = cpue.where(~catch["cpue_nokm2"].isna().groupby(keys).any())
        grid = pd.MultiIndex.from_product([df["hauljoin"], list(TAXA)], names=["hauljoin", "taxon"])
        cpue = cpue.reindex(grid, fill_value=0.0).dropna().rename("cpue_nokm2").reset_index()
        df = cpue.merge(df, on="hauljoin", how="left", validate="many_to_one")
        df["log1p_cpue_no_km2"] = np.log1p(df["cpue_nokm2"])
        # 5. The metric's group: a copy of the feature `taxon`, shipped as a scoring column (MET-2); `taxon` stays a
        #    feature.
        df["taxon_group"] = df["taxon"]
        return drop_columns(df, [*DROPPED_HAUL_COLUMNS, "date_time", "longitude_dd_start", "cpue_nokm2"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=["taxon", "srvy", "stratum", "taxon_group"],  # taxon_group: the metric's, never a feature
            datetime={"date": "%Y-%m-%d"},
        )

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        haul, catch = raw["haul"], raw["catch"]
        code_taxon = {code: taxon for taxon, codes in TAXA.items() for code in codes}
        caught = (
            catch.assign(taxon=catch["species_code"].map(code_taxon), caught=True)
            .drop_duplicates(["hauljoin", "taxon"])
            .pivot(index="hauljoin", columns="taxon", values="caught")
            .reindex(index=haul["hauljoin"], columns=list(TAXA))
            .notna()
        )
        caught.index = haul.index
        by_region = caught.groupby(haul["srvy"]).mean().T.round(3).rename_axis("taxon")
        positive_code = haul["performance"].ne(0).map({False: "code 0", True: "positive code"})
        by_code = caught.groupby(positive_code).mean().T.round(3).rename_axis("taxon")
        year = pd.to_datetime(haul["date_time"].str[:10], format="%Y-%m-%d").dt.year
        goa = haul["srvy"].eq("GOA")
        join = {}
        for label, rows in {
            "GOA 1990-2023 (1984 design)": goa & year.lt(GOA_NEW_DESIGN_FROM),
            "GOA 2025 (2025 design)": goa & year.ge(GOA_NEW_DESIGN_FROM),
        }.items():
            placed = _goa_stratum_1984(
                haul.loc[rows, "latitude_dd_start"], haul.loc[rows, "longitude_dd_start"], raw["goa_strata"]
            )
            same = placed == haul.loc[rows, "stratum"].to_numpy()
            join[label] = {
                "hauls": int(rows.sum()),
                "inside a 1984 stratum": round(float(np.mean(placed >= 0)), 3),
                "join gives FOSS's stratum": round(float(np.mean(same)), 3) if label.startswith("GOA 1990") else "-",
            }
        return [
            Decision(
                "The 11 taxa: where each is caught",
                "The share of hauls with a catch of each taxon by survey region: most zeros are habitat outcomes "
                "within a region, and every taxon is caught in more than one region (curation notes).",
                by_region,
            ),
            Decision(
                "The 2025 GOA hauls are placed in the strata of the 1984 design",
                "GAP's polygons of the 1984 design, joined on the start position, hold every haul of the 2025 design; "
                "on the earlier GOA hauls the join returns FOSS's own stratum except where a tow starts near a "
                "boundary, so the column keeps one coding across the redesign.",
                pd.DataFrame(join).T.rename_axis("hauls of"),
            ),
            Decision(
                "The performance code is dropped as a feature",
                "Share of hauls with a catch of each taxon by performance code: the code is recorded after the tow "
                "and the catch rate differs by it, so as a feature it would carry part of the outcome; the hauls "
                "themselves stay.",
                by_code,
            ),
            Decision(
                "The tow's effort is dropped; the cut is claimed for walleye pollock only",
                "Short tows (under 0.75 of the median duration of their region and year) against the mean of their "
                "stratum and year, in the cells that hold short and full tows: the share of hauls with a catch, and "
                "the log1p numbers per km^2 over all hauls and over the hauls with a catch. Short tows catch most "
                "taxa less often, and where they catch one its density is higher, as a smaller area swept gives "
                "without any stop on the catch. Over all hauls walleye pollock alone stands well above its cells: "
                "its tows end early on a large catch (curation notes).",
                _short_tows(haul, catch),
            ),
        ]
