---
unique_name: onestop_eye_movements_critical_span
name: 'OneStop: A 360-Participant English Eye Tracking Dataset with Different Reading Regimes (OneStop Eye Movements)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Wrong Domain / Source Modality
- Needs extensive data wrangling
tags:
- Non-IID (Grouped)
- AI-Filled (Verify)
original_source: Other
year: '2025'
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
source_links:
- https://doi.org/10.1038/s41597-025-06272-2
- https://osf.io/2prdq/
- https://osf.io/z7pyn/
- https://github.com/lacclab/OneStop-Eye-Movements
- https://pmc.ncbi.nlm.nih.gov/articles/PMC12727756/
- https://arxiv.org/abs/2410.04484
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: a large documented eye-tracking corpus (360 readers, 2.6 million word tokens, 2025) that could rebuild the relevance-from-gaze task of `eye_movements` with readers to group by, but the critical-span target is our construction, the source's own prediction tasks are trial-level, and the modality question of the old record stays.
- Source: Berzak, Malmaud, Shubi, Meiri, Lion, Levy, "OneStop: A 360-Participant English Eye Tracking Dataset with Different Reading Regimes", Scientific Data 12:1995 (2025), doi 10.1038/s41597-025-06272-2 (PMC12727756, read in summary; arXiv 2410.04484); data on OSF (osf.io/2prdq; eye-tracking data CC BY 4.0, OneStopQA materials CC BY-SA 4.0), code at github.com/lacclab/OneStop-Eye-Movements. As published: 360 L1 English readers of 30 Guardian articles, one comprehension question per paragraph (486 questions); ordinary reading (Gathering) and information seeking (Hunting, the question shown before the paragraph) between subjects, plus repeated reading; raw EDF/ASCII, fixation reports and word-level interest-area reports for seven interest periods; word annotations (frequency, GPT-2 surprisal, length, spaCy syntax). The critical span is the STARC annotation of the text a correct answer depends on ("Typically, the critical span does not contain the answer in verbatim form").
- Use case: implicit relevance feedback, the 2005 challenge's framing: an interface infers from gaze which passage a reader finds relevant to the query they hold. The descriptor names "predictive modeling of cognitive state" and "real time prediction of information seeking", and the README lists reading-comprehension prediction (EMNLP 2024) and reading-goal decoding (ACL 2025) as uses, not the critical span. Fit approximate (a text annotation stands for the reader's judgement). Regime grouped by participant (a new reader), SPLIT-23.
- Siblings and duplicates: `eye_movements` (TBD -> 2nd Tier, `Wrong Domain / Source Modality`, TabSTAR; CC: "Unresolvable leak, groups"); `bsnip1_psychosis_eye_movement` (eye tracking for a diagnosis, another task). Another source, not a duplicate (PROV-4). External collections: none found.
- Better data: found as better data for `eye_movements`; no further search this round.
- Papers and pages: the data descriptor; Shubi et al., "Fine-Grained Prediction of Reading Comprehension from Eye Movements" (EMNLP 2024) and "Decoding Reading Goals from Eye Movements" (ACL 2025), named in the README, not read.
- Metric: none found for a critical-span task (the descriptor and the README checked), so the fallback `roc_auc` for a binary word or sentence label (MET-8, MET-11); inputs the participant id as the group, which ships as the split group.
- Risks for /add-dataset: the table is ours to build from the interest-area reports (word or sentence, Hunting trials only, the aggregation); the word, its position and the question settle the span without any gaze, so shipping them makes a reading-comprehension text task (SEL-12) and dropping them makes the task unlike its use; repeated-reading trials of the same reader; the modality call of `eye_movements` (signals judged case by case, SEL-15).
- Priority: gap 0, use case 0 (ours), source + (a peer-reviewed data descriptor), shape + (about 9,700 Hunting trials of 180 readers, word-level rows), risk - (a constructed target that the text alone may decide).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `eye_movements`.
- as published: 360 native English readers (303 Boston, 57 Haifa), EyeLink 1000 Plus at 1000 Hz; 19,438 regular paragraph trials plus 3,888 repeated-reading trials over 30 Guardian articles (OneStopQA, 486 ...; target: whether a word (or sentence) of the paragraph lies in the question's critical span, i.e. the text that is relevant to the question the reader holds, read off ...; access: open.
- Why: eye_movements is the PASCAL 2005 'Inferring Relevance from Eye Movements' challenge: word-level eye-movement features (fixation counts and durations, regressions, saccade lengths) of sentences read under a question, target irrelevant / relevant / correct answer. OneStop's Hunting condition is the same setting (reader ...
- Adds: 360 instead of a handful of readers (the 2005 set is about 10.9k word rows on OpenML 1044), a peer-reviewed data descriptor and open CC BY 4.0 release where the record notes 'Cannot find the source dataset', participant IDs for a grouped split (the record's CC flag was an unresolvable group leak), word-level tabular ...
