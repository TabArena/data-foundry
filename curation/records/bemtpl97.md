---
unique_name: bemtpl97
name: beMTPL97
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
tags:
- AI-Filled (Verify)
year: '1997'
domain: insurance
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://dutangc.github.io/CASdatasets/reference/beMTPL97.html
source_row: 1045
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

beMTPL97 from the CASdatasets actuarial collection: a Belgian motor third-party liability portfolio used for claim-frequency (and severity) modelling, a classic real-world tabular insurance task with policyholder/vehicle features and a count/exposure target. It is a genuine, well-known actuarial dataset, representative of tabular ML, typically modelled with an IID split. Considerations: the natural target is claim COUNT with exposure offset (Poisson), which a human should map to a supported problem type (regression, or binary has-claim), and confirm it is not a duplicate of other CASdatasets MTPL tables already in the benchmark.

---

Also see https://arxiv.org/abs/2605.22892 and https://cas.uqam.ca/pub/web/CASdatasets-manual.pdf
