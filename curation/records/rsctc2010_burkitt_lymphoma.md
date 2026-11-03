---
unique_name: rsctc2010_burkitt_lymphoma
name: OpenML-1083 mouseType
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
tags:
- AI-Filled (Verify)
- Tiny Data
- Many features
collections:
- TabBench-Bio
original_source: Other
year: '2010'
domain: medical & healthcare
problem_type: Multiclass Classification
source_links:
- http://tunedit.org/challenge/RSCTC-2010-A
- https://www.openml.org/d/1083
- https://arxiv.org/abs/2609.07441
- https://www.openml.org/d/1084
- https://www.openml.org/d/1088
- https://doi.org/10.1007/978-3-642-13529-3_4
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: three DNA-microarray class sets of the RSCTC 2010 Discovery Challenge on OpenML in one record; the Burkitt set's classes match the expression signature of Hummel et al. 2006 (a label computed from the arrays), mouseType's classes are undocumented, and the three sets come from three different studies.
- Source: the RSCTC 2010 Discovery Challenge on TunedIT (Wojnarski et al. 2010, "RSCTC'2010 Discovery Challenge: Mining DNA Microarray Data for Medical Diagnosis and Treatment", LNCS 6086, pp. 4-19; paywalled and not read; the tunedit.org page is dead). OpenML (uploaded 2014-10-07, "Source: Unknown - Date unknown"): "Data from the RSCTC 2010 Discovery Challenge. All datasets contain between 100 and 400 samples ... All attributes are numeric and represent measurements from DNA microarrays. Attributes are normalized in some way". As published, target `Decision`: 1083 mouseType 214 x 45,101 (the probe count of the Mouse 430 2.0 array), 7 classes (69 to 13 rows); 1084 BurkittLymphoma 220 x 22,283 (HG-U133A), 3 classes (128, 48, 44); 1088 variousCancers_final 383 x 54,675 (HG-U133 Plus 2.0), 9 classes (155 to 16).
- Burkitt: GEO GSE4475 (Hummel et al. 2006, NEJM 354:2419-2430, PMID 16760442): "Gene expression profiling employing Affymetrix GeneChips (U133A) was performed in 220 mature aggressive B-cell lymphomas ... The molecular Burkitt lymphoma signature identified 44 cases." The OpenML shape and its smallest class (44) match, so the three classes are likely molecular Burkitt, intermediate and non-molecular Burkitt from that signature: a match by counts, stated neither by OpenML nor by the challenge.
- Use case: the type of a lymphoma or tumour from an expression array, as the challenge's title has it; for Burkitt, telling Burkitt lymphoma from DLBCL, which decides the chemotherapy. Fit approximate at best; regime IID (one array per patient presumed, not checked).
- Siblings and duplicates: `gcm_multiclass_cancer` (Global Cancer Map, 2001 arrays), `ova_breast` (GEMLeR, from expO on U133 Plus 2.0; variousCancers_final is on the same array and may share samples, a PROV-4 check), `brca_breast_cancer` (`No`, SEL-4). The three OpenML sets are three source studies, so three datasets (PROV-7), not versions; the record's name (mouseType) and its unique name (Burkitt) disagree. External collections: TabBench-Bio (OpenML 1083, 1084 and 1088 all enabled).
- Better data: a candidate of the benchmark TabBench-Bio (the run searched no further).
- Papers and pages: Wojnarski et al. 2010 (not read); Hummel et al. 2006 (abstract and GSE4475 summary read); https://www.openml.org/d/1083, https://www.openml.org/d/1084, https://www.openml.org/d/1088.
- Metric: the challenge's measure is not confirmed (paper paywalled, TunedIT gone; recalled as balanced accuracy, unverified); TabBench-Bio ranks by macro-F1 (Sec. 3.5). Unless the challenge's measure is confirmed, the fallback `log_loss` (MET-8).
- Risks for /add-dataset: the Burkitt labels may be computed from the same arrays (SEL-5 and `Trivial`, or SEL-4): confirm from GSE4475's sample characteristics; mouseType's classes and series are unknown (PROV-2, PROV-1 after a search); values "normalized in some way" across the challenge's files (LEAK-30); 2006-era arrays (`Outdated`); split the record into one per OpenML set before adding.
- Priority: gap + (multiclass is thin), use case 0, source 0 (the challenge paper not read, OpenML names no source), shape 0 (214 to 383 rows), risk - (a likely computed label).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 214 x 45,101; target: Decision (7 classes).
- Why: Class from DNA microarray profiles (RSCTC 2010 Discovery Challenge set; class meaning not documented on OpenML) | Lymphoma class from DNA microarray profiles (RSCTC 2010 Discovery Challenge set) | Cancer type from DNA microarray profiles (RSCTC 2010 Discovery Challenge set)
- Notes: Source on OpenML: 'Data from the RSCTC 2010 Discovery Challenge' (Wojnarski et al., RSCTC 2010, LNCS 6086); the tunedit link is dead and the underlying GEO series is not named. | Same RSCTC 2010 provenance gap as mouseType; the underlying GEO series is not named on OpenML. | Same RSCTC 2010 provenance gap as mouseType.
