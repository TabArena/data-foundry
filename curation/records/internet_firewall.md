---
unique_name: internet_firewall
name: internet_firewall
checked_by:
- Lennart
suggestion: TBD -> Yes
tags:
- Non-IID (Grouped)
collections:
- TabArena Reject
year: '2019'
source_links:
- 10.24432/C5131M
source_row: 607
type_adapter_id: curation-record-v1
---

# internet_firewall

## Comments

CC: "rejected after post-hoc analysis due to groups"
CC: ""data set was collected from the internet traffic records on a university's firewall. 4 classes. Likely temporal

Requires group split. All models perform with >.99 AUC, therefore a group split is required

""The Log
records used were taken from the Palo Alto 5020 Firewall
device used at Firat University. The receiving log record
consists of 65532 records and is obtained as a recording result
of approximately 30 seconds""""

Unclear / unsure how to create groups based on ports correctly?

## Reference

see UCI
