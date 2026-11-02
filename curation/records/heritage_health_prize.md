---
unique_name: heritage_health_prize
name: Heritage Health Prize (Heritage Provider Network, Kaggle 2011-2013), DaysInHospital
checked_by:
- Andrej
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Not Available (from Paper))
- Available on Request
tags:
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
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a web search for zero-inflated regression candidates, the source pages and, where the notes say so, the downloaded data. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> Yes`, priority 3: the sponsor names the prediction and the decision and the
competition fixed the metric; the data cannot be downloaded today, which EV-4 makes a note and not a reason for `No`, so
the earlier `No` is no fast reject.
- Source: Heritage Provider Network's Heritage Health Prize on Kaggle, 2011-04-04 to 2013-04-04, entries until
  2012-10-04 (Kaggle API). As published: releases 1-3 (`HHP_release1.zip` to `HHP_release3.zip` and two data
  dictionaries, Kaggle API file list): Members, Claims, Labs, Rx and DaysInHospital for Y2 and Y3; "3 years of
  de-identified HPN data on 113,000 patients" (El Emam et al. 2012, JMIR 14(1):e33, Introduction); DaysInHospital
  top-coded "at the 99th percentile" (Methods, "Top-Coding"). Y4 labels were never released.
- Use case: HPN wants to "reliably predict which patients will be admitted to the hospital" and "alert providers to
  patients at risk for hospital admissions", who "can develop new care plans" (prize announcement, KDnuggets, December
  2010); Kaggle: "Identify patients who will be admitted to a hospital within the next year using historical claims
  data". A provider, at the start of a year, decides on a care plan; fit direct. Regime temporal: features from one
  year, days in hospital in the next (Y1 to Y2 for training, Y2 to Y3 for testing).
- Siblings and duplicates: none among the records. External collections: none found.
- Papers and pages: El Emam et al. 2012 (the de-identification); the milestone papers (forum topics 904, 1528, 2764).
- Metric: RMSLE (Kaggle API, "Root Mean Squared Logarithmic Error"), the leaderboard metric (MET-4): `rmsle` with
  `target_transform="log1p"` on DaysInHospital (MET-3); inputs none.
- Risks for /add-dataset: access first: a download of one dictionary file answers "You don't have access to this
  resource" (2026-10-27); a participant in topic 7560 (2014): "There is no possibility of obtaining the data, as stated
  on the Data page"; the earlier AI triage quoted the data page ("DATA IS NO LONGER AVAILABLE FOR ANY REASON") and Rule
  22 (other use needs the sponsor's prior written approval; not re-read here). Next step: a curator's Kaggle account
  that entered in 2011-12, or a request to HPN (then `Data Requested`); `Not Available (from Paper))` kept as the state
  until then. After that: claims aggregated per member and year from the year before the target only (the target is
  built from the same year's claims, LEAK-10), four tables joined; the de-identification (suppression, top-coding) is
  disclosure control, to note under PROV-3. No open family question applies (a zero is a year without a stay; the cap at
  15 days is a top-code, not a zero).
- Priority: gap 0 (medical), use case + (HPN names actor and decision), source + (HPN's data dictionaries and the
  de-identification paper), shape + (113,000 members, three years), risk - (four tables to aggregate and join).

**Assessment (AI, 2026-10-30):** the last search for a copy, as the curator asked. Two GitHub repositories serve the
complete release 3 (`sandro-pasquali/RBelgium_HeritageHealthPrize`, 2012, `Data/HHP_release3.zip`, 55 MB;
`truongkhanhduy95/Heritage-Health-Prize`, 2018), identical by CRC32 and matching the documentation (Members 113,000
rows; DaysInHospital_Y2 76,038 rows, 84.5% zeros, maximum 15). Both are unlicensed redistributions: the official rules
allow the data "solely for purposes of the Competition" (Rule 5), require entrants to erase it afterwards, and need the
"Sponsor's prior written approval" for any other use (Rule 22), so building from them would break the terms. The Harvard
Data Privacy Lab's ForeverData archive (collection 1015) held releases 1-3 and now answers 403, with access by a request
form; Hugging Face `cestwc/heritage-health-prize-release-3` holds per-member aggregates without the target; Kaggle
offers no route. So the data is obtainable only on request (HPN's contact page, citing Rule 22), and the GitHub copy
would make it buildable once HPN approves.

CC (2026-10-30, Andrej): `TBD -> 2nd Tier`, priority 3 (the AI screening had `TBD -> Yes`, priority 3; zero-inflated
screening review page). "Try one last time to find a copy of the data somewhere. If not possible we set it to 2nd tier
because we would have to request the data first, otherwise we can rediscuss it. Would it make sense to add a decision
marker for data upon request?" No usable copy turned up (the GitHub copies break the competition's terms; see the
Assessment above), so the note's 2nd Tier applies; the request to HPN is the way in.

CC (2026-10-30, Andrej), in chat: `TBD -> Yes`, priority 3: "Data on request shall be a TBD then for the cases where it
mattered." The verdict rests on the merits; `Available on Request` records that the request is still to be made (EV-4:
access alone decides no verdict).

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
