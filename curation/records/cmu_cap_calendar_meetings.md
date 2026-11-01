---
unique_name: cmu_cap_calendar_meetings
name: 'CAP (Calendar Apprentice) meeting data, CMU: full raw logs of two users'' calendars'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 3
decision_markers:
- Outdated
tags:
- AI-Filled (Verify)
original_source: Website
year: '1994'
problem_type: Multiclass Classification
source_links:
- https://doi.org/10.1145/176789.176798
- http://www.cs.cmu.edu/afs/cs/project/theo-5/www/cap-data.html
- http://www.cs.cmu.edu/afs/cs.cmu.edu/project/theo-5/www/cap-kb.names
- http://www.cs.cmu.edu/afs/cs.cmu.edu/project/theo-5/www/cap-kb.key
- https://doi.org/10.1023/A:1007335615132
- https://www.cs.cmu.edu/afs/cs.cmu.edu/usr/avrim/Calendar
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 3: the CMU Calendar Apprentice files, the source of `calendardow`: 1,790 timestamped meeting requests in C4.5 format with 32 documented features and four targets (day of week, start time, duration, location), plus the raw calendars of two users; a real assistant decision, but one academic calendar of the early 1990s.
- Source: Mitchell, Caruana, Freitag, McDermott & Zabowski, "Experience with a learning personal assistant", CACM 37(7), 1994 (doi 10.1145/176789.176798): "a calendar manager, called CAP (Calendar APprentice), that learns user scheduling preferences from experience", with "approximately five user-years of experience" (Abstract). The data page (cs.cmu.edu/afs/cs/project/theo-5/www/cap-data.html) offers a homework sample (133 training, 67 test examples), "User1 Data" ("a superset of the CACM paper data", 14 MB), "User2 Data" (4 MB) and the C4.5 files cap-kb.data, cap-kb.names and cap-kb.key ("the last few columns are class assignments for various experiments"); no licence stated. Preview (2026-10-31): cap-kb.data holds 1,790 rows (file dated 1995-01-11), each a timestamp, year, month and day (1992 in the first rows), Feature00-Feature31 and four class columns; cap-kb.key maps the features to CAP attributes (time since and until the last and next meeting with these attendees, the most common days and times of these attendees and of this meeting type over the last 60 days, location, sorted attendees, event and seminar type, course, speakers, position, department and sponsor of the attendees) and names the classes `day-of-week`, `req-start-time`, `req-location`, `req-duration`.
- Use case: when the user enters a meeting request, CAP proposes the default day, time, duration and location, and the user accepts or edits it; actor the assistant and its user, moment the request, decision the suggested default; a prediction of the user's own choice, not a ranking of items (SEL-9 does not apply, our reading); fit approximate: one professor's calendar of the early 1990s stands for calendar users. Regime temporal: CAP learns online from past meetings, and every row has a timestamp (SPLIT-6).
- Siblings and duplicates: `calendardow` (`No`, `Missing source information`; PMLB and OpenML 40663, 399 rows x 32 features, the day-of-week target), the record this was found for: per the run's Assessment cap-kb.names lists the same Feature00-Feature31 with the same arities, so its source is found and its reject ground no longer holds; it is a cut of these files (PROV-6), and the curator decides which one enters and whether `calendardow` is reopened. External collections: PMLB and OpenML (as calendarDOW).
- Better data: found as better data for `calendardow` (the data-scouting run of 2026-10-30/31); no further search.
- Papers and pages: Mitchell et al. 1994 (CACM, abstract read); Blum, "Empirical Support for Winnow and Weighted-Majority Algorithms: Results on a Calendar Scheduling Domain", Machine Learning 26, 1997 (doi 10.1023/A:1007335615132; not read); the CMU data page.
- Metric: not read (the CACM text is a compressed PostScript file on the page); CAP offers one default, so the source's score is likely the accuracy of its suggestion, a hard argmax decision, unconfirmed (MET-5, MET-6); the fallback `log_loss` (MET-1, MET-8); inputs none beyond the timestamp for the split.
- Risks for /add-dataset: which of the four targets to ship (one per dataset, CLEAN-18); "time-until-next-meeting" and "day-of-week-of-next-meeting-with-these-attendees" read meetings already on the calendar: check they were computed from entries made before the request (LEAK-10); attendee, speaker and sponsor values are names of real people (CLEAN-4: a stable id); the raw User1 and User2 logs are larger but must be rebuilt into features; early-1990s data (`Outdated`).
- Priority: gap + (multiclass is thin), use case 0 (approximate), source + (CACM paper and CMU page), shape + (1,790 meetings x 32 mixed features, timestamped), risk − (`Outdated`, names, the choice of target).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `calendardow`.
- as published: One row per meeting request. User1 (Tom Mitchell's calendar, a superset of the CACM data; about 1,685 meetings over two years per Blum 1997) and User2 (about 554 meetings); raw ...; target: day of the week of the meeting (Mon-Fri), as in calendarDOW; the same files also hold duration, location and start time; access: open.
- Why: Source of calendarDOW found: cap-kb.names lists Feature00-Feature31 with the same names and arities as PMLB/OpenML 40663, and cap-kb.key maps them to CAP attributes (time since last meeting with these attendees, most common day/time of these attendees in the last 60 days, event type, seminar type, attendee position, ...
- Adds: About 2,240 meetings from two users against 399, plus the published meaning of every feature. Caveats: still small and dated (1991-1993), one academic calendar dominates, the features must be rebuilt from frame files, no licence stated, and the data names real CMU people (attendees, speakers, sponsors): a ...
- A newer release of the same source as the record(s) named above (PROV-6): the curator decides which one enters.
