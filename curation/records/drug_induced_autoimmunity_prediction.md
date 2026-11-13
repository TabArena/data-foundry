---
unique_name: drug_induced_autoimmunity_prediction
name: Drug Induced Autoimmunity Prediction
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 2
tags:
- Tiny Data
- Non-IID (Grouped)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Revised Later'
- Expanding Science Catalogue
collections:
- New (BeyondArena)
original_source: UCI
year: '2025'
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5332M
notebook_path: datasets/beyond_iid/new_iid/drug_induced_autoimmunity_prediction/drug_induced_autoimmunity_prediction.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/drug_induced_autoimmunity_prediction/dataset.py
source_row: 773
type_adapter_id: curation-record-v1
---

## Comments

"This dataset comprises molecular descriptors generated using RDKit," -> to ChatGPT's domain understanding, this means it collected/curated it and did not create fake data

Based on GitHub and the descriptions, it looks like real data https://github.com/Huangxiaojie2024/InterDIA


need to check SMILES ID

CC (2026-10-14, Lennart): Drop the SMILES as a feature, as in every SMILES dataset; the source's RDKit descriptors carry the structure.

**Assessment (AI, 2026-10-14):** The SMILES as text lowered LightGBM's ROC AUC from 0.835 to 0.810 (15 of 15 splits). Without it 9 pairs of stereoisomers share every descriptor (PubChem: quinine and quinidine, and eight drugs entered twice with other stereo marks, streptomycin once as positive and once as negative), 3 pairs across the source's train and test files. One row of each pair is kept and both streptomycin rows are dropped, as for qsar_oral_toxicity: 587 drugs, 140 positive.

CC (2026-10-19, Andrej): Labels undocumented; not a blocker.
- The source doesn't say how negatives were chosen; likely "no autoimmune reaction reported" (as in Wu et al. 2021). A few look like gaps (venlafaxine positive, its metabolite desvenlafaxine negative). Not severe: the classic drug-induced lupus drugs are all positive.
  - Wu Y, Zhu J, Fu P, Tong W, Hong H, Chen M. Machine Learning for Predicting Risk of Drug-Induced Autoimmune Diseases by Structural Alerts and Daily Dose. Int J Environ Res Public Health. 2021;18(13):7139. doi:10.3390/ijerph18137139

CC (2026-10-19, Andrej): Split changed to scaffold-grouped; keep.
- Analog lookup under random splits: about a third of the test drugs have a close structural relative in training with the same label, and looking up the label of the most similar training drug (Tanimoto similarity of Morgan fingerprints, no model) reaches ROC AUC 0.822 against TabPFN's 0.854. Fixed by holding out whole Bemis-Murcko scaffolds (a drug's ring skeleton): the signal survives and the models still separate (LightGBM 0.815 IID vs 0.758 grouped; random forest 0.776 vs linear 0.702 on the grouped splits).
- Why a scaffold split: the use case screens new drug candidates, which come from chemical series not yet tested; the Therapeutics Data Commons ADMET benchmarks split all their endpoints by scaffold for this reason, among them drug-induced liver injury, a drug-level label like this one. The source validated on random splits (its test file is as similar to its training file as a random split is), so our scores are lower than the paper's AUC 0.88-0.89 by design.
  - Huang K, Fu T, Gao W, Zhao Y, Roohani Y, Leskovec J, Coley CW, Xiao C, Sun J, Zitnik M. Therapeutics Data Commons: Machine Learning Datasets and Tasks for Drug Discovery and Development. Proc Neural Inf Process Syst Track Datasets Benchmarks. 2021. arXiv:2102.09548
  - Bemis GW, Murcko MA. The Properties of Known Drugs. 1. Molecular Frameworks. J Med Chem. 1996;39(15):2887-2893. doi:10.1021/jm9602928
- Groups: 443 (390 ring scaffolds plus the 53 ring-free drugs, each a group of its own: they share no skeleton, and their nearest neighbour's label agrees only at the base rate, 0.925).
- Record: `required_split` set to `Grouped (NON-IID)` (was `Random (IID)`, `?`); tag `Non-IID (Grouped)` added.

CC (2026-10-19, Andrej): The source's descriptors lose structure; add MACCS keys before shipping. **For discussion with Lennart**, as it revisits his 2026-10-14 call for every SMILES dataset.
- Scaffold-grouped ROC AUC, mean of 30 splits, by what the SMILES contributes next to the source's 176 descriptors:

  | features | LR | RF | boosting | TabPFN 3.5 |
  |---|---|---|---|---|
  | descriptors (shipped) | 0.717 | 0.770 | 0.774 | 0.803 |
  | + reactive-metabolite alerts (14) | 0.707 | 0.775 | 0.773 | 0.807 |
  | **+ MACCS keys (166)** | 0.715 | 0.795 | 0.790 | **0.826** |
  | + Morgan counts (1,024) | 0.771 | 0.816 | 0.780 | 0.816 |
  | MACCS keys alone | 0.678 | 0.826 | 0.794 | 0.825 |
  | Morgan counts alone | 0.742 | 0.753 | 0.764 | 0.788 |

- Dropping the SMILES costs accuracy. MACCS keys (166 yes/no flags for standard substructures, computed from the SMILES with RDKit) next to the source's descriptors lift the scaffold-grouped ROC AUC: TabPFN 3.5 0.803 -> 0.826 (better on 27 of 30 splits), random forest 0.770 -> 0.795, LightGBM-style boosting 0.774 -> 0.790. MACCS alone matches the descriptors (random forest 0.826). So the 2026-10-14 finding that the SMILES adds nothing holds only for the raw string as text, not for the structure in it.
- Reactive-metabolite alerts (14 SMARTS from Wu et al. 2021, aromatic amine, hydrazine, thiophene, ...) add nothing next to the descriptors (TabPFN +0.003): those descriptors already count such groups.
- Morgan counts are not the answer: for the best model they help less than MACCS (TabPFN 0.816 vs 0.826, worse on 20 of 30 splits) at six times the columns, and alone they are worse than the descriptors alone.
- Suggestion (pending Lennart): `Yes`, after `_clean` adds the MACCS keys as `maccs_*` columns from the SMILES (alongside `rdkit_descriptors`, before the SMILES is dropped) and the stereoisomer de-duplication is re-checked on the wider frame. 166 dense binary columns, unlike the ~1,000 sparse Morgan columns the 2026-10-14 round ruled out for a gain of 0.01-0.015.
  - Durant JL, Leland BA, Henry DR, Nourse JG. Reoptimization of MDL Keys for Use in Drug Discovery. J Chem Inf Comput Sci. 2002;42(6):1273-1280. doi:10.1021/ci010132r
To do: add the MACCS keys to `dataset.py` (a framework helper, as `rdkit_descriptors`), then rebuild (the build is stale).

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: the 20 RDKit fragment counts that hold only 0 and 1 (found on the data in `_feature_types`).

CC (2026-10-21, Lennart): ok on the hidden-group item (SMR_VSA10, SMR_VSA7): "Yes do so, it likely is a grouped dataset, in the open PRs, there is a finding from Andrej on this as well."

**Assessment (AI, 2026-10-21):** The SMR_VSA10/SMR_VSA7 groups of the hidden-group sweep are not analog series: of the values shared by two or more drugs, 17% and 20% fall within one Bemis-Murcko scaffold (adjusted Rand index against the scaffolds 0.04 and 0.08); their larger gap comes from the value 0 (68 and 79 drugs) landing in one test fold, a shift on an informative feature. No two source rows share a canonical SMILES; without stereo marks the 9 known stereoisomer pairs match. The scaffold grouping of open PR #15 (Andrej; 443 groups, a drug without a ring its own group) is the series split: on the 587 drugs, untuned ROC AUC random vs scaffold-grouped (10 x 3 folds) is LightGBM 0.826 vs 0.771, random forest 0.828 vs 0.776, logistic regression 0.739 vs 0.705, in line with PR #15 (TabPFN 0.854 vs 0.803). Recommend merging PR #15's grouping and rebuilding; this branch leaves `dataset.py` IID because PR #15 edits the same file (issue 1 of the record's Review). The curator has the call.

CC (2026-10-21, Lennart): on which 0/1 columns are flags: "no if we can infer from the semantic context, keep it a number, this is a real-world bias. We want to make things categorical if we know from the context they are indeed such" (CLEAN-14, amended again). Reverted: the 20 RDKit fragment counts (fr_*) that hold only 0 and 1 stay numeric; `_feature_types` only.

CC (2026-10-21, Lennart): make this dataset grouped here as well ("we want to have the correct state here as well and fix the issue going forward"); PR #15 is updated later as needed.

**Assessment (AI, 2026-10-21):** PR #15's scaffold grouping is now in the working copy: the split groups on the Bemis-Murcko scaffold (`murcko_scaffolds` in `data_foundry.v2.chemistry`; 443 groups, a drug without a ring its own group), `dataset check` 0 errors and 0 warnings. Measured on the 587 drugs, untuned LightGBM ROC AUC 0.771 grouped against 0.826 random; the hidden-group probe's SMR_VSA10/SMR_VSA7 groups do not follow the scaffolds (adjusted Rand 0.04 and 0.08) and need no split of their own. Andrej's question on MACCS keys stays open on PR #15. Needs a rebuild.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Huang, Liu & Huang 2024 (InterDIA) report AUC, accuracy, sensitivity, specificity, F1 and MCC side by side, no unique metric (MET-5).

**Assessment (AI, 2026-10-27):** The open questions for the curator are in the record's Review (review of the Tiny Data datasets, written from the earlier findings, no review panel); the AI recommends shipping it after changes. Priority 4: gap +, use case +, source +, shape -, risk +.
CC (2026-10-26, Andrej): The SMILES is important for performance, so it stays in the data.
- `dataset.py`: `SMILES` is no longer dropped; it ships as a string feature next to the source's 176 descriptors (177 features, 587 rows unchanged). This settles the MACCS question above by shipping the structure itself instead of one chosen fingerprint, so a model can read it as it likes.
- Stereoisomer de-duplication is unchanged: it compares the descriptors only, not the SMILES, so the same 9 pairs are found (their SMILES differ only in the stereo marks) and the row count stays 587 with 140 positive.
- The 2026-10-14 rule for every SMILES dataset (drop the string) is overridden here only; the `dataset_identifier_column` warning (one SMILES per row) is accepted in the definition, as for `phiusil_phishing`: the structure is the input of the task, not a row id.
- Still to do: rebuild (the build is stale).

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found a related task: `dilist_drug_induced_liver_injury` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target ships as No/Yes, Yes the event (1 is the event).

CC (2026-11-01, Lennart): SMILES ship as a typed structure column, not pre-encoded and never as text (path C of the discussion doc "SMILES Handling in Data Foundry and TabArena v0.2" (https://claude.ai/artifact/6r49WpR9Uard5ogo7qK4rB)): the benchmark encodes it; the recommended encoding in Data Foundry is RDKit's 2D descriptors with the MACCS keys.

**Assessment (AI, 2026-11-01):** the definition now ships `SMILES` (RDKit's canonical form) in `smiles_columns`, as Andrej decided to keep it on 2026-10-26, but typed as a structure, and the source's 176 RDKit descriptors leave: the recommended encoding reproduces them (LightGBM / random forest ROC AUC over the 60 scaffold splits: source descriptors 0.771 / 0.776, our full RDKit set 0.772 / 0.777) and adds the MACCS keys (0.796 / 0.799, better on 51 and 59 of 60 splits); the SMILES read as text gives 0.763 / 0.766. The stereoisomer pairs are now found on the stereo-free canonical SMILES: the same 9 pairs, 587 drugs, 140 positive. The split groups come from `scaffold_groups` (the same 443 groups, other folds).

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship: a real structure-based screen, split by scaffold with the SMILES as a typed structure (issue 1 resolved 2026-11-01); only the fit label should move to approximate for the undocumented negatives (issue 2). Priority 2: gap 0, use case 1, source 1, shape 0, risk -1.

CC (2026-11-11, Andrej): Four decisions from the v0.2 review page (folder the Review, issues 2-5): the fit becomes approximate, the scaffold split stays with the label's reporting window written down, all 587 drugs stay, and the record's collection facts are corrected.
- Fit `approximate` (issue 2, B): the source does not say how the negative drugs were chosen, most likely "no autoimmune reaction reported" as in the nearest documented set (Wu et al. 2021), an unverified label definition. `fit_reason` and a curation bullet name the gap; no row, split or score changes.
- Time basis (issue 3, B): no prototype fits, so the definition states the facts in a `Time basis:` line and claims no tag. The label is what had been reported by the compilation (InterDIA, 2025), so it accrues with a drug's time on the market: ChEMBL dates 496 of the 587 drugs by first approval, 1940-2020 (the API's `molecule_structures__canonical_smiles__flexmatch` and `first_approval`; 575 of the 597 source rows matched). The scaffold split stays: a forward split by approval year would test the delay of the label rather than the drugs. Untuned logistic regression, random forest and histogram gradient boosting on the source's RDKit descriptors over the 496 dated drugs, ROC AUC (Slurm job 1366251, 2026-11-06; the scaffold rows of the same run: 0.676 / 0.721 / 0.717):

  | Test from | Training drugs | Test drugs | Forward: LR / RF / boosting | Random folds of the same training size |
  |---|---|---|---|---|
  | 1990 | 219 | 277 | 0.606 / 0.642 / 0.607 | 0.716 / 0.740 / 0.721 |
  | 1995 | 267 | 229 | 0.582 / 0.698 / 0.714 | 0.716 / 0.777 / 0.754 |
  | 2000 | 351 | 145 | 0.617 / 0.692 / 0.765 | 0.740 / 0.794 / 0.803 |
  | 2005 | 399 | 97 | 0.692 / 0.828 / 0.810 | 0.752 / 0.812 / 0.825 |

- All 587 drugs kept (issue 4, B), the fact written into the curation notes and `fit_reason` instead of a row drop: the drugs approved from 2010 on are almost all negative (binomial p 0.0002 against the earlier drugs) and the structure shows the era (molecular weight alone separates that block at ROC AUC 0.693), but they are the drugs the use case screens for, and dropping them would take a tenth of a small dataset out on an inferred year. Positive share by approval era, on the shipped 587 drugs:

  | First approval | Drugs | Positive share |
  |---|---|---|
  | before 1960 | 41 | 0.415 |
  | 1960-1979 | 88 | 0.227 |
  | 1980-1999 | 222 | 0.270 |
  | 2000-2004 | 48 | 0.208 |
  | 2005-2009 | 45 | 0.178 |
  | 2010-2020 | 52 | 0.058 |
  | no ChEMBL year | 91 | 0.242 |

- Collection facts (issue 5, C): `Samples: No Time Dimension` becomes `Samples: Over Time`, with `Time: Dated` (the approval year comes from a parent source, ChEMBL, which dates 84% of the drugs) and `Target: Revised Later` (the label is assigned and then accrues as reports come in; venlafaxine is positive while its active metabolite desvenlafaxine is negative).
- Applied in `dataset.py`: `fit="approximate"` with the gap in `fit_reason`, three curation bullets (the fit, the time basis, the era gradient of the label), the reason for keeping the scaffold split in `splits_comment`; the metric's `reason` now dates InterDIA 2025, as its BibTeX does. `dataset check` 0 errors, 0 warnings, README regenerated. Not rebuilt (the build has been stale since 2026-10-14).
  - Huang L, Liu P, Huang X. InterDIA: Interpretable prediction of drug-induced autoimmunity through ensemble machine learning approaches. Toxicology. 2025;511:154064.
  - Wu Y, Zhu J, Fu P, Tong W, Hong H, Chen M. Machine Learning for Predicting Risk of Drug-Induced Autoimmune Diseases by Structural Alerts and Daily Dose. Int J Environ Res Public Health. 2021;18(13):7139. doi:10.3390/ijerph18137139
  - ChEMBL web services (https://www.ebi.ac.uk/chembl/api/data/molecule), queried 2026-11-06.

CC (2026-11-13, Andrej): time basis `UnseenGroup` instead of no prototype (2026-11-11):
- The use case aims at groups the data does not hold, which the held-out groups of the split stand for; `UnseenGroup` (SPLIT-32, the question before the prototypes) names that, where `Timeless` named the target and "no tag" named nothing.
- The split does not change; the definition's `Time basis:` line keeps the measured evidence.

## Review

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

## Reference

@article{huang2025interdia,
  title={InterDIA: Interpretable prediction of drug-induced autoimmunity through ensemble machine learning approaches},
  author={Huang, Lina and Liu, Peineng and Huang, Xiaojie},
  journal={Toxicology},
  volume={511},
  pages={154064},
  year={2025},
  publisher={Elsevier}
}
