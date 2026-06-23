---
unique_name: sf_police_incidents
name: sf-police-incidents
tags:
- 2nd Tier / Scientfic Discovery
- Non-IID (Temporal)
collections:
- TabArena Reject
- TabSTAR
year: '2018'
source_links:
- openml 42732
- The dataset was downloaded on 05.11.2018. from  https://data.sfgov.org/Public-Safety/Police-Department-Incident-Reports-Historical-2003/tmnf-yvry
source_row: 845
needs_review:
- suggestion
type_adapter_id: curation-record-v1
---

# sf-police-incidents

## Comments

CC: "Interesting task, but actually requires temporal split. Could also argue that with the given features random is fine, but I believe that violent crimes may also be clustered around certain dates (i.e. due to demonstrations); moreover, the data might be biased during collection" 

Ethical problems, and we could just get a newer version
