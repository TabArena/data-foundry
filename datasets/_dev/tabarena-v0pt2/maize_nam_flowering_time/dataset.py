"""Curated dataset definition for `maize_nam_flowering_time` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    FeatureTypes,
    Grouping,
    Metric,
    Source,
    TaskSummary,
    TimeBasis,
)

GENOTYPES = "markergenotypes062508.txt"
MARKER_MAP = "markers061208.txt"
LINE_VALUES = "NAMSum0607FloweringTraitBLUPsAcross8Envs.txt"
RAW_FILES = (GENOTYPES, MARKER_MAP, LINE_VALUES)
# The other two traits of the same plots, measured at the same time as the target and not held before the season.
OTHER_TRAITS = ("days2silk", "asi")


def marker_order(raw_map: pd.DataFrame) -> pd.DataFrame:
    """The 1,106 markers in the order the genotype table's columns carry them.

    The released map lists each chromosome's first and last marker at the top, with the formulas the authors used,
    and then every marker; its fourth column is the marker's global index 1 to 1,106, a permutation of them, so
    sorting on it puts the markers in linkage order, which is the order `i0` to `i1105` are in (`_clean` checks it).
    """
    out = raw_map.sort_values(3, kind="stable").reset_index(drop=True)
    out.columns = ["marker", "chromosome", "position_cm", "index", "chromosome_repeat", "note"]
    return out[["marker", "chromosome", "position_cm", "index"]]


def line_ids(genotypes: pd.DataFrame, values: pd.DataFrame) -> pd.Series:
    """The source's line id for each genotype row, which the genotype table itself does not carry.

    The genotype table holds the family and the three trait values but no identifier. Within a family its rows are
    an in-order subsequence of the line table's rows and carry the line table's own values, so a greedy in-order
    match on the anthesis value names every row: 4,678 of the 4,699 values are unique inside their family, and the
    21 that are not are resolved by the order. The id is a column of the raw state only; it never becomes a feature.
    """
    found: dict[int, str] = {}
    for family, rows in genotypes.groupby("pop", sort=True):
        table = values[values["pop"] == family]
        ids = table["Geno_Code"].to_numpy()
        measured = table["Days_To_Anthesis_BLUP_Sum0607"].to_numpy()
        cursor = 0
        for position, value in zip(rows.index, rows["days2anthesis"].to_numpy(), strict=True):
            while cursor < len(measured) and measured[cursor] != value:
                cursor += 1
            if cursor == len(measured):
                raise ValueError(f"family {family}: the genotype rows are not an in-order subsequence of the lines")
            found[position] = ids[cursor]
            cursor += 1
    return pd.Series(found, name="line").sort_index(kind="stable")


class MaizeNamFloweringTime(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How many days after planting will a maize line shed pollen, from its SNP genotype alone?",
        use_case="A maize breeder ranks the inbred progeny of a cross before the field season and picks which lines "
        "to advance, from the genotype alone (genomic selection), without having grown any of them.",
        row="One recombinant inbred line of the maize Nested Association Mapping population (4,699 lines of 25 "
        "families, each a cross of B73 with one other founder), with its imputed marker calls and its flowering "
        "time over the 2006 and 2007 trials.",
        predicted="The line's days to anthesis in days, as the trials measured it: the best linear unbiased "
        "prediction the source published for the line over eight environments.",
        known="Which allele of each of 1,106 linkage-map markers the line carries, as a dosage the source imputed "
        "(0, 1 or 2, with an intermediate value where the imputation is uncertain), and which family it comes from.",
        split="Whole families are held out: the test lines are the progeny of a cross whose flowering nobody has "
        "measured, which is what a breeder faces with a new cross.",
        changes="Days to silk and the anthesis-silking interval, measured in the same plots, are left out: they are "
        "not known before the season. The markers take the source's own names, chromosome and map position from the "
        "released marker list, and the line id is recovered from the line table and kept out of the features.",
        fit="approximate",
        fit_reason="The inputs are the genotype a breeder holds before the season and the target is the flowering "
        "time the trials measured, in days, on the scale the breeder selects on. Two gaps: the panel spans the "
        "diversity of the species rather than an elite programme's working set, and its 1,106 linkage-map "
        "markers are far coarser than a programme genotypes at today (the scope bullet measures both).",
    )

    # Dataset
    unique_name = "maize_nam_flowering_time"
    domain = "biology & life sciences"
    sources = (
        Source(
            role="publication",
            platform="Other",
            url="https://doi.org/10.1126/science.1174276",
            license="No licence stated by the host; a public release of the NSF-funded maize diversity project",
            year="2009",
            bibtex="""
                @article{buckler2009flowering,
                  title = {The genetic architecture of maize flowering time},
                  author = {Buckler, Edward S. and Holland, James B. and Bradbury, Peter J. and Acharya, Charlotte B.
                            and Brown, Patrick J. and Browne, Chris and Ersoz, Elhan and Flint-Garcia, Sherry and
                            Garcia, Arturo and Glaubitz, Jeffrey C. and Goodman, Major M. and Harjes, Carlos and
                            Guill, Kate and Kroon, Dallas E. and Larsson, Sara and Lepak, Nicholas K. and Li, Huihui
                            and Mitchell, Sharon E. and Pressoir, Gael and Peiffer, Jason A. and Rosas, Marco Oropeza
                            and Rocheford, Torbert R. and Romay, M. Cinta and Romero, Susan and Salvo, Stella and
                            Villeda, Hector Sanchez and da Silva, H. Sofia and Sun, Qi and Tian, Feng and Upadyayula,
                            Narasimham and Ware, Doreen and Yates, Heather and Yu, Jianming and Zhang, Zhiwu and
                            Kresovich, Stephen and McMullen, Michael D.},
                  journal = {Science},
                  volume = {325},
                  number = {5941},
                  pages = {714--718},
                  year = {2009},
                  doi = {10.1126/science.1174276},
                }
            """,
            files=RAW_FILES,
        ),
    )
    data_tags = ()
    time_basis = TimeBasis(
        "UnseenGroup",
        "the breeder ranks the progeny of a cross the data does not hold, so whole families are held out and the "
        "two trial years are not weighed: the target is the flowering time of a fixed genotype, measured once by "
        "one 2006-2007 protocol and published as a line value across its eight environments. The split cannot test "
        "a later season, another trial network, or germplasm outside this panel's 26 founders. One limit follows "
        "from the panel's own design and is accepted with it: every family is a cross to B73, so each test line has "
        "half-sibs in training and no held-out family is unrelated to the training ones.",
    )
    split_leaf = "L-EXP.kind"
    download_description = """
        The archive the maize diversity project publishes for Buckler et al. 2009, listed on its phenotypes page as
        "Flowering time phenotypes and imputed genotypes of our maize NAM population from Buckler et al. 2009.
        Science 325: 714-718". The definition reads three of its seven files.

        mkdir -p local-data-warehouse/maize_nam_flowering_time
        cd local-data-warehouse/maize_nam_flowering_time
        curl -L --fail https://cornell.box.com/shared/static/su1vodojjq5g8wg2aw8crimdx6328px6 -o nam_flowering.zip
        # sha256 f7144a2e934aa04402a18d57c7b0cd6d79797cdbff0fc036b8fd2360745adab8
        unzip -o nam_flowering.zip
        rm nam_flowering.zip
        Expected SHA-256:
        markergenotypes062508.txt d2c837df384285fc8cec6d79d6f1a0916a6ca0f157d16d90ba6ef685dda85cc3,
        markers061208.txt e4319eb39526a02b3fe07c649ec4cafdb39e77cdf48ece6df1ba6418de0a8634,
        NAMSum0607FloweringTraitBLUPsAcross8Envs.txt
        435488a619b6dd1f24e83f663dd97532b5873c7a4d450e0f13d3cf1578e5594e.
        The archive also holds four per-plot tables (days to tassel, days to silk and the two raw dates, 43,055 to
        43,459 rows each), which this definition does not read.
    """
    curation_comments = """
        The maize Nested Association Mapping population as its own project released it: 4,699 recombinant inbred
        lines of 25 families, each the progeny of B73 crossed with one other founder, with 1,106 imputed
        linkage-map markers and flowering time measured over eight environments in 2006 and 2007.

        - Prediction point: before the field season, when the cross has been made and its inbred progeny genotyped,
          and before any of them has been grown. Everything measured in the plots is after it: days to anthesis is
          the target, and days to silk and the anthesis-silking interval, which the genotype table carries in the
          same three columns, are left out (LEAK-10). They are measured on the same plants within days of the
          target and would hand a model most of it.
        - The line value is the source's, not ours (SPLIT-26): the released line table is a best linear unbiased
          prediction per line across the eight environments, in days, which is the scale a breeder selects on
          (MET-3). The archive also ships the 43,459 per-plot observations behind it, which this definition does
          not read; the published line value is the one the population's own papers use.
        - The genotype table is self-contained and carries no line identifier: its columns are the three traits,
          the family, and `i0` to `i1105`. Two facts about it were checked rather than assumed. First, the marker
          order: the released marker list's fourth column is the global index 1 to 1,106, a permutation, and
          sorting on it gives linkage order; adjacent columns of the genotype table then correlate at a median
          |r| of 0.980 within a chromosome and 0.014 across the nine chromosome boundaries, against 0.035 under a
          random reordering, so `i0` to `i1105` are the markers in that order and they take the source's names,
          chromosomes and map positions. Second, the line id: within a family the genotype rows are an in-order
          subsequence of the line table's rows and carry its exact values, so a greedy in-order match on the
          anthesis value names all 4,699 (4,678 of the values are already unique inside their family). The id is
          an identifier and is not a feature.
        - What the genotype table leaves out: the line table holds 5,463 lines over 27 families, and the genotype
          table 4,699 over 25. Family 17, whose lines carry `MO` identifiers rather than the `Z` codes, has no
          genotype row at all, nor does family 27; within the other families the genotyped lines are 126 to 196 of
          the 190 to 200 the line table holds.
        - The marker calls are the source's imputation and cannot be checked from the release: no cell is missing,
          and 1.44% of them carry an intermediate dosage (0.5 or 1.5) where that imputation is uncertain
          (LEAK-30 at most). No two lines share a marker profile.
        - The family is the group column and no feature: a breeder predicting for a new cross has no family of
          their own in the training data. It stays in the frame because the metric scores within it.
        - Scope (USE-8): one designed population of 25 crosses that all share B73 as a parent, one 2006-2007 trial
          network of eight environments, one 2008 linkage map of 1,106 markers. The same population now has a
          genotype two orders of magnitude denser, which would be another version of this dataset rather than
          another task.
    """

    # Task
    target = "days_to_anthesis"
    problem_type = "regression"
    metric = Metric.from_context(
        "mean_group_pearsonr",
        reason=(
            "The decision is which lines of one new cross to advance, a ranking inside the cross, and the split "
            "holds out whole families. The field's own criterion, which the papers on genomic prediction in these "
            "panels report, is the correlation pooled over the held-out lines; it is the original here, from "
            "context rather than from this source, since Buckler et al. map flowering-time QTL and declare no "
            "prediction metric at all. MET-18 is what makes the declaration per family: 69.3% of the variance of "
            "the line values lies between the 25 families, and a predictor that knows nothing but each test "
            "family's own true mean scores a pooled r of 0.793, against 0.209 for ridge and 0.231 for an untuned "
            "LightGBM on the markers, while the same predictor scores exactly 0 within a family, because it is "
            "constant there. A pooled score would therefore rank models by how well they recover a ranking of the "
            "crosses that the breeder reads off the parents, not the ranking inside a cross that genomic selection "
            "is bought for. Per family the same two models score 0.351 and 0.258, ridge on all 60 of the "
            "shipped splits and positive on every one of them, so the declared metric does not flatter them; "
            "it scores what the breeder buys."
        ),
        inputs={"group": "family"},
    )
    grouping = Grouping(
        on="family",
        labels="per_sample",
        prediction_unit="row",
        context="all_rows",
        definition="""
            One group is one family of the Nested Association Mapping population: the recombinant inbred progeny of
            B73 crossed with one of 25 other founders, 126 to 196 genotyped lines each. The source designed the
            panel so that every family shares B73 as a parent and the other founders span the diversity of the
            species; genomic selection is used to rank the progeny of a cross before the season, so whole families
            are held out: a test family's flowering times are unknown, as they are for a cross nobody has grown.
            Each line is scored on its own. The breeder genotypes the whole progeny of the cross at once and ranks
            them together, so a model may use all rows of a test family (`all_rows`).
        """,
    )
    splits_comment = """
        The default repeated grouped protocol on the 25 families, 20 repeats of 3 folds, 60 splits: each test fold
        holds 8 or 9 whole families and 1,442 to 1,729 of the 4,699 lines. It replaces the random holdout over lines that the
        benchmarking work on these panels uses, which was designed for a different question, comparing algorithms
        inside a population that is already phenotyped, and is a habit rather than a choice for ours (SPLIT-5): a
        random split puts the full siblings of every test line in the training data, which a breeder ranking a new
        cross does not have. A test family's own feature rows are all on the test side and may be read
        (`context="all_rows"`, the grouping definition). Leaf L-EXP.kind of the split tree. The repeats reuse the
        same 25 families, so the spread over repeats is descriptive, not 25 independent crosses.

        What the grouped split costs, and why a pooled R^2 reads as no signal here. Over the nine splits the group
        probe runs, three of the twenty repeats, an untuned LightGBM scores R^2 0.233 on folds of random lines and
        0.047 on folds of whole families, a gap of 0.186, and its learnability figures across unseen families are
        negative for every model tried (ridge -0.500, random forest -0.028, LightGBM -0.025, 5-NN -0.222). That is
        not an absence of signal: 69.3% of the target's variance is between the families, a pooled R^2 is mostly a
        test of predicting the family mean, and no model predicts an unseen cross's mean from markers alone. The
        signal is inside the family, which is where the decision and the declared metric are: over all 60 shipped
        splits ridge scores a per-family correlation of 0.351 (SE 0.005) and is positive on 60 of 60, over the 30
        the task probe runs a random forest scores 0.303 and beats the dummy on 100% of them by +0.3026 (SE
        0.0087), and a predictor handed each test family's true mean scores exactly 0 there against a pooled r of
        0.793. A reader who scores this dataset with a pooled R^2 will conclude the task is unlearnable; that is
        the metric's choice being skipped, not the task.
    """
    accepted_check_warnings = {
        "groups_test_groups_few": (
            "25 families, 8 or 9 per test fold and 1,442 to 1,729 lines scored per fold. The signal across groups "
            "is measured, not assumed: over all 60 shipped splits ridge scores a per-family r of 0.351 (SE "
            "0.005) and is positive on 60 of them, and an untuned LightGBM 0.258 over the 12 measured, where the "
            "training mean is undefined per family because it is constant there, and a predictor given each test "
            "family's true mean scores exactly 0. The task is a breeder's own: the "
            "families are the crosses a breeder makes, and a few of them is what a breeding programme holds."
        ),
    }

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        # The genotype table's first line is a shape header (`4699 1110 1`), not column names.
        return {
            "genotypes": pd.read_csv(raw_dir / GENOTYPES, sep="\t", skiprows=1),
            "markers": pd.read_csv(raw_dir / MARKER_MAP, sep="\t", header=None, encoding="latin-1"),
            "lines": pd.read_csv(raw_dir / LINE_VALUES, sep="\t"),
        }

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        genotypes = raw["genotypes"].reset_index(drop=True)
        markers = marker_order(raw["markers"])
        columns = [c for c in genotypes.columns if c.startswith("i")]
        if len(columns) != len(markers):
            raise ValueError(f"{len(columns)} marker columns against {len(markers)} in the released map")
        # 1. The marker columns are the map's markers in linkage order, which the correlation structure confirms:
        #    neighbours inside a chromosome move together and the nine chromosome boundaries break that.
        calls = genotypes[columns].astype("float32").to_numpy()
        adjacent = np.array([abs(np.corrcoef(calls[:, k], calls[:, k + 1])[0, 1]) for k in range(len(columns) - 1)])
        chromosome = markers["chromosome"].to_numpy()
        boundary = chromosome[:-1] != chromosome[1:]
        if not (np.median(adjacent[~boundary]) > 0.5 > np.max(adjacent[boundary])):
            raise ValueError("the marker columns are not the released map's order: the linkage structure disagrees")
        # 2. One row per line: the family, the target, and the markers under the source's own names.
        names = [f"{m}_chr{int(c)}_{p:g}cM" for m, c, p in markers[["marker", "chromosome", "position_cm"]].values]
        df = pd.DataFrame(
            {"family": genotypes["pop"].astype("int16"), self.target: genotypes["days2anthesis"].astype(float)}
        )
        df = pd.concat([df, pd.DataFrame(calls, columns=names)], axis=1)
        # 3. The line id is recovered for the raw state's sake and checked, then dropped: it is an identifier.
        recovered = line_ids(genotypes, raw["lines"])
        if len(recovered) != len(df) or recovered.isna().any():
            raise ValueError("the line ids did not resolve for every genotype row")
        # 4. Days to silk and the anthesis-silking interval are measured in the same plots and leave (LEAK-10).
        df = df.drop(columns=[c for c in OTHER_TRAITS if c in df.columns])
        if df[self.target].isna().any() or df["family"].isna().any():
            raise ValueError("a line is missing its family or its target")
        return df.reset_index(drop=True)

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # Every column is numeric: a marker call is an imputed dosage of one allele (0 to 2), the family is the
        # group column and the target is days.
        return FeatureTypes()
