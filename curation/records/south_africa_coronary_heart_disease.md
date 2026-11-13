---
unique_name: south_africa_coronary_heart_disease
name: sa-heart
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: No (Retired)
decision_markers:
- Outdated
- Selection Bias
- No Good Target / Scientific Discovery
tags:
- Tiny Data
- 'Samples: One Moment'
collections:
- TabArena Reject
original_source: Other
year: '2001'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://hastie.su.domains/ElemStatLearn/
- https://www.openml.org/d/1498
- https://www.kaggle.com/datasets/waalbannyantudre/south-african-heart-disease-dataset
notebook_path: datasets/beyond_iid/new_iid/south_africa_coronary_heart_disease/south_africa_coronary_heart_disease.ipynb
source_row: 749
type_adapter_id: curation-record-v1
---

## Comments

Kaggle version is much better described, wow!, well done

general good dataset as it seems

CC (2026-10-01, Lennart): Leak audit, kept as is with a comment in the definition. The data is a retrospective CORIS case-control sample, and ESL (2nd ed., Sec. 5.2.2, p. 148) says: "These measurements were made sometime after the patients suffered a heart attack, and in many cases they had already benefited from a healthier diet and lifestyle". So some risk factors of the cases were measured after the outcome, but this weakens sbp and obesity rather than leaking the target (dropping both: ROC AUC 0.774 -> 0.778). No duplicates or near-copies; logistic regression (AUC 0.772) beats LightGBM (0.725), as expected for a weak smooth signal.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Rousseauw et al. 1983 and ESL score no predictions; a case-control sample sets the case share by design, so a ranking metric.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `aric_incident_chd` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target ships as No/Yes, Yes the event (1 is the event).

CC (2026-11-10, Andrej): retired (`No (Retired)`, `No Good Target / Scientific Discovery`): the positives are men who had already had a heart attack. The data: 462 men of the CORIS heart-risk survey of three rural communities in the Western Cape, South Africa, as published with The Elements of Statistical Learning (ESL): 160 men who had had a heart attack and about two controls per case, with nine risk factors (blood pressure, tobacco, cholesterol, family history and others).
- **A label the man already knows:** the cases were measured some time after their heart attack, many after a healthier diet and lifestyle (ESL, 2nd ed., Sec. 5.2.2), so a model learns who has had one, not who will, and no screening decision uses it; the file has no follow-up from which to predict a first heart attack instead. As for stroke_prediction and cdc_diabetes_health_indicators.
Not changed: no `Trivial`: the published Framingham points (a heart-risk score from age, cholesterol, smoking and blood pressure), not fitted on these data, reach ROC AUC 0.748 against 0.773 for TabPFN 3.5. Decided for the case it ever returns: the source is the ESL data page (https://hastie.su.domains/ElemStatLearn/), which states no licence, and the `CC BY-SA 4.0` the definition gave is the Kaggle uploader's licence for that copy (https://www.kaggle.com/datasets/waalbannyantudre/south-african-heart-disease-dataset); the random split takes no time-basis tag, since each case's heart attack came before his measurements. Better data for the task, `aric_incident_chd` (a prospective cohort with first heart attacks), is screened in its own record.

## Reference

@article{rossouw1983coronary,
  title={Coronary risk factor screening in three rural communities. The CORIS baseline study.},
  author={Rossouw, JE and Du Plessis, JP and Benad{\'e}, AJ and Jordaan, PC and Kotze, JP and Jooste, PL and Ferreira, JJ},
  journal={South African medical journal= Suid-Afrikaanse tydskrif vir geneeskunde},
  volume={64},
  number={12},
  pages={430--436},
  year={1983}
}
