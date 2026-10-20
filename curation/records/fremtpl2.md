---
unique_name: fremtpl2
name: freMTPL2
checked_by:
- Andrej
suggestion: 'Yes'
tags:
- Two-Regime Zeros
- Non-IID (Temporal)
domain: insurance
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.kaggle.com/datasets/karansarpal/fremtpl2-french-motor-tpl-insurance-claims
source_row: 1044
type_adapter_id: curation-record-v1
---

## Comments

French Motor Third-Party Liability policies from CASdatasets, a standard actuarial benchmark. The canonical task is
claim frequency (Poisson regression of the claim count on exposure and policy features), usually with a random split.
Meets the criteria: unique original source, real predictive target, representative tabular data, no ethical issue.

CC (2026-10-20, Andrej): **Target: aggregate claim amount per policy (two-regime zeros). Temporal split on
`year_index` = `IDpol` // 1,000,000 (0-6, all kept). Drop `ClaimNb` and `IDpol`, keep `Exposure` capped at 1.**
Measured on the OpenML copies (41214, 41215):
* `freMTPL2freq`: one row per policy, 678,013 x 12: `IDpol`, `ClaimNb`, `Exposure` and nine rating features (`Area`,
  `VehPower`, `VehAge`, `DrivAge`, `BonusMalus`, `VehBrand`, `VehGas`, `Density`, `Region`; four categorical); 36,102
  claims. CASdatasets docs: 677,991 policies, "observed mostly on one year", "approximately 2011-2013"; the 22-row
  difference is unchecked.
* `freMTPL2sev`: one row per claim, 26,639 x 2 (`IDpol`, `ClaimAmount`), claimed policies only. Rows per policy equal
  `ClaimNb` for all but one (one short); 1,373 policies have several rows. Amounts 1 to 4,075,401, median 1,172. Fixed
  IRSA-IDA amounts (docs) 1,204, 1,128.12, 1,172, 1,128 and 602 are 42.3% of claims: point masses in the positive part.
* Build: sum `ClaimAmount` per `IDpol`, left-join onto `freMTPL2freq`, 0 where there is no severity row. Drop the 9,116
  claimed policies without a severity row (false zeros) and the 195 orphan severity rows (`IDpol` 2,220,367-2,286,775,
  absent from the current CASdatasets copy). Result: 668,897 x 10, 96.27% zeros.
* The claim count alone is the classic alternative target; not both (same policies, swapped target).
* `year_index` is inferred, not documented: the same vehicles recur under a new `IDpol` each year. Rows matched on
  `Area`, `VehPower`, `VehBrand`, `VehGas`, `Density`, `Region` with `DrivAge` and `VehAge` both +1 give 46,445-57,212
  one-to-one pairs from index i to i+1 for i = 0-3, 7,907 for 4 -> 5 and 10,470 for 5 -> 6, under 300 for any other
  pair; a control shift (`DrivAge` +1 only) gives about 1,000. Ages +2 link i to i+2. Seven yearly steps do not fit the
  docs' "2011-2013", so the calendar years are unknown; the split uses only the order (`unit="unique"`).
* Repeats: 38% of rows share their full feature vector with another row (consecutive IDs; 94% of these groups sum to
  <= 1 year of exposure: one policy-year split into records). With the renewal links, 66% of rows belong to a vehicle
  seen in more than one year.
* Drift by index, claim rate after the build: 5.6%, 4.7%, 3.4%, 3.3%, 3.5%, 2.2%, 1.9% (index 0 held 9,099 of the 9,116
  false zeros). Indices 5-6 hold newer cars (mean `VehAge` 3.0-3.5 against about 7.6) and almost no full-year exposures.
* Split check, untuned LightGBM, 10 features, scored on indices 2-6 (AUC for a claim / R^2 on log1p amount): random
  5-fold 0.718 / 0.035 (72.8% of test rows have their vehicle in train), grouped by reconstructed vehicle 0.715 / 0.037,
  forward by `year_index` 0.709 / 0.028. Repeated vehicles barely inflate the random score; the gap is drift, partly
  less training data in the early folds.
* `ClaimNb`: same period as the target, 0 exactly where the amount is.
* `IDpol` encodes the year and the file order: the first tenth (`IDpol` <= 144,089) has an 18.5% claim rate before the
  build; alone, AUC 0.57 for a claim. Only `year_index` is kept from it, as the time column.
* `Exposure`: a feature, not a divisor. The contracted period is known at pricing (a mid-year cancellation also
  shortens it); dividing would inflate short policies' targets. Alone: AUC 0.63. 1,224 policies above 1 (max 2.01).
* The other nine features are known at policy start; `BonusMalus` reflects claims before the period.

---

Also see https://arxiv.org/abs/2605.22892 and https://cas.uqam.ca/pub/web/CASdatasets-manual.pdf

**AI note (two-regime-zero audit, 2026-10-19):** aggregate claim amount as target, on the OpenML copies (41214, 41215,
uploaded 2018):
* 678,013 policies, 96.32% with an aggregate amount of exactly 0.
* 9,116 of the 34,060 policies with `ClaimNb` > 0 have no severity row, so their summed amount would be a false zero.
* 195 OpenML severity rows name policies missing from `freMTPL2freq`. The current CASdatasets copy (GitHub, 26,444
  severity rows) is the OpenML table without exactly those 195.
* Siblings: `bemtpl97`, `frempl_french_motor_personal_line` (a different French portfolio).
