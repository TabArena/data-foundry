"""Curated dataset definition for `fremtpl2` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, Metric, TaskSummary, drop_columns

RAW_FILES = {
    "freMTPL2freq.rda": "82c8598513d9fa78226b6c7d271a9940eca4b8083e9e32320a75d377bdfe15a3",
    "freMTPL2sev.rda": "78e6e5016ae046603b37e88ff8ad8ca327f5d59f827c1f75d140388de09b14b3",
}
"""The two tables of CASdatasets commit 227fb56b8734bdb7c0327a41180e01d2ddaeaf26, with their SHA-256."""

RATING_FACTORS = ["VehPower", "VehAge", "DrivAge", "BonusMalus", "VehBrand", "VehGas", "Area", "Density", "Region"]
"""The policy's rating factors, as the help page lists them (Exposure and ClaimNb aside)."""

AREA_LEVELS = ["A", "B", "C", "D", "E", "F"]
"""The help page: the density of the city community, "from "A" for rural area to "F" for urban centre"."""

DEFAULT_VEHICLE_AGE = 99
"""VehAge from here on (99 and 100, 48 rows) is a default date: no car is 86 to 98 years old, and 21 of the 23 cars of
age 99 in IDpol block 0 are 100 in their next-year row."""

BLOCK = 1_000_000
"""IDpol runs in seven blocks of a million (1-179,639 up to 6,000,016-6,114,330)."""


def _ids(column: pd.Series) -> np.ndarray:
    """IDpol, a factor of numbers in the rda files, as integers."""
    return pd.to_numeric(np.asarray(column.cat.categories)[column.cat.codes.to_numpy()]).astype("int64")


def next_year_rows(raw: pd.DataFrame) -> pd.DataFrame:
    """Pairs of rows that look like one policy in two consecutive years: evidence for the split, not used in cleaning.

    The rule: the later row's IDpol is the earlier one's plus 1,000,000 plus 1 to 9, it has the same brand, fuel,
    region, density and power, the driver is one year older and the car as old or one year older; the smallest offset
    wins.
    """
    fixed = ["VehBrand", "VehGas", "Region", "Density", "VehPower"]
    cols = ["IDpol", "DrivAge", "VehAge", *fixed]
    early = raw[cols].astype(dict.fromkeys(["VehBrand", "VehGas", "Region"], str))
    pairs = []
    for offset in range(1, 10):
        merged = early.assign(key=early["IDpol"] + BLOCK + offset).merge(
            early, left_on="key", right_on="IDpol", suffixes=("", "_next")
        )
        same = np.logical_and.reduce([merged[c].eq(merged[f"{c}_next"]).to_numpy() for c in fixed])
        aged = merged["DrivAge_next"].eq(merged["DrivAge"] + 1) & (merged["VehAge_next"] - merged["VehAge"]).isin(
            [0, 1]
        )
        pairs.append(merged.loc[same & aged.to_numpy(), ["IDpol", "IDpol_next"]].assign(offset=offset))
    found = pd.concat(pairs, ignore_index=True).sort_values(["IDpol_next", "offset"], kind="stable")
    return found.drop_duplicates("IDpol_next").drop_duplicates("IDpol")


class Fremtpl2(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How many claims will a French motor-insurance policy make in the part of the year it is insured?",
        use_case=(
            "For example, a pricing actuary sets the premium of motor third-party liability policies, estimating each "
            "policy's expected number of claims from its rating factors and the time it is insured."
        ),
        row=(
            "One of 677,991 policy records of an unnamed French insurer's motor portfolio, each observed mostly "
            "within one accounting year, about 2011 to 2013."
        ),
        predicted="The number of claims with a recorded cost in that period (0 to 16; 96.3% have none).",
        known=(
            "The car's power, age, brand and fuel, the driver's age, the bonus-malus level, the density, area and "
            "region of residence, and the time insured in the year, which may reflect a cancellation later in it."
        ),
        split=(
            "Random policy records are held out, standing for comparable policies of the same portfolio and years; the "
            "release has no dates, and a policy's record of another year can be on the training side."
        ),
        changes="",
        fit="approximate",
        fit_reason=(
            "The rating factors and the claim counts mirror pricing a policy, but the release has no calendar dates, "
            "so a later year cannot be held out as an insurer would (forced from temporal). Realized exposure is "
            "kept on purpose although it can reflect a later cancellation. The insurer is unknown."
        ),
    )

    unique_name = "fremtpl2"
    year = "2014"
    domain = "insurance"
    source = "Other"
    source_url = "https://dutangc.github.io/CASdatasets/reference/freMTPL.html"
    license = "GPL (>= 2), declared by CASdatasets; the insurer's terms not stated"
    data_tags = ("Spatial", "ForcedIIDFromTemporal")
    download_description = """
        Download the two tables of the CASdatasets R package (Dutang and Charpentier) at a pinned commit of its
        GitHub repository. Install rdata==1.1.0 and its dependencies in the environment used to run this definition.
        mkdir -p "${DATA_FOUNDRY_WAREHOUSE:-local-data-warehouse}/fremtpl2"
        curl -L --fail https://raw.githubusercontent.com/dutangc/CASdatasets/227fb56b8734bdb7c0327a41180e01d2ddaeaf26/data/freMTPL2freq.rda -o "${DATA_FOUNDRY_WAREHOUSE:-local-data-warehouse}/fremtpl2/freMTPL2freq.rda"
        curl -L --fail https://raw.githubusercontent.com/dutangc/CASdatasets/227fb56b8734bdb7c0327a41180e01d2ddaeaf26/data/freMTPL2sev.rda -o "${DATA_FOUNDRY_WAREHOUSE:-local-data-warehouse}/fremtpl2/freMTPL2sev.rda"
        Expected SHA-256: freMTPL2freq.rda 82c8598513d9fa78226b6c7d271a9940eca4b8083e9e32320a75d377bdfe15a3,
        freMTPL2sev.rda 78e6e5016ae046603b37e88ff8ad8ca327f5d59f827c1f75d140388de09b14b3.
        OpenML 41214 and 41215 are copies of the older CASdatasets 1.0-8 (2018), before the package's update of
        June 2022: 678,013 policies whose claim counts do not all match the claims table, so they are not this data.
        From the repository root, set DATA_FOUNDRY_DATASETS_ROOT=datasets/_dev/tabarena-v0pt2.
    """
    bibtex = r"""
        @manual{DutangCharpentierCASdatasets,
          author = {Dutang, Christophe and Charpentier, Arthur},
          title = {{CASdatasets}: Insurance Datasets},
          year = {2026},
          note = {R package version 1.2-1, GitHub commit 227fb56b8734bdb7c0327a41180e01d2ddaeaf26; freMTPL2freq and freMTPL2sev entered on 14 October 2014},
          doi = {10.57745/P0KHAG},
          url = {https://github.com/dutangc/CASdatasets}
        }
        @misc{NollSalzmannWuthrich2018,
          author = {Noll, Alexander and Salzmann, Robert and W{\"u}thrich, Mario V.},
          title = {Case Study: {French} Motor Third-Party Liability Claims},
          year = {2018},
          howpublished = {SSRN},
          doi = {10.2139/ssrn.3164764},
          note = {Code: https://github.com/JSchelldorfer/ActuarialDataScience, folder 1}
        }
    """
    curation_comments = """
        We start with data/freMTPL2freq.rda (677,991 policies) and data/freMTPL2sev.rda (26,444 claims) from CASdatasets commit 227fb56b8734bdb7c0327a41180e01d2ddaeaf26, joined on IDpol, the link the help page names.

        - Prediction point: the quotation of the policy for the accounting year, from the rating factors the help page lists; the source gives no dates ("observed mostly on one year", "approximately 2011-2013").
        - Target: ClaimNb as released (0 to 16), no cap, annualization, weight or offset. CASdatasets' update of 23 June 2022 set each count to the policy's claims in freMTPL2sev, as Wüthrich and Merz (2023, Sec. 13.1, p. 553) do by hand: the old counts of the first policies "do not seem to be correct because these claims do not have claim severity counterparts". _clean checks that every count equals the claims table and that no claim names a missing policy. Those first 9,387 policies (IDpol up to 24,951) all had claims before (9,942), 293 have now, and they stay: LightGBM trained on the others expects 292.6 claims there against 307 observed (0.97 on a random fifth of the others), and their next-year rows claim at 0.048 a year against 0.076 for the rest of block 0.
        - Not capped: the 8 policies with 5 to 16 claims (Noll et al.'s code caps at 4, "that might be data error", FreMTPL_1b load data.r line 30; Wüthrich and Merz drop them as "may be data error", p. 554) each have as many claims with a cost. Exposure above one year (1,224 rows, up to 2.01, IDpol blocks 1 and 2 only), capped at 1 by both, stays: the help page says only "mostly on one year", so it is unusual, not shown impossible (CLEAN-11).
        - Counts of 5 to 16 (Lennart, 2026-11-04: kept): seven of the eight policies are one profile (power 4, brand B1, area D, density 824, Languedoc-Roussillon, bonus-malus 50): 72 claims over 3.63 years, every claim with a positive cost, which Wüthrich and Merz suspect to be one driver or a rental fleet. A cap is a modelling choice of the literature, not a shown error, and the 2022 update ties each count to a costed claim; the 19 rows carry 0.0012 of the mean deviance 0.2534.
        - Exposure above one year (Lennart, 2026-11-04: kept): 1,224 rows of 1.01 to 2.01 years (median 1.04) in two policy ranges, IDpol 1,179,653-1,199,005 (961 rows) and the end of block 2 (263), which record a whole contract period rather than cutting at the accounting year and have no links to other years. The literature caps at 1 on the assumption that every policy lies inside one year, which these rows contradict; capping would raise their modelled rate by 11% on average. Exposure is the time at risk.
        - Potential leak, kept on purpose: Exposure, the share of the year insured, is shorter when the policy ended during the year, so it can record a later cancellation. It stays as the exposure the source puts into the expected count, as in bemtpl97. Claims proportional to it score 0.2534 against 0.2595 for the mean count, and LightGBM on all inputs 0.2326 (3 random folds), so it carries about a fifth of the gain. Revisit if policy dates become available.
        - Metric: the mean Poisson deviance of ClaimNb against the expected count, by which Noll, Salzmann and Wüthrich compare models in and out of sample (FreMTPL_1b load data.r line 35, 100 times the mean) and Wüthrich and Merz's out-of-sample loss (Sec. 5.2.4, Eq. 5.28). The shared scorer floors a predicted mean at machine epsilon (Lennart, 2026-11-04, on bemtpl97).
        - Dtypes: Area ordered A (rural) to F (urban centre) as the help page defines it, bands of Density; VehBrand, VehGas and Region (22 regions before 2016) nominal; the rest numbers. IDpol dropped. A car age of 99 or 100 (48 rows) is a default date, as no car is 86 to 98 and 21 of the 23 aged 99 are 100 a year later: missing (CLEAN-10). Anomaly: a driver age of 99 has 70 rows against 5 at 98, kept as possible.
        - Copies kept: every IDpol is distinct; 28,768 rows equal another, neighbouring IDpols often share all rating factors, and about half the rows of blocks 1, 3, 5 and 6 repeat a car of the block before with the driver a year older (decision table), with no key the source states. Grouping rows linked this way (430,298 groups) changes nothing: LightGBM skill over the portfolio frequency 0.0821 random, 0.0819 grouped (3 folds each).
        - Split forced IID from temporal (ForcedIIDFromTemporal, SPLIT-8): an insurer fits on past years and prices the next. The blocks 0-1, 2-3 and 4-6 look like consecutive years of three sub-portfolios; tested on 1, 3 and 6 after training on the rest, skill is 0.0847 against 0.0820 for random rows of that size. Recover the years if a release has them.
        - Year 2014: the tables entered CASdatasets on 14 October 2014 (the package's NEWS); the first release holding them is not pinned. Source: "Unknown private insurer".
    """

    accepted_check_warnings = {
        "dataset_duplicate_rows": (
            "Each copy is a distinct policy (own IDpol): rating cells are coarse, so many policies share every factor, "
            "and the repetition is the portfolio (Lennart, 2026-11-04)."
        ),
        "dataset_conflicting_duplicate_rows": (
            "390 rows share every factor with another policy but differ in claim count: claims are rare, random events "
            "of identical risk profiles, not noise (Lennart, 2026-11-04)."
        ),
        "task_target_value_dominant": "96% of the policies have no claim: real no-claim policies, the nature of claim frequency.",
    }
    target = "ClaimNb"
    problem_type = "regression"
    metric = Metric.source(
        "mean_poisson_deviance",
        original=(
            "Poisson deviance loss of the claim counts against the expected counts, in and out of sample (reported as "
            "100 times the mean)"
        ),
        reference=(
            "https://github.com/JSchelldorfer/ActuarialDataScience/blob/3f761ef830d28c14dda5443d504d192069a64ca3/"
            "1%20-%20French%20Motor%20Third-Party%20Liability%20Claims/Tools/FreMTPL_1b%20load%20data.r#L35"
        ),
        params={"min_prediction": 1e-6},
        definition=(
            "2*mean(y*log(y/mu)-y+mu) over the expected counts mu; 0*log(0/mu)=0; mu below 1e-6 counts as 1e-6 "
            "(two orders below one day of exposure at a low claim frequency); the case study's Poisson.Deviance is "
            "100 times it"
        ),
    )
    splits_comment = """
        Default IID protocol: random 3-fold cross-validation, one repeat for a train side of 451,994 rows, with the
        benchmark split seed 4267 after the base class's content ordering and shuffle with seed 42. Each row is a
        distinct IDpol; the source
        gives no dates and no policy key across rows, so a policy's record of another year, or another record of the
        same year, can fall on the other side. This evaluates comparable policies of the same portfolio and years,
        not a later year.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        import rdata

        for name, expected in RAW_FILES.items():
            if hashlib.sha256((raw_dir / name).read_bytes()).hexdigest() != expected:
                raise ValueError(f"{name} does not match the pinned CASdatasets release")
        freq = rdata.read_rda(raw_dir / "freMTPL2freq.rda")["freMTPL2freq"].rename(columns=str)
        sev = rdata.read_rda(raw_dir / "freMTPL2sev.rda")["freMTPL2sev"].rename(columns=str)
        freq["IDpol"] = _ids(freq["IDpol"])
        sev["IDpol"] = _ids(sev["IDpol"])
        # The source's own link: each claim of freMTPL2sev names its policy by IDpol.
        orphans = ~sev["IDpol"].isin(freq["IDpol"])
        if orphans.any():
            raise ValueError(f"{int(orphans.sum())} claims of freMTPL2sev name no policy of freMTPL2freq")
        claims = sev.groupby("IDpol").size().rename("sev_claims")
        return freq.join(claims, on="IDpol").fillna({"sev_claims": 0})

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        if not raw["IDpol"].is_unique:
            raise ValueError("Expected one row per IDpol")
        if not raw["ClaimNb"].eq(raw["sev_claims"]).all():
            raise ValueError("Expected every claim count to equal the policy's claims in freMTPL2sev")
        if not raw["Exposure"].between(1 / 366, 2.01).all():
            raise ValueError("Expected exposures between one day and 2.01 years")
        # No cap, no row filter: the counts match the claims table, and exposures above a year are kept (notes).
        df = raw.assign(ClaimNb=raw["ClaimNb"].astype("int64"))
        for column in ["VehPower", "VehAge", "DrivAge", "BonusMalus", "Density"]:
            df[column] = df[column].astype("int64")
        # A car age of 99 or 100 years is a default registration date, not an age (notes): missing, the row stays.
        df["VehAge"] = df["VehAge"].astype("float64").mask(df["VehAge"].ge(DEFAULT_VEHICLE_AGE))
        return drop_columns(df, ["IDpol", "sev_claims"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            ordinal={"Area": AREA_LEVELS},  # rural to urban centre, bands of Density
            categorical=["VehBrand", "VehGas", "Region"],
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        block = raw["IDpol"] // BLOCK
        pairs = next_year_rows(raw)
        later = pairs["IDpol_next"] // BLOCK
        same_profile = raw[RATING_FACTORS].astype(str).agg("|".join, axis=1)
        neighbour = same_profile.eq(same_profile.shift()) & block.eq(block.shift())
        per_block = pd.DataFrame(
            {
                "rows": block.value_counts().sort_index(kind="stable"),
                "claims per year": (raw.groupby(block)["ClaimNb"].sum() / raw.groupby(block)["Exposure"].sum()).round(
                    4
                ),
                "rows with an earlier-year row (rule)": later.value_counts().reindex(range(7), fill_value=0),
                "rows equal in all rating factors to the previous IDpol": neighbour.groupby(block).sum(),
            }
        )
        per_block.index = [f"{b}" if b == 0 else f"{b} million" for b in per_block.index]
        per_block.index.name = "IDpol block"
        return [
            Decision(
                "IID split kept, though IDpol links some policies across years",
                "The release has no dates. IDpol runs in seven blocks; in blocks 1, 3, 5 and 6 a share of the rows "
                "repeat a row of the block before with the same car and region, the driver one year older (the rule "
                "in next_year_rows), and within a block neighbouring IDpols often share every rating factor. Neither "
                "is a key the source states, so the split stays IID and the question goes to the curator.",
                per_block,
            )
        ]
