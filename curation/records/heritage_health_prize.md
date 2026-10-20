---
unique_name: heritage_health_prize
name: Heritage Health Prize (Heritage Provider Network, Kaggle 2011-2013), DaysInHospital
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Not Available (from Paper))
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
- Non-IID (Temporal)
original_source: Kaggle
year: '2011'
domain: medical & healthcare
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.kaggle.com/competitions/hhp
- https://www.kaggle.com/competitions/hhp/data
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a web search for zero-inflated regression candidates, the source pages and, where the notes say so, the downloaded data. A human must verify the suggestion, the metadata and the notes before relying on them.**

Heritage Provider Network's $3 million prize on Kaggle (2011-2013): de-identified records of about 113,000 HPN
members (release 3: Members, 2.67 million Claims rows, Labs, Rx; forum topic 1008) and the target DaysInHospital,
inpatient plus ER days in the following year, capped at 15 "as a privacy measure" (data page). Labels exist for Y2
and Y3; Y4 was the hidden test and its labels were not released. Zero mechanism: no hospital stay that year. In release 1,
64,361 of 77,289 Y2 members had 0 days (83.3%, forum topic 389; the host then fixed an odd/even artefact of its
cleaning, so later releases differ slightly). Not measured: `competitions download hhp` returns 403 because this
account never entered, and the data page reads "DATA IS NO LONGER AVAILABLE FOR ANY REASON". Only accounts that
accepted the rules before 2012-10-04 can still download.

The task fits the benchmark: aggregate one year's claims per member and predict the next year's days, training on
Y1 to Y2 and testing on Y2 to Y3 (temporal). DaysInHospital is built from the same year's claims (data page: "based
on the Claims Table with admissions in Y2 or Y3"), so features may only come from the year before; `ClaimsTruncated`
refers to the feature year and is known at prediction time. No as unobtainable data, following
`shaoxing_hourly_precipitation_fusion`. To check: whether a curator's Kaggle account entered in 2011-12 and can still
download, and whether Rule 22 (research use "without Sponsor's prior written approval" is forbidden; requests go to
HPN) counts as a request-only download, which the licence rule says is no reason for a No; then it would be
TBD -> 2nd Tier pending a request. Terms: Rule 22 of the official rules, data for the competition only.

## Reference

Heritage Provider Network (2011). Heritage Health Prize. Kaggle competition, 2011-04-04 to 2013-04-04,
https://www.kaggle.com/competitions/hhp.

Lead: web search 2026-10-20 for zero-inflated regression candidates (not in the v4 workbook).
