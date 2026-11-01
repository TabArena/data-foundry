---
unique_name: eudirectlapse
name: eudirectlapse, motor renewal lapse in a European direct channel (CASdatasets)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- AI-Filled (Verify)
original_source: Other
domain: insurance
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://dutangc.github.io/CASdatasets/reference/eudirectlapse.html
- '# uslapseagent, another lapse table of the same package (US whole-life policies), not this record''s data'
- https://dutangc.github.io/CASdatasets/reference/uslapseagent.html
- '# Milhaud and Dutang 2018, the paper on uslapseagent'
- https://doi.org/10.1007/s13385-018-0165-7
- https://doi.org/10.57745/P0KHAG
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: a real European motor book of 23,060 renewal quotes with the offered, previous and market premiums and a lapse flag, documented in CASdatasets; insurance is thin, and lapse is a task the benchmark does not have.
- Source: CASdatasets R package (Dutang and Charpentier; https://dutangc.github.io/CASdatasets/reference/eudirectlapse.html; deposit "Insurance dataset", Recherche Data Gouv doi:10.57745/P0KHAG, CASdatasets 1.2-0, 2024): "based on one-year vehicle insurance renewal quotes for an unknown year and an unknown insurer"; source "Unknown non-life insurers from European Union". As published: one table, 23,060 rows x 19 columns: `lapse`, `polholder_age`, `polholder_BMCevol`, `polholder_diffdriver`, `polholder_gender`, `polholder_job`, `policy_age`, `policy_caruse`, `policy_nbcontract`, `prem_final`, `prem_freqperyear`, `prem_last`, `prem_market`, `prem_pure`, `vehicl_age`, `vehicl_agepurchase`, `vehicl_garage`, `vehicl_powerkw`, `vehicl_region`.
- Use case: a direct-channel motor insurer, when it sends the renewal quote, sets the premium and retention offers from the chance that the customer leaves; fit direct (the offered premium `prem_final` and the market proxy are known at the quote); regime IID (no date and no customer id ship).
- Siblings and duplicates: other CASdatasets records `fremtpl2` and `bemtpl97` (`TBD -> Yes`, priority 4), `eumtpl`, `ausprivauto0405`, `swedish_motorcycle_insurance`, `msha_mine_injury_frequency` (other tables and tasks, PROV-7); `insurance_dataset_based_on_real_world_statistics` (`No`, synthetic, the record this was found for). No lapse record before (grep: lapse, eudirectlapse). External collections: none found beyond CASdatasets.
- Better data: found as better data for `insurance_dataset_based_on_real_world_statistics`, by the gap scout for insurance, and in the curator's Zotero collection (the data-scouting run of 2026-10-30/31); no further search. The package's other lapse table, `uslapseagent` (US whole-life policies, surrender with competing exits; Milhaud and Dutang 2018, European Actuarial Journal, doi:10.1007/s13385-018-0165-7), is a different dataset and task: noted in `source_links`, no record of its own.
- Papers and pages: the CASdatasets page (it gives no reference); the CASdatasets manual (https://cas.uqam.ca/pub/web/CASdatasets-manual.pdf, not read here).
- Metric: none found (the page names no task and no paper), so the fallback `roc_auc` (or `log_loss`); inputs none.
- Risks for /add-dataset: insurer, country and year are unknown (PROV-2 note, as `fremtpl2`'s "Unknown private insurer"); `prem_pure` (the technical premium) and `prem_final` are the insurer's own model outputs, known at the quote and kept as such; read the lapse share and what counts as a lapse (non-renewal only, or cancellations as well) from the data; `vehicl_powerkw` is banded.
- Priority: gap + (insurance thin), use case 0 (the page names no use), source + (CASdatasets codebook, as for `fremtpl2`), shape + (23k rows, 18 mixed features).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `insurance_dataset_based_on_real_world_statistics`; the gap scout for insurance; the curator's Zotero collection, item 302: "Package index".
- as published: 23,060 renewal quotes x 19 columns: policyholder (age, BMC evolution, driver relation, gender, job), policy (age, car use, number of contracts), premiums (prem_final offered, prem_last, prem_market, ...; target: lapse (1 if the customer left at renewal); access: open.
- Why: lapse is named in the area and not in the benchmark; a clean binary target with the offered, last and market premiums known at the renewal quote; mixed types | the retention half of the synthetic personal-auto record (its stated uses: 'predicting customer conversion and retention'), on a real insurer book with the ...
- Adds: a retention task in non-life insurance with price features. A second lapse set in the same package, uslapseagent (29,317 US whole-life policies issued 1995-2008, tied-agent channel, surrender with death and other exits as competing risks; Milhaud and Dutang 2018, European Actuarial Journal 8(1), ...
