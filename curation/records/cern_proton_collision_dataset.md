---
unique_name: cern_proton_collision_dataset
name: CERN Proton Collision Dataset
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
tags:
- 2nd Tier / Scientific Discovery
- AI-Filled (Verify)
collections:
- New (BeyondArena)
domain: physics & astronomy
problem_type: Other
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/fedesoriano/multijet-primary-dataset
- http://opendata.cern.ch/record/1000 / http://opendata.cern.ch/record/553
source_row: 832
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`No Good Target / Scientific Discovery`, SEL-3): the example output of a CMS analysis tool that "computes the razor variables MR and Rsq" for real MultiJet events; no label and no task, and the computed variables are functions of the row's megajets.
- Source: CERN Open Data Portal record 554, Javier Duarte, 2015 (data 2010 RunB, parent /MultiJet/Run2010B-Apr21ReReco-v1/AOD; good-run list record 1000), CC0: "Example CSV output file for SUSYBSMAnalysis-RazorFilter", "computes the razor variables MR and Rsq, used in supersymmetric particle searches", 21,726 events; the CSV "can be used in online applications" (a histogram tool). Columns Run, Lumi, Event, MR, Rsq, the four-vectors of two megajets, HT, MET, nJets, nBJets. Kaggle copy by fedesoriano (2020, "CERN Proton Collision Dataset") repeats it, no task. The record's second link (record 1000 / 553) is the good-run list and parent dataset, not this file.
- Use case: none; real collision data has no truth label, and MR and Rsq are kinematic functions of the megajet four-vectors and MET (Phys. Rev. D 90, 112001), so a regression on them is close to a formula (SEL-5).
- Siblings and duplicates: `cern_electron_collision_data` (same uploader, same verdict proposed); `higgs`, `susy`, `hepmass` are simulations, a different case.
- Metric: none (no task is defined anywhere).
- Physics is a thin domain; the gap does not create a target.
- Reject check (AI, 2026-10-22): stands. CERN record 554 (https://opendata.cern.ch/record/554): 'Example CSV output file for SUSYBSMAnalysis-RazorFilter' that 'computes the razor variables MR and Rsq'; CSV meant for the online histogram tool. Real collision data with no label; MR/Rsq are kinematic functions of the row (SEL-3, SEL-5).

CERN Open Data multijet (proton collision) primary dataset of measured jet/event kinematics. As with the electron-collision data, this is particle-physics scientific-discovery measurement data with no canonical supervised predictive target, and any derived target risks being a deterministic function of the kinematic inputs. It is not a representative real-world tabular classification/regression task. A human should confirm the absence of a usable target before rejecting, but the description supports a No.
