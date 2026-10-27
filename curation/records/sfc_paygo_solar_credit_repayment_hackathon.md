---
unique_name: sfc_paygo_solar_credit_repayment_hackathon
name: SFC PAYGo Solar Credit Repayment Hackathon
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: finance
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://zindi.africa/competitions/sfc-paygo-solar-credit-repayment-hackathon
source_row: 1022
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Duplicate`, PROV-6): the 3-day hackathon (4-6 June 2021, $300) on "over ~3000 PAYGo SHS contracts" is a subset of the follow-up SFC PAYGo Solar Credit Repayment Competition (~37,000 contracts, same host, same page text, same task and metric), which calls it "the hackathon which was a subset of this dataset".
- Source: Zindi hackathon "SFC PAYGo Solar Credit Repayment Hackathon", host Solar Frontier Capital, 142 participants (https://zindi.africa/competitions/sfc-paygo-solar-credit-repayment-hackathon, read through the Zindi API); files Train.csv, Test.csv, metadata.csv, VariablesDefinition.txt, StarterNotebook.ipynb; target the next six monthly payments per contract; metric RMSE ("The error metric for this competition is the Root Mean Squared Error").
- Duplicate of: `sfc_paygo_solar_credit_repayment_competition` (https://zindi.africa/competitions/sfc-paygo-solar-credit-repayment-competition): its Data Description says "StarterNotebook.ipynb - this is the starter notebook for the hackathon which was a subset of this dataset", and this hackathon's page says "Once this hackathon is finished join the follow-up competition here - SFC PAYGo Solar Credit Repayment Competition". A cut with fewer rows and no distinct task is a duplicate (PROV-6); the fuller competition is the record to keep (screened `TBD -> 2nd Tier`, priority 2, for its forecasting-like target).
- Also: a discussion thread (6401) reports target months past the cut-off in the hackathon data, one more reason to prefer the competition's release.
- Reject check (AI, 2026-10-22): stands. Zindi API: the competition's Data Description says 'StarterNotebook.ipynb - this is the starter notebook for the hackathon which was a subset of this dataset' (~37000 contracts) and the hackathon (4-6 June 2021) has '~3000 PAYGo SHS contracts' and 'Once this hackathon is finished join the follow-up competition'; same host, target and RMSE (https://zindi.africa/competitions/sfc-paygo-solar-credit-repayment-competition). A smaller cut with no distinct task (PROV-6); keep sfc_paygo_solar_credit_repayment_competition.

Zindi SFC PAYGo solar credit repayment 'hackathon', predicting PAYGo solar customer payments, a real fintech credit-repayment tabular task. It is very likely the same underlying data as the 'competition' variant and should be de-duplicated so only one is kept. A human must compare the two records, confirm the canonical source, the target/problem type, table join structure, size, temporal split, and license, and drop the duplicate.

---

predict PAYGo solar customer payments
