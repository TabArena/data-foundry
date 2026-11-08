---
unique_name: fremtpl2
name: freMTPL2
checked_by:
- Myunghwan
- Lennart
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 3
tags:
- Two-Regime Zeros
original_source: Other
year: '2014'
domain: insurance
required_split:
- Random (IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.kaggle.com/datasets/karansarpal/fremtpl2-french-motor-tpl-insurance-claims
- https://dutangc.github.io/CASdatasets/reference/freMTPL.html
- https://cas.uqam.ca/pub/web/CASdatasets-manual.pdf
- https://doi.org/10.2139/ssrn.3164764
v2_path: datasets/_dev/tabarena-v0pt2/fremtpl2/dataset.py
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

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 4: the documented French MTPL portfolio for claim frequency, an insurer's pricing task, and insurance is thin. The earlier plain `Yes` was set by the older AI pass (no curator name in `checked_by`), so it is put back to `TBD -> Yes` for the curator to confirm.
- Source: CASdatasets R package (Dutang and Charpentier), `freMTPL` page (https://dutangc.github.io/CASdatasets/reference/freMTPL.html): "risk features are collected for 677,991 motor third-part liability policies", "The period is approximately 2011-2013", source "Unknown private insurer". Two tables joined on `IDpol`: `freMTPL2freq` (677,991 x 12: `IDpol`, `ClaimNb`, `Exposure`, `Area`, `VehPower`, `VehAge`, `DrivAge`, `BonusMalus`, `VehBrand`, `VehGas`, `Density`, `Region`) and `freMTPL2sev` (26,444 claims: `IDpol`, `ClaimAmount`). The Kaggle link in `source_links` is a re-upload (karansarpal); the first publication is CASdatasets (the year it entered the package was not confirmed, so `year` stays empty; superseded 2026-11-05: `year` is 2014, Assessment below).
- Use case: an insurer sets the premium of a motor TPL policy at underwriting from the rating factors (claim frequency per year of exposure, Noll, Salzmann and Wuthrich, "Case study: French motor third-party liability claims", SSRN 3164764); fit direct for the frequency target `ClaimNb` with `Exposure`; regime IID, one row per policy-period and no date, but see the risks.
- Siblings and duplicates: `bemtpl97` (Belgian MTPL, CASdatasets, a different portfolio: no duplicate, PROV-7); no other freMTPL record (grep over `curation/records/` for fremtpl, MTPL, CASdatasets, ClaimNb). External collections: CASdatasets, OpenML (freMTPL2freq / freMTPL2sev uploads); used in Deprez, Verbeke and Verdonck, "Is TabPFN the Silver Bullet for Insurance Pricing?" (arXiv 2605.22892, 2026: TabPFN vs GLM and XGBoost on two public MTPL sets, frequency and severity).
- Papers and pages: CASdatasets manual https://cas.uqam.ca/pub/web/CASdatasets-manual.pdf; Noll et al. (doi:10.2139/ssrn.3164764); Denuit, Charpentier and Trufin 2021 (doi:10.1016/j.insmatheco.2021.09.001); Miljkovic and Fernandez 2018 (doi:10.3390/risks6020057); Pocuca et al. 2020 (doi:10.1016/j.insmatheco.2020.06.004); arXiv 2605.22892.
- Metric: no competition; the actuarial case study (Noll et al.) compares frequency models by the out-of-sample Poisson deviance with `Exposure` (read from the abstract and the papers that follow it, the full text not read here); likely a deliberate choice (MET-5), inputs `Exposure` (ships). Severity would be a gamma deviance on `ClaimAmount`. To confirm in /add-dataset; else the fallback.
- Risks for /add-dataset: choose the target (`ClaimNb` frequency with `Exposure`, or severity from the join, one `_sev` dataset); `ClaimNb` is capped and `Exposure` above 1 is truncated in the case study's cleaning (check); identical risk profiles recur across rows (the actuarial literature builds a group id from equal features before splitting), so check a grouped split (SPLIT, LEAK); some `ClaimAmount` values are fixed IRSA-IDA convention amounts ("Some claim amounts of `freMTPL2sev` are fixed claim amounts based on the French IRSA-IDA claim convention").
- Priority: gap + (insurance thin), use case + (pricing named by the case study), source + (CASdatasets page and papers), shape + (678k rows, mixed types), risk - (target, exposure and repeated profiles to settle).

---

Also see https://arxiv.org/abs/2605.22892 and https://cas.uqam.ca/pub/web/CASdatasets-manual.pdf

**AI note (two-regime-zero audit, 2026-10-19):** aggregate claim amount as target, on the OpenML copies (41214, 41215,
uploaded 2018):
* 678,013 policies, 96.32% with an aggregate amount of exactly 0.
* 9,116 of the 34,060 policies with `ClaimNb` > 0 have no severity row, so their summed amount would be a false zero.
* 195 OpenML severity rows name policies missing from `freMTPL2freq`. The current CASdatasets copy (GitHub, 26,444
  severity rows) is the OpenML table without exactly those 195.
* Siblings: `bemtpl97`, `frempl_french_motor_personal_line` (a different French portfolio).

CC (2026-10-28, Myunghwan): Hold freMTPL2, not reject it. Missing timing information prevents a defensible prediction point and split, and the released fields do not support a trustworthy contract/group-level evaluation. Preserve the candidate and completed evidence; reopen only if reliable timing and a defensible observation/linkage unit become available, followed by curator reconsideration.

**Assessment (AI, 2026-10-29):** Preserve the applied hold as TBD -> Yes with DF: Suspended, not No or scientific acceptance. Every released IDpol is distinct; identical rating profiles do not establish contract identity. The requested zero/non-zero association check found weak positive within-profile dependence (pair correlation about 0.017; 131 both-positive pairs versus 81.79 expected under the stated profile-size-stratified null), not a causal linkage finding. The approved task intent remains original uncapped ClaimNb with Exposure as a predictor and source count Poisson deviance. The annualized/capped implementation is an unapproved historical draft, omitted from this PR along with its v2 pointer; it is not a qualified version of the approved count task. The official active reservation was released. No automatic restart, refit, build or acceptance follows the hold.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `eumtpl` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-04, Lennart): `Yes`, added like beMTPL97 rather than held ("dont hold, add them and we can review them case by case"; on beMTPL97: "do (a) and ship both"): IID with the `ForcedIIDFromTemporal` tag (SPLIT-8). `eumtpl` is screened later ("we can screen that task later, this is fine for now without it, if it is a duplicate raise this again").

**Assessment (AI, 2026-11-04):** review panel (none): built through /add-dataset steps 0-6, no panel. 677,991 policies, the 2022 CASdatasets counts, `VehAge` 99/100 missing; `dataset check` passes and the probes flag nothing. Consecutive `IDpol` blocks look like consecutive years (48-60% of rows reappear one block later); the open questions are in the folder's REVIEW.md.

CC (2026-11-04, Lennart): IID with the Forced tag stays ("follow the recommendation"; the inferred links between `IDpol` blocks are not the source's key and change the score by nothing), and the claim counts are the 2022 CASdatasets version ("use the newer version"). The metric is checked as declared.

CC (2026-11-04, Lennart): resolved as implemented: exposure above one year is kept (two policy ranges recording whole contract periods) and the counts of 5 to 16 are kept uncapped (seven of the eight are one profile); both are named in the definition's notes.

**Assessment (AI, 2026-11-04):** review panel (none): built through /add-dataset steps 0-6 and checked against the literature (Noll et al.; Wüthrich and Merz 2023 Sec. 13.1); no panel ran, and all its issues are settled.

**Assessment (AI, 2026-11-04):** review panel (full, second pass after Lennart's PR #33 review): ship after changes, not as defined; disputed: LEAK-17/SPLIT-8/SPLIT-24 (IID or grouped on the inferred policy chains), LEAK-10 against LEAK-37 (realised `Exposure` as a feature), LEAK-10 (the `BonusMalus` mask, settled for blocks 0-4); for the curator: issues 5-9. Priority 3: gap +, use case -, source +, shape +, risk - (gap: insurance is thin among the 107 accepted definitions; use case: the fit is approximate, with no dates and realised exposure kept; source: the CASdatasets help page and the Noll, Salzmann and Wuthrich case study; shape: 677,991 rows, 10 mixed features; risk: likely leaks through `BonusMalus` and `Exposure` and the policy chains across the split, three Must issues open).

CC (2026-11-05, Lennart): "Blank blocks 0-4": `BonusMalus` is missing in `IDpol` blocks 0-4 (597,998 rows, 88.2%), where it looks recorded after the row's own claims, and kept in blocks 5-6, where it behaves like a start-of-year value (issue 5, B; LEAK-10, LEAK-7; as zillow_prize, melbourne_housing_market, online_shoppers). bemtpl97 keeps its `bm`, which its source registers at the start of the policy period. LightGBM Poisson with `Exposure` as a free feature, shipped folds (3): mean deviance 0.2327 before, 0.2435 after.

CC (2026-11-05, Lennart): "Set to missing": `DrivAge` 99 is missing in block 0 (66 rows), a default code like `VehAge` 99 (issue 9, B; CLEAN-10); the 4 rows at 99 outside block 0 stay at 99.

**Assessment (AI, 2026-11-05):** `year` set to 2014, the definition's value: freMTPL2freq and freMTPL2sev entered CASdatasets on 14 October 2014 (`pkg/inst/NEWS` at CASdatasets commit 324c15c999), the first publication (PROV-9). This supersedes the screening's "`year` stays empty" (2026-10-22).

CC (2026-11-05, Lennart): issue 6 (exposure) is parked, with bemtpl97's issue 1 and both declared metrics, until the zero-inflated stack (PRs #44-#47) is merged; a GitHub issue gives the context and the typical modelling (offset or weight).

CC (2026-11-05, Lennart): the split stays IID for now (issue 7, B); prior work uses a random hold-out or a split grouped on identical rating factors, none links records across years; revisit later.

CC (2026-11-05, Lennart): the renewal signal read from other rows is an evaluation leak handled by LEAK-9 as amended on 2026-11-05 (issue 8, (a)), named in `fit_reason`.

**Assessment (AI, 2026-11-05):** the parked exposure question is GitHub issue #51 (https://github.com/TabArena/data-foundry/issues/51).

**Assessment (AI, 2026-11-05):** PR #46 rebased onto `main`: Andrej's CC of 2026-10-20 (aggregate claim amount, temporal split on `year_index`) came from the zero-inflated branch and is kept as his proposal; the record's fields follow the later CC lines (2026-11-04/05, Lennart: `ClaimNb` with `Exposure`, IID with `ForcedIIDFromTemporal`), which the v2 folder implements. Whether the aggregate claim amount ships as a dataset of its own is open.

CC (2026-11-06, Lennart): option A of #51 (issue 6 of the folder's REVIEW.md): the target is claim_frequency = ClaimNb / Exposure, the claims per year insured; Exposure is the weight scoring column, the metric's `weight` input and the task's `sample_weight`, never a feature (LEAK-41, MET-14, MET-15, adopted 2026-11-06); `mean_poisson_deviance` with the floor 1e-4 claims per year (MET-13). It equals the source's count deviance with an exposure offset times n/sum(Exposure) of the scored rows (1.886 to 1.896 on the shipped folds), so models rank as by the source's metric. Supersedes the call of 2026-10-20 (Andrej, lines above: Exposure "a feature, not a divisor", capped at 1) and the AI line of 2026-10-29 that called the annualised form an unapproved draft: the conditional measurement came later (+0.0040 mean deviance as a free feature; never better at quotation), and with the weight, dividing does not inflate short records.

CC (2026-11-06, Lennart): the claim amounts (the proposal of PR #46) stay out for now; a task on the amount per year insured or on the claim size is a separate decision, made on leak-free numbers (D12 of the exposure study).

**Assessment (AI, 2026-11-06):** the definition now ships the 9 rating factors as features, with `Exposure` the weight scoring column, the metric's `weight` input and the `sample_weight`, never a feature (CC of 2026-11-06 above); issues 5, 6, 8 and 9 of the folder's REVIEW.md are resolved, and issue 7 is re-opened by a new measurement: one rating profile of 19 rows (72 claims over 3.63 years) makes 94-102% of the 0.0007 to 0.0017 by which the random split scores better than one grouped on identical rating factors. This supersedes the 2026-11-04 panel line's "realised exposure kept", "10 mixed features" and "three Must issues open", and the risk sign of its priority 3, which rested on them.

**Assessment (AI, 2026-11-06):** review panel (full, re-review under LEAK-41, MET-14 to MET-16): ship after changes, text only (made); disputed: issue 7 (a note on the one rating profile behind the gap to a split grouped on identical rating factors, or that grouping) and X2 (how LEAK-41's 1/weight ceiling reads for a deviance); for the curator: issues 7 and 10, and the cross-dataset items X1 and X2.

**Assessment (AI, 2026-11-06):** priority 3 stands (selection.md, Priority): a gap in the benchmark (insurance) +, a good shape (677,991 units, 9 features) +, a strong source (CASdatasets, Wüthrich and Merz) +; the fit stays approximate; a known risk -, now issue 7 re-opened (one 19-row rating profile makes the IID-against-grouped gap), in place of the exposure and the BonusMalus questions the 2026-11-04 line weighed, both settled.

**Assessment (AI, 2026-11-06):** the split question raised today (group on identical rating factors, for the one 19-row rating profile) is issue 11 of the folder's REVIEW.md, a new issue, not a re-opened issue 7: issue 7 (grouping on the inferred policy chains) stays resolved as of 2026-11-05. Where the three lines of 2026-11-06 above say "issue 7 is re-opened", "disputed: issue 7", "for the curator: issues 7 and 10" or "now issue 7 re-opened", read issue 11.

CC (2026-11-08, Lennart): issue 11 of the folder's REVIEW.md, as implemented (ok): the random split stays (`ForcedIIDFromTemporal`), with the note on the one rating profile of the high counts. Its 19 rows of 677,991 (72 claims over 3.63 years) make 94-102% of the 0.0007 to 0.0017 by which the random folds score better than folds grouped on identical rating factors; without them the gap is about 0, and LightGBM ranks ahead of a Poisson GLM under every split. Follows the IID call of 2026-11-05 (issue 7) and bemtpl97; the counts of 5 to 16 stay as kept on 2026-11-04.

CC (2026-11-08, Lennart): the declared metric (`mean_poisson_deviance`) is checked, as declared on the PR #47 review board.

CC (2026-11-08, Lennart): issue 10, reply (c): the `Two-Regime Zeros` tag stays, and bemtpl97 gets it too: the tag describes the target's distribution (96.3% of the policies without a claim), not the task's model, so a Poisson model that reproduces the zeros does not remove it; the tag's definition in records.md says so.
