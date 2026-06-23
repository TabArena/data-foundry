---
unique_name: ova_breast
name: OVA_Breast
checked_by:
- Lennart
suggestion: TBD -> Yes
decision_markers:
- Missing source information
- Data Quality Issue
- Needs extensive data wrangling
tags:
- New IID
collections:
- TabArena Reject
- TabSTAR
year: '2010'
source_links:
- openml 1128, 1166, 1140
- GEMLeR (down http://gemler.fzv.uni-mb.si/, paper https://pmc.ncbi.nlm.nih.gov/articles/PMC2896709/)
- https://euhubs4data.eu/datasets/know-center-gmbh-gemler/
- AP_Colon_Kidney, AP_Breast_Kidney, AP_Breast_Ovary
- 'way back machine: https://web.archive.org/web/20160309223905/http://gemler.fzv.uni-mb.si/'
source_row: 602
type_adapter_id: curation-record-v1
---

# OVA_Breast

## Comments

CC: "Need to inspect relation to other OVA datasets. >10K features Not in TabRepo, No, if truly consitsing of 4 datasets. Moreover preprocessing unclear; generally misisng inforamtion; not matching description from paper; domain expert needed"


"GEMLeR datasets are divided in two sections - "one-versus-all" (OVA) and "all-paired" (AP) benchmarking datasets."
Unclear why OVA and not just multiclass prediction task, sounds like a better idea?
Needs manual work to undon OVA problems and recover original samples, but not that much

Can we get all 9 original classes/datasets labels back from OpenML backup: 
 OVA_Breast: 1128, OVA_Colon 1161, OVA_Endometrium 1142, OVA_Kidney 1134, OVA_Lung 1130, OVA_Omentum 1139, OVA_Ovary 1166, OVA_Prostate 1146, OVA_Uterus 1138

We only have the "small" data with 10k features after unsuperivsed feature selection from the original 50k. original source is lost and 10k makes sense to use in the application as far as I would say.

## Reference

Stiglic, G., & Kokol, P. (2010). Stability of Ranked Gene Lists in Large Microarray Analysis Studies. Journal of biomedicine biotechnology, 2010, 616358.
https://onlinelibrary.wiley.com/doi/10.1155/2010/616358
