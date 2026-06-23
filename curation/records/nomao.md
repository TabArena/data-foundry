---
unique_name: nomao
name: nomao
checked_by:
- Lennart
suggestion: TBD -> 2nd Tier
decision_markers:
- Wrong Domain / Source Modality
- NLP (Text)
collections:
- TabArena Reject
- TabSTAR
source_links:
- 10.24432/C53G79
- openml 1486
source_row: 591
type_adapter_id: curation-record-v1
---

# nomao

## Comments

CC: ""UPDATE: The data was actually extracted from a table with text columns [Name, Phone, Address, GPS], i.e.: [La poste, 3631, 13 Rue De La Clef 59000 Lille France, (50.64, 3.04)]. The available samples are bivariate comparisons, but likely already filtered for obvious cases. Most features are extracted from text.

Deduplication task. Instances compare two spots. Might be clustered data as different labeling methods were used to label dthe data, although most were simply labeled by humans. TabRepo results show very low errors for all models; taks sounds not like a predictive task? ""

## Reference

Laurent Candillier and Vincent Lemaire. Design and Analysis of the Nomao Challenge - Active Learning in the Real-World. In: Proceedings of the ALRA : Active Learning in Real-world Applications, Workshop ECML-PKDD 2012, Friday, September 28, 2012, Bristol, UK.
