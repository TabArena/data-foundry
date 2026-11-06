"""Curated dataset definition for `fremtpl2` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import hashlib
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
    drop_columns,
)

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
"""VehAge from here on (99 and 100, 48 rows) is a default date: no car is 86 to 98 years old, and the 14 of the 23 cars
of age 99 that next_year_rows pairs with a next-year row are all 100 there."""

BLOCK = 1_000_000
"""IDpol runs in seven blocks of a million (1-179,639 up to 6,000,016-6,114,330)."""

LAST_LATE_BONUS_MALUS_BLOCK = 4
"""BonusMalus looks recorded after the row's own claims in IDpol blocks 0-4 (597,998 rows) and like a value taken at the
start of the year in blocks 5-6: blanked in blocks 0-4 (notes)."""

DEFAULT_DRIVER_AGE = 99
"""DrivAge 99 in block 0 (66 rows) is a default code: 1 row at 96 and none at 97-98 there, block 1 has no driver older
than 97, and none of the 66 has a next-year row (62.7% of block 0 has one)."""


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
        question="How many claims per year insured will a French motor-insurance policy make?",
        use_case=(
            "For example, a pricing actuary sets the yearly premium of motor third-party liability policies at the "
            "quote, estimating each policy's expected claims per year insured from its rating factors."
        ),
        row=(
            "One of 677,991 policy records of an unnamed French insurer's motor portfolio, each observed mostly "
            "within one accounting year, about 2011 to 2013."
        ),
        predicted=(
            "Claims per year insured: the claims with a recorded cost in the record's period divided by the time it "
            "was insured (96.3% have none). Each record counts in proportion to that time, in training and scoring."
        ),
        known=(
            "The car's power, age, brand and fuel, the driver's age, the bonus-malus level (in 12% of the records), "
            "and the density, area and region of residence. The time insured is no input: a claim can cut it short, "
            "so it is the rate's denominator and each record's weight."
        ),
        split=(
            "Random policy records are held out, standing for comparable policies of the same portfolio and years; the "
            "release has no dates, and a policy's record of another year can be on the training side."
        ),
        changes=(
            "We divide the claim count by the time insured and weight each record by that time, as the source's "
            "models do with an offset. We blank the bonus-malus level in the first five policy-number ranges (88% of "
            "the records), where it looks recorded after the year's own claims, and set default codes of car age "
            "(99, 100) and driver age (99, in the first range) to missing."
        ),
        fit="approximate",
        fit_reason=(
            "The rating factors and the claim frequency mirror pricing a policy, but the release has no calendar "
            "dates, so a later year cannot be held out as an insurer would (forced from temporal). The insurer is "
            "unknown. The bonus-malus level is blank in 88% of records. A model reading other rows can find a "
            "next-year record (kept)."
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
        - Target: claim_frequency = ClaimNb / Exposure, the claims per year insured (MET-14), with Exposure as the row weight of the metric and the training weight (`sample_weight`, MET-15) and never a feature (LEAK-41). ClaimNb leaves the frame as a part of the target, and _clean checks that claim_frequency x Exposure gives it back. The counts are as released (0 to 16). CASdatasets' update of 23 June 2022 set each count to the policy's claims in freMTPL2sev, as Wüthrich and Merz (2023, Appendix B, Sec. 13.1) do by hand: the old counts of the first policies "do not seem to be correct because these claims do not have claim severity counterparts". _clean checks that every count equals the claims table and that no claim names a missing policy. Those first 9,387 policies (IDpol up to 24,951) all had claims before (9,942), 293 have now, and they stay: their next-year rows claim at 0.048 a year against 0.076 for the rest of block 0.
        - Not capped: the 8 policies with 5 to 16 claims (Noll et al.'s code caps at 4, "that might be data error", FreMTPL_1b load data.r line 30; Wüthrich and Merz drop them as "may be data error", Sec. 13.1) each have as many claims with a cost. Exposure above one year (1,224 rows, up to 2.01, IDpol blocks 1 and 2 only), capped at 1 by both, stays: the help page says only "mostly on one year", so it is unusual, not shown impossible (CLEAN-11).
        - Counts of 5 to 16 (Lennart, 2026-11-04: kept): seven of the eight policies are one profile (power 4, brand B1, area D, density 824, Languedoc-Roussillon, bonus-malus 50): 72 claims over 3.63 years, every claim with a positive cost, which Wüthrich and Merz suspect to be one driver or a rental fleet. A cap is a modelling choice of the literature, not a shown error, and the 2022 update ties each count to a costed claim; the 19 rows carry 0.0012 of the mean deviance 0.2534.
        - Exposure above one year (Lennart, 2026-11-04: kept): 1,224 rows of 1.01 to 2.01 years (median 1.04) in two policy ranges, IDpol 1,179,653-1,199,005 (961 rows) and the end of block 2 (263), which record a whole contract period rather than cutting at the accounting year and have no links to other years. The literature caps at 1 on the assumption that every policy lies inside one year, which these rows contradict; capping would raise their modelled rate by 11% on average. Exposure is the time at risk; these rows keep weights of up to 2.01.
        - Exposure (LEAK-41, MET-15; issue 6, resolved 2026-11-06): the share of the year insured is shorter when the policy ended during the year, often after a claim, so as a free feature it recorded the outcome. Beyond a log(Exposure) offset it was worth another 0.0039 to 0.0045 of mean deviance (0.0033 to 0.0047 and 21-30% of LightGBM's gain after the BonusMalus blanking, 3 folds), a Poisson GLM gave log(Exposure) a coefficient of 0.641 where an offset is 1, and at the quote (every policy priced for a full year) the free model was never better than the offset model while actual claims came in 1.29 times its price. Exposure now ships as the rate's denominator and each row's weight, the source's offset model: with the weight, dividing does not inflate short records. Part of the short records are renewals during the year recorded as two records (Wüthrich and Merz, Sec. 13.1).
        - Metric: the mean Poisson deviance of the claim frequency weighted by Exposure, sum(w*d)/sum(w). It equals the mean Poisson deviance of ClaimNb against the expected count Exposure x rate, by which Noll, Salzmann and Wüthrich compare models in and out of sample (FreMTPL_1b load data.r line 35, 100 times the mean) and Wüthrich and Merz's out-of-sample loss (Sec. 5.2.4), times n/sum(Exposure) of the scored rows (1.886 to 1.896 on the shipped folds, 1.891 overall): the source's metric on its offset model, so models rank as by the source's metric on every fold (MET-11, origin source). Floor 1e-4 claims per year on the predicted rate, two orders below the smallest plausible rate (MET-13, Lennart's rule of 2026-11-04 on the scale the metric scores).
        - Dtypes: Area ordered A (rural) to F (urban centre) as the help page defines it, bands of Density; VehBrand, VehGas and Region (22 regions before 2016) nominal; the rest numbers. IDpol dropped. A car age of 99 or 100 (48 rows) is a default date, as no car is 86 to 98 and the 14 of the 23 aged 99 that next_year_rows pairs are all 100 a year later: missing (CLEAN-10). Anomaly: a driver age of 99 has 70 rows against 5 at 98, kept as possible (superseded 2026-11-05: the 66 in block 0 are missing, CC below); 66 of them are in block 0, after 1 row at 96 and none at 97-98, and none of the 66 has a next-year row (62.7% of block 0 has one).
        - Copies kept: every IDpol is distinct; 28,768 rows copy an earlier row (40,903 rows sit in groups of equal rows; 30,987 and 43,947 after the BonusMalus blanking), neighbouring IDpols often share all rating factors, and at least half the rows of blocks 1, 3, 5 and 6 (48.7%, 48.3%, 49.2%, 60.3%) repeat a car of the block before with the driver a year older (decision table: 161,883 pairs, against 16 to 75 under shuffled or shifted controls), with no key the source states. These shares are lower bounds: a wider IDpol offset finds up to 75.3% in block 6. Chaining these pairs with neighbouring IDpols that share every rating factor gives 430,298 groups. For a model that scores one row at a time, grouping on them moves LightGBM skill over the portfolio frequency from 0.0821 to 0.0819 (3 folds each). A model that reads other rows can do more: for 16% of test rows the policy's next-year row is on the training side, the shipped columns single it out for 55% of linked rows, and its claim count and exposure are worth 0.0021 of mean deviance (0.0002 without BonusMalus) (corrected 2026-11-05: 0.0021 is the oracle that also reads the next-year row's bonus-malus ratio, 0.0020 re-measured; claim count and exposure alone are worth 0.0003; after the blanking the full oracle is worth 0.0008, 3 folds).
        - Split forced IID from temporal (ForcedIIDFromTemporal, SPLIT-8): an insurer fits on past years and prices the next. The blocks 0-1, 2-3 and 4-6 are read as consecutive periods of three sub-portfolios, with two caveats: from block 0 to 1 and 2 to 3 the bonus-malus barely moves (94.5% unchanged from 0 to 1, where the French system lowers it after every claim-free year), and in blocks 4-6 0.2% of linked rows cover a full year and 63-66% of linked pairs have exposures summing to at most 1.01, so they look like one contract year split across accounting years. Tested on blocks 1, 3 and 6 after training on blocks 0, 2, 4 and 5, LightGBM's mean deviance on those rows (BonusMalus in all rows) is 0.23316 against 0.23267 for the same rows under the shipped folds (+0.00049, SE 0.00016): the IID split is slightly optimistic, and the ranking against a Poisson GLM is unchanged. Recover the years if a release has them.
        - Year 2014: the tables entered CASdatasets on 14 October 2014 (`pkg/inst/NEWS` at CASdatasets commit 324c15c999; the NEWS.md of the pinned commit does not list them); the first release holding them is not pinned. Source: "Unknown private insurer".
        - CC (2026-11-05, Lennart): BonusMalus blanked in IDpol blocks 0-4 (597,998 rows, 88.2%), where it looks recorded after the row's own claims (issue 5, B; LEAK-10, LEAK-7). There it is frozen from block 0 to 1 and 2 to 3 and claimants pile on the first malus step 62-63; in blocks 5-6 it follows the previous year's claims, as a start-of-year value does, and stays, as in zillow_prize, melbourne_housing_market and online_shoppers. bemtpl97 keeps its bm: its source says "The risk factors are registered at the start of the policy period" (binning manuscript, Sec. 2), the freMTPL2 help page says nothing of the kind, and the 2026-11-04 call that the two are treated alike covered the split and the fit. LightGBM Poisson, Exposure a free feature, shipped folds (3): mean deviance 0.2327 before, 0.2435 after (+0.0127 in blocks 0-3, -0.0013 in blocks 5-6); dropping the column too costs 0.0009 more in blocks 5-6.
        - CC (2026-11-05, Lennart): DrivAge 99 set to missing in block 0 (66 rows), a default code like VehAge 99 (issue 9, B; CLEAN-10). None of the 66 has a next-year row, so the missing value marks the same rows the 99 did. The 4 rows at 99 outside block 0 stay at 99: next_year_rows pairs the one in block 3 with a block-2 row at 98, and two of the three in block 4 with block-5 rows at 100.
        - CC (2026-11-05, Lennart): the split stays IID (`ForcedIIDFromTemporal`) for now (issue 7, B): prior work on freMTPL2 uses a random hold-out or a split grouped on identical rating factors, and none links records across years; revisit if the inferred policy chains become a recorded key.
        - CC (2026-11-05, Lennart): the label-free renewal signal stays (issue 8, as implemented, answered (a)): it is an evaluation leak, read from other rows, handled by LEAK-9 as amended on 2026-11-05 (a protocol line the benchmark checks; a method that learns from the test block is called out and not benchmarked), as medical_facility_operational_data. After issue 5 a model that reads the next-year record gains 0.0008 mean deviance (0.0009-0.0010 without `BonusMalus`).
        - CC (2026-11-06, Lennart): issue 6 resolved by option A of https://github.com/TabArena/data-foundry/issues/51: the target is the claims per year insured, Exposure the weight of the metric and of training and never a feature (LEAK-41, MET-14, MET-15), the floor 1e-4 a year (MET-13). Supersedes the call of 2026-10-20 (Andrej: Exposure "a feature, not a divisor", capped at 1) and the parking of 2026-11-05: the conditional measurement came later (+0.0040; never better at quotation), and with the weight, dividing does not inflate short records.
        - CC (2026-11-06, Lennart): the claim amounts (the proposal of PR #46, D12) stay out for now; a task on amounts per year insured or on the claim size is a separate decision, made on leak-free numbers.
    """

    accepted_check_warnings = {
        "dataset_duplicate_rows": (
            "Each copy is a distinct policy (own IDpol): rating cells are coarse, so many policies share every factor, "
            "and the repetition is the portfolio (Lennart, 2026-11-04)."
        ),
        "dataset_conflicting_duplicate_rows": (
            "520 rows (390 before BonusMalus was blanked in blocks 0-4) share every factor with another policy but "
            "differ in claim count: claims are rare, random events of identical risk profiles, not noise (Lennart, "
            "2026-11-04)."
        ),
        "task_target_value_dominant": "96% of the policies have no claim: real no-claim policies, the nature of claim frequency.",
    }
    target = "claim_frequency"
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
        params={"min_prediction": 1e-4},
        inputs={"weight": "Exposure"},
        definition=(
            "2*sum(w*(y*log(y/mu)-y+mu))/sum(w) over the claims per year y and the predicted rates mu, w = Exposure "
            "(years insured); 0*log(0/mu)=0; mu below 1e-4 claims per year counts as 1e-4. Equals the source's mean "
            "count deviance of the expected counts Exposure*mu times n/sum(Exposure) of the scored rows (1.886 to "
            "1.896 on the shipped folds); the case study's Poisson.Deviance is 100 times the count deviance"
        ),
    )
    scoring_columns = (
        ScoringColumn(
            column="Exposure",
            role="weight",
            used_by="mean_poisson_deviance",
            description=(
                "years insured in the record's period (1/366 to 2.01), realized: shorter when the policy ended early, "
                "often after a claim. The claim frequency's denominator; each row's weight in the metric and in "
                "training; never a feature"
            ),
        ),
    )
    sample_weight = "Exposure"
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
        # Claims per year insured, weighted by the years insured (MET-14, MET-15): the count leaves the frame as a part
        # of the target, and Exposure stays only as the weight scoring column, never a feature (LEAK-41).
        df["claim_frequency"] = df["ClaimNb"] / df["Exposure"]
        if not np.allclose(df["claim_frequency"] * df["Exposure"], df["ClaimNb"], rtol=0, atol=1e-9):
            raise ValueError("Expected claim_frequency x Exposure to give back ClaimNb")
        for column in ["VehPower", "VehAge", "DrivAge", "BonusMalus", "Density"]:
            df[column] = df[column].astype("int64")
        # A car age of 99 or 100 years is a default registration date, not an age (notes): missing, the row stays.
        df["VehAge"] = df["VehAge"].astype("float64").mask(df["VehAge"].ge(DEFAULT_VEHICLE_AGE))
        # Both masks read the IDpol block, so they run before IDpol is dropped.
        block = df["IDpol"] // BLOCK
        # BonusMalus in blocks 0-4 looks recorded after the row's own claims (notes, LEAK-10): blanked there.
        df["BonusMalus"] = df["BonusMalus"].astype("float64").mask(block.le(LAST_LATE_BONUS_MALUS_BLOCK))
        # A driver age of 99 in block 0 is a default code, as VehAge 99 is (notes); the 4 rows at 99 elsewhere stay.
        df["DrivAge"] = df["DrivAge"].astype("float64").mask(block.eq(0) & df["DrivAge"].eq(DEFAULT_DRIVER_AGE))
        return drop_columns(df, ["IDpol", "sev_claims", "ClaimNb"])

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
