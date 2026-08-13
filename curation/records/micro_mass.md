---
unique_name: micro_mass
name: micro-mass
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Tiny Data
- Non-IID (Grouped)
- Many class
collections:
- TabArena Reject
- TabSTAR
original_source: UCI
year: '2013'
domain: biology & life sciences
required_split:
- '?'
- Grouped (NON-IID)
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5T61S
notebook_path: datasets/beyond_iid/grouped/micro_mass/micro_mass.ipynb
source_row: 792
type_adapter_id: curation-record-v1
---

## Comments

CC: "spectral data. Clustered data. Need to check more carefully, but might be nice to include as an example for n<<d datasets"

Need to really understand the data and how we can use it, but otherwise sounds good to use!

From looking at the paper, data, and asking ChatGPT, I think we need to group by strain and hold out all replications.

20 classes.

## Reference

Mahé et al. (2014). Automatic identification of mixed bacterial species fingerprints in a MALDI-TOF mass-spectrum. Bioinformatics.

Vervier et al., A benchmark of support vector machines strategies for microbial identification by mass-spectrometry data, submitted
