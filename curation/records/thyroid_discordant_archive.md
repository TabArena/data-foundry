---
unique_name: thyroid_discordant_archive
name: 'Thyroid Disease: the Garvan Institute archive (thyroid0387), discordant assay results'
checked_by:
- Andrej
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
priority: 2
tags:
- 'Samples: Over Time'
- 'Time: Dated'
- Dated Event Log
- Non-IID (Temporal)
original_source: UCI
year: '1987'
collection_period: Aug 1984 - Jan 1987
domain: medical & healthcare
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5D010
v2_path: datasets/_dev/tabarena-v0pt2/thyroid_discordant_archive/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-11-12, Andrej): thyroid_discordant's Review issue 4: "Do C and add it as a new dataset, then I decide on this". Option C of the AI answer of 2026-11-11: rebuild the discordant task from the parent archive of the same UCI folder (`thyroid0387.data`, 9,172 Garvan Institute requests, August 1984 to January 1987, dated by their record ids), label = archive code R ("discordant assay results"), split by request date: train on 1984-1985, test on three windows of 1986 and January 1987. Whether it replaces thyroid_discordant, ships next to it or is dropped is decided in its Review.

**Assessment (AI, 2026-11-12):** added as `datasets/_dev/tabarena-v0pt2/thyroid_discordant_archive/` without a review panel (the curator's ask: build it, then decide); the open question is in its Review, issue 1: keep this version, thyroid_discordant, or both. Recommend this version, which contains 3,553 of thyroid_discordant's 3,711 rows with the same label (PROV-6); the curator has the call. `thyroid0387.data`: 9,162 requests after dropping 10 repeated entries, 197 with code R (2.2%); referral source dropped, TBG kept, four impossible ages set to missing. Three four-month windows from February 1986 to January 1987 (24, 54 and 25 positives, training on 61% to 87% of the rows); untuned LightGBM 0.977 to 0.996 (mean 0.987), logistic regression 0.849 to 0.903 (0.878), against 0.972 and 0.828 on thyroid_discordant's random splits. `dataset check`: 0 errors, 1 warning (`dataset_pure_feature_value`: on thyroxine and TSH not measured, both on the request), not built. Priority 2: gap 0, use case 0, source +, shape +, risk - (the same task and requests as thyroid_discordant).

CC (2026-11-12, Andrej): Review issue 1, option B: archive version only; verdict ship, split and metric checked (`ok`). thyroid_discordant is not retired yet: his note on its issue 4, three minutes later, asks first why it was in the benchmark.
- Applied: `accepted_check_warnings` takes `dataset_pure_feature_value` (on thyroxine and TSH not measured are on the request, before the report comment; no leak); `dataset check` 0 errors, 0 warnings; not built.

CC (2026-11-16, Lennart): PR #102 review: the temporal split is ok (the request date from the record id, three four-month windows from February 1986).

**Assessment (AI, 2026-11-16):** checked against main for PR #102 (from the UCI zip, untuned LightGBM, ROC AUC on each window's rows): training on earlier requests only scores 0.964, 0.990 and 0.998, random training rows of the same size from any period outside the window 0.970, 0.989 and 0.998, random 3 x 3 folds over all rows 0.970, 0.993 and 0.988; so the windows test later requests rather than remove a leak. What moves with time: code R is 1.3% to 2.8% per quarter but 4.4% in 1986Q3 (chi-square across quarters p = 1.4e-5, p = 0.57 without it), and T3 is ordered for 79-87% of requests up to 1985Q3 and 32-75% after, while code R needs three of the five tests (0 of 458 requests with two or fewer). The source split by time too: the zip's ann-thyroid files, which their readme gives as the data of Quinlan's 1987 case study, train on 3,772 requests of 1985 and test on 3,428 of 1986 (all 2,317 and 1,560 rows that match exactly one archive record by their six numeric values fall in those years; the archive holds 3,428 requests of 1986). `DF: Yes` added: the dataset reaches `main` with this PR.

CC (2026-11-17, Andrej): the declared split (temporal on `request_date`, windows of 4 months, 3 windows at fixed cutoffs, no gap) is checked: the split decision tree, walked without the current split, reaches the split it ships (blind split walk).

CC (2026-11-26, Andrej): better data checked 2026-11-25 (review issue 2, A): no open table beats the archive; candidates and verdicts in the review. Verdict ship; nothing open in the review.

CC (2026-11-26, Lennart): accepted `splits_dimensions_off_protocol` (SPLIT-15) after the rebuild of 2026-11-26: three windows against SPLIT-33's nine, as thyroid_discordant's split decision; five would train on 30%.

## Review

**Outcome:** added. Built on Andrej's mark on thyroid_discordant issue 4 ("Do C and add it as a new dataset, then I
decide on this"): the discordant task rebuilt from the parent archive in the same UCI folder (`thyroid0387`, the
Garvan Institute's requests of August 1984 to January 1987), label = report code R, split by request date into three
four-month windows from February 1986 to January 1987. No review panel (not asked); `dataset check` passes with one
warning. The AI recommends keeping this version and retiring thyroid_discordant, whose rows it contains (issue 1).

**Main points:** Settled 2026-11-26, verdict ship. Better-data check (2026-11-25, issue 2, A on 2026-11-26): Keep thyroid_discordant_archive as it is (A): it already is the better data (the source's full archive, 9,162 requests, 197 discordant), and every other open thyroid table is a copy or subset of it, holds no discordant label, or is another collection. Earlier: Settled: this version ships (issue 1, B, 2026-11-12; split and metric `ok`). thyroid_discordant
is retired as its `Duplicate` (that dataset's issue 4, a, 2026-11-12).

**Record judgment:** valid. The label is the archive's own report code R, "discordant assay results"
(`thyroid0387.names`); who wrote the comments is not stated, so the fit stays `approximate`, as for
thyroid_discordant. Priority 2: gap 0, use case 0, source +, shape +, risk - (the same task and patients as
thyroid_discordant).

**Issues for Andrej:**

1. **Keep the rebuilt archive version, the original, or both?**

   * **Problem:**
     - This dataset holds thyroid_discordant's task with 2.5 times the requests and 3.4 times the discordant
       results, and a split by request date.
     - 3,553 of thyroid_discordant's 3,711 rows are records of this archive, with the same label for all 58 positives.
     - Keep this version, the original, or both?
   * **What differs:**

     | | thyroid_discordant | thyroid_discordant_archive |
     |---|---|---|
     | File | `dis.data` + `dis.test`, Quinlan's extract from an earlier version of the archive | `thyroid0387.data`, the archive's latest version |
     | Requests | 3,711 (1985; 158 undated) | 9,162 (August 1984 to January 1987) |
     | Discordant | 58 (1.6%) | 197 (2.2%) |
     | Label | "discordant", undefined in the file | code R in the report comment, "discordant assay results" |
     | Features | 26 | 29: also TBG with its flag (constant in the dis file) and the request date |
     | Split | 10 x 3 random | 3 windows of 4 months, each trained on all earlier requests |
     | Positives per test fold | 19 or 20 | 24, 54 and 25 |

   * **Windows** (untuned LightGBM and logistic regression, ROC AUC):

     | Test window | Training rows | Training positives | Test rows | Test positives | LightGBM | Logistic regression |
     |---|---|---|---|---|---|---|
     | February to May 1986 | 5,572 (61%) | 94 | 1,145 | 24 | 0.977 | 0.849 |
     | June to September 1986 | 6,717 (73%) | 118 | 1,230 | 54 | 0.989 | 0.881 |
     | October 1986 to January 1987 | 7,947 (87%) | 172 | 1,215 | 25 | 0.996 | 0.903 |
     | Mean | | | | | 0.987 | 0.878 |
     | thyroid_discordant, its 30 random splits, same models | 2,474 | 38-39 | 1,237 | 19-20 | 0.972 | 0.828 |

   * **Experiments:**
     - Training on the past costs little: random training rows of the same size from all periods give LightGBM 0.979
       and 0.990 on the two older windows (against 0.977 and 0.989), logistic regression 0.869 and 0.882 (against
       0.849 and 0.881); the newest window has only earlier rows outside it.
     - The request date as an input changes nothing (LightGBM 0.987 with, 0.987 without).
     - The gap between the two models is 0.11 here and 0.14 on thyroid_discordant: the methods still separate.
     - `dataset check`: one warning, two request fields that almost never go with code R: on thyroxine (1,239
       requests, 1 discordant) and TSH not measured (834, 1 discordant). Both are on the request, before the
       comment, so they are no leak.
   * **Background:** the windows are option C's up to three requests: one declaration cannot express its half-year,
     quarter and four months, and the archive holds only 2 requests in January 1986 and 1 in June 1986, none
     discordant; with four-month windows January trains the oldest window and June is tested with the summer. The
     share of code R is 4.4% in June to September 1986 against 1.7% to 2.1% elsewhere, and T3 is ordered less often
     from late 1985 on; the windows test both. Two versions of one dataset that give the same task enter once[^1a]; a
     better version from the source replaces the current one[^1b].
   * **Unknown:** whether repeat patients cross the cutoffs: the archive has no patient id.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Both (implemented) | both folders ship | nothing removed | the same task and 3,553 requests twice in the benchmark |
     | B | Archive version only | thyroid_discordant retired as `Duplicate`; this one ships | 2.5 times the rows and 3.4 times the positives; the label defined by the source; tests later requests | the model gap shrinks from 0.14 to 0.11; thyroid_discordant's review and build are set aside |
     | C | Original only | this record `No` with `Duplicate`; its folder removed | the reviewed, built dataset stays | 58 positives in a random split; the date known and unused |

   * **Recommendation:** B: the archive is the source's own fuller version of the same task, it contains the
     original's requests, and its windows hold 24 to 54 positives each. **Decision:** both (A), the archive version
     (B), or the original (C)?

   **Notes for the AI:** on A or B, set `accepted_check_warnings = {"dataset_pure_feature_value": "on_thyroxine and
   TSH_measured are on the request, before the report comment: a patient on thyroxine or without a TSH result is
   rarely commented as discordant (1 of 1,239 and 1 of 834); no leak"}` and re-run `dataset check`. On B, retire
   thyroid_discordant: record `No (Retired)` with `Duplicate` (keep `BeyondArena`), priority removed, a CC line naming
   this dataset; the folder leaves in a retirement PR; close its issues 2 and 4 as superseded. On C, this record gets
   `No` with `Duplicate`, its folder and `v2_path` go, and the claim is released. The scripts are in the review's
   checks for this dataset.

   [^1a]: **PROV-6** (Must): different versions or cuts of one underlying dataset are duplicates when neither adds a
     distinct task (added or dropped rows or columns). **PROV-4** (Must): a dataset enters once.
   [^1b]: **TP-6** (Must): a valid task stays; a better version the source itself defines replaces the current one.
     **TP-9** (Must): count the positives per test window of a temporal task. **SPLIT-14** (Must): at least 3
     windows, none training on less than half of the data.

   **Andrej (2026-11-12, change):** Option B: Archive version only.

   **Answer (AI, 2026-11-12):** the archive version stays and ships (verdict ship; split and metric `ok`).
   thyroid_discordant is not retired yet: your note on its issue 4, three minutes after this mark, asks first ("Before
   finally deciding to drop this dataset, why was it even here ...?"). Its retirement waits for your answer there.
   - Applied here, as the notes say for B: the `dataset_pure_feature_value` warning accepted with its reason (on
     thyroxine and TSH not measured are on the request, before the comment; no leak); `dataset check` 0 errors, 0
     warnings; not built.

   **Resolved (2026-11-12, Andrej):** B, archive side: archive version kept; the original's retirement waits for
   thyroid_discordant issue 4. `accepted_check_warnings` takes `dataset_pure_feature_value` with its reason;
   `dataset check` 0 errors, 0 warnings, README regenerated; not built. The original is now
   retired (2026-11-12): thyroid_discordant is `No (Retired)` with `Duplicate`, naming this dataset (its issue 4, a);
   its folder leaves in a retirement PR.

2. **Is there better data than the Garvan archive for the discordant-results task, or keep thyroid_discordant_archive as it is?**

   * **Problem:**
     - No open table holds more discordant results than the archive: the label exists only in it (code R, 197 of 9,162 requests) and in Quinlan's 1985 extract dis (58 of 3,772, the retired thyroid_discordant), and the Kaggle "Thyroid Disease Data" upload of 9,172 rows is the archive file cell for cell, codes included.
     - The other tables are Quinlan's extracts of the same requests with other comment groups (allbp, allhyper, allhypo, allrep, sick, ann-thyroid), two older Garvan files with no record ids, or a different collection (new_thyroid, 215 patients from Townsville); their targets are mostly near-trivial on the thyroid tests.
     - Keep the archive version and look no further, or add a second task from the same archive (its diagnosis groups as one multiclass target)?
   * **Background:**
     - The question may point at the retired original: thyroid_discordant (dis.data and dis.test, 3,711 rows) was retired on 2026-11-12 as `Duplicate` of this dataset, and its folder left main in #102 (2026-11-16). The "better data" for it was this archive rebuild, so nothing about it is left open.
     - The archive in v0.2 (main): 9,162 requests (August 1984 to January 1987), 29 features, label code R ("discordant assay results"), three four-month windows from February 1986 (24, 54 and 25 positives), ROC AUC.
     - Candidates, all downloaded and checked on 2026-11-25:

       | Data | Rows | Label | Relation to the archive | Access, licence | Verdict |
       |---|---|---|---|---|---|
       | thyroid0387.data (shipped) | 9,172 (9,162 after 10 repeated entries) | code R, 197 | itself | UCI, CC BY 4.0 | keep |
       | dis.data + dis.test (retired thyroid_discordant) | 3,772 | discordant, 58 | 3,553 of its 3,711 shipped rows are archive records, same label for all 58 | UCI zip | not better: retired as `Duplicate` |
       | allbp, allhyper, allhypo, allrep, sick | 3,772 each | one other comment group each | the same 3,772 requests as dis | UCI zip; OpenML 38 (sick), 40707, 40708 | not better: subsets, no discordant label |
       | ann-train + ann-test | 7,200 | 3 classes (normal, hyper-, subnormal function) | "the datas Quinlans used in the case study" (ann-Readme), 1985 train, 1986 test | UCI zip | not better: another target, near-trivial (table below) |
       | hypothyroid.data, sick-euthyroid.data | 3,163 each | hypothyroid 151; sick-euthyroid 293 | no record ids; 0 of 3,163 rows match an archive record on age, sex and the five tests | UCI zip | not better: no discordant label, older and smaller |
       | Kaggle emmanuelfwerr "Thyroid Disease Data" (thyroidDF.csv) | 9,172 | the archive's code string | identical: all 9,172 record ids, codes and cell values equal | Kaggle, CC0 | not better: a copy |
       | Kaggle yasserhessein "Thyroid Disease Data Set" | 3,771 | binaryClass, 291 positives | one of Quinlan's 3,772-request extracts | Kaggle, CC BY-NC-SA 4.0 | not better: a copy of a subset |
       | Kaggle jainaru "Thyroid Disease Data" | 383 | thyroid cancer recurrence | another study (already the record differentiated_thyroid_cancer_recurrence) | Kaggle, CC BY 4.0 | not this task |
       | new_thyroid (UCI new-thyroid) | 215 | 3 classes, 5 lab tests | not Garvan: Coomans, James Cook University, Townsville (new-thyroid.names) | UCI | not better: another collection, `Too Small` |
       | OpenML 47589 | 9,172 | referral source | the archive with the codes dropped | OpenML | not this task |
       | The archive's other comment groups | 9,162 | hyperthyroid, hypothyroid, binding protein, general health, replacement therapy, antithyroid treatment | same requests, another target | as the archive | a different task, the only real alternative (option B) |

   * **Effect on the task:** none under A: the shipped task already uses the largest set with the discordant label and the split the dates allow. B would add a second task on the same 9,162 requests; it does not change this one.
   * **Experiments:** UCI zip (https://archive.ics.uci.edu/static/public/102/thyroid+disease.zip) and the three Kaggle uploads downloaded on 2026-11-25; a batch job and 1411475; untuned LightGBM (300 trees), logistic regression (median imputation, scaled), a depth-2 tree and the best single test chosen on each training side; 5 x 5 stratified folds on the archive's 9,162 requests (random folds, to compare targets, not the shipped windows); ROC AUC.

     | Target on the archive (one comment group against the rest) | Positives | LightGBM | Logistic regression | Tree depth 2 | Best single test |
     |---|---|---|---|---|---|
     | discordant (R), the shipped label | 197 (2.2%) | 0.992 | 0.876 | 0.911 | 0.853 |
     | hypothyroid (E-H) | 659 (7.2%) | 1.000 | 0.973 | 0.994 | 0.988 |
     | hyperthyroid (A-D) | 228 (2.5%) | 0.995 | 0.962 | 0.940 | 0.926 |
     | general health (K) | 573 (6.3%) | 0.994 | 0.947 | 0.955 | 0.933 |
     | replacement therapy (L-N) | 355 (3.9%) | 0.998 | 0.968 | 0.965 | 0.758 |
     | binding protein (I-J) | 414 (4.5%) | 0.994 | 0.865 | 0.906 | 0.836 |
     | antithyroid treatment (O-Q) | 34 (0.4%) | 0.992 | 0.992 | 0.839 | 0.871 |
     | ann-thyroid, 3 classes, its own 1985/1986 split (macro one-vs-rest) | 250 non-normal in test | 0.999 | 0.990 | 0.991 | |

     | The diagnosis groups as one 8-class target (the group of the comment in force, its first letter when two groups) | Log loss | Macro one-vs-rest ROC AUC |
     |---|---|---|
     | LightGBM | 0.272 | 0.992 |
     | Logistic regression | 0.434 | 0.957 |
     | Tree depth 3 | 0.511 | 0.844 |
     | Class shares | 1.042 | 0.500 |

     - Code R leaves the widest room between the methods among the source's own groups (logistic regression 0.876, a depth-2 tree 0.911); hypothyroid is a short rule on TSH (best single test 0.988), and binding protein splits into two opposite conditions, of which "increased" alone is mostly T4U (0.932).
     - The 8-class target separates the methods (log loss 0.272 against 0.434), but 143 requests carry comments of two groups, so the class needs a rule of our own, and the multiclass task is not one the source defines (its letter table names the binary groups: "decision trees were derived for the most frequent classes of comments").
   * **Consistency:** in this batch the archive is the case where the better data was already found and shipped: like sdss_17's DR17 full set, it is the source's own fuller release of the same task, and the smaller cut (thyroid_discordant) is retired as its `Duplicate`[^prov6]. A better dataset from another source would be its own record[^better]; none exists here. A second target on the same rows would be another task, not a duplicate[^prov7].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the archive version, nothing more (implemented) | thyroid_discordant_archive ships as it is; no record created | the largest table with the discordant label; split by request date; nothing better found | none found |
     | B | Also add the archive's diagnosis groups as a multiclass task | a new record and definition from thyroid0387: 8 classes (no condition and seven comment groups), the same request-date windows | the methods separate (log loss 0.272 against 0.434); the source's main labels, which the discordant task leaves unused | the same 9,162 requests twice in the benchmark; 143 requests need a rule of our own for their class; most groups are near-trivial on their own (hypothyroid 0.988 on TSH alone); Lennart's screening read the diagnoses as "no real target" |

   * **Recommendation:** A: the archive is the better data, already in v0.2; every other open thyroid table is a copy or a subset of it, lacks the discordant label, or comes from another collection, so nothing replaces it or needs adding. **Decision:** A or B?

   **Notes for the AI:** On A: a CC (<date>, Andrej) line in thyroid_discordant_archive's record ("better data checked 2026-11-25: no open table beats the archive; candidates and verdicts in the review"), `Andrej` stays in checked_by; no definition change. On B: new record `thyroid_garvan_diagnosis_groups` (original_source UCI, source link https://doi.org/10.24432/C5D010, PROV-7 comment naming thyroid_discordant_archive as the same requests with another target) and a definition folder in datasets/_dev/tabarena-v0pt2/ reusing thyroid_discordant_archive's `_load_raw` and `_clean` and its windows; the class from the comment in force (the part after "|"), its first letter's group when two groups, "-" as no condition; metric log loss; dataset check through sbatch. Evidence: the run's evidence folder (scripts/targets.py, scripts/multiclass.py, out/targets.csv, out/multiclass.csv, dl_uci/, dl_kaggle/). Side fact for new_thyroid's record (not changed here): its comment calls it a duplicate of thyroid_discordant, but new-thyroid is Coomans' Townsville data, not Garvan; its `Too Small` verdict stands on its own.

   [^prov6]: **PROV-6** (Must): different versions or cuts of one underlying dataset are duplicates too when neither adds a distinct task: a swapped target, another slice of the same cohort, added or dropped rows or columns.
   [^prov7]: **PROV-7** (Must; narrows PROV-4 and PROV-6): records that share a source but give different tasks are not duplicates.
   [^better]: selection.md, "Small or dated, and the task is still done today": a better dataset from another source is its own record, a newer release of the same source is a version (PROV-6), and the old record keeps the verdict its own data earns until the curator decides.

   **Andrej (2026-11-26, ok):** As recommended (A).

   **Resolved (2026-11-26, Andrej):** A, the archive stays as it is: no open thyroid table beats it, and nothing replaces it or needs adding. No definition change.

## Reference

@misc{quinlan1986thyroid,
  author={Quinlan, Ross},
  title={{Thyroid Disease}},
  year={1986},
  howpublished={UCI Machine Learning Repository},
  doi={10.24432/C5D010}
}
@inproceedings{quinlan1987inductive,
  title={Inductive knowledge acquisition: a case study},
  author={Quinlan, John Ross and Compton, Paul J and Horn, KA and Lazarus, Leslie},
  booktitle={Proceedings of the Second Australian Conference on Applications of expert systems},
  pages={137--156},
  year={1987}
}
