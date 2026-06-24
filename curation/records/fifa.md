---
unique_name: fifa
name: fifa
suggestion: 'No'
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
- Duplicate
original_source: Kaggle
year: '2022'
required_split:
- Random (IID)
source_links:
- https://www.openml.org/search?type=data&id=45012
- https://www.kaggle.com/datasets/stefanoleone992/fifa-22-complete-player-dataset
type_adapter_id: curation-record-v1
---

# fifa

## Comments

Imported from the TabArena curation workbook.

TabArena curation verdict: Artificial/Simulated.

FIFA data on football/soccer players; not originally intended for predictive task; from a game database; unclear if attributes really determine wage; wage comes from different source 

rtificial. Dataset was scraped from fifa games. Initially we thought the wage (target) was from a different source and that the task makes sense if we want to predict real life wages based on fifa stats. However, also the wage is from fifa and all the features are defined using some internal deterministic system, which makes it not a real task.

Potential issue: not a predictive task

Lennart: not an original predictive task, but I could imagine this being used in such a way

Andrej: Not a predictive task, but there might be value in analyzing more accurate predictions

Duplicate of `fifa_players` (same FIFA player data).

## Reference

Kaggle (2021). Fifa 22 complete player dataset. https://www.kaggle.com/datasets/ stefanoleone992/fifa-22-complete-player-dataset.
