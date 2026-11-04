---
unique_name: fremtpl2
name: freMTPL2
checked_by:
- Myunghwan
- Lennart
suggestion: 'Yes'
priority: 3
original_source: Other
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

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 4: the documented French MTPL portfolio for claim frequency, an insurer's pricing task, and insurance is thin. The earlier plain `Yes` was set by the older AI pass (no curator name in `checked_by`), so it is put back to `TBD -> Yes` for the curator to confirm.
- Source: CASdatasets R package (Dutang and Charpentier), `freMTPL` page (https://dutangc.github.io/CASdatasets/reference/freMTPL.html): "risk features are collected for 677,991 motor third-part liability policies", "The period is approximately 2011-2013", source "Unknown private insurer". Two tables joined on `IDpol`: `freMTPL2freq` (677,991 x 12: `IDpol`, `ClaimNb`, `Exposure`, `Area`, `VehPower`, `VehAge`, `DrivAge`, `BonusMalus`, `VehBrand`, `VehGas`, `Density`, `Region`) and `freMTPL2sev` (26,444 claims: `IDpol`, `ClaimAmount`). The Kaggle link in `source_links` is a re-upload (karansarpal); the first publication is CASdatasets (the year it entered the package was not confirmed, so `year` stays empty).
- Use case: an insurer sets the premium of a motor TPL policy at underwriting from the rating factors (claim frequency per year of exposure, Noll, Salzmann and Wuthrich, "Case study: French motor third-party liability claims", SSRN 3164764); fit direct for the frequency target `ClaimNb` with `Exposure`; regime IID, one row per policy-period and no date, but see the risks.
- Siblings and duplicates: `bemtpl97` (Belgian MTPL, CASdatasets, a different portfolio: no duplicate, PROV-7); no other freMTPL record (grep over `curation/records/` for fremtpl, MTPL, CASdatasets, ClaimNb). External collections: CASdatasets, OpenML (freMTPL2freq / freMTPL2sev uploads); used in Deprez, Verbeke and Verdonck, "Is TabPFN the Silver Bullet for Insurance Pricing?" (arXiv 2605.22892, 2026: TabPFN vs GLM and XGBoost on two public MTPL sets, frequency and severity).
- Papers and pages: CASdatasets manual https://cas.uqam.ca/pub/web/CASdatasets-manual.pdf; Noll et al. (doi:10.2139/ssrn.3164764); Denuit, Charpentier and Trufin 2021 (doi:10.1016/j.insmatheco.2021.09.001); Miljkovic and Fernandez 2018 (doi:10.3390/risks6020057); Pocuca et al. 2020 (doi:10.1016/j.insmatheco.2020.06.004); arXiv 2605.22892.
- Metric: no competition; the actuarial case study (Noll et al.) compares frequency models by the out-of-sample Poisson deviance with `Exposure` (read from the abstract and the papers that follow it, the full text not read here); likely a deliberate choice (MET-5), inputs `Exposure` (ships). Severity would be a gamma deviance on `ClaimAmount`. To confirm in /add-dataset; else the fallback.
- Risks for /add-dataset: choose the target (`ClaimNb` frequency with `Exposure`, or severity from the join, one `_sev` dataset); `ClaimNb` is capped and `Exposure` above 1 is truncated in the case study's cleaning (check); identical risk profiles recur across rows (the actuarial literature builds a group id from equal features before splitting), so check a grouped split (SPLIT, LEAK); some `ClaimAmount` values are fixed IRSA-IDA convention amounts ("Some claim amounts of `freMTPL2sev` are fixed claim amounts based on the French IRSA-IDA claim convention").
- Priority: gap + (insurance thin), use case + (pricing named by the case study), source + (CASdatasets page and papers), shape + (678k rows, mixed types), risk - (target, exposure and repeated profiles to settle).

freMTPL2 is the well-known French Motor Third-Party Liability insurance dataset from CASdatasets, a standard actuarial benchmark. The canonical predictive task is claim frequency modelling (Poisson/count regression of claim number against exposure and policy features), a genuine real-world tabular regression/count task that is widely used and adequately sized (hundreds of thousands of policies). It maps cleanly to the criteria: unique original source, real predictive target, representative tabular data, no ethical issue. Note it comes as freq + severity tables (freMTPL2freq / freMTPL2sev) so a human should confirm which table/target is used and how exposure is handled; an IID split is standard.

---

Also see https://arxiv.org/abs/2605.22892 and https://cas.uqam.ca/pub/web/CASdatasets-manual.pdf

CC (2026-10-28, Myunghwan): Hold freMTPL2, not reject it. Missing timing information prevents a defensible prediction point and split, and the released fields do not support a trustworthy contract/group-level evaluation. Preserve the candidate and completed evidence; reopen only if reliable timing and a defensible observation/linkage unit become available, followed by curator reconsideration.

**Assessment (AI, 2026-10-29):** Preserve the applied hold as TBD -> Yes with DF: Suspended, not No or scientific acceptance. Every released IDpol is distinct; identical rating profiles do not establish contract identity. The requested zero/non-zero association check found weak positive within-profile dependence (pair correlation about 0.017; 131 both-positive pairs versus 81.79 expected under the stated profile-size-stratified null), not a causal linkage finding. The approved task intent remains original uncapped ClaimNb with Exposure as a predictor and source count Poisson deviance. The annualized/capped implementation is an unapproved historical draft, omitted from this PR along with its v2 pointer; it is not a qualified version of the approved count task. The official active reservation was released. No automatic restart, refit, build or acceptance follows the hold.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `eumtpl` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-04, Lennart): `Yes`, added like beMTPL97 rather than held ("dont hold, add them and we can review them case by case"; on beMTPL97: "do (a) and ship both"): IID with the `ForcedIIDFromTemporal` tag (SPLIT-8). `eumtpl` is screened later ("we can screen that task later, this is fine for now without it, if it is a duplicate raise this again").

**Assessment (AI, 2026-11-04):** review panel (none): built through /add-dataset steps 0-6, no panel. 677,991 policies, the 2022 CASdatasets counts, `VehAge` 99/100 missing; `dataset check` passes and the probes flag nothing. Consecutive `IDpol` blocks look like consecutive years (48-60% of rows reappear one block later); the open questions are in the folder's REVIEW.md.

CC (2026-11-04, Lennart): IID with the Forced tag stays ("follow the recommendation"; the inferred links between `IDpol` blocks are not the source's key and change the score by nothing), and the claim counts are the 2022 CASdatasets version ("use the newer version"). The metric is checked as declared.

CC (2026-11-04, Lennart): resolved as implemented: exposure above one year is kept (two policy ranges recording whole contract periods) and the counts of 5 to 16 are kept uncapped (seven of the eight are one profile); both are named in the definition's notes.

**Assessment (AI, 2026-11-04):** review panel (none): built through /add-dataset steps 0-6 and checked against the literature (Noll et al.; Wüthrich and Merz 2023 Sec. 13.1); no panel ran, and all its issues are settled.

**Assessment (AI, 2026-11-04):** review panel (full, second pass after Lennart's PR #33 review): ship after changes, not as defined; disputed: LEAK-17/SPLIT-8/SPLIT-24 (IID or grouped on the inferred policy chains), LEAK-10 against LEAK-37 (realised `Exposure` as a feature), LEAK-10 (the `BonusMalus` mask, settled for blocks 0-4); for the curator: issues 5-9. Priority 3: gap +, use case -, source +, shape +, risk - (gap: insurance is thin among the 107 accepted definitions; use case: the fit is approximate, with no dates and realised exposure kept; source: the CASdatasets help page and the Noll, Salzmann and Wuthrich case study; shape: 677,991 rows, 10 mixed features; risk: likely leaks through `BonusMalus` and `Exposure` and the policy chains across the split, three Must issues open).
