"""Curated dataset definition for `frempl_french_motor_personal_line` (data-foundry v2). Evidence: README.md."""

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
    ScoringColumn,
    TaskSummary,
    drop_columns,
)
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

# The five samples of the portfolio that share one schema (CASdatasets freMPL5 to freMPL9).
FILES = (5, 6, 7, 8, 9)
# The 20 columns every one of the five files holds, in their order.
SOURCE_COLUMNS = [
    "Exposure",
    "LicAge",
    "RecordBeg",
    "RecordEnd",
    "Gender",
    "MariStat",
    "SocioCateg",
    "VehUsage",
    "DrivAge",
    "HasKmLimit",
    "ClaimAmount",
    "ClaimNbResp",
    "ClaimNbNonResp",
    "ClaimNbParking",
    "ClaimNbFireTheft",
    "ClaimNbWindscreen",
    "OutUseNb",
    "RiskArea",
    "BonusMalus",
    "ClaimInd",
]
# The policyholder's attributes that stay fixed from one record of a policy to the next.
PROFILE = ["Gender", "MariStat", "SocioCateg", "VehUsage", "HasKmLimit", "RiskArea"]
TARGET = "log1p_claim_amount"


def _continues_next(raw: pd.DataFrame) -> pd.Series:
    """True where the next row of the same file continues the record: the same profile, starting where it ends."""
    nxt = raw.groupby("file", sort=False).shift(-1)
    same = np.logical_and.reduce([raw[c].eq(nxt[c]).to_numpy() for c in PROFILE])
    return pd.Series(
        same & raw["RecordEnd"].eq(nxt["RecordBeg"]).to_numpy() & (nxt["DrivAge"] - raw["DrivAge"]).between(0, 1),
        index=raw.index,
    )


def _policy_components(df: pd.DataFrame, link: pd.Series) -> np.ndarray:
    """The policy component of each record of ``df`` (rows in file order): records are joined where one may continue
    the other, in the next row of its file (``link``) or in any of the five files: the same profile, starting the day
    the other ends, the driver's age the same or one more, the licence age advanced by the months between the two
    starts within one month.
    """
    pos = np.arange(len(df))
    rec = df[[*PROFILE, "DrivAge", "LicAge"]].assign(
        pos=pos, beg=pd.to_datetime(df["RecordBeg"]).to_numpy(), end=pd.to_datetime(df["RecordEnd"]).to_numpy()
    )
    m = rec[rec["end"].notna()].merge(rec, left_on=[*PROFILE, "end"], right_on=[*PROFILE, "beg"], suffixes=("", "_n"))
    months = (m["end"].dt.year - m["beg"].dt.year) * 12 + (m["end"].dt.month - m["beg"].dt.month)
    m = m[(m["DrivAge_n"] - m["DrivAge"]).between(0, 1) & ((m["LicAge_n"] - m["LicAge"] - months).abs() <= 1)]
    nxt = pos[link.to_numpy()]
    i = np.concatenate([m["pos"].to_numpy(), nxt])
    j = np.concatenate([m["pos_n"].to_numpy(), nxt + 1])
    graph = coo_matrix((np.ones(len(i)), (i, j)), shape=(len(df), len(df)))
    return connected_components(graph, directed=False)[1]


class FremplFrenchMotorPersonalLine(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "What will a French motor policy's claims cost over one period of cover in 2004, from its rating factors, "
            "its claim history and the period's length?"
        ),
        use_case=(
            "For example, a French motor insurer pricing a personal-line policy: when a period of cover starts, it "
            "estimates the claim cost from the rating factors to rank the risk and set the premium. The source names "
            "no use."
        ),
        row=(
            "One record of a car policy at an unnamed French private insurer in 2004: a period of cover within the "
            "year with fixed rating factors (115,155 records from five samples of the portfolio; a policy whose "
            "contract changed during the year has several consecutive records)."
        ),
        predicted=(
            "The total claim amount of the record's guarantee over its period (currency not stated): 0 for 90.6% of "
            "the records, those with no claim or with a not-at-fault claim whose recourse covered the payment "
            "(0.84%). Shipped as log1p, scored on the amount."
        ),
        known=(
            "The driver's age, gender, marital status and socio-professional category, the licence age, the vehicle "
            "use and a km limit, the bonus-malus, a risk area, the claims of the four preceding years by type, the "
            "out-of-use periods in those years, and the period's length in whole months: up to 31 December, or to "
            "the next record when the contract changed."
        ),
        split=(
            "Policies held out: a policy's records, in one sample file or across them, stay on one side, so the test data "
            "stands for other policies' periods in the same year; a tariff is applied to next year's policies, which "
            "a release of one year cannot test."
        ),
        changes=(
            "We stacked five samples of the portfolio that share one schema, dropped 45 exact copies, set 967 "
            "negative amounts to 0, gave the 25,131 records that ended early with no continuation the length known "
            "at their start, rounded every length to whole months, and dropped the record dates and the claim "
            "indicator."
        ),
        fit="approximate",
        fit_reason=(
            "The features are an insurer's rating factors, known when a period starts. But held-out policies of one "
            "year stand in for next year's; the amount spans every counted claim type (windscreen, at fault, not at "
            "fault, parking, fire-theft), its basis (paid or incurred) and valuation date not stated; the sample "
            "cuts are undocumented; and a record that continues in a next one keeps its realised length, known at "
            "its end."
        ),
    )

    # Dataset
    unique_name = "frempl_french_motor_personal_line"
    year = "2014"
    domain = "insurance"
    source = "Other"  # the R package CASdatasets (Dutang and Charpentier); no closer schema value
    source_url = "https://dutangc.github.io/CASdatasets/reference/freMPL.html"
    license = "GPL (>= 2)"  # CASdatasets DESCRIPTION
    data_tags = ("ForcedGroupedFromTemporal",)
    download_description = """
        The R package CASdatasets (Dutang and Charpentier; DOI 10.57745/P0KHAG) holds freMPL1 to freMPL10, "ten
        datasets [that] come from a private motor French insurer" (man/freMPL.Rd). We take freMPL5 to freMPL9 of
        version 1.2-1, whose files of 2026-04-10 remove "around 9995" duplicated rows per file (NEWS), from the
        package's GitHub repository at the commit that made that change (3f5c00c, "update freMPL* files by removing
        duplicated rows", 2026-04-11; still the files on master on 2026-11-01), and export them to CSV with pyreadr;
        in R, write.csv(freMPL5, "freMPL5.csv", row.names = FALSE) gives the same values. Older releases and mirrors
        carry the duplicated rows.

        mkdir -p local-data-warehouse/frempl_french_motor_personal_line/rda && cd local-data-warehouse/frempl_french_motor_personal_line
        for i in 5 6 7 8 9; do wget -P rda https://raw.githubusercontent.com/dutangc/CASdatasets/3f5c00cf7312e0a002c220668ccb73ac5b577dd0/data/freMPL$i.rda; done
        sha256sum rda/freMPL*.rda
        # 9186f84c52891d2dca5bd217c0fcbab33b96070f87718b8d7b3438a92ff47dd8  rda/freMPL5.rda
        # 4914f3c9d4b931bdd06cc4d56fa536d04c651865dade8d2d307f1985f4517a06  rda/freMPL6.rda
        # 1ee5857879265a805c68ec48087590561f383422506de44bd0f9df0e0038c6db  rda/freMPL7.rda
        # 14141da2ad0d6f25b59753e5f04af00ca32f58add1d249e8ba8dea66c6a772b2  rda/freMPL8.rda
        # 471aa6d3e1179e8ec5347f659f855652ea5a1603d427f2752a0d2e4518a1fab0  rda/freMPL9.rda
        uvx --from pyreadr==0.5.7 --with pandas==3.0.6 python -c "import pyreadr; [pyreadr.read_r(f'rda/freMPL{i}.rda')[f'freMPL{i}'].to_csv(f'freMPL{i}.csv', index=False) for i in range(5, 10)]"
        sha256sum freMPL*.csv
        # 852f97105e5740ef03a26f77aec396963da56bd99792e4155e9bc315949a87eb  freMPL5.csv
        # 9515b43e9339f3831f16e4548cc0341f79c4fc351a9b0afdabc5c91262dbd563  freMPL6.csv
        # 7b760c18457a9d0eb5a146f8828fab596f83a0778a92d2c9ff9c2182792456b9  freMPL7.csv
        # e8e8215963d599c8d11566fc52b12cae2b902347b94989e73c0fbb1e8ccafa13  freMPL8.csv
        # cc64d8948983a4ed4850a12d826a04a390681953deeff61764359fd8e966274a  freMPL9.csv
    """
    bibtex = r"""
        @manual{Dutang2026CASdatasets,
          title = {{CASdatasets}: Insurance Datasets},
          author = {Dutang, Christophe and Charpentier, Arthur},
          year = {2026},
          note = {R package version 1.2-1; the data sets freMPL1 to freMPL10 entered the package on 9 September 2014},
          doi = {10.57745/P0KHAG},
          url = {https://dutangc.github.io/CASdatasets/reference/freMPL.html}
        }
    """
    curation_comments = """
        We start with freMPL5 to freMPL9 of CASdatasets 1.2-1, five samples of one French motor portfolio of 2004.

        - Prediction point: the start of a record, a period of cover with fixed rating factors, when the insurer prices it. The rating factors, the claim counts of the four preceding years and the bonus-malus are known then; the claims of the period are not. A record ends at the end of 2004 (48%) or when the contract changes or ends. 38% of the records start on 1 January, the calendar cut of the release rather than a pricing event, so a record holds the factors in force over its period.
        - Year: the data sets entered CASdatasets on 9 September 2014 ("freMPL1.rda 09/09/2014" to "freMPL10.rda 09/09/2014" in the dated data list of the package's NEWS, version 1.0-7, the oldest in its GitHub repository).
        - Which files: freMPL5 to freMPL9 share 20 columns in one order and one coding, so they are stacked without a file column (115,200 records). They are samples of one portfolio drawn differently, sharing policies across files: the claim rate runs from 7.7% (freMPL9) to 10.0% by file, and a model tells each file from the others at a one-vs-rest AUC of 0.57 to 0.64. But a model trained on four files ranks the claims of the fifth like random folds do (claim AUC 0.690 against 0.687), and a new record has no file. freMPL1 to freMPL4 and freMPL10 are left out: freMPL1 repeats 39% of its contracts and their claim amounts in freMPL5 to freMPL9, freMPL2 to freMPL4 hold amounts derived from freMPL1's claims, and freMPL10 has another column list (measured on 1.2-1 in the curation record, 2026-10-20; not re-measured here). Each file's size is a round number (16,000 to 32,400 records), so each is a sample of a chosen size; why the samples were cut is undocumented.
        - 45 exact copies dropped (89 records share all 20 columns, their dates included, with another record; 10 of the copies within a file, 35 across files): a copy over this many columns is a collection artefact, not a second record (LEAK-18). Once the dates are dropped and the length is rounded to months, 391 records repeat another record's features and amount (124 of them in the same within-file chain), and 49 share the features with another amount: records of the same profile and length in other periods of 2004, kept (LEAK-18); 0.3% to 0.4% of each test fold had its features in the training side on the earlier chain folds, 0.1% to 0.2% on the shipped component folds.
        - 967 negative amounts (0.84% of the records, -1,948 to -2) set to 0. Every one has `ClaimInd` = 0, but they are claims of the period: of the 246 with a next record, 95.1% are followed by a rise of the not-at-fault claim counter (after 0.19% of the zero amounts and 18.6% of the positive ones), so they are not-at-fault claims whose recourse covered the payment, with no net claim cost to the period. They are -2.4% of the net claim cost. AIcrowd's pricing game of 2020-21 set negative totals to 0 on the 2017 game's portfolio.
        - `ClaimInd` dropped: the claim indicator of the same period, 1 exactly where the amount is positive (a part of the target).
        - `RecordBeg` and `RecordEnd` dropped. `Exposure` is the record's length in years, (end - start) / 365 within 0.006, an open record ending on 31 December. The end of a record is not known when it starts, and the exact value of `Exposure` alone gave it away: its three decimals told a record that ended early from an open one at AUC 0.91 (0.61 once rounded to months).
        - `Exposure` of the 25,131 records (21.8%) that end before 31 December with no continuation in their file is set to the length known at their start, the `Exposure` of the open records that start the same day (every start day has some); then every `Exposure` is rounded to whole months, 0 for the 3,964 records shorter than half a month (LEAK-10, LEAK-7). Their end was not foreseen, and claims drive it: they hold 20.7% of the exposure but 38.9% of the claim cost (837 per exposure-year against 311 for open records) and 66 of the 109 largest claims. On the earlier folds by within-file chain the fix raises the row Gini from 0.281 to 0.332 and lowers the claim AUC from 0.689 to 0.673, both on 9 of 9 splits (untuned LightGBM): the realised length ranked claim occurrence too well and hid the large claims that ended their contracts. The rounding costs nothing (0.330 and 0.673 with three decimals) and stops the decimals from marking a record that continued (AUC 0.92 to 0.71). This departs from the curator's call for fremtpl2 (CC 2026-10-20, `Exposure` kept as recorded) and from the AI's suggested call of 2026-10-30: here the dates locate the early ends row by row, which fremtpl2's data cannot, and the shipped value encoded them. Confirmed by the curator (Andrej, 2026-11-02) and recorded as the LEAK-10 case for time on risk cut short by the outcome: the cut is fixed where the data locates it.
        - Potential leak, kept on purpose: the 34,324 records that end early and continue in the next record of their file (the contract changed) keep their realised length, known only at their end. Some changes follow a claim (a vehicle replaced): these records cost 407 per exposure-year against 311 for open records. They stay because a change is often planned (the bonus-malus steps down at the change, as at an anniversary) and the release cannot tell the planned changes from the others. Revisit if a release gives the contracted term or why a record ended.
        - Note: `Exposure` stays a feature: the period is known when a policy is priced, and pricing models take it as known (a GLM offset). Added to the other features it lifts the claim AUC from 0.565 to 0.673 (untuned LightGBM, the 9 shipped splits); as a raw score it ranks claims at 0.654 and losses at a row Gini of 0.277, against 0.332 for a model on all features (earlier chain folds; under the shipped metric the length alone scores 0.028 against 0.147), which beats it on 9 of 9 splits, so the task is no lookup of the length (TP-4).
        - Policy components, the group column `policy_component` (never a feature; Andrej, 2026-11-03, review issue 1: B, the most conservative key): a policy whose contract changed in 2004 has several records. 34,324 records (30%) continue in the next row of their file (the same profile, starting the day the record ends, the driver's age the same or one more; 1 such link by chance with the rows shuffled), and 10,292 more continue only in another sample file (the same profile and dates, the licence age advanced by the months between the starts within one). Every record joined to another by either link is in one component: 68,857 components of 1 to 13 records, 85,124 records in components of two or more. A later record's claim counters include the earlier record's claim, so in the training side it would tell a test record's claim; the folds keep each component on one side (SPLIT-9). Links across files match about 1% by chance; a chance link only puts two policies in one group, which makes the split stricter (SPLIT-24, exactness weighed against coverage).
        - The claim counts are taken at each record's start: at least one rises at the next record after 95% of the claims and after 2.3% of the other records, so they hold the history known when the record starts and never its own claim.
        - Target `log1p_claim_amount`, log1p of `ClaimAmount` ("Total claim amount of the guarantee"), the scale a model of a skewed amount is fit on; the metric is computed on the amount (`target_transform="log1p"`, MET-3). 90.6% of the records are 0: no claim, or a not-at-fault claim whose recourse covered the payment (89.7% as published, plus the 0.84% negative amounts set to 0). Only the claim part carries signal: on the three shipped folds of the first repeat a claim model ranks claims at AUC 0.67, but a severity model scores R^2 -0.20 to -0.01 on the claimants (-0.02 to -0.01 on log amounts), and even the true claim indicator times the claimants' mean explains only 2% to 15% of the variance of the amount. Which guarantee the amount covers is not named, but the counter that rises after a claim shows every counted type: of the 2,361 claims followed by exactly one counter rise, 40% raise the windscreen counter, 28% the at-fault one, 17% the not-at-fault one, 9% parking and 6% fire-theft. Whether the amounts are paid or incurred, and when they were valued, is not stated.
        - Dtypes: `Gender`, `MariStat`, `SocioCateg` (the union of the five files' codes, 46 CSP codes, 23 of them with fewer than 10 records), `VehUsage` and the yes/no flag `HasKmLimit` categorical; `RiskArea` stays a number, as shipped (the source: "Unknown risk area between 1 and 13, possibly ordered"); ages, counts, `BonusMalus` and `Exposure` (in years, whole months) numeric.
        - Anomaly: the largest claim, 802,620, is 3.6% of all claim cost (the next is 163,427); the ten largest are 7.6%. Kept as recorded.
        - Anomaly: 47 records imply a licence before the age of 17 (`DrivAge` in whole years minus `LicAge` in months below 17 years); the dates both ages refer to are not documented, so they stay as recorded.
        - Note: `Gender` was a rating factor in 2004; EU law has barred it from insurance prices since 21 December 2012 (Court of Justice, Test-Achats, C-236/09). Kept, as the insurer recorded it.
    """
    accepted_check_warnings = {
        "task_target_value_dominant": (
            "Zero-inflated by nature: the claim amount is 0 for 90.6% of the records, those with no claim (89.7%) or "
            "with a not-at-fault claim whose recourse covered the payment (0.84%, negative amounts set to 0); not a "
            "cap or a placeholder."
        ),
    }

    # Task
    target = TARGET
    problem_type = "regression"
    metric = Metric.from_context(
        "ordered_lorenz_gini",
        reason=(
            "CASdatasets defines no task or metric for freMPL (the freMPL page, NEWS), and no paper that defines a "
            "task on these tables was found. Tariffs are compared by the Gini index of an ordered Lorenz curve of "
            "losses (Frees, Meyers and Cummings 2011, JASA 106:1085-1098; CAS Monograph 5, sec. 7.2.4): records "
            "sorted by predicted cost per year of cover, the cumulative share of the exposure against the cumulative "
            "share of the losses. The base is the feature `Exposure` before its rounding (`exposure_at_start`): the "
            "length known at the start for records that ended alone, whose early end often follows a claim (with "
            "their realised length as base a constant prediction scored 0.184); continued records keep their realised "
            "length in the base as in the feature, so the ratio stays neutral (with the known-at-start length there, "
            "the length alone would score 0.176 of a model's 0.249). The length alone scores 0.028 here, where the "
            "row Gini gave it 0.277 of a model's 0.319 (Andrej, 2026-11-03, review issue 4: C). Not normalized: 0 is an order "
            "no better than the base, the same cost per year for every record. On the 9 shipped splits untuned "
            "LightGBM scores 0.147 (0.052 to 0.179), random predictions 0.049 on average (0.015 to 0.104), the same "
            "models' row Gini 0.324."
        ),
        inputs={"weight": "exposure_at_start"},
        target_transform="log1p",
    )
    scoring_columns = (
        ScoringColumn(
            column="exposure_at_start",
            role="weight",
            used_by="ordered_lorenz_gini",
            description=(
                "the record's length in years as the feature `Exposure` holds it before its rounding to months (known "
                "at the start except for continued records, as in the feature): records are sorted by prediction / exposure_at_start and the cumulative share of the "
                "losses is set against the cumulative share of this exposure. Never a feature."
            ),
        ),
    )
    grouping = Grouping(
        on="policy_component",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a policy component: a record and every record that may continue it, in the next row of its sample file or in another file (the same six profile columns, starting the day the other ends, the driver's age the same or one year more, the licence age advanced by the months between the starts within one), joined transitively; 68,857 components of 1 to 13 records, 85,124 records in components of two or more. The release has no policy id. The use case prices a period when it starts: a later record of the policy does not exist yet, and its claim counters include the earlier record's claim, so all records of a component stay on one side (SPLIT-9). Each record is one prediction, made from its own row. About 1% of the links across files match by chance; such a link only joins two policies into one group, the conservative side (SPLIT-24; Andrej, 2026-11-03: the most conservative key).
        """,
    )
    splits_comment = """
        Default splits, grouped by policy component (`policy_component`): a policy's records, in one sample file or
        across them, stay on one side (68,857 components for 115,155 records). A tariff is fit on past policy-years and applied to the
        next year's policies, so the task is temporal by its use case, but the release holds one year (records within
        2004), so held-out policies of the same year stand in for next year's (ForcedGroupedFromTemporal, SPLIT-8).
        Windows inside 2004 can train only on records whose period had ended by the cutoff: 13% to 39% of the rows for
        1 April, 1 July and 1 October, below the 50% floor, and only contracts that ended early; on the records that
        start in the next three months they reach a claim AUC of 0.55, 0.59 and 0.62, against 0.60, 0.59 and 0.62 for
        as many random records. Random records would put a test record's later records in the training side: about a
        fifth of each test fold had one, and its claim counters rose after 87% of the test record's claims and after
        0.9% of the others. A lookup that finds such a record among the training rows from the features alone took a
        LightGBM model from a normalized Gini of 0.303 to 0.395 on the same test rows when those later records stayed
        in training (3 of 3 folds, before the `Exposure` fix); LightGBM alone reads one row at a time and scores the
        same either way. Grouping costs nothing measured: on the earlier folds by within-file chain untuned LightGBM
        scored a row Gini of 0.332 and a claim AUC of 0.673, 0.329 and 0.673 on random ones, and the component key
        against the chain 0.2785 against 0.2827 (before the fix); on the shipped component folds it scores a row Gini
        of 0.324 and a claim AUC of 0.668. The component also joins the 10,292 records that continue only in another
        file, which the chains left apart; under the chains a lookup of such a record had ranked claims at AUC 0.51.
        Shipped forced on the curator's call (Andrej, 2026-11-02: "Forced group splits should be fine"). The leak test
        across the split (SPLIT-8, 2026-11-02, on the chain folds) finds none, and the leak probe on the component
        folds flags nothing (2026-11-03): the 0.37% of test rows whose features were in training agree on a claim less than the base rate (84%
        against 91%), and the training side's mean outcome of the test row's start month (and risk area by month) moves
        the Gini by -0.0005 on average; dropping the test rows' own quarter from training costs no more than dropping as
        many random rows.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        frames = []
        for i in FILES:
            df = pd.read_csv(raw_dir / f"freMPL{i}.csv")
            assert list(df.columns) == SOURCE_COLUMNS, i
            df["file"] = i
            frames.append(df)
        return pd.concat(frames, ignore_index=True)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.copy()
        # 1. Exact copies over all 20 source columns (the dates included): a collection artefact (45 rows).
        df = df[~df.duplicated(subset=SOURCE_COLUMNS, keep="first")]
        # 2. Negative amounts occur only with ClaimInd = 0: not-at-fault claims whose recourse covered the payment,
        #    no net claim cost of the period, set to 0.
        assert (df.loc[df["ClaimAmount"] < 0, "ClaimInd"] == 0).all()
        df["ClaimAmount"] = df["ClaimAmount"].clip(lower=0)
        # 3. The claim indicator is a part of the target.
        assert (df["ClaimInd"].eq(1) == df["ClaimAmount"].gt(0)).all()
        # 4. The record dates: Exposure is their difference; the end is not known when the record starts.
        start = pd.to_datetime(df["RecordBeg"], format="%Y-%m-%d")
        end = pd.to_datetime(df["RecordEnd"], format="%Y-%m-%d").fillna(pd.Timestamp("2005-01-01"))
        assert ((end - start).dt.days / 365 - df["Exposure"]).abs().max() < 0.007
        # 5. The policy component, the group column: a record and every record that may continue it, in the next row
        #    of its file or in another file (issue 1, B).
        link = _continues_next(df)
        df["policy_component"] = _policy_components(df, link)
        # 6. A record that ended before 31 December with no continuation takes the length known at its start: the
        #    Exposure of the open records that start the same day (else the days to 1 January 2005 / 365, at most 1).
        #    Every Exposure is then rounded to whole months, so its decimals do not tell how a record ended.
        open_record = df["RecordEnd"].isna()
        to_year_end = np.floor(np.minimum((pd.Timestamp("2005-01-01") - start).dt.days / 365, 1.0) * 1000) / 1000
        known_at_start = df["Exposure"].where(open_record).groupby(start).transform("median").fillna(to_year_end)
        ended_alone = ~open_record & ~link
        df.loc[ended_alone, "Exposure"] = known_at_start[ended_alone]
        #    The metric's base is the feature's length before the rounding (issue 4, C): known at the start for open
        #    records and those that ended alone; for continued records the realised length, as in the feature (a leak
        #    kept on purpose), so the ratio of the two stays neutral. A scoring column, never a feature.
        df["exposure_at_start"] = df["Exposure"]
        df["Exposure"] = (df["Exposure"] * 12).round() / 12
        df = drop_columns(df, ["ClaimInd", "RecordBeg", "RecordEnd", "file"])
        # 7. The target on the log1p scale (the metric inverts it: target_transform="log1p").
        df[TARGET] = np.log1p(df.pop("ClaimAmount"))
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["Gender", "MariStat", "SocioCateg", "VehUsage", "HasKmLimit"])

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        records = raw[~raw.duplicated(subset=SOURCE_COLUMNS)]
        link = _continues_next(records)
        status = pd.Series(
            np.select([records["RecordEnd"].isna(), link], ["open at year end", "continued"], "ended alone"),
            index=records.index,
        )
        length = pd.cut(records["Exposure"], [0, 0.1, 0.25, 0.5, 0.75, 0.99, 1.0], include_lowest=True)
        claims = (
            records.groupby([length, status], observed=True)["ClaimInd"]
            .agg(records="size", claim_rate="mean")
            .unstack()
            .round(3)
        )
        claims.columns = [f"{stat}, {state}" for stat, state in claims.columns]
        claims.index = claims.index.astype(str).rename("realised Exposure (years)")
        nxt = records.groupby("file", sort=False).shift(-1)
        sign = np.sign(records["ClaimAmount"]).map({-1.0: "negative", 0.0: "zero", 1.0: "positive"})
        negatives = (
            records.assign(
                next_record=link,
                not_at_fault_rise=link & nxt["ClaimNbNonResp"].gt(records["ClaimNbNonResp"]),
            )
            .groupby(sign.rename("ClaimAmount"))
            .agg(
                records=("ClaimInd", "size"),
                claim_ind_1=("ClaimInd", "mean"),
                with_next_record=("next_record", "sum"),
                not_at_fault_rise=("not_at_fault_rise", "sum"),
            )
        )
        negatives["share of those with a next record"] = (
            negatives["not_at_fault_rise"] / negatives["with_next_record"]
        ).round(4)
        component = pd.Series(_policy_components(records, link))
        sizes = (
            component.value_counts()
            .value_counts()
            .sort_index(kind="stable")
            .rename_axis("records in the component")
            .rename("components")
        )
        return [
            Decision(
                "Records that ended with no continuation take the length known at their start",
                "A record ends at the end of 2004 or when the contract changes or ends; the end is not known when "
                "the record starts. Records that ended with no continuation in their file had more claims than open "
                "ones of the same length, so they take the `Exposure` of the open records that start the same day. "
                "The dates are dropped and every length is rounded to whole months, since the exact value alone told "
                "an ended record from an open one (AUC 0.91).",
                claims,
            ),
            Decision(
                "Negative claim amounts are set to 0",
                "Every negative amount belongs to a record with `ClaimInd` = 0, yet the not-at-fault claim counter "
                "rises at the next record after 95% of them, as after a claim: not-at-fault claims whose recourse "
                "covered the payment, with no net claim cost to the period.",
                negatives,
            ),
            Decision(
                "The records of a policy stay on one side of the split",
                "A record continues another, in the next row of its file or in another file, when the profile is the "
                "same, it starts the day the other ends and the driver's age is the same or one more (across files "
                "also the licence age advanced by the months between the starts). A later record's claim counters "
                "include the earlier record's claim: under random records, a lookup on the features alone lifted a "
                "LightGBM model's normalized Gini by 0.09 on the same test rows, a gain that went with those later "
                "records. Every record joined by such a link is in one group (`policy_component`), the most "
                "conservative key (Andrej, 2026-11-03).",
                sizes,
            ),
        ]
