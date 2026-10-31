---
unique_name: eumtpl
name: euMTPL, European motor TPL portfolio (CASdatasets)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: Other
year: '2024'
domain: insurance
problem_type: Regression
original_data_state: One Table
source_links:
- https://dutangc.github.io/CASdatasets/reference/euMTPL.html
- https://dutangc.github.io/CASdatasets/news/index.html
- https://cas.uqam.ca/pub/web/CASdatasets-manual.pdf
- https://doi.org/10.57745/P0KHAG
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: a European motor TPL portfolio (Italian, by its CARD claim types) of 2,373,197 policy-years over three years, with claim counts and costs per claim type, a year and a policy id: 3.5 times freMTPL2; insurance is thin, but the target to ship and the thin documentation are open.
- Source: CASdatasets R package (Dutang and Charpentier), `euMTPL` (https://dutangc.github.io/CASdatasets/reference/euMTPL.html), new in version 1.2-0 ("euMTPL.rda 2024/06/07", news page; deposit doi:10.57745/P0KHAG): "The euMTPL compiles three years of experience from a European MTPL (Motor Third Party Liability) portfolio", collected "during the first decade of the 21st century"; source "Unknown non-life insurers from European Union". As published: one table, 2,373,197 rows x 19 columns: `policy_id`, `year`, `group` (train, validation and test, 70/10/20), `fuel_type`, `vehicle_category`, `vehicle_use`, `province`, `horsepower`, `gender`, `age`, `exposure`, and `cost_*` and `num_*` for four claim types (NC "No Card", CG "Card Gestionario", CD "Card Debitore", FCD).
- Use case: a motor insurer prices a policy at underwriting or renewal from its rating factors through the expected claim frequency per year of exposure, as for `fremtpl2`; fit direct for a claim count with `exposure`; regime temporal by `year` (one policy over three years) or grouped by `policy_id`; check the shipped `group` split against both (SPLIT-19 if it is the source's own).
- Siblings and duplicates: `fremtpl2` and `bemtpl97` (`TBD -> Yes`, priority 4; other portfolios, PROV-7), `eudirectlapse` (same package, lapse task), `ausprivauto0405`, `swedish_motorcycle_insurance`. No euMTPL record before (grep: eumtpl). External collections: none found beyond CASdatasets.
- Better data: found as better data for `bemtpl97` and `fremtpl2`, by the gap scout for insurance, and in the curator's Zotero collection (the data-scouting run of 2026-10-30/31); no further search.
- Papers and pages: the CASdatasets page (it gives no reference), the news page, the manual (not read).
- Metric: none found for this table (no paper); the out-of-sample Poisson deviance with `exposure` is the actuarial habit for claim frequency (see the `fremtpl2` screening), to settle in /add-dataset, else the fallback `rmse`; inputs `exposure` (ships).
- Risks for /add-dataset: the target (one claim type, or the sum of the `num_*` counts); the CARD types are Italian direct-settlement conventions, so check the cost columns for fixed amounts before a severity target; `year` holds small codes (the page's example shows 7) and the currency is not stated; `province` has missing values; insurer and country are not named (PROV-2 note); the page lists `cost_fcd` and `num_fcd` while its example prints `fcg`; 2.4M rows (a 1m cap).
- Priority: gap + (insurance thin), use case 0 (none named by the source), source + (CASdatasets codebook, as for `fremtpl2`), shape + (2.4M policy-years, mixed types, year and policy id), risk - (target choice and claim conventions).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `bemtpl97`, `fremtpl2`; the gap scout for insurance; the curator's Zotero collection, item 302: "Package index".
- as published: 2,373,197 policy-years x 19 columns: policy_id, year, group (a shipped 70/10/20 train/validation/test split), fuel_type, vehicle_category, vehicle_use, province, horsepower, gender, age, exposure, ...; target: claim frequency (a num_* count, or their sum, with exposure) or claim cost (cost_*); access: open.
- Why: same kind of task as fremtpl2 and bemtpl97 but larger and with a panel: one policy over three calendar years, so a temporal or policy-grouped split is natural; CASdatasets is the documented collection those records already rest on | The same pricing task as fremtpl2 and bemtpl97 with 3.5 times freMTPL2's rows, a year ...
- Adds: 3.5 times freMTPL2's rows, a year column and policy ids (temporal and grouped regimes), several claim types; a third MTPL portfolio from another country (Italian CARD convention, by the cost columns). Risks: the insurer and the paper are not named (PROV-2 note), which target to ship, the shipped group split to check ...
