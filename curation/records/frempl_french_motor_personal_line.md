---
unique_name: frempl_french_motor_personal_line
name: freMPL1-10 (CASdatasets, French motor personal line insurance, private insurer, 2004)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
- Larger IID Data
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

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured; extended on 2026-10-20 at Andrej's request with a file-by-file analysis of all ten tables. A human must verify the suggestion, the metadata and the notes before relying on them.**

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

## Reference

CASdatasets (Dutang C., Charpentier A.), `freMPL1` to `freMPL10`, "Unknown French private insurer".
https://dutangc.github.io/CASdatasets/reference/freMPL.html

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master rows 63-69 (freMPL2, freMPL3, freMPL5, freMPL6,
freMPL7, freMPL8, freMPL9).
