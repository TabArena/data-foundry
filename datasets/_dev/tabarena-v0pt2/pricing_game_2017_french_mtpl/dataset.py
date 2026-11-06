"""Curated dataset definition for `pricing_game_2017_french_mtpl` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, Grouping, Metric, TaskSummary, drop_columns

# The rules' three keys of a claim and of a policy-year ("When merging claims with contracts, don't forget to use the
# three IDs as keys", 3rdPricingGame.pdf, Sec. 4.4).
KEYS = ["id_client", "id_vehicle", "id_year"]
TARGET = "claim_amount"
CATEGORICAL = [
    "pol_coverage",
    "pol_pay_freq",
    "pol_payd",
    "pol_usage",
    "pol_department",
    "drv_drv2",
    "drv_sex1",
    "drv_sex2",
    "vh_fuel",
    "vh_make",
    "vh_model",
    "vh_type",
    "id_client",  # the group column, never a feature
]
# 17,794 communes, median 2 policies each: high-cardinality text (CLEAN-14); the department is the category.
STRING = ["pol_insee_code"]
# The youngest age at which a licence can have been taken: 16 or 17 is possible abroad (US 16, UK 17).
MIN_LICENCE_AGE = 16
# Above the heaviest vehicles of the table (vans of 3,500 kg); only one Peugeot 205 of 7,901 kg passes it.
MAX_WEIGHT = 5000


class PricingGame2017FrenchMtpl(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "What will a French car insurance policy cost in claims over the year, from the policy, driver and "
            "vehicle factors known when its premium is set?"
        ),
        use_case=(
            "A motor insurer pricing its policies for the year: when the premium is set, it estimates each policy's "
            "claim cost to rank the risks and set the price. The 2017 actuarial pricing game posed this task: players "
            "priced 100,000 policies and competed for the clients in simulated markets."
        ),
        row=(
            "One car policy of an unnamed French insurer in Year 0 of the 2017 pricing game: one vehicle of a client, "
            "covered for the year (100,000 policies of 91,488 clients; the calendar year is not given, about 2010-11 "
            "by the vehicles on sale, an estimate)."
        ),
        predicted=(
            "The total of the policy's claims in the year, in euros, over every guarantee of its cover (liability "
            "only for the Mini cover): 0 for 88.9% of the policies, those without a claim or whose claims net to 0 "
            "or less after legal recourse."
        ),
        known=(
            "The bonus-malus, cover level, policy age and time since its last change, payment frequency, "
            "pay-as-you-drive and use, the commune and its department, both drivers' age, sex and years of licence, "
            "the vehicle's age, engine, power, fuel, make, model, years on sale, top speed, type, value and weight, "
            "and how many vehicles the client insures."
        ),
        split=(
            "All policies of a client stay on one side, so the test data stands for clients whose claims of the year "
            "are not known; pricing the next year from this one, as the game did, needs a second claim year."
        ),
        changes=(
            "We summed each policy's claims, set the 1,116 negative totals (legal recourse) to 0, made placeholder "
            "and impossible values missing (a licence of 111 years or taken before 16, a weight of 0 or 7,901 kg, "
            "the zeros of an absent second driver), joined make and model, added the client's vehicle count and the "
            "commune's department, kept the commune as text, and dropped the identifiers."
        ),
        fit="approximate",
        fit_reason=(
            "The features are the rating factors known when a premium is set, and the target is the policy's own "
            "claims. But the game priced the next year knowing each policy's claims of this one, and only one claim "
            "year is published, so held-out clients of the same year stand in; the insurer and how the policies were "
            "chosen are not stated."
        ),
    )

    # Dataset
    unique_name = "pricing_game_2017_french_mtpl"
    year = "2017"
    domain = "insurance"
    source = "Other"  # the 2017 actuarial pricing game's toolbox (Charpentier); no closer schema value
    source_url = "https://actinfo.hypotheses.org/86"
    license = "GPL (>= 2)"  # CASdatasets DESCRIPTION; the game's pages state no terms
    data_tags = ("ForcedGroupedFromTemporal", "Spatial")
    download_description = """
        The third actuarial pricing game (Arthur Charpentier with the ACTINFO chair and the Institut des Actuaires,
        announced on https://actinfo.hypotheses.org/86 on 10 January 2017) gave its players the Year-0 underwriting
        file PG_2017_YEAR0.csv and claims file PG_2017_CLAIMS_YEAR0.csv in http://freakonometrics.free.fr/PG3/toolbox.zip,
        which is gone (404 on 2026-11-01, not in the Wayback Machine). The rules are archived:
        http://web.archive.org/web/20190919092227/http://freakonometrics.free.fr/PG3/3rdPricingGame.pdf.
        The R package CASdatasets (Dutang and Charpentier; DOI 10.57745/P0KHAG) holds the two files as pg17trainpol
        and pg17trainclaim (man/pricingame.Rd). We take them from the package's GitHub repository at the commit of
        2026-06-10 (227fb56, master on 2026-11-01; the files date from 2024-05-27) and export them to CSV with
        pyreadr; in R, write.csv(pg17trainpol, "pg17trainpol.csv", row.names = FALSE) gives the same values.

        mkdir -p local-data-warehouse/pricing_game_2017_french_mtpl/rda && cd local-data-warehouse/pricing_game_2017_french_mtpl
        for f in pg17trainpol pg17trainclaim; do wget -P rda https://raw.githubusercontent.com/dutangc/CASdatasets/227fb56b8734bdb7c0327a41180e01d2ddaeaf26/data/$f.rda; done
        sha256sum rda/pg17train*.rda
        # 2eba91dc2243339e5e8fe1c20e36c76d0c8a9c169bb49ce8e4e7ef77c48e492a  rda/pg17trainclaim.rda
        # 7b0010b021215cf48cdeeccf1f10d44d2d9f9e4f5b60b28d3704cbf1af373a7b  rda/pg17trainpol.rda
        uvx --from pyreadr==0.5.7 --with pandas==3.0.6 python -c "import pyreadr; [pyreadr.read_r(f'rda/{n}.rda')[n].to_csv(f'{n}.csv', index=False) for n in ('pg17trainpol', 'pg17trainclaim')]"
        sha256sum pg17train*.csv
        # 7597871a99636332cd02bd7d1d4104ce89b9f9dff07cc32fafe2358dd3bf6c8b  pg17trainclaim.csv
        # 6029c702700f45e803e5c9a3cdd299e59084868e45f329268d3793a295427de5  pg17trainpol.csv
    """
    bibtex = r"""
        @misc{Charpentier2017PricingGame,
          author = {Charpentier, Arthur},
          title = {Third Actuarial Pricing Game},
          year = {2017},
          howpublished = {\url{https://actinfo.hypotheses.org/86}},
          note = {With the ACTINFO chair of the Institut Louis Bachelier and the Institut des Actuaires; data released
            to the players on 10 January 2017; distributed as pg17trainpol and pg17trainclaim in the R package
            CASdatasets (Dutang and Charpentier), DOI 10.57745/P0KHAG}
        }
    """
    curation_comments = """
        We start with pg17trainpol and pg17trainclaim of CASdatasets, the Year-0 underwriting and claims files of the third actuarial pricing game (2017).

        - Prediction point: when a policy's premium for the year is set. The players priced each policy's annual premium before the year's claims were known (rules, p. 1), and every age and duration is counted "from the beginning of the current year" (rules, Sec. 4.7, 4.14).
        - Year and source: the files went to the players on 10 January 2017 (rules, p. 1); the portfolio itself dates from about 2010-11, since no model launched in 2011 or later is in it while 2010 launches are, at a vehicle age of 1 (an estimate). The game's toolbox is gone; CASdatasets, co-authored by the game's organiser, matches what the rules state: 100,000 policies, the last client A00091488 (91,488 clients), at most 6 claims per vehicle in Year 0 (Sec. 4.31), all of Year 0; it holds 14,243 claims. pg17testyear1 to pg17testyear4 hold the same policies in Years 1 to 4 without claims, so only Year 0 has a target. The AIcrowd Insurance Pricing Game (2020-21) adds three claim years on noised features behind an account (the curation record); not used.
        - Target `claim_amount`: the claims joined on id_client, id_vehicle and id_year (rules, Sec. 4.4) and summed per policy; 12,654 policies have a claim (at most 6). 1,263 claims are negative, "claims where our driver's liability is not engaged, so there's a legal recourse" (Sec. 4.33), and 589 are 0.
        - What the total covers: every guarantee of the policy's cover, so liability alone only for Mini (8.6% of the policies, 2.0% of the claim cost); Maxi (64.5% of the policies, 83.4% of the cost) adds damage, theft and glass. 843 claims are exactly 1,236.00 EUR and 75 exactly 618.00 EUR, the flat amount of the French inter-insurer IRSA convention for material damage and its half; the negative claims are the other side of the convention, a recovery when the client was not liable (median -516, 99.7% above -1,236). Whether the amounts are paid or incurred, and at what evaluation date, is not stated.
        - Amount, not a claim indicator, unlike pricing_game_2016_french_fleet: these are euros with a full tail (largest total 141,828), the pure premium the game priced, where pg16's charges are scaled by one constant and stop at 8,565.
        - 1,116 negative policy totals (-1,864 to -0.02) set to 0, as the AI suggested (record, 2026-10-30) and as frempl_french_motor_personal_line does; AIcrowd set the same totals to 0 on this portfolio. The reason: Tweedie and Poisson losses, the usual ones for a pure premium, need a non-negative target. The clip raises the total claim cost by 4.8% (Mini 12.5%, Maxi 4.3%). The total is clipped, not each claim: 213 policies mix positive and negative claims (80 net below 0). 88.9% of the targets are then 0.
        - Raw amount, not log1p: the Tweedie deviance scores the expected claim cost in euros, its level included, and a log1p fit transformed back prices policies at about 1% of their cost (deviance skill -5.1, below a constant prediction). Under the normalized Gini the scale made no clear difference (untuned, 9 shipped splits: random forest 0.298 on the amount, 0.297 on log1p; LightGBM 0.248 and 0.251). frempl_french_motor_personal_line ships log1p with a Gini. **Exception to CLEAN-16 (2026-11-03, Andrej):** a metric that scores the level in euros, which a log1p fit loses.
        - Only the claim part carries signal (repeat 0): untuned LightGBM ranks claims at AUC 0.611, a severity model scores R^2 -0.036 on the claimants (-0.018 on log amounts), and the true claim indicator times the claimants' mean reaches R^2 0.158. The largest total, 141,828, is 1.2% of all claim cost; kept.
        - `pol_bonus` is the bonus-malus at the start of the year: to Year 1 it rises by 24-25% for 1,230 policies with a Year-0 claim and 373 without (pg17testyear1), the French rule after a claim (Sec. 4.5); alone it ranks Year-0 claims at AUC 0.518.
        - Made missing, rows kept: `drv_age2` and `drv_age_lic2`, 0 exactly for the 66,814 policies without a second driver ("When not, this age is 0", Sec. 4.15); a licence held longer than the driver has lived (111 years for 24 first and 768 second drivers, 2 other first drivers; the rules warn of "some outliers", Sec. 4.19); a licence that, by the driver's age, was taken before 16 (8 first drivers, at 5 to 15, and 2 second drivers, at 8 and 10; CLEAN-11, as caracas_cervical_cancer); `vh_weight` of 0 (3,744) and the 7,901 kg of one Peugeot 205 (the other 1,384 weigh 740 to 1,300 kg), and `vh_value` of 0 (2). `vh_cyl` of 0 stays: the 5 vehicles are electric (`vh_fuel` "Hybrid"). `vh_age` is missing for one policy, as published.
        - Kept: 47 first and 6 second drivers licensed at 16 or 17 by their ages, which licences from abroad allow (UK 17, US 16); the ages are whole years and the dates behind them are not documented.
        - `vh_model` is make plus model ("consider concatenating vh_make and vh_model", Sec. 4.25): 45 model names occur under more than one make (`308` is a Peugeot and a Mercedes), so 1,076 levels instead of 1,023 (CLEAN-12).
        - `client_n_vehicles` added: the client's number of policies (1 for 91.4% of the clients, at most 9), the highest number of its `id_vehicle` (CLEAN-3, CLEAN-19). The insurer knows it when quoting, and the game matched clients by the sum of their policies' premiums (Rule 2). Untuned LightGBM on the log1p target, 3 folds by client: normalized Gini 0.263 with it, 0.256 without.
        - `pol_department` added: the first two characters of `pol_insee_code`, which the rules name as the department (Sec. 4.12; 96 values, Corsica 2A and 2B; CLEAN-12). In the same untuned log1p probe, run while the commune was still a category, it lowered the Gini (0.256 to 0.243), as a 96-level category can in an untuned model; kept as the coarse geography an insurer zones by. `pol_insee_code` is text (CLEAN-14): 17,794 communes, median 2 policies, 6,775 with one.
        - Dropped: `id_policy` (id_client and id_vehicle joined), `id_vehicle` ("their rank should not represent anything valuable", Sec. 4.2) and `id_year` (one value). `id_client` is the group column.
        - Dtypes: the policy, driver and vehicle labels and the department categorical (`pol_coverage` ordered Mini to Maxi in the rules, kept as a category), the commune a string; bonus-malus, ages, durations and the vehicle's measures numeric. One pair of policies, one client's two vehicles without a claim, is identical in every feature: kept.
        - Exposure: no exposure column, and none is needed. The 100,000 policies are each present once in every year's file, with annual premiums (rules, Sec. 4), so a row is a whole policy-year; the release does not say so. The shortest `pol_duration` is 1, so no policy was written during Year 0, and the newest policies claim more often, not less (a claim in 13.7% of the policies at duration 1 against 12.3% from 6 on), where part years would claim less: nothing points to a year cut short. The target is the policy's claims of the year, scored unweighted, as the game priced each policy for the year (MET-14, MET-15). For the 4,152 pay-as-you-drive policies (`pol_payd`) the real exposure, the distance driven, is not released.
        - Note: `drv_sex1` and `drv_sex2` kept, as the rules offer them ("can be used as discriminatory variable in this pricing game", Sec. 4.16). EU law has barred sex from insurance prices since 21 December 2012; in the data's year, about 2010-11, it was still a legal rating factor, so the insurer could use it.
    """

    # Task
    target = TARGET
    problem_type = "regression"
    metric = Metric.stand_in(
        "mean_tweedie_deviance",
        original=(
            "each player's profit over Years 1 to 4 in simulated markets of 10 players: the premiums minus the losses "
            "of the clients it won, each client choosing among the three cheapest offers, a player whose losses pass "
            "170% of its premiums going bankrupt (rules, objective (2))"
        ),
        reason=(
            "The market needs the other players' premiums and the claims of Years 1 to 4, which the release does not "
            "hold, so the profit cannot be computed. A player wins the clients it prices lowest and goes bankrupt when "
            "its losses pass 170% of its premiums, so its profit rests on both the order and the level of its "
            "premiums. The mean Tweedie deviance at power 1.5 (a compound Poisson-gamma cost, the actuarial loss for a "
            "pure premium with many zero claims) scores both; a prediction below 1 EUR counts as 1 EUR. Closeness "
            "measured in simulated Year-1 markets under the game's Rule 2 on the shipped splits, models as players: "
            "across a mixed field of models a Poisson or Tweedie deviance follows the profit order at a Kendall tau of "
            "0.58 to 0.79, the normalized Gini at 0.12 to 0.59 (means per market variant), as the Gini is blind to any "
            "monotone transform of the predictions: a steeper copy of the best model ties the top Gini (0.317) and "
            "earns less than a flat premium. Among six strong, comparable learners the Gini leads (0.91 against "
            "0.69). Chosen over the Gini by the curator (Andrej, 2026-11-03)."
        ),
        params={"power": 1.5, "min_prediction": 1.0},
        reference="http://web.archive.org/web/20190919092227/http://freakonometrics.free.fr/PG3/3rdPricingGame.pdf",
    )
    grouping = Grouping(
        on="id_client",
        labels="per_sample",
        prediction_unit="row",
        context="all_rows",
        definition="""
            One group is a client (id_client); its rows are its insured vehicles, one policy each (91,488 clients, 91.4% with one vehicle, at most 9). The game priced each policy but matched clients: "We match clients (and not policies) and insurance companies (players). Consider a client with policies I = {i1, i2, ..., ik}, then this client computes" the sum of its policies' premiums (3rdPricingGame.pdf, Rule 2). When a year's premiums are set, the claims of the client's other vehicles in that year are not known, so all of a client's policies stay on one side. Each policy is one prediction; the features of all the client's vehicles are known (context all_rows), and their count is the feature `client_n_vehicles`.
        """,
    )
    splits_comment = """
        Default splits, grouped by client (id_client): all policies of a client stay on one side, since a client's other
        vehicles' claims of the same year are not known when its premiums are set. Grouped and random folds score alike
        for untuned LightGBM with a Tweedie loss (Gini 0.258 against 0.262, 9 splits each). An untuned random forest
        (100 trees, leaves of at least 50 rows, a third of the features per split) scores 0.276 on grouped and 0.324 on
        random folds (3 splits each, unpaired), but on the same random folds, removing the test clients' other vehicles
        from its training rows, against removing as many other multi-vehicle rows, changes its Gini by -0.002 +- 0.003
        (6 splits), so the gap is not shown to come from a client's other vehicles. The task is temporal by its use
        case, since the game's players fit a tariff on Year 0 and priced Year 1 knowing each policy's Year-0 claims, but
        CASdatasets holds the claims of Year 0 only, so held-out clients of the same year stand in for next year's
        policies (ForcedGroupedFromTemporal, SPLIT-8). Its cost, measured on the AIcrowd copy of the portfolio (Gini,
        LightGBM Tweedie): 0.268 for this design, 0.277 for next year's held-out policies and 0.305 for next year with
        the policy's own past claims; the stand-in underrates the real task, it does not flatter it. A later claim year
        adds the claim history and should be recovered; AIcrowd's later claim years, on noised features behind an
        account, give two windows only. Shipped forced on the curator's call (Andrej, 2026-11-02: "Forced group splits
        should be fine"). The leak test across the split finds none (untuned LightGBM, 9 splits, Gini 0.223): no
        exact or near copies; the training side's mean target of a test row's household or vehicle proxy, department
        or commune of the same year changes the Gini by -0.005 to +0.003 (sd 0.004 to 0.010), and removing the
        training rows of the test rows' communes, against as many random rows, by +0.008 +- 0.029.
    """
    accepted_check_warnings = {
        "task_target_value_dominant": (
            "Zero-inflated by nature: the claim total is 0 for 88.9% of the policies, those with no claim in the year "
            "(87.3%) or whose claims net to 0 or less after legal recourse (1.6%, negative totals set to 0); not a cap "
            "or a placeholder."
        ),
    }

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        pol = pd.read_csv(raw_dir / "pg17trainpol.csv", dtype={"pol_insee_code": str})
        claims = pd.read_csv(raw_dir / "pg17trainclaim.csv")
        assert pol["id_policy"].is_unique
        assert not claims.duplicated([*KEYS, "id_claim"]).any()
        # The claims of each policy-year, joined on the rules' three keys.
        per_policy = claims.groupby(KEYS, sort=True).agg(
            claim_total=("claim_amount", "sum"),
            claim_count=("claim_amount", "size"),
            claim_negative=("claim_amount", lambda s: int((s < 0).sum())),
        )
        raw = pol.merge(per_policy.reset_index(), on=KEYS, how="left", validate="one_to_one")
        assert raw["claim_count"].sum() == len(claims)
        return raw.fillna({"claim_total": 0.0, "claim_count": 0, "claim_negative": 0})

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.copy()
        # 1. The target: the policy's claim total, a negative total (net legal recourse) set to 0.
        df[TARGET] = df["claim_total"].clip(lower=0)
        # 2. The client's number of policies, the highest number of its id_vehicle (V01, V02, ...).
        df["client_n_vehicles"] = df.groupby("id_client")["id_policy"].transform("size")
        assert (
            df["id_vehicle"].str[1:].astype(int).groupby(df["id_client"]).transform("max") == df["client_n_vehicles"]
        ).all()
        # 3. The department: the first two characters of the INSEE commune code (2A and 2B for Corsica).
        assert df["pol_insee_code"].str.len().eq(5).all()
        df["pol_department"] = df["pol_insee_code"].str[:2]
        # 4. An absent second driver has age 0 and licence age 0: missing (its sex is missing already).
        absent = df["drv_drv2"].eq("No")
        assert (df.loc[absent, ["drv_age2", "drv_age_lic2"]] == 0).all().all()
        assert df.loc[absent, "drv_sex2"].isna().all()
        for col in ("drv_age2", "drv_age_lic2"):
            df[col] = df[col].mask(absent)
        # 5. A licence held longer than the driver has lived (111 years for 792 drivers, 2 others), or taken before
        #    16 by the driver's age (8 first and 2 second drivers, at 5 to 15): missing (CLEAN-11).
        for lic, age in (("drv_age_lic1", "drv_age1"), ("drv_age_lic2", "drv_age2")):
            df[lic] = df[lic].mask((df[lic] > df[age]) | (df[age] - df[lic] < MIN_LICENCE_AGE))
        # 6. A vehicle weight or value of 0, and the 7,901 kg of one Peugeot 205 (the others weigh 740 to 1,300 kg):
        #    missing. A cylinder capacity of 0 stays (electric vehicles).
        for col in ("vh_weight", "vh_value"):
            df[col] = df[col].mask(df[col].eq(0))
        heavy = df["vh_weight"].gt(MAX_WEIGHT)
        assert heavy.sum() == 1
        df["vh_weight"] = df["vh_weight"].mask(heavy)
        # 7. The model name joined to its make, as the rules advise (Sec. 4.25): 45 names occur under several makes.
        df["vh_model"] = df["vh_make"] + " " + df["vh_model"]
        # 8. Identifiers: id_policy joins id_client and id_vehicle, the vehicle rank means nothing, id_year is
        #    constant; id_client stays as the group column. The claim aggregates are the target.
        assert df["id_policy"].eq(df["id_client"] + "-" + df["id_vehicle"]).all()
        assert df["id_year"].nunique() == 1
        return drop_columns(df, ["id_policy", "id_vehicle", "id_year", "claim_total", "claim_count", "claim_negative"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=CATEGORICAL, string=STRING)

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        claimed = raw[raw["claim_count"] > 0]
        sign = np.sign(claimed["claim_total"]).map({-1.0: "negative", 0.0: "zero", 1.0: "positive"})
        mix = np.where(claimed["claim_negative"] == 0, "no negative claim", "some negative claim")
        totals = pd.crosstab(sign, mix, margins=True).rename_axis(index="policy total", columns="claims")
        second = raw["drv_drv2"].eq("Yes")
        young1 = raw["drv_age_lic1"].le(raw["drv_age1"]) & (raw["drv_age1"] - raw["drv_age_lic1"] < MIN_LICENCE_AGE)
        young2 = (
            second & raw["drv_age_lic2"].le(raw["drv_age2"]) & (raw["drv_age2"] - raw["drv_age_lic2"] < MIN_LICENCE_AGE)
        )
        placeholders = pd.DataFrame(
            {
                "rows": [
                    int((~second).sum()),
                    int(raw["drv_age_lic1"].eq(111).sum()),
                    int(raw.loc[second, "drv_age_lic2"].eq(111).sum()),
                    int((raw["drv_age_lic1"].ne(111) & (raw["drv_age_lic1"] > raw["drv_age1"])).sum()),
                    int(young1.sum()),
                    int(young2.sum()),
                    int(raw["vh_weight"].eq(0).sum()),
                    int(raw["vh_weight"].gt(MAX_WEIGHT).sum()),
                    int(raw["vh_value"].eq(0).sum()),
                    int(raw["vh_cyl"].eq(0).sum()),
                ],
                "made missing": ["yes"] * 9 + ["no (electric vehicles)"],
            },
            index=pd.Index(
                [
                    "drv_age2 and drv_age_lic2 = 0, no second driver",
                    "drv_age_lic1 = 111",
                    "drv_age_lic2 = 111",
                    "drv_age_lic1 above drv_age1, other values",
                    "drv_age1 - drv_age_lic1 below 16 (licence before 16)",
                    "drv_age2 - drv_age_lic2 below 16 (licence before 16)",
                    "vh_weight = 0",
                    "vh_weight = 7,901 kg (one Peugeot 205)",
                    "vh_value = 0",
                    "vh_cyl = 0",
                ],
                name="value",
            ),
        )
        return [
            Decision(
                "Negative policy totals are set to 0",
                "A negative claim comes from a legal recourse (rules, Sec. 4.33). Tweedie and Poisson losses need a "
                "non-negative target, so a policy whose claims net below 0 counts as 0, as the AI suggested (record, "
                "2026-10-30) and as frempl does; AIcrowd set these totals to 0 on the same portfolio. The total is "
                "clipped, not each claim; the clip raises the total claim cost by 4.8% (Mini 12.5%).",
                totals,
            ),
            Decision(
                "Placeholder and impossible values are made missing",
                "The rules give 0 as the age of an absent second driver (Sec. 4.15); a licence of 111 years, longer "
                "than the driver's age or taken before 16, a weight or value of 0 and a Peugeot 205 of 7,901 kg cannot "
                "be.",
                placeholders,
            ),
        ]
