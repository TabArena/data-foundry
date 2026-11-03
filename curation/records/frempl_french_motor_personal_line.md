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

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured; extended on 2026-10-20 at Andrej's request with a file-by-file analysis of all ten tables. A human must verify the suggestion, the metadata and the notes before relying on them.**

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
shared reasoning is in `curation/inputs/two_regime_zero_triage_summary.md`, "Policy calls of 2026-10-30"); the curator
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

## Reference

CASdatasets (Dutang C., Charpentier A.), `freMPL1` to `freMPL10`, "Unknown French private insurer".
https://dutangc.github.io/CASdatasets/reference/freMPL.html

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master rows 63-69 (freMPL2, freMPL3, freMPL5, freMPL6,
freMPL7, freMPL8, freMPL9).
