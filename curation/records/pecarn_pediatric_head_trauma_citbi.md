---
unique_name: pecarn_pediatric_head_trauma_citbi
name: PECARN Identification of Children at Very Low Risk of Clinically Important Brain Injuries after Head Trauma (public-use dataset)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- AI-Filled (Verify)
original_source: Other
year: '2012'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.1016/S0140-6736(09)61558-0
- https://pecarn.org/datasets/
- https://pecarn.org/studyDatasets/documents/TBIPUDDocumentation_000.pdf
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: 42,412 children with minor blunt head trauma at 25 North American emergency departments, the history and examination recorded before imaging, and clinically important brain injury as the outcome; the cohort behind the PECARN head-CT rule.
- Source: Pediatric Emergency Care Applied Research Network (PECARN); Kuppermann et al., "Identification of children at very low risk of clinically-important brain injuries after head trauma: a prospective cohort study", Lancet 374:1160-1170 (2009; PubMed abstract read, the full text returned 403): 42,412 analysed (derivation 8,502 under 2 years and 25,283 aged 2 and older; validation 2,216 and 6,411), CT in 14,969 (35.3%), ciTBI in 376 (0.9%), neurosurgery in 60. Public-use dataset with "Documentation and Data Dictionary for the Public Use Dataset-Release Date April 2012" (read 2026-10-31): one row per patient (`PatNum`, "A randomly generated number"), about 125 variables: the form's author and the mechanism (`EmplType`, `InjuryMech_Recat`, `High_impact_InjSev`), history (amnesia, loss of consciousness, seizure, headache, vomiting), GCS components, mental status, skull-fracture signs, haematoma, neurological deficits, other injuries, CT indications (`CTForm1`, `Ind*`, `CTSed*`), age, sex, ethnicity, race, `Observed`, `EDDisposition`, CT results (`CTDone`, `EDCT`, `PosCT`, `Finding1` to `Finding23`), the outcome components (`DeathTBI`, `HospHead`, `HospHeadPosCT`, `Intub24Head`, `Neurosurgery`) and the target `PosIntFinal`. The public file includes children "regardless of GCS score" (the rule used GCS 14-15), so its row count may differ from 42,412; no site or date column.
- Use case: an emergency physician decides whether a child with minor head trauma gets a head CT, from the history and examination at presentation (documentation: the rules "identified children at very low risk of clinically important traumatic brain injuries (TBI) for whom CT scans can routinely be obviated"); fit direct; regime IID (no site or date in the public file; the study's derivation and validation split is not marked in the dictionary, to confirm).
- Siblings and duplicates: `regensburg_pediatric_appendicitis` (`Yes`, a pediatric emergency diagnosis, another task); `crash_head_injury_outcome` (unscreened: adults with significant head injury, outcome at six months, another task). No other PECARN record (grep: pecarn, head trauma, brain injur). External collections: none found here (whether the imodels package ships it was not checked; the web search budget was used up).
- Better data: a related task next to `regensburg_pediatric_appendicitis`; no further search this round. PECARN's blunt abdominal trauma set (12,044 children, the scout's count) is a sibling cohort with another task.
- Papers and pages: the Lancet paper; the PECARN datasets page (pecarn.org/datasets).
- Metric: the source reports the rules' sensitivity and negative predictive value at their operating point (abstract), the hard decision of a published rule, not a threshold or cost fixed for a new model; the derivation's misclassification cost was not read (full text 403). So the fallback `roc_auc` (MET-6, MET-8), unless the paper fixes a cost ratio (MET-7), to check.
- Risks for /add-dataset: drop the CT decision and everything after it (`CTForm1`, `Ind*`, `CTSed*`, `Observed`, `EDDisposition`, the CT results and findings, the outcome components; LEAK-10); the hospitalization criterion needs "TBI on CT", so a child without a CT can be positive only through death, neurosurgery, intubation or the follow-up (a verification gap in the label, USE-5); 0.9% positives, about 75 per fifth of the data; access by request with a three-year Research Data Use Agreement, IRB approval or exemption, and destruction of copies after three years (pecarn.org/datasets; noted only, EV-4).
- Priority: gap 0 (medical, binary, IID not thin), use case + (the CT decision, documented), source + (Lancet paper, PECARN data dictionary), shape + (about 42,000 children, about 100 mixed predictors), risk 0.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through a related task next to `regensburg_pediatric_appendicitis`.
- as published: 42,412 children enrolled at 25 North American emergency departments, 2004-2006 (PECARN datasets page); one row per child with the history and examination findings recorded before imaging. Columns ...; target: Clinically important traumatic brain injury (death, neurosurgery, intubation over 24 hours or hospital admission of 2 nights or more for TBI); access: request (request form and a three-year Research Data Use Agreement from the PECARN data centre).
- Why: A different pediatric emergency-department diagnosis task with a strong prospective multi-centre source and a decision someone acts on; the same kind of setting as the appendicitis record (clinical findings at presentation, decide on imaging or surgery).
- Adds: About 54 times more children than the appendicitis set, prospective collection across 25 sites, a widely used published rule as baseline. PECARN also offers the blunt abdominal trauma set (12,044 children, intra-abdominal injury needing intervention) as a sibling.
