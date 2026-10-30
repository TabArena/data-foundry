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
            "spending category for a specified alternative trip plan, "
            "conditional on the trip happening as specified."
        ),
        row="One labeled tourist survey record in the 2022 competition's training file (18,506 records).",
        predicted=(
            "The original cost_category: Low Cost, Lower Cost, Normal Cost, High Cost, Higher Cost or Highest Cost. "
            "The release does not document monetary boundaries or the expenditure basis."
        ),
        known=(
            "Visitor country, age group and first-trip status; travel party, purpose, activity, information source, "
            "tour arrangement, package inclusions and nights on the mainland and Zanzibar. Historical realized "
            "plan-like attributes instantiate the specified scenario."
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
            "The conditional-plan scenario uses the observed trip attributes, assuming the plan is fulfilled. "
            "The release does not specify currency, per-person versus party or trip versus daily expenditure, "
            "class thresholds, survey year or respondent/party linkage."
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

        - Prediction point: a visitor supplies visitor context and a proposed trip plan, assumed to occur as specified.
          Nights, activity, party and package attributes are scenario inputs even though recorded in an exit survey.
          package_food denotes package inclusion, not meal consumption. cost_category stays target-only.
        - Keep all six source classes and source Log Loss. Currency, expenditure basis and class thresholds are
          undocumented in the inspected release; no regression target or monetary boundaries are reconstructed.
        - Drop Tour_ID (18,506 unique opaque tour_id plus eight alphanumeric characters); no chronology is documented.
        - Merge the evident Widlife Tourism spelling (5,988 training rows) into Wildlife Tourism (2,283 rows).
        - Merge UAE (187 rows) into UNITED ARAB EMIRATES and BURGARIA (2 rows) into BULGARIA, both already
          present in the source. Other country distinctions stay as published.
        - Retain ordinary missing values. Both party counts are set missing for 94 records with a zero total;
          a tourist record cannot describe a party with no people. No positive counts or night outliers are clipped.
        - Source coding limits: 142 Independent records have a Yes package inclusion, while 104 Package Tour records
          have all seven inclusions No. Among records with both party counts known, 62 Alone records sum above one;
          344 records with a nonmissing non-Alone relationship sum to one. Questionnaire routing and count scope
          are unverified, so retain reported flags and positive counts rather than guess a recoding.
        - Retain all rows and stratified random evaluation, accepted by Myunghwan on 2026-10-25 after reviewing
          repetition evidence. Across all nine folds, 9.8509% of test evaluations match a training profile and
          90.1491% do not (pooled across three repeats, not distinct people). Identical coarse plans may have
          different spending; respondent/party linkage remains unverified (LEAK-16/18).
        - The curator-provided official Zindi archive matches all four retained source files exactly.
          Independent authenticated retrieval is not claimed.
          The mmu_2022 source repeats the same description, six-class metric and non-archive file sizes; the existing
          duplicate record is left unchanged. The 2020 regression competition is a different published task/cut.
    """
    target = "cost_category"
    problem_type = "multiclass_classification"
    metric = Metric.source(
        "log_loss",
        original="Log Loss",
        reference="https://zindi.africa/competitions/ai4d-lab-tanzania-tourism-classification-challenge#evaluation",
    )
    accepted_check_warnings = {
        "dataset_duplicate_rows": "Myunghwan accepted row retention and stratified random evaluation on 2026-10-25 after reviewing all nine saved folds: 9.8509% matching and 90.1491% nonmatching test evaluations across three repeats. The 965 exact row extras are repeated coarse profiles; they do not establish repeated people. Retain empirical source-row frequencies; respondent/party linkage remains unverified.",
        "dataset_conflicting_duplicate_rows": "Myunghwan accepted retention on 2026-10-25 after reviewing same- and different-label profile matches. The checker counts 468 additional distinct feature/label combinations; 410 profiles contain multiple labels (1,324 rows). Identical coarse plans can have different spending categories. No outcome-based deduplication or invented respondent grouping; linkage remains unverified.",
    }
    splits_comment = """
        Stratified random 3-fold cross-validation with 3 repeats, using benchmark split seed 4267 and row shuffle 42.
        Tests represent held-out visitor/trip records from the represented survey population under the fulfilled-plan scenario.
        No date column or chronological meaning of Tour_ID is documented. Random evaluation follows this use case,
        rather than inferring independence solely from missing timestamps. Repeated respondent/party linkage cannot
        be verified from the release. Similar feature profiles are not asserted to be real respondent groups.
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
        return FeatureTypes(categorical=[c for c in df if c not in numeric and c != self.target])

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
