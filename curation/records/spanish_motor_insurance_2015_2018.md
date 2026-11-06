---
unique_name: spanish_motor_insurance_2015_2018
name: Spanish motor insurance portfolio 2015-2018 (Lledó and Pavía, Mendeley 5cxyb5fp4f)
checked_by:
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 3
tags:
- Two-Regime Zeros
- Non-IID (Temporal)
original_source: Other
year: '2023'
domain: insurance
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://data.mendeley.com/datasets/5cxyb5fp4f
- https://doi.org/10.17632/5cxyb5fp4f.2
- https://doi.org/10.1007/s13385-024-00398-0
v2_path: datasets/_dev/tabarena-v0pt2/spanish_motor_insurance_2015_2018/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**AI-FILLED, UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from the source pages, papers and data previews named below (measured where the notes say so). A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-20):** `TBD -> 2nd Tier`, priority 3: a real policy-year table of a Spanish non-life insurer
with a clear claim-cost target, secondary to the 2022-2024 release of the same research group, and it needs three
fixes (claim-history columns that hold later years, truncated 2018 years, no exposure).
- Source: Segura-Gisbert, Lledó and Pavía (Universitat de València), Mendeley Data 5cxyb5fp4f (v1 10 August 2023, v2
  30 July 2024, CC BY 4.0), described in European Actuarial Journal 15:241-253 (online 2 September 2024). Sec. 1, p.
  242: "During a research project conducted by the authors within a Spanish insurance company, specialized in non-life
  insurance, we gained access to one of their motor vehicle insurance portfolio datasets and were authorized to share
  a sample of anonymized data." As published: 105,555 policy-years (renewals from November 2015 to November 2018) of
  53,502 policies x 30 columns, and a file with claim types for about 15% of claims (Sec. 4).
- Target and zeros (measured 2026-10-20): `Cost_claims_year`, payments plus reserves (Sec. 3), 0 in 81.4% of rows,
  exactly the rows with `N_claims_year` = 0; the zero is an observed claim-free policy-year. Positive costs run from
  40.05 to 260,853. Two regimes: a claim or not, then its cost.
- Use case: the paper names "price renewal strategies ... as well as pricing mechanisms for new business" (Sec. 1): an
  insurer at renewal sets next year's premium. The fit is approximate until exposure is rebuilt. Regime temporal by
  renewal year (SPLIT-6), with policies repeating across years (SPLIT-13).
- Siblings and duplicates: `spanish_motor_insurance_coverage_level_2022_2024` (Espinosa, Lledó and Atance 2026, TBD ->
  Yes). Neither article says whether the insurer is the same; the 2022-2024 article cites this release as [9]
  (Background: "A coverage-level breakdown is provided solely by [9], only for claims and for a limited share (15%) of
  the portfolio"). The periods do not overlap and the schemas differ (policy-years by renewal without exposure here;
  calendar insured-years with exposure and seven covers there), so no rows are shared. If it is one insurer, this is
  an earlier period of the same portfolio with the same task: a PROV-6 or PROV-7 call for the curator. A copy sits on
  openICPSR (project 193182).
- Risks for /add-dataset: `N_claims_history` is the same in every row of a policy (all 32,923 policies with several
  rows), so early rows count later claims, and `Lapse` and `Date_lapse` are set at the end of the contract. With them,
  untuned LightGBM on 2015-17 -> 2018 reaches AUC 0.97 for a claim, against 0.72 without: drop them or rebuild them
  from earlier rows (LEAK-10). The data "includes claims up to 2018" (Sec. 3), so policy-years renewed in 2018 are cut
  short: the zero share rises from about 70% (renewals of 2016-Q1 to Q3) to 99.2% (2018-Q4). Keep complete years or
  build exposure from the dates (USE-5). `Value_vehicle` is the value "on 31/12/2019". R^2 on log cost among claimants
  -0.01: the weak severity signal of the family.
- Priority: gap 0, use case + (the paper names renewal pricing), source + (paper and variable dictionary), shape +
  (105,555 rows, about 25 usable features, dated), risk - (the claim-history leak, truncated last year).

**Assessment (AI, 2026-10-30):** suggested call for policy question 3 of the zero-inflated review, where Andrej asked
for a call per dataset from its references and the domain's practice instead of one convention for the family (the
shared reasoning: a time exposure or a sum insured is a feature, and a rating-cell table weights the metric by its
exposure; negative amounts that are recoveries become 0; the source's metric first, else the normalized Gini as a
context metric, since RMSE on raw amounts follows a few large claims and a Tweedie or Poisson deviance needs positive
predictions; MET-10 as amended on 2026-11-02 (Andrej) later declined a family-wide metric, so each table's metric is
decided on its own); the curator
has the call.
- Target: `Cost_claims_year` per renewal year.
- Exposure: no column; keep the complete renewal years (drop those renewed close to the 2018 claims cut-off), or build
  exposure from the dates and use it as a feature.
- Negative amounts: none (minimum 40.05).
- Metric: normalized Gini as a context metric (MET-11); the paper reports no model.
- Drop `N_claims_history`, `Lapse` and `Date_lapse`, or rebuild the history from earlier rows (LEAK-10).

CC (2026-10-30, Andrej): `Yes`, priority 3 (the AI screening had `TBD -> 2nd Tier`, priority 3; zero-inflated screening
review page).

**Assessment (AI, 2026-11-01):** added as `datasets/_dev/tabarena-v0pt2/spanish_motor_insurance_2015_2018/` by /add-dataset with the full review panel; the open questions are in its `REVIEW.md`. Recommend shipping; issue 1 (the task changed from renewal pricing to new-business pricing for customers with one policy) could still turn it to `No`. A policy's later yearly rows hold a remnant of earlier claims, not the year's own (0.9% have a claim after a claim-free year, against about a third of first years), so only first years are kept (25,665 rows, 5 monthly test windows of 2017). Changes after the panel: the 5,069 renewals never in force and `Payment` dropped, a 12-month gap before each window. Corrections to the notes above: PROV-6 and PROV-7 against the 2022-2024 sibling are settled as not a duplicate, closing the screening's call for the curator; "the zero is an observed claim-free policy-year" held for 83% of the zeros, not all (17% were years without cover). The screening's renewal use case and the Assessment's target and exposure lines wait for your mark on issue 1. Priority 3: gap + (insurance thin), use case 0 (fit approximate), source + (data article and variable sheet), shape + (25,665 rows, temporal), risk - (the premium alone ranks as well as any method; the task is open).

CC (2026-11-03, Andrej): the task as built is confirmed (issue 1 (A) in spanish_motor_insurance_2015_2018): each policy's first year, the pricing of a new contract, not renewal pricing over all policy-years.

CC (2026-11-03, Andrej): `Value_vehicle` stays (issue 3 (A)): "we can add to the comment that we assume that the value changes proportionally".

CC (2026-11-03, Andrej): no request to the authors now (issue 4): "Write a comment that we could do this for a future version, but now go with the task as we have it for simplicity".

**Assessment (AI, 2026-11-03):** the screening lines above describe renewal pricing over all policy-years; what ships is new-business pricing on each policy's first year (issue 1), so they are superseded.

CC (2026-11-03, Andrej): every first year is kept, with the customer's other policies in force at the start in place of the calendar-year count (issue 2, design S): "Good, we can ship S with 5 splits." Ship, re-checking `Trivial` on the first benchmark run (issue 5): "With design S we can ship."

CC (2026-11-03, Andrej): the check warning `task_target_value_dominant` accepted: "for these tasks this is natural and a core challenge" (zero-inflated target).

CC (2026-11-06, Lennart): issue 6 of the folder's REVIEW.md resolved. The task stays per contract under the exposure rules adopted this day (MET-14's per-contract clause, MET-15): every first year is a contract of exactly one calendar year, known at the quote (37,090 of 37,090), and `Premium` is the written annual premium, not prorated (Spearman -0.03 with the share of the year in force among the cut years), so no feature carries a cut; no weight and no offset. The count of first years cut short by a lapse is 2,055 of 37,090 (5.5%; 233 of the 4,362 test rows; 1,632 of them half-yearly payers who stopped paying, at a median of half the year), not the 1,236 that `fit_reason` gave: that was the count of the one-policy design (25,665 rows), left in the text when design S kept every first year (Andrej, 2026-11-03, issue 2). Per contract the cut years claim like full years (a claim in 35.4% of each), per year at risk 1.9 times as often (1.53 claims a year against 0.81). It confirms the per-contract target of issue 1 (Andrej, 2026-11-03); what keeps it per contract is the constant planned term, unlike fremtpl2 and bemtpl97, whose periods are realized lengths with no planned term.

## Reference

Segura-Gisbert J., Lledó J., Pavía J.M. (2025). Dataset of an actual motor vehicle insurance portfolio. European Actuarial Journal 15:241-253. https://doi.org/10.1007/s13385-024-00398-0
Data: Mendeley Data, https://doi.org/10.17632/5cxyb5fp4f.2 (CC BY 4.0).

Lead: zero-inflated screening review, policy question 6 (curator's go, Andrej, 2026-10-20); sibling of `spanish_motor_insurance_coverage_level_2022_2024`.
