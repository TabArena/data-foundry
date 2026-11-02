"""Curated dataset definition for `cape_floristic_region_family_cover` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Grouping, Metric, TaskSummary, drop_columns

# The two covariates that sit exactly on the 1-minute grid: plots with the same two values lie in one cell of a 1-minute
# lattice of the coordinates and each such cell holds one pair of values, so the pair is the cell, the group of the
# split. `RFL_CONC`, which the paper also gives as 1-minute (Tang et al. 2023, Sec. 2), has 8 values and is not on it.
ONE_MINUTE_GRID_COLUMNS = ["apan_mean_an", "tminave07c"]


class CapeFloristicRegionFamilyCover(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "How much succulent Crassulaceae cover, on the scale of the release, does a 10 x 5 m plot hold at a site "
            "of two Cape Floristic Region reserves, with the surveyed plots of its own 1-minute climate grid cell held "
            "out?"
        ),
        use_case=(
            "For example, a reserve ecologist maps the expected cover of succulent Crassulaceae from a site's "
            "location and climate, to choose where to survey or protect succulent-rich vegetation; the source "
            "names prediction to unobserved sites, not an actor."
        ),
        row=(
            "One survey of one vegetation plot of 10 x 5 m: 119 plots in Baviaanskloof and 61 at Cape Point, where "
            "the plots are permanent and were surveyed in 1966, 1996 and 2010. The release holds one survey of each "
            "plot, of 2010-2011 by the paper (the Baviaanskloof years are not verified)."
        ),
        predicted=(
            "The family's cover as released, from 0 to 0.99, relative to a per-plot quantity the source does not "
            "document, so not a share of the plot's area: 0 in 49% of the plots (none recorded) and exactly 0.99 in "
            "12%, either a cap or a code for full cover; the source says neither."
        ),
        known="The plot's coordinates and reserve, and four long-term climate averages read from grids at its site.",
        split=(
            "Whole 1-minute climate grid cells (about 1.9 x 1.5 km) are held out with all their plots, so a test plot "
            "stands for a site of the two reserves with the surveyed plots of its own cell held out; nearer plots of "
            "other cells stay in training. Sites in cells with no survey lie farther from any plot than the test plots "
            "do."
        ),
        changes=(
            "We predict one family of the two in the file and drop the other, and we hold out grid cells where the "
            "paper split plots at random."
        ),
        fit="approximate",
        fit_reason=(
            "No actor is named, the label is relative to a per-plot quantity the source does not document (0.99 a cap "
            "or a code), and the inputs are climate and position only, without vegetation type, terrain or fire "
            "history (the paper ties the family to rocky outcrops and rarely burnt sites). A 50 m2 plot stands for a "
            "mapped site, and only sites inside the two reserves are covered."
        ),
    )

    # Dataset
    unique_name = "cape_floristic_region_family_cover"
    year = "2021"
    domain = "biology & life sciences"
    source = "GitHub"
    source_url = "https://github.com/beckytang/ZIB_data/tree/97da77c9c87434e85bba0e081fa27b148a2df9a9"
    license = None  # the repository has no licence file (GitHub API: no licence, 2026-10-30); the paper states none
    data_tags = ("Spatial",)
    download_description = """
        We download the file from the first author's GitHub repository, pinned to the commit of 2021-06-05 that holds it.

        mkdir -p local-data-warehouse/cape_floristic_region_family_cover && wget -O local-data-warehouse/cape_floristic_region_family_cover/cfr_zib_data.csv https://raw.githubusercontent.com/beckytang/ZIB_data/97da77c9c87434e85bba0e081fa27b148a2df9a9/cfr_zib_data.csv
    """
    bibtex = r"""
        @article{tang2023zero,
          title = {Zero-Inflated Beta Distribution Regression Modeling},
          author = {Tang, Becky and Frye, Henry A. and Gelfand, Alan E. and Silander, Jr., John A.},
          journal = {Journal of Agricultural, Biological and Environmental Statistics},
          volume = {28},
          pages = {117--137},
          year = {2023},
          doi = {10.1007/s13253-022-00516-z},
          note = {Data: \url{https://github.com/beckytang/ZIB_data} (2021); preprint arXiv:2112.07249}
        }
    """
    curation_comments = """
        We start with `cfr_zib_data.csv` from the first author's GitHub repository `beckytang/ZIB_data` (commit 97da77c of 2021-06-05; 180 rows, 10 columns, no missing values, no duplicate rows), the example data of Tang, Frye, Gelfand and Silander (2023); pages below are those of arXiv:2112.07249v2.

        - Prediction point: an ecologist wants the Crassulaceae cover at a site that has not been surveyed, knowing its coordinates, its reserve and the climate grids at the site. The paper's spatial models "enable prediction to unobserved sites with known environmental attributes" (Sec. 6, p. 16).
        - The rows: Sec. 2, p. 4: "Our data were collected between 2010 and 2011 from plots concentrated in two regions of South Africa: 61 plots in the Cape Point section of Table Mountain National Park and 119 plots in the Baviaanskloof Mega-Reserve"; "each 10 x 5 m plot was sampled for its floristic composition using observations of percent cover". The Cape Point plots are permanent plots on a systematic 914 m grid, surveyed in 1966, 1996 and 2010 (metadata of Slingsby et al. 2017, figshare 10.6084/m9.figshare.4737358); the release holds one survey of each. The authors' Baviaanskloof deposit on Dryad dates its surveys 1991/92 and 2011/12, so the Baviaanskloof years are not verified.
        - Target: `CRASSULACEAE`, the family's cover as released (its scale: two bullets below). Chosen over `RESTIONACEAE`, the other family in the file: the paper presents its spatial analyses and its model comparison for Crassulaceae and puts Restionaceae in the supplement (Sec. 5.2, p. 15); Restionaceae sits at 0.99 in 79 of 180 plots (56 of the 61 at Cape Point), so the reserve alone explains a third of its variance (a mean per reserve: skill 0.36 against 0.12 for Crassulaceae, random folds). A Restionaceae target on the same plots would be a swapped target, not a second dataset (PROV-6).
        - Dropped `RESTIONACEAE`: it is recorded in the same survey as the target, over the same per-plot quantity, so it is unknown at an unsurveyed site (LEAK-10).
        - Dropped `plot`, an identifier (`BK_n`, `CP_n`; the prefix repeats the reserve).
        - Zeros: 88 of 180 plots (48.9%) have no Crassulaceae recorded (Sec. 2, p. 4: "49% of the observations for Crassulaceae and 31% of observations for Restionaceae are 0"). They stay as observed absences: failed detection "is extremely unlikely in our example system which is comprised almost exclusively of evergreen perennial species in an open shrubland" (Sec. 1, p. 2), and on the 57 Cape Point plots of the independent 2010 survey (Slingsby et al. 2017) presence and absence agree on every plot. The paper's split into zeros from unsuitability and zeros by chance is its model's assumption, not a column.
        - Anomaly, the target's scale (USE-5): the paper speaks of percent cover, but the value is not a share of the 50 m2. In all 23 Baviaanskloof plots with both families between 0 and 0.99, the two values are fractions over one per-plot number (or a multiple of it) that runs from 31 to 2,626 between plots, so both are relative to a quantity measured per plot that the source does not document. It is not the summed cover of the two families either: 21 plots sum to more than 1 over the two (up to 1.98), BK_3 to 1.74 with neither at 0.99. Kept as released at fit approximate. The authors' Baviaanskloof survey on Dryad (doi:10.5061/dryad.kk174, CC0) may hold the species covers, but its file downloads only by hand and was not checked; the Cape Point survey on figshare counts individuals, from which cover cannot be rebuilt.
        - Anomaly, kept on purpose (LEAK-26): the cover stops at 0.99. 21 plots (11.7%, 20 of them in Baviaanskloof) hold exactly 0.99, the next values are 0.986, 0.961 and 0.949, and the 71 other positive values are all distinct. Neither the paper nor the repository says what 0.99 is: full cover recoded below 1 (the paper models cover "continuous on [0, 1)" and does "not address the notion of '1-inflation'", Sec. 1, p. 2) fits, and so does a cap, min(x, 0.99), on a value that can exceed 1 (BK_3 above; CP_2 sits at 0.99 in both families). The plots stay: they are 21 of the 25 values at or above 0.8, a classifier trained on other cells finds them at ROC AUC 0.88, and dropped from the data they take an untuned random forest's skill from 0.48 to 0.19 on the remaining 159 rows (shipped folds). RMSE reads 0.99 as an exact value, and these plots decide which model wins: on the shipped folds they are 12% of the test plots and 36% of the forest's squared error (27% for LightGBM); of four untuned models the forest has the lowest RMSE on 34 of 60 splits and a hurdle model on 18, while scored without these plots the hurdle model wins 45 and the forest 3. Revisit if the Dryad file or the authors document the family covers.
        - Features: `latitude`, `longitude`, `region` (Baviaanskloof or Cape Point) and four climate covariates, "largely derived from the WorldClim (Hijmans et al. 2005) and Schulze (Schulze 1997) climate datasets" (Sec. 2, p. 4): `apan_mean_an` (mean annual evaporation, 1-minute grid), `tminave07c` (average minimum July temperature in degrees C, 1-minute), `RFL_CONC` (rainfall concentration index, 0 to 100; 1-minute by the paper, but with 8 values, 41.5 at every Cape Point plot, it is not on the 1-minute grid) and `BioClimMAP30s` (30 arc seconds, next bullet). The release holds the raw values (the paper centred and scaled them for its own fits, Sec. 5.1, p. 14), so nothing is scaled over all rows.
        - Anomaly: `BioClimMAP30s` is labelled mean annual precipitation by the paper (Sec. 2, p. 4), but its values (17.2 to 21.9, each a whole number over 60) are not millimetres, which run to hundreds at both reserves. In Baviaanskloof it ranks the plots like mean annual temperature (Spearman +0.99 with CHELSA's 1981-2010 mean annual temperature, -0.77 with its precipitation); at Cape Point the evidence is mixed. Its identity is not established. Kept as published (PROV-14): no conversion is published, and another grid in its place would be a rebuild.
        - Grouped by the 1-minute climate grid cell, where the paper split plots at random (Sec. 5.3, p. 15: "a training set of 99 locations and a test set of 20 locations", within Baviaanskloof). The Baviaanskloof plots are clustered: a median 0.5 km from the nearest plot, while a random site of the surveyed area (the plots' convex hull) is 1.63 km from one; the covers of two plots correlate (Pearson) at 0.58 to 0.66 under 1 km (82 pairs), 0.34 at 1 to 2 km (98), 0.22 at 2 to 4 km (300) and about 0 beyond 4 km. Random folds put Baviaanskloof test plots a median 0.73 km from training, the cell folds 1.69 km. The group key is exact (SPLIT-24, SPLIT-26): the plots that share `apan_mean_an` and `tminave07c`, 104 cells of 1 to 5 plots at most 1.8 km apart, which equal a 1-minute lattice of the coordinates (no cell spans two lattice cells, no lattice cell holds two). `RFL_CONC` stays out of the key, since it would split 4 of these cells. The 26 groups of plots that share all four climate values lie inside the cells. Untuned LightGBM R^2 falls from 0.43 on random folds to 0.36 on the cell folds, and a random forest's skill over the training mean from 0.53 to 0.48, above the mean on 60 of 60 (60 splits each).
        - Zeros and cover are both learnable on the cell folds: an oracle that knows which plots are 0 and predicts the training mean of the others reaches a skill of 0.33, a random forest 0.48; a hurdle model's two stages reach ROC AUC 0.80 for presence and R^2 0.28 on the plots with cover (60 shipped splits).
        - The reserves weigh differently: at Cape Point 12 of the 16 plots with cover are below 0.05, and a random forest's cover skill against the reserve's own mean is 0.03 there (out of fold, 10 repeats) while it ranks presence at ROC AUC 0.78. The pooled RMSE scores mostly Baviaanskloof and the contrast between the reserves.
    """

    # Task
    target = "CRASSULACEAE"
    problem_type = "regression"
    metric = Metric.fallback(
        reason=(
            "Tang et al. (2023) compare models on held-out plots by Tjur's R2 and the AUC of zero against positive "
            "cover and by two CRPS variants of the predictive distribution, averaged over 30 random 99/20 splits "
            "within Baviaanskloof (Sec. 3.4 and 5.3): several criteria, none named as the one that decides (MET-5). "
            "The paper picks its priors by the CRPS of the full distribution (Sec. 5.1-5.2, p. 15) but says that "
            "score cannot compare models with different sources of zeros (Sec. 3.4, p. 10), and any CRPS needs a "
            "predictive distribution. The repository's README defines no metric."
        ),
    )
    grouping = Grouping(
        on="climate_cell",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a cell of the 1-minute climate grids: the plots that share their mean annual evaporation and July minimum temperature, the two covariates that sit exactly on a 1-minute lattice of the coordinates (104 cells of 1 to 5 plots, at most 1.8 km apart; 53 cells hold one plot). The use case is the cover at a site that has not been surveyed: the paper's spatial models "enable prediction to unobserved sites with known environmental attributes" (Tang et al. 2023, Sec. 6, p. 16). The sample is clustered: in Baviaanskloof a plot is a median 0.5 km from the nearest other plot, a random site of the surveyed area 1.63 km, and the covers of plots under 1 km apart correlate at 0.58 to 0.66. Random folds put the Baviaanskloof test plots a median 0.73 km from training, less than half the distance a map faces; held-out cells put them 1.69 km away. Stricter than the paper's protocol, which split the Baviaanskloof plots at random (Sec. 5.3). Each plot is one prediction.
        """,
    )
    splits_comment = """
        Grouped splits on the 1-minute climate grid cell: every plot of a cell stays on one side, so a test plot stands for a site of the two reserves with the surveyed plots of its own cell held out. In Baviaanskloof the test plots lie a median 1.69 km from the nearest training plot (25% within 1 km), about as far as a random site of the surveyed area lies from a plot (1.63 km, 27%). Sites in cells with no survey lie farther, a median 2.03 km (11% within 1 km), and covers still correlate at 0.34 between plots 1 to 2 km apart and 0.22 at 2 to 4 km, so the score is somewhat optimistic for them. At Cape Point the cells are stricter than mapping: test plots lie 0.92 km from training, a site of the surveyed area 0.43 km from a plot.
    """

    accepted_check_warnings = {
        "meta_license_unknown": (
            "The repository has no licence file (GitHub API, 2026-10-30) and the paper states none; no other licence "
            "is known. The data are the authors' own public release of their paper's example table."
        ),
    }

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "cfr_zib_data.csv")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # the group: plots in one cell of the 1-minute lattice share these two values exactly (and no other cell does)
        df["climate_cell"] = df.groupby(ONE_MINUTE_GRID_COLUMNS, sort=True).ngroup().map("cell_{:03d}".format)
        # the plot id is an identifier; the other family's cover is recorded in the same survey as the target
        return drop_columns(df, ["plot", "RESTIONACEAE"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=["region", "climate_cell"],
        )
