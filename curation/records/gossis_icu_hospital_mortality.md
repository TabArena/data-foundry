---
unique_name: gossis_icu_hospital_mortality
name: 'WiDS Datathon 2020: patient survival in the ICU (MIT GOSSIS extract)'
checked_by:
- AI (UNVERIFIED)
- Andrej
data_foundry_status:
- 'DF: Yes'
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 2
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
original_source: Kaggle
year: '2020'
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/widsdatathon2020
- https://physionet.org/content/eicu-crd/2.0/
- https://doi.org/10.1097/ccm.0000000000005518
- https://www.kaggle.com/datasets/mitishaagarwal/patient
- https://www.kaggle.com/competitions/widsdatathon2020/data
- https://doi.org/10.13026/530d-1e61
v2_path: datasets/_dev/tabarena-v0pt2/gossis_icu_hospital_mortality/dataset.py
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: the WiDS Datathon 2020 table of 91,713 labelled ICU stays from 200+ US hospitals, scored by ROC AUC on in-hospital death from the first 24 hours; an established task, but the run created a second record for the same competition (`wids_icu_hospital_death`), and the table is a cut of the eICU database whose record proposes the same task (PROV-6).
- Source: WiDS Datathon 2020 on Kaggle (opened 2020-01-10, 951 teams; https://www.kaggle.com/competitions/widsdatathon2020), data from MIT's GOSSIS initiative, also on PhysioNet as "WiDS (Women in Data Science) Datathon 2020: ICU Mortality Prediction" v1.0.0 (2020-01-22; Lee, Raffa, Ghassemi, Pollard, Kalanidhi, Badawi, Matthys, Celi; https://doi.org/10.13026/530d-1e61, credentialed access). As published: training_v2.csv with 91,713 labelled stays and unlabeled.csv with 39,308 stays without labels, "more than 130,000 hospital Intensive Care Unit (ICU) visits"; the data dictionary (read) lists 188 variables: vitals 52, labs 60, blood gas 16, APACHE covariates 28, comorbidities 8, demographics 16 (with the target), identifiers 3 (`encounter_id`, `hospital_id`, `patient_id`), APACHE groupings 2, two APACHE IVa death probabilities and one GOSSIS example prediction; target `hospital_death` ("Whether the patient died during this hospitalization"). The US cohort is very probably the eICU-CRD part of GOSSIS (2014-2015; not stated on the PhysioNet page).
- Use case: "create a model that uses data from the first 24 hours of intensive care to predict patient survival" (PhysioNet): the prediction point is stated, the actor is not; the GOSSIS and APACHE use is an objective severity estimate for risk adjustment and ICU benchmarking (Raffa et al. 2022, not read); fit direct for that estimate at 24 h; regime IID (as `wids_diabetes_mellitus` shipped) or grouped by `hospital_id` (a score used at a new hospital), to decide; `patient_id` may repeat.
- Siblings and duplicates: `wids_icu_hospital_death` (created by the same run, screening batch 53, for the same Kaggle competition and target: the same dataset, PROV-4; one of the two should become `Duplicate`); `eicu_collaborative_research_database` (`TBD -> 2nd Tier`, priority 3, whose screening proposes ICU mortality at 24 h: this table is a cut of it with the task defined, PROV-6, the curator decides which enters); `eicu_crd_2020_2021` (unscreened, a newer eICU release); `wids_diabetes_mellitus` (`Yes`, WiDS 2021, the GOSSIS table with diabetes as target: overlapping stays and a distinct task, PROV-7); `2_month_survival_rate_prediction` (`Yes`, SUPPORT: another source). External collections: TabBank's sheet marks the Kaggle copy "Patient Survival Prediction" (https://www.kaggle.com/datasets/mitishaagarwal/patient) as a simplified version (the run's note).
- Better data: no new search; found as better data for `2_month_survival_rate_prediction`, `eicu_collaborative_research_database` and `wids_diabetes_mellitus`, and through the curator's Zotero collection (items 47, "TabBank", and 80, "PhysioNet").
- Papers and pages: the Kaggle competition; the PhysioNet page (read); Raffa et al. 2022, GOSSIS (Crit Care Med, https://doi.org/10.1097/ccm.0000000000005518, not read); top solutions not read.
- Metric: ROC AUC (Kaggle API evaluationMetric "Area Under Receiver Operating Characteristic Curve"; PhysioNet: scored "on a Kaggle leaderboard using AUROC"), a leaderboard metric (MET-4): `roc_auc`. Inputs: none.
- Risks for /add-dataset: `apache_4a_hospital_death_prob` and `apache_4a_icu_death_prob` are APACHE IVa model outputs from first-day data (known at 24 h, not fit on this table; keep as a reference or drop, to decide); the duplicate record and the eICU version (PROV-4, PROV-6); only the 91,713 labelled stays can ship; readmitted stays and repeated patients (`readmission_status`, `patient_id`); the Kaggle rules and the PhysioNet data use agreement (no criterion, EV-4).
- Priority: gap 0 (medical, binary, IID and grouped are not thin), use case 0 (the source states the prediction point, not the actor or decision), source + (PhysioNet page with authors, data dictionary, GOSSIS paper), shape + (91,713 stays, about 186 columns, hospitals), risk - (a duplicate record and an eICU version to settle).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `2_month_survival_rate_prediction`, `eicu_collaborative_research_database`, `wids_diabetes_mellitus`; a related task next to `wids_diabetes_mellitus`; the curator's Zotero collection, item 47: "TabBank"; the curator's Zotero collection, item 80: "PhysioNet".
- as published: training_v2.csv: 91,713 ICU encounters labelled (about 186 columns per the dictionary; not counted), from 'more than 130,000' ICU visits over one year in 200+ US hospitals (eICU, 2014-2015); ...; target: hospital_death (death before hospital discharge), from data of the first 24 hours of ICU care; ROC AUC; access: registration.
- Why: same quantity as SUPPORT's (short-term death of seriously ill hospitalized adults) from features of the same kind (APACHE physiology, age, diagnosis group, comorbidities, admission source) at an early prediction point; Knaus authored both APACHE and the SUPPORT model | Same GOSSIS first-24h ICU table as ...
- Adds: 10x more patients (91,713 vs 9,105), 2014-2015 instead of 1989-1994, 200+ hospitals instead of 5, hospital_id and icu_id for a grouped split; caveats: in-hospital death instead of death by day 60, ICU only, ships APACHE IV death probabilities (drop or keep as a reference); data use limited to the datathon by the ...
- A newer release of the same source as the record(s) named above (PROV-6): the curator decides which one enters.

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: the same WiDS Datathon 2020 competition (`wids_icu_hospital_death`; PROV-4). The curator keeps one, or both as distinct tasks.

CC (2026-11-11, Andrej): built as the v2 dataset that replaces wids_diabetes_mellitus (BeyondArena v0.2 review page, wids_diabetes_mellitus issue 1, c: "Replace the target by in-hospital death"): WiDS 2020's training_v2.csv, 91,713 ICU stays at 147 hospitals, `hospital_death` (8.6%), split by hospital (its issue 5 answer), ROC AUC. APACHE IVa's two death probabilities dropped (another model's prediction, CLEAN-6; ROC AUC 0.861 alone, LightGBM 0.902 with or without them); identifiers, `icu_id`, the constant `readmission_status` and three duplicate columns dropped. Carried over from the diabetes marks where they apply: no clipped flags are built; no age 0 occurs; the 1,756 BMI mismatches all sit at GOSSIS's clipping bounds, so BMI ships as published (Review issue 2). Licence: Kaggle Competition Rules (rules tab not readable without acceptance); the PhysioNet copy (https://doi.org/10.13026/vc0e-th79) is credentialed under the PhysioNet Restricted Health Data License 1.5.0.

**Assessment (AI, 2026-11-11):** review panel (small: claim auditor, split auditor, critic; no mediator): ship after changes (the critic; the repeat-patient note reworded and one wording fix applied); disputed: none; for the curator: issues 1-3 (time-basis tag `ForcedGroupedFromTemporal` per SPLIT-8, BMI at clipping bounds kept per CLEAN-11, negative pre-ICU days kept). Checks 0 errors, 0 warnings; probes flag nothing; LightGBM 0.898-0.902 against linear 0.881-0.884, APACHE IVa 0.861; grouped 0.901 vs random 0.903. Priority 2: gap 0, use case + (the source states the prediction point; the APACHE use is established), source + (PhysioNet page with authors, data dictionary), shape + (91,713 rows, 147 hospitals), risk - (licence terms unread on Kaggle; a duplicate record and the eICU parent to settle).

CC (2026-11-11, Andrej): BeyondArena v0.2 review page: issue 1 "Option B: ForcedGroupedFromTemporal." — the hospital split is tagged `ForcedGroupedFromTemporal` (SPLIT-8; one undated year, a later period untested) with a `Time basis:` line in `curation_comments`. Issues 2 and 3 `ok`: BMI at GOSSIS's clipping bounds and the 778 negative `pre_icu_los_days` (a registration lag) ship as published, with notes.

## Review

**Outcome:** added. The WiDS Datathon 2020 training table (https://www.kaggle.com/competitions/widsdatathon2020), MIT's
GOSSIS ICU data: 91,713 stays at 147 US hospitals, first-day vitals, labs, APACHE values, admission facts and chronic
conditions; target in-hospital death (8.6%); split by hospital; ROC AUC (the competition's metric). Built on
Andrej's mark of 2026-11-11 (wids_diabetes_mellitus, issue 1, c) in place of the diabetes task on the same cohort.
APACHE IVa's two death probabilities are dropped (another model's prediction; with them LightGBM scores the same,
0.902); they stay the reference (0.861). Checks clean (0 errors, 0 warnings); probes flag nothing; LightGBM 0.898 to
0.902 against linear 0.881 to 0.884. Licence: Kaggle's rules tab could not be read (behind acceptance); the PhysioNet
copy is credentialed (PhysioNet Restricted Health Data License 1.5.0): a release-checklist item, not a verdict reason.
Weighed: an established task with a clinical baseline, many hospitals +; a time basis to name, two cleaning calls -.

**Main points:** All issues resolved (2026-11-11): the hospital split is tagged `ForcedGroupedFromTemporal` (issue
1); BMI at the clipping bounds (issue 2) and the negative pre-ICU days (issue 3) ship as published.

**Record judgment:** valid source and target. The record's screening holds on the data (claim audit: nothing refuted).
The duplicate record `wids_icu_hospital_death` (the same competition) and the eICU parent
(`eicu_collaborative_research_database`, the same task proposed) are left to the curator on their records.

**Issues for Andrej:**

1. **Tag the hospital split `ForcedGroupedFromTemporal`, since the stays are undated?**

   * **Problem:**
     - A severity score is fit on past stays and used on later ones, but the release covers one year with no date.
     - The rules ship such a task in the closest regime, tagged as forced from temporal, after a leak test[^1a].
     - Add the tag, or leave the grouped split untagged since its reason is the new hospital?
   * **Background:** for the same cohort (wids_diabetes_mellitus, issue 4) no order carries time: within each hospital,
     late vs early stays give adversarial AUC 0.500 by file order, `encounter_id` and `patient_id`. eICU records a
     discharge year (2014/2015) but publishes no key to these rows.
   * **Experiments:** leak test done: no copies across the split, no row-order signal (next-row label match 0.843
     against 0.842 by chance), `patient_id` one per row.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | No tag (implemented) | grouped split as now | the split's reason is the new hospital | says nothing about the untested later period |
     | B | `ForcedGroupedFromTemporal` | the tag and a `Time basis:` line | names what the split cannot test; follows the rule for lost time | drift within one year is likely small |

   * **Recommendation:** B: the use case runs forward and the time is lost. **Decision:** A or B?

   **Notes for the AI:** on B, `data_tags = ("ForcedGroupedFromTemporal",)` and a curation bullet: `- Time basis:
   ForcedGroupedFromTemporal: ICU stays of one year (eICU, 2014-2015), released without a date or an order (no signal
   in the file order, encounter_id or patient_id); the split holds out hospitals, and a later period of stays, which a
   dated release would allow, is not tested.` `dataset check`.

   [^1a]: **SPLIT-8** (Must): a task temporal in nature or by its use case whose release cannot give the windows ships
     in the closest regime, tagged as forced from temporal, after a leak test across the split.

   **Resolved (2026-11-11, Andrej):** B: `data_tags = ("ForcedGroupedFromTemporal",)` and a `Time basis:` bullet in
   `curation_comments` (a later period of stays is not tested); `dataset check` rerun.

2. **Keep BMI at GOSSIS's clipping bounds as published, unlike wids_diabetes_mellitus?**

   * **Problem:**
     - 1,756 rows have a BMI more than 0.01 from weight over height squared; every one has BMI, weight or height at a
       fixed clipping bound (BMI 14.84 / 67.81, weight 38.6 / 186 kg, height 137.2 / 195.59 cm).
     - The wids_diabetes_mellitus mark of 2026-11-11 set such BMIs missing as impossible; there too, all 2,549 sit at
       a bound (the critic's check), so the premise was wrong.
     - Keep them as published (clipped extremes), or set them missing as in the diabetes task?
   * **Effect on the task:** these rows die at 12.9% against 8.6% (17.8% at the lower BMI bound), so a missing value
     would mark them; the values are real extremes clipped by the source.
   * **Experiments:** LightGBM, 5 folds grouped by hospital:

     | BMI | ROC AUC |
     |---|---|
     | as published | 0.902 |
     | set missing at a mismatch | 0.9015 |

   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | BMI, weight and height as published, a note on the bounds | not impossible values; as the clipped vitals ship | departs from the diabetes mark |
     | B | Set missing | as wids_diabetes_mellitus | the same handling as the earlier mark | removes real extremes; the missing value marks sicker patients |

   * **Recommendation:** A: a value at a clipping bound is not impossible. **Decision:** A or B?

   **Notes for the AI:** on B, `df["bmi"] = df["bmi"].mask((df["bmi"] - df["weight"] / (df["height"] / 100) ** 2).abs()
   > 0.01)` in `_clean`, the clipping bullet rewritten; `dataset check`.

   **Resolved (2026-11-11, Andrej):** A (`ok`): BMI, weight and height ship as published at GOSSIS's clipping bounds;
   the clipping bullet records the mark.

3. **Keep the 778 negative pre-ICU stays as published?**

   * **Problem:**
     - `pre_icu_los_days` is below 0 in 778 rows (median -0.30 days, 647 above -1 day, minimum -24.9), a hospital
       registration recorded after the ICU admission, at 86 hospitals.
     - The cleaning rules set an impossible value missing and keep the row[^3a]; as a recording lag the value still
       says "admitted straight to the ICU".
     - Keep as published, or set missing?
   * **Effect on the task:** these rows die at 3.2% against 9.0% just above zero; missing would mark the same rows, as
     no other value of the column is missing.
   * **Experiments:** LightGBM, 5 folds grouped by hospital: 0.902 either way.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | values as published, the note names the registration lag | keeps "straight to the ICU"; the data as released | a negative duration in the data |
     | B | Set missing | negative values missing | follows the cleaning rule | the missing value marks the same rows; loses the near-zero meaning |

   * **Recommendation:** A: mostly hours of registration lag, and missing carries the same signal. **Decision:** A or B?

   **Notes for the AI:** on B, `df["pre_icu_los_days"] = df["pre_icu_los_days"].mask(df["pre_icu_los_days"] < 0)`, the
   anomaly bullet rewritten; `dataset check`. On A, add to the bullet: "a registration lag in eICU (hospital admission
   recorded after the ICU admission); kept, as missing values would mark the same rows (2026-11-11)".

   [^3a]: **CLEAN-11** (Should): impossible values become missing, and the row stays.

   **Resolved (2026-11-11, Andrej):** A (`ok`): the 778 negative values ship as published; the anomaly bullet names the
   registration lag and why they are not set missing.

**Review panel:** ship after changes (critic; small panel: claim auditor, split auditor, critic, no mediator). Claim
audit: 21 claims, nothing refuted, one wording fixed (the "Undefined diagnoses" mapping), the licence untested (Kaggle's
rules tab not readable). Split audit: hospital grouping right; grouped 0.901 vs random 0.903; open: the time-basis tag
(issue 1). Critic: issues 1 to 3, the repeat-patient note reworded (applied), and the same-cohort records to settle.

<details><summary>Claim audit</summary>

Nothing refuted; one wording imprecise; licence untested.

| Claim | Test | Result | Evidence |
|---|---|---|---|
| 91,713 stays, 8.6% died; 147 hospitals, 2 to 4,333 stays | pandas | holds | 0.0863; min 2, max 4,333 |
| US hospitals; one year, not dated | PhysioNet page, ethnicity codes | holds, indirectly | "a one-year timeframe"; consortium also abroad, no breakdown |
| every feature known at 24 h | dictionary, leak probes | holds | `*_apache` are first-24 h worst values; diagnoses at admission; best single feature `gcs_verbal_apache` 0.703 |
| no copies across the split | leak probe, raw copies, quasi-identifiers | holds | 0.0% of test rows copied; 0 raw copies; readmits matched 3 of 560 vs 2 by chance |
| APACHE IVa dropped; 0.863 on 81,395 rows; -1 in 2,371, missing 7,947 | AUC on rows >= 0 | holds | 0.8627 |
| ids one per row; `icu_id` nested in hospital | nunique; ICU ids per hospital | holds | 91,713 each; 0 of 241 ICUs shared |
| `readmission_status` constant; three duplicate columns | value counts; hash scan | holds | no other duplicate groups |
| clipping bounds; 1,756 BMI mismatches all at a bound | min/max, counts | holds | 443/422, 459/447, 453/429 rows at the bounds; 12.9% died |
| 778 negative pre-ICU days | pandas | holds | median -0.298; 647 above -1 |
| "Undefined diagnoses" variants map to different systems | crosstab | partly holds | the first maps to Cardiovascular 2,948 and Musculoskeletal/Skin 820 (wording fixed) |
| 57 of 66 WiDS 2020 test hospitals unseen | unlabeled.csv | holds | 95.7% of its stays at unseen hospitals |
| metric ROC AUC from the source | Kaggle API, PhysioNet | holds | "Area Under Receiver Operating Characteristic Curve" |
| licence | PhysioNet; Kaggle rules | half tested | PhysioNet Restricted Health Data License 1.5.0 confirmed; Kaggle rules unread |

Probe notes, no finding: the number format alone scores 0.776, from the arterial blood gas columns (whether a gas was
taken marks sicker patients, missingness 0.67) and clipping bounds; interpolation-like cells carry no class pattern.

</details>

<details><summary>Split audit</summary>

Verdict: right, with notes.

| Split | ROC AUC | sd | Death rate per fold |
|---|---|---|---|
| as shipped, 3x3 by hospital | 0.901 | 0.0025 | 7.6% to 9.6% |
| random 3x3 | 0.903 | 0.0021 | 8.6% |
| by ICU 3x3 | 0.902 | 0.0029 | 8.3% to 9.0% |
| by hospital 5x1 | 0.904 | 0.0074 | 8.1% to 9.0% |
| random, without / with `hospital_id` | 0.9033 / 0.9023 | | |

- Time basis not stated (one undated year, forward use case): add `ForcedGroupedFromTemporal` and a `Time basis:`
  line; no re-split.
- Fold balance: the largest hospital is at most 17.6% of a test fold; 3x3 is the rule's default; 5 folds would be
  worse.
- The features name the hospital (82.8% among the 20 largest), but `hospital_id` adds nothing: case mix carries the
  outcome.
- Hospital is the right group: every ICU belongs to one hospital; the organisers' test file has 57 of 66 hospitals
  unseen.
- No hidden groups or near copies across hospitals.

</details>

<details><summary>Critic</summary>

Ship after changes; nothing makes it a wrong task.

1. Same-cohort records not settled: the eICU parent proposes the same task; wids_diabetes_mellitus must leave in the
   same change (applied on its record); `wids_icu_hospital_death` needs a curator mark.
2. No time-basis tag on a forward use case: add `ForcedGroupedFromTemporal` and a `Time basis:` line (issue 1).
3. BMI kept here, set missing on the diabetes task: every mismatch in both files sits at a clipping bound, so the
   reasons do not differ; recommend keep (issue 2).
4. Negative pre-ICU days are impossible as a duration: set missing or name the registration lag (issue 3).
5. "One stay per patient" was unsupported: `patient_id` is minted per row; reworded (applied).

Dropped: the licence (no verdict reason), the model spread (LightGBM 0.901, linear 0.884, APACHE 0.861), the
`*_apache` inputs (a fixed scoring rule's first-day values), the clipped values.

</details>
