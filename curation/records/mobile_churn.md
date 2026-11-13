---
unique_name: mobile_churn
name: mobile_churn
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
priority: 1
decision_markers:
- Missing source information
tags:
- Larger IID Data
- 'Samples: One Moment'
- 'Target: Later'
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

**Assessment (AI, 2026-10-20):** Re-check by the review panel: the source search has ended with no upstream. Every path ends at the anonymous Kaggle upload of 2019 (no description, licence unknown, no other datasets by the uploader); OpenML 44231 is a copy, and no source defines churn or its horizon. The data place the label after the month's snapshot for both classes and no column restates it, but the panel recommends `No` with `Missing source information` under PROV-1 as written, unless the curator amends PROV-1/PROV-2 to cover an untraceable upload with an undefined label rule (Review issue 1). Priority 1: gap - (no thin domain, problem type or regime), use case - (the source names no actor or decision; the use case is ours), source - (anonymous upload), shape + (54,207 accounts, 57 features), risk - (recommended not to ship; undefined target).

CC (2026-10-21, Lennart): option (a) of the consistency check on one-snapshot churn sets: tagged `ForcedIIDFromTemporal`; SPLIT-8 now covers a release with one stock month or one undated snapshot. The tag stays; Review issue 4 settled.

CC (2026-10-21, Lennart): an upload whose first platform cannot be traced is kept for now, case by case, when the data looks sound and there is a source to point to ("if the data looks good enough even without a good source but there is a source, we want to keep it for now and risk it"); PROV-1/PROV-2 amended, the gap written as an approximate fit with a note.

**Assessment (AI, 2026-10-21):** REVIEW.md issue 1 settled and removed; the outcome now recommends shipping as defined, issue 2 (the drop of SIM cards never activated) stays open.

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: user_intake, user_has_outgoing_calls, user_has_outgoing_sms, user_use_gprs, user_does_reload.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Kaggle dataset with unknown origin (no paper, no operator); no task or metric defined.

CC (2026-10-22, Lennart): issue 2: confirm the drop of the SIM cards never activated, in every month ("looks good to me").

**Assessment (AI, 2026-10-22):** settled as implemented; REVIEW.md removed (nothing left open). Not built yet.

CC (2026-10-26, Lennart): verdict ship.

CC (2026-11-01, Lennart): marks on the review board of PR #37: month, the record month, stays a number (the curator's cycle rule).

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `orange_belgium_churn_uplift` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-13, Andrej): collection fact `Target: Later` (Review issue 1, C): whether the account churns, which the data place after the month's end, so it arrives after the features; the forced tag and the split stay.

CC (2026-11-13, Andrej): time basis `DelayedTarget` instead of `ForcedIIDFromTemporal`: the end of the record month is the shared prediction moment and churn follows it (`Target: Later`); the source states neither the churn rule nor its window, which is taken as closed. The random split stays.

## Review

**Outcome:** added. The record gained `Target: Later` on 2026-11-13.

**Main points:** Nothing open: issue 1 resolved on 2026-11-13 (`Target: Later` recorded).

**Issues for Andrej:**

1. **Stay forced and record `Target: Later`, or `CrossSectional`?**

   * **Problem:**
     - The record names no `Target:` fact, which reads as a target measured with the features[^cs-1].
     - The label is whether the account churns, which the data place after the month's end: it arrives after the features, so the use case looks forward and the forced tag fits[^fo-1].
     - The missing fact is what makes it look cross-sectional.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Leave as is (implemented) | the forced tag stays, the record keeps no `Target:` fact | no change | the record contradicts the label's timing |
     | B | `CrossSectional` | the tag reads the label as a present state | none found | the label arrives later, which a present state excludes |
     | C | Stay forced, record `Target: Later` | the record gains the fact; tag and split stay | the record says when the label arrives; the facts guard can check it | none found |

   * **Recommendation:** C. **Decision:** A, B or C?

   **Notes for the AI:** on C, add `Target: Later` to the record with a CC line; the definition does not change.

   [^cs-1]: **SPLIT-32** (Should, 2026-11-13): a target measured together with the features, which the use case reads for new units at their own present, is `CrossSectional`, whether the dates survive or not; its line says whether the drift of the relation was measured or is untested. A label that only arrives later is no present state.
   [^fo-1]: **SPLIT-8** (Must): a forward use case without usable time ships in the closest regime, tagged forced from temporal, with a `Time basis:` line naming the reason.

   **Andrej (2026-11-13, change):** Option C: Stay forced, record Target: Later.

   **Resolved (2026-11-13, Andrej):** C. The record has `Target: Later`; the forced tag and the split stay (`CrossSectional`, option B, was dropped the same day).

## Reference

Kaggle
