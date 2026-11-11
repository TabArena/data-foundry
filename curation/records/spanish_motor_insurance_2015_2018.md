---
unique_name: spanish_motor_insurance_2015_2018
name: Spanish motor insurance portfolio 2015-2018 (Lledó and Pavía, Mendeley 5cxyb5fp4f)
checked_by:
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Andrej
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

**Assessment (AI, 2026-11-01):** added as `datasets/_dev/tabarena-v0pt2/spanish_motor_insurance_2015_2018/` by /add-dataset with the full review panel; the open questions are in its Review. Recommend shipping; issue 1 (the task changed from renewal pricing to new-business pricing for customers with one policy) could still turn it to `No`. A policy's later yearly rows hold a remnant of earlier claims, not the year's own (0.9% have a claim after a claim-free year, against about a third of first years), so only first years are kept (25,665 rows, 5 monthly test windows of 2017). Changes after the panel: the 5,069 renewals never in force and `Payment` dropped, a 12-month gap before each window. Corrections to the notes above: PROV-6 and PROV-7 against the 2022-2024 sibling are settled as not a duplicate, closing the screening's call for the curator; "the zero is an observed claim-free policy-year" held for 83% of the zeros, not all (17% were years without cover). The screening's renewal use case and the Assessment's target and exposure lines wait for your mark on issue 1. Priority 3: gap + (insurance thin), use case 0 (fit approximate), source + (data article and variable sheet), shape + (25,665 rows, temporal), risk - (the premium alone ranks as well as any method; the task is open).

CC (2026-11-03, Andrej): the task as built is confirmed (issue 1 (A) in spanish_motor_insurance_2015_2018): each policy's first year, the pricing of a new contract, not renewal pricing over all policy-years.

CC (2026-11-03, Andrej): `Value_vehicle` stays (issue 3 (A)): "we can add to the comment that we assume that the value changes proportionally".

CC (2026-11-03, Andrej): no request to the authors now (issue 4): "Write a comment that we could do this for a future version, but now go with the task as we have it for simplicity".

**Assessment (AI, 2026-11-03):** the screening lines above describe renewal pricing over all policy-years; what ships is new-business pricing on each policy's first year (issue 1), so they are superseded.

CC (2026-11-03, Andrej): every first year is kept, with the customer's other policies in force at the start in place of the calendar-year count (issue 2, design S): "Good, we can ship S with 5 splits." Ship, re-checking `Trivial` on the first benchmark run (issue 5): "With design S we can ship."

CC (2026-11-03, Andrej): the check warning `task_target_value_dominant` accepted: "for these tasks this is natural and a core challenge" (zero-inflated target).

CC (2026-11-06, Lennart): issue 6 of the record's Review resolved. The task stays per contract under the exposure rules adopted this day (MET-14's per-contract clause, MET-15): every first year is a contract of exactly one calendar year, known at the quote (37,090 of 37,090), and `Premium` is the written annual premium, not prorated (Spearman -0.03 with the share of the year in force among the cut years), so no feature set after the quote carries the cut, while the quote-time factors predict it through risk selection; no weight and no offset. The count of first years cut short by a lapse is 2,055 of 37,090 (5.5%; 233 of the 4,362 test rows; 1,632 of them half-yearly payers who stopped paying, at a median of half the year), not the 1,236 that `fit_reason` gave: that was the count of the one-policy design (25,665 rows), left in the text when design S kept every first year (Andrej, 2026-11-03, issue 2). Per contract the cut years claim like full years (a claim in 35.4% of each), per year at risk 1.9 times as often (1.53 claims a year against 0.81). It confirms the per-contract target of issue 1 (Andrej, 2026-11-03); what keeps it per contract is the constant planned term, unlike fremtpl2 and bemtpl97, whose periods are realized lengths with no planned term.

**Assessment (AI, 2026-11-06):** review panel (focused, re-review under LEAK-41, MET-14 to MET-16): ship after changes, text only, applied in the notes (the CLEAN-11 counts, now 22 licences and 26 contracts dated after the year's start, the splits comment's test windows, 12 of whose 4,362 rows are not new contracts and stay, and the exposure paragraph's sentence on what carries the cut: no feature set after the quote carries it, and the quote-time factors predict it through risk selection, ROC AUC 0.71, mostly `Premium`); disputed: none between agents (no advocate or critic in this tier); for the curator: issues 7 (whether MET-14's per-contract clause covers the half-yearly payers who stop paying at six months, to settle once with australian_vehicle_insurance_2004_2005's issue on the same clause) and 8 (the wording "so no feature carries a cut" of the CC of 2026-11-06, left as written until then).

CC (2026-11-08, Lennart): the target stays the year's claim cost per contract (Review issue 7 (B), "Per contract, the clause amended"); MET-14's per-contract clause is amended for this case, its wording settled with australian_vehicle_insurance_2004_2005's issue 8 on the same clause. The mean share of the year in force is 0.992 for annual payers and 0.936 for half-yearly payers, so a price per year in force differs from the per-contract one by at most about 6% between the two groups.

**Assessment (AI, 2026-11-08):** applied in the definition: the exposure paragraph of the notes gives the 6% bound (re-computed on the 37,090 kept first years: 0.9923 for 24,470 annual payers, 0.9356 for 12,620 half-yearly payers) and names the amended clause without quoting its wording, which waits for australian_vehicle_insurance_2004_2005's issue 8. On the curator's mark of Review issue 8 (B), "Reword", the CC line of 2026-11-06 above was reworded in place: "so no feature carries a cut" now reads "so no feature set after the quote carries the cut, while the quote-time factors predict it through risk selection", as in the definition's CC bullet and issue 6's resolved turn. `dataset check`: 0 errors, 0 warnings.

CC (2026-11-08, Lennart): the declared metric (`normalized_gini`) is checked, as declared on the PR #47 review board.

CC (2026-11-09, Andrej): no column for the customer's earlier policy-years at the insurer; a note in the definition measures the gap (review issue 10, C: "Option C: A, with the gap measured in the notes").

**Assessment (AI, 2026-11-09):** recounted on the raw file with the definition's filters, the issue's numbers hold: 442 of the 4,362 test rows (10.1%) have an earlier policy-year under the same birth-date and licence-date key that ended by the quote; they claim in 26.9% of the cases after an earlier claim (182 rows) and 11.5% after claim-free years (260), against 38.0% without one (3,920); the training sides hold 15, 18, 24, 32 and 44 such rows (the windows of August to December 2017).

CC (2026-11-09, Andrej): columns held only for training rows stay out for now, no training-only role (cross-dataset item of 2026-11-09; MET-14, LEAK-41, MET-16); the notes list them.

CC (2026-11-09, Andrej): the training labels' maturity is stated in the notes (cross-dataset item of 2026-11-09, option B).

CC (2026-11-09, Andrej): a curation decision on the metric (Review issue 9, A; consistency check option (a)): "We keep A because it was how the Kaggle competition looked like. But note this decision as a curation decision." `normalized_gini` ordered by the prediction stays, each policy weighted 1, not the Gini against the premium. The source is a data article with no task and no metric, so the ground is the form of the insurers' Kaggle competitions (Allstate 2011, Liberty Mutual 2014) and the 2022-2024 sibling's call of 2026-11-02 (MET-11: a context metric names its basis); the use case now reads "to rank the risk and set the premium", as the sibling's, which is what this form scores (MET-1). Provisional; revisit with wisconsin_local_government_property_insurance_fund issue 4 and spanish_motor_insurance_coverage_level_2022_2024 issue 11: both were settled on 2026-11-09 with their metrics kept, so it stands.

CC (2026-11-09, Andrej): ship (review page of 2026-11-09).

## Review

**Outcome:** added. The AI recommends shipping it as built: the re-review of 2026-11-06 under the exposure rules found
no rule broken, and its text fixes are applied. On 2026-11-08 the target stayed per contract with the rule's
per-contract clause amended for this case (issue 7, wording settled with australian_vehicle_insurance_2004_2005's
issue 8), and the sentence of your CC on what carries the cut was reworded (issue 8). A sample of a Spanish non-life insurer's motor portfolio (Mendeley Data 5cxyb5fp4f version 2, CC BY
4.0; Segura-Gisbert, Lledó and Pavía 2025). One row is a policy's first year of cover in the release (37,090 rows),
and the target is that year's claim cost per contract (payments plus reserves), with no weight. It is shipped as log1p
and scored on the amount by the normalized Gini, a context metric. The split is temporal: 5 monthly test windows,
August to December 2017, each trained on the years that had ended by the window's start.

Validity:
- SEL-1 and SEL-2 hold.
- USE-1 holds for new-business pricing, fit approximate (USE-8; issue 1).
- USE-5 was triggered three times, each fixed without reading a label: the later yearly rows are dropped (issue 1),
  the years without cover are dropped (USE-7), and the calendar-year count of policies is replaced by the policies in
  force at the start (issue 2); whether claims are booked across a customer's policies stays a note.
- USE-6 holds for `Premium`.
- LEAK-10 was triggered: the end-of-policy columns, `Seniority` and `Payment` are dropped, and `Value_vehicle` is kept
  (issue 3).
- LEAK-41 holds: no weight ships, and the share of the year in force is no feature (as one it would add 0.011 mean
  Gini, up in 5 of 5 windows). The quote-time factors predict which first years a lapse cuts short at ROC AUC 0.71,
  mostly through `Premium`: risk selection, which stays.
- MET-14 holds by its per-contract clause: every first year has a planned term of one calendar year, and 2,055 of
  37,090 (5.5%) are cut short by a lapse (issue 6); the clause is amended to cover the half-yearly payers who stop at
  six months (issue 7, 2026-11-08; a price per year in force would differ by at most about 6%). MET-15 holds: no
  weight and no offset.
- MET-16 holds: the release has no survey or design weight (the sample's design is not described, a gap `fit_reason`
  names).
- SPLIT-9 and SPLIT-10 were triggered (training years not yet ended at the window's start), fixed by a 12-month gap;
  SPLIT-14 holds (53% to 73% of the rows train).
- PROV-6 and PROV-7 hold against `spanish_motor_insurance_coverage_level_2022_2024`: not a duplicate (other years,
  schema and task). PROV-13: no request to the authors now (issue 4).

Value: a small real signal (TP-2). TabPFN beats the premium alone in all 5 windows (mean Gini 0.221 against 0.162);
`Trivial` is re-checked on the first benchmark run (TP-4; issue 5). Every window can be scored (MET-2): 261 to 371
claims a window, and a constant scores 0.

Quality: the ages are computed by the calendar, impossible dates are made missing (CLEAN-11) and the fill values are
noted (CLEAN-10).

Weighed: documented source, licence and real decision +; thin signal beyond the premium, noisy monthly windows -.

Nothing is left open: issues 7 and 8 were settled on 2026-11-08 (Lennart); the amended clause's wording is written in
the rules with australian_vehicle_insurance_2004_2005's issue 8.

Changes made after the review panel of 2026-11-06 (AI), no decision needed; rows, features, target, metric and split
are unchanged: the CLEAN-11 counts are corrected (22 licences and 26 contracts dated after the year's start, not 12
and 8); the splits comment no longer says the test windows hold new contracts only (12 of their 4,362 rows are not,
and they stay) and gives 763 rows, not 766, for the smallest window; the exposure paragraph says that no feature set
after the quote carries the cut, and that the quote-time factors predict it through risk selection.

**Main points:** Nothing is open. Resolved: on 2026-11-09 the Gini ordered by the prediction kept as a curation
decision, on the ground of the insurers' Kaggle competitions and the 2022-2024 sibling, with the use case reworded to
match (9, A), and no column for the customer's earlier policy-years, the gap measured in a note (10, C); on 2026-11-03 first-year pricing (1), every first year kept with the
customer's other policies in force at the start (2, design S), `Value_vehicle` kept (3), no request to the authors now
(4), ship and re-check `Trivial` (5); on 2026-11-06 the per-contract target under the exposure rules, with the count of
first years cut short corrected to 2,055 (6); on 2026-11-08 the per-contract target with MET-14's clause amended for
this case, its wording settled with australian_vehicle_insurance_2004_2005's issue 8 (7), and the sentence of your CC
reworded (8).

**Verdict (2026-11-09, Andrej):** ship (review page of 2026-11-09).

**Issues for Andrej and Lennart:**

1. **Confirm the task as built: pricing a new contract from its first year, not renewal pricing over all policy-years?**

   * **Problem:**
     - Your `Yes` (2026-10-30) was given on renewal pricing over all policy-years, but a policy's later yearly rows do
       not record that year's claims.
     - So the definition keeps each policy's first year only, the pricing of a new contract.
     - Confirm the changed task, or retire the dataset?
   * **Background:** the screening's task: at renewal, an insurer sets next year's premium, with one row per
     policy-year. The release does not support that task. A policy's later yearly rows record a shrinking remnant of
     earlier claims, so a model trained on these rows would learn last year's claims, not next year's risk.
   * **Experiments:**
     - After a claim-free year, only 0.9% of the next years have a claim (133 of 14,980 years with cover), against
       about a third of first years.
     - After a year with claims, the count falls in 99.9% of cases.
     - Last year's count alone ranks the later rows at a Gini of 0.86.
     - The 2022-2024 release of the same research group shows 17.4% after a claim-free year, so the defect belongs to
       this release. That figure counts claims as here: a next year with a recorded claim after a year with none (of
       145,964 years). The 2022-2024 file's precedent check counts claim cost instead, a next year with a cost above 0
       after a year without one, and finds 14.6% (of 149,929 years); that release records some claims at zero cost. In
       this release the two counts coincide, since a year's cost is 0 exactly when its claim count is.
   * **Consistency:** rows whose label the data shows to be another quantity are dropped[^s1], as in rain_in_australia
     and ames_housing[^s2]. corporate_credit_rating was retired only because its bad labels could not be located; here
     they can be. Your `Yes` decides which task is built, so the changed task needs your confirmation.
   * **Effect on the task:** every test row is a new contract. Training also holds older contracts' first year in the
     release (a renewal, November 2015 to November 2016). The data mirrors the use case only approximately[^s3].
   * **Panel:** the blind reviewer flagged the mix of new and renewed contracts in training; the panel kept those rows
     for training, since the test rows are the ones the use case names.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Each policy's first year only (implemented) | every test row is a new contract; `use_case`: the insurer refines its quoted premium for a new contract[^s4] | labels are that year's claims; the data article names "pricing mechanisms for new business" among the uses (Sec. 1) | not the task your `Yes` was given on; training mixes in renewals |
     | B | Retire with `Data Quality Issue` | the dataset does not ship until the authors' raw data (issue 4) restores the renewal years | could come back as the renewal task | no dataset in the meantime |

   * **Recommendation:** A, confirm: a first year's label is that year's claims, and the data article names pricing
     for new business among its uses. **Decision:** confirm (A), or retire (B)?

   [^s1]: **USE-5** (Must): predict what the actor acts on, and check how the source built its label before accepting
     it; a label checked and found to be another quantity than the one the actor acts on still fails (Lennart,
     2026-10-21, diabetes_3).
   [^s2]: rain_in_australia and ames_housing (Lennart, 2026-10-26).
   [^s3]: **USE-8** (Must): write how closely the data mirrors the use case; approximate means a stand-in with a known
     gap, named as such.
   [^s4]: **USE-6** (Must): anything known at the prediction point is a legitimate input, including a number the
     company itself computed; a company's own estimate made before the outcome is an input, and the model refines it.

   **Resolved (2026-11-03, Andrej):** A, the task as built: each policy's first year, the pricing of a new contract.

2. **Keep only customers with no other policy at the insurer, or keep every first year with a note?**

   * **Problem:**
     - A policy's claims move with the claims of the same customer's other policies running at the same time.
     - If claims are booked across policies, rows with two or more policies carry the other policies' claims.
   * **Experiments:**
     - Among first years that have such a policy in the sample, 80% have a claim when that policy has one and 6% when
       it does not (2,493 rows; 35% across all first years).
     - Of the 1,532 such pairs (a first year and the same customer's other policy, overlapping by more than 180 days),
       1,519 insure different vehicles.
     - The link grows with the number of days the two years overlap. The same customer's years more than 180 days
       apart show only a mild link (21% against 12%).
     - For customers with no other policy in the sample, claims per row grow in proportion to `Policies_in_force`,
       the customer's number of policies: 0.65, 1.15, 1.61, 2.01 and 2.46 for 1 to 5 or more (over all first rows,
       the README's table gives 0.64 to 3.15).
     - The costs are not copies. Within a pair they are unrelated, and at every count each claimant row carries a
       full-size cost (863 to 1,002 on average).
   * **Effect on the task:** if claims are booked across policies, those rows are 31% of the rows and 45% of the test
     rows, and a model scores them by `Policies_in_force`. With every first year kept, almost all of a model's gain
     over the premium comes from that count (logistic regression, the mediator's run):

     | inputs | Gini |
     |---|---|
     | premium alone | 0.162 |
     | all features but the count | 0.168 |
     | premium and the count only | 0.228 |
     | all features | 0.233 |

     A tariff learned from these rows would charge customers with several policies for the way claims are booked.
   * **Unknown:** the release cannot say whether claims are booked to every policy of the customer, or whether such
     customers really claim together. Only the authors can (issue 4).
   * **Panel:**
     - The critic: a label checked and found to be another quantity still fails, so those rows go[^p1].
     - The advocate: the rule that assigns claims to policies is undocumented and each policy's money is its own, so
       the label ships as an approximate fit with a note (as diabetes_3)[^p2].
     - The mediator sided with the critic, for four reasons: the check was made; the pattern is the same kind as in
       issue 1 (found from the data, mechanism unknown, rows dropped); the remedy ladder puts a fix of the definition
       before a note[^p3]; and the origin has to be checked before a suspected damage is kept[^p4].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Customers with no other policy (implemented) | keeps the rows with `Policies_in_force == 1` (25,665 rows; 2,385 test rows, 117-195 claims per window) and drops the column, then constant; `use_case` names customers with no other policy | no row can carry another policy's claims | 31% of the rows and 45% of the test rows go, and the premium alone then ranks as well as any method tried (issue 5); the count covers the calendar year, so customers who add a policy later in the year go too (they claim at the same rate, 31.2% against 31.2%) |
     | B | Every first year, with a note | keeps all 37,090 first years; the `Policies_in_force` note says the count also tracks claims that occur together on a customer's policies; `fit_reason` names the gap | keeps every customer | a tariff learned from it charges for the way claims are booked; needs the authors' check first (issue 4) |

   * **Recommendation:** A, the filter, so that no row can carry another policy's claims; revisit it if the authors
     show that claims are booked per policy.
     **Decision:** filter (A), or note (B)?

   **Notes for the AI:** on B, the count loses the 2,865 policies written later in the year that can be found in the
   sample (LEAK-10 fixes a late value it can locate); the later policies outside the sample stay, under a
   `Potential leak, kept on purpose:` note; `fit_reason` names the gap. PROV-13 requires the authors' request
   (issue 4) before this note.

   [^p1]: **USE-5** (Must): a label checked and found to be another quantity than the one the actor acts on still
     fails (Lennart, 2026-10-21, diabetes_3).
   [^p2]: **USE-5** (Must): a label from a named publication whose construction is undocumented and cannot be
     checked may ship with `fit="approximate"` and a note naming the gap.
   [^p3]: The remedy ladder (principles.md): take the mildest remedy that resolves the problem: repair from the
     origin; fix the definition (drop, lag, filter, re-split, re-target); keep it with a documented note; exclude.
   [^p4]: **PROV-13** (Must): when a release is damaged, check whether the origin has the clean data before keeping
     the damage or retiring the dataset.

   **Andrej (2026-11-03, discuss):** This feels like something there could be better options for. We want to prevent
   leaks, have a task that is realistic, and at the same time use as many of our samples as possible. How can we
   achieve that best?

   **Answer (AI, 2026-11-03):**

   * **Problem:**
     - The best of the designs tried keeps every first year (37,090 rows, 45% more test rows) and replaces the
       insurer's calendar-year count by what is known when the contract starts: how many of the customer's other
       policies in the sample are in force that day.
     - It uses nothing from after the start, the split stays the same, and TabPFN beats the premium in all 5 windows.
     - What it does not settle is the label: if the insurer books a claim on every policy of a customer, the rows of
       customers with several policies carry claims of their other cars; only the authors could say.
   * **Why the old count leaks:** `Policies_in_force` counts the calendar year, so it includes policies a customer adds
     after the contract starts. Those customers claim at 48.9% in their first year, against 31.4% for customers with
     one policy and 22.8% for customers who already had another policy in force: adding a policy after a claim (a
     replacement car) would explain it, and a count that sees it reads the future.
   * **Experiments:** the 5 windows as shipped (August to December 2017, 12-month gap), normalized Gini on the amount;
     TabPFN with its default settings on a GPU (Slurm), untuned LightGBM beside it:

     | Design | Rows | Test rows per window | TabPFN | LightGBM | Premium alone | Windows TabPFN beats the premium |
     |---|---|---|---|---|---|---|
     | A: customers with one policy (implemented) | 25,665 | 477 | 0.185 | 0.165 | 0.234 | 1 of 5 |
     | E: train on every first year, test on one-policy customers | 37,090 | 477 | 0.169 | 0.130 | 0.234 | 1 of 5 |
     | C: every first year, no count | 37,090 | 872 | 0.171 | 0.119 | 0.162 | 2 of 5 |
     | S: every first year, other policies in force at the start | 37,090 | 872 | 0.221 | 0.146 | 0.162 | 5 of 5 |
     | B: every first year, the calendar-year count | 37,090 | 872 | 0.217 | 0.189 | 0.162 | 4 of 5 |

     - Within each kind of customer the premium still ranks about as well as TabPFN (one-policy customers 0.234 against
       0.162); design S's lead comes from ranking the kinds of customers against each other, by the count known at
       the start.
     - More training rows alone do not help the one-policy customers (E against A).
   * **Unknown:** whether claims are booked across a customer's policies. Rows with another policy running at the
     same time claim together (80% when that policy claims, 6% when not), yet those customers claim less overall.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Customers with one policy (implemented) | 25,665 rows, the count dropped | no row can carry another policy's claims | 31% of the rows go; the premium leads in 4 of 5 windows |
     | S | Every first year, count at the start | 37,090 rows; `Policies_in_force` replaced by the customer's other sampled policies in force at the start | all rows; nothing from after the start; TabPFN beats the premium in every window | if claims are booked across policies, some labels carry other cars' claims |
     | B | Every first year, the calendar-year count | as the panel's option B | all rows | the count sees policies added after a claim |

   * **Recommendation:** S: it meets all three of your aims, and the label question stays as a note until a later
     version asks the authors (issue 4). **Decision:** A, S or B?

   **Notes for the AI:** script `designs.py` (frames and LightGBM), `tabpfn_windows.py` and `tabpfn_subsets.py`
   (Slurm jobs 1342221 and 1342226) in the run folder of 2026-11-03 (spanish/). On S: build `other_policies_at_start`
   in `_clean` from the raw rows (a customer is a birth date and a licence date; another policy of the customer with
   cover on the row's start), drop `Policies_in_force`, rewrite the filter bullet, `use_case`, `row` and the notes,
   re-run `dataset check` and the leak probe on Slurm.

   **Andrej (2026-11-03, discuss):** How many different splits do we get that way?

   **Answer (AI, 2026-11-03):**

   * **Problem:**
     - Five, the same as now: one test window per month from August to December 2017.
     - Design S adds customers, not dates, so the windows stay where the 12-month gap and the rule that a window
       trains on at least half the rows put them; July 2017 would train on 45% of the rows (50% now).
     - What changes is the size of each window: about twice the test rows and claims.
   * **Experiments:** monthly windows, training on the rows that started at least 12 months before the window:

     | Window | Test rows now (A) | Claims now (A) | Test rows with S | Claims with S | Share of rows in training, S |
     |---|---|---|---|---|---|
     | 2017-12 | 569 | 195 | 973 | 371 | 73% |
     | 2017-11 | 477 | 153 | 922 | 337 | 71% |
     | 2017-10 | 538 | 149 | 938 | 325 | 64% |
     | 2017-09 | 393 | 117 | 763 | 261 | 58% |
     | 2017-08 | 408 | 136 | 766 | 276 | 53% |
     | 2017-07 (below the floor) | 479 | 130 | 885 | 284 | 45% |

     - More splits would need shorter windows (half months: about 10 windows of 400 to 500 rows under S) or a lower
       floor than the rule's half of the rows; neither adds data, and shorter windows are noisier.
   * **Recommendation:** unchanged, S, with the five monthly windows: the same splits, with twice the claims per test
     window. **Decision:** A, S or B?

   **Andrej (2026-11-03, discuss):** Good, we can ship S with 5 splits.

   **Resolved (2026-11-03, Andrej):** S. Every first year is kept (37,090 rows); `Policies_in_force` is replaced by
   `other_policies_at_start`, the customer's other sampled policies with cover running on the row's start; the five
   monthly windows stay. `use_case`, `row`, `known`, `changes`, `fit_reason`, the notes, the splits comment and the
   third decision are rewritten; `dataset check` and the leak probe re-run on Slurm.

3. **Keep `Value_vehicle`, a valuation of 31 December 2019?**

   * **Problem:**
     - The variable sheet gives the "Market value of the vehicle on 31/12/2019", a date after every year in the data.
     - It is one value per policy, a property of the vehicle.
     - A value looked up after the outcome stays only when the data shows it did not change, and you decide that case by
       case[^v1].
   * **Experiments:** it does not move with the claims (measured on the shipped rows):
     - the type, age, power, size and weight explain 97% of its log;
     - what is left of it after those characteristics ranks the policies with a claim at ROC AUC 0.497, no better than
       chance (0.492 for a cost over 2,000);
     - no vehicle was registered after its row's start;
     - dropping it costs nothing measurable: untuned LightGBM ranks the 5 windows at 0.140 without it and 0.116 with
       it, inside one window's noise (bootstrap SE 0.08-0.11).
   * **Consistency:** follows onlinenewspopularity (kept on a traced test)[^v2].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | kept with a `Potential leak, kept on purpose:` note and a condition to revisit it (a release with the value at each renewal); `fit_reason` names it as kept, not as a gap[^v3] | the data shows it does not move with the claims | a value dated after every year in the data |
     | B | Drop | `Value_vehicle` removed | no late value; costs nothing measurable | loses a property of the vehicle |

   * **Recommendation:** A, keep: the data shows it does not move with the claims. **Decision:** keep (A), or drop
     (B)?

   [^v1]: **LEAK-10** (Must): a feature holds only what existed at the prediction point; out go attributes looked up
     after the outcome, "unless the data shows they did not change". The curator decides that clause case by case
     (amended 2026-10-26).
   [^v2]: onlinenewspopularity: its counts read at a later pull were kept because the part that can be traced showed
     no gain (LEAK-10, Lennart, "go with (a)").
   [^v3]: **USE-8** (Must): a potential leak kept on purpose does not by itself make a fit approximate.

   **Andrej (2026-11-03, ok):** This should be fine, we can add to the comment that we assume that the value changes
   proportionally

   **Resolved (2026-11-03, Andrej):** A, kept; the note now says we assume the value changes in proportion between
   the year's start and the valuation date, so the 2019 value ranks the vehicles as their value at the time would.

4. **Ask the authors for their pre-cleaned raw data?**

   * **Problem:**
     - The article offers "the pre-cleaned raw data" (Sec. 1), which would show how claims are assigned to years and
       to a customer's policies.
     - That settles issue 2, and it could bring back the renewal years of issue 1 and the customers with several
       policies.
     - An agent cannot send the request: will you write to the authors?
   * **Effect on the task:** with the filters above, the damaged rows are dropped, not kept, so the request does not
     block shipping. It is required before the note of issue 2's option B[^a1].
   * **Consistency:**
     - No precedent. In the zero-inflated review you sent no requests for records whose data is only on request[^a2];
       this asks for the rows behind a table already released.
     - The 2022-2024 sibling's REVIEW.md asks nothing that this request would settle; ask about it too only if it
       turns out to be the same insurer, which neither article says.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Nothing sent yet (implemented) | the dataset ships on the filters of issues 1 and 2 | ships now | issue 2 stays unsettled |
     | B | Send it, ship in the meantime | you ask the authors; the dataset ships on the filters until they answer | could settle issue 2 and bring back the renewal years and the customers with several policies | needs you to write; an agent cannot send it |
     | C | No request | the filters stay for good | no effort | the renewal years and the customers with several policies stay out |

   * **Recommendation:** B, send it, and ship in the meantime: the answer could settle issue 2, and shipping does not
     wait on it. **Decision:** send it (B), or not (C)?

   [^a1]: **PROV-13** (Must): check the origin before keeping a damage or retiring a dataset.
   [^a2]: Zero-inflated review, policy question 8 (2026-10-30).

   **Andrej (2026-11-03, ok):** Write a comment that we could do this for a future version, but now go with the task as
   we have it for simplicity

   **Resolved (2026-11-03, Andrej):** A, no request now; the notes say a future version could ask the authors for the
   pre-cleaned raw data and bring back the renewal years and the customers with several policies.

5. **Ship now and re-check `Trivial` on the first benchmark run, or hold until tuned results exist?**

   * **Problem:**
     - `Trivial` means that one raw input matches or beats the methods in every test window[^t1].
     - Here that input is `Premium`, the insurer's own price and the natural core of a pricing task[^t2].
   * **Experiments:**
     - On the shipped design (normalized Gini, mean of the 5 windows), the premium alone ranks at 0.234, ridge and
       logistic models at 0.230, and a LightGBM tuned on an inner time split at 0.176. The premium leads the best
       method in 3 of 5 windows and loses October and August.
     - With every first year kept, it leads in 1 of 5 (0.162 against 0.235), but there the gain comes from
       `Policies_in_force` (issue 2).
     - These models are proxies. The benchmark's tuned methods have not run[^t3].
   * **Consistency:** `Trivial` is not proven on either design, and a task stays until a concrete reason to retire it
     is found[^t4]. This reads the `Trivial` rule as wisconsin_local_government_property_insurance_fund (this run) and
     sepsis_survival did.
   * **Panel:** the critic would call the dataset `Trivial` unless tuned methods beat the premium in every window,
     which reverses the rule's burden of proof. Both sides asked for tuned results before shipping.
   * **For your weighing:** whichever design ships, the dataset mostly tests how well a model uses the insurer's own
     premium. The other rating factors add little beyond it.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Ship and re-check (implemented) | on the first benchmark run, retire it as `Trivial` if the premium alone matches or beats the tuned methods in every window | the burden of proof stays on `Trivial` | ships before the tuned results both sides asked for |
     | B | Hold | kept out of the collection until the benchmark's tuned methods have run on this dataset alone | tuned results before shipping | the dataset waits for a separate run |

   * **Recommendation:** A, ship and re-check: `Trivial` is not proven, and a task stays until a concrete reason to
     retire it is found. **Decision:** ship and re-check (A), or hold (B)?

   [^t1]: **TP-4** (Must): `Trivial` needs proof. Read what the dominant feature means first: the natural core of a
     task (a listed price for a sale price) is expected to dominate. Then the raw feature has to match or beat the
     methods fold by fold.
   [^t2]: **USE-6** (Must): anything known at the prediction point is a legitimate input, including a number the
     company itself computed; the model refines it.
   [^t3]: **TP-1** (Must): a flag is a question, not a verdict; the probes fit untuned models, so check every flag
     against the benchmark's tuned methods before acting on it.
   [^t4]: **TP-2** (Should): a small but real signal is no reason to retire; retire, fix or keep a task for a
     concrete reason found in the task itself, and until one is found, the task stays.

   **Andrej (2026-11-03, discuss):** Do the necessary analysis. You can also use a better model like TabPFN, trained on
   a GPU to test this

   **Answer (AI, 2026-11-03):**

   * **Problem:**
     - TabPFN (default settings, on an A100) does not beat the premium alone on the shipped design: 0.185 against
       0.234 over the 5 windows, ahead only in August.
     - It is not `Trivial` by the rule, which needs the premium to match or beat the methods in every window, but it
       is close.
     - On design S of issue 2 TabPFN beats the premium in every window (0.221 against 0.162).
   * **Experiments:** per window, normalized Gini on the amount:

     | Window | Premium alone (A) | TabPFN (A) | Premium alone (S) | TabPFN (S) |
     |---|---|---|---|---|
     | 2017-08 | 0.199 | 0.281 | 0.177 | 0.330 |
     | 2017-09 | 0.311 | 0.275 | 0.244 | 0.277 |
     | 2017-10 | 0.408 | 0.288 | 0.258 | 0.275 |
     | 2017-11 | 0.129 | 0.027 | 0.076 | 0.135 |
     | 2017-12 | 0.123 | 0.052 | 0.054 | 0.086 |

     - On one-policy customers the premium stays ahead under either design (0.234 against 0.162 to 0.185), so a model
       adds little to the insurer's own price for them.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Ship and re-check (implemented) | re-check `Trivial` on the first benchmark run | a tuned method beats the premium in at least one window | on design A the premium leads in 4 of 5 windows |
     | B | Hold | wait for the benchmark's tuned methods | tuned results first | the dataset waits |

   * **Recommendation:** A, ship and re-check, best together with design S of issue 2, where TabPFN beats the premium
     in every window. **Decision:** A or B?

   **Andrej (2026-11-03, discuss):** With design S we can ship.

   **Resolved (2026-11-03, Andrej):** A, ship with design S and re-check `Trivial` on the first benchmark run; the
   notes give the TabPFN and premium scores per window.

6. **Keep the claim cost per contract under the exposure rules, with the count of first years cut short corrected?**

   * **Problem:**
     - The exposure rules adopted on 2026-11-06 ship a cost that accrues over a varying time at risk as a rate per
       year, weighted by that time, unless every contract has the same planned term, known when it is priced[^e-rate].
     - 2,055 of the 37,090 first years end early by a lapse, while `fit_reason` still gave 1,236, the count of the
       earlier design that kept only customers with one policy (25,665 rows).
   * **Background:** Every first year in the table is a contract of exactly one calendar year: `Date_next_renewal`
     falls one calendar year after the year's start in all 37,090 rows. A lapse inside the year is known only when
     the policy ends, so `Date_lapse` is no input[^e-late]; 1,632 of the 2,055 lapses are half-yearly payers who
     stopped paying, at a median of half the year. `Premium` is the written annual premium, not prorated.
   * **Effect on the task:** None: rows, target, metric and split stay. The cost per contract carries the claims of
     the contracts that lapse, as the annual contract the insurer prices does.
   * **Experiments:** On the shipped rows (the exposure study of 2026-11-05, re-run for this issue):
     - Per contract the cut years claim like full years: a claim in 35.4% of each, 0.78 claims against 0.81.
     - Per year at risk they claim 1.9 times as often: 1.53 claims a year against 0.81.
     - Among the cut years the premium does not move with the share of the year in force (Spearman -0.03), so no
       feature tells a cut year apart; 233 of the 4,362 test rows are cut years.
   * **Consistency:** fremtpl2 and bemtpl97 became rates per year insured on the same day, as their periods are
     realized lengths with no planned term; pricing_game_2017_french_mtpl keeps whole policy-years, each present in
     every year's file.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Per contract (implemented) | the year's claim cost per first year, unweighted; the count corrected | one planned term for every contract; no feature carries the cut | the 2,055 cut years count as whole contracts |
     | B | Cost per year at risk, weighted | the cost over the share of the year in force, that share the metric's weight and the training weight | the actuarial rate | a rate over a term every contract shares; the decision prices a contract |
     | C | Drop the cut years | full years only | no cut years | selects rows by a length the outcome cuts[^e-select] |

   * **Recommendation:** A: the contract is priced for one calendar year, so its claim cost is what the insurer acts
     on. **Decision:** A, B or C?

   [^e-rate]: **MET-14** (Should, 2026-11-06): a count or amount over a varying amount at risk ships as the rate per
     unit; "A per-contract target stays when the planned term is constant and known at the prediction point; the notes
     give the share cut short (spanish_motor_insurance_2015_2018: 2,055 of 37,090)." **MET-15** (Must): when the
     decision is per contract, the target is scored unweighted and no sample weight is declared.
   [^e-late]: **LEAK-10** (Must): a column recorded after the outcome is no feature.
   [^e-select]: **LEAK-41** (Must): no model is trained or scored on rows selected by the realized weight, such as
     full-year rows only.

   **Resolved (2026-11-06, Lennart):** A, per contract (MET-14's per-contract clause, MET-15): every first year is a
   contract of one calendar year and the premium is the written annual premium, so no feature set after the quote
   carries the cut, while the quote-time factors predict it through risk selection. `fit_reason` now gives 2,055 of 37,090 first years cut short by a lapse (1,632 half-yearly payers who stopped
   paying), not the 1,236 of the earlier one-policy design; the notes carry the exposure paragraph. Per contract the
   cut years claim like full years, per year at risk 1.9 times as often. `dataset check`: 0 errors, 0 warnings
   (`splits_rows_unused` accepted: the 5,685 first years in every window's 12-month gap).

7. **Does the per-contract target still hold for the half-yearly payers who stop paying at six months?**

   * **Problem:**
     - The target stays the claim cost per contract under a rule clause that keeps a whole contract's cost when every
       contract has the same planned term, known at the quote[^m1], and this dataset is the clause's only example, so
       the rule cannot check the case on its own.
     - 1,632 of the 2,055 first years cut short are half-yearly payers who stopped paying, 1,353 of them exactly six
       calendar months in, so they paid about half of their annual premium, which reads as revenue earned in
       proportion to the time in force (the insurer's rule on a lapse is not published), the case for which the rules
       name a rate weighted by that time[^m2].
     - Keep the per-contract target as the rule reads now, amend the clause to say why it holds here, or switch to the
       cost per year in force with a weight?
   * **Background:**
     - Per contract, the target is the claim cost of the whole contract, which the insurer prices for one year; a
       rate divides that cost by the share of the year the policy ran, and weights each row by that share in training
       and scoring.
     - Every first year here has a planned term of exactly one calendar year (37,090 of 37,090 rows). A lapse inside
       the year is known only when the policy ends, so it is no input[^m3].
     - As written, the rules do not conflict: the weight is required only once the target is a rate, and the clause
       keeps this one per contract[^m2]. The open point is whether the clause's condition is enough when the revenue
       on a cut contract is earned pro rata, a choice of how the rule is written.
   * **Effect on the task:** small on prices: the mean share of the year in force is 0.992 for annual payers and 0.936
     for half-yearly payers, so a price per year in force would put the half-yearly payers at most about 6% higher
     against the annual payers than the cost per contract does. How far it reorders models is not measured (Unknown).
     233 of the 4,362 test rows are cut years, and nobody knows at the quote which they will be.
   * **Experiments:** on the shipped rows, matched to the container row by row (the claim auditor):
     - Per contract the cut years claim like full years: a claim in 35.4% of each, 0.78 claims against 0.81.
     - Per year at risk they claim 1.9 times as often: 1.53 claims a year against 0.81.
     - With the rating factors held equal, half-yearly payers pay about 20% more premium, and 12.9% of their first
       years are cut short against 1.7% of annual payers'. A cut year carries 3.5% more premium (standard error 0.8%)
       than a full one with the same factors and payment method, so the premium is the written annual premium, not
       prorated.
   * **Consistency:**
     - fremtpl2, bemtpl97, frempl_french_motor_personal_line and pricing_game_2016_french_fleet ship a rate weighted by
       the time at risk: their periods are realized lengths with no planned term. Here every contract has the same
       planned term.
     - spanish_motor_insurance_coverage_level_2022_2024 ships a weighted rate: its rows are calendar years with
       mid-year starts, its premiums are earned pro rata and annualised, and the rate was Andrej's call (2026-11-02).
       If the half-yearly lapses here count as premium earned pro rata, the planned term is the only fact left that
       sets this dataset apart from it.
     - australian_vehicle_insurance_2004_2005 asks about the same clause from the other side (its issue 8): its
       planned term is one year too, yet 98.1% of its policies are observed only part of the year, so the rate ships
       there. Settle the clause once for both.
   * **Unknown:** the insurer's rule for the premium it keeps on a lapse is not in the article. Whether the 20% that
     half-yearly payers pay is a surcharge for paying in instalments (the lapse risk priced into the contract) or
     selection, the data cannot tell. A re-score on the shipped windows would show whether the two targets rank models
     differently; it was not run.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Per contract, the rule as written (implemented) | nothing changes | one planned term for all 37,090 contracts; per contract the cut years claim like full years; the gap is at most about 6% | the clause's only example is this dataset; the rule does not say why revenue earned pro rata on a cut leaves the target per contract |
     | B | Per contract, the clause amended | the notes' exposure paragraph gets the 6% bound; the clause says that a cut known only at the policy's end and priced into the contract (a surcharge for paying in instalments) does not make the target a rate | the rule says why this case stays per contract; one amendment can also settle australian's issue | a rule changed on one dataset's evidence; that the surcharge prices the lapse is an inference |
     | C | Cost per year in force, weighted | the target becomes the cost over the share of the year in force, and that share the weight of the Gini and of training; issue 6 reopens | the actuarial rate; the revenue on 1,632 contracts is earned pro rata; as the 2022-2024 sibling | divides by a time in force nobody knows at the quote, though every contract is planned for one year; the decision prices a whole contract |

   * **Recommendation:** B: the per-contract target stays on the evidence (one planned term, a gap of at most about
     6%, a cut nobody knows at the quote), and the amended clause states why, so the rule can be checked without this
     dataset[^m4]; write it together with australian's issue on the same clause. **Decision:** A, B or C?

   **Notes for the AI:** on B, add one sentence to the exposure paragraph of `curation_comments`: "The mean share of
   the year in force is 0.992 for annual payers and 0.936 for half-yearly payers, so a price per year in force differs
   from the per-contract one by at most about 6% between the two groups." Amend MET-14's per-contract clause in
   `metrics.md` with the curator's wording, in one change with australian_vehicle_insurance_2004_2005's issue on the
   same clause (its issue 8, option C: "... known at the prediction point and observed in full for most rows"),
   and update the clause's Cases row; re-run `dataset check`. On C: the share of the year in force as a
   `ScoringColumn(role="weight")` and the `sample_weight`, the target the cost per year in force (log1p, as the
   2022-2024 sibling), `normalized_weighted_gini` with the `weight` input, `_clean` asserting that the target times the
   share rebuilds the cost, probe 22, and a turn on issue 6 that reopens it. The numbers: the claim auditor's audit2 to
   audit5 in the panel folder of the exposure review (2026-11-06); the percentages are from log coefficients 0.180
   (standard error 0.004) and 0.034 (0.008), re-run with more digits.

   [^m1]: **MET-14** (Should, 2026-11-06, Lennart): a count or amount accrued over a varying amount at risk ships as
     the rate per unit when the decision prices per unit; "A per-contract target stays when the planned term is
     constant and known at the prediction point; the notes give the share cut short (spanish_motor_insurance_2015_2018:
     2,055 of 37,090)."
   [^m2]: **MET-15** (Must, 2026-11-06, Lennart): "When a rate target's denominator is realized and the decision's
     quantity is a sum over it (a premium earned pro rata, a book's claims), the denominator is the metric's row
     weight ... and the task's `sample_weight`, never a feature"; "When the decision is per unit of an equal-area map,
     per loan or per contract, the rate is scored unweighted and no sample weight is declared."
   [^m3]: **LEAK-10** (Must): a column recorded after the prediction point is no feature, so `Date_lapse` stays out.
     **LEAK-41** (Must, 2026-11-06, Lennart): a weight, or a column that encodes it, set or cut after the prediction
     point is never a model input; a feature known at the prediction point that predicts it through risk selection
     stays.
   [^m4]: Principles, "Exceptions and amendments": an amendment replaces a rule's text in place under the same ID, with
     the date, the curator and the case that prompted it; an exception departs from a Should rule for one dataset and
     names the fact that sets the case apart.

   **Resolved (2026-11-08, Lennart):** B, the target stays per contract and MET-14's per-contract clause is amended for
   this case; its wording is written once with australian_vehicle_insurance_2004_2005's issue 8 on the same clause,
   still open. The notes' exposure paragraph gives the 6% bound (mean share of the year in force 0.992 for annual
   payers, 0.936 for half-yearly payers, re-computed on the 37,090 first years) and names the amendment; the record has
   the CC line. `dataset check`: 0 errors, 0 warnings.

8. **Reword the sentence "so no feature carries a cut" in your CC of 2026-11-06?**

   * **Problem:**
     - Your CC gives as the reason that the premium is the written annual premium, "so no feature carries a cut", but
       the features known at the quote predict which first years a lapse cuts short at ROC AUC 0.71, mostly through
       `Premium`.
     - What the data shows is narrower and leaves your decision as it is: no feature set after the quote carries the
       cut, and the quote-time factors predict it through risk selection, which the rules allow[^w1].
     - An AI does not rewrite a curator's CC[^w2], so the wording is yours: reword it, add a dated correction, or leave
       it?
   * **Background:**
     - A cut year is a first year that a lapse ends before its planned year is over; a feature carries the cut when a
       model can read from it that the year was cut short.
     - The sentence stands in three places: the CC bullet of the definition's notes and the record's CC line ("so no
       feature carries a cut"), and the resolved turn of issue 6 above ("so no feature carries the cut").
     - The exposure paragraph of the notes (the AI's text) and the rule's Cases row already give the narrower statement
       (changed today).
   * **Effect on the task:** none: the rows, features, target, metric and split stay; only the stated reason changes.
   * **Experiments:** a LightGBM of the cut on the 18 shipped features, cross-fitted (5 folds, 3 seeds; the claim
     auditor):
     - ROC AUC 0.711 (standard deviation 0.002), 0.678 without `Premium`, 0.709 without `Value_vehicle`.
     - With the rating factors held equal, half-yearly payers pay about 20% more, and 12.9% of their first years are
       cut short against 1.7% of annual payers'.
     - The share of the year in force itself, as a feature, would add 0.011 mean Gini (higher in 5 of 5 windows): the
       leak your sentence guards against is real, and no shipped feature carries it.
   * **Consistency:** spanish_motor_insurance_coverage_level_2022_2024 notes the same kind of fact: its features rank
     the cancellations at ROC AUC 0.77, mostly through the payment frequency, kept as a note.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Your words as they are (implemented) | the CC lines stay; the exposure paragraph above the CC bullet gives the narrower statement | your words untouched | the notes state the reason twice, once wider than the data |
     | B | Reword | "so no feature carries a cut" ("the cut" in issue 6's turn) becomes "so no feature set after the quote carries the cut, while the quote-time factors predict it through risk selection" in the definition's CC bullet, the record's CC line and issue 6's resolved turn | the reason stated once, as the data shows it | your words change |
     | C | Your words with a dated correction | an AI line under the record's CC line and under the definition's CC bullet gives the narrower statement | your words untouched; the correction is visible | the wider statement stays in three places |

   * **Recommendation:** B: your decision is unchanged, and the notes and the record then give its reason once, as the
     data shows it. **Decision:** A, B or C?

   **Notes for the AI:** on B, with the curator's approval, replace "so no feature carries a cut" by "so no feature set
   after the quote carries the cut, while the quote-time factors predict it through risk selection" in the CC bullet
   of `curation_comments` (`dataset.py`) and the record's CC line of 2026-11-06 (through the store API), and "so no
   feature carries the cut" in issue 6's resolved turn; re-run `dataset check`. On C, append to the record an
   Assessment line of the day: "the CC of 2026-11-06 says "so no feature carries a cut"; the data shows that no feature
   set after the quote carries it, and that the quote-time factors predict it through risk selection (ROC AUC 0.71,
   mostly `Premium`), which LEAK-41 and USE-6 allow", and add the same as a `Note (AI, <date>):` bullet after the CC
   bullet of the notes.

   [^w1]: **LEAK-41** (Must, 2026-11-06, Lennart): a column the task uses as a weight, set or cut after the prediction
     point, is never a model input, nor a column that encodes it; "a feature known at the prediction point that
     predicts the weight through risk selection stays (USE-6)". **USE-6** (Must): anything known at the prediction
     point is a legitimate input, including a number the company itself computed.
   [^w2]: Records, "Who wrote a comment line": a `CC` line is the curator's decision with its reasoning; the AI never
     deletes a comment line, and marks a statement it no longer holds with a dated `Assessment (AI, ...)` line.

   **Resolved (2026-11-08, Lennart):** B, on your mark the sentence was reworded in place in the three places: "so no
   feature set after the quote carries the cut, while the quote-time factors predict it through risk selection" now
   stands in the definition's CC bullet, the record's CC line of 2026-11-06 (through the store API) and issue 6's
   resolved turn; the decision is unchanged.

9. **Score the claim cost against the premium charged, with `Premium` kept as a feature?**

   * **Problem:**
     - The metric orders the policies by the prediction alone, each weighted 1 (dataset.py:198-211), while the use
       case is to find the risks the quote prices too high or too low (dataset.py:87-91) and the metric's own reason
       cites the Gini that orders policies by the ratio of a score to the premium (dataset.py:203-206).
     - As declared, a model also earns credit for the risk the insurer's own price already ranks: the premium alone
       scores a mean normalized Gini of 0.162 over the five windows (dataset.py:185).
     - Switch to the Gini against the premium, read from a scoring copy of `Premium`, with `Premium` kept as a
       feature, as wisconsin_local_government_property_insurance_fund scores against its fund's premium?
   * **Background:**
     - The Gini against the premium (Frees, Meyers and Cummings 2011; `ordered_lorenz_gini` in the library) sorts the
       policies by prediction over premium and sets the cumulative share of the claim cost against the cumulative
       share of the premium. A prediction proportional to the premium scores 0, and a positive score means the model
       finds policies whose cost outruns their price. It is not normalized.
     - `Premium` is the year's net premium, set at the quote and kept as a feature on your call[^s9a]. A metric input
       that is also a valid feature stays a feature and ships a second time as a scoring column, so no metric reads a
       feature[^s9b], as liberty_mutual_fire_peril_loss_cost's `var11_weight` copies `var11`.
     - The metric reads each prediction on the amount, after the inverse of log1p. Under a ratio to the premium the
       size of a prediction counts, not only its order: wisconsin ships dollars for that reason (its issue 2), and the
       log1p scale here was chosen under the declared Gini (dataset.py:174).
   * **Effect on the task:** the score then credits only what a model adds to the insurer's price, which is the
     decision of the use case; echoing the premium scores 0 in every window instead of 0.162. Rows, features and
     split stay.
   * **Experiments:** counted on the raw file, the five shipped windows, no model fitted:

     | Window | Premium alone, Gini as declared | Premium alone, Gini against the premium | Constant, Gini against the premium |
     |---|---|---|---|
     | 2017-08 | 0.177 | 0.000 | 0.116 |
     | 2017-09 | 0.244 | 0.000 | 0.025 |
     | 2017-10 | 0.258 | 0.000 | 0.017 |
     | 2017-11 | 0.076 | 0.000 | 0.168 |
     | 2017-12 | 0.054 | 0.000 | 0.169 |

     - A constant orders the policies by the inverse of their premium and scores 0.099 on average: in the test
       windows the dearest fifth of the policies runs a loss ratio of 0.73, against 0.97 to 1.16 for the other
       fifths. So the level a model has to beat is above 0.
     - TabPFN (mean 0.221 as declared) and LightGBM were not re-scored under the Gini against the premium.
   * **The re-check of issue 5:** your call of 2026-11-03 ships the dataset and re-checks `Trivial` on the first
     benchmark run (dataset.py:185). B does not settle that re-check by itself; it changes its yardstick. The premium
     alone then scores 0 by construction, so the re-check asks whether a tuned method beats the best single input
     under the new metric (a constant already scores 0.025 to 0.169) in at least one window.
   * **Consistency:**
     - wisconsin_local_government_property_insurance_fund scores the same Gini against its premium, the source's
       metric there, and keeps the premium out of the inputs; its issue 4, raised today, asks whether to ship it as a
       feature with a copy as the base, which would make the two tables alike.
     - spanish_motor_insurance_coverage_level_2022_2024 keeps its premiums as features and scores the actuarial Gini
       ordered by the prediction and weighted by exposure, on Andrej's call of 2026-11-02; its metric reason names
       both forms. Under B the two Spanish tables are scored in different forms unless that one follows.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Gini ordered by the prediction (implemented) | `normalized_gini`, each policy weighted 1, as now | the form the insurers' Kaggle competitions took; nothing to re-measure | credits the ranking the premium already gives (0.162 for the premium alone); departs from the reference its own reason cites |
     | B | Gini against the premium, `Premium` still a feature | `ordered_lorenz_gini` on a scoring copy `premium_base`; the target stays log1p | scores the decision of the use case; echoing the premium scores 0; as wisconsin | not normalized, and a constant scores 0.099; the log1p scale was chosen under the old metric; the Spanish siblings then differ |
     | C | B with the target in euros | as B, and the target ships as the amount, untransformed | the ratio reads each prediction's size, which a fit on the amount targets, as wisconsin's dollars | a scale change on top of the metric change, not yet measured |

   * **Recommendation:** B: the use case is to find the risks the quote misprices, which is what the Gini against the
     premium scores[^s9c], and the premium stays an input as you decided; the scale is re-measured under the new
     metric before it ships, and C follows only if the amount does clearly better. **Decision:** A, B or C?

   **Notes for the AI:** on B, in `_clean` add `df["premium_base"] = df["Premium"]` (all positive, the smallest
   40.14); `scoring_columns = (ScoringColumn(column="premium_base", role="weight", used_by="ordered_lorenz_gini",
   description=...),)`; `Metric.from_context("ordered_lorenz_gini", reason=..., target_transform="log1p",
   inputs={"weight": "premium_base"})`. Rewrite the metric reason (the Frees, Meyers and Cummings form; the
   constant's 0.025 to 0.169), the `Premium` bullet of the notes (dataset.py:185: the premium alone now scores 0, so
   the comparison with TabPFN is restated) and `task_summary.predicted`. MET-2's sentence "A value the models must
   not get (a rating's output such as a premium, ...) is a scoring column only" needs wording that keeps the actor's
   own quote a feature; settle it with wisconsin's issue 4. Re-run `dataset check` and the task probes, then through
   sbatch on a GPU partition TabPFN and a Tweedie LightGBM, fit on log1p and on the amount, on the 5 windows under
   the new metric; on C also drop `target_transform` and rename the target. The baseline counts:
   `_ordered_lorenz_gini` and `_normalized_gini` of `data_foundry.v2.metrics` on the shipped test windows.

   **Andrej (2026-11-09, as implemented):** We keep A because it was how the Kaggle competition looked like. But note this decision as a curation decision.

   **Consistency check (AI, 2026-11-09): Keep A on the ground of the insurers' Kaggle competitions and the 2022-2024 sibling, with the use case reworded to match?**
   * **Problem:**
     - This dataset had no Kaggle competition: it comes from a data article (European Actuarial Journal 15:241-253,
       2025) and its Mendeley record, which name no task and no metric (dataset.py:201-203), so the reason as written
       would not hold in the record.
     - What does support A: the metric's reason cites the form the insurers' own Kaggle competitions took (Allstate
       2011, Liberty Mutual 2014: the losses ordered by the prediction, each policy weighted 1), and your call on the
       2022-2024 sibling (2026-11-02) scores the same way[^s9d].
     - The use case here reads "to find the risks the quote prices too high or too low", which is what B scores; the
       sibling's reads "to rank the risk and set the premium", which is what A scores.

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | A, the reason restated | the metric stays; the recorded decision names the insurers' Kaggle competitions and the 2022-2024 sibling as its ground; the use case reworded to "to rank the risk and set the premium", as the sibling's; the sibling's issue 11 decided the same way | your A, with a reason that holds; use case and metric agree; the two Spanish tables match | the premium alone still scores 0.162 as declared |
     | b | B | the Gini against the premium, as wisconsin | scores the use case as now written | departs from your A |

   * **Recommendation:** a: it keeps your call and records it on the ground that holds. **Decision:** a or b?

   **Resolved (2026-11-09, Andrej):** a (marked as implemented on the review page of 2026-11-09, no new note): A stays,
   `normalized_gini` ordered by the prediction, each policy weighted 1. The metric reason now states its ground: the
   source is a data article with no task and no metric, so the form follows the insurers' Kaggle competitions (Allstate
   2011, Liberty Mutual 2014) and the 2022-2024 sibling's call of 2026-11-02. The use case reads "to rank the risk and
   set the premium", as the sibling's. Recorded as a curation decision (a CC in the notes and the record). It was
   provisional until wisconsin_local_government_property_insurance_fund issue 4 and the sibling's issue 11 were
   decided; both kept their metrics on 2026-11-09, so it stands.

   [^s9d]: **MET-11** (Must): a `context` metric names its basis; here the form of the insurers' Kaggle competitions,
     since the source names none (**MET-4** on a competition's own metric does not apply). **MET-1** (Must): the
     metric scores the decision of the use case, so the use case's wording and the metric agree under a.

   [^s9a]: **USE-6** (Must): anything known at the prediction point is a legitimate input, including a number the
     company itself computed. **TP-4** (Must): the natural core of a task (a listed price for a sale price) is
     expected to dominate. Andrej, 2026-11-03, issue 5: ship with design S and re-check `Trivial` on the first
     benchmark run.
   [^s9b]: **MET-2** (Must; amended 2026-11-02, Andrej; reworded 2026-11-05, Lennart): "An input that is also a valid
     feature, known at the prediction point for train and test rows alike, stays a feature and ships a second time as
     a scoring column, a copy the metric reads"; the same rule adds "A value the models must not get (a rating's
     output such as a premium, or a realized amount at risk) is a scoring column only", which wisconsin applies to its
     premium. The rule is in main.
   [^s9c]: **MET-1** (Must): the declared metric scores the real task, the decision of the use case, the way a
     practitioner would have chosen a model for it. **MET-11** `context`: with no source metric, the metric the task
     makes obvious.

10. **Give the customer's earlier policy-years at the insurer as features at the quote?**

   * **Problem:**
     - When a customer with earlier policies at the insurer takes a new contract, the insurer knows how those
       policies' years went, but the only history the table gives is the count of the customer's other policies
       running at the start (dataset.py:172).
     - Counted on the raw file, 442 of the 4,362 test rows (10.1%) have an earlier policy-year of the same customer
       that ended before the quote, and they claim in 26.9% of the cases after an earlier claim against 11.5% after
       claim-free years (38.0% for the rows without one).
     - Ship that history as features, although the training sides hold it in only 15 to 44 rows per window (the
       release starts in November 2015, so a training row's earlier years are not in it)?
   * **Background:**
     - No customer id is published: the definition takes a customer to be a birth date and a driving-licence date,
       the key `other_policies_at_start` already uses (your design S of issue 2). Counted on the raw file, the
       policies under one key share the area and the sales channel in 98.7% of the keys, against 60% and 50% for
       random pairs of policies, so most links are one customer; false links would gather on dates such as 1
       January (1.5% of the birth dates and 1.6% of the licence dates).
     - An earlier policy-year counts when it ended, at its renewal or a lapse, on or before the new contract's start.
       The claim flag reads only the other policies' first years, since a later row holds a remnant of the first
       year's claims (dataset.py:170).
     - The audit of 2026-11-09 counted 486 rows (11.1%; 27.3% against 10.6%): it also counted as earlier years the
       renewals that never came into force, which the table drops (dataset.py:169).
   * **Effect on the task:** in deployment the insurer prices a returning customer with its record; the benchmark's
     models would meet the history almost only in the test rows. Per window the training side holds 15, 18, 24, 32
     and 44 rows with an earlier policy-year (August to December), the test window 72 to 103.
   * **Experiments:** counted on the raw file, the 4,362 test rows, no model fitted:
     - Among customers with another policy running at the start, an earlier claim gives 28.6% (140 rows), claim-free
       earlier years 11.3% (177), no earlier year 28.0% (254), so the history adds to `other_policies_at_start`.
     - Among customers without one: 21.4% (42), 12.0% (83) and 38.7% (3,666).
   * **Unknown:** whether part of the 26.9% is a remnant of an earlier claim booked onto the new policy. The release
     cannot tell claims booked across a customer's policies from customers who claim together (dataset.py:172), and a
     policy's later rows carry a remnant of its first year's claims (dataset.py:170).
   * **Consistency:** a known entity's history is legitimate and its previous outcome a feature[^s10a];
     wisconsin_local_government_property_insurance_fund's issue 5, raised today, asks the same for a member's earlier
     years, where the training sides hold that history from 2007 on.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | No customer history | only `other_policies_at_start`; `fit_reason` names the driver's claims history as missing | no feature the training sides lack; no claim flag on an inferred key | holds back what the insurer knows of a returning customer (10.1% of the test rows) |
     | B | Earlier policy-years as features | `earlier_policy_years` (count) and `earlier_claim` (any claim in their first years), by the birth-date and licence-date key, missing without a known key | the history the insurer has at the quote; 26.9% against 11.5% | 15 to 44 training rows per window hold it, so a model meets it almost only in the test rows; rests on an inferred key; a claim booked across policies would read as history |
     | C | A, with the gap measured in the notes (implemented) | no new column; a notes bullet gives the share of test rows with earlier years, their claim shares and why no column ships | the gap is stated; no column a model cannot learn | the information stays out |

   * **Recommendation:** C: the history is real and known at the quote, but with the release starting in November
     2015 and the 12-month gap, the training sides hold it in 15 to 44 rows, too few to learn from; the note records
     what the table lacks. **Decision:** A, B or C?

   **Notes for the AI:** the counts: other policies' first rows with cover (`_covered`, `k == 0`) under the same key
   (`Date_birth` + `Date_driving_licence`), ended (the earlier of `Date_next_renewal` and `Date_lapse`) on or before
   the row's `Date_last_renewal`. On C, add a `Note:` bullet after the `other_policies_at_start` bullet with the
   numbers above. On B, build both columns in `_clean` before the later rows go (step 4), numeric, missing where the
   key is unknown; add them to `task_summary.known`; re-run `dataset check`, the leak probes, and through sbatch
   TabPFN on the 5 windows with and without them.

   **Andrej (2026-11-09, change):** Option C: A, with the gap measured in the notes.

   **Resolved (2026-11-09, Andrej):** C: no column for the customer's earlier policy-years; a `Note:` bullet after the
   `other_policies_at_start` bullet gives the gap, recounted on the raw file with the definition's filters (the issue's
   numbers hold: 442 of the 4,362 test rows, 26.9% against 11.5% and 38.0%, 15 to 44 training rows per window).

   [^s10a]: **USE-10** (Must): "For a known entity, its history is legitimate: the split is temporal and the previous
     outcome is a feature." **CLEAN-19** (Should): we build a feature that is an input the actor reads at the
     prediction point from other rows of the same release, kept only where they are known by then. Both in main.

**Review panel:** ship after changes, text only (mediator). A focused re-review of 2026-11-06 under LEAK-41 and
MET-14 to MET-16, by a claim auditor and a mediator. Claims: 19; 14 hold, 4 refuted and 1 partly refuted, all
statements of the notes (the CLEAN-11 counts, the splits comment's test windows, its smallest window and its older
contracts, and "no feature carries the cut"), now fixed there, the last also issue 8; beyond the 19 claims, one
decision untested (issue 7).
Blind review: not part of this tier. Agreed: no Must refuted; the per-contract target with no weight and no offset;
the 12-month gap and the 5 windows; the 12 test rows that are not new contracts stay. Disputed: no agent disputes (no
advocate or critic in this tier); for the curator: the per-contract clause and the half-yearly lapses (issue 7) and the
wording of the CC (issue 8). The mediator's issues 1 and 2 are issues 7 and 8. Two figures of the reports differ on a
re-count: of the 12 test rows that are not new contracts, 3 have a contract dated after the year's start and 9 were
written 2 to 6 months earlier (not 5 and 7), and the premium effects given as 18% and 3.4% are log coefficients of
0.18 and 0.034, about 20% and 3.5%. This block replaces the panel of 2026-11-01, which issues 1 to 5 cite.

<details><summary>Mediator</summary>

**Mediator (2026-11-06): spanish_motor_insurance_2015_2018, focused re-review under the exposure rules**

Panel: claim auditor only; its report is the next section. The panel had no advocate or critic, so the only disputes
are the auditor's refutations of the definition's text. I ran no new experiment: audit2 to audit5 already settle the
facts, with rows matched to the container by key (37,090 of 37,090, premium difference 0.0).

**1. Judgment record**

Verdict: ship after changes. The changes are text only, and no rebuild is needed.

Validity:

- USE-1 holds (approximate fit, as settled).
- LEAK-10 holds: `Date_lapse` and `Payment` stay out of the features.
- LEAK-41 holds:
  - No weight ships, and the realized share of the year in force is not a feature. Adding it would gain +0.011 mean
    Gini, up in 5 of 5 windows, so the leak would be real.
  - The quote-time features predict the cut at AUC 0.711. That is risk selection, which LEAK-41 and USE-6 allow.
- SPLIT-10 and SPLIT-14 hold: the 12-month gap; 52.9% to 72.9% of rows train.
- The splits text misstates the test windows (12 of 4,362 test rows are not new contracts). No effect on validity.

Value:

- MET-2 holds: 261 to 371 positives per window; constant scores 0, oracle 1.
- MET-14's per-contract clause holds on its stated condition: a planned term of exactly one calendar year in 37,090
  of 37,090 rows.
- MET-15 is not triggered: the target is not a rate, so it is scored unweighted with no sample weight (sample_weight
  None, scoring_columns []).

Quality: the CLEAN-11 counts are stale, but the code masks every case correctly. Note fixes only.

Weighed: nothing new. The weighing of issues 1 to 6 stands.

For the curator:

- Issue 1: whether MET-14's per-contract clause still covers a contract whose half-yearly payers earn the insurer
  half the premium when they stop at six months. This is a call about how the rule is written, not a validity breach.
- Issue 2: sign-off on rewording the curator's CC sentence "so no feature carries a cut".

**2. Changes to make now (no decision needed)**

All are in the definition's `dataset.py`. Regenerate README.md afterwards, and add a CHANGELOG entry for the working
copy.

a. CLEAN-11 bullet (line 182). EV-1 applies: a measurement on the data outranks the text.

- Replace "12 rows" with 22, and "8 rows" with 26.
- Replace "5 of them start in 2017, the only first rows after November 2016 that are not new contracts" with: 14 of
  the 26 start in 2017; 28 first rows from December 2016 on are not new contracts.
- These are leftovers of the one-policy design (25,665 rows), the same as the 1,236. The NaN counts equal the date
  counts, so the code is right.

b. splits_comment (line 231). EV-1 applies; the rows were checked by date.

- "The test windows hold new contracts only (766 to 973 a month...)" is wrong. 12 of 4,362 test rows are not new
  contracts: Dec 4, Nov 2, Oct 0, Sep 4, Aug 2.
- Of those 12: 5 have a contract date after the year's start (contract_years made missing), and 7 are the release's
  first row of a contract written 2 to 6 months earlier in 2017. All 12 have Policies_in_force of 2 or more.
- The smallest window holds 763 rows (September), not 766.
- "the older contracts' first years ... start before December 2016 and train only" is also wrong: 28 such rows start
  from December 2016, and 12 of them are in test windows.
- Keep the 12 rows. Each is a first year priced at its start, which is the use case's row.
- Suggested text: "The test windows hold new contracts, apart from 12 first rows of contracts written earlier in 2017
  or dated after the year's start (763 to 973 a month, 261 to 371 with a claim)."

c. Exposure note (line 176). LEAK-41 applies, and the sentence's wording is not backed by the data.

- Replace "so no feature carries the cut" with: no feature set after the quote carries the cut; the quote-time
  factors predict it through risk selection (ROC AUC 0.71, mostly `Premium`: +18% at equal risk factors for
  half-yearly payers, who lapse 12.9% against 1.7%), which LEAK-41 allows.
- Optionally add that cut years carry 3.4% more premium (se 0.8%) at equal factors, not about half. That is stronger
  evidence than the Spearman figure that the premium is not prorated.
- This matches the sibling's note in spanish_motor_insurance_coverage_level_2022_2024 (features rank cancellation at
  AUC 0.77, mostly through payment frequency, kept as a note).

d. Cases row of MET-14 in `metrics.md` (line 319). It ends with "so no feature carries the cut". Reword it as in (c),
so the rule file states only what the data shows. This changes a case's wording, not the rule.

The same phrase appears in the CC lines (dataset.py line 192, record line 97, REVIEW.md issue 6 "Resolved"). Those
are the curator's words, and an AI does not rewrite a CC. See issue 2.

**3. Issues for the curator (ranked)**

Issue 1. Does MET-14's per-contract clause still hold when half-yearly payers who stop at six months pay half? (P6,
MET-14 Should against MET-15 Must; a call on how the rule is written.)

Problem:

- MET-15 names "a premium earned pro rata" as the case for a weight.
- 1,632 of the 2,055 cut years are half-yearly payers who stopped paying. 1,353 of them lapse exactly six calendar
  months in; 0 of the 423 annual payers do. On those contracts the insurer collects half the annual premium.
- MET-14's per-contract clause asks only for a constant planned term known at the quote, and it cites this dataset as
  its own example. The rule therefore cannot test this case on its own.

Is it a conflict? No, by the rules as written:

- MET-15's Must applies "when a rate target's denominator is realized". MET-14's clause keeps the target per
  contract, so there is no rate and MET-15 does not bind.
- Both rules hold on their own. The open question is whether the clause's condition is enough when revenue on a cut
  is earned pro rata. That is a question about the rule's wording, so it is for the curator, not for the mediator.

Effect:

- Mean share of the year in force is 0.992 for annual payers and 0.936 for half-yearly payers. A per-earned-year
  price differs from the per-contract one by at most about 6% between the two groups.
- 233 of the 4,362 test rows are cut years.
- The cut cannot be known at the quote.

Best evidence for keeping per contract (option A, implemented):

- The planned term is constant in 37,090 of 37,090 rows.
- Per contract, cut years claim like full years (35.4% against 35.4%; 0.78 against 0.81 claims).
- The premium is the written annual premium. Half-yearly payers carry +18% premium at equal risk factors. This may be
  a fractioning loading, meaning the insurer prices the lapse risk into the contract (an inference: the data cannot
  tell a loading from selection).
- The 6% bound is small against the risk spread the Gini ranks.

Best evidence for a per-earned-year rate with a weight (option B):

- The insurer's revenue on 1,632 contracts is earned pro rata, which is the case MET-15 names.
- Per year at risk the cut years claim 1.9 times as often (1.53 against 0.81).
- The clause's only example is this dataset.

Options:

- (a) Keep A. Add the 6% bound as one sentence to the Exposure note, and amend MET-14's clause to say that a cut known
  only at the policy's end, and priced into the contract (for example by a fractioning loading), does not make the
  target a rate.
- (b) Keep A, with no amendment.
- (c) Switch to B: the share of the year in force becomes the weight scoring column and the sample_weight (MET-15),
  with a weighted Gini. This reopens issue 6.

What would settle it:

- The insurer's earned-premium rule on a lapse (not in the article).
- Whether the Gini ranking of models differs between A and B on the shipped windows, a cheap re-score.

Issue 2. Rewording the CC sentence (P7-level accuracy, and it touches the curator's words).

- "So no feature carries a cut" is wrong as worded (AUC 0.711, mostly `Premium`). What holds is that no feature set
  after the quote carries it.
- The substance of the decision does not change.
- Options:
  - (a) Approve the rewording of the CC in dataset.py, the record and the REVIEW.md "Resolved" line.
  - (b) Leave the CC as it is and add a dated AI correction line under it.

Side point (low rank, no action asked, not part of today's change):

- `Payment` was dropped under LEAK-10 as the "last payment method".
- Yet `Premium` carries the payment frequency of that year at the quote, through the +18%. That is quote-time
  information, so it is no leak.
- It means dropping `Payment` hides little. Re-adding the frequency as a quote-time feature could be revisited if the
  source confirms that the first year's method is the one recorded.

**4. Disputed points**

There was no adversarial dispute, since the tier had no advocate or critic. The auditor's refutations against the
definition's text, each settled by rank:

- R1, the CLEAN-11 counts: settled by EV-1 (the measurement wins). Change 2a.
- R2, the splits_comment: settled by EV-1. Change 2b. Keeping the 12 rows follows USE-1, since they are first years
  priced at their start.
- R3, "no feature carries the cut": settled by EV-1 on the facts. LEAK-41 and USE-6 decide that the quote-time
  predictors stay; this is not a conflict and not a failure. Changes 2c and 2d, plus issue 2.
- U1, pro-rata revenue: a call about how the rule is written. Issue 1.
- No Must is refuted.
- Minor: the REVIEW.md participant block (around line 1168) gives Spearman 0.05. That is an agent's text, not the
  definition's, so no action.

**5. Agreed facts (measured on the shipped rows, key-aligned)**

- 37,090 rows and 18 features.
- 2,055 cut short by a lapse (5.5%), at a median share in force of 0.501.
  - 1,632 of them are half-yearly payers; 1,353 of those lapse exactly at six months.
  - Half-yearly payers make up 79% of the cut years and 31% of the full years.
- 233 of the 4,362 test rows are cut, per window: Dec 37, Nov 48, Oct 57, Sep 44, Aug 47.
- `Date_next_renewal` equals the start plus one calendar year in 37,090 of 37,090 rows, the cut rows included.
- Claims, per contract against per year at risk:
  - A claim in 35.4% of both cut and full years; 0.78 against 0.81 claims.
  - 1.53 against 0.81 claims per year at risk (1.89 times as often).
- The premium is not prorated: Spearman -0.026 among cut years. Cut years carry +3.4% premium at equal factors (se
  0.8%).
- The cut is predicted from features at AUC 0.711 ± 0.002. Without `Premium` it is 0.678; without `Value_vehicle`,
  0.709.
- `Value_vehicle`:
  - Integer values lapse 1.5 percentage points less within cells.
  - No link to claims (+0.0002).
- No weight, no scoring column, no metric inputs.
- normalized_gini can be scored on every window: constant ~0, oracle 1.000.
- Test windows hold 973, 922, 938, 763 and 766 rows, with 371, 337, 325, 261 and 276 claims.
- Train max start is 2016-11-30, and train max next renewal is 2017-11-30, which is before the test window opens on
  2017-12-01.
- Not-new contracts:
  - 12 not-new test rows.
  - 28 not-new first rows from December 2016 on.
  - 26 contract dates and 22 licence dates after the start, matching the NaN counts of contract_years and
    years_licensed.
- Mean share in force: 0.992 for annual payers, 0.936 for half-yearly payers.

**6. Consistency with precedent**

- fremtpl2, bemtpl97, frempl_french_motor_personal_line and pricing_game_2016_french_fleet use a rate with a weight.
  This case differs on one fact: here the term is planned and constant, while there the periods are realized lengths
  with no planned term. The record already states this, so it is consistent.
- spanish_motor_insurance_coverage_level_2022_2024 uses a weighted rate with annualised premiums. It differs on facts:
  - Its rows are calendar years with mid-year starts, so there is no constant planned term.
  - Its premiums are earned pro rata, so they had to be annualised.
  - Its target was already a rate by the curator's call (Andrej, 2026-11-02).
  - Its practice of noting quote-time predictors of cancellation (AUC 0.77, mostly payment frequency) is the model
    for change 2c, so the two agree.
- The open point is issue 1. If the curator decides that pro-rata premium earned on half-yearly lapses brings this
  case under MET-15's "premium earned pro rata", it would no longer differ from the sibling on that ground. Then
  either the per-contract clause is amended to say why it still holds (option a), or the dataset moves to B (option
  c).
- The decision register shows no other precedent against today's change.

</details>

<details><summary>Claim audit</summary>

**Claim auditor (2026-11-06): spanish_motor_insurance_2015_2018, focused re-review**

Rows aligned to the container by a key merge (audit1's first listing used an unaligned order and is superseded by
audit2 and audit3).

**Verdict**

The change itself holds: 2,055 of 37,090, the exposure paragraph's numbers, the constant planned term behind MET-14's
per-contract clause, and the unweighted metric with no weight or scoring column (MET-15) all survive tests on the data.
Refuted: stale counts next to the change. The CLEAN-11 note gives 12 licences and 8 contracts dated after the year's
start; the data has 22 and 26. It also says "5 of them start in 2017, the only first rows after November 2016 that are
not new contracts"; there are 14 such rows and 28 first rows that are not new contracts. The splits_comment says "test
windows hold new contracts only (766 to 973 a month)": 12 test rows are not new contracts, and September holds 763.
These are the same one-policy-design leftovers as the 1,236. The wording "no feature carries the cut" is too strong.
The features known at the quote predict the cut at ROC AUC 0.71, mostly through Premium. That is risk selection, which
LEAK-41 and USE-6 allow, and the cut does not change the per-contract target. So the sentence needs rewording; no
feature has to go. Nothing threatens validity: no Must rule is refuted.

**Claim table**

| # | claim | source | test | result | evidence | rule |
|---|---|---|---|---|---|---|
| 1 | 2,055 of 37,090 first years cut short by a lapse (5.5%) | fit_reason, Exposure note, CC, record, MET-14 text | rebuilt the shipped rows from raw; cut = Date_lapse < Date_next_renewal | holds | 2,055 (0.0554) | MET-14 |
| 2 | 1,632 of them half-yearly payers who stopped paying | Exposure note, CC | Payment==1 among cut rows; lapse date against start + 6 calendar months | holds | 1,632; 1,353 of them lapse exactly 6 months in (0 of 423 annual payers do); half-yearly share 79% of cut years against 31% of full years | MET-14 |
| 3 | median cut at half the year | Exposure note | share of the year in force among cut rows | holds | median 0.501 | - |
| 4 | 233 of the 4,362 test rows cut | Exposure note, record | cut counted per shipped test window | holds | 37+48+57+44+47 = 233 (Dec..Aug) | - |
| 5 | planned term exactly one calendar year in all 37,090 rows, known at the quote | Exposure note, CC, MET-14 clause | Date_next_renewal == start + 1 calendar year | holds | 37,090 of 37,090, including all 2,055 cut rows (the field is not rewritten at lapse) | MET-14 |
| 6 | Premium is the written annual premium, not prorated (Spearman -0.03) | Exposure note, record | Spearman among cut years; log premium on cut, controlling for type, vehicle age, value, power, channel, area, new, Payment | holds (stronger than stated) | Spearman -0.026; cut years cost +3.4% more premium (se 0.8%), not about half; median 318.7 against 288.8, higher in each of the three large types | LEAK-41 |
| 7 | "so no feature carries the cut" | Exposure note, CC, record ("no feature carries a cut") | cross-fitted LightGBM of cut on the 18 shipped features | refuted as worded (no leak) | AUC 0.711 +- 0.002; Premium is the top gain (dropping it: 0.678). Premium sits 18% higher (se 0.4%) for half-yearly payers at equal risk factors, and half-yearly payers lapse 12.9% against 1.7%. These are quote-time values: risk selection, allowed by LEAK-41 ("a feature known at the prediction point that predicts the weight through risk selection stays") and USE-6 | LEAK-41, LEAK-10 |
| 8 | per contract, cut years claim like full years (35.4% each; 0.78 against 0.81 claims); per year at risk 1.9 times as often (1.53 against 0.81) | Exposure note, record, MET-14 Cases row | recomputed on shipped rows and in the test windows | holds | 0.3543/0.3537; 0.784/0.807; 1.527/0.807 = 1.89. In the test windows 37.3% against 35.9% | MET-14 |
| 9 | the per-contract target suits the decision (prices an annual contract), unweighted | Exposure note, CC, MET-14 clause, MET-15 per-contract clause | bound on how far the per-contract ranking can sit from a per-earned-year ranking: mean share in force by payment method | holds (immaterial gap, see U1) | mean share in force 0.992 for annual payers and 0.936 for half-yearly payers. The per-contract and per-earned-year prices differ by at most about 6% between the two groups | MET-14, MET-15 |
| 10 | no weight and no offset; scored unweighted | dataset.py metric, CC | container: sample_weight(c), scoring_columns, metric inputs | holds | sample_weight None, scoring_columns [], inputs {} | MET-15 |
| 11 | metric computable on every fold | metric block | constant, random and oracle scored per fold with scorer(c); positives counted | holds | constant ~1e-16 (0), oracle 1.000, positives 261 to 371 per window | MET-2 |
| 12 | realized length never a feature | Exposure note, LEAK-41 | realized share in force added as a feature, LightGBM, 3 seeds, 5 windows | holds (the leak would be real) | it is not shipped; adding it moves the mean Gini 0.152 to 0.163 (+0.011, up in 5 of 5 windows). The cut flag alone scores +-0.013 | LEAK-41 |
| 13 | "The test windows hold new contracts only" | splits_comment | Date_start_contract == Date_last_renewal on the test rows | refuted | 12 of 4,362 test rows are not new contracts (4 Dec, 2 Nov, 0 Oct, 4 Sep, 2 Aug). 5 have a contract dated after the year's start (contract_years missing). 7 are the release's first row of a contract written 2 to 6 months earlier in 2017. All 12 have Policies_in_force of 2 or more | SPLIT (statement), EV-1 |
| 14 | "766 to 973 a month, 261 to 371 with a claim" | splits_comment | rows and positives per window | partly refuted | rows 763 (Sep) to 973; positives 261 to 371 hold | - |
| 15 | "the older contracts' first years in the release start before December 2016 and train only" | splits_comment | not-new first rows starting from 2016-12-01 | refuted | 28 such rows; 12 fall in test windows, the rest in the gap | - |
| 16 | CLEAN-11: licence after the start in 12 rows, contract after the start in 8 rows, "5 of them start in 2017, the only first rows after November 2016 that are not new contracts" | curation_comments (CLEAN-11 bullet) | date comparisons and NaN counts on the shipped frame | refuted (stale counts) | years_licensed NaN 22 (licence after start 22); contract_years NaN 26 (contract after start 26), 14 of them starting from 2017; 28 not-new first rows from Dec 2016 | CLEAN-11 (the count, not the rule) |
| 17 | train/test bounds: newest window trains Nov 2015 to Nov 2016; 53-73% of rows | splits_comment | split inspection | holds | train max start 2016-11-30, train max next renewal 2017-11-30 < 2017-12-01; 19,629/37,090 = 52.9% to 27,043 = 72.9% | SPLIT-10, SPLIT-14 |
| 18 | Value_vehicle (2019) does not encode the policy's outcome | curation_comments (kept on purpose) | LEAK-41's "precision marks the cut": integer share of the value by cut, within type x vehicle age x new cells; the same for claims | holds for the target; a weak mark of the cut | integer values lapse 1.5 pp less within cells (4.9% against 7.2% raw). No link to claims (+0.0002 within cells). Dropping Value_vehicle moves the cut AUC only 0.711 to 0.709. No weight ships, so LEAK-41's Must does not bind | LEAK-41, LEAK-11 |
| 19 | 1,236 removed from the text | dataset.py, README, record | grep | holds | only in the CC sentence that explains the correction | - |

**Refuted / untested, ranked** (principles: validity first, Must first; none of these is a Must or a validity breach)

- R1 (Should, evidence). CLEAN-11 counts and the "only first rows after November 2016 that are not new contracts"
  clause (#16, #15). Stale from the one-policy design (25,665 rows), like the 1,236. Real values: 22 licences and 26
  contracts dated after the start, 14 of them from 2017, and 28 not-new first rows from December 2016.
  - Effect: notes only; the code masks every case correctly (NaN counts equal the date counts).
  - Mildest remedy: correct the numbers in the CLEAN-11 bullet. A rebuild is not needed for the code; the README is
    generated, so regenerate it.
- R2 (Should, evidence). splits_comment "The test windows hold new contracts only (766 to 973 a month ...)" (#13,
  #14). 12 of 4,362 test rows (0.3%) are not new by the date test. They are the first rows in the release of very
  young contracts of multi-policy customers, plus 5 rows with an impossible contract date. 763, not 766.
  - Effect: none on validity. They are first years priced at their start, which is the use case's row.
  - Mildest remedy: "The test windows hold new contracts, apart from 12 first rows of contracts written earlier in
    2017 or dated after the year's start (763 to 973 a month, 261 to 371 with a claim)". Name the 12 in the CLEAN-11
    bullet. Keep them.
- R3 (Should, wording). "so no feature carries the cut" (Exposure note, CC, record) (#7). Quote-time features predict
  the cut at AUC 0.71, Premium most of all (+18% premium for half-yearly payers at equal risk factors). That premium
  gap may be a fractioning loading or selection; the data cannot tell them apart. What holds is that no feature set
  after the quote carries it. Premium is not prorated: cut years pay 3.4% more premium, not half.
  - Mildest remedy: "no feature set after the quote carries the cut; the quote-time factors predict it through risk
    selection (AUC 0.71, mostly the premium), which LEAK-41 allows".
  - A side point, not today's change and no action asked: Payment was dropped as "last payment method" (LEAK-10), yet
    the year's Premium carries the payment frequency of that year at the quote.
- U1 (untested decision, no change asked). MET-15 names "a premium earned pro rata" as the case for a weight. The
  1,632 half-yearly payers who stop at six months pay half the annual premium, so their revenue is earned pro rata.
  The per-contract target stands on MET-14's per-contract clause, and that clause cites this dataset itself, so the
  rule cannot check the case independently.
  - Bound: the per-earned-year price differs from the per-contract one by a factor of 0.992 (annual) against 0.936
    (half-yearly), at most about 6%. That is small against the risk spread the Gini ranks, and the cut is unknown at
    the quote. Holds as a curator's call.
  - Remedy, only if the curator wants it closed: one sentence in the Exposure note giving this bound.

Not touched today and still holding: the metric (normalized_gini, fallback from context, no weight) is computable on
every fold with 261 to 371 positives, and no copy across the split was looked for beyond the settled LEAK-18 note.

Minor: REVIEW.md's participant block (line ~1168) gives Spearman 0.05 for premium against share in force; the
definition and the record give -0.03 (measured -0.026). This is the agent's text, not the definition's, so no action.

</details>

## Reference

Segura-Gisbert J., Lledó J., Pavía J.M. (2025). Dataset of an actual motor vehicle insurance portfolio. European Actuarial Journal 15:241-253. https://doi.org/10.1007/s13385-024-00398-0
Data: Mendeley Data, https://doi.org/10.17632/5cxyb5fp4f.2 (CC BY 4.0).

Lead: zero-inflated screening review, policy question 6 (curator's go, Andrej, 2026-10-20); sibling of `spanish_motor_insurance_coverage_level_2022_2024`.
