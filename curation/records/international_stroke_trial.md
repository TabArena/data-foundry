---
unique_name: international_stroke_trial
name: International Stroke Trial database (version 2)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- AI-Filled (Verify)
source_links:
- https://doi.org/10.7488/ds/104
- https://doi.org/10.1186/1745-6215-12-101
- https://doi.org/10.1016/S0140-6736(97)04011-7
- http://web.archive.org/web/20260128022518/https://datashare.ed.ac.uk/handle/10283/128
- https://datashare.ed.ac.uk/handle/10283/128
- https://doi.org/10.1186/1745-6215-13-24
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Duplicate`, PROV-4): the International Stroke Trial database (Edinburgh DataShare, https://doi.org/10.7488/ds/104), the same file as `international_stroke_trial_outcome` (screened `TBD -> Yes`, priority 3, on 2026-10-31); this record's target, death or dependency at six months, is OCCODE 1-2 against 3-4, a two-class framing of the four-class outcome that record carries (PROV-6, CLEAN-18), so one record holds the dataset and the curator picks two or four classes there.
- Source: Sandercock, Niewada, Członkowska and the IST Collaborative Group, "The International Stroke Trial database", Trials 12:101 (2011, https://doi.org/10.1186/1745-6215-12-101; full text read via Europe PMC, PMC3104487), correction Trials 13:24 (2012, https://doi.org/10.1186/1745-6215-13-24); data https://doi.org/10.7488/ds/104 (DataShare answered 403 on 2026-10-31). Both records list these links. As published: 19,435 patients randomised 1991-1996, one row per patient with the randomisation variables, the 14-day form, the six-month follow-up and three model predictions (EXPDD, EXPD6, EXPD14). The variable list: "OCCODE Six month outcome (1-dead/2-dependent/3-not recovered/4-recovered/0 or 9 - missing status"; Methods: "The primary outcome was the proportion of patients who were either dead or dependent on other people for activities of daily living at six months after randomisation."
- Use case, regime, metric and risks: as in `international_stroke_trial_outcome` (prognosis at randomisation, fit approximate for care without thrombolysis, grouped by hospital or country, the fallback metric, randomisation variables only). The alternative target, death at 14 days (ID14), is another target on the same cohort (PROV-6), and its form was unblinded ("These unblinded data, may therefore be subject to some degree of bias").
- For the canonical record: this record's Assessment adds the licence (ODC-By) and the advice to take the corrected file; carry both over. If the curator prefers this name for the dataset, swap the two records instead (the screening sits in the other one).
- Siblings: `international_stroke_trial_outcome`; `stroke_prediction` (`No`, SEL-7) and the other stroke records are other data. Better data: from the curator's Zotero collection (items 79, 127, 136); no further search this round.
- Reject check (AI, 2026-10-31): stands. Same file (https://doi.org/10.7488/ds/104), and the binary target is a framing of one column: 'OCCODE Six month outcome (1-dead/2-dependent/3-not recovered/4-recovered/0 or 9 - missing status' and 'The primary outcome was the proportion of patients who were either dead or dependent on other people for activities of daily living at six months after randomisation' (Sandercock et al. 2011, variable list and Methods, PMC3104487, re-read 2026-10-31). ID14 is only named as an alternative, from forms the paper calls unblinded. Carry the ODC-By licence, the corrected-file advice and the Lancet 1997 DOI (10.1016/S0140-6736(97)04011-7) over to international_stroke_trial_outcome.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 127: "Datasets"; the curator's Zotero collection, item 136: "Datasets"; the curator's Zotero collection, item 79: "Datasets".
- as published: 19,435 patients with acute ischaemic stroke, 467 hospitals in 36 countries, 1991-1996, 99% follow-up. Variables at randomisation (age, sex, consciousness, deficits, stroke subtype, blood pressure, ...; target: Death or dependency at 6 months (alternatively death at 14 days); access: open.
- Why: A large, open, real trial cohort with standard outcomes known after the prediction point; country gives a grouped split. | Large public trial cohort with a prognostic target and baseline features known at randomisation; country gives a grouped split | An open, large and documented trial database with hospital and ...
- Adds: Acute stroke prognosis; the stroke records are small or synthetic Kaggle sets. It is dated (1990s, no thrombolysis), but the task is still done today. | An acute-stroke prognosis task; the stroke records are survey or Kaggle tables. Licence now confirmed (ODC-By). Use the corrected file (the original garbled event ...
