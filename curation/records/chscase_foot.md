---
unique_name: chscase_foot
name: chscase_foot
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- No Good Target  / Scientific Discovery
- Too Small
- Outdated
tags:
- Tiny Data
- AI-Filled (Verify)
year: '1995'
domain: Other
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.openml.org/search?type=data&id=703
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 1: the proposed fast reject (SEL-3 (with the curators' workbook verdict; TP-5 not measured)) did not hold in the reject check, so it stays a candidate with the doubt listed.
- Proposed reject (refuted): `No` (`No Good Target  / Scientific Discovery`, SEL-3): the source names no target, OpenML's default target is the season year of a mis-parsed table of NFL games, and the curators already judged it too small and too thin on information; this restores the workbook verdict that an AI policy note had turned into `TBD -> 2nd Tier`.
- Source: file `foot.dat` of the StatLib `chscase` collection from Chatterjee, Handcock & Simonoff, "A Casebook for a First Course in Statistics and Data Analysis" (Wiley, 1995); OpenML 703 (uploaded 2014): "attribute names were generated automatically since there was no information in the data itself", "CLASSTYPE: numeric / CLASSINDEX: none specific"; default target `col_6`. As published on OpenML: 526 rows x 6 columns; preview rows read `BUF__MIA,-1,0,0,1,89`: col_1 a game (visitor__home NFL teams), col_2 a mix of -1/0/1 and team codes (the parse is shifted on some rows, e.g. `GB`, `KC`, `NE` alone in col_1), col_6 = 89, the season.
- Use case: none recorded; the casebook case is a teaching example on football games (likely point spreads), and the OpenML target is a constant-like year, not an outcome (SEL-3).
- Siblings and duplicates: `chscase_geyser1` (Lennart `No`: "outdated, trivial and not useful for our purpose"), same casebook. The workbook import on this record: "TabArena curation verdict: Tiny data", "Lennart: too small", "Andrej: Insufficient information".
- Metric: none (no task is defined).
- `Too Small` stays as the curators' marker (TP-5 not measured here); `Outdated` added (1989-era teaching data).
- Reject check (AI, 2026-10-22): does not stand. The SEL-3 reason rests on OpenML 703's mis-parse (default target col_6 = season 89/90/91). The source names a predictive question: the casebook table of contents lists the foot case as 'Betting on professional football -- can you beat the bookies?' (http://www.stern.nyu.edu/~jsimonof/Casebook/guide.html, categorical-data chapter), and the StatLib file (http://lib.stat.cmu.edu/datasets/chscase, foot.dat) has columns visitor, home, a -1/0/1 column (264/15/247, plausibly the result against the spread), three 0/1-ish columns, week 1-17 and season 89-91. A bettor's decision is a use case SEL-2 can weigh; the curators' 'too small' is no reject reason before processing (record's own policy note), 'insufficient information' is partly answered by the case title.
- For /add-dataset: TBD -> 2nd Tier, priority 1. Add stage must: get the casebook case text (Stern Casebook pages, Updates/Data folders) to name every column and confirm col_2 is the result against the spread; check whether the spread itself is in the file (without it the task is near-noise by market design, TP-4/TP-2); measure TP-5 on 526 games; weigh Outdated (1989-91) and a market-efficiency (scientific-discovery) reading of the case.

Small statistics-textbook casebook dataset ('chscase_foot') with only 526 samples and limited task information. The prior TabArena curation verdict was 'Tiny data, too small for 3-fold CV', and multiple reviewers (Lennart, Andrej) flagged it as too small or insufficiently informative. 526 rows is below the practical threshold for the benchmark's CV protocol. Reject; the size and existing verdicts are clear.

**Update (policy):** "Too Small" is no longer a rejection reason — dataset size is assessed *after* Data Foundry processing. Re-classified off No to TBD -> 2nd Tier pending that post-DF size check.

---

Imported from the TabArena curation workbook.

TabArena curation verdict: Tiny data.

526 samples, too small for 3-fold CV.

Limited task information, only 526 samples. No free version of book available? Task seems pretty simple

Lennart: too small

Andrej: Insufficient information

## Reference

A Casebook for a First Course in Statistics and Data Analysis," by Samprit Chatterjee, Mark S. Handcock and Jeffrey S. Simonoff, John Wiley and Sons, New York, 1995
