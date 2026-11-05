---
unique_name: utility_scale_pv_generation_2017_2022_unidentified
name: PV utility-scale dataset (2017-22), source unidentified
checked_by:
- Andrej
suggestion: 'No'
decision_markers:
- Missing source information
tags:
- Two-Regime Zeros
domain: environmental science & climate
required_split:
- '?'
problem_type: Regression
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (v4 of 2026-10-19, a list of 69 candidates, not in the repository), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `No` (`Missing source information`, PROV-1): the lead names no publication, link or
publisher, and repeated searches found no release with its row count and period.
- Source: none. The lead is the two-regime-zero workbook, Master row 32: "Legacy photovoltaic-generation candidate
  with an unresolved plant/site identity and no matched original data release"; its Dataset URL is a Google search;
  "Paper / DOI URL: Not identified"; "Repository / companion URL: Not located"; "Deep-review outcome: Exact source
  unresolved"; "196,776 samples and 2017-2022 are inherited clues only, not verified properties of an identified
  release".
- Searched 2026-10-27: the web for "196,776" and "196776" with photovoltaic, solar and PV; utility-scale PV
  generation data for 2017-2022; Kaggle datasets for "utility scale solar", "utility-scale PV" and "solar power plant
  2017 2022"; the reject check also searched the Hugging Face API, Zenodo, Mendeley Data and Data in Brief. The nearest
  hits (LBNL Solar-to-Grid, hourly; NREL representative profiles, modelled; a global facility-level PV inventory on
  Zenodo, 2026; Elia's Belgian PV series) match neither the count nor the period, and the workbook rules out
  substituting one. 196,776 is not a whole number of days at 15 or 10 minutes (2,049.75 and 1,366.5 days). The
  earlier AI triage (2026-10-19) and the workbook's own deep review found nothing either.
- If a source turns up: one plant's generation over time would face SEL-10 and TP-10 like
  `unisolar_la_trobe_pv_generation`, whose night is coded missing rather than 0.
- Reject check (AI, 2026-10-27): stands. PROV-1 (Must). After searches of the web, Kaggle, Hugging Face, Zenodo,
  Mendeley Data and Data in Brief, nothing matches the workbook row, whose only link is a search
  (Master row 32), and PROV-2 has no upload to point to.

CC (2026-10-30, Andrej): `No`, as screened (verified on the zero-inflated screening review page).

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

Lead: the two-regime-zero workbook (v4, 2026-10-19), Master row 32 (PV utility-scale dataset (2017-22)).
