---
unique_name: mobile_churn
name: mobile_churn
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 1
decision_markers:
- Missing source information
tags:
- Larger IID Data
collections:
- TabSTAR
original_source: Kaggle
year: '2019'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.openml.org/search?type=data&id=44231&sort=runs&status=active
- https://www.kaggle.com/datasets/dimitaryanev/mobilechurndataxlsx
v2_path: datasets/_dev/tabarena-v0pt2/mobile_churn/dataset.py
source_row: 656
type_adapter_id: curation-record-v1
---

## Comments

Another case of missing data but data looking very good and real.

Check year/month and user account id column if temporal or grouped splits are needed.

**Assessment (AI, 2026-10-07):** IID split: user_account_id is unique per row; year is constant (2013). 12,262 accounts with neither the intake flag nor an activation date are SIM cards never taken into use, not customers. Only 0.2-0.5% used minutes, SMS or data in 100 days. They came in provisioning batches, churn at 54% (June) and 80% (August), and held 61% of the churners. The v2 definition drops them in every month; the kept July and August rows are those months' new customers. Unlike churn_telco_europa, both classes share their month's snapshot date, and the churners' last activity bunches just before it. No row overlap with the SATO, DSN or Europa churn files. The source and the churn definition remain undocumented.

**Assessment (AI, 2026-10-20):** priority 1 for the review of the added dataset: gap -, use case -, source -, shape +, risk - (Issue 1: source and churn definition unknown (unclear target); alternative is No). Real-looking prepaid churn data with unknown origin and an undocumented label; another common churn task with weak provenance.

**Assessment (AI, 2026-10-20):** Re-check by the review panel: the source search has ended with no upstream. Every path ends at the anonymous Kaggle upload of 2019 (no description, licence unknown, no other datasets by the uploader); OpenML 44231 is a copy, and no source defines churn or its horizon. The data place the label after the month's snapshot for both classes and no column restates it, but the panel recommends `No` with `Missing source information` under PROV-1 as written, unless the curator amends PROV-1/PROV-2 to cover an untraceable upload with an undefined label rule (REVIEW.md issue 1). Priority 1: gap - (no thin domain, problem type or regime), use case - (the source names no actor or decision; the use case is ours), source - (anonymous upload), shape + (54,207 accounts, 57 features), risk - (recommended not to ship; undefined target).

CC (2026-10-21, Lennart): option (a) of the consistency check on one-snapshot churn sets: tagged `ForcedIIDFromTemporal`; SPLIT-8 now covers a release with one stock month or one undated snapshot. The tag stays; REVIEW.md issue 4 settled.

CC (2026-10-21, Lennart): an upload whose first platform cannot be traced is kept for now, case by case, when the data looks sound and there is a source to point to ("if the data looks good enough even without a good source but there is a source, we want to keep it for now and risk it"); PROV-1/PROV-2 amended, the gap written as an approximate fit with a note.

**Assessment (AI, 2026-10-21):** REVIEW.md issue 1 settled and removed; the outcome now recommends shipping as defined, issue 2 (the drop of SIM cards never activated) stays open.

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: user_intake, user_has_outgoing_calls, user_has_outgoing_sms, user_use_gprs, user_does_reload.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Kaggle dataset with unknown origin (no paper, no operator); no task or metric defined.

CC (2026-10-22, Lennart): issue 2: confirm the drop of the SIM cards never activated, in every month ("looks good to me").

**Assessment (AI, 2026-10-22):** settled as implemented; REVIEW.md removed (nothing left open). Not built yet.

## Reference

Kaggle
