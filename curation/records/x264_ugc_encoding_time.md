---
unique_name: x264_ugc_encoding_time
name: x264 performances on the YouTube UGC Dataset (input sensitivity of configurable systems)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- Non-IID (Grouped)
- AI-Filled (Verify)
original_source: Other
year: '2020'
domain: technology & internet
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.5281/zenodo.3928253
- https://doi.org/10.5281/zenodo.7675704
- https://github.com/llesoil/input_sensitivity/tree/master/data/x264
- https://github.com/llesoil/input_sensitivity/blob/master/data/x264/others/ugc_meta/all_features.csv
- https://media.withyoutube.com/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: x264 encodings of 1,397 YouTube UGC videos under 201 configurations each (about 280,800 rows) with 24 encoder options and per-video properties; the encoding-time task of the shipped `video_transcoding_time_prediction`, newer and from a documented study.
- Source: "x264 performances on the Youtube UGC Dataset", Zenodo, 2020-07-02 (doi 10.5281/zenodo.3928253, CC BY 4.0; author listed as "X", the anonymised submission): "the results of a performance analysis of x264 ... for 201 configurations and 1397 videos of the Youtube User General Content Dataset", one CSV per video (res_ugc.zip, 9.8 MB); companion data of Lesoil, Acher, Blouin, Jezequel (Univ. Rennes, IRISA), "Input Sensitivity on the Performance of Configurable Systems: An Empirical Study", Journal of Systems and Software 2023 (repository replica doi 10.5281/zenodo.7675704). Preview of one video file (Animation_360P-3e40.csv, 201 rows): `configurationID`, 24 options (`cabac`, `ref`, `deblock`, `analyse`, `me`, `subme`, `mixed_ref`, `me_range`, `trellis`, `8x8dct`, `fast_pskip`, `chroma_qp_offset`, `bframes`, `b_pyramid`, `b_adapt`, `direct`, `weightb`, `open_gop`, `weightp`, `scenecut`, `rc_lookahead`, `mbtree`, `qpmax`, `aq-mode`) and the measures `size`, `usertime`, `systemtime`, `elapsedtime` (m:ss.xx), `cpu`, `frames`, `fps`, `kbs`; per-video properties in the repository's `all_features.csv` (`WIDTH`, `HEIGHT`, `SPATIAL_COMPLEXITY`, `TEMPORAL_COMPLEXITY`, `CHUNK_COMPLEXITY_VARIATION`, `COLOR_COMPLEXITY`, three DMOS scores; the category from the file name).
- Use case: the study measures how performance depends on the input video; a video platform estimating, before the job runs, the encoding time of a new upload under a configuration (to schedule, or to pick a configuration within a time budget) is our reading, as on the sibling ("proactive load balancing"); fit approximate (one machine, short clips: `frames` is 600 in the preview). Regime grouped by video (201 rows per video; a new upload is a new group, SPLIT-29).
- Siblings and duplicates: `video_transcoding_time_prediction` (Lennart, `Yes`, shipped in BeyondArena, `Outdated`; Deneke et al. 2014, 68,784 transcodings, grouped): another source, not a duplicate (PROV-4); no other x264 record (`grep -il x264`). External collections: none of our vocabulary.
- Better data: found as better data for `video_transcoding_time_prediction`; no further search this round.
- Papers and pages: the two Zenodo records and the repository README (read); the JSS paper not read (no open copy reached).
- Metric: none found (Zenodo pages, repository README; the paper not read), so the fallback; the sibling scores a time spanning orders of magnitude with `rmsle` on the original scale (CC 2026-10-21), the same to decide here (MET-3, MET-8). Inputs: none.
- Risks for /add-dataset: one target to pick (`elapsedtime` or `usertime`) and the other measures dropped (`size`, `fps`, `kbs`, `cpu`, `systemtime` come from the same run, LEAK); a 10 ms resolution of `elapsedtime` against sub-second runs on small clips; the complexity scores are computed from the video content (SEL-13 to weigh: they describe the encoder's input, not what the video shows); the 201 configurations are a designed sample, not drawn from use (USE-8); a join of 1,397 files with the metadata.
- Priority: gap 0 (technology, regression, grouped not thin), use case 0 (our reading), source + (a journal paper with a replication package), shape + (about 280,800 rows, 1,397 groups, mixed options and video properties), no risk point (a light join only).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `video_transcoding_time_prediction`.
- as published: 1,397 YouTube UGC videos x 201 x264 configurations = about 280,800 encodings; per row 24 x264 options (cabac, ref, subme, me, bframes, rc_lookahead, mbtree, ...) plus measured size, usertime, ...; target: encoding time of a video under a configuration (elapsedtime or usertime, seconds); alternatives fps, output size; access: open.
- Why: same quantity (time to encode a video into a target format) from the same kinds of features (input video properties plus encoding parameters), known before the job runs; grouped by video like the old record
- Adds: about 4x the rows (280k vs 68,784), measured in 2020 rather than 2014, a full designed grid of 201 configurations per video on a modern encoder (x264), documented input properties and a peer-reviewed paper with replication package; the old record carries `Outdated`
