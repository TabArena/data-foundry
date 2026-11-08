"""Curated dataset definition for `spanish_homeowners_motor_insurance_2010_2014` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    TaskSummary,
    Temporal,
    TemporalSplits,
    drop_columns,
)

RAW_FILE = "data_ex.csv"
TARGET = "log1p_home_claim_cost"
# The release's year 1 is 2010 (data article, Table 1: 2010 to 2014).
FIRST_YEAR = 2009
# The rating fields: one value per customer in every year of the release (measured: no customer's value changes).
RATING_FIELDS = [
    "gender",
    "Age_client",
    "age_of_car_M",
    "Car_power_M",
    "Car_2ndDriver_M",
    "num_policiesC",
    "metro_code",
    "Policy_PaymentMethodA",
    "Policy_PaymentMethodH",
    "Insuredcapital_content_re",
    "Insuredcapital_continent_re",
    "appartment",
    "Client_Seniority",
]
# The codes of the data article (Sec. 1) and the Mendeley description, with their labels.
LABELS = {
    "gender": {1: "male", 0: "female"},
    "Car_2ndDriver_M": {0: "no", 1: "yes"},
    "metro_code": {0: "rural", 1: "urban or metropolitan"},
    "Policy_PaymentMethodA": {1: "annual", 0: "monthly"},
    "Policy_PaymentMethodH": {1: "annual", 0: "monthly"},
    "appartment": {1: "apartment", 0: "house"},
}
# The customer's claims of the years before the row's year, known at its renewal (USE-10, LEAK-34).
HISTORY = {
    "prev_home_claims": "NClaims2",
    "prev_home_claim_cost": "Claims2",
    "prev_motor_claims": "NClaims1",
    "prev_motor_claim_cost": "Claims1",
}
PAST_COUNTS = {"past_home_claims": "NClaims2", "past_motor_claims": "NClaims1"}


def _ordered(raw: pd.DataFrame) -> pd.DataFrame:
    """The rows of each customer in year order (the file is ordered by year, then by customer)."""
    return raw.sort_values(["PolID", "year"], kind="stable")


def _with_history(raw: pd.DataFrame) -> pd.DataFrame:
    """The previous year's and the earlier years' claims of the same customer; missing in 2010 (no history shipped)."""
    df = _ordered(raw).copy()
    by_customer = df.groupby("PolID", sort=False)
    for new, col in HISTORY.items():
        df[new] = by_customer[col].shift(1)
    for new, col in PAST_COUNTS.items():
        df[new] = by_customer[col].transform(lambda s: s.shift(1).cumsum())
    return df


class SpanishHomeownersMotorInsurance20102014(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "What will a Spanish customer who holds both a motor and a home policy at one insurer cost it in home "
            "claims in the coming year?"
        ),
        use_case=(
            "A Spanish insurer, at the yearly renewal of a customer who holds its motor and its home policy, "
            "estimates the coming year's home claim cost to set the home premium. The model paper prices the next "
            "period's home premium for such customers (Frees et al. 2021, Sec. 3.5, Table 8)."
        ),
        row=(
            "One customer-year, 2010 to 2014, of a random sample of 40,284 private customers who held both policies "
            "in 2010, followed until they lapsed either policy: 122,935 rows, fewer each year (40,284 in 2010, "
            "13,284 in 2014)."
        ),
        predicted=(
            "The year's home claim cost in euros, 0 for 98.2% of the customer-years. Shipped as log1p, scored on "
            "the amount."
        ),
        known=(
            "The customer's age, gender and years with the insurer; the car's age, power and second driver; urban "
            "or rural; the payment method of each policy; the insured values of the contents and the building; "
            "apartment or house; and the customer's motor and home claims of the earlier years in the release."
        ),
        split=(
            "Three yearly windows, 2014, 2013 and 2012, each trained on all earlier years, so the test data stands "
            "for next year's renewals of the customers still holding both policies."
        ),
        changes=(
            "We added the customer's claims of the previous year and the earlier years as inputs, and dropped the "
            "year's own outcomes: the home claim count, the motor claims, the claim type and the renewal at the "
            "year's end."
        ),
        fit="approximate",
        fit_reason=(
            "Real renewals of one insurer's bundle customers, but the rating fields were read once, at an unstated "
            "date; with no current premium the task ranks renewal risk; no customer enters after 2010, so the test "
            "years drift towards claim-free survivors (30.7% of claim years end in a lapse, 24.5% of claim-free "
            "years), while lapse rows claim more (2.21% against 1.65%), so lapse years stay."
        ),
    )

    # Dataset
    unique_name = "spanish_homeowners_motor_insurance_2010_2014"
    year = "2021"
    domain = "insurance"
    source = "Other"  # Mendeley Data, the repository the authors published in; no closer schema value
    source_url = "https://doi.org/10.17632/vfchtm5y7j.1"
    license = "CC BY 4.0"
    data_tags = ()
    download_description = """
        Version 1 of the Mendeley Data record (DOI 10.17632/vfchtm5y7j.1, published 2021-06-03, CC BY 4.0) holds one
        file, data_ex.csv (122,935 rows x 22 columns, the first an unnamed row number). The file link comes from the
        record's API (https://data.mendeley.com/public-api/datasets/vfchtm5y7j/files?folder_id=root&version=1),
        which also gives its SHA-256 (checked on 2026-11-02). The simulated data of the model paper (Zenodo
        10.5281/zenodo.5425210) is a separate release and not used.

        mkdir -p local-data-warehouse/spanish_homeowners_motor_insurance_2010_2014 && cd local-data-warehouse/spanish_homeowners_motor_insurance_2010_2014
        wget -O data_ex.csv https://data.mendeley.com/public-files/datasets/vfchtm5y7j/files/6a105b8a-fd66-443a-9866-8e7ed11c63e1/file_downloaded
        sha256sum data_ex.csv
        # 904906d5bd00566bd60af40be7ea12b2cb253c2724799ffa761f77d574354eeb  data_ex.csv
    """
    bibtex = r"""
        @article{guillen2021homeowners,
          title = {Case study data for joint modeling of insurance claims and lapsation},
          author = {Guillen, Montserrat and Bolanc{\'e}, Catalina and Frees, Edward W. and Valdez, Emiliano A.},
          journal = {Data in Brief},
          volume = {39},
          pages = {107639},
          year = {2021},
          doi = {10.1016/j.dib.2021.107639},
          note = {Data: Mendeley Data, version 1, doi:10.17632/vfchtm5y7j.1, published 3 June 2021}
        }
    """
    curation_comments = """
        We start with data_ex.csv of Mendeley Data vfchtm5y7j, version 1 (Guillen, Bolancé, Frees and Valdez; described in Data in Brief 39:107639, 2021, read on the University of Barcelona's open copy; the model paper is Frees, Bolancé, Guillen and Valdez 2021, Expert Systems with Applications 185:115552, read on the ANU open copy).

        - Prediction point: the customer's yearly renewal, when the insurer prices the coming year's home cover. The rating fields and the claims of the earlier years are known then; the year's claims and whether the customer renews at its end are not. The model paper (Sec. 3.5) prices the next period's home premium for such customers and argues that the premium should allow for the chance that the insured does not renew; its Table 8 compares the home premiums of three risk profiles with and without the dependence of claims and lapse.
        - Rows: every customer-year of the release is a task row. The sample is "a representative sample of all customers who had homeowners and motor insurance ... In 2010" (data article, Specifications Table), followed until the customer lapses either policy ("If the customer does not renew one of those two policies or both, we do not have more information after this lapse occurs", Sec. 1). Every customer starts in year 1 and the years of each are consecutive (measured; the Specifications Table's "Some new policy holders enter the sample" does not hold in the file). The 10,988 customers still holding both policies after 2014 are 27% of the 2010 sample; lapsers keep every year they were in force, so nothing is selected on survival (USE-5); lapse rows have the higher home claim share (2.21% against 1.65% pooled; 2.01-2.69% against 1.51-1.77% by year), so nothing points to cutting lapse years. The test years hold the customers who renewed both policies until then: the book an insurer prices at that renewal, though one with no new customers after 2010, and one that drifts towards claim-free survivors (30.7% of the years with a home claim end in a lapse, 24.5% of the claim-free years). There is no current premium, so the task ranks renewal risk (USE-8, fit approximate).
        - Time: `year` (1 to 5) becomes `policy_year`, 2010 to 2014 (Table 1 of the data article). Whether a year is a calendar year or a policy year from each renewal is not stated.
        - Target `log1p_home_claim_cost`, log1p of `Claims2` ("the sum of claims cost in the homeowners insurance policy for the corresponding year", in euros), the scale a model of a skewed amount is fit on; the metric is computed on the amount (`target_transform="log1p"`, MET-3). 98.2% of the rows cost 0; no negative amount. The positive costs run from 2.06 to 27,280 euros (median 169). The yearly counts of customers with a home claim (660, 531, 448, 310, 240) and their mean costs match Table 1 of the data article.
        - Why log1p and not the raw amount (MET-3): on the 3 shipped windows untuned LightGBM ranks the costs at a mean normalized Gini of 0.219 fit on log1p and 0.213 by a Tweedie loss on the amount (0.215 by squared error on the amount, on the same rows before the labels were mapped); fit on the amount by squared error it scores R^2 -0.041 on the amount, fit on log1p -0.003. The scale changes no ranking, so the default for a skewed amount holds (CLEAN-16): log1p, which keeps the models off the few largest claims (the 20 largest of each test year carry 40% to 58% of its total loss), with the metric on the amount (MET-3). Other families on log1p: ridge 0.280, a random forest 0.271 (a logistic model of the claim alone 0.272; apartment or house alone 0.177; a constant 0), each above apartment alone in every window.
        - Only the claim part carries signal (the hurdle check of task_probes.md, 3 shipped windows): a claim is ranked at ROC AUC 0.68 to 0.69 (hurdle classifier), while a severity model on the claimants reaches R^2 -0.07 to -0.02 on log costs, and the true claim indicator times the claimants' training mean explains 16% to 22% of the variance of the amount. The hurdle model (claim probability times severity) ranks at a mean Gini of 0.203, the direct log1p model at 0.213.
        - Dropped as the year's own outcomes (USE-3, LEAK-10): `NClaims2`, the year's home claim count (a part of the target: the cost is positive only where it is; 1,742 rows have a claim with no cost, kept as 0, claims closed without payment); `Types`, the joint code of a motor and a home claim in the year; `NClaims1` and `Claims1`, the year's motor claims (the data article's description gives `NClaims2` the motor wording; the counts show it is the home count); `Retention`, whether the customer renews at the year's end (0 exactly on each lapser's last row).
        - Added: the customer's claims of the previous year (`prev_home_claims`, `prev_home_claim_cost`, `prev_motor_claims`, `prev_motor_claim_cost`) and the claim counts of all earlier years in the release (`past_home_claims`, `past_motor_claims`), all missing in 2010, whose history the release does not hold. A known customer's history is a legitimate input (USE-10, LEAK-34), and insurers reward a claim-free year at renewal (model paper, footnote 1). A home claim the year before raises the year's home claim share from 1.7% to 6.0% (2,477 rows); it is no carried-over remnant: of 98 years with a home cost after a year with one, 2 repeat the amount. The `past_*` counts span more years as the year grows (mean `past_home_claims` 0.029 in 2011, 0.121 in 2014); they are kept as the counts the insurer reads at each renewal, and in every training year the count covered that year's span. As per-year rates they scored lower (ridge 0.268 against 0.279, LightGBM 0.215 against 0.219; CLEAN-19).
        - Note: the release's previous-year claims are as finally recorded; at a renewal the insurer knows the claims reported until then, so the last weeks' claims and part of the costs may still be missing. Home claims are reported soon after the event; how far the costs had developed is not stated.
        - Note: every rating field holds one value per customer in all years (measured: no customer's value changes in any field; `Age_client` does not grow by a year), so the fields were read once, at a date the sources do not give. The Specifications Table says "A sample of customer in 2010 was selected", which suggests the selection in 2010; no field is described as the "last" value; and no age implies a read in 2015 (4 customers are 18 and 10 under 23, though these 10 also have seniority above age minus 18, so the floor is circumstantial). No field moves with the claims over time: each field's ROC AUC for a home claim is flat across 2010-2014 and across the years before a customer's lapse (appartment 0.63-0.65 in every year; no field moves by more than 0.045 by year, and at most 0.07, without a trend, by years before a lapse). They are kept (LEAK-10: the read date cannot be located row by row, and the part that can be traced shows no gain). Revisit if the authors give the read date.
        - `PolID` (the customer id, a group of rows; the model sees the customer's history through the added columns) and the file's unnamed row number (ordered by year, then customer) are dropped.
        - The codes get the labels of the data article (Sec. 1): `gender` (male, female), `Car_2ndDriver_M` (no, yes), `metro_code` (rural, urban or metropolitan), `Policy_PaymentMethodA` and `Policy_PaymentMethodH` (annual, monthly; of the motor and the home policy), `appartment` (apartment, house; "0 for houses or semi-attached houses", model paper Table 4); all categorical.
        - Potential leak, kept on purpose: `Policy_PaymentMethodA`, the motor policy's payment method, read once at an unknown date (LEAK-37, LEAK-10). Against motor claims it shows the pattern for which spanish_motor_insurance_2015_2018 drops its last payment method: annual payment is 9.6 points rarer after a motor claim among customers who renew, 0.6 among those who lapsed in 2010, so a switch to monthly payment after a motor claim is possible. It stays because the target is the home claim, where the pattern is absent (5.9 against 8.1 points, the reverse order), and the pair adds no gain a late read could carry: dropping both payment fields moves the mean Gini by -0.013 (null SD of the 3-window mean 0.045), dropping A alone by +0.002, and the pair's gain on renewing minus lapse rows is -0.006 [-0.018, 0.006]; on customers who never had a motor claim the pair still adds +0.019 (leak check of 2026-11-02, nine tests). Revisit if a release gives the read date or a payment history.
        - Note: `Insuredcapital_content_re` and `Insuredcapital_continent_re` (the insured values of the contents and the building) are on a log scale: they run from 2.4 to 14.4 and 5.7 to 15.4, and their exponentials have medians over rows of 31,647 and 104,457 euros. The sources do not say so (the model paper's Table 8 profiles use 3, 8 and 15); kept as recorded. 403 customers have equal values for the two, and 9.7% a content value above the building's.
        - Exposure: no exposure column, and none is needed. A row is a customer-year, and the data article frames a lapse as not renewing at the year's end ("If the customer does not renew one of those two policies or both, we do not have more information after this lapse occurs", Sec. 1), so a lapse year is a whole year as far as the sources say. The release has no dates, so the share of years cut short cannot be measured, only bounded: if a lapse can fall within the year, at most the 29,296 lapse rows are cut short (23.8% of the rows; 17.3 / 22.1 / 24.3% of the test years 2014 / 2013 / 2012). The lapse rows show no sign of a cut: they claim more often, not less (2.21% against 1.65% of rows), and the lapse at the year's end, the only marker a cut could have, adds no Gini as a feature (LightGBM, mean of 3 seeds, 2014 / 2013 / 2012: 0.168 / 0.280 / 0.179 without, 0.129 / 0.265 / 0.168 with). The insured values of the contents and the building are sums insured, rating factors and not an amount at risk the cost grows with in proportion: the elasticity of the cost per row to the insured value is 0.13 (contents) and 0.15 (building), against 1 for an amount at risk (the coefficient of the log value in a log-link Tweedie fit; every 95% interval, also given the other rating fields, ends below 0.5). Across the quintiles of the contents value (median 13,126 to 66,766 euros) the home claim cost per row runs 8.16, 6.37, 6.77, 7.57 and 10.82 euros, and across the building's (35,868 to 258,136 euros) 8.03, 7.56, 7.18, 6.68 and 10.25. So they take neither an offset nor a weight and stay features (MET-14; scored unweighted per contract, MET-15; no LEAK-41 suspect). Their read date is unknown, so their timing is mixed: they are kept under LEAK-10's later-pull clause after the leak check of nine tests (review issue 1, the note above).
        - Anomaly: `num_policiesC` is "the total number of policies held by the same customer in the insurance company" (Sec. 1) but holds only 0 (19%) and 1 (81%), though every customer holds at least two policies; its meaning is unclear. Kept as recorded.
        - Anomaly: `age_of_car_M` ("the number of years since the vehicle was bought by the customer") is 0 for 8,050 of the 40,284 customers (20%), against 406 at 1 and 640 at 2. These customers are older (65 against 58 years) and longer with the insurer (15.3 against 9.1 years), with less powerful cars: not new cars, likely an unknown purchase date. For 161 customers the value exceeds their age minus 18, so the field likely counts the car's age rather than the years since this customer bought it. CLEAN-10 not triggered: the description does not let us infer a code; kept as recorded.
        - Anomaly: `Client_Seniority` is at least 5.0 years for every customer, either by the sample's selection or because it was read at the end of the window (neither is stated), and for 76 customers it exceeds their age minus 18, so it likely counts from a household's or a policy's first contract. Kept as recorded.
        - Anomaly: `Car_power_M` holds a few unusual powers (4 to 15 for 103 rows), in the range of licence-free microcars, so not impossible (CLEAN-11); kept as recorded. `metro_code` is "rural" for 84% of the rows, odd for a Spanish bundle book, and barely separates apartments (62% of the rural customers, 69% of the urban); the labels follow both papers and are kept.
    """

    accepted_check_warnings = {
        "task_time_on_few_unique": (
            "Yearly renewals over five policy years (2010-2014), so the three test windows train on two to four earlier "
            "years; the panel has no finer time (Andrej, 2026-11-02)."
        ),
        "task_target_value_dominant": (
            "Zero-inflated by nature: 98.2% of customer-years have no home claim cost, a real no-claim year and not a "
            "placeholder (Andrej, 2026-11-02)."
        ),
    }

    # Task
    target = TARGET
    problem_type = "regression"
    metric = Metric.from_context(
        "normalized_gini",
        reason=(
            "The data article (Data in Brief 39:107639, Sec. 2) fits Tweedie and logistic models without a held-out "
            "evaluation, and the model paper (ESWA 185:115552, Secs. 3.3-3.5) estimates marginal Tweedie fits and "
            "their dependence and prices three risk profiles; neither scores predictions, and the Mendeley record "
            "defines no task. In insurance pricing, models are compared by the Gini index of an ordered Lorenz curve "
            "of losses: Frees, Meyers and Cummings (2011, JASA 106:1085-1098; Frees is an author of this release) "
            "order the policies by the relativity of a score to the premium, and Allstate's Kaggle competition "
            "(2011), whose rows were whole vehicle-years, the row Gini declared here. The release has no premium, so "
            "every row counts once, ordered by the prediction. RMSE on the amount follows a few large claims: the "
            "20 largest of each test year hold 83% to 94% of its sum of squares, untuned LightGBM scores R^2 -0.07 "
            "to 0.00 on the amount while it ranks claims at ROC AUC 0.61 to 0.70, and even the true claim indicator "
            "times the claimants' mean explains 16% to 22% of the variance. A mean Tweedie deviance on the amount "
            "(power 1.5), the source's own model family, ranks the training-mean constant above every fitted model in "
            "every window, LightGBM with the Tweedie objective included (2014 / 2013 / 2012: 27.1 / 18.2 / 22.2 "
            "against 21.8 / 18.0 / 20.3), while under the Gini the same models score 0.11 to 0.32 against 0 for the "
            "constant. Decided for this table on its own evidence (MET-10, MET-11). The Gini's limits: it ignores "
            "the price level, which pricing sets separately, and the 20 largest claims carry 40% to 58% of each test "
            "year's loss, so a random prediction scores within a null SD of 0.066 to 0.101 in one window; compare "
            "models on the mean of the 3 windows."
        ),
        target_transform="log1p",
    )
    temporal = Temporal(
        on="policy_year",
        splits=TemporalSplits(window=1, unit="unique", n_windows=3),
        horizon=1,
        horizon_unit="years",
    )
    splits_comment = """
        An insurer refits its renewal price on the years it has seen and applies it to the next year's renewals: 3
        test windows of one year, 2014, 2013 and 2012, newest first, each trained on every earlier year (89%, 75% and
        57% of the rows). The test years hold 13,284, 17,044 and 22,505 customer-years, of which 240, 310 and 448 have
        a home claim cost. One window is noisy: a random prediction scores within a null SD of 0.066 to 0.101 of the
        Gini, so compare models on the mean of the 3 windows (TP-9). The test customers are all known: the same
        customers' earlier years are in training (91% of the test rows), and their claims enter as inputs.

        No gap (an exception to SPLIT-10, serving SPLIT-14). At a renewal the previous year's claims are not final.
        The sources do not say how `year` runs. Read as a calendar year, only the claims of the last weeks are
        missing: hiding the newest training year's claims of the last 30 or 90 days gives untuned LightGBM a mean
        Gini of 0.226 and 0.203, against 0.219 as shipped. Read as a policy year from each customer's renewal, the
        newest training year can overlap the test year by up to a year; the upper bound is a run without the newest
        training year, which moves the mean from 0.219 to 0.200 (2014 0.161 to 0.148, 2013 0.315 to 0.244, about one
        null SD, 2012 0.182 to 0.207). Both effects are within the noise. A one-year gap, the smallest the yearly
        column allows, leaves 2012 a training side of 33%, so only two windows would meet SPLIT-14; the curator
        declined a SPLIT-10 amendment (CC on avito_demand_prediction, 2026-11-02).
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / RAW_FILE)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # 1. The rows of each customer in year order; the years are consecutive and start in year 1.
        df = _with_history(raw)
        by_customer = df.groupby("PolID", sort=False)
        assert (by_customer["year"].diff().dropna() == 1).all()
        assert (by_customer["year"].min() == 1).all()
        # 2. The rating fields hold one value per customer (read once, at an unstated date).
        assert (by_customer[RATING_FIELDS].nunique() == 1).all().all()
        # 3. The home cost is positive only where the home claim count is; no negative cost.
        assert not ((df["Claims2"] > 0) & (df["NClaims2"] == 0)).any()
        assert (df["Claims2"] >= 0).all()
        # 4. The time column: year 1 is 2010.
        df["policy_year"] = df["year"] + FIRST_YEAR
        # 5. The codes get their labels.
        for col, labels in LABELS.items():
            assert set(df[col]) <= set(labels), col
            df[col] = df[col].map(labels)
        # 6. The year's own outcomes (home count, motor claims, claim type, renewal), the id and the row number.
        df[TARGET] = np.log1p(df["Claims2"])
        return drop_columns(
            df, ["Claims2", "NClaims2", "Types", "NClaims1", "Claims1", "Retention", "PolID", "year", "Unnamed: 0"]
        )

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=list(LABELS))

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        from sklearn.metrics import roc_auc_score

        rows = _with_history(raw)
        by_customer = rows.groupby("PolID", sort=False)
        changed = (by_customer[RATING_FIELDS].nunique() > 1).sum().rename("customers whose value changes")
        claim = rows["Claims2"] > 0
        auc = pd.DataFrame(
            {
                2009 + y: [
                    roc_auc_score(claim[rows["year"] == y], rows.loc[rows["year"] == y, c]) for c in RATING_FIELDS
                ]
                for y in range(1, 6)
            },
            index=RATING_FIELDS,
        ).round(3)
        fields = pd.concat([changed, auc], axis=1)
        fields.columns.name = "ROC AUC for a home claim, by year"
        by_year = (
            rows.assign(policy_year=rows["year"] + FIRST_YEAR, home_claim=claim)
            .groupby("policy_year")
            .agg(
                rows=("home_claim", "size"),
                with_a_home_claim_cost=("home_claim", "sum"),
                share=("home_claim", "mean"),
                mean_cost_of_claimants=("Claims2", lambda s: s[s > 0].mean()),
                lapse_at_year_end=("Retention", lambda s: int((s == 0).sum())),
            )
            .round(4)
        )
        history = (
            rows.assign(home_claim=claim, previous_year=np.where(rows["prev_home_claims"] > 0, "home claim", "none"))
            .loc[rows["year"] > 1]
            .groupby("previous_year")["home_claim"]
            .agg(rows="size", share_with_a_home_claim_cost="mean")
            .round(4)
        )
        return [
            Decision(
                "The rating fields are one reading per customer, and kept",
                "No customer's value changes over the years in any rating field, so each was read once, at a date "
                "the sources do not give. No field's link to a home claim moves over the years, as a field read "
                "after the claims would. Rows: all customer-years of the release.",
                fields,
            ),
            Decision(
                "Three yearly test windows: rows and home claims per year",
                "Each test year holds a few hundred customers with a home claim cost; the customers who lapse leave "
                "after their year, so the yearly rows fall. Rows: all customer-years of the release.",
                by_year,
            ),
            Decision(
                "The customer's earlier claims are inputs",
                "A home claim in the previous year raises the year's home claim share about threefold; the insurer "
                "knows it at the renewal. Rows: the customer-years from 2011 on.",
                history,
            ),
        ]
