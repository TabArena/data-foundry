---
unique_name: bank8fm
name: bank8FM
suggestion: 'No'
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
year: '?'
required_split:
- Random (IID)
problem_type: Binary Classification
source_links:
- https://www.openml.org/search?type=data&id=725
type_adapter_id: curation-record-v1
---

## Comments

Imported from the TabArena curation workbook.

TabArena curation verdict: Artificial/Simulated.

Other variant: bank32h. Very low TabRepo test errors, All NNs beat trees, and the data is simulated - It is likely that there is some kind of leak. Also a custom split was given, maybe that would have prevented a leakage?; has customers and banks multiple times, maybe requires group-based splits

Potential issue: Simulated (but might be alright); Sounds deterministic from the description

Lennart: Simulated/Likely deterministic funciton

Andrej: Simulated

## Reference

https://www.cs.toronto.edu/~delve/index.html
