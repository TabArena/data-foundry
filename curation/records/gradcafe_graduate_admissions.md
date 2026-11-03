---
unique_name: gradcafe_graduate_admissions
name: GradCafe admission results (self-reported graduate admission decisions)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
decision_markers:
- Selection Bias
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: Website
year: '? (2015)'
domain: education
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.thegradcafe.com/survey/
- https://github.com/deedy/gradcafe_data
- https://www.kaggle.com/datasets/karun95/gradcafe-computer-science-results
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: 271,807 graduate admission results self-reported on GradCafe (scraped in 2015), observed decisions with university, program, GPA and GRE; education is thin, but the posters select themselves and one applicant's posts share no id.
- Source: GradCafe's results survey (thegradcafe.com/survey, user posts; today "About 958,902 relevant results", no bulk download). Bulk copy: deedy/gradcafe_data on GitHub (created 2015-11-17, no licence): all.csv, "There are 271,807 rows", from the query "u*", and cs.csv, "27,822 results" for "computer*"; 19 columns: uni_name, major, degree, season, decision ("Accepted", "Rejected", "Wait listed", "Interview" and "Other"), decision_method, decision_date, ugrad_gpa ("often scores on 10.0 scales are reported with no clear disambiguation"), gre_verbal, gre_quant, gre_writing, is_new_gre, gre_subject, status, post_data, comments. Kaggle karun95/gradcafe-computer-science-results (2019) holds one gradcafe.csv of 800 MB, larger than its title suggests: a later scrape to compare.
- Use case: an applicant, before applying, estimates the chance of admission at a program to decide where to apply; not named by the source; fit approximate (self-reported results); regime temporal by season (one applicant's posts fall in one season; standards and score scales drift, as the new GRE).
- Siblings and duplicates: `from_scores_to_seats_the_grad_school_ml_challenge` (TBD -> 2nd Tier, priority 1, a Zindi hackathon most likely on Acharya's "Chance of Admit" data); no GradCafe record (grep for gradcafe). External collections: none found.
- Better data: found as better data for `from_scores_to_seats_the_grad_school_ml_challenge`; no further search this round.
- Papers and pages: the GitHub README; the GradCafe survey page; papers that used the scrape were not searched (search budget spent).
- Metric: none found (GitHub README, GradCafe page); fallback `roc_auc` on accepted against rejected (MET-8); inputs none.
- Risks for /add-dataset: `comments`, `decision_method` and `decision_date` are written with the decision (LEAK-1: drop); the poster is not identified, so one profile repeats across schools (LEAK-16, SPLIT-29; a season split keeps a person on one side); GPA on mixed scales, test scores often blank (CLEAN); "Interview", "Wait listed" and "Other" to drop or map (USE-5); self-selected posters (`Selection Bias`); GradCafe's terms of service not read.
- Priority: gap + (education thin, 3 accepted), use case 0 (none named), source 0 (an unlicensed scrape of a user board; the README documents the columns), shape + (271,807 rows, mixed features, seasons), risk - (self-selection and the hidden applicant groups).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `from_scores_to_seats_the_grad_school_ml_challenge`.
- as published: 271,807 decisions in all subjects and 27,822 in computer science, 2006-2015; columns: university, major, degree, season, decision (Accepted, Rejected, Wait listed, Interview, Other), decision method ...; target: admitted or rejected on one application (university, program, degree, season); access: open (GitHub scrape without a licence; GradCafe's terms not checked).
- Why: the Zindi task (admission from GRE, GPA and the target university) with observed decisions instead of the 'Chance of Admit' of Acharya's Kaggle set. The Hackade files (mirrored on Kaggle by adebolarabiu, 2025-04-04) have Acharya's seven columns plus Location and Age and about 4,100 IDs: most likely an enlarged copy
- Adds: hundreds of thousands of real decisions over ten seasons with program and university named. Risks: self-reported and self-selected posters (selection bias), GPA on mixed scales, test scores often blank, no licence on the scrape
