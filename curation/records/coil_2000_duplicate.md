---
unique_name: coil_2000_duplicate
name: Insurance Company Benchmark (COIL 2000)
suggestion: 'No'
decision_markers:
- Duplicate
original_source: UCI
year: '2000'
required_split:
- Random (IID)
source_links:
- https://doi.org/10.24432/C5630S
type_adapter_id: curation-record-v1
---

# Insurance Company Benchmark (COIL 2000)

## Comments

Shipped in the BeyondArena / TabArena (v0.1) collection(s).

TabArena curation verdict: Tabular.

data from users; contains zip code (maybe spatial), also grouped data as some attributes are derived from the zip code; predict if user is interested in insurance policy

Potential issue: grouped data, spatial information

Lennart: Leaning towards yes, data is looking good and its is an (old) predictive task. Need to preprocess data

Andrej: Might require split by customers, but generally looks fine

## Reference

CoIL Challenge 2000: The Insurance Company Case
By P. van der Putten, M. van Someren. 2000

Published in Sentient Machine Research, Amsterdam
