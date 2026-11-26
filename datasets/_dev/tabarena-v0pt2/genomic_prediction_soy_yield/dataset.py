"""Curated dataset definition for `genomic_prediction_soy_yield` (data-foundry v2). Evidence: README.md."""

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
    Source,
    TaskSummary,
    TimeBasis,
)

RAW_FILES = ("data.line.qa.csv", "data.check.qa.csv", "gen.qa.csv")
FIT_ITERATIONS = 10_000
# The six checks grown across the trial, in the blocks of every family: the common parent IA3023 and five
# cultivars. The other 39 strains of the check table are the families' own founder parents (`check_effects`).
COMMON_CHECKS = ("IA3023", "U06-100052", "LD04-11056", "LD04-13265", "IA2094", "U09-215057")


def two_way_effects(plots: pd.DataFrame) -> tuple[pd.Series, pd.Series]:
    """The least-squares effects of `yield = strain + environment`, an additive fit without an interaction.

    Solved by backfitting, alternating group means, which converges to the least-squares solution; the environment
    effects are centred over the environments, so the strain effects keep the kg/ha scale.
    """
    y = plots["yield"].to_numpy(float)
    strain, strains = pd.factorize(plots["strain"], sort=True)
    env, envs = pd.factorize(plots["environ"], sort=True)
    n_strain, n_env = np.bincount(strain), np.bincount(env)
    strain_effect, environment = np.zeros(len(strains)), np.zeros(len(envs))
    for _ in range(FIT_ITERATIONS):
        new_strain = np.bincount(strain, y - environment[env]) / n_strain
        new_env = np.bincount(env, y - new_strain[strain]) / n_env
        new_env -= new_env.mean()
        shift = max(float(np.abs(new_strain - strain_effect).max()), float(np.abs(new_env - environment).max()))
        strain_effect, environment = new_strain, new_env
        if shift < 1e-9:
            break
    else:
        raise ValueError(f"the effects moved by {shift:.2e} kg/ha in the last iteration: not converged")
    return pd.Series(strain_effect, index=strains), pd.Series(environment, index=envs)


def check_effects(
    checks: pd.DataFrame, environments: pd.Index, strains: tuple[str, ...] = COMMON_CHECKS
) -> tuple[pd.Series, pd.Series]:
    """Where a plot was grown, measured on the check plots alone: model 1 of Diers et al. 2018.

    The environment effects are the centred environment term of the check + environment fit over the plots of the
    common checks, the founder parents left out. One field block is one set of one environment and holds one family;
    its effect is the mean residual of its check plots after the check x environment means, shrunk toward 0 by
    `vb / (vb + ve / n)` with moment estimates of the block variance `vb` and the plot variance `ve`, as the paper
    takes its block effects as BLUPs. No line's yield enters either effect.
    """
    used = checks[checks["strain"].isin(strains) & checks["environ"].isin(environments) & checks["yield"].notna()]
    _, environment = two_way_effects(used)
    residual = used["yield"] - used.groupby(["environ", "strain"])["yield"].transform("mean")
    by_block = residual.groupby([used["environ"], used["set"]])
    block = by_block.agg(["mean", "size"])
    ve = float(by_block.var().mean())
    vb = max(float(block["mean"].var() - (ve / block["size"]).mean()), 0.0)
    return environment, block["mean"] * vb / (vb + ve / block["size"])


def line_values(plots: pd.DataFrame, checks: pd.DataFrame, strains: tuple[str, ...] = COMMON_CHECKS) -> pd.Series:
    """One yield value per line in kg/ha: the mean of its plots, each corrected for where it was grown.

    A plot's environment effect and the effect of its field block come from the check plots alone
    (`check_effects`), so no line's yield enters another line's value; what is left is averaged over the line's own
    plots, which keeps the value on the kg/ha scale and does not shrink it toward the mean.
    """
    plots = plots.dropna(subset=["yield"])
    environment, block = check_effects(checks, pd.Index(plots["environ"].unique()), strains)
    env_effect = plots["environ"].map(environment).to_numpy(float)
    block_effect = block.reindex(pd.MultiIndex.from_frame(plots[["environ", "set"]])).to_numpy()
    uncovered = np.isnan(env_effect) | np.isnan(block_effect)
    if uncovered.any():
        raise ValueError(f"{int(uncovered.sum())} line plots sit where the checks of the adjustment were not grown")
    return (plots["yield"] - env_effect - block_effect).groupby(plots["strain"]).mean().rename("yield_kg_ha")


class GenomicPredictionSoyYield(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How much grain will a soybean line yield in the Midwest trial network, from its SNP genotype alone?",
        use_case="A soybean breeder ranks the inbred progeny of a cross before the field season and picks which lines "
        "to put into yield trials, from the genotype alone (genomic selection), without having grown any of them.",
        row="One recombinant inbred line of the SoyNAM population (5,143 lines of 39 biparental families, all sharing "
        "the parent IA3023), with its quality-assured SNP calls and its yield over the 2011-2013 trials.",
        predicted="The line's grain yield in kilograms per hectare, as the trials measured it: the mean of its plots "
        "after each is corrected for its environment and its field block, both measured on the check plots.",
        known="Which copy of each of 4,312 SNP markers the line carries (0, 1 or 2; a marker the line's cross does "
        "not segregate for is not scored and stays missing), and which cross the line comes from.",
        split="Whole crosses are held out: the test lines are the progeny of a cross whose yields nobody has "
        "measured, which is what a breeder faces with a new cross.",
        changes="We compute the line's yield value from the plot yields, since the source publishes plots, not line "
        "values; the agronomic traits measured in the same plots (height, maturity, lodging, protein, oil, seed size) "
        "are left out, as they are not known before the season.",
        fit="approximate",
        fit_reason="The inputs are the genotype a breeder holds before the season and the target is the yield the "
        "trials measured, on the scale the breeder selects on. The gap is the germplasm: SoyNAM is an unselected "
        "research panel with seven exotic founders, so the level reached here is not a breeder's at-home accuracy. "
        "The breadth costs about 0.06 of within-family ability rather than flattering the score (the notes measure "
        "it).",
    )

    # Dataset
    unique_name = "genomic_prediction_soy_yield"
    domain = "biology & life sciences"
    sources = (
        Source(
            role="publication",
            platform="Other",
            url="https://cran.r-project.org/package=SoyNAM",
            license="GPL-3",
            year="2015",
            bibtex="""
                @manual{xavier2015soynam,
                  title = {{SoyNAM}: Soybean Nested Association Mapping Dataset},
                  author = {Xavier, Alencar and Beavis, William and Specht, James and Diers, Brian and Mian, Rouf
                            and Howard, Reka and Graef, George and Nelson, Randall and Schapaugh, William and Wang,
                            Dechun and Shannon, Grover and McHale, Leah and Cregan, Perry and Song, Qijian and Lopez,
                            Miguel and Muir, William and Rainey, Katy},
                  year = {2015},
                  note = {R package, version 1.6.2 (2022-01-04); data of the SoyNAM project funded by the United
                          Soybean Board, downloaded 2015-11-16 from soybase.org/SoyNAM},
                  url = {https://cran.r-project.org/package=SoyNAM},
                }
            """,
            files=RAW_FILES,
        ),
    )
    data_tags = ()
    time_basis = TimeBasis(
        "UnseenGroup",
        "the breeder ranks the progeny of a cross the data does not hold, so whole crosses are held out and the "
        "trial years are not weighed: the target is the yield of a fixed genotype, measured once by one 2011-2013 "
        "protocol, and the field blocks the years differ by are removed from it. The split cannot test a later "
        "season, another trial network, or germplasm outside this panel's 40 parents. One limit follows from the "
        "panel's own design and is accepted with it: all 39 families share the parent IA3023, so every test line has "
        "half-sibs in training and no held-out cross is unrelated to the training ones (a held-out family is still "
        "ranked at a pooled r of 0.433 by LightGBM).",
    )
    split_leaf = "L-EXP.kind"
    download_description = """
        The SoyNAM project's data, as the CRAN package publishes it. The three `soybase` R objects (the
        quality-assured release) are converted to CSV once; the definition reads the CSVs.

        mkdir -p local-data-warehouse/genomic_prediction_soy_yield && cd local-data-warehouse/genomic_prediction_soy_yield
        curl -L --fail https://cran.r-project.org/src/contrib/SoyNAM_1.6.2.tar.gz -o SoyNAM_1.6.2.tar.gz
        # once a newer version is on CRAN, 1.6.2 moves to
        # https://cran.r-project.org/src/contrib/Archive/SoyNAM/SoyNAM_1.6.2.tar.gz
        # sha256 0bd87f7b101456006a42a11679809349f7545b95dee0b43d954aa5b642995aaa
        tar xzf SoyNAM_1.6.2.tar.gz SoyNAM/data/soybase.RData
        uvx --from rdata==1.1.0 --with pandas==2.3.3 --with numpy python -I -c "
        import numpy as np, pandas as pd, rdata
        d = rdata.read_rda('SoyNAM/data/soybase.RData')
        for name in ('data.line.qa', 'data.check.qa'):
            d[name].reset_index(drop=True).to_csv(name + '.csv', index=False)
        g = d['gen.qa']
        pd.DataFrame(np.asarray(g), index=np.asarray(g.coords['dim_0'].values),
                     columns=np.asarray(g.coords['dim_1'].values)).rename_axis('strain').astype('Int8').to_csv('gen.qa.csv')
        "
        rm -r SoyNAM SoyNAM_1.6.2.tar.gz
        Expected SHA-256: data.line.qa.csv ade35f885d05cbf7d4be05149c4ff274117e8463209e5a87c146cea06311b111,
        data.check.qa.csv 7d0f20376083cb709d8235851e3c0e35084c36b13502b48f3980ab498e51f43c,
        gen.qa.csv ef2ba68429e04ca439d220bb0bd3afd5e85811ff023e87685c94369b85b5eb18.
    """
    curation_comments = """
        We start with the quality-assured `soybase` release of the SoyNAM R package: `data.line.qa` (62,572 plots of
        the lines), `data.check.qa` (10,721 plots of the checks and parents) and `gen.qa` (5,180 x 4,312 SNP calls).

        - Where the data first appeared (PROV-8, PROV-9): the SoyNAM project released it on SoyBase, whose page the
          package cites ("downloaded on November 16th 2015 from soybase.org/SoyNAM") and which now answers 404. The
          CRAN package of the project's own members is the surviving publication: version 1.0 of 2015-07-29, 1.2 of
          2015-11-18 right after that download, 1.4 of 2018-02-02 with the Indiana 2013-2014 trials, and the pinned
          1.6.2 of 2022-01-04. Hence the year 2015. Diers et al. 2018 (G3 8(10):3367, doi:10.1534/g3.118.200332)
          describe the trials, Song et al. 2017 (Plant Genome 10(2)) the SNP chip, Xavier et al. 2016 (G3 6(8):2611)
          genomic prediction in this panel.
        - Prediction point: before the field season, when the cross has been made and its inbred progeny genotyped,
          and before any of them has been grown. Everything measured in the plots is after it: the yield is the
          target, and height, maturity (R8), lodging, protein, oil and seed size are left out (LEAK-10). They are
          the largest thing the definition keeps out, so the size is worth stating: line values of the six traits,
          built as the target was before 2026-11-26, score +0.391 on the declared metric (R^2 0.191) against the
          markers' +0.213 (R^2 0.057), R8 alone +0.168, and markers with the six traits stacked +0.332, which is
          +0.12 (+56%) over the markers alone (honest five-fold cross-validation inside each family).
        - Maturity is the first thing a breeder asks of a soybean yield model. Within a family the line value
          correlates 0.266 with an R8 line value built the same way, and ridge's within-family ability falls only
          from 0.198 to 0.182 when that maturity component is taken out of the yield inside the family, while a
          genomic prediction of R8 alone correlates 0.110 with the yield (3 grouped folds). A maturity component is
          there; the task is yield, not maturity.
        - The release ships plot yields, not line values, so the line value is ours to compute (one row per line is
          what the breeder decides on, SPLIT-23). Each of the 56,929 plots that carry a yield is corrected for its
          environment and for its field block, both measured on the check plots alone, and a line's corrected plots
          are averaged, so the value keeps the kg/ha scale and is not shrunk toward the mean (MET-3). That is model
          1 of Diers et al. 2018, which takes the block effects from the checks and shrinks them toward 0 as BLUPs;
          here the shrinkage is the variance ratio `vb / (vb + ve / n)`, 0.43 to 0.92 over the 1,707 blocks (median
          0.75 at 4 check plots). The package's own `BLUP()` builds its `CHECK()` index from check rows only in the
          same spirit. Two departures from the paper remain true: its second stage has the entry random and no
          environment term at all, while ours averages the line's own corrected plots and carries a centred
          environment effect, the largest term; and its block effects come from 10 check varieties with a
          planting-date covariate, where we have the six checks grown across this trial and no planting date, which
          is not in the quality-assured release at all (in the original it takes 0 to 3 values per environment, 1.02
          per environment x set block, so the environment term absorbs it). Neither release supports the paper's
          exact model, since the block set is only in the quality-assured objects and the planting date only in the
          original ones. Measured on the shipped data: the environment effects run from -1,436 (MI 2012) to +1,536
          (NE 2011) kg/ha, the block effects have an SD of 318 kg/ha (425 before the shrinkage), and a plot departs
          from its line's value by 539 kg/ha SD. The line values run from 2,029 to 4,584 kg/ha (mean 3,578, SD 354;
          within a family 237); with 11 plots a line on average, the entry-mean heritability is 0.789, against the
          0.822 Diers et al. publish in their Table 2. (The 125,468 variance between the line values already carries
          the plot error's 290,930/11.)
        - Both corrections come from the check plots alone, so no line's yield enters another line's value
          (LEAK-10) and no statistic over the lines enters the target (LEAK-29, LEAK-30): a line's value is the mean
          of its own plots, and all the line table contributes to the correction is which 18 environments have a
          line yield at all. The check table's 45 strains, which fill the 1,707 blocks with 9,755 plots, are not 45
          checks: 39 are the families' own founder parents, 38 of them standing only in their own family's blocks
          (40 to 45 blocks each) and LD02-4485 serving as a general check in 18 families while 66 of its 416 plots
          sit in the blocks of family 12, the family it fathered. The correction uses the other six, grown across
          the trial: IA3023, the common parent of every line, in the blocks of all 39 families (1,367), with
          U06-100052 (1,702), LD04-11056 (1,327) and LD04-13265 (1,323), and IA2094 and U09-215057 in 18 families
          each (371 and 370). Those six fill every one of the 1,707 blocks with 7,294 plots (1 to 16 a block, median
          4), so every line plot has both corrections and the same strains measure the field in every family's
          blocks. Taking the 39 founders in as well, each carrying its own family's genetics, moves the line values
          by 27.8 kg/ha SD (r 0.9969, within-family r 0.9942; family means by at most 38 kg/ha) and lifts the
          declared metric by 0.005 for ridge while lowering it by 0.001 for LightGBM over 3 grouped folds, inside a
          fold-to-fold spread of 0.05 and 0.03.
          Removing the block at all is what matters: each family was planted in its own four blocks (sets A to D),
          so without the correction a family's value carries the patch of field it was grown on. Against a value
          corrected for the environment only, the line values correlate 0.9585 (Spearman 0.9476) and differ by 103
          kg/ha SD, against a line SD of 354.
        - The construction was brought into line with Lennart's build of this dataset on 2026-11-26. Before that the
          environment effects were fitted over all 56,929 line plots, which tied a test line's yield to the value of
          the training lines grown beside it, and the block correction was one slope on an index of all 45 check
          strains. The new values correlate 0.9925 with the old ones (Spearman 0.9906; within a family 0.987, the
          lowest family 0.956), sit 29 kg/ha lower on average and differ by 44 kg/ha SD, 39 kg/ha within a family,
          against a line SD of 354. The score moves less than a fold: over 3 grouped folds ridge by
          eigendecomposition scores 0.207 on the old values and 0.198 on the new ones (the paired difference per
          fold runs -0.002 to -0.017) and an untuned LightGBM 0.223 against 0.229 (-0.011 to +0.036 for the new
          values), while either model's score moves 0.03 to 0.06 between folds. The entry-mean heritability falls
          from 0.809 to 0.789, since the check-based corrections carry their own error into a plot.
        - Note: the plain mean of a line's plots, the simplest alternative, correlates 0.937 (Spearman 0.920) with
          the shipped value and differs by 129 kg/ha SD. It is biased by which environments a family was grown in: a
          family misses up to 3 of the 18 environments, whose effects span 2,972 kg/ha.
        - The quality-assured release is the one we read, not the original `soynam` objects of the same package
          (`data.line`, `data.check`, `gen.raw`) and not the Azodi et al. 2019 cut (below). The reason is the field
          block: `data.line`'s `spot` column has one value per environment (all 60,744 rows are set `2A`), so the
          block the data paper corrects for cannot be recovered from it, while `data.line.qa` carries the set (156
          blocks = 39 families x 4). The cost is 401 lines, one family (46) and 299 markers; family 46 is the
          source's own QA decision, dropped by Diers et al. because its lines were genotypically identical with the
          female founder. The two phenotype tables agree on 53,397 of the 55,945 plot yields they share.
        - Missing marker calls stay missing (CLEAN-7): 25.65% of the calls are not scored. They are not noise but the
          design, and the structure is a block structure: of the 168,168 family-by-marker blocks (39 x 4,312), 41,304
          (24.56%) carry no call at all, 126,584 (75.27%) are scored on 90% or more of the family's lines, 280
          (0.17%) sit between 10% and 90% and none between 0.1% and 10%, and every one of the 126,864 blocks with
          any call is polymorphic within its family. So a marker is scored in the families whose cross segregates
          for it, and a breeder meets the same pattern in a new cross. What the pattern is worth depends on the
          score, which an IID re-user of this frame should know: pooled, the mask of unscored calls alone is worth
          R^2 +0.1629 while the genotype values are worth +0.0016, and the mask names the family exactly (k-means on
          the mask recovers the 39 families at adjusted Rand 1.0000), so an IID split or a pooled metric here would
          measure the handling of missing values. Within a family, where the declared metric scores, the mask is
          worth r -0.028 against the calls' +0.213, and filling the blocks with the family mean moves the declared
          metric by +0.0009. No imputation, over all rows or within a family.
        - Leak probes (3 splits, untuned LightGBM): no test line has an exact feature copy in training on any of the
          60 splits, the nearest-neighbour R^2 is negative (-0.42 on the closest tenth), and a depth-2 or depth-3
          tree on the label scores below the mean. Single features score high (`Gm19_40068456_A_G` alone R^2 0.145,
          two markers on chromosome 17 0.118 and 0.115; the all-feature fit falls from 0.072 to 0.047 without the
          first), and what they read is the missingness, not the allele: `Gm19_40068456_A_G` is scored in 1,928 of
          the 5,143 lines and segregates in 15 of the 39 families, its missing indicator alone scores 0.144 against
          the call's 0.145, and among the lines that carry a call the dose explains R^2 0.0078 pooled and 0.0022
          within a family (the three genotype classes differ by 70 kg/ha against a line SD of 354). The column is a
          label of the cross, which is also why a single feature beats the all-feature fit (0.072). It is not a
          shortcut: per family, the best single feature scores 0.016 against 0.244 for LightGBM on all markers, and
          under the family split a test family's own mean is unreachable. Which markers are unscored is information
          a breeder has for a new cross too, since its parents fix the same loci.
        - The genotypes ship as the source codes them, 0, 1 or 2 copies of one allele (6.5% of the calls are
          heterozygous), as numeric counts (CLEAN-14), with the source's marker names (chromosome and position, such
          as `Gm01_10510009_G_T`). No marker is constant, all-missing or an exact copy of another on the shipped
          lines, and no two lines carry the same genotype, so the standard drops remove nothing.
        - Anomaly: 70 of the 5,142 lines that both matrices hold have raw and quality-assured genotype rows that
          disagree on 10% to 85% of their shared calls, where every other line disagrees on none (median 0%), so for
          those lines one of the two matrices holds a different sample. Both rows still match their own family better
          than any other of the 39, so it is a mix-up inside the family, not a swapped family. The shipped matrix is
          the quality-assured one and nothing is mixed; the 70 lines stay, as there is no evidence which of the two
          rows is the line's own. (Noted while comparing the releases: 1,984 of the 4,312 markers are coded against
          the other allele in `gen.raw` than in `gen.qa`, which is why a naive comparison of the two matrices
          disagrees on 43.2% of all calls.)
        - Version: the benchmark TabBench-Bio ships the Azodi et al. 2019 cut of this population (Dryad
          doi:10.5061/dryad.xksn02vb9, Zenodo record 4980429, CC0), 19 files of six species. Four are of this
          population: `soy_pheno.csv` (5,014 lines x HT, R8, YLD), `soy_geno.csv` (5,014 x 4,234 markers recoded
          -1/0/1) and `soy_CVFs.csv` (their random fold assignments), plus the shared `README.txt`. The definition
          reads none of them: their README and the paper's Methods say "Phenotype values were normalized between 0
          and 1" (the shipped YLD has mean 0 and SD 1), so the yield is off its kg/ha scale (MET-3), and the Methods
          say only that the data "were generated from the SoyNAM population", never how a line value was computed
          from the plots (PROV-13, PROV-8). Their 5,014 lines are what is left after "Lines with missing phenotypic
          value for any of the three traits were removed". The 15 files of the other five species (maize, rice,
          sorghum, spruce, switchgrass) are other panels and other tasks. The soy HT and R8 columns would be cuts of
          this table without a distinct task (PROV-6). Licences, since two are in play: what ships comes from the
          GPL-3 package, and the CC0 Dryad/Zenodo record is this derived cut, which we deliberately do not read.
        - The 37 rows of `gen.qa` that are parents or check cultivars, not lines, have no line yield and are left
          out, as are the 31 lines that have a yield but no genotype row and the 5,643 line plots whose yield is
          missing. `data.line.qa`'s 19th environment, NE 2013, carries no yield at all (5,230 of those 5,643 rows),
          which is why the correction runs over 18.
        - The family is the group column and no feature: a breeder predicting for a new cross has no family of their
          own in the training data. It is kept in the frame because the metric scores within it.
        - Considered and rejected as a feature: `set`, the plot column that looks like a field position. It is a
          per-line maturity group (5,149 of the 5,174 lines keep one letter across all their environments), it
          carries within-family R^2 0.1157 on the target in sample, more than the markers earn, and 0.6044 on
          adjusted R8, and it is half of the target's own block correction. It is a plot attribute, recorded with
          the trial and not held before the season, so it is out under LEAK-10. It is also the channel behind the
          row order: a predictor that is nothing but a line's position in the unshuffled frame scores 0.134 on the
          declared metric, because the line order tracks the maturity set. The framework's seed-42 shuffle is left
          on and is load-bearing here: after it, row position scores -0.0011.
        - Scope (USE-8): one population of 39 crosses that all share the parent IA3023, one 2011-2013 Midwest trial
          network of 18 environments, one SNP chip (Song et al. 2017, the SoyNAM 6K BreadChip). The germplasm is
          broader than a breeding programme's, and that is the gap the fit statement names: the panel was designed
          unselected, and 7 of the 38 non-recurrent parents are exotic PI accessions whose families average 3,159
          against 3,671 kg/ha for the 32 elite-parent families, so an elite programme crosses a narrower set than
          this and the level reached here is not a breeder's at-home accuracy. The direction is measured and it is
          not the flattering one: dropping the 7 exotic families lifts the declared metric from 0.236 to 0.276,
          while dropping 7 elite families instead lowers it to 0.219 (20 draws, SD 0.008), so the breadth costs
          about 0.06 of within-family ability, a heterogeneous training panel predicting the elite families worse.
          What the breadth does inflate is a pooled score: 55.3% of the line-value variance lies between families
          here against 35.0% among the elite families alone, one more reason the metric is within the family.
          Within-family selection in this panel is a different task (a random split of the lines), as is yield in
          another network.
    """

    # Task
    target = "yield_kg_ha"
    problem_type = "regression"
    metric = Metric.from_context(
        "mean_group_pearsonr",
        reason=(
            "The decision is which lines of one new cross to advance, a ranking inside the cross, and the split holds "
            "out whole crosses. The field's own criterion, which the papers on this population report (Xavier et al. "
            "2016, 'predictive ability'; Azodi et al. 2019 rank by Pearson's r 'as it is the standard metric for GP "
            "performance'), is the correlation pooled over the held-out lines; it is the original here. 55.3% of the "
            "variance of the line values lies between the 39 families (Diers et al. 2018 publish 0.57 from their own "
            "trials), and a pooled correlation scores that ranking of the crosses, which a breeder reads off the "
            "parents, more than the ranking inside a cross that genomic selection is bought for: on the first 6 "
            "shipped splits, giving every test line the true mean of its own cross and nothing else scores a pooled "
            "r of 0.68 (RMSE 238 kg/ha) against 0.24 (359 kg/ha) for ridge on the markers, while the same blind "
            "predictor scores 0 within the family. The breeder reads that ranking for free: the non-recurrent "
            "parent's own yield in the same trials predicts its family's mean at r = 0.937 over the 38 families. "
            "Pooled, the markers themselves are worth almost nothing (R^2 +0.0016 over 3 grouped folds, -0.0245 over "
            "5) while the mask of unscored calls alone is worth +0.1629, so a pooled score would rank models by "
            "their handling of missing values; within a family the mask is worth r -0.028 against the calls' +0.213. "
            "Ridge itself scores 0.236 pooled and 0.239 per family, so the declared metric does not flatter it."
        ),
        inputs={"group": "family"},
    )
    grouping = Grouping(
        on="family",
        labels="per_sample",
        prediction_unit="row",
        context="all_rows",
        definition="""
            One group is a biparental family of the SoyNAM population: the inbred progeny of IA3023 crossed with one
            of 39 other parents, 98 to 140 lines each. The source designed the panel as more than 5,000 inbred lines
            "derived from 40 biparental populations, where progenies were not exposed to selection", every family
            sharing "the cultivar IA3023 as the standard parent" (SoyNAM package manual, Dataset); genomic selection
            is used to rank the progeny of a cross before the season,
            so whole families are held out: a test family's yields are unknown, as they are for a cross nobody has
            grown. Each line is scored on its own. The breeder genotypes the whole progeny of the cross at once and
            ranks them together, so a model may use all rows of a test family (`all_rows`), and that is worth
            having: centring each marker within the row's own family lifts ridge on the declared metric from 0.229
            to 0.308 (+0.0795 over the 60 splits), as much as an oracle handed the test family's true mean (0.309).
            The grouping is recoverable from the missing-call pattern alone (k-means on the mask recovers the 39
            families at adjusted Rand 1.0000), so the gain is open to every participant, with or without the column.
        """,
    )
    splits_comment = """
        The default repeated grouped protocol on the 39 families, 20 repeats of 3 folds: each test fold holds 13
        whole families and about a third of the 5,143 lines. It replaces the split the work on this population uses,
        "an 80/20 training/testing approach ... where 20% of the lines were held out" over 10 replicates (Azodi et
        al. 2019, Methods), which was designed for their own question, benchmarking algorithms inside a population
        that is already phenotyped, and is a habit rather than a choice for ours (SPLIT-5): a random split puts the
        siblings of every test line in the training data, which a breeder ranking a new cross does not have. On a
        pooled R^2 that buys a lot (LightGBM 0.579 +- 0.010 over random lines against 0.270 +- 0.055 over held-out
        families, 3 x 3 folds), but nearly all of it is the family mean, which the declared metric does not score:
        on that metric the departure costs 0.036 (ridge) to 0.117 (LightGBM). A test family's own feature rows are
        all on the test side and may be read (`context="all_rows"`, the grouping definition): centring the markers
        within the row's own family is worth +0.0795 on the declared metric, so a model that ignores the grouping
        spends its fit on variance the metric discards. Leaf L-EXP.kind of the split tree. The repeats reuse the
        same 39 families, so the spread over repeats is descriptive, not 39 independent crosses.
    """
    accepted_check_warnings = {
        "groups_test_groups_few": (
            "39 families, 13 per test fold and about 1,714 lines scored per fold. The signal across groups is "
            "measured, not assumed: GBLUP, ridge, random forest and LightGBM all beat the dummy on the declared "
            "metric on 100% of the folds; per-family r has SD 0.09 to 0.10, so the standard error of the metric "
            "over 39 families is 0.015 to 0.017 against a mean of 0.18 to 0.23, 12 to 16 standard errors from "
            "zero; a null that shuffles the labels inside each test family (500 runs, each scored over the 60 "
            "folds as the models are) gives mean +0.0001, SD 0.0031, max 0.0089, so the measured score sits 68 "
            "null SDs above it at the p = 0.002 floor of 500 runs; and 38 of the 39 families score positive under "
            "ridge, all 39 under the other three."
        ),
    }

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        return {
            "lines": pd.read_csv(raw_dir / "data.line.qa.csv"),
            "checks": pd.read_csv(raw_dir / "data.check.qa.csv"),
            "genotypes": pd.read_csv(raw_dir / "gen.qa.csv", index_col="strain").astype("float32"),
        }

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        # 1. The line's yield value in kg/ha, from the plots: the environment and the field block of each plot,
        #    both measured on the check plots, removed; the line's own adjusted plots averaged.
        values = line_values(raw["lines"], raw["checks"])
        # 2. One row per line, genotypes beside the value; the parents and checks of `gen.qa` have no line value and
        #    the lines without a genotype have no features, so the two are joined on the lines they share.
        family = raw["lines"].drop_duplicates("strain").set_index("strain")["family"].astype("int16")
        df = pd.concat([family, values, raw["genotypes"]], axis=1, join="inner")
        assert df["family"].notna().all()
        assert df[self.target].notna().all()
        # 3. The line id is an identifier and leaves; the family stays as the group column.
        df = df.reset_index(drop=True)
        # 4. Constant, all-missing and duplicated marker columns (none on the shipped lines).
        markers = [c for c in df.columns if c not in ("family", self.target)]
        informative = df[markers].nunique(dropna=True) > 1
        df = df.drop(columns=[c for c in markers if not informative[c]])
        markers = [c for c in df.columns if c not in ("family", self.target)]
        duplicated = df[markers].T.duplicated()
        df = df.drop(columns=[c for c, dup in zip(markers, duplicated, strict=True) if dup])
        # Missing calls stay missing: a marker is not scored in a family whose cross does not segregate for it
        # (CLEAN-7), and imputing would invent the call a breeder does not have either.
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # Every column is numeric: the marker calls are counts of one allele (0, 1, 2; CLEAN-14), the family is the
        # group column and the target is kg/ha.
        return FeatureTypes()

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        plots = raw["lines"].dropna(subset=["yield"])
        checks = raw["checks"]
        environment, block = check_effects(checks, pd.Index(plots["environ"].unique()))
        with_founders = tuple(sorted(checks.loc[checks["yield"].notna(), "strain"].unique()))
        used = checks[checks["strain"].isin(COMMON_CHECKS) & checks["yield"].notna()]
        per_block = used.groupby(["environ", "set"]).size()
        shipped = line_values(plots, checks)
        lines = shipped.index.intersection(raw["genotypes"].index)
        family = raw["lines"].drop_duplicates("strain").set_index("strain")["family"].loc[lines]
        builds = {
            "the six common checks (shipped)": shipped,
            "the common checks and the 39 founders": line_values(plots, checks, with_founders),
            "the environment only, no field block": (plots["yield"] - plots["environ"].map(environment))
            .groupby(plots["strain"])
            .mean(),
            "the plain mean of a line's plots": plots.groupby("strain")["yield"].mean(),
        }
        builds = {name: value.loc[lines] for name, value in builds.items()}
        target_table = pd.DataFrame(
            {
                "r with the shipped value": {
                    k: round(float(np.corrcoef(v, builds["the six common checks (shipped)"])[0, 1]), 4)
                    for k, v in builds.items()
                },
                "within-family r": {
                    k: round(
                        float(
                            np.mean(
                                [
                                    np.corrcoef(v.loc[i], builds["the six common checks (shipped)"].loc[i])[0, 1]
                                    for i in family.groupby(family).groups.values()
                                ]
                            )
                        ),
                        4,
                    )
                    for k, v in builds.items()
                },
                "difference SD (kg/ha)": {
                    k: round(float((v - builds["the six common checks (shipped)"]).std()), 1) for k, v in builds.items()
                },
                "SD (kg/ha)": {k: round(float(v.std()), 1) for k, v in builds.items()},
                "between-family share": {
                    k: round(float(v.groupby(family).transform("mean").var() / v.var()), 3) for k, v in builds.items()
                },
            }
        ).rename_axis("line value from")
        return [
            Decision(
                "The line value corrects each plot for its environment and its field block, on the check plots alone",
                f"Each family was planted in its own four blocks, so an effect of the field becomes a difference "
                f"between families, and a family misses up to 3 of the 18 environments. Both corrections come from "
                f"the {len(COMMON_CHECKS)} checks grown across the trial: {len(used):,} plots that fill all "
                f"{len(block):,} blocks ({int(per_block.min())} to {int(per_block.max())} a block, median "
                f"{int(per_block.median())}), so no line's yield enters another line's value. The environment "
                f"effects span {float(environment.max() - environment.min()):,.0f} kg/ha and the shrunken block "
                f"effects have an SD of {float(block.std()):,.0f} kg/ha, against a line SD of "
                f"{float(shipped.loc[lines].std()):,.0f}.",
                target_table,
            ),
            Decision(
                "Missing marker calls stay missing",
                "A marker is scored in the families whose cross segregates for it, so the missing calls are the "
                "design of a nested association panel, not lost data; a new cross shows the same pattern.",
                df.drop(columns=[self.target])
                .isna()
                .groupby(df["family"])
                .mean()
                .mean(axis=1)
                .describe()
                .round(3)
                .rename("share of a family's marker calls not scored"),
            ),
        ]
