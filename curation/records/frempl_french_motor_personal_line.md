---
unique_name: frempl_french_motor_personal_line
name: freMPL1-10 (CASdatasets, French motor personal line insurance, private insurer, 2004)
checked_by:
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 3
tags:
- Two-Regime Zeros
- Non-IID (Grouped)
original_source: Other
year: '2014'
domain: insurance
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://dutangc.github.io/CASdatasets/reference/freMPL.html
- https://github.com/dutangc/CASdatasets/tree/master/data
- https://dutangc.perso.math.cnrs.fr/RRepository/pub/web/NEWS.html
v2_path: datasets/_dev/tabarena-v0pt2/frempl_french_motor_personal_line/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (v4 of 2026-10-19, a list of 69 candidates, not in the repository), the source pages and papers, and the data itself where the notes say it was downloaded and measured; extended on 2026-10-20 at Andrej's request with a file-by-file analysis of all ten tables. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> Yes`, priority 2: a documented French motor portfolio of 2004 with four years of
claim history, best taken as five same-schema samples (freMPL5-9, 115,200 policy records); how the samples were cut is
undocumented and some amounts are negative.
- Source: CASdatasets (Dutang and Charpentier), `freMPL1`-`freMPL10`: "This collection of ten datasets comes from a
  private motor French insurer. Each dataset includes risk features, claim amount and claim history of around 30,000
  policies for year 2004." Source: "Unknown French private insurer." Target `ClaimAmount`, "Total claim amount of the
  guarantee"; the history columns count claims "in the 4 preceding years". The version that first held the tables was
  not found (the NEWS lists them from 1.2-0, 2024), so `year` stays empty; 1.2-1 (2026-04-10) removed "around 9995"
  duplicate rows per file.
- Use case: for example, an insurer pricing a policy from its rating factors and claim history; the page names no use;
  fit direct for that use. Regime IID: records within 2004 (`RecordBeg`, `RecordEnd`), no policy id.
- Siblings and duplicates: one record for all ten files (earlier triage: freMPL5-9 near-random disjoint slices;
  freMPL1-4 nested, their amounts derived from freMPL1's claims; freMPL10 another column list). `fremtpl2` (Yes, Andrej)
  is another French portfolio of another period and schema: no duplicate (PROV-7), but a second French motor table, so
  whether both ship is a weighing call; also the three pricing-game records and `bemtpl97`. OpenML: none by name.
- Papers and pages: the CASdatasets freMPL page and NEWS; no paper found that defines a task on these tables.
- Metric: none found (the CASdatasets page), so the fallback (`rmse`).
- Earlier AI triage, 2026-10-19/20, measured on CASdatasets 1.2-1: freMPL5-9 89.7% zeros and 0.6-1.0% negative amounts
  (all with `ClaimInd` = 0); untuned LightGBM: AUC 0.689 for a claim, R^2 0.031 on log1p over all rows.
- Risks for /add-dataset: pin CASdatasets 1.2-1 or later, or deduplicate; which files make the dataset (the earlier
  recommendation: freMPL5-9 stacked, no file column); negative amounts and `Exposure` as a feature or weight, the
  family's open insurance-conventions question (`fremtpl2` kept `Exposure` as a feature capped at 1); drop `ClaimInd`.
- Priority: gap 0, use case 0 (no decision named), source + (the publisher documents every column), shape + (115,200
  records, 18 mixed features), risk - (undocumented sample cuts, negative amounts).

**Assessment (AI, 2026-10-30):** suggested call for policy question 3 of the zero-inflated review, where Andrej asked
for a call per dataset from its references and the domain's practice instead of one convention for the family (the
shared reasoning: a time exposure or a sum insured is a feature, and a rating-cell table weights the metric by its
exposure; negative amounts that are recoveries become 0; the source's metric first, else the normalized Gini as a
context metric, since RMSE on raw amounts follows a few large claims and a Tweedie or Poisson deviance needs positive
predictions; MET-10 as amended on 2026-11-02 (Andrej) later declined a family-wide metric, so each table's metric is
decided on its own); the curator
has the call.
- Target: `ClaimAmount` on freMPL5-9 stacked (115,200 records), as recommended above.
- `Exposure`: a feature, as in the `fremtpl2` call (records cover parts of 2004, mean 0.44).
- Negative amounts (0.6-1.0% of rows): set to 0. They occur only with `ClaimInd` = 0, so they are no claim of the
  record's period (presumably recoveries on earlier claims); AIcrowd set negative totals to 0 on the 2017 game's
  portfolio (`pricing_game_2017_french_mtpl`).
- Metric: normalized Gini as a context metric (MET-11); no source metric.
- Pin CASdatasets >= 1.2-1; drop `ClaimInd`.

CC (2026-10-30, Andrej): `Yes`, priority 5 (the AI screening had `TBD -> Yes`, priority 2; zero-inflated screening
review page).

Ten tables from one "private motor French insurer", each with "risk features, claim amount and claim history of
around 30,000 policies for year 2004" (CASdatasets documentation). The workbook lists freMPL2, 3, 5-9 as seven
candidates (Master rows 63-69) and says not to merge them; measured on the data, they are cuts of one portfolio, so
they share this record. Version matters: CASdatasets 1.2-1 (files dated 2026-04-10) notes "Remove duplicated rows in
`freMPL*.rda` files (around 9995 rows for each file)" (NEWS). All numbers here are on 1.2-1 (the downloaded file sizes
match its NEWS listing); older releases and mirrors carry about 10,000 duplicate rows per file, so the definition must
pin CASdatasets >= 1.2-1 or deduplicate. Every file's row count is a multiple of 100 (20,600 to 38,300), so each file
is a sample of a chosen size, not a split by region or period. Why the samples were cut is undocumented; the package
releases are named by university year, so teaching samples are plausible (unconfirmed, the maintainers could say).

How the files relate. There is no policy id; rows were matched on the 11 columns all ten share (record dates, exposure,
ages, licence age, bonus-malus, gender, marital status, socio-professional category, usage, km limit), a key that is
unique for about 99.8% of rows within a file.
* freMPL5-9: same 20 columns in the same order, same dtypes and coding (risk area 1-13, mean 7.82-7.92; only a few rare
  socio-professional codes differ), 34-105 shared rows per pair, 115,200 policy-years. A classifier finds the source
  file from the features 31.1% of the time against 28.1% by chance: near-random slices of one portfolio.
* freMPL1 holds the same target as freMPL5-9: 7,961 of its 20,535 contracts (39%) reappear there, and the claim amounts
  agree on 795 of 796 positive claims (126/126, 266/266, 196/197, 140/140, 67/67 for files 5-9).
* freMPL1-4: the contract sets are nested, freMPL1 = freMPL3 inside freMPL4 (100%) inside freMPL2 (99.8%); freMPL2's
  17,718 extra contracts are the newest drivers (mean bonus-malus 76, 13% at the starting level 100). The claims nest
  the other way: freMPL2-4 have a claim only where freMPL1 has one, and their amount is then mostly exactly 0.849 x
  freMPL1's (60%, 54% and 81% of their claims), otherwise a smaller share, never larger. So freMPL2-4 are amounts
  derived from freMPL1's claims, not independent coverages as the documentation's "claim amount of the guarantee"
  suggests; freMPL3's `DeducType` (Normal, Partially refunded, Majorized, Proportional) hints at deductible or refund
  schemes, undocumented.
* freMPL10: a different column list, risk area mean 5.50, 15 socio-professional codes absent from freMPL5, about 22
  claims in 22,100 rows (99.9% zero), and 300-700 rows shared with each of freMPL5-9.
* Two feature views of overlapping customers, not a cold-start split: freMPL1-4 add vehicle details (body, price,
  engine, energy, speed, class, `RiskVar`, `Garage`), freMPL5-10 the claim counts by type "in the 4 preceding years"
  and a risk area. freMPL1-4 lean newer (bonus-malus mean 69.6 vs 59.3, 8.2% vs 1.1% at 100, licence under 3 years
  2.7% vs 0.6%), but 21% of their contracts are also in freMPL5-9, and bonus-malus is itself claim history.

Zero mechanism, confirmed from the data: `ClaimAmount` is 0 where `ClaimInd` = 0 (no claim during the record), 89.7%
over freMPL5-9; 0.6-1.0% of rows have negative amounts, all with `ClaimInd` = 0, presumably recoveries. Untuned
LightGBM, 3-fold random CV, negatives set to 0, `ClaimInd` dropped: ROC AUC for a claim 0.689 (freMPL5-9), 0.667
(freMPL2), 0.650 (freMPL1), 0.605 (freMPL4); R^2 on log1p amount among claimants -0.03 to -0.23 (0.031 for freMPL5-9
on the full log1p target). Only the claim / no-claim part carries signal, as in `forest_fires`.

Recommendation: one dataset, freMPL5-9 stacked (115,200 rows, 18 features). Use the union of the socio-professional
levels, add no file column, drop `ClaimInd`, set negatives to 0 or drop them (family rule still open), decide whether
`Exposure` is a feature or a weight (also open), and drop the 89 exact duplicate rows (another 1,693 rows share
the 11 base columns with a row but differ in claim history or amount, so they are distinct records).
Random (IID) split: no record spans all of 2004 (mean exposure 0.44), and chaining consecutive records of one profile
finds 431 pairs against 309 by chance, so policyholders cannot be traced; grouping by file would leave five
near-identical groups. Leave out freMPL1 (39% of its rows duplicate freMPL5-9 rows and target), freMPL2-4 (targets
derived from freMPL1's claims; the same data with a swapped target) and freMPL10. Pooling all ten files with a
coverage column does not work: 243,100 rows hold only 163,679 contracts (44% of rows share a contract with another
row), only 11 of 28 feature columns are common, and a contract's freMPL1 row nearly gives away its freMPL2-4 rows. If
the vehicle features matter more, use freMPL1 (optionally with `DeducType` joined from freMPL3) instead of
freMPL5-9, not in addition. No second task for freMPL1-4 either: `fremtpl2` already covers French motor insurance with
vehicle features (678k policies). Also considered and rejected: adding the vehicle block to freMPL5-9 and the
12,580 freMPL1-only contracts as extra rows. On the 7,955 shared contracts the vehicle block lifts the claim AUC
from 0.675 to 0.685 (base columns alone 0.668); the union would hold about 127,800 rows with vehicle details for
16% and claim history for 90%. The missing-block pattern does not leak (AUC 0.511 on its own), but it is an
artefact of how the samples were cut, for 11% more rows. Licence: GPL (>= 2) (CASdatasets). Siblings from the same
package: `fremtpl2`, `bemtpl97` (different portfolios).

**Assessment (AI, 2026-11-01):** added as `datasets/_dev/tabarena-v0pt2/frempl_french_motor_personal_line/` by /add-dataset with the full review panel; the open questions are in its `REVIEW.md`. Recommend shipping; only the forced split of one year (its issue 5, with australian's issue 1) could still turn it to `No`. Changes after the panel: folds grouped by policy chain (`ForcedGroupedFromTemporal`), since under random records a policy's later records in training gave its claims away; `Exposure` of the 25,131 records that ended early without a continuation replaced by the length known at their start (LEAK-10, LEAK-7). Corrections to the screening above, from the data: `year` is 2014 (the 1.0-7 NEWS; set now, it was empty); 3,805 records span all of 2004; policies can be traced within a file (34,324 links, 1 by chance); the files hold 16,000-32,400 records in 1.2-1 and are not near-random slices; the 967 negative amounts are not recoveries on earlier claims (all have `ClaimInd` = 0; read as a not-at-fault claim whose recourse covered the payment, set to 0). The record's `required_split` (Random) and `Larger IID Data` tag disagree with the definition (field rows in REVIEW.md, left for your mark). Priority 3 (your 5 of 2026-10-30 was set before the measurements): gap + (insurance), use case 0 (fit approximate), source +, shape +, risk - (issue 5 can turn it to `No`).

CC (2026-11-02, Andrej): the forced grouped split ships (issue 5 (a)): "Forced group splits should be fine. Regarding forced IID, did you make sure there are no leaks? Whenever there are no leaks we can ship." Recorded in SPLIT-8 (amended 2026-11-02: a forced grouped split ships; a forced IID split ships only when the leak test across the random split finds none).

CC (2026-11-02, Andrej): the `Exposure` fix confirmed (issue 2 (a)): the 25,131 records that end early without a continuation get the length known at their start, every `Exposure` rounded to months; recorded as the LEAK-10 case for time on risk cut short by the outcome (leak_checks.md, Mechanisms table): the cut is removed or fixed where the data locates it, kept with its measured size where it cannot.

**Assessment (AI, 2026-11-02):** the leak test across the forced grouped split (SPLIT-8 as amended 2026-11-02) finds none, on the 9 shipped splits with untuned LightGBM. Shared rows and units: 0.37% of each test fold has its 16 features in the training side, and those copies agree on a claim less often than the base rate (84% against 91%); the group probe finds no IID-grouped gap (R^2 0.025 both) and the hidden-group probe no other key (gaps -0.001 to +0.003); the 10,292 records whose policy continues only in another file, the one link the chains leave open, give nothing away (the successor lookup ranks claims at AUC 0.51 and lowers the Gini on 8 of 9 splits). Shared period (2004, by start month): the training side's mean claim rate and amount per start month and per risk area and start month, added as features, move the Gini by -0.0005 on average (-0.015 to +0.014) and the claim AUC by +0.0003; removing from training the test rows' own quarter costs no more than removing as many random rows (Gini -0.000, AUC +0.0005 on average, 12 fold-quarters). Features from other rows' outcomes: none in the column audit; the claim counters and bonus-malus hold the policy's own history, its earlier records in the same chain. how_much_did_it_rain's `No` named a measured period shock on both sides; none is found here.

CC (2026-11-03, Andrej): the record takes the definition's split, `Grouped (NON-IID)`, and the tag `Non-IID (Grouped)` in place of `Larger IID Data` (record-field rows in frempl_french_motor_personal_line).

CC (2026-11-03, Andrej): the claim amounts stay as published with the note on their unknown basis and valuation date (issue 3 (A)).

**Assessment (AI, 2026-11-03):** the exposure-weighted Gini chosen in issue 4 (B) leaks as first worded: with the realised length as the base, a constant prediction scores 0.184 on the shipped splits, because records that ended early (often by their claim) have a short realised length. Not applied; the row Gini stays until the curator chooses; the base known at the start scores the length alone at 0 (model 0.137).

CC (2026-11-03, Andrej): the folds are grouped by the cross-file policy component, the most conservative key (issue 1 (B)): "I choose B".

CC (2026-11-03, Andrej): the metric is the exposure-weighted Gini of the ordered Lorenz curve with the length known at the start as its base (issue 4 (C)): "I go with your option C".

CC (2026-11-03, Andrej): ship (verdict); the metric, the exposure-weighted Gini with the length known at the start as its base, checked.

CC (2026-11-06, Lennart): issue 6 resolved by D9 of the exposure study (https://github.com/TabArena/data-foundry/issues/51): the target is the claim amount per realized year on the log1p scale (CLEAN-16 as amended: a rate scored by a Gini keeps the curator's scale); `Exposure`, the realized length, is the weight of the metric and of training and never a feature (LEAK-41, MET-14, MET-15); the length to 31 December stays a feature (CLEAN-22, USE-6); `exposure_at_start` is dropped; the metric is `ordered_lorenz_gini` per unit of `Exposure`, Andrej's unnormalised CAS form, now on the rate. Supersedes Andrej's call of 2026-11-03 (issue 4: option C, the length known at the start as the base, chosen over option B, the realized base, under which a constant prediction scored 0.184): under the rate a constant scores 0, whereas option B scored totals against a realized base; LEAK-41 now guards against 1/length, which alone scores 0.184 against 0.183 for the honest model.

**Assessment (AI, 2026-11-06):** the re-review panel's text changes are in the definition (rows, features, target, weight, split and metric unchanged): the protocol line against reading other test rows gives the gain as +0.26 to +0.44, depending on what is read (0.44 to 0.64 against honest scores of 0.17 to 0.20, 9 of 9 splits each), and says that a test record's successor is found without `policy_component`, from the features and `Exposure` (39% of the records linked, 99.7% of the links within one component); 1/`Exposure` alone (0.184) is no longer called the ceiling a leak would reach, since `Exposure` as a feature lifts the honest model from 0.183 to 0.256; models are compared by paired fold differences (random orders' per-fold SD 0.037, up to 0.071; the 802,620 claim moves the fold that holds it by about 0.06); the start date ships as `length_to_year_end`, one value per start day. The unrounded `length_to_year_end` is the AI's call, not part of D9 (the CC of 2026-11-06 above does not name it): it undoes Andrej's month rounding in the CC of 2026-11-02 above (issue 2 (a)), which outranks it until Lennart marks REVIEW.md issue 9. D9 also supersedes the rest of that CC (the realized length kept on the 34,324 continued records) and the 2026-11-01 assessment's `Exposure` fix, which the CC of 2026-11-06 does not name (issue 9).

**Assessment (AI, 2026-11-06):** review panel (full, re-review under LEAK-41, MET-14 to MET-16): ship after changes (the text changes made, above; the split fix of issue 8 waits on the curator's mark and a rebuild); disputed: the fix for a policy's later records that change one profile column and sit across the split (+0.020 for a model that reads training rows, 9 of 9 splits; a route across the grouped split that the leak test of 2026-11-02 above did not cover), a widened component or a per-fold filter, both sides now preferring the widened component (issue 8), and the length to 31 December on the log1p scale, dropped with LEAK-41's sentence on a part known at the start read as a permission (the advocate) or kept with the identity scale (the critic, and the mediator by rank) (issue 7); for the curator: issues 8, 7 and 9 (and cross-dataset item X2 on the word "ceiling").

CC (2026-11-08, Lennart): issue 8 (B), "Widen the component": the policy component also joins a record to a successor whose contract change changed one profile column (the same gender, starting the day the record ends, the driver's age the same or one more, the licence age advanced by the months between the starts within one, exactly one of the other five profile columns changed and no claim or out-of-use counter lower), so the group column `policy_component` has 61,091 components of 1 to 90 records. It widens the key of Andrej's call of 2026-11-03 (issue 1 (B): the cross-file component on six equal profile columns, 68,857 components) in the direction of that call, the most conservative key, and closes a route SPLIT-9 forbids.

**Assessment (AI, 2026-11-08):** issue 8 (B) is applied in `_policy_components`: the one-column links give 61,091 components of 1 to 90 records (90,373 records in components of two or more), the same partition the split auditor built on 2026-11-06. On the new shipped folds none of the 9,160 one-column pairs (over 7,120 earlier records) crosses a split, no test row has a candidate successor in training, and the auditor's lookup gains +0.001 (SD 0.012, higher on 5 of 9 splits; +0.020 on 9 of 9 before; the issue expected about -0.0045 from the auditor's own random folds), with the honest fit at 0.170 in the auditor's settings (0.174 before, an unpaired comparison). The route among the test rows that the LEAK-9 protocol line forbids stays: +0.355 with the in-component successor's counter rise and start, +0.259 with the next record of the file (9 of 9 each). Re-measured on the new folds (untuned LightGBM weighted by `Exposure`, 3 seeds): a Tweedie fit 0.181 (0.147 to 0.245; 0.183 before), squared error on log1p 0.152 (0.156), 1/`Exposure` alone 0.184, `Exposure` as a feature 0.258 (0.256), the length to 31 December alone 0.006 (0.005), random orders 0.001 (per-fold SD 0.037); for issue 7, squared error on log1p 0.184 without the length (lower with it on 9 of 9; 0.185, 7 of 9 before) and a Tweedie fit 0.177 without it (higher with it on 6 of 9); for issue 9, the month rounding -0.005 with a Tweedie fit (higher on 3 of 9; -0.002 before) and +0.002 with squared error on log1p, 2,714 records repeating another of their policy when rounded (2,704). `dataset check`: 0 errors, 0 warnings. Leak probe: no feature alone above an R^2 of 0.002, 0.4% of test rows with an exact feature copy in training. Group probe: no IID-grouped gap (R^2 0.005 both). Probe 22: `length_to_year_end` gains -0.029 through `Exposure` with a weighted Tweedie fit and -0.058 with L2, no feature above noise. The container is not rebuilt.

CC (2026-11-08, Lennart): issue 7 (b), "Identity scale, the length kept": the target ships as the claim amount per realized year, untransformed (`claim_amount_per_year`, no `target_transform`), and `length_to_year_end`, the length to 31 December known at the record's start, stays a feature. It reverses the clause of D9 (issue 6, Lennart, 2026-11-06) that kept the log1p scale: on log1p the length misleads a weighted squared-error fit, CLEAN-16 as amended then asks to drop the feature or ship the identity scale, and LEAK-41 ships the part of the time on risk known at the start as its own column, so only the identity scale meets both, as in pricing_game_2016_french_fleet (D11). D9's target, weight and metric stand.

CC (2026-11-08, Lennart): issue 9 (B), "Agree.": the length to 31 December ships unrounded. It depends on the start day alone, one value per start day at the source's precision, so its decimals carry no end and the month rounding of 2026-11-02 hides nothing; rounded to months, 2,714 records would repeat the features and target of another record of their policy and a weighted Tweedie fit would lose 0.003 to 0.005 (two runs on the same folds). D9 (issue 6) and this call supersede Andrej's call of 2026-11-02 (issue 2 (a): the 25,131 early ends given the length known at their start, the realized length kept on the 34,324 continued records, every length rounded to months), and D9 his call of 2026-11-03 (issue 4, option C: the length known at the start as the metric's base).

**Assessment (AI, 2026-11-08):** issues 7 (b) and 9 (B) are applied: `TARGET = "claim_amount_per_year"`, `ClaimAmount` / `Exposure` with no `target_transform` (`_clean` checks that the target times `Exposure` gives `ClaimAmount` back), the weight `Exposure` and `per_unit` unchanged; `predicted`, the notes on the dates, the length, the hybrid, the stand-ins, the learners, the target and the LEAK-9 oracle, the metric reason, the splits comment's probe lines and two CC bullets are rewritten. The folds are the same partition (every test fold holds the same policy components), but the container orders its rows by their content, the target included, so the rows changed order and the scores of fits that the scale does not touch moved by up to 0.005 (LightGBM's row subsampling). On the 9 shipped splits (untuned LightGBM weighted by `Exposure`, 3 seeds): a Tweedie fit 0.183 (0.143 to 0.240), squared error on the cost per year 0.154 (0.119 to 0.224; 0.029 below Tweedie, SE 0.004, 9 of 9), squared error on log1p 0.154 with the length and 0.184 without (lower with it on 9 of 9); the length adds +0.007 to Tweedie (SE 0.003, 6 of 9) and +0.002 to squared error on the cost per year (SE 0.004, 5 of 9; +0.004 and -0.003 in the run of the answer); 1/`Exposure` alone 0.184, `Exposure` as a feature 0.257 with Tweedie and 0.229 with squared error on the cost per year (+0.075 and +0.076, 9 of 9 each); the old hybrid length in place of the length 0.008 lower with Tweedie and 0.006 higher with squared error on the cost per year (SE 0.010, 7 of 9); the month rounding -0.003 with Tweedie (SE 0.0015, higher rounded on 2 of 9) and -0.002 with squared error; the next record of the file as an oracle +0.258 with Tweedie and +0.244 with squared error; ignoring the weight costs Tweedie 0.027 and squared error 0.058 (9 of 9 each). The repeats are unchanged: 610 records repeat another's features and target, 2,714 within their policy when rounded. `dataset check`: 0 errors, 0 warnings. Leak probe: no feature alone above an R^2 of 0, 0.4% of test rows with an exact feature copy in training. Task probe: `no_signal` (R^2 skill +0.001, the tail), while on the declared metric the linear family scores 0.203 and the dummy 0 (5 of 5 splits). Probe 22: `length_to_year_end` gains -0.038 through `Exposure` with a weighted Tweedie fit (SD 0.018) and -0.023 with L2 on the cost per year (SD 0.040), no feature above noise. The container is not rebuilt.

CC (2026-11-08, Lennart): the declared metric (`ordered_lorenz_gini` with `per_unit=True`, weighted by the realized length) is checked, as declared on the PR #47 review board; the rate now ships on the identity scale (issue 7 (b)).

CC (2026-11-08, Lennart): `Gender` leaves the features, on the stance Lennart set in australian_vehicle_insurance_2004_2005's issue 7 ("A stance for the family; as if we were to simulate the case in europe always"): sex is no rating factor of any insurance pricing task of this collection, whatever the actor's jurisdiction, as if the actor priced in the EU, where the Test-Achats ruling (CJEU C-236/09) has barred it for new contracts since 21 December 2012; the Tensions row on rating factors in principles.md is amended so. `Gender` stays in the key of the policy component. Supersedes the definition's note that kept `Gender` as the insurer recorded it, with an EU-law note (AI, /add-dataset, 2026-11-01), which shipped with Andrej's verdict of 2026-11-03.

**Assessment (AI, 2026-11-08):** the stance is applied: `_clean` builds `policy_component` with `Gender` among the profile columns (step 5) and drops it after (step 8); `_feature_types` no longer lists it; `known` and `changes` in the task summary, the notes (a "Dropped" bullet in place of the note that kept it, the dtypes, the copies, the length, the hybrid, the stand-ins, the learners, the fold noise and the LEAK-9 oracle), the grouping definition, the metric reason and the splits comment's leak-probe line are updated, and a CC bullet added. The partition is identical: the same 61,091 components (1 to 90 records, 90,373 records in components of two or more) and the same test records in every one of the 9 splits; `Gender` is constant within every component. The rows changed order (the container orders them by their content). `Gender` carried nothing measurable (untuned LightGBM weighted by `Exposure`, 9 splits x 3 seeds, the same rows and folds): a weighted Tweedie fit scores 0.1819 without it and 0.1815 with it (-0.0004 with it, SE 0.002, higher with it on 5 of 9 splits), squared error on the cost per year 0.1527 and 0.1519 (-0.0008, SE 0.002, 5 of 9), squared error on log1p 0.1542 and 0.1532 (-0.0009, 5 of 9). The cost per exposure-year is 434 for women and 450 for men, 9.4% of each with a claim. Without `Gender` (the scores in the notes and the metric reason, each moved by up to 0.004 from the run with it): a Tweedie fit 0.182 (0.147 to 0.245), squared error on the cost per year 0.153 (0.108 to 0.228), 1/`Exposure` alone 0.184, `Exposure` as a feature 0.254 with Tweedie and 0.228 with squared error, the next record as an oracle +0.257, random orders -0.001 (per-fold SD 0.035, 100 per fold), the 50,000 loss cap moves the folds that hold the largest claim by 0.021 to 0.075. More records repeat another's features and target: 928 (610 with `Gender`), none with a claim, 169 share the features with another target (130), 0.56% to 0.68% of each test fold has its features in training (0.35% to 0.48%); rounded to months, the length would make 2,704 records repeat another record of their policy (2,714). `dataset check`: 0 errors, 0 warnings. Leak probe: no feature alone above an R^2 of 0, 0.6% of test rows with an exact feature copy in training (0.5% with the same label only). Task probe: `no_signal` (R^2 skill +0.001), while on the declared metric the linear family scores 0.206 and the dummy 0 (5 of 5 splits; 0.203 with `Gender`). Probe 22: the features predict `Exposure` at R^2 0.34, 86% of the gain from `length_to_year_end`, which gains -0.051 through `Exposure` with a weighted Tweedie fit (SD 0.035) and -0.049 with L2 (SD 0.065), no feature above noise. Not re-run: the lookups of 2026-11-08 (the one-column successors in training, +0.001; the in-component successor, +0.355), measured with `Gender` on the same folds. The container is not rebuilt.

CC (2026-11-09, Andrej): a record gets no claim amount of the record its contract change continues and no flag that it continues one (review issue 10, A, as implemented); the claim counters and the bonus-malus stay the history.

CC (2026-11-09, Andrej): columns held only for training rows stay out for now, no training-only role (cross-dataset item of 2026-11-09; MET-14, LEAK-41, MET-16); the notes list them.

CC (2026-11-09, Andrej): the training labels' maturity is stated in the notes (cross-dataset item of 2026-11-09, option B).

CC (2026-11-09, Andrej): review issue 11, B: the metric is `normalized_weighted_gini` weighted by `Exposure`, in place of `ordered_lorenz_gini` per unit of `Exposure` (D9), with the reason in the curation notes ("I would like to change it as you said and also add an explanation why to the curation notes").

**Assessment (AI, 2026-11-09):** applied: the metric, its reason and a metric bullet in the notes (the two forms rank every model the same on each fold: ten predictors in the same order on each of the 9 shipped splits and on the mean; the perfect order's Gini is 0.959 to 0.966, so scores read 3.5% to 4.3% higher). The bullets on the metric's stand-ins, the learners and the paired comparisons are re-measured in the declared form (untuned LightGBM, 3 seeds; weighted Tweedie 0.178, squared error 0.146, 1/`Exposure` 0.191); older numbers are labelled unnormalised. `dataset check`: 0 errors, 0 warnings; README regenerated; no container built.

## Reference

CASdatasets (Dutang C., Charpentier A.), `freMPL1` to `freMPL10`, "Unknown French private insurer".
https://dutangc.github.io/CASdatasets/reference/freMPL.html

Lead: the two-regime-zero workbook (v4, 2026-10-19), Master rows 63-69 (freMPL2, freMPL3, freMPL5, freMPL6,
freMPL7, freMPL8, freMPL9).
