---
unique_name: profb
name: profb
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target (yet)
- Not Representative
tags:
- 2nd Tier / Scientfic Discovery
- AI-Filled (Verify)
collections:
- TabArena Reject
- TabSTAR
year: '1992'
domain: Other
required_split:
- Random (IID)
problem_type: TBD
original_data_state: One Table
source_links:
- https://www.openml.org/d/470
- https://lib.stat.cmu.edu/datasets/profb
source_row: 799
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

NFL game-score data for the 1989-1991 seasons (StatLib/OpenML d/470). The curator notes the OpenML target is wrong, the intended use was an interpretability illustration rather than prediction, and it is unclear what a valid target would be; it already sits in TabArena Reject. The lack of a clear meaningful target and its origin as an interpretability example make it unrepresentative. Suggest No; a human could revisit whether a sensible predictive target (e.g. game outcome) exists, but it currently lacks one.

---

CC: "scores for all National Football League games from the 1989, 1990, and 1991 seasons, wrong target used on OpenML, need more thought on what the actual target could be. In general, the task was rather presented as an interpretability task"

## Reference

https://lib.stat.cmu.edu/datasets/
