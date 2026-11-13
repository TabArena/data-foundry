---
unique_name: naticusdroid_android_permissions_dataset
name: naticusdroid+android+permissions+dataset
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
- WIP (DF)
claimed_by: Andrej
suggestion: No (Retired)
decision_markers:
- Selection Bias
original_source: UCI
year: '2022'
required_split:
- Random (IID)
source_links:
- https://doi.org/10.24432/C5FS64
notebook_path: datasets/beyond_iid/old_iid/naticusdroid_android_permissions_dataset/naticusdroid_android_permissions_dataset.ipynb
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

permissions extracted from more than 29000 benign & malware Android apps released between 2010-2019. Can be used to create a malware detection system. Might require temporal split' recommended split si time-unaware

Potential issue: maybe temporal relationships

Lennart: I think the task can be understood as gap filling without a temporal split, as we might want to classify if an app released in the past is malware!

Andrej: Unclear whether temporal split

CC (2026-10-06, Lennart): Kept after the task-probe review: the `no_spread` flag (three untuned families at skill +0.962 to +0.968) does not hold for tuned methods. On BeyondArena the best (LimiX-2) reaches ROC AUC 0.989 and the median 0.986, with no other method within noise of the best (Kendall's W 0.96).

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Mathur et al. 2021 report accuracy, precision, recall and F1 on a balanced set with 75% duplicates; after deduplication we ship 35% malware, so the paper's accuracy does not mean the same (MET-2). roc_auc is the binary fallback.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `kronodroid_android_malware` (TBD -> Yes, priority 2), `drebin_android_malware` (TBD -> 2nd Tier, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship after two changes: one row per permission set with its majority label (our de-duplication left 96 opposite-label twins, a leak still in v0.2), and Selection Bias with an approximate fit (no malware app has any permission introduced 2015-2018). Priority 2: gap 0, use case 0, source 1, shape 1, risk -1.

CC (2026-11-12, Andrej): BeyondArena v0.2 review page, issues 2-4; the input data did not change (7,491 rows, repeated rows dropped as before). Issue 1 (the repeated permission sets) is still open.

**Changes made:**

1. **Problem:** no malware row declares a permission Android or Google Play introduced in 2015-2018 (FOREGROUND_SERVICE, the install-referrer service, REQUEST_INSTALL_PACKAGES, USE_FINGERPRINT), which 14.5% of the benign rows declare. The malware comes from AMD, the Android Malware Dataset, whose 71 families were discovered 2010-2016 (Md Rafid Islam and Mohammad Ashrafuzzaman Khan, "Diagnosing and Mitigating Domain Shift in Permission-Based Android Malware Detection", arXiv:2605.09028, 2026, Sec. 3.1; Fengguo Wei, Yuping Li, Sankardas Roy, Xinming Ou and Wu Zhou, "Deep Ground Truth Analysis of Current Android Malware", DIMVA 2017, LNCS 10327:252-276, doi:10.1007/978-3-319-60876-1_12). **Change:** marker `Selection Bias`, fit approximate, `dataset_pure_feature_value` accepted (issue 2, B).
2. **Change:** a `Time basis: Snapshot` bullet (apps of 2010-2019 classified after release); the tag enters `data_tags` once PR #50 is in the working copy (issue 3, B).
3. **Change:** tags `Samples: Over Time` and `Time: Lost` in place of `Samples: No Time Dimension` (issue 4, B).

**Problems found, not changed:**

- The de-duplication on all columns, label included, leaves 96 permission sets as one benign and one malware row, so a test row's twin in training always carries the opposite label; open as issue 1 on the review page, with the leak measurements of 2026-11-12.
- The release holds no hash, package name, family or date, so rows cannot be linked to their apps; variants of one AMD family sit on both sides of the random split.

CC (2026-11-13, Andrej): retired (`No (Retired)`, reason `Selection Bias`; BeyondArena v0.2 review page, issue 1, e).
- **Why:** what no version of this release can fix is the collection, not the lookup. The benign apps come from AndroZoo and the malware from AMD (families discovered 2010-2016), and the period shows in the permissions (ROC AUC 0.970 to 0.991 even without the 26 store, library and benign-only permissions). Test malware has family siblings in training. Both need per-app dates or ids, which the UCI file lacks.
- **Not the reason:** the exact lookup (79% of test apps on the full file, the opposite-label twins in the shipped 7,491 rows) is fixable without dates by dropping the repeated permission sets (7,299 rows), but that leaves the collection gap.
- **Replacement candidate:** `kronodroid_android_malware` (record `TBD -> Yes`, priority 2): 78,137 apps of 2008-2020 with per-app dates and 240 malware families, so it can test new apps and new families.
- The folder stays until the retirement PR removes it and clears `v2_path`; the claim stays. Priority removed.
- Sources: Mathur A, Podila LM, Kulkarni K, Niyaz Q, Javaid AY. NATICUSdroid: A malware detection framework for Android using native and custom permissions. Journal of Information Security and Applications 2021;58:102696, https://doi.org/10.1016/j.jisa.2020.102696. UCI, https://doi.org/10.24432/C5FS64. Wei F, Li Y, Roy S, Ou X, Zhou W. Deep Ground Truth Analysis of Current Android Malware. DIMVA 2017, LNCS 10327:252-276, https://doi.org/10.1007/978-3-319-60876-1_12.

## Review

**Outcome:** added. UCI's NATICUSdroid data (Mathur et al. 2021): Android apps of 2010-2019 described by 85 declared
permissions, labelled malware or benign; the definition drops the 75% of the file that repeats a row (29,332 to 7,491
rows, 35% malware) and splits at random. The AI recommends shipping it after two changes: one row per permission set
with its majority label, which removes a leak our de-duplication created (issue 1), and the `Selection Bias` marker
with an approximate fit, because the malware rows lack every permission introduced in 2015-2018 (issue 2). Reviewed
without a panel, from the gathered evidence: the record, the curator's task-probe decision of 2026-10-06, an
earlier leak analysis of TabArena's copy (the same 7,491 rows), its run on the shipped data, and one cheap check.
Validity: the permissions are known before an app runs; the de-duplication on all columns left 96 permission sets as
one benign and one malware row each, so a test row's training twin always carries the opposite label (issue 1); 14
permissions occur only in benign apps, four of them introduced by Android or Google Play in 2015-2018 (issue 2). Value:
on the shipped data the benchmark methods range from ROC AUC 0.989 (best) and 0.988 (TabPFN-3.5) over a median of 0.986
to 0.979 (random forest), logistic regression 0.981; close to the ceiling, but the curator found no method within noise
of the best (2026-10-06). Quality: nothing beyond the issues. Weighed: a documented malware set with permissions a
store sees before install (+), a leak we made and can undo (-), classes that look collected apart (-).

**Main points:** Retired on 2026-11-13 (issue 1, e): `No (Retired)` with `Selection Bias`, because the two
collections of different periods and the family siblings cannot be separated without app ids or dates;
`kronodroid_android_malware` is the dated replacement candidate. The folder leaves in a retirement PR. Issues 2-4
settled: `Selection Bias` with an approximate fit (2), a `Snapshot` of 2010-2019 (3), `Samples: Over Time` with
`Time: Lost` (4). Not rebuilt.

**Record judgment:** valid with the two changes. The curator's IID split ("gap filling": classify apps released in
the past) stands; issue 2 adds the measured reason why the record's early note ("might require temporal split") matters
anyway. The metric (ROC AUC, fallback) is settled. The data-scouting run of 2026-10-31 found better data for the same
task, `kronodroid_android_malware` (priority 2, per-app dates of 2008-2020) and `drebin_android_malware` (2nd tier),
screened in their own records and not added yet; KronoDroid's dates can test issue 2. The record has no `problem_type`
or `domain`; the definition's values can be filled in without a mark.

**Issues for Andrej:**

1. **Give each permission set one row with its majority label?**

   * **Problem:**
     - The definition drops repeated rows on all columns, the label included, so each of the 96 permission sets that
       UCI apps carry with both labels stays as exactly one benign and one malware row (192 rows, 2.6%).
     - A test app whose twin is in training therefore always has the opposite label, while among the UCI apps of these
       sets 90.6% carry their set's majority label, which is what a detector that knows earlier apps would see.
     - Keep the pairs, or give each set one row labelled by the majority of its apps?
   * **Background:** the UCI file has 29,332 apps, 74.5% of them exact copies of another row, which the paper does not
     mention. The 96 mixed sets hold 5,624 apps (19% of the file); their malware share runs from 0.7% to 98.4%: 30
     sets are mostly malware, 50 mostly benign, 16 tied (11 of them one app of each class). A feature may never give
     the target away, here by its reverse[^1a].
   * **Effect on the task:** a random split puts 35 to 48 test rows per split next to a training twin with the
     opposite label. A model that trusts exact matches, as a deployed detector should, is punished there: on those
     rows TabPFN-3.5 puts 55.6% of its probability on the wrong class, and a column holding the twin's label ranks
     them perfectly. LIMIX-2's first place on all rows comes from being less wrong on them.
   * **Experiments:** on the v0.2 rows (rebuilt from the UCI file with the definition's steps, 7,491 rows) the 96 sets
     occur exactly twice, each with both labels. From an earlier leak analysis (3 x 3 random splits, untuned
     LightGBM): adding the twin's label as a column takes 1-AUC from 0.0156 to 0.0119 (9 of 9 splits) on the current
     table; on the majority table the score is 0.0105 and the column reaches no row. TabPFN-3.5 with that column took
     26% off its error, all of it on the exposed rows.
   * **Consistency:** jm1 dropped every copy of a measure profile that occurs with both labels (176 rows, 1.6%). Here
     that is option C, which would drop the sets holding 19% of the apps, where the labels are a real ambiguity of the
     task rather than damage[^1b]; the majority keeps that region with the label the apps support.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the pairs (implemented) | 7,491 rows; 96 sets as one benign and one malware row | the release as de-duplicated so far | the twin's label is the wrong answer by construction; rewards distrusting exact matches |
     | B | One row per set, majority label | 7,379 rows; the 80 sets with a majority keep one row with that label; the 16 tied sets dropped | no twins; the label a detector would see; the 7,299 rows without a twin unchanged | uses the labels once to resolve copies; 112 rows fewer |
     | C | Drop every twin row | 7,299 rows | label-free and simple; as jm1 | drops the 96 hardest sets (19% of the apps) |
     | D | All UCI rows, grouped by set | 29,332 rows; split grouped on the permission set | closest to the collected apps | a different, four times larger task; groups of up to 2,009 apps; whether copies are distinct apps is not documented |

   * **Recommendation:** B: it removes the leak and keeps the ambiguous sets with the label most of their apps carry,
     at a cost of 112 rows. **Decision:** keep the pairs (A), majority label (B), drop the twins (C), or the full file
     grouped by set (D)?

   **Notes for the AI:** on B, in `_clean` after the rename: group the UCI rows on all permission columns, take the
   majority of `Malware` per group, drop the groups with a tie, then drop `BADGE_COUNT_READ` (an exact copy of
   `BADGE_COUNT_WRITE`); expect 7,379 rows, 852 to 853 malware per test fold. The `dataset_conflicting_duplicate_rows`
   warning goes. Update `row`, `changes`, the curation notes and the record; CHANGELOG entry; rebuild on the curator's
   ask.

   [^1a]: **LEAK-10** (Must): a feature holds only what existed at the prediction point and never gives the target
     away.
   [^1b]: **LEAK-20** (Should): feature vectors that occur with both labels: drop every copy, unless they are genuine
     label ambiguity the task has (case: jm1).

   **Answer (AI, 2026-11-06):**

   * **What changed:** the new rules give repeats of a unit the data does not record one of four verdicts, set by
     three tests[^1c]. Apps that declare the same permissions read as distinct apps, the natural verdict, so the
     definition's removal of repeated rows is a drop of natural look-alikes, and a drop has to show what it does to the
     target[^1d].
   * **Verdict: natural.** It holds clearly for the benign repeats and the mixed sets; for the malware repeats it rests
     on reading a family's variants as distinct apps.
     - **The link is a shared make-up, far above chance:** 21,937 of the 29,332 apps (74.8%) repeat an earlier app's
       set, against 1,567 with each permission shuffled within its class and 11,010 when each class keeps its
       strongest links between permissions (200 draws each). Repeats are densest among apps with few permissions (97%
       of those with 0 to 3), but half of the apps with 16 or more repeat too. The largest set, 2,009 apps (94%
       benign), declares 2 permissions; the next six are all malware, 370 to 1,171 apps sharing one set of 8 to 15
       permissions each, the mark of one malware family or kit.
     - **The label goes with the set about as with similar sets:** pairs of apps with the same set share the label in
       93.5% of cases, one permission apart in 87.5%, two apart in 83.0%, against 50% from the class shares. The 96
       sets with both labels (5,624 apps) are distinct apps by construction, as one app cannot carry two labels.
     - **The malware repeats come in batches:** the file is a benign block followed by a malware block. In the benign
       block two rows of one set sit next to each other 280 times, as in a random order (292); in the malware block
       2,559 times against 206. The malware was stored set by set, most likely by family, which fits distinct
       variants of one family and also one app gathered more than once; with no hash, package name or date the
       release cannot tell which.
   * **What the drop does to the target:**
     - It removes 82.1% of the malware apps and 66.7% of the benign ones, so the malware share falls from 50.1%
       (14,700 of 29,332 apps) to 35.0% (2,624 of 7,491 rows); B gives 34.7%, C 34.6%.
     - It changes what a row stands for, from an app to a permission set: the 2,009 apps of the commonest set count
       once, like a set held by one app, so the test leaves out the apps whose exact set is already labelled, the easy
       cases in use (`fit_reason` says so).
     - Neither share is the one a store meets (the authors balanced the file), and ROC AUC does not depend on it; what
       changes is the unit scored. **Question:** does a table of distinct permission sets still stand for "is this
       released app malware", or should the rows be the apps?
   * **A full-file random split as an option row:** yes, as E, since it is what the natural verdict gives.
     - Random 3-fold splits (3 repeats): 79.4% of test apps have their set in training, and the training apps'
       majority label is right for 97.6% of them (ROC AUC 0.993 for that lookup).
     - It removes the opposite-label twins without using the labels: the 96 mixed sets keep every app with its own
       label.
     - The methods still separate, nearer the ceiling (three quick models on the same 9 splits, the benchmark methods
       not run): 1 - ROC AUC 0.0065 for gradient boosting, 0.0066 for a random forest and 0.0112 for logistic
       regression on the full file, against 0.0148, 0.0226 and 0.0191 on the shipped rows. Boosting beats logistic
       regression on 9 of 9 splits on both, but ties the forest on the full file (5 of 9). On test apps whose set is
       not in training the full-file models reach ROC AUC 0.981 to 0.986.
     - D now groups on the feature vector itself, standing in for an unknown unit, which the rules bar[^1e].
   * **Consistency:** E follows sepsis_survival_minimal_clinical_records and
     ai4d_lab_tanzania_tourism_classification_challenge, which keep repeated profiles of distinct people with a random
     split[^1f].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the pairs (implemented) | 7,491 rows, 35.0% malware; 96 sets as one benign and one malware row | the release as de-duplicated so far | the twin's label is the wrong answer by construction; a row is a set, not an app |
     | B | One row per set, majority label | 7,379 rows, 34.7% malware | no twins; each set once | uses the labels to resolve copies; drops natural look-alikes, 82% of the malware apps |
     | C | Drop every twin row | 7,299 rows, 34.6% malware | label-free | drops the 96 hardest sets (19% of the apps) |
     | D | All apps, grouped by set | 29,332 apps; groups of up to 2,009 | keeps every app | groups on the feature vector itself, which the rules bar |
     | E | All apps, random split | 29,332 apps, 50.1% malware; copies kept; 79% of test apps share their set with a training app | the natural verdict; the apps the use case scores; no twins, without using labels; the methods still separate | near the ceiling, the two tree models tie; the malware batches may hold one app more than once |

   * **Recommendation:** changes from B to E: the mixed sets show that repeated sets hold distinct apps, the benign
     repeats have no order, a store sweeping released apps meets the variants of known families, and E removes the
     twins without touching the labels; B if you read the malware batches as one app counted many times.
     **Decision:** keep the pairs (A), majority label (B), drop the twins (C), grouped by set (D) or all apps with a
     random split (E)?

   **Notes for the AI:** on E, in `_clean` remove `drop_duplicates` (keep the `BADGE_COUNT_READ` drop); `row` (29,332
   apps), `changes`, `split` (random apps; 79% of test apps share their set with a training app) and `fit_reason`
   (drop the sentence on each set counting once); the metric reason's "after deduplication we ship 35% malware" (now
   50%); the `dataset_conflicting_duplicate_rows` warning accepted with the 96 mixed sets as real ambiguity; a curation
   bullet "- Entity leakage, natural (2026-11-06): 74.8% of the apps repeat an earlier app's permission set, far above
   chance (1,567 with permissions shuffled within class, 11,010 keeping each class's strongest links), as apps built
   the same way; same-set pairs share the label in 93.5% of cases against 87.5% one permission apart, and 96 sets hold
   both labels, so the repeats are distinct apps. The malware block keeps a set's apps together (2,559 neighbouring
   pairs against 206 in a random order), likely by family; without hashes, variants and re-collected apps cannot be
   told apart. Under random 3-fold splits 79% of test apps share their set with a training app." Re-run issue 2's
   counts and rewrite issue 3's `Snapshot` line (the repeats kept, not dropped) on the full file; CHANGELOG entry;
   `CC (<date>, Andrej):` line in the record; rebuild on the curator's ask.

   [^1c]: **LEAK-41** (Must, draft PR #62): repeats of a unit the data does not record are natural (distinct
     look-alikes: the random split stays and the notes give the overlap), an entity fix, a temporal fix, or not
     recoverable (identifiable copies dropped). **LEAK-42** (Should, draft PR #62): three tests set the verdict:
     matches against a chance rate that keeps the data's structure, label agreement against what the shared features
     predict, and an order; records of one unit side by side in the file are more often copies entered together.
   [^1d]: **LEAK-41** (Must, draft PR #62): every drop gives the share dropped and the label shares before and after,
     and asks whether the target still stands for the use case. **LEAK-19** (Should): copies uneven by class give the
     share per class and the class balance after the drop.
   [^1e]: **SPLIT-24** (Must): group on a true group id or one constructed from the data, never on a hash of the
     feature vector standing in for an unknown entity (maternal_health_risk).
   [^1f]: **LEAK-18** (Should): few features and plausible repeats are natural: keep them and say so
     (sepsis_survival_minimal_clinical_records keeps 110,204 rows over 975 distinct feature rows;
     ai4d_lab_tanzania_tourism_classification_challenge its 965 exact copies, Lennart, 2026-11-05).

   **Andrej (2026-11-12, discuss):** If there is a leak it should be fixed. Also, I don't understand your
   recommendation. How can it be that same samples appear with different targets, you should find the source and give
   me the correct feature-label pairs.

   **Answer (AI, 2026-11-12):** Identical rows are different apps, and the UCI file already holds the correct pairs;
   keeping every app (E) removes the leak.

   * **Problem:**
     - The file stacks two collections: rows 1-14,632 are benign apps from AndroZoo, rows 14,633-29,332 malware apps
       from AMD, the Android Malware Dataset (71 families discovered 2010-2016, each sample flagged by at least half
       of VirusTotal's scanners)[^1g]. Each row is one app with its collection's label.
     - The release keeps only 85 yes/no permissions per app, so two different apps that request the same of these get
       the same row: 2,009 apps request only INTERNET and ACCESS_NETWORK_STATE, 1,895 benign and 114 malware.
     - No row can be traced to its app: the UCI file and page carry no hash, package name or date, the authors' code
       holds only a trained model, the paper is paywalled and AMD's site is offline. None needs it: each row already
       carries its own app's label.
     - The leak was ours: the de-duplication on all columns, label included, cut each of the 96 mixed sets to one
       benign and one malware row, so a test row's twin in training always carried the opposite label.

     | | Apps | Benign (AndroZoo) | Malware (AMD) | Permission sets |
     |---|---|---|---|---|
     | UCI file, every app (E) | 29,332 | 14,632 | 14,700 | 7,395 |
     | in sets with one label | 23,708 | 10,245 | 13,463 | 7,299 |
     | in sets with both labels | 5,624 | 4,387 | 1,237 | 96 |
     | shipped so far (A, de-duplicated) | 7,491 rows | 4,867 | 2,624 | 7,395 |

   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | All apps, random split (E) | 29,332 apps, each with its own label | the correct pairs; no twin with a forced opposite label | 79% of test apps share their set with a training app, as look-alikes; near the ceiling (1 - ROC AUC 0.0065 boosting, 0.0112 logistic regression) |
     | b | One row per set, majority label (B) | 7,379 rows | no twins | gives 530 apps of the mixed sets the other class's label |
     | c | Drop the mixed sets (C) | 7,299 rows | label-free | drops 5,624 correct pairs, the hardest 19% of the apps |

   * **Recommendation:** a: the only fix that keeps every app's own label; A keeps the leak, and D groups on the
     feature vector, which the rules bar[^1h]. **Decision:** a, b or c?

   [^1g]: Islam and Khan 2026, "Diagnosing and Mitigating Domain Shift in Permission-Based Android Malware
     Detection", arXiv:2605.09028 (https://arxiv.org/abs/2605.09028), Sec. 3.1: "14,700 malware from Argus Lab's AMD
     and 14,632 benign applications from Androzoo"; the counts match the file's two blocks. AMD: Wei et al. 2017,
     "Deep Ground Truth Analysis of Current Android Malware", DIMVA (https://cse.usf.edu/~xou/publications/dimva17.pdf),
     24,650 samples. The NATICUSdroid paper (https://doi.org/10.1016/j.jisa.2020.102696) is paywalled; the UCI page
     (https://doi.org/10.24432/C5FS64) and the authors' code (https://github.com/akshaymathur05/Naticus_Test) name no
     source.
   [^1h]: **LEAK-18** (Should): few features and plausible repeats are natural: keep them and say so. **SPLIT-24**
     (Must): never group on a hash of the feature vector standing in for an unknown entity.

   **Andrej (2026-11-12, chat):** Why is naticus droid all resolved? I found it to be leaky and wanted answers.

   **Answer (AI, 2026-11-12):** The shipped rows (A) are leaky, by our own de-duplication, and the full file (E) is
   not, but most of E's score is a lookup of look-alike apps: which version should ship?

   * **Problem:**
     - Issue 1 was closed by mistake on your note; the definition is back to the shipped 7,491 rows (A), with issues
       2-4 applied.
     - In A an exact match in training always carries the opposite label (the 96 twin pairs), and a rule that
       predicts that label cuts the error by a quarter.
     - E keeps every app with its own label, so no such rule works, but 79% of its test apps have their exact
       permission set in training (median 40 apps), and a lookup of those labels gets 97.6% of them right.
   * **Experiments:** LightGBM (untuned) and logistic regression, ROC AUC, mean over the shipped split (stratified
     random 3-fold, 3 repeats, seed 4267).

     | Test rows scored | LightGBM | Logistic regression |
     |---|---|---|
     | A, all (as shipped) | 0.9846 | 0.9808 |
     | A, the 192 twin rows | 0.381 | 0.493 |
     | A, the other rows | 0.9891 | 0.9864 |
     | A, with "opposite of the twin" laid over the model | 0.9883 | 0.9854 |
     | A without the twin rows (7,299 rows) | 0.9894 | 0.9865 |
     | E, all apps | 0.9939 | 0.9888 |
     | E, set seen in training (79% of test apps) | 0.9952 | 0.9905 |
     | E, set not seen (21%) | 0.9868 | 0.9815 |
     | E, lookup for seen sets, the model for the rest | 0.9923 | 0.9918 |

     - **(a) Twins in A:** on the 44 test rows per fold whose twin is in training, LightGBM puts 57% of its
       probability on the wrong class; the opposite rule is right on all of them and takes 1 - AUC from 0.0154 to
       0.0117 (logistic regression 0.0192 to 0.0146), on 9 of 9 splits.
     - **(b) Repeats in E:** with LightGBM a permission set not seen in training scores 0.987 to 0.989 in every
       version, so E's 0.994 comes from the lookups; with a lookup for seen sets, logistic regression comes within
       0.0021 of LightGBM.
     - **(c) The two collections:** the four permissions introduced 2015-2018 carry almost nothing, and without
       every store, badge-library or benign-only permission the models still reach 0.970 (A) and 0.991 (E):

       | Permissions used | A, LightGBM | A, logistic regression | E, LightGBM |
       |---|---|---|---|
       | all 85 | 0.9846 | 0.9808 | 0.9939 |
       | only the 4 introduced 2015-2018 | 0.572 | 0.572 | 0.537 |
       | all but those 4 | 0.9835 | 0.9792 | 0.9938 |
       | only 26 store, badge-library or benign-only ones[^1i] | 0.858 | 0.858 | 0.763 |
       | all but those 26 | 0.9704 | 0.9595 | 0.9906 |

     - The period still runs through other permissions: without the four, benign apps that declare one of them
       are told from the malware with half the error of the other benign apps (1 - AUC 0.009 against 0.018,
       LightGBM on A).
     - **(d) Family siblings:** AMD's 71 families are uneven (Airpush alone is 32% of its 24,650 samples; 23
       families of 100 or more hold 95.5%), so if the file's 14,700 malware apps are a proportional sample, a
       random split leaves about 0.02% of test malware without a family sibling in training, in A and E alike.
     - The file has no family id and its order gives none: holding out stretches of the malware block costs 0.003
       to 0.005 (E 0.9894, A 0.9819, LightGBM), and 79% of the held-out malware in E still finds its exact set in
       training. Grouping on the permission set is barred[^1j], so the split scores variants of known families.
   * **Is it leaky?**
     - A: yes, a leak we made; 192 rows (2.6%) hold a quarter of the error.
     - E: no constructed leak; AndroZoo and AMD are collections of distinct app files, so a repeat is another app,
       version or family variant with the same 85 permissions, which a store sweeping published apps meets (issue
       3, `Snapshot`). It would be a leak only if one file were counted twice, which the release, without hashes,
       cannot show.
     - Issue 2 stays B: the class is not just the collection (0.970 without the 26), and the period gap that runs
       through the rest is what the `Selection Bias` marker names; (c) gives no reason to retire.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Keep A (implemented) | 7,491 rows with the 96 twin pairs | no change | leaky: the opposite rule cuts the error by a quarter |
     | b | Drop the twin rows | 7,299 rows, each permission set once with its single label | no leak, without using labels; no exact repeat across the split; scores new permission sets | drops the 96 sets that both classes declare (5,624 apps, 19%), an ambiguity the task has |
     | c | Every app (E) | 29,332 apps, each with its own label | the correct pairs; no constructed leak; the unit a store scores | 79% of test apps are lookups; the methods separate partly by how well they memorise sets |
     | d | Every app without the four later permissions | E with 81 permissions | removes a period marker | buys nothing (0.9938 against 0.9939); the period runs through other permissions too |
     | e | Retire: the class is the collection | `No (Retired)` | no two-collection task | not supported: 0.970 to 0.991 without the 26 store, library and benign-only permissions |

   * **Recommendation:** c: it fixes A's leak with the pairs the source gives, and the lookups it adds are the
     look-alikes the `Snapshot` use meets; b if you read an exact repeat across the split as leakage, or want the
     score to rest on new permission sets only. **Decision:** keep A (a), drop the twins (b), every app (c), every
     app without the four later permissions (d), or retire (e)?

   **Notes for the AI:** on c, the edit of 2026-11-12 (`dataset check` 0 errors, 0 warnings), with issue 2's counts on the full file (7.5% of benign apps) and issue 3's bullet as
   written there; the record CC line gets the issue 1 item back. On b: in `_clean` after `drop_duplicates`, drop
   every row whose permissions occur with both labels (7,299 rows); the `dataset_conflicting_duplicate_rows` warning
   goes; `row`, `changes`, the Time basis bullet (no twins) and the 14.5% re-counted. On d: c, then drop the four
   columns and reword `fit_reason` and the warning. On e: the retirement steps of the brief.

   [^1i]: Six Google Play and Play-services permissions (billing, licence check, push messaging, install referrer,
     activity recognition, Google services), the 15 that the ShortcutBadger badge library declares, and the 14 that
     no malware app declares (nine of them among the first 21).
   [^1j]: **SPLIT-24** (Must): group on a true group id or one constructed from the data, never on a hash of the
     feature vector standing in for an unknown entity (maternal_health_risk).

   **Andrej (2026-11-13, discuss):** The look up is clearly a leak. To me it seems as if we can't resolve it without
   temporal information, so I lean towards retiring it, what do you think?

   **Answer (AI, 2026-11-13):** I agree with retiring, but not because of the lookup: dropping the repeated sets (b)
   removes the lookup without dates. What no version of this release can fix is the rest: test malware has family
   siblings in training, and the two classes come from two collections of different periods. Both need app ids or
   dates, which the file lacks. KronoDroid has both.

   | Problem | Fixable without dates? | How, or why not |
   |---|---|---|
   | exact lookup (E: 79% of test apps, 97.6% right) | yes | b: each permission set once, mixed sets dropped (7,299 rows); no test set is in training; LightGBM 0.9894, LR 0.9865, as for unseen sets in E (0.987-0.989) |
   | family siblings (about 99.98% of test malware) | no | no family id or hash in the file; AMD labels families by SHA-256, so they cannot be joined |
   | two collections (benign AndroZoo, malware AMD 2010-2016) | no | no per-app date; the period shows in the permissions (0.970-0.991 without the 26 store, library and benign-only ones; issue 2) |

   * **The lookup is fixable:** the rules we have now say to drop exact copies over many binary features (85
     permissions), and to drop every copy of a vector that carries both labels[^1k]. That gives b and needs no
     dates. "Score only unseen sets" gives the same rows: in b, every test set is new.
   * **Grouping on the permission set:** barred with no exception. SPLIT-24 allows a key "constructed exactly from
     the data" only from columns that define the entity, and here different apps share one permission set. When the
     real groups matter and cannot be recovered, SPLIT-25 says to retire rather than group on a guess.
   * **Family labels:** AMD (Wei et al. 2017) names a family per sample hash, and the UCI file has no hash, package
     name or row order to join on (issue 1, 2026-11-12). Matching on permissions would be a guess.
   * **Dates:** AndroZoo dates each app by SHA-256 and AMD gives first-seen years per family; neither can be joined
     to these rows. No public version of NATICUSdroid with hashes turned up (UCI ships one `data.csv`).
   * **Value after b:** 0.986-0.989 on new permission sets, near the ceiling. Boosting leads logistic regression by
     0.003, and what that rewards is partly the period gap.
   * **Replacement:** `kronodroid_android_malware` (record, `TBD -> Yes`, priority 2) has 78,137 apps of 2008-2020
     with per-app dates and 240 malware families, so it can test new apps and new families.
   * **Marker:** `Selection Bias`. Its own definition, "cases and controls collected apart or in different periods",
     is the reason that cannot be fixed here; the record already carries it from issue 2. `Class-dependent Recording`
     does not fit: both classes are measured alike. The vocabulary has no leak marker, and the lookup would not be the
     reason anyway.

   | | Option | What it does | Pro | Con |
   |---|---|---|---|---|
   | a | Keep A (implemented) | 7,491 rows with the 96 twin pairs | no change | the leak we made |
   | b | Drop the twins | 7,299 rows, each set once with its single label | no lookup, without dates; the rules' answer for exact copies | family siblings and the collection gap stay; near the ceiling |
   | c | Every app (E) | 29,332 apps | each app keeps its own label | 79% of test apps are lookups |
   | e | Retire | `No (Retired)` with `Selection Bias`; folder left for the retirement PR; KronoDroid weighed as the replacement | no task whose score rests on collections and families it cannot separate | no Android malware task until KronoDroid is added |

   * **Recommendation:** e, as you lean, with `Selection Bias` as the reason and KronoDroid as the replacement. Choose
     b if you want to keep a task until KronoDroid is in: it is the only version without the lookup. **Decision:**
     retire (e), drop the twins (b), every app (c) or keep A (a)?

   [^1k]: **LEAK-18** (Should): many degrees of freedom and an exact match are a collection artefact: drop it and give
     the share. **LEAK-20** (Should): feature vectors that occur with both labels: drop every copy, unless they are
     genuine label ambiguity the task has. **SPLIT-25** (Must): when the real groups matter and cannot be recovered,
     retire the dataset rather than group on a guess.

   **Andrej (2026-11-13, discuss):** Reply (e): Retire

   **Resolved (2026-11-13, Andrej):** e: record `suggestion` `No (Retired)` (`data_foundry_status` keeps `DF: Yes`
   and `BeyondArena`), priority removed. The reason is `Selection Bias`, already on the record from issue 2: benign
   and malware apps come from two collections of different periods, and test malware has family siblings in
   training, and neither can be fixed without app ids or dates. No second marker: `Class-dependent Recording` does
   not fit (both classes are measured alike), and the lookup, the only leak, is fixable (b), so it is not the reason.
   CC line names `kronodroid_android_malware` (78,137 apps of 2008-2020 with per-app dates and 240 families) as the
   dated replacement candidate. The folder and `v2_path` stay until a retirement PR removes them; the claim stays.
   Split and metric marked ok. Not rebuilt.

2. **Mark the classes as collected apart, or retire the dataset for data with dates?**

   * **Problem:**
     - Fourteen permissions occur only in benign apps (the open `dataset_pure_feature_value` warning), among them four
       that Android or Google Play introduced in 2015-2018, which 14.5% of the benign apps and none of the 2,624 malware
       apps declare.
     - So the malware rows look older than the benign ones, or come from outside Google Play, and permissions that
       came or went with Android versions and store libraries separate the classes beside what the apps do.
     - Keep the dataset with the gap named, or retire it until data with dates replaces it?
   * **Background:** the four are `FOREGROUND_SERVICE` (Android 9, 2018), Google Play's install-referrer service
     (2017), `REQUEST_INSTALL_PACKAGES` (Android 6, required from apps targeting Android 8, 2017) and `USE_FINGERPRINT`
     (Android 6, 2015); in the full UCI file 114, 696, 228 and 279 benign apps declare them and no malware app does.
     The other ten benign-only permissions are phone makers' launcher badge permissions (Huawei, Oppo, Sony, Samsung
     and others), which a badge library adds to an app. The reverse holds for old ones: `RESTART_PACKAGES` (deprecated
     in 2010) is declared by 14.0% of malware and 1.9% of benign apps, Google's cloud push messaging by 3.7% of
     malware and 58.9% of benign apps. The paper says only that the apps were "collected during 2010-2019".
   * **Effect on the task:** `REQUEST_INSTALL_PACKAGES` is what a dropper (malware that installs further apps) declares
     on Android 8 and later, and here it marks an app as benign; a detector that sweeps apps of the same years meets
     recent malware with such permissions, so the score overstates how well recent malware is found.
   * **Experiments:** a check on the v0.2 rows (5 folds): ROC AUC with all 85 permissions 0.981 (logistic regression)
     and 0.986 (gradient boosting); without the four dated ones 0.979 and 0.985; without all 14 benign-only ones 0.978
     and 0.985; "declares any of the 14" alone 0.62. The dated permissions are not what carries the score, and whether
     the rest also carry the period cannot be told without dates.
   * **Unknown:** the apps' dates, or the sources of each class in the paper (paywalled; its NDSS 2021 poster and the
     UCI page give only "2010-2019"). Malware often targets old Android versions, so that every permission is granted
     at install, and is spread outside Google Play, so part of the absence may be behaviour, not period.
     `kronodroid_android_malware`, with per-app dates, would settle it once added.
   * **Consistency:** website_phishing (phishing and legitimate sites from two lists) and superconductivity (only
     superconductors) carry the `Selection Bias` marker with an approximate fit and stay (Lennart, 2026-10-27)[^2a].
     Retiring would follow the rule for an artefact that runs through several features a practical model would use
     and cannot be undone[^2b]; that rule is written for recording artefacts, and here the measurements are alike and
     the sampling differs.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep as is (implemented) | fit direct; the warning stays open | no change | states a fit the data contradicts; the warning has no decision |
     | B | Keep, name the gap | record marker `Selection Bias`; fit approximate; `fit_reason` names the missing 2015-2018 permissions among malware; the warning accepted with that reason | follows the other collected-apart datasets; holds under both readings (older malware, or malware outside Google Play) | the benchmark still rewards the period or store signal |
     | C | Retire, wait for dated data | record `No (Retired)` with `Selection Bias`; folder removed; KronoDroid considered as the replacement | no task whose classes may differ by period | loses a documented malware task on a suspicion that dates would have to confirm |

   * **Recommendation:** B: dropping the dated permissions hardly moves the score, a behavioural reading fits the same
     numbers, and the dates that would decide it are not in the data; C if you read the period as running through the
     whole permission set. **Decision:** keep and name the gap (B), keep as is (A), or retire (C)?

   **Notes for the AI:** on B, add the marker to the record, set `fit="approximate"` with a `fit_reason` sentence such
   as "No malware app declares a permission Android or Google Play introduced in 2015-2018 (FOREGROUND_SERVICE, the
   install-referrer service, REQUEST_INSTALL_PACKAGES, USE_FINGERPRINT), which 14.5% of benign apps declare, so the
   malware looks older or from outside Google Play, and such permissions mark the benign class", and accept
   `dataset_pure_feature_value` with the same reason. If issue 1 takes B, re-run the counts on the 7,379 rows first.

   [^2a]: The `Selection Bias` marker: the rows are not drawn from the population the use case predicts for, so a
     class looks different there; the verdict usually stays Yes and `fit_reason` names the gap.
   [^2b]: **LEAK-15** (Must; amended 2026-10-27, Andrej, on gallstone_disease): a recording artefact that runs
     through several features that would matter for prediction in practice, and that cannot be undone, retires the
     dataset.

   **Resolved (2026-11-12, Andrej):** B: record marker `Selection Bias`; `fit="approximate"` with the drafted
   `fit_reason` sentence on the shipped rows (14.5% of the benign rows declare one of the four dated permissions;
   shortened to stay under 70 words); `dataset_pure_feature_value` accepted with the same reason; record CC line.
   Counted on the de-duplicated rows while issue 1 is open; on the full file the share is 7.5% of benign apps.

3. **Time basis: name the random split a `Snapshot` of 2010-2019, or forced from temporal?**

   * **Problem:**
     - The apps were released over 2010-2019 and the release keeps no date: the raw file is sorted by class, and inside the malware half the share of apps declaring `RESTART_PACKAGES` (deprecated in 2010) jumps from under 1% to 13-27% in the last four tenths, collections stacked by source rather than a calendar.
     - The record says `Samples: No Time Dimension` (issue 4); the definition splits at random and names no time basis; Lennart reads the task as gap filling (classify apps already released), and Andrej left the split open.
     - Under gap filling the split is a `Snapshot` of 2010-2019; under detecting newly released apps it is forced from temporal, since malware adapts and the dates are lost[^3a].
   * **Background:**
     - The definition's question is "Is an Android app that is already released malware", the gap-filling reading;
       the benign half of the raw file shows no drift along its order (each of the dated permissions flat across
       its tenths).
     - Read literally, the first of the five questions gives `Timeless`: an app is malware or not whenever it is
       scanned. Issue 2 shows why that misleads: the classes differ by period (no malware app declares a permission
       introduced in 2015-2018), which a `Timeless` basis would hide.
     - The check a `Snapshot` asks for, whether a sample of the test sample's time carries its label: 75% of the UCI
       rows repeat another row (dropped), the 96 opposite-label twins are issue 1, and with no app id or family,
       variants of one malware family across the split cannot be told from apps that happen to ask the same
       permissions.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | No time basis (implemented) | as now | nothing to write | `dataset check` notes a split that is not temporal without a basis; the open question on the record stays open |
     | B | Snapshot of 2010-2019 | `Snapshot` and a `Time basis:` line naming the period and the gap-filling use | follows the definition's question and Lennart's call; states the period | a detector of new apps is not what it scores |
     | C | Forced from temporal | `ForcedIIDFromTemporal` and its line | states that new apps are what a detector meets and the dates are missing | departs from the definition's question; needs `use_case` reworded |
     | D | Timeless | `Timeless` and its line | an app's label does not change | hides the period difference between the classes (issue 2) |

   * **Recommendation:** B: the definition asks about apps already released, and no date exists to test more; C if
     you read the use as detecting apps released after the training data. **Decision:** A, B, C or D?

   **Notes for the AI:** once PR #50 is in this working copy, on B: `data_tags = ("Snapshot",)` and in
   `curation_comments` the bullet `- Time basis: Snapshot: apps released over 2010-2019, classified after release, as
   a store or scanner sweeps apps already published (the definition's question; Lennart: gap filling). The release
   keeps no date: the raw file is sorted by class, and inside the malware half RESTART_PACKAGES (deprecated 2010) jumps
   from under 1% to 13-27% of apps in the last four tenths, collections stacked by source (Time: Lost). Beyond issue
   1's twins no row of the period is known to carry another's label; malware families cannot be told without ids.
   Detecting apps released after the training data would need release dates and a split by time
   (kronodroid_android_malware has them).`; the `split` sentence says the same in one line; `dataset check`. On C:
   `ForcedIIDFromTemporal`, a line in the same form, and `use_case` reworded to scanning new apps.

   [^3a]: **SPLIT-32** (Should): `Snapshot` when the use case only fills in a time the data covers, the line naming
     the period, after checking that no sample of a test sample's time carries its target; `Timeless` when time
     cannot affect the target; samples over time whose period moves the target, with the time lost, get a forced
     split (SPLIT-8).

   **Resolved (2026-11-12, Andrej):** B: the drafted `- Time basis: Snapshot: ...` bullet in `curation_comments`, on
   the shipped rows (naming the 96 twins the de-duplication leaves) and ending with what the split cannot test; the
   `split` sentence calls the test data a snapshot of apps released 2010-2019. The `Snapshot` tag enters `data_tags`
   once PR #50 is in the working copy.

4. **Correct the record's collection facts?**

   * **Problem:**
     - The record carries `Samples: No Time Dimension`, the fact for designed runs or a catalogue where it plays no role when an item was measured.
     - The apps were released over 2010-2019, and when an app was made shows in what it declares (issue 2), while the release keeps no date.
     - Set `Samples: Over Time` and `Time: Lost`, and leave the target fact empty, since when the malware labels were assigned is not documented?
   * **Background:** UCI: permissions "extracted from more than 29000 benign & malware Android apps released between
     2010-2019" (https://doi.org/10.24432/C5FS64). Malware labels usually come from antivirus scans after release and
     can be revised, which would be `Target: Revised Later`, but nothing in the source says how these were set[^4a].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the record's fact (implemented) | `Samples: No Time Dimension` | no edit | states that time plays no role, which issue 2 contradicts |
     | B | Correct it | `Samples: Over Time`, `Time: Lost` | the facts the source supports | none found |

   * **Recommendation:** B. **Decision:** keep (A) or correct (B)?

   **Notes for the AI:** on B, in the record's `tags` replace `'Samples: No Time Dimension'` with `'Samples: Over
   Time'` and add `'Time: Lost'`; a `CC (<date>, Andrej):` line and `Andrej` in `checked_by`.

   [^4a]: **SPLIT-32** (Should): `Samples: Over Time` when the samples arose over a period, with `Time: Dated` or
     `Time: Lost`; `Target: Revised Later` when the target is assigned and then updated; no target fact when the
     target exists with the features.

   **Resolved (2026-11-12, Andrej):** B: record `tags` `Samples: Over Time` and `Time: Lost` in place of `Samples: No
   Time Dimension`, also in the PR #50 worktree's copy of the record; `Andrej` already in `checked_by`; record CC line.

## Reference

NATICUSdroid: A malware detection framework for Android using native and custom permissions
 By A. Mathur, Laxmi M. Podila, Keyur Kulkarni, Quamar Niyaz, A. Javaid. 2021
 
 Published in J. Inf. Secur. Appl.
