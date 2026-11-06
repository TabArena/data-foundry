---
unique_name: spanish_homeowners_motor_insurance_2010_2014
name: Spanish homeowners and motor insurance customers, 2010-2014
checked_by:
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 3
tags:
- Non-IID (Temporal)
- Two-Regime Zeros
original_source: Other
year: '2021'
domain: insurance
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://data.mendeley.com/datasets/vfchtm5y7j/1
- https://doi.org/10.17632/vfchtm5y7j.1
- https://doi.org/10.1016/j.dib.2021.107639
v2_path: datasets/_dev/tabarena-v0pt2/spanish_homeowners_motor_insurance_2010_2014/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**AI-FILLED, UNVERIFIED. Drafted by an AI assistant on 2026-11-02 from the original release and papers named below. A human must verify the suggestion and notes.**

**Screening (AI, 2026-11-02):** `TBD -> Yes`, priority 3: real customer-year homeowners claim costs with coverage amounts, recurring customers and three possible annual test windows; the annual inputs and loss availability still need checking.
- Source: Guillen, Bolance, Frees and Valdez, Mendeley Data v1, 3 June 2021, DOI 10.17632/vfchtm5y7j.1. One CSV (`data_ex.csv`): 122,935 customer-years of 40,284 private Spanish customers followed over 2010-2014, initially holding both home and motor contracts. Proposed target `Claims2`, annual home claim cost in euros, including claim-free years; retain the real release, not the separately published simulation code (PROV-3, PROV-8).
- Use case: an insurer at renewal estimates the coming year's home claim cost to set the premium for a bundled customer. The model paper (Frees et al. 2021, Sec. 3.5, p. 8) describes pricing "assuming the insured will renew their policy" and illustrates home premiums in Table 8; the data paper Sec. 2, p. 4 models annual home claims with rating variables. Fit provisionally direct, subject to checking when those variables were recorded (USE-1, USE-3, USE-8). Split temporally for recurring customers (USE-10, SPLIT-6, SPLIT-13). Table 1 of the data paper reports yearly counts 40,284 / 29,818 / 22,505 / 17,044 / 13,284: test 2012, 2013 and 2014 after training on 57.0%, 75.3% and 89.2% of the rows, respectively (SPLIT-14). This assumes preceding-year losses were available; a reporting gap may change the feasible windows (SPLIT-9, SPLIT-10).
- Siblings and duplicates: searched records by DOI, title, authors and coverage field names; no matching source found. `spanish_motor_insurance_2015_2018` and `spanish_motor_insurance_coverage_level_2022_2024` are different releases, authors and periods; Wisconsin is another portfolio. No external benchmark membership verified; do not treat that as proof of absence (PROV-4 to PROV-7).
- Papers and pages: Guillen et al. (2021), "Case study data for joint modeling of insurance claims and lapsation", Data in Brief 39:107639, Secs. 1-2 and Table 1; Frees et al. (2021), "Dependence modeling of multivariate longitudinal hybrid insurance data with dropout", Expert Systems with Applications 185:115552, Secs. 3.3-3.5. Data paper Sec. 1, p. 3: "the number of policies per year decreases over time." The published renewal cohort is selected, not a sample of every Spanish household.
- Metric: no unique held-out claim-cost selection metric found in the original papers' case study. They estimate Tweedie models and dependence, and illustrate premiums; fitting by deviance does not establish a held-out benchmark metric. Proposed fallback `rmse` in euros, inputs none (MET-1, MET-5); do not transfer Wisconsin's premium-based Gini. The release's variable list has no premium column.
- Risks for /add-dataset: drop the same-year home count `NClaims2`, joint outcome code `Types`, and renewal outcome `Retention` as inputs; same-year motor count/cost are also future outcomes at renewal (USE-3, LEAK-10). Verify annual rating-field timing, the meaning of the insured-value scales, complete-year exposure and claim development. Attrition is substantial and the source explicitly models dependence between claims and lapse; do not silently select five-year survivors (USE-5). Table 1 reports only 448 / 310 / 240 positive home-claim records in the proposed test years, so a large total row count does not establish stable severity scores (TP-9). No data probes or definition built at screening.
- Priority: start 1; gap 0 (insurance, regression and temporal are not thin in this run); use case + (the source's premium and renewal decision); source + (original data release and papers); shape + (dated customer panel, coverage and mixed rating fields); risk - (input timing, exposure and attrition).

Screen verification: no ethics objection found in the release, and real provenance supported by the data paper (SEL-1, SEL-16, PROV-1); scope/use case and temporal structure supported by the source (SEL-3, USE-1, SPLIT-6); no duplicate found by provenance search (PROV-4). Prediction-time availability, label maturity and score stability cannot be verified from the description alone; confirm in /add-dataset. CSV dimensions and values were not independently measured in this screen (EV-7).

CC (2026-11-02, Andrej): `Yes`, priority 3, as the AI screening proposed (screening review page of the Wisconsin alternatives). Precedent check: consistent with spanish_motor_insurance_2015_2018 and wisconsin_local_government_property_insurance_fund; late claims, attrition and the positives per test year (448 / 310 / 240) are settled in /add-dataset.

**Assessment (AI, 2026-11-02):** added as `datasets/_dev/tabarena-v0pt2/spanish_homeowners_motor_insurance_2010_2014/` by /add-dataset with the full review panel; the open questions are in its `REVIEW.md`. Recommend shipping; the five issues (13 once-read rating fields kept, no gap before each test year, the Gini, frozen ages, two warnings) are weighings, none a reason for `No`. Target `Claims2` shipped as log1p, scored by `normalized_gini` on the amount from context: the screening's proposed `rmse` is superseded (every model scores R^2 at or below 0 on the amount; on a Tweedie deviance a constant beats every model). Split: test years 2012/2013/2014, expanding, no gap (train 57.0/75.3/89.2%, 448/310/240 claimants). Inputs: the year's own outcomes dropped (`NClaims2`, `Types`, `NClaims1`, `Claims1`, `Retention`); prior-year claims added. Measured: untuned Gini 0.11-0.32 (bootstrap SE 0.06-0.11 per year); no leak; lapse years kept (claim share 2.21% against 1.65%). Priority 3: gap + (insurance thin), use case + (renewal pricing, fit approximate), source + (original release and papers), shape + (122,935 customer-years, temporal), risk - (small signal, rating-field read date unknown, 240-448 claimants per test year).

CC (2026-11-02, Andrej): issues 2-5 as implemented: no gap before each test year (issue 2); `normalized_gini` on the amount from context, decided for this table, the screening's `rmse` proposal struck (issue 3); the frozen ages kept as released with the note (issue 4); `task_time_on_few_unique` and `task_target_value_dominant` accepted (issue 5). Issue 1 (the once-read rating fields): "You should do an extensive leakage check and then suggest what to do. Asking the authors is not an option"; the check is running.

**Exception to SPLIT-10 (2026-11-02, Andrej):** no gap for late-reported claims (issue 2). The panel is yearly; a one-year gap leaves the 2012 window 33% of the rows, below SPLIT-14's floor. Hiding 30 or 90 days of the newest year's claims moves the mean Gini from 0.219 to 0.226 and 0.203, within noise. Serves SPLIT-14, as pricing_game_2016_french_fleet.

CC (2026-11-02, Andrej): ship. Issue 1 (a), "I go with a)": the 13 once-read rating fields kept under LEAK-10's later-pull clause after the nine-test leak check (no gain a late read could carry into the home target), `Policy_PaymentMethodA` with its potential-leak note (LEAK-37). Issues 2-5 as recorded above.

## Reference

Guillen, M., Bolance, C., Frees, E.W., Valdez, E.A. (2021). Insurance data for homeowners and motor insurance customers monitored over five years. Mendeley Data, V1. https://doi.org/10.17632/vfchtm5y7j.1

Guillen, M., Bolance, C., Frees, E.W., Valdez, E.A. (2021). Case study data for joint modeling of insurance claims and lapsation. Data in Brief 39:107639. https://doi.org/10.1016/j.dib.2021.107639
Open text: https://diposit.ub.edu/server/api/core/bitstreams/67e7e6d7-6cbb-4493-905a-42cc7e0d1073/content

Frees, E.W., Bolance, C., Guillen, M., Valdez, E.A. (2021). Dependence modeling of multivariate longitudinal hybrid insurance data with dropout. Expert Systems with Applications 185:115552. https://doi.org/10.1016/j.eswa.2021.115552
Open text: https://openresearch-repository.anu.edu.au/items/b08797a2-d65f-4ed9-9440-0befc4b3516c

Lead: Andrej requested screening on 2026-11-02 while reviewing Wisconsin property insurance alternatives.
