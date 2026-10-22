---
unique_name: titanic
name: Titanic
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Trivial
- Not Representative
tags:
- 2nd Tier / Scientfic Discovery
- AI-Filled (Verify)
collections:
- TabArena Reject
- TabSTAR
year: '1997'
domain: social science
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- Pick one of the 1000s of copies (e.g. openml 40704)
- 'One of the original sources is Eaton & Haas (1994) Titanic: Triumph and Tragedy, Patrick Stephens Ltd, which includes a passenger list created by many researchers and edited by Michael A. Findlay.'
- https://www.openml.org/search?type=data&id=40945
source_row: 806
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Assessment (AI, 2026-10-22):** the curator's `No` stands, on the ground the CC line gives ("Not a real predictive task"): no one makes a decision with a survival prediction for the passengers of a ship that sank in 1912.
- Source: passenger list of the RMS Titanic (1912) with survival, compiled from Eaton & Haas (1994) and Encyclopedia Titanica; the common 1,309-row version (Harrell's titanic3, OpenML 40945) and Kaggle's tutorial split (891 + 418). Countless re-uploads.
- Use case: none; the table is used to teach and to look back at who survived (SEL-3; `passenger_list_for_the_estonia_ferry_disaster` was judged the same way: "Like Titanic, a scientific discovery task", Lennart). Regime if kept: IID.
- Siblings and duplicates: `passenger_list_for_the_estonia_ferry_disaster` (`TBD -> 2nd Tier`, Lennart). External collections: TabSTAR; TabArena Reject.
- Metric: Kaggle's tutorial competition scores accuracy (a tutorial's habit, not a decision's metric).
- Counter-argument (markers only): `Trivial` has no evidence from a task probe (TP-4); a sex-and-class rule is strong but not a perfect solve. `No Good Target  / Scientific Discovery` matches the stated reason better than `Trivial`; the curator has the call.

The ubiquitous Titanic survival dataset, already in the TabArena Reject collection. The curator notes it is a toy/interpretability example with no real deployment value (a survival predictor for a sinking ship is not a meaningful predictive task), and it is one of thousands of re-uploaded copies. It is small, toy, and not representative of real-world tabular ML. Recommend reject, consistent with prior curation.

---

CC: "Not sure, but isn't the task trivial? Not a meaningful task, rather toy example; also rather an interpretability task to determine if there were correlations in the data, it would be hard to deploy such a model in the real world when a boat sinks... Don't know which of our criteria applies, but this is clearly a toy dataset and I don't see why it should be included. Not a real predictive task"

## Reference

?
