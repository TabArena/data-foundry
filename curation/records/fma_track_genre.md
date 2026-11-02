---
unique_name: fma_track_genre
name: 'FMA: A Dataset for Music Analysis (fma_metadata: tracks.csv, features.csv, echonest.csv)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 3
decision_markers:
- Wrong Domain / Source Modality
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
original_source: Other
required_split:
- Grouped (NON-IID)
problem_type: Multiclass Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://arxiv.org/abs/1612.01840
- https://github.com/mdeff/fma
- https://os.unil.cloud.switch.ch/fma/fma_metadata.zip
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 3: a peer-reviewed genre dataset with artist-set labels and one row per track, but its features are audio summaries and its authors built it for models on the audio itself, so the modality doubt of `spotify_tracks_dataset` holds here too.
- Source: Defferrard, Benzi, Vandergheynst, Bresson, "FMA: A Dataset for Music Analysis", ISMIR 2017 (arXiv 1612.01840, first version December 2016); data and code at https://github.com/mdeff/fma. As published: 106,574 tracks of 16,341 artists and 14,854 albums, 161 genres of which 16 are roots; `fma_metadata.zip` (342 MiB, CC BY 4.0): tracks.csv (per-track metadata: title, artist, album, genres, tags, listens), genres.csv, features.csv (518 librosa statistics per track), echonest.csv (Echo Nest audio features for 13,129 tracks); subsets small (8,000 tracks, 8 balanced genres), medium (25,000 tracks, 16 unbalanced top genres), large and full (106,574 tracks); 47% of tracks carry a single top genre (paper, Table 2).
- Labels: the genres are "annotated by the artists themselves ... they might be inconsistent and motivated by factors not necessarily objective, such as achieving a higher play count" (Sec. 2.4).
- Use case: a music archive or streaming service tagging an uploaded track with its genre ("a classification system enables end users to search for the types of music they are interested in", Sec. 3.1); fit approximate, since the service has the audio. Regime grouped by artist: the paper's split keeps "artists to be part of one set only, thus avoiding any artist and album effect" (Sec. 2.7).
- Siblings and duplicates: `spotify_tracks_dataset` (Lennart, Mustafa, Alex: `TBD -> 2nd Tier`, DF: Suspended, `Wrong Domain / Source Modality`, `No Good Target (yet)`; a scraped genre per search query): another source, not a duplicate (PROV-4); `yearprediction_the_million_song_dataset` (`No`, a recommendation challenge). External collections: none found.
- Better data: found as better data for `spotify_tracks_dataset`; no further search this round.
- Papers and pages: the paper; the WWW 2018 challenge on the audio clips, "Learning to Recognize Musical Genre from Audio" (Defferrard et al., arXiv 1803.05337).
- Metric: the paper reports test accuracy of LR, kNN, SVM and MLP per feature set for the top genre on the medium subset, best 63% (SVM on MFCC plus spectral contrast, and on all 518 features; Table 6), as "a lower-bound and an indication of the task's difficulty": one baseline table, not a decision's metric, so the fallback `log_loss` (MET-5, MET-6, MET-8); the 2018 challenge's metric was not read.
- Risks for /add-dataset: SEL-12: the features summarise the audio, and the authors meant the audio for its own models ("A major motivation to construct this dataset was to enable the use of the powerful DL set of techniques to music analysis", Sec. 3.2); the Echo Nest columns cover only 13,129 tracks; listens, favorites and comments accrue after upload (LEAK for a new track); no top genre when a track's genres span several roots; the split by artist.
- Priority: gap + (multiclass thin), use case 0 (approximate), source + (ISMIR paper, CC BY metadata), shape + (25,000 tracks in medium, about 50,000 with a top genre; 518 features plus metadata; grouped), risk - (audio-derived features, the parent's modality doubt).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `spotify_tracks_dataset`.
- as published: 106,574 tracks of 16,341 artists, 161 genres in a hierarchy (16 top-level; fma_medium: 25,000 tracks with one of 16 top genres); features.csv: 518 librosa summary statistics per track; echonest.csv: ...; target: top-level genre of a track (genre_top), multiclass; access: open.
- Why: the same task as the record (genre from precomputed audio features and track metadata) with a real label: genres set by the artists on the Free Music Archive, not the search-query artefact that makes the record's label noisy and its track IDs repeat (the record's `No Good Target (yet)`)
- Adds: a traceable genre label and one row per track, a genre hierarchy, a peer-reviewed source; the Echo Nest subset has the same kind of audio features as the record. Older (2017) and the features are still derived from audio, so the record's `Wrong Domain / Source Modality` concern applies the same way
