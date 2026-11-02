---
unique_name: ambassador_skill_up_hackathon
name: ambassador-skill-up-hackathon
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
required_split:
- '?'
problem_type: TBD
source_links:
- https://zindi.africa/competitions/ambassador-skill-up-hackathon/data
source_row: 978
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Duplicate`, PROV-4): a Zindi Ambassador skill-up hackathon (2023-05-26 to 2023-05-29, 28 participants, prize "Knowledge") that reuses the SFC PAYGo Solar Credit Repayment Competition (2021) data and text.
- Source: the 2021 competition, recorded as `sfc_paygo_solar_credit_repayment_competition` (TBD -> Yes) and `sfc_paygo_solar_credit_repayment_hackathon` (TBD -> Yes). Both pages have the subtitle "Can you predict PAYGo solar customer payments?", the same data description ("explore and cleanse a dataset consisting of over ~37000 PAYGo SHS contracts ... expected future payments for n months ahead (for this competition n=6)"), the same files (VariablesDefinition.txt, Train.csv, Test.csv, metadata.csv, StarterNotebook.ipynb) and the same submission example (`ID_0026TMW x m1 1700`).
- Note for the kept record: the task predicts the next six months of payments per contract, which /add-dataset must check against SEL-10 and TP-10.
- Metric: RMSE (Zindi evaluation page), as in 2021.
- Reject check (AI, 2026-10-22): stands. PROV-4. Same subtitle ("Can you predict PAYGo solar customer payments?"), same seven files, same Evaluation (ratio 0.998) and the same submission example. The Data Description repeats the 2021 text: "over ~37000 PAYGo SHS contracts ... n months ahead (for this competition n=6)". The original sfc_paygo_solar_credit_repayment_competition is kept (TBD -> 2nd Tier), and that record carries the SEL-10/TP-10 question. https://zindi.africa/competitions/ambassador-skill-up-hackathon

Generic Zindi 'ambassador skill-up hackathon' with no comments, no described target, and no problem framing in the record. This is most likely a small community/learning hackathon rather than a substantive real-world dataset, but there is too little information to reject outright. A human must open the Zindi page to determine the actual predictive target, modality, size, and whether the data is genuine real-world tabular data; defaulting to 2nd Tier pending that inspection.
