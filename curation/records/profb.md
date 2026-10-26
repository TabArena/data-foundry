---
unique_name: profb
name: profb
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
tags:
- 2nd Tier / Scientific Discovery
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

**Screening (AI, 2026-10-22):** `No` (`No Good Target / Scientific Discovery`, SEL-3, SEL-8): NFL scores and point spreads for 1989-1991 compiled by Hal Stern for a 1992 Joint Statistical Meetings talk, published on StatLib for investigating questions, not for a prediction; the OpenML target is a relabelling.
- Source: StatLib `profb` (Hal Stern, Robin Lock; 1992), OpenML 470 (2014); as published: 672 games (224 regular-season games per season) x 9 variables (Home/Away, Favorite Points, Underdog Points, Pointspread, team codes, Year, Week, Special).
- Use case: none the source states. It asks "How well do the oddsmakers of Las Vegas predict the outcome of professional football games? Is there really a home field advantage - if so how large is it?" and says "These questions and a host of others can be investigated using this data set": a look-back study (SEL-3, USE-2). OpenML's default target `Home/Away` ("Favored team is at home (1) or away (0)") is a fact of the schedule known before the game, not an outcome anyone predicts (SEL-8).
- Siblings and duplicates: none in `curation/records/`; external collections: TabSTAR, the TabArena workbook's rejects ("TabArena Reject").
- Human notes: the CC line ("wrong target used on OpenML, need more thought on what the actual target could be. In general, the task was rather presented as an interpretability task").
- A constructed target (the favourite covers the spread) would be a betting task on 672 games with the spread as the main input; the source does not define it.
- Reject check (AI, 2026-10-22): stands. StatLib/OpenML 470 (https://www.openml.org/d/470): 'These questions and a host of others can be investigated using this data set' (home advantage, oddsmakers' accuracy), which is a look-back study (SEL-3). OpenML's target 'Home/Away = Favored team is at home' is a fixed fact of the schedule, a relabelling (SEL-8). The record's CC says the same: 'wrong target used on OpenML ... the task was rather presented as an interpretability task'.

NFL game-score data for the 1989-1991 seasons (StatLib/OpenML d/470). The curator notes the OpenML target is wrong, the intended use was an interpretability illustration rather than prediction, and it is unclear what a valid target would be; it already sits in TabArena Reject. The lack of a clear meaningful target and its origin as an interpretability example make it unrepresentative. Suggest No; a human could revisit whether a sensible predictive target (e.g. game outcome) exists, but it currently lacks one.

---

CC: "scores for all National Football League games from the 1989, 1990, and 1991 seasons, wrong target used on OpenML, need more thought on what the actual target could be. In general, the task was rather presented as an interpretability task"

## Reference

https://lib.stat.cmu.edu/datasets/
