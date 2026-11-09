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

**Assessment (AI, 2026-11-04):** review panel (none): built through /add-dataset steps 0-6, no panel. 677,991 policies, the 2022 CASdatasets counts, `VehAge` 99/100 missing; `dataset check` passes and the probes flag nothing. Consecutive `IDpol` blocks look like consecutive years (48-60% of rows reappear one block later); the open questions are in the record's Review.

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

CC (2026-11-06, Lennart): option A of #51 (issue 6 of the record's Review): the target is claim_frequency = ClaimNb / Exposure, the claims per year insured; Exposure is the weight scoring column, the metric's `weight` input and the task's `sample_weight`, never a feature (LEAK-41, MET-14, MET-15, adopted 2026-11-06); `mean_poisson_deviance` with the floor 1e-4 claims per year (MET-13). It equals the source's count deviance with an exposure offset times n/sum(Exposure) of the scored rows (1.886 to 1.896 on the shipped folds), so models rank as by the source's metric. Supersedes the call of 2026-10-20 (Andrej, lines above: Exposure "a feature, not a divisor", capped at 1) and the AI line of 2026-10-29 that called the annualised form an unapproved draft: the conditional measurement came later (+0.0040 mean deviance as a free feature; never better at quotation), and with the weight, dividing does not inflate short records.

CC (2026-11-06, Lennart): the claim amounts (the proposal of PR #46) stay out for now; a task on the amount per year insured or on the claim size is a separate decision, made on leak-free numbers (D12 of the exposure study).

**Assessment (AI, 2026-11-06):** the definition now ships the 9 rating factors as features, with `Exposure` the weight scoring column, the metric's `weight` input and the `sample_weight`, never a feature (CC of 2026-11-06 above); issues 5, 6, 8 and 9 of the record's Review are resolved, and issue 7 is re-opened by a new measurement: one rating profile of 19 rows (72 claims over 3.63 years) makes 94-102% of the 0.0007 to 0.0017 by which the random split scores better than one grouped on identical rating factors. This supersedes the 2026-11-04 panel line's "realised exposure kept", "10 mixed features" and "three Must issues open", and the risk sign of its priority 3, which rested on them.

**Assessment (AI, 2026-11-06):** review panel (full, re-review under LEAK-41, MET-14 to MET-16): ship after changes, text only (made); disputed: issue 7 (a note on the one rating profile behind the gap to a split grouped on identical rating factors, or that grouping) and X2 (how LEAK-41's 1/weight ceiling reads for a deviance); for the curator: issues 7 and 10, and the cross-dataset items X1 and X2.

**Assessment (AI, 2026-11-06):** priority 3 stands (selection.md, Priority): a gap in the benchmark (insurance) +, a good shape (677,991 units, 9 features) +, a strong source (CASdatasets, Wüthrich and Merz) +; the fit stays approximate; a known risk -, now issue 7 re-opened (one 19-row rating profile makes the IID-against-grouped gap), in place of the exposure and the BonusMalus questions the 2026-11-04 line weighed, both settled.

**Assessment (AI, 2026-11-06):** the split question raised today (group on identical rating factors, for the one 19-row rating profile) is issue 11 of the record's Review, a new issue, not a re-opened issue 7: issue 7 (grouping on the inferred policy chains) stays resolved as of 2026-11-05. Where the three lines of 2026-11-06 above say "issue 7 is re-opened", "disputed: issue 7", "for the curator: issues 7 and 10" or "now issue 7 re-opened", read issue 11.

CC (2026-11-08, Lennart): issue 11 of the record's Review, as implemented (ok): the random split stays (`ForcedIIDFromTemporal`), with the note on the one rating profile of the high counts. Its 19 rows of 677,991 (72 claims over 3.63 years) make 94-102% of the 0.0007 to 0.0017 by which the random folds score better than folds grouped on identical rating factors; without them the gap is about 0, and LightGBM ranks ahead of a Poisson GLM under every split. Follows the IID call of 2026-11-05 (issue 7) and bemtpl97; the counts of 5 to 16 stay as kept on 2026-11-04.

CC (2026-11-08, Lennart): the declared metric (`mean_poisson_deviance`) is checked, as declared on the PR #47 review board.

CC (2026-11-08, Lennart): issue 10, reply (c): the `Two-Regime Zeros` tag stays, and bemtpl97 gets it too: the tag describes the target's distribution (96.3% of the policies without a claim), not the task's model, so a Poisson model that reproduces the zeros does not remove it; the tag's definition in records.md says so.

CC (2026-11-08, Lennart): on D12 of 2026-11-06 (the claim-amount task kept out "for now"): "fremtpl2's claim-amount task -> which task is more representative of the real use case? use that one and the other is not created as we dont want to have duplicates". One task ships: the claims per year insured, as implemented (the AI's pick on the evidence below, issue 12 of the record's Review, for Lennart to confirm on the board); the claim cost per year insured is not created as a second dataset of the same policies. Supersedes Lennart's CC of 2026-11-06 that kept the amounts out for a later decision, and with it Andrej's proposal of 2026-10-20 (the aggregate claim amount as the target), which D12 had held open.

**Assessment (AI, 2026-11-08):** the two tasks measured on 9 random splits (the 3 shipped folds and two more partitions of the same rows), five honest models fitted with `Exposure` as the weight and never a feature. The join of freMTPL2sev is clean in the pinned release (26,444 claims on 24,944 policies, each count equal to its policy's claims with an amount, no amount without a claim); the amounts run from 1 to 4,075,401 EUR, the tail is real (French motor liability covers bodily injury without a limit, Code des assurances R211-7; CLEAN-11), and the largest claim is 6.8% of all amounts and 19% of the test fold it falls in. Claims per year, weighted Poisson deviance: the best LightGBM removes 2.26% of the constant's deviance (SD 0.18%, 9 of 9), the GLM 1.79%; a regularised LightGBM beats the GLM on 9 of 9 (split SD of the gap 0.03%, bootstrap SE within a fold 0.08%); Kendall's W of the five models 0.89. Claim cost per year: weighted Gini 0.23 to 0.27 with a split SD of 0.07 to 0.09 (0.34 to 0.40 on the three test folds that hold the 4.08M claim, 0.13 to 0.27 on the others), the GLM ahead of the regularised LightGBM by +0.011 on 7 of 9 (bootstrap SE 0.021), W 0.43; weighted Tweedie deviance at power 1.5 (floor 0.1 EUR) 5.4% of the constant's for the GLM (SD 4.4%). The rating factors predict no claim size beyond the tail (gamma GLM -0.8% with claims capped at 200,000 EUR, 3 of 9 above 0), and the frequency LightGBM times the mean claim ranks the cost per year better (Gini 0.29) than any model fitted on it. The insurer prices the cost per year from a frequency and a severity model (USE-5); here the rating part of the price is the frequency's, which the source scores (MET-1, MET-11). Same tail in bemtpl97's release (its largest policy amount 1.99M EUR, 6.1% of all amounts), so the same reasoning keeps its claims per year; bemtpl97 not edited.

CC (2026-11-08, Lennart): issue 12, A (as implemented): one task, the claims per year insured; the claim cost per year insured is not created.

## Review

**Outcome:** added. The AI recommends shipping it: the re-review panel of 2026-11-06 under the exposure rules found no
rule of validity broken, its changes are text only and made (below), and a new measurement raised a new split question
(issue 11, settled on 2026-11-08: the random split kept with the note). Like every container with a `sample_weight`, it
enters no run before the collection's training-weight gate (`BENCHMARK_CHANGES_TODO.md`, "Training weights", "The
gate"). A French motor third-party liability portfolio (CASdatasets freMTPL2, 677,991 policy records, about 2011-2013):
the target is the claims per year insured (`ClaimNb` / `Exposure`, 0 for 96.3%) from the 9 rating factors; `Exposure`,
the share of the year insured, is each record's weight in training and scoring and never a feature (option A of #51,
issue 6); random 3-fold split tagged forced from temporal; scored by the source's Poisson deviance, weighted by
`Exposure`. Validity: MET-14 and MET-15 hold (an unweighted LightGBM scores 0.50043 against the weighted constant's
0.47980 on fold 0, so a method must use the weight); LEAK-41 holds: the rating factors predict `Exposure` at R^2 0.17
and none gains through it above noise, and the notes now report what it would leak as a feature (+0.0082 Poisson,
+0.0075 L2; a rate fitted on it alone 0.47114 against the constant's 0.47929); LEAK-10 holds with `BonusMalus` blank in
blocks 0-4, where it likely follows the year's own claims (issue 5, EV-6); LEAK-9: next-year records found by reading
other rows (label-free flags about 0.0010) stay under the protocol line (issue 8); SPLIT-8 holds (IID with
`ForcedIIDFromTemporal`; holding out the later blocks costs +0.0009); SPLIT-29 does not apply (19 rows are not many),
but by SPLIT-30 the one rating profile behind 94-102% of the gap to a split grouped on identical rating factors was a
question for you, kept with the note on 2026-11-08 (issue 11). Value: MET-11 holds above the floor (the scorer equals
the source's offset count deviance times n/sum(Exposure), 1.886-1.896 per fold) and MET-13 holds (the floor of 1e-4 a
year binds for no prediction of a Poisson LightGBM); TP-2, a small real signal: a weighted Poisson LightGBM beats the
constant rate on 3 of 3 folds by 0.0096 to 0.0127 (D^2 about 2.3%, actual over expected 1.00, Gini 0.195), while a
random column moves fold scores by up to 0.0006, so strong methods differ in the fourth decimal; the task probe flags
`no_signal`, but the flag reads an R^2-type skill (+0.002), which a Poisson count has near 0.01 by nature, and on the
declared metric the probe's LightGBM scores 0.47283 against the dummy's 0.47838 and beats it on 3 of 3 splits (EV-3);
re-check with the first tuned run (TP-1). The honest skill fell from about 6% to 2% with the `BonusMalus` blanking
(issue 5), not with the rate target. Quality: CLEAN-11 (no cap, exposures above a year kept) and CLEAN-10 (default ages
missing) hold as settled. Weighed: the reference table of actuarial frequency modelling, scored by the source's own
metric +; `BonusMalus` blank in 88% of records, no dates, a thin signal -. Issues 10 (the record's tag stays, and
bemtpl97 gets it) and 11 (the random split stays) were settled on 2026-11-08, and so were X1 (the test rows' weight is
for the scorer only) and X2 (LEAK-41 reports the weight-alone score, no ceiling) in the working copy's REVIEW.md ("From
PR #47"), which this panel raised with bemtpl97's. Open since 2026-11-08, on Lennart's question about D12: which one
task these policies ship (issue 12, no panel). The AI keeps the claims per year and recommends it: on 9 random splits it
tells a regularised LightGBM from the GLM on 9 of 9, while a score of the claim cost per year insured follows where a
few claims land (one claim of 4.08M EUR is 18 to 19% of its test fold's claim amount; weighted Gini W 0.43); the claim
cost per year is not created.

Changes made after the review panel (AI, 2026-11-06), text only (rows, target, weight, metric, features and split
unchanged): the `Exposure` bullet reports LEAK-41's numbers on the declared metric; the two accepted duplicate warnings
give the counts the check now reports (181,197 copies, 8,128 conflicting rows) and read most groups as one policy-year
split into records; "Counts of 5 to 16" and `splits_comment` name the profile and its effect on the split; the split
and renewal numbers are restated on the declared metric and older numbers are marked; the `Exposure` description says
blocks 5-6 are cut mostly at a date; the metric's identity is stated above the floor; `known` and `fit_reason` say why
`BonusMalus` is blank and how small the signal is; the notes say a method must use the weight. The panel's reports
quote the definition before these changes.

**Main points:** Open: none. Settled on 2026-11-08: one task, the claims per year insured, and the claim cost per year
insured is not created (issue 12); the tag `Two-Regime Zeros` stays and bemtpl97 gets it, as the tag describes the
target's distribution (issue 10); the random split stays, with the note on the one rating profile behind its gap to a
split grouped on identical rating factors (issue 11).

**Issues for Lennart:**

5. **Blank `BonusMalus` in blocks 0-4, where it looks recorded after the row's own claims?**

   * **Problem:**
     - `BonusMalus` is the French bonus-malus coefficient (50 to 350), which falls by 5% after each claim-free year and
       rises by 25% per at-fault claim.
     - If a row's value was read after that row's claims, it carries the target, which the insurer does not know when
       quoting.
     - It looks recorded after them in blocks 0-4 (597,998 rows, 88%) and like a value taken at the start of the year
       in blocks 5-6.
   * **Background:** The blocks are the million-wide `IDpol` ranges, read as periods of three sub-portfolios (0-1, 2-3,
     4-5-6).
   * **Experiments:** column auditor; the frozen values confirmed by the claim and split auditors.
     - In blocks 4-6, where consecutive records of one policy can be compared, it behaves like a value taken at the
       start of the year: it falls in 92-94% of claim-free pairs and rises after a claim in 35-37%; it moves with the
       previous year's claims, hardly with its own row's.
     - In blocks 0-3 it is frozen across the two years (94.5% unchanged from block 0 to 1) and moves with its own
       row's claims as strongly as with the other year's.
     - The footprint is the first malus step from the floor, 62-63 (50 x 1.25), among drivers 30 and older:

     | rows | share at 62-63, with a claim | without a claim |
     |---|---|---|
     | blocks 0-3 | 5.3-6.8% | 1.5-1.7% |
     | block 4, no next-year row | 7.8% | 1.3% |
     | block 4 with a next-year row, and blocks 5-6 | 1.1-2.2% | 1.4-1.6% |

   * **Effect on the task:** `BonusMalus` carries 42% of LightGBM's gain over the mean count (0.0112 of 0.0269).
     Removing it worsens the deviance by 0.0131 in blocks 0-3 and changes it by -0.0005 (SE 0.0003, within noise) in
     blocks 5-6. It also carries most of the split leak of issue 7 (0.0021 with it, 0.0002 without).
   * **Unknown:** Not shown, likely[^likely]: no source statement says when the value was recorded (the panel's search
     of the source found none[^source-first]), and the whole freMTPL2 literature uses it as its main rating factor.
   * **Consistency:** Blanking follows zillow_prize and melbourne_housing_market (the second clause of the rule against
     features recorded after the outcome[^after-outcome]); none went the other way. Keeping it as is needs an amendment
     of that rule, not an exception.
   * **Panel:** The critic's narrower mask (blocks 0-3 plus the block-4 rows without a next-year row) was rejected by
     the mediator: there a missing value would mean "not renewed", and those rows claim 0.141 against 0.070 per year,
     missingness that encodes the outcome[^after-outcome].
   * **Option details:**
     - B: blank it in blocks 0-4 (597,998 rows, 88%), the form of online_shoppers ("keep only the period where it
       behaves like history").
     - C: drop the column, equivalent in effect; it adds nothing measurable in blocks 5-6.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | in all rows | the main rating factor | likely holds the target; a rule amendment |
     | B | Blank blocks 0-4 | 88% of rows missing | as online_shoppers; smallest fix[^smallest] | gone in 88% of rows |
     | C | Drop the column | removed | same effect; nothing lost in blocks 5-6 | also gone where it is history |

   * **Recommendation:** B, blank blocks 0-4. **Decision:** A (keep as is, an amendment of the rule), B (blank blocks
     0-4) or C (drop the column)?

   [^after-outcome]: **LEAK-10** (Must). Blanking follows its second clause (zillow_prize, melbourne_housing_market);
     keeping the column as is needs an amendment of LEAK-10, not an exception.
   [^likely]: **EV-6**: "likely", not shown.
   [^source-first]: **LEAK-3** (Should): read the source first.
   [^smallest]: **LEAK-7**: the smallest fix.

   **Resolved (2026-11-05, Lennart):** B. `BonusMalus` is missing in `IDpol` blocks 0-4 (597,998 rows, 88.2%) and kept
   in blocks 5-6 (79,993 rows, 50-190). Re-measured on the same folds (LightGBM Poisson, `Exposure` a free feature):
   mean deviance 0.2327 to 0.2435, +0.0127 in blocks 0-3, and 0.0013 better in blocks 5-6, where the column now carries
   0.0007-0.0009 (so B over C). The next-year channel of issue 7 falls from 0.0020 to 0.0008; the "0.0021 for claim
   count and exposure" in the notes was wrong (they are worth 0.0003) and is corrected. bemtpl97 keeps its `bm`: its
   source registers the risk factors at the start of the policy period. A LEAK-10 Cases row; `dataset check` clean, leak
   probes without a flag.

6. **Take realised `Exposure` out of the features and score with it as an offset?**

   * **Problem:**
     - `Exposure` is the share of the year the policy was insured, known at the end of the period.
     - A policy cancelled after a claim gets a short exposure, so the column carries part of the outcome.
     - At quotation the insurer knows the planned term, not a later cancellation.
   * **Background:** Now `Exposure` is a free feature under "Potential leak, kept on purpose", as in
     bemtpl97[^bemtpl97]; the note now gives the sizes below.
   * **Experiments:** claim auditor, column auditor, domain practitioner, task gamer.
     - Among rows with a previous-year record (renewals, no new business), rows with exposure of 0.1 years or less
       claim 0.255 a year against 0.056 for a full year.
     - Within each exposure band, a claim lowers the chance of a next-year record (0.19 against 0.27, up to 0.47
       against 0.53).
     - A Poisson GLM on the rating factors gives log(`Exposure`) a free coefficient of 0.641, where a pure offset would
       be 1.
     - Size of the kept leak: used as a free feature beyond a log(`Exposure`) offset it is worth 0.0039-0.0045 mean
       deviance, 14-19% of LightGBM's gain (three agents). The proportional, legitimate part is 0.0061 (0.2595 to
       0.2534). Part of the excess is renewals during the year recorded as two records (Wüthrich and Merz 2023,
       [Sec. 13.1](https://link.springer.com/chapter/10.1007/978-3-031-12409-9_13)), so the leak is mixed but not
       absent.
   * **Consistency:** No exception of the rule against features recorded after the outcome covers it[^no-exception]. A
     follows kick `WheelType` (2026-10-22) and heart_failure_followup_survival `time` (2026-09-30), both dropped once
     the mechanism was measured; it departs from bemtpl97, where the mechanism had not been measured.
   * **Panel:** Disputed: the advocate argued the exception for a planned term[^no-exception] and conceded that a note
     does not resolve a Must[^after-outcome]; the critic asks for A.
   * **Option details:**
     - A: `Exposure` becomes a scoring column and the score is the Poisson deviance of the predicted rate x
       `Exposure`, the offset form of Noll, Salzmann and Wüthrich. It costs a new metric in
       `src/data_foundry/v2/metrics.py` and reopening bemtpl97 to match.
     - B: keep it and amend the rule[^after-outcome] for exposure denominators, recording 0.0039-0.0045 as the leak's
       size.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Offset in the score | `Exposure` scores only | removes the leak; as kick | new metric; reopen bemtpl97 |
     | B | Keep, amend the rule (implemented) | free feature, noted | as bemtpl97 | leak of 14-19% of the gain |

   * **Recommendation:** A (mediator). **Decision:** A or B, with bemtpl97 following the same call?

   [^after-outcome]: **LEAK-10** (Must).
   [^no-exception]: **LEAK-37** covers a planned term, and none ships; **LEAK-11** needs a value that weakens the
     signal, and this one strengthens it; **LEAK-38** sends a measured mechanism back to **LEAK-10**. The advocate
     argued LEAK-37.
   [^bemtpl97]: Myunghwan, 2026-10-23 and 2026-10-26 (bemtpl97).

   **Lennart (2026-11-05, discuss):** We have a stack of PRs for zero inflated data and exposure, is this already
   handled there? Note that it is quite important to treat this correctly and it might need to be used as sample weight
   or a feature that can be used as such (maybe as a special feature metadata?) please check the PR stack and context
   background what we should do here

   **Answer (AI, 2026-11-05):** Not handled. PRs #44 to #47 add no exposure offset, no Poisson deviance with an exposure
   input and no training-weight declaration, so option A still needs new code. What they do:
   - #44 adds a LEAK-10 case row, "time on risk cut short by the outcome" (Andrej, 2026-11-02): fix the cut where the
     data locates it, otherwise keep it with a measured note. It names fremtpl2 as a departure.
   - #44 and #45 let an input known at the prediction point stay a feature and also be the metric's weight; #45's
     `mean_poisson_deviance` takes no weight.
   - #47's spanish_motor_insurance_coverage_level_2022_2024 comes nearest to A (a per-year target, exposure as a weight
     scoring column); its issue 5 says "Data Foundry has no training-weight column yet".
   - #46 rewrites this record from an older base with Andrej's CC of 2026-10-20, a different design (total claim amount,
     a split by IDpol block, Exposure capped at 1 as a feature); merging it conflicts with this definition, and the two
     designs need reconciling.

   The actuarial convention is a Poisson GLM with offset log(Exposure) ([Noll, Salzmann and Wüthrich,
   code](https://github.com/JSchelldorfer/ActuarialDataScience)), or the frequency ClaimNb/Exposure with Exposure as the
   sample weight
   ([scikit-learn](https://scikit-learn.org/stable/auto_examples/linear_model/plot_poisson_regression_non_normal_loss.html));
   both give the same deviance. A special feature is the wrong place: special features are model inputs. The right shape
   for A, here and in bemtpl97: target ClaimNb/Exposure, `Exposure` a weight scoring column, `mean_poisson_deviance`
   with a `weight` input, and a declared training weight that the benchmark passes as `sample_weight` and never as a
   feature. That last part is new in the API, the container and the benchmark.
   - (a) A, for this dataset and bemtpl97: exposure becomes a weight, in the score and in training (new code);
   - (b) B, for both: the feature stays, with an amendment of LEAK-10 for exposure as a denominator.

   **Lennart (2026-11-05, discuss):** open this as a seperate issue on github, provide the context for it there and what
   typical modelling would do and park this and bemtpl until then and the stack of zero-inflated is over

   **Deferred (2026-11-05):** parked, with bemtpl97 issue 1 and both declared metrics, until the zero-inflated stack
   (PRs #44-#47) is merged. The GitHub issue (context, typical modelling: an offset or a weight, what the stack provides
   and what is missing) is [#51](https://github.com/TabArena/data-foundry/issues/51).

   **Resolved (2026-11-06, Lennart):** A, as the rate with a weight (option A of
   [#51](https://github.com/TabArena/data-foundry/issues/51), the exposure study of 2026-11-05). The target is
   `claim_frequency` = `ClaimNb` / `Exposure`; `Exposure` is the weight scoring column, the `weight` input of
   `mean_poisson_deviance` and the task's `sample_weight`, and never a feature (LEAK-41, MET-14, MET-15, adopted the same
   day); the floor is 1e-4 claims per year (MET-13). This is the offset model: on every shipped fold the weighted rate
   deviance equals the count deviance of the same predictions times n/sum(Exposure) of the scored rows (1.886 to
   1.896), so models rank as by the source's metric. Supersedes Andrej's call of 2026-10-20 ("a feature, not a
   divisor", capped at 1) and the parking above: the conditional measurement came later (+0.0040; never better at
   quotation), and with the weight, dividing does not inflate short records. `dataset check`: 0 errors, 0 warnings.

7. **Group the split on the inferred policy chains (`ForcedGroupedFromTemporal`) instead of IID?**

   * **Problem:**
     - The release has no dates, but `next_year_rows` links 161,883 pairs of records across consecutive `IDpol` blocks
       (same car and region, the driver one year older), against 16 to 75 under shuffled or shifted controls (a chance
       rate of 0.02-0.05%).
     - Under the random split, 16% of test rows have the same policy's next-year record on the training side, and a
       model that reads other rows (a nearest-neighbour or in-context model, or a participant's lookup feature) can
       find it from the shipped columns alone: the true partner is the only candidate for 54.6% of linked rows.
     - That record holds information about this year's claims that an insurer pricing a renewal never has, because it
       comes from the future.
   * **Background:** The definition is IID with `ForcedIIDFromTemporal`, your call of 2026-11-04[^call]. The first
     pass recommended IID, and "follow the recommendation" took that advice; this pass measured the next-year channel
     and recommends grouping.
   * **Experiments:**
     - The next-year record's claim count and exposure lower mean deviance by 0.0021 with `BonusMalus`, 0.0002 without
       it (3 of 3 folds), and by nothing under grouped folds (mediator). The previous-year record, legitimate history,
       is worth 0.00015.
     - Relinked from shipped columns only, a stacked GLM gains 0.0057 skill (the share of the exposure baseline's
       deviance a model removes) on 3 of 3 folds; grouping on the chains halves it to 0.0024 (domain practitioner).
     - For models that score one row at a time, grouping costs nothing: LightGBM mean deviance 0.23265 shipped against
       0.23238-0.23245 grouped (three seeds), a difference of 0.0002-0.0003 (SE 0.0002), about the 0.0002 by which two
       random seeds differ.
     - The entity carries little of the label itself: pair correlation of claims 0.017.
   * **Consistency:** Grouping follows nba_players_2016_2019 and open_university_learning_analytics_dataset
     (2026-10-21, grouped on a key the release gives). The rules ask for a split by the entity when the periods are
     stacked and the entities recur across them[^entity], and bar the size of the gap as a reason[^gap].
   * **Panel:** Disputed: the critic and the mediator ask for A; the advocate holds that grouping does not remove the
     label-free renewal signal (issue 8) and that the rule on constructed keys[^key] does not clearly admit a
     rule-built key.
   * **Option details:**
     - A: `ForcedGroupedFromTemporal` on the `next_year_rows` chains, with the rule also searching IDpol offsets -1 to
       -9 (another 26,851 matches between rows the forward search leaves unpaired). It needs a ruling that a key built
       by this exact rule counts as "constructed exactly from the data"[^key], and it changes the split; row-wise scores
       do not move.
     - B: keep IID and record the facts that set the case apart: the links are inferred between inferred years, the
       entity carries almost none of the label (pair correlation 0.017, so the rule on entities that carry the label
       does not fire[^label-entity]), and pricing serves renewals, which are known policies[^renewals]. After issue 5
       the label channel left is 0.0002, a size and not a reason.
     - C and D are the consistency check's (c) and (d) below.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Group on the chains | `ForcedGroupedFromTemporal` | as nba, open_university | a ruling on the key |
     | B | IID, facts recorded (implemented) | notes give the facts | row-wise scores same | departs from the text |
     | C | A year per sub-portfolio | 353,887 rows | as distribution_transformers_at_cauca_department | fewer rows |
     | D | Amend the rule | IID for inferred entities | IID the closest regime | a rule change |

   * **Recommendation:** A (mediator). **Decision:** A, B, C or D (the consistency check's (a) to (d) below)?

   [^entity]: **LEAK-17** (Must) and **SPLIT-8**'s text ("grouped by the entity when the periods are stacked and the
     entities recur across them"), against **SPLIT-13** (Should).
   [^gap]: **SPLIT-4** and **SPLIT-30** bar the size of the gap as a reason.
   [^key]: **SPLIT-24**: a key "constructed exactly from the data".
   [^label-entity]: **SPLIT-29**.
   [^renewals]: **SPLIT-13**, **USE-10**.
   [^call]: Lennart, 2026-11-04: "follow the recommendation"; the links "are not the source's key and change the score
     by nothing".

   **Consistency check (AI, 2026-11-04):** your call on fremtpl2 (IID on stacked periods with recurring policies,
   2026-11-04) departs from SPLIT-8's text and differs from nba_players_2016_2019 and open_university (grouped,
   2026-10-21). Its stated reason, "change the score by nothing", is one SPLIT-4 and SPLIT-30 do not count, and the
   next-year channel (0.0021) was not measured then. What sets fremtpl2 apart?

   - (a) No fact sets it apart: group on the chains, as nba and open_university were.
   - (b) The links are inferred between blocks whose years are themselves inferred, the entity carries almost none of
     the label (correlation 0.017, SPLIT-29 does not fire), and pricing serves renewals (SPLIT-13): recorded in the
     notes in place of "change the score by nothing".
   - (c) Keep one inferred year per sub-portfolio, as distribution_transformers_at_cauca_department (blocks 0, 2 and 4:
     353,887 rows).
   - (d) Amend SPLIT-8: when entities are only inferred and carry little of the label, the closest regime is IID.

   **Lennart (2026-11-05, discuss):** How is this data used in related work and prior work? what did people do i nthe
   past for this dataset?

   **Answer (AI, 2026-11-05):** No published use links freMTPL2 records across years; papers use a random hold-out, or
   lately a split grouped on identical rating factors.
   - Noll, Salzmann and Wüthrich: random 90/10 (`set.seed(100)`), ClaimNb capped at 4 and Exposure at 1, Poisson
     deviance of a GLM with offset log(Exposure) ([code](https://github.com/JSchelldorfer/ActuarialDataScience)).
   - Wüthrich and Merz (2023, [Sec. 13.1](https://link.springer.com/chapter/10.1007/978-3-031-12409-9_13)): claims
     recounted from freMTPL2sev, Exposure capped at 1, one fixed 610,206/67,801 partition that later papers reuse; they
     note that renewals are split into two records but "do not have the necessary information to perform this merger".
   - Schelldorfer (2021 code) and [Lorentzen and
     Mayer](https://lorentzenchr.github.io/responsible_ml_material/xai_2_explaining_models.html): 80/20 grouped on
     identical rating factors, since ignoring the groups lifts LightGBM's pseudo-R² from 5.0% to 6.0%.
   - scikit-learn: random 67/33; [Holvoet et al.](https://arxiv.org/abs/2310.12671): six stratified folds. OpenML 41214
     has no supervised task.

   So A (grouping on the chains) goes further than any prior work, and the literature's key (identical factors) is not
   our chain key. If you group, the key that joins the chains with identical-factor rows (430,298 groups in the notes)
   is exact and close to the literature's; otherwise B, with the literature (a random split) as the recorded reason. Not
   verified: how Wüthrich and Merz drew their partition (the chapter was not readable).

   **Lennart (2026-11-05, discuss):** Ok so from this I take we can tick to IID for now based on the samll survey but
   may need to revist this in the future

   **Resolved (2026-11-05, Lennart):** B. The split stays IID with `ForcedIIDFromTemporal` for now; prior work gives no
   reason to group, and it is revisited if the inferred policy chains become a recorded key.

11. **Keep the random split with a note on the one rating profile behind its gap to a split grouped on identical rating factors, or group on those factors?**

   * **Problem:**
     - The re-review of 2026-11-06 ran the grouping your survey of issue 7 found in prior work, folds grouped on
       identical rating factors, and the random folds score 0.0007 to 0.0017 better, 94-102% of it from one profile.
     - That profile is the same car and driver a year apart, 19 rows with 72 claims over 3.63 years (19.8 claims a year
       against the portfolio's 0.074), which Wüthrich and Merz suspect to be one driver or a rental fleet; it holds
       seven of the eight policies with 5 to 16 claims you kept on 2026-11-04.
     - Under the random split LightGBM predicts 3.8 to 17.2 claims a year for the profile's test rows from their copies
       on the training side (0.073 to 0.078 when grouped), the only memorization the random split rewards.
   * **Background:**
     - Issue 7 (resolved 2026-11-05, B) settled grouping on the inferred chains. This is a different key, the one prior
       work uses.
     - The profile: power 4, brand B1, regular fuel, area D, density 824, Languedoc-Roussillon, bonus-malus 50 (blank as
       shipped), car and driver aged 12 and 52 in block 2, 13 and 53 in block 3; its rows fall 6/7/6 into the three test
       folds.
     - Your call of 2026-11-05 rests on prior work, and one strand of it, Schelldorfer (2021) and Lorentzen and Mayer,
       groups on identical rating factors because ignoring the groups lifts LightGBM's pseudo-R^2 from 5.0% to 6.0%; the
       correlation of 0.017 in issue 7's option B was measured on the inferred chains, not on this profile.
     - On this table the 9 shipped rating factors are the whole feature vector, and 92.9% of their 138,537 groups of
       identical rows sum to at most 1.01 years, so most groups look like one policy-year split into records.
   * **Effect on the task:** On the random split LightGBM scores better by 7-15% of its gain over the constant rate,
     almost all of it from recognising this profile; a Poisson GLM gains 0.0001, and LightGBM ranks ahead of the GLM
     under every split.
   * **Experiments:** split and claim auditors, independently, LightGBM Poisson fitted with the weight, 7 runs of 3
     folds:
     - grouped minus random: +0.00157 and +0.00167 on the shipped folds, +0.0007 to +0.0013 with other seeds;
     - without the profile's rows: -0.0002 to +0.00015;
     - an explicit memorizer gains nothing: a lookup of the profile's training rate blended into LightGBM scores 0.46823
       against 0.46813, and the training twins' claims, left one out, add +0.0001 on average;
     - grouping costs nothing elsewhere: 488,666 groups, folds of 224,778 to 226,838 rows;
     - holding out the later blocks costs +0.0009 (SE 0.00035), +0.00046 without the profile.
   * **Consistency:**
     - A follows your call of 2026-11-05 and bemtpl97 (random split; the two treated alike on 2026-11-04).
     - B departs from maternal_health_risk, where a key made of the whole feature vector was barred as a stand-in for an
       unknown entity[^fv-key], and from bemtpl97, unless you rule that the profile is the entity here.
     - C undoes your keep of the counts of 5 to 16 of 2026-11-04.
   * **Panel:** The advocate and the critic agree that the new fact goes to you, and the mediator recommends A.
     - Advocate: 19 rows are not the many rows that make a random split wrong[^many-rows], LightGBM ranks the same under
       every split and the size of a gap decides nothing[^gap-size], and new quotes keep their rating profile, which
       makes it a feature[^composite].
     - Critic: Schelldorfer and Lorentzen and Mayer group on exactly this key against exactly this optimism, and a key
       whose groups mostly sum to one policy-year marks the entity, which the rule on keys allows[^fv-key].
   * **Unknown:** whether the profile is one contract, one driver or one fleet; a source statement, or your ruling that
     identical rating factors define the entity for freMTPL2, would settle it.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the random split, with the note (implemented) | the notes and `splits_comment` name the profile and its effect | follows your call of 2026-11-05 and bemtpl97; 19 rows of 677,991 are not many | an optimism of about 0.001 on LightGBM stays |
     | B | Group on identical rating factors | `ForcedGroupedFromTemporal`, the 9 shipped factors as the group key (488,666 groups, 350,129 of them single rows) | the key of Schelldorfer and of Lorentzen and Mayer; removes the only memorization | a ruling that the profile is the entity; bemtpl97 checked alike |
     | C | Drop the profile's 19 rows | a row filter in `_clean` | removes the memorization | undoes your keep of 2026-11-04; nobody recommends it |

   * **Recommendation:** A, keep the random split with the note: 19 rows of 677,991 do not make a random split wrong,
     LightGBM ranks the same under every split, and the size of the gap decides nothing; B is the choice if you read
     the profile as one policy or one fleet, and then a consistency check with maternal_health_risk and bemtpl97 comes
     first. **Decision:** A, B or C?

   **Notes for the AI:** on B, give the definition a `Grouping` whose group column is built from the 9 shipped rating
   factors (`BonusMalus` blank in blocks 0-4; never a feature), set the tag `ForcedGroupedFromTemporal`, rewrite
   `splits_comment`, `task_summary.split` and the notes' split bullets, re-run `dataset check` and the group and leak
   probes, record the answer to the consistency check, and check bemtpl97 for the same structure. On C, filter the 19
   rows in `_clean` (the profile above) and rewrite the "Counts of 5 to 16" bullet. On A, nothing more: the note is in
   the definition. Either way the SPLIT-8 Cases row of fremtpl2 in `splits.md` follows the decision. If Lennart picks
   B, post a `**Consistency check (AI, <date>):**` turn before applying it: grouping on identical rating factors departs
   from maternal_health_risk (a feature-vector key barred) and from bemtpl97 (random split). Options: (a) the
   literature's key, with 92.9% of groups at most a policy-year, recorded as the fact that sets it apart; (b) keep the
   random split; (c) reopen bemtpl97; (d) amend the rule on constructed keys.

   [^many-rows]: **SPLIT-29** (Must): an IID split is wrong when many rows share an entity that new data would not have
     and the entity carries the label; **LEAK-17** (Must) groups repeated entities.
   [^gap-size]: **SPLIT-4** and **SPLIT-30** (Must): the split follows what the task does in reality, not the size of
     the gap; a hidden-group hit is a question, and the data is re-split only when the context says the rows share an
     entity new data would not have, or the evidence is very strong.
   [^fv-key]: **SPLIT-24** (Must): group on a true id or on one constructed exactly from the data, such as identical
     values in the columns that define the entity, never on a hash of the feature vector standing in for an unknown
     entity (maternal_health_risk).
   [^composite]: `splits.md`, "Composite keys": when the key is what one row's entity is, group on it; when new rows
     keep the key, it is a feature.

   **Resolved (2026-11-08, Lennart):** A, as implemented: the random split stays (`ForcedIIDFromTemporal`), and the
   notes and `splits_comment` name the profile and its effect on the gap to a grouped split; the CC of 2026-11-08 in
   the notes and the record says so. Rows, target, weight, metric and split are unchanged.

8. **Keep the label-free renewal and record-structure signal with a note?**

   * **Problem:**
     - Whether a policy has a later or a sibling record can be read from the test features themselves.
     - A policy with a later record was renewed rather than ended, and renewed policies claim about half as often
       (0.070 against 0.141 claims per year in block 0).
     - A model that computes these signals from the test rows learns whether the policy was renewed, which the insurer
       does not know when quoting.
   * **Background:** Statistics over train and test rows of the records identical except `Exposure` (their number and
     summed exposure) carry the same early-termination effect. Now kept; the notes do not name it.
   * **Experiments:** the renewal signal is worth 0.0017 mean deviance with `BonusMalus` (split auditor) and
     0.0009-0.0010 without it (mediator), under random and grouped folds alike; the task gamer's record-structure
     statistics gain 0.0006-0.0007.
   * **Consistency:** none for record existence. The rule on transductive leaks covers scaling only, so this is a
     weighing call[^transductive].
   * **Option details:** none removes it. No split does, and merging records into one row per policy-year needs a key
     the source does not give, so the only other way is a `No`.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep with a note (implemented) | a note and a tension row | the data as published | a weak leak stays |
     | B | `No` | the dataset does not ship | no such leak | loses the dataset |

   * **Recommendation:** A, keep with the note. **Decision:** A (keep with the note; the tension row follows) or B
     (`No`)?

   **Notes for the AI:** on A, add a `Potential leak, kept on purpose:` note with these numbers, and a new row under
   the tension "a weak transductive leak against the data as published" (today it lists only the scaling cases
   sf_permit_time and home_credit), written in the same change.

   [^transductive]: **LEAK-10** (the mechanism, transductive); **LEAK-30** covers scaling only.

   **Consistency check (AI, 2026-11-05):** the signal comes from a model reading other rows, so it is an evaluation leak
   (LEAK-9), not the scaling of stored values (LEAK-30). Kept with a note, it is the fourth case met by a protocol line,
   after sepsis_prediction_1m, 5g_energy_consumption and medical_facility_operational_data issue 7, whose check is open.
   - (a) the LEAK-9 note and the medical issue 7 protocol line, settled with medical 7's answer (its amendment would
     cover this case too);
   - (b) a LEAK-30 tension row, as the issue proposes;
   - (c) `No`.

   Give the letter in the note. Either way the leak is named in `fit_reason` with its size without `BonusMalus`
   (0.0009-0.0010), which fits issue 5.

   **Lennart (2026-11-05, ok):** Reply (a): the LEAK-9 note and the medical issue 7 protocol line, settled with medical
   7's answer (its amendment would c…

   **Resolved (2026-11-05, Lennart):** (a). The renewal signal is an evaluation leak handled by LEAK-9 as amended today
   (a protocol line the benchmark checks; a method that learns from the test block is called out and not benchmarked);
   `fit_reason` names it. After issue 5 it is worth 0.0008 mean deviance.

9. **Set `DrivAge` 99 to missing in block 0, as `VehAge` 99/100 is?**

   * **Problem:**
     - 70 rows have a driver aged 99, against 5 at 98 and 3 at 100; 66 of them are in block 0, after 1 row at 96 and
       none at 97-98, none of the 66 has a next-year record (62.7% of block 0 has one), and block 1 has no driver
       older than 97.
     - That is the default-code pattern for which the definition sets `VehAge` 99 and 100 to missing.
     - Kept, a model reads 66 unknown ages as 99-year-old drivers; the effect is limited to those rows.
   * **Background:** Now kept "as possible".
   * **Consistency:** `VehAge` in the same definition[^default].
   * **Panel:** Both the advocate and the critic conceded the change.
   * **Option details:**
     - A: keep 99 and record that it is a top code (a real age of 99 or more).
     - B: set the 66 block-0 values to missing, a cleaning change, so left to you.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | 99 a top code (implemented) | kept, reason recorded | no cleaning change | 66 unknown ages as 99 |
     | B | Set to missing | the 66 block-0 values missing | as `VehAge` | a cleaning change, so left to you |

   * **Recommendation:** B, set the 66 values to missing. **Decision:** B (missing) or A (a recorded top-code reason)?

   [^default]: **CLEAN-10** (Should).

   **Lennart (2026-11-05, change):** Option B: Set to missing.

   **Resolved (2026-11-05, Lennart):** B. `DrivAge` 99 in block 0 (66 rows) is missing, as `VehAge` 99 and 100; the 4
   rows at 99 in blocks 3-4 stay (three pair a year apart with a real age). A CLEAN-10 Cases row. The record's `year` is
   2014 (PROV-9).

10. **Keep the record's tag `Two-Regime Zeros` on a claim-count target?**

   * **Problem:**
     - The record carries the tag `Two-Regime Zeros`, which came with a proposal to predict the claim amount, a task
       that stays out for now[^amount].
     - The tag marks a target whose lowest value is by far the most frequent one and separate from the rest of its
       distribution[^tag-def], while the shipped target counts claims per year insured, 0 for 96.3% of the records.
     - A Poisson count reproduces those zeros: from the rating factors and each record's time insured it expects 96.2%
       zeros against 96.3% observed, so the zero is the count's first step, not a regime of its own.
   * **Effect on the task:** none on the rows, the split or the score: the tag lives only in the record, a priority tag
     on the dashboard, and lists the dataset among the two-regime targets.
   * **Experiments:** the review writer (AI), on the 3 shipped folds, out of fold: a weighted Poisson LightGBM's rate
     times the time insured expects 96.23% zeros, the constant portfolio rate 96.21%, against 96.32% observed.
   * **Consistency:** Dropping it follows how_much_did_it_rain_ii (2026-10-30) and
     thailand_road_accident_register_2019_2022 (2026-11-01), whose tags went when the zero proved the count's first
     step[^tag-cases]; the insurance tables that keep it predict a claim amount (australian_vehicle_insurance_2004_2005,
     spanish_motor_insurance_coverage_level_2022_2024).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the tag (implemented) | the record stays tagged | none found for the shipped count | a count tagged as a two-regime target |
     | B | Drop the tag | the record's `tags` lose it | follows the tag's definition and the thailand precedent | none found |

   * **Recommendation:** B, drop the tag: the shipped target is a count whose zeros a Poisson model reproduces; a CC
     restores it if the amount task comes back. **Decision:** A or B?

   **Notes for the AI:** on B, remove `Two-Regime Zeros` from the record's `tags` through the store API and add an
   `**Assessment (AI, <date>):**` line with the zero shares above.

   **Consistency check (AI, 2026-11-08):** Keep `Two-Regime Zeros` on fremtpl2 when bemtpl97, the same target treated
   alike, carries none?

   * **Problem:**
     - The target is claims per year, scored by a Poisson deviance, and a Poisson model reproduces its zeros (96.2%
       expected against 96.3% observed), which the tag's definition excludes[^f10a].
     - bemtpl97 (same target and metric, treated alike since 2026-11-04) has no tag, and
       thailand_road_accident_register_2019_2022 lost its tag for the same reason; the mark has no note.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Keep it as a marker for the amount task | a CC line says the tag holds a place for the claim-amount task kept out for later | your mark stands | a tag for a task that does not ship |
     | b | Drop it, as bemtpl97 and thailand | the record's `tags` lose it | like cases alike | none found |
     | c | Tag bemtpl97 too | both tagged | the pair alike | against the tag's definition twice |

   * **Recommendation:** (b).
   * **Decision:** (a), (b) or (c)?

   **Lennart (2026-11-08, ok):** Reply (c): Tag bemtpl97 too; the tag should when the target has the kind of
   distribution indepdet of just the task as far as I understand

   **Resolved (2026-11-08, Lennart):** the tag stays on fremtpl2 and bemtpl97 gets it too: the tag describes the
   target's distribution (here 96.3% of the policies without a claim), not the task's model, and the tag's definition
   in records.md now says so.


   [^f10a]: records.md, `tags` (Andrej, 2026-10-30); thailand_road_accident_register_2019_2022.


   [^amount]: Andrej, 2026-10-20 (the amount design of PR #46); kept out by D12 of the exposure study of 2026-11-05 (CC
     of 2026-11-06 in the notes).
   [^tag-def]: The tag's definition (Andrej, 2026-10-30, `records.md`, `tags`): "If the low value is by far the most
     frequent one and independent of the remaining target distribution, then we can treat it as two regime zero,
     otherwise not".
   [^tag-cases]: thailand_road_accident_register_2019_2022 (2026-11-01): "a count model given the features predicts
     89.2% zeros against 89.0% observed, so the zero is the first step of the count, as for how_much_did_it_rain_ii".

12. **Ship the claims per year insured, as now, or the claim cost per year insured, and only one of the two?**

   * **Problem:**
     - You asked which of the two tasks on these policies is more representative of the real use case, to ship that one
       and not create the other[^f12-ask].
     - The insurer prices the claim cost per year insured, but builds that price from a model of the claims per year and
       one of the claim size, and the source's case study scores the claims per year[^f12-use].
     - On this table a score of the cost per year follows where a few claims land: the largest claim, 4.08M EUR, is 18
       to 19% of the claim amount of the test fold it falls in.
   * **Background:**
     - The amounts come from freMTPL2sev, summed per policy and divided by `Exposure`, each policy weighted by
       `Exposure`; the join is clean in the pinned release (26,444 claims on 24,944 policies, each count equal to its
       policy's claims with an amount, no amount on a policy without a claim).
     - The tail is real, not a data error[^f12-clean]: French motor liability covers bodily injury without a limit
       ([Code des assurances, R211-7](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006812124)), and the
       three largest claims (4.08M, 1.40M and 1.30M EUR) came from drivers aged 18 to 20.
     - Noll, Salzmann and Wüthrich, Lorentzen and Mayer, and Wüthrich and Merz model the claims per year with the
       Poisson deviance; the [scikit-learn Tweedie
       example](https://scikit-learn.org/stable/auto_examples/linear_model/plot_tweedie_regression_insurance_claims.html)
       models the cost per year (Tweedie at power 1.9, a Lorenz Gini weighted by exposure, each amount capped at 200,000
       EUR) and concludes that "the claim amount is very challenging to predict".
     - D12 of 2026-11-06 kept the amounts out for a later decision[^f12-d12].
   * **Effect on the task:** A keeps the rows, target, weight, metric and split as shipped; B changes the target and the
     metric, and the claim count leaves the frame; either way the other task is not created.
   * **Experiments:** the AI, on 9 random splits (the 3 shipped folds and two more partitions of the same rows), five
     honest models (two GLMs, three LightGBMs) fitted with the weight, `Exposure` never a feature:
     - claims per year, weighted Poisson deviance: the best LightGBM removes 2.26% of the constant rate's deviance (SD
       0.18%, 9 of 9) and the GLM 1.79%; a regularised LightGBM beats the GLM on 9 of 9 by 0.32% (split SD 0.03%,
       bootstrap SE within one test fold 0.08%); the five models keep their order across splits (Kendall's W 0.89, where
       1 is the same order on every split);
     - claim cost per year, weighted Gini: 0.23 to 0.27 for the five models, split SD 0.07 to 0.09; the GLM and the
       regularised LightGBM score 0.34 to 0.40 on the three test folds that hold the 4.08M claim and 0.13 to 0.27 on the
       other six; the GLM leads by +0.011 (7 of 9, bootstrap SE within a fold 0.021); W 0.43;
     - claim cost per year, weighted Tweedie deviance at power 1.5 (floor 0.1 EUR): the GLM removes 5.4% of the
       constant's (SD 4.4%, -0.3% to 11.5%; bootstrap SE within a fold 3.5%); W 0.78, mostly from two LightGBMs that
       chase the tail and lose to the constant on 3 and on 9 of the 9 splits;
     - the claim size: a gamma GLM of the mean claim gains 5.8% (SD 8.5%) over the mean claim as released and -0.8%
       (above 0 on 3 of 9) with the claims capped at 200,000 EUR; the frequency LightGBM times the mean claim ranks the
       cost per year better (Gini 0.29) than any model fitted on it (0.23 to 0.27);
     - with the claims capped at 200,000 EUR in the score alone, the cost's Gini still orders the models at W 0.40;
     - the portfolio cost per year of the 9 test folds runs from 140 to 194 EUR, their claims per year from 0.0730 to
       0.0745.
   * **Consistency:**
     - australian_vehicle_insurance_2004_2005 ships the cost per year with the weighted Gini, kept on 2026-11-08: its
       source scores no frequency, and there the frequency models tied while the Gini separated the GLM from boosting
       (+0.031, 8 of 9); here the measurements run the other way[^f12-d8].
     - bemtpl97 ships the claims per year, as A; its release holds the claim amounts too, with the same tail (the
       largest policy 1.99M EUR, 6.1% of all amounts, on a quarter of the rows), and its source builds the price from a
       frequency and a severity model, scoring each by its deviance and the price by a Gini[^f12-bem].
     - frempl_french_motor_personal_line and pricing_game_2016_french_fleet ship the cost per year: frempl's source
       defines no task, and pricing_game_2016's game priced the cost, whose material-damage charges stop at 13,992 EUR a
       period.
   * **Panel:** none; asked by Lennart on 2026-11-08.
   * **Unknown:** how tuned methods score the cost per year; the untuned models above are the evidence.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Claims per year insured (implemented) | `ClaimNb` / `Exposure`, weighted Poisson deviance, as shipped; the amounts are not created as a task | the source's metric; tells the models apart on 9 of 9 splits; the part of the price the rating factors set on this table | not the price itself; the claim size is left out |
     | B | Claim cost per year insured | `ClaimAmount` / `Exposure`, weighted Tweedie deviance at power 1.5 (floor 0.1 EUR) or the weighted Gini; the claim count leaves; the claims per year are not created | the quantity the insurer prices; as australian | one claim moves every model's Gini by about 0.15; the Gini orders the models by chance (W 0.43); a frequency model ranks it better than models fitted on it |

   * **Recommendation:** A, the claims per year: on this table the price varies with the rating factors through the
     claims per year, which the source scores and which tells the models apart on every split, while a score of the cost
     per year follows where a handful of claims land. On the use case alone the cost per year is the closer quantity; on
     the measurements it is not a close call. **Decision:** A or B?

   **Notes for the AI:** on A, nothing more: the notes' bullet "One task" and the CC of 2026-11-08 in the notes and the
   record say it; bemtpl97 stays as it is. On B: `_load_raw` sums `ClaimAmount` per `IDpol`; `_clean` builds
   `claim_cost_per_year` = `ClaimAmount` / `Exposure`, asserts that it times `Exposure` gives the amount back, and drops
   `ClaimNb` (MET-14, LEAK-10); `metric = Metric.from_context("mean_tweedie_deviance", params={"power": 1.5,
   "min_prediction": 0.1}, inputs={"weight": "Exposure"}, ...)` with a reason that names the power and the floor
   (MET-13: two orders below the cheapest rating cell of at least 500 policies, 55.7 EUR a year, rounded down to a power
   of ten), or `normalized_weighted_gini` if Lennart prefers australian's; `ScoringColumn.used_by` follows; rewrite
   `task_summary` (question, predicted, changes, fit_reason), the target-dominant acceptance, the notes' target, metric,
   "Counts of 5 to 16" and split bullets and `splits_comment` (the random split stays, its folds move with the new
   content order); `dataset check`, the task probe and probe 22 with both objectives (LEAK-41: the weight alone scores
   0.32 Gini on the cost per year, above every honest model, and `Exposure` as a feature adds +0.13); the CC line; the
   tag stays; then ask whether bemtpl97 follows.

   **Resolved (2026-11-08, Lennart):** A, as implemented: one task, the claims per year insured; the claim cost per year insured is not created (no duplicate).


   [^f12-ask]: Lennart, 2026-11-08, on D12: "fremtpl2's claim-amount task -> which task is more representative of the
     real use case? use that one and the other is not created as we dont want to have duplicates".
   [^f12-use]: **USE-5** (Must): predict what the actor would act on, at the resolution they act on it; **MET-1**
     (Must): the declared metric scores the decision of the use case; **MET-11** (Must): A's metric has origin
     `source` (the case study's Poisson deviance on its offset model), B's would be `context`.
   [^f12-clean]: **CLEAN-11** (Should): impossible values become missing, and values that are only unusual stay.
   [^f12-d12]: Lennart, 2026-11-06 (D12 of the exposure study): the claim amounts "stay out for now; a task on amounts
     per year insured or on the claim size is a separate decision, made on leak-free numbers"; the amount task was
     Andrej's proposal of 2026-10-20 (the aggregate claim amount per policy).
   [^f12-d8]: D8 of 2026-11-06 and australian_vehicle_insurance_2004_2005 issue 8, answered (a) on 2026-11-08 (Lennart);
     **MET-10** (Weigh): the resolution on our folds is a factor in the choice of metric.
   [^f12-bem]: Henckaerts, Côté, Antonio and Verbelen, [arXiv:1904.10890](https://arxiv.org/abs/1904.10890), Sec. 2:
     "P&C insurers usually opt for a so-called frequency-severity strategy to price a contract"; Sec. 5.1: loss ratio
     lift, double lift and the Gini index of Frees et al. (2013).

**Review panel:** ship after changes (mediator). Tier full, a re-review of 2026-11-06 under LEAK-41 and MET-14 to
MET-16, after option A of #51 (issue 6): 12 reports. Claims: 32 audited; 20 hold, 3 hold in part (`Exposure`'s share of
the gain, LEAK-41's reporting, the wording of the high counts), 3 refuted (the two accepted-warning reasons and the
"Copies kept" counts, stale since `Exposure` left the features), 2 stale record lines, 2 untested (the old-target split
numbers, now labelled; the book's quotes), and 2 re-measures the change note asked for (the record-count exploit, the
memorizer under the two splits); all in the definition are fixed. Blind review: include with changes; it read the blank
`BonusMalus` as a preparation defect (it is the blanking of issue 5) and asked for the weighted Poisson deviance, which
the task declares. Task gamer: one real exploit, `Exposure` read as a feature (+0.0072 to +0.0088 per fold, +0.0088 to
+0.0111 with the other records' summed exposure), which `feature_columns()` drops; a participant can read the test rows'
weight only from the scoring columns (X1). Agreed: ship with text changes only, made above (rows, target, weight,
metric, features and split unchanged). Disputed: the one profile that makes the gap to a split grouped on identical
rating factors, kept with a note (advocate, mediator) or grouped (critic); agreed after the rebuttals that it goes back
to you (issue 11); and how LEAK-41's 1/weight ceiling reads for a deviance (X2). One count of the reports is corrected
on a re-count: the profile is 19 rows with 72 claims over 3.63 years on the shipped as on the raw factors, falling 6/7/6
into the test folds; the 20 rows with 77 claims over 4.63 years in the split auditor's filter add the eighth high-count
policy, one row of another profile with no copy.

<details><summary>Mediator</summary>

**fremtpl2: mediator's report (exposure re-review 2026-11-06, full tier)**

The advocate and the critic agree on the verdict and on every change. One dispute is left: whether issue 7 goes back to you as a question or is closed by a note. By the rules it goes back to you, and I recommend option (a), keeping IID with a note. I ran one cheap experiment, to settle how LEAK-41's "score of 1/weight alone" reads for a deviance (numbers under "Agreed facts", item 8).

**1. Judgment record**

Verdict: ship after changes. All the changes are text; the data, target, weight, metric, features and split stay as defined.
Validity:
- SEL holds. USE-1 and USE-5 hold (fit approximate).
- MET-14 and MET-15 hold.
- LEAK-41 holds in its decision: Exposure is never an input, and no feature carries it above noise. Its reporting clause (Must) is not met yet; the notes fix it (change 1).
- LEAK-10 holds: BonusMalus is blanked in blocks 0-4 (issue 5, "likely", EV-6).
- LEAK-9: the protocol line covers the renewal and record-structure signal (issue 8).
- SPLIT-8 holds: IID, ForcedIIDFromTemporal.
- SPLIT-29 is not triggered: 20 rows of 677,991 are not "many".
- SPLIT-30: the 20-row profile is a hidden-group hit, so it is a question. Issue 7 is re-opened with that fact.
Value:
- TP-1: the no_signal flag was checked against the declared metric. Poisson LightGBM beats the constant on every fold by 0.0096 to 0.0127 (D² about 2.3%, A/E 1.00, Gini 0.195). The flag comes from an R²-type skill.
- TP-2: a small real signal, keep.
- MET-11: the source's metric. MET-13: the 1e-4 floor holds.
Quality: CLEAN-11 and CLEAN-10 hold as settled. Stale or unlabelled numbers and two stale accepted-warning reasons are to be restated (EV-7).
Weighed: issue 7, note against grouping. No other weighing is new.
For the curator:
- issue 7 re-opened, a weighing call;
- two items shared with bemtpl97: the test-row weight a participant can read, and how LEAK-41's "1/weight alone" reads for a deviance;
- the "Two-Regime Zeros" tag (minor).

**2. Changes to make now (no decision needed)**

All are in the definition's notes or fields, REVIEW.md, the record, or a Cases row. Numbers are on the declared scale unless marked.

1. LEAK-41 reporting clause (Must). Add one sentence to the Exposure bullet:
   - Exposure as a feature gains +0.0082 with the weighted Poisson fit (per fold 0.0086 / 0.0087 / 0.0073) and +0.0075 with L2 (full data). Probe 22 (50k cap) gives +0.0048 and +0.0067. Decide on the worse; the column is out either way.
   - The ceiling: a rate model on Exposure alone scores 0.47114 against the constant's 0.47929 (claim auditor). Raw 1/Exposure is no ceiling under a deviance (item 8).
   - The rating factors predict Exposure at R² 0.17. No feature's gain runs through it above 2 SD. Region and DrivAge are highest (1.1-1.4 SD), are known at the quote, and stay (USE-6).
   - Replace "21-30% of LightGBM's gain" with 43% on the declared scale, or drop the share.
   - The same sentence goes into bemtpl97 (precedent checker C1).
2. The two accepted-warning reasons (EV-7; the reading under LEAK-17). The acceptances stay; only the stated facts change.
   - dataset_conflicting_duplicate_rows: 8,128 rows (1.2%), not 520; 7,971 of them differ in claim count.
   - dataset_duplicate_rows: 181,197 exact copies (26.7%). 327,862 rows sit in 138,537 feature-identical groups, and 92.9% of those groups sum to at most 1.01 years. So most groups look like one policy-year split into records, not distinct policies.
   - The measured harm, all at or below the noise of about 0.0006 per fold: twin memorizer +0.0001; group size and siblings' exposure without the row's own Exposure, 0.0004; transductive record count +0.0005. The one exception is the profile of issue 7.
3. "Counts of 5 to 16" bullet (EV-7). Correct the wording:
   - The seven policies have 66 claims over 1.38 years.
   - "72 claims over 3.63 years" belongs to the 19 rows of the profile on the raw factors. On the shipped factors (BonusMalus blank) the profile is 20 rows, 77 claims and 4.63 years.
   - "0.0012 of 0.2534" is the count scale; on the declared scale it is 0.0023 of 0.4793.
   - Add the fleet sentence here and in splits_comment. Under IID the profile's rows fall 6/7/7 across the folds, and LightGBM predicts 3.8-17.2 claims a year for them from their training copies (0.073-0.078 when grouped). It makes 94-102% of the IID-vs-grouped gap (+0.0008 to +0.0017). Without it the gap is -0.0002 to +0.00015.
   - Both sides call this sentence required whatever you decide on issue 7.
4. Restate the split and renewal numbers on the declared scale, and add one dating clause ("numbers before 2026-11-06 are on the count target with Exposure a feature; the declared score is 1.891 times the count deviance") (EV-7).
   - Forced-temporal cost: +0.0009 (SE 0.00035), +0.00046 without the profile.
   - Renewal channel: label-free flags about 0.0010; full oracle 0.0015-0.0025 (upper bounds, they read IDpol).
   - Record-count exploit: +0.0005 (it was +0.00071 on the count target with Exposure a feature).
   - "Copies kept": 327,862 rows in feature-identical groups and 181,197 exact copies. The old counts included Exposure as a column.
   - Label 0.0821/0.0819, 0.23316/0.23267 and 0.2327/0.2435 as old-target numbers.
5. Exposure ScoringColumn description (LEAK-41, wording). Add that in blocks 5-6 the records are mostly cut at a calendar date: block 6 never exceeds 0.74 of a year, and 99.8% of block 5 is a partial year.
6. Metric definition and notes (MET-11). Add "for predictions above the floor" to the identity with the source's count deviance (precedent checker B3).
7. TP call in REVIEW.md and fit_reason (TP-1, TP-2):
   - give the per-fold deviance skill, D², A/E and Gini;
   - say the no_signal flag comes from R², and a Poisson count has R² near 0.01 by nature;
   - fold resolution is about 0.0006, so strong methods differ in the fourth decimal;
   - the honest skill fell from about 0.064 to 0.023 because of the BonusMalus blanking (issue 5), not option A;
   - re-check against tuned methods when they exist.
8. Weight requirement (MET-15), in fit_reason or the task text. The task needs sample_weight: an unweighted LightGBM scores 0.50043 against the constant's 0.47980 (fold 0, A/E 0.64). Results should record whether a method used the weight.
9. BonusMalus wording (EV-6, settles the critic's rebuttal point 3).
   - Keep "likely". Do not present the gamer's +0.040 as the size of the leak: it is a partial restore over blocks 0-4 and mixes the leak with any real quote-time signal.
   - Both outside reviewers read the blanking as a preparation defect. Keep it prominent in task_summary.known as well as in changes.
10. Records:
   - REVIEW.md Outcome header: it still describes the count target.
   - The record gets a 2026-11-06 Assessment line: 9 features, Exposure the weight, issues 5, 6, 8 and 9 resolved, issue 7 re-opened.
   - SPLIT-8 Cases row for fremtpl2 (splits.md line 257): rewrite to the 2026-11-05 reason (precedent checker prompt 1, option a). Drop the gap-size reason, which SPLIT-4 and SPLIT-30 bar. Label +0.00049 as the forward-by-block hold-out on the old target, not the grouping cost.

**3. Issues for the curator, ranked**

1. Issue 7 re-opened: keep IID with a note, or group on identical rating factors? (P4; SPLIT-30 Must, with SPLIT-29, LEAK-17 and SPLIT-24.)
   - Problem: one rating profile is the entire IID-vs-grouped gap. It has 20 rows, 77 claims and 4.63 years, a rate of 16.6 claims a year against the portfolio's 0.07. Wüthrich and Merz suspect one driver or a rental fleet. It is the only memorization a random split rewards.
   - Effect: +0.0008 to +0.0017 on LightGBM, 7-15% of its skill over the constant. The GLM gap is 0.0001. The LightGBM-over-GLM ranking is the same under every split. An explicit memorizer gains nothing (best blend 0.46823 against 0.46813).
   - The dispute, settled by the rules:
     - Both sides now agree SPLIT-30 makes the hit a question, so it goes to you and is not closed by a note.
     - The critic's first claim, that the fact refutes the issue-7 resolution, does not hold. You resolved issue 7 on prior work, and the 2026-11-05 survey already listed the strand that groups on identical factors. The 0.017 correlation was about the inferred chains, not this profile.
     - The new fact is the measured content of that grouping: one profile.
   - Advocate's best evidence, for (a):
     - SPLIT-29 needs "many rows", and 20 of 677,991 are not many.
     - The ranking is unchanged, and the gap size never decides (SPLIT-4, SPLIT-30).
     - On this table the shipped 9-factor key is the whole feature vector. SPLIT-24 bars "a hash of the feature vector standing in for an unknown entity" (maternal_health_risk).
     - New quotes keep their rating profile (splits.md "Composite keys": when new rows keep the key, it is a feature).
   - Critic's best evidence, for (b):
     - Schelldorfer (2021) and Lorentzen and Mayer group on exactly this key, against this optimism.
     - 92.9% of feature-identical groups sum to at most a year, so the key mostly marks one policy-year: an entity by SPLIT-24's "identical values in the columns that define the entity".
     - It costs nothing elsewhere: 488,666 groups, folds of 224,778 to 226,838 rows.
   - Options:

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Keep IID, fleet note (change 3) | the score's dependence on 20 rows is stated | follows your 2026-11-05 call; SPLIT-29 not met | a known 0.001 optimism stays |
     | b | Group on identical shipped factors | ForcedGroupedFromTemporal, GroupKFold | the literature's key; removes the only memorization | a ruling that the profile is the entity (SPLIT-24); bemtpl97 to check alike |
     | c | Drop the 20 rows | a filter | removes it | undoes the 2026-11-04 keep; not recommended by anyone |

   - Recommendation: (a).
   - What would settle it: your ruling on whether identical rating factors "define the entity" for freMTPL2 (SPLIT-24), or a source statement that the profile is one contract.
2. Cross-dataset, shared with bemtpl97: the test-row weight is readable from the scoring columns. (P4; LEAK-41 Must "never a model input", LEAK-9 Should.)
   - Problem: the participant kit hands out Exposure for test rows in scoring.parquet, because the metric needs it. A participant who uses it as a feature gains +0.0084 / 0.0088 / 0.0072 per fold (gamer). Adding the siblings' summed Exposure brings it to 0.0088-0.0111.
   - Advocate and column auditor: this is the scoring-column contract of every weighted task, not a defect of this definition.
   - Critic: agrees it needs no change to the definition.
   - Needed now for fremtpl2: only change 1, which states the size.
   - Decision, across datasets:
     - (a) a LEAK-9 protocol line for every weighted task: a method that reads a scoring column as input is called out and not benchmarked, as with the renewal line;
     - (b) the harness withholds scoring columns from the predict call and the scorer reads them afterwards (code and API);
     - (c) both.
   - My lean is (c): the rule is a Must, and (a) alone relies on spotting it.
3. Cross-dataset, shared with bemtpl97: how LEAK-41's "score of 1/weight alone" reads for a deviance. (P4; LEAK-41 text against probe 22's text.)
   - Facts: the rule text has no Gini limit; probe 22 scores 1/weight "for a Gini metric". My run on the shipped folds:

     | Prediction | Score per fold | Against the constant (0.4774-0.4807) |
     |---|---|---|
     | 1/Exposure | 3.636 to 3.657 | far worse |
     | k/Exposure, k fit on train | 0.4904 to 0.4915 | worse |
     | rate per Exposure band (20 bands), fit on train | 0.4708 to 0.4724 | better |
     | rate model on Exposure alone (claim auditor) | 0.47114 | better |

     Under a level-sensitive metric, raw 1/weight scores worse than the constant, so it cannot serve as a ceiling. The meaningful ceiling is a rate fit on the weight alone.
   - Precedent checker: Gini only. Advocate and critic: the rule's text governs; rules win over a reading.
   - Needed now: change 1 reports the rate fit on the weight alone, which meets either reading.
   - Decision: amend LEAK-41 and probe 22 to read "for a ranking metric (Gini), 1/weight alone; for a level-sensitive metric, a model of the target on the weight alone", or keep the text. The amendment is recommended; bemtpl97 follows either way.
4. Tag "Two-Regime Zeros" (record; quality). It came from Andrej's amount task, which D12 keeps out. Your definition (policy question 4: a low value that dominates and is separate) may or may not fit a Poisson rate with 96.3% zeros. Keep or drop?

**4. Agreed facts**

1. Target, weight and metric:
   - The target is ClaimNb/Exposure (0 to 365, 96.32% zero). ClaimNb is out, and _clean checks that the count rebuilds.
   - The features are the 9 rating factors. sample_weight is Exposure, and so is the metric's weight.
2. The scorer equals the source's offset count deviance times n/sum(Exposure), to 1e-15. The factors are 1.8956, 1.8919 and 1.8864 per fold (1.891 overall), so models rank as by the source's metric (MET-11).
3. The floor never binds for LightGBM (0.0%). An all-zero prediction scores a finite 1.30.
4. The weight is required: unweighted fits lose to the weighted constant (0.49792 to 0.50043 against 0.47929 to 0.47980; A/E 0.64).
5. Honest skill:
   - Poisson LightGBM beats the constant on every fold by 0.0096 to 0.0127 (D² about 2.3%, A/E 1.00, Gini 0.195).
   - A random-column control moves fold scores by up to about 0.0006.
   - The task probe's no_signal flag reads R².
6. Exposure as a feature: +0.0082 Poisson and +0.0075 L2 (full data); +0.0048 and +0.0067 in probe 22. On the count scale this is 0.0043, so the notes' 0.0039-0.0045 holds in absolute size, but its share is 43%, not 21-30%.
7. Probe 22: the rating factors predict Exposure at R² 0.17. No feature passes 2 SD; Region and DrivAge are at 1.1-1.4 SD, and both are known at the quote.
8. The weight-alone readings: Exposure alone scores 0.47114 against the constant's 0.47929. Raw 1/Exposure scores about 3.65, and k/Exposure about 0.490 (my run).
9. The profile:
   - 20 rows on the shipped key, 77 claims, 4.63 years. On the raw factors it is 19 rows, 72 claims, 3.63 years; the seven policies with 5-16 claims have 66 claims over 1.38 years.
   - It makes 94-102% of the IID-vs-grouped gap. Without it the gap is -0.0002 to +0.00015.
10. Twin memorizer +0.0001. Record-count exploit +0.0005 (below noise). Forced-temporal cost +0.0009 (+0.00046 without the profile). Renewal flags about 0.0010; full oracle 0.0015-0.0025.
11. Duplicates: 8,128 conflicting rows; 181,197 exact copies; 327,862 rows in 138,537 feature-identical groups, 92.9% of which sum to at most 1.01 years.
12. Exposure timing:
   - a claim lowers the chance of a next-year record in every partial-year band;
   - blocks 5-6 are cut mostly at a date (block 6 at most 0.74 of a year);
   - no row is selected by its weight.
13. Settled points:
   - BonusMalus blanking (issue 5) is settled and not reopened. The restore gain of 0.040 mixes the leak with any real quote-time signal.
   - Not capping is settled (CLEAN-11): capping in training hurts (0.46909 against 0.46850).
   - The default codes are settled (CLEAN-10).
14. Stale record lines: the 2026-11-04 Assessment ("realised exposure kept, 10 features, three Must issues open") and REVIEW.md's Outcome header.

The task gamer's exploits, mapped to rules and notes. The definition has no "Potential leak, kept on purpose:" bullet; the relevant notes are the Exposure bullet and the issue-8 CC (LEAK-9).

| # | Exploit | Rule | Note it maps to | New or known | Gain against the note |
|---|---|---|---|---|---|
| 1 | Exposure plus group size plus siblings' summed Exposure, +0.0088 to 0.0111 | LEAK-41 (the weight, and "a sum of a group's exposures"); LEAK-9 (reads test rows) | Exposure bullet; issue-8 CC | known | without the row's own Exposure, 0.0004 (noise); the rest is exploit 2 |
| 2, 2b | Exposure, or a full-year flag, as a feature, +0.0072 to 0.0088 | LEAK-41 | Exposure bullet | known | differs from the note only in scale and share (change 1); needs the test-row weight (curator item 2) |
| 3 | Transductive group size over train and test, +0.0005 | LEAK-9 | issue 8 / issue-8 CC | known | 0.00071 before; now below noise; the note gives no number (change 4) |
| F1 | BonusMalus restored from the source, +0.040 | LEAK-10 | issue 5 CC | known, settled | not an exploit (change 9) |
| - | Looking rows up in the published source recovers the labels | none in this definition | none | known for any public dataset | not counted |

Nothing new.

**5. Consistency with precedent**

- The precedent checker finds the definition consistent with bemtpl97 and the four insurance tables decided on 2026-11-06.
  - The three reversals (Andrej, 2026-10-20; the AI line of 2026-10-29; the 1e-6 floor) each carry a stated fact or an amendment.
  - There is no drift and no third exception. register.json has no flag on fremtpl2 or bemtpl97.
- Reflection prompt 1 (SPLIT-8 Cases row): adopted as option (a), in change 10, with the critic's addition that the gap-size reason goes.
- Issue 7, option (a) follows your 2026-11-05 call and bemtpl97 (IID, "treated alike", 2026-11-04). Option (b) would depart from:
  - maternal_health_risk (a feature-vector hash barred under SPLIT-24), unless you rule that the rating profile is the entity;
  - bemtpl97, unless you check it for the same structure.
  If you choose (b), the check to answer is:

  > **Consistency check (AI, 2026-11-06):** grouping fremtpl2 on identical rating factors departs from maternal_health_risk (a feature-vector key barred, SPLIT-24) and from bemtpl97 (IID). What sets it apart?
  > (a) the literature's key, and 92.9% of the groups sum to at most a policy-year, so the profile defines the entity here, recorded as the SPLIT-24 fact;
  > (b) keep IID as bemtpl97;
  > (c) reopen bemtpl97 to group alike;
  > (d) amend SPLIT-24 for rating profiles.
- C1, the LEAK-41 reporting gap, is shared with bemtpl97: same fix (change 1), same cross-dataset item (issue 3).
- Side notes from the precedent checker, outside this definition:
  - australian_vehicle_insurance_2004_2005/dataset.py (lines 127 and 279) cites Andrej's fremtpl2 call for amounts that fremtpl2 no longer ships (D12): check the wording there.
  - Tell Andrej that three of his exposure calls are now superseded.
- Minor, untouched: the claim auditor's unweighted count-scale fit gives 0.2633, not the 0.26187 that MET-15's Cases row quotes. The direction is the same; no change.

</details>

<details><summary>Claim audit</summary>

**fremtpl2 -- claim auditor, exposure re-review (2026-11-06, tier full)**

Verdict: today's change holds. The target, the weight, the metric identity, the source reference, the floor and
LEAK-41's decision itself all survive their tests. Nothing that breaks validity was refuted. What fails is text that
today's change made stale: the two accepted duplicate warnings, the "Copies kept" counts, the Exposure leak's share,
and a set of numbers measured on the count scale or the old target that the notes now give without a label. LEAK-41's
reporting duty is only partly met: the L2 gain and the Exposure-alone ceiling are missing. The re-measures the change
note asked for are done below (IID against grouped on identical factors, the record-count exploit, a twin memorizer).

Setup: the definition loaded with load_definition; shipped folds (1 x 3, 451,994 / 225,997); scorer from
data_foundry.v2.metrics. LightGBM 4.7 Poisson (400 trees, lr 0.05, 31 leaves, min_child_samples 200), fitted with
sample_weight = Exposure unless stated otherwise.
Scales: the declared metric = count deviance x n/sum(Exposure) (1.891 overall). The constant portfolio rate scores
0.47929 on the declared scale, which is 0.25342 on the count scale.

**Claims (claim, source, test, result, evidence, rule)**

**Today's change**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | Target claim_frequency = ClaimNb/Exposure, the count rebuilds, ClaimNb leaves the frame | notes "Target", _clean, task_summary.changes | load the container: columns, the code's assert, target range | HOLDS | 11 columns, no ClaimNb, no IDpol; _clean's allclose assert passes; target 0 to 365 (1 claim in 1/365 year); 96.32% zeros ("96.3% have none" holds) | MET-14 |
| 2 | Exposure no feature; it is the weight scoring column, the metric's weight and the sample_weight | notes, scoring_columns, sample_weight, task_summary.known | feature_columns(c), sample_weight(c), spec.inputs | HOLDS | features = the 9 rating factors; sample_weight(c) = "Exposure"; spec inputs {"weight": "Exposure"}; the declared sample weight is the metric's row weight | MET-15, LEAK-41, MET-2 |
| 3 | The weighted rate deviance = the count deviance with an offset x n/sum(Exposure), 1.886-1.896 per fold, 1.891 overall | notes "Metric", metric.definition, CHANGES | constant prediction on each fold: scorer vs hand-coded weighted deviance vs count deviance of Exposure*mu | HOLDS (exact) | folds: scorer 0.479803 / 0.480681 / 0.477393 = hand = count x ratio to 1e-15; ratios 1.8956, 1.8919, 1.8864; overall 1.8913. Algebra: `d_count(N, v*mu) = v*d_rate(N/v, mu)`, so the per-fold ranking is the source's | MET-11 (source) |
| 4 | The source compares models by this count deviance with an exposure offset, 100 x the mean | metric.original, reference (FreMTPL_1b load data.r#L35) | read the pinned R files | HOLDS | L35: Poisson.Deviance <- 200*(sum(pred)-sum(obs)+sum(log((obs/pred)^obs)))/n; "FreMTPL2 Part 1" L76-88: glm(ClaimNb ~ ..., offset=log(Exposure), family=poisson()), then 100*Poisson.Deviance(test$fitGLM, test$ClaimNb) in and out of sample. The source's data caps ClaimNb at 4 and Exposure at 1 (L30-31); ours does not (settled, CLEAN-11) | MET-1, MET-3, MET-11 |
| 5 | Floor 1e-4 claims per year, two orders below the smallest plausible rate | notes "Metric", params | out-of-fold predictions of a Poisson LightGBM and an L2 LightGBM; zero prediction on every fold | HOLDS | Poisson LightGBM: min 0.0104, 0.1% quantile 0.0208, 0% at the floor; L2: 0.055% at the floor (1.4% with Exposure as a feature); all-zero prediction scores 1.30 (finite) on every fold; task probe reports the floor share (RF 0.5%) | MET-13 |
| 6 | "with the weight, dividing does not inflate short records" / an unweighted fit targets another quantity (MET-15's fremtpl2 numbers: 0.1186 vs 0.0738, worse than the constant) | notes Exposure CC, README training-weight block, MET-15 | unweighted vs weighted Poisson LightGBM; the two constants | HOLDS | unweighted mean rate 0.11863 vs weighted 0.07377 (x1.61); unweighted LightGBM 0.49792 and the unweighted constant 0.49892, both worse than the weighted constant 0.47929; weighted LightGBM 0.46822. (MET-15's 0.26187 is not reproduced exactly: my unweighted fit is 0.2633 on the count scale. Same direction) | MET-15 |
| 7 | Exposure is cut short by claims ("a claim can cut it short") | task_summary.known, ScoringColumn description | P(next-year row) by exposure band and claim, blocks 0/2/4/5, next_year_rows | HOLDS | in each partial band a claim lowers continuation: <=0.25: 0.169 vs 0.263; 0.25-0.5: 0.255 vs 0.324; 0.5-0.75: 0.370 vs 0.444; 0.75-0.99: 0.406 vs 0.469; full year: 0.663 vs 0.629 (not cut) | LEAK-41, LEAK-10 |
| 8 | Exposure as a free feature was worth 0.0039-0.0045 beyond the offset, "21-30% of LightGBM's gain" after the blanking | notes Exposure bullet | Poisson LightGBM on the shipped folds, 9 features vs 9 + Exposure | ABSOLUTE SIZE HOLDS, SHARE REFUTED | +0.00819 on the declared scale (per fold 0.0086 / 0.0087 / 0.0073) = 0.0043 on the count scale, inside 0.0039-0.0045. Against the constant-rate baseline the model with Exposure gains 0.01926 and Exposure is 43% of it, not 21-30%; it is 74% of the honest model's gain over the constant (0.0111) | LEAK-41, EV-7 |
| 9 | LEAK-41 reporting: the gain with an L2 fit and with the weighted actuarial fit, decided on the worse, and the score of 1/weight alone as the ceiling | LEAK-41 (Must) requires it of the definition | full-data fits; Exposure alone | PARTLY MET (missing numbers) | notes give only the count-scale offset gain (0.0039-0.0045). Measured: Poisson +0.0082, L2 +0.0075 (0.47112 -> 0.46363); the worse is the Poisson one. Exposure alone scores 0.47114 against 0.47929 for the constant: a leak through Exposure would reach 0.0082, 74% of what the 9 honest features reach (0.46822). Probe 22 (50k cap): +0.0048 Poisson, +0.0067 L2; features predict Exposure at R^2 0.17, no feature's gain runs through it above noise. Neither probe 22's numbers nor the ceiling are in the notes | LEAK-41 |
| 10 | Poisson GLM gives log(Exposure) a free coefficient of 0.641 | notes Exposure bullet | sklearn PoissonRegressor with Noll et al.'s binning plus log(Exposure) as a covariate, all rows | HOLDS in substance | 0.626 with the raw BonusMalus, 0.568 with the blanked one (+ missing indicator); the design decides the third digit. Well below 1 either way | EV-1 |
| 11 | Re-measure of the record-count exploit (gamer's +0.00071 before) | CHANGES "still to re-measure" | add n = number of rows with the identical feature vector in the full frame (train + test) | MEASURED (smaller) | +0.00051 on the declared scale (per fold 0.00070 / 0.00062 / 0.00022), = 0.00027 count scale; adding the train twins' summed exposure and count adds nothing (0.46805). Under the grouped split +0.00035 | LEAK-9 (issue 8, settled) |
| 12 | Re-measure of a memorizer, IID vs a split grouped on identical rating factors (issues 7, 8 settled on the count target) | CHANGES | (a) GroupKFold on the feature-vector hash vs the shipped folds; 3 more random seeds of each; (b) LightGBM given the train-side twins' claims and exposure (leave-one-out) | (a) GAP FROM THE FLEET ONLY; (b) NO GAIN | (a) grouped is worse by 0.00167 (shipped folds), 0.00070 / 0.00127 / 0.00078 (seeds 1-3). 94% of the gap sits in the 8 rows with 5-16 claims; without them grouped - IID = -0.00005 / -0.00010 / -0.00021. (b) +0.00010 / +0.00041 / -0.00010 per fold, noise. So the random split rewards learning the 5-16-claim fleet from its sibling rows (6-15% of LightGBM's gain over the constant) and nothing else | SPLIT-8, LEAK-17, CLEAN-11 |

**Task summary and splits**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 13 | 677,991 records; BonusMalus "in 12% of the records", "blank in 88%" | task_summary.row, known, fit_reason | count | HOLDS | 79,993 kept (11.8%), 597,998 blank (88.2%) | - |
| 14 | The signal is real (implied by shipping; the task probe flags no_signal, TP-1/TP-2) | probes/task.txt | weighted Poisson LightGBM vs the train-side constant rate, every fold | SIGNAL HOLDS; the probe flag is an artefact of its L2/R^2 models | gains 0.0109 / 0.0127 / 0.0096 per fold (D^2 about 2.3%); L2 LightGBM gains only 0.008 and the probe's skill is R^2. REVIEW.md should say why the flag is overruled | TP-1, TP-2 |
| 15 | Random 3-fold CV, train 451,994 / test 225,997, each row a distinct IDpol | splits_comment | splits; raw IDpol | HOLDS | 3 folds of 451,994 / 225,997, disjoint; IDpol unique. "after the base class's content ordering and shuffle with seed 42": untested | SPLIT-1 |
| 16 | "for 16% of test rows the next-year row is on the training side; the shipped columns single it out for 55% of linked rows" | notes "Copies kept" | next_year_rows; for each linked earlier row, count rows matching the fixed factors, DrivAge+1, VehAge +0/1 (no IDpol, no Exposure) | HOLDS after the change | 161,883 pairs = 23.9% of rows, x2/3 = 15.9%; exactly one candidate for 54.6% | LEAK-9 |

**Accepted warnings**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 17 | dataset_conflicting_duplicate_rows: "520 rows (390 before BonusMalus was blanked) share every factor with another policy but differ in claim count" | accepted_check_warnings | the bundle check's own logic (bundle_checks.py ~L622) on the shipped frame | REFUTED (number stale) | with Exposure now a scoring column the check sees 8,128 conflicting rows (1.2%); 7,971 of them differ in the claim count. 520 is what the old frame (Exposure a feature) gives | P6, EV-7 |
| 18 | dataset_duplicate_rows: "Each copy is a distinct policy (own IDpol) ... the repetition is the portfolio" | accepted_check_warnings | same check; exposure sums of the feature-identical groups | REFUTED in substance (numbers absent) | the check now counts 181,197 exact duplicate rows (26.7%); 327,862 rows (48.4%) sit in 138,537 groups with identical features; 92.9% of those groups (298,355 rows) sum to <= 1.01 years, the signature of one policy-year split into records (the notes' own "renewals during the year recorded as two records"; Andrej's 94%). Each has its own IDpol, but most copies do not look like distinct policies. Measured harm is small (item 12) | P6, LEAK-17 |
| 19 | task_target_value_dominant: "96% of the policies have no claim" | accepted_check_warnings | count | HOLDS | 96.32% | - |

**Curation notes, other bullets**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 20 | 26,444 claims; counts 0-16; each count equals the claims table | notes intro, "Target" | raw counts | HOLDS | 26,444; 0-16; _clean's assert passes | PROV-13 |
| 21 | first 9,387 policies (IDpol <= 24,951), 293 claims now; their next-year rows claim at 0.048 vs 0.076 | notes "Target" | raw + next_year_rows | HOLDS | 9,387; 293; 0.04799 vs 0.07586. "(9,942) before": untested (needs the OpenML copy) | - |
| 22 | 8 policies with 5-16 claims; "seven of the eight policies are one profile ...: 72 claims over 3.63 years"; "the 19 rows carry 0.0012 of the mean deviance 0.2534" | notes "Counts of 5 to 16" | raw | HOLDS IN PART (wording) | 8 policies; the seven of the profile have 66 claims over 1.38 years. 72 claims over 3.63 years are the 19 rows of the profile (DrivAge 52/53, VehAge 12/13). 0.0012 / 0.2534 is the count scale; on the declared scale it is 0.0023 of 0.4793 | P6, EV-7 |
| 23 | Exposure above one year: 1,224 rows, up to 2.01, blocks 1 and 2; 961 in IDpol 1,179,653-1,199,005; median 1.04 | notes | raw | HOLDS | 1,224 (961 in block 1, all in that range; 263 in block 2); max 2.01; median 1.04. "capping would raise their rate by 11%": untested | CLEAN-11 |
| 24 | Dtypes: VehAge 99/100 = 48 rows, no car 86-98; DrivAge 99 = 70 rows vs 5 at 98, 66 in block 0 after 1 at 96 and none at 97-98; 22 regions; Area bands of Density | notes "Dtypes", CC 2026-11-05 | raw | HOLDS | 48; 0 cars aged 86-98 (max 85); 70 / 5 / 3 at 100; 66; 1 / 0 / 0; 22; Area density ranges A 1-50, B 50-100, C 100-500, D 500-1,993, E 2,001-9,850, F 10,008-27,000 (they touch at 50 only) | CLEAN-10 |
| 25 | "Copies kept: 28,768 rows copy an earlier row (40,903 in groups; 30,987 and 43,947 after the blanking)" | notes "Copies kept" | duplicates on the model's inputs of today's frame | REFUTED (stale) | those counts include Exposure as a column. On the shipped inputs: 327,862 rows in feature-identical groups, 181,197 exact copies with the target; leak probe: 36.4% of test rows have an exact feature copy in train | P6, EV-7 |
| 26 | "grouping on them moves LightGBM skill from 0.0821 to 0.0819"; split-test +0.00049; BonusMalus 0.2327 -> 0.2435; renewal oracle 0.0021 / 0.0008 | notes "Copies kept", "Split forced IID", CC 2026-11-05 | - | UNTESTED under the new target (measured with Exposure a feature on the count target; the notes do not say so) | chain-grouped and block-temporal splits not rebuilt here; the identical-factor grouping of item 12 is the nearest new number | EV-7 |
| 27 | Year 2014: tables entered CASdatasets on 14 October 2014 | notes "Year", record | pkg/inst/NEWS at CASdatasets 324c15c999 | HOLDS | "freMTPL2sev.rda 14/10/2014", "freMTPL2freq.rda 14/10/2014" | PROV-9 |
| 28 | Help-page quotes "observed mostly on one year", "approximately 2011-2013" | notes "Prediction point", task_summary.row | the CASdatasets page | HOLDS | both on the freMTPL page | PROV |
| 29 | Wüthrich and Merz (2023) Sec. 13.1 / 5.2.4 quotes, "renewals recorded as two records"; "at the quote the free model was never better, actual 1.29 x price" | notes | - | UNTESTED (the book is not open access; the quote-scenario run was not redone) | - | - |

**Record**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 30 | Screening 2026-10-22: the case study caps ClaimNb and truncates Exposure (check); compares models by out-of-sample Poisson deviance with Exposure | record | R files | HOLDS | L30-31 pmin(ClaimNb,4), pmin(Exposure,1); Part 1 L87-88 | MET-1 |
| 31 | Screening "fit direct ... ClaimNb with Exposure"; Assessment 2026-10-29 "Exposure as a predictor"; Andrej 2026-10-20 "a feature, not a divisor, capped at 1" | record | - | SUPERSEDED, and marked so by CC 2026-11-06 | - | - |
| 32 | Assessment 2026-11-04 (priority 3): "realised exposure kept", "10 mixed features", "three Must issues open"; tag "Two-Regime Zeros" | record | compare with the definition | STALE | 9 features now; Exposure no feature; issues 5-9 resolved. No newer priority line; the tag comes from Andrej's amount task (D12: the amounts stay out) | - |

**REFUTED AND UNTESTED, RANKED (validity first, Must first)**

No validity refutation. Today's design (rate target, Exposure as the weight only, the offset-equivalent deviance, floor
1e-4) holds on every test.

1. LEAK-41 reporting partly met (Must; item 9). The notes give only the count-scale offset gain. Missing: the L2 gain
   (+0.0075), the actuarial gain on the declared scale (+0.0082, the worse of the two) and the Exposure-alone ceiling
   (0.47114 against the constant's 0.47929, 74% of what the honest features reach). What it changes: a reader cannot
   see how large the removed leak was on the metric that ships. Mildest remedy: one sentence in the Exposure bullet
   with these numbers and probe 22's (R^2 0.17; no feature's gain runs through Exposure above noise).
2. Accepted warnings stale (items 17, 18). The conflicting-duplicate reason says 520 rows; the check now counts 8,128
   (1.2%). The duplicate reason says each copy is a distinct policy; the check now counts 181,197 exact copies
   (26.7%), and 92.9% of the feature-identical groups sum to at most a year, which looks like one policy-year split
   into records. What it changes: the acceptance justifies other numbers than the check reports. Measured harm is
   small: a twin memorizer gains nothing (+0.0001), and grouping costs nothing outside the fleet. Mildest remedy:
   rewrite both reasons with today's counts and the split-records reading, and cite item 12's numbers.
3. "Copies kept" counts stale (item 25), and the split numbers measured on the old target are not labelled
   (item 26). New measures for the paragraph: grouping on identical rating factors costs 0.0007-0.0017 (4 runs),
   94% of it from the 8 rows with 5-16 claims (without them -0.0000 to -0.0002); the record-count exploit is +0.0005
   (0.0002-0.0007 per fold). What it changes: the random split rewards learning the fleet from its sibling rows, 6-15%
   of LightGBM's gain over the constant (SPLIT-8, CLEAN-11 tension). The IID decision itself is untouched. Mildest
   remedy: replace the counts and add the fleet sentence next to "Counts of 5 to 16".
4. Exposure's share "21-30% of LightGBM's gain" (item 8). On the shipped baseline it is 43% (0.0082 of 0.0193); the
   absolute 0.0039-0.0045 holds on the count scale. Mildest remedy: give the share on the declared metric, or drop it.
5. Mixed scales (items 22, 26, and 0.2534 / 0.0012 / 0.0021 / 0.23316 / 0.2327 / 0.0008). These are count-scale or
   old-target numbers, while the declared metric is 1.891 times the count scale. Mildest remedy: one clause, "numbers
   before 2026-11-06 are on the count target with Exposure as a feature; the declared score is 1.891 x the count
   deviance".
6. "Seven policies ... 72 claims over 3.63 years" (item 22). The seven have 66 claims over 1.38 years; 72 claims over
   3.63 years are the 19 profile rows. Mildest remedy: reword.
7. Task probe flag no_signal (item 14). It is overruled by the declared metric: a weighted Poisson LightGBM beats the
   constant on every fold by 0.0096-0.0127. REVIEW.md should record why (the probe's L2/R^2 models), not leave the flag
   unanswered.
8. Record stale (item 32): the latest priority assessment predates today (realised exposure kept, 10 features, Must
   issues open), and the tag "Two-Regime Zeros" fits the amount task, not claim frequency. Remedy: an Assessment line
   for today's change, and the tag reviewed.
Untested: the Wüthrich and Merz quotes (book); "never better at quotation, 1.29"; the chain-grouped and block-temporal
splits under the rate target; "capping would raise their rate by 11%"; "9,942 before"; the content-ordering shuffle.

</details>

<details><summary>Column audit</summary>

**fremtpl2 column audit (column-auditor, exposure re-review 2026-11-06, full tier)**

Verdict: fine under the new rules. Exposure is out of the features (LEAK-41, MET-15 met); no remaining feature
carries it through a post-quote channel; every feature is a rating factor known at the quote. One documentation gap
(LEAK-41 asks the definition to report the probe-22 numbers; the notes do not). Nothing settled in issues 5, 7, 8, 9
is reopened by today's change.

Inputs read: the folder's dataset.py, README.md and REVIEW.md (incl. my 2026-11-04 column
table, REVIEW.md lines 594-683), leak_checks.md (LEAK-41, probe 22), cleaning_features.md (CLEAN-10, CLEAN-16),
metrics.md (MET-15), CHANGES.md, probes/probe22.txt, probes/probe22_l2.txt, participant_kit/task.md.
Prediction point (first curation_comments bullet): the quotation of the policy for the accounting year.

Runs:
- dtype probe: `dtype_probes.py fremtpl2` -> "0 of 9 columns flagged; no codebook" (CASdatasets help page read by
  hand, as on 2026-11-04).
- Frame profile of the built container (677,991 x 11; features = the 9 rating factors; sample_weight = Exposure).
- Probe-22 design extended to the four features the probe did not check, plus a replication for Region and DrivAge
  (shipped 3 folds x 3 seeds, 50k
  caps, LightGBM Poisson weighted by Exposure).
- Region x IDpol block table of mean Exposure (raw via _load_raw, IDpol // 1e6).

**Column table**

| column | meaning (CASdatasets help page) | known at quote? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| claim_frequency (target) | ClaimNb / Exposure, claims with a cost per year insured | outcome | float64, 0 to 365 (1 claim in 1 day); weighted mean 0.0738, unweighted 0.1186; untransformed; _clean checks x Exposure rebuilds ClaimNb | fine | MET-14, CLEAN-16 (deviance -> identity scale) |
| Exposure (weight scoring column) | years insured in the record's period | no: realized, cut short by cancellations, often after a claim | float64, 1/366 to 2.01, 181 values: 2-decimal grid on 99.0% of rows, day fractions /365 and /366 on the 1-3-day rows; 1,224 rows > 1 kept | fine as weight + denominator, never a feature (feature_columns excludes it) | LEAK-41, MET-15, CLEAN-11 |
| VehPower | power of the car ("ordered values") | yes | int64 4-15, numeric keeps the order; 2,926 at 15 vs 2,350 at 14 (possible top code, source silent) | fine | CLEAN-14 |
| VehAge | car age, years | yes | float64 0-85; 99/100 (48 rows) missing as default date; 80-85 kept as unusual | fine | CLEAN-10, CLEAN-11 |
| DrivAge | driver age, years | yes | float64 18-100; 66 block-0 rows at 99 missing (issue 9 settled); 4 at 99 and 3 at 100 elsewhere kept | fine | CLEAN-10 |
| BonusMalus | French bonus-malus coefficient (50-350) | yes in blocks 5-6 (start-of-year value); blanked in blocks 0-4 (issue 5 settled) | float64, 79,993 non-null (11.8%, matches task_summary "12%"), 50-190 | fine | LEAK-10, LEAK-7 |
| VehBrand | car brand, "unknown categories" | yes | category, 11 levels, unordered | fine | CLEAN-14 |
| VehGas | Diesel or Regular | yes | category, 2 levels | fine | CLEAN-14 |
| Area | density class, "A rural ... F urban centre" | yes | ordered category A<B<C<D<E<F, order matches the help page and Density bands (A 1-50, B 50-100, C 100-500, D 500-1993, E 2001-9850, F 10008-27000) | fine (coarse copy of Density, published by the source) | CLEAN-14 |
| Density | inhabitants per km2 of the city | yes | int64 1-27,000; 27,000 = 10,514 rows, all Ile-de-France (Paris, likely rounded) | fine | CLEAN-11 |
| Region | 22 pre-2016 regions | yes | category, 22 levels | fine | CLEAN-14 |
| IDpol (dropped) | policy number; its block marks period/sub-portfolio | n/a | dropped after the block-based masks | fine | CLEAN-3 |
| ClaimNb, sev_claims (dropped) | the count and its rebuild from freMTPL2sev | outcome | dropped; ClaimNb is part of the target | fine | LEAK-10 |

**The weight column and the features that predict it (LEAK-41, probe 22)**

Exposure values: mean 0.529, median 0.49; 24.8% exactly 1; 18.8% at <= 0.1. The claim rate falls steeply with it
(0.172 per year at <= 0.1, 0.055 at a full year, 0.040 above a year), the cancellation-after-claim footprint that
made it a leak as a feature. It ships only as the weight scoring column; feature_columns(c) returns the 9 rating
factors without it.

Features fitted on Exposure (probe 22): R^2 0.169, Spearman 0.411; top by gain Region 29%, DrivAge 21%, VehAge 19%,
VehBrand 11%, Density 11%. Leak reference: Exposure as a feature gains +0.0048 (SD 0.0019) Poisson, +0.0067
(SD 0.0042) L2. Weight-mediated gain per feature, the worse of the two fits (LEAK-41 decides on the worse):

| feature | mediated, Poisson (probe) | mediated, L2 (probe) | mine, Poisson | timing | call |
|---|---|---|---|---|---|
| Region | +0.00099 (SD 0.00082) | +0.0016 (SD 0.0042) | +0.0012 (SD 0.0009) | quote | stays (USE-6) |
| DrivAge | +0.0012 (SD 0.0019), 38% | +0.0006 (SD 0.0025) | +0.0016 (SD 0.0011) | quote | stays (USE-6) |
| VehAge | -0.00003 (SD 0.0016) | -0.0011 (SD 0.0027) | - | quote | stays |
| VehBrand | -0.0073 (SD 0.021) | +0.0009 (SD 0.0036) | - | quote | stays |
| Density | +0.0003 (SD 0.0015) | -0.0022 (SD 0.0034) | - | quote | stays |
| VehPower | not checked | not checked | +0.00014 (SD 0.00075) | quote | stays |
| BonusMalus | not checked | not checked | +0.00005 (SD 0.00057) | quote (blocks 5-6) | stays |
| VehGas | not checked | not checked | +0.00007 (SD 0.00092) | quote | stays |
| Area | not checked | not checked | +0.00002 (SD 0.00088) | quote | stays |

None is above 2 SD; Region and DrivAge sit at 1.1-1.4 SD in both runs, so they are the two to name. Both are fixed
at the quote, so LEAK-41 keeps them whatever they score. The mechanism is structural, not outcome-driven:
- Region: mean Exposure by region spans 0.36-0.66, mostly through the sub-portfolio mix of the IDpol blocks (block
  means 0.61/0.63/0.50/0.50/0.57/0.38/0.36 for blocks 0-6; Centre is 23-34% of blocks 0-4 and 1.8% of blocks 5-6;
  Haute-Normandie is at 0.27-0.30 in blocks 2-3 only). R^2 of Exposure on Region 0.065, on block 0.047, on
  block x Region 0.100. That is how the accounting cuts contracts per sub-portfolio, fixed before the year.
- DrivAge (Spearman +0.16) and VehAge (+0.18): older drivers and cars stay longer, i.e. less churn: risk selection
  (USE-6), not a value set after the quote.
- BonusMalus's missingness is the block 0-4 vs 5-6 indicator: R^2 0.025 on Exposure alone (non-null rows mean
  0.368 vs 0.550), mediated gain +0.00005. The block is fixed when the record is created; stays.
No feature is a value set or cut after the quote (no earned premium, no realized length, no group sum of exposures,
no precision marker). The precision marker sits only in Exposure itself (day fractions /365 vs /366 on the
1-3-day rows), which is no feature.

**Problems, ranked (principles.md order: validity first)**

1. Documentation gap, LEAK-41 (Must rule; this is its reporting clause, a mild fix). LEAK-41 says "for each suspect
   column the definition reports its gain on the declared metric with an L2 fit on the shipped scale and with the
   weighted actuarial fit, and decides on the worse". The notes report Exposure's own gains (0.0039-0.0047) but
   not probe 22's feature-side result. No column is above noise, so nothing is "suspect" in the strict sense, but
   Region and DrivAge are the probe's top features with 1.1-1.4 SD mediated gains.
   Remedy (mildest): one sentence in the Exposure bullet of curation_comments, e.g. "Probe 22: the rating factors
   predict Exposure at R^2 0.17 (Region, DrivAge, VehAge first, through the sub-portfolio mix and churn); no
   feature's gain goes through it above noise under the Poisson or the L2 fit (largest Region +0.0010 to +0.0016,
   DrivAge +0.0006 to +0.0012); all are known at the quote and stay (LEAK-41, USE-6)." No code change.

2. Protocol note, not a column problem (LEAK-9; for the task gamer). The participant kit hands out Exposure for every
   row in scoring.parquet, test rows included, as the metric needs it. A participant who reads the test rows' weight
   as an input recovers the +0.0048 leak. This is the scoring-column contract every weighted task has ("Scoring
   columns ... never features" in task.md); nothing to change in the definition. Flagged so the gamer's report
   measures it under the rate target.

3. Questions carried over, unchanged by today (no action): VehPower 15 may be a "15 or more" top code (2,926 vs
   2,350 at 14; source silent; numeric is still lossless for order); Density 27,000 is likely Paris rounded.
   Neither changes a verdict.

Settled points not reopened: BonusMalus blanking in blocks 0-4 (issue 5), IID split (issue 7), renewal signal
(issue 8), DrivAge 99 in block 0 (issue 9). Today's change does not touch these columns' timing; my extended probe
shows BonusMalus does not carry Exposure (+0.00005).

</details>

<details><summary>Split audit</summary>

**fremtpl2 - split auditor, exposure re-review (2026-11-06, full tier)**

VERDICT: right with notes. IID (ForcedIIDFromTemporal) still matches the use case under the rate target. Every row is
on the training side whatever its time on risk, so no side is selected by the realized weight (LEAK-41, SPLIT-9). One
new fact reopens issue 7 as a question, not a fix. The whole IID-vs-grouped gap that the study left open comes from a
single 20-row rating profile (the counts 5-16 kept on 2026-11-04). LightGBM learns it from copies on the training side.
Without those 20 rows the gap is zero.

Setup: LightGBM Poisson (300 trees, lr 0.05, 31 leaves, min_child 200) on claim_frequency with sample_weight=Exposure.
Scores are the declared metric (Exposure-weighted mean Poisson deviance, floor 1e-4). I checked my function against
the container scorer on fold 0 (dummy 0.47980 both). "OOF" means the out-of-fold score over all 677,991 rows, so the
splits are compared on the same rows. All numbers are on the rate scale; divide by about 1.89 for the old count scale.

1. Regime
   Pricing at the quote, for comparable policies of one portfolio. A temporal split would fit, but the release has no
   dates (SPLIT-8). The declared regime matches. The 9 features are the rating factors, and Exposure, ClaimNb and IDpol
   are out. The split comment and task_summary.split describe the regime correctly.

2. Memorizer under IID and under a split grouped on identical rating factors (the study's open item)
   OOF deviance, 3 folds:

   | | dummy | LightGBM | Poisson GLM |
   |---|---|---|---|
   | IID (shipped folds) | 0.47929 | 0.46813 | 0.47171 |
   | grouped, shipped 9-feature key | 0.47931 | 0.46970 | 0.47182 |
   | grouped, raw factors (lit. key) | 0.47930 | 0.46902 | - |
   | grouped, next-year chains | 0.47930 | 0.46860 | - |

   Seed noise: IID with other random folds gives 0.46824 and 0.46839. Grouped on the shipped key with other seeds gives
   0.46905 and 0.46920. The LightGBM gap is +0.0008 to +0.0016, which is 7-14% of its skill over the dummy (0.0112).
   The GLM gap is +0.0001.
   - An explicit memorizer gains nothing. 36.4% of test rows (23.2% of test exposure) have an exact feature copy on the
     training side. A pure lookup of the profile's training rate, shrunk to the portfolio rate, scores 0.48459, worse
     than the dummy. Blending the lookup into LightGBM (k = 0.5, 2, 10 years) never beats LightGBM (best 0.46823).
   - The whole gap is one profile. The grouping gap has a 0.00157 total over rows, and the 50 rows with the largest
     change carry 102% of it. They sit in profiles of 3-20 rows that have a claim. One profile does it: power 4, B1,
     Regular, area D, density 824, Languedoc-Roussillon, BonusMalus blank, car/driver 12/52 in block 2 and 13/53 in
     block 3. It has 20 rows, 77 claims and 4.63 years, a rate of 16.6 claims a year against about 0.07 for the
     portfolio. It includes the 7 policies with 5-16 claims that the notes already name, which Wuthrich and Merz suspect
     to be one driver or a rental fleet. Under IID its rows fall 6/7/7 across the folds. LightGBM predicts 3.8-17.2
     claims a year for its test rows from the training copies. Grouped on the shipped key, it predicts 0.073-0.078.
     Without those 20 rows (8 rows in the "bigcount" filter of the result files):
       IID 0.46746 / 0.46759 / 0.46751 against grouped 0.46750 / 0.46758 / 0.46766 (seeds 0/1/2), a gap of -0.00001
       to +0.00015. For the GLM the gap is 0.46951 against 0.46958.
     The ranking (LightGBM ahead of the GLM) is the same under every split.
   - Rule: SPLIT-29 / LEAK-17 (Must) with SPLIT-30 (a hit is a question). This is not "many rows". It is one entity
     whose rows carry the label and that new quotes would not share. Under IID a model is rewarded for recognising it,
     and that is the only memorization the data rewards. The rate target does not create it: the weighted rate equals
     the count deviance with an offset. Issue 7 was settled without this number, and the 2026-11-04 call that kept
     counts 5-16 weighed their share of the deviance, not their effect on the split.
   - Remedies, mildest first:
     (a) Keep IID and add one sentence to splits_comment and the notes. It names the profile and the gap (+0.0008 to
         +0.0016 on LightGBM, 0 without it) and says the IID score depends on how its 20 rows fall.
     (b) Group on the identical shipped rating factors. This is the key Schelldorfer and Lorentzen-Mayer use, for this
         reason. It costs nothing elsewhere: 488,666 groups, folds of 224,778-226,838 rows. Per the brief, an equal
         profile is not a proven entity id. Here it is a composite key for which one fleet or driver is the evidence
         (splits.md pattern "Composite keys"). The tag would move to ForcedGroupedFromTemporal.
     A filter (dropping the 20 rows) undoes the 2026-11-04 keep and is not recommended. I lean to (a). (b) is the
     choice if the curator reads the profile as one entity. This is the curator's call; the issue 7 options need this
     row added.

3. Next-year records across the split (issue 8, re-measured on the rate)
   161,883 inferred pairs (next_year_rows). 66.5% of them have their two rows on different sides of the shipped folds.
   30.9% of test rows have a linked row (previous or next year) on the training side. The features below are upper
   bounds, because they read IDpol, which does not ship. Shipped columns single out the partner for about 55% of links
   (notes). LightGBM OOF on IID, 0.46813:
     + has-previous / has-next flags (label-free)          0.46716  (-0.00097)
     + partner's Exposure (training side only)             0.46737  (-0.00077)
     + flags + partner's Exposure + partner's rate         0.46677  (-0.00136)
     + the above + partner's shipped BonusMalus            0.46563  (-0.00250)
   Without the 20-row profile the gains are the same (-0.00097 / -0.00142 / -0.00262). Grouping on the chains removes
   the label part but not the flags: LightGBM + flags scores 0.46746 against 0.46860 for LightGBM alone under the chain
   split. This matches issue 8 (LEAK-9 protocol line; no split removes it). Note: the notes quote it on the count scale
   (0.0008 after blanking; 0.0009-0.0010 for the label-free signal). On the shipped metric the full oracle is about
   0.0015-0.0025 and the flags about 0.0010. The numbers in fit_reason and the notes should be restated on the rate
   scale.

4. Time on risk cut at the accounting year and at the release
   Exposure by IDpol block (share below a year / exactly a year / above a year; max):
   - blocks 0-4: 65-77% / 23-35% / 0-0.9% (the 1,224 rows above a year are in blocks 1-2)
   - block 5: 99.8% / 0.17% (73 rows) / 0; quantiles 50% 0.33, 99% 0.96
   - block 6: 100% / 0 / 0; max 0.74, 90% 0.73

   Block 6 never reaches 0.74 of a year, so it is cut at a calendar date (most likely the extraction date), not only by
   the outcome. Block 5 is almost all partial years too. The rate falls less with exposure there (0.082 at
   Exposure <= 0.25 to 0.057 at 0.75-1) than in blocks 0-4 (0.147 to 0.077, 0.055 at a full year). So in 5-6 the short
   records are largely censored rather than ended by a claim. Under IID:
   - No side admits or drops rows by the weight. The rate with Exposure as weight treats a censored record
     proportionally, so LEAK-41's "no model trained or scored on rows selected by the realized weight" holds.
   - Note for the definition: the Exposure ScoringColumn description says "shorter when the policy ended early, often
     after a claim". In blocks 5-6 it is mostly cut by a date (block 6 capped at 0.74). Add one clause; this is
     wording, not a split change.
   - Note for any later temporal variant (SPLIT-8: recover the years): block 6, the newest period, covers about three
     quarters of a year, a season-shaped test window. A model tested there scores a partial year.
   - Records of one contract year split across two accounting years: 54,109 pairs have exposures summing to <= 1.01
     (63-67% of linked pairs in blocks 3-5). 66.5% of them straddle the folds. They are part of the transductive
     signal of item 3, not a separate issue.

5. The forced-temporal alternative, re-run on the rate
   Train on blocks 0, 2, 4, 5 (396,446 rows) and test on blocks 1, 3, 6 (281,545 rows). LightGBM scores 0.47077,
   against 0.46987 for the same rows under the shipped IID folds: +0.00090 (row bootstrap SE 0.00035; dummy 0.48176).
   Without the 20-row profile the gap is +0.00046 against 0.46909. The notes give +0.00049 on the count scale; on the
   rate it is +0.0009, half of it the same profile. The ranking against the GLM is unchanged. IID is slightly
   optimistic, as the notes already say.

Ranked (principles.md: P4 honest evaluation first)
 1. Should, open question to the curator (SPLIT-29/LEAK-17 via SPLIT-30; reopens issue 7 with a new number). One
    20-row profile with 77 claims makes the whole IID-vs-grouped gap (+0.0008 to +0.0016, 7-14% of LightGBM's skill).
    Mildest remedy: a note (a). Alternative: group on identical shipped rating factors (b).
 2. Note (LEAK-9, issue 8 settled). Restate the next-year signal on the shipped metric: label-free flags about 0.0010,
    with partner labels and next-year BonusMalus up to about 0.0025 (upper bounds by IDpol).
 3. Note (LEAK-41 wording). The Exposure description should say blocks 5-6 are cut by a date (block 6 at most 0.74
    year). Record the partial-year newest block for a future temporal variant (SPLIT-8, SPLIT-12).
 4. Note (SPLIT-8). Restate the forced-temporal cost on the rate: +0.0009 (+0.0005 without the profile).
 Not a problem: an explicit profile memorizer gains nothing (best blend 0.46823 against LightGBM 0.46813). No row is
 selected by its weight. The split sizes are 451,994 / 225,997 x 3.

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner (pricing actuary, French motor third-party liability book): fremtpl2, exposure re-review 2026-11-06, full tier**

**VERDICT**

Fit: approximate (unchanged). Option A makes the target and its weighting exactly what I price with (claims per year
insured, each record counting by its time insured), so the target is no longer a gap; the remaining gaps are inputs
I always have at the quote (the bonus-malus coefficient, blank in 88% of records) and the missing calendar year.
Metric scores the decision: yes. The Exposure-weighted Poisson deviance of the rate is the source's offset-model
deviance up to a per-fold constant, strictly consistent for the expected rate, at the unit I price (a policy-year).

**WHAT I MEASURED (shipped folds, declared scorer)**

LightGBM Poisson (500 trees, lr 0.03, 31 leaves, min_child 200), trained with sample_weight = Exposure, 9 features:
- fold 0: constant 0.47980, LightGBM 0.46864, skill 0.0233; A/E 0.992; exposure-weighted Gini 0.192
- fold 1: constant 0.48068, LightGBM 0.46810, skill 0.0262; A/E 1.000; Gini 0.203
- fold 2: constant 0.47739, LightGBM 0.46764, skill 0.0204; A/E 1.007; Gini 0.191
- mean skill 0.0233 (SD 0.0029), A/E 1.000, Gini 0.195; 0.0% of predictions at the 1e-4 floor.
  Skill on rows with BonusMalus present (blocks 5-6, ~26.7k test rows per fold): 0.0129; on blanked rows 0.0242.

Same model trained WITHOUT the weight (fold 0): deviance 0.50043 against the constant's 0.47980 (skill -0.043),
  A/E 0.642 (the book priced 1.56 times too high), Gini 0.136. This confirms MET-15's 1.61x on the new scale.
Earlier panel's actuary (REVIEW.md, BonusMalus in all rows, log(Exposure) offset): skill 0.0644. The fall to 0.0233 is
  the cost of the BonusMalus blanking of 2026-11-05 (issue 5), not of option A: option A is the offset model.
Task probe (probes/task.txt) flags no_signal (TP-1, TP-2) from an R^2-type skill (+0.002). Read with care: a claim
  frequency model always has R^2 near 0.01 because Poisson noise dominates; on the declared deviance the skill is
  0.023, A/E is 1.00 and the Gini 0.19 (typical published MTPL frequency Ginis are 0.2-0.3). The signal is real.

**Q1. AT THE QUOTE, DO I HAVE THESE INPUTS? (USE-3, USE-6)**

- VehPower, VehAge, VehBrand, VehGas, DrivAge, Area, Density, Region: yes, all on the quote form or derived from the
  address (commune density, region). Standard French tariff variables.
- BonusMalus (the CRM, coefficient de reduction-majoration, Code des assurances A121-1): I ALWAYS have it at the quote,
  from the relevé d'information the previous insurer must hand over, and it is the strongest single factor in the
  French tariff. Its blanking in blocks 0-4 is justified by the release (it looks recorded after the year's claims,
  LEAK-10, settled issue 5), but the task is now "price most of the book without the CRM". This is the largest
  remaining gap between the data and my decision (skill 0.064 -> 0.023 on the same model class).
- Exposure: correctly not an input now (LEAK-41). At the quote I know the planned term (a year), not the realized
  share of the year; a cancellation after a claim is information from after the quote. Probe 22: the features
  predict Exposure at R^2 0.169, and no feature's gain runs through Exposure above noise (Poisson and L2 fits), so
  nothing else needs to go.
- Missing inputs I would always have: new business vs renewal and tenure, start date and calendar year, product or
  sub-portfolio code (blocks 4-6 are mostly part-year records), cover level and deductible, vehicle group / value
  (SRA classification), number of named drivers, licence age. Gender is rightly absent (banned in EU pricing since
  21 December 2012, Test-Achats).

**Q2. IS THE TARGET WHAT I ACT ON? (USE-5, MET-14)**

Yes. The frequency model of a tariff estimates lambda(x), claims per year insured; the pure premium is lambda(x)
times the expected severity, and the annual premium is earned pro rata to the time insured. claim_frequency =
ClaimNb / Exposure with Exposure as the weight is the textbook form: Ohlsson and Johansson (2010) model the claim
frequency with the duration as the GLM weight; Noll, Salzmann and Wuthrich use log(Exposure) as offset; scikit-learn's
freMTPL2 example ships exactly Frequency = ClaimNb / Exposure with sample_weight = Exposure in fit and score. I want a
positive number (an expected rate), not a class.
Would I weight records by their time insured? Yes, without hesitation (MET-15): the book's claims and the earned
premium are sums over time insured, and the weighted rate is the maximum-likelihood rate of a constant claim hazard
even when a claim ends the policy (the record is then censored at the claim, and N / time at risk is still the
hazard's estimator). That is why the earlier free-Exposure model under-priced full-year quotes (actual 1.29 times its
price) and the weighted rate does not. Unweighted, the same model prices the book 1.56 times too high (A/E 0.642).
Frequency alone, without severity (D12), is a standard standalone model in a frequency-severity tariff; no gap.
Kept rows with Exposure up to 2.01 (1,224) and the 8 policies with 5-16 costed claims: fine for me; their weights are
their time at risk and they carry little of the score (0.0012 of 0.2534 on the count scale for the high counts).

**Q3. DOES ONE ROW MATCH ONE DECISION? IS THE TEST WHAT I FACE? (USE-10, SPLIT-8)**

- One row is a policy-year record, the unit of a frequency model's data; renewals split across two accounting years
  (Wuthrich and Merz, Sec. 13.1) and split contract years in blocks 4-6 are two rows of one contract, which the weight
  now handles correctly: each part counts by its own time.
- The test I face is next year's renewals plus new business. Random rows stand in for it (ForcedIIDFromTemporal); the
  earlier panel measured out-of-time no harder (+0.00049 deviance, ranking unchanged). Under the rate target this is
  unchanged: nothing about the split depends on the target's form.
- My known policies' own history is legitimate (USE-10), but the CRM carries it by design; it is gone in 88% of rows.

**Q4. WOULD I USE THIS MODEL?**

As a model-selection benchmark for a frequency model: yes, more so than before, because the score now rewards the
quantity I price and no longer rewards reading the realized Exposure. I would not deploy a tariff fitted on it: no
CRM in most rows, no year, an unknown insurer.
I would trust a model that: predicts a positive rate for every policy; balances the book (A/E near 1, here 0.99-1.01);
ranks risks (Gini about 0.2); is monotone where tariffs are (rate falls with the CRM bonus where present).
I would distrust: any method that ignores the sample weight (it loses to the constant, see above); gains from a
method reading other rows (the next-year record, settled issue 8; the gamer's +0.00071 is still to be re-measured
under the rate); and predictions pinned at the floor (random forest 0.5% in the task probe: a zero rate is
unpriceable).

**Q5. DOES THE METRIC SCORE MY DECISION? Yes (MET-1, MET-8, MET-13, MET-14, MET-15).**

- mean_poisson_deviance of the rate weighted by Exposure = the source's count deviance against Exposure x rate times
  n / sum(Exposure) of the scored rows (1.886-1.896 per fold), a constant within a fold: models rank as by the source's
  metric (MET-11 origin source). It is strictly consistent for the mean rate, it penalizes a wrong level as well as a
  wrong ranking, and it scores the policy-year I price.
- The weight is right (MET-15): the decision's quantity, the book's claims against the earned premium, is a sum over
  time insured.
- The floor 1e-4 claims per year is about 740 times below the portfolio rate (0.0738) and two orders below any
  plausible risk cell: it never binds on a sane model (0.0% for LightGBM) and bounds the cost of a zero prediction
  (MET-13). I would clip there too.
- No threshold, k or cost matrix exists in pricing: MET-6, MET-7 and MET-9 do not apply.
- What I would choose: the same metric. I would add actual/expected on the book and an exposure-weighted Lorenz curve
  and Gini as diagnostics, as scikit-learn's freMTPL2 example and Wuthrich and Merz do, but not as the score: A/E is
  not a scoring rule and the Gini ignores the level.

**GAPS, RANKED BY HOW MUCH THEY CHANGE THE TASK**

1. BonusMalus blank in 88% of records (settled issue 5). I always have the CRM at the quote; without it honest skill
   is 0.023 instead of 0.064. The task stays real but is "price without the CRM" for most rows. Not to reopen (the
   column looks post-outcome there), but the largest gap.
2. A method without sample-weight support is mis-scored by design: unweighted, LightGBM scores 0.50043 against the
   constant's 0.47980 (A/E 0.64). That is correct for my decision (such a model would mis-price the book) but it is a
   benchmark-design consequence: the harness must pass `sample_weight` to every method that takes one and the
   leaderboard should say which methods could not (in-context learners without a weight argument).
3. No calendar year (SPLIT-8, ForcedIIDFromTemporal): measured small, ranking unchanged.
4. Missing standard tariff inputs (tenure, product code, cover/deductible, vehicle group, start date) and a mixed book
   (frequency 0.059-0.086 by block): a coarser tariff than any insurer's, an honest public subset.
5. Cross-row channel to next-year records (settled issue 8): unchanged by option A; the gamer's re-measure is open.
6. Exposure-as-target denominator: closed by option A. Exposure as a free feature was worth +0.0048 (SD 0.0019,
   probe 22); it is now no input.

**WHAT AN EXPERT WOULD CHANGE**

- Nothing in the target, the weight or the metric: this is how I would set them up.
- fit_reason / notes: state the honest skill under the shipped rate target (about 0.023 deviance skill, A/E 1.00, Gini
  0.19, my 3-fold LightGBM) and that the BonusMalus blanking, not option A, took it from about 0.064, so a reader does
  not read the low skill as a broken target.
- Task probe reading: the no_signal flag on an R^2-type skill is misleading for a Poisson frequency task; record the
  deviance skill next to it or accept the flag with that reason.
- Benchmark protocol / README: say that the task needs the sample weight and that a method ignoring it scores worse
  than the constant rate (MET-15's 0.26187 vs 0.25342 on the count scale; 0.50043 vs 0.47980 here, fold 0).

**SOURCES**

- CASdatasets freMTPL help page: https://dutangc.github.io/CASdatasets/reference/freMTPL.html
- scikit-learn, "Poisson regression and non-normal loss" (freMTPL2: Frequency = ClaimNb/Exposure, sample_weight =
  Exposure in fit and in mean_poisson_deviance; Lorenz/Gini and calibration as diagnostics; Exposure not a feature):
  https://scikit-learn.org/stable/auto_examples/linear_model/plot_poisson_regression_non_normal_loss.html
- Noll, Salzmann and Wuthrich 2018 (SSRN 3164764) and its code (FreMTPL_1b load data.r, line 35), as cited in dataset.py.
- Wuthrich and Merz 2023, Statistical Foundations of Actuarial Learning, Sec. 5.2.4 and Appendix 13.1 (from the
  definition's notes; not re-read today).
- Ohlsson and Johansson 2010, Non-Life Insurance Pricing with Generalized Linear Models (claim frequency with duration
  as weight; from my knowledge, not fetched).
- Code des assurances A121-1 (CRM): https://www.legifrance.gouv.fr/codes/id/LEGIARTI000036754143/2018-04-01/ (as cited
  by the earlier panel; not re-fetched).
- Panel inputs: CHANGES.md, probes/task.txt, probes/probe22.txt, probes/probe22_l2.txt, REVIEW.md (earlier practitioner
  block), dataset.py; rules use_case.md (USE-3, USE-5, USE-6, USE-8, USE-10), metrics.md (MET-1, MET-6 to
  MET-9, MET-11, MET-13 to MET-15), leak_checks.md (LEAK-10, LEAK-41).

</details>

<details><summary>Blind review</summary>

**BLIND REVIEW: freMTPL2 claim frequency (clean room: data.parquet 200,000-row sample, task.md)**

Reviewer worked only from the clean room folder and the public web.

VERDICT: Include with changes. The task (exposure-weighted Poisson claim frequency for motor TPL pricing) is real, standard and honest, and Exposure is the right training/scoring weight. But as prepared, BonusMalus, the strongest rating factor, is 88% missing (0 missing in canonical copies). The scoring metric must also be a Poisson deviance: under weighted MSE the task cannot tell models apart.

**TASK**

An insurer's pricing actuary predicts the expected yearly claim count per policy (frequency = ClaimNb / Exposure) from rating factors known at underwriting. The prediction feeds the frequency part of the premium (frequency x severity). This is a real, central use, and freMTPL2freq is the reference dataset of the actuarial ML literature (Noll, Salzmann & Wuthrich, SSRN 3164764).

**EXPOSURE AS WEIGHT: CORRECT**

For a Poisson count N ~ Poi(lambda * e), the frequency y = N/e has variance lambda/e. Fitting y with weight e is equivalent to Poisson regression of N with a log(e) offset, which is exactly how the source literature uses it. Scoring with e as the test-row weight is also correct: it gives an exposure-weighted portfolio loss. Exposure must not be a feature (it is a duration and is only known after the fact), and task.md says it is not. Note that exposure is strongly associated with frequency in this data (weighted frequency 0.169 in the lowest exposure quintile (<=0.12y) vs 0.057 in the highest), a known artefact of freMTPL2. Using exposure as a feature would therefore leak, and the prepared task correctly keeps it out.

**CONCERNS, MOST TO LEAST SERIOUS**

1. BonusMalus is 88% missing, which looks like a preparation or source-version defect.
   Evidence: 176,395 of 200,000 rows have NaN. Missingness is flat across row position (0.880-0.885 per decile), so it is not a block. Missingness is not random: mean Exposure is 0.55 for missing rows vs 0.37 for observed rows, and claim_frequency is 0.124 vs 0.101. The OpenML copy (d/43593, from CASdatasets 1.0-6) reports 0 missing values for BonusMalus. CASdatasets documents it as "Bonus/malus, between 50 and 350". The CASdatasets changelog says nothing about NAs. In the observed rows the feature carries strong signal (weighted frequency 0.058 at BM=50 vs 0.108 at BM>100). In this table, however, a LightGBM Poisson model loses almost nothing without it (deviance 0.4757 with vs 0.4759 without).
   Change: Reload from a version where BonusMalus is complete (CASdatasets 1.0-x / OpenML 41214 or 43593, 678,013 rows), or find and fix the conversion that dropped it. If the current CASdatasets 1.2-1 release really has these NAs, document that and prefer the older complete release.

2. The metric must be exposure-weighted Poisson deviance. Under weighted MSE/RMSE/R2 the task is noise.
   Evidence (3-fold CV on the 200k sample, LightGBM, exposure weights). Weighted Poisson deviance: constant 0.4828, model 0.4757 (-1.5%). Weighted MSE: constant 0.25708, model 0.25650 (R2 about 0.002). Under the constant prediction, the 10 largest rows contribute 13.5% of the weighted SSE and the top 100 contribute 31%. These are one-claim policies with tiny exposure: target up to 365 at exposure 1/365, each adding N^2/e to the SSE. task.md says only "regression" and does not name a metric.
   Change: Fix the metric to weighted mean Poisson deviance, optionally with Gini/lift. Do not use RMSE or R2.

3. The signal is small and benchmark resolution needs checking.
   Evidence: the best model improves deviance by only about 1.5% over the mean, and claims are rare (3.7% of rows have a claim; about 7,400 claim events in 200k rows). On the full data with complete BonusMalus, the literature reports roughly 4-5% deviance reduction. With 3 folds on 678k rows there is enough data, but differences between strong methods will be in the 4th decimal.
   Change: Use the full 678k rows. Report deviance with fold standard errors or use more repeats. Fixing concern 1 should roughly double the headroom.

4. Known data-quality items are not addressed.
   Evidence: 363/200k rows have Exposure >1 (max 2.01), while the source says data are "observed mostly over one year". Implied ClaimNb (y*e is integer in every row) reaches 11, and the literature usually caps ClaimNb at 4 and Exposure at 1 as data errors (Noll et al. / Wuthrich). VehAge reaches 85. There are 19 NaN in VehAge and 18 in DrivAge (DrivAge max 99), and canonical copies have none. This suggests implausible values (e.g. 100) were nulled somewhere, which is acceptable if intended.
   Change: Cap Exposure at 1 and ClaimNb at 4 as in the reference papers, or state why not. Document the VehAge/DrivAge NaNs.

5. Near-duplicate rows cross the IID split.
   Evidence: 10.7% of rows share their full feature vector with another row in the 200k sample, and 2.5% are complete duplicates including target and exposure. freMTPL2 is known to contain the same policyholder split into several exposure periods (no policyholder ID is available). With a 3.7% claim rate and Poisson noise, I expect the leakage to be mild, but it slightly favours memorising models.
   Change: Optionally group by the full feature vector when splitting, or at least note it. Not blocking.

6. Minor preparation notes.
   Types are sensible: VehBrand, VehGas, Area and Region are categorical, and Area A-F is ordinal and almost a binned version of Density (Area exactly follows log-density cut-points; it is redundant but harmless). VehPower is int. Region uses region names ("Centre", "Ile-de-France", ...) rather than R-codes; this is fine and consistent with CASdatasets 1.2-1. The row count of 677,991 matches the CASdatasets 1.2-1 docs ("dim 677991 12"); the older version has 678,013 rows. IDpol is correctly dropped. I could not find what the 1.2 release changed.

**WHAT I COULD NOT CHECK**

- Whether the 88% BonusMalus NAs come from the CASdatasets 1.2-1 file itself or from the preparation. I could not download the .rda, the CASdatasets PDF manual would not extract (no PDF tools), and the Kaggle page did not render.
- The full 677,991 rows: I saw only the 200k sample.
- The metric and the actual fold assignment used by the benchmark.
- Whether the null VehAge/DrivAge values were intended cleaning.

Sources: https://dutangc.github.io/CASdatasets/reference/freMTPL.html ; https://dutangc.github.io/CASdatasets/news/index.html ; https://api.openml.org/d/43593 ; https://huggingface.co/datasets/mabilton/fremtpl2/blob/main/README.md ; https://ifoa-adswp.github.io/IBLM/reference/load_freMTPL2freq.html

</details>

<details><summary>Task gamer</summary>

**TASK GAMER REPORT - freMTPL2 claim_frequency (Poisson deviance, weight = Exposure, IID 3-fold)**

VERDICT: Only one real exploit exists: the training weight (Exposure). Using it as a feature cuts the deviance by
about 0.008 (1.7%). Adding the siblings' Exposure in duplicate-feature groups brings the cut to about 0.010. A much
bigger flaw works the other way: the preparation blanked BonusMalus, the strongest rating factor, on 88% of rows
(every source row with IDpol < 5,000,000). That costs an honest model about 0.040.

Honest baseline: LightGBM, objective=poisson, lr 0.05, 400 trees, 31 leaves, min_child_samples 200, sample_weight =
Exposure, on features(). Scores per fold: 0.46900 0.46844 0.46806 (mean 0.46850). Untuned default LGBM with L2 loss
scores 0.46931.
Noise reference: the baseline plus a column of random numbers scores 0.46961 0.46891 0.46822 (mean 0.46892), so
fold-level changes below about 0.0006 are noise.

**EXPLOITS (ranked by gain; lower is better, gain = baseline - exploited)**

| # | Exploit | Script | Honest | Exploited | Gain per fold (range) | Deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| 1 | Exposure + duplicate-group size + siblings' summed Exposure | a2_copies.py (B2), a4_exposure_format.py (D3) | 0.46850 | 0.45847 | 0.0101 / 0.0111 / 0.0088 | No: siblings' exposures are only known once the year is over | Same as 2; additionally a grouped split by the feature key |
| 2 | Training weight Exposure (or 1/Exposure, E==1, E>1) as a feature | a1_baseline_weight.py | 0.46850 | 0.46036 | 0.0084 / 0.0088 / 0.0072 | Partly: a planned term is known at the quote, a term cut short by cancellation is not | Keep Exposure out of the features (already done); see note |
| 2b | Only a "full year" flag (Exposure >= 0.99) | a5_exposure_where.py | 0.46900 (fold 0) | 0.46438 | 0.0046 (fold 0) | Same as 2 | Same as 2 |
| 3 | Duplicate-group size counted over train+test (features only, transductive) | a2_copies.py (A) | 0.46850 | 0.46802 | 0.0006 / 0.0010 / -0.0000 | Partly (counting identical risks in the portfolio is possible; counting the test rows is not) | Grouped split; at the noise level anyway |

**FLAWS THAT HURT AN HONEST MODEL**

| # | Flaw | Script | Kit score | Score without the flaw | Gain | Fix |
|---|---|---|---|---|---|---|
| F1 | BonusMalus blanked on 597,998 of 677,991 rows | compare_source.py, a6_bm_restore.py | 0.46850 | 0.42876 (BM restored from the source on 566,782 matched rows; 108,766 still NaN) | 0.0392 / 0.0390 / 0.0411 | Rebuild the column from the source; the full fix is larger than this partial restore shows |
A participant cannot avoid F1 with an honest choice from the kit. The restore needs a lookup in the published source,
which works on any public dataset, so it is not counted as an exploit. It only measures what the preparation lost.
With BonusMalus restored, adding Exposure still gains about the same: 0.42876 -> 0.42123.

**FINDINGS**

1/2. Exposure as a feature (the weight attack). Claims per year fall steeply with exposure: 0.30 for E <= 0.05,
0.14 for (0.05, 0.1], 0.12 for (0.1, 0.25], 0.097, 0.080, 0.075, 0.055 at E = 1, and 0.040 for E > 1. As a feature,
Exposure cuts the deviance from 0.46850 to 0.46036. On fold 0, rows with E < 0.25 hold 54% of the gain but only 7%
of the weight, and full-year rows hold 29% of the gain. A model at the quote knows the planned term. It does not know
whether the policy will be cancelled or replaced during the year, and a claim can cause either. Short exposures
having more claims per year is the usual sign of that. The fact that would decide it: the share of exposures below
one year that come from mid-year starts or the end of the observation window (known at the quote) rather than from
cancellations (not known). The data cannot answer this. The kit already keeps Exposure out of features(), so the
fix is in place: Exposure stays a scoring and weight column only. A stricter version would cap Exposure at 1, as
the case study does, but that changes the metric.

1. Duplicate groups and siblings' exposure. 327,862 rows (48%) share every feature value with another row: 222,470
rows sit in pairs and the largest group has about 20 rows. In the source, such groups are consecutive IDpols, which
suggests one policy split into several contract records. A group's Exposure sums to a median of 0.98, so a row's
siblings tell you how its year was split. Adding the group size and the siblings' Exposure on top of own Exposure
gives 0.45847, an extra 0.0019 over Exposure alone. Without own Exposure, the group size and siblings' Exposure gain
only 0.0004, which is noise (B: 0.46811). The siblings' claims do not leak: leave-one-out sibling claims and
exposure from training rows score 0.46855 (C), and P(claim) is 3.2% when a sibling has a claim versus 2.5% when
none does. The IID row split separates the records of one policy, but this barely moves the score. The mildest fix
is a split grouped by the feature key, as an option, not a must.

F1. BonusMalus blanking. The source (OpenML 41214, freMTPL2freq) has BonusMalus on every row. In the kit it is
present only on 79,993 rows. Matching the kit to the source on claims, exposure and features shows the kit keeps
BonusMalus exactly for IDpol >= 5,000,006 (77,549 of 77,549 matched rows) and blanks it for every IDpol <=
4,189,196. Where it is present, it equals the source value 100% of the time. The blanking is an IDpol range, not
random and not by value: the blank share is 85-93% for every BonusMalus value. Restoring BonusMalus on the 84% of
rows that match uniquely improves the honest model by 0.040, which is five times the Exposure exploit. Because the
blanking follows IDpol, "BonusMalus missing" also stands for IDpol < 5M. The baseline already uses the NaN, and an
explicit missing indicator adds nothing (0.46850). Fix: re-ingest BonusMalus. The blanks look like a parsing or
type step that failed for most of the file. Other differences from the source: 22 rows dropped (678,013 ->
677,991), VehAge > 85 set to NaN (48 rows; source max 100), 66 DrivAge NaN, BonusMalus max 190 vs 230 in the
source, and Region codes renamed to names. Exposure and ClaimNb are not capped (max 2.01 and 16, as in the source),
and claim_frequency = ClaimNb / Exposure exactly.

**ATTACKS THAT FOUND NOTHING**

- Missing-value indicators (BonusMalus NaN, NaN count): 0.46850, no change. The model already uses the NaNs.
- Exposure precision: 1% of rows have an exposure off the 2-decimal grid (multiples of 1/365). They are just the
  shortest exposures (mean 0.005). As a flag alone: 0.46850, no change. Added to Exposure: 0.46036, no change.
- Training-set siblings' claims (target encoding of the duplicate group, leave-one-out): 0.46855 (+0.0000).
- Group size counted on training rows only: 0.46853.
- Row order: claim rate by 50k-row block runs 0.071-0.077 with no trend. Next-row claim agreement is 0.92914 against
  0.92913 expected under independence, and IDpol is not in the kit. Nothing.
- Fold composition: test claims per year 0.0735 / 0.0738 / 0.0740 against train 0.0739 / 0.0737 / 0.0737, and no
  overlap between train and test.
- Formats: every numeric feature is a whole number. Nothing to read from decimals.
- Honest training choices (the opposite flaw): capping ClaimNb at 4 and Exposure at 1 in training, as the source case
  study does, scores 0.46909. Capping ClaimNb only scores 0.46915. Dropping training rows with ClaimNb >= 5 scores
  0.46995. All three are worse than the baseline, so the uncapped training rows do not hurt an honest model.
- Looking the rows up in the published source: it works (566,782 unique matches give IDpol and BonusMalus), but it
  is not ranked. The source's ClaimNb is the label, so the lookup recovers the target of most rows.

**NOT CHECKED**

- Whether short exposures are cancellations or mid-year starts. That needs the insurer's contract data. It decides
  how much of exploit 2 a deployed model would legitimately have.
- Hyperparameter tuning, and models other than LightGBM. All gains are measured with one fixed LightGBM setup.
- Web search turned up no competition leak threads for this dataset (it is a CASdatasets/OpenML benchmark, not a
  Kaggle competition). A Springer chapter on CASdatasets notes that policies with more than 5 claims look like data
  errors from one driver with very short exposures. Dropping them from training hurt (see above).

Sources: https://api.openml.org/d/41214 (downloaded to work/src/fremtpl2freq.arff),
https://link.springer.com/chapter/10.1007/978-3-031-12409-9_13 ,
https://dutangc.perso.math.cnrs.fr/RRepository/pub/web/vignettes/poisson_vignette.html

</details>

<details><summary>Precedent check</summary>

**fremtpl2 precedent check, full tier, exposure re-review of 2026-11-06.**

VERDICT: Consistent. The definition follows bemtpl97 and the PR #47 insurance tables on every point the new rules fix. Each of the three calls it reverses is reversed with a stated fact. I found no departure without a reason, no drift and no third exception. One reflection prompt is drafted, about a stale precedent row in splits.md. One reporting gap against LEAK-41 is shared with bemtpl97.

The register (register.json, 25 flags) has no flag on fremtpl2 or bemtpl97. The only insurance hits are pricing_game_2016_french_fleet (SPLIT-10/SPLIT-14 amendment due) and spanish_motor_insurance_2015_2018 (the "trivial" mechanism). Neither bears on this definition.

**A. The definition against its precedents**

1. Target is the rate ClaimNb/Exposure. ClaimNb leaves the frame and _clean checks that it rebuilds (MET-14, LEAK-10).
   CONSISTENT. Same as bemtpl97 (nclaims/expo, the same rebuild check; Lennart, 2026-11-06), australian_vehicle_insurance_2004_2005, frempl_french_motor_personal_line and pricing_game_2016_french_fleet (all 2026-11-06, metrics.md Cases).
   MET-14's per-contract clause (spanish_motor_insurance_2015_2018: a planned term of exactly one calendar year, known when written) does not apply. freMTPL2 has no planned term and no dates, and 1,224 rows are longer than a year.

2. Exposure is the weight scoring column, the metric's weight input and sample_weight, and never a feature (LEAK-41, MET-15).
   CONSISTENT. bemtpl97 does the same with expo (+0.0043, 17%). This matches the LEAK-10/LEAK-41 Cases row "time on risk cut short by the outcome" (leak_checks.md line 441) in its "denominator, cut not locatable" branch, as with bemtpl97, australian and spanish_motor_insurance_coverage_level_2022_2024.
   - frempl and pricing_game_2016 keep a start-known length (to 31 December) as a feature, because their dates locate the cut.
   - fremtpl2 has no dates, so no start-known part can be built. That fact sets it apart from those two (LEAK-41: "a part known at the start ships as its own column").
   - No rows are selected by the realized weight, as LEAK-41 requires. No row has zero exposure (minimum 1/366).

3. Metric is mean_poisson_deviance weighted by Exposure, origin source (MET-11).
   CONSISTENT. bemtpl97 is the same (a factor n/sum(expo) of about 1.12 against Henckaerts Eq. 5). Here the factor is 1.886 to 1.896 per fold, a per-fold constant, so models rank the same: MET-11's identity clause.

4. Rate shipped untransformed (CLEAN-16, amended 2026-11-06 on fremtpl2): CONSISTENT. A deviance-scored rate ships on the identity scale, as bemtpl97 does.

5. No cap on counts, exposures above one year kept (CLEAN-11): CONSISTENT with Lennart's CC of 2026-11-04 (records/fremtpl2.md line 106) and with bemtpl97 (nclaims 0 to 5, no cap). Under the weight these rows count up to 2.01 times. That follows from the 2026-11-04 fact that they record whole contract periods.

6. Not reopened by today's change: BonusMalus blanked in blocks 0-4 and kept in 5-6 (LEAK-10/LEAK-7 Cases row, leak_checks.md line 444, 2026-11-05), DrivAge 99 (CLEAN-10, cleaning_features.md line 337, 2026-11-05), IID split (2026-11-05) and the LEAK-9 protocol line (2026-11-05).
   - bemtpl97 keeps bm. The stated distinguishing fact is still in place: its source registers the risk factors at the start of the policy period.
   - The issue 7 and 8 numbers were measured on the count target with Exposure as a free feature. CHANGES.md already lists them for re-measurement; this is a size question, not a precedent one.
   - LEAK-41 now names "a sum of a group's exposures" as encoding the weight. This covers part of issue 8's record-structure signal (the summed exposure of identical records). The resolution of issue 8 (LEAK-9, protocol line) stays consistent.

**B. The calls the definition reverses**

B1. Andrej, CC 2026-10-20 (curation/records/fremtpl2.md lines 38-70): Exposure "a feature, not a divisor", capped at 1.
   REVERSED WITH A STATED FACT (CC 2026-11-06, Lennart, record line 128; REVIEW.md issue 6). Each of his reasons is answered:
   - "The contracted period is known at pricing." His own line concedes that a mid-year cancellation shortens it. The measurements came later (EV-1/EV-2, a measurement outranks a reading):
     - Exposure as a free feature beyond an offset is worth +0.0039 to +0.0045, about 25% of the skill.
     - A Poisson GLM gives log(Exposure) a coefficient of 0.641 (an offset is 1).
     - At quotation the free model was never better than the offset model.
   - "Dividing would inflate short policies' targets." Answered by the weight. MET-15's "Why": an unweighted fit gives 1.61 times the portfolio rate (0.1186 against 0.0738) and scores worse than a constant. With the weight, it does not inflate.
   - "Capped at 1." Already reversed 2026-11-04 (CLEAN-11, the two ranges of whole contract periods).
   This is a rule change made on purpose, not an exception. LEAK-41 (Must) is new, and the LEAK-10 Cases row "time on risk cut short" (Andrej, 2026-11-02, which named fremtpl2 as a departure) was amended in place with name and date, as principles.md asks.
   - The same reversal covers his line on australian_vehicle_insurance_2004_2005 (2026-11-02, "Exposure kept: consistent (fremtpl2, onlinenewspopularity)") and Myunghwan's bemtpl97 calls of 2026-10-23 and 2026-10-26. All were reversed the same day by the same rule, so like cases are decided alike.
   - Not a consistency failure, but worth telling Andrej: three of his exposure calls (fremtpl2 2026-10-20, the LEAK-10 row 2026-11-02, australian 2026-11-02) now stand superseded.
   - Side note: australian_vehicle_insurance_2004_2005/dataset.py (lines 127 and 279) cites "Andrej's call on fremtpl2 of 2026-10-20" as the precedent for keeping fixed claim amounts as recorded. That part of the call was never reversed, but fremtpl2 does not ship amounts (D12, 2026-11-06). The citation now points to an unshipped design. It still holds as a curator call; a wording check is enough.

B2. AI assessment, 2026-10-29 (record line 96): "approved task intent remains original uncapped ClaimNb with Exposure as a predictor". It called the annualised/capped form "an unapproved historical draft".
   REVERSED WITH A STATED FACT. It is an AI line, which ranks below a curator decision ("Who decides"). The 2026-11-06 CC names it and gives the same facts as B1. The 2026-10-29 line rejected the annualised draft as unapproved, not on its merits. Today's form is annualised but uncapped, and the curator has approved it. No conflict.

B3. The floor of 2026-11-04: min_prediction=1e-6 on the expected count (Lennart, bemtpl97 CC, records/bemtpl97.md line 76: "two orders below the smallest plausible mean"; carried to fremtpl2). Now 1e-4 claims per year.
   REVERSED WITH A STATED FACT, as an amendment. MET-13 was amended 2026-11-06 ("on the scale the metric scores": 1e-4 claims per year on fremtpl2 and bemtpl97). The same rationale is applied on the rate scale, identically in both datasets. This is not drift.
   - Task probe: share at the floor is 0.1% for LightGBM and 0.5% for random forest (bemtpl97 0.0%), reported as MET-13 asks.
   - For the metric auditor, not a precedent issue: with some predictions floored on the rate scale, "equals the source's count deviance times n/sum(Exposure)" holds only for unfloored predictions (the source has no floor).

**C. Findings (real, but not departures by a curator)**

C1. The LEAK-41 reporting clause is not met, by fremtpl2 or by bemtpl97.
   LEAK-41 (Must, leak_checks.md line 103): "For each suspect column the definition reports its gain on the declared metric with an L2 fit on the shipped scale and with the weighted actuarial fit, and decides on the worse."
   - fremtpl2's notes give only the Poisson/actuarial gain (+0.0039 to +0.0045; MET row +0.0040). There is no L2 figure and no probe 22 numbers.
   - Probe 22 measured both:
     - Poisson: +0.004806 (SD 0.0019); features predict Exposure at R² 0.1687.
     - L2: +0.006742 (SD 0.0042), the worse of the two, so the one LEAK-41 says to report.
   - australian_vehicle_insurance_2004_2005 and frempl_french_motor_personal_line report probe 22 / L2. bemtpl97 does not either.
   - The decision does not change (the column is out either way). This is a notes fix for both datasets alike, not a curator question. The 1/weight ceiling applies to a Gini metric (probe 22 text), so it is not needed here.

C2. The SPLIT-8 Cases row for fremtpl2 is stale and misquotes its number (splits.md line 257, dated 2026-11-04). It reads: "grouping by the inferred chains costs +0.00049 Poisson deviance and leaves the ranking unchanged".
   - +0.00049 (SE 0.00016) is the forward-by-block test, not the grouping cost: train on blocks 0, 2, 4, 5 and test on 1, 3, 6 (the definition's split note).
   - The grouping cost was 0.0002 to 0.0003 (REVIEW.md issue 7).
   - The reason given is the size of the gap, which SPLIT-4 and SPLIT-30 (both Must) bar. The 2026-11-04 consistency check flagged this, and the CC of 2026-11-05 (issue 7, B) replaced it with "prior work uses a random hold-out or a split grouped on identical factors; revisit if the chains become a recorded key".
   - The row was not updated. A later case citing it would inherit a reason the rules do not count ("a precedent that contradicts a rule is flagged, not followed"). Reflection prompt 1 below.

C3. Value precedent to re-read (for the task-probe agent and the mediator).
   - The 2026-11-04 panel judged "real and small signal (keep)" (TP-2) on numbers that included the Exposure leak and the unblanked BonusMalus.
   - Today's task probe flags no_signal (TP-1, TP-2): LightGBM r2 0.002, deviance 0.47283 against the dummy's 0.47838, about 1.2% on the declared metric.
   - bemtpl97, the same design, is not flagged: r2 0.015, about 3.1%.
   - The flag reads the r2-based "skill", not the declared deviance. This is not a departure, but the TP precedent for fremtpl2 now rests on superseded numbers and needs a fresh call.

C4. Minor: REVIEW.md's Outcome header still describes "the number of claims ... scored by the source's mean Poisson deviance" (the count target).

**D. Drift and third exceptions**

- Lennart on exposure: count with Exposure as a feature ("the metric is checked as declared", 2026-11-04), then parked (2026-11-05), then the rate with a weight (2026-11-06). The change comes with a new measurement and a new Must (LEAK-41), applied to all six insurance tables the same day. That is an amendment, not drift.
- Floor: one rationale, one amendment, applied identically to bemtpl97 and fremtpl2. No drift.
- No exception is recorded in this definition (LEAK-41 and MET-15 are Musts with no exceptions; MET-14 is followed), so no count toward a third exception.

**Reflection prompt 1 (C2), in the review-file issue shape**

**Should the SPLIT-8 Cases row for fremtpl2 carry the 2026-11-05 reason instead of the 2026-11-04 gap size?**

* **Problem:**
  - The row in splits.md (line 257) gives "grouping by the inferred chains costs +0.00049 Poisson deviance and leaves the ranking unchanged" as the reason for IID[^gap].
  - +0.00049 is the forward-by-block test (train blocks 0, 2, 4, 5; test 1, 3, 6). The grouping cost was 0.0002-0.0003.
  - Your call of 2026-11-05 (issue 7, B) rests on prior work (a random hold-out or a split grouped on identical factors), and the row does not say so.
  - All numbers were measured on the count target with Exposure as a feature.
* **Options:**

  | | Option | What it does | Pro | Con |
  |---|---|---|---|---|
  | a | Rewrite the row to the 2026-11-05 reason | the links are inferred between inferred years and are not the source's key[^key]; prior work uses a random or factor-grouped split; revisit if a key is recorded; +0.00049 labelled as the temporal-hold-out cost | a precedent that holds under the rules | a row edit in the knowledge file |
  | b | Keep the row as is | none | no edit | a gap-size reason the rules bar, a misattributed number |
  | c | Reopen issue 7 to group on the chains | ForcedGroupedFromTemporal | as nba_players_2016_2019, open_university (2026-10-21) | goes beyond prior work; a ruling on the key |

* **Recommendation:** (a). The definition already states the 2026-11-05 reason. Only the precedent row lags, and a stale row is what a later case would follow.

[^gap]: **SPLIT-4** and **SPLIT-30** (Must): the size of the gap never decides.
[^key]: **SPLIT-24** (Must): a key "constructed exactly from the data"; **SPLIT-8**.

**Precedents cited (with dates)**

- bemtpl97: rate nclaims/expo, expo as weight, floor 1e-4 (Lennart, 2026-11-06); bm kept (2026-11-05); IID, ForcedIIDFromTemporal, "treated alike" (2026-11-04).
- australian_vehicle_insurance_2004_2005, frempl_french_motor_personal_line, pricing_game_2016_french_fleet, spanish_motor_insurance_coverage_level_2022_2024: MET-14/MET-15/LEAK-41, 2026-11-06.
- spanish_motor_insurance_2015_2018: per contract stays, MET-14 clause, 2026-11-06.
- pricing_game_2017_french_mtpl: no exposure column, whole policy-years, 2026-11-06.
- leak_checks.md: line 103 LEAK-41; line 441 Cases row "time on risk cut short" (Andrej 2026-11-02, amended Lennart 2026-11-06); line 444 BonusMalus row (2026-11-05).
- metrics.md: MET-13 floor amendment and MET-14/15 rows (2026-11-06).
- splits.md: line 256 bemtpl97, line 257 fremtpl2.
- cleaning_features.md: line 193 CLEAN-16, line 337 CLEAN-10.

</details>

<details><summary>Advocate</summary>

**ADVOCATE OPENING BRIEF: fremtpl2, exposure re-review 2026-11-06, full tier**

Position: ship as defined. The target, the weight, the metric, the features and the split all stay. The evidence agents found real problems, but each one is a stale note, a missing reporting sentence or a protocol note. Each is fixed by editing text (curation_comments, accepted-warning reasons, a ScoringColumn description, REVIEW.md). None needs a change to the data pipeline. No agent refuted any validity claim (claim auditor: "No validity refutation. Today's design ... holds on every test").

1. The target, the weight and the metric are the source's own design, and they rank models exactly as the source does. (MET-14, MET-15, LEAK-41 Must; MET-11 Should)
   - Evidence:
     - The scorer equals the source's offset count deviance times n/sum(Exposure) to 1e-15 on every fold. The per-fold factors are 1.8956 / 1.8919 / 1.8864, so the ranking is the source's (claim auditor, item 3).
     - The source code fits glm(ClaimNb ~ ..., offset=log(Exposure)) and scores with the Poisson deviance (item 4).
     - The practitioner: "Nothing in the target, the weight or the metric: this is how I would set them up." The same setup is in scikit-learn's freMTPL2 example.
     - The blind reviewer reached the same answer on its own, without the notes ("EXPOSURE AS WEIGHT: CORRECT").
     - Fitting without the weight scores worse than the constant: 0.50043 against 0.47980, A/E 0.642 (practitioner). This is MET-15's reason, measured.
     - The floor of 1e-4 never binds on a sane model: 0.0% for LightGBM. An all-zero prediction still scores a finite 1.30 (item 5, MET-13).
     - The precedent checker found the definition "consistent" with bemtpl97 and four other insurance tables decided the same day. Each of the three reversed calls is reversed with a stated fact. There is no drift and no third exception. The register has no flag.
   - Answers: no agent objects to the core design. This point is the base the other points rest on.

2. Honest evaluation holds: no feature carries the realized weight. (P4; LEAK-41 Must, LEAK-10 Must, USE-6)
   - Evidence:
     - feature_columns are the 9 rating factors. Exposure is the weight only (claim auditor, item 2).
     - Probe 22: the features predict Exposure at R² 0.17. No feature's gain runs through Exposure above 2 SD under either the Poisson or the L2 fit. The largest are Region (+0.0010 to +0.0016) and DrivAge (+0.0006 to +0.0016) (column auditor).
     - Both are fixed at the quote, so LEAK-41 keeps them by their timing ("risk selection stays", USE-6).
     - No row is selected by its weight under IID (split auditor, item 4).
     - The gamer found one real exploit only: Exposure, or the summed Exposure of the twins, used as a feature (+0.008 to +0.010). The kit already blocks it ("Keep Exposure out of the features (already done)").
     - Reading the scoring column of the test rows is the protocol contract of every weighted task (LEAK-9; column auditor, problem 2). It is not a flaw of this definition.
   - Answers: the gamer's exploit table. P4 is the highest rank in play, and it holds.

3. The BonusMalus blanking is a settled leak fix, not a preparation defect. (LEAK-10 Must, LEAK-7 Should; P4 over P6)
   - The blind reviewer and the gamer call it a defect and ask for a re-ingest (+0.040 if restored). Neither had the notes.
   - The gamer's own finding, "kept exactly for IDpol >= 5,000,006 ... blanks for every IDpol <= 4,189,196", is the definition's block mask (dataset.py line 268, `mask(block.le(LAST_LATE_BONUS_MALUS_BLOCK))`). It is not a parsing failure.
   - The curator's call of 2026-11-05 (issue 5, B) rests on measurements:
     - In blocks 0-4 the coefficient is frozen from block 0 to 1, 94.5% unchanged, where the French system lowers it after every claim-free year.
     - In those blocks claimants pile on the first malus step, 62-63, so the value looks recorded after the row's own claims.
     - In blocks 5-6 it follows the previous year's claims, as a start-of-year value does, and it stays.
     - It is distinguished from bemtpl97 by a stated source fact: "risk factors are registered at the start of the policy period".
   - A post-outcome value restored would of course lower the deviance. The +0.040 measures the leak, not lost honest signal.
   - Rank: P4 (validity) outranks P6 (value). The cost of the fix (honest skill 0.064 down to 0.023, practitioner) is the price of honesty. It is not a reason to restore the column ("a real task carries ... it does not carry a leak").
   - Concession: the evidence that the value is post-outcome is a measurement of distributions, not a statement by the source. Today's change does not reopen issue 5 (column auditor; precedent checker, A6).
   - Mildest remedy for the confusion: the practitioner's sentence in fit_reason, that the blanking, not option A, took the skill from about 0.064 to 0.023.

4. The IID split stays. The new gap is one 20-row fleet, and the gap size never decides the split. (SPLIT-4 / SPLIT-30 Must; SPLIT-8; issue 7 settled 2026-11-05)
   - Evidence:
     - The IID-vs-grouped gap is +0.0008 to +0.0016. Of it, 94-102% comes from one profile: 20 rows, 77 claims in 4.63 years.
     - Without that profile the gap is -0.00001 to +0.00015 (split auditor) and -0.00005 to -0.00021 (claim auditor).
     - An explicit memorizer gains nothing: the best blend scores 0.46823 against LightGBM's 0.46813; twins' leave-one-out changes the score by +0.0001.
     - The record-count exploit is +0.0005, below the gamer's noise floor of 0.0006.
     - The ranking, LightGBM over the GLM, is the same under every split.
     - The forced-temporal cost is +0.0009, half of it the same profile.
   - Rules: SPLIT-4 and SPLIT-30 bar deciding a split on the size of its gap. The curator's 2026-11-05 reason (prior work uses a random or a factor-grouped split) is untouched.
   - Mildest remedy: the split auditor's option (a), one sentence that names the profile and its effect. Grouping on identical factors (option b) is a weighing call for the curator. It is not needed for validity.

5. The signal is real. The no_signal flag comes from an R²-type skill. (TP-1 Must: a flag is a question; TP-2 Should)
   - Evidence:
     - On the declared deviance a weighted Poisson LightGBM beats the constant on every fold: by 0.0109 / 0.0127 / 0.0096, D² about 2.3% (claim auditor, item 14).
     - The practitioner measured A/E 1.000 and an exposure-weighted Gini of 0.195, against 0.2-0.3 for published MTPL frequency models.
     - The probe itself says "beats the dummy on 100% of the splits".
     - A Poisson count has R² near 0.01 by nature.
   - Precedents: forest_fires, kept at R² 0.013 under TP-2; clock_protein_toxicity, kept.
   - Remedy: record in REVIEW.md why the flag is overruled.

6. The cleaning choices the blind reviewer questions are settled, and they help an honest model. (CLEAN-11, CLEAN-10; P7)
   - Not capping: ClaimNb is not capped at 4 and Exposure is not capped at 1 (CLEAN-11, 2026-11-04: whole contract periods). The gamer measured that capping in training hurts: 0.46909 against 0.46850; capping the claims only, 0.46915; dropping ClaimNb >= 5, 0.46995.
   - The VehAge 99/100 values (48 rows) and the block-0 DrivAge 99 values (66 rows) are made missing as default codes, and the notes document it (CLEAN-10, issue 9 settled; claim auditor, item 24 holds).
   - The 677,991 rows match the CASdatasets 1.2-1 documentation (blind reviewer).
   - These are P7 quality points. They are documented and do not change what the target means.

7. Concessions. Each is real; each is fixed by text, not by changing the data.
   a. LEAK-41 reporting clause (Must, its reporting part). Add one sentence to the Exposure bullet with:
      - Poisson gain +0.0082 on the declared scale;
      - L2 gain +0.0075 on the full data (+0.0067 in probe 22);
      - the Exposure-alone score, 0.47114 against the constant's 0.47929;
      - probe 22's R² 0.17, and that no feature carries the weight above noise.
      The decision does not change: the column is out either way. bemtpl97 needs the same sentence (precedent checker, C1).
   b. Stale accepted-warning reasons:
      - conflicting duplicates: now 8,128, not 520;
      - exact copies: now 181,197, and most feature-identical groups look like one policy-year split into records.
      Rewrite both with today's counts. The harm is measured as small (point 4).
   c. Stale numbers in "Copies kept".
   d. Count-scale numbers and old-target numbers given without a label. One clause fixes it: the declared score is 1.891 times the count deviance.
   e. The "seven policies, 72 claims over 3.63 years" wording: those are the 19 profile rows, not the seven policies.
   f. Exposure share "21-30%": it is 43% on the declared scale, so state that or drop the share.
   g. The Exposure description: in blocks 5-6 the short records are mostly cut at a calendar date (block 6 stops at 0.74 of a year).
   h. The SPLIT-8 Cases row in splits.md misquotes the +0.00049 (precedent checker, reflection prompt 1, option a).
   i. Protocol and README note: methods must receive sample_weight, and one that ignores it scores worse than the constant.
   j. The record's latest Assessment line and the tag "Two-Regime Zeros" predate today.
   Why these do not block shipping:
   - They are independent failures, not conflicts.
   - The one Must among them (LEAK-41's reporting clause) is fully met by the mildest step of the remedy ladder, fixing the definition's notes.
   - None touches validity: the claim auditor found no refutation of the target, the weight, the metric or the leak decision.

Judgment record as I argue it:
- Verdict: ship after text changes. The data, the target, the weight, the metric and the split stay as defined.
- Validity:
  - LEAK-41 holds; its reporting part is to be completed.
  - LEAK-10 holds: the BonusMalus blanking, issue 5, settled.
  - SPLIT-8 holds, with SPLIT-4 and SPLIT-30 holding: IID, plus a fleet note.
  - MET-14 and MET-15 hold.
- Value: TP-2, a small real signal (deviance skill 0.0096-0.0127 on every fold); the no_signal flag is overruled with its reason.
- Quality: CLEAN-11 and CLEAN-10 hold as settled; the notes need refreshing.
- For the curator: the split auditor's option (b), grouping on identical rating factors, is a weighing call. My recommendation is option (a), the note.

</details>

<details><summary>Critic</summary>

**fremtpl2: critic's opening brief (exposure re-review, 2026-11-06, full tier)**

My position is that fremtpl2 should ship only after changes. None of my points justifies excluding it. Today's design holds on every test the panel ran: the target ClaimNb/Exposure, Exposure used only as the weight, a deviance that ranks models exactly as the source's offset deviance does (ratio 1.886-1.896 per fold), and the 1e-4 floor. My case is about two things. First, a settled split decision now rests on a fact that one entity refutes. Second, the Must reporting duty of LEAK-41 is unmet, and much of the text describes a frame that no longer ships.

1. One 20-row entity produces the whole gap between the IID and the grouped split. It refutes the fact issue 7 was settled on. (P4; SPLIT-29 and LEAK-17, both Must, put to the curator as a question under SPLIT-30.)
   - **Problem:** Issue 7 option B, as implemented, kept IID because "the entity carries almost none of the label (pair correlation 0.017, so SPLIT-29 does not fire)". One profile breaks that.
     - The profile: power 4, B1, Regular, area D, density 824, Languedoc-Roussillon, BonusMalus blank, car/driver 12/52, then 13/53.
     - It has 20 rows, 77 claims and 4.63 years, a rate of 16.6 claims a year against a portfolio rate of 0.07.
     - Wüthrich and Merz suspect it is one driver or a rental fleet.
   - **Effect:**
     - Under IID its rows fall 6/7/7 across the folds. LightGBM predicts 3.8-17.2 claims a year for its test rows from their training copies. Grouped, it predicts 0.073-0.078.
     - LightGBM's grouped-minus-IID gap is +0.0008 to +0.0017. That is 7-15% of its skill over the constant.
     - 94-102% of that gap sits in these rows. Without them the gap is -0.0002 to +0.00015.
     - So the only memorization the shipped split rewards is recognising this one entity. Part of the forced-temporal cost (+0.0009) comes from the same profile; without it the cost is +0.00046.
   - **Evidence:** split_auditor item 2 and claim_auditor item 12, measured independently and in agreement. Neither found any gain for a twin memorizer outside the fleet (claim_auditor +0.0001; split_auditor best blend 0.46823 against 0.46813).
   - **Strength of the case:** SPLIT-29 needs "many rows", and 20 rows of 677,991 is not many. SPLIT-24 bars grouping on a hash of the feature vector. So this is not a clear Must breach. But the stated fact behind the IID exception no longer holds, and the principles require such a decision to be put back to the curator ("a documented decision is not a correct one").
   - **Remedy:** Reopen issue 7 with this fact. Mildest acceptable fix:
     - correct the issue-7 rationale in REVIEW.md and the notes;
     - add one sentence to splits_comment and the "Counts of 5 to 16" bullet: the profile, its 77 claims, and that the IID score depends on how its 20 rows fall.
     - Alternative for the curator: group on the identical shipped rating factors, as Schelldorfer and Lorentzen-Mayer do (splits.md "Composite keys"). It costs nothing elsewhere: 488,666 groups, folds of 224,778-226,838 rows.
     - I do not ask to drop the rows; that would undo the keep of 2026-11-04.

2. The reporting clause of LEAK-41 is not met. (P4; LEAK-41, Must.)
   - **Problem:** LEAK-41 asks the definition to report, on the declared metric, the gain from an L2 fit and from the weighted actuarial fit, to decide on the worse, and to state the score of 1/weight alone as the ceiling a leak would reach. The notes give only a count-scale offset gain (0.0039-0.0045) and nothing from probe 22.
   - **Effect:** A reader cannot see on the shipped metric how large the removed leak was, or that no shipped feature carries it.
   - **Evidence:**
     - Claim auditor item 9 (full data): Poisson +0.0082, L2 +0.0075. Exposure alone scores 0.47114 against the constant's 0.47929, which is 74% of what the 9 honest features reach.
     - Probe 22 (50k cap): Poisson +0.0048, L2 +0.0067. The features predict Exposure at R² 0.17. No feature's gain runs through Exposure above 2 SD; Region and DrivAge sit at 1.1-1.4 SD (column auditor).
     - The precedent checker found the same gap in bemtpl97 (C1).
   - **Strength of the case:** The precedent checker reads the ceiling as needed only for a Gini metric. The rule's text does not say so.
   - **Remedy:** A note, not a design change. One sentence in the Exposure bullet with these numbers, naming Region and DrivAge as the probe's top features. Both are known at the quote and stay (USE-6). The same fix goes into bemtpl97.

3. Both accepted duplicate warnings are justified by numbers and a reading that today's frame refutes. (P4/P6; EV-7, with LEAK-17 behind the reading.)
   - **Problem:**
     - The conflicting-duplicates reason says 520 rows. With Exposure no longer a feature, the check sees 8,128 rows (1.2%).
     - The duplicate-rows reason says "each copy is a distinct policy ... the repetition is the portfolio". The check now counts 181,197 exact copies (26.7%). 327,862 rows (48.4%) sit in 138,537 groups with identical features, and 92.9% of those groups sum to at most 1.01 years. That is the signature of one policy-year split into records, as the notes themselves say ("renewals during the year recorded as two records"). 66.5% of the linked pairs straddle the folds.
   - **Effect:** Small on the score:
     - a twin memorizer gains +0.0001;
     - group size and the siblings' exposure, without the row's own Exposure, gain 0.0004 (noise);
     - the transductive count over train and test gains +0.0005.
     - But the acceptance argues from a fact the data contradicts.
   - **Evidence:** claim_auditor items 17, 18 and 25; task_gamer findings 1 and 3; split_auditor item 4.
   - **Remedy:** Rewrite both accepted_check_warnings with today's counts and the split-records reading, citing the measured harm above.

4. The value flag is left unanswered. (P6; TP-1 Must, TP-2 Should.)
   - **Problem:** The task probe flags no_signal (TP-1, TP-2), and REVIEW.md does not say why it is overruled. The 2026-11-04 call "real and small signal (keep)" rested on numbers that included the Exposure leak and the unblanked BonusMalus (precedent checker C3).
   - **Effect:** The flag itself is an artefact: the probe reads an R²-type skill. But the honest headroom is thin, and readers should see it:
     - deviance skill over the constant is 0.0096-0.0127 per fold (about 2.3% D², A/E 1.00, Gini 0.19);
     - a random-column control moves fold scores by up to about 0.0006 (task gamer);
     - strong methods will differ in the fourth decimal (blind reviewer concern 3).
   - **Evidence:** probes/task.txt; claim_auditor item 14; domain_practitioner measurements; task_gamer noise reference.
   - **Remedy:** A recorded TP call in REVIEW.md and fit_reason. It should give the deviance skill per fold, explain why the R² flag misleads for a Poisson frequency, and attribute the drop from about 0.064 to about 0.023 to the BonusMalus blanking, not to option A. Check against tuned methods when they exist (TP-1). This is not grounds to retire (TP-2).

5. The task works only if the method uses the weight, and the definition does not say so where a benchmarker will look. (P6; MET-15, Must, on its consequence.)
   - **Problem:** MET-15 makes Exposure the sample_weight. A method that cannot take a weight does not just score worse; it loses to the constant.
   - **Effect:** An unweighted LightGBM scores 0.50043 against the constant's 0.47980 (fold 0, A/E 0.64). The unweighted constant scores 0.49892 against 0.47929 for the weighted one. A leaderboard that mixes weighted and unweighted methods ranks weight support, not modelling.
   - **Evidence:** domain_practitioner Q4 and gap 2; claim_auditor item 6.
   - **Remedy:** A note. One sentence in fit_reason or the task description: the task needs the sample weight, a method that ignores it scores worse than the constant rate, and results should record whether a method used it.

6. Many numbers in the notes are stale, on another scale, or wrong. (P7 and the writing rules; EV-7.)
   - The declared score is 1.891 times the count deviance, but the notes mix in, without a label:
     - count-scale numbers (0.2534, 0.0012, 0.0021, 0.0008);
     - old-target numbers from runs with Exposure as a feature (0.23316 against 0.23267, +0.00049; 0.0821 against 0.0819; 0.2327 against 0.2435).
   - Restated on the shipped metric:
     - the forced-temporal cost is +0.0009 (+0.00046 without the profile);
     - the renewal flags are worth about 0.0010, and the full oracle 0.0015-0.0025 (split_auditor items 3 and 5).
   - "21-30% of LightGBM's gain" for Exposure is 43% on the shipped baseline (claim_auditor item 8).
   - The "Copies kept" counts include Exposure as a column. The rows in feature-identical groups now number 327,862 (claim_auditor item 25).
   - "Seven of the eight policies ... 72 claims over 3.63 years" is wrong: the seven have 66 claims over 1.38 years, and 72 claims over 3.63 years belong to the 19 profile rows (claim_auditor item 22).
   - The Exposure scoring-column description, "shorter when the policy ended early, often after a claim", misses how blocks 5-6 are cut. There Exposure is cut mostly by a date: block 6 never exceeds 0.74 years, and 99.8% of block 5 is a partial year (split_auditor item 4).
   - **Remedy:** Restate these numbers on the declared metric. Add one clause dating the older numbers ("before 2026-11-06, on the count target with Exposure a feature"). Add one clause on date-cut exposures in blocks 5-6.

7. The surrounding records lag today's design. (Principles, "Keeping the rules current"; SPLIT-4 and SPLIT-30 for the Cases row.)
   - The SPLIT-8 Cases row for fremtpl2 (splits.md line 257) gives "grouping by the inferred chains costs +0.00049" as the reason for IID. That number is the temporal hold-out, not the grouping cost. The size of a gap is a reason SPLIT-4 and SPLIT-30 bar. A later case would follow this row (precedent checker C2).
   - REVIEW.md's Outcome header still describes the count target.
   - The record's latest Assessment (2026-11-04) says "realised exposure kept, 10 features, three Must issues open".
   - The tag "Two-Regime Zeros" comes from the amount task that D12 keeps out.
   - **Remedy:**
     - rewrite the Cases row to the 2026-11-05 reason (precedent checker reflection prompt 1, option a);
     - update the Outcome header;
     - add an Assessment line for today's change and review the tag.

Not raised: the BonusMalus blanking, which is settled in issue 5 (LEAK-10) and not reopened by today's change. Both outside reviewers took it for a preparation defect. The task gamer measured a restore at 0.040 and guessed at "a parsing step that failed". It is a deliberate curator decision, and the size of a gap does not override a leak rule. The fact that two independent readers misread it argues only for keeping it prominent, which task_summary.known and changes already do.

</details>

<details><summary>Advocate rebuttal</summary>

**ADVOCATE REBUTTAL: fremtpl2, exposure re-review 2026-11-06**

Summary: the critic and I agree on the verdict ("ship only after changes"; "None of my points justifies excluding it"). I concede six of the seven points in full. I dispute one point only in its framing: what the 20-row fleet refutes. Every remedy left on the table is text. None changes the target, the weight, the metric, the features or the split.

1. The 20-row entity and issue 7: conceded in part, disputed in part.
   - Conceded:
     - The fact is new and measured twice: split_auditor item 2 and claim_auditor item 12.
     - Issue 7 never weighed it, and SPLIT-30 (Must) says a probe hit is a question. It goes to the curator.
     - The note in splits_comment and in the "Counts of 5 to 16" bullet is required, not optional.
   - Disputed: the claim that it "refutes the fact issue 7 was settled on".
     - Issue 7 concerns another entity: the inferred next-year chains (REVIEW.md lines 197, 210, 1065: "The links are inferred ... between blocks"). Its fact is the pair correlation of claims along those links, 0.017. Nothing today measures that again or contradicts it.
     - The fleet is a separate entity, rows with identical rating factors. It adds a new fact beside the old one; it does not overturn the old one.
     - The critic's own rule reading stands: SPLIT-29 needs "many rows", and 20 of 677,991 are not many. SPLIT-24 (Must) lets us group only on a true id or a key "constructed exactly from the data". An identical profile is a composite key whose status as one entity rests on one inference (Wüthrich and Merz suspect one driver or a fleet). So no Must breach is shown.
     - The ranking (LightGBM over the GLM) is the same under every split. The gap is 0.0008-0.0017, and SPLIT-4 and SPLIT-30 bar deciding on gap size.
   - What follows: add an issue-7 row ("a 20-row profile with 77 claims makes the IID-vs-grouped gap") with the split auditor's options (a) note and (b) group on identical factors. I recommend (a). Correct the rationale's wording in REVIEW.md only so it does not suggest that the 0.017 covers the fleet.

2. The LEAK-41 reporting clause: conceded in full, including the ceiling.
   - The rule's text is general: "it states the score of 1/weight alone as the ceiling a leak would reach". I find no Gini-only limit in it. The precedent checker's reading is narrower than the rule, and rules win over readings.
   - The sentence should give:
     - Poisson +0.0082 and L2 +0.0075 (full data), or +0.0048 and +0.0067 (probe 22), deciding on the worse;
     - the ceiling: Exposure alone scores 0.47114 against the constant's 0.47929;
     - R² 0.17, with Region and DrivAge at 1.1-1.4 SD, both kept under USE-6.
   - My opening brief (point 7a) already listed these numbers.
   - The same fix goes into bemtpl97. This is the mildest step of the remedy ladder and fully meets the Must.

3. The stale accepted-warning reasons: conceded.
   - The new counts are 8,128 conflicting rows and 181,197 exact copies. The "distinct policy" reading is contradicted by the 92.9% of groups that sum to at most 1.01 years.
   - The measured harm is noise-level: +0.0001 for the twin memorizer, 0.0004 for the siblings, +0.0005 for the transductive count. So the warnings stay accepted, with the reasons rewritten as the critic proposes.

4. The value flag: conceded.
   - The TP call belongs in REVIEW.md and fit_reason. It should give:
     - the per-fold deviance skill, 0.0109 / 0.0127 / 0.0096;
     - D² about 2.3%, A/E 1.00 and Gini 0.19;
     - why the R² flag misleads for a Poisson frequency;
     - that the drop from 0.064 to 0.023 comes from the BonusMalus blanking (issue 5), not option A.
   - The thin headroom is a fact readers should see. Two qualifications:
     - The honest gain is 16-21 times the gamer's noise reference of 0.0006, so the folds tell models apart. TP-2 says a small real signal is no reason to retire, and the critic agrees.
     - The TP-1 recheck with tuned methods is a later step, not a condition for shipping.

5. A method must use the weight: conceded.
   - Unweighted, LightGBM scores 0.50043 against the constant's 0.47980. Name the requirement in fit_reason or the task description, and record whether each method used the weight.
   - This is the consequence MET-15 (Must) intends: a model that ignores time insured misprices the book (A/E 0.64). So it is a note, not a design change.

6. Stale, unlabelled and wrong numbers: conceded.
   - The fixes, as listed:
     - restate the numbers on the declared scale (forced-temporal +0.0009, or +0.00046 without the profile; renewal flags about 0.0010, oracle 0.0015-0.0025);
     - the Exposure share is 43%, not 21-30%;
     - "Copies kept": 327,862 rows in feature-identical groups;
     - the seven policies have 66 claims over 1.38 years;
     - add the date-cut clause for blocks 5-6 to the Exposure description;
     - add one dating clause for the older numbers.
   - These are P7 and writing fixes.

7. Records that lag today's design: conceded.
   - The fixes:
     - rewrite the SPLIT-8 Cases row (splits.md line 257) to the 2026-11-05 reason; option (a) of the precedent checker. The row today cites a gap size, which SPLIT-4 and SPLIT-30 bar, and calls the temporal hold-out a grouping cost;
     - update REVIEW.md's Outcome header;
     - add a 2026-11-06 Assessment line to the record;
     - review the tag "Two-Regime Zeros".

On BonusMalus: the critic and I agree. The blanking is settled (issue 5, LEAK-10), and the restore gain of 0.040 measures the leak, not lost signal.

Joint position for the mediator: ship after text changes 1(a), 2-7. The one curator question is issue 7's new row, (a) note against (b) grouping on identical factors. My recommendation is (a). Nothing in either brief calls for changing the data, the target, the weight, the metric or the feature set.

</details>

<details><summary>Critic rebuttal</summary>

**fremtpl2: the critic's rebuttal (exposure re-review, 2026-11-06)**

**Where we stand:** we agree on the verdict: ship after text changes, with the data, target, weight, metric and features left as they are. The advocate's point 7 concedes my points 2, 3, 5, 6 and 7 in substance, and my point 4 mostly, through its own point 5. One dispute is left, on the split (advocate's point 4). I narrow my own claim there and keep only one ask: issue 7 goes back to the curator with the new fact, not just a note.

**Point 1 (the target, weight and metric are the source's design): concede.** The scorer equals the source's offset count deviance times n/sum(Exposure) to 1e-15 on every fold (claim auditor, item 3). An unweighted fit loses to the constant. The floor never binds. The precedent checker finds the definition consistent. MET-11, MET-13, MET-14 and MET-15 hold.

**Point 2 (no feature carries the realized weight): concede.** In probe 22 and the column auditor's extension to all 9 features, no feature passes 2 SD, under the Poisson fit or the L2 fit. Region and DrivAge are fixed at the quote, so they stay (LEAK-41, USE-6). The gamer's twins' summed Exposure is a feature a participant builds, not one that ships. LEAK-41 names that kind of feature as off limits, and the kit already blocks it. What remains is the reporting clause, which point 7a concedes.

**Point 3 (the BonusMalus blanking is settled): concede the conclusion, dispute one sentence.**

- Issue 5 stands, and today's change does not reopen it. I did not raise it either.
- The sentence I dispute: "The +0.040 measures the leak, not lost honest signal." That claims more than the evidence shows.
  - Issue 5 rests on "likely, not shown" (EV-6). No statement from the source dates the value. The finding is a distribution footprint, as the advocate concedes.
  - The gamer's restore is one number covering blocks 0-4. It cannot separate the post-claim part from what a quote-time coefficient would legitimately give.
  - The earlier panel's number is +0.0127 on the count scale in blocks 0-3, about 0.024 on the rate scale. It was measured with Exposure as a feature.
  - The rule is untouched: LEAK-10 is a Must, the size of a gap never decides, and the curator's B stands.
- Remedy: the notes and fit_reason keep "likely" wording. They should not present 0.040 as the size of the leak. The practitioner's sentence on 0.064 down to 0.023 is fine, as long as it is worded as the cost of the blanking.

**Point 4 (the IID split stays; the gap is one fleet; gap size never decides): partly concede, keep one ask.**

What I concede:
- The curator's resolution of 2026-11-05 (REVIEW.md issue 7) rests on prior work: "prior work gives no reason to group". It does not rest on the correlation of 0.017 that option B listed. My opening wrongly treated that fact as the decisive reason.
- SPLIT-29 needs "many rows", and 20 of 677,991 is not many. So no Must forces a re-split.
- The size of the gap decides nothing (SPLIT-4, SPLIT-30), whether for grouping or against it.
- The explicit memorizer gains nothing outside the fleet. The ranking is the same under every split.

What I dispute: that option (a), a note, closes the issue. The reason is the prior-work reason itself.
- The 2026-11-05 survey in REVIEW.md lists Schelldorfer (2021) and Lorentzen and Mayer, who use an 80/20 split grouped on identical rating factors. They group because ignoring the groups lifts LightGBM's pseudo-R² from 5.0% to 6.0%. So one strand of the prior work the curator relied on does group, on exactly this key.
- Today's measurement shows what that grouping guards against here:
  - 94-102% of the IID-vs-grouped gap sits in one profile: 20 rows, 77 claims, 16.6 claims a year.
  - Under IID, LightGBM predicts 3.8-17.2 claims a year for its test rows. Grouped, it predicts 0.073-0.078.
  - Sources: split auditor item 2, claim auditor item 12.
- That is a new fact about the reason the decision rests on, not a size. The principles require a call whose evidence has moved to be put back to the curator. They do not say the AI settles it ("surface it, do not override it").
- SPLIT-24 does not bar the factor key. It allows "identical values in the columns that define the entity" (splits.md, "Composite keys"). What it bars is a hash standing in for an unknown entity. Which of the two the factor key is here is the curator's ruling.

Remedy, still the mildest:
- Option (a) now: one sentence in splits_comment and in the "Counts of 5 to 16" bullet, as the advocate also proposes.
- Issue 7 reopened as a question, with this fact added and options (a) and (b) set out for the curator. This is not a demand to re-split.

**Point 5 (the signal is real): concede, with one addition to the remedy.**

- The deviance skill is 0.0096-0.0127 on every fold, and TP-2 keeps a small real signal.
- The recorded TP call should also give the resolution. Per fold, a random-column control moves scores by up to about 0.0006 (gamer), so strong methods will differ in the fourth decimal. That is a fact for readers of the leaderboard, not a reason to retire (TP-1, TP-2).

**Point 6 (cleaning choices are settled): concede.**

- CLEAN-11: capping in training hurts (0.46909 against 0.46850; dropping counts of 5 or more, 0.46995).
- CLEAN-10: the default codes are set to missing and documented.
- Both are P7 and settled.

**Point 7 (concessions a to j): agreed.** These match my points 2, 3, 5, 6 and 7, and the remedies are the same. Two additions:
- (a) LEAK-41's text asks for the ceiling score of 1/weight alone, with no exception for a deviance metric. The advocate includes it (0.47114 against 0.47929), so we agree; the precedent checker's reading that it applies only to Gini should not be followed.
- (h) The SPLIT-8 Cases row should also drop the gap-size reason, not only correct the number, since SPLIT-4 and SPLIT-30 bar that reason.

**Joint judgment record as I would now put it:**

- Verdict: ship after text changes.
- Validity:
  - LEAK-41 holds; its reporting clause is to be completed with the L2 gain, the gain on the declared metric and the 1/weight ceiling.
  - LEAK-10 holds (issue 5), in "likely" wording.
  - MET-14 and MET-15 hold.
  - SPLIT-8 holds as IID with a fleet note. Issue 7 goes back to the curator as a question on the factor-grouped option (b), with today's fact: the gap is one 20-row profile, and that profile is what the prior-work grouping guards against.
- Value: TP-2 keeps it. The no_signal flag is overruled, with the deviance skill and the per-fold noise of about 0.0006 recorded.
- Quality: all the stale numbers, scales, warning reasons, descriptions and record lines are restated.

</details>
