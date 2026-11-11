---
unique_name: amazon_employee_access
name: Amazon_employee_access
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
tags:
- 'Samples: Over Time'
- 'Time: Lost'
- 'Target: Varying Delay'
original_source: Kaggle
year: '2013'
required_split:
- Random (IID)
problem_type: Binary Classification
source_links:
- https://www.openml.org/search?type=data&id=4135
- https://www.kaggle.com/c/amazon-employee-access-challenge
notebook_path: datasets/beyond_iid/old_iid/amazon_employee_access/amazon_employee_access.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/amazon_employee_access/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

I LOVE this dataset - we need to include it. BUT: Need to carefully check how the split in the Kaggle challenge was. Also could require time split - but it seems as if the task was conceptualized with time-invariant features

Potential issue: grouped data (manager-employees); test data was temporal (only on new employees!); problem in words: if the train samples in the kaggle data would have the same employee multiple times for multiple resources, then it breaks non-grouped/non-temporal assumptions

Lennart: Yes, if the groups are not a problem and we do not have repeated employee entries? Time should be ignorable as the processes did not change during collection (?);

Andrej: Fits criteria

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source roc_auc — Area Under Receiver Operating Characteristic Curve (https://www.kaggle.com/competitions/amazon-employee-access-challenge (Kaggle API evaluationMetric)).

CC (2026-11-11, Andrej): review marks on both issues, applied to the definition.

- Issue 1 (ok, keeping the call of 2026-11-10): `ROLE_CODE` is dropped in `_clean` and from the categorical list. It maps one to one onto `ROLE_TITLE` (343 values each, every title one code and every code one title), so the definition shipped one attribute twice (CLEAN-5); `known` now lists eight attributes and the last sentence of `fit_reason` reads "Kaggle's test requests come from the same requesters: 88.6% from a requester profile of its training file".
- Issue 2 (change, Option B): `data_tags = ("ForcedIIDFromTemporal",)` with its `Time basis:` bullet: requests were made one by one over 2010 and 2011, the release keeps no request date and Kaggle's training file is shuffled (denial rate flat over its tenths, chi-squared p = 0.45; the next row shares a requester profile no more often than in shuffled order), so random requests stand in for the requests to come (SPLIT-8, SPLIT-32). UCI 216's dated access history uses other ids and cannot date these rows.
- The folds do not change, so the IID framing kept for this dataset (requester profiles recur, as in the competition's own test, 88.6%) stands. `dataset check`: 0 errors, 0 warnings; not rebuilt. The review moved from the folder's `REVIEW.md` into this record's `## Review` section.

## Review

**Outcome:** added. Amazon's Kaggle competition of 2013: 32,769 requests by employees for access to a resource,
collected in 2010 and 2011, each described by the resource and the requester's manager and role (eight role codes);
the target is whether access was granted (94.2%), scored by ROC AUC, the competition's metric, on random requests.
The AI recommends shipping it after dropping `ROLE_CODE`, a relabelled copy of `ROLE_TITLE` (issue 1). Reviewed
without a review panel, from the gathered evidence: the record, a model run on the TabArena v0.1 version of the
same requests, the BeyondArena results and checks on the shipped data and on Kaggle's test file. Validity: the
definition keeps the competition's task and metric; most requesters recur, and denials cluster by requester, which a
random split rewards, but Kaggle's own test requests come from the same requesters even more often (88.6% against 84%
to 85% in our folds), so the random split mirrors the competition, as the split rules' case for this dataset already
says. Value: on six BeyondArena folds the methods spread from ROC AUC 0.812 (TabDPT) and 0.853 to 0.857 (linear model)
to 0.887 (LIMIX-2), with stable ranks (Kendall's W 0.97). Quality: one column copies another (issue 1). Weighed: a
real access-control decision with the host's metric and a clear spread +, codes without meaning and recurring
requesters -.

**Main points:** Both issues settled (2026-11-10): `ROLE_CODE` dropped (issue 1), the random split tagged forced from
temporal (issue 2); record `domain` set to business & marketing (2026-11-11). Nothing open.

**Record judgment:** valid. The use case is the host's: predict from the requester's role whether access would be
granted, to cut manual grants and revokes (fit `direct`). The early worry of the record ("test data was temporal (only
on new employees!)") does not hold for the requester profiles: of Kaggle's 58,921 test requests, 88.6% come from a
profile (the eight columns other than `RESOURCE`) seen in its training file, 97.2% from a manager seen there and all
from resources seen there, against 83.8% to 84.8% of the test requests of our random folds. The definition's
`fit_reason` says the competition's test held other employees; that sentence should go (Notes of issue 1). Our
experiments found that 90% of the requests share their requester profile with another, and a request is denied in 33%
of cases when another of the same profile's training requests was denied, 2% otherwise: the IID split rewards knowing
the requester, which a deployed model does for an existing employee, and the split rules list this dataset as a task
that keeps its IID framing and could get a grouped variant later. A simple model (penalised logistic
regression on the codes and their combinations, with the requester profile as a random effect) ranks first of 95
benchmark
methods on the v0.1 splits: a value note.

**Issues for Andrej:**

1. **Drop `ROLE_CODE`, a relabelled copy of `ROLE_TITLE`?**

   * **Problem:**
     - `ROLE_CODE` and `ROLE_TITLE` map one to one onto each other (343 values each), so the definition ships one
       attribute twice: drop `ROLE_CODE`, or keep both?
   * **Background:** checked on the shipped data, 32,769 rows: each title has one code and each code one title. The
     model run found the same, and the AutoGluon preprocessing its models run behind drops `ROLE_CODE` as a
     duplicate. The cleaning rules drop exact copies of another column[^1a].
   * **Effect on the task:** none on what can be predicted; a copied column gives methods that sample or weigh
     columns a double vote for one attribute.
   * **Consistency:** follows credit_approval's issue 2 of this round (`A4`, a relabelled copy of `A5`) and
     boreal_postfire_lichen_biomass (one-to-one recodings dropped).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep both (implemented) | nine code columns as published | the file as Amazon released it | one attribute twice |
     | B | Drop `ROLE_CODE` | eight columns; `ROLE_TITLE` keeps the information | no copied column | the checksum changes; a rebuild |

   * **Recommendation:** B, an exact copy of another column goes. **Decision:** keep both (A), or drop `ROLE_CODE`
     (B)?

   **Notes for the AI:** on B, drop `ROLE_CODE` in `_clean` and from the categorical list, add a `curation_comments`
   bullet; in either case replace the last sentence of `fit_reason` ("the competition's test held other employees")
   with "Kaggle's test requests come from the same requesters: 88.6% from a requester profile of its training file";
   `dataset check`; CHANGELOG entry.

   [^1a]: **CLEAN-5** (Should): drop constant columns, all-missing columns and exact copies of another column.

   **Resolved (2026-11-10, Andrej):** B: `_clean` drops `ROLE_CODE` and the categorical list no longer names it; a
   curation bullet says why; the task summary's `known` no longer lists the role code, and the last sentence of
   `fit_reason` now reads "Kaggle's test requests come from the same requesters: 88.6% from a requester profile of its
   training file". `dataset check` re-run.

   **Resolved (2026-11-11, Andrej):** his mark of today (ok, no note) keeps the state he decided on 2026-11-10, and
   that state is now on this branch too, which had the column still in: `_clean` drops `ROLE_CODE`, the categorical
   list no longer names it, the curation bullet says why, `known` lists eight attributes and `fit_reason` ends on
   Kaggle's test requests. Read as "keep what was decided", not as a return to option A, since no note asked for the
   copied column back. `dataset check`: 0 errors, 0 warnings; not rebuilt.

2. **Time basis: name the random split forced from temporal (`ForcedIIDFromTemporal`)?**

   * **Problem:**
     - Requests arrived one by one over 2010 and 2011, and the release keeps no time: Kaggle's training file is
       shuffled (the denial rate is flat over its tenths, chi-squared p = 0.45, and neighbouring rows share a
       requester profile no more often than shuffled rows do).
     - The record's collection facts fit what was found (`Samples: Over Time`, `Time: Lost`, `Target: Varying
       Delay`), but the definition names no time basis.
     - The use case decides the requests to come, and which roles get which resources changes as roles, managers and
       resources change, so of the time bases only the forced tag fits: name it, or another one?
   * **Background:** the questions that tell the time bases apart[^2a]:
     - Can time affect the target? Yes: an approval follows an organisation whose roles, managers and resources
       change.
     - Does the use case predict for a time after its data? Yes: the auto-access model decides new requests from
       requests already decided.
     - One shared prediction moment? No: each request is predicted when it is made, and the approver decides after a
       delay of their own.
     - Does arrival over time move the target? Argued from the source, as nothing dated can measure it: new resources
       appear and teams are reorganised; with the time lost that is the forced case[^2b].
     - Lineage: UCI 216 "Amazon Access Samples" (the same donor, 2011) has a dated access history, but it is a
       sibling, not the source of these rows: its requests run from March 2005 to August 2010, and its ids are another
       anonymisation (resource ids up to 35,217 against 312,153 here; 2% of Kaggle's resources and 11% of its
       managers match an id there, as chance gives), so it cannot date them.
   * **Experiments:** today's checks on Kaggle's `train.csv` (re-downloaded), model-free:

     | Check | Result |
     |---|---|
     | Denial rate per tenth of the file | 5.2% to 6.3%, no trend (chi-squared p = 0.45); lag-1 correlation 0.005 |
     | Next row with the same requester profile | 0.01% of rows, against 0.02% in shuffled order |
     | `RESOURCE`, `MGR_ID`, `ROLE_TITLE` against the row position | rank correlation at most 0.009 |

     - The leak test across a forced split[^2b]: no order to leak through, and no copy of a request; the requester
       profile recurs (84% of test requests share one with training, and denials cluster by profile, 33% against
       2%), which is the competition's own test (88.6%) and the framing kept for this dataset[^2c]. Whether requests
       of one period share their outcome cannot be tested without dates.
   * **Unknown:** whether the role and manager codes are as of the request or as of the extract (the competition
     speaks of "current employees" and "the manager of the current EMPLOYEE ID record"); if the extract, a requester's
     later role sits in an earlier request. Only Amazon could say.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | No time basis (implemented) | no time tag; `dataset check` notes a split that is not temporal and does not say why | nothing changes | the score's meaning in time is not stated |
     | B | Forced from temporal | the tag `ForcedIIDFromTemporal` and a `Time basis:` line naming 2010-2011, the shuffled file and what a dated release would change | says what the random score stands for; no fold changes, so the decided framing stays | none found |
     | C | Stationary relation | the tag `StationaryRelation` and a line arguing that access follows role and resource whenever it is asked for | none found | the organisation changes over two years; no dated data to measure it on |

   * **Recommendation:** B: a forward use case whose time is lost is what the forced tag names; the requester overlap
     stays the competition's framing, as decided. **Decision:** no time basis (A), forced (B) or stationary relation
     (C)?

   **Notes for the AI:** once PR #50 is in, on B: `data_tags = ("ForcedIIDFromTemporal",)` and the curation bullet
   "- Time basis: ForcedIIDFromTemporal: access requests made one by one over 2010 and 2011 (the competition's text);
   the release keeps no request date and Kaggle's training file is shuffled (denial rate flat over its tenths,
   chi-squared p = 0.45), so random requests stand in for the requests to come. UCI 216's dated access history uses
   other ids and cannot date them; a dated release would allow a split by request date."; no `splits_comment`
   (default split); the record's facts stay. Evidence: `~/claude_jobs/time_review/amazon_employee_access/`
   (`scripts/order.py`, `order.txt`, `uci216_note.txt`).

   [^2a]: **SPLIT-32** (Should): how and when samples, features and the target arrive is information for the split;
     the record keeps the source's collection facts, and a definition can name the use-case prototype it follows
     (`Timeless`, `Snapshot`, `DelayedTarget`, `StationaryRelation`) with a `Time basis:` line stating the fact behind
     it; a forward task whose time is lost or too short is forced.
   [^2b]: **SPLIT-8** (Must): a task temporal by its use case whose release cannot give the windows ships in the
     closest regime that keeps the rows, tagged as forced from temporal, after a leak test across the split: a row's,
     its unit's or its period's outcome shared with the other side, a hidden group, an order dependence.
   [^2c]: **SPLIT-31** (Should): over related entities, IID can match how a task is framed even when it is optimistic;
     amazon_employee_access is its case (IID kept, a candidate for a grouped or temporal variant).

   **Resolved (2026-11-10, Andrej):** B: `data_tags = ("ForcedIIDFromTemporal",)` and the drafted `Time basis:
   ForcedIIDFromTemporal:` bullet in `curation_comments` (requests of 2010-2011, the shuffled file, UCI 216 cannot date
   them). Split unchanged; record facts unchanged.

   **Andrej (2026-11-11, change):** Option B: Forced from temporal.

   **Resolved (2026-11-11, Andrej):** B, now carried by this branch, which has PR #50: `data_tags =
   ("ForcedIIDFromTemporal",)` and the drafted `Time basis: ForcedIIDFromTemporal:` bullet in `curation_comments`
   (requests made one by one over 2010 and 2011, the shuffled training file with its flat denial rate, chi-squared
   p = 0.45, and UCI 216's dated history, which uses other ids and cannot date them). No fold changes, so the IID
   framing the split rules keep for this dataset stays; the record's collection facts are unchanged.

## Reference

https://www.kaggle.com/c/amazon-employee-access-challenge
