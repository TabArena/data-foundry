---
unique_name: raman_microplastics_weathered
name: Weathered Microplastics
checked_by:
- AI (UNVERIFIED)
- Andrej
suggestion: 'No'
decision_markers:
- No Good Target (yet)
tags:
- AI-Filled (Verify)
- Tiny Data
- Many features
- Spectral Data
- 'Samples: No Time Dimension'
- 'Entities: Recur'
- Experimental Results
collections:
- RamanBench
original_source: Other
year: '2020'
domain: environmental science & climate
collection_period: Unknown
problem_type: Multiclass Classification
source_links:
- https://doi.org/10.1016/j.scitotenv.2020.139990
- https://data.mendeley.com/datasets/kpygrf9fg6
- https://arxiv.org/abs/2605.02003
- https://doi.org/10.17632/kpygrf9fg6
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-11-25, Andrej): `No`, marker `No Good Target (yet)`, on the source check below: the polymer label of 140 of the 173 rows is a commercial spectral-library match of the same spectrum a model would be given, and the 14 rows with an independent method are too few for any split.

CC (2026-11-25, Andrej): the source release was checked, and it settles the record against the dataset rather than for it. Recommendation: `No`, marker `No Good Target (yet)`; the verdict is not changed here.

- The cut was the smaller problem and the source does fix it: Mendeley 10.17632/kpygrf9fg6 holds one text file per spectrum with its own id (`sta-1` to `sta-18`, `wea-1` to `wea-155`) and a `content.xlsx` of 173 usable rows, against the 77 spectra of the benchmark's copy.
- The label is not independent of the spectrum. `content.xlsx` carries a "Score from KnowItAll" for 140 of the 173 rows (45.6 to 99.5), and for those 140 rows no other method is named: the polymer was read off a commercial spectral-library match of the same spectrum a model would be given. A model would be learning to reproduce that matching program, not to identify a polymer.
- Only 14 rows name an independent method (11 ATR-FTIR, 1 Py-GC-MS, 2 verified by ATR-FTIR), 10 more say "identified subjectively based on Raman", and 9 say the polymer could not be identified at all (8 of them typed `/`).
- Restricting the task to the independently identified rows leaves 14, far below any split.
- The classes are also steeply imbalanced over 10 polymers: PE 74, PP 54, PET 16, PVC 9, `/` 8, PA 6, PC 2, PS 2, NC 1, ABS 1.


**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: real field-collected weathered microplastics with a named identification use, but RamanBench's cut keeps 77 spectra in 3 polymer classes, does not match the source's counts, and the smallest class has about 10 spectra.
- Source: Dong, Zhang, Xing, Chen, She and Luo, "Raman spectra and surface changes of microplastics weathered under natural environments", Science of the Total Environment 739:139990, 2020 (https://doi.org/10.1016/j.scitotenv.2020.139990); data "A Raman database of microplastics weathered under natural environments" on Mendeley Data (https://doi.org/10.17632/kpygrf9fg6, 2020-04-07, CC BY 4.0). As published: "This dataset contains 20 Raman spectra of standard samples and 155 Raman spectra of weathered microplastics. 135 Raman spectra of weathered microplastics can be identified. Among these 135 Raman Spectra, we selected 124 spectra with distinct peaks to build the Raman database of weathered microplastics (RDWP)" (Mendeley); one TXT file per spectrum (`sta-*` standards, `wea-*` weathered) and `content.xlsx` with the polymer per file (raman-data `MendeleyLoader`); per the raman-data card PE 62, PP 44, PET 10, PVC 4, PA 2 among the RDWP spectra. RamanBench's cut: 77 spectra x 1,144 bins (202-3498 cm-1), 3 classes (classes under 9 spectra removed).
- Use case: an environmental lab identifies the polymer of microplastic particles from sediment: the RDWP "was built to accurately identify microplastics in natural environments" (abstract); the paper studies how weathering changes the spectra and names no actor or decision beyond identification. Fit direct for the particles; regime IID (one spectrum per particle as far as the release shows; not verified).
- Siblings and duplicates: none (grep over the records for microplastic, the DOIs). External collections: RamanBench, which lists it as trivial ("perfect:LR", configs/v1/quality_exclusions.json); its scores are no evidence for our task (EV-4).
- Better data: a candidate of the benchmark RamanBench; no new search (run brief).
- Papers and pages: Dong et al. 2020 (abstract via Semantic Scholar); the Mendeley page; RamanBench Tables 3, 11, 16.
- Metric: none from the source (a descriptive study and a database for library matching): fallback `log_loss` (MET-1, MET-5); RamanBench scores macro-F1.
- Risks for /add-dataset: the cut (77) does not match the source's counts (124 RDWP, 135 identifiable, 175 in all), so rebuild from the Mendeley files and `content.xlsx` (PROV-13); the smallest kept class (PET, about 10) leaves 2-3 spectra per test fold (TP-8); standards and weathered particles in one class may record differently (LEAK-13 to check); polymer identity from a spectrum may be near-trivial (TP-4 to probe); raw spectral bins weigh against (SEL-15).
- Priority: gap + (multiclass thin), use case 0 (the use is named, the actor and decision are not), source + (paper and Mendeley deposit), shape 0 (77 spectra), risk - (cut to rebuild, a short class).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark RamanBench (https://arxiv.org/abs/2605.02003).
- as published: 77 spectra x 1,144 wavenumber features; 3 classes (raman-data id: microplastics_weathered); target: polymer type.
- Why: Identify the polymer type of naturally weathered microplastic particles from river sediments
- Notes: Raw Raman spectral bins (1,144 wavenumber points, 202-3498 cm-1) as features; SEL-15 judges such signals case by case. 3 of 10 polymer classes kept after rare-class filtering. HF mirror: https://huggingface.co/datasets/HTW-KI-Werkstatt/RamanBench/tree/main/microplastics_weathered
