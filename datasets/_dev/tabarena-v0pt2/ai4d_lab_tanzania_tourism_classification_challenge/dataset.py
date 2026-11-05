"""Curated Tanzania tourism expenditure classification; evidence is in README.md."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, Metric, TaskSummary, drop_columns


class Ai4dLabTanzaniaTourismClassificationChallenge(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Which spending category applies to a visitor's specified Tanzania trip?",
        use_case=(
            "A tour operator or the Tanzania Tourism Board uses historical visitor and trip records to estimate the "
            "spending category for a specified alternative trip plan, conditional on the trip happening as specified. "
            "The survey's own users, the National Bureau of Statistics and the Bank of Tanzania, fill in a departing "
            "respondent's spending band from the rest of the exit form when the expenditure answer is missing or "
            "implausible."
        ),
        row="One labeled tourist survey record in the 2022 competition's training file (18,506 records).",
        predicted=(
            "The original cost_category, ordered Lower Cost < Low Cost < Normal Cost < High Cost < Higher Cost < "
            "Highest Cost. "
            "The bands are not published; linked to a 2020 copy of the same survey, they cut the party's total trip "
            "spending at about 0.5M, 1M, 5M, 10M and 50M Tanzanian shillings (approximate edges)."
        ),
        known=(
            "Visitor country, age group and first-trip status; travel party, purpose, activity, information source, "
            "tour arrangement, package inclusions and nights on the mainland and Zanzibar. For the statistician these "
            "are the completed exit form at departure; for the planner the realized trip stands in for the plan."
        ),
        split=(
            "Held-out visitor/trip records from the represented survey population, using stratified random folds. "
            "This does not test future seasons, unsupported itineraries or causal effects of changing a plan."
        ),
        changes=(
            "We drop the opaque tourist identifier, merge the Widlife Tourism spelling into Wildlife Tourism, "
            "merge UAE and BURGARIA into their existing country categories, and make both party counts missing when "
            "their recorded sum is zero. Original labels and rows stay."
        ),
        fit="approximate",
        fit_reason=(
            "The statistician's task is mirrored: every input is on the form at departure, and the random folds test "
            "other respondents of the same survey. For the planner the observed trip stands in for a plan assumed "
            "fulfilled, and an operator quotes from a rate card, so a band guess changes little. Six bands are coarser "
            "than the amount either needs, with reconstructed edges. No survey year or respondent/party linkage."
        ),
    )

    unique_name = "ai4d_lab_tanzania_tourism_classification_challenge"
    year = "2022"
    domain = "business & marketing"
    source = "Zindi"
    source_url = "https://zindi.africa/competitions/ai4d-lab-tanzania-tourism-classification-challenge"
    license = "CC BY-SA 4.0; publisher also states non-commercial research or education use (competition rules)."
    download_description = """
        We use Train.csv from the original 2022 classification task. The curator-provided official Zindi
        archive passed its ZIP CRC check, and all four extracted files match the retained competition bytes
        and SHA-256 hashes. Independent authenticated retrieval is not claimed. Public copies provide an
        additional reproduction route. The immutable public commit below recreates the exact training input.

        python - <<'PY'
        import hashlib, pathlib, urllib.request
        url = "https://raw.githubusercontent.com/dylannguyen2809/ai4d/3c3a6f155e24115fb67ec469d2335e1ef718c178/data/Train.csv"
        data = urllib.request.urlopen(url).read()
        assert len(data) == 3147987
        assert hashlib.sha256(data).hexdigest() == "1a71082258df9f998f14691170080674b719a347a0ad2c0862dd5e7a5e83899f"
        path = pathlib.Path("local-data-warehouse/ai4d_lab_tanzania_tourism_classification_challenge/Train.csv")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        PY
    """
    bibtex = r"""
        @misc{Zindi2022TanzaniaTourismClassification,
          author = {{AI4D Africa's Anglophone Research Lab} and {Zindi}},
          title = {Tanzania Tourism Classification Challenge},
          year = {2022},
          howpublished = {\url{https://zindi.africa/competitions/ai4d-lab-tanzania-tourism-classification-challenge}},
          note = {Tourist expenditure survey attributed by the publisher to Tanzania's National Bureau of Statistics}
        }
    """
    curation_comments = """
        We start with the 18,506 labeled rows in Train.csv; the 6,169 unlabeled Test.csv rows are not training labels.

        - CC (2026-11-05, Lennart): the survey statistician joins the trip planner as actor (issue 3, option B; USE-9): NBS and the Bank of Tanzania, who estimate tourism earnings from the exit survey, fill in a respondent's spending band from the rest of the form when the expenditure answer is missing or implausible. That actor has every input at departure, and its test is other respondents of the same survey, which the random folds measure. The planner stays, so the use case still looks forward and the `ForcedIIDFromTemporal` tag stays (SPLIT-8); the fit stays approximate (six bands, USE-5).
        - CC (2026-11-05, Lennart): the scorer reads probability columns in the sorted order of the class labels (scikit-learn's classes_) and checks named columns; the ordered categories stay metadata (issue 5, C; MET-2).
        - Prediction point: a visitor supplies visitor context and a proposed trip plan, assumed to occur as specified.
          Nights, activity, party and package attributes are scenario inputs even though recorded in an exit survey.
          package_food denotes package inclusion, not meal consumption. cost_category stays target-only.
        - Keep all six source classes and source Log Loss (MET-4). The release does not state the label's basis; the
          2020 cut of the same survey ships total_cost ("The total tourist expenditure in TZS"). On 2,401 rows that
          link uniquely to it, cuts of the party's total cost at 0.5M / 1M / 5M / 10M / 50M TZS reproduce the class
          for 97.9% (the same cuts per person: 58.9%); class medians run from 250k to 58.0M TZS. The edges are
          approximate (a third-party copy of the 2020 files). The cost itself exists only for that 4,809-row subset,
          so the six classes stay (USE-5).
        - Drop Tour_ID (18,506 unique opaque tour_id plus eight alphanumeric characters); no chronology is documented.
        - Merge the evident Widlife Tourism spelling (5,988 training rows) into Wildlife Tourism (2,283 rows).
        - Merge UAE (187 rows) into UNITED ARAB EMIRATES and BURGARIA (2 rows) into BULGARIA, both already
          present in the source. Other country distinctions stay as published.
        - Types (2026-11-04, Lennart; CLEAN-25, CLEAN-14): cost_category is an ordered category, Lower Cost < Low
          Cost < Normal Cost < High Cost < Higher Cost < Highest Cost. The source lists the classes alphabetically
          and gives no boundaries; Lower and Low are read as comparatives, as High < Higher < Highest are. The
          linked 2020 costs back the order: Spearman 0.965 for it, 0.945 with Lower and Low swapped. age_group is ordered bands (<18 < 18-24 < 25-44 < 45-64 < 65+). The party counts and nights stay numbers.
        - Retain ordinary missing values. Both party counts are set missing for 94 records with a zero total;
          a tourist record cannot describe a party with no people. No positive counts or night outliers are clipped.
        - travel_with is missing for 1,075 records, 1,045 (97.2%) of them one-person parties; it stays missing, since
          recoding it to Alone would be a guess (LEAK-8). 54 trips exceed 90 nights in total and one has 371
          (365 + 6); none is impossible, so all stay (CLEAN-11).
        - Source coding limits: 142 Independent records have a Yes package inclusion, while 104 Package Tour records
          have all seven inclusions No. Among records with both party counts known, 62 Alone records sum above one;
          344 records with a nonmissing non-Alone relationship sum to one. Questionnaire routing and count scope
          are unverified, so retain reported flags and positive counts rather than guess a recoding.
        - Retain all rows and stratified random evaluation, accepted by Myunghwan on 2026-10-25 after reviewing
          repetition evidence. Across all nine folds, 9.8509% of test evaluations match a training profile and
          90.1491% do not (pooled across three repeats, not distinct people). The copies are distinct respondents
          the coarse features cannot tell apart, kept under LEAK-18 (few coarse features, plausible repeats; Lennart, 2026-11-05, issue 7 (d), not a widened LEAK-19): 361 repeated
          profiles are Alone (213 of them with more than one label), and 67.8% of copy groups are larger than their
          party. A split grouped by feature profile costs +0.0047 log loss (+0.0025 without age_group; LightGBM, one
          repeat), and out-of-fold copy lookups gain nothing (1.0765 against 1.0755). Residual LEAK-17 risk: With
          Spouse is enriched among copy rows (44.6% against 27.8%), bounded by that grouped cost of about 0.005.
          Grouping on a feature hash is not allowed (SPLIT-24), and the release has no respondent/party linkage.
        - The curator-provided official Zindi archive matches all four retained source files exactly.
          Independent authenticated retrieval is not claimed.
          The mmu_2022 source repeats the same description, six-class metric and non-archive file sizes; the existing
          duplicate record is left unchanged. The 2020 "Tanzania Tourism Prediction" competition (6,476 rows,
          total_cost) is an earlier subset of the same survey with the raw TZS cost: 72.3% of its 4,809 training
          rows match a row here, against 23.4% by chance. It is a duplicate version under PROV-6, not shipped. The
          year stays 2022 (PROV-9): the 2020 file holds neither cost_category nor about 74% of these rows.
    """
    target = "cost_category"
    problem_type = "multiclass_classification"
    metric = Metric.source(
        "log_loss",
        original="Log Loss",
        reference="https://zindi.africa/competitions/ai4d-lab-tanzania-tourism-classification-challenge#evaluation",
    )
    accepted_check_warnings = {
        "dataset_duplicate_rows": "Myunghwan accepted row retention and stratified random evaluation on 2026-10-25 after reviewing all nine saved folds: 9.8509% matching and 90.1491% nonmatching test evaluations across three repeats. The 965 exact row extras are distinct respondents the coarse features cannot tell apart (LEAK-19): 361 repeated profiles are Alone and 67.8% of copy groups are larger than their party. A split grouped by profile costs +0.0047 log loss and copy lookups gain nothing. Residual LEAK-17 risk (With Spouse enriched, 44.6% against 27.8%) is bounded at about 0.005.",
        "dataset_conflicting_duplicate_rows": "Myunghwan accepted retention on 2026-10-25 after reviewing same- and different-label profile matches. The checker counts 468 additional distinct feature/label combinations; 410 profiles contain multiple labels (1,324 rows). On rows linked to the 2020 cut, such profiles have different real spending, so the ambiguity is genuine (LEAK-20). No outcome-based deduplication and no grouping on a feature hash (SPLIT-24).",
    }
    data_tags = ("ForcedIIDFromTemporal",)
    splits_comment = """
        Stratified random 3-fold cross-validation with 3 repeats, using benchmark split seed 4267 and row shuffle 42.
        Tests represent held-out visitor/trip records from the represented survey population under the fulfilled-plan scenario.
        No date column or chronological meaning of Tour_ID is documented, and the raw row order carries none
        (neighbouring labels agree 0.2211 against 0.2228 by chance). The use case looks forward (a trip before the
        visit), so the split is IID forced from temporal (SPLIT-8): a dated survey wave would test drift of the TZS
        band edges and of the visitor mix; recover it if NBS publishes it. No valid window exists to measure that
        cost. Repeated respondent/party linkage is not in the release; a split grouped by exact feature profile
        costs +0.0047 log loss, and similar profiles are not asserted to be real respondent groups.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        path = raw_dir / "Train.csv"
        expected = "1a71082258df9f998f14691170080674b719a347a0ad2c0862dd5e7a5e83899f"
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError("Train.csv does not match the verified original competition bytes.")
        return pd.read_csv(path)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = drop_columns(raw, ["Tour_ID"])
        df["main_activity"] = df["main_activity"].replace({"Widlife Tourism": "Wildlife Tourism"})
        df["country"] = df["country"].replace({"UAE": "UNITED ARAB EMIRATES", "BURGARIA": "BULGARIA"})
        # Zero in each sex count cannot describe the party that supplied this tourist record.
        zero_party = df["total_female"].add(df["total_male"]).eq(0)
        df.loc[zero_party, ["total_female", "total_male"]] = float("nan")
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        numeric = {"total_female", "total_male", "night_mainland", "night_zanzibar"}
        ordinal = {
            self.target: ["Lower Cost", "Low Cost", "Normal Cost", "High Cost", "Higher Cost", "Highest Cost"],
            "age_group": ["<18", "18-24", "25-44", "45-64", "65+"],
        }
        return FeatureTypes(ordinal=ordinal, categorical=[c for c in df if c not in numeric and c not in ordinal])

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        records = []
        for label, frame in [("Source, excluding ID", raw.drop(columns="Tour_ID")), ("Curated", df)]:
            features = frame.drop(columns=self.target)
            groups = frame.groupby(list(features.columns), observed=True, dropna=False)[self.target].agg(
                ["size", "nunique"]
            )
            records.append(
                {
                    "frame": label,
                    "rows": len(frame),
                    "distinct feature profiles": len(groups),
                    "exact row extras": int(frame.duplicated().sum()),
                    "profiles with multiple labels": int(groups["nunique"].gt(1).sum()),
                    "rows in those profiles": int(groups.loc[groups["nunique"].gt(1), "size"].sum()),
                }
            )
        return [
            Decision(
                title="Retain common survey profiles under the accepted evaluation",
                why=(
                    "The observed inputs are coarse visitor and trip descriptors. Their equality, including "
                    "different expenditure categories for the same profile, does not identify a repeated person "
                    "or party. Myunghwan accepted retaining empirical source-row frequencies and random evaluation on "
                    "2026-10-25; respondent/party linkage remains unverified for independent review."
                ),
                evidence=pd.DataFrame(records),
            )
        ]
