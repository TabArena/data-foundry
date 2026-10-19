---
unique_name: fremtpl2
name: freMTPL2
checked_by:
- AI (UNVERIFIED)
suggestion: 'Yes'
tags:
- AI-Filled (Verify)
domain: insurance
required_split:
- Random (IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.kaggle.com/datasets/karansarpal/fremtpl2-french-motor-tpl-insurance-claims
source_row: 1044
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

freMTPL2 is the well-known French Motor Third-Party Liability insurance dataset from CASdatasets, a standard actuarial benchmark. The canonical predictive task is claim frequency modelling (Poisson/count regression of claim number against exposure and policy features), a genuine real-world tabular regression/count task that is widely used and adequately sized (hundreds of thousands of policies). It maps cleanly to the criteria: unique original source, real predictive target, representative tabular data, no ethical issue. Note it comes as freq + severity tables (freMTPL2freq / freMTPL2sev) so a human should confirm which table/target is used and how exposure is handled; an IID split is standard.

---

Also see https://arxiv.org/abs/2605.22892 and https://cas.uqam.ca/pub/web/CASdatasets-manual.pdf

**AI note (two-regime-zero audit, 2026-10-19):** the two-regime-zero workbook
(`curation/inputs/two_regime_zero_datasets_v4.xlsx`, Master row 6) proposes the aggregate claim amount instead of the
claim count as the target: join `freMTPL2sev` to `freMTPL2freq` and sum `ClaimAmount` per `IDpol`. Measured on the
OpenML copies (41214 and 41215, uploaded 2018) on 2026-10-19: 678,013 policies, 96.32% with an aggregate amount of
exactly 0. The join has a flaw that matters for that target: 9,116 of the 34,060 policies with `ClaimNb` > 0
have no severity row, so their summed amount would be a false zero, and 195 OpenML severity rows name policies missing
from the frequency table. The current CASdatasets copy (GitHub) has 26,444 severity rows: the OpenML table without
exactly those 195 orphans. If the amount is used, drop or flag the claimed policies without severity rows and keep
`ClaimNb` out of the features. Siblings: `bemtpl97`, and the new `frempl_french_motor_personal_line` (a different
French portfolio).
