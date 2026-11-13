---
unique_name: micro_mass
name: micro-mass
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 4
tags:
- Tiny Data
- Non-IID (Grouped)
- Many class
- Spectral Data
- 'Samples: No Time Dimension'
- 'Entities: Recur'
collections:
- TabArena Reject
- TabSTAR
original_source: UCI
year: '2013'
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5T61S
notebook_path: datasets/beyond_iid/grouped/micro_mass/micro_mass.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/micro_mass/dataset.py
source_row: 792
type_adapter_id: curation-record-v1
---

## Comments

CC: "spectral data. Clustered data. Need to check more carefully, but might be nice to include as an example for n<<d datasets"

Need to really understand the data and how we can use it, but otherwise sounds good to use!

From looking at the paper, data, and asking ChatGPT, I think we need to group by strain and hold out all replications.

20 classes.

CC (2026-10-12, Lennart): Kept in TabArena v0.2 after the task-probe review (flag `few_minority`, multiclass). Six species fall below 5 spectra in some strain-grouped test folds (B. thuringiensis: 11 spectra from 8 strains, 2-6 per fold; C. difficile 14 from 7). The grouped split makes fold sizes uneven. The six are 18% of the test rows and 25% of a random forest's log loss (0.88 against 2.94 for the class shares). Too Small is for a task whose scored units are a handful; one rare class of the source's own labels that does not decide the score is part of the task.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source hierarchical_balanced_accuracy — accuracy averaged per strain, then per species (Vervier et al. 2015, arXiv:1506.07251), with `Strain` (the group column) as its group input; scored metric changed from log_loss.

**Assessment (AI, 2026-10-27):** The open questions for the curator are in the record's Review (review of the Tiny Data datasets, written from the earlier findings, no review panel); the AI recommends shipping it. Priority 4: gap +, use case + (Mahé et al. 2014 and Vervier et al. 2015 name the use), source +, shape -, risk +.
**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found a related task: `driams_antimicrobial_resistance` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-02, Lennart): The spectrum is declared as a spectrum (`spectra`, CLEAN-26; PR #21) in the state the instrument's software left it, a VITEK MS peak list on 1,300 fixed bins (`peaks`); the m/z of the bins is not published, so the axis is the bin number. The recommended encoding leaves a peak list as it is, so models see the same values as before; the constant and copied bins stay dropped.

CC (2026-11-12, Andrej): reviewed under the rule for cuts of growing scientific catalogues. The panel is a one-off 2013 deposit of 20 species built for one study, the archive gives a strain nothing but an integer from 1 to 213, and a species the panel does not hold cannot be predicted at all, so no arrival key exists and the strain-grouped split stands (Review issue 4, open).

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship as defined: a lab use the source names, strains held out, and a wide spread of methods; Andrej's dispute (about 80% of the error sits in sister species the instrument cannot separate) is a value concern that no validity rule turns into a retirement. Priority 4: gap 1, use case 1, source 1, shape 0, risk -0.

CC (2026-11-04, Andrej): keep as defined (issue 1, A): 20 species scored per spectrum with the source's metric; the sister-species complexes are a limit laboratories also meet. The declared split (by strain) and metric checked and kept. Tagged `Spectral Data`: each row is one MALDI-TOF mass spectrum (a peak list on 1,300 bins), declared as a spectrum in the definition.

CC (2026-11-06, Andrej): time basis `Timeless` accepted on the BeyondArena v0.2 review page (issue 3, B, through the cross-dataset item on five more routine `Timeless` issues): the species is a fixed property of the strain, and the release holds no acquisition date, run or plate. The `Time basis:` line is in the definition's notes, ending with what the split cannot test; the tag enters `data_tags` once PR #50 is in the working copy.

CC (2026-11-12, Andrej): review page mark (issue 4, A): the strain-grouped split stays. The panel is a single 2013 deposit; the strain identifier is an integer with no accession or date, so no split by entry date can be built; noted in the `Time basis:` line.

## Review

**Outcome:** added. The AI recommends shipping it as defined; the one open question is Andrej's dispute of Lennart's
keep (issue 1). Reviewed without a review panel, from the gathered evidence: the record, an earlier check of
2026-10-15 (own runs on strain-grouped splits) and model runs on the shipped data. The data are 571
MALDI-TOF mass spectra (the instrument's fingerprint of a colony's proteins) of 213 bacterial strains of 20 species
(Mahé et al. 2014, UCI), one prediction per spectrum, whole strains held out, scored with the source's accuracy
averaged per strain and then per species. Validity: a clinical laboratory identifies the species of an isolated
colony from one spectrum, a direct fit; holding out strains is justified (logistic regression log loss 0.29 on random
splits against 0.49 on strain-grouped ones), the strain ids carry no label, and the spectrum ships as the
instrument's peak list, declared as a spectrum (Lennart, 2026-11-02). Value: the methods spread widely (log loss 0.43
to 1.18 over the benchmark methods run on all 60 shipped splits), but five complexes of sister species the instrument
cannot tell apart hold 64% of the rows and about 80% of the errors (issue 1). Quality: nothing open. Weighed: a lab
use the source names +, a wide spread of methods +, much of the score an instrument floor shared by all methods -.

**Main points:** All four issues are settled; the strain-grouped split stays (issue 4, A, 2026-11-12).

**Record judgment:** valid. The grouping by strain is right; Lennart's comment of 2026-10-12 settles the small species
and his comment of 2026-11-02 the spectrum declaration. The record says nothing on the sister-species complexes. The
Assessment of 2026-10-31 names `driams_antimicrobial_resistance` as a related task: it predicts antibiotic resistance
from MALDI-TOF spectra, not the species, so it is no better data for this task. The `## Reference` block cites Vervier
et al. as "submitted"; it is arXiv:1506.07251 (2015). No record field disagrees with the definition.

**Issues for Andrej:**

1. **Keep the dataset, though most of its error comes from sister species the instrument cannot tell apart?**

   * **Problem:**
     - Andrej disputes Lennart's keep: five complexes of close relatives that MALDI-TOF is known not to separate hold
       64% of the rows and about 80% of logistic regression's errors and log loss.
     - Much of what the benchmark scores is then a floor set by the instrument, the same for all methods, while the
       methods' differences come from the other rows.
     - Keep as defined, retire, or score at the level of the complex?
   * **Background:**
     - The complexes are Escherichia coli with three Shigella species, Bacillus cereus and thuringiensis,
       Streptococcus mitis and oralis, Enterobacter cloacae and asburiae, and Citrobacter freundii and braakii. The
       archive's README says the panel was built that way: "20 Gram positive and negative bacterial species covering
       9 genera among which several species are known to be hard to discriminate by mass spectrometry". The species
       mix is a designed, balanced panel, not the mix a laboratory meets.
     - For retiring, the dispute cited the weighed factor "raw spectral bins lean out", under which other spectral
       records were rated `TBD -> 2nd Tier` or `No`. That factor was amended on 2026-11-02: a measured spectrum,
       declared as one, is in scope unless a spectrum model is clearly better[^1a]. micro_mass now ships the
       instrument's peak list declared as a spectrum, which the benchmark leaves as it is[^1b].
     - For keeping: the methods spread, and a dataset whose tuned methods spread is kept unless a validity rule
       fails[^1c]. None fails here: no id leak, the split is right, and tabular models are competitive on these
       bins[^1d]. The sister species are a real limit of the use case, which laboratories also meet.
   * **Effect on the task:** TabPFN 3.5's lead over logistic regression (log loss 0.457 against 0.489) comes from the
     rows outside the complexes, which both models get nearly all right (0.138 against 0.252, 97% to 100% accuracy);
     inside the complexes logistic regression is slightly better (0.625 against 0.639).
   * **Experiments:**
     - Earlier check (2026-10-15, own runs, 15 strain-grouped splits, 5 repeats of 3 folds; TabPFN 3.5 on 6 of them):
       78% of logistic regression's errors and 82% of its log loss fall inside the complexes; merged into one label
       per complex, accuracy is 97%. B. thuringiensis is right 24% of the time; 9 of 213 strains are wrong in every
       repeat. Peak pooling and total-ion normalisation of the spectra did not improve the models, and logistic
       regression matches the source's linear SVM (accuracy 0.875 against 88.9%, Vervier et al. 2015).
     - BeyondArena (scored per spectrum by log loss): method ranks agree across folds (Kendall's W 0.99).
     - Model runs on the shipped data (log loss): over the benchmark methods run on all 60 splits, from 0.43
       (TabM, TabPFN 2.6) to 1.18 (TabDPT); on the 2 splits the run used, LIMIX-2 0.257, logistic regression 0.32 to
       0.33. Its agent also found 85% of the error between sibling species of one genus, and a logistic regression
       built on the taxonomy (order, genus, species within genus, Shigella merged into Escherichia) ranks second of
       41 (0.277).
   * **Consistency:** follows pancreatic_cancer_mouse_detection, a spectral dataset Andrej kept with its raw spectra
     (2026-10-21); the spectral records rated `TBD -> 2nd Tier` or `No` were judged under the factor since amended.
   * **Sources:** the UCI page, <https://doi.org/10.24432/C5T61S>; Mahé P, Arsac M, Chatellier S, et al., "Automatic
     identification of mixed bacterial species fingerprints in a MALDI-TOF mass-spectrum", Bioinformatics
     2014;30(9):1280-1286, <https://doi.org/10.1093/bioinformatics/btu022>; Vervier K, Mahé P, Veyrieras J-B, Vert
     J-P, "Benchmark of structured machine learning methods for microbial identification from mass-spectrometry
     data", arXiv:1506.07251 (2015), <https://arxiv.org/abs/1506.07251>.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep as defined (implemented) | 20 species, scored per spectrum with the source's metric | the source's task and metric; the methods spread; a limit labs also meet | much of the score is an instrument floor shared by all methods |
     | B | Retire | record `No (Retired)` with `Wrong Domain / Source Modality`; folder removed | removes a task dominated by an instrument floor | the tests show tabular models competitive, so this would amend the modality rule rather than apply it; the spectrum factor it rested on is amended |
     | C | Score per complex | the five complexes merged into one label each (13 classes) | scores only what the instrument can separate | a label merge of our own invention, which is no better version of the task[^1e] |

   * **Recommendation:** A. No validity rule fails, the methods spread, and the sister species are part of the real
     task. **Decision:** keep (A), retire (B) or score per complex (C)?

   **Notes for the AI:** on A, a `CC (<date>, Andrej):` line in the record with the decision, and `Andrej` stays in
   `checked_by`. On B, the retirement steps: record `No (Retired)` with marker `Wrong Domain / Source Modality`,
   folder removed, `v2_path` cleared, CHANGELOG entry. On C, a species-to-complex map in `_clean` (E. coli and the three
   Shigella; B. cereus and B. thuringiensis; S. mitis and S. oralis; E. cloacae and E. asburiae; C. freundii and
   C. braakii), the metric's per-species average then runs over complexes; test the merge as the target rule asks
   (classes per test fold, signal) and re-run the leak probes on the source's labels.

   **Andrej (2026-11-04, ok):** Let's do A

   **Resolved (2026-11-04, Andrej):** keep as defined (A), with a CC line in the record; the declared split (by
   strain) and metric checked and kept.

   [^1a]: **SEL-15**, weighed factor "A spectrum" (amended 2026-11-02, Lennart): a measured spectrum is a reading of
     the entity, and declared as one the benchmark encodes it as the field does; it is in scope unless a spectrum
     model is clearly better. It was "raw spectral bins lean out" until spectra had a declared type and a default
     encoding.
   [^1b]: **CLEAN-26** (Should): a spectrum ships as the source publishes it and is declared as a spectrum; the
     recommended encoding leaves a peak list as it is.
   [^1c]: **TP-3** (Must): if tuned methods spread, keep the dataset; a rule of an earlier part still wins.
   [^1d]: **SEL-12** (Must): data from a non-tabular modality is out where modality-specific models are clearly
     better, judged per dataset; vectorised signals are fine where tabular models are competitive. Marker
     `Wrong Domain / Source Modality`.
   [^1e]: **TP-6** (Must): keep apart whether the task is valid and whether it is the best version; a fix of our own
     invention (a label merge made from names) is not a better version.

2. **Tag the record as spectral data?**

   **Andrej (2026-11-04, note on the record):** If this is spectral data? If yes, is there a spectral data tag and if
   not, add it?

   **Answer (AI, 2026-11-04):**

   * **Your question:** is micro_mass spectral data, and is there a tag for it?
   * **Found:**
     - Yes: each row is one MALDI-TOF mass spectrum of a colony, the instrument's peak list on 1,300 fixed bins, and
       the definition declares it as a spectrum (`Spectrum(technique="mass_spectrometry")`, since 2026-11-02).
     - The record vocabulary had no such tag: the declared spectrum lived only in the definition, and the closest
       record field was the collection `RamanBench`.
     - pancreatic_cancer_mouse_detection is the other v0.2 definition that declares a spectrum; it is not tagged yet.

   **Resolved (2026-11-04, Andrej):** the tag `Spectral Data` was added to the vocabulary and to this record; tagging
   other spectral records waits for your call.

3. **Time basis: name the strain-grouped split `Timeless`, as the species is a property of the strain?**

   * **Problem:**
     - The species of each strain is known from the reference collection before it is cultured, and the row is the
       instrument's peak list of that culture, so nothing in a row arrives after the spectrum.
     - The record carries `Samples: No Time Dimension` with no time or target fact, and the definition names no time
       basis, although the strains were isolated at unstated places and times.
     - `Timeless` names a target that is a fixed property of the item and a split random or grouped by item family,
       which is the shipped split by strain[^3a].
   * **Background:**
     - The archive carries no acquisition date, run, plate or operator: the metadata file of the reference set holds
       the species and the strain number only, and the README describes a designed panel of 20 species, 7 to 20
       strains each, measured 1 to 6 times per strain on the VITEK-MS and reduced to 1,300 peak bins by the routine
       software.
     - The strain collection behind the panel accumulated over years, but which strains it holds does not change a
       strain's species, and the use case is a colony cultured in the laboratory today.
     - Whether a strain's replicates were run on different days or instruments is not published; the split keeps a
       strain's replicates on one side, so a batch shared by one strain's replicates cannot cross it.
   * **Effect on the task:** none on the data, split or score; the line states why a split that is not temporal is
     safe in time, and what it cannot test.
   * **Experiments:** the time probe on the source files (2026-11-06) found no order drift (consecutive rows share the
     species no more above chance than a shuffle, p 0.58) and no date-like or period column; the 300-odd columns it
     lists as period-encoding are sparse peak bins, a false alarm of the kind the spectral datasets give it.
   * **Consistency:** follows pancreatic_cancer_mouse_detection, the other spectral definition of this review, whose
     time issue recommends `Timeless` for a designed measurement campaign.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Strain-grouped split, no time basis (implemented) | as now | nothing to change | the definition does not say why a split that is not temporal is safe in time |
     | B | Strain-grouped split, `Timeless` | as now; the tag and a `Time basis:` line naming the fixed species, the undated campaign and the batch question the grouping already covers | states the fact the split rests on; names what the split cannot test | none found; no data, split or score changes |
     | C | Strain-grouped split, `Snapshot` | the prototype for one moment, with the line naming the 2013 campaign | reads the campaign as the one moment the data cover | the panel is a designed set of measurements, not a population of one moment to fill in, and its same-time check has nothing to hold out here |

   * **Recommendation:** B: the species belongs to the strain, the spectrum is all the laboratory has at
     identification, and the release holds no date or run order. **Decision:** A, B or C?

   **Notes for the AI:** on B, once PR #50 is in: `data_tags = ("Timeless",)` (the class adds the grouped tags) and a
   curation bullet `- Time basis: Timeless: the species is a fixed property of the strain, known from the reference
   collection before the culture, and the row is the spectrum of that culture. The release holds no acquisition date,
   run or plate (the metadata file has the species and the strain number only), and the file order carries no campaign
   order (time probe, 2026-11-06: no order drift, p 0.58). Not tested: an isolate of a species or a strain type the
   panel does not hold, and a run batch shared across strains, which no column records.`; `splits_comment` unchanged;
   `dataset check`; no rebuild (comment only).

   [^3a]: **SPLIT-32** (Should): how the data was collected is information for the split; the record carries the
     source's collection facts and a definition can name the use-case prototype it follows with a `Time basis:` line.
     `Timeless`: the target is a fixed property of the item, the same whenever it is measured (a material's strength,
     a molecule's activity, a species, the outcome of a designed run); the split is random or grouped by item family.
     `Snapshot`: the use case only fills in a time the data cover, and the line names the moment or the period.

   **Resolved (2026-11-06, Andrej):** B, accepted through the cross-dataset item "Accept five more routine `Timeless`
   issues with one mark?" The `Time basis: Timeless:` bullet is in `curation_comments`, ending with what the split
   cannot test (an isolate of a species or a strain type the panel does not hold); the split and `data_tags` are
   unchanged. The tag `Timeless` enters `data_tags` once PR #50 is in the working copy.

4. **Keep the strain-grouped split, or split by when a strain entered the collection?**

   * **Problem:**
     - The archive records a strain as "strain identifier (integer from 1 to 213)" and nothing else, so no accession,
       date, run or plate exists from which an arrival order could be recovered[^4a].
     - The reference panel is a designed set of 20 species, built for one study and deposited once in 2013, and no
       spectrum has been added to it since.
     - Keep the strain-grouped split, or split by an arrival key?
   * **Background:**
     - A wave here would be a deposit at a culture collection: strain collections do grow, and a clinical laboratory's
       isolate bank grows every week, but the deposit we ship is one paper's panel of 7 to 20 strains per species,
       chosen so that several species are hard to tell apart by mass spectrometry (the archive's README).
     - The 20 species are the label set, not items of a catalogue: a species the panel does not hold cannot be
       predicted by any model trained on these rows, so a later arrival is an open-set question and no split of these
       571 spectra tests it.
     - The family key exists and is the shipped one: the strain, with the species and the five sister-species
       complexes above it; issue 1 weighs those complexes and issue 3 named the split `Timeless`.
     - The use case fills in a collection that already exists: a laboratory identifies a colony against the
       instrument's reference database, which it holds before the culture is grown.
   * **Experiments:** the time probe on the source files (2026-11-06) found no date-like or period column and no
     order drift (consecutive rows share the species no more above chance than a shuffle, p 0.58); the metadata file
     holds two columns, `Species` and `Strain`, and strain numbers run across species rather than in species blocks
     (the first rows are strain 1 Streptococcus oralis, strain 2 Escherichia coli, strain 3 Listeria ivanovii).
   * **Effect on the task:** none measurable: with no arrival order in the release, no split by entry date can be
     built, so the only question is whether the strain grouping stands, and it does.
   * **Consistency:** follows the company compound collection at the edge of the catalogue case (`bioresponse`), where
     the set is an inventory already collected rather than a catalogue that grows, and the four regulatory toxicity
     sets, which kept the family key.
   * **Sources:** the UCI page, <https://doi.org/10.24432/C5T61S>; Mahé P, Arsac M, Chatellier S, et al., "Automatic
     identification of mixed bacterial species fingerprints in a MALDI-TOF mass-spectrum", Bioinformatics
     2014;30(9):1280-1286, <https://doi.org/10.1093/bioinformatics/btu022>.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the strain-grouped split (implemented) | no change; the finding goes in the notes | holds out a strain never measured, which is the use case; no arrival order exists to hold out instead | the panel's species mix is the study's, not a laboratory's, which the fit text says |
     | B | Split by the strain number as an arrival order | expanding windows on the strain index, the grouping dropped | the only integer in the release that could be an order | the archive calls it an identifier, it runs across species, and the time probe found no order drift; a split on it would hold out nothing the strain key does not |

   * **Recommendation:** A: a one-off deposit with no recoverable arrival order, where the species a laboratory can
     predict is fixed by the panel. **Decision:** A or B?

   **Notes for the AI:** on A, extend the `Time basis: Timeless:` bullet in `curation_comments` with one sentence:
   the panel is a single 2013 deposit, the strain identifier is an integer with no accession or date, and no arrival
   order can be recovered; no data, split or score changes, `dataset check`, no rebuild. On B, a `strain_rank` column
   and a temporal declaration on it would be needed, and the windows checked against the floor that every training
   side holds at least half the rows.

   [^4a]: **SPLIT-34** (Should): a dataset drawn from an expanding science catalogue, a cut of a database or testing
     programme that keeps growing, can be split by the item, by its family or by when it entered the catalogue, and
     where the actor predicts for items the catalogue does not hold yet the entry date holds out what a family key
     leaves in. A catalogue that is not growing, a recoverable date that is not the date items entered, and labels
     that are not final each put a dataset outside the case, and there the family key is the one that stands for the
     use case.

   **Resolved (2026-11-12, Andrej):** A: the strain-grouped split stays. The `Time basis: Timeless:` bullet in
   `curation_comments` now says the panel is a single 2013 deposit whose strain identifier carries no accession or
   date, so no arrival order can be recovered; record CC line. Data, split and score unchanged; `dataset check`
   re-run.

## Reference

Mahé et al. (2014). Automatic identification of mixed bacterial species fingerprints in a MALDI-TOF mass-spectrum. Bioinformatics.

Vervier et al., A benchmark of support vector machines strategies for microbial identification by mass-spectrometry data, submitted
