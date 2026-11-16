"""Curated dataset definition for `ny_wcb_assembled_claims_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import csv
from pathlib import Path

import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    RowBudget,
    TaskSummary,
    Temporal,
    TemporalSplits,
    drop_columns,
    set_missing,
)

CHUNKS = tuple(f"claims_id_{start:07d}.csv" for start in range(0, 8_000_000, 1_000_000))
"""The table as downloaded: 8 chunks of the Socrata API by claim identifier (see `download_description`)."""

PREPARED = "claims.parquet"
"""The 8 chunks in one parquet file, every column as text (`_prepare_raw_files`)."""

HISTORY_START = pd.Timestamp("2016-01-01")
"""The first assembly date kept: the class mix of the assembled claims settles after the EDI ramp of 2014-2015."""

RELEASE_CUT = pd.Timestamp("2020-01-01")
"""The first assembly date left out: later claims have had under 6.7 years to reach their benefit type."""

TARGET_LEVELS = ["NON-COMP", "MED ONLY", "TEMPORARY", "PPD SCH LOSS", "PPD NSL", "PTD", "DEATH"]
"""The codebook's benefit types from least to most severe, without `1. CANCELLED` (rows dropped)."""

DATE_COLUMNS = ["assembly_date", "c2_date", "c3_date"]
"""The dates kept; the other date columns are dropped as text."""

POST_ASSEMBLY = [
    # Dates and counts of the Board's process after assembly (codebook; none falls on or before the assembly date).
    "ancr_date",
    "interval_assembled_to_ancr",
    "controverted_date",
    "first_hearing_date",
    "first_appeal_date",
    "section_32_date",
    "hearing_count",
    "ime4_count",
    "closed_count",
    "current_claim_status",
    "highest_process",
    # The award itself: the dates the claim was classified PPD or PTD restate classes 4 to 6 of the target.
    "ppd_scheduled_loss_date",
    "ppd_non_scheduled_loss_date",
    "ptd_date",
    # Established through the Board's adjudication: positive for 0.2% of NON-COMP claims, 91% to 100% of the awarded.
    "average_weekly_wage",
    # The claim's representation now, no date: changed for 28% of claims between weeks and five years after assembly.
    "atty_rep_ind",
    # "As determined by the WCB": an occupational disease (or no accident) holds 0 NON-COMP claims of 11,389.
    "accident_ind",
    "occupational_disease_ind",
    # OIICS codes were assigned when a claim reached ANCR (FAQ 7), and are blank in the EDI years kept here.
    "oiics_event_exposure_code",
    "oiics_event_exposure_desc",
    "oiics_injury_source_code",
    "oiics_injury_source_desc",
    "oiics_nature_injury_code",
    "oiics_nature_injury_desc",
    "oiics_pob_code",
    "oiics_pob_desc",
    "oiics_secondary_source_code",
    "oiics_secondary_source_desc",
]

LATE_VALUES = [
    # Stored at their latest value, filled or changed after assembly on claims that grew, with a traced gain (notes).
    # The injury: WCIO cause, nature and part of body, code and description.
    "wcio_cause_of_injury_code",
    "wcio_cause_of_injury_desc",
    "wcio_nature_of_injury_code",
    "wcio_nature_of_injury_desc",
    "wcio_pob_code",
    "wcio_pob_desc",
    # The employer's industry (NAICS sector).
    "industry_code",
    "industry_desc",
    # The worker: the age (computed from the birth date, FAQ 6) with the birth year, the accident date, the home ZIP.
    "age_at_injury",
    "birth_year",
    "accident_date",
    "zip_code",
    # The medical fee region (mapped from the home ZIP) and the Board's district office.
    "medical_fee_region",
    "district_name",
    # The insurer: blanks filled, transfers to the special funds (FAQ 11), spellings rewritten on active claims.
    "carrier_name",
    "carrier_type",
]


class NyWcbAssembledClaims1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "When New York's Workers' Compensation Board opens a claim, which benefits will it end up awarding: none, "
            "medical care only, temporary lost-wage benefits, a permanent partial or total disability award, or "
            "death benefits?"
        ),
        use_case=(
            "When the Board assembles a claim, the insurer's lost-time desk routes it: a fast track for claims likely "
            "to end without lost-time benefits, an adjuster and early case management for claims likely to become "
            "permanent ones. The source names no prediction; the use case is ours."
        ),
        row=(
            "One workers' compensation claim assembled by the Board from 2016 to 2019, without claims cancelled as "
            "duplicates, claims adjudicated outside the Board and Paid Family Leave claims."
        ),
        predicted=(
            "The claim's benefit type as recorded in September 2026, at least 6.7 years after assembly: one of seven "
            "classes from no indemnity (65%) to death benefits (0.05%)."
        ),
        known=(
            "The claim type, the county where the injury happened, the worker's sex, the assembly date, and the "
            "dates the employer's report and the worker's claim form arrived, when they arrived by assembly."
        ),
        split=(
            "Each test window is four months of 2019 (newest first); training is up to a random million earlier "
            "claims from 2016 on, as for a model refit three times a year."
        ),
        changes=(
            "We drop every field the Board sets after assembly (hearings, decisions, the wage it establishes, the "
            "attorney flag) and every field stored at a value filled or changed later: the injury, the employer's "
            "industry, the insurer, the worker's age, accident date and home ZIP, the fee region and the district. "
            "The form dates count only when they precede assembly, and the claims run from 2016 to 2019."
        ),
        fit="approximate",
        fit_reason=(
            "The desk holds inputs that the table lacks (why the claim was assembled, the reported wage and lost "
            "time, the insurer's denial, the occupation, the narrative); the label is the benefit type to date; and "
            "the task was changed a lot to avoid a leak (the injury, insurer, age and ZIP dropped). Kept, not a gap: "
            "the remaining fields are also 2026 values, and their traced part shows no gain."
        ),
    )

    # Dataset
    unique_name = "ny_wcb_assembled_claims_1m"
    version_of = "ny_wcb_assembled_claims"
    version_comment = """
        We use the three four-month windows of 2019 as test windows. We sample per test window (v2 split protocol): each window keeps at most 500k of its rows, and its train side is a random 1M of all earlier rows from 2016 on (all of them when fewer), drawn in one random order for all windows; the frame keeps only the rows a split uses. Random rather than recent training rows keep every year of the EDI era in the training data, as for the other `_1m` versions (TabReD).
    """
    year = "2026"  # the snapshot we pin (rows updated 2026-09-21); the table is reposted quarterly
    domain = "insurance"
    source = "GOV Website"
    source_url = "https://data.ny.gov/d/jshw-gkgu"
    license = "OPEN-NY Terms of Use (data.ny.gov); no licence named on the dataset page"
    data_tags = ("Spatial",)
    download_description = """
        The table is live and reposted quarterly; we pin the state of 2026-11-08 (rows updated 2026-09-21,
        5,655,563 claims). The bulk export (https://data.ny.gov/api/views/jshw-gkgu/rows.csv?accessType=DOWNLOAD)
        broke off at about 1.4 GB, so we read the Socrata API in 8 chunks of claim identifiers:

        mkdir -p local-data-warehouse/ny_wcb_assembled_claims && cd local-data-warehouse/ny_wcb_assembled_claims
        for b in 0 1000000 2000000 3000000 4000000 5000000 6000000 7000000; do
            curl -sS --fail -o claims_id_$(printf %07d $b).csv "https://data.ny.gov/resource/jshw-gkgu.csv?\\$limit=2000000&\\$order=claim_identifier&\\$where=claim_identifier%3E=$b%20AND%20claim_identifier%3C$((b+1000000))"
        done

        The overview and the data dictionary (the codebook) are the two attachments of the dataset page.
        A later download gives a newer snapshot: newer benefit types for the same claims, and newer field values.
    """
    bibtex = r"""
        @misc{nyswcb2026AssembledClaims,
          author       = {{New York State Workers' Compensation Board}},
          title        = {Assembled Workers' Compensation Claims: Beginning 2000},
          year         = {2026},
          howpublished = {\url{https://data.ny.gov/d/jshw-gkgu}},
          note         = {Open NY dataset jshw-gkgu, rows updated 2026-09-21. Accessed: 2026-11-08},
        }
    """
    curation_comments = """
        We start with the 5,655,563 claims of the Open NY table "Assembled Workers' Compensation Claims: Beginning 2000" (54 columns, read through the Socrata API on 2026-11-08), with its data dictionary and overview (FAQ).

        - Prediction point: the claim's assembly date, when the Board "learns of a workplace injury and assigns the claim a Board case number" (overview) and the insurer's lost-time desk routes the claim. A field is kept only if it holds what was known then. The desk also holds inputs the table does not publish: the reason for assembly (more than a week of lost time, a serious injury, a dispute, a C-3), the employer-reported wage and lost time, the insurer's own denial, the occupation, the injury narrative, the first medical report (C-4) and an attorney at assembly.
        - Label maturity (LEAK-24): the target is the benefit type "as of the date the data set was created" (FAQ 4). Comparing the same claims in a June 2021 copy of the table (Kaggle, new-york-state/nys-assembled-workers'-compensation-claims) with our 2026 snapshot, the type changed later for 36% of 2021 claims, 8.2% of 2019 claims, 2.6% of 2017 claims and 0.9% of 2014 claims. We cut the release at assembly 2020-01-01, so the newest claims (2019) have had at least 6.7 years; this also leaves out the COVID-19 claims of 2020 to 2022. The labels are not final: at that age the 2014 claims still lacked 12% of their 2026 PPD NSL and 13% of their PTD awards, so about that share of the test windows' eventual PPD NSL and PTD awards is still to come (3-7% for the training years), and PPD SCH LOSS is about 0.25 points lower in 2019Q4 than in the quarters before.
        - History (SPLIT-20): we start at assembly 2016-01-01. EDI filing became mandatory on 2014-04-23 (overview); the Board then assembled more claims (174k in 2013, 259k in 2014, 282k in 2015), and the mix of what it assembled moved through 2015 (NON-COMP 45.0% in 2015Q1 and 61.3% in 2015Q4, MED ONLY 22.2% and 10.4%) before it held from 2016 (NON-COMP 63.7-65.6% and MED ONLY 7.5-8.7% in every quarter to 2019).
        - We drop the CANCELLED claims ("assembled in error or determined to be a duplicate", 1.5% of 2016-2019): no outcome of an injury (USE-5).
        - We drop the claims under alternative dispute resolution ("adjudication processes external to the Board", 10,678 claims, 0.9%): 99.96% of them are NON-COMP because the Board awards nothing on them, so their label is not the claim's benefit (LEAK-25: located by the flag, which changed for 2 of 3,055 claims after assembly). The flag is then N for all but 78 rows (U) and is dropped.
        - We drop the Paid Family Leave claims (PFL Discrimination, PFL No Insurance; 190 claims): not injuries.
        - Dropped as set after assembly (LEAK-10; the list `POST_ASSEMBLY` in the code): the ANCR, controverted, hearing, appeal and Section 32 dates and the interval to ANCR (none on or before the assembly date), the hearing, IME-4 and closed counts, the current status and the highest process; the PPD and PTD dates (they restate the target); the average weekly wage (established through the Board's adjudication, overview; positive for 0.2% of the NON-COMP and 38% of the MED ONLY claims, 78-100% of the other classes); the attorney flag (whether the claim is represented now, without a date: 14.0% of the represented claims are NON-COMP against 64.6% of all; it changed for 28% of the claims assembled 1-17 June 2021 between June 2021 and 2026); the accident and occupational-disease flags ("as determined by the WCB": no NON-COMP claim among the 11,389 occupational diseases); and the OIICS codes (assigned when a claim reached ANCR, FAQ 7; blank from 2016).
        - C-2 and C-3 dates: the employer's report (C-2) and the worker's claim form (C-3) are kept only when received on or before the assembly date (LEAK-7: the smallest fix); a later date is set to missing: 94,799 C-2 dates (8.2% of the claims) and 214,492 of the 341,344 C-3 dates. A C-3 that arrives after assembly marks a contested or growing claim (29% of those claims are NON-COMP against 64.6%), so the later dates would leak. Tables published from 2022 define the C-2 date as the earliest equivalent filing, eClaims included, and apply that definition to older claims too; the June 2021 copy used the old definition, so the C-2 date at assembly cannot be checked against it.
        - Dropped as stored after assembly (LEAK-10, values from a later pull; the list `LATE_VALUES` in the code): the table keeps no history, only each claim's latest values. On claims seen weeks after assembly, the injury codes, the industry, the age and the accident date were filled later mostly on claims that grew, the home ZIP and the insurer changed, and a field still blank in 2026 marks a claim that went nowhere (WCIO codes blank: 94% NON-COMP). Matched test on the 105,786 claims of January-June 2021 (same 2026 labels; train and test both on their June 2021 values or both on their 2026 values; LightGBM, 3 seeds): the 2026 values of all fields beat the June 2021 values by 0.030 to 0.037 log loss, a lower bound since the June 2021 values were already weeks old. Each dropped field carries part of it, above two standard errors in all three designs (over time, at equal age, at random): the three WCIO codes (+0.016 alone), the industry (+0.007 to +0.009), the age and the accident date together (+0.006 to +0.007; the birth year goes with the age) and the home ZIP (+0.006 to +0.011); the fee region (mapped from the ZIP) and the district (real moves for about 0.4% of claims) in two designs (+0.001 to +0.003 each). The 2,439 accident dates after assembly in 2016-2019 (85% occupational diseases; 84% of 3,039 in 2015-2019) are dates of disablement the Board set later (FAQ 5), not impossible values.
        - The insurer (carrier name and type) is dropped the same way, which leaves a thin task (an open question for the curator). The insurer exists at assembly, but the table holds what the claim's latest filing wrote: blanks filled for claims that progressed, transfers to the special funds after an award (FAQ 11), and spellings rewritten on claims with later filings (66,256 of the 73,382 name changes after June 2021, 31.9% NON-COMP against 64.6%). Traced gain: +0.004 to +0.007 for the name with its spellings merged, +0.002 to +0.004 for the type. On the 2019 windows (300k training claims, one seed) the kept fields score log loss 1.019, 1.022 and 1.041 against 1.055, 1.060 and 1.076 for the class shares, and 0.965 to 0.998 with the insurer.
        - Potential leak, kept on purpose (LEAK-10 as amended 2026-10-26: the late cells cannot be located row by row, and the traced part shows no gain): the claim type, the county, the sex, the C-2 and C-3 dates by assembly and the assembly date are their 2026 values too. On the matched claims their 2026 values beat their June 2021 values by +0.0006, +0.0003 and +0.0008 log loss (z 1.7, 0.3 and 1.9 in the three designs). The C-3 date is borderline: 131 C-3 dates on or before assembly first appeared after June 2021 (of the 105,786 matched claims; 19% NON-COMP, 31% PPD SCH LOSS), and swapping it alone shows z 1.3 to 3.3 by design and field set. The C-2 date cannot be traced (its 2022 definition). Revisit if the Board publishes an archive of the quarterly tables or the claims' first reports.
        - Missing values (CLEAN-10): gender U (6,479 claims) and the county UNKNOWN (3,381) are the codebook's unknowns, set to missing.
        - Codes and words (CLEAN-12): the claim type NON-WC (276 claims) is decoded as the codebook's World Trade Center volunteer claims (FAQ 8).
        - Dropped as identifiers or constants: the claim identifier; the COVID-19 indicator (N for every claim before 2020).
        - Note: sex (gender) stays a feature: no New York rule found bars it in claim handling. Insurance Law s2607 bars it in issuing, cancelling and renewing a policy, which here is the employer's; DFS Circular Letter 7 (2024) "is not intended to address phases of the insurance product lifecycle other than underwriting and pricing" (para. 8); Directive 2004/113/EC, which the collection's stance on sex in insurance pricing follows, excludes employment and occupation (Art. 3(4)). Without it the log loss of the kept fields rises by 0.0044, 0.0030 and 0.0035 on the three 2019 windows (SE 0.0003; LightGBM on 300k training claims, 3 seeds). An open question for the curator, decided with the stance on factors the actor's own law bars (rais_employment_separation).
        - Duplicates: 60.3% of the rows repeat an earlier row in every column, the label included, and 14.9% share all features with a row of another class: six coarse fields (one day, one county, one sex, one claim type, no form by assembly) cannot tell these claims apart. Kept: they are different claims, and no test row repeats a training row, as the assembly date differs.
        - Target: the codebook's classes without their rank number, as an ordered category from NON-COMP to DEATH (the codebook orders them "from least to most severe").
    """

    # Task
    target = "claim_injury_type"
    problem_type = "multiclass_classification"
    metric = Metric.fallback(
        reason=(
            "The Board publishes the table for analysis and defines no prediction task or metric (dataset page, "
            "overview, data dictionary). No competition or paper on this table defines one: searched the web and "
            "the Kaggle competitions for workers' compensation, WCB and claim injury type on 2026-10-31 and "
            "2026-11-08; a university course's Kaggle-in-class task on 2020-2022 claims scored macro F1 on hard "
            "labels, with no cost or threshold and on post-assembly fields, so it is not a source for this task."
        ),
    )

    # Splits
    temporal = Temporal(on="assembly_date", splits=TemporalSplits(window=4, unit="months", n_windows=3))
    row_budget = RowBudget(train=1_000_000, test=500_000)
    splits_comment = """
        Three test windows of four months, the whole of 2019 (September-December, May-August, January-April; newest first), each trained on the claims assembled from 2016-01-01 up to the window's start. The horizon is our choice: the Board posts the table quarterly and names no refit cadence or prediction; three windows are what a task of this size gets, and four months each cover 2019 once, every season in one window. The windows hold 97,676 to 101,201 claims (all of them are tested); the newest window trains on a random 1M of its 1,052,895 earlier claims, the other two on all of theirs (951,694 and 854,018), so the oldest window trains on 74% of the claims. No gap (SPLIT-10): every claim is in the data from its assembly whatever its outcome, so the newest training rows are not the fast ones, and no row is selected by its outcome. A refit at a window's start would not yet have known the final types of the newest training claims: an estimated 14.5-16.8% of each train side's labels changed after the window start (interpolated from the June 2021 copy by the claims' age at the window start; 12-14% while the history started in 2015, whose older claims had settled more). LightGBM trained on 18 months of claims that end k months before the window loses about 0.001 log loss per month of k (0.011 to 0.016 at 12 months; 2 seeds, history from 2015), smoothly and with no step at the window edge, so the newest labels give no shortcut to the test rows. A gap of a year would already leave the oldest window below half of the claims (48%), and the delay is longer.
    """

    prepared_raw_files = (PREPARED,)

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        import pyarrow as pa
        import pyarrow.csv as pacsv
        import pyarrow.parquet as pq

        tables = []
        for name in CHUNKS:
            with open(raw_dir / name, newline="") as handle:
                header = next(csv.reader(handle))
            # An empty unquoted field is a missing value (the API quotes every value it has).
            options = pacsv.ConvertOptions(column_types=dict.fromkeys(header, pa.string()), strings_can_be_null=True)
            tables.append(pacsv.read_csv(raw_dir / name, convert_options=options))
        pq.write_table(pa.concat_tables(tables), raw_dir / PREPARED)

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_parquet(raw_dir / PREPARED)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.copy()
        # 1. Dates: the API writes 2015-12-14T00:00:00.000.
        for col in DATE_COLUMNS:
            df[col] = pd.to_datetime(df[col].str.slice(0, 10), format="%Y-%m-%d")
        # 2. After the EDI ramp, up to the claims with at least 6.7 years to reach a benefit type.
        df = df[(df["assembly_date"] >= HISTORY_START) & (df["assembly_date"] < RELEASE_CUT)]
        # 3. Rows that are no outcome of an injury, or whose label the Board does not set.
        df = df[df[self.target] != "1. CANCELLED"]
        df = df[df["alternative_dispute_resolution"] != "Y"]
        df = df[~df["claim_type"].str.startswith("PFL")]
        # 4. Fields set after assembly, and fields stored at values filled or changed after assembly.
        df = drop_columns(df, [*POST_ASSEMBLY, *LATE_VALUES, "alternative_dispute_resolution"])
        # 5. The form dates only when they arrived by assembly.
        for col in ("c2_date", "c3_date"):
            df[col] = df[col].where(df[col] <= df["assembly_date"])
        # 6. Proxy missing values: the codebook's unknowns.
        df = set_missing(df, {"gender": ["U"], "injured_in_county_name": ["UNKNOWN"]})
        # 7. Codes and their words: Non-WC is the codebook's World Trade Center volunteer claim (FAQ 8).
        df["claim_type"] = df["claim_type"].replace({"NON-WC": "WORLD TRADE CENTER VOLUNTEER CLAIM (NON-WC)"})
        df = df.rename(columns={"injured_in_county_name": "county_of_injury"})
        # 8. The identifier and a constant.
        df = drop_columns(df, ["claim_identifier", "covid_19_indicator"])
        # 9. The target: the codebook's names without their rank number.
        df[self.target] = df[self.target].str.replace(r"^\d+\.\s*", "", regex=True)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=["claim_type", "county_of_injury", "gender"],
            datetime=DATE_COLUMNS,
            ordinal={self.target: TARGET_LEVELS},
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        year = raw["assembly_date"].str.slice(0, 4).astype(int)
        target = raw[self.target]
        by_year = pd.DataFrame(
            {
                "claims": year.value_counts().sort_index(kind="stable"),
                "NON-COMP": (target == "2. NON-COMP").groupby(year).mean(),
                "MED ONLY": (target == "3. MED ONLY").groupby(year).mean(),
                "PPD SCH LOSS": (target == "5. PPD SCH LOSS").groupby(year).mean(),
                "PPD NSL": (target == "6. PPD NSL").groupby(year).mean(),
                "WCIO codes filled": raw["wcio_nature_of_injury_code"].notna().groupby(year).mean(),
            }
        )
        by_year.index.name = "assembly year"
        window = (year >= HISTORY_START.year) & (year < RELEASE_CUT.year) & (target != "1. CANCELLED")
        rows = raw[window]
        assembled = pd.to_datetime(rows["assembly_date"].str.slice(0, 10))
        wage = pd.to_numeric(rows["average_weekly_wage"]).fillna(0) > 0
        c3_late = pd.to_datetime(rows["c3_date"].str.slice(0, 10)) > assembled
        flags = {
            "average weekly wage > 0": wage,
            "attorney/representative = Y": rows["atty_rep_ind"] == "Y",
            "occupational disease = Y": rows["occupational_disease_ind"] == "Y",
            "alternative dispute resolution = Y": rows["alternative_dispute_resolution"] == "Y",
            "C-3 received after assembly": c3_late,
        }
        shares = pd.DataFrame(
            {name: rows[self.target][flag].value_counts(normalize=True) for name, flag in flags.items()}
        ).T.fillna(0.0)
        shares = shares[sorted(shares.columns)]
        shares.insert(0, "claims", [int(flag.sum()) for flag in flags.values()])
        shares.loc[f"all claims ({HISTORY_START.year}-{RELEASE_CUT.year - 1}, without CANCELLED)"] = [
            len(rows),
            *rows[self.target].value_counts(normalize=True).reindex(shares.columns[1:], fill_value=0.0),
        ]
        shares.columns = [str(c).split(". ", 1)[-1] for c in shares.columns]
        shares.index.name = "claims with"
        return [
            Decision(
                "Claims assembled 2016-2019: after the EDI ramp, with at least 6.7 years to reach a benefit type",
                "The Board assembled more claims, and more of them without indemnity, once electronic filing began "
                "in 2014, and coded the injury in WCIO codes from then; the class mix still moved through 2015 "
                "(MED ONLY 16% against 8% from 2016), so we start in 2016. The benefit type is the one recorded in the "
                "2026 snapshot. Permanent awards are still being made years after assembly: in a June 2021 copy of "
                "the table the same 2014 claims had 88% of their 2026 PPD NSL awards, so we keep the claims with at "
                "least 6.7 years (assembled before 2020), which also leaves out the COVID-19 years; about 12% of the "
                "2019 claims' PPD NSL awards are still to come. The shares of the permanent classes fall visibly from "
                "the 2022 claims on.",
                by_year.round(4),
            ),
            Decision(
                "Fields the Board sets after assembly are dropped",
                "Each row is a field whose value depends on the claim's course, with the class shares of the claims "
                "that have it: the wage is established only for claims with lost time, the attorney flag is the "
                "claim's representation now, the occupational-disease flag is the Board's determination, claims "
                "under alternative dispute resolution get no Board award, and a claim form that arrives after "
                "assembly marks a contested claim. The first four are dropped (the dispute-resolution claims as "
                "rows), the C-3 date is kept only when it precedes assembly.",
                shares.round(4),
            ),
        ]
