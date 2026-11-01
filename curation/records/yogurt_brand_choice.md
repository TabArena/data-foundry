---
unique_name: yogurt_brand_choice
name: Yogurt scanner panel brand choice (Jain, Vilcassim and Chintagunta 1994)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Outdated
tags:
- AI-Filled (Verify)
original_source: Other
year: '? (1994)'
domain: business & marketing
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://jhelvy.github.io/logitr/reference/yogurt.html
- https://doi.org/10.1080/07350015.1994.10524547
- https://cran.r-project.org/package=mlogit
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: 2,412 yogurt purchases of 100 households in Springfield, Missouri, from a 1994 scanner-panel study, with each brand's price and newspaper feature and the chosen brand as the target; a real revealed-preference panel, but small, dated, with eight marketing inputs of one kind and a signal that sits in household history.
- Source: Jain, Vilcassim and Chintagunta, "A Random-Coefficients Logit Brand-Choice Model Applied to Panel Data", Journal of Business & Economic Statistics 12(3):317-328, 1994 (doi 10.1080/07350015.1994.10524547 by Crossref; the record's earlier link ...10524546 resolves to another JBES article, Cai's "A Markov Model of Switching-Regime ARCH", and was replaced). The rows are distributed in R: logitr "Raw data downloaded from the package mlogit v0.3-0 by Yves Croissant", and Ecdat `Yogurt`; where they were first published (a journal data archive or the authors) was not found. As published (Ecdat copy previewed): 2,412 rows x 10 columns: `id` (100 households), `feat.<brand>` and `price.<brand>` for yoplait, dannon, hiland and weight (Weight Watchers), and `choice`; dannon 970, yoplait 818, weight 553, hiland 71 (in 26 households); 4 to 185 occasions per household (median 15); rows sorted by household, no date. logitr: "2,412 choice observations" by 100 households in Springfield, Missouri, over about two years.
- Use case: a retailer or a manufacturer predicts which brand a household buys on its next trip, given the shelf prices and features, to target promotions; the paper's aim is to estimate the heterogeneity of preferences and of the response to marketing (abstract on RePEc: ignoring it "results in a downward bias in the parameter estimates of the marketing variables"), so the decision is ours and the fit approximate. Regime: the TFM paper holds out purchase occasions of known households (its abstract: "medium-data regime (10--40 purchase occasions per consumer)"), an order within each household; no timestamp ships, so whether the row order within a household is the time order has to be confirmed (SPLIT-7, SPLIT-22), and a split on new households drops the history that carries the signal (USE-10).
- Siblings and duplicates: no other record holds this data (grep by yogurt, brand choice, mlogit, scanner). The other choice record is `london_passenger_mode_choice` (not screened yet). External collections: none (the R packages mlogit, Ecdat and logitr carry it).
- Better data: from the curator's Zotero collection (item 228); no further search this round (the run's note names larger licensed panels, the IRI Academic Dataset and NielsenIQ Homescan via Kilts, not checked).
- Papers and pages: Jain et al. 1994 (abstract read on RePEc; the text is paywalled and was not read, PROV-17); Liu and Zhang, "Tabular Foundation Models for Discrete Choice Estimation" (https://arxiv.org/abs/2607.13314, 2026; abstract read: "individual-level heterogeneity encoding is the dominant driver of predictive accuracy").
- Metric: the 1994 paper is a likelihood estimation (its evaluation not read); the TFM paper reports "holdout log-likelihood and hit rate" side by side, so no unique original (MET-5), and the fallback `log_loss` on the four brands is the holdout log-likelihood both use. Inputs: the household id, when the split is within households.
- Risks for /add-dataset: the household's past choices carry the signal, so features from earlier occasions must be built without the test occasion, and a model on prices and features alone must beat each household's own brand shares (TP-10; LEAK on lagged targets); Hiland has 71 occasions in 26 households (TP-5, TP-8 per fold); the period and the store coverage are in the paper's data section, not read; Ecdat describes the rows as "a cross-section" of "individuals" (PROV-15: they are purchase occasions of 100 households).
- Priority: gap + (multiclass is thin), use case 0 (an estimation paper; the decision is ours), source + (a peer-reviewed paper; the data maintained in R packages), shape 0 (2,412 occasions, but 100 households and eight inputs of one kind), risk - (a household-history signal and a row order to confirm; dated, `Outdated`).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 228: "Tabular Foundation Models for Discrete Choice Estimation".
- as published: 2,412 purchase occasions by 100 households in Springfield, Missouri, about two years (1980s); per occasion, price and a newspaper-feature flag for each of 4 brands (9,648 rows in long format); target: brand chosen (Dannon, Yoplait, Weight Watchers, Hiland; 4 classes, shares 40/34/23/3%); access: open.
- Why: A classic real revealed-preference panel with a clear target, household grouping and a time order
- Adds: A discrete-choice marketing task with a household-grouped or temporal split. Caveats: small and dated, with few features, and the signal sits mostly in household history. Larger modern scanner panels (IRI Academic Dataset, NielsenIQ Homescan via Kilts) need registration or a licence and were not checked.
