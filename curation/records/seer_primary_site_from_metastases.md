---
unique_name: seer_primary_site_from_metastases
name: 'SEER Research Data (Incidence 1975-2023): primary site from metastasis sites at diagnosis'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Selection Bias
tags:
- AI-Filled (Verify)
original_source: GOV Website
domain: medical & healthcare
problem_type: Multiclass Classification
source_links:
- https://seer.cancer.gov/data/
- https://seer.cancer.gov/data-software/documentation/seerstat/nov2024/seerstat-variable-dictionary-nov2024.pdf
- https://seer.cancer.gov/data/access.html
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: the NCI's population registry records the sites of distant metastasis at diagnosis since 2010 (six sites since 2016), so the primary site can be predicted from the spread, histology, age and sex in a large, recent cohort. Histology codes that name the organ are the main risk.
- Source: National Cancer Institute, SEER Program, "SEER Research Data" (seer.cancer.gov/data, read 2026-10-31): cases diagnosed 1975-2023 from registries "covering approximately 45.9 percent of the U.S. population", accessed through the SEER*Stat application after registration and acknowledging the SEER Research Data Use Agreement. The SEER*Stat variable dictionary of the November 2024 submission lists "SEER Combined Mets at DX-bone (2010+)", "-brain", "-liver" and "-lung" (from NAACCR items 2851 for 2010-2015 and 1112 from 2016), "Mets at DX-Distant LN (2016+)" (item 1114) and "Mets at DX-Other (2016+)" (item 1117), marked as available in the Research database and in case listings (read from a text extraction of the PDF; to confirm). Site recode, histology, age, sex, race and year of diagnosis are standard fields. Rows not counted: the metastatic subset needs SEER*Stat.
- Use case: an oncologist facing metastases decides where to look for the primary tumour and which work-up or therapy to start, from where the metastases are, the histology, age and sex. Fit approximate, as for `ljubljana_primary_tumor`: the rows are patients whose primary was found, not the cancers of unknown primary the decision is about (`Selection Bias`). Regime IID or temporal by year of diagnosis, to decide.
- Siblings and duplicates: `ljubljana_primary_tumor` (`Yes`, 339 Ljubljana patients of the 1980s, `Selection Bias`, fit approximate since 2026-10-27) is the same task from another source, so its own record (PROV-4). `seer_breast_cancer_survival` and `seer_breast_cancer_5y_survival` (unscreened) draw on the same registry for another task (PROV-7). External collections: none known.
- Better data: found as better data for `ljubljana_primary_tumor` (the data-scouting run of 2026-10-30/31); no further search.
- Papers and pages: the SEER data and access pages; the SEER*Stat variable dictionary (November 2024).
- Metric: none found (SEER publishes statistics and no prediction task; the Ljubljana papers report accuracy only, and `ljubljana_primary_tumor` declares the fallback), so the fallback `log_loss` (MET-1, MET-8); inputs none.
- Risks for /add-dataset: ICD-O-3 histology codes such as hepatocellular, renal cell or ductal carcinoma name the organ, so ship histology in the broad groups a metastasis biopsy gives (adenocarcinoma, squamous, small cell, ...) or the task comes close to `Trivial` (TP-4). The lymph-node and "other" sites start in 2016, so use 2016 onward for all six sites. The grouping of site recodes into classes, and rare sites (TP-8). The Research file has only the year of diagnosis. The agreement's terms on sharing are to be read before shipping (no criterion, EV-4).
- Priority: gap + (multiclass thin), use case 0 (approximate, as for `ljubljana_primary_tumor`), source + (NCI SEER, variable dictionary), shape + (likely tens of thousands of metastatic cases or more, mixed types), risk - (organ-naming histology codes; size not counted).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `ljubljana_primary_tumor`.
- as published: Tumours from population registries covering about 45.9% of the US population; the variables 'SEER Combined Mets at DX-bone/brain/liver/lung (2010+)', 'Mets at DX-Distant LN (2016+)', 'Mets at ...; target: Primary site (site recode), among patients with distant metastases at diagnosis; access: registration.
- Why: Same task as ljubljana_primary_tumor (primary site from the sites of spread, histologic type, age and sex), features of the same kind known at diagnosis
- Adds: Population-based and recent (2010-2023) instead of 339 Ljubljana patients of 1980s; caveats: fewer metastasis sites (6 against 13), same selection (primary found), and the SEER data agreement forbids redistribution, so shipping it needs a check
