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
# The policyholder's attributes that stay fixed from one record of a policy to the next, unless the contract change
# that ends a record changes one of them (all but `Gender`). `Gender` links the records of a policy and then leaves the
# features (sex is no rating factor; the notes).
PROFILE = ["Gender", "MariStat", "SocioCateg", "VehUsage", "HasKmLimit", "RiskArea"]
# The claim and out-of-use counters of the four preceding years: none falls from a record to its policy's next one.
COUNTERS = ["ClaimNbResp", "ClaimNbNonResp", "ClaimNbParking", "ClaimNbFireTheft", "ClaimNbWindscreen", "OutUseNb"]
TARGET = "claim_amount_per_year"


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
    the other, in the next row of its file (``link``) or in any of the five files: the same gender, starting the day
    the other ends, the driver's age the same or one more, the licence age advanced by the months between the two
    starts within one month, and either the same profile or exactly one of the other five profile columns changed
    with no counter lower (a contract change that also changed the risk area, the km limit, the vehicle use, the
    socio-professional category or the marital status; review issue 8).
    """
    pos = np.arange(len(df))
    rec = df[[*PROFILE, *COUNTERS, "DrivAge", "LicAge"]].assign(
        pos=pos, beg=pd.to_datetime(df["RecordBeg"]).to_numpy(), end=pd.to_datetime(df["RecordEnd"]).to_numpy()
    )
    m = rec[rec["end"].notna()].merge(rec, left_on=["Gender", "end"], right_on=["Gender", "beg"], suffixes=("", "_n"))
    months = (m["end"].dt.year - m["beg"].dt.year) * 12 + (m["end"].dt.month - m["beg"].dt.month)
    m = m[(m["DrivAge_n"] - m["DrivAge"]).between(0, 1) & ((m["LicAge_n"] - m["LicAge"] - months).abs() <= 1)]
    changed = sum(m[c].ne(m[f"{c}_n"]).astype(int) for c in PROFILE if c != "Gender")
    kept = np.logical_and.reduce([m[f"{c}_n"].ge(m[c]).to_numpy() for c in COUNTERS])
    m = m[changed.eq(0) | (changed.eq(1) & kept)]
    nxt = pos[link.to_numpy()]
    i = np.concatenate([m["pos"].to_numpy(), nxt])
    j = np.concatenate([m["pos_n"].to_numpy(), nxt + 1])
    graph = coo_matrix((np.ones(len(i)), (i, j)), shape=(len(df), len(df)))
    return connected_components(graph, directed=False)[1]


class FremplFrenchMotorPersonalLine(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "What will a French motor policy's claims cost per year of cover over one period of 2004, from its rating "
            "factors, its claim history and the time left in the year?"
        ),
        use_case=(
            "For example, a French motor insurer pricing a personal-line policy: when a period of cover starts, it "
            "estimates the claim cost per year of cover from the rating factors to rank the risk and set the premium. "
            "The source names no use."
        ),
        row=(
            "One record of a car policy at an unnamed French private insurer in 2004: a period of cover within the "
            "year with fixed rating factors (115,155 records from five samples of the portfolio; a policy whose "
            "contract changed during the year has several consecutive records)."
        ),
        predicted=(
            "The claim amount of the record's guarantee per year of cover (currency not stated): the period's total "
            "divided by its realized length. 0 for 90.6% of the records, those with no claim or with a not-at-fault "
            "claim whose recourse covered the payment (0.84%). Shipped and scored as the amount per year, untransformed; "
            "each record counts in proportion to its realized length, in training and scoring."
        ),
        known=(
            "The driver's age, marital status and socio-professional category, the licence age, the vehicle use and "
            "a km limit, the bonus-malus, a risk area, four years of claim and out-of-use history, and the time from "
            "the period's start to 31 December. Not gender, which EU insurers may no longer price on, nor the "
            "realized length: a claim can cut it short, so it is the rate's denominator and each record's weight."
        ),
        split=(
            "Policies held out: a policy's records, in one sample file or across them, stay on one side, so the test data "
            "stands for other policies' periods in the same year; a tariff is applied to next year's policies, which "
            "a release of one year cannot test."
        ),
        changes=(
            "We stacked five samples of the portfolio that share one schema, dropped 45 exact copies, set 967 "
            "negative amounts to 0, divided each amount by the record's realized length, weighted each record by "
            "that length, shipped the start date as the time from it to 31 December (one value per start day), and "
            "dropped the end date, the claim indicator and gender (used only to link a policy's records)."
        ),
        fit="approximate",
        fit_reason=(
            "The features are an insurer's rating factors, known when a period starts. But held-out policies of one "
            "year stand in for next year's; the amount spans every counted claim type (windscreen, at fault, not at "
            "fault, parking, fire-theft), its basis (paid or incurred) and valuation date not stated; and the sample "
            "cuts are undocumented."
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
        - 45 exact copies dropped (89 records share all 20 columns, their dates included, with another record; 10 of the copies within a file, 35 across files): a copy over this many columns is a collection artefact, not a second record (LEAK-18). Once the dates and `Gender` are dropped, 928 records repeat another record's features and target (20 of them in the same policy component, none with a claim; 610 with `Gender`), and 169 share the features with another target (130 with `Gender`): other policies with the same profile, history and start day, kept (LEAK-18); 0.56% to 0.68% of each test fold has its features in the training side on the shipped folds (0.35% to 0.48% with `Gender`, 0.39% to 0.46% before the component was widened on 2026-11-08, 0.1% to 0.2% with the length feature before 2026-11-06, 0.3% to 0.4% on the earlier chain folds).
        - 967 negative amounts (0.84% of the records, -1,948 to -2) set to 0. Every one has `ClaimInd` = 0, but they are claims of the period: of the 246 with a next record, 95.1% are followed by a rise of the not-at-fault claim counter (after 0.19% of the zero amounts and 18.6% of the positive ones), so they are not-at-fault claims whose recourse covered the payment, with no net claim cost to the period. They are -2.4% of the net claim cost. AIcrowd's pricing game of 2020-21 set negative totals to 0 on the 2017 game's portfolio.
        - `ClaimInd` dropped: the claim indicator of the same period, 1 exactly where the amount is positive (a part of the target).
        - `RecordEnd` dropped; `RecordBeg` ships only as `length_to_year_end` (below), a one-to-one recoding of the start date (366 values for the 366 start days). 31 December is the release's end, not a term of the policy: 48.4% of the records are still open there and 38.2% start on 1 January, the release's start, while the insurer prices a year of cover from the policy's anniversary, which the release does not give. `Exposure` is the record's realized length in years, (end - start) / 365 within 0.006, an open record ending on 31 December; the records open at the year end that start on the same day all have the same `Exposure`. The end of a record is not known when it starts, and the exact value of `Exposure` gave it away while it was a feature: its three decimals told a record that ended early from an open one at AUC 0.91 (0.61 once rounded to months).
        - Exposure (LEAK-41, MET-14, MET-15; issue 6, resolved 2026-11-06): `Exposure` is each record's time on risk, realized. Of the 115,155 records, 55,700 are open at 31 December, where the realized length is the length to the year end; 34,324 continue in the next record of their file (the contract changed); 25,131 end before 31 December without a continuation. Their end was not foreseen, and claims drive it: the records that ended alone hold 20.7% of the exposure but 38.9% of the claim cost (837 per exposure-year against 311 for open records) and 66 of the 109 largest claims. Some changes follow a claim too (a vehicle replaced): continued records cost 407 per exposure-year, though a change is often planned (the bonus-malus steps down at the change, as at an anniversary). The target is the claim amount per realized year, and `Exposure` is its denominator and each record's weight in the metric and in training (`sample_weight`), never a feature (LEAK-41). Every record has a positive length (0.001 to 1 year; at least one day between the dates), so the metric scores every row and no row goes (USE-7).
        - The length known at the start stays a feature (CLEAN-22, USE-6, LEAK-41; Lennart, 2026-11-08, review issue 7 (b)): `length_to_year_end`, the time from the record's start to 31 December in years, the `Exposure` the source gives the open records that start the same day (one value per start day, and every start day has some). It equals `Exposure` on the open records and bounds it on the others, so it is the part of the time on risk known at the start. It is the start day in another unit, and 31 December is the release's end, not a term of the policy. On the cost per year it adds little: +0.004 to a weighted Tweedie fit (SE 0.004, higher with it on 6 of 9 splits; +0.004 and +0.007 in two runs with `Gender` on the same folds), +0.002 to weighted squared error on the cost per year (SE 0.004, higher with it on 5 of 9; -0.003 and +0.002 with `Gender`); on the log1p scale, shipped until 2026-11-08, it misled squared error (the bullet on learners). It ships unrounded (Lennart, 2026-11-08, review issue 9 (B)): it depends on the start day alone, at the source's precision of three decimals, so its decimals carry no end; the rounding to whole months of 2026-11-02 hid the decimals of the realized length, which is no feature now. Rounded, 2,704 records would repeat the features and target of another record of their policy that starts 0 to 15 days apart (3,828 such repeats in all, against 928; 2,714 and 3,445 with `Gender`), and a weighted Tweedie fit would lose 0.004 (SE 0.0013, higher rounded on 1 of 9 splits; 0.003 and 0.005 in two runs with `Gender`), while squared error on the cost per year would not move (+0.000, SE 0.002, higher rounded on 5 of 9; -0.002 with `Gender`; on the folds of 2026-11-08).
        - The length feature before 2026-11-06 was `Exposure` itself, corrected where the data locates the cut (Andrej, 2026-11-02; the LEAK-10 case for time on risk cut short by the outcome): the 25,131 records that ended alone took the length known at their start, every length was rounded to whole months, and the 34,324 continued records kept their realized length, a potential leak kept on purpose. On the earlier folds by within-file chain the fix raised the row Gini from 0.281 to 0.332 and lowered the claim AUC from 0.689 to 0.673, both on 9 of 9 splits; the rounding cost nothing (0.330 and 0.673 with three decimals) and stopped the decimals from marking a record that continued (AUC 0.92 to 0.71). The kept part was worth about 0.045 under the metric of 2026-11-03 (0.254 against 0.209 with the length known at the start on every record, 7 of 9 splits; the exposure study of 2026-11-05). In place of `length_to_year_end` that hybrid now scores 0.005 lower with a weighted Tweedie fit (higher on 4 of 9 splits), 0.004 higher with weighted squared error on the cost per year (SE 0.009, higher on 6 of 9) and 0.045 lower with weighted squared error on log1p (higher on 4 of 9; on the folds of 2026-11-08, without `Gender`); LEAK-41 keeps it out whatever it scores, as a length corrected on some rows and realized on others. `exposure_at_start`, the base of the metric of 2026-11-03, is dropped.
        - The metric rewards any stand-in for the realized length (LEAK-41, probe 22): on the 9 shipped splits 1/`Exposure` alone scores 0.184 (0.134 to 0.264), as much as an honest model with a weighted Tweedie loss (0.182; 1/`Exposure` higher on 5 of 9 splits) and more than one with weighted squared error on the cost per year (0.153; 8 of 9); `Exposure` added as a feature lifts the Tweedie model to 0.254 (+0.072) and the squared-error one to 0.228 (+0.076, 9 of 9 each), so 1/`Exposure` alone does not bound what a stand-in used with the features would reach. With the target and base of 2026-11-03, 1/length scored 0.184 against 0.176 for an honest model (the exposure study). Probe 22: the features predict `Exposure` at R^2 0.34, 86% of the gain from `length_to_year_end`, known at the start, which gains nothing through `Exposure` (-0.051 with a weighted Tweedie fit, SD 0.035; -0.049 with L2 on the cost per year, SD 0.065; on the folds of 2026-11-08, without `Gender`; USE-6). The length to 31 December alone scores 0.006 and the weighted constant 0; the models beat the length alone on 9 of 9 splits by at least 0.088 (TP-4).
        - Learners differ by loss (CLEAN-16 as amended). The cost per year ships on the identity scale (Lennart, 2026-11-08, review issue 7 (b)), where a weighted squared-error fit estimates the cost per year that breaks even, the quantity the Gini orders by, which the length to 31 December does not move: across its bands the cost per realized year stays at 394 to 469 and the claims per realized year at 0.20 to 0.22. That fit scores 0.153, 0.029 below a weighted Tweedie fit (0.182; SE 0.004, lower on 9 of 9 splits), led by the tail (up to 11.6 million per year, 58,087 on a record of under two days; the 15,303 records shorter than a month hold 4.3% of the claim cost). On the log1p scale, shipped until then, a weighted squared-error fit estimates the exposure-weighted mean of log1p(cost per year) instead, and that mean rises with the time to 31 December (0.29 up to 3 months, 0.98 to 1.08 from 9 months on, weighted by the realized length): a short period's cost per year is large when it has a claim, but a claim is rarer. So that fit ranks short periods too low when it sees `length_to_year_end`: 0.154 with the feature and 0.187 without (lower with it on 9 of 9). Ignoring the weight costs the Tweedie fit 0.025 and squared error on the cost per year 0.060 (lower on 9 of 9 each). Untuned LightGBM with the exposure study's settings, 3 seeds per split, on the folds of 2026-11-08 with the target on the identity scale and without `Gender` (the container orders its rows by their content, so each change of the target or the columns reorders the rows: each score moved by up to 0.005 from the run on log1p, and by up to 0.004 from the run with `Gender`). The benchmark records each learner's loss.
        - Models are compared by their paired differences per fold, not by their mean scores alone (TP-2, EV-2): random orders spread with a per-fold SD of 0.035 (0.017 to 0.063; 100 per fold), and the large claims decide the fold that holds the largest, 802,620: with each loss capped at 50,000 in scoring, a weighted Tweedie fit on fold 1 of the first repeat drops from 0.238 to 0.163, the fold that holds that claim in each repeat by 0.021 to 0.075, the other six folds by 0.008 at most (on the folds of 2026-11-08, without `Gender`; with it 0.233 to 0.157, 0.016 to 0.076 and 0.011; about 0.06 on the folds of the review panel of 2026-11-06). The scores keep every loss uncapped.
        - Potential leak, kept on purpose (LEAK-9, an evaluation leak): the folds keep a policy's records together, so a test record's later records are test rows too (34,324 records continue in the next row of their file, 10,292 more only in another file, and about 3,200 more with one profile column changed, in the component since 2026-11-08). A later record's start gives the earlier record's realized length, and its claim counters tell the earlier record's claim: a continued record had a claim in 88.9% of the cases where the next record's counters rose and in 1.1% of the others. A model that reads a test record's later records gains +0.26 to +0.44 depending on what it reads, 0.44 to 0.64 against honest scores of 0.17 to 0.20 (9 of 9 splits each): on the widened folds of 2026-11-08, +0.257 with the next record of the file as an oracle (0.439 against 0.182 with a weighted Tweedie fit; +0.244 with squared error on the cost per year, 0.397 against 0.153; without `Gender`) and +0.355 with the in-component successor's counter rise and start; on the folds of 2026-11-06 (the review panel), +0.285 with the next record's counter rise and start, +0.387 with a successor rebuilt from the test rows and +0.437 with `Exposure` among the inputs as well. The successor is found without `policy_component`, from the features and `Exposure`: the next record's `length_to_year_end` is the record's own minus its `Exposure`, and its `LicAge` (in months) the record's own plus 12 times its `Exposure`, which links 39% of the records, 99.7% of the links within one component. Each test record is predicted from the training rows and its own features only; no feature or model step may use other test rows, and a method that reads a test record's later records is called out and not benchmarked (LEAK-9 as amended 2026-11-05, as for fremtpl2 and medical_facility_operational_data). The line also covers the later records whose contract change changed one profile column, test rows since the component was widened (review issue 8).
        - Policy components, the group column `policy_component` (never a feature; Andrej, 2026-11-03, review issue 1: B, the most conservative key; widened by Lennart, 2026-11-08, review issue 8: B): a policy whose contract changed in 2004 has several records. 34,324 records (30%) continue in the next row of their file (the same profile, starting the day the record ends, the driver's age the same or one more; 1 such link by chance with the rows shuffled), and 10,292 more continue only in another sample file (the same profile and dates, the licence age advanced by the months between the starts within one). A contract change can also change one profile column (the risk area, the km limit, the vehicle use, the socio-professional category or the marital status), so a record also continues one that ends the day it starts with the same gender, the driver's age the same or one more, the licence age advanced as above, exactly one of the other five profile columns changed and no claim or out-of-use counter lower: 9,160 such pairs over 7,120 earlier records, about 3,200 of them true links (the later record's counters rise after 75.5% of the earlier record's claims and after 41.9% of its other records, while the same search with the end date shifted by one or two months, or with two or more columns changed, shows no such contrast; the review panel of 2026-11-06). Every record joined to another by any of these links is in one component: 61,091 components of 1 to 90 records, 90,373 records in components of two or more. A later record's claim counters include the earlier record's claim, so in the training side it would tell a test record's claim; the folds keep each component on one side (SPLIT-9). With the one-column successors in other components, a lookup of a test record's candidate successors in training lifted a weighted Tweedie fit from 0.174 to 0.195 (+0.020, 9 of 9 splits); on the widened folds no such pair crosses a split, and the same lookup gains +0.001 (SD 0.012, higher on 5 of 9). About 1% of the same-profile links across files and about two thirds of the one-column links match by chance; a chance link only puts two policies in one group, which makes the split stricter (SPLIT-24, exactness weighed against coverage).
        - The claim counts are taken at each record's start: at least one rises at the next record after 95% of the claims and after 2.3% of the other records, so they hold the history known when the record starts and never its own claim.
        - Target `claim_amount_per_year`, `ClaimAmount` ("Total claim amount of the guarantee") over `Exposure`: the claim cost per year of cover (MET-14), untransformed. `ClaimAmount` leaves the frame as a part of the target, and `_clean` checks that the target times `Exposure` gives it back. The identity scale since 2026-11-08 (Lennart, review issue 7 (b); log1p until then): a log-scale rate with `length_to_year_end` as a feature misleads squared-error fits, and of CLEAN-16's two remedies, dropping the feature or the identity scale, only the identity scale also meets LEAK-41's sentence that the part of the time on risk known at the start ships as its own column; what a weighted fit on it estimates is in the bullet on learners. The metric scores the cost per year as shipped (MET-3). 90.6% of the records are 0: no claim, or a not-at-fault claim whose recourse covered the payment (89.7% as published, plus the 0.84% negative amounts set to 0). Only the claim part carries signal: on the three shipped folds of the first repeat a claim model ranks claims at AUC 0.67, but a severity model scores R^2 -0.20 to -0.01 on the claimants (-0.02 to -0.01 on log amounts), and even the true claim indicator times the claimants' mean explains only 2% to 15% of the variance of the amount. Which guarantee the amount covers is not named, but the counter that rises after a claim shows every counted type: of the 2,361 claims followed by exactly one counter rise, 40% raise the windscreen counter, 28% the at-fault one, 17% the not-at-fault one, 9% parking and 6% fire-theft. Whether the amounts are paid or incurred, and when they were valued, is not stated.
        - Dtypes: `MariStat`, `SocioCateg` (the union of the five files' codes, 46 CSP codes, 23 of them with fewer than 10 records), `VehUsage` and the yes/no flag `HasKmLimit` categorical; `RiskArea` stays a number, as shipped (the source: "Unknown risk area between 1 and 13, possibly ordered"); ages, counts, `BonusMalus` and `length_to_year_end` (in years) numeric; `Exposure` is the weight scoring column, never a feature; `Gender` is no feature (below).
        - Anomaly: the largest claim, 802,620, is 3.6% of all claim cost (the next is 163,427); the ten largest are 7.6%. Kept as recorded.
        - Anomaly: 47 records imply a licence before the age of 17 (`DrivAge` in whole years minus `LicAge` in months below 17 years); the dates both ages refer to are not documented, so they stay as recorded.
        - Dropped: `Gender`, the driver's gender (Male 71,816 records, Female 43,339), a rating factor in 2004. Sex leaves the rating factors of every insurance pricing task of this collection, whatever the actor's jurisdiction or the data's year, as EU law has required for new contracts since 21 December 2012 (Test-Achats, CJEU C-236/09, 1 March 2011): the benchmark asks how good such models would be in today's European market, where they may not use sex (the Tensions row on rating factors in principles.md, amended 2026-11-08; CC below). A French insurer pricing today is in that market, so here the stance and the law agree. `Gender` still builds the policy component, since a policy's records share it (`_clean`, step 5), and leaves the frame after it (step 8): the same 61,091 components, and every split holds the same test records; the rows changed order, as the container orders them by their content. It carried nothing measurable: with it a weighted Tweedie fit scores 0.0004 lower (0.1815 against 0.1819, SE 0.002, higher with it on 5 of 9 splits) and weighted squared error on the cost per year 0.0008 lower (0.1519 against 0.1527, SE 0.002, 5 of 9; untuned LightGBM, 3 seeds, the shipped folds). The cost per exposure-year is 434 for women and 450 for men, and 9.4% of the records of each have a claim. The scores of these notes, the metric reason and the splits comment are re-measured without it, except the lookups of a test record's successors (+0.001 and +0.355, and the honest 0.170 in the split auditor's settings, measured with it on the same folds; +0.020 on the folds before) and the runs named by an earlier date.
        - CC (2026-11-06, Lennart): issue 6 resolved by D9 of the exposure study (https://github.com/TabArena/data-foundry/issues/51): the target is the claim amount per realized year on the log1p scale (CLEAN-16 as amended: a rate scored by a Gini keeps the curator's scale); `Exposure`, the realized length, is the weight of the metric and of training and never a feature (LEAK-41, MET-14, MET-15); the length to 31 December stays a feature (CLEAN-22, USE-6); `exposure_at_start` is dropped; the metric is `ordered_lorenz_gini` per unit of `Exposure`, Andrej's unnormalised CAS form, now on the rate. Supersedes Andrej's call of 2026-11-03 (issue 4: option C, the length known at the start as the base, chosen over option B, the realized base, under which a constant prediction scored 0.184): under the rate a constant scores 0, whereas option B scored totals against a realized base; LEAK-41 now guards against 1/length, which alone scores 0.184 against 0.183 for the honest model.
        - CC (2026-11-08, Lennart): issue 8 resolved, "Widen the component": the policy component also joins a record to a successor whose contract change changed one profile column (the same gender, starting the day the record ends, the driver's age the same or one more, the licence age advanced by the months between the starts within one, exactly one of the other five profile columns changed and no claim or out-of-use counter lower): 61,091 components of 1 to 90 records. It widens the key of Andrej's call of 2026-11-03 (issue 1: B, the cross-file component on six equal profile columns, 68,857 components) in the direction of that call, the most conservative key, and closes a route SPLIT-9 forbids: a lookup of those successors in training gained +0.020 (9 of 9 splits), +0.001 on the widened folds (5 of 9). The scores in these notes and the metric reason are re-measured on the new folds.
        - CC (2026-11-08, Lennart): issue 7 resolved, "Identity scale, the length kept": the target ships as the claim amount per realized year, untransformed (`claim_amount_per_year`, no `target_transform`), and `length_to_year_end` stays a feature. It reverses the clause of D9 (issue 6, 2026-11-06) that kept the log1p scale: on log1p the length misleads a weighted squared-error fit, CLEAN-16 as amended then asks to drop the feature or ship the identity scale, and LEAK-41 ships the part of the time on risk known at the start as its own column, so only the identity scale meets both, as in pricing_game_2016_french_fleet (D11). D9's target, weight and metric stand.
        - CC (2026-11-08, Lennart): issue 9 resolved, B: the length to 31 December ships unrounded; it depends on the start day alone, so the month rounding of 2026-11-02 hides nothing, and rounded to months 2,714 records would repeat another record of their policy and a weighted Tweedie fit would lose 0.003 to 0.005. D9 and this call supersede Andrej's call of 2026-11-02 (issue 2 (a): the early ends given the length known at their start, the realized length kept on the 34,324 continued records, every length rounded to months), and D9 his call of 2026-11-03 (issue 4, option C: the length known at the start as the metric's base).
        - CC (2026-11-08, Lennart): `Gender` leaves the features, on the stance Lennart set in australian_vehicle_insurance_2004_2005's issue 7 ("A stance for the family; as if we were to simulate the case in europe always"): sex is no rating factor of any insurance pricing task of this collection, whatever the actor's jurisdiction, as under EU law (Test-Achats). It stays in the policy component's key, which is unchanged (61,091 components). Supersedes the note that kept `Gender` as the insurer recorded it, with the EU-law note (AI, /add-dataset, 2026-11-01), which shipped with Andrej's verdict of 2026-11-03. It carried nothing measurable (-0.0004 with a weighted Tweedie fit, -0.0008 with squared error on the cost per year, with it against without; 5 of 9 splits each).
    """
    accepted_check_warnings = {
        "task_target_value_dominant": (
            "Zero-inflated by nature: the claim amount per year is 0 for 90.6% of the records, those with no claim "
            "(89.7%) or with a not-at-fault claim whose recourse covered the payment (0.84%, negative amounts set to "
            "0); not a cap or a placeholder."
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
            "sorted by the predicted cost per year of cover, the cumulative share of the exposure against the "
            "cumulative share of the losses. The target is the cost per realized year and the realized length "
            "`Exposure` its weight (`per_unit`), so the curve is that form, not normalized as Andrej chose on "
            "2026-11-03 (review issue 4): 0 is the same cost per year for every record, which scores exactly 0, and "
            "random orders score -0.001 on average (per-fold SD 0.035). The metric rewards any stand-in for the "
            "realized length: 1/`Exposure` alone scores 0.184, as much as the honest model (0.182), and `Exposure` as "
            "a feature lifts the model to 0.254, so `Exposure` and every column that encodes it stay out of the "
            "features (LEAK-41; Lennart, 2026-11-06, review issue 6). On the 9 shipped splits untuned LightGBM "
            "weighted by `Exposure` scores 0.182 (0.147 to 0.245) with a Tweedie loss on the cost per year and 0.153 "
            "(0.108 to 0.228) with squared error on it, 0.029 lower, led by the tail of the rate over records as "
            "short as a day (3 seeds)."
        ),
        params={"per_unit": True},
        inputs={"weight": "Exposure"},
    )
    scoring_columns = (
        ScoringColumn(
            column="Exposure",
            role="weight",
            used_by="ordered_lorenz_gini",
            description=(
                "the record's realized length in years as published, (end - start) / 365 within 0.006 (0.001 to 1): "
                "shorter when the contract changed or ended during 2004, often after a claim. The claim amount per "
                "year's denominator; each record's weight in the metric and in training; never a feature"
            ),
        ),
    )
    sample_weight = "Exposure"
    grouping = Grouping(
        on="policy_component",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a policy component: a record and every record that may continue it, in the next row of its sample file or in another file, joined transitively. A record continues another when it starts the day the other ends, with the same gender (the source's `Gender`, read here and no feature), the driver's age the same or one year more and the licence age advanced by the months between the starts within one, and either the same six profile columns or exactly one of the other five changed (the risk area, the km limit, the vehicle use, the socio-professional category or the marital status, which a contract change can change) with no claim or out-of-use counter lower. 61,091 components of 1 to 90 records, 90,373 records in components of two or more. The release has no policy id. The use case prices a period when it starts: a later record of the policy does not exist yet, and its claim counters include the earlier record's claim, so all records of a component stay on one side (SPLIT-9). Each record is one prediction, made from its own row. About 1% of the same-profile links across files and about two thirds of the 9,160 one-column links match by chance; such a link only joins two policies into one group, the conservative side (SPLIT-24; Andrej, 2026-11-03: the most conservative key; Lennart, 2026-11-08: widened to the one-column links, review issue 8).
        """,
    )
    splits_comment = """
        Default splits, grouped by policy component (`policy_component`): a policy's records, in one sample file or
        across them, stay on one side (61,091 components for 115,155 records). A tariff is fit on past policy-years and applied to the
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
        against the chain 0.2785 against 0.2827 (before the fix); on the component folds of 2026-11-03 it scored a row
        Gini of 0.324 and a claim AUC of 0.668 (the total amount as target, before 2026-11-06). The component also
        joins the 10,292 records that continue only in another file, which the chains left apart; under the chains a
        lookup of such a record had ranked claims at AUC 0.51. Since 2026-11-08 (Lennart, review issue 8) it also
        joins a record to a successor whose contract change changed one profile column (61,091 components, 68,857
        before): with those successors in other components, a lookup of a test record's candidate successors in
        training lifted a weighted Tweedie fit from 0.174 to 0.195 (+0.020, 9 of 9 splits; untuned LightGBM, 300
        trees, one seed); on the shipped folds none of the 9,160 such pairs crosses a split, the lookup gains +0.001
        (SD 0.012, higher on 5 of 9), and the honest fit scores 0.170 (0.132 to 0.243), against 0.174 on the folds
        before, an unpaired comparison inside the fold SD of about 0.03.
        Shipped forced on the curator's call (Andrej, 2026-11-02: "Forced group splits should be fine"). The leak test
        across the split (SPLIT-8, 2026-11-02, on the chain folds) finds none, and the leak probe on the component
        folds flags nothing (2026-11-03): the 0.37% of test rows whose features were in training agree on a claim less than the base rate (84%
        against 91%), and the training side's mean outcome of the test row's start month (and risk area by month) moves
        the Gini by -0.0005 on average; dropping the test rows' own quarter from training costs no more than dropping as
        many random rows. Re-run on 2026-11-06 with the claim cost per year, it flags nothing: no feature alone above an
        R^2 of 0.003, and the 0.42% of test rows with an exact feature copy in training agree with it as often as two
        random records do (82%). Re-run on the widened folds of 2026-11-08, it flags nothing: no feature alone above
        an R^2 of 0.002, and 0.4% of test rows with an exact feature copy in training (0.3% with the same label only);
        the group probe finds no gap between random and grouped folds (R^2 0.005 both), both on the log1p scale. With
        the cost per year on the identity scale (2026-11-08, review issue 7) the leak probe flags nothing either: no
        feature alone above an R^2 of 0, and the same 0.4% of test rows with an exact feature copy in training; without
        `Gender` (2026-11-08, the same folds) it flags nothing, no feature alone above an R^2 of 0, and 0.6% of test
        rows with an exact feature copy in training (0.5% with the same label only). Each test record is predicted
        from the training rows and its own features only; no feature or model step may use other test rows: a test
        record's later records are test rows too, those whose contract change changed one profile column included,
        and their start and claim counters give its realized length and its claim (LEAK-9; the curation notes).
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
        #    of its file or in another file (issue 1, B), also where the contract change changed one profile column
        #    (issue 8, B).
        link = _continues_next(df)
        df["policy_component"] = _policy_components(df, link)
        # 6. The length to 31 December, known at every record's start: the Exposure the source gives the open records
        #    that start the same day (one value per start day, and every start day has some). A feature, unrounded;
        #    the realized Exposure is not (issue 6).
        to_year_end = df["Exposure"].where(df["RecordEnd"].isna()).groupby(start).transform("median")
        assert to_year_end.notna().all()
        assert (to_year_end >= df["Exposure"]).all()
        df["length_to_year_end"] = to_year_end
        # 7. The target: the claim amount per realized year, untransformed (issue 7, b). Exposure, the realized length,
        #    cut short when the contract changed or ended, stays only as the rate's denominator and the weight scoring
        #    column, never a feature (LEAK-41, MET-14, MET-15). Every record has one (USE-7: none to drop).
        assert (df["Exposure"] > 0).all()
        df[TARGET] = df["ClaimAmount"] / df["Exposure"]
        assert np.allclose(df[TARGET] * df["Exposure"], df["ClaimAmount"], rtol=1e-9, atol=1e-6)
        df = drop_columns(df, ["ClaimInd", "ClaimAmount", "RecordBeg", "RecordEnd", "file"])
        # 8. Sex is no rating factor of an insurance pricing task in this collection, whatever the actor's
        #    jurisdiction, as under EU law (Test-Achats; notes). `Gender` built the policy component (step 5) and
        #    leaves the features after it.
        return drop_columns(df, ["Gender"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["MariStat", "SocioCateg", "VehUsage", "HasKmLimit"])

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
        claims.index = claims.index.astype(str).rename("realized Exposure (years)")
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
        size = pd.Series(_policy_components(records, link)).value_counts()
        bands = ["1", "2", "3", "4", "5", "6-10", "11-20", "21-50", "51-100"]
        band = pd.cut(size, [0, 1, 2, 3, 4, 5, 10, 20, 50, 100], labels=bands)
        sizes = (
            size.groupby(band, observed=False)
            .agg(components="size", records="sum")
            .rename_axis("records in the component")
        )
        return [
            Decision(
                "The realized length weights the claim cost per year and is no feature",
                "A record ends at the end of 2004 or when the contract changes or ends; the end is not known when "
                "the record starts, and records that ended with no continuation in their file had more claims than "
                "open ones of the same realized length. So the target is the claim amount per realized year, the "
                "realized `Exposure` is each record's weight in the metric and in training and never a feature, and "
                "every record takes as a feature the length known at its start, the `Exposure` of the open records "
                "that start the same day (issue 6).",
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
                "also the licence age advanced by the months between the starts). A contract change can also change "
                "one profile column, so a record with the same gender, dates and ages, exactly one of the other five "
                "profile columns changed and no counter lower continues it too (9,160 such pairs, about 3,200 of them "
                "true links). A later record's claim counters include the earlier record's claim: under random "
                "records, a lookup on the features alone lifted a LightGBM model's normalized Gini by 0.09 on the "
                "same test rows, and with the one-column successors in other groups a lookup of them in training "
                "lifted the Gini by 0.020 (9 of 9 splits). Every record joined by such a link is in one group "
                "(`policy_component`), the most conservative key (Andrej, 2026-11-03; widened by Lennart, "
                "2026-11-08).",
                sizes,
            ),
        ]
