---
unique_name: pbcseq
name: pbcseq
checked_by:
- Lennart
suggestion: TBD -> Yes
decision_markers:
- Duplicate
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
- TabSTAR
year: '1991'
source_links:
- https://www.openml.org/d/516
- 'Statlib (mirror: https://mldata-static.ml.tu-berlin.de/repository/data/viewslug/statlib-20050214-pbcseq/index.html)'
source_row: 616
type_adapter_id: curation-record-v1
---

# pbcseq

## Comments

CC: "Survival analysis task, likely better data exists nowadays, data collected from different sites, might require special preprocessing, might also require custom split; also temporal"

Duplicate / version of 10.24432/C5R02G, need to determine which one to use!

"The F&H data set contains only baseline measurements of the laboratory parameters. This data set contains multiple laboratory results, but only on the first 312 patients. Some baseline data values in this file differ from the original PBC file, for instance, the data errors in prothrombin time and age which were discovered after the original analysis, during research work on dfbeta residuals. (These two data points are discussed in F&H, figure 4.6.7). Another major difference is that there was significantly more follow-up for many of the patients at the time this data set was assembled."

Can only use 312 cases most likely? 

Also more clearly a strict survival task, so maybe out of scope task?

## Reference

PBC data set, as discussed in appendix D of Fleming and Harrington, Counting Processes and Survival Analysis, Wiley, 1991. An analysis based on the enclised data is found in Murtaugh PA. Dickson ER. Van Dam GM. Malinchoc M. Grambsch PM. Langworthy AL. Gips CH. "Primary biliary cirrhosis: prediction of short-term survival based on repeated patient visits." Hepatology. 20(1.1):126-34, 1994.
