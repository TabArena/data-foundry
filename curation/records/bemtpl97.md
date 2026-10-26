---
unique_name: bemtpl97
name: beMTPL97
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- AI-Filled (Verify)
original_source: Other
year: '1997'
domain: insurance
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://dutangc.github.io/CASdatasets/reference/beMTPL97.html
- https://ideas.repec.org/a/taf/sactxx/v2018y2018i8p681-705.html
source_row: 1045
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 4: a documented Belgian MTPL portfolio for claim frequency or severity, the insurer's pricing task, and insurance is thin.
- Source: CASdatasets R package (Dutang and Charpentier), `beMTPL97` page: "Unknown insurer", 163,212 unique policyholders, 18 columns (`id`, `expo`, `claim`, `nclaims`, `amount`, `average`, `coverage`, `ageph`, `sex`, `bm`, `power`, `agec`, `fuel`, `use`, `fleet`, `postcode`, `long`, `lat`); the page cites Henckaerts, Antonio, Clijsters and Verbelen (2018), "A data driven binning strategy for the construction of insurance tariff classes", Scandinavian Actuarial Journal 2018(8), as the reference for the data. One table. The `year` 1997 is the portfolio year the name suggests; the page does not state it (first publication of the data is about 2018).
- Use case: an insurer sets the premium of a policy at underwriting from the rating factors (Henckaerts et al.: GAMs on the number of claims and on severity, then GLM tariff classes); fit direct for the frequency target (`nclaims` with `expo` as exposure); regime IID, one row per policyholder, no date column.
- Siblings and duplicates: `fremtpl2` (French MTPL, CASdatasets, a different portfolio, so no duplicate, PROV-7); no other Belgian MTPL record. External collections: CASdatasets; used in Deprez, Verbeke and Verdonck (arXiv 2605.22892, 2026, TabPFN for insurance pricing on two public MTPL sets, which ones not confirmed from the abstract).
- Papers and pages: https://dutangc.github.io/CASdatasets/reference/beMTPL97.html; Henckaerts et al. 2018 (https://ideas.repec.org/a/taf/sactxx/v2018y2018i8p681-705.html, open working paper KU Leuven AFI 583471); CASdatasets manual https://cas.uqam.ca/pub/web/CASdatasets-manual.pdf.
- Metric: none found as one ranked criterion (the abstract of Henckaerts et al. reports model fit of GAMs and GLMs; the full text was not read; the CASdatasets page states none), so the fallback (rmse on the claim count) unless the full text fixes Poisson deviance; a deviance would need `expo` as an input, which ships (MET-1, MET-5).
- Risks for /add-dataset: choose one target (`nclaims` per exposure, or `amount` / `average` for severity on claimants); `claim`, `amount`, `average` are framings of the outcome and must be dropped as features (LEAK, USE-3); `postcode` with `long`/`lat` is spatial and may call for a grouped check; `expo` as weight or offset needs a decision.
- Priority: gap + (insurance thin), use case + (pricing named by the paper), source + (CASdatasets page and a paper), shape + (163k rows, mixed types, spatial), risk - (target and exposure handling to settle).

beMTPL97 from the CASdatasets actuarial collection: a Belgian motor third-party liability portfolio used for claim-frequency (and severity) modelling, a classic real-world tabular insurance task with policyholder/vehicle features and a count/exposure target. It is a genuine, well-known actuarial dataset, representative of tabular ML, typically modelled with an IID split. Considerations: the natural target is claim COUNT with exposure offset (Poisson), which a human should map to a supported problem type (regression, or binary has-claim), and confirm it is not a duplicate of other CASdatasets MTPL tables already in the benchmark.

---

Also see https://arxiv.org/abs/2605.22892 and https://cas.uqam.ca/pub/web/CASdatasets-manual.pdf
