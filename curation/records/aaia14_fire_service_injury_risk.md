---
unique_name: aaia14_fire_service_injury_risk
name: 'AAIA''14 Data Mining Competition: key risk factors for Polish State Fire Service'
checked_by:
- AI (UNVERIFIED)
data_foundry_status:
- WIP (Triage)
claimed_by: Lennart
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
tags:
- AI-Filled (Verify)
source_links:
- https://fedcsis.org/2014/aaia/dm_awards.html
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-08):** `No` (`No Good Target / Scientific Discovery`, SEL-3): the data poses "does this post-action EWID report record a casualty", a label its author already knows, and the source says the attributes that predict it serve post-incident analysis, not the safety of firefighters or victims.
- Source: AAIA'14 Data Mining Competition "Key risk factors for Polish State Fire Service" on Knowledge Pit (FedCSIS 2014), Janusz et al., ACSIS vol. 2, pp. 345-354 (doi 10.15439/2014F507, read in full); data from the State Fire Service's EWID incident reports. As published: about 50,000 reports x 11,852 attributes (Knowledge Pit; the paper: the number of distinct words of the narrative "plus several hundreds of attributes from the quantitative part", Sec. III), attributes identified by integer ids; three labels (injured firefighters, children, other civilians; positive rates about 0.004, 0.007 and 0.059).
- Use case: none the table mirrors. A report is submitted "by Incident Commander ... after a fire and rescue action" (Sec. I, p. 345), and the three labels were distinguished from the same reports (Sec. III, p. 348). The predictive attributes describe the injury itself: nouns for the injured parties, and attribute-section fields such as `action_people_evacuation`, `localizing_people`, `oxygen_therapy`, `hospital_name` (Sec. IV.A, Table I). The source: these attributes "can be useful for a post-incident analysis of the causes ... However, those terms alone do not reveal any specific risk factors ... The knowledge resulting from the identification of those attributes does not have a direct impact on the safety of firefighters and incident victims" (p. 351); their named use is information retrieval (SEL-9).
- Rules: SEL-3 / USE-2 (no decision fits the task the data poses); SEL-8 (the original task was feature selection for risk-factor discovery, scored by a fixed Naive Bayes ensemble's AUC minus a size penalty, Sec. III); USE-3 / LEAK-10 (the report is written after the action and both its narrative and attribute fields describe the injury; no common prediction point can be rebuilt from unnamed attribute ids: LEAK-10's retire clause). USE-12 does not apply: the on-scene decision support the source hopes for (the ICRA project, Sec. IV.D) is future work, not the task this table mirrors. The reject-checker read the paper in full and confirmed the reject on these grounds (2026-11-08).
- Note: the data host challenge.mimuw.edu.pl times out and no archived copy of the files was found (recorded, not a reason; EV-7).
- Reopen if: a release with named attributes and a codebook that marks which attribute-section fields exist at alarm or arrival (a new record for an injury-risk task at dispatch).

Found by the data-scouting run of 2026-11-08 for the large-datasets review (wide tables outside biology and medicine, and tables with 2M+ rows).
