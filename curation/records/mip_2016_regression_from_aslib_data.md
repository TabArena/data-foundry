---
unique_name: mip_2016_regression_from_aslib_data
name: MIP-2016-regression from aslib_data
checked_by:
- Lennart
suggestion: TBD -> 2nd Tier
tags:
- Non-IID (Grouped)
collections:
- TabArena Reject
- TabSTAR
year: '2016'
source_links:
- openml 43071
- http://miplib.zib.de/ also see https://github.com/coseal/aslib_data/tree/master/MIP-2016
source_row: 696
type_adapter_id: curation-record-v1
---

# MIP-2016-regression from aslib_data

## Comments

CC: "algorithm runtime performance data. Was part of a challenge. Sounds good. But it seems as if there were repeated evaluations of the same algorithm, so might require a group split. Algorithm selection data genearlly requires / assumes a group-based split w.r.t to the instances "

We already have two datasets from AsLib, we can add more later if we really want to. 
Moreover, for these the task is a bit unclear as they treat multi-label as regresison task but it is hard to know if that is the optimal solution (instead of pairwise, etc). We could incldue all kinds of version in the future, but again, too much of the same might add a negatie bias

## Reference

Part of Open Algorithm Challenge 2017 ("Mira").
