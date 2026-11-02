---
unique_name: wastewater_treatment
name: wastewater_treatment
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
tags:
- Many features
- AI-Filled (Verify)
collections:
- New (BeyondArena)
year: '2019'
domain: biology & life sciences
problem_type: Other
original_data_state: Database (or multiple to-be-joined tables)
source_row: 864
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`No Good Target / Scientific Discovery`, SEL-3): a global microbiome survey of wastewater plants published to explain diversity and biogeography, with no prediction target.
- Source: Wu et al. (Global Water Microbiome Consortium), "Global diversity and biogeography of bacterial communities in wastewater treatment plants", Nature Microbiology, 13 May 2019 (doi 10.1038/s41564-019-0426-5); as published: 16S rRNA OTU tables "from ~1,200 activated sludge samples taken from 269 WWTPs in 23 countries on 6 continents" (http://gwmc.ou.edu/data-disclose.html) and plant metadata in SI Table 1, to be joined.
- The task: none. The abstract frames the study as discovery: "the diversity of microorganisms and the factors that control it are poorly understood"; it reports a core community "strongly linked to activated sludge performance" and that turnover "appears to be largely driven by stochastic processes"; "Our findings enhance our mechanistic understanding of the global diversity and biogeography of activated sludge bacterial communities within a theoretical ecology framework". No target, no prediction.
- Siblings and duplicates: none in `curation/records/`.
- Metric: none.
- Doubt to weigh: SI Table 1 may hold plant performance (removal rates) that a task could predict from the microbiome; that would be a new task of ours on a sparse, very wide OTU table, not the source's. The old `Not Representative` marker is dropped.
- Reject check (AI, 2026-10-22): stands. Original task (SEL-8) is discovery: Wu et al., Nature Microbiology 2019 (https://doi.org/10.1038/s41564-019-0426-5), "Our findings enhance our mechanistic understanding of the global diversity and biogeography of activated sludge bacterial communities". The collection's own target (Zschaubitz et al. 2025, CSBJ, Table 1, https://pmc.ncbi.nlm.nih.gov/articles/PMC12049816/) is 'avg. temp' / 'Continent' on 687 samples x 66,743 OTUs: quantities measured at sampling, predicted by no one, the same pattern as tara_oceans, bog_lakes, ports (stand today). Nothing sets wastewater apart: a plant-performance target from SI Table 1 would be our own new task, not the source's. SEL-3 (Must).

A global microbiome study: 16S rRNA OTU tables from ~1,200 activated-sludge samples across 269 WWTPs in 23 countries (Nature Microbiology 10.1038/s41564-019-0426-5), joined with metadata. This is an OTU abundance table — extremely high-dimensional and sparse, used for ecological/scientific discovery rather than a standard real-world tabular predictive task, and not representative of typical tabular ML. There is no clear, defensible predictive target out of the box. It should be rejected as scientific-discovery / not representative, though a human could confirm no usable target (e.g., continent/process type) is salvageable.

---

A systematic global-sampling effort, analysing the 16S ribosomal RNA gene sequences from ~1,200 activated sludge samples taken from 269 WWTPs in 23 countries on 6 continents.; metadata source: SI Table 1; otu table source: http://gwmc.ou.edu/data-disclose.html

## Reference

10.1038/s41564-019-0426-5
