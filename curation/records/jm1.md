---
unique_name: jm1
name: jm1
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 2
tags:
- 'Samples: One Moment'
- 'Target: Unknown'
original_source: Other
year: '2004'
domain: technology & internet
required_split:
- Random (IID)
problem_type: Binary Classification
source_links:
- https://www.openml.org/search?type=data&id=1053
- https://openscience.us/repo/defect/
- http://promise.site.uottawa.ca/SERepository/datasets/jm1.arff
notebook_path: datasets/beyond_iid/old_iid/jm1/jm1.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/jm1/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Might be outdated, but otherwise seems fine at first glance

Potential issue: Text domain (?) with custom expert features

Lennart: see above

Andrej: Seems fine to include, but there are many related tasks (pc1,pc2,pc3,pc4,mc1,kc1,kc2,jm1). I would suggest an additional selection step where tasks with correlated model performance results are excluded.

CC (2026-10-01, Lennart): Leak audit: deduplicated to be on the safe side. 25% of rows (2,730 in 669 groups) share their code-metric vector with another row, mostly trivial modules (e.g. 173 copies of a 4-line, complexity-1 function); 88 vectors occur with both labels. A random split puts copies on both sides (LightGBM AUC 0.743 on the shipped splits vs 0.727 grouped by identical vector). The v2 definition now drops exact duplicate rows (1,973) and every copy of a vector that appears with both labels (176 rows): 10,885 -> 8,736 rows. No feature is derived from the target; the splits stay IID.

**Assessment (AI, 2026-10-14), source URL and download:** The source URL http://promise.site.uottawa.ca/SERepository/datasets/jm1.arff is the right page and still serves the file over plain http (Last-Modified 2005-03-02); over https it gives 404, which is what a browser or fetch tool that upgrades to https sees. The Wayback Machine holds captures from 2022-01-19 to 2026-10-10, all with the same content digest (https://web.archive.org/web/20240126152134id_/http://promise.site.uottawa.ca/SERepository/datasets/jm1.arff). The PROMISE file, its Wayback copy and OpenML 1053's ARFF (https://api.openml.org/data/v1/download/53936/jm1.arff) are byte-identical (md5 0c19aefce52ccb955d0de57e4c0fe8bf, the checksum OpenML lists), and the parquet that `_load_raw` reads through openml-python holds the same 10,885 x 22 values. The file names NASA and the NASA Metrics Data Program (mdp.ivv.nasa.gov) as creators and Tim Menzies as donor (2004-12-02). The definition keeps `source` and `source_url`, and its download description now gives the openml-python command and these copies.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Menzies & Di Stefano 2004 report probability of detection (PD) and of false alarm (PF) at operating points, a trade-off with no fixed threshold or combined score; the ROC curve is PD against PF. roc_auc is the binary fallback.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `unified_bug_dataset` (TBD -> 2nd Tier, priority 2), `apachejit` (TBD -> Yes, priority 2), `smartshark_release_defect_prediction` (TBD -> Yes, priority 3); a related task: `apachejit` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target ships as No/Yes, Yes the event (True means defects).

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship as defined: real NASA defect data cleaned as the field cleans it; methods spread, and the Halstead zero block, tested, marks no class. Priority 2: gap 0, use case 0, source 1, shape 1, risk -1.

CC (2026-11-12, Andrej): ship as defined (BeyondArena v0.2 review page, issues 1 and 2, A). The random split is read as a `Snapshot` of one code version, its `Time basis:` line in the curation notes (the tag enters the definition with PR #50); the Halstead tool's zero block (893 rows, all 16 Halstead and line-count measures 0) is noted there as kept, since it marks no class. `domain` filled from the definition (technology & internet). The declared split and metric checked and kept.

## Review

**Outcome:** added. NASA's JM1 software-defect data from the PROMISE repository (Menzies and Di Stefano 2004): one row
per C function of a real-time ground system, 21 static code measures (line counts, McCabe and Halstead measures), the
label whether the function had a reported defect; random splits after removing repeated measure profiles (10,885 to
8,736 rows). The AI recommends shipping it as defined. Reviewed without a panel, from the gathered evidence: the record,
the curator's leak-audit decision of 2026-10-01, model runs on the shipped data and on TabArena's copy, and
one cheap check. Validity: real modules and reports; the label's period and whether the code was measured before or
after the fixes are not stated (fit approximate says so). Value: on BeyondArena's version (with the copies) the
benchmark
methods range from ROC AUC 0.789 (best) and 0.786 (TabPFN-3.5) over a median of 0.756 to 0.723 (logistic regression),
and the best explicit model (a lookup of similar modules around a quadratic logistic model) ranks 13 of 41, so the task
separates methods. Quality: on 893 rows (10.2%) of the v0.2 frame all 16 Halstead and line-count measures are 0 while
the size and complexity measures are not, so the Halstead tool gave no output; tested, this marks no class (the flag
alone scores ROC AUC 0.52; defect share 0.30 against 0.21, higher among large modules and lower among small ones), and
a gradient-boosting model scores the same with the zeros as shipped or set to missing (0.709 against 0.710, 5 folds).
Change that needs no decision: a note on these zeros in the curation notes. Weighed: real defect data of a classic
benchmark family with a clear inspection use (+), an unstated label period and possibly post-fix measures (-).

**Main points:** Nothing open. Settled 2026-11-12: ship as defined, the Halstead zero block noted in the curation
notes (issue 1, A); the random split named a `Snapshot` of one code version, its `Time basis:` line in the curation
notes (issue 2, A).

**Record judgment:** valid. The de-duplication is the curator's (2026-10-01) and follows the cleaning the field adopted
for the NASA files, which removes repeated and inconsistent cases (Shepperd, Song, Sun and Mair, "Data Quality: Some
Comments on the NASA Software Defect Datasets", IEEE Transactions on Software Engineering 2013;39(9):1208-1215,
[doi:10.1109/TSE.2013.11](https://doi.org/10.1109/TSE.2013.11)). Measured on the shipped rows: the 1,973 exact copies
removed are 95% defect-free, mostly small modules, so the defect share rises from 19.4% to 22.0%; the 176 removed rows
are the 88 profiles that occur with both labels. Andrej's early remark (keep one of the many related NASA tasks) is met:
only jm1, the largest, is in. The data-scouting run of 2026-10-31 found newer defect data (`apachejit`, priority 2;
`smartshark_release_defect_prediction`, priority 3; `unified_bug_dataset`, 2nd tier), screened in their own records and
not added yet. The record has no `domain`; the definition's `technology & internet` can be filled in without a mark.

**Issues for Andrej:**

1. **Ship as defined?**

   * **Problem:**
     - Nothing open was found: real modules and defect reports, the curator's removal of repeated and conflicting
       measure profiles, and a zero block of the Halstead tool that, tested, marks no class.
     - The label's period and whether the code was measured before the fixes are not stated, which the approximate
       fit already says.
     - Ship as defined, or retire?
   * **Experiments:** on BeyondArena's version the benchmark methods spread from ROC AUC 0.789 to 0.723 (median 0.756);
     on the v0.2 rows, gradient boosting scores 0.709 with the Halstead zeros as shipped and 0.710 with them set to
     missing (5 folds); the zero-block flag alone 0.52.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Ship as defined (implemented) | 8,736 modules, 21 measures, random splits, ROC AUC | a classic defect task; methods spread; cleaned as the field cleans these files | label period unstated; possibly post-fix measures |
     | B | Retire | `No (Retired)`, a CC line, the folder removed | leaves the place to newer defect data once added | no defect of the data found; the newer sets are not added yet |

   * **Recommendation:** A: the methods spread and no reason in the task itself argues for retiring it[^1a].
     **Decision:** A or B?

   [^1a]: **TP-3** (Must): if tuned methods spread, keep the dataset.

   **Andrej (2026-11-12, ok):** (no note)

   **Resolved (2026-11-12, Andrej):** A: ship as defined, 8,736 modules, 21 measures, random splits, ROC AUC. The
   change that needed no decision is in: an `Anomaly:` bullet on the 893 rows (10.2%) whose 16 Halstead and
   line-count measures are all 0 (recounted 2026-11-12; defect share 0.30 against 0.21; flag alone ROC AUC 0.52,
   gradient boosting 0.709 shipped against 0.710 set to missing). Split and metric checked and kept. `dataset check`:
   0 errors, 0 warnings, 0 info; README regenerated (curation notes only). Not rebuilt.

2. **Time basis: name the random split a `Snapshot` of one code version?**

   * **Problem:**
     - The 21 code measures were extracted once, from one version of JM1's C code, and joined with whether each function had a reported defect; neither the version, the period of the defect reports, nor whether the code was measured before or after the fixes is stated, and the file has no function name or date.
     - The use case ranks the not-yet-inspected functions of the same program, so a random split over functions fills in the defect state of one code base at one moment, a `Snapshot`, and the record's `Samples: One Moment` agrees.
     - Name the random split a `Snapshot`, or a `ForcedIIDFromTemporal` that reads the use case as predicting the defects of a later release?
   * **Background:**
     - The table was donated to PROMISE by Tim Menzies on 2 December 2004 from the NASA Metrics Data Program, whose documentation is offline; its header says only that the data "comes from McCabe and Halstead features extractors of source code".
     - The prototypes, by the rule's questions: whether a function has a defect depends on its history and its testing, so not `Timeless`; the use case fills in the defects of this code base at the moment of the extraction, so a `Snapshot`[^2a]. For a snapshot the rule asks that no sample of a test sample's moment carry its target; all functions share one moment, and a defect report that touched several functions of one file would label them together, which no file or function name lets us test.
     - Defect prediction across releases, the more common use, needs version data that JM1 lacks; the newer defect sets found by the scouting carry commit dates (`apachejit`) or releases (`smartshark_release_defect_prediction`).
   * **Experiments:** the time probe of 2026-11-06 (OpenML's order of the rows) finds no order of the label (p = 0.71) and no date column. Two searches of 2026-11-06 found no document that says when the measures were taken relative to the defect reports; Shepperd et al. (2013) treat the data quality, not the timing.
   * **Unknown:** if the measures describe the fixed code, the features come after the target; issue 1's ship decision and the fit already name that risk, and the record's target fact cannot be set until the timing is known.
   * **Effect on the task:** none on the data or the scores; the tag and its line state why a random split stands for the use case.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random split, `Snapshot` (implemented) | the shipped split; once PR #50 is in, the tag and a `Time basis:` line naming the extraction | matches the definition's use case, this program's uninspected functions; matches the record's one moment | the moment is undated; whether the measures precede the defect reports is unknown |
     | B | Random split, `ForcedIIDFromTemporal` | the same split, tagged as a forward task whose time is lost[^2b] | names the common use, the next release, as untested | the definition's use case is the one code base; the file holds one version, so there is no period to be forced from |

   * **Recommendation:** A: one extraction of one code base, and a use case that ranks the functions of that code base. **Decision:** A or B?

   **Notes for the AI:** on A, once PR #50 is in: `data_tags = ("Snapshot",)` and a curation bullet `- Time basis:
   Snapshot: one extraction of the static code measures of one version of JM1, joined with each function's defect
   reports (NASA Metrics Data Program; donated to PROMISE on 2 December 2004); the test functions are functions of the
   same code base at the same moment. When the code was measured relative to the defect reports and their fixes is not
   stated.` No `splits_comment` change. On B, `data_tags = ("ForcedIIDFromTemporal",)` and a bullet saying that version
   data would allow a split by release.

   [^2a]: **SPLIT-32** (Should): how the data was collected is information for the split; a definition can name the
     use-case prototype it follows with a `Time basis:` line. A use case that only fills in a time the data covers
     (one census, one scrape) is a `Snapshot`, and the line names the moment; time can then reach a target only
     through samples of the same time.
   [^2b]: **SPLIT-8** (Must): a task temporal in nature or by its use case whose release cannot give the windows ships
     in the closest regime, tagged as forced from temporal; a release that is one moment is not forced but a
     `Snapshot` or `DelayedTarget`.

   **Andrej (2026-11-12, ok):** (no note)

   **Resolved (2026-11-12, Andrej):** A: the random split stays, read as a `Snapshot`. A curation bullet `- Time basis:
   Snapshot: ...` names the one extraction of one code version (NASA Metrics Data Program; PROMISE, 2 December 2004),
   says the timing of the measures against the defect reports is not stated, and ends with what the split cannot
   test (a later release; defects one report shares across a file's functions). The tag `Snapshot` enters
   `data_tags` once PR #50 is in the working copy. No `splits_comment` change; record CC line.

## Reference

https://openscience.us/repo/defect/
