---
unique_name: ringnorm
name: ringnorm
suggestion: 'No'
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
year: '1996'
required_split:
- Random (IID)
problem_type: Binary Classification
source_links:
- https://www.openml.org/search?type=data&id=1496
type_adapter_id: curation-record-v1
---

# ringnorm

## Comments

Imported from the TabArena curation workbook.

TabArena curation verdict: Deterministic.

Class 1 has mean zero and covariance 4 times the identity. Class 2 has mean (a,a,..a) and unit covariance. a = 2/sqrt(20). Breiman reports the theoretical expected misclassification rate as 1.3%.

Potential issue: Artificial

Lennart: not a real distribution

Andrej: Artificial

## Reference

http://www.cs.toronto.edu/~delve/data/ringnorm/desc.html
