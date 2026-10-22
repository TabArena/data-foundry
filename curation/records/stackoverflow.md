---
unique_name: stackoverflow
name: StackOverflow
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- NLP (Text)
- Needs extensive data wrangling
tags:
- 2nd Tier / Scientfic Discovery
- Non-IID (Temporal)
- AI-Filled (Verify)
collections:
- New (BeyondArena)
domain: technology & internet
required_split:
- Temporal (NON-IID)
problem_type: Multiclass Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.kaggle.com/competitions/predict-closed-questions-on-stack-overflow/data?select=train.csv
source_row: 848
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Assessment (AI, 2026-10-22):** the curator's `No` (CC line) stands on the text and wrangling load; one counter-argument: "no purpose" does not hold, the host named a use and the decision.
- Source: Kaggle "Predict Closed Questions on Stack Overflow", hosted by Stack Exchange, August to November 2012, 161 teams, 20,000 USD; as published: train.csv with the question at posting time (user and account fields such as reputation at post creation, title, body markdown, up to 5 tags) and the label OpenStatus (open, not a real question, not constructive, off topic, too localized), plus the full 2012-07 Stack Overflow dump (6.7 GB 7z) and leaderboard files.
- Use case: Stack Exchange's blog (https://stackoverflow.blog/2012/08/21/stack-exchange-machine-learning-contest/): "an algorithm that predicts whether (and for what reason) a question will be closed", for "giving users who are composing questions advice on how to improve them while they're composing them", and for better flagging; "everything we knew about them right before they were posted". Actor, moment and decision are named; fit direct. Regime temporal (questions over 2008-2012; the final ranking used fresh questions).
- Siblings and duplicates: `stackoverflow_salary_data` and `stackoverflow_polarity` are other tasks. External collections: none found.
- Papers and pages: Lezina et al. (Uchenye Zapiski Kazanskogo Universiteta 155(4), 2013, pp. 118-133) on the contest, who report user characteristics and topical features as the most important; Stanford CS224d report (lefrankl) scored by the contest's multiclass log loss.
- Metric: multiclass log loss on the Kaggle leaderboard (MET-4); inputs none.
- **Counter-argument (AI):** the CC's facts stand (much of the signal is in the title and body, and the user history needs joins), so `NLP (Text)` and `Needs extensive data wrangling` fit; "no purpose" does not: the host stated the decision above. A tabular cut (user and post metadata plus tags, text left out or reduced to lengths) would be a different, weaker task than the source's, which is why the `No` still holds. The curator has the call.

The Kaggle 'Predict Closed Questions on Stack Overflow' competition data. The curator notes it is dominated by free text, requires heavy feature engineering from user/post IDs and special tag preprocessing, and is described as 'just a collection of data, no purpose.' This is essentially an NLP/text task masquerading as tabular, where text models would dominate and substantial wrangling is needed. Recommend reject as not representative of standard tabular ML.

---

CC: "A lot of text data; requires heavy feature engineering from user IDs and post ID to useful signal; tags require special preprocessing"

Just a collection of data, no purpose.
