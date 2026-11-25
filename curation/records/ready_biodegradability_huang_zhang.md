---
unique_name: ready_biodegradability_huang_zhang
name: Aerobic ready and inherent biodegradation of organic chemicals (Huang & Zhang 2022)
checked_by:
- AI (UNVERIFIED)
- Andrej
data_foundry_status:
- WIP (Triage)
claimed_by: Andrej
suggestion: TBD -> Yes
priority: 3
tags:
- Non-IID (Grouped)
- AI-Filled (Verify)
- Expanding Science Catalogue
- 'Samples: Over Time'
- 'Time: Lost'
- 'Entities: Recur'
original_source: Other
year: '2022'
collection_period: Unknown
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.1021/acs.est.2c01764
- '# the files, the route that works: datasets/external_data/class_all.csv and Huang_Zhang_RegressionDataset.xlsx'
- https://github.com/pkoerner6/Prediction-of-Aerobic-Biodegradability-of-Organic-Chemicals
- '# the curated versions of this data (Koerner et al. 2024), a choice inside this record'
- https://doi.org/10.1039/d4em00431k
v2_path: datasets/_dev/tabarena-v0pt2/ready_biodegradability_huang_zhang/dataset.py
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-25):** `TBD -> Yes`, priority 3: the ready-biodegradability question of `qsar_biodeg` on 6,139 chemicals instead of 1,055, compiled from eChemPortal screening-test records and a literature set; deep pass, with the counts, the label and the baselines measured on the files on 2026-11-25, which corrects the block of 2026-10-31 below.
- Source: Huang and Zhang, "Classification and Regression Machine Learning Models for Predicting Aerobic Ready and Inherent Biodegradation of Organic Chemicals in Water", Environmental Science & Technology 56(17), 2022 (doi 10.1021/acs.est.2c01764). Methods, Dataset Preparation: the data was "mainly collected using the eChem portal", only reliability 1 and 2 records, "All ready and inherent biodegradation data for aerobic conditions were included", "more than 20,000 records" curated to the 12,750-record `RegressionDataset`. As published for classification, measured: `ClassDataset_original` 4,593 chemicals derived from the regression set, `ClassDataset_external` 1,546 compiled from the literature as a second source, `ClassDataset_all` 6,139 = the two together, one row per chemical, 6,137 distinct canonical structures, 34.9% readily biodegradable, every SMILES parses, 1,546 rows without a CAS number. The earlier block read 6,139 as the original alone and 6,032 as the regression set: it is 4,593 and 6,139, and the regression file is 12,750 records on 6,102 CAS numbers. The ACS article and its supporting information refuse an automated download (403, no archive copy), so the files come from Körner et al.'s repository (`datasets/external_data/class_all.csv` and `Huang_Zhang_RegressionDataset.xlsx`, GPL-3.0); both were downloaded and read on 2026-11-25.
- Target: the label is a reading of the test result, not a column of the source. Rebuilt from the regression workbook as the ready endpoint at 28 days with at least 60% degradation (70% for DOC die-away), it reproduces 4,495 of the 4,591 classes of `ClassDataset_original` (97.9%); the same rule is in Körner's code. Guideline mix of the 6,130 ready 28-day records: OECD 301 F 24.6%, 301 B 23.4%, 301 C 22.5%, 301 D 17.2%, 310 2.7%, 301 A and 301 E 2.6% each, EU Method C.4 variants 3.7%, against OECD 301 C alone in `qsar_biodeg`. The paper reads the series as one protocol: the guidelines "were originally designed to be equivalent except that they can handle chemicals with different physicochemical properties", and the DOC threshold is 70% because DOC methods read higher.
- Use case: a producer or registrant screens a structure before commissioning a ready-biodegradation test, and a regulator prioritises chemicals for persistence assessment. The paper's own reason is the test (Introduction): "As most experimental tests normally last at least 28 days, the cost for testing a sample commonly falls in the range of 3000-8000 USD or more ... This is a significant financial burden to industries that need to develop environmentally friendly chemical products"; the closing section names "the research community, chemical industries, and regulators" and "more accurate risk assessment of the existing and new chemicals". Fit direct: the only input is the structure, which exists before any test. Collection `Samples: Over Time` (dossiers and studies accumulate), `Time: Lost` (no test date in the classification file, the regression workbook or Körner's REACH export; eChemPortal links each record to its dossier page, which was not scraped), `Entities: Recur` (12,750 records on 6,102 CAS numbers in the parent file, and about 102 structures in both parts of `ClassDataset_all`); type `Expanding Science Catalogue`, a registration and screening programme that keeps growing, as for `qsar_biodeg`.
- Split: leaf `L-FAMILY.key`, grouped on the Bemis-Murcko scaffold with `UnseenGroup` (SPLIT-31, SPLIT-36), because the use case screens chemicals like those already registered rather than the catalogue's next entries (`CAT.next-items` no, the answer `qsar_biodeg` carries) and the data computes a scaffold key: 1,308 distinct scaffolds over the 6,139 chemicals, measured, against 209 in `qsar_biodeg`. Nothing dates the rows, so `CAT.entry-date` is no and the walk reaches the same leaf whichever way the first question is answered; there is no temporal option. Open: whether structures that are one chemical once stereochemistry is set aside share a group.
- Siblings and duplicates: `qsar_biodeg` (`Yes`, shipped; NITE/MITI through Mansouri et al. 2013), `qsar_biodegradation` (`No`, its copy), `ready_biodegradability_mansouri_external` (`TBD -> 2nd Tier`, 670 chemicals, 619 of them in this set). Not a duplicate of `qsar_biodeg`, which ends at another original source (PROV-4), but it holds 1,011 of its 1,055 chemicals (95.8%) on canonical SMILES or CAS-RN, 976 of them with the same class, and a model trained on the 5,183 chemicals it holds beyond them scores 0.938 ROC AUC on `qsar_biodeg`'s own 1,055, as high as one trained on `qsar_biodeg` under its own split (0.935); all measured. The pair is the curator's decision (Assessment of 2026-11-12 below). Körner et al.'s `Curated_SCS`, `Curated_final` and `Curated_BIOWIN` are cuts of the same data with no distinct task, so they are versions to choose inside this record, not records of their own (PROV-6). External collections: none found.
- Better data: found as better data for `qsar_biodeg`. Nothing larger for the same task: OPERA `RBiodeg_QR` 1,603 structures (1,444 of them inside this set), NITE's CSCL workbook 1,363 chemicals, Körner's REACH export 2,858 chemicals, Lunghini et al. 2020's "Global" set 3,146 compounds (a publisher's supplementary file, not obtained), VEGA distributes models rather than a table; a search for a 2023-2026 compilation larger than 6,139 found none.
- Papers and pages: Huang and Zhang 2022 as above, with two public prediction services for its models. Körner, Glüge, Glüge and Scheringer, "Critical insights into data curation and label noise for accurate prediction of aerobic biodegradability of organic chemicals", Environ. Sci.: Processes Impacts 2024 (doi 10.1039/d4em00431k), re-derives the set from its own ECHA export and reports mismatched chemical identifiers and train/test leakage between the two parts; its article page refuses an automated fetch (403), so what is said about it here is read from its repository README and its code, not from the article.
- Metric: no deliberate choice. The paper evaluates "based on different matrices, including accuracy, sensitivity, specificity, balanced accuracy, ROC AUC, and f_1" (Methods) and reports all six side by side for the final model (85.6, 90.3, 80.4, 85.4, 91.8 and 85.1%) without naming the one that decides (MET-5); its threshold metrics fix no threshold and no cost (MET-6), and Körner et al. rank by balanced accuracy, equally unfixed. So the fallback `roc_auc` (MET-8), which is also what `qsar_biodeg` declares; inputs none. The paper's own split was built "to ensure high similarities of chemicals among the training, validation, and test subsets", so its published numbers say nothing about a scaffold split (SPLIT-5).
- Risks for /add-dataset: first the 10-day window. The rebuilt label is "at least 60% at day 28" and ignores the pass window the OECD 301 series requires, and 505 of the 8,115 records of Körner's REACH export (6.2%) carry the registrants' own verdict "readily biodegradable, but failing 10-day window", which is not readily biodegradable to the actor who acts on it (measured); that export carries `interpretation_of_results` for 2,858 chemicals if the record wants the regulatory reading (TP-6, USE-1). Then: repeat tests that disagree are kept with one class for 209 of the 4,966 chemicals with a 28-day ready test (4.2%); 2 exact duplicate structures, 145 pairs that are one chemical once stereochemistry is set aside (15 with conflicting classes) and 22 repeated CAS numbers (6 conflicting), so copies are dropped or held on one side (LEAK-19); 100 structures of the 1,546 literature rows (6.5%) are also in the 4,593, 7 with the opposite class; the `pka_*` and `α_*` columns are Körner's, computed from the structure, and leave as the Dragon descriptors did (CLEAN-24); descriptors are computed per fold, never over all rows (LEAK-29). The version to ship is an open choice and not a free gain: `Curated_SCS` (5,185) repairs the identifiers but also drops every chemical whose repeat tests disagree, so it removes the ambiguity `ClassDataset_all` keeps (read from Körner's code), and `Curated_final` / `Curated_BIOWIN` drop the hard cases by other models' predictions (TP-6).
- Priority: gap 0 (chemistry, binary classification and grouped splits are all well covered), use case + (the actor, the moment and the cost of the test are the source's own words), source + (peer-reviewed, reliability-filtered regulatory records, a second paper auditing it, files reachable), shape + (6,139 chemicals, 1,308 scaffolds, the label reproduced for 97.9% of the rows, and untuned LightGBM beats logistic regression by 0.076 ROC AUC over 3 x 10 scaffold-grouped folds against 0.025 on `qsar_biodeg`), risk - (the label ignores the 10-day window, and the repeat tests of 4.2% of the chemicals disagree).

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: ready biodegradability (yes/no) of about 6,100 chemicals with SMILES, compiled (per the run's Assessment) from REACH screening-test records, the task of `qsar_biodeg` on about six times the chemicals; a later study shows label noise and identifier errors in it, so the curator chooses between the original and its curated version.
- Source: Huang and Zhang, "Classification and Regression Machine Learning Models for Predicting Aerobic Ready and Inherent Biodegradation of Organic Chemicals in Water", Environmental Science & Technology 56(17), 2022 (doi 10.1021/acs.est.2c01764; the paper and its supporting information were not reachable, 403). As carried by Körner et al.'s repository (GPL-3.0): `datasets/external_data/class_original.csv` (1.8 MB; header previewed: name, name_type, cas, source = `ClassDataset_original`, smiles, y_true, plus pKa and speciation columns Körner added), `class_external.csv`, `class_all.csv`, and `Huang_Zhang_RegressionDataset.xlsx` (2.0 MB); curated versions in `datasets/curated_data/` (`class_curated_final.csv`, `class_curated_scs.csv`, `class_curated_biowin.csv`). The sizes in the Assessment below (6,139 substances; 12,750 regression records on 6,032 substances) come from the run, not re-counted.
- Use case: a registrant or regulator screens a chemical for persistence under REACH before or instead of an OECD 301 test (the label is the outcome of such tests); fit direct for a new chemical, approximate until Huang and Zhang's own statement is read. Regime grouped on the Bemis-Murcko scaffold, as for every molecule set with exact structures (SPLIT-31 as amended 2026-10-26).
- Siblings and duplicates: `qsar_biodeg` (`Yes`, TabArena v0.1: Mansouri et al. 2013, 1,055 chemicals with 41 descriptors) and its copy `qsar_biodegradation` (`No`); another compilation of overlapping test data, so not a duplicate (PROV-4), but some chemicals will be in both. Körner's curated sets are versions of this one (PROV-6). External collections: none found.
- Better data: found as better data for `qsar_biodeg`; no further search this round.
- Papers and pages: Huang and Zhang 2022 (ES&T); Körner, Glüge, Glüge, Scheringer, "Critical insights into data curation and label noise for accurate prediction of aerobic biodegradability of organic chemicals", Environmental Science: Processes & Impacts 2024 (doi 10.1039/d4em00431k), whose README reports correcting "mismatched chemical identifiers and data leakage between training and test sets" and removing chemicals with high variance across studies, balanced accuracy 80.9% before and 94.2% after filtering possibly noisy labels, and warns that filtering may have removed difficult-to-learn substances.
- Metric: Huang and Zhang's metric not read (paper unreachable); Körner et al. name balanced accuracy, a threshold metric with no threshold or costs fixed (MET-6), so the fallback `roc_auc` (MET-8); inputs none.
- Risks for /add-dataset: label noise (one chemical tested several times with conflicting results; how the original resolved them) and the CAS-SMILES mismatches Körner found: repair from the origin (PROV-13) or ship the curated version, but not the label-noise-filtered one, which drops the hard cases on purpose (a target the curation chose, TP-6); the Körner speciation columns are his additions, not the source's; the chemicals shared with `qsar_biodeg`; descriptors computed from SMILES per fold, never from all rows (LEAK-29). The regression set (percent degradation by guideline and duration) mixes test types and is a second task to judge on its own.
- Priority: gap 0 (chemistry, binary, grouped are not thin), use case 0 (not read from the source), source + (a peer-reviewed compilation; the REACH origin per the run, not read), shape + (about 6,100 chemicals with structures, scaffold groups), risk - (label noise and identifier errors shown by Körner et al.).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `qsar_biodeg`.
- as published: classification: 6,139 substances (ready biodegradable yes/no); regression: 12,750 test records on 6,032 substances (percent degradation with test guideline and duration); compiled from ECHA REACH ...; target: ready biodegradable (yes/no) from OECD 301-type screening tests; access: open (copies in Koerner et al.'s repository, datasets/external_data/class_original.csv and Huang_Zhang_RegressionDataset.xlsx, GPL-3.0; the ES&T supporting information as the original was not opened).
- Why: Same target (ready vs not ready biodegradable) and unit (the chemical) as qsar_biodeg, with structure-derived features known before the test
- Adds: About 6 times more chemicals (6,139 against 1,055), a newer and regulatory source (REACH dossiers), structures given (RDKit descriptors and a scaffold split as for the other SMILES datasets); Koerner et al. 2024 publish a curated version with a label-noise analysis

**Assessment (AI, 2026-11-12):** pair with `qsar_biodeg` open (Andrej's decision on its review, 2026-11-12): when this set is added, match its chemicals to qsar_biodeg's 1,050 on canonical SMILES and CAS-RN, report the share of qsar_biodeg's chemicals found here and their class agreement, and put the pair to the curator; qsar_biodeg is retired if this set holds most of its chemicals with the same class.

**Assessment (AI, 2026-11-25):** review panel (full): ship after changes; disputed: USE-8 (the fit word, issue 1), LEAK-19/LEAK-20 (whether the copy key takes a last step to the CAS number, issue 2), PROV-13 (repair or drop the 29 rows that carry another substance's structure, issue 3); for the curator: issues 1-5. Priority 3: gap 0, use case +, source +, shape 0, risk - (chemistry, binary classification and grouped splits are all well covered; the actor, the moment and the cost of the test are the source's own words; a peer-reviewed compilation of reliability-filtered regulatory records, with a second paper auditing it and the files reachable; 5,719 chemicals with one feature, the structure, and a real spread between methods - untuned LightGBM 0.886 against a linear 0.789 and a dummy 0.500; the label pools seven protocols that disagree on 26.9% of the chemicals tested under more than one, and about 0.5% of the rows carry another substance's structure).

**Assessment (AI, 2026-11-25):** the review panel corrected five facts of today's screening block, which stays as written. EU Method C.4 is 4.4% of the 6,130 28-day ready records in its four variants, not 3.7% (the C.4-C variant, 0.7%, was left out of the list). The article is readable after all: the accepted manuscript is free at par.nsf.gov/servlets/purl/10350359 and every sentence the definition quotes from the paper checks out against it word for word, while the data files of the supporting information stay ACS-only, so the Körner route and the unknown licence stand. Körner et al.'s curated sets are not cuts of this file: their code concatenates Lunghini et al. 2020's set onto their own ECHA-derived compilation, so they are a different compilation plus an addition, and part of the Lunghini set the block calls "not obtained" is in that repository. The overlap with qsar_biodeg is 1,005 of its 1,055 chemicals (95.3%) with 976 (97.1%) agreeing, measured on the key the definition now uses, against the block's 1,011 and 976 on canonical SMILES or CAS-RN. The label rebuild reproduces 4,482 of 4,591 classes (97.6%) under the rule that any 28-day test passing makes the chemical ready; the block's 4,495 (97.9%) is the majority rule - both numbers are real, on two rules.

**Assessment (AI, 2026-11-25):** for the open pair with qsar_biodeg (issue 5 of that record's review, where the decision of 2026-11-12 put it), measured here on 2026-11-25: this set holds 1,005 of its 1,055 chemicals (95.3%), 976 of them (97.1%) with the same class. What the replacement is not is the same label on more chemicals: qsar_biodeg is OECD 301 C alone, where the pass rate is 27.2% and the 10-day window does not apply, while this label pools seven protocols (33.8% pass here, and 26.9% of the 688 chemicals tested under more than one guideline get opposite calls). Folding in the 102 chemicals the sibling has and this set lacks measures 0.893 against 0.890 ROC AUC, no measurable gain; it is issue 4 of this record's review.

CC (2026-11-25, Andrej): review of the added dataset (Review 1 to 5).

CC (2026-11-25, Andrej): review issue 1, A: the fit stays `direct`, with the gap named in the fit reason. The label is the day-28 reading and leaves out the 10-day window, but its definition is the source's own and reproduced at 97.6%, the task is the screen the source deploys, and its test chemicals are no easier than the chemicals a registrant would screen next. The comments keep the fact that qsar_biodeg is OECD 301 C alone, where the window does not apply.

CC (2026-11-25, Andrej): review issue 2, A: the copy key stops at the structure, the InChIKey connectivity block of the desalted, stereo-free compound, with no further step to one row per CAS number. The 8 CAS numbers that still name two rows each stay, named in the copies bullet.

CC (2026-11-25, Andrej): review issue 3, B: "Option B: Repair from ECHA where its formula and its weight agree with each other and disagree with the shipped structure." The rows whose structure is not the substance their CAS number names take ECHA's own structure from the dossier export of the same release, and the rows the file contradicts by itself leave.

CC (2026-11-25, Andrej): review issue 4, A: qsar_biodeg's 102 extra chemicals are not folded in - one provenance per record, and the merge measured no gain, so the sibling retires as replaced rather than absorbed, which its own record decides.

CC (2026-11-25, Andrej): review issue 5, B: "Option B: Accept with the sibling's text and its rider." `meta_license_unknown` is accepted with the text qsar_biodeg carries - the article states no licence for the supporting information that holds the data, and the GPL-3.0 of the repository the file is copied from governs its code and not the data it redistributes - and with the rider that the licence is regularised before the data ships outside the group.

**Assessment (AI, 2026-11-25):** the decisions above are applied; measured on the frame that now ships (2026-11-25). The repair reads `iuclid_echa.csv` from the same release, which gives one molecular formula and one molecular weight for 2,764 registered substances, always agreeing with each other, and reaches 1,901 of the 6,139 rows (31.0%). 34 of those rows (1.8%) carry a structure that is neither the composition ECHA's formula gives nor the substance ECHA's own structure draws, and whose weight is more than 0.5 from ECHA's: 19 take ECHA's structure, 15 keep the published one (11 dossiers carry no structure, 4 contradict their own formula). 4 further rows leave on the internal name-against-structure check: they name a carbon skeleton (limonene, an azo dye, a zinc neodecanoate, a butylpyridinium aluminate) and hold no carbon at all. The 270-of-3,767 bulk comparison against Körner et al.'s curated structures and the 1,546 literature rows, which carry no CAS number, stay out for their scale. 5,714 chemicals ship, 33.8% readily biodegradable, 4,389 from the original part and 1,325 from the literature one; 4,329 scaffold groups, 1,792 to 2,101 test rows a fold. `dataset check`: 0 errors, 0 warnings (1 accepted). Probes: no leak flag, 0.0% of the 17,142 test evaluations have an exact feature copy in training; untuned LightGBM 0.890 and a random forest 0.889 against a linear 0.791 and a dummy 0.500, spread +0.198; IID 0.893 against grouped 0.887, gap 0.007. The 19 repairs leave the duplicate structure untouched: 110 clusters the InChIKey step adds, none of them holding a repaired row, and 8 CAS numbers still on two rows each. The sibling overlap is now 1,001 of qsar_biodeg's 1,055 chemicals (94.9%), 972 of them (97.1%) with the same class.

## Review

**Outcome:** added, and settled: Andrej decided issues 1 to 5 on 2026-11-25, and they are applied. Huang and Zhang's `ClassDataset_all` as Körner et al.'s repository carries it: 6,139 chemicals, the classification reading of 4,593 of the authors' own eChemPortal screening records plus 1,546 compiled from the literature, which become 5,714 once the structures ECHA's own dossier contradicts are repaired (issue 3) and copies of one compound are resolved on the house key for molecules. One feature, the chemical's structure as a declared SMILES; target `Biodegradable`, 33.8% `Yes`; fit `direct` with the 10-day window named as a bounded gap (issue 1); grouped on the Bemis-Murcko scaffold of the desalted compound (4,329 groups, 3 repeats of 3 folds, 1,792 to 2,101 test rows); `roc_auc` as the fallback, the paper reporting six metrics side by side without naming the one that decides. Validity: the only input is a structure that exists before any test is commissioned, so no value here can be recorded late; the task gamer, with the participant kit and no notes, found no exploit above +0.0016 ROC AUC against a ±0.0003 noise band, and the claim auditor checked 46 statements of which 41 hold, several to the digit. Value: on the probes re-run after the repair, untuned LightGBM 0.890 and a random forest 0.889 against a linear 0.791 and a dummy 0.500, a spread of +0.198, and an IID-against-grouped gap of 0.007; no leak flag, and 0.0% of the 17,142 test evaluations have an exact feature copy in training. `dataset check`: 0 errors, 0 warnings (`meta_license_unknown` accepted, issue 5).

**Main points:** All five issues are decided and applied: the fit stays `direct` with the window written down (1), the copy key stops at the structure, leaving 8 CAS numbers on two rows each (2), the 19 rows ECHA's dossier contradicts take ECHA's structure and 4 rows the file contradicts by itself leave (3), `qsar_biodeg`'s 102 extra chemicals stay out (4), and the licence warning is accepted with the sibling's text and its rider (5). The pair with `qsar_biodeg` itself stays on that record, where the decision of 2026-11-12 put it; the comments carry the two facts it needs. Applied earlier without a decision: the panel's one change to the data, the copy key now running to the InChIKey connectivity block, which closes the 2.2 to 2.4% of test rows that had their own chemical in training (those rows scored 0.929 against 0.884) and costs 126 rows; and in the text, the 10-day window named in `fit_reason` and the question reworded to the day-28 reading, the pooled-protocol table (27.2% pass under 301 C against 52.7% under 310, and 26.9% of the 688 chemicals tested under more than one guideline getting opposite calls), the three-way analogue breakdown with the price of the bare-benzene rule, the CAS registration order in `time_basis`, the free manuscript link, the release's unlisted files, the multi-component and carbon-free rows, and four corrected statements.

**Record judgment:** the panel's judgment record (mediator):

```text
Verdict: ship after changes.
Validity: SEL-1/SEL-2 hold; USE-1 holds (the one input is a structure, known before any test);
  USE-5 holds (the day-28 reading is the source's own assay, read without the window clause, not
  another quantity - chicago_traffic_crashes bar, Lennart 2026-11-05); USE-8 triggered: the gap is
  not in `fit_reason` - write it; the word direct/approximate is the curator's (issue 1).
  LEAK-10 holds; LEAK-29 holds (nothing fitted over all rows); LEAK-19/LEAK-20 triggered and
  departed from without a stated reason - fixed in the copy key (house key of molecules.md).
  SPLIT-1, SPLIT-24, SPLIT-31 (as amended 2026-10-26), SPLIT-36, SPLIT-37 hold; the split stays,
  its description is corrected. PROV-1/PROV-4 hold; PROV-13 triggered: ~29-35 rows carry another
  substance's structure and the origin's own data is in the release - repair or drop (issue 3).
Value: TP-2, a large real signal (LightGBM 0.885, dummy 0.500, forest-linear +0.196, 628-710
  positives a test fold); MET-2, MET-5, MET-6, MET-8 hold, roc_auc confirmed verbatim against the
  paper.
Quality: CLEAN-24 (amended, Lennart 2026-11-01) held against the blind reviewer's "pre-encode or
  exclude": no change. CLEAN notes added for the multi-component and the carbon-free rows.
Weighed: size +, source +, use case +, gap 0, risk - (pooled protocols, label damage in ~0.5%).
For the curator: 5 issues, of which 1 and 2 are weighing calls and 3 is a Must whose remedy is a
  choice between repair and drop.
```

The panel measured the frame as it stood before the copy-key fix, so the block above and the panel's own sections are two steps behind the folder. The fix is applied as one pass of the new key over the raw rows, so it drops 420 rows rather than the 428 of the mediator's two-stage estimate: 5,719 chemicals, 33.8% of them readily biodegradable. The repair of issue 3 then took 19 structures from ECHA's dossiers and dropped 4 rows the file contradicts by itself, and the frame that ships is 5,714 chemicals, still 33.8% readily biodegradable. Every number the notes state was re-measured on that last frame, which moved the group counts (4,329 groups), the analogue shares, the sibling overlap (1,001 of `qsar_biodeg`'s 1,055 chemicals, 94.9%, with 97.1% agreeing) and the headline (0.890 on the task probe).

**Issues for Andrej:**

1. **Does the fit stay `direct` now that the 10-day window is written down?**

   - **Problem:**
     - The shipped label is the test reading at day 28, while the OECD 301 series requires the pass level to be reached inside a 10-day window before a chemical counts as readily biodegradable.
     - On the 28.5% of the chemicals that Körner et al.'s REACH export reaches, the registrants' own conclusion turns 89 of 778 positives negative (11.4% of them, 1.6% of all chemicals here), measured three times independently.
     - The gap is uneven and the guideline is not a shipped column: 1.4% of the 301 C records, where the window does not apply, against 13 to 23% of the rest.
   - **Background:** the label definition itself is settled and verified: at least 60% degradation at day 28, 70% where the method follows dissolved organic carbon, the rule the paper states and Körner et al.'s code implements, rebuilt from the authors' own regression workbook on 4,482 of 4,591 chemicals (97.6%). What sets this set apart from its sibling belongs in the record either way: `qsar_biodeg` is OECD 301 C alone, where no window applies, so that label *is* the regulatory conclusion and this one is not.
   - **Effect on the task:** none on the container: A and B ship identical data, and the word sets how the benchmark describes its own target.
   - **Experiments:** the registrants' own verdicts in the REACH export, by guideline (share of the records called readily biodegradable in any form that are flagged "but failing 10-day window"):

     | Guideline | Records called readily biodegradable | Flagged "failing 10-day window" |
     |---|---|---|
     | OECD 301 B | 1,005 | 15.7% |
     | OECD 301 F | 881 | 16.8% |
     | OECD 301 D | 643 | 13.7% |
     | OECD 301 E | 133 | 22.6% |
     | OECD 310 | 122 | 13.1% |
     | OECD 301 C (MITI) | 348 | 1.4% |

   - **Panel:** split, and the mediator left the weighing here. The advocate and the domain practitioner, the one agent playing the actor, hold for `direct` ("I would not move the fit to approximate for it: the label is verified, documented and reproduced at 97.6%"); the critic and the precedent checker hold for `approximate`, because a gap that is measured should not thereby become direct.
   - **Consistency:** `account_debt_south_africa` and `coffee_rating_prediction` read approximate for gaps that are perfectly well understood, and `diabetes_3` and `differentiated_thyroid_cancer_recurrence` for label gaps that were smaller or unverified. Against that, the rule that narrows the approximate case asks whether the data mirrors another well-defined use case practitioners have[^f1]: the day-28 screen is the source's own deployed classification task, served deliberately "without specifying the experimental conditions and reaction time", not a use case rephrased here to excuse a gap. The practitioner also measured the screening population: 19.9% of the 846 registered chemicals outside the compilation have a close analogue in a training-sized sample, against 18.9% for the test folds, the opposite direction from `qsar_oral_toxicity`, which reads approximate.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | `direct`, the gap named as a kept, bounded gap (implemented) | `fit_reason` now names the window, the measured flip rate and its unevenness; no row changes | the label definition is settled and reproduced at 97.6%, which is what the approximate cases lack; the task is the source's own deployed screen, with its test chemicals no easier than the next registered chemical; the sibling and the QSAR folders stay comparable | a measured gap to the conclusion the actor acts on is described as direct, which the approximate cases above would not be |
     | B | `approximate`, the same text in `fit_reason` | One word in the task summary; no row changes | matches the house cases where a known gap to the actor's quantity made the fit approximate; nothing is lost, since the container is identical | reads as a weaker dataset than it is: inputs, timing and split are exact and the label is verified to the digit |
     | C | Drop the 89 chemicals the registrants' conclusion contradicts | 5,719 rows become about 5,630 | the target column then contains no chemical known to be called the other way | the audit covers a quarter of the set, so dropping only the audited contradictions selects on coverage; the sources' own class leaves the file |

   - **Recommendation:** A. The gap is now written in `fit_reason` whichever way this goes, and the three facts that decide it point one way: the definition of the label is the source's own and verified, the task the benchmark poses is the screen the source deploys, and the actor's own test chemicals are no easier than the chemicals they would screen next. B is defensible, since a measured gap is still a gap, and it costs nothing, which is why the panel split on it. **Decision:** keep `direct` with the gap named (A), move to `approximate` (B), or drop the 89 contradicted chemicals (C)?

   **Notes for the AI:** B is `fit="approximate"` in `task_summary` and nothing else; the `fit_reason` text already names the gap. C drops in `_clean` the chemicals whose CAS number carries only "readily biodegradable, but failing 10-day window" conclusions in `iuclid_echa.csv`, which means downloading that file as a second source and naming it in `download_description` and `sources`. Whichever is chosen, keep the sentence in the comments that `qsar_biodeg` is 301 C alone.

   [^f1]: **USE-8** (Must): write how closely the data mirrors the use case; approximate is "a stand-in with a known gap, named as such". **USE-9** (Should; narrows USE-8): before settling on approximate, ask whether the data as shipped mirrors another well-defined use case practitioners have, weighed against a use case rephrased only to excuse a gap. **USE-5** (Must): predict what the actor acts on; it fails only when a label is shown to be another quantity (Lennart, `chicago_traffic_crashes`, 2026-11-05), which the mediator found not to be the case here.

   **Andrej (2026-11-25, ok):** As implemented (A).

   **Resolved (2026-11-25, Andrej):** A: `fit="direct"` stays and `fit_reason` keeps the gap, re-measured on the frame that ships after issue 3: the label is the day-28 reading, and on the quarter of the chemicals the REACH export reaches the registrants' own conclusion turns 89 of 779 positives negative, 1.6% of all rows. No row changes for this issue, and the comments keep the sentence that `qsar_biodeg` is OECD 301 C alone, where the window does not apply.

2. **Does the copy key take one more step, to one row per CAS number?**

   - **Problem:**
     - The copy key now goes to the InChIKey connectivity block of the desalted, stereo-free structure, which is the house key for molecules, and after it no two shipped rows are one structure.
     - Eight CAS numbers still name two rows each (16 rows), two of them carrying both classes, because the two rows are written as different substances.
     - A CAS number names a substance rather than a structure, and 1,330 of the shipped rows, the literature part, carry none at all.
   - **Background:** the decision item of 2026-11-25 assigned this choice to this record. `aquatic_toxicity_lunghini_consensus`, built in the same batch, keys on an InChIKey skeleton or a CAS number, which is an AI draft on its own review and not yet a decision.
   - **Effect on the task:** about 10 further rows and nothing measurable on the score; the two conflicting pairs cost every method the same points.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Stop at the structure key, name the remnant in the notes (implemented) | The 8 repeated CAS numbers stay, named in the copies bullet | the key is one a 2D encoding can see, so no row is merged that a model could tell apart; it applies to every row, not to the three quarters that carry a CAS number | two chemicals of one registered substance can sit on both sides of the split |
     | B | Add the CAS step after the structure key | One row per CAS number, both-class CAS numbers dropped whole: about 10 fewer rows | the second key the decision item named, and the one the sibling built in this batch uses; a CAS number is what an actor acts on | merges rows whose structures genuinely differ (a salt family, a reaction mass written two ways); the literature quarter has no CAS, so the key is uneven |

   - **Recommendation:** A. The remnant is 16 rows, the rule asks for the key a model can see, and a CAS key would reach only the three quarters of the set that carry a CAS number; the sibling's CAS step is itself an open draft, so there is no settled call to follow. If the answer here is B, the sibling's own review should be answered the same way. **Decision:** stop at the structure key (A) or add the CAS step (B)?

   **Notes for the AI:** B is one more `groupby` in `_clean` on the raw `cas` column before the structure key, with the same drop-both-classes-then-keep-one rule and `NaN` rows kept; it changes the counts in the copies bullet, in `task_summary.row` and in `_decisions`, and needs the probes re-run.

   **Andrej (2026-11-25, ok):** As implemented (A).

   **Resolved (2026-11-25, Andrej):** A: the copy key stays the InChIKey connectivity block of the desalted, stereo-free compound, and no CAS step is added. On the frame that ships after issue 3 the remnant is unchanged: 8 CAS numbers name two rows each (16 rows, 2 of them with both classes), and the copies bullet names them. `aquatic_toxicity_lunghini_consensus`, whose key takes a CAS step, keeps that as the open draft of its own review; nothing here moves it.

3. **Repair the rows that carry another substance's structure, or drop them?**

   - **Problem:**
     - 29 of the 1,840 shipped rows that can be matched to ECHA's own registered substance (1.6% of them, 0.5% of the set) carry a structure that is not that substance, which is damage in the only input column.
     - The origin's clean data is in the release the definition already downloads: `iuclid_echa.csv` carries ECHA's `molecular_formula`, `molecular_weight` and `smiles_echa` for 2,858 CAS numbers, so these rows can be adjudicated without a new source[^f2].
     - Three of them need no outside source at all: limonene is shipped as calcium oxide, an azo dye as sodium sulfate, a butylpyridinium aluminate as ammonium aluminium sulfate.
   - **Background:** the reason first recorded for not repairing, "no third source", is wrong; the reason that does hold is scale: the bulk disagreement with Körner et al.'s curated structures is 270 of 3,767 shared CAS numbers, a lookup and an adjudication of its own, and the 1,330 literature rows carry no CAS number to adjudicate by. That bulk comparison stays out of scope either way.
   - **Effect on the task:** about half a percent of the rows ask a model to predict one substance's test result from another substance's structure.
   - **Experiments:** three measurements of the same thing, the first two on the frame as it stood before the copy-key fix, the third on the frame as it ships now:

     | Measurement | Rows reached by CAS | Same parent | Another substance |
     |---|---|---|---|
     | column audit, molecular formula only | 1,791 | 95.5% | 35 (1.95%) |
     | mediator: parent, hydrogens ignored, counter-ions normalised | 1,852 | 98.2% | 29 (1.57%) |
     | the same, on the shipped frame | 1,840 | 98.2% | 29 (1.58%, 0.51% of all rows) |

     Every one of the 29 is a CAS number for which ECHA reports a single molecular formula, so the dossier is not itself ambiguous. The examples the panel names: CAS 163802-53-7, a silyl sorbate shipped as phenothiazine; 18162-75-9, a silylmethyl morpholine shipped as morpholine; 1173693-36-1, a difluorophenyl isoxazole shipped as chlorobenzene; 6156-18-9, 4927-36-0 and 6259-53-6.

   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Ship as published, with the damage measured in the notes (implemented) | The copies bullet names the share and the file that could adjudicate it | no structure is replaced by a parse of a dossier; the published compilation stays what the paper published | keeps a known wrong input where the origin's own answer is at hand, which the rule on damaged data does not allow[^f2] |
     | B | Repair from ECHA where its formula and its weight agree with each other and disagree with the shipped structure | About 29 structures are replaced by `smiles_echa`; a second file of the same release enters `_load_raw` | the remedy the rule asks for, and the one two QSAR siblings took; two concordant dossier fields decide each case | `smiles_echa` is Körner et al.'s parse of the dossier, so a repaired structure is one source's reading; a second raw file to download and check |
     | C | Drop those rows | About 29 rows leave (0.5%) | no parse enters the data, and the known-wrong rows are gone | loses real test results, and the drop is itself a selection: only the CAS-matchable 30% of the set is audited |
     | D | Repair the unambiguous ones, drop the rest | B where formula and weight agree, C where they do not | takes the cheapest honest answer per row | two rules for one defect |

   - **Recommendation:** B, together with the internal check the practitioner names (an element in the chemical's name that its structure does not contain), which needs no outside source, catches the three visible cases and is added whichever of B, C and D is chosen. The rule puts repair above a note when the origin has the clean data, and here it does; C throws away test results for a defect that is adjudicated by two concordant dossier fields. **Decision:** keep as published (A), repair (B), drop (C), or repair the unambiguous and drop the rest (D)?

   **Notes for the AI:** B adds `iuclid_echa.csv` to the copy source's `files` and to `download_description`, builds the ECHA formula and weight per CAS in `_clean`, and replaces `SMILES` where both disagree with the shipped structure; the record and the copies bullet then say how many rows were repaired, and the leak, task and group probes are re-run because the structures change. The name-vs-element check goes into `_clean` under B, C and D alike. The 270-of-3,767 bulk comparison against `Curated_SCS` and the rows without a CAS number stay out of scope, with scale as the stated reason.

   [^f2]: **PROV-13** (Must): check whether the origin has the clean data before keeping damaged data, and repair when it has; the remedy ladder puts repair above a note. Cases: `qsar_bioconcentration` (2026-10-07) and `qsar_oral_toxicity` (2026-10-21) repaired structures from PubChem and Wikidata; `nci_aids_antiviral_screen` (Lennart, 2026-11-02) kept where the damage was not demonstrable.

   **Andrej (2026-11-25, change):** "Option B: Repair from ECHA where its formula and its weight agree with each other and disagree with the shipped structure."

   **Resolved (2026-11-25, Andrej):** B, with the name-against-structure check the recommendation adds. `_load_raw` now joins `iuclid_echa.csv` of the same release (its own `Source(files=...)` entry, hash and download line) onto the rows by CAS number, three columns wide: ECHA's molecular formula, molecular weight and structure. `_clean` repairs a row when the dossier's formula and weight agree with each other and both disagree with the shipped structure, which has neither the composition the formula gives nor, once salts and repeated fragments are resolved, the substance ECHA's own structure draws, and whose weight is more than 0.5 from ECHA's; the replacement is taken only where ECHA's structure parses and has the composition its own formula gives, so nothing enters the data against the dossier. **19 rows are repaired** - 2,2-bis(methylthio)propane, shipped as a fluorophenyl thiourea sulfonamide; a trimethoxysilyl sorbate, shipped as phenothiazine; a difluorophenyl isoxazole, shipped as chlorobenzene, among them - of 34 rows the dossiers contradict, out of the 1,901 of 6,139 rows (31.0%) a dossier reaches. The other **15 keep the published structure**: 11 dossiers carry no structure at all and 4 carry one that contradicts their own formula; the copies bullet names them. The internal check drops **4 rows** whose name states a carbon skeleton while the structure holds no carbon (limonene drawn as calcium oxide, an azo dye as sodium sulfate, a zinc neodecanoate as zinc sulfate, a butylpyridinium aluminate as ammonium aluminium sulfate) - a repair cannot reach them, since no dossier adjudicates them. The 270-of-3,767 bulk comparison against Körner et al.'s curated structures and the 1,546 literature rows stay out, with scale as the stated reason. The frame goes from 5,719 to **5,714 chemicals**, still 33.8% readily biodegradable (4,389 from the original part, 1,325 from the literature one), on 4,329 scaffold groups. `dataset check`: 0 errors, 0 warnings (1 accepted, issue 5). Probes re-run: no leak flag and 0.0% of the 17,142 test evaluations with an exact feature copy in training; task probe untuned LightGBM 0.890, random forest 0.889, linear 0.791, dummy 0.500, spread +0.198, no flags; group probe IID 0.893 against grouped 0.887, gap 0.007. Every count, share and model figure the definition states was re-measured on this frame, which moved the analogue shares, the bare-benzene price, the registration-order scores and the sibling overlap (1,001 of `qsar_biodeg`'s 1,055 chemicals, 94.9%, 97.1% of them agreeing).

4. **Fold in the 102 chemicals `qsar_biodeg` has and this set lacks?**

   - **Problem:**
     - The decision item of 2026-11-25 assigned this choice to this record.
     - Merging the two compilations gives 6,207 chemicals once 31 conflicting chemicals are dropped, and an untuned LightGBM then scores 0.893 against 0.890 without them, no measurable gain.
     - The two compilations end at different original sources, so joining them would make one record out of two provenances[^f3].
   - **Effect on the task:** 1.6% more chemicals, and `qsar_biodeg` would retire as a feedstock of this set rather than as a set it replaces.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Do not fold them in (implemented) | This record stays Huang and Zhang's compilation as published | one provenance per record; no measurable gain to buy with it; the sibling retires as replaced, not absorbed | the 102 chemicals of the sibling are not in the benchmark once it retires |
     | B | Fold them in | 102 chemicals are added from the sibling's release, conflicting chemicals dropped | the benchmark keeps every chemical the two sources hold | two compilations in one record, 3.2% of the shared chemicals disagreeing; the paper's own set is no longer what ships |
     | C | Send it back to the pair item on the sibling's record | Nothing here changes; the choice is decided with the retirement | the pair is decided in one place | leaves this record's own definition open until then |

   - **Recommendation:** A. The fold-in buys 0.003 ROC AUC, which is inside the fold-to-fold spread, and costs the record its single provenance. **Decision:** do not fold in (A), fold in (B), or decide it with the pair (C)?

   [^f3]: **PROV-4** (Must): two records are duplicates only when they end at the same original source. **TP-6** (Must): a valid task stays until the better version is actually there.

   **Andrej (2026-11-25, ok):** As implemented (A).

   **Resolved (2026-11-25, Andrej):** A: the 102 chemicals stay out and this record ships Huang and Zhang's compilation as published, so `qsar_biodeg` retires as a set this one replaces rather than as a feedstock of it. Nothing changes in `dataset.py`; the comments carry the two facts the pair needs, and the retirement itself stays on the sibling's record, where the decision of 2026-11-12 put it.

5. **Accept the licence warning with this text?**

   - **Problem:**
     - `dataset check` raises one warning, `meta_license_unknown`: the article names no licence for the supporting information that holds the data.
     - The repository the file is downloaded from is GPL-3.0 for its code, which does not govern the data it redistributes, so no licence can be declared for the publication source.
     - `accepted_check_warnings` is empty, which is the curator's line to write.
   - **Background:** the same warning on `qsar_biodeg` was accepted on 2026-11-02 ("note it but it is not blocking"), with the rider that the licence is regularised before the data ships outside the group.
   - **Effect on the task:** none on the data; it is what the folder records about redistributing the file.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Leave it unaccepted (implemented) | The warning stays open on every check | nothing is asserted about a licence nobody granted | the folder carries an open warning with no decision behind it |
     | B | Accept with the sibling's text and its rider | `accepted_check_warnings` records that the article states no licence for its supporting information, that the GPL-3.0 of the copy governs code and not data, and that the licence is regularised before the data ships outside the group | the same call as the sibling, with the same rider | the rider has to be honoured when the collection is published |
     | C | Accept without the rider | As B, without the sentence about shipping outside the group | shorter | drops the condition the sibling's acceptance carried |

   - **Recommendation:** B, the sibling's call for the same kind of file. **Decision:** accept with the rider (B), accept without it (C), or leave the warning open (A)?

   **Notes for the AI:** B is this entry in the definition, plus a `CC` line in the record: `accepted_check_warnings = {"meta_license_unknown": "The article states no licence for the supporting information that holds the data, and the repository the file is copied from is GPL-3.0 for its code, which does not govern the data it redistributes, so no licence can be declared. Accepted as on qsar_biodeg (2026-11-02): noted, not blocking, and to be regularised before the data ships outside the group."}`. C is the same without the last clause.

   **Andrej (2026-11-25, change):** "Option B: Accept with the sibling's text and its rider."

   **Resolved (2026-11-25, Andrej):** B: `accepted_check_warnings` now carries `meta_license_unknown` with the sibling's text - the article states no licence for the supporting information that holds the data, and the GPL-3.0 of the repository the file is copied from governs its code and not the data it redistributes - and with the rider that the licence is regularised before the data ships outside the group, dated to this decision. The record carries the same as a `CC` line. `dataset check` now reads 0 errors, 0 warnings, with the one warning ignored as accepted.

**Review panel:** ship after changes (mediator). Claims: 46 checked, 41 hold, several to the digit, 4 refuted in wording or arithmetic (all corrected) and 1 leak residue, now closed by the copy-key fix. Blind review, without our notes or rules: a good prediction problem, but it asks for precomputed descriptors in place of the SMILES, which the house rule on molecule sets settles against. Task gamer, with the kit alone: no exploit above +0.0016 ROC AUC against a ±0.0003 noise band, "the task cannot be meaningfully gamed". Agreed: the prediction point, the one feature, the metric, the leaf and the split. Disputed: the fit word (issue 1), the copy key's last step (issue 2) and whether the damaged structures are repaired or dropped (issue 3).

<details><summary>Mediator</summary>

**Mediator — `ready_biodegradability_huang_zhang`**

**Judgment record**

```text
Verdict: ship after changes.
Validity: SEL-1/SEL-2 hold; USE-1 holds (the one input is a structure, known before any test);
  USE-5 holds (the day-28 reading is the source's own assay, read without the window clause, not
  another quantity — chicago_traffic_crashes bar, Lennart 2026-11-05); USE-8 triggered: the gap is
  not in `fit_reason` — write it; the word direct/approximate is the curator's (issue 1).
  LEAK-10 holds; LEAK-29 holds (nothing fitted over all rows); LEAK-19/LEAK-20 triggered and
  departed from without a stated reason — fixed in the copy key (house key of molecules.md).
  SPLIT-1, SPLIT-24, SPLIT-31 (as amended 2026-10-26), SPLIT-36, SPLIT-37 hold; the split stays,
  its description is corrected. PROV-1/PROV-4 hold; PROV-13 triggered: ~29-35 rows carry another
  substance's structure and the origin's own data is in the release — repair or drop (issue 3).
Value: TP-2, a large real signal (LightGBM 0.885, dummy 0.500, forest-linear +0.196, 628-710
  positives a test fold); MET-2, MET-5, MET-6, MET-8 hold, roc_auc confirmed verbatim against the
  paper.
Quality: CLEAN-24 (amended, Lennart 2026-11-01) held against the blind reviewer's "pre-encode or
  exclude": no change. CLEAN notes added for 145 multi-component rows and 7 carbon-free rows.
Weighed: size +, source +, use case +, gap 0, risk - (pooled protocols, label damage in ~0.5%).
For the curator: 5 issues, of which 1 and 2 are weighing calls and 3 is a Must whose remedy is a
  choice between repair and drop.
```

No Must is unfixable and nothing here argues for exclusion; neither brief asked for it.

**Changes to make now (no decision needed)**

| # | Change | Rule |
|---|---|---|
| 1 | **Copy key: apply the house key in full.** After `FragmentRemover` + stereo removal, key also on the InChIKey connectivity block of the desalted structure, in `desalted(..., stereo=False)` **only** — the shipped `SMILES` and the scaffold key untouched. Measured by me on the shipped frame: 112 clusters / 229 rows are still one chemical, 17 clusters (37 rows) carry both classes, 77 clusters span more than one scaffold group; applying the definition's own rule (drop both-class whole, keep one of the rest) gives **5,711 rows (−2.3%)**. The charge step alone (`Uncharger`) gives 88 clusters / 176 rows / 12 both-class → 5,745 rows. Headline ≈ 0.8858 → 0.883. | LEAK-19, LEAK-20 (Should) + `molecules.md` "the key is the structure … **add the InChIKey for tautomers**"; precedent `qsar_oral_toxicity` (Lennart, 2026-11-01). No fact sets this case apart, so the rule decides; the ladder's step 2 (fix the definition) |
| 2 | Name the known false merges in the notes: isopropylmagnesium chloride collapses onto propane (a conflicting cluster, dropped whole either way) and one aluminium acetoacetate chelate onto its ligand. Claim-auditor's "do not change the key" warning does **not** reach this fix: it was aimed at a largest-fragment key, and I verified that under this key the nine acetate salts, the sodium/zinc dithiocarbamates and the triethylammonium pesticides all stay distinct. | LEAK-19, `molecules.md` ("the largest fragment is no salt stripper") |
| 3 | Name the 10-day window in `fit_reason` and reword `task_summary.question` to what `predicted` already says (≥60% by day 28, ≥70% for DOC), instead of "readily biodegradable". | USE-8 (Must, the writing duty); the practitioner, the critic and the advocate all ask for it |
| 4 | Disclose what the grouping does: the three-way close-analogue breakdown (ringless **36.1%**, benzene-only 15.6%, scaffold-grouped **6.6%**, against 22.4% random overall), the ringless-vs-random comparison (36.1% vs 35.2%), the measured consequence (LightGBM 0.844 on ringless test rows with a ≥0.7 analogue, 0.842 without), and the task-gamer's price of the published rule (benzene rows 0.8962 as shipped, 0.8356 if the class were held out whole, 0.0077 on the task). Soften `task_summary.split`. **No re-split.** | SPLIT-31 as amended (2026-10-26) prescribes the singleton treatment; SPLIT-4 (Must): "the split follows what the task does in reality, not the size of the gap" |
| 5 | `time_basis`: drop the absolute "cannot be measured here". The CAS block gives a coarse first-registration order on 75.9% of rows, the RB share falls 45.0% → 18.5% along it (Spearman −0.172), and holding out the newest 30% scores 0.871 against 0.875 random and 0.873 scaffold-grouped on the same rows — so no temporal option is given up (SPLIT-37 step 4 bars the CAS order anyway, and 1,409 rows carry none). | EV-2 (a measurement outranks the page), SPLIT-37 |
| 6 | Correct four shipped statements: EU Method C.4 is **4.4%** (268/6,130; C.4-C at 0.7% was dropped, the list sums to 99.3%), not 3.7%; on the key the sentence names it is **136 compounds / 137 rows, 10 opposite**, not 100/7; the accepted manuscript *is* free (`par.nsf.gov/servlets/purl/10350359`) — put the link in `download_description` and drop "no archive copy" (the SI data files remain ACS-only, so the Körner route and `license=None` stand); Körner's curated sets are **not** cuts of this data — `processing_functions.py:1102-1112` concatenates Lunghini et al.'s set onto his own ECHA compilation (fix in the record and in issue 3's option B). | EV-2, writing; PROV-6 rests on the fourth |
| 7 | Add the protocol table to `curation_comments` and to the `qsar_biodeg` retirement note: pass rate by guideline (301 C 27.2%, 301 D 37.6%, 301 F 38.8%, 301 B 40.5%, 301 A 46.6%, 310 52.7%), **705 chemicals tested under more than one guideline, 27.2% of them getting opposite calls**, with the source's own sentence that its classification task drops the conditions on purpose. | USE-4, TP-6; the retirement of `qsar_biodeg` is being decided against this set |
| 8 | One sentence each for: 145 multi-component rows (2.48%, up to 368 heavy atoms, RB 0.407 vs 0.343) whose encoding sums over components; 7 carbon-free rows (0.12%); the three release files with no reason given (`chemical_speciation.xlsx`, `substance_file.xlsx`, `RegisteredSubstances_organic6.pkl` — none adds rows), and that the primary release could not be listed at all. | CLEAN (P7, note); USE-7 is **not** reached — the practitioner's finding is that registrants do commission this test for UVCBs and reaction masses, so no filter |
| 9 | Correct the hand-off's issue 1 ("the only option under which no test chemical has its own structure in training" — false for 22–37 rows) and issue 3 ("with no third source" — false; the reason is **scale**, 270 structures against the 3 and 1 of the repaired siblings). | EV-2; `principles.md`, "Arguing a call" |

**Issues for the curator, ranked**

**1. The fit word: `direct` or `approximate` (P3, USE-8 Must — a weighing the rules leave open)**

**Problem.** The shipped label is the day-28 reading; the OECD 301 series requires the pass level inside a 10-day window before a registrant or regulator calls a chemical readily biodegradable. `fit="direct"`, and `fit_reason` does not name the gap (change 3 fixes the writing whichever way this goes).

**Effect.** None on the container: options (a) and (b) ship identical data. It sets how the benchmark describes itself.

**For `approximate`:** the gap is measured, systematic and uneven — 505 of 8,115 REACH records read "readily biodegradable, but failing 10-day window"; on the quarter of the set the export reaches, the registrants' own conclusion flips **89 of 783 positives (11.4%)** (claim-auditor independently 92 of 786); by guideline the flip rate is 1.4% for 301 C (the MITI exemption) and 13.1–22.6% for the rest, and the guideline is not a shipped column. USE-8's clause is "a stand-in with a known gap, named as such"; `account_debt_south_africa` and `coffee_rating_prediction` are approximate for gaps that are perfectly well understood, so measuring a gap should not convert it into a direct fit. `diabetes_3` (Lennart, 2026-10-21) and `differentiated_thyroid_cancer_recurrence` are approximate for smaller or unmeasured label gaps.

**For `direct`:** the label definition is settled to the digit and reproduced from the authors' own workbook at **97.6%** (4,482/4,591), so none of USE-8's listed approximate cases (unsettled or unverifiable definition) applies; USE-9 (Should, narrows USE-8) asks whether the data mirrors another well-defined use case practitioners have — the source's own deployed classification predictor serves exactly this label, deliberately "without specifying the experimental conditions and reaction time", so the use case is the source's, not one rephrased to excuse a gap. The one agent playing the actor measured the screening population and found held-out test chemicals *less* like the training side than the next real registered chemical (19.9% close analogue for 846 untested REACH chemicals against 18.9% for the test folds — the opposite direction from `qsar_oral_toxicity`, which is why that one reads approximate) and wrote: "I would not move the fit to approximate for it."

**What would settle it.** Nothing measurable is missing; this is the weighing USE-8 leaves to judgement. **Decision:** (a) `approximate`, gap in `fit_reason`; (b) `direct`, gap in `fit_reason` as a kept, bounded gap; (c) drop the 89 contradicted chemicals (not recommended by anyone — it selects on the audited quarter only). Whichever is chosen, write the fact that sets this set apart from its sibling: **`qsar_biodeg` is 301 C alone, where the window does not apply, so the sibling's label *is* the regulatory conclusion and this one's is not.**

**2. The copy key's last step: one row per CAS-RN? (P4, LEAK-19/LEAK-20 Should — a weighing)**

**Problem.** After change 1 the house key is met. The decision item of 2026-11-25 assigned a further open choice to this record: the **22 repeated CAS numbers** (15 still repeating after the shipped key, 3 with both classes). `aquatic_toxicity_lunghini_consensus`, built in this batch, keys on an InChIKey skeleton *or* a CAS-RN.

**Effect.** ~15 further rows; nothing measurable on the score.

**Each side.** For: it is the second key the decision item named, and a CAS number names the substance an actor acts on. Against: a CAS names a substance, not a structure (it merges rows a 2D encoding genuinely cannot share), and 1,409 of the shipped rows carry no CAS at all, so the key is applied to three quarters of the set only. **Decision:** add the CAS step, or stop at the structure/InChIKey key and record the 15 remnants in the notes.

**3. ~30 rows carry another substance's structure: repair or drop (P5, PROV-13 **Must**)**

**Problem.** The damage is in the only input column — the model is asked to predict one substance's test result from another substance's structure. The hand-off rejected repair for having "no third source"; that is false, and the source is inside the release the definition already downloads: `datasets/iuclid_echa.csv` carries ECHA's own `molecular_formula`, `molecular_weight` and `smiles_echa` for 2,858 CAS numbers.

**Effect, measured twice.** Column-auditor: of 1,791 CAS-matchable shipped rows, 35 (1.95%) carry a different molecular formula. **My own run** (desalted parent, hydrogens ignored, counter-ion conventions normalised): 1,852 rows reached, 1,819 (98.2%) the same parent, **29 (1.57% of the matched rows, 0.50% of the set) a different substance**, every one on a CAS for which ECHA reports a single formula. The two measurements agree and overlap on the examples: CAS 163802-53-7 (a silyl sorbate shipped as phenothiazine), 18162-75-9 (a silylmethyl morpholine shipped as morpholine), 4927-36-0, 6156-18-9, 6259-53-6, 1173693-36-1. The practitioner found the visible tip with no outside source at all — limonene shipped as `[Ca+2].[O-2]`, an azo dye shipped as sodium sulfate.

**Rule.** PROV-13 (Must): check whether the origin has the clean data **before** keeping the damage, and repair when it has. The ladder puts repair above a note, so "keep with a note" is not available here. Precedents: `qsar_bioconcentration` (2026-10-07) and `qsar_oral_toxicity` (2026-10-21) repaired structures from PubChem/Wikidata; `nci_aids_antiviral_screen` (Lennart, 2026-11-02) kept where the damage was not demonstrable — here it is demonstrable for these rows.

**Decision:** (a) repair from `smiles_echa` where ECHA's formula **and** weight agree with each other and against the shipped structure; (b) drop those rows (~0.5%); (c) (a) for the unambiguous ones and (b) for the rest. Add in either case the internal name-vs-element check the practitioner names (an element in the chemical's name absent from its structure), which needs no outside source. **Out of scope either way:** the 270-of-3,767 bulk adjudication against Körner's `Curated_SCS`, and the 1,409 literature rows that carry no CAS — the reason to stop there is **scale**, which must replace "no third source" in the record (change 9).

**4. Fold in the 102 chemicals `qsar_biodeg` has and this set lacks? (P5/P6, PROV-4 Must, TP-6 Must — assigned here, missing)**

The decision item of 2026-11-25 assigned this to this record's review and no draft issue carries it. The measurement already exists: merged 6,207 chemicals, 31 conflicting chemicals dropped, LightGBM **0.893 against 0.890** — no measurable gain. PROV-4 keeps the two compilations distinct. **Recommendation: do not fold in**, so `qsar_biodeg` retires as replaced rather than as a feedstock. **Decision:** raise and settle here, or send it back to the pair item on `qsar_biodeg`'s record.

**5. The pair with `qsar_biodeg` (procedure)**

The pair is live as issue 5 of `qsar_biodeg`'s own review, which is where the decision of 2026-11-12 put it — nothing here retires it. Two facts belong in that retirement note before it is decided: this set holds 967–969 of `qsar_biodeg`'s 1,055 chemicals (91.7%) with 97.1% class agreement, **and** the replacement's label is *pooled* across seven protocols while `qsar_biodeg` is 301 C alone (27.2% pass against 34.3% here, 27.2% of multi-guideline chemicals getting opposite calls). Also unresolved and yours by convention: the `meta_license_unknown` acceptance text (`accepted_check_warnings` left empty for you; `qsar_biodeg` CC 2026-11-02, "note it but it is not blocking", with the "regularise before it ships outside the group" rider).

**The task gamer's exploits, mapped**

The definition carries **no `Potential leak, kept on purpose:` note and no accepted check warnings** (the one `dataset check` warning, `meta_license_unknown`, is left for the curator), so every exploit is measured against an empty set of notes.

| Gamer finding | Rule | Known or new | Verdict |
|---|---|---|---|
| **1.** Neighbour/density counts computed over train **and** test (+0.0016 against a ±0.0003 band) | LEAK-29/LEAK-30 territory, but the curation fits nothing over all rows — this is the modeller transducing | New, not noted | No issue. Nothing in the data to fix; one clause if the curator wants transduction declared out of scope |
| **2 / F2.** Twin labels — the same chemical in train as a salt, charged form or tautomer (5.3–6.1% of test rows; +0.0003 alone, **0.0064** when twins are co-grouped) | LEAK-19, LEAK-20 (Should) | **Known mechanism, measured gain differs from the note.** ¶6 documents the dedup and claims the rule "settles them with the rest"; three agents and I measure 88–116 clusters surviving, 2.2–2.4% of test evaluations with their own chemical in training, those rows scoring 0.929 against 0.884 (0.902 once the twin is removed from training) | **Issue → fixed by change 1.** Note why the leak probe read 0.0%: it compares the shipped SMILES, which are distinct by construction |
| **F1.** Bare benzene (17.1%) split into singletons; held out whole it costs 0.0077 on the task | SPLIT-31 as amended (2026-10-26) | **Known and prescribed** — the gamer was sandboxed without the rules and read it as a size cap | No change; the price is disclosed (change 4) |
| **F3.** Ringless third (36.4%) split at random, 36.1% keep a close analogue | SPLIT-31 as amended | **Known and prescribed**; consequence measured at ~0 (0.844 vs 0.842) | Disclosure only (change 4) |
| **F4.** 46 groups / 122 rows with contradictory labels; dropping them from training gains nothing | LEAK-20 | Known in kind; the residue is the same copy-key gap | Removed by change 1 (17 both-class clusters go whole) |
| **3.** 1-NN Tanimoto label (−0.0001) | — | — | A legitimate model; nothing |
| Formats, row order, ids, post-hoc columns, pseudo-labelling, source as a proxy, weights, rank transforms | LEAK-10, LEAK-39, CLEAN-23 | — | **All empty.** "The task cannot be meaningfully gamed" |
| The labels are readable off the public GitHub copy | — | Known, true of every public dataset we ship | Out of scope, as the gamer itself noted |

**Agreed facts**

Both briefs accept these; all were measured on 2026-11-25, most of them by two or three agents independently.

* **Source and counts.** `class_all.csv` carries Huang & Zhang's `ClassDataset_all`: 6,139 chemicals = 4,593 `ClassDataset_original` + 1,546 `ClassDataset_external`, 34.92% positive; the per-part label counts (537 ones / 1,009 zeros in the external part) are the paper's own. The accepted manuscript is free at `par.nsf.gov`, and **every quotation the definition makes from the paper checks out verbatim**, including the six-metric sentence and the source's similarity-maximising split.
* **The label** is the ready endpoint at day 28, ≥60% (≥70% for DOC), rebuilt from the authors' workbook at 4,482/4,591 = 97.6% (98.2% on a majority rule); Körner's code implements the same rule. The paper never mentions the 10-day window. 209 of 4,966 chemicals (4.2%) have repeat tests on both sides of the threshold; the source resolved them and the class ships as published.
* **The 10-day gap**: 505 of 8,115 REACH records are "readily biodegradable, but failing 10-day window"; on the 1,642–1,673 shipped chemicals the export reaches, 89 of 783 (11.4%) / 92 of 786 (11.7%) positives flip — 1.5% of all rows; ~0 for 301 C, 13–23% elsewhere.
* **The feature.** One shipped feature, `SMILES`, RDKit-canonical, all 6,139 parse; `scaffold` is the group column, no feature. `pka_*`, `α_*` (Körner's MolGpKa outputs), `name`, `name_type`, `cas`, `source`, `Unnamed: 0` all correctly dropped; no missing value anywhere; row order shuffled. **There is no column that could be unknown at the prediction point** — the blind reviewer, without our notes, reached the same conclusion.
* **The copies as implemented.** 729 structures hold more than one fragment, 585 lose something to the remover; 236 compounds in 498 rows, 32 with both classes dropped whole (74 rows), 220 further rows dropped; 6,139 → 5,845, 34.3% `Yes`. After that key, 88–116 clusters are still one chemical (my run: 88 with charges neutralised, 112 on the InChIKey block), 12–17 of them carrying both classes.
* **The split.** 4,426 groups, 4,096 of size one (2,126 ringless 36.4%, 999 benzene-only 17.1%), 330 series of 2–105, largest group 1.8% of rows; no group spans train and test in any of the 9 folds; 1,763–2,117 test rows with 628–710 positives each; a constant prediction scores exactly 0.5000 on all nine. Close training analogue 18.9% grouped against 22.4% random. Nothing in any of the three files dates a row. The source's own cross-part split would be **easier** (0.910 against 0.897), so there is no case for grouping on `source`.
* **Value.** LightGBM 0.885 (0.878–0.896 across folds), linear 0.789, dummy 0.500, forest−linear +0.196, IID-vs-grouped gap 0.010. A better honest model reaches 0.8895; no exploit exceeds +0.0016 against a ±0.0003 noise band.
* **Damage.** ~29–35 of the ~1,800 CAS-matchable rows carry a structure that is not the registered substance; 7 rows contain no carbon, 3 of them visibly the wrong substance from the shipped file alone; 145 rows (2.48%) are multi-component substances.
* **The pair.** 967–969 of `qsar_biodeg`'s 1,055 chemicals (91.7%) are here as one compound, 939–941 (97.1%) with the same class; the two compilations end at different original sources (PROV-4), so neither is a copy of the other.

**Consistency with precedent**

I follow the precedent-checker's report. Its decisions 1 (the scaffold leaf, `UnseenGroup`, the ringless/benzene treatment), 2 (`roc_auc` by MET-5/6/8), 3 (CLEAN-24 drops), 4 (3×3), 8 (the pair handled on `qsar_biodeg`'s record) and 10 (the licence warning) are **consistent**, and I add two of my own:

* **Against the blind reviewer's headline change** (replace `SMILES` with precomputed descriptors, or exclude): **not taken.** CLEAN-24 as amended (Lennart, 2026-11-01) settles it, thirteen shipped molecule folders follow it — including `qsar_biodeg` itself, whose Dragon descriptors left under the same amendment — and the blind reviewer's own 0.878-vs-0.878 sits inside the −0.025/+0.010 band the amendment cites. Rules win over an outside view, and P7 is the lowest rank in the book; taking it would be an unannounced amendment touching all thirteen folders. The reviewer is unaware of the house rules by design, so this is not new evidence.
* **Against a different split** (the gamer's decorated-scaffold benzene grouping, the reviewer's Butina clustering): **not taken.** SPLIT-31 as amended prescribes the singleton treatment, `qsar_bioconcentration` (34% ringless) and `qsar_oral_toxicity` (23% + 18%) match, and SPLIT-4 (Must) says the size of the gap never decides. Both briefs agree.

Three departures and one gap, all handled above: decision 6 (the copy key) **departed without a stated reason** and no fact sets this case apart, so the rule decides — change 1; decision 7 (the fit) departs and goes to the curator as issue 1; decision 5 (shipping as published rather than repairing the 270) **departs with a stated reason that is factually wrong** — the reason becomes scale, and the demonstrable subset is repaired or dropped (issue 3); decision 9's two assigned open choices are now raised (issues 2 and 4). No drift: Andrej's molecule calls of 2026-11-11 → 11-12 → 11-13 on `qsar_biodeg` end at what this folder implements. No reason has produced a third exception, so no amendment is due.

</details>

<details><summary>Claim audit</summary>

**Claim audit — `ready_biodegradability_huang_zhang`**

Everything below was measured on 2026-11-25 on the shipped definition (`make_splits()` → 5,845 rows, 9 splits), the raw `class_all.csv`, Huang & Zhang's `RegressionDataset.xlsx`, Körner et al.'s ECHA export, and the paper's accepted manuscript. The measurements were run outside the repository, which I did not edit.

**Headline: the definition survives the attack.** 41 of 46 checkable claims hold, several of them to the digit. Four are wrong in wording or arithmetic (all low severity, all documentation), and one leak attack found a real but negligible residue. The split claim that I expected to break — the acyclic third gets no grouping — is true as a description but **refuted as a problem**: the measurement says it does not inflate the score.

**Claims table**

| # | Claim | Source | Test (EV-1) | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | 6,139 rows = 4,593 `ClassDataset_original` + 1,546 `ClassDataset_external`; "around 65% negative / 35% positive" | `curation_comments` ¶2, quoting the paper | count the raw file; read the paper's §Dataset Preparation | **holds** | 4,593 / 1,546; 34.92% positive; per part 1,607/2,986 and **537/1,009** — the paper states "537 1s and 1009 0s" for the external set verbatim | PROV-1 |
| 2 | The copy carries Huang & Zhang's `ClassDataset_all` | `Source(role="copy")`, `download_description` | fingerprint the copy against the paper's own counts | **holds (indirect; SI not downloadable)** | counts and per-part label counts match the article exactly, incl. 537/1,009 | PROV-4 |
| 3 | "The ACS article and its supporting information refuse an automated download (403, no archive copy)" | record, Screening 2026-11-25; `download_description` | look once more (MET-1) | **REFUTED for the article** | the accepted manuscript is free at `par.nsf.gov/servlets/purl/10350359`; I fetched and read it. The SI data files are still ACS-only | MET-1, PROV-13 |
| 4 | Label = ready endpoint, day 28, ≥60% (70% for DOC); reproduces 4,482 of 4,591 (97.6%), majority/mean 98.2% | `curation_comments` ¶3 | rebuild the rule from the workbook, merge on CAS | **holds exactly** | any-pass 4,482/4,591 = 97.63%; majority 4,508 = 98.19%; the record's 4,495 (97.9%) is the ≥0.5-majority variant — both numbers are real, two rules | USE-5 |
| 5 | Guideline mix of the 28-day ready records: 301 F 24.6, 301 B 23.4, 301 C 22.5, 301 D 17.2, 310 2.7, 301 A 2.6, 301 E 2.6, **EU C.4 3.7%** | `curation_comments` ¶3; record | count on 6,130 records | **REFUTED (last figure)** | all OECD figures exact; EU Method C.4 = 268/6,130 = **4.4%** (E 1.4, D 1.2, A 1.1, **C 0.7 omitted**); the list sums to 99.3% | writing |
| 6 | DOC methods read 70% because they read higher; the paper treats the series as one protocol | `curation_comments` ¶3 | read the paper | **holds, verbatim** | p. 7: "the DOC-based standard methods usually set a threshold of 70% (not 60% for other principles)" | USE-5 |
| 7 | All 6,139 SMILES parse; shipped in RDKit canonical form | `curation_comments` ¶4 | parse with the pinned RDKit 2026.03.6 | **holds** | 0 failures; 6,137 distinct canonical SMILES (2 exact copies) | CLEAN-24 |
| 8 | `pka_*`/`α_*` are Körner's MolGpKa computations and leave (CLEAN-24) | `curation_comments` ¶5 | read Körner's README/`add_pka_values.py` | **holds** | README §`add_pka_values.py`, MolGpKa venv — model outputs of the structure, not measurements | CLEAN-24 |
| 9 | 729 structures have >1 fragment, 585 lose something to `FragmentRemover` | `curation_comments` ¶6 | recompute | **holds exactly** | 729 / 585 | LEAK-19 |
| 10 | 236 compounds in >1 row (498 rows); 32 with both classes dropped whole (74 rows); 204 agree, 220 rows dropped; 5,845 remain; 34.3% vs 34.9% | `curation_comments` ¶6, `_decisions` | recompute the key and the arithmetic | **holds exactly** | 236/498, 32/74, 204/220, 6,139−294 = 5,845, 0.3432 vs 0.3492 | LEAK-19, LEAK-20 |
| 11 | "15 would be one row to a 2D encoding even with their salts, the other 17 are a salt and its free form" | `curation_comments` ¶6 | count stereo-free duplicate groups with conflicting classes | **holds** | 145 stereo-free duplicate groups, **15** conflicting; 32−15 = 17 | LEAK-20 |
| 12 | 4,436 rows from the original part, 1,409 from the literature part | `task_summary.row`, `curation_comments` ¶6 | trace the kept raw rows | **holds exactly** | 4,436 / 1,409 | — |
| 13 | "The two parts share no exact structure" | `curation_comments` ¶6 | intersect canonical SMILES by part | **holds** | 0 shared | PROV-4 |
| 14 | "100 of the literature chemicals are a chemical of the first part **once stereochemistry and salts are set aside**, 7 with the opposite class" | `curation_comments` ¶6 | recompute on the key the sentence names | **REFUTED (the key named)** | salts+stereo removed: **137 rows / 136 compounds, 10 opposite**. The 100/7 come from stereo-only (salts kept) — the builder's `flat` key in `03_chars.py`, not the key `_clean` uses | writing / LEAK-19 |
| 15 | 209 of 4,966 chemicals (4.2%) have repeat 28-day tests on both sides | `curation_comments` ¶7; record | recompute from the workbook | **holds exactly** | 209 / 4,966 = 4.21% | TP-6 |
| 16 | 10-day window: 505 of 8,115 export records; export reaches 1,642 shipped chemicals; 91.5% agreement; 89 of 783 positives flip (1.5% of all) | `curation_comments` ¶8 | rebuild independently from `iuclid_echa.csv` | **holds (direction and magnitude)** | 505/8,115 exact. My rule ("any record concluding readily biodegradable"): 1,673 reached (28.6%), 88.6% agreement, **92 of 786 flip (11.7%, 1.57% of all)**. The builder's rule (ready-endpoint records only, CAS through the dedup key) gives their numbers; both say the same thing | USE-5, TP-6 |
| 17 | The paper never mentions the 10-day window | implicit in ¶8 ("the label … ignores the 10-day window") | full-text search | **holds** | no occurrence of "10-day"/"ten-day"/"window" in the main text; the label is the source's own | USE-5 |
| 18 | 4,426 groups, 4,096 alone, 330 series of 2–105; largest series cyclohexane 1.8%; no other scaffold reaches a tenth | `curation_comments` ¶9, `grouping`, README | recompute groups and sizes | **holds exactly** | 4,426 / 4,096 / 330 (min 2, max 105); `C1CCCCC1` 105 rows = 1.80%; only `""` and `c1ccccc1` exceed 10% | SPLIT-31 |
| 19 | 2,126 ringless (36.4%) and 999 benzene-only (17.1%) are held out one by one | `grouping.definition`, `task_summary.split` | recompute | **holds** | 2,126 (36.37%) and 999 (17.09%); note the two do **not** add to the 4,096 singletons — the other 971 are chemicals with a unique real scaffold (the sentence reads as a partition) | SPLIT-31 |
| 20 | Under the groups 18.9% of test chemicals have a training chemical at Tanimoto ≥0.7 (median 0.515) against 22.4% (0.552) at random | `curation_comments` ¶9, `splits_comment` | recompute, Morgan r2/2048 on the de-salted structure, 3 folds | **holds** | 18.91% / median 0.521; random 22.56% / 0.553 | SPLIT-36 |
| 21 | "a test chemical belongs to a family the model has not seen" | `task_summary.split` | break the 18.9% down by subgroup, then fit | **true for 46.5% of rows, not for the acyclic 36.4% — but no measured effect** | ≥0.7 analogue share: ringless **36.1%**, benzene-only 15.6%, real scaffold **6.6%**. LightGBM AUC on ringless rows **with** a close analogue 0.844 vs **without** 0.842; ringless 0.853 vs real-scaffold 0.851 overall | SPLIT-31, SPLIT-36 |
| 22 | No group spans train and test; each row tested once per repeat | `splits_comment`, split regime | check all 9 splits | **holds** | 0 group overlaps; 5,845 distinct test rows per repeat; 1,439–1,501 test groups a fold | SPLIT-1 |
| 23 | "no test chemical has its own structure in training" | the builder's hand-over, issue 1, implied by ¶6 | stricter chemical key: largest fragment (≥70% of heavy atoms in every member), stereo removed | **REFUTED, negligible** | 13 keys / 26 rows; **34 of 17,535 test evaluations (0.19%)** have the same parent molecule in training, 24 with the same label. Examples below | LEAK-19 |
| 24 | File order is chemistry, not a clock: neighbours share a ring skeleton 9.6% vs 2.8%, a class 66.4% vs 54.6%, rank corr −0.04 | `curation_comments` ¶10 | reproduce | **holds** | class 66.44% vs 54.99%; rank corr −0.036 / −0.019. The 9.6%/2.8% is on the non-empty Murcko scaffold of the **published** structure (builder's `16_blocks.py`); on the de-salted scaffold it is 35.0%/16.3% and on the `scaffold_groups` key 3.9%/0.03% — the number is key-dependent but the claim (order is chemistry) holds | LEAK-29 |
| 25 | Nothing dates a row; no temporal option; `UnseenGroup` | `time_basis` | check all three files for a date column | **holds** | `class_all.csv`, the workbook and `iuclid_echa.csv` carry no test or dossier date | SPLIT-37 |
| 26 | qsar_biodeg: 967 of 1,055 (91.7%) here as one compound, 939 (97.1%) same class | `curation_comments` ¶11 | rematch independently | **holds** | 969 (91.8%), 941 (97.1%) — ±2 from tie-handling on duplicated keys | PROV-4 |
| 27 | Metric: the paper evaluates "based on different matrices, including accuracy, sensitivity, specificity, balanced accuracy, ROC AUC, and f_1" and reports 85.6, 90.3, 80.4, 85.4, 91.8, 85.1% without naming the deciding one | `Metric.fallback` reason | read the Methods and Results in the manuscript | **holds, verbatim** | Methods p. 4 is the quoted sentence word for word; Results p. 9: "prediction accuracy, sensitivity, specificity, balanced accuracy, AUC, and f_1 score of 85.6, 90.3, 80.4, 85.4, 91.8, and 85.1%, respectively, on the test set (Table S13)". No criterion is named anywhere; model choice was made on prescreening, and Bayesian optimisation "did not observe improvement" | MET-5, MET-6 |
| 28 | `roc_auc` is the right declaration | `metric = Metric.fallback(...)` | MET-5 → MET-8 | **holds** | six metrics side by side, no threshold, no cost, no k; Körner's balanced accuracy equally unfixed; same call as `qsar_biodeg`, `gallstone_disease`, `ljubljana_breast_cancer` | MET-5, MET-6, MET-8 |
| 29 | The metric is computable on our data (unit, inputs, folds) | MET-2 | score a dummy on each fold through `data_foundry.v2.metrics.scorer` | **holds** | unit = the row = the chemical; `scoring_columns: null`, no weight; every fold has both classes (positives 628–710, negatives 1,103–1,407 of 1,763–2,117); a constant prediction scores exactly 0.5000 on all 9 folds | MET-2 |
| 30 | The metric means the same here as on the source's task | MET-2 | compare target, classes, balance | **holds** | same binary target, same two classes, 34.3% positive against the paper's "around 35%"; ROC AUC is prior-free anyway. (The paper balanced its *training* set — irrelevant to a ranking metric) | MET-2 |
| 31 | "The source split at random … 'to ensure high similarities of chemicals among the training, validation, and test subsets'", so its figures say nothing about this split | `curation_comments` ¶9; record | read the paper | **holds, verbatim** | Methods p. 4: "Chemical similarity calculation based on FPs and the Tanimoto index was then carried out for chemical grouping to ensure high similarities of chemicals among the training, validation, and test subsets" | SPLIT-5 |
| 32 | Only the structure is known at the prediction point; fit direct | `task_summary.known`, `fit` | list the shipped feature columns | **holds** | `feature_cols = ('SMILES',)`; `scaffold` is the group column and no feature; `Unnamed: 0`, `name`, `name_type`, `cas`, `source`, `pka_*`, `α_*` all dropped | USE-1, LEAK-10 |
| 33 | License unknown for the publication source | `Source(license=None)`, the one check warning | read the ASSOCIATED CONTENT block | **holds** | "The Supporting Information is available free of charge at https://pubs.acs.org/doi/…" — datasets listed, no licence named. Leaving `accepted_check_warnings` empty is correct: the reference says the curator fills it | — |
| 34 | 1,308 distinct scaffolds; 2 exact duplicates; 145 stereo pairs (15 conflicting); 22 repeated CAS (6 conflicting); 1,546 rows without CAS | record, Screening | recount | **holds exactly** | 1,308 / 2 / 145 (15) / 22 (6) / 1,546 | — |
| 35 | Probe results (leak none, task spread +0.196, group gap 0.010) | builder report | re-fit LightGBM on 3 folds | **consistent** | my LightGBM 0.886 overall, matching the probe's 0.884 | TP-2 |

**Refuted and untested, ranked**

Nothing here reaches a Must, and nothing touches validity (P1–P5) in a way that changes what the benchmark measures. Ranked by rank then strength then effect.

**1. (P4, LEAK-19, Should, weak) The copy key leaves 13 parent molecules on both sides of the split — 0.19% of test evaluations.**
`FragmentRemover` strips RDKit's inorganic salts and solvents but keeps organic counter-ions, as `curation_comments` ¶6 says; the consequence it does not say is that a compound and its organic salt stay as two rows in two different scaffold groups. Conservative test (largest fragment ≥70% of heavy atoms in every member, stereochemistry removed): 13 keys, 26 rows, 8 of them spanning scaffold groups; across the 9 shipped splits **34 of 17,535 test evaluations (0.19%)** have a training row that is the same parent molecule, 24 with the same label. Concrete pairs: potassium hydrogen phthalate / tetramethylammonium hydrogen phthalate (both Yes); oleoyl sarcosine free acid / its triethanolamine salt (also an E/Z pair); lauramidopropyl betaine as free cation / as methylsulfate; **clavulanic acid Yes / tert-butylamine clavulanate No** — one of those two is wrong, and the pair is an in-set label contradiction the key did not catch.
*What it changes:* nothing measurable — 0.19% of evaluations, and finding #21 shows the model gets no lift from a close training analogue in this set. It does make the hand-over's "the only option under which no test chemical has its own structure in training" an overstatement.
*Mildest remedy:* one sentence in `curation_comments` ¶6 — the key keeps organic counter-ions, 13 parent molecules therefore stay as two rows, 0.19% of test evaluations. **Do not change the key**: collapsing to the largest fragment would wrongly merge 9 different acetate salts and the triethylammonium pesticides into one row each, exactly the trap `canonical_smiles`' own docstring warns about (I measured 84 such keys, 196 rows, against the 13 real ones).

**2. (P4, SPLIT-31/36, Should, wording) The split claim is true for half the set and empty for the acyclic third — but the consequence is nil.**
`task_summary.split` and `splits_comment` lead with "whole chemical series are held out … a family the model has not seen", then add the caveat. The caveat is the larger half of the story: a Bemis-Murcko scaffold is empty for an acyclic molecule, so each of the 2,126 ringless chemicals (36.4%) is its own group and that third is split at random — and it is the *most* self-similar part of the set, because an acyclic homologous series (fatty acids, alcohols, glycol ethers, surfactants) is the archetypal chemical series. Measured per fold: Tanimoto ≥0.7 training analogue for **36.1%** of ringless test rows, 15.6% of benzene-only, **6.6%** of scaffold-grouped rows — against 22.6% under a plain random split of everything. The single 18.9% in the `splits_comment` is an average over three very different regimes.
*Why the attack fails on the consequence:* LightGBM (recommended SMILES encoding, 3 shipped folds) scores **0.844** on ringless test rows that have a ≥0.7 analogue in training and **0.842** on those that do not; ringless overall 0.853 against 0.851 for the scaffold-grouped rows. The twins are there and the model does not cash them. (For the scaffold-grouped rows an analogue *does* help — 0.923 vs 0.843 — but those are 6.6% of rows and already inside the grouping.)
*What it changes:* a reader of `splits_comment` believes the grouping does more than it does for a third of the rows.
*Mildest remedy:* add the 36.1% / 15.6% / 6.6% breakdown and the 0.844-vs-0.842 measurement to `splits_comment` or ¶9. No change to the split, and no case for inventing an acyclic grouping key (it would be a family-wide call across every SMILES dataset and the measurement says there is nothing to buy).

**3. (P5/writing, low) Two numbers in `curation_comments` are wrong as written.**
(a) ¶3 "EU Method C.4 3.7%" — the true share of the 6,130 28-day ready records is **4.4%** (268 records: C.4-E 1.4, C.4-D 1.2, C.4-A 1.1, **C.4-C 0.7 dropped**); the listed percentages sum to 99.3%. Same figure in the record's screening block.
(b) ¶6 "100 … once stereochemistry **and salts** are set aside, 7 with the opposite class" — on that key it is **136 compounds (137 rows), 10 opposite**; 100/7 is the stereo-only key. Both the paper's external validation set and its training set are therefore a third more entangled than the sentence says — which strengthens, not weakens, the case for the dedup as implemented.
*Mildest remedy:* correct both numbers (one is a fact in a shipped README).

**4. (P5, PROV-13 / MET-1, low) "No archive copy" of the article is wrong.**
The accepted manuscript is free at <https://par.nsf.gov/servlets/purl/10350359>. I read it, and every quotation the definition makes from the paper checks out word for word — so this changes no decision; it only means the next reader need not take the metric, the counts, the label threshold and the source's split on trust. The SI *data* files remain ACS-only and unlicensed, so the Körner route and `license=None` stand.
*Mildest remedy:* put the PAR link in the record and in `download_description`.

**5. (minor consistency, no remedy needed)** ¶7 argues against Körner's curated sets because they "drop such chemicals instead, which removes the hard cases rather than the ambiguity (TP-6)", while `_clean` drops 32 compounds (74 rows) for having both classes. The two are different (a compound carrying both labels in one target column cannot be scored at all, LEAK-20, against dropping every chemical whose repeat tests disagree) and the scale differs by two orders — 32 of 5,877 compounds (0.54%) against Körner's 954. Worth a half-sentence only if the curator asks; I would leave it.

**Untested, and why**

* **Is `class_all.csv` byte-identical to the SI's XLSX?** The SI is not machine-downloadable (403) and the manuscript carries no data. Indirect evidence is as strong as it gets short of the file: 4,593 / 1,546 / 6,139, 1,607 vs 2,986 in the original part, and **537 ones / 1,009 zeros in the external part — the paper states exactly those two numbers**.
* **Which of two structure retrievals is right for a given CAS** (Körner's `Curated_SCS` disagrees on 270 of 3,767 shared CAS numbers). Needs a third identifier source; the builder's "could not check" stands, and the handoff's issue 3 is the right place for it.
* **The record's pair evidence for retiring `qsar_biodeg`** (0.938 transfer vs 0.935 in-set). Outside the definition; I re-verified only the overlap it rests on (969/1,055, 941 same class), which holds.
* **Whether structures that are one chemical once stereochemistry is set aside should share a scaffold *group*** (the screening block's open question). I tested the consequence instead rather than the framing: 130 agreeing stereo pairs exist, 39 straddle groups, and the measured lift from a close training analogue is zero (finding 2), so the answer is "it does not matter here".

**Three claims I tried hardest to break and could not**

* The label reconstruction — 4,482/4,591 on the exact rule the comment states, to the row.
* The metric reason — every clause, including the six numbers and the source's own similarity-based split, is verbatim in a paper the record said could not be read.
* Metric computability (MET-2) — a constant prediction scores exactly 0.5000 on all nine folds, both classes are present in every one with 628+ positives, and the metric needs no scoring column.

**Sources:** [NSF PAR copy of Huang & Zhang 2022](https://par.nsf.gov/servlets/purl/10350359), [PubMed record](https://www.pubmed.gov/35973069/), [Körner et al. 2024 (ESPI)](https://pubs.rsc.org/en/content/articlehtml/2024/em/d4em00431k), [Huang's classifier repository](https://www.github.com/KuanHuang/aerobic-biodeg-xgb-classifier).

</details>

<details><summary>Column audit</summary>

**Column audit — `ready_biodegradability_huang_zhang`**

Read: `dataset.py`, the record (screening block of 2026-11-25), the builder's hand-over and probe logs, `principles.md`, `use_case.md`, `leak_checks.md`, `cleaning_features.md`. Frame loaded through `dataset_io.from_definition` (5,845 × 3); the scripts and the evidence were kept outside the repository.

**1. The files of the release**

The primary release (Huang & Zhang's ACS supporting information) cannot be listed — `pubs.acs.org` refuses the fetch and no archive holds it — so the audit is against the copy the definition downloads from, listed through the GitHub tree API. Every data file of that repository:

| File | Read by `_load_raw`? | Reason given in `curation_comments` |
|---|---|---|
| `datasets/external_data/class_all.csv` | **yes** | — |
| `datasets/external_data/class_original.csv`, `class_external.csv` | no | named: "the two parts of this file" ✓ |
| `datasets/external_data/Huang_Zhang_RegressionDataset.xlsx` | no | named: the authors' regression task ✓ |
| `datasets/curated_data/class_curated_{scs,final,biowin}.csv` | no | named: Körner's versions ✓ |
| `datasets/iuclid_echa.csv` | no | named: read for the 10-day window ✓ |
| `datasets/chemical_speciation.xlsx` | no | **not named** |
| `substance_file.xlsx` | no | **not named** |
| `reach_study_results/RegisteredSubstances_organic6.pkl` | no | **not named** |

I checked the three unnamed ones. `chemical_speciation.xlsx` is Körner's hand-checked species-at-pH-7.4 table (`cas, smiles, env_smiles, checked_by, source`), the input of the `α_*` columns the definition drops; `substance_file.xlsx` is 8.7 kB of CAS + SMILES for the example notebook; `RegisteredSubstances_organic6.pkl` is the raw REACH pull behind `iuclid_echa.csv` (`processing_functions.py:1283`). None holds more rows of Huang & Zhang's series, so **no row is missed** — the gap is only in the list. One of them, `iuclid_echa.csv`, turns out to matter for a different reason (finding 1).

**2. The columns**

**Shipped frame** (no missing value anywhere; not a temporal task, so there is no missing-share-by-period to answer and `splits_feature_missing_in_test` cannot fire — `dataset check` raised only `meta_license_unknown`):

| Column | Meaning (from the source) | Known at the prediction point? | Dtype and cleaning | Verdict | Rule |
|---|---|---|---|---|---|
| `SMILES` | The tested chemical's structure, RDKit-canonical, salts and stereochemistry as published | **Yes** — a structure exists before any test is commissioned; no window, no post-outcome field, no outcome-driven missingness | `string`, declared `Smiles(column="SMILES")`, encoded by the benchmark; source-computed descriptors (`pka_*`, `α_*`) correctly removed | fine as a column; the *values* are wrong for ~2% of the checkable rows (finding 1), and a handful are out of the task's scope (finding 2) | CLEAN-24, PROV-13 |
| `Biodegradable` | Readily biodegradable from an OECD 301-series / EU C.4 screening test: ≥60% at day 28, ≥70% for DOC die-away | the outcome | `category`, unordered, `['No','Yes']`, `Yes` = the event (2,006 / 5,845 = 34.3%) | fine | CLEAN-25 |
| `scaffold` | The Bemis-Murcko scaffold of the desalted structure; 4,426 groups, 4,096 of size 1, largest `C1CCCCC1` with 105 rows | derived from `SMILES` | `string`, group column only, not in `feature_cols` | fine | SPLIT-31 |

I verified Körner's label code directly: `reg_df_remove_studies_not_to_consider` keeps `endpoint == "ready"` and `time_day == 28.0`, and `label_data_based_on_percentage` is exactly `DOC Die Away ≥ 0.70, else ≥ 0.60` — the rule `curation_comments` states.

**Raw columns that leave** (all 25 accounted for):

| Column | Meaning | Verdict on the drop |
|---|---|---|
| `Unnamed: 0` | row number — verified exactly `range(6139)` | correct (CLEAN-3); the time probe's `id_drift` on it is this and nothing else |
| `name`, `cas` | chemical name and CAS-RN; **missing for exactly the 1,546 literature rows** | correct (CLEAN-3). Their missingness is a perfect indicator of which part of the compilation a row comes from; dropping them removes it |
| `name_type` | IUPAC Name / EC Name / blank | correct |
| `source` | `ClassDataset_original` / `ClassDataset_external` | correct (CLEAN-22, the `logKOW_type` shape). It costs nothing: the two parts' RB rates after cleaning are 34.2% and 34.7% |
| `pka_acid_1..4`, `pka_base_1..4`, `α_acid_0..4`, `α_base_0..4` | Körner's MolGpKa predictions and speciation fractions, computed from the structure (`add_pka_values.py`) | correct (CLEAN-24, as the Dragon descriptors of `qsar_biodeg`) |

**Findings, ranked**

**1. The dataset's one feature is the wrong molecule for about 2% of the rows that can be checked — and the release carries the file that adjudicates them (P5, PROV-13 Must)**

The record and the hand-off both know of Körner's "mismatched chemical identifiers", and hand-off issue 3 rejects repairing them ("option C would adjudicate 270 structures **with no third source**"). There is a third source, and it is already inside the release the definition downloads from: `datasets/iuclid_echa.csv` carries ECHA's own `smiles_echa`, `molecular_formula` and `molecular_weight` for 2,858 CAS numbers, straight from the dossiers — independent of both Huang & Zhang's and Körner's curated tables.

Matched by CAS, it reaches **1,791 of the 5,845 shipped rows (30.6%)**. Comparing neutral, desalted parents:

- identical parent structure: 1,710 (95.5%)
- same molecular formula: 1,756 (98.0%)
- **different molecular formula: 35 (1.95%)**, RB rate 0.257 against 0.343 overall

Roughly ten of the 35 are only a counter-ion count; the rest are a different substance. Flagrant examples, shipped structure vs ECHA's:

| CAS | Source's own name | Shipped | ECHA |
|---|---|---|---|
| 6156-18-9 | 2,2-Bis(methylthio)propane | `NS(=O)(=O)c1ccc(NC(=S)Nc2ccc(F)cc2)cc1` (C13H12FN3O2S2) | `CSC(C)(C)SC` (C5H12S2) |
| 4927-36-0 | 5-methyl-5-phenylhexan-3-one | C13H11N3O3S2 | C13H18O |
| 163802-53-7 | 3-(trimethoxysilyl)propyl hexa-2,4-dienoate | phenothiazine (C12H9NS) | C12H22O5Si |
| 1173693-36-1 | 1-[5-(2,6-difluorophenyl)-isoxazol-3-yl]ethanone | chlorobenzene (C6H5Cl) | C11H9F2NO2 |
| 1809-14-9 / 3658-48-8 / 4712-55-4 | dialkyl phosphonates | written `O=[P+](OR)OR` — a phosphonium cation, no P–H | `O=P(OR)OR` |
| 617-86-7 / 993-07-7 | triethyl-/trimethylsilane | Si–H lost (C6H15Si) | C6H16Si |

This is not label noise; it is damage in the only input column, and PROV-13 is a Must that asks whether the origin has the clean data before the damage is kept. Nobody has asked it for these rows.

**Honest limits.** `smiles_echa` is Körner's parse of the dossier (his own `entry_echa_evaluation` flags 1,169 records as "Omitted undefined stereo in OpenBabel" and 304 as "no SMILES"), so it is not infallible — but `molecular_formula` and `molecular_weight` are the dossier's own fields and agree with it, which is two concordant signals against one. The check cannot reach the 1,409 literature rows, which carry no CAS at all.

**Mildest remedy, in order.** (a) A measured note in `curation_comments`: "of the 1,791 rows that can be matched by CAS to ECHA's own registered substance, 35 (2.0%) carry a different molecular formula" — so a curator reading the hand-off's issue 3 knows the size and that a third source exists. (b) Better, and still cheap: repair under PROV-13 the subset where ECHA's formula **and** molecular weight agree with each other and disagree with the shipped structure — an unambiguous adjudication, a second file of the same release, no new source. (c) At minimum, correct the hand-off's "no third source", which is the stated reason issue 3 recommends shipping as published.

**2. Seven rows carry no carbon at all; three of them are visibly the wrong substance (P3, USE-7 / P5)**

Ready biodegradability is defined for an organic test substance — OECD 301 measures DOC removal, oxygen demand or CO₂ evolution from the substance's own carbon. Seven shipped structures contain no carbon, and all seven are labelled `No`:

| CAS | Source's name | Shipped SMILES |
|---|---|---|
| 31765-95-4 | tetrasodium [μ-[[3,3'-[azoxybis[(2-hydroxy-p-phenylene)azo]]bis[...]]] (an azo dye) | `O=S(=O)([O-])[O-].[Na+].[Na+]` — **sodium sulfate** |
| 67226-45-3 | 1-Butylpyridinium heptachlorodialuminate | `...[Al+3].[NH4+]` — **ammonium aluminium sulfate** |
| 73018-51-6 | 1-methyl-4-(prop-1-en-2-yl)cyclohex-1-ene (limonene) | `[Ca+2].[O-2]` — **calcium oxide** |
| 20786-60-1, 13703-82-7, 12040-58-3, 7775-09-9 | borates and sodium chlorate | inorganic, as named |

The first three are finding 1 again, but visible from the shipped file alone with no outside source. The other four are inorganic substances whose class is a definitional certainty, not a measurement: a producer never commissions an OECD 301 on sodium chlorate, and a model gets them right from "no carbon". 7 of 5,845 = 0.12%, so this changes nothing numerically.

**Mildest remedy.** Name them in `curation_comments` (the `desalted` docstring already anticipates wholly-inorganic structures but does not say why they stay), or drop them under USE-7. Either is fine; the note is enough. The three mismatched ones should go into finding 1's list whatever is decided.

**3. The compound key keeps the counter-ion count, so salt families of one acid survive as separate rows (P4, LEAK-19 Should — weak)**

`_clean` keys on `desalted(..., stereo=False)`, the canonical SMILES after `FragmentRemover`. That removes the metal but keeps the **multiplicity** of the organic anions, so `X.X` and `X` are different keys. Keying on the *set* of fragments instead merges 18 keys (36 rows) that the shipped key separates, every one of them straddling scaffold groups:

- same substance, two counter-ions, classes agreeing: sodium vs zinc acrylate (Yes/Yes), potassium vs bismuth 3,3,5,5-tetramethylhexanoate (No/No), sodium vs calcium dioctyl sulfosuccinate (Yes/Yes), potassium vs calcium oleoyl sarcosinate, lithium vs calcium oleate, potassium vs aluminium formate, barium vs lithium triflate, sodium vs zinc hydroxymethanesulfinate, nicotine vs nicotine sulfate, N-isopropylhydroxylamine vs its sulfate — eleven pairs
- **genuinely different substances the set key would wrongly merge**: sodium (Yes) vs **zinc** diethyldithiocarbamate (No), sodium (Yes) vs zinc dimethyldithiocarbamate / ziram (No), sodium vs zinc p-toluenesulfinate — the metal makes the fungicide
- **a structure written wrongly, not a copy**: CAS 62132-67-6 "1-Dodecene, **dimers**" is written `C=CCCCCCCCCCC.C=CCCCCCCCCCC`, two separate dodecene molecules rather than the C24 dimer, and pairs with dodec-1-ene itself; same for CAS 34363-01-4 "P-Menth-1-Ene Dimer"

Cost of leaving it: **76 of 17,535 test evaluations (0.43%)** have a training row of the same set key, at 89.5% label agreement. On the looser largest-fragment key it is 379 (2.16%) at 72.6% agreement, barely above the 65.7% base rate.

**Mildest remedy.** A sentence in the copies bullet naming the residue and its size; the shipped key stays. An automatic switch to the set key is *not* the right fix — it would merge the zinc/sodium dithiocarbamates and then drop them whole under LEAK-20, losing real chemistry, and it would merge two dimers with their monomers. If the curator wants them gone, the eleven agreeing pairs can be dropped by hand.

**4. `time_basis` says nothing dates a row; a coarse registry order exists and the target drifts strongly along it (P4, note only)**

`time_basis` states "Nothing dates a row ... the order in which the registration programme tested chemicals cannot be measured here." The CAS registry number is assigned in order of first registration, and it is present for 4,436 of the 5,845 rows (75.9%). Sorted by its first block, the readily-biodegradable share falls monotonically across quintiles: **45.0% → 38.8% → 35.6% → 33.0% → 18.5%** (Spearman −0.172, p ≈ 1e-30).

I ran the split that claim rules out. On the 4,436 CAS-bearing rows, encoded SMILES, untuned LightGBM:

| Split | ROC AUC |
|---|---|
| hold out the newest 30% by CAS block | 0.871 (test RB 0.224 vs train 0.393) |
| hold out the newest 20% | 0.857 |
| random 70/30, same rows | 0.875 |
| scaffold-grouped 3-fold, same rows | 0.873 |

So the **conclusion survives** — an entry-order split costs 0.002–0.016 ROC AUC, nothing — but the sentence is too absolute, and a reader checking it would find the drift and wonder.

**Mildest remedy.** One sentence in `time_basis`: the CAS number gives a coarse first-registration order on three quarters of the rows, the class rate falls from 45.0% to 18.5% along it, and holding out the newest block costs 0.004 ROC AUC against a random split on the same rows — so no temporal option is given up.

**5. Körner's curated sets are not cuts of this data: they add chemicals from Lunghini et al. (P5, factual correction)**

The record's siblings bullet says `Curated_SCS`, `Curated_final` and `Curated_BIOWIN` "are cuts of the same data with no distinct task", and the hand-off's issue 3 weighs them as such. `creating_datasets.py` calls `create_classification_data_based_on_regression_data(..., with_lunghini=True)`, and that function (`processing_functions.py:1102-1112`) concatenates `get_external_dataset_lunghini(...)` onto Körner's **own** ECHA-derived set. So they are a different compilation plus an external addition, not a subset. This also bears on the "Better data" bullet, which lists Lunghini et al. 2020's set as "a publisher's supplementary file, not obtained" — part of it is obtained, inside this same repository.

**Mildest remedy.** Correct the sentence in the record and in issue 3's option B; nothing in the shipped data changes.

**6. Three files of the release have no reason given (P5, documentation)**

`datasets/chemical_speciation.xlsx`, `substance_file.xlsx`, `reach_study_results/RegisteredSubstances_organic6.pkl` — see §1. None adds rows, so this is not the `g_research_crypto_forecasting_1m` shape. **Remedy:** add them to the "Not read from the repository" bullet with one clause each. Worth saying plainly in the same bullet that the primary release (the ACS supporting information) could not be listed at all, so the file audit rests on the copy.

**7. 145 rows are multi-component substances whose "structure" is a concatenation (P7, note)**

After salt removal, 145 rows (2.48%) hold two or more **distinct organic** components, 42 hold three or more, 14 hold five or more, up to 368 heavy atoms (rosin salts, hydrocarbon reaction masses, polyvalent metal resinates). Their RB rate is 0.407 against 0.343 overall. The recommended encoding (RDKit 2D descriptors, MACCS, ECFP4) sums these over components, so for those rows the feature vector describes the mixture and not a molecule. The source tested them and a registrant does screen UVCBs, so they belong — but a line in the notes keeps a reader from reading every row as one compound. **Remedy:** one sentence; no action on the data.

**Checked and clear**

An attack that finds nothing is a result, so: everything below I tried to break and could not.

- **Timing.** The only feature is a structure, which exists before any test is commissioned. None of SPLIT-32's arrival patterns applies: no extraction window, no row overwritten at period end, no length the outcome cuts short, no end-of-event stand-in, no figure looked up later per entity, no lag of another row's target, nothing fitted over the release. The one id, `cas`, is dropped and in any case precedes the test.
- **No training weight**, so probe 22 / LEAK-41 do not apply.
- **Every count in `curation_comments` reproduces exactly** on my own run: 729 structures with more than one fragment, 585 losing something to the remover, 6,139 → 5,845 rows, 34.3% `Yes`, 4,426 groups, 4,096 of size 1, largest group `C1CCCCC1` at 105 rows (1.8%).
- **Row order** (CLEAN-23): shuffled — Spearman of frame position against raw position −0.0005.
- **Dtype probe**, re-run: `0 of 0 columns flagged` — correct, there is no ordinary feature column to type. No count typed categorical, no code typed numeric, no ordinal scale to order.
- **Missingness**: zero in all three shipped columns; the task is not temporal, so there is no per-period level to read and no partial drop-off to look for.
- **The dropped columns lose nothing a model should have had**: `source` separates two parts whose RB rates are 34.2% and 34.7%; `name`/`cas` missingness was a perfect indicator of the literature part and is now gone.
- **The target** is the source's own reading, and the threshold rule in Körner's code matches the definition's words exactly.

</details>

<details><summary>Split audit</summary>

**Split audit — `ready_biodegradability_huang_zhang`**

**Verdict: right, with notes.** The leaf, the regime, the group key and the fold mechanics are correct and robust to the one contestable answer in the tree. Two problems in what the split actually holds out; one is a Must.

**The tree walk (SPLIT-36)**

Record type `Expanding Science Catalogue` → **[CAT.next-items]**: the source keeps its model to chemicals like those it was built from and validates it on a second compilation ("compiled from the literature because it would be meaningful to validate our models using data from a different source"), i.e. items *from elsewhere*, not the programme's next entries → **no** → **Family-key step** → **[FAMILY.key]**: the data computes the Bemis-Murcko scaffold → **L-FAMILY.key**, *Grouped · `UnseenGroup` (the family key)*.

That is what the definition names (`split_leaf = "L-FAMILY.key"`), ships (`grouping(on="scaffold")`, `TimeBasis("UnseenGroup", …)`) and tags. Consistent with the `qsar_biodeg` precedent (SPLIT-37 cases row), same reasoning.

I checked the definition's robustness claim ("the walk reaches the same leaf whichever way the first question is answered") and it holds: the paper's closing does say "existing **and new** chemicals", so [CAT.next-items] can be read *yes* — but **[CAT.entry-date] is then no**, measured: no date in `class_all.csv`, the regression workbook or Körner's REACH export; the only sequence-like identifier is the CAS RN, which SPLIT-37 step 4 bars (a registration that predates catalogue entry) and which 1,546 of the 6,139 rows lack entirely; and the file is not CAS-ordered anyway (Spearman(position, CAS block) = −0.065, 48.8% of consecutive steps increasing). Same leaf either way. No forced leaf, no unreached leaf, no question without a fitting answer.

Regime matches the use case: a chemical nobody has tested is a cold start (USE-10) → grouped, not temporal. Not temporal, so the horizon/windows/floor sections do not apply; the time probe confirms there is no clock (below).

**Finding 1 — the copy key strips the counter-ion but leaves the charge, so 116 copies of one chemical survive and cross the split**

**Rule:** LEAK-19/LEAK-20 (Must, P4) and SPLIT-37 step 1 ("the item key always holds").

`desalted()` runs `FragmentRemover`, which removes `[Na+]` from `CC(=O)[O-].[Na+]` and leaves the **anion** `CC(=O)[O-]`, which never matches the free acid `CC(=O)O`. So the rule the definition states for itself — "a salt and its free form count once" (`curation_comments`, the hand-over's issue 1, option A: *"the only option under which no test chemical has its own structure in training"*) — does not hold.

Measured on the shipped 5,845 rows (my own measurement):

| copy key | distinct | extra copies | clusters | conflicting-label clusters |
|---|---|---|---|---|
| shipped (desalt + no stereo) | 5,845 | 0 | 0 | 0 |
| + `Uncharger` (salt/free acid, protonated amine, zwitterion) | 5,757 | **88** | 88 | 12 |
| + mobile-H/tautomer (neutral InChIKey skeleton) | 5,729 | **116** | 111 | 16 |

* **They cross the split:** 91 of the 111 clusters span more than one scaffold group (a ring-less chemical is its own group, so the grouping cannot hold them together). Per fold, **45.9 clusters sit on both sides; 2.40% of the test rows have their own chemical in training** (1.83% on the charge step alone).
* **It buys a lookup:** pooled over repeat 0's three folds (untuned LightGBM on the recommended encoding), the 136 twin test rows score **ROC AUC 0.929 / log loss 0.363** against **0.884 / 0.432** on the rest. Dropping the twin from the training side moves those same rows to **0.902 / 0.480** — i.e. without their copy they are *harder* than average, so the advantage is the copy. Headline cost: 0.8858 → 0.8831.
* **Entity-leakage tests (LEAK-42/43):** the link is exact chemical identity after standard normalisation, not a guess (SPLIT-24's "constructed from the data exactly"); the label travels with it (**86.4%** of the 88 clusters agree against **54.9%** chance for a random pair at p = 0.343); there is no order. 59 of the 88 straddle the compilation's two parts — the very mechanism the note says it settled for 100 chemicals; 59 more survive it.
* Examples: acetic/acrylic/formic/salicylic/phthalic/adipic/succinic acid and their Na/K/Li/Zn salts, EDTA and DTPA, octyl sulfate, dodecylbenzenesulfonate, diethylamine and its hydrochloride, betaine and cocamidopropyl betaine as zwitterion vs neutral; tautomers 2-hydroxypyridine/2-pyridone, 2-mercaptobenzothiazole/-thione, cyanuric acid, 5-aminotetrazole. Conflicting pairs include benzene-1,3-disulfonic acid (free acid `No`, disodium salt `Yes`) and pyrithione (free `Yes`, sodium `No`).

**Mildest remedy — a filter, not a re-split:** add `rdMolStandardize.Uncharger` (and optionally `TautomerEnumerator().Canonicalize`) to the **copy key only**, inside `desalted(..., stereo=False)`; the shipped `SMILES` and the scaffold key stay exactly as published. Cost: 5,845 → 5,757 rows (−1.5%), or → 5,729 (−2.0%) with tautomers, which also removes the 16 both-class clusters that today cost every model the same points. One false merge to be aware of: `C[CH-]C.[Cl-].[Mg+2]` (isopropylmagnesium chloride) collapses onto propane — it is a conflicting cluster, so it would be dropped whole either way.

**Finding 2 — the family key buys nothing for the ring-less third of the set, and the shipped number hides that**

**Rule:** SPLIT-37 step 5 / SPLIT-31 (Should, P4) — disclosure, not a re-split.

Close training analog (Tanimoto ≥ 0.7, Morgan r = 2, 2,048 bits, on the desalted compound), over all 9 shipped folds against random splits of the same sizes:

| test chemicals | grouped | random |
|---|---|---|
| all (reproduces the shipped figure) | **18.9%** | **22.4%** |
| with a ring (63.6% of rows) | **9.0%** | 15.2% |
| ring-less (36.4% of rows) | **36.1%** | 35.2% |

For ring-bearing chemicals the scaffold key cuts close analogs by 41%; for the ring-less third it does nothing at all, and that third is the analog-dense one (homologous series). `splits_comment` reports only the 18.9/22.4 average and says ring-less chemicals "are held out one by one", which reads as a design choice rather than "a third of the set gets a random draw and keeps a close analog 36% of the time"; `task_summary.split` says plainly "a test chemical belongs to a family the model has not seen". SPLIT-31 prescribes exactly this treatment and the precedents match (qsar_bioconcentration 34% ring-less, qsar_oral_toxicity 23% + 18%), so nothing changes in the split — **remedy: one clause with the breakdown in `splits_comment` and the `Time basis:` line.**

**Attacks that found nothing (results in the definition's favour)**

* **No group overlap** in any of the 9 folds; test folds 1,763–2,117 rows with 628–710 positives; 3 repeats × 3 folds is SPLIT-33's tier for a ~3,900-row training side.
* **The group id is a true computed key**, not a similarity cluster or a feature hash (SPLIT-24 ✓). No scaffold reaches a tenth (largest, cyclohexane, 1.8%); benzene-only (17.1%) and ring-less (36.4%) are broken into singletons as SPLIT-31 asks. One prediction = one chemical from its structure alone; nothing is known about a new series but its members' structures; no aggregation. All verified against the frame.
* **The time probe's two flags are not a clock.** `Unnamed: 0` is exactly the row index (verified bit-for-bit), so `id_drift` is `order_drift` twice. The class does not trend along the file (Spearman −0.036 in the regression-derived part, −0.019 in the literature part), the tenths swing 0.241–0.568 without direction, and the two parts have the same positive rate (0.350 / 0.347). The neighbour statistics the definition quotes reproduce exactly (next-row class agreement 0.664 against 0.549 chance).
* **The source's own cross-source design is not a harder split than the shipped one.** Train on the 4,436 regression-derived chemicals → test on the 1,409 literature ones: **ROC AUC 0.910**, against **0.897** for a scaffold-grouped split of the same sizes. So holding out the compilation's parts would be *easier*, and there is no case for grouping on `source` (SPLIT-37 step 6: disclose, do not group).
* **Stereochemistry in the scaffold key costs nothing:** computing the scaffold on the stereo-free compound changes 225 scaffold strings but merges no groups (4,426 either way).
* The IID-vs-grouped gap (0.894 vs 0.885) is small because 4,096 of 4,426 groups hold one chemical — expected, and no argument either way (SPLIT-4: the size of the gap never decides).

The measurements above are my own: the folds, the analogue shares, the copies, the row order, the model effects, and a re-run of the time probe.

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner — `ready_biodegradability_huang_zhang`**

I played the two actors the definition names: **a producer/registrant screening a structure before commissioning a ready-biodegradability test**, and **a regulator ranking registered chemicals for persistence screening**. I ran every measurement below myself.

**Verdict**

**Fit: direct** — the structure is genuinely all I hold before the test, the test is genuinely the thing I am deciding whether to buy, and the scaffold-held-out test chemicals are, measurably, *no easier* than the real chemicals I would screen. The declared `fit="direct"` stands, but `task_summary.question` overstates the target (finding 1).

**Metric: yes** — `roc_auc` scores my decision and I would pick a model by it. Details at the end.

**Answers to the five questions, as the actor**

1. **Do I have the inputs?** Yes, entirely. The structure exists before any test; nothing in the frame is recorded after my decision. Nothing I would *always* hold is missing: measured water solubility, log K_ow and vapour pressure sit in the same REACH Annex VII tier and I usually do have them, but every deployed tool in this field (EPI Suite BIOWIN, VEGA, OPERA, and the authors' own online predictor) takes SMILES alone, so the source's prediction point is honestly reproduced (USE-3, USE-6). Dropping `cas` is right beyond CLEAN-21: CAS numbers are issued roughly chronologically, so keeping it would smuggle in registration vintage.
2. **Is the target what I act on?** Not exactly — see finding 1. It is the test reading at day 28, not the regulatory conclusion.
3. **One row, one decision?** Yes: one chemical, one screening call, one row (the duplicate collapse makes this hold, MET-17-style). The test data is what I face — I measured it (finding 5).
4. **Would I use it?** Yes. What would make me trust it is an applicability-domain statement per query, which the authors ship with their predictor and the benchmark does not. What makes me distrust it is finding 2.
5. **Metric?** Yes — below.

**Findings, ranked by how much they change the task**

**1. The target is the day-28 reading, not "readily biodegradable" as I or a regulator use the word (USE-5, USE-8)**

The OECD 301 series requires the 60%/70% pass level to be reached inside a **10-day window** before a substance counts as readily biodegradable. The label here ignores it, and the paper never mentions it (`grep -i "10-day|window"` over the full text returns nothing).

How much it costs me, from the registrants' own verdicts in Körner's REACH export (`interpretation_of_results`, my `g3.py`):

| Guideline | records called readily biodegradable in any form | share flagged "**but failing 10-day window**" |
|---|---|---|
| OECD 301 B | 1,005 | 15.7% |
| OECD 301 F | 881 | 16.8% |
| OECD 301 D | 643 | 13.7% |
| OECD 301 E | 133 | 22.6% |
| OECD 310 | 122 | 13.1% |
| **OECD 301 C (MITI)** | **348** | **1.4%** |

The 301 C row is the known exemption — the 10-day window does not apply to the MITI test — visible here in the dossiers themselves. So the curation note's framing ("the label ... ignores the 10-day window") is right but **uneven**: the gap is ~0 for the 22.5% of day-28 records run under 301 C and roughly 1 in 7 for the rest. Since the guideline is not a shipped column, no one downstream can tell which rows are affected. The builder's own measurement agrees in size (89 of 783 positives flip, 11.4%).

This does not sink the task — issue 2's option A is right, two label definitions in one target column would be worse — but two things should change:
- `task_summary.question` currently reads "**Is a chemical readily biodegradable** in a standard aerobic screening test". To me that phrase is the regulatory conclusion. It should read as `predicted` already does: *does the chemical reach 60% degradation by day 28 (70% for DOC-based methods)*.
- `fit_reason` should name the window as a known, measured gap in the target, the way USE-8 asks, rather than leaving it only in `curation_comments`. I would not move the fit to approximate for it: the label is verified, documented and reproduced at 97.6%, which is the opposite of the `differentiated_thyroid_cancer_recurrence` situation, and the gap is bounded and measured.

**2. The label pools seven protocols, and the protocol is the one thing I choose (USE-4, TP-6)**

Measured on the authors' own regression workbook, day-28 ready records (`g2.py`):

| Guideline | records | pass rate |
|---|---|---|
| OECD 301 F | 1,510 | 38.8% |
| OECD 301 B | 1,433 | 40.5% |
| **OECD 301 C (MITI)** | 1,377 | **27.2%** |
| OECD 301 D | 1,055 | 37.6% |
| OECD 310 | 167 | 52.7% |
| OECD 301 A | 161 | 46.6% |

And on repeat-tested chemicals: of the **705 chemicals tested under more than one guideline, 27.2% get opposite pass/fail calls**; of the 194 with repeats under a *single* guideline, 13.4% disagree. So roughly half the test-retest noise is protocol-driven, not laboratory noise.

The source knows this: its regression model ranks `principle` the **3rd** and `guideline` the **9th** most important feature of all, and its deployed *regression* predictor makes the user pick the guideline and principle from a dropdown. Its *classification* predictor deliberately does not — "to expand the application of this study to when only binary classification is needed (an industry norm) **without specifying the experimental conditions and reaction time**". That sentence is what makes the shipped task legitimate under USE-4: it is exactly the source's classification task, at the stage the source describes, and OECD designed the series to be equivalent. But the pooled label carries a ceiling no method can pass, and the current `curation_comments` give only the qualitative version ("the paper treats them as one protocol"). The numbers above belong there.

**This also changes the `qsar_biodeg` retirement claim.** That record is MITI/301 C alone — the strictest protocol in the table, 27.2% pass against 34.3% here. The replacement is not the same label on more chemicals; it is a *pooled* label. the live decision item on `qsar_biodeg` lists this only as a one-clause con of option C. A reader deciding C deserves the 27.2%-cross-protocol-disagreement number.

**3. Some rows carry a structure that is not the substance that was tested (CLEAN, builder issue 3)**

This is the defect that worries me most as a user, because it corrupts the **feature**, not the label, and the builder's issue 3 frames it as "which of the two structure retrievals is right (needs a third source)". For part of it, no third source is needed — the shipped file contradicts itself. All 8 carbon-free rows in `class_all.csv` (`g4.py`):

- `1-methyl-4-(prop-1-en-2-yl)cyclohex-1-ene` (limonene, CAS 73018-51-6) → SMILES `[Ca+2].[O-2]` (calcium oxide), label `No`
- a tetrasodium copper azo dye (CAS 31765-95-4) → SMILES `O=S(=O)([O-])[O-].[Na+].[Na+]` (sodium sulfate)
- `Neodecanoic acid, zinc salt, basic` → zinc sulfate
- `1-Butylpyridinium heptachlorodialuminate` → ammonium aluminium sulfate

Eight rows is nothing; the point is that they are the visible tip of the 270-of-3,767 shared CAS numbers (7.2%) that the builder measured against Körner's repaired `Curated_SCS`. I support **option A (ship as published)** — I do not want the label-noise-filtered cuts, which remove exactly the hard chemicals I need a model to be honest about — but I would add the cheap middle path the issue does not list: drop the handful of rows whose name and structure cannot be the same substance by an internal check (an element in one and absent from the other), which needs no adjudication and no third source.

**4. A few rows are decisions nobody makes (USE-7, minor)**

38 rows (0.6%) have no organic carbon beyond a single hetero-bonded atom: calcium carbonate (labelled `Yes` — a carbonate evolving CO₂ in a CO₂-evolution test is a test artefact, not biodegradation), sodium chlorate, borates, CFC-11, trifluoroiodomethane. REACH waives the ready-biodegradability study for inorganic substances, so I would never commission this test for them. Too few to matter; worth one clause in `curation_comments` rather than a filter.

**5. Not a gap — the split is a faithful, mildly conservative stand-in for my screening population (USE-8, SPLIT-31)**

I ran the `qsar_oral_toxicity` check on this set. The screening population I used is the **846 REACH-registered chemicals in Körner's ECHA export that are not in the compilation** — real registered substances outside the training data (`g5.py`, Morgan r=2/2048, nearest-neighbour Tanimoto on the desalted structure):

| Query chemicals | reference | close analog (T ≥ 0.7) | median nearest |
|---|---|---|---|
| scaffold-grouped test folds | their training side (~3,900) | 18.9% | 0.522 |
| random folds | their training side | 22.2% | 0.550 |
| **846 REACH chemicals outside the set** | random 3,900-chemical subsample | **19.9%** | **0.541** |

A held-out test chemical is slightly *less* like the training side than the next real registered chemical is. This is the opposite direction from `qsar_oral_toxicity` (11.2% for the untested population against 15.1% for its test folds, which is why that one reads approximate), and it is why I read this fit as direct rather than approximate despite the superficially similar 18.9%-vs-22.4% numbers. The precedent-checker should have this: on the analog spread alone this set sits between `qsar_bioconcentration` (direct) and `qsar_oral_toxicity` (approximate), and the measurement above is what breaks the tie.

Secondary: the paper projects **15.6% readily biodegradable across DSSTox** against 34.3% here. The chemical universe I screen is more NRB than the training set. That is a prior shift, not a coverage gap (98.4% of DSSTox is inside the model's applicability domain), and it has a direct metric consequence — below.

**What an expert in the domain would change**

1. Reword `task_summary.question` to the day-28 reading, and name the 10-day window in `fit_reason` (finding 1).
2. Put the guideline numbers in `curation_comments` and in the `qsar_biodeg` retirement note (finding 2), with the source's own sentence that its classification task drops the conditions on purpose.
3. Add the internal name-vs-structure check as a cheap partial repair (finding 3).
4. Note, for the benchmark's own record, that the serious practitioner task in this source is the **conditional** one — the 12,750-record regression workbook where the guideline, principle and time are inputs, which is what the authors' own regression predictor serves. `curation_comments` correctly calls it "a task of its own"; I would say explicitly that it is the version an actor who has already chosen the test method would use, so a later curator does not re-litigate it.
5. Nothing about the split, the feature or the prediction point. Those are right.

**Does the metric score my decision?**

**Yes.** `Metric.fallback` → `roc_auc`, and I would choose the same.

- **MET-1/MET-2, unit:** the unit is the chemical, one row is one screening call, and after the duplicate collapse each chemical votes once. No scoring inputs are needed.
- **MET-5/MET-6:** the paper reports accuracy, sensitivity, specificity, balanced accuracy, ROC AUC and F₁ side by side and names none as deciding, so there is no deliberate original. Two further facts strengthen the rejection: its classification model was fitted after **data balancing** ("data balancing was first performed"), so its 85.6% accuracy is not on our 34.3%-positive frame at all (MET-2's "same class balance" clause, as on `emscad` and `taiwanese_bankruptcy_prediction`); and the screening population's prior differs again (15.6% projected RB across DSSTox). A hard-label score computed on our balance would transfer to neither.
- **MET-7:** no source fixes a cost or a threshold. The real decisions are asymmetric — a wrong "will pass" costs me a 28-day, $3,000–8,000 test plus a higher-tier study, a wrong "will fail" costs me a candidate molecule I should have kept — but nobody publishes the ratio, so a threshold-free metric is the right call, not an invented matrix.
- **MET-8/MET-9:** my dominant real decisions are rankings — which of my candidate structures to synthesise, which registered chemicals to put first in a persistence screen — and ROC AUC holds for every cost and prior, which matters precisely because the prior shifts. 34.3% positive is not imbalanced, so MET-9 gives no reason for average precision.

One caveat I would record rather than act on: for the per-chemical go/no-go, calibration matters and ROC AUC does not see it — a strictly proper rule (log loss, Brier) would score that part, and regulatory screening in this field is in fact operated at fixed cut-offs on a model's probability output (the ECHA R.11 BIOWIN screening combinations; I could not verify the exact numeric thresholds, see below). I would **not** overrule `roc_auc` on that: MET-8's binary fallback is `roc_auc`, the ranking use is real, and consistency with the retiring `qsar_biodeg` and the QSAR siblings is worth keeping.

**Sources**

- Huang & Zhang, *Environ. Sci. Technol.* 56(17), 2022, [doi:10.1021/acs.est.2c01764](https://doi.org/10.1021/acs.est.2c01764) — read from the extracted text of the accepted manuscript: the cost/duration motivation, the classification-task design sentence, the SHAP ranking of `principle`/`guideline`, the free online predictors and their inputs, Table 1 (DSSTox applicability domain, 15.6% RB).
- Körner et al. 2024, [doi:10.1039/d4em00431k](https://doi.org/10.1039/d4em00431k), and their repository's `iuclid_echa.csv` REACH export — the registrants' own `interpretation_of_results`, including the 505 "readily biodegradable, but failing 10-day window" records.
- `Huang_Zhang_RegressionDataset.xlsx` (same repository) — guideline, principle, time and percent degraded, for the protocol analysis.
- OECD Test No. 301 and 310 pass criteria and the 10-day window, including the MITI/301 C exemption and the 14-day option for 301 D: [oecd.org/environment/test-no-301-ready-biodegradability_9789264070349-en](https://www.oecd.org/environment/test-no-301-ready-biodegradability_9789264070349-en), [test-no-310](https://www.oecd.org/environment/test-no-310-ready-biodegradability-co2-in-sealed-vessels-headspace-test_9789264224506-en) — **search results only**; oecd.org returns 403, the FAO toolkit page 404, eur-lex returned an empty body and echa.europa.eu returns 403 for the R.11 and Part C guidance, so I could not obtain primary quotes. The 301 C exemption is nevertheless established here independently, from the dossier verdicts (1.4% vs 13.7–22.6%).
- ECHA R.11 BIOWIN persistence screening combinations: [UBA mirror of the Part C screening-criteria table](https://www.umweltbundesamt.de/system/files/medien/2674/dokumente/table_screening_criteria_part_c.pdf), [UBA mirror of R.11](https://www.umweltbundesamt.de/system/files/medien/2674/dokumente/information_requirements_r11_0.pdf) — fetched but unreadable (no PDF text extraction available in this environment); the numeric thresholds remain **unverified** and I have asserted none.
- REACH Annex VII 9.2.1.1 and the Annex XI §1.3 QSAR adaptation route: [legislation.gov.uk consolidated Annex VII](https://www.legislation.gov.uk/eur/2006/1907/annex/VII/data.pdf).

</details>

<details><summary>Blind review</summary>

**Verdict**

**Include only with changes — and the required change is structural: as delivered the table is a single free-text SMILES string plus a redundant scaffold string, which a tabular learner cannot use at all (AUC 0.500, majority-class accuracy), so in a tabular benchmark it must either be re-prepared with precomputed molecular features or excluded.**

Underneath the packaging this is a *good* prediction problem — real decision, no temporal leakage possible, honest signal (AUC ≈ 0.88), labels verified against the public source — but the preparation turns it into a test of whether a pipeline has a character-n-gram text encoder, not a test of tabular modelling.

**Concerns, most to least serious**

**1. It is not a tabular task as prepared — the only feature is a chemical line notation**

`data.parquet` is 5,845 × 3: `SMILES` (string, all 5,845 values unique), `scaffold` (string, 4,426 unique), `Biodegradable` (category No/Yes, 3,839/2,006 = 65.7%/34.3%). There is no numeric column.

What that means in practice, measured under the stated 3×3 scaffold-grouped regime:

| Treatment of the two string columns | AUC | acc | bal. acc |
|---|---|---|---|
| both as categoricals (LightGBM, native categorical) | **0.500** | 0.656 | 0.500 |
| SMILES as text, char 1–6-gram TF-IDF + LogReg | 0.878 | 0.810 | 0.777 |
| SMILES → char-TFIDF → SVD-64 → LightGBM | 0.859 | 0.795 | 0.757 |
| **RDKit MACCS + Morgan-1024 + 12 descriptors, LightGBM** | **0.878** | 0.811 | 0.784 |
| MACCS keys alone, LightGBM | 0.876 | 0.814 | 0.789 |
| SMILES string length alone | 0.642 | 0.649 | 0.529 |

Two things stand out. A generic tabular pipeline gets **exactly nothing** — every SMILES is unique, so the column is a 5,845-level ID and the model returns the base rate. And a naive character-n-gram encoder reaches **0.878, identical to full cheminformatics featurization**. So the dataset does not discriminate between tabular methods; it discriminates between pipelines that happen to apply n-gram hashing to a string column and those that do not. That is the wrong axis for a tabular benchmark.

**Change:** replace `SMILES` with precomputed numeric features — MACCS (167 bits) is enough on its own here, or MACCS + ~12 RDKit physicochemical descriptors (MolWt, logP, TPSA, HBD, HBA, rotatable bonds, rings, FractionCSP3, aromatic rings, heavy atoms, NHOH, NO). Keep `SMILES` as a non-feature identifier. That version is a legitimately good tabular task. If the benchmark's prep step cannot do chemistry featurization, exclude it.

**2. The split does not deliver the "grouped by scaffold" regime it claims**

`task.md` says *"Regime: grouped by `scaffold` (whole groups are held out)"*. The scaffold column does not implement a scaffold split.

- **1,000 rows (17.1% of the dataset) whose true Bemis–Murcko scaffold is plain benzene were each given their own singleton group** instead of one benzene group. I reproduced the column with `MurckoScaffold.MurckoScaffoldSmiles` (mapping empty → `"single: <smiles>"`): it matches on only **79.45%** of rows, and every one of the 1,001 mismatches is a molecule whose real scaffold is `c1ccccc1`. There is not a single row in the file with `scaffold == 'c1ccccc1'`.
- Consequence: **4,096 of 5,845 rows (70%) sit in singleton groups**; the largest group has 105 rows instead of 1,000. Under a true Murcko grouping there would be 3,428 groups with a 1,000-row largest group; here there are 4,426 with a 105-row largest.
- The grouping therefore does almost no work. Max-Tanimoto (Morgan-2048) from each test molecule to its nearest training molecule: **0.553 under the scaffold split vs 0.572 under a plain random split**; the share of test molecules with an *identical* fingerprint in train is **6.9% grouped vs 6.3% random**. Model performance barely moves: AUC **0.878 grouped vs 0.883 random**.

This may have been deliberate (a 1,000-member benzene group would wreck 3-fold balance), but it is undocumented, and as it stands `task.md` oversells the regime. Fold sizes are also uneven: test folds range 1,813–2,178 rows (31.3%–37.3%).

**Change:** either state plainly that benzene-scaffold compounds are split at random and that 70% of rows are singleton groups, or switch to a grouping that actually holds out chemistry (e.g. Butina clustering at Tanimoto 0.6, or generic Murcko frameworks). If the grouping is kept as-is, calling the regime "random" would be more honest than "grouped by scaffold."

**3. The same substance appears in both train and test as different salt/protonation forms**

The preparer deduplicated on a stereochemistry-insensitive key and dropped conflicting-label groups (294 of the source's 6,139 unique canonical SMILES removed), but did not desalt. After collapsing to the neutral, desalted, stereo-stripped parent I find **169 parent compounds covering 391 rows that are still present more than once**, and **139 of those 169 are spread across more than one `scaffold` group**, so the split does not keep them together. Examples from the file:

| SMILES | label | scaffold group |
|---|---|---|
| `C=CC(=O)O` (acrylic acid) | Yes | `single: C=CC(=O)O` |
| `C=CC(=O)[O-].[Na+]` (sodium acrylate) | Yes | `single: C=CC(=O)[O-]` |
| `C=CCOCC(O)CS(=O)(=O)O` | No | `single: C=CCOCC(O)CS(=O)(=O)O` |
| `C=CCOCC(O)CS(=O)(=O)[O-].[Na+]` | No | `single: C=CCOCC(O)CS(=O)(=O)[O-]` |
| `C1COCCN1` (morpholine) | No | `C1COCCN1` |
| `C1COCCN1.NS(=O)(=O)O` | No | `C1COCCN1` |

Across the nine folds, **4.7% of test rows (83–104 per fold)** have the same parent substance sitting in train; 6.9% have a bit-identical Morgan fingerprint in train.

To my credit of the preparation, the damage is small: on those identical-fingerprint test rows the model scores acc 0.845 / AUC 0.849 versus acc 0.812 / AUC 0.869 on the rest — a ~3-point accuracy bonus on 7% of rows, so roughly 0.2 accuracy points on the headline. Real, but second-order. **41 of the 169 parent groups carry conflicting labels**, which is the more damaging half: that is irreducible noise sitting on both sides of the split.

**Change:** deduplicate on the desalted/neutralized parent (largest organic fragment, uncharged, stereo removed) and drop groups that disagree, as the preparer already did at the stereo level.

**4. Label noise sets a hard ceiling, and `task.md` does not warn about it**

The target is the OECD 301-series ready-biodegradability pass/fail. Huang & Zhang built it from eChemPortal records restricted to *"reliability levels 1 (reliable without restriction) and 2 (reliable with restrictions)"*, and their own text acknowledges the threshold is protocol-dependent — *"DOC-based standard methods usually set a threshold of 70% (not 60% for other principles) to classify the ready biodegradability"* — so one binary label is collapsing heterogeneous test protocols.

Two independent measurements of the resulting noise:
- The pooled file is Huang & Zhang's `ClassDataset_all` = `ClassDataset_original` (4,593) + `ClassDataset_external` (1,546), and the paper states the external set *"was compiled from the literature because it would be meaningful to validate our models using data from a different source."* Of **118 substances that appear in both sources** (matched on InChIKey skeleton), **8.5% carry opposite labels**.
- The follow-up study whose repo is linked in `task.md` concluded: *"despite comprehensive data curation, only marginal improvement was observed in the classification model's performance. This was attributed to three potential reasons: 1) a significant number of data labels were noisy…"* — and only got balanced accuracy from 80.9% to 94.2% by **filtering labels with another predictive model**, which is circular and not a real ceiling.

My grouped balanced accuracy of 0.784–0.789 sits right at the realistic 80.9% figure. This is not a reason to exclude — the signal is genuine and well above the 0.657 base rate — but the benchmark should not expect methods to separate above ~0.88 AUC, and small AUC differences between methods will be inside the noise floor.

**5. Out-of-scope rows survive the curation**

In a dataset about *"aerobic biodegradability of **organic** chemicals"*:
- **16 rows contain no organic fragment at all**: `[Ca+2].[O-2]` (calcium oxide), `[B].[Mg+2].[O-2]`, `[Na+].[O-][Cl+2]([O-])[O-]` (sodium perchlorate), `O=S(=O)([O-])[O-].[Na+].[Na+]`, `OB(O)O.[K]`, plus `C` (methane), `CI`, `CBr`, `CCl`, `CS`, `C#C`. An inorganic salt cannot be "readily biodegradable" in any mechanistic sense; these are label artifacts.
- **248 rows are genuine multi-organic-component mixtures / UVCB-like entries**, e.g. `CCCC(C)C.CCCCCCC`, `CCCCCC.c1ccc2ccccc2c1.c1ccccc1`, `C1=CCCC1.C=C/C=C/C.C=C/C=C\C`. A structure–property model has no well-defined input for these.
- A further 404 rows are salt forms (652 multi-component rows total, 11% of the file).

**Change:** drop the 16 non-organic rows and consider dropping the 248 mixtures; they add noise that no method can learn.

**6. The preparation is undocumented and `scaffold`'s role is ambiguous**

`task.md` gives three DOIs/URLs and nothing about what was done. I reconstructed it: the file is `ClassDataset_all` (6,139 unique canonical SMILES) minus 294 rows removed by a stereochemistry-insensitive dedup that drops label-conflicting groups. **All 5,845 labels match the public source exactly (100% agreement)** and the class balance matches the paper's *"all have around 65% of negative (0s, NRB) and 35% of positive (1s, RB) records."* So provenance is sound — it just isn't written down. The exact filter is not reproducible from the file alone: two near-miss reconstructions of mine gave 5,704 and 5,969 rows rather than 5,845.

Also, with "3 columns (target included)" it is unclear whether `scaffold` is a *feature* or only a split key. If it is a feature, note that for the 3,125 `"single: …"` rows it is a **verbatim copy of the SMILES column** — harmless (no target leakage; whole-group holdout means test scaffold values are unseen) but redundant and confusing.

**Change:** add to `task.md` the label definition (OECD 301 A–F; ≥60% ThOD/ThCO₂ or ≥70% DOC removal within 28 days), the dedup rule, the benzene exclusion, and an explicit statement of whether `scaffold` is a feature.

**7. Things that are fine (checked, no action)**

- **Real use, honest evaluation direction.** The decision is concrete: a REACH registrant or a regulator screening a substance for persistence/PBT assessment *before* commissioning a 28-day OECD 301 test, or triaging a large inventory. The only input is molecular structure, which is known at the moment of the decision by construction. **There is no column that could be unknown at prediction time** — no assay conditions, no measured endpoints, no post-outcome fields leaked in.
- **Real, not generated.** Experimental records from eChemPortal/ECHA/OECD SIDS. All 5,845 SMILES parse in RDKit; spot-checks are chemically correct: acetic acid Yes, glycerol Yes, sorbitol Yes, benzoic acid Yes, lauric acid Yes; DDT No, diuron No, 1,2-dichlorobenzene No, 4-chlorophenol No; **all 60 rows with a perfluoroalkyl chain are labelled No**, exactly as PFAS chemistry requires.
- **Not trivial, big enough to score.** 0.878 AUC vs a 0.657 majority baseline, fold-to-fold std 0.007–0.008 across 9 splits with ~1,950 test rows each. Comfortably resolvable.
- **No ordering leakage.** Row index alone gives AUC 0.491; corr(index, target) = −0.005.
- **No weight column.** `task.md` labels none, and none is needed; the sixth question is N/A here.
- **Types/missingness are clean.** Zero nulls anywhere, `string[python]` and unordered `category` dtypes, no encoding artifacts.

**What I could not check**

- **The exact label definition.** Huang & Zhang put the classification-set construction in SI Text S1.2 and Table S6. ACS (`pubs.acs.org`) returned 403; I obtained the main-text PDF from the public NSF-PAR mirror but it does not carry the SI. So I could not verify the exact biodegradation threshold used, nor how multiple conflicting study results for one chemical were aggregated into one binary label. The 8.5% cross-source disagreement in §4 is my empirical substitute.
- **The Körner et al. 2024 full text.** Both `pubs.rsc.org` and `chemrxiv.org` returned 403. My quotes from that work come only from the abstract published in the linked GitHub repository's README. In particular I could **not** verify their claim of *"data leakage between test and training set"* in the Huang & Zhang data — in the repo's own copies I found **zero** canonical-SMILES overlap and only 5 InChIKey matches between `ClassDataset_original` and `ClassDataset_external`, so either the repo ships corrected files or the leakage was at the identifier level. Either way, pooling both sets into one CV pool, as done here, makes the question moot.
- **The underlying experimental records.** I cannot confirm that any individual eChemPortal entry is correct; I can only confirm the file faithfully reproduces what the published source says.

**Sources:** [Huang & Zhang 2022, ES&T 56(17):12755–12764](https://doi.org/10.1021/acs.est.2c01764) (full text via [NSF-PAR](https://par.nsf.gov/servlets/purl/10350359), abstract via [PubMed 35973069](https://pubmed.ncbi.nlm.nih.gov/35973069/)) · [Körner et al. 2024, Environ. Sci.: Processes Impacts 26, 1780–1795](https://doi.org/10.1039/d4em00431k) (abstract only, via repo README) · [pkoerner6/Prediction-of-Aerobic-Biodegradability-of-Organic-Chemicals](https://github.com/pkoerner6/Prediction-of-Aerobic-Biodegradability-of-Organic-Chemicals)

</details>

<details><summary>Task gamer</summary>

**Verdict**

**This task is close to ungameable: no feature I could build adds more than ~0.002 AUC over an honest LightGBM (0.8854), and every format, order, duplicate-label and post-hoc-column attack came back empty — but the split itself is softer than its stated "whole scaffold groups held out" regime, because the single largest scaffold class (benzene, 1009 rows) was dissolved into 999 one-row groups and ~470 rows are the same chemical written twice, together worth about +0.007 AUC of free optimism that every model collects automatically.**

Honest baseline: untuned `LGBMClassifier` on RDKit 2D descriptors (217) + ECFP4-2048 computed from the shipped SMILES (`features()` ships only `SMILES`, so featurisation is unavoidable) — **mean ROC-AUC 0.8854** across the 9 splits (0.8777–0.8969). Noise band: refitting with one extra column of random numbers gives 0.8851 / 0.8852 / 0.8854 (mean moves ±0.0003; individual splits ±0.004). A better *honest* model (descriptors + ECFP4 + MACCS + count-ECFP6, mild tuning) reaches **0.8895** — that is modelling, not an exploit, and exploits are measured against both.

**Exploits ranked by gain**

| # | Exploit | Script | Honest score | Exploited score | Gain (per split, range) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| 1 | Composition/density features counted over train **and test** rows together (neighbour counts at Tanimoto ≥0.5…0.9, scaffold/formula/structure counts over the whole table) | measured | 0.8854 / 0.8895 | 0.8870 / 0.8905 | +0.0016 / +0.0010; per split −0.0016 … +0.0055, 6/9 positive | No — it needs the benchmark's own test rows | Nothing to fix in the data; it is barely above noise. Declare transduction out of scope if it matters |
| 2 | Twin label: the measured label of a train row that is the same chemical after salt/charge/tautomer/stereo normalisation (5.3–6.1% of test rows have one) | measured | 0.8854 | 0.8857 | +0.0003 — inside the noise band | No, but the baseline already harvests it implicitly | Merge the twins into one group (see F2) |
| 3 | 1-NN Tanimoto label + similarity as features | measured | 0.8854 | 0.8853 | −0.0001 | Yes (k-NN is a legitimate model) | — |

Nothing else moved the number. **The task cannot be meaningfully gamed.**

**Flaws that make the task easier than its stated regime**

These are not extra points I can take — the baseline already banks them — but they inflate every reported score relative to the regime `task.md` promises.

| # | What is wrong | Honest choice | Shipped-split score | Honest-split score | Fix |
|---|---|---|---|---|---|
| F1 | The benzene scaffold class (1009 rows, 17% of the data) is not grouped: 999 of them sit in one-row groups, so monoaromatics are split at random | Hold the class out whole, as every other scaffold is | 0.8882 (re-split on shipped groups); **0.8962 on the benzene rows themselves** | 0.8805 (benzene merged into one group); **0.8356 on the benzene rows** | Remove the group-size cap, or sub-group benzene by a decorated scaffold instead of exploding it into singletons |
| F2 | 205 groups / 469 rows are the same chemical written twice (free acid vs metal or amine salt, charged vs neutral, tautomer, stereoisomer); 172 of them get **different** `scaffold` strings and therefore cross folds | Group by the standardised structure as well | 0.8882 | 0.8818 (groups = scaffold ∪ standardised-structure ∪ Tanimoto ≥0.7 single-linkage) | Standardise (largest fragment, neutralise, canonical tautomer, strip stereo) before computing the scaffold key; dedupe or at least co-group |
| F3 | Acyclic compounds (2124 rows, 36%) always get a `single:` singleton group, so homologous series are split at random | Group homologues together | 12.0% of acyclic test rows have a train row at ECFP4 Tanimoto = 1.0, vs 1.7% of ring rows; median max similarity to train 0.60 vs 0.44 | folded into F2's 0.8818 | Give acyclic molecules a homologue-family key (e.g. carbon-chain-collapsed skeleton) |
| F4 | 46 duplicate groups (122 rows) carry **contradictory labels** — the same chemical is Yes in one row and No in another | Drop them from training | 0.8854 | 0.8849 — **no gain**, so this is label noise the model already tolerates | Resolve or drop the contradictions so the test side is not self-defeating either |

**Mechanisms**

**F1 (the real finding).** The shipped `scaffold` column is a Bemis–Murcko scaffold of the salt-stripped molecule, except that a class above some size cap is replaced by `single: <SMILES>`, one group per row. Exactly one class exceeds the cap: `c1ccccc1` never appears as a group value, and its 1009 members occupy 999 groups of size one, while `C1CCCCC1` (107) and `c1ccc2ccccc2c1` (65) survive intact. Consequence: a benzene-scaffold test row sits a median Tanimoto of 0.58 from a benzene train row, and the baseline scores 0.8962 on those rows but 0.8356 when the whole class is held out — a 0.061 drop on 17% of the data, 0.0077 on the task. Mildest fix: keep the cap but split the class by a decorated scaffold (ring + first-shell substituents) rather than by row.

**F2/F3.** The preparation already removed 293 rows of `class_all.csv` that were stereo/salt variants of a kept row (247 of the 293 collapse onto a kit row under my normaliser), so deduplication was attempted — but a different normaliser than mine, and 205 groups survived: acetic acid appears as 10 separate rows (free acid plus La/Cr/Co/Y/Li/Nd… salts) in 10 different scaffold groups; oleic acid as 9; sodium *p*-toluenesulfinate appears once as `…S(=O)[O-].[Na+]` (No) and once as `…S(=O)[O][Na]` (Yes). Because the scaffold key is computed on the SMILES as written, each salt form becomes its own group, so 5.3–6.1% of each test fold has a literal twin in train. Re-splitting with those twins co-grouped costs 0.0064 AUC. Fix: standardise before keying.

**Exploit 1.** How many analogues a compound has *inside the benchmark* is curation information, not chemistry: well-studied industrial series (fatty acids, surfactants) are over-represented and mostly biodegradable. Counting neighbours over all 5845 rows gives 0.8869; counting them over the training rows only — the honest version — gives 0.8858, against a 0.8854 baseline. So ~+0.0011 is attributable to seeing the test rows, which is marginal and I would not defend it as a finding beyond its size.

**Attacks that found nothing**

1. **Formats.** No numeric columns at all (decimals, trailing zeros, sentinels, precision: N/A). No missing values. Every one of the 5845 SMILES is byte-exactly RDKit-canonical output, all ASCII — the kit re-canonicalised everything, which kills source-tagging by string style. Format-only features (charge flags, fragment count, stereo markers, explicit-H brackets, isotopes, dative bonds, metals, bracket/digit/case counts) fit alone reach 0.794, but that is molecular size and ionic character, i.e. chemistry: adding them to the full model gives 0.8854, exactly the baseline (measured).
2. **Representation as a proxy for source.** Refitting on standardised structures (largest fragment, neutralised, destereo, canonical tautomer) gives 0.8863, *better* than the as-shipped 0.8854 — so the shipped protonation/salt representation carries no hidden label information. Matching all 5845 rows to the published `class_all.csv` confirms it: P(Yes) is 0.342 for `ClassDataset_original` and 0.347 for `ClassDataset_external`, so even the true source column is not predictive (measured, measured).
3. **Order and ids.** No id column. Correlation of the target with row position −0.005; next-row label agreement 0.5455 against a chance 0.5492; adding the row index as a feature gives 0.8851. The rows are shuffled (measured).
4. **Copies across the split.** Covered above: present (F2) but not separately exploitable (+0.0003).
5. **The training rows / temporal leakage.** `task.json` has no time column, no `prediction_time`, no `time_of`: nothing to test.
6. **Columns from after the prediction point.** The kit ships only `SMILES`; the published source's post-hoc fields (CAS, name, source, pKa, study reliability) were all dropped. None available.
7. **The weight.** `sample_weight` is null.
8. **Transforms over all rows.** Rank/quantile/standardised versions of the descriptors: no effect — LightGBM is invariant to monotone transforms; only the *count* features of exploit 1 carry transductive information.
9. **Test-set composition.** A train-vs-test classifier reaches AUC 0.62 on split r0f0 — the folds are structurally distinguishable, as a group split implies — but that gives no handle on the label. Pseudo-labelling confident test rows and refitting: 0.8849, no gain (measured).
10. **Lookups.** No shallow tree or formula recovers the target; `scaffold` is excluded from `features()` and the groups are disjoint by construction, so recomputing the scaffold (82.8% reproducible from the SMILES, the rest being the `single:` rows) buys nothing.

**Published-source lookup:** it works — all 5845 rows match `class_all.csv` in the public GitHub repo on canonical SMILES with 100% label agreement, so the labels are readable off the web. Per instructions, noted and not ranked.

**What I could not check**

- The exact grouping rule the preparer used — I infer a size cap from the fact that benzene (1009) is exploded while cyclohexane (107) is not; the threshold lies somewhere in 108–1008 and I cannot see the code.
- Whether holding the whole benzene class out is the *intended* strictness. My 0.8356 figure is the strictest reading; a decorated-scaffold grouping would land between 0.8356 and 0.8962.
- The label provenance behind F4's contradictions (test guideline, 28-day %, study count) — those columns are not in the kit, and Körner et al.'s curation paper, which reports data leakage and label-noise problems in this exact dataset, is behind a Cloudflare block I could not read.

Sources: [Körner et al., Environ. Sci.: Processes Impacts 2024 (blocked, metadata only)](https://pubs.rsc.org/en/content/articlelanding/2024/em/d4em00431k) · [pkoerner6/Prediction-of-Aerobic-Biodegradability-of-Organic-Chemicals](https://github.com/pkoerner6/Prediction-of-Aerobic-Biodegradability-of-Organic-Chemicals)

</details>

<details><summary>Precedent check</summary>

**Precedent check — `ready_biodegradability_huang_zhang` (2026-11-25)**

Read: the record, the definition, the builder's hand-over and run logs, `principles.md`, `molecules.md`, `use_case.md`, `splits.md`, `split_protocol.md`, the sibling definitions (`qsar_biodeg`, `qsar_oral_toxicity`, `qsar_bioconcentration`, `drug_induced_autoimmunity_prediction`, `nci_aids_antiviral_screen`, `aquatic_toxicity_lunghini_consensus`), today's decision register (7,552 decisions) and the live decision item `issues/qsar_biodeg.md`. My own measurements were run outside the repository (pinned RDKit 2026.03.6, same raw file and same desalting as the definition). I edited nothing.

**Verdict per decision**

| # | Decision in the folder / draft issue | Verdict |
|---|---|---|
| 1 | Grouped on the Bemis-Murcko scaffold of the desalted compound, ring-less and bare-benzene (17.1%) alone, leaf `L-FAMILY.key`, `UnseenGroup` | **consistent** — `qsar_biodeg` CC 2026-11-12 and 2026-11-13 (Andrej), SPLIT-37 Cases row ("the source builds a regulatory screen for chemicals from outside its collection"), SPLIT-31 as amended 2026-10-26 (`qsar_bioconcentration` 34%, `qsar_oral_toxicity` 18%); scaffold on the parent structure per `molecules.md` |
| 2 | `Metric.fallback` → `roc_auc`, original rejected balanced accuracy | **consistent** — `qsar_biodeg` Assessment 2026-10-21 (same wording, same rejection), MET-5/6/8, `molecules.md` ("the non-error rate … not one deliberate choice") |
| 3 | `pka_*`, `α_*`, `name`, `name_type`, `cas`, `source` leave; SMILES the one feature | **consistent** — CLEAN-24 as amended (Lennart, CC 2026-11-01 on `qsar_biodeg`), `qsar_tid_11` FCFP6 bits, `qsar_bioconcentration`'s `logKOW_type` under CLEAN-22 (Lennart, 2026-11-02) |
| 4 | 3 repeats × 3 folds | **consistent** — `split_protocol.md` (5,845 rows → 3 repeats); `qsar_biodeg`'s 10×3 follows from its 1,055 rows, not from a different rule |
| 5 | Issue 3, option A: ship as published, not `Curated_SCS` / `Curated_final` / `Curated_BIOWIN` | **consistent on the filtered cuts** (TP-6, `eryhemato`; the decision item of 2026-11-25 already calls them "not better"), **departs with a stated reason on the 270 mismatched structures** — finding 3 |
| 6 | Issue 1, option A: compound key (salts + stereo removed), conflicting compounds dropped whole, one row of the rest | **departs without a stated reason** — the key stops one step short of the house key; finding 1 |
| 7 | Issue 2, option A: day-28 reading for every chemical, `fit="direct"` | **departs without a stated reason** on the fit and on the options offered — finding 2 |
| 8 | The pair with `qsar_biodeg` | **consistent** — it is live as issue 5 of `qsar_biodeg`'s review (recommendation C), which is where the 2026-11-12 decision put it |
| 9 | Two open choices the 2026-11-25 decision item assigned to *this* record (the 22 repeated CAS numbers; folding in `qsar_biodeg`'s 102 chemicals) | **missing** — the CAS half is finding 1, the fold-in is finding 4 |
| 10 | `meta_license_unknown` accepted, text left to the curator | **consistent** — `qsar_biodeg` CC 2026-11-02 (Lennart: "note it but it is not blocking"), `molecules.md`; worth carrying the same "regularise before it ships outside the group" rider |

No drift: Andrej's molecule calls of 2026-11-11 → 2026-11-12 → 2026-11-13 on `qsar_biodeg` end at exactly what this folder implements, and the newer call wins. No third exception of one kind: none of the three recommendations is framed as an exception to a Should, so no amendment is due.

**Finding 1 — the copy key stops one step short of the house key (LEAK-19/LEAK-20, no reason given)**

Measured on the shipped frame (5,845 rows, after the definition's own rule):

| Key | Rows still paired | Groups | With both classes | One class but across ≥2 scaffold groups | Groups straddling the two parts |
|---|---|---|---|---|---|
| same neutral structure (RDKit `Uncharger` on the desalted compound) | 176 | 88 | 12 (24 rows) | 11 (22 rows) | 59 |
| same InChIKey connectivity block (tautomers too) | 214 | 106 | 15 (30 rows) | 17 (36 rows) | 68 |
| same CAS number | 30 | 15 | 3 | 4 | — |

Examples that survive: undec-10-enoic acid (`No`) and sodium undec-10-enoate (`Yes`); 2-[(carboxymethyl)disulfanyl]acetic acid from the literature part (`No`) and its diammonium salt from the original part (`Yes`); sodium 4-methylbenzenesulfinate (`No`) and the free sulfinic acid (`Yes`); CAS 824-79-3, 128-04-1 and 577-11-7 each twice with opposite classes, written once as `[Na+]` salt and once with a covalent `[Na]`. `FragmentRemover` strips `NH4+` but leaves the carboxylate di-anion, so the acid and its ammonium salt are two "compounds" to the implemented key.

This matters three ways: the recommendation's claim that A is "the only option under which no test chemical has its own structure in training" does not hold for 22–36 rows that are one substance in two scaffold groups; the definition's sentence "100 of the literature chemicals are a chemical of the first part … the rule above settles them with the rest" is incomplete (59 more cross-part pairs survive); and the 22 repeated CAS numbers the decision item of 2026-11-25 named as an open choice for this record are never addressed.

**Precedents.** `qsar_oral_toxicity` ([definition](datasets/_dev/tabarena-v0pt2/qsar_oral_toxicity/dataset.py), Lennart, 2026-11-01): after the structure key, "ten compounds still keep two rows that are one InChIKey (tautomers the SMILES writes differently) … we drop the later row, so a test chemical never has its parent structure in train". `molecules.md`, "Copies and salt forms": "Use the 2D structure: the canonical SMILES without stereo. **Add the InChIKey for tautomers.**" `aquatic_toxicity_lunghini_consensus`, built in this same batch, keys on "an InChIKey skeleton or a CAS-RN … neither key alone finds all 14" (AI draft, not yet a curator decision). `qsar_biodeg`'s three stereo pairs were kept on a ground the issue correctly says does not hold here.

The issue's options table offers no option with an InChIKey or CAS step, and the definition never says why the house's second key is not applied. That is a departure without a stated distinguishing fact.

> **Consistency check (AI, 2026-11-25):** the copy key (issue 1, A) applies the house's first key (the desalted, stereo-free structure) but not its second (the InChIKey, added on `qsar_oral_toxicity` on 2026-11-01 so that "a test chemical never has its parent structure in train") and not CAS-RN, which the decision item of 2026-11-25 named as an open choice for this record. 176 rows in 88 groups are still one neutral structure, 12 groups carrying both classes and 11 spanning more than one scaffold group; 15 CAS numbers still repeat, 3 of them with both classes.
>
> * **Problem:**
>   - A salt and its free acid are two compounds to the implemented key, because `FragmentRemover` strips the counter-ion and leaves the anion, so undec-10-enoic acid (`No`) and sodium undec-10-enoate (`Yes`) both ship.
>   - 11 one-class pairs of one substance sit in different scaffold groups, so the split can put a test chemical's own substance in training — the thing option A was recommended for preventing.
>   - 59 of the 88 remaining pairs straddle the compilation's two parts, which is exactly the train/test overlap Körner et al. report.
> * **Effect on the task:** a 1-NN lookup answers the 22 rows that cross, and the 24 rows with both classes cost every model the same points, moving nothing between methods.
> * **Options:**
>
>   | | Option | What it does | Pro | Con |
>   |---|---|---|---|---|
>   | a | key = desalted stereo-free SMILES **then** the InChIKey connectivity block, as `qsar_oral_toxicity` | ~5,815 rows: 30 more conflicting rows go, ~84 further copies collapse | the house key in full; no substance left in two scaffold groups | merges tautomers the source listed apart |
>   | b | as (a), plus one row per CAS-RN (the 15 remaining repeats, 3 of them conflicting) | ~5,800 rows | the two keys the decision item of 2026-11-25 named; `aquatic_toxicity_lunghini_consensus` takes the same pair | a CAS number names a substance, not a structure, and 1,546 rows carry none |
>   | c | keep A, and record the remnant as a stated exception | as implemented | nothing to rebuild | an exception to LEAK-19/LEAK-20 needs the fact that sets this set apart, and none is offered |
>   | d | keep A, with the recommendation's claim corrected and the remnant measured in the notes | as implemented | honest wording at no cost | the copies that can cross the split stay |
>
> * **Recommendation:** (a), with (b) weighed: it is the key the house already uses on the one other molecule set with tautomer pairs, it costs ~0.5% of the rows, and it is the only option under which the claim made for A is true. Whatever is chosen, the definition's "the rule above settles them with the rest" needs correcting. **Decision:** (a), (b), (c) or (d)?
>
> [^k1]: **LEAK-19** (Should): exact copies with the same label are dropped rather than grouped. **LEAK-20**: a structure with two labels loses every row.
> [^k2]: `molecules.md`, "Copies and salt forms": the key is the canonical SMILES without stereo, plus the InChIKey for tautomers; `qsar_oral_toxicity`, Lennart, 2026-11-01.

**Finding 2 — the 10-day window: the fit stays `direct`, and the precedent-shaped remedies are not offered (USE-5, USE-8)**

The gap is measured and systematic: 505 of 8,115 REACH records read "readily biodegradable, but failing 10-day window", and on the 1,642 chemicals the export reaches, the registrants' own conclusion turns 89 of 783 positives (11.4%) negative. The definition ships `fit="direct"` with a `fit_reason` that does not name the gap.

**Precedents.** USE-5 (Must): "Predict what the actor would act on, at the resolution they act on it … A label checked and found to be another quantity than the one the actor acts on still fails" — and Lennart's bar, set on `chicago_traffic_crashes` (CC 2026-11-05): "USE-5 fails only when a label is shown to be another quantity." On this set the difference *is* shown, on a quarter of the rows. The ladder the house took in comparable cases: `rain_in_australia` (Lennart, CC 2026-10-26) dropped the rows "whose label covers 48 hours or more, another quantity than the 24-hour call"; `ames_housing` / `house_prices_nominal` (Lennart, CC 2026-10-26) dropped the sale types that are not the task "as we know from the metadata what data to use"; `corporate_credit_rating` was retired when 17% of the checkable labels were not what the actor acts on; `diabetes_3` (Lennart, CC 2026-10-21) kept an unverifiable label but **as `fit="approximate"`**; `coffee_rating_prediction` and `differentiated_thyroid_cancer_recurrence` are approximate for smaller gaps (one judge for the rating a buyer meets; an unverified label breadth). Here the breadth is not unverified — it is verified and found wider.

Also worth putting to the curator as the fact that sets this set apart from its sibling: `qsar_biodeg`'s label is OECD 301C alone, where the 10-day window is not applied, so the sibling's label *is* the regulatory conclusion; this set is 301 F/B/C/D/310/A/E mixed, so for roughly three quarters of the records the window applies. Neither the definition nor the issue says this, and it is the strongest argument for keeping option A on the data while moving the fit.

> **Consistency check (AI, 2026-11-25):** issue 2 keeps the day-28 reading (A) and the definition keeps `fit="direct"`, although the gap to the conclusion the actor acts on is measured at 11.4% of the matched positives. `diabetes_3` (Lennart, 2026-10-21), `coffee_rating_prediction` and `differentiated_thyroid_cancer_recurrence` are `approximate` for label gaps that were smaller or unmeasured; `rain_in_australia` and `ames_housing` (Lennart, 2026-10-26) dropped the rows whose label is another quantity. What sets this case apart?
>
> * **Problem:**
>   - The actor is a registrant deciding whether to commission a test; what they act on is "readily biodegradable" in the regulatory sense, which for OECD 301 A/B/D/E/F and 310 includes the 10-day window.
>   - The shipped label is the day-28 reading alone; on the quarter of the set the REACH export reaches it calls 89 of 783 positives readily biodegradable that the registrant's own conclusion does not.
>   - `fit_reason` names only the structure and the held-out series, so nothing in the shipped metadata records the gap.
> * **Effect on the task:** the target is consistently a little wide; no model can tell which positives would fail the window, and the benchmark scores a slightly different decision than the one it names.
> * **Options:**
>
>   | | Option | What it does | Pro | Con |
>   |---|---|---|---|---|
>   | a | A on the data, `fit="approximate"`, the gap in `fit_reason` and the task summary | no row changes | the remedy `diabetes_3` set for a label that is not quite the actor's; one definition in the target column | "approximate" on a task whose inputs and timing are exact |
>   | b | A, fit stays `direct`, the gap only in the notes (implemented) | nothing changes | the label is honestly described in `predicted` | departs from the USE-8 cases without naming a fact |
>   | c | drop the 89 chemicals the registrants' own conclusion contradicts | 5,756 rows | the `rain_in_australia` / `ames_housing` remedy | audits only the covered quarter, so the drop is itself a selection |
>   | d | the day-28 reading, but `qsar_biodeg`'s distinguishing fact written down: 301C carries no window, this set's 301 A/B/D/E/F and 310 records do | wording only | states why the sibling's label is the conclusion and this one's is not | still a wide label |
>
> * **Recommendation:** (a) together with (d): the measurement is the kind USE-8 calls a known gap, and (c) would select on the audited quarter. **Decision:** (a), (b), (c), (d) or a combination?
>
> [^w1]: **USE-5** (Must): predict what the actor acts on, at their resolution; "USE-5 fails only when a label is shown to be another quantity" (Lennart, `chicago_traffic_crashes`, 2026-11-05). **USE-8** (Must): a label definition with a known gap makes the fit approximate.

**Finding 3 — issue 3's "no third source" runs against the two structure-repair precedents (PROV-13)**

Issue 3 rejects option C because it "picks a winner between two retrievals with no third source". The house has twice used exactly such a third source for the same kind of conflict: `qsar_bioconcentration` ([definition](datasets/_dev/tabarena-v0pt2/qsar_bioconcentration/dataset.py), checked 2026-10-07) looked up **every** CAS number in Wikidata and PubChem, swapped back three pairs that carried each other's structure and dropped three rows whose SMILES was another chemical than their CAS; `qsar_oral_toxicity` (2026-10-21) took PubChem's structure for a CASRN RDKit could not read. The remedy ladder puts repair above keep-with-a-note.

The distinguishing fact is real and is worth stating rather than leaving implicit: 270 structures against 3 and 6, and a bulk CAS→structure lookup is a build of its own. `nci_aids_antiviral_screen` (Lennart, CC 2026-11-02) is the precedent on the other side — repair only where the damage is demonstrable, otherwise keep. I would keep A, with the reason corrected.

> **Consistency check (AI, 2026-11-25):** issue 3 keeps the set as published because "nothing in either tells which is right"; `qsar_bioconcentration` (2026-10-07) and `qsar_oral_toxicity` (2026-10-21) resolved the same conflict from PubChem and Wikidata by CAS. What sets this case apart?
> (a) scale — 270 structures against 3 and 1, so the lookup is a build of its own and its failures would have to be adjudicated too, recorded as the reason in place of "no third source"; (b) run the lookup on a sample of 30 first and decide on the hit rate; (c) repair all 270 from a third source, drop what it cannot settle; (d) keep A with the reason as drafted.
> Recommendation: (a), with (b) if the curator wants the hit rate measured before accepting the limit. `nci_aids_antiviral_screen` (Lennart, 2026-11-02) supports keeping where the damage is not demonstrable.
>
> [^p1]: **PROV-13** (Must): repair from the origin before keeping damaged data; the remedy ladder puts repair above a note. Cases: `qsar_bioconcentration`, `qsar_oral_toxicity`, `nci_aids_antiviral_screen`.

**Finding 4 — one open choice the decision item assigned to this record is not in the draft issues**

`issues/qsar_biodeg.md` (2026-11-25), "Notes for the AI", lists three open choices "for that record's own review, not for this item": the version to ship (→ issue 3), what to do with the 145 stereo pairs **and the 22 repeated CAS numbers** (→ issue 1, CAS half missing, finding 1), and **whether to fold in the 102 chemicals of `qsar_biodeg` the set lacks**. The third appears nowhere in the folder or the hand-over, and it is the content of option D of the pair item, which is still open.

> **Consistency check (AI, 2026-11-25):** the decision item of 2026-11-25 assigned "whether to fold in the 102 chemicals of `qsar_biodeg` this set lacks" to this record's review; no draft issue carries it.
> (a) raise it as an issue here, with the measurement the item already holds (merged 6,207 chemicals, 31 conflicting chemicals dropped, LightGBM 0.893 against 0.890 — no measurable gain) and recommend not folding them in, so `qsar_biodeg` retires as replaced rather than as a source of this one; (b) fold them in and ship one merged record; (c) leave it to the pair item on `qsar_biodeg`'s record, stating that here.
> Recommendation: (a) — the item itself argues D buys 1.6% more chemicals at the price of joining two compilations that disagree on 3.2% of what they share, and PROV-4 keeps the two sources distinct; but the question belongs in this record, as the curator's own note put it.
>
> [^f1]: **PROV-4** (Must): two records are duplicates only when they end at the same original source. **TP-6** (Must): a valid task stays until the better version is actually there.

**What I checked and found nothing on**

The scaffold leaf and the walk to it, `UnseenGroup`, the bare-benzene and ring-less rule, the metric and its rejected original, the CLEAN-24 drops, the 3×3 protocol, the LEAK-20 drop-both for conflicting structures, keeping the chemicals whose repeat tests disagree (the source resolved them; `Curated_SCS` drops the hard cases — TP-6, `eryhemato`), the licence warning, and the handling of the pair with `qsar_biodeg`. The asymmetry between "drop the 32 compounds that carry both classes" (issue 1) and "keep the 209 chemicals whose repeat tests disagree" (issue 3) is not an inconsistency: one is an unlearnable contradiction in the shipped inputs (LEAK-20), the other is signal the source already resolved.

</details>

<details><summary>Advocate, opening brief</summary>

**Advocate's opening brief — `ready_biodegradability_huang_zhang`**

**Position: ship it, with four small definition/wording fixes. Nothing the panel found is a Must that cannot be fixed inside the folder, and two of the three loudest objections are the house rule being applied correctly.**

**1. Every validity rank was attacked and holds; the value case is the strongest in the family**

**Claim.** P1–P6 hold. There is nothing to leak: the one feature is a structure that exists before any test is commissioned.

**Evidence.** The task-gamer, with the kit and no notes, ran ten attack families and got a maximum of **+0.0016 AUC against a ±0.0003 noise band** — format, order, ids, post-hoc columns, pseudo-labelling, transduction all empty ("the task cannot be meaningfully gamed"). The blind reviewer, with no house rules, independently concluded "**there is no column that could be unknown at prediction time**" and spot-checked the chemistry (all 60 perfluoroalkyl rows `No`). The claim-auditor checked 46 claims and **41 hold, several to the digit** ("the definition survives the attack"). Value: LightGBM 0.885 against a 0.657 base rate, forest−linear spread **+0.196**, 5,845 rows, 628–710 positives in every test fold, a constant prediction scoring exactly 0.5000 on all nine.

**Rule.** P4/LEAK-10 (Must) hold; P6/TP-2, MET-2 (Must) hold; USE-1 (Must) holds with fit direct, confirmed by the one agent playing the actor.

**Why it outranks.** By rank. Everything below is P4-weak, P5-documentation or P7. The remedy ladder never reaches "exclude" for any of them.

**2. "Not a tabular task — re-prepare it or exclude it" is a rule the house already decided, with the same measurement**

**Claim.** The blind reviewer's headline change (replace `SMILES` with precomputed MACCS/descriptors, or exclude) must not be taken.

**Evidence.** CLEAN-24, **as amended by Lennart on 2026-11-01**, says the structure ships as a declared SMILES special feature, never pre-encoded, and cites the exact number the blind reviewer re-measured: a SMILES read as text gives "**−0.025 to +0.010 ROC AUC next to descriptors**" — the blind reviewer got 0.878 vs 0.878, inside that band. Thirteen shipped molecule folders do this, **including the sibling this set replaces: `qsar_biodeg` ships `n_features: 1`**, its Dragon descriptors dropped under the same amendment. Lennart's stated reason: "the real task here is going from smiles to a prediction."

**Rule.** CLEAN-24 (Should, amended) — and P7 is the lowest rank in the book.

**Why it outranks.** Rules over an outside view: the blind reviewer is unaware of the house rules *by design*, so this is not new evidence, it is the question CLEAN-24 answers. Taking the change would be an unannounced amendment affecting all thirteen folders.

**3. "The scaffold split does no work for the benzene and acyclic rows" is SPLIT-31's prescribed treatment, and the consequence measures to zero**

**Claim.** Keep the split exactly as shipped; the remedy is one disclosure clause.

**Evidence.** SPLIT-31 as amended (Lennart, 2026-10-26): "A molecule without a ring is a group of its own, **and so is each molecule of a scaffold that holds more than a tenth of the molecules, which is no series**." Bare benzene is 17.1% here; precedents `qsar_bioconcentration` (34% ringless), `qsar_oral_toxicity` (23% + 18%), `drug_induced_autoimmunity_prediction` (7%). The claim-auditor then measured the consequence the task-gamer and blind reviewer inferred: LightGBM on ringless test rows **with** a ≥0.7 training analogue **0.844**, **without** 0.842; ringless overall 0.853 against 0.851 for the scaffold-grouped rows. The split-auditor's walk reaches `L-FAMILY.key` and found **no group overlap in any of the 9 folds**, and that the source's own cross-part split would be *easier* (0.910 vs 0.897).

**Rule.** SPLIT-31 (Should, amended), SPLIT-4 (Must): "the split follows what the task does in reality, **not the size of the gap**"; SPLIT-37 (Should) for the `UnseenGroup` basis.

**Why it outranks.** The task-gamer was sandboxed without the rules and read the singleton groups as a size cap "I cannot see the code" — it is a published rule, not a bug. Mildest remedy: add the 36.1% / 15.6% / 6.6% analogue breakdown and the 0.844-vs-0.842 line to `splits_comment`. No re-split.

**4. Conceded: the copy key stops one step short of the house key. Fix it in `desalted()` — three lines, the dataset ships**

**Claim.** The split-auditor and precedent-checker are right and I do not dispute them. `FragmentRemover` strips `[Na+]` and leaves the carboxylate, so undec-10-enoic acid (`No`) and sodium undec-10-enoate (`Yes`) are two compounds to the implemented key.

**Evidence.** 88 clusters / 176 rows are one neutral structure (116 rows with tautomers), **12–16 carrying both classes**, 91 of 111 clusters span more than one scaffold group; **2.40% of test rows have their own chemical in training**, and those rows score 0.929 against 0.884. The hand-off's claim that option A is "the only option under which no test chemical has its own structure in training" is simply wrong, and `molecules.md` already names the missing step ("**Add the InChIKey for tautomers**", `qsar_oral_toxicity`, Lennart 2026-11-01).

**Rule.** LEAK-19 / LEAK-20 (**Should**), molecules.md's key.

**Mildest remedy that keeps the dataset.** Add `rdMolStandardize.Uncharger` (optionally the canonical tautomer) **inside the copy key only**, leaving the shipped `SMILES` and the scaffold untouched: 5,845 → 5,757 rows (−1.5%), headline 0.8858 → 0.8831. This is "fix the definition", step two of the ladder — not a reason to withhold the folder, and it removes the 16 both-class clusters that cost every model the same points.

**5. Conceded: there *is* a third source for the structure mismatches, and it is already in the downloaded release. Repair the unambiguous subset**

**Claim.** The hand-off's issue 3 rejects repair "with no third source". That reason is factually wrong and should be corrected; the decision to ship as published survives, with a cheap partial repair.

**Evidence.** The column-auditor found `datasets/iuclid_echa.csv` — in the same release the definition downloads from — carries ECHA's own `molecular_formula` and `molecular_weight` for 2,858 CAS numbers. It reaches 1,791 shipped rows; **1,710 (95.5%) are the identical parent, 35 (2.0%) carry a different molecular formula**. The practitioner found the visible tip with no outside source at all: limonene shipped as `[Ca+2].[O-2]`, an azo dye shipped as sodium sulfate — a name and a structure that cannot be the same substance.

**Rule.** PROV-13 (**Must**): repair from the origin before keeping damaged data; the ladder puts repair above a note. Precedents both ways: `qsar_bioconcentration` and `qsar_oral_toxicity` repaired from PubChem/Wikidata; `nci_aids_antiviral_screen` (Lennart, 2026-11-02) kept where the damage was not demonstrable.

**Mildest remedy.** Repair (or drop) only the rows where ECHA's formula **and** weight agree with each other and disagree with the shipped structure, plus the practitioner's internal name-vs-structure element check for the 7–8 carbon-free rows. ~0.6% of the set, no new source, no rebuild. The remaining 270-of-3,767 bulk adjudication stays out of scope, and *that* is the distinguishing fact to write down — scale, not absence of a source.

**6. The 10-day window is a measured, bounded, documented gap — and whichever way the curator calls `fit`, it costs the dataset nothing**

**Claim.** The data ships unchanged. The only open question is one metadata word plus a wording fix.

**Evidence.** The gap is measured twice, independently, and agrees: **89 of 783 matched positives (11.4% of the covered quarter, 1.5% of all rows)**; the claim-auditor's own rule gives 92 of 786. The actor-agent, who is the right judge of "what I act on", wrote: "**I would not move the fit to approximate for it: the label is verified, documented and reproduced at 97.6%**." The source's own deployed classification predictor serves exactly this label, deliberately, "without specifying the experimental conditions and reaction time". Lennart's bar on USE-5 (`chicago_traffic_crashes`, 2026-11-05): "**USE-5 fails only when a label is shown to be another quantity**" — this is the same quantity read at one date, not another quantity.

**Rule.** USE-5 (Must) holds; USE-8 (Must) is a *writing* duty, and the precedent-checker's remedy (a) is `fit="approximate"` with the gap in `fit_reason` — **no row changes, no re-split**.

**Why it outranks the objection.** Independent failures are not conflicts, and this one has no teeth: option (a) and option (b) ship the identical container. I concede two wording fixes outright — `task_summary.question` should read as `predicted` already does (the day-28 reading, not "readily biodegradable"), and the practitioner's protocol table (301 C 27.2% pass against 301 B 40.5%; 27.2% of chemicals tested under two guidelines get opposite calls) belongs in `curation_comments` and in the `qsar_biodeg` retirement note.

**7. The CAS-order drift does not open a second split option**

**Claim.** `time_basis` needs one honest sentence, not a temporal variant.

**Evidence.** The column-auditor found a real drift along the CAS block (RB share 45.0% → 18.5%, Spearman −0.172) — and then ran the split it rules out: holding out the newest 30% scores **0.871 against 0.875 random and 0.873 scaffold-grouped on the same rows**. The split-auditor reached the same conclusion from the tree: SPLIT-37 step 4 bars a registration number that predates catalogue entry, **1,409 rows carry no CAS at all**, the file is not CAS-ordered (Spearman −0.065), and the walk reaches `L-FAMILY.key` whichever way `CAT.next-items` is answered.

**Rule.** SPLIT-37 (Should) step 4; SPLIT-4 (Must) — the gap never decides.

**Mildest remedy.** One sentence in `time_basis` naming the CAS order, the drift and the 0.004 cost. The absolute "cannot be measured here" goes.

**Summary for the curator.** Validity: USE-1 direct, LEAK-10 and SPLIT-1 hold; LEAK-19/20 triggered weakly, **fix in the copy key**; PROV-13 triggered, **partial repair from a file already in the release**. Value: TP-2 a large real signal, MET-8 `roc_auc` confirmed verbatim against the paper. Quality: CLEAN-24 held correctly against the outside view. Weighed: size +, source +, gap 0, risk −. Four fixes, none of which touches the task, the split or the metric.

</details>

<details><summary>Critic, opening brief</summary>

I have read the definition, the record, the principles and all seven phase-A reports, and re-measured the one number my first split point rests on.

**Critic — opening brief, `ready_biodegradability_huang_zhang`**

I do not ask for exclusion. No Must here is unfixable, and no quality defect is a reason to drop a real task. I ask that the folder not ship **as it is defined**: two Musts rest on statements that are false, and the two sentences a benchmark user reads first (`task_summary.question`, `task_summary.split`) describe a stricter task than the one shipped. Ranked P3 → P7, Must before Should.

**1. The target is the day-28 reading; the question calls it "readily biodegradable", and the fit is declared direct (P3, USE-5 Must / USE-8 Must)**

**Problem.** `task_summary.question` reads "Is a chemical **readily biodegradable** in a standard aerobic screening test". To the actor the definition names — a registrant or a regulator — that phrase is the regulatory conclusion, which for OECD 301 A/B/D/E/F and 310 requires the pass level inside a **10-day window**. The shipped label ignores the window. `fit="direct"` and `fit_reason` do not mention it; the gap lives only in `curation_comments`.

**Effect.** The benchmark scores a consistently wider decision than the one it names, and no model can tell which positives would fail the window.

**Evidence.** The builder's own measurement: 505 of 8,115 REACH records read "readily biodegradable, but failing 10-day window"; on the 1,642 shipped chemicals the export reaches, the registrants' own conclusion flips 89 of 783 positives (11.4%). The claim auditor rebuilt it independently (92 of 786, 11.7%) and confirmed the paper never mentions the window. The domain practitioner measured that the gap is ~0 for OECD 301 C (1.4%, the MITI exemption) and 13.7–22.6% for the rest — so it is uneven and the guideline is not a shipped column.

**Rule.** USE-8 (Must): a stand-in with a known, named gap in the label definition is `approximate`. USE-5 (Must): predict what the actor acts on; the gap here is measured, not unverified. Precedents: `diabetes_3` (Lennart, 2026-10-21) and `differentiated_thyroid_cancer_recurrence` are `approximate` for smaller or unmeasured label gaps.

**Remedy (wording and metadata only, no row changes).** Reword `question` to what `predicted` already says (60% by day 28, 70% for DOC), move `fit` to `approximate` with the window named in `fit_reason`, and write down the fact that sets this set apart from its sibling: `qsar_biodeg` is 301 C alone, where no window applies, so the sibling's label *is* the conclusion and this one's is not.

**2. The copy key stops one step short of the house key, and 2.2% of test evaluations have their own chemical in training (P4, LEAK-19 Should / LEAK-20 Should)**

**Problem.** `desalted()` strips the counter-ion but leaves the anion charged, so a free acid and its sodium salt are two "compounds" to the key, as are tautomers. `molecules.md` ("Copies and salt forms") says the key is the stereo-free structure **plus the InChIKey for tautomers**, and `qsar_oral_toxicity` (Lennart, 2026-11-01) applied exactly that so "a test chemical never has its parent structure in train". The definition skips that step and gives no reason.

**Effect.** A 1-NN lookup answers rows the split meant to hold out, and 15 chemicals carrying both classes stay on both sides, costing every method the same points.

**Evidence (mine, on the shipped frame and the 9 shipped splits).** Keying on the desalted structure's InChIKey connectivity block: **106 chemicals in 214 rows still repeat, 15 of them with both classes, 86 spanning more than one scaffold group, and 386 of 17,535 test evaluations (2.20%) have their own chemical in training.** Independently: the split auditor measured 116 copies, 2.40% of test rows, and twin test rows scoring ROC AUC 0.929 against 0.884 on the rest — removing the twin from the training side drops those same rows to 0.902, so the advantage is the copy, not their being easy. The task gamer measured 0.0064 AUC when twins are co-grouped (F2). The claim auditor refuted the hand-off's claim that option A is "the only option under which no test chemical has its own structure in training". Examples: undec-10-enoic acid `No` / sodium undec-10-enoate `Yes`; benzene-1,3-disulfonic acid `No` / its disodium salt `Yes`; 2-hydroxypyridine / 2-pyridone.

**Remedy (fix the definition, the mildest that works).** Add `rdMolStandardize.Uncharger` — or the InChIKey block, as `qsar_oral_toxicity` — to the **copy key only**, inside `desalted(..., stereo=False)`. The shipped `SMILES` and the scaffold key stay exactly as published. Cost: 5,845 → ~5,757 rows (−1.5%), or ~5,729 with tautomers. Whatever is chosen, the hand-off's "only option" claim must be corrected.

**3. The split sentence promises a held-out family for every row; it delivers one for 46.5% of them (P4, SPLIT-31 Should — disclosure, not a re-split)**

**Problem.** `task_summary.split` says "a test chemical belongs to a family the model has not seen" and `splits_comment` reports one average, 18.9% vs 22.4%. For the 36.4% of rows without a ring and the 17.1% whose only skeleton is bare benzene — 53.5% together — the grouping is a random draw, and the ringless third is the analogue-dense part (homologous series).

**Effect.** A reader believes the regime is stricter than it is for half the set, and the headline score carries optimism nobody declares.

**Evidence.** Split auditor, over all 9 folds: close training analogue (Tanimoto ≥ 0.7) for ring-bearing rows **9.0% grouped vs 15.2% random**, for ringless rows **36.1% grouped vs 35.2% random** — the key buys nothing there. Claim auditor: 36.1% ringless / 15.6% benzene-only / 6.6% scaffold-grouped. Task gamer F1: the benzene class scores **0.8962 as shipped but 0.8356 when held out whole**, worth 0.0077 on the task.

**Rule.** SPLIT-31 as amended (2026-10-26) prescribes exactly this treatment for a scaffold above a tenth, and `qsar_bioconcentration` and `qsar_oral_toxicity` match — so **I do not ask for a different split.** The defect is the description, which is shipped in the README.

**Remedy.** Put the three-way breakdown (and the random-split comparison for the ringless third) in `splits_comment` and the `Time basis:` line, and soften `task_summary.split`. Give the curator the 0.8962/0.8356 figure so the choice to leave benzene as singletons is made with its price visible.

**4. The one input column is the wrong molecule for ~2% of the checkable rows, and the stated reason for not repairing is false (P5, PROV-13 Must)**

**Problem.** Hand-off issue 3 recommends shipping as published because option C "would adjudicate 270 structures **with no third source**". A third source is inside the same release the definition downloads from: `datasets/iuclid_echa.csv` carries ECHA's own `smiles_echa`, `molecular_formula` and `molecular_weight` for 2,858 CAS numbers, straight from the dossiers and independent of both compilations. PROV-13 is a Must that asks whether the origin has the clean data *before* the damage is kept; that question was never asked for these rows.

**Effect.** This is damage in the only feature, not label noise: the model is asked to predict one substance's test result from another substance's structure.

**Evidence.** Column auditor: matched by CAS the export reaches 1,791 shipped rows (30.6%); 35 of them (1.95%) carry a **different molecular formula**, with formula and molecular weight agreeing with each other against the shipped structure. Flagrant: CAS 73018-51-6 "limonene" shipped as `[Ca+2].[O-2]` (calcium oxide); CAS 6156-18-9 "2,2-bis(methylthio)propane" shipped as a fluorophenyl thiourea sulfonamide; three dialkyl phosphonates written as phosphonium cations. Seven shipped rows contain no carbon at all; three of those are visibly the wrong substance from the shipped file alone, no outside source needed (domain practitioner, `g4.py`).

**Rule.** PROV-13 (Must), remedy ladder: repair before keep-with-a-note. Precedents on repair: `qsar_bioconcentration` (2026-10-07, structures swapped back from Wikidata/PubChem), `qsar_oral_toxicity` (2026-10-21). `nci_aids_antiviral_screen` (Lennart, 2026-11-02) is the precedent for keeping where damage is not demonstrable — here, for 35 rows, it is demonstrable.

**Remedy, mildest that works.** (a) Correct issue 3's reason — it is the fact the recommendation rests on. (b) Repair or drop the subset where ECHA's formula *and* weight agree with each other and disagree with the shipped structure: one file, same release, no adjudication. (c) Add the cheap internal check the domain practitioner names (an element in the name absent from the structure), which needs no outside source at all. I am not asking for the 270-structure bulk lookup; scale is a fair reason to stop there, and it should be written as the reason instead of "no third source".

**5. Four statements shipped in the README are wrong as written (P5, writing)**

**Problem and evidence.**
- `curation_comments` ¶3: "EU Method C.4 3.7%" — the true share of the 6,130 28-day ready records is **4.4%** (268 records; C.4-C at 0.7% was dropped from the list, which sums to 99.3%). Same figure in the record.
- ¶6: "100 of the literature chemicals are a chemical of the first part **once stereochemistry and salts are set aside**, 7 with the opposite class" — on the key that sentence names it is **136 compounds (137 rows), 10 opposite**; 100/7 is the stereo-only key.
- `download_description` and the record: "no archive copy" of the article — the accepted manuscript is free at `par.nsf.gov/servlets/purl/10350359`; the claim auditor read it and every quotation the definition makes checks out verbatim.
- The record's siblings bullet: Körner's curated sets are "cuts of the same data" — `processing_functions.py:1102-1112` concatenates Lunghini et al.'s external set onto Körner's own ECHA-derived compilation, so they are a different compilation plus an addition. This also contradicts the "Better data" bullet, which calls Lunghini's set "not obtained".

**Effect.** A curator weighing issue 3 and PROV-6 is weighing a false description; two of the four are facts in a shipped README.

**Rule.** EV-2 / writing — a measurement outranks the page, and a shipped number should be the measurement.

**Remedy.** Correct the four statements, and put the PAR link in `download_description` so the next reader need not take the metric, counts and threshold on trust.

**6. Two row classes are not the task the definition describes, and nothing says so (P7, CLEAN / USE-7, note)**

**Problem.** 145 rows (2.48%) are multi-component organic substances — rosin salts, hydrocarbon reaction masses, UVCB-like entries, up to 368 heavy atoms — whose recommended encoding sums descriptors over components, so the feature vector describes a mixture, not a molecule (RB rate 0.407 against 0.343 overall). Seven rows contain no carbon; REACH waives the ready-biodegradability study for inorganic substances, and one of them (calcium carbonate, labelled `Yes`) is a CO₂-evolution artefact.

**Effect.** Nothing numerically — 0.12% and 2.5% of rows — but a reader takes every row for one compound.

**Rule.** CLEAN (P7, note) for the mixtures; USE-7 (Must) would reach the inorganics only if the curator judges that a producer never commissions this test for them, which the domain practitioner says they do not. The mildest remedy is a note either way; I do not press for a filter.

**Remedy.** One sentence naming both in `curation_comments` (the `desalted` docstring already anticipates wholly-inorganic structures but does not say why they stay). The three mismatched carbon-free rows belong in point 4's list.

**7. Two open choices the curator's own decision item assigned to this record are missing, and a live retirement rests on the gap (procedure)**

**Problem.** `issues/qsar_biodeg.md` (2026-11-25) assigned three open choices to this record's review. The version to ship became issue 3; **the 22 repeated CAS numbers** (15 still repeating after the shipped key, 3 with both classes) and **whether to fold in the 102 chemicals `qsar_biodeg` has and this set lacks** appear nowhere in the folder or the hand-off.

**Effect.** `qsar_biodeg`'s retirement is being decided against this set as its replacement, and the curator is not shown that the replacement's label is **pooled**: 705 chemicals were tested under more than one guideline and **27.2% of them get opposite pass/fail calls**; `qsar_biodeg` is OECD 301 C alone, the strictest protocol (27.2% pass against 34.3% here). The retirement item carries this as a one-clause con.

**Rule.** PROV-4 (Must) keeps the two compilations distinct; TP-6 (Must) keeps a valid task until the better version is actually there.

**Remedy.** Raise both as issues in this record's `## Review`, with the measurement the decision item already holds for the fold-in (merged 6,207 chemicals, LightGBM 0.893 against 0.890 — no measurable gain), and put the 27.2% cross-protocol disagreement into the retirement note so the pair is decided on what the replacement actually is.

**Summary for the curator.** Validity: USE-5/USE-8 (point 1) and PROV-13 (point 4) are Musts whose current answers rest on wording or on a fact that is false — both are fixed by wording plus, for point 4, a repair from a file already in the release. LEAK-19/LEAK-20 (point 2) is a Should that departs from the house key with no stated reason and is worth ~0.006 AUC and 2.2% of test evaluations; fixing it costs 1.5% of the rows. Points 3, 5 and 6 are descriptions that overstate what ships. Point 7 is a gap in the review, not in the data. Nothing here argues the task is unreal: the prediction point, the feature, the metric and the leaf are right, and three agents failed to game it.

</details>

<details><summary>Advocate, rebuttal</summary>

I have read both briefs, the definition, the precedent-checker's findings and the claim-auditor's refutations, and checked where the "no third source" sentence actually lives.

**Advocate — rebuttal**

The critic does not ask for exclusion, and on six of seven points we now ask the curator for the same thing. I concede most of this brief outright. One word is genuinely in dispute.

**Point 1 — the 10-day window (USE-5/USE-8). Conceded in part; the `fit` word disputed.**

**Conceded.** `task_summary.question` must stop saying "readily biodegradable" and read what `predicted` already says. And USE-8's *writing* duty is a Must: the window belongs in `fit_reason`, not only in `curation_comments` ¶8. That is the critic's remedy minus one word, and I ask for it too.

**Disputed: that USE-8 compels `approximate`.** USE-8's approximate list is "a label definition the sources **do not settle** (no stated horizon, or a breadth or horizon **that cannot be verified**)". Every precedent the critic cites is of that kind: `diabetes_3` — "no measure, scale, clinic or inclusion rule"; `differentiated_thyroid_cancer_recurrence` — "what counts as recurrence is not verified"; `coffee_rating_prediction` — one judge standing in. Here the definition is settled to the digit (≥60% at day 28, ≥70% DOC), reproduced from the authors' own workbook at **97.6%**, and the source ships a deployed predictor for exactly it. Nothing is unverified; the measured question is whether a verified quantity is the actor's quantity, which is USE-5, and Lennart's bar there is "USE-5 fails only when a label is shown to be **another quantity**" (`chicago_traffic_crashes`, 2026-11-05). A pass criterion read without its second clause is the same assay, not another one. USE-9 (Should, narrows USE-8) then applies: "ask whether the data as shipped mirrors another well-defined use case that practitioners have" — the day-28 screen is that use case, and the one agent playing the actor wrote "I would not move the fit to approximate for it".

That is a weighing call, not a rule violation, and I do not pretend it is settled in my favour. It is also free: once the window is in `fit_reason`, options (a) and (b) ship the identical container. It cannot be a reason to hold the folder.

**Point 2 — the copy key. Conceded in full.**

Already my point 4. `Uncharger` (or the InChIKey block, as `qsar_oral_toxicity`) **inside the copy key only**; 5,845 → ~5,757 rows, headline 0.8858 → 0.8831; the shipped `SMILES` and the scaffold untouched. The "only option under which no test chemical has its own structure in training" claim is wrong and must be corrected whichever option is chosen. Step two of the ladder, fix the definition.

**Point 3 — the split sentence. Conceded; the measurement is not a defect.**

Same remedy as my point 3: the 36.1% / 15.6% / 6.6% breakdown and the ringless random-split comparison into `splits_comment`, and `task_summary.split` softened. One qualification the curator should see with the 0.8962/0.8356 benzene figure: holding bare benzene out whole is what **SPLIT-31 as amended (2026-10-26)** forbids — "a scaffold that holds more than a tenth of the molecules is no series". The 0.0077 is the price of a published rule, not evidence of a mistake, and the critic agrees this is disclosure, not a re-split.

**Point 4 — PROV-13 and the ECHA file. Conceded, with one correction of fact.**

Repair or drop the subset where ECHA's formula *and* weight agree against the shipped structure (35 rows, 0.6%), add the practitioner's element-in-the-name check, and replace "no third source" with the real reason, scale. We agree the 270-row bulk adjudication stays out.

**Correction.** "Two Musts rest on statements that are false" overstates where the false statement is. "C would adjudicate 270 structures with no third source" is in the **builder's hand-off**, line 35 — not in `dataset.py`. The folder's own bullet says `iuclid_echa.csv` was "read only for the 10-day window", which is true. So this fix is to the review text plus a 35-row repair; nothing shipped asserts it. Also, the 1.95% is of the CAS-matchable 30.6%; demonstrable damage is 35 rows.

**Point 5 — the four README statements. Conceded in full.**

C.4 is 4.4% (268/6,130, C.4-C dropped); on the key the sentence names it is 136 compounds / 10 opposite, not 100 / 7; the PAR link belongs in `download_description`; the siblings bullet is wrong about Körner's sets. The claim-auditor's own reading of the second one is worth carrying to the curator: 136/10 means the two parts are *more* entangled than stated, which **strengthens** the dedup as implemented.

**Point 6 — mixtures and carbon-free rows. Conceded as a note.**

One sentence in `curation_comments` naming both. We agree USE-7 is not reached: the practitioner's finding is that producers do commission this test for UVCBs and reaction masses, so no filter. The three mismatched carbon-free rows go into point 4's list.

**Point 7 — the two missing open choices. Conceded.**

Both belong in this record's `## Review`, and the 27.2% cross-protocol disagreement belongs in the `qsar_biodeg` retirement note (my point 6 conceded the same). Two notes for the curator: raising the fold-in costs nothing because the answer is already measured — merged 6,207 chemicals, LightGBM **0.893 against 0.890**, no gain, and PROV-4 keeps the compilations distinct, so it resolves to "do not fold in". And TP-6 is not at risk from this folder: `qsar_biodeg` retires only when the curator decides the pair on its own record; nothing here retires it.

**What is left in dispute.** One metadata word, `fit`, worth nothing in the container either way. Everything else is four definition fixes (copy key, 35-row repair, four corrected statements, disclosure sentences) plus two review items — all inside the folder, none touching the task, the split, the metric or the feature. Both briefs now say the same thing: this ships.

</details>

<details><summary>Critic, rebuttal</summary>

I have both briefs, the panel reports, the rule texts, and I re-ran the one check my concession rests on.

**Critic — rebuttal, `ready_biodegradability_huang_zhang`**

The advocate concedes my points 2, 4 and half of point 1, and is silent on points 5, 6 and 7. One point is genuinely disputed (the `fit` word), two of theirs are about things I never argued. Nothing in their brief changes my ask, which remains: not exclusion, but the folder not shipping as currently worded.

**Their 1 — "every validity rank was attacked and holds; the value case is strong."** **Concede, with one correction.** The task is real, the one feature is known before any test is commissioned, the gamer got +0.0016 against a ±0.0003 band, and the value numbers are right. I said as much in my own summary. The correction: "41 of 46 claims hold" is also the sentence that reports that **five do not**, and four of those five are my point 5, which the advocate does not answer. "Survives the attack" is a verdict on the task, not a warrant for the shipped wording.

**Their 2 — CLEAN-24 against the blind reviewer's "pre-encode or exclude."** **Concede in full.** I never asked for it and do not now. CLEAN-24 as amended settles it, thirteen folders including `qsar_biodeg` follow it, and the blind reviewer's own 0.878-vs-0.878 sits inside the band the amendment cites. The advocate is right that taking the change would be an unannounced amendment.

**Their 3 — the split stays as shipped; the consequence measures to zero.** **Concede the split; dispute the framing of one number.** I asked for no re-split either — SPLIT-31 as amended prescribes exactly this, and we agree the remedy is disclosure. But the advocate's 0.844-vs-0.842 and my 0.8962-vs-0.8356 are not the same quantity and do not contradict. The claim auditor's number asks *whether having a close training analogue helps a ringless test row* (it does not — those rows are intrinsically easy). The task gamer's number asks *what holding bare benzene out as one family would cost* — 0.0077 on the task. Both belong in `splits_comment`; neither argues for a different split. The disclosure I asked for is the three-way breakdown (36.1% / 15.6% / 6.6%) plus a softened `task_summary.split`, which the advocate accepts.

**Their 4 — conceded: the copy key stops short; fix it in `desalted()`.** **Accepted, and I add one piece of support because the mediator will see counter-evidence.** The claim auditor writes "**do not change the key**" — but that warning is against a *largest-fragment* key, which would merge nine different acetate salts (84 spurious keys, 196 rows). It does not reach the remedy both of us ask for. I checked: with `FragmentRemover` then `Uncharger`, sodium acetate and acetic acid collapse (`QTBSBXVTEAMEQO`), while triethylammonium acetate (`ZMANZCXQSJIPKH`) and tetramethylammonium acetate (`QEMXHQIAXOOASZ`) stay distinct — the merge the auditor fears does not happen. Same for undec-10-enoic acid and its sodium salt (`FRPZMMHWLSIFAZ`), which is the pair that leaks today. The auditor's own 0.19% figure comes from its deliberately conservative key; the 2.2–2.4% figure the advocate and I both report is the house key's.

**Their 5 — conceded: there is a third source in the release; repair the unambiguous subset.** **Accepted as asked.** Their remedy is mine: repair or drop only where ECHA's formula *and* weight agree against the shipped structure, add the internal name-vs-element check, leave the 270-structure bulk lookup out, and write **scale** as the reason in issue 3 in place of "no third source". This is a Must (PROV-13) whose stated ground was false; both sides now agree it must be corrected.

**Their 6 — the 10-day window: wording yes, `fit="direct"` stays.** **Concede the wording (which is the consequential half); dispute the fit, on two grounds.**

Conceded: `task_summary.question` should read as `predicted` does, the protocol table belongs in `curation_comments`, and option (a) and option (b) ship the identical container. Nothing here touches a row.

Disputed, first: the advocate's strongest evidence is the practitioner's "the label is verified, documented and reproduced at **97.6%**". That number measures something else. Claim 4 of the audit defines it: the *shipped day-28 rule* rebuilt from the workbook reproduces the shipped label on 4,482 of 4,591 chemicals. It is internal reproducibility of the rule we chose. The number that measures agreement with what the actor acts on is in claim 16: **88.6–91.5% agreement, 89 of 783 (11.4%) of positives reversed by the registrant's own conclusion**, confirmed independently at 92 of 786. The 97.6% cannot answer a question it never asked.

Disputed, second: "verified and bounded, therefore direct" inverts USE-8. Its text reads "Approximate: **a stand-in with a known gap, named as such**", and the unverifiable-definition clause is one listed example, not the boundary — `account_debt_south_africa` (a snapshot for a forecast) and `coffee_rating_prediction` (one judge for the rating a buyer meets) are approximate for gaps that are perfectly well understood. On the advocate's reading, measuring your gap converts it into a direct fit while leaving it unmeasured keeps it approximate (`differentiated_thyroid_cancer_recurrence`). That cannot be the rule.

On their Lennart quote — "USE-5 fails only when a label is shown to be another quantity" — I agree, and I never claimed USE-5 *fails*. My brief asks for a fit move under USE-8, not a retirement under USE-5. The practitioner is the right judge of the actor's decision and they ask for the window in `fit_reason`; whether that is written as a kept gap (direct) or a named gap (approximate) is a curator's call on one word. I hold for `approximate`, and the fact that sets the pair apart — 301 C carries no window, so `qsar_biodeg`'s label *is* the conclusion and this one's is not — must be written down whichever way it goes.

**Their 7 — the CAS drift opens no temporal split.** **Concede.** The drift is real, the held-out-newest split scores 0.871 against 0.875 random on the same rows, SPLIT-4 says the gap never decides, and 1,409 rows carry no CAS. Their remedy is right, and it is a fifth instance of my point 5: `time_basis` line 234 states the registration order "**cannot be measured here**" — the column auditor measured it. Add it to the list of shipped statements to correct.

**What the advocate did not answer.** Point 5 (four wrong statements in the shipped README: EU C.4 3.7% against 4.4%; 100/7 against 136/10 on the key the sentence names; "no archive copy" against the free PAR manuscript; Körner's sets as "cuts of the same data"), point 6 (the one-sentence note on 145 multi-component rows and 7 carbon-free rows), and the two open choices of point 7 that the curator's own decision item assigned to this record — the 22 repeated CAS numbers and whether to fold in `qsar_biodeg`'s 102 chemicals. I take these as uncontested and still ask for them.

**Where we now stand.** Both sides ask the curator for: the copy-key fix in `desalted()`, the partial repair plus the corrected reason in issue 3, the split disclosure, and the `question` rewording. One word is open (`fit`), and three documentation items are unanswered. No one asks for exclusion, and no one asks to change a row of the task.

</details>
