---
unique_name: sarcoma
name: SARC
checked_by:
- Andrej
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
priority: 3
decision_markers:
- Selection Bias
tags:
- Tiny Data
- 'Samples: No Time Dimension'
- Experimental Results
collections:
- New (BeyondArena)
original_source: Website
year: '2018'
collection_period: 1994-2013
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://acgt.cs.tau.ac.il/multi_omic_benchmark/download.html
v2_path: datasets/_dev/tabarena-v0pt2/sarcoma/dataset.py
source_row: 783
type_adapter_id: curation-record-v1
---

## Comments

used in the TabPFN-Wide paper. from their download instructions: to map the methylation probe IDs to gene symbols, download the file from `https://webdata.illumina.com/downloads/productfiles/humanmethylation450/humanmethylation450_15017482_v1-2.csv`

**Assessment (AI, 2026-10-07):** No reason for `DF: Suspended` is recorded here or in git. TabPFN-Wide (arXiv 2510.06162v1, Sec. 5) classifies `histological_type`, so `problem_type` should be Multiclass Classification. That field is the submitted diagnosis: the TCGA sarcoma study (Cell 2017) confirmed 206 cases by expert review, excluded the others (QC failures, "3 probable melanomas", uncertain types) and reclassified 20. Added as `datasets/_dev/tabarena-v0pt2/sarcoma/` with the reviewed type from the study's GDC master patient table: 201 patients (the 5 MPNST dropped; LMS 80, DDLPS 50, UPS 44, MFS 17, SS 10) and 25,971 omic features. Open: the study treats UPS and MFS as one spectrum.

CC (2026-10-12, Lennart): Kept in TabArena v0.2 after the task-probe review (flag `few_minority`, multiclass). Synovial sarcoma has 10 rows, 3-4 per test fold. They are 5% of the test rows and 6.5% of a random forest's log loss (0.64 against 1.41 for the class shares). Too Small is for a task whose scored units are a handful; one rare class of the source's own labels that does not decide the score is part of the task.

CC (2026-10-19, Lennart): for the next pass, rebuild the methylation block from the GDC's per-sample beta values: the source kept 5,000 probes, by our notes chosen by variance over all patients and imputed with k-nearest neighbours over all patients. Kept as is until then.

**Assessment (AI, 2026-10-20):** priority 3 for the review of the added dataset: gap + (problem_type multiclass_classification), use case -, source +, shape -, no known risk. A very wide (26k features), tiny (201 patients) multiclass omics task that covers the wide-data regime; its use case is invented.

**Assessment (AI, 2026-10-20):** review panel (full): ship after changes; applied: the 61 `Methy_rs*` SNP genotype probes dropped, fit set to approximate (five confirmed types stand in for every referred sarcoma), the label note says the review required 12q15 copy-number gain for DDLPS (not shipped, so SEL-5 is not triggered), the source's all-patient preprocessing written as a kept potential leak, and a `splits_comment` added. The use case is real (molecular sarcoma typing, Koelsche et al. 2021), not invented. Open: merge MFS and UPS, and IID or site-grouped split (Review issues 3 and 4). Priority 3: gap +, use case -, source +, shape -, risk 0 (gap: multiclass; use case: fit approximate; shape: 201 patients; risk: the leak is weak and kept by the curator, and the open issues are weighing calls, not a leak or an unclear target).

CC (2026-10-21, Lennart): "let us stay with direct fit if the task (without leakage) would be a direct fit and only move to approximate fit if we had to change a lot to avoid the leak"; USE-8 amended. The fit stays approximate for the closed set of five confirmed types; the kept preprocessing over all patients is no longer a reason for it.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback log_loss — The source (Rappoport & Shamir 2018) is a clustering benchmark without a label, and the TCGA study (Cell 2017) defines no prediction metric. The task paper the definition cites, TabPFN-Wide (Kolberg et al. 2025, arXiv 2510.06162), reports AUROC and accuracy on COAD/LGG/BRCA/GBM/OV, but SARC 'is only used for attention analysis' (Table 1 caption), so no metric is defined for this task.

CC (2026-10-22, Lennart): issue 3: merge myxofibrosarcoma and undifferentiated pleomorphic sarcoma. Issue 4: keep the IID split by patient. Record field `problem_type` takes the definition's value (multiclass).

**Assessment (AI, 2026-10-22):** four classes: leiomyosarcoma 80, undifferentiated pleomorphic sarcoma or myxofibrosarcoma 61, dedifferentiated liposarcoma 50, synovial sarcoma 10 (the TCGA study's single spectrum and the methylation classifier's one class, Koelsche et al. 2021). Random forest log loss 0.650 to 0.469, macro ROC AUC 0.958 to 0.984; the only probe flag is `few_minority` (synovial sarcoma, 3 per test fold). Holding whole sites out now raises the forest's log loss from 0.46 to 0.58 (stated in `splits_comment`). The best single feature (MDM2) reaches skill 0.24 against 0.75 for the best model. dataset check: 0 errors, 0 warnings. REVIEW.md removed (nothing left open). Not built yet.

CC (2026-10-26, Lennart): verdict ship.

**Assessment (AI, 2026-10-26):** the reason behind issue 4, from the cross-dataset item on TCGA tissue sites: the site is weakly visible from the features (one site against the rest ROC AUC 0.70-0.75, 0.69-0.73 within dedifferentiated liposarcoma), so IID by patient rests on the use case (a lab types new patients' tumours), not on a null gap; one site holds 101 of the 201 rows. In glioma_grading the features did not predict the site. Cases row in splits.md (SPLIT-29, SPLIT-31).

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `sarcoma_methylation_classification` (TBD -> Yes, priority 3); a related task: `cns_tumor_methylation_classification` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-12, Andrej): reviewed under the rule for cuts of growing scientific catalogues. TCGA has closed: the GDC still lists the 261 sarcoma cases the 2017 study worked from, the plate code that marks a TCGA batch is recoverable only from the full GDC barcode (127 plates over the cohort, trimmed away in the benchmark's files), and the one date the index gives is the year of diagnosis (169 of 261 cases), which is not the date a case entered the programme; the random split over patients stands (Review issue 5, open).

CC (2026-11-12, Andrej): Review issue 5, A: the random split over patients stays. TCGA is closed, so no later wave exists; the aliquot plate is recoverable only from the GDC and stands for the source site, and the year of diagnosis (169 of 261 cases) dates the patient, not the entry into TCGA; recorded in a curation note.

CC (2026-11-18, Andrej): collection type stays `Experimental Results` (Review issue 7, A as implemented; full-information split check). Supersedes the Clinical Study mark of 2026-11-17 (issue 6):
- the type rule for undated patient data names this dataset as experimental results;
- as a clinical study the split would reopen on the GDC year of diagnosis, with no new fact for it.

## Review

**Outcome:** added. The TCGA sarcoma cut of the Rappoport & Shamir multi-omic benchmark: 201 patients whose
histological type expert pathologists confirmed, 25,910 expression, methylation and microRNA measurements, split at
random over patients. Everything the earlier review opened was settled on 2026-10-22 and the dataset was shipped
(Lennart, 2026-10-26). Reopened on 2026-11-12 under the review of how cuts of growing scientific catalogues split:
TCGA is a programme that added its cases in batches, so whether this cut should be split by when a case entered it
was never asked. The AI recommends keeping the random split over patients.

**Main points:** Settled: the random split over patients stays; the TCGA batch and the year of diagnosis were checked
as arrival keys and are in the notes (issue 5, A, 2026-11-12); the collection type stays `Experimental Results`
(issues 6 and 7, 2026-11-18).

**Issues for Andrej:**

5. **Keep the random split over patients, or split by when the case entered TCGA?**

   * **Problem:**
     - TCGA has stopped growing: the sarcoma cohort was closed with the study that supplies our label and the GDC
       still lists its 261 cases, so no case arrives after this cut[^5a].
     - The one date the parent source gives per case is the year of diagnosis (169 of the 261 cases, 1996 to 2013),
       which is when the patient was diagnosed, not when the case entered the programme.
     - Keep the random split over patients, split by the TCGA batch, or split by the year of diagnosis?
   * **Background:**
     - A wave here would be a TCGA batch: the tissue a source site shipped, typed on one aliquot plate. The plate
       code sits in the full TCGA barcode and is recoverable from the GDC (127 distinct plates over the 261 cases),
       but not from our rows: the benchmark trims every barcode to the sample (`TCGA.3B.A9HI.01`).
     - The family key is the tissue source site, the barcode's second field, and the curator already weighed it: one
       site holds 101 of the 201 rows and 40 of the 50 dedifferentiated liposarcomas, holding whole sites out raises
       a random forest's log loss from 0.46 to 0.58, and the IID split by patient was kept because a lab types the
       tumours of new patients (Lennart, 2026-10-22). That decision is not reopened here.
     - The use case fills in a collection that already exists: the model assigns one of four confirmed types that the
       study's review fixed, so a type the cohort does not hold cannot be predicted at all, whichever key splits it.
   * **Experiments:** the GDC's case index for TCGA-SARC, queried 2026-11-12: 261 cases, 169 with a
     `year_of_diagnosis` (64.8%, 1996 to 2013, 117 of them 2009 or later), every case with at least one aliquot
     barcode and 127 distinct plate codes over the cohort. No field in the index dates the accrual itself.
   * **Effect on the task:** a split by the year of diagnosis would hold out patients diagnosed late, which is not a
     wave of the catalogue but a property of the patients, and 35% of the cohort carries no year at all; a split by
     plate would hold out a shipment, which is the family key the source site already stands for.
   * **Consistency:** follows the screen whose only recoverable order predated the programme, where the family key
     was kept (`nci_aids_antiviral_screen`, 2026-11-11), and the company collection at the edge of the catalogue case
     (`bioresponse`); the four regulatory toxicity sets and the inventory screen kept their family key on the same
     reading.
   * **Sources:** the benchmark page, <https://acgt.cs.tau.ac.il/multi_omic_benchmark/download.html>; the TCGA
     sarcoma study, Cancer Genome Atlas Research Network, "Comprehensive and Integrated Genomic Characterization of
     Adult Soft Tissue Sarcomas", Cell 2017;171(4):950-965.e28, <https://doi.org/10.1016/j.cell.2017.10.014>; the
     GDC's project page, <https://portal.gdc.cancer.gov/projects/TCGA-SARC>.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the random split over patients (implemented) | no change; the finding goes in the notes | the cohort is closed, so there is no later wave to hold out; the lab's use case is new patients of the same referral stream | the optimism for a lab whose patients come from elsewhere stays, as the splits comment says |
     | B | Split by the TCGA batch (aliquot plate) | groups rebuilt from the GDC barcodes, the random split dropped | holds out a shipment of tissue | the plate is not in our data; a shipment is the source site under another name, and that key was already weighed and declined |
     | C | Split by the year of diagnosis | expanding windows on 169 of 261 cases | the only calendar the source gives | it dates the patient, not the entry into TCGA, and a third of the cohort has no year |

   * **Recommendation:** A: the catalogue is closed, so no key here holds out items that arrived later, and the two
     candidates either repeat the site key or date the wrong event. **Decision:** A, B or C?

   **Notes for the AI:** on A, a `curation_comments` bullet next to the split bullet recording that TCGA is closed,
   that the plate code is recoverable only from the GDC, and the dating numbers above; no data, split or score
   changes, and no rebuild. On B, the plate codes have to be fetched per aliquot from the GDC and joined on the
   patient barcode before any grouping is declared.

   [^5a]: **SPLIT-37** (Should): a dataset drawn from an expanding science catalogue, a cut of a database or testing
     programme that keeps growing, can be split by the item, by its family or by when it entered the catalogue, and
     where the actor predicts for items the catalogue does not hold yet the entry date holds out what a family key
     leaves in. A catalogue that is not growing, a recoverable date that is not the date items entered, and labels
     that are not final each put a dataset outside the case, and there the family key is the one that stands for the
     use case.

   **Resolved (2026-11-12, Andrej):** A: the random split over patients stays. A `curation_comments` bullet after the
   split bullet records that TCGA is closed, that the plate code is recoverable only from the GDC, and the dating
   numbers (year of diagnosis for 169 of 261 cases, 1996 to 2013); record CC line. Data, split and score unchanged;
   `dataset check` re-run.

6. **Collection type: `Clinical Study` instead of `Experimental Results` for TCGA's profiled sarcoma specimens?**

   * **Problem:**
     - the rule[^split-34]'s tie rule names this case: patient data without dates is experimental results when it has no time dimension ('a tumour's type measured on banked specimens'), and the record carries `Samples: No Time Dimension`.
     - TCGA is closed and its one date, the year of diagnosis (169 of 261 cases), dates the patient, not the case's entry, so no arrival order exists under either type.
     - Re-walked as a clinical study for later patients at the same lab, the folds stay random over patients and only the tag becomes `ForcedIIDFromTemporal`; the other-site branch gives site folds, measured (random forest log loss 0.46 to 0.58) and declined on 2026-10-22.
   * **The doubt:** A multi-site patient cohort (TCGA, 32 tissue source sites) is closer to a clinical study than to designed runs.
   * **What changes:** Nothing.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `Experimental Results` with `Samples: No Time Dimension`: stratified random 3-fold CV × 20 repeats (seed 4267) over the 201 patients, test 67, train 134, `Timeless` (implemented) | No change. | Matches the rule[^split-34] rule 5 word for word; `Timeless` says what holds: a primary tumour's type does not change once assigned. | TCGA's patients did arrive over years from 32 tissue source sites, which the type does not show; site optimism (one site holds 101 of 201 rows) is left to the split note. |
     | B | Tag `Clinical Study` with `Samples: Over Time`: the same random 3-fold CV × 20 over the 201 patients, tagged `ForcedIIDFromTemporal` (later patients, order lost, one row per patient) | The record's type tag and `Samples:` fact change; `data_tags` `Timeless` → `ForcedIIDFromTemporal` and the `Time basis:` line rewritten; folds unchanged, container rebuilt for the tag. | Names the patients' arrival over time and the untested later period. | Breaks the rule[^split-34] rule 5, which puts banked tumour specimens without a time dimension under experimental results; the folds do not change, so nothing measured changes. |

   * **Recommendation:** A, because the rule[^split-34] rule 5 gives this exact case ('a tumour's type measured on banked specimens') to experimental results, and the folds are the same under both.. **Decision:** A or B?

   **Notes for the AI:** blind walk of 2026-11-17 (split tree at cd3877cb). On B: change the record's type tag to `Clinical Study`, re-walk the tree from it and check whether the leaf changes; update the type rules' examples.

   [^split-34]: **SPLIT-34** (Should): Every record of a definition names how its source collected the rows with one **data collection type**, set at screening from the source and true whatever task is built on it.

   **Andrej (2026-11-17, change):** Option B: Tag Clinical Study. Then rewalk

   **Answer (AI, 2026-11-17):** The type rules give this very case as their example of experimental results: change the
   type against them?

   * **Problem:**
     - The type rules sort undated patient data by how it arrived: experimental results when the data has no time
       dimension, "a tumour's type measured on banked specimens", which is the rules' own wording for this dataset[^sa1].
     - TCGA's specimens were banked by 32 tissue source sites and profiled later; nothing dates a patient's arrival.
     - The walk again as a clinical study depends on where the model is used: at another site, the 32 sites are
       enough to hold out (whole sites, `UnseenGroup`); at the same lab for later patients, the order is lost
       (random folds, `ForcedIIDFromTemporal`). As experimental results it is random folds, `Timeless`, as shipped.
   * **Background:** the definition measured holding out sites: log loss 0.46 rises to 0.58, and kept random folds for
     a lab typing new patients.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | `Clinical Study`, the model used at another site | type tag changes; folds hold out whole tissue source sites (32), `UnseenGroup` | tests the transfer to a new site, which costs 0.12 log loss | breaks the rule's own case; needs a written exception |
     | b | `Clinical Study`, the model used at the same lab | type tag changes; random folds, `ForcedIIDFromTemporal` | the reading you marked | breaks the rule's own case; the folds do not change |
     | c | Keep `Experimental Results` (implemented) | no change | the rule and its case agree | the specimens stay read as designed measurements |

   * **Recommendation:** c, unless the use case is another site; then the question is the split (a), not the type.
     **Decision:** a, b or c?

   [^sa1]: **SPLIT-34** (Should), rule 5: patient data without dates is a clinical study when the patients arrived
     over time, and experimental results when the data has no time dimension (a tumour's type measured on banked
     specimens).

   **Resolved (2026-11-18, Andrej):** superseded by issue 7, where `Experimental Results` is kept as implemented (A); the type tag and the folds do not change.

7. **Keep the type `Experimental Results`, as the type rules name sarcoma?**

   * **Problem:**
     - You marked `Clinical Study` (2026-11-17); the type rule for undated patient data names sarcoma itself as experimental results (tumour types measured on banked specimens)[^s34r5].
     - lung_adenocarcinoma_metastasis, the rule's other example, keeps `Experimental Results` by your ok of the same day.
     - As a clinical study it would be walked as later patients at one lab, with the GDC's year of diagnosis (169 of 261 cases) as an arrival date: a new split question, not only a tag.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | `Experimental Results` (implemented) | No change | What the type rule says | |
     | B | `Clinical Study` | The type rule and its cases are amended; the split is re-walked on the years of diagnosis | Your mark | The two TCGA sets differ for no stated reason; the split reopens |

   * **Recommendation:** A, because the type rule names this dataset and the split would reopen for no new fact. **Decision:** A or B?

   [^s34r5]: **SPLIT-34** rule 5 (Should): "Patient data without dates is a clinical study when the patients arrived over time (`Samples: Over Time`), and experimental results when the data has no time dimension (`Samples: No Time Dimension`: a tumour's type measured on banked specimens)." Its cases: "sarcoma, lung_adenocarcinoma_metastasis (experimental results)".

   **Andrej (2026-11-18, ok):** As implemented (A).

   **Resolved (2026-11-18, Andrej):** A, as implemented: `Experimental Results` with `Samples: No Time Dimension`, as the type rule's own example (a tumour's type measured on banked specimens); random folds over patients, `Timeless`. Nothing changes.

## Reference

N. Rappoport and R. Shamir. Multi-omic and multi-view clustering algorithms: review and cancer benchmark. Nucleic Acids Research, 46(20):10546–10562, Oct 2018. URL https://doi. org/10.1093/nar/gky889.
