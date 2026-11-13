---
unique_name: thyroid_discordant_archive
name: 'Thyroid Disease: the Garvan Institute archive (thyroid0387), discordant assay results'
checked_by:
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 2
tags:
- Non-IID (Temporal)
original_source: UCI
year: '1987'
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

CC (2026-11-12, Andrej): BeyondArena v0.2 review page, thyroid_discordant issue 4: "Do C and add it as a new dataset, then I decide on this". Option C of the AI answer of 2026-11-11: rebuild the discordant task from the parent archive of the same UCI folder (`thyroid0387.data`, 9,172 Garvan Institute requests, August 1984 to January 1987, dated by their record ids), label = archive code R ("discordant assay results"), split by request date: train on 1984-1985, test on three windows of 1986 and January 1987. Whether it replaces thyroid_discordant, ships next to it or is dropped is decided in its Review.

**Assessment (AI, 2026-11-12):** added as `datasets/_dev/tabarena-v0pt2/thyroid_discordant_archive/` without a review panel (the curator's ask: build it, then decide); the open question is in its Review, issue 1: keep this version, thyroid_discordant, or both. Recommend this version, which contains 3,553 of thyroid_discordant's 3,711 rows with the same label (PROV-6); the curator has the call. `thyroid0387.data`: 9,162 requests after dropping 10 repeated entries, 197 with code R (2.2%); referral source dropped, TBG kept, four impossible ages set to missing. Three four-month windows from February 1986 to January 1987 (24, 54 and 25 positives, training on 61% to 87% of the rows); untuned LightGBM 0.977 to 0.996 (mean 0.987), logistic regression 0.849 to 0.903 (0.878), against 0.972 and 0.828 on thyroid_discordant's random splits. `dataset check`: 0 errors, 1 warning (`dataset_pure_feature_value`: on thyroxine and TSH not measured, both on the request), not built. Priority 2: gap 0, use case 0, source +, shape +, risk - (the same task and requests as thyroid_discordant).

CC (2026-11-12, Andrej): Review issue 1, option B: archive version only; verdict ship, split and metric checked (`ok`). thyroid_discordant is not retired yet: his note on its issue 4, three minutes later, asks first why it was in the benchmark.
- Applied: `accepted_check_warnings` takes `dataset_pure_feature_value` (on thyroxine and TSH not measured are on the request, before the report comment; no leak); `dataset check` 0 errors, 0 warnings; not built.

## Review

**Outcome:** added. Built on Andrej's mark on thyroid_discordant issue 4 ("Do C and add it as a new dataset, then I
decide on this"): the discordant task rebuilt from the parent archive in the same UCI folder (`thyroid0387`, the
Garvan Institute's requests of August 1984 to January 1987), label = report code R, split by request date into three
four-month windows from February 1986 to January 1987. No review panel (not asked); `dataset check` passes with one
warning. The AI recommends keeping this version and retiring thyroid_discordant, whose rows it contains (issue 1).

**Main points:** Settled: this version ships (issue 1, B, 2026-11-12; split and metric `ok`). thyroid_discordant
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

   * **Windows** (untuned LightGBM and logistic regression, ROC AUC, Slurm jobs 1379934 and 1379941):

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
   checks for this dataset (jobs 1379934 and 1379941).

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
