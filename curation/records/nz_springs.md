---
unique_name: nz_springs
name: nz_springs
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
tags:
- Many features
- AI-Filled (Verify)
collections:
- New (BeyondArena)
year: '2018'
domain: biology & life sciences
required_split:
- Random (IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_row: 859
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`No Good Target  / Scientific Discovery`, SEL-3): a microbial biogeography survey of 925 New Zealand geothermal springs, published to find what drives community composition; the candidate targets (temperature, pH) are measured on site with a probe, so no decision needs them predicted.
- Source: Power et al., "Microbial biogeography of 925 geothermal springs in New Zealand", Nature Communications 9:2876, 2018 (doi 10.1038/s41467-018-05020-y), the 1000 Springs Project. As published: 1,019 water samples from 974 features in 18 fields, 925 springs after QC; 46 physicochemical parameters (ICP-MS metals, nitrogen species, H2S, sulfate, conductivity, DO, ORP, pH, turbidity, temperature in situ); 16S rRNA reads in ENA (PRJEB24353); metadata on 1000springs.org.nz; the record's OTU table and metadata came "via email from Matthew Stott".
- Deciding words (paper, abstract and aim): "We measured bacterial and archaeal community composition, 46 physicochemical parameters"; "We determined that diversity is primarily influenced by pH at temperatures <70 °C"; the study's aim is "to determine factors that influence biogeographical patterns". The methods are correlational (Mantel, PERMANOVA, ANOSIM, constrained correspondence analysis, edgeR); no predictive model is trained or validated. The paper only remarks that geochemistry "could be predictive of community composition".
- Use case: none; temperature and pH are read with a thermocouple and a handheld meter at sampling, and predicting a community from chemistry is the discovery question itself (SEL-3, USE-2).
- Siblings: none in `curation/records/`.
- Metric: none (no prediction task in the paper).
- Doubt for the reject-checker: a framing "predict community diversity from the 46 parameters" could be argued; it still has no actor or decision.
- Reject check (AI, 2026-10-22): stands. Power et al. 2018 (https://pmc.ncbi.nlm.nih.gov/articles/PMC6056493/) set out 'to determine factors that influence biogeographical patterns' with correlational methods only. No predictive task is published. The candidate targets (temperature, pH) are measured on site, so no actor's decision needs them predicted (SEL-3, USE-2). I found no later predictive use of the 1000 Springs data.
- Collection (AI, 2026-10-22): this record is one of the environmental-metabarcoding datasets of Zschaubitz et al. 2025, "A benchmark analysis of feature selection and machine learning methods for environmental metabarcoding datasets" (CSBJ, doi 10.1016/j.csbj.2025.04.017), whose Table 1 fixes one target per dataset (a measured environmental variable such as depth, pH, temperature or a nutrient). The collection picked targets "based on an expectation that there is a correlation" to benchmark feature selection, not for a decision, and the targets are measured at sampling anyway; so the reject holds under SEL-3 and SEL-8 (reject check 6).

Sampling of New Zealand geothermal springs with metadata (temperature 13.9-100.6C, pH <1-9.7) plus a microbial OTU/16S count table (Nature Communications 2018, doi 10.1038/s41467-018-05020-y). A regression target such as temperature or pH from the OTU/metadata features is conceivable, but this is microbiome scientific-discovery data with very many (sparse OTU) features and an unclear, possibly small sample count. It leans toward scientific discovery rather than a representative tabular task. Suggest TBD -> 2nd Tier; a human must confirm the sample size after joining tables, the intended target, and whether OTU features make it representative.

---

Sampling of NZ geothermal springs with lots of metadata and a good range (13.9–100.6 °C and pH < 1–9.7); metadata source: via email from Matthew Stott; otu table source: from Matthew Stott

## Reference

10.1038/s41467-018-05020-y
