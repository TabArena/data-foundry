---
unique_name: medical_charges
name: medical_charges
tags:
- 2nd Tier / Scientfic Discovery
collections:
- TabArena Reject
- TabSTAR
source_links:
- openml 42130
- openml 44146
source_row: 824
needs_review:
- suggestion
type_adapter_id: curation-record-v1
---

# medical_charges

## Comments

CC: "grinsztajn uses trivial preprocessed version. Some features should not be used for prediction. Seems to be crawled data. Most available features would not be available at inference time in a real task. Remaining features mostly strings. Likely grouped data from hospitals and providers as well. Many string features like street names requiring special preprocessing."
