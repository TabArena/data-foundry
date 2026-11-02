---
unique_name: openalex_journal_citedness
name: OpenAlex Sources (journals and other venues) with summary citation metrics
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target (yet)
tags:
- AI-Filled (Verify)
original_source: Website
year: '2022'
problem_type: Regression
source_links:
- https://doi.org/10.48550/arXiv.2205.01833
- https://help.openalex.org/api-entities/sources/source-object
- https://api.openalex.org/sources
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages and previews of the published tables, NOT from a built dataset. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: OpenAlex's table of sources (OurResearch, 2022), 276,534 venues of which 217,251 are journals, with an impact-factor-style `2yr_mean_citedness` that OpenAlex computes for every source itself; open and large, but nobody needs a prediction of a number the catalogue already publishes, the `No Good Target (yet)` the curator set on the JCR and SJR siblings.
- Source: Priem, Piwowar and Orr, "OpenAlex: A fully-open index of scholarly works, authors, venues, institutions, and concepts", arXiv 2205.01833 (2022): "a new, fully-open scientific knowledge graph (SKG), launched to replace the discontinued Microsoft Academic Graph"; the API's sources endpoint (276,534 sources on 2026-10-31; by type 217,251 journals, 25,054 ebook platforms, 19,850 conferences, 7,293 repositories, 6,949 book series) and the source-object documentation. As published: one nested JSON object per source with type, host organization, country, topics and topic share, is_oa, is_in_doaj, APC prices, societies, first and last publication year, works_count, cited_by_count, counts_by_year and summary_stats. The target, per the docs, is "the mean cited_by_count of the source's works published this year or in the two years before"; 92,274 journals have a value above 0.
- Use case: none. The docs call it a "journal impact factor-style measure", and OpenAlex publishes it for every source, so a librarian or funder reads it rather than predicts it (USE-2, SEL-3). The scout's reading (estimating the impact of a journal no index covers) is written by the curation and concerns venues outside OpenAlex. Regime IID over sources, or temporal by snapshot.
- Siblings and duplicates: `journal_score_jcr` (Clarivate JCR via CARTE; Lennart: `TBD -> 2nd Tier`, `No Good Target (yet)`) and `journal_score_sjr` (Scimago; the same verdict; CARTE/TARTE, MulTaBench, STRABLE) hold the same kind of target for journals from other indexes, so no duplicates (PROV-4). External collections: none for OpenAlex itself.
- Better data: found as better data for `journal_score_jcr` and `journal_score_sjr`; no further search this round.
- Papers and pages: the arXiv paper (abstract read); https://help.openalex.org/api-entities/sources/source-object.
- Metric: none found, so the fallback `rmse` (MET-1, MET-8) on a heavy-tailed target (its shipped scale is a decision for the add stage, MET-3).
- Risks for /add-dataset: works_count, cited_by_count, counts_by_year, h_index and i10_index are built from the same citations as the target and go (LEAK-10, SEL-5); the values change with every update, so a snapshot date must be fixed; many sources have no or near-zero citedness (restrict to journals with works in the window); what remains is the descriptive profile (publisher, country, topics, OA status, APC).
- Priority: gap 0, use case 0 (none), source + (a paper and API documentation), shape + (over 200,000 journals, mixed types), risk - (no target with a decision; leak columns to drop).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `journal_score_jcr`, `journal_score_sjr`.
- as published: one row per source; about 250,000 sources (count from memory, to verify; the docs give subsets: about 65,000 fully OA, 23,000 in DOAJ, 36,000 CWTS core); fields: type, publisher (host organization), ...; target: summary_stats.2yr_mean_citedness, an impact-factor-style mean citations of the works of the two prior years (or h_index); access: open.
- Why: The same quantity as the JCR impact factor (and close to the SJR score) for the same units, journals, with descriptive features of the same kind as the CARTE tables
- Adds: An open CC0 source instead of the licensed Clarivate JCR (the CARTE copy's licence is doubtful), roughly ten times the journals of JCR, yearly snapshots. Does not by itself fix the records' 'No Good Target (yet)': the use case stays thin. Leak: counts_by_year, works_count and cited_by_count nearly determine the ...
