---
unique_name: ports
name: ports
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
domain: biology & life sciences
required_split:
- Random (IID)
problem_type: TBD
original_data_state: Database (or multiple to-be-joined tables)
source_row: 860
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`No Good Target / Scientific Discovery`, SEL-3, USE-2): microbial communities sampled in shipping ports, published for a biogeography study; the classifiers of port or region serve to find which taxa differ between places, not a decision.
- Source: Ghannam, Schaerer, Butler, Techtmann (2020), "Biogeographic Patterns in Members of Globally Distributed and Dominant Taxa Found in Port Microbial Communities", mSphere (10.1128/mSphere.00481-19), with the companion Schaerer et al. (2019), "Global Comparison of the Bacterial Communities of Bilge Water, Boat Surfaces, and External Port Water", AEM (10.1128/AEM.01804-19); data on GitHub rghannam/portmicrobes (GPL-3.0): ASV count and taxonomy tables as R .rds files and pm_metadata.csv (port, region, season, water chemistry); a few hundred samples from 20 ports in five regions (not counted).
- Use case: none the source states: "Here, we display how supervised machine learning approaches can be useful to understand microbial biodiversity and biogeography using microbes from globally distributed shipping ports. Our findings indicate that the members of globally dominant phyla are important for differentiating locations". The repository's random-forest port classifiers reach 0.98 to 0.995 accuracy from genus or ASV counts (data/machine_learning/model_stats/localstats.csv), near `Trivial` as well.
- Siblings and duplicates: none in `curation/records/`; external collections: none known.
- Metric: the repository reports log loss, accuracy, mean precision and recall side by side (MET-5: no unique one).
- Reject check (AI, 2026-10-22): stands. mSphere abstract (https://doi.org/10.1128/mSphere.00481-19): ML is used 'to understand microbial biodiversity and biogeography'. The full text (PMC6992368) only speculates that this 'may allow for the future prediction or classification of a geospatial location', and no actor or decision is named. The companion AEM paper (invasive bacteria on boats) concerns bilge and hull samples, not a prediction task. The port classifier reaches accuracy 0.994 on 1,218 samples x 3,214 ASVs, close to trivial. SEL-3 / USE-2.
- Collection (AI, 2026-10-22): this record is one of the environmental-metabarcoding datasets of Zschaubitz et al. 2025, "A benchmark analysis of feature selection and machine learning methods for environmental metabarcoding datasets" (CSBJ, doi 10.1016/j.csbj.2025.04.017), whose Table 1 fixes one target per dataset (a measured environmental variable such as depth, pH, temperature or a nutrient). The collection picked targets "based on an expectation that there is a correlation" to benchmark feature selection, not for a decision, and the targets are measured at sampling anyway; so the reject holds under SEL-3 and SEL-8 (reject check 6).

16S rRNA microbiome data from ports with separate OTU count and metadata tables (refs mSphere/AEM 2019). A predictive target (e.g. port/region or an environmental variable from OTU features) might be constructed, but this is microbiome scientific-discovery data with very many sparse OTU features and likely a modest sample count. It is borderline for representative tabular ML. Suggest TBD -> 2nd Tier; a human must define a meaningful target, join the count and metadata tables, and check sample size and feature representativeness.

---

16S rRNA sequences from ports; metadata source: https://github.com/rghannam/portmicrobes/tree/master/data/metadata; otu table source:https://github.com/rghannam/portmicrobes/tree/master/data/counts_taxonomy

## Reference

10.1128/mSphere.00481-19 ; 10.1128/AEM.01804-19
