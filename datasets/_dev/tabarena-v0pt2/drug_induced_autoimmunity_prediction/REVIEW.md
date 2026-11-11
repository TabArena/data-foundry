# drug_induced_autoimmunity_prediction

**Outcome:** added. The 587 drugs labelled for drug-induced autoimmunity (InterDIA, Huang et al. 2025, UCI 1104),
each given by its structure as a SMILES string, the one feature, and held out by chemical scaffold. Reviewed without a
panel, from the gathered evidence (the record with Andrej's reviews of 2026-10-19 and 2026-10-26, the earlier
experiments, a model run on the shipped data); the AI recommends shipping it, with the fit label of issue 2
changed to approximate. Issue 1 is resolved: since 2026-11-01 every SMILES dataset ships the structure as a typed
structure column that the benchmark encodes, and here the source's 176 RDKit descriptors left with it. Validity: a
screen of drug candidates by structure, with the structure the only input; whole Bemis-Murcko scaffolds (a drug's ring
skeleton; 443 groups) are held out, as a screen meets drugs of untested series; how the negative drugs were chosen is
undocumented, judged not a blocker on 2026-10-19, which the fit rule as amended on 2026-10-21 counts as a known gap
(issue 2). Value: on the scaffold splits the models separate (ROC AUC over 60 splits with the recommended encoding:
LightGBM 0.796, random forest 0.799, logistic regression 0.70 to 0.72 in earlier checks). An earlier check had TabPFN
3.5 on the source's descriptors only tie a training-free nearest-analog lookup (0.768 against 0.764, generic
scaffolds); MACCS keys from the structure lift it from 0.803 to 0.826 (27 of 30 scaffold splits). On the shipped
random splits the 40 benchmark methods span ROC AUC 0.74 (logistic regression) to 0.865, and a hand-written
structural-similarity model ties the best: the analog effect the scaffold split takes out.
Quality: 9 stereoisomer pairs, one 2D structure each, keep one row; both streptomycin rows (one per label) leave.
Andrej's mark on the review page of 2026-10-27: ship, metric ok. Weighed: a real screening use and an open licence +,
the scaffold split and the structure itself +, undocumented negatives -, 587 drugs -.

**Main points:** all issues are settled (2026-11-11, Andrej): the SMILES ships as a typed structure (issue 1), the
fit is `approximate` for the undocumented negatives (issue 2), the scaffold split stays with a `Time basis:` line and
no tag (issue 3), all 587 drugs stay with the era gradient of the label written down (issue 4), and the record carries
`Samples: Over Time`, `Time: Dated` and `Target: Revised Later` (issue 5). Nothing rebuilt.

**Record judgment:** valid and current to 2026-11-01 (Andrej's CC lines of 2026-10-19 and 2026-10-26, Lennart's of
2026-11-01). Corrections that need no decision: the metric's `reason` in the definition dated InterDIA 2024, where its
BibTeX and the record say 2025 (corrected 2026-11-11); the built container (2026-10-14) still carries the source's
descriptors, so the dataset needs a rebuild; the record's early "need to check SMILES ID" is done.

**Issues for Andrej:**

1. **Keep the SMILES string as a feature (PR #15): an exception to CLEAN-24 here, or an amendment for every SMILES
   dataset?** A SMILES is a line of text that spells out a molecule's structure. CLEAN-24 (Should) ships the structure
   as RDKit descriptors and drops the string, for apistox, this dataset and qsar_bioconcentration (Lennart,
   2026-10-14). On 2026-10-26 Andrej decided the string stays here ("the SMILES is important for performance"):
   PR #15 ships it as a string feature next to the source's 176 descriptors (177 features, 587 rows), with a CC
   line. The working copy on this branch still drops it, and PR #15 is open.
   - Effect on the task: the descriptors lose structure. MACCS keys, 166 yes/no flags for standard substructures
     computed from the SMILES, lift the scaffold-grouped ROC AUC next to the descriptors (TabPFN 3.5 0.803 to 0.826,
     better on 27 of 30 splits; random forest 0.770 to 0.795). Shipping the string lets a model read the structure
     its own way; a model that cannot read text gains nothing from it, and as plain text the string lowered LightGBM
     from 0.835 to 0.810 on random splits (15 splits, 2026-10-14).
   - Implemented: on PR #15 only.
   - Alternative (a): merge PR #15 and record an exception to CLEAN-24 for this dataset, with the fact that sets it
     apart (the MACCS gain under a scaffold split). Cost: SMILES datasets are treated two ways.
   - Alternative (b): amend CLEAN-24 so every SMILES dataset ships the string next to the descriptors (apistox and
     qsar_bioconcentration change too). Cost: two more definitions change; the gain is measured here only.
   - Alternative (c): keep the working copy as it is (string dropped) and close PR #15. Cost: undoes Andrej's
     decision of 2026-10-26 and the structure the descriptors miss.
   - Rule: CLEAN-24 (Should) and the procedure for a departure: an exception names the fact that sets the case apart,
     an amendment changes the rule (principles.md, "Exceptions and amendments"). Lennart has not answered the question
     on PR #15.
   - Recommendation: (a), and ask Lennart whether (b) is wanted. Decision: (a), (b) or (c).

   **Resolved (2026-11-01, Lennart):** an amendment for every SMILES dataset, closest to (b) in a new form, after
   Andrej's call of 2026-10-26 to keep the structure. The structure ships as a SMILES column typed as a structure
   (`special_features`, since 2026-11-02), never as text and never pre-encoded; the benchmark encodes it, by default
   with RDKit's 2D descriptors, the 166 MACCS keys and the ECFP4 counts. Here the source's 176 RDKit descriptors left
   too, as the recommended encoding reproduces them: scaffold-grouped ROC AUC over 60 splits, LightGBM / random forest,
   source descriptors 0.771 / 0.776, the full RDKit set 0.772 / 0.777, with the MACCS keys 0.796 / 0.799 (better on 51
   and 59 of 60 splits), the SMILES read as text 0.763 / 0.766. Recorded in the record's CC line and the CHANGELOG
   (2026-11-01); not built.

2. **Keep the fit `direct`, or make it `approximate` because the negatives are undocumented?**

   * **Problem:**
     - Neither the InterDIA paper nor its repository says how drugs were picked as positive or negative, and a few
       negatives look like reporting gaps (venlafaxine is positive, its active metabolite desvenlafaxine negative).
     - Since 2026-10-21 the fit rule counts an unverified label definition as a known gap that makes the fit
       approximate, while this definition reads `direct`, as marked on 2026-10-19, before that amendment.
     - Keep `direct`, or move to `approximate` with the gap named in `fit_reason`?
   * **Background:** the fit states how closely the benchmark task mirrors the use case, here a toxicologist who
     screens candidates by structure[^2a]; it changes no row, split or score. On 2026-10-19 Andrej judged the
     undocumented labels not a blocker: the classic drug-induced lupus drugs are all positive, and "not reported"
     negatives are normal for side-effect data. The nearest documented set calls a drug negative when its label names
     no autoimmune term (Wu Y, Zhu J, Fu P, Tong W, Hong H, Chen M. Machine Learning for Predicting Risk of
     Drug-Induced Autoimmune Diseases by Structural Alerts and Daily Dose. Int J Environ Res Public Health.
     2021;18(13):7139. https://doi.org/10.3390/ijerph18137139). Other negatives are simple compounds (phosphate,
     carbonate, glycine, nitric oxide), and cyproterone acetate is positive while cyproterone is negative. The
     definition's `predicted` text names the gap; `fit_reason` does not.
   * **Effect on the task:** none on the data; a reader of `fit` learns that a negative may mean "no reaction
     reported" rather than "shown safe", so a model is rewarded for predicting what was reported.
   * **Consistency:** blood_tests_drink_prediction (the quantity known, how it was recorded not), diabetes_3 (a label
     whose construction is undocumented) and differentiated_thyroid_cancer_recurrence (what counts as recurrence not
     verified) ship approximate for the same kind of gap[^2b]. Keeping `direct` here departs from them; the AI's best
     guess at a fact that sets this case apart is that the positives' meaning is clear (a reported autoimmune
     reaction) and only the rule for the negatives is missing.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Direct (implemented) | `fit="direct"`; the gap stays named in `predicted` only | the mark of 2026-10-19 stands; the positives' meaning is clear | departs from the amended fit rule and its three cases |
     | B | Approximate | `fit="approximate"`; `fit_reason` names the undocumented negatives | follows the amended rule and its cases; no data change | changes a label on a dataset already reviewed |

   * **Recommendation:** B, as the rule now reads and the three cases were decided. **Decision:** keep `direct` (A),
     or make it `approximate` (B)?

   **Notes for the AI:** on B, set `fit="approximate"` and append to `fit_reason`: "The source does not say how the
   negative drugs were chosen (likely no autoimmune reaction reported, as in Wu et al. 2021), an unverified label
   definition." Add a CC line (Andrej) and `checked_by` stays; run `dataset check`; rebuild with the SMILES change.

   [^2a]: **USE-8** (Must): write how closely the data mirrors the use case; an unverified label definition is a known
     gap and makes the fit approximate (amended 2026-10-21, Lennart, on differentiated_thyroid_cancer_recurrence).
   [^2b]: **USE-5** (Must): a label from a named publication whose construction is undocumented and cannot be checked
     may ship with `fit="approximate"` and a note naming the gap, decided case by case (Lennart, 2026-10-21).

   **Andrej (2026-11-11, change):** Option B: Approximate.

   **Resolved (2026-11-11, Andrej):** B. `fit="approximate"`, with the undocumented negatives named in
   `fit_reason` ("likely no autoimmune reaction reported, as in Wu et al. 2021, an unverified label definition")
   and in a curation bullet of `dataset.py`; the record's CC line of 2026-11-11 records it. No row, split or score
   changes; `dataset check` 0 errors, 0 warnings. Not rebuilt.

3. **Time basis and split: split by first approval year, or keep the scaffold split with the label's reporting window
   named?**

   * **Problem:**
     - ChEMBL dates 496 of the 587 drugs by first approval (1940 to 2020), and the positive share falls from 28.7%
       before 1980 and 27.0% in 1980-99 to 19.4% in 2000-09 and 5.8% from 2010 (3 of 52, against 25.9% before,
       binomial p 0.0002), so the label follows how long a drug has been in use.
     - The record carries `Samples: No Time Dimension` with no time or target fact, and the definition names no time
       basis, while the split holds out whole Bemis-Murcko scaffolds.
     - No prototype fits: the propensity is a property of the structure, but the recorded label accrues with reports
       and its window has not closed for the newest drugs, so the facts go to you rather than the nearest tag[^3a].
   * **Background:**
     - How the labels were made is undocumented (issue 2); the nearest precedent calls a drug negative when its label
       names no autoimmune term, so a negative reads as "nothing reported yet" and a drug can change side as reports
       accrue.
     - The era is readable from the structure: the median molecular weight rises from 309 before 1980 to 430 from 2010
       on, molecular weight alone separates the approvals from 2010 at ROC AUC 0.693, and the share of drugs with a
       structural alert rises to 0.615 after 2010.
     - The scaffold groups already separate eras in part: among scaffold groups with more than one dated drug the mean
       gap in approval year is 14.5 years against 19.1 for all pairs, and a drug's nearest fingerprint analog was
       approved within 5 years 31% of the time against 19% by chance (median gap 11 years).
     - That is far weaker than qsar_tid_11, where 85-90% of the close training analogs were first published in the
       test compound's own year.
   * **Effect on the task:** the scaffold split tests a new chemical series on the labels as reported by 2025; a
     forward split would test drugs whose reporting window is shortest, so most of its difficulty is the delay, not
     the chemistry.
   * **Experiments:** approval years from ChEMBL (flexmatch on the canonical SMILES: 575 of 597 source rows matched,
     496 of the 587 shipped drugs dated), then untuned logistic regression, random forest and histogram gradient
     boosting on the source's RDKit descriptors, ROC AUC (Slurm job 1366251, 2026-11-06); the scaffold rows are 10
     repeats of 3 scaffold-grouped folds over the 496 dated drugs (logistic regression 0.676, random forest 0.721,
     boosting 0.717):

     | Test from | Training drugs (positive) | Test drugs (positive) | Forward: LR / RF / boosting | Random folds of the same training size |
     |---|---|---|---|---|
     | 1990 | 219 (57) | 277 (61) | 0.606 / 0.642 / 0.607 | 0.716 / 0.740 / 0.721 |
     | 1995 | 267 (75) | 229 (43) | 0.582 / 0.698 / 0.714 | 0.716 / 0.777 / 0.754 |
     | 2000 | 351 (97) | 145 (21) | 0.617 / 0.692 / 0.765 | 0.740 / 0.794 / 0.803 |
     | 2005 | 399 (107) | 97 (11) | 0.692 / 0.828 / 0.810 | 0.752 / 0.812 / 0.825 |

     - A forward split costs 0.03 to 0.13 ROC AUC at the early cuts and nothing at 2005, where only 11 of 97 test
       drugs are positive; positives are the older drugs overall (Mann-Whitney p 0.0017, ROC AUC of an earlier
       approval for the label 0.596).
   * **Consistency:** qsar_tid_11 issue 2 recommends a split by first publication year for a dated catalogue whose
     series move with the year; it differs here because what moves with the year is also the label's maturity, so the
     newest windows cannot be scored honestly.
   * **Unknown:** when each reaction was first reported, which would date the label itself rather than the approval;
     neither the paper nor its repository gives it.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Scaffold split, no time basis (implemented) | as now | nothing to change | the definition says nothing about the reporting window behind the labels |
     | B | Scaffold split, a `Time basis:` line and no tag | as now; the line gives the approval years, the era gradient of the label and what the split cannot test | states the facts without claiming a prototype that does not fit; no data, split or score changes | a definition without a tag, which the date-column note may keep flagging |
     | C | Scaffold split, `Timeless` | as B, with the tag | the propensity to cause autoimmunity is a property of the structure | the shipped label is not that property but what was reported by 2025, and it moves with the era |
     | D | Split by first approval year | windows from the ChEMBL years, each trained on the drugs approved earlier | mirrors a screen of a new drug; the dates are recoverable for 496 of 587 | the newest drugs are labelled negative mostly for want of reports (3 of 52 from 2010), so the last window scores reporting delay; 91 undated drugs would leave or need a guessed year |

   * **Recommendation:** B: the dates are recoverable and the era gradient is real, but the label's own window is open
     for the newest drugs, so a forward split would score the reporting delay; the line says that plainly and the
     scaffold split keeps testing new series. **Decision:** A, B, C or D?

   **Notes for the AI:** on B, once PR #50 is in: no tag, and a curation bullet `- Time basis: no prototype fits.
   Whether a drug can cause an autoimmune reaction is a property of its structure, but the label is what had been
   reported by the compilation (InterDIA, 2025), so it accrues with time on the market: ChEMBL dates 496 of the 587
   drugs by first approval (1940-2020) and the positive share falls from 28.7% before 1980 to 5.8% from 2010 on (3 of
   52). The split holds out scaffolds, which separates eras only in part (mean approval-year gap within a scaffold
   group 14.5 years against 19.1 for all pairs). Not tested: a newly approved drug, whose reporting window is still
   open; trained on the drugs approved before a cut, ROC AUC falls by 0.03-0.13 for cuts up to 2000 (Slurm job
   1366251, 2026-11-06).` On D, add the year in `_prepare_raw_files` from a one-off ChEMBL extract (the API's
   `molecule_structures__canonical_smiles__flexmatch` and `first_approval`, as
   `scripts/approval_years.py` of this review), keep it as a feature, `temporal = Temporal(on="first_approval", ...)`
   with windows of at least about 50 test drugs and every training side at half the rows or more, drop `grouping` and
   the scaffold column, rewrite the split text and `fit_reason`, record `required_split: Temporal (NON-IID)`;
   `dataset check`, CHANGELOG, record CC.

   [^3a]: **SPLIT-32** (Should): how the data was collected is information for the split; a definition can name the
     use-case prototype it follows with a `Time basis:` line, and when none of the prototypes fits, the dataset and
     its use case go to the curator with the arrival facts found rather than under the nearest tag. `DelayedTarget`
     requires that the target's window has closed for every sample. **SPLIT-1** (Must): the split is the one that most
     closely mirrors the real-world application. **SPLIT-31** (Should), as amended 2026-10-26 (Lennart): a molecule
     dataset whose rows carry exact structures groups on the Bemis-Murcko scaffold, as a new chemical often comes from
     a series not yet measured.

   **Andrej (2026-11-11, change):** Option B: Scaffold split, a Time basis: line and no tag.

   **Resolved (2026-11-11, Andrej):** B. The scaffold split stays and no prototype tag is claimed; the curation
   comments carry a `Time basis:` line with the approval years (ChEMBL dates 496 of the 587 drugs, 1940-2020), the
   era gradient of the label, the forward-cut table and what the split cannot test. `splits_comment` says why no
   forward split: the label's reporting window is still open for the newest drugs. Applied in `dataset.py`; no data
   change.

4. **Keep the 52 drugs approved since 2010, whose negatives may only mean "not reported yet"?**

   * **Problem:**
     - Of the 52 dated drugs first approved from 2010 on, 49 are negative (5.8% positive against 25.9% before,
       binomial p 0.0002), a share no chemistry explains.
     - A model can tell that era from the structure (molecular weight alone separates the approvals from 2010 at ROC
       AUC 0.693; the median rises from 309 before 1980 to 430), so it can learn "modern drug, so negative".
     - Those rows teach the reporting delay rather than the reaction: keep them with the fact written down, or drop
       them[^4a]?
   * **Background:**
     - The three positives approved since 2010 are teriflunomide, elvitegravir and rilpivirine; the other 49 include
       recent oncology and antiviral drugs whose labels carry no autoimmune term yet.
     - 91 of the 587 drugs have no ChEMBL approval year, and their positive share (24.2%) is that of the older drugs,
       so they are not a second recent block.
     - The share of drugs carrying a structural alert rises to 0.615 after 2010 while their positive share falls, so
       the alert features point the wrong way in that block.
   * **Effect on the task:** dropping them removes 8.9% of the rows and 3 of the 140 positives, and takes away the
     drugs that look most like tomorrow's candidates; keeping them leaves a block of rows whose label is the
     compilation's reporting window.
   * **Experiments:** the era gradient and the molecular-weight separation above (Slurm job 1366251 and the ChEMBL
     lookup of 2026-11-06); no model was run on the frame with the block removed.
   * **Consistency:** follows taiwanese_bankruptcy_prediction (company-year blocks kept with the effect written down)
     and labour_inspection_compliance (one undated account set kept with a note); the alternative is the row drop
     porto_seguro's issue 4 recommends for rows whose recording differs.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep all 587, nothing said (implemented) | as now | the source's rows | the reporting window is invisible to a benchmark user |
     | B | Keep all 587, the fact written down | the curation notes and the task summary name the era gradient, and issue 2's `fit_reason` names the undocumented negatives | keeps the rows and the hardest cases; the mildest remedy; one line of text | a model is still rewarded for reading the era |
     | C | Drop the drugs approved from 2010 on | 535 rows, 137 positives, and the ChEMBL year joined in `_prepare_raw_files` to find them | removes the block whose label is mostly a reporting gap | 8.9% of a 587-row dataset leaves, with the most modern chemistry; 91 undated drugs cannot be checked the same way |

   * **Recommendation:** B: the block is real and measured, but dropping a tenth of a tiny dataset on an inferred
     approval year costs more than the note, and the recent drugs are the ones the use case cares about.
     **Decision:** A, B or C?

   **Notes for the AI:** on B, a curation bullet `- Label and time on the market: 49 of the 52 drugs ChEMBL dates to a
   first approval from 2010 on are negative (5.8% against 25.9% earlier, p 0.0002), so a recent approval mostly
   predicts the label; the structure shows the era (molecular weight alone separates the 2010s at ROC AUC 0.693).
   Kept on purpose: the label is what had been reported by 2025 (2026-11-06).`, and the same fact in one clause of
   `fit_reason` on issue 2's B; `dataset check`; no rebuild (comment only). On C, join the year in
   `_prepare_raw_files`, drop the rows, re-run the probes and the scaffold grouping, CHANGELOG and a rebuild.

   [^4a]: **LEAK-1** (Must) and **LEAK-10** (Must): a column that comes into existence after the prediction point is a
     leak whatever the split, and every feature is checked to have existed at that point; here the feature is sound
     and the label is the one shaped by time, which **SPLIT-32** (Should) records as `Target: Revised Later`.
     **USE-8** (Must): an unverified label definition is a known gap and makes the fit approximate (issue 2).

   **Andrej (2026-11-11, change):** Option B: Keep all 587, the fact written down.

   **Resolved (2026-11-11, Andrej):** B. All 587 drugs kept; a curation bullet gives the positive share by approval
   era (0.058 for the 52 drugs approved from 2010 on against 0.259 earlier, binomial p 0.0002) and the era's
   visibility from the structure (molecular weight alone, ROC AUC 0.693), and one clause of `fit_reason` carries the
   fact. No data change.

5. **Correct the record's collection facts: drugs approved over decades, dated through ChEMBL?**

   * **Problem:**
     - The drugs were first approved between 1940 and 2020, and ChEMBL gives the year for 496 of the 587 the
       definition ships (575 of 597 source rows match a ChEMBL molecule by flexmatch on the SMILES).
     - The record carries `Samples: No Time Dimension`, the fact for designed runs or a catalogue where it plays no
       role when an item was measured, while here the label's share moves with the approval era (issue 3).
     - Set `Samples: Over Time`, `Time: Dated` and `Target: Revised Later`[^5a]?
   * **Background:** the label is a compilation of reports up to 2025, so it is assigned and then accrues as reports
     come in (venlafaxine is positive while its metabolite desvenlafaxine is negative), which is what the target fact
     records; the approval year is not in the release itself but in a parent source that matches by structure.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | `Samples: No Time Dimension` (implemented) | as now | a drug's chemistry does not depend on its approval year | hides a catalogue that grew over decades and a label that grows with it |
     | B | `Samples: Over Time`, `Time: Dated` | the tag replaced and the time fact added | the source as it is; ChEMBL dates 84% of the drugs | the dates come from a parent source, not from the release |
     | C | As B, plus `Target: Revised Later` | the target fact added as well | names the label that accrues with reports, the fact behind issues 3 and 4 | rests on how the labels were probably made, which the source does not document |

   * **Recommendation:** C: the era gradient of the label is measured, and the facts should carry what drives issues 3
     and 4. **Decision:** A, B or C?

   **Notes for the AI:** on B or C, in the record's `tags`: `'Samples: No Time Dimension'` becomes
   `'Samples: Over Time'`, plus `'Time: Dated'` (and `'Target: Revised Later'` on C); add a CC line with the ChEMBL
   lookup (the API's `molecule_structures__canonical_smiles__flexmatch` and `first_approval`, 496 of 587 dated,
   1940-2020) and keep `Andrej` in `checked_by`.

   [^5a]: **SPLIT-32** (Should): the record's collection facts, true whatever task is built on the source:
     `Samples: No Time Dimension` (designed runs, or a catalogue of properties where it plays no role when an item was
     measured) against `Samples: Over Time`; for samples over time `Time: Dated` when the release or its source keeps
     the time or lets us recover it (a date kept in a parent upload counts); `Target: Revised Later` when the target
     is assigned, then updated or propagated.

   **Andrej (2026-11-11, change):** Option C: As B, plus Target: Revised Later.

   **Resolved (2026-11-11, Andrej):** C. The record's tags are now `Samples: Over Time`, `Time: Dated` and
   `Target: Revised Later` in place of `Samples: No Time Dimension`, with the ChEMBL lookup in the CC line of
   2026-11-11; `Andrej` stays in `checked_by`.

