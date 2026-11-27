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
# The other two flowering traits, measured on the same plants within days of the target.
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


class MaizeNamFloweringTime(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Which lines of one maize cross will flower earliest, from their marker genotypes alone?",
        use_case="A maize breeder ranks the inbred progeny of a cross before the field season and picks which lines "
        "to advance, from the genotype alone (genomic selection), without having grown any of them.",
        row="One recombinant inbred line of the maize Nested Association Mapping population (4,699 lines of 25 "
        "families, each a cross of B73 with one other founder), with its marker calls and its flowering time over "
        "the 2006 and 2007 trials.",
        predicted="The line's days to anthesis in days, as the trials measured it: the best linear unbiased "
        "prediction the source published for the line over eight environments. What the task delivers is the "
        "ordering inside one cross, not a date (the notes measure both).",
        known="For each of 1,106 linkage-map markers, how much of the line's genome there came from the family's "
        "non-B73 founder rather than from B73, as the source imputed it (0, 1 or 2, with 0.5, 1 and 1.5 marking "
        "where the imputation places a switch of parental origin), and which family the line comes from.",
        split="Whole families are held out: the test lines are the progeny of a cross whose flowering nobody has "
        "measured, which is what a breeder faces with a new cross.",
        changes="Days to silk and the anthesis-silking interval, measured in the same plots, are left out: they are "
        "not known before the season. The markers take the source's own names, chromosome and map position from the "
        "released marker list, and the line id is read from the genotype table and kept out of the features.",
        fit="approximate",
        fit_reason="The inputs are the genotype a breeder holds before the season and the target is the flowering "
        "time the trials measured, in days, on the scale the breeder selects on. The gap is the germplasm: this is "
        "a research panel designed to span the species, all crossed to one parent and deliberately unselected, so "
        "the level reached here is not a breeder's at-home accuracy.",
    )

    # Dataset
    unique_name = "maize_nam_flowering_time"
    domain = "biology & life sciences"
    sources = (
        Source(
            role="publication",
            platform="Other",
            url="https://doi.org/10.1126/science.1174276",
            license="No licence stated by the host, which asserts copyright without granting one; a public release "
            "of the NSF-funded maize diversity project",
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
        "two trial years are not weighed: the target is the flowering time of a fixed genotype, published as a line "
        "value across its eight environments. The split cannot test a later season, another trial network, or "
        "germplasm outside this panel's 26 founders; the last of those is measurable here and is markedly harder, "
        "since holding out a whole germplasm group (tropical, temperate, mixed, sweet, popcorn) drops the declared "
        "metric to 0.116 for ridge and 0.202 for a random forest, with the two-family sweet-corn group negative for "
        "every model. Five groups are too few to split on, so it stays a limit rather than the split. One limit "
        "follows from the panel's own design and is accepted with it: every family is a cross to B73, so each test "
        "line has half-sibs in training and no held-out family is unrelated to the training ones.",
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
        The archive also holds four per-plot tables (days to tassel, days to silk and the two raw dates, 43,054 to
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
          target: days to silk correlates 0.886 with it within a family and is predicted equally well (0.373
          against 0.372), so it is the same trait rather than a second one.
        - **What a marker column is, and what it is not.** These are not SNP calls. The source coded every marker
          relative to B73, so a 2 means "this line's segment here came from this family's non-B73 founder" and
          names a different plant in each of the 25 families. Measured: every one of the 25 x 1,106 family-by-marker
          mean calls lies between 0.441 and 1.581, 93.5% of them between 0.8 and 1.2, and not one marker is fixed in
          any family, where a real SNP panel across 25 diverse founders would be monomorphic in many of them. Two
          consequences run through everything below. The coding discards founder identity, so the between-family
          part of the target is not reachable from the features at all, which is why no model predicts an unseen
          cross's mean and why the metric is declared per family. And a model fitted here cannot be carried to a
          breeder's own genotype file, which holds alleles rather than parent-of-origin dosages.
        - How much of the matrix is a call: no cell is missing, but 7.71% of them are not a call either. 6.27% hold
          1 and 1.44% hold 0.5 or 1.5, and these are the source's posterior over where the parental origin switches,
          not heterozygosity: walking each line along a chromosome, every run of 0.5 is flanked by a 0 and a 1,
          every run of 1.5 by a 1 and a 2, and 79.6% of the runs of 1 by a 0 on one side and a 2 on the other, so
          the values climb a ladder 0, 0.5, 1, 1.5, 2 across each breakpoint. The release carries no unimputed
          version of this marker set, so it is kept with this note rather than repaired (LEAK-30 at most).
        - The line value is the source's, not ours (SPLIT-26): the released line table is a best linear unbiased
          prediction per line across the eight environments, in days, which is the scale a breeder selects on
          (MET-3). The archive also ships the 43,459 per-plot observations behind it, which this definition does
          not read; the published line value is the one the population's own papers use. Against an
          environment-adjusted plot mean built from those tables it correlates 0.976, and the between-family share
          of the variance is 0.605 on the raw plot means against 0.635 after adjusting for environment, so the
          family differences are genetic rather than an artefact of where each family was grown.
        - The field design behind that value, from the per-plot tables: nine location-year-rep cells over 2006 and
          2007, which are the source's eight environments (Raleigh's two reps are one environment), with environment
          effects spanning 26 days. The eight are not the same eight for every family: nine families miss Columbia
          MO 2006 and get Columbia MO 2007 instead, and a line appears in 2 to 9 cells (median 7). Field blocks are
          balanced, each holding 24 or 25 of the 25 families, so there is no family-by-block confound to remove.
        - The genotype table's first column is the line id (`Z001E0001` and so on); it is read, checked against the
          line table and then dropped, since an identifier is no model input. All 4,699 ids are in the line table
          and every one of their three trait values matches it exactly.
        - The marker columns arrive unnamed as `i0` to `i1105` and take their names from the released map, whose
          fourth column is the global index 1 to 1,106 and so gives linkage order. Three facts confirm that order on
          the data itself: all nine chromosome boundaries have an adjacent correlation of at most 0.024 while all
          1,096 within-chromosome adjacencies are at least 0.696 (median 0.980); the breaks fall at columns 175,
          302, 432, 543, 682, 760, 838, 944 and 1,029, exactly the map's own chromosome blocks; and, since
          reversing a chromosome would preserve every adjacency, the direction is fixed by comparing the observed
          recombination fractions with the map's distances in sequence, which agree at Spearman 0.936 forward
          against 0.049 reversed, in every one of the ten chromosomes.
        - What the genotype table leaves out. The line table holds 5,463 rows: the 25 families, plus the IBM
          population (`pop` 17, B73 crossed with Mo17 and intermated, 200 lines with `MO` identifiers) and a
          281-row block of inbreds (`pop` 27) that includes B73 itself and the founder lines. Neither is a family
          of this panel and neither is genotyped here, so the checks and the founders never become rows of the
          task. Of the 764 line-table rows with a value and no markers, those two account for 481; the other 283
          sit inside the 25 families, 74 of them in `pop` 13, which ships 126 lines against 181 to 196 elsewhere.
          Those 283 flower slightly earlier than their genotyped family-mates (family-centred mean -0.343 days
          against +0.021, p = 0.030) and are more variable (SD 2.76 against 2.04), while their unadjusted means are
          indistinguishable.
        - No two lines share a marker profile. Seven pairs are more than 95% identical on the binarised calls, and
          all seven are inside one family, so a grouped split never puts them on opposite sides.
        - The family is the group column and no feature: a breeder predicting for a new cross has no family of
          their own in the training data. It stays in the frame because the metric scores within it. No single
          marker gives it away either: the largest between-family share of a marker's variance is 0.037.
        - Scope (USE-8): one designed population of 25 crosses that all share B73 as a parent, one 2006-2007 trial
          network of eight environments, one 2008 linkage map of 1,106 markers. Density is not the limit: a line
          carries about 25 recombination breakpoints over a 1,399 cM map, so 1,106 markers is roughly 31 per
          segment, and a tenth of them keeps 92% of the declared metric. The same population now has a genotype
          three orders of magnitude denser, but in absolute alleles rather than parent-of-origin dosages, which
          would be another task rather than a denser version of this one.
    """

    # Task
    target = "days_to_anthesis"
    problem_type = "regression"
    metric = Metric.from_context(
        "mean_group_pearsonr",
        reason=(
            "The decision is which lines of one new cross to advance, a ranking inside the cross, and the split "
            "holds out whole families. The original from context is the pooled correlation the field reports; "
            "Buckler et al. map flowering-time QTL and declare no prediction metric at all, and the closest "
            "published prediction work on this very population and these traits, Ogut et al. 2015 (Heredity "
            "114:552-563), reports ability within each family and across families side by side and warns that the "
            "across-family figures run up to twice the within-family ones. MET-18 is what makes the declaration "
            "per family: 69.3% of the variance of the line values lies between the 25 families, and a predictor "
            "that knows nothing but each test family's own true mean scores a pooled r of 0.793, against 0.209 for "
            "a ridge at alpha 1,000 and 0.245 for an untuned LightGBM on the markers, while that same predictor "
            "scores exactly 0 within a family, which is this metric's convention for a prediction that does not "
            "vary inside a group. A pooled score would therefore rank models by how well they recover a ranking of "
            "the crosses that the breeder already holds: the non-recurrent founder's own days to tassel, measured "
            "in these very trials, predicts its family's mean at r = 0.965, and predicting held-out lines from "
            "that number alone scores a pooled r of 0.764 against the markers' 0.225. Per family, over all 60 "
            "shipped splits, the ridge at alpha 1,000 scores 0.351 (SE 0.005 over splits, 0.030 over the 25 "
            "families) and the untuned LightGBM 0.265, where the repo's untuned ridge at alpha 1 scores 0.164; the "
            "best honest model found is a ridge at alpha 3,000 on within-family centred inputs at 0.421. The "
            "metric is what the breeder buys: response to selection is intensity x accuracy x the within-family "
            "SD, and that SD is fixed at 1.99 days here, so ranking models by the within-family correlation ranks "
            "them by realised gain. Selecting the earliest fifth of each held-out cross returns about 1.0 days for "
            "the ridge against 0.77 for a random forest, which is 40% of what a perfect ranking would return, and "
            "is positive in 94% of crosses."
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
            them together, so a model may use all rows of a test family (`all_rows`). That grant is declared for
            the use case and not for a gain, and here it is worth nothing measurable: centring a test family's
            markers on its own mean rather than on the training mean gives identical scores, because the declared
            metric is a correlation inside the group and a per-family shift does not change it. What does pay is
            centring the markers inside every family on the training side, which needs no grant at all and lifts
            the untuned ridge from 0.164 to 0.278.
        """,
    )
    splits_comment = """
        The default repeated grouped protocol on the 25 families, 20 repeats of 3 folds, 60 splits: each test fold
        holds 8 or 9 whole families and 1,442 to 1,729 of the 4,699 lines. It replaces the random holdout over
        lines that the benchmarking work on these panels uses, which was designed for a different question,
        comparing algorithms inside a population that is already phenotyped, and is a habit rather than a choice
        for ours (SPLIT-5): a random split puts the full siblings of every test line in the training data, which a
        breeder ranking a new cross does not have, and it is measurably not harmless, since the markers name a
        line's family on 50.3% of held-out lines against 4.0% by chance, so an IID split hands a model the
        between-family component the grouped one withholds (pooled R^2 +0.220 against +0.051). Leaf L-EXP.kind of
        the split tree. All 60 training sides are distinct family sets and each family is a test family exactly 20
        times, but the sides overlap at a mean Jaccard of 0.498, so the honest unit is the family: the spread over
        repeats is descriptive, and the uncertainty about a new cross is the spread over the 25 families, four to
        six times the spread over splits.

        What the split costs, measured on both metrics, since they disagree. On the declared metric it costs 0.024
        for the untuned ridge, 0.035 for a random forest and 0.036 for LightGBM against the same 60 splits drawn at
        random over lines; paired family by family it costs 0.017 to 0.028. On a pooled R^2 it costs 0.370. The
        alternatives were run and none is better: a map-keyed split inside each family is no harder than random
        lines, a founder's half-sib group is the family itself since B73 is the only common parent, and
        leave-one-germplasm-group-out is markedly harder but has five groups, one of them a single family.

        Why a pooled R^2 reads as no signal here, and why that reading is refused. Every model scores below the
        training mean on unseen families at every ridge penalty, pooled R^2 running from -0.84 to -0.136, and the
        group probe's learnability figures are negative for all of them (ridge -0.500, random forest -0.028,
        LightGBM -0.025, 5-NN -0.222). On its face that is SPLIT-28, a task with no signal across its groups. It is
        not: the between-family component is not reachable from these features by construction, since the markers
        are parent-of-origin dosages that name no founder, and models do not merely miss an unseen cross's mean but
        get it backwards, predicting means in a 76.6 to 77.7 band against a true 70.2 to 82.9 and correlating
        -0.72 (ridge) and -0.78 (random forest) with it across the 25 families. The signal is inside the family,
        where the decision and the declared metric are, and it is measured rather than asserted: the ridge at alpha
        1,000 scores a per-family 0.351 and is positive on 60 of 60 splits and in 24 of the 25 families, a random
        forest 0.303, and a null that shuffles the labels inside each test family puts the observed score 53
        standard deviations above it (200 runs, null mean 0.0005, SD 0.0068, none reaching the observed). A reader
        who scores this dataset with a pooled R^2 will conclude the task is unlearnable; that is the metric's
        choice being skipped, not the task. The curator signs that reading off in the record's review.
    """
    accepted_check_warnings = {
        "groups_test_groups_few": (
            "25 families, 8 or 9 per test fold and 1,442 to 1,729 lines scored per fold. The signal across groups "
            "is measured, not assumed, and on the spread that matters, which is over the families rather than over "
            "the 60 splits that reuse them: the ridge at alpha 1,000 scores a per-family 0.351 with an SD of 0.150 "
            "over the 25 families, an SE of 0.030, positive in 24 of them, running from -0.043 (P39, sweet corn) "
            "to +0.506; a random forest scores 0.303 and beats the dummy on 100% of the 30 splits the task probe "
            "runs by +0.3026 (SE 0.0087); the training mean is undefined per family because it is constant there, "
            "and a predictor given each test family's true mean scores exactly 0. A within-family label "
            "permutation null over 200 runs has mean 0.0005 and SD 0.0068, putting the observed 53 SDs above it "
            "with no run reaching it. The task is a breeder's own: the families are the crosses a breeder makes, "
            "and a few of them is what a breeding programme holds."
        ),
    }

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        # The genotype table's first line is a shape header (`4699 1110 1`), and its header row names 1,110
        # columns for 1,111 fields, so the first field, the line id, becomes the index.
        genotypes = pd.read_csv(raw_dir / GENOTYPES, sep="\t", skiprows=1, index_col=0)
        genotypes.index.name = "line"
        return {
            "genotypes": genotypes,
            "markers": pd.read_csv(raw_dir / MARKER_MAP, sep="\t", header=None, encoding="latin-1"),
            "lines": pd.read_csv(raw_dir / LINE_VALUES, sep="\t"),
        }

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        genotypes = raw["genotypes"]
        markers = marker_order(raw["markers"])
        columns = [c for c in genotypes.columns if c.startswith("i")]
        if len(columns) != len(markers):
            raise ValueError(f"{len(columns)} marker columns against {len(markers)} in the released map")
        # 1. The line ids the table carries are the line table's own, with its values.
        published = raw["lines"].set_index("Geno_Code")
        shared = published.reindex(genotypes.index)
        if shared["Days_To_Anthesis_BLUP_Sum0607"].isna().any():
            raise ValueError("a genotype row's line id is not in the published line table")
        if not np.allclose(shared["Days_To_Anthesis_BLUP_Sum0607"], genotypes["days2anthesis"]):
            raise ValueError("a genotype row's trait does not match the published line value for that id")
        # 2. The marker columns are the map's markers in linkage order, which the correlation structure confirms:
        #    neighbours inside a chromosome move together and the nine chromosome boundaries break that.
        calls = genotypes[columns].astype("float32").to_numpy()
        adjacent = np.array([abs(np.corrcoef(calls[:, k], calls[:, k + 1])[0, 1]) for k in range(len(columns) - 1)])
        chromosome = markers["chromosome"].to_numpy()
        boundary = chromosome[:-1] != chromosome[1:]
        if not (np.min(adjacent[~boundary]) > np.max(adjacent[boundary])):
            raise ValueError("the marker columns are not the released map's order: the linkage structure disagrees")
        # 3. One row per line: the family, the target, and the markers under the source's own names. The line id
        #    is an identifier and does not ship; days to silk and the interval are never selected in (LEAK-10).
        names = [f"{m}_chr{int(c)}_{p:g}cM" for m, c, p in markers[["marker", "chromosome", "position_cm"]].values]
        df = pd.DataFrame(
            {
                "family": genotypes["pop"].astype("int16").to_numpy(),
                self.target: genotypes["days2anthesis"].astype(float).to_numpy(),
            }
        )
        df = pd.concat([df, pd.DataFrame(calls, columns=names)], axis=1)
        if len(df.columns) != len(markers) + 2:
            raise ValueError(f"{len(df.columns)} columns against the {len(markers) + 2} the task has")
        if df[self.target].isna().any() or df["family"].isna().any():
            raise ValueError("a line is missing its family or its target")
        return df.reset_index(drop=True)

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # Every column is numeric: a marker call is an imputed parent-of-origin dosage (0 to 2), the family is the
        # group column and the target is days.
        return FeatureTypes()
