---
unique_name: fda_device_covid19_serology
name: Device COVID-19 Serology
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
tags:
- AI-Filled (Verify)
collections:
- STRABLE
source_links:
- https://open.fda.gov/apis/device/covid19serology/
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/device-covid19serology
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`No Good Target / Scientific Discovery`, SEL-3; USE-2): the US government's independent evaluation of COVID-19 antibody tests against fixed reference panels of samples of known status; the label is the panel's reference truth, known before any test runs, and STRABLE itself finds the table a look-up task.
- Source: "Independent Evaluations of COVID-19 Serological Tests", on openFDA since 2020-06-05 (open.fda.gov/about/updates). "Independent testing by US Government Laboratories" (the Frederick National Laboratory for Cancer Research, NCI, or the CDC); each test was evaluated against Panel 1 to Panel 4, each of "frozen SARS-CoV-2 antibody-positive serum samples (n=30) and antibody-negative samples (n=80)", the panel designed "to enable a laboratory-based evaluation" (open.fda.gov/apis/device/covid19serology). 13,420 rows, one per device evaluation and sample, 31 fields with the device's `igg_result`, `igm_result`, `iga_result`, `pan_result`, the sample's `group` ("Positives," "Negatives," "HIV+") and `antibody_truth`, "The true qualitative antibody presence result" (open.fda.gov/fields/devicecovid19serology.yaml). STRABLE: the same 13,420 rows, 11 columns, the IgG and IgM readings and `group` dropped; `iga_result` and `pan_result` are NA on 99% and 89% of rows.
- Why no task: the table scores devices against a reference whose status is fixed by the panel's design; nobody predicts `antibody_truth` for a panel sample (USE-2, SEL-3), and what remains with the device readings is each device's sensitivity and specificity, the evaluation's own subject. STRABLE, App. C.2, item 26: "Each row is one test device applied to one serum sample from a fixed reference panel", and "Under row-level i.i.d. splits, this table behaves as a look-up task" (also `Trivial`, TP-4).
- Siblings and duplicates: the other STRABLE FDA records are other tasks; no other record of serology test evaluations. External collections: STRABLE.
- Metric: none found (the openFDA page and field reference; STRABLE's AUROC, App. D.1, is benchmark-wide).
- Reject check (AI, 2026-10-31): stands. openFDA: the panels were built 'to enable a laboratory-based evaluation and to provide reasonable estimates and confidence intervals for test performance' (https://open.fda.gov/apis/device/covid19serology/), and STRABLE App. C.2 item 26: 'Since every device is evaluated on the same reference samples, the label is almost fully determined by the pair (panel, sample number)' (https://arxiv.org/html/2605.12292v2). The truth is fixed by the panel's design. With the sample ids dropped, what remains is the device's own result, i.e. its sensitivity, the evaluation's subject. `Trivial` is dropped: TP-4 needs our own fold-by-fold proof, and a statement by another benchmark is no evidence (EV-4).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 13,420 rows x 11 columns incl. target (STRABLE parquet); target: antibody_truth.
- Why: Predict whether a reference serum sample truly contains SARS-CoV-2 antibodies from a test device's result row
- Notes: The paper itself flags it as a look-up task: every device is evaluated on the same reference panel, so the label is almost fully determined by (panel, sample number) under row-level IID splits.
