---
unique_name: spotify_tracks_dataset
name: Spotify Tracks Dataset
checked_by:
- Lennart
- Mustafa
- Alex
data_foundry_status: Suspended
suggestion: TBD -> 2nd Tier
decision_markers:
- Wrong Domain / Source Modality
- Data Quality Issue
- No Good Target (yet)
- Time-series (Classification)
tags:
- Larger IID Data
- Many class
- Free Text (Sentences)
collections:
- New (BeyondArena)
- TexTabBench
- CARTE/TARTE
original_source: Kaggle
year: '2022'
domain: technology & internet
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset
source_row: 511
type_adapter_id: curation-record-v1
---

# Spotify Tracks Dataset

## Comments

This data does not include any original audio data but already gives preprocessed features, which is problematic, but we can work with it.

Also note that the track IDs appear multiple times, need to check what kind of duplicates these are.

The task of predicting the genre is closer to training an embedding model than a real classifier, but given the high-level features, it could be seen as the prediction head on top of such an embedding model that also includes artist metadata.
Also note that the genre is not really the real genre of the track (based on some real-world tag or human expertise), and instead an artifact from the scraping of the data https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset/discussion/374642#2222338 
So, at best, this represents a noisy labeling.
This also explains why the track IDs are not unique, as one track can appear in multiple genres! https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset/discussion/374642#3400868
I conclude that we should not use track ID but instead need to look for our own alternative label. Hence, let us keep this as TBD for now and revisit it later. 

Time_signature column seems wrong (https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset/discussion/374642#3036205)

## Reference

https://doi.org/10.34740/kaggle/dsv/4372070
