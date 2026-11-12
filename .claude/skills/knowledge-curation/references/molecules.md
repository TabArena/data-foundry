# Molecule datasets (SMILES)

A guide for datasets whose rows are molecules: QSAR, toxicity, bioactivity, ADME and physico-chemical properties.
It adds no rules of its own. The rules live in their part files and are cited by ID here (CLEAN-24, SPLIT-31,
LEAK-16 to LEAK-20, PROV-6, USE-8, MET-5, MET-11). This file collects what a curator needs to know to apply them to
molecules: the background, the decisions taken so far, the pitfalls we hit, and the measured evidence. The last
section says where Data Foundry implements each part.

Read it when screening or adding a dataset with a SMILES, a structure file (SDF/MOL), molecule identifiers (CAS,
PubChem CID, ChEMBL ID, NSC, DTXSID), or descriptor or fingerprint columns computed from a structure.

## The background in brief

* **SMILES** writes a molecule's graph as a line of text. One molecule has many valid SMILES; every toolkit has its own
  canonical form (RDKit's, ChEMBL's and PubChem's differ). Compare structures only after canonicalising them with one
  toolkit.
* **Fragments.** A `.` separates disconnected parts: a salt's counter-ion, a solvent, a hydrate's water, a mixture, a
  metal complex. The parent compound is usually one of the fragments, but not always the largest (below).
* **Stereochemistry.** `@`/`@@` mark tetrahedral centres, `/` and `\` double-bond geometry. A 2D encoding ignores them,
  so stereoisomers look identical to it. Some sources carry stereo that means nothing. The NCI screen's structures were
  converted to 3D by Corina, and the stereo read back from those coordinates is arbitrary.
* **Tautomers** are one compound written as different SMILES. The standard InChI normalises many of them, so the
  InChIKey is the better key for "the same compound".
* **The InChIKey** is a 27-character hash in three blocks. The first block (14 characters) is the connectivity, the
  skeleton. The second covers stereo and isotopes, the last the protonation.
* **Identifiers.**
  * A CAS number names a substance, not a structure, and spreadsheets turn some CAS numbers into dates.
  * A ChEMBL ID is stable, but the structure behind it belongs to a release (ChEMBL 17 and today can differ).
  * NSC numbers are the NCI's, PubChem CIDs PubChem's, DTXSIDs the EPA's.
  * A row's identifier is the key to recover its structure from the release the data was drawn from.
* **Descriptors.** Numbers computed from the structure by a program: Dragon (commercial, cannot be recomputed without
  it), PaDEL, RDKit, Mordred. Their values depend on the program and its version.
* **Fingerprints.** Bit or count vectors of substructures. ECFP and FCFP are circular Morgan fingerprints (FCFP types
  atoms by function); MACCS keys are 166 predefined substructures. Hashing makes the bit positions specific to a
  program: RDKit cannot recompute Pipeline Pilot's FCFP6 bits (qsar_tid_11: no source bit matched exactly by any RDKit
  bit, at any position).
* **Calculated against measured properties.** MLOGP, ALOGP, XLogP and KOWWIN calculate logP from the structure; an
  experimental logKOW is measured. One column can mix both: qsar_bioconcentration's logKOW is a measurement for 652
  chemicals and a consensus prediction for 122, which the source paper states ("Experimental KOW values were obtained
  from VEGA log P dataset. If no experimental value was provided, a consensus KOW was predicted", Grisoni et al. 2015,
  Sec. 3.1, read 2026-11-01) and the decimals confirm (64% of the predicted values are exact thirds of three-decimal
  numbers, the mean of three predictions). Keep the mixed column when the actor of the use case would also reach for a
  prediction (USE-6), and say in the notes which rows are which. A per-row flag is not the place for it: it records
  how the source filled its table rather than a property of the molecule, so it leaves under CLEAN-22 and the
  provenance goes into the curation comments and a decision table, as qsar_bioconcentration's `logKOW_type` did on
  2026-11-02 (Lennart). Measure such a flag before trusting either story about it - that one scored macro ROC AUC
  0.534 against 0.5 for chance and nothing at all on top of the structure, which answers the leak question it was
  raised under.
* **The Bemis-Murcko scaffold** is the ring systems and the chains linking them, with side chains removed. A molecule
  without a ring has none.

## What ships (CLEAN-24)

The task is going from the structure to a prediction (Lennart, 2026-11-01). So:

* **The structure ships as a SMILES column** marked as a structure, never as plain text and never pre-encoded. The
  benchmark encodes it, as it encodes dates and text.
  * The recommended encoding is RDKit's 2D descriptors, the 166 MACCS keys and the ECFP4 counts. That is one pipeline
    choice to revisit; a feature selection step may follow it.
* **Columns the source computed from the structure leave**, whether a program could recompute them or not. They are
  one modelling choice of the authors.
  * Leaving so far: drug_induced_autoimmunity_prediction's RDKit descriptors, qsar_tid_11's FCFP6 bits,
    qsar_oral_toxicity's ECFP bits.
  * qsar_bioconcentration's 9 Dragon descriptors left for a leak (LEAK-31) before this rule.
* **What stays:**
  * measured properties (qsar_bioconcentration's logKOW);
  * facts that do not come from the structure (apistox's pesticide-type flags and first publication year).
* **The form of the SMILES:**
  * RDKit's canonical SMILES, every fragment kept.
  * Stereo kept, unless the source's stereo is meaningless (the NCI screen), and then removed with the reason in a note.
* **Recovering a structure:**
  * When the source ships only descriptors or fingerprints, recover the structures by the rows' identifiers from the
    release the data came from: ChEMBL 17 for qsar_tid_11, the authors' supporting information or workbook for
    qsar_biodeg, qsar_fish_toxicity and qsar_aquatic_toxicity. A UCI copy often leaves the structures out while the
    authors' own page or the paper's supporting information still has them.
  * Link row by row and prove the link, and keep the proof in the definition as an assertion: the same row count and
    order, every shared column identical, or a few simple descriptors recomputed with RDKit (atom counts, nitro
    groups). On all four datasets so far the authors' file was the shipped file plus the structures, row for row.
  * The authors' file can also be the better source: qsar_fish_toxicity's workbook carries the target at full
    precision, where the UCI copy rounds it to three decimals.
  * When no public release has the structures, the descriptors stay: bioresponse (Kaggle published anonymous, scaled
    descriptors and no identifiers) and clock_protein_toxicity (the 171 molecules carry internal codes, and their
    structures exist only as drawings in a Word figure).

## Copies and salt forms (LEAK-16, LEAK-19, LEAK-20)

* **The key is the structure.**
  * Use the 2D structure: the canonical SMILES without stereo.
  * Add the InChIKey for tautomers: qsar_oral_toxicity's 10 pairs that are one InChIKey but two SMILES.
  * Do not use a fingerprint or descriptor vector. It merges different chemicals: deduplicating qsar_oral_toxicity on
    its bit vectors had dropped 11 chemicals that only collided.
* **Salts are a decision of their own.**
  * The largest fragment is no salt stripper. On apistox it turns triclopyr and picloram triethylammonium into the same
    triethylamine; on the NCI screen it would merge different compounds in 56 groups (dicyclohexylamine salts of
    different acids).
  * A list of inorganic ions and solvents (RDKit's `FragmentRemover` defaults: halides, metal ions, water, sulfate,
    ammonia, mesylate) is safer for the key; organic counter-ions stay.
  * Keep the shipped SMILES whole. Use the stripped form only for the copy key and the scaffold.
* **One structure with two labels:** drop every row of it, as for drug_induced_autoimmunity_prediction's streptomycin,
  qsar_oral_toxicity's 20 structures and the NCI screen's 46. With one label, keep one row.
* **Stereoisomers with their own measured value** stay when the target is continuous and the values differ: qsar_tid_11
  keeps 474 rows in 217 groups, whose potency differs by up to 4.48 pXC50. The SMILES keeps the stereo; a 2D encoding
  cannot tell them apart, which the definition notes. They share a scaffold, so they never straddle the split.

## Splits (SPLIT-31)

* **Scaffold groups** are the default when the rows carry exact structures. A new compound under assessment usually
  comes from a series not measured yet.
  * A molecule without a ring is a group of its own, and so is each molecule of a scaffold holding more than a tenth of
    the set: the bare benzene ring, 34% of qsar_bioconcentration and 18% of qsar_oral_toxicity.
  * Compute the scaffold on the parent structure when counter-ions have rings.
* **Measure what the split changes:** the share of test compounds with a close training analog (Tanimoto at least 0.7,
  Morgan radius 2, 2,048 bits), under a random split and under the groups.

  | Dataset | Random split | Scaffold groups | Other |
  |---|---|---|---|
  | qsar_bioconcentration | 12.6% | 6.4% | |
  | qsar_oral_toxicity | 24.7% | 16.3% | untested chemicals: 11.0% |
  | qsar_tid_11 | 79.7% | 59.2% | |
  | nci_aids_antiviral_screen | 32.4% | 15.3% | |

  Scores drop by design: drug_induced_autoimmunity_prediction's TabPFN fell from 0.854 to 0.768 ROC AUC, and
  qsar_tid_11's LightGBM from 0.747 to 0.657 R^2. Under random splits a nearest-neighbour lookup with no model reached
  0.822 on drug_induced.
* **A source's time split can stand in.** apistox's decade windows give 10-24% close analogs, against 14-19% for
  scaffold groups and 17-30% at random, so it stays temporal.

## Use case, targets and metrics

* **The use case:** a chemist or assessor predicts a property of an untested compound from its structure, before a
  test.
  * The fit is direct when the test compounds stand for untested ones.
  * It is approximate when a tested reference set is closer to training than the compounds a screener meets.
    qsar_oral_toxicity has 16.3% close analogs, against 11.0% for its untested prediction set (USE-8).
* **Labels are often thresholds on a measured value:** LD50 at most 50 mg/kg for "very toxic", at most 11 µg per bee
  (the US EPA's threshold). Keep the source's class. A continuous alternative (logBCF, pXC50) is the record's note or a
  task of its own.
* **Expert conclusions ship at the resolution the field reads them at.** Keep the source's classes, and merge them
  only by an established convention of the field, with the merge tested (CLEAN-17). The NCI screen concludes CA, CM or
  CI; four independent releases over eighteen years merge CA and CM into one active class (the 2007 HIVA challenge,
  MoleculeNet, OGB's `ogbg-molhiv`, ChemPile), and that binary call is what a screening team acts on, so
  `nci_aids_antiviral_screen` ships it (Lennart, 2026-11-02). What a merge gives up belongs in a decision table: there
  the two active classes are a potency scale, which the log selectivity index separates at ROC AUC 0.948.
* **The NCI screen's censored values are no regression target:** its EC50 was not reached in 38,048 of 39,365 rows.
  Censoring is decided case by case: asp_potassco_classification and sat11_hand_algo_runtime keep a solver's
  timeout at its recorded limit (a minority of the runs, charged by the metric, PAR10).
* **Impossible values leave** (qsar_tid_11's pXC50 of -6.24). Values that are medians over many sources are noted.
* **Metrics:**
  * The Milano group reports the non-error rate (balanced accuracy) as its house measure, not one deliberate choice, so
    the fallback applies (MET-5).
  * MoleculeNet and OGB score ROC-AUC on the active-against-inactive label. A dataset that ships that same label
    takes the metric with it (MET-4); one that keeps finer classes scores a different target, and falls back to log
    loss (MET-11).

## Sources and provenance

* **Benchmarks are processed copies.** MoleculeNet, TDC, OGB, ChemPile and TUDataset each copy a primary source; go to
  that primary (the NCI DTP release, the ChEMBL release, the authors' supporting information).
* **A challenge cut of a public screen is a version of it** (PROV-6). HIVA (`hiva_agnostic`) is 4,229 compounds of the
  NCI screen with anonymised bits: its rows link to NSC numbers by their bits, 97% of them with confidence. The full
  release ships instead (Lennart, 2026-11-01).
* **Licences are often unstated.** Supporting information usually states none; the Milano workbooks are "freeware ...
  with proper reference". A licence is never a verdict reason (EV-4), but note it.
* **Commercial descriptor software** (Dragon, Pipeline Pilot) makes features that nobody can recompute: one more reason
  to ship the structure.

## Pitfalls we hit

| Pitfall | Dataset | What we did |
|---|---|---|
| SD records without `M  END`; the file is Unix-compressed (`.Z`) | nci_aids_antiviral_screen | add `M  END` before parsing; `gzip -dc` |
| RDKit rejects metals, boron, pentavalent silicon | nci_aids_antiviral_screen (609), qsar_oral_toxicity (1) | drop with counts by class; repair from PubChem by CAS when one row |
| CAS numbers turned into dates by a spreadsheet | qsar_oral_toxicity (155 rows) | match by InChIKey |
| Two chemicals carry each other's SMILES and descriptors | qsar_bioconcentration (3 pairs) | swap back, checked in Wikidata and PubChem |
| A row's SMILES is another chemical than its CAS | qsar_bioconcentration (3) | drop |
| RDKit's `Ipc` reaches 6e166, past float32 | qsar_oral_toxicity | ship as log10(1 + Ipc) (the encoding does) |
| Stereo read from 3D coordinates | nci_aids_antiviral_screen | remove it |
| A SMILES read as text | apistox, qsar_bioconcentration, drug_induced | a text embedding gives nothing, character n-grams -0.025 to +0.010: type it as a structure |

## Evidence on encodings (2026-10 and 2026-11)

| Change | Effect |
|---|---|
| the SMILES as Qwen3 text embedding, apistox | ROC AUC 0.78-0.81, against 0.70-0.82 with no structure; ECFP4 bits or character n-grams 0.83-0.85 |
| the SMILES as character n-grams next to descriptors | -0.025 to +0.010 ROC AUC |
| MACCS keys next to RDKit's descriptors | +0.025 / +0.023 on drug_induced (LightGBM / random forest); -0.006 to +0.009 elsewhere |
| our full RDKit set in place of drug_induced's 176 source descriptors | +0.001 / +0.002: the source's set reproduced |
| ECFP4 counts added to descriptors and MACCS, qsar_tid_11 | R^2 0.601 to 0.658, above the authors' FCFP6 bits (0.645) |
| Mordred's descriptors added, qsar_bioconcentration | -0.020 / -0.013 macro ROC AUC |

## In Data Foundry

* **A definition:** `special_features = (Smiles(column="SMILES"),)`, a special feature in one column, written by
  `canonical_smiles(...)`. Options:
  `largest_fragment=True` (check what it keeps first) and `stereo=False` (the copy key). The split groups come from
  `scaffold_groups(...)`.
  * Reference definitions: qsar_oral_toxicity (copies by structure and InChIKey, a repair, a prepared raw file),
    qsar_tid_11 (structures recovered from a ChEMBL release), drug_induced_autoimmunity_prediction (stereo pairs),
    nci_aids_antiviral_screen (an SD file, salts, unreadable records), apistox (a temporal molecule task).
  * The recipe: [definitions.md](../../knowledge-data-foundry/references/definitions.md), "The preprocessing recipe
    (`_clean`)", step 6, and the `special_features` bullet of "Field mapping".
* **The container** records the column in `task_metadata.special_features` (kind `smiles`, layout `column`, encoding
  required, the recommended encoding's id); `special_features(container, "smiles")` lists it, and
  `encode_special_feature(df, feature)` (`data_foundry.v2.special`) encodes it.
* **Encodings:** `encode_smiles` and `DEFAULT_SMILES_ENCODING` (`data_foundry.v2.chemistry`); the date and text
  encodings and `recommended_encodings()` are in `data_foundry.v2.encodings`.
* **Checks:** the bundle check `dataset_smiles_column` parses every value with the pinned RDKit, and a SMILES column
  raises no `dataset_identifier_column`.
* **Probes:** they see the column in the recommended encoding (`dataset_io.py`); the blind reviewer's clean room keeps
  the string.
* **What TabArena still needs** (the guard against the text embedding, the encoder, the cache, timing in the fit time):
  `datasets/_dev/tabarena-v0pt2/BENCHMARK_CHANGES_TODO.md`, "Encodings and their caches".
