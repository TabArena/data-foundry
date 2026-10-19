---
unique_name: utility_scale_pv_generation_2017_2022_unidentified
name: PV utility-scale dataset (2017-22), source unidentified
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Missing source information
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
domain: environmental science & climate
required_split:
- '?'
problem_type: Regression
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

The workbook carries this row over from an earlier audit (196,776 samples, 2017-2022, utility-scale PV generation,
night-time zeros), but its only link is a Google search and its own v4 deep review found no matching release. A
second search on 2026-10-19 (the number with and without a thousands separator, utility-scale and PV terms, the date
range) found nothing either. 196,776 rows would be one site at 15-minute resolution for about 5.6 years, which fits
the date range and says nothing more. Without a traceable source this is `No` with `Missing source information`.

If the citation turns up, it would still be generation forecasting like `unisolar_la_trobe_pv_generation`, and
UNISOLAR shows that a release can code night as missing rather than 0, so the claimed zero regime is unverified as
well.

## Reference

No source identified. The workbook lists PVDAQ (https://data.openei.org/submissions/4568) and an LBNL solar series
(https://data.openei.org/submissions/5963) only as unmatched alternatives, not as the source.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 32 (PV utility-scale dataset (2017-22)).
