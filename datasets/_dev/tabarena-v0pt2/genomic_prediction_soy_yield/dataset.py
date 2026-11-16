"""Curated dataset definition for `genomic_prediction_soy_yield` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, Grouping, Metric, TaskSummary

TARGET = "yield_kg_ha"
# The six checks grown in nearly every set of every environment (the common parent IA3023 and five cultivars); the
# founders, also grown as checks, each stand only in their own family's sets.
COMMON_CHECKS = ("IA3023", "U06-100052", "LD04-11056", "LD04-13265", "IA2094", "U09-215057")
# A line whose raw genotype row agrees with its QA row at fewer than this share of the calls is another sample.
SAME_SAMPLE_MIN = 0.90


def two_way_effects(plots: pd.DataFrame) -> tuple[pd.Series, pd.Series]:
    """Least-squares effects of the additive model yield = entry + environment, without interaction.

    Solved by backfitting (alternating group means), which converges to the least-squares solution; the environment
    effects are centred over the environments.

    Args:
        plots: One row per plot with `strain`, `environ` and a non-missing `yield`.

    Returns:
        The entry effects indexed by strain, and the centred environment effects indexed by environment.
    """
    y = plots["yield"].to_numpy(dtype=float)
    entry_idx, entries = pd.factorize(plots["strain"], sort=True)
    env_idx, envs = pd.factorize(plots["environ"], sort=True)
    n_entry, n_env = np.bincount(entry_idx), np.bincount(env_idx)
    entry_eff, env_eff = np.zeros(len(entries)), np.zeros(len(envs))
    for _ in range(10_000):
        new_entry = np.bincount(entry_idx, y - env_eff[env_idx]) / n_entry
        new_env = np.bincount(env_idx, y - new_entry[entry_idx]) / n_env
        new_env -= new_env.mean()
        change = max(np.abs(new_entry - entry_eff).max(), np.abs(new_env - env_eff).max())
        entry_eff, env_eff = new_entry, new_env
        if change < 1e-9:
            break
    else:
        raise RuntimeError("backfitting did not converge")
    return pd.Series(entry_eff, index=entries), pd.Series(env_eff, index=envs)


def check_effects(checks: pd.DataFrame, environments: pd.Index) -> tuple[pd.Series, pd.Series]:
    """Environment and field-block effects estimated on the common check plots alone (Diers et al. 2018, model 1).

    The environment effects come from the additive check + environment fit. A block is one set of one environment
    (each holds one family); its effect is the mean residual of its check plots after the check x environment means,
    shrunk toward 0 by vb / (vb + ve / n) with moment estimates of the block variance vb and the plot variance ve.

    Args:
        checks: The check plots, with `environ`, `set`, `strain` and `yield`.
        environments: The environments with line yields.

    Returns:
        The centred environment effects indexed by environment, and the block effects indexed by (environ, set).
    """
    cc = checks[checks["strain"].isin(COMMON_CHECKS) & checks["environ"].isin(environments) & checks["yield"].notna()]
    _, env = two_way_effects(cc)
    res = cc["yield"] - cc.groupby(["environ", "strain"])["yield"].transform("mean")
    by_block = res.groupby([cc["environ"], cc["set"]])
    block = by_block.agg(["mean", "size"])
    ve = by_block.var().mean()
    vb = max(block["mean"].var() - (ve / block["size"]).mean(), 0.0)
    return env, block["mean"] * vb / (vb + ve / block["size"])


def line_values(plots: pd.DataFrame, checks: pd.DataFrame) -> pd.Series:
    """The mean of each line's plots after removing the check-based environment and block effects, in kg/ha.

    Args:
        plots: One row per line plot with `environ`, `set`, `strain` and a non-missing `yield`.
        checks: The check plots (see `check_effects`).

    Returns:
        The line values indexed by strain.
    """
    env, block = check_effects(checks, pd.Index(plots["environ"].unique()))
    env_eff = plots["environ"].map(env)
    block_eff = block.reindex(pd.MultiIndex.from_frame(plots[["environ", "set"]])).to_numpy()
    assert env_eff.notna().all(), "a plot without a check-based environment effect"
    assert not np.isnan(block_eff).any(), "a plot without a check-based block effect"
    return (plots["yield"] - env_eff - block_eff).groupby(plots["strain"]).mean()


def own_genotypes(
    raw: pd.DataFrame, qa: pd.DataFrame, family: pd.Series, lines: pd.Index, markers: list[str]
) -> tuple[pd.DataFrame, pd.Series]:
    """Each line's own calls: its raw row, or its QA row back on the raw coding where the raw row is another sample.

    The QA matrix codes 1,984 markers on the other allele and leaves blank every marker that does not segregate in a
    family; such a marker carries the common parent's allele in every line of the family, so a family-wide blank
    takes IA3023's raw call. A blank of a single line (a failed call) stays missing.

    Args:
        raw: The raw calls (`gen.raw`), one row per sample, indexed by strain.
        qa: The QA calls (`gen.qa`), indexed by strain.
        family: The family of each QA line, indexed by strain.
        lines: The task's lines.
        markers: The QA marker set.

    Returns:
        The calls of the lines (0/1/2, missing kept), and the source of each line's row.
    """
    raw, qa = raw[markers].astype("float64"), qa[markers].astype("float64")
    both = raw.index.intersection(qa.index)
    flipped = (raw.loc[both] == 2 - qa.loc[both]).sum() > (raw.loc[both] == qa.loc[both]).sum()
    qa.loc[:, flipped] = 2 - qa.loc[:, flipped]
    blank = qa.isna().groupby(family.reindex(qa.index)).all()  # family x marker: no line of the family has a call
    paired = lines.intersection(raw.index).intersection(qa.index)
    called = raw.loc[paired].notna() & qa.loc[paired].notna()
    same = ((raw.loc[paired] == qa.loc[paired]) & called).sum(axis=1) / called.sum(axis=1)
    source = pd.Series("raw", index=lines)
    source[lines.difference(qa.index)] = "raw, no QA row"
    source[same.index[same < SAME_SAMPLE_MIN].union(lines.difference(raw.index))] = "QA, repaired"
    repaired = source.index[source == "QA, repaired"]
    rows = qa.loc[repaired]
    fill = rows.isna().to_numpy() & blank.loc[family[repaired]].to_numpy()
    ia3023 = np.broadcast_to(raw.loc["IA3023"].to_numpy(), rows.shape)
    calls = raw.reindex(lines)
    calls.loc[repaired] = np.where(fill, ia3023, rows.to_numpy())
    return calls, source


class GenomicPredictionSoyYield(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "What grain yield, in kg/ha in an average environment of the trial, will a soybean line from a new cross "
            "give, predicted from its SNP genotype alone?"
        ),
        use_case=(
            "A soybean breeder, before field-testing the progeny of new crosses, ranks the inbred lines by their "
            "genotype and advances the best to yield trials (genomic selection), as Azodi et al. (2019) frame the "
            "task for this population."
        ),
        row=(
            "One recombinant inbred line of the SoyNAM population (39 families, each a cross of the common parent "
            "IA3023 with one founder), grown in 1 to 16 of 18 US Midwest environments in 2011-2013 (median 11)."
        ),
        predicted=(
            "The line's yield in kg/ha in the trial's average environment: the mean of its plots after removing the "
            "environment and field-block effects estimated on the check plots, so lines grown in different places "
            "compare fairly."
        ),
        known="The line's genotype at 4,312 SNP markers of the SoyNAM 6K chip (0, 1 or 2 copies of one allele).",
        split=(
            "Whole families are held out, so the test lines stand for the progeny of a cross never phenotyped before."
        ),
        changes=(
            "We compute the line value from the plot yields (the source ships plots, Azodi a standardized value of "
            "undocumented origin), and hold out whole families where Azodi held out random lines."
        ),
        fit="direct",
        fit_reason=(
            "The genotype is what a breeder knows of a new line before any field trial, and the line value over "
            "many environments is what selection acts on. A held-out family stands for a new cross with the "
            "program's common parent. Train and test lines share the 2011-2013 seasons, so no transfer to new years "
            "is tested."
        ),
    )

    # Dataset
    unique_name = "genomic_prediction_soy_yield"
    year = "2015"
    domain = "biology & life sciences"
    source = "Other"  # the SoyNAM project's release (SoyBase, now offline), shipped in the CRAN package SoyNAM
    source_url = "https://cran.r-project.org/package=SoyNAM"
    license = "GPL-3"  # the CRAN package's licence (DESCRIPTION, SoyNAM 1.6.2)
    download_description = """
        The SoyNAM data were released by the SoyNAM project on SoyBase (https://soybase.org/SoyNAM/, offline since
        2022); we download the CRAN package SoyNAM 1.6.2 (2022-01-04), which holds them as downloaded from SoyBase on
        2015-11-16, and export its .RData objects to parquet with pyreadr (no R needed).
        mkdir -p local-data-warehouse/genomic_prediction_soy_yield && cd local-data-warehouse/genomic_prediction_soy_yield
        wget https://cran.r-project.org/src/contrib/SoyNAM_1.6.2.tar.gz  # sha256 0bd87f7b101456006a42a11679809349f7545b95dee0b43d954aa5b642995aaa; later in src/contrib/Archive/SoyNAM/
        tar xzf SoyNAM_1.6.2.tar.gz
        uvx --from pyreadr==0.5.7 --with pandas==3.0.6 --with pyarrow python -c "import pyreadr; r = {**pyreadr.read_r('SoyNAM/data/soynam.RData'), **pyreadr.read_r('SoyNAM/data/soybase.RData')}; [r[k].astype({c: str for c in ('environ', 'strain', 'set')}).reset_index(drop=True).to_parquet(k.replace('.', '_') + '.parquet', index=False) for k in ('data.line.qa', 'data.check.qa')]; [r[k].rename_axis('strain').reset_index().to_parquet(k.replace('.', '_') + '.parquet', index=False) for k in ('gen.raw', 'gen.qa')]"
    """
    bibtex = """
        @misc{xavier2015soynam,
          title = {{SoyNAM}: Soybean Nested Association Mapping Dataset},
          author = {Xavier, Alencar and Beavis, William and Specht, James and Diers, Brian and Mian, Rouf and Howard, Reka and Graef, George and Nelson, Randall and Schapaugh, William and Wang, Dechun and Shannon, Grover and McHale, Leah and Cregan, Perry and Song, Qijian and Lopez, Miguel and Muir, William and Rainey, Katy},
          year = {2015},
          howpublished = {\\url{https://cran.r-project.org/package=SoyNAM}},
          note = {R package, version 1.6.2 (2022); data of the SoyNAM project downloaded from SoyBase on 16 November 2015}
        }
    """
    curation_comments = """
        We start with four objects of the CRAN package SoyNAM 1.6.2, exported to parquet: the SoyNAM project's quality-assured line plots (`data.line.qa`, 62,572 line-environment rows), its check plots (`data.check.qa`, 10,721 rows), the raw SNP calls (`gen.raw`, 5,590 samples x 4,611 markers) and the quality-assured SNP matrix (`gen.qa`, 5,180 lines x 4,312 markers).

        - Prediction point: a breeder ranks inbred lines of new crosses before they enter yield trials, so the only input is the line's genotype; no field trait of the line (height, maturity, lodging, seed composition) is known then, and none ships.
        - Source and year: the SoyNAM project (United Soybean Board; Song et al. 2017, Plant Genome 10(2), https://doi.org/10.3835/plantgenome2016.10.0109, for the population and the 6K SNP chip; Diers et al. 2018, G3 8(10):3367, https://doi.org/10.1534/g3.118.200332, for the yield trials and the QA) released the data on SoyBase, whose page is offline since 2022 (archived from March 2016). The CRAN package SoyNAM, written by the project's own members, holds them as "downloaded on November 16th 2015 from https://soybase.org/SoyNAM/index.php"; its first version is of 2015-07-29, so the year is 2015, the earliest dated public copy (PROV-9). It is a best guess: the SoyBase release date could not be pinned, and a SoyBase data store named SoyNAM_2014 hints at 2014 without a date. Azodi et al. (2019, G3 9(11):3691, Zenodo 4980429) published a derived cut (5,014 lines, 4,234 markers coded -1/0/1, three traits standardized to mean 0 and SD 1 although its README says "normalized between 0 and 1"); its yield `YLD` correlates 0.971 with the plain mean of a line's plots and neither its README nor the paper says how it was computed, so we rebuild from the origin (PROV-8, PROV-13) and cite Azodi for the task and the metric.
        - Metric: Pearson's r over all test lines, as Azodi et al. (2019, "Assessing predictive performance") compare their models by it, "as it is the standard metric for GP performance"; MSE only tuned the hyper-parameters (MET-5). A correlation ignores the scale and offset of the predictions, which matches a selection that ranks lines. On held-out families about half of the pooled r is the ranking of the families: 55% of the target's variance lies between families, and a breeder's no-genomics baseline, each line predicted by the yield of its founder parent grown as a check in the same trials (mid-parent value), scores pooled r 0.70 over all lines and 0.66 on the 9 shipped test folds (0.47-0.74; optimistic: in practice a parent's yield comes from earlier trials), above ridge (0.57) and LightGBM (0.56) on every fold. The ranking within a cross, what genomics adds at this decision, is the mean within-family r: 0.29 (ridge) and 0.26 (LightGBM); the two metrics order ten probe models alike on the shipped splits (Kendall tau 0.96, 2026-11-09).
        - Lines: the 5,146 lines of the QA phenotype table that have a yield and a genotype row (5,145 raw rows; one line, DS11-11202, has only a QA row; 28 QA lines have neither). The QA release drops 399 of the 5,544 genotyped lines of the original table, for the reasons Diers et al. (2018) give: a SNP genotype identical to the common parent IA3023, off-type segregation, and family 46, crossed with a wrong founder, whole; 154 of the 399 lie nearest to another family's mean genotype. The QA also merges the plots of near-identical entries under one line name (56 lines with more than 13 plots, up to 36; in 5 of them the merged entry is a distinct genotype, a sibling, not a copy). Kept, as the QA kept them: 96 lines nearest to another family's mean genotype (off-types) and 186 lines with more than 20% heterozygous calls (up to 66%; inbred lines from F5 plants carry about 6%), likely mixed seed or DNA. Parents and check cultivars are not selection candidates and are left out as rows; their plots only adjust the target.
        - Target: `yield_kg_ha`, the mean of a line's plots after removing the environment effect and the field-block effect of each plot, both estimated on the plots of the six common checks alone (IA3023 and five cultivars), as Diers et al. (2018, models 1 and 2) estimate shrunken block effects from the checks and use them as covariates. Each set of an environment is one field block that holds one family (1,707 of 1,707 environment x set blocks) and 1 to 16 plots of the common checks (median 4); the environment effects span -1,436 to +1,536 kg/ha and the block effects have an SD of 367 kg/ha (target SD 354), so without them a line, and a whole family, is ranked partly by where it was grown. Lines saw 1 to 16 of the 18 environments with yield (median 11; NE_2013 has no yield). Since the adjustments come from check plots only, no line's plots enter another line's target. The line value repeats better across disjoint halves of the environments than the least-squares means without blocks (decision table). SoyNAM spans late maturity group II to early IV, and a line's maturity (R8) correlates 0.33 with its yield (0.23 within families), so part of the ranking is lateness, as in the trial reports; no maturity ships.
        - Features: the calls of the 4,312 markers the SoyNAM group quality-assured "based on proportion of missing loci and correct segregation patterns" (package help), coded 0/1/2 as in the raw release (heterozygous 1 is 5% of the calls), as numbers: an allele dosage, the additive coding of genomic prediction. Each line takes its raw calls, the unprocessed values, where they are its own sample. For 70 lines (1.4%) the raw row of the same name is another sample: it agrees with the line's QA row at under 90% of the calls (down to 15%; 5,011 lines agree at 99% or more), since the QA renamed samples in its phenotypes and genotypes alike. These 70 lines, and DS11-11202, take their QA row back on the raw coding: the QA's allele flips (1,984 markers) undone, a marker the QA blanks for the whole family (it does not segregate there, so every line carries the common parent's allele) filled with IA3023's raw call, a failed call left missing. On the other lines this rebuilt QA row equals the raw calls in 99.3% of the cells. Three lines without a QA row keep their raw row. No line is dropped. Predicted from the other lines, the 70 lines reach a within-family r of -0.06 with their raw rows and 0.32 with the rebuilt QA rows, against 0.39 (SD 0.09) for 70 random lines, so the QA row is the sample that was phenotyped. The 299 markers outside the QA set are 53% missing and not used. Missing calls (1.4% of the cells, at most 19.8% of a marker) stay missing: no imputation over all rows.
        - Dropped: the line id (`strain`, an identifier; its middle digits are the family). The family is the group column, never a feature. No duplicate genotypes among the lines, no constant marker.
    """

    # Task
    target = TARGET
    problem_type = "regression"
    metric = Metric.source(
        "pearsonr",
        original="Pearson's correlation coefficient r between the predicted and the true trait value of held-out lines",
        reference="https://doi.org/10.1534/g3.119.400498",
    )
    grouping = Grouping(
        on="family",
        labels="per_sample",
        prediction_unit="row",
        context="all_rows",
        definition="""
            One group is a SoyNAM family: the 98 to 140 recombinant inbred lines of one cross between the common parent IA3023 and one of the founders ("derived from 40 biparental populations, where progenies were not exposed to selection", package help; 39 families after the QA). Genomic selection ranks the progeny of new crosses before they are phenotyped, so the test lines belong to families with no phenotyped sibling; about half of the variance of the line values lies between families (55%), which a random split of lines would hand to the model through the siblings. Each line is one prediction. The breeder genotypes and ranks the lines of a new cross together and knows which lines are siblings, so a model may see all rows of a test family (`all_rows`). Azodi et al. (2019) held out 20% of random lines, a within-population design; holding out whole families is stricter.
        """,
    )
    splits_comment = """
        Grouped splits on the family (3 folds, 13 families per test fold): every line of a cross stays on one side, so a model ranks the lines of crosses it has never seen, each with the common parent IA3023. Azodi et al. (2019) held out 20% of random lines instead.
    """

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        cols = ["environ", "strain", "family", "set", "yield"]
        return {
            "plots": pd.read_parquet(raw_dir / "data_line_qa.parquet", columns=cols),
            "checks": pd.read_parquet(raw_dir / "data_check_qa.parquet", columns=cols),
            "gen_raw": pd.read_parquet(raw_dir / "gen_raw.parquet").set_index("strain"),
            "gen_qa": pd.read_parquet(raw_dir / "gen_qa.parquet").set_index("strain"),
        }

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        # 1. The line value from the plots with a yield (NE_2013 has none), adjusted on the check plots, in kg/ha.
        plots = raw["plots"][raw["plots"]["yield"].notna()]
        values = line_values(plots, raw["checks"])
        family = raw["plots"].groupby("strain")["family"].first()
        # 2. The QA lines with a genotype row, on the QA marker set: each line's own sample (raw, or the QA row).
        lines = values.index.intersection(raw["gen_raw"].index.union(raw["gen_qa"].index))
        df, _ = own_genotypes(raw["gen_raw"], raw["gen_qa"], family, lines, list(raw["gen_qa"].columns))
        assert df.shape == (5146, 4312), df.shape
        # 3. The family as the group column; the line id (the index) is dropped.
        df.insert(0, "family", family.loc[lines].map("family_{:02d}".format).to_numpy())
        df[TARGET] = values.loc[lines].to_numpy()
        return df.reset_index(drop=True)

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["family"])

    def _decisions(self, raw, df) -> list[Decision]:
        plots = raw["plots"][raw["plots"]["yield"].notna()].copy()
        checks = raw["checks"]
        family = raw["plots"].groupby("strain")["family"].first()
        genotyped = raw["gen_raw"].index.union(raw["gen_qa"].index)
        lines = plots.groupby("strain").size().index.intersection(genotyped)  # sorted by the groupby
        env, block = check_effects(checks, pd.Index(plots["environ"].unique()))
        plots["block"] = block.reindex(pd.MultiIndex.from_frame(plots[["environ", "set"]])).to_numpy()
        shipped_name = "check-based environment and block effects (shipped)"

        def options(pl: pd.DataFrame) -> dict[str, pd.Series]:
            return {
                "plain mean of the plots": pl.groupby("strain")["yield"].mean(),
                "least-squares mean, line + environment": two_way_effects(pl)[0],
                "least-squares mean of the block-adjusted plots": two_way_effects(
                    pl.assign(**{"yield": pl["yield"] - pl["block"]})
                )[0],
                shipped_name: line_values(pl, checks),
            }

        full = {k: v.loc[lines] for k, v in options(plots).items()}
        fam = family.loc[lines]
        envs = np.array(sorted(plots["environ"].unique()))
        rng = np.random.default_rng(1)
        rep, within = {k: [] for k in full}, {k: [] for k in full}
        for _ in range(10):
            half = rng.permutation(envs)[:9]
            a = options(plots[plots["environ"].isin(half)])
            b = options(plots[~plots["environ"].isin(half)])
            for k in full:
                common = a[k].index.intersection(b[k].index).intersection(lines)
                va, vb, fa = a[k].loc[common], b[k].loc[common], fam.loc[common]
                rep[k].append(np.corrcoef(va, vb)[0, 1])
                da, db = va - va.groupby(fa).transform("mean"), vb - vb.groupby(fa).transform("mean")
                within[k].append(np.corrcoef(da, db)[0, 1])
        target_table = pd.DataFrame(
            {
                "r with the shipped value": {
                    k: round(float(np.corrcoef(v, full[shipped_name])[0, 1]), 3) for k, v in full.items()
                },
                "SD (kg/ha)": {k: round(float(v.std()), 1) for k, v in full.items()},
                "between-family share": {
                    k: round(float(v.groupby(fam).transform("mean").var() / v.var()), 3) for k, v in full.items()
                },
                "repeatability across environment halves": {k: round(float(np.mean(x)), 3) for k, x in rep.items()},
                "within families": {k: round(float(np.mean(x)), 3) for k, x in within.items()},
            }
        ).rename_axis("line value")
        n_env = plots[plots["strain"].isin(lines)].groupby("strain")["environ"].nunique()
        common_checks = checks[checks["strain"].isin(COMMON_CHECKS) & checks["yield"].notna()]
        env_table = pd.DataFrame(
            {
                "effect (kg/ha)": env.round(1),
                "common-check plots": common_checks.groupby("environ").size().reindex(env.index),
                "sets (blocks)": block.groupby(level=0).size().reindex(env.index),
                "SD of the block effects (kg/ha)": block.groupby(level=0).std().round(1).reindex(env.index),
                "lines with a yield": plots.groupby("environ")["strain"].nunique().reindex(env.index),
            }
        ).rename_axis("environment")
        _, source = own_genotypes(raw["gen_raw"], raw["gen_qa"], family, lines, list(raw["gen_qa"].columns))
        geno_table = source.value_counts().rename_axis("genotype row").rename("lines").to_frame()
        return [
            Decision(
                "The target adjusts each plot for its environment and field block, both estimated on the check plots",
                f"Lines were grown in {int(n_env.min())} to {int(n_env.max())} of 18 environments (median "
                f"{int(n_env.median())}), and each set of an environment is a field block holding one family; the "
                "source's data paper (Diers et al. 2018) removes block effects estimated on the check plots. The "
                "check-based value uses no line's plots for another line's value, repeats about as well as the "
                "block-adjusted least-squares mean and far better than the values without blocks (10 random halves of "
                "the environments; over all lines and within families).",
                target_table,
            ),
            Decision(
                "Environment and block effects from the six common checks",
                "Centred environment effects of the 18 environments with yield, from the check + environment fit, and "
                "the shrunken block effects of each environment's sets; every line plot has both.",
                env_table,
            ),
            Decision(
                "Each line's own genotype sample",
                f"A raw row that agrees with the line's QA row at fewer than {SAME_SAMPLE_MIN:.0%} of the calls is "
                "another sample; such a line takes its QA row back on the raw coding (flips undone, family-wide "
                "blanks filled with IA3023's call, failed calls missing), as does the one line with only a QA row. "
                "No line is dropped.",
                geno_table,
            ),
        ]
