---
unique_name: kick
name: kick / CAR_BAD_BUY_KICK
checked_by:
- Andrej
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
- TabSTAR
original_source: Kaggle
year: '2011'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/c/DontGetKicked/overview
- https://www.openml.org/search?type=data&id=41162&sort=runs&status=active
notebook_path: datasets/beyond_iid/temporal/kick/kick.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/kick/dataset.py
source_row: 723
type_adapter_id: curation-record-v1
---

## Comments

CC: "Is from a competition, nice tabular data task. Might require temporal split or some time-invariant feature engineering; original data has more features that are interesting (like KickDate) but unclear if this makes it temporal; kickdate only in description in data. Need to check original data for more, but likely we could ignore time and group-based problems after preprocessing the original data; likely we can ignore temporal impact. No (after preprocessing)."

Old competition without clear restriction on data usage. Can assume public domain

The competition used a random split

CC (2026-10-01, Lennart): Leak audit:
- **Split:** the temporal split stays. The Kaggle train/test split was neither temporal nor grouped: both cover Jan 2009 - Dec 2010 (test is 36-44% of every quarter), and 78.9% of test rows sit at an auction location (Auction + VNZIP1) that is also in train (72 of 128 test locations). The earlier claim that the competition grouped by Auction and VNZIP1 came from a notebook check that compared train "Auction + VNZIP1" with test "VNZIP1" only (0 overlap by construction); the curation comments are corrected. A grouped split would test unseen auctions, but a model is deployed on future purchases at mostly known auctions.
- **WheelType, potential leak kept on purpose:** missing WheelType is likely blanked when a car is kicked back: missing for 24.9% of bad buys in every month vs 1.5% of good cars, erratically (Sep-Oct 2010: 1 good vs 218 bad). Dropping WheelType/WheelTypeID: LightGBM AUC on our temporal splits 0.757 -> 0.691. Kept because the company released the data this way for the competition (missing in 4.5% of Kaggle test rows vs 4.3% of train) and the recording process is not documented. Revisit if it is.
- The note above that "the competition used a random split" is closer to the truth than the old curation comment.

## Reference

faysal, Will Adams, and Will Cukierski. Don't Get Kicked!. https://kaggle.com/competitions/DontGetKicked, 2011. Kaggle.
