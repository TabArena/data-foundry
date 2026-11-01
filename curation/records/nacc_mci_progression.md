---
unique_name: nacc_mci_progression
name: 'NACC Uniform Data Set: MCI progression / diagnosis'
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- AI-Filled (Verify)
source_links:
- https://naccdata.org
- https://doi.org/10.64898/2026.03.13.26347938
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Duplicate`, PROV-4, PROV-6): the same NACC Uniform Data Set as `nacc_uds_dementia_conversion`; stable against progressive MCI at three years is the MCI slice of that record's conversion target and adds no distinct task.
- Source: the NACC Uniform Data Set (Beekly et al. 2007, https://doi.org/10.1097/WAD.0b013e318142774e), requested through naccdata.org, this record's first link ("56,000+" participants, "217,000+" visits). The record's second link, Kohli et al., "AutoML-Multiverse ...", medRxiv 2026 (https://doi.org/10.64898/2026.03.13.26347938; the curator's Zotero item 133), is a paper that used the data, not its source (PROV-10, PROV-12): "two independent cohorts studying Alzheimer's disease progression (ADNI, N≤1,930; NACC, N≤1,057)", with "stable versus progressive mild cognitive impairment (MCI) classification accuracy was 0.68±0.06 (ADNI) and 0.63±0.08 (NACC)" (abstract).
- Siblings and duplicates: `nacc_uds_dementia_conversion` (this run, `TBD -> Yes`) names the same source with its first publication, and its target, "clinical diagnosis (normal / MCI / dementia) at the next visit, i.e. conversion", contains MCI-to-dementia progression. A slice of the same cohort with another horizon is a duplicate when it adds no distinct task (PROV-6, as `arsenic_male_lung` to `arsenic_male_bladder`). The binary framing and the Zotero item are written into `nacc_uds_dementia_conversion` as its alternative framing.
- Better data: found as better data for `tadpole`; the canonical record is `nacc_uds_dementia_conversion`.
- Reject check (AI, 2026-10-31): stands. Both end at the NACC Uniform Data Set (naccdata.org; Beekly et al. 2007). The paper behind this record uses NACC only as a cohort: 'two independent cohorts studying Alzheimer's disease progression (ADNI, N≤1,930; NACC, N≤1,057)', with stable versus progressive MCI at '0.63±0.08 (NACC)' (abstract, https://medrxiv.org/lookup/doi/10.64898/2026.03.13.26347938). Stable against progressive MCI is the MCI rows of the kept record's conversion target with a fixed horizon, for the same memory-clinic decision, and nacc_uds_dementia_conversion already carries it as its binary alternative. Note: the abstract states no horizon, so '3-year' is the scout's reading.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `tadpole`; the curator's Zotero collection, item 133: "AutoML-Multiverse: An Instability-Aware Framework for Quantifying Analytic Variability ...".
- as published: participants of US ADRCs, tens of thousands longitudinal; the paper uses up to 1,057 per task (clinical/cognitive, MRI, CSF); target: stable vs progressive MCI at 3-year follow-up (or diagnosis CN/MCI/AD); access: request.
- Why: the large multi-centre US cohort next to ADNI; the paper uses it as an independent replication cohort
- Adds: a second Alzheimer cohort besides ADNI/TADPOLE; access by data request and DUA
