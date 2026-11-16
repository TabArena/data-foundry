---
unique_name: sorel_20m_malicious_pe
name: 'SOREL-20M: Sophos-ReversingLabs 20 million Windows PE malware dataset'
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 2
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
- Many features
original_source: Company
year: '2020'
domain: technology & internet
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://github.com/sophos/SOREL-20M
- https://arxiv.org/abs/2012.07634
v2_path: datasets/_dev/tabarena-v0pt2/sorel_20m_malicious_pe_1m/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-08):** `TBD -> Yes`, priority 2: Sophos and ReversingLabs' 19.4M Windows PE files of 2017-2019 with first-seen times, a recommended time split and the 2,381 EMBER v2 features, the largest public table for static malware detection; 97% of the vector is hashed bins or histograms of the file, and the labels come from undisclosed internal sources.
- Source: Harang and Rudd (Sophos AI), "SOREL-20M: A Large Scale Benchmark Dataset for Malicious PE Detection", arXiv 2012.07634 (14 December 2020, read in full); code and README at github.com/sophos/SOREL-20M; data in the public S3 bucket `s3://sorel-20m/09-DEC-2020/` ("The SOREL-20M S3 bucket is public, so no credentials are required", README; its Terms and Conditions of Use PDF is noted only, EV-4). As published (Sec. 2): `meta.db`, a SQLite index with the sha256, `is_malware`, the first-seen time `rl_fs_t`, vendor detection counts and behaviour tags (token counts); the `ember_features` LMDB with one EMBER v2 vector per file; the `pe_metadata` LMDB (pefile dumps, about 480 GB); 9,919,251 disarmed malware binaries and no benign ones ("Benign files are excluded due to potential intellectual property concerns", Sec. 5). Files first seen from 1 January 2017 to 10 April 2019; the recommended time split gives 12,699,013 training, 2,495,822 validation and 4,195,042 test files (Sec. 1), of them 7,596,407 / 962,222 / 1,360,622 malicious and 5,102,606 / 1,533,579 / 2,834,441 benign (Table 1): 19,389,877 files, 51.2% malicious.
- The task's table: one row per file, 19,389,877 x 2,381 EMBER v2 values, target `is_malware`, time `rl_fs_t` (less the files whose features could not be extracted, a list in the repository); above the 1M row cap, so a `_1m` version. Download for it: `meta.db` 3.79 GB and `ember_features/data.mdb` 76.9 GB (S3 listing, 2026-11-08); the npz arrays in `lightGBM-features/` hold the same features, 172 GB.
- Use case: a security vendor's static detector decides whether a newly seen PE file is malicious and blocks it, at a low false-alarm rate (Sec. 1: commercial models, evaluation "at lower false positive rates (1 in 1000 or below)"); fit approximate: the setting is mirrored, but the labels come from "a combination of non-public, internal information as well as a number of static rules and analyses" (README FAQ), a construction we cannot check (USE-5). Regime temporal: the source splits by the first-seen time in ReversingLabs telemetry, so the test files are newer than the training files (SPLIT-19).
- Siblings and duplicates: `ember2024_malware_detection` (this run; the EMBER authors, VirusTotal files of 2023-2024, 3.2M files, EMBER v3): the same task from another source with other files, no duplicate (PROV-4); `microsoft_malware_prediction` (this run) predicts infection per machine from telemetry, another task. EMBER 2017 and 2018 have no record (grep: sorel, sophos, ember, malware). External collections: none of ours.
- Better data: none searched (found by the data-scouting run of 2026-11-08); in passing, `ember2024_malware_detection` holds the same task on newer files (2023-2024) but six times fewer, its own record.
- Papers and pages: the arXiv paper; the README and its FAQ; Anderson and Roth, "EMBER" (arXiv 1804.04637) and `ember/features.py` for the feature definition; Joyce et al. 2025 (EMBER2024, Table 1) list SOREL (20M) among the public 1M+ file sets.
- Metric: none fixed. The paper shows ROC curves (Figs. 4-6) and argues for scores at false positive rates of "1 in 1000 or below", a range rather than one operating point (MET-7), so the fallback `roc_auc` (MET-8); a partial AUC up to FPR 1e-3 is a context option for the curator (MET-11); inputs none.
- Risks for /add-dataset: of the 2,381 values, 1,708 are hashed bins (imports 1,280, section properties 250, exports 128, header strings 50) and 608 are histograms of the raw bytes (byte 256, byte-entropy 256, printable characters 96); about 65 are recorded file, header and data-directory fields (`ember/features.py`). These are computed encodings of a raw object, the CLEAN-24 question by analogy, but no benign binary ships, so the vector is the only representation; a hashed bin mixes several import or section names. The detection counts and tags in `meta.db` are label-side and leave (LEAK-10); 80 GB of LMDB to convert.
- Priority: gap 0 (technology & internet, binary and temporal not thin), use case 0 (the actor is clear, the fit approximate for the undisclosed labels), source + (paper, README, code, public bucket), shape + (19.4M dated files x 2,381), risk - (encodings of the raw file, undisclosed labelling, a newer sibling in `ember2024_malware_detection`).

Found by the data-scouting run of 2026-11-08 for the large-datasets review (wide tables outside biology and medicine, and tables with 2M+ rows).

CC (2026-11-08, Lennart): accepted for adding (`Yes`) in the screening review of the large candidates, round 2, together with ember2024_malware_detection: the same task (static detection of Windows PE files) from another source, and neither is better data (SOREL-20M: 19.4M files of 2017-2019, vendor labels, EMBER v2 features; EMBER2024: 2.9M files of 2023-2024, open VirusTotal labels, EMBER v3 features), so both enter (principles.md, Tensions: same task, another source).

**Assessment (AI, 2026-11-09):** review panel (full): ship after changes (made: the sample's text corrected, prefix 0 is 48.9% malicious against 50.5% for the release with about 40k extra benign training files from SHA-ordered batches of Jul-Aug 2017 and Jun-Jul 2018, test windows unaffected, EV-1; the feed rhythm of first_seen named in fit_reason, USE-8; the stated 0 and late values of header_coff_timestamp noted as kept, CLEAN-10; proposed: accept dataset_missing_value_sentinel, CLEAN-10; rebuttal round skipped, the briefs agreed on every fact); disputed: EV-1/USE-8 (the sample prefix), MET-5/MET-10/MET-11 (ROC AUC against partial AUC at max_fpr=1e-3, with SPLIT-10's gap), USE-6/USE-8 (first_seen to the minute); for the curator: issues 1-5. Priority 2: gap 0, use case 0, source +, shape +, risk - (use case: fit approximate, the 2-4 detection grey zone absent and the class mix set by collection; shape: 1.25M rows, 2,322 features; risk: unpublished labels, a SHA-ordered benign batch in the oldest train side, ROC AUC near ceiling).
