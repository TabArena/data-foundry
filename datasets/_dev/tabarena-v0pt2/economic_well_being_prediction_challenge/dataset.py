"""Curated economic well-being prediction task (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.time_basis import TimeBasis
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Grouping,
    Metric,
    Source,
    SplitPlan,
    TaskSummary,
    decode,
    drop_columns,
)
from data_foundry.v2.splits import SPLIT_RANDOM_STATE, grouped_splits

CODE_LABELS = {"urban_or_rural": {"R": "Rural", "U": "Urban"}}

# Whole countries in 9 folds, one repeat: every country is tested once (seven folds of 3 countries, two of 2).
N_COUNTRY_FOLDS = 9

# The raw files, pinned: Zindi's Train.csv and Test.csv, the source's cluster table and the shoreline.
SOURCE_TABLE = "dhs_wealth_index.csv"
COASTLINE = "ne_50m_coastline.geojson"
RAW_SHA256 = {
    "Train.csv": "caf159ff5c84630ca3ec61793ab362073cfed396e348ecca12f60f4d13efa93c",
    "Test.csv": "e1d61ea14428f23643547b5a322ffc9015e4df0fc9bb798ec675cf2475c149ab",
    SOURCE_TABLE: "e68c0466599a6fa3cfc6bcfaa9e5626276ed1e50f184deed7ed4f89c2e0efba8",
    COASTLINE: "271f1c4c1908312bac6b29d158ea1356544beafc129f260005300913aa5ea283",
}
# Written by `_prepare_raw_files`: Test.csv's accepted rows with their recovered Target, and the join's per-row check
# (no coordinates, no survey or cluster ids).
LABELLED_TEST = "Test_labelled.csv"
JOIN_CHECK = "join_check.csv"

# The join (review issue 9): Zindi's distance to the capital is recomputed exactly at the source table's coordinates
# (WGS84 ellipsoid, from a capital point fitted per country); the shoreline distance (Natural Earth) differs from
# Zindi's by kilometres, so it only breaks near-ties. A match is accepted when it is unambiguous: the distance to the
# capital agrees within CAPITAL_TOL_KM, no other cluster of the cell agrees as well, and no other cluster of the cell
# sits at the same coordinate.
CAPITAL_TOL_KM = 0.002
COST_SCALE_KM = {"capital": 0.002, "shoreline": 3.0}
RIGHT_CLUSTER = 0.0014  # Zindi's Target is the rescaled index plus a per-row deviation of about +-0.0013
CAPITAL_START = {  # the official capitals, the start of the fit
    "Angola": (-8.84, 13.23),
    "Benin": (6.50, 2.60),
    "Burkina Faso": (12.37, -1.53),
    "Cameroon": (3.87, 11.52),
    "Central African Republic": (4.37, 18.56),
    "Cote d'Ivoire": (6.82, -5.28),
    "Democratic Republic of Congo": (-4.32, 15.31),
    "Ethiopia": (9.03, 38.74),
    "Ghana": (5.56, -0.20),
    "Guinea": (9.64, -13.58),
    "Kenya": (-1.29, 36.82),
    "Lesotho": (-29.31, 27.48),
    "Malawi": (-13.96, 33.79),
    "Mali": (12.64, -8.00),
    "Mozambique": (-25.97, 32.57),
    "Nigeria": (9.08, 7.40),
    "Rwanda": (-1.95, 30.06),
    "Senegal": (14.72, -17.47),
    "Sierra Leone": (8.48, -13.23),
    "Swaziland": (-26.31, 31.14),
    "Tanzania": (-6.16, 35.75),
    "Togo": (6.13, 1.22),
    "Uganda": (0.35, 32.58),
    "Zambia": (-15.39, 28.32),
    "Zimbabwe": (-17.83, 31.05),
}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _haversine_km(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(np.radians, (lat1, lon1, lat2, lon2))
    a = np.sin((lat2 - lat1) / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2) ** 2
    return 2 * 6371.0088 * np.arcsin(np.sqrt(a))


def _ellipsoid_km(lat1, lon1, lat2, lon2):
    """Lambert's formula for the WGS84 ellipsoid (agrees with Zindi's distance to the capital within 0.002 km)."""
    a, f = 6378.137, 1 / 298.257223563
    b1 = np.arctan((1 - f) * np.tan(np.radians(lat1)))
    b2 = np.arctan((1 - f) * np.tan(np.radians(lat2)))
    dl = np.radians(lon2 - lon1)
    sig = 2 * np.arcsin(np.sqrt(np.sin((b2 - b1) / 2) ** 2 + np.cos(b1) * np.cos(b2) * np.sin(dl / 2) ** 2))
    sig = np.maximum(sig, 1e-12)
    p, q = (b1 + b2) / 2, (b2 - b1) / 2
    x = (sig - np.sin(sig)) * np.sin(p) ** 2 * np.cos(q) ** 2 / np.cos(sig / 2) ** 2
    y = (sig + np.sin(sig)) * np.cos(p) ** 2 * np.sin(q) ** 2 / np.sin(sig / 2) ** 2
    return a * (sig - f / 2 * (x + y))


def _shoreline_km(lat: np.ndarray, lon: np.ndarray, geojson: Path) -> np.ndarray:
    """Distance to the Natural Earth coastline, its segments densified to 0.1 km."""
    from sklearn.neighbors import BallTree

    pts = []
    for feature in json.loads(geojson.read_text())["features"]:
        g = feature["geometry"]
        for line in g["coordinates"] if g["type"] == "MultiLineString" else [g["coordinates"]]:
            a = np.asarray(line, dtype=float)
            if len(a) > 1:
                n = np.maximum(1, np.ceil(_haversine_km(a[:-1, 1], a[:-1, 0], a[1:, 1], a[1:, 0]) / 0.1)).astype(int)
                for i in range(len(a) - 1):
                    pts.append(a[i] + np.linspace(0, 1, n[i], endpoint=False)[:, None] * (a[i + 1] - a[i]))
            pts.append(a[-1:])
    coast = np.vstack(pts)
    coast = coast[(coast[:, 0] > -40) & (coast[:, 0] < 70) & (coast[:, 1] > -50) & (coast[:, 1] < 45)]
    _, nn = BallTree(np.radians(coast[:, ::-1]), metric="haversine").query(np.radians(np.c_[lat, lon]), k=30)
    return _ellipsoid_km(lat[:, None], lon[:, None], coast[nn, 1], coast[nn, 0]).min(axis=1)


def _fit_capitals(zindi: pd.DataFrame, src: pd.DataFrame) -> dict[str, tuple[float, float]]:
    """Per country, the capital point whose distances, sorted within each country x year x urban cell, best match
    Zindi's released distances (assignment-free).
    """
    from scipy.optimize import minimize

    keys = ["country", "year", "urban_or_rural"]
    cells_z = {k: np.sort(g["dist_to_capital"].to_numpy()) for k, g in zindi.groupby(keys)}
    cells_s = {k: g[["LATNUM", "LONGNUM"]].to_numpy() for k, g in src.groupby(keys)}
    capitals = {}
    for country, start in CAPITAL_START.items():
        cells = [k for k in cells_z if k[0] == country and k in cells_s]

        def loss(p, cells=cells):
            total = 0.0
            for k in cells:
                a = cells_z[k]
                b = np.sort(_ellipsoid_km(cells_s[k][:, 0], cells_s[k][:, 1], p[0], p[1]))
                m = min(len(a), len(b))
                total += np.abs(a[:m] - b[:m]).sum()
            return total

        fit = minimize(
            loss, np.array(start), method="Nelder-Mead", options={"xatol": 1e-6, "fatol": 1e-6, "maxiter": 4000}
        )
        capitals[country] = (float(fit.x[0]), float(fit.x[1]))
    return capitals


def _join(zindi: pd.DataFrame, src: pd.DataFrame) -> pd.DataFrame:
    """Assign Zindi's rows one-to-one to the source table's clusters within country x year x urban (the distance to
    the capital decides, the shoreline breaks near-ties) and flag the ambiguous matches.
    """
    from scipy.optimize import linear_sum_assignment

    keys = ["country", "year", "urban_or_rural"]
    cells_s = dict(iter(src.groupby(keys)))
    out = []
    for k, g in zindi.groupby(keys):
        s = cells_s.get(k)
        if s is None:
            out += [
                {"row": i, "wealthpooled": np.nan, "capital_gap_km": np.nan, "near_tie": False, "shared": False}
                for i in g.index
            ]
            continue
        dc = np.abs(g["dist_to_capital"].to_numpy()[:, None] - s["capital_km"].to_numpy()[None, :])
        ds = np.abs(g["dist_to_shoreline"].to_numpy()[:, None] - s["shoreline_km"].to_numpy()[None, :])
        ri, ci = linear_sum_assignment(dc / COST_SCALE_KM["capital"] + ds / COST_SCALE_KM["shoreline"])
        candidates = (dc <= CAPITAL_TOL_KM).sum(axis=1)
        place = s["LATNUM"].round(6).astype(str) + "," + s["LONGNUM"].round(6).astype(str)
        shared = place.map(place.value_counts()).to_numpy() > 1
        for r, c in zip(ri, ci):
            out.append(
                {
                    "row": g.index[r],
                    "wealthpooled": s["wealthpooled"].iloc[c],
                    "capital_gap_km": dc[r, c],
                    "near_tie": candidates[r] > 1,
                    "shared": bool(shared[c]),
                }
            )
        out += [
            {"row": g.index[r], "wealthpooled": np.nan, "capital_gap_km": np.nan, "near_tie": False, "shared": False}
            for r in sorted(set(range(len(g))) - set(ri))
        ]
    m = pd.DataFrame(out).set_index("row").sort_index(kind="stable")
    m["accepted"] = (m["capital_gap_km"] <= CAPITAL_TOL_KM) & ~m["near_tie"] & ~m["shared"]
    return m


class EconomicWellBeingPredictionChallenge(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="What is a survey cluster's wealth index in a country without surveys of its own?",
        use_case=(
            "An agency maps local wealth today for the past survey years of a country without surveys of its own, "
            "filling the gaps between the more expensive surveys to inform geographic targeting of support. It holds "
            "every map layer as read today. A model trained on the surveys of other countries is evaluated on every "
            "survey of a held-out country."
        ),
        row=(
            "One survey cluster: 28,618 rows, 25 countries, 1994–2016; 21,454 from the released training file and "
            "7,164 from the source's test file, whose labels are recovered from the source's cluster table."
        ),
        predicted=(
            "The source's cluster-average, asset-related wealth index, from zero to one with higher values "
            "indicating greater wealth. It describes the survey year, not future income."
        ),
        known=(
            "The survey year, urban/rural context, built-up area by epoch through 2014, land cover, water, population "
            "density, nighttime lights and distances, each as read today: one read of each layer serves every row, "
            "whatever its survey year, as the source released them. The prediction point is today, so later reads are "
            "known."
        ),
        split=(
            "Whole countries held out with all their survey years, in 9 folds of 2 or 3 countries: each of the 25 "
            "countries is tested once and the other 22 or 23 train; the source's own 7 test countries are among them."
        ),
        changes=(
            "We add the source's 7 test countries, with labels recovered from the source's cluster table, and keep "
            "the training file's rows and labels as released; 30 test rows whose cluster cannot be told apart from a "
            "neighbour's are left out. We hold out whole countries and drop the row ID. We keep the source's feature "
            "values, the later reads of the layers included."
        ),
        fit="approximate",
        fit_reason=(
            "The source documents neither its label (a pooled asset index, rescaled) nor several layer epochs; "
            "recovered test-file labels differ from the hidden ones by up to about 0.0013, the source's per-row "
            "deviation. Every layer is the read the agency holds today (Andrej, 2026-11-24). The test stands for a "
            "country never surveyed, not for the gap between two surveys of one country."
        ),
    )

    unique_name = "economic_well_being_prediction_challenge"
    sources = (
        Source(
            role="publication",
            platform="Zindi",
            url="https://zindi.world/competitions/aims-data-science-hackathon",
            license=(
                "CC BY-SA 4.0 (competition rules); the labels are cluster-level wealth indices from DHS surveys, whose "
                "terms of use bar commercial use; used for non-commercial academic research only."
            ),
            year="2021",
            bibtex=r"""
        @misc{Zindi2021EconomicWellBeing,
          author = {{Zindi} and {AIMS} and {Microsoft}},
          title = {AIMS Data Science Hackathon and Economic Well-Being Prediction Challenge},
          year = {2021},
          howpublished = {\url{https://zindi.world/competitions/aims-data-science-hackathon}},
          note = {Public Economic Well-Being challenge rerun on Zindi}
        }
    """,
        ),
    )
    domain = "social science"
    data_tags = ("Spatial",)
    split_leaf = "L-PLACE.groups"
    time_basis = TimeBasis(
        "UnseenGroup",
        "survey clusters of 25 countries, 1994-2016; a test country stands for a country without surveys of its own, "
        "mapped for the years the other countries' surveys cover, which are all in training. Not tested: a later year.",
    )
    download_description = """
        Obtain Train.csv and Test.csv from the Economic Well-Being Prediction Challenge data page:
        https://zindi.world/competitions/economic-well-being-prediction-challenge/data
        (login or acceptance of the source terms may be needed; an independent publisher checksum is unavailable).
        Train.csv is 5,829,604 bytes, SHA-256 caf159ff5c84630ca3ec61793ab362073cfed396e348ecca12f60f4d13efa93c; public
        copies on GitHub have the same SHA-256 (checked 2026-11-21). Test.csv is 1,805,196 bytes, SHA-256
        e1d61ea14428f23643547b5a322ffc9015e4df0fc9bb798ec675cf2475c149ab, equal to the public copy at
        https://raw.githubusercontent.com/simiel/economic-well-being-prediction-competition/226eb21c40bb46b7d24319c0ee0a5b896e01ee4a/Test.csv
        Then the source's cluster table (Yeh et al. 2020, MIT) and the Natural Earth coastline, both at pinned commits:

        d=local-data-warehouse/economic_well_being_prediction_challenge && mkdir -p $d
        curl -sSfL -o $d/dhs_wealth_index.csv https://raw.githubusercontent.com/sustainlab-group/africa_poverty/cb769c744872e52c35f9c60e94b0dc2a696d389a/data/dhs_wealth_index.csv
        curl -sSfL -o $d/ne_50m_coastline.geojson https://raw.githubusercontent.com/nvkelso/natural-earth-vector/a726d63745ff99cf26a03ae1c7cfb0d4f12fa517/geojson/ne_50m_coastline.geojson

        dhs_wealth_index.csv is 5,073,675 bytes, SHA-256 e68c0466599a6fa3cfc6bcfaa9e5626276ed1e50f184deed7ed4f89c2e0efba8;
        ne_50m_coastline.geojson is 1,640,858 bytes, SHA-256
        271f1c4c1908312bac6b29d158ea1356544beafc129f260005300913aa5ea283. `_prepare_raw_files` checks all four hashes and
        writes Test_labelled.csv and join_check.csv next to them (no coordinates, no survey or cluster ids); the build
        reads only local files. The original AIMS task and the public rerun describe the same task; no byte-for-byte
        comparison against the original AIMS download has been made.
    """
    curation_comments = """
        We start with the curator-provided Train.csv and Test.csv from Zindi's Economic Well-Being Prediction Challenge, and recover the labels of Test.csv, which Zindi never released, from the source's cluster table.

        - Test.csv joined (Andrej, 2026-11-24, review issue 9, option b): the competition's rows are the clusters with coordinates of the africa_poverty cluster table of Yeh et al. 2020 (`data/dhs_wealth_index.csv` of github.com/sustainlab-group/africa_poverty at commit cb769c74, MIT); Train.csv and Test.csv together hold 28,648 of its 28,649 clusters with coordinates, in 25 countries (cluster counts equal in 95 of 96 country-years; Nigeria 2008 rural has one source cluster more). `_prepare_raw_files` assigns each Zindi row one-to-one to a cluster within country x year x urban: the distance to the capital is recomputed at the table's coordinates on the WGS84 ellipsoid from a capital point fitted per country to Zindi's released distances (every pair agrees within 0.002 km), and the distance to Natural Earth's 50 m coastline (pinned commit), which differs from Zindi's shoreline by a median 2.4 km, only breaks near-ties. The coordinates, survey ids and cluster ids stay in the raw folder and are never shipped.
        - Recovered labels: Target = 0.245034 x wealthpooled + 0.343664, refit on Train.csv (21,336 rows within 0.01 of the first fit). On Train.csv the join finds the right cluster (recovered label within 0.0014 of Target) for 21,321 of 21,454 rows (99.38%); Zindi's Target is the rescaled index plus a per-row deviation spread over about +-0.0013 (sd 0.0007 and mean 0 in every country-year), so the recovered Test.csv labels differ from Zindi's hidden values by up to about 0.0013. The 133 Train.csv misses are 131 Central African Republic 1994-95 rows at shared locality points, which no distance separates, and one Cameroon 2004 pair 0.0012 km apart in distance to the capital.
        - The bar, matched to the data (Andrej, 2026-11-24): a match is accepted only where it is unambiguous, the distance to the capital within 0.002 km, no other cluster of the cell within 0.002 km of it as well, and no other cluster of the cell at the same coordinate. On Train.csv the accepted matches are 21,146 rows, and all 21,146 give the right cluster; the build stops if this share falls below 99.9%. Train.csv rows keep their released Target whatever the match. Of Test.csv's 7,194 rows, 7,164 are accepted and added (none at a shared coordinate; 30 rows of Angola, Benin, Burkina Faso, Uganda and Zimbabwe have a second cluster within 0.002 km and are left out). No source indicator column ships: the framework has no non-input column besides the target, the group and the metric's scoring columns, and a row's file follows from its country.
        - Prediction point: today. The agency maps the past survey years of a country without surveys of its own (the source's aim, "filling in the gaps between the more expensive surveys"), with a model fitted to the surveys of other countries, and holds every layer as read today. So every input is used as the source released it, one read of each layer on rows of every survey year, as the source itself did (its 2015-2019 land cover on rows from 1998). This replaces, for this use case, Myunghwan's rule of 2026-10-31 against fields that describe a later state than the survey (Andrej, 2026-11-24, review issue 4). Calendar-year timing stays the accepted approximation (Myunghwan, 2026-11-02).
        - Target: Myunghwan accepted prediction of the supplied source index with approximate fit when approving ship (2026-11-02). Retain all 21,454 supplied labels of Train.csv unchanged. They are a cluster-average wealth index on 0–1, not currency or a poverty probability: the source table's `wealthpooled` (an asset index from one principal component pooled over all surveys, averaged per cluster), min-max rescaled over the 25 countries, plus Zindi's per-row deviation of about +-0.0013 (review issue 9).
        - Potential leak, kept on purpose: the index was rescaled with one min-max over the whole release, rows of later years included (exactly one 0, Ethiopia 2005, and one 1, Nigeria 2013, both Train.csv rows; in those two countries' splits one test label sets an end of the scale). An affine rescale passes no row-level information; revisit if the source documents a per-survey normalisation.
        - Keep the four landcover_* columns (crops, urban, permanent and seasonal water within 10 km): the source links a 2015-2019 Copernicus product without saying which epoch was sampled, so for rows before 2015 they are a later read, which the agency mapping today holds. Built-up by epoch (GHSL, through 2014) is kept unmasked on every row for the same reason: it is today's layer, also where an epoch ends after the survey year.
        - Water, population density and nighttime lights are each one read used on every row; their represented epochs are not documented. Water describes stable water bodies, and at the same place it does not change between surveys. Potential leak, kept on purpose: ghsl_pop_density is most likely GHS-POP's 2015 epoch (it responds to 2000-2014 construction like the 2015-2019 land cover, log coefficient 0.46 against 0.32) and is used on the 24,196 rows before 2015; kept because the agency maps today with today's layers (review issue 4). Potential leak, kept on purpose: nighttime_lights is one read of an undated layer (values up to 383, so VIIRS from 2012 or a radiance-calibrated DMSP composite) used on rows from 1994 on; kept because the agency maps today with today's read (review issue 5). At the same place it does not change over 13 or more years (log change -0.016) while the target rises by +0.158, so it carries no later state of the label; revisit if the source names the product.
        - Same-place check (2026-11-21, on Train.csv): 1,204 pairs of clusters of one country at the same place (both distances within 0.3 km, pre-1975 built-up within 0.005), surveyed up to 22 years apart. Water, population and lights do not change between them (population and lights: mean log change within ±0.035 in every band of years), while the target rises by +0.158 at 13 or more years. The country-year means of these inputs differ in all 52 consecutive comparisons only because each survey samples different clusters; the fixed 2000-2014 layer differs in all 52 for the same reason.
        - dist_to_capital and dist_to_shoreline are distances in km to the official capital and to the shoreline: coastal clusters lie about 210 km from it in Côte d'Ivoire, 480 km in Nigeria and 350 km in Tanzania (Yamoussoukro, Abuja and Dodoma, not Abidjan, Lagos or Dar es Salaam), and within a few km in Senegal and Sierra Leone.
        - Decode the source’s R/U urban_or_rural codes to Rural/Urban categorical labels (CLEAN-12, current main). Meanings are unchanged; unknown codes raise. Keep it as a category: the source starter notebook explicitly uses it. Generic metadata boilerplate does not identify this field as prohibited. Country is the group, not an input; ID is dropped; year remains a numeric input. No country/year frequency encodings or full-data statistics are added.
        - Keep all rows and numeric scales. Original labels are unique, and repeated predictor profiles are not established collection errors. 129 rows share all inputs with a row of another target value: they are Central African Republic clusters of 1994-95, whose positions are locality points (41 exact location groups, 205 rows, some holding a Rural and an Urban row at one point); Test.csv has no clusters at a shared coordinate. Country groups keep them on one side. Zero numeric measurements remain zero; the source documents no alternative missing-code convention (population density is 0 on 2,262 rows, 2,250 of them with no built-up in any GHSL epoch).
        - Licence: the competition grants CC BY-SA 4.0. The labels are cluster means of DHS and Malaria Indicator Surveys (the competition does not name DHS; the africa_poverty cluster table of Yeh et al. 2020 holds the same index), and the DHS terms of use (https://dhsprogram.com/data/terms-of-use.cfm) bar any marketing or commercial venture and the redistribution of DHS micro-level data; the shipped rows are cluster-level indices, not micro-level data, and carry no coordinates, survey ids or cluster ids (the join of review issue 9 reads coordinates only in the raw folder). The benchmark uses the data for non-commercial academic research only (Andrej, 2026-11-24, review issue 10).
        - Scope: the inputs are mapped quantities aggregated to 5 km (built-up fractions, modelled population, calibrated lights, water, land-cover fractions) plus GIS distances, read as measurements of a place, as for covertype, the GeoAI NO2 challenge and AirQo; no raw reflectance is used to recognise image content (the reason crop-type datasets were rejected).
        - Metric: RMSE, the source's metric, scores the wealth level. With one country per split, one offset for the whole country was 0.1-53% of a split's squared error for a random forest (Lesotho lowest, Malawi highest; mean 17%, measured 2026-11-24 on the earlier one-country splits of 16 countries), while geographic targeting acts on the ranking of places within a country, which RMSE scores only in part.
        - Temporal limitation: survey year orders label content. Target harmonization using future actual states cannot be ruled out. Label publication dates are absent, a limitation on literal historical deployment claims rather than an extra acceptance gate for this task, whose prediction point is today.
        - Split walk (the split decision tree, SPLIT-36, from the record's collection type Survey): [SUR.meets] the model estimates wealth for a country without surveys of its own, a place outside what the training surveys covered → Place step → [PLACE.several] the data holds 25 countries: yes → leaf L-PLACE.groups, Grouped · `UnseenGroup`, whole countries held out with all their survey years. The definition ships this leaf's split (Andrej, 2026-11-24), in 9 folds of 2 or 3 countries, each of the 25 countries tested once (the source's own 7 test countries among them), as the source tests unseen countries over all years (Andrej, 2026-11-25).
    """

    target = "Target"
    problem_type = "regression"
    metric = Metric.source(
        "rmse",
        original="Root Mean Squared Error",
        reference="https://zindi.world/competitions/economic-well-being-prediction-challenge",
    )
    grouping = Grouping(
        on="country",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition=(
            "One group is a country, held out with all its survey years: a test country stands for a country without "
            "surveys of its own, as in the source's test of 7 countries over 1998-2016, which the dataset holds too. "
            "Every country is tested once, in 9 folds of 2 or 3 countries."
        ),
    )
    splits_comment = """
        Whole countries in 9 folds, one repeat (Andrej, 2026-11-25): each of the 25 countries is held out once with
        all its survey years, two or three countries per fold (seven folds of 3, two of 2), assigned by the framework's
        grouped k-fold with shuffled countries and its fixed seed; each split trains on the other 22 or 23 countries.
        This replaces leave one country out over the 16 countries surveyed in 2014-2016 (2026-11-24), which never
        tested 9 countries, Benin, one of the source's own test countries, among them; under a prediction point of
        today an older survey is as valid a test as a newer one. Folds of several countries were chosen over one
        country per split for larger test sides (about 3,200 rows per fold against 1,150), and one repeat over 3 x 3
        because the repeats of repeated folds share most of their training countries. Measured (2026-11-25, 20 draws
        of the country folds per design, four models, mean RMSE over splits; reference: leave one country out over all
        25): 1 x 9 is off the reference by +0.0010 to +0.0024 and ranks the models as the reference does in 90% of
        draws; 3 x 3, which trains on 16-17 countries, is off by +0.0020 to +0.0044, in 85%, and halves the gap
        between LightGBM and a random forest (-0.0021 against -0.0039 on the reference; 1 x 9: -0.0034). Its scores
        vary less between draws (SD 0.0008-0.0013 against 0.0010-0.0017), less than its bias. All 7 of the source's own test
        countries (Test.csv, 1998-2016) are tested, with their recovered labels. The split decision tree reaches
        L-PLACE.groups for this survey (Survey: a country without surveys of its own lies outside what the training
        surveys covered; the place step: several countries). A test country's clusters of every year are on the test
        side; no later year is tested.
    """
    accepted_check_warnings = {
        "groups_test_groups_few": "Accepted (Andrej, 2026-11-25): a test country stands for a country without "
        "surveys of its own, so two or three whole countries per fold is the task (9 folds, each of the 25 countries "
        "tested once). The signal carries over to unseen countries: over 20 draws of the 9 folds LightGBM scores RMSE "
        "0.1138 against 0.1230 for night lights alone, and leave one country out over all 25 gives 0.1123 against "
        "0.1218 (2026-11-25).",
        "splits_dimensions_off_protocol": "Accepted (Andrej, 2026-11-25): 1 x 9 country folds instead of the "
        "protocol's 3 x 3. Over 20 draws each, 1 x 9 lands closer to leave one country out over all 25 (bias "
        "+0.0010 to +0.0024 RMSE against +0.0020 to +0.0044 for 3 x 3, which trains on a third fewer countries) and "
        "keeps its model ranking in 90% of draws against 85%; the splits comment says why.",
    }

    prepared_raw_files = (LABELLED_TEST, JOIN_CHECK)

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        # Recover the labels of Test.csv from the source table (review issue 9), validated on Train.csv's labels
        for name, digest in RAW_SHA256.items():
            if _sha256(raw_dir / name) != digest:
                raise ValueError(f"{name} differs from the pinned file (SHA-256 {digest})")
        dtype = {"ID": "str", "country": "str", "urban_or_rural": "str"}
        train = pd.read_csv(raw_dir / "Train.csv", dtype=dtype).assign(part="train")
        test = pd.read_csv(raw_dir / "Test.csv", dtype=dtype).assign(part="test")
        zindi = pd.concat([train, test], ignore_index=True)
        src = pd.read_csv(
            raw_dir / SOURCE_TABLE, usecols=["country", "year", "URBAN_RURA", "LATNUM", "LONGNUM", "wealthpooled"]
        )
        src = src.dropna(subset=["LATNUM", "LONGNUM"]).rename(columns={"URBAN_RURA": "urban_or_rural"})
        if set(src["country"]) != set(CAPITAL_START) or set(zindi["country"]) != set(CAPITAL_START):
            raise ValueError("the countries of the source table and of Zindi's files differ")
        capitals = _fit_capitals(zindi, src)
        src["capital_km"] = [
            _ellipsoid_km(la, lo, *capitals[c]) for la, lo, c in zip(src.LATNUM, src.LONGNUM, src.country)
        ]
        src["shoreline_km"] = _shoreline_km(src["LATNUM"].to_numpy(), src["LONGNUM"].to_numpy(), raw_dir / COASTLINE)
        m = zindi.join(_join(zindi, src))
        # Target = a * wealthpooled + b, refit on Train.csv's matched rows (outliers off by > 0.01 left out of the fit)
        t = m[(m["part"] == "train") & m["wealthpooled"].notna()]
        design = np.c_[t["wealthpooled"], np.ones(len(t))]
        coef = np.linalg.lstsq(design, t["Target"], rcond=None)[0]
        inlier = np.abs(t["Target"] - design @ coef) < 0.01
        coef = np.linalg.lstsq(design[inlier.to_numpy()], t.loc[inlier, "Target"], rcond=None)[0]
        m["recovered"] = coef[0] * m["wealthpooled"] + coef[1]
        m["right_cluster"] = (m["recovered"] - m["Target"]).abs() <= RIGHT_CLUSTER
        accepted_train = m[(m["part"] == "train") & m["accepted"]]
        if accepted_train["right_cluster"].mean() < 0.999:
            raise ValueError(f"the join finds the right cluster for only {accepted_train['right_cluster'].mean():.4%}")
        cols = [
            "ID",
            "part",
            "country",
            "year",
            "urban_or_rural",
            "Target",
            "recovered",
            "capital_gap_km",
            "near_tie",
            "shared",
            "accepted",
            "right_cluster",
        ]
        m[cols].assign(a=coef[0], b=coef[1]).to_csv(raw_dir / JOIN_CHECK, index=False)
        labelled = m[(m["part"] == "test") & m["accepted"]]
        labelled[[*test.columns.drop("part"), "recovered"]].rename(columns={"recovered": "Target"}).to_csv(
            raw_dir / LABELLED_TEST, index=False
        )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        dtype = {"ID": "str", "country": "str", "urban_or_rural": "str"}
        train = pd.read_csv(raw_dir / "Train.csv", dtype=dtype)
        test = pd.read_csv(raw_dir / LABELLED_TEST, dtype=dtype)
        return pd.concat([train.assign(file="Train.csv"), test.assign(file="Test.csv")], ignore_index=True)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        return decode(drop_columns(raw, ["ID", "file"]), CODE_LABELS)

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        rows = raw.groupby(["country", "file"]).size().unstack(fill_value=0)
        fold_of = {
            country: fold
            for fold, (_train, test) in self._country_folds(df)[0].items()
            for country in df["country"].iloc[test].unique()
        }
        rows["test_fold"] = rows.index.map(fold_of)
        check = pd.read_csv(self.raw_dir / JOIN_CHECK)
        check["status"] = np.select(
            [check["accepted"], check["shared"], check["near_tie"]],
            ["accepted", "shared coordinate", "near-tie in the distance to the capital"],
            "no match within 0.002 km",
        )
        join = check.groupby(["part", "status"]).agg(rows=("ID", "size"), right_cluster=("right_cluster", "sum"))
        join.loc[join.index.get_level_values("part") == "test", "right_cluster"] = np.nan
        return [
            Decision(
                title="Test.csv's 7 countries added with labels recovered from the source table",
                why=(
                    "Zindi's Train.csv and Test.csv are the coordinate-bearing clusters of the africa_poverty table; "
                    "each Zindi row is assigned to its cluster within country x year x urban by the recomputed "
                    "distance to the capital, the shoreline breaking near-ties, and kept only where the match is "
                    "unambiguous. On Train.csv the accepted matches give the released Target up to Zindi's per-row "
                    "deviation (right_cluster: within 0.0014); Test.csv rows get the refit rescale of wealthpooled."
                ),
                evidence=join.reset_index(),
            ),
            Decision(
                title="Rows per country and file, and the fold that tests each country",
                why="Whole countries in 9 folds of 2 or 3, one repeat: every country is tested once, all its years.",
                evidence=rows.reset_index(),
            ),
        ]

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["country", "urban_or_rural"])

    @staticmethod
    def _country_folds(df: pd.DataFrame) -> dict:
        # One repeat of grouped k-fold over the countries; shuffled countries in about equal numbers per fold.
        return grouped_splits(
            df.reset_index(drop=True),
            n_repeats=1,
            group_on="country",
            group_labels="per_sample",
            n_folds=N_COUNTRY_FOLDS,
            random_state=SPLIT_RANDOM_STATE,
        )

    def _make_splits(self, df: pd.DataFrame) -> SplitPlan:
        splits = self._country_folds(df)
        tested = [df["country"].iloc[test].unique() for _train, test in splits[0].values()]
        assert sorted(len(c) for c in tested) == [2, 2, 3, 3, 3, 3, 3, 3, 3], tested
        assert sum(len(c) for c in tested) == df["country"].nunique() == 25
        return SplitPlan(splits=splits)
