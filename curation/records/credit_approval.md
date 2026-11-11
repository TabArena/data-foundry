---
unique_name: credit_approval
name: Credit Approval
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: Yes (Disagreement)
decision_markers:
- Outdated
- Not Representative
- Anonymized
tags:
- Tiny Data
- 'Samples: Over Time'
- 'Time: Lost'
collections:
- New (BeyondArena)
original_source: UCI
year: '1987'
domain: finance
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.24432/C5FS30
- https://doi.org/10.24432/C5259N
notebook_path: datasets/beyond_iid/new_iid/credit_approval/credit_approval.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/credit_approval/dataset.py
source_row: 775
type_adapter_id: curation-record-v1
---

## Comments

The UCI source contains two datasets, this is the crx dataset in the data

Credit Approval (690 rows), From a Japanese

**Assessment (AI, 2026-10-14):** The 690 rows are `crx.data`, Quinlan's Credit Approval (UCI 27; the source is "confidential", so the lender and country are not stated), not Japanese data. The same UCI zip holds the Japanese Credit Screening data (UCI 28, `credit.lisp`, 125 examples, Chiharu Sano 1992; the second source link, 10.24432/C5259N), which we do not use. Statlog (Australian Credit Approval) (UCI 143) is the same 690 applications with recoded values and filled-in missing values: its rows are those of `crx.data` in another order (four numeric columns and the label match as a multiset).

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Quinlan 1987 and the Statlog Australian study score error rate without costs or a threshold; accuracy rejected.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `hmda_mortgage_application_decision` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-11, Andrej): review marks applied (Review issues 1, 2 and 3); 15 attributes to 14, the 690 applications and the random split unchanged.

- Issue 1 (`ok`): ship as defined; nothing to change beyond issues 2 and 3.
- Issue 2 (B, "Option B: Drop A4."): `A4` is a relabelled copy of `A5` (u is always g in 519 rows, y always p in 163, l always gg in 2, and the same 6 rows are missing in both), so it is dropped and the categorical list no longer names it. Statlog's recoding of these applications (Australian Credit) also lacks the column.
- Issue 3 (B, "Option B: Forced from temporal."): `data_tags = ("ForcedIIDFromTemporal", "Anonymized")` with the `Time basis:` bullet in the notes: applications decided by a bank over a period Quinlan does not state, `crx.data` carrying no date or id and ordered in blocks of one class, so random applications stand in for the applications to come. A dated release would allow a split by application date. Split unchanged.
- `dataset check` passes (0 errors, 0 warnings).

## Review

**Outcome:** added. `crx.data` of UCI 27 (Quinlan 1987): 690 credit card applications to a confidential bank, the
label its past approval decision (44% `+`), all 15 attributes disguised as symbols. The AI recommends shipping it with
one small change: drop `A4`, a relabelled copy of `A5` (issue 2, new). Reviewed without a panel, from the gathered
evidence: the record, the earlier experiments of October, model runs on the shipped data, and one
descriptive check on 2026-11-04. Validity: the label imitates the bank's decision rather than repayment, and the
disguised attributes cannot be checked for timing (`fit` approximate, `Anonymized`); Andrej kept it on 2026-10-15,
agreeing with Lennart, and found no exclusion reason. Value: logistic regression 0.925, random forest 0.933 and TabPFN
0.939 ROC AUC on 60 splits, TabPFN ahead of the random forest on 53; `A9` alone gives 0.862, so not `Trivial`; of
the 40 benchmark methods the best scores 0.940 and the median 0.936, logistic regression 0.918 to 0.923. Quality:
`A4` and `A5` are one coding twice. Weighed: a documented source and a real lending decision +; 1987, a disguised
bank, an approval label, a crowded finance block, and a candidate with better data for the same kind of task -.

**Main points:** All three issues settled (2026-11-11): ship as defined (issue 1), `A4` dropped (issue 2), the random
split tagged forced from temporal (issue 3).

**Record judgment:** valid. Quinlan's own description (MIT AI Memo 930, 1986, p. 12: "provided by a large bank",
"two decision classes") confirms the label is the bank's decision; the markers `Outdated`, `Not Representative` and
`Anonymized` say what is weak. Statlog Australian Credit Approval (UCI 143) holds the same 690 applications recoded and
is rejected as `Duplicate`; this copy keeps the original values and the real missing values. A data scout found
`hmda_mortgage_application_decision` (screened `TBD -> Yes`, not added) as better data for a lender's approve-or-deny
decision; by our pattern this record keeps the verdict its own data earns.

**Issues for Andrej:**

1. **Ship in TabArena v0.2 as defined?**

   * **Problem:**
     - Andrej's review (CC 2026-10-15) kept the dataset, agreeing with Lennart, after weighing each possible reason to
       exclude it, and nothing found since contradicts that call.
     - The label imitates a bank's approval decision of the 1980s, and Statlog Australian Credit Approval (UCI 143)
       holds the same 690 applications recoded, which we do not ship.
     - Ship as defined, or name what is missing?
   * **Background:** the reasons Andrej weighed on 2026-10-15:
     - Disguised attributes are no requirement for inclusion and carry the `Anonymized` tag and marker (on `main`
       with PR #17, which merges before this branch).
     - The dominant `A9` (t/f; unofficial names call it "prior default", a community reading, not from Quinlan or
       UCI) leaves much to the other features: logistic regression without it scores 0.850.
     - The age of the data and the unnamed bank are the `Outdated` and `Not Representative` markers.
     - Finance's weight in the benchmark is a question of composition, not a defect of the data.
   * **Experiments:**
     - October 2026, 20 x 3 splits on `crx.data`: logistic regression 0.925, random forest 0.933, TabPFN 0.939 ROC
       AUC; TabPFN beats the random forest on 53 of 60 splits; `A9` alone 0.862.
     - Model runs on the shipped data (20 x 3 splits): the best benchmark method scores 0.940, the median
       0.936, logistic regression 0.918 to 0.923. A penalised additive scorecard with separate slopes for `A9` = t
       ranks 5th of 41 on its own and 1st blended with a small CatBoost (0.941), so the task is close to a scorecard
       and its spread is mainly linear against the rest.
   * **Consistency:** credit_g (small, old consumer credit) was kept after its code-table fix (2026-10-15); a
     `Duplicate` rejection of another copy is no precedent against this one.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Ship as defined (implemented) | 690 applications, 15 attributes, ROC AUC | a real lender's decisions with native missing values and mixed categoricals; methods separate | 1987, disguised attributes, an approval label; finance already has many tasks |
     | B | Retire | `No (Retired)`, a CC line, the folder removed | less weight on finance; leaves room for a modern approval task once one is added | no defect of the data found; reverses Andrej's and Lennart's keep |

   * **Recommendation:** A, Andrej's keep of 2026-10-15 stands: the methods spread, and no feature is shown to give
     the label away[^1a][^1b]. **Decision:** A or B?

   [^1a]: **TP-3** (Must): if tuned methods spread, keep the dataset.
   [^1b]: **TP-4** (Must): `Trivial` needs proof; the raw feature has to match the methods fold by fold.

   **Resolved (2026-11-11, Andrej):** A: ship as defined; nothing to change beyond issues 2 and 3.

2. **Drop `A4`, a relabelled copy of `A5`?**

   * **Problem:**
     - `A4` (u, y, l) maps one to one onto `A5` (g, p, gg): u is always g (519), y always p (163), l always gg (2), and
       the same 6 rows are missing in both.
     - The definition ships both, so every model sees one attribute twice.
     - Drop `A4`, or keep both?
   * **Background:** Statlog's recoding of these applications (Australian Credit) has 14 attributes, and the one it
     lacks is this column: its counts 519, 163 and 2 match `A4` (Michie D, Spiegelhalter DJ, Taylor CC, eds. Machine
     Learning, Neural and Statistical Classification. Ellis Horwood, 1994, Sec. 9.2.2; matched by an earlier check).
     `A10` (t/f) is exactly `A11` > 0 (295 and 395 rows), a flag derived from a count rather than a copy, so it
     stays.
   * **Effect on the task:** none on what can be predicted; a copied column gives methods that sample or weigh
     columns a double vote for one attribute.
   * **Experiments:** check of 2026-11-04 on `crx.data` (690 rows): the crosstab above, no exception. The
     model runs on the shipped data found the same and drop `A5` in their simple models.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep both (implemented) | `A4` and `A5` as published | the file as Quinlan released it | one attribute twice |
     | B | Drop `A4` | 14 attributes, as in Statlog | no exact copy; the remaining column holds all its information | the checksum changes; a rebuild |

   * **Recommendation:** B, an exact copy of another column goes[^2a]. **Decision:** A or B?

   **Notes for the AI:** on B, add `"A4"` to a `df.drop(columns=...)` in `_clean` and remove it from the categorical
   list; a `curation_comments` bullet with the crosstab; `dataset check`; CHANGELOG entry; rebuild on the curator's
   ask.

   [^2a]: **CLEAN-5** (Should): drop constant columns, all-missing columns and exact copies of another column.

   **Andrej (2026-11-11, change):** Option B: Drop A4.

   **Resolved (2026-11-11, Andrej):** B: `_clean` drops `A4` and the categorical list no longer names it; a curation
   bullet gives the crosstab; the task summary's `known` now says fourteen attributes, eight categorical. `dataset
   check` re-run.

3. **Time basis: name the random split forced from temporal (`ForcedIIDFromTemporal`)?**

   * **Problem:**
     - Applications reached the bank over a period Quinlan never states, and the release keeps no time: no date or
       id, and `crx.data` is ordered in blocks of one class (the next row has the same label in 97.8% of rows,
       against 50.6% by chance), an assembly order, not time.
     - The record's collection facts fit what was found (`Samples: Over Time`, `Time: Lost`, no target fact, as the
       label is the bank's decision on the application), but the definition names no time basis.
     - The use case decides the applications to come, and a bank's approval policy can change with the credit
       climate, so of the time bases only the forced tag fits: name it, or another one?
   * **Background:** the questions that tell the time bases apart[^3a]:
     - Can time affect the target? Yes: an approval follows the bank's policy of its day.
     - Does the use case predict for a time after its data? Yes: the lender decides new applications by imitating
       past decisions.
     - One shared prediction moment? No: each application at its own date, decided on arrival.
     - Does arrival over time move the target? Argued from the source, as nothing dated can measure it: lending
       policies change; with the time lost that is the forced case[^3b].
     - Is it one moment after all? The 690 could be one short batch, but no source says so; even then a `Snapshot`
       would fit only a use case that fills in decisions of that batch, not one that decides new applications.
     - A stationary relation would need the bank's policy to be unchanged over the period, which no source states.
   * **Experiments:** today's time probe on `crx.data`: no date-like column and no id, the raw order sorted by the
     class. The leak test across a forced split: no two applications share a feature vector, and no file order
     reaches the frame; whether applications of one period share their outcome cannot be tested without dates.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | No time basis (implemented) | `data_tags = ("Anonymized",)`; `dataset check` notes a split that is not temporal and does not say why | nothing changes | the score's meaning in time is not stated |
     | B | Forced from temporal | the tag `ForcedIIDFromTemporal` and a `Time basis:` line naming the unstated period, the class-sorted file and what a dated release would change | says what the random score stands for; the leak test finds nothing | none found |
     | C | Stationary relation | the tag `StationaryRelation` and a line arguing that the bank decided the same way throughout | none found | no source states an unchanged policy; no dated data to measure it on |

   * **Recommendation:** B: a forward use case whose time is lost is what the forced tag names. **Decision:** no time
     basis (A), forced (B) or stationary relation (C)?

   **Notes for the AI:** once PR #50 is in, on B: `data_tags = ("ForcedIIDFromTemporal", "Anonymized")` and the
   curation bullet "- Time basis: ForcedIIDFromTemporal: credit card applications decided by a bank over a period
   Quinlan does not state; `crx.data` has no date or id and is ordered in blocks of one class (assembly, not time), so
   random applications stand in for the applications to come. A dated release would allow a split by application
   date."; no `splits_comment` (default split); the record's facts stay. Probe output:
   `~/claude_jobs/time_review/b3_probe/credit_approval.json`.

   [^3a]: **SPLIT-32** (Should): how and when samples, features and the target arrive is information for the split;
     the record keeps the source's collection facts, and a definition can name the use-case prototype it follows
     (`Timeless`, `Snapshot`, `DelayedTarget`, `StationaryRelation`) with a `Time basis:` line stating the fact behind
     it; a forward task whose time is lost or too short is forced.
   [^3b]: **SPLIT-8** (Must): a task temporal by its use case whose release cannot give the windows ships in the
     closest regime that keeps the rows, tagged as forced from temporal, after a leak test across the split; it says
     what a dated release would change.

   **Andrej (2026-11-11, change):** Option B: Forced from temporal.

   **Resolved (2026-11-11, Andrej):** B: `data_tags = ("ForcedIIDFromTemporal", "Anonymized")` and the drafted `Time
   basis: ForcedIIDFromTemporal:` bullet in `curation_comments`; default split, no `splits_comment`; the record's facts
   stay.

## Reference

@article{quinlan1987simplifying,
  title={Simplifying decision trees},
  author={Quinlan, J. Ross},
  journal={International journal of man-machine studies},
  volume={27},
  number={3},
  pages={221--234},
  year={1987},
  publisher={Elsevier}
}
