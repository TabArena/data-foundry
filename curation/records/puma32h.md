---
unique_name: puma32h
name: puma32H
suggestion: 'No'
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
year: '?'
required_split:
- Random (IID)
problem_type: Binary Classification
source_links:
- https://www.openml.org/search?type=data&id=752
type_adapter_id: curation-record-v1
---

# puma32H

## Comments

Imported from the TabArena curation workbook.

TabArena curation verdict: Artificial/Simulated.

Regression. Simulation of robot arm control. Not a tabular data task; maybe a deterministic formula exists to compute the accelaration -> "Number of inputs 32 degree of non-linearity (fairly linear or non-linear) amount of noise in the output (moderate or high)."

Potential issue: Simulated (but might be alright), control task

Lennart: Simulated, but likely a real random variable. If deterministic, no.

Andrej: Simulated

## Reference

Luis Torgo
