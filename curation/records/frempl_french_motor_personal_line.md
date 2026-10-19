---
unique_name: frempl_french_motor_personal_line
name: freMPL1-10 (CASdatasets, French motor personal line insurance, private insurer, 2004)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
domain: insurance
required_split:
- Random (IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://dutangc.github.io/CASdatasets/reference/freMPL.html
- https://github.com/dutangc/CASdatasets/tree/master/data
- https://dutangc.perso.math.cnrs.fr/RRepository/pub/web/NEWS.html
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

Ten tables from one "private motor French insurer", each with "risk features, claim amount and claim history of
around 30,000 policies for year 2004" (CASdatasets documentation). The workbook lists freMPL2, 3, 5, 6, 7, 8 and 9 as
seven distinct candidates (Master rows 63-69) and says not to merge them. Measured on the downloaded tables
(2026-10-19), that does not hold: they are cuts of one portfolio, so all seven rows go into this one record.

freMPL1-4 share a schema with vehicle features (body, price, engine, energy, maximum speed, class, `RiskVar`,
`Garage`). freMPL1 and freMPL3 are the same 20,594 distinct policy-years (every feature vector matches) with
different claim amounts, i.e. different guarantees; freMPL3 adds a deductible type. freMPL2 (38,300 rows) and freMPL4
(26,300) contain 20,555 and 20,592 of those policy-years. Picking more than one of them is the same data with a
swapped target. freMPL5-9 share a second schema without vehicle details but with claim counts by type "in the 4
preceding years" (responsible, non-responsible, parking, fire-theft, windscreen, out-of-use) and a risk area; they are
disjoint (0-8 shared feature vectors per pair) and together hold 115,200 policy-years. freMPL10 overlaps each of them
by 288-580 rows.

Zero mechanism, confirmed from the data: `ClaimAmount` is 0 where `ClaimInd` = 0 (no claim on the guarantee during
the record), 88.3% (freMPL1) to 99.9% (freMPL10) of rows, 89.7% over freMPL5-9. freMPL1, 2 and 5-9 also have 0.6-1.0%
negative amounts, all with `ClaimInd` = 0, presumably recoveries; they need a rule (set to 0 or drop). A quick
untuned LightGBM (3-fold random CV, negatives set to 0, `ClaimInd` dropped) gives ROC AUC 0.65 for a claim and R^2
0.001 on the log1p amount for freMPL1, and 0.69 and 0.031 for freMPL5-9: the zeros carry the variance, as in
`forest_fires`, and the amount signal is small.

Recommendation: one dataset, freMPL5-9 concatenated (115,200 rows, 17 features with the claim history), or freMPL1
alone if the vehicle features matter more; drop `ClaimInd`. IID: all records start and end within 2004. No policy id,
so a policy split into several records cannot be traced. Licence: GPL (>= 2) (CASdatasets). Siblings from the same
package: `fremtpl2`, `bemtpl97` (different portfolios).

## Reference

CASdatasets (Dutang C., Charpentier A.), `freMPL1` to `freMPL10`, "Unknown French private insurer".
https://dutangc.github.io/CASdatasets/reference/freMPL.html

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master rows 63-69 (freMPL2, freMPL3, freMPL5, freMPL6,
freMPL7, freMPL8, freMPL9).
