---
unique_name: vcbench_founder_success
name: 'VCBench: founder success prediction'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: Website
year: '2025'
domain: finance
problem_type: Binary Classification
source_links:
- https://vcbench.com
- https://arxiv.org/abs/2509.14448
- https://huggingface.co/datasets/vela-research/VCBench
- https://arxiv.org/abs/2604.00339
- https://github.com/ihlamury/vcbench
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: VCBench, 9,000 anonymised profiles of US founders (companies mostly founded 2010-2018) built from LinkedIn and Crunchbase, success being an exit or IPO above 500M USD or more than 500M USD raised; a real investor-screening task with a leaderboard (F0.5), but only 4,500 labelled profiles are released, the job lists carry no dates, and the data is on request.
- Source: Chen, Ternasky, Kwesi, Griffin, Yin, Salifu, Amoaba, Mu, Alican, Ihlamur (Vela Research), "VCBench: Benchmarking LLMs in Venture Capital", arXiv 2509.14448 (v1 2025-09-17, v2 2026-05-05); site https://vcbench.com ("Request the dataset"); Hugging Face card https://huggingface.co/datasets/vela-research/VCBench (the repository holds only the card; licence "vcbench-research-terms": "Each requester agrees not to distribute or republish it", a term, EV-4). As published (paper, §3 and §4): 9,000 profiles, 810 successful (9%); "Most companies were founded in the U.S. between 2010 and 2018"; a founder is unsuccessful without an exit, IPO or large follow-on funding "within eight years of founding"; structured JSON per founder (educations_json: degree, field, QS ranking; jobs_json: role, company size, industry, duration; IPOs and acquisitions grouped; 61 industry clusters) plus an `anonymized_prose` rendering of the same fields; names, companies, locations and dates removed (§4.3.1), job dates turned into duration buckets (§4.3.2); an LLM flags and unifies strings but does not generate fields (§4.2, §4.3.2); 4,500 released with labels, 4,500 held for the private leaderboard (§6.0.5).
- Use case: a venture investor screens founders at company inception to decide whom to back; the metric weights precision because "false positives are more costly than false negatives" (§6); fit direct for the decision, the inputs approximate (undated job histories); regime IID (the source's random public and private halves; founding years are removed, so no temporal split) (SPLIT-3).
- Siblings and duplicates: no record holds founder or venture data (grep by vcbench, founder); external collections: none in our vocabulary.
- Better data: from the curator's Zotero collection (item 157, Ihlamur 2026); no further search this round.
- Papers and pages: Chen et al. 2025 (nine LLMs; the market index at 1.9% precision, Y Combinator about 1.7x and tier-1 firms about 2.9x that); Ihlamur, "When Career Data Runs Out: Structured Feature Engineering and Signal Limits for Founder Success Prediction" (arXiv 2604.00339, 2026: 28 engineered features with XGBoost stumps, validation F0.5 0.303; the prose is "a lossy re-encoding" of the JSON); repository https://github.com/ihlamury/vcbench (not read).
- Metric: the leaderboard ranks by F0.5, "which weights precision twice as heavily as recall" (paper §6; vcbench.com), a leaderboard metric on hard labels (MET-4), so F0.5 with the threshold chosen on the training side, a custom metric shipped with the dataset (MET-13); inputs none.
- Risks for /add-dataset: the job list may hold the founded company itself or later jobs, with a company size that may be as of collection (LEAK: a grown company's size gives the label away; dates are gone, so check by role and duration); prior IPOs and acquisitions must precede the founding (LEAK); the 9% success rate is enriched against the 1.9% market base (a sampled class mix, no marker by the pattern); nested JSON to flatten; the prose column re-encodes the same fields as text (drop, SEL-12); the profiles derive from personal LinkedIn data, anonymised (keep them local); request access (EV-4).
- Priority: gap 0 (finance has 15), use case + (the source names the investor and the decision), source + (arXiv paper with a data section, a site and a card), shape + (4,500 labelled founders, categorical, ordinal and count fields), risk - (a likely leak through company size and undated jobs).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 157: "When Career Data Runs Out: Structured Feature Engineering and Signal Limits for Founder ...".
- as published: 9,000 anonymised founder profiles (4,500 public labelled, 4,500 private test); structured JSON (jobs, education, prior IPOs/acquisitions) plus generated prose; 9% positive; target: Founder success: company exit or IPO above $500M valuation, or more than $500M raised (binary); access: request (research terms, no redistribution or republication).
- Why: A real, documented finance/VC task with a public leaderboard (F0.5) Risks: no redistribution (likely blocks shipping); the profiles are derived from personal LinkedIn data; part of the input is LLM-generated prose.
- Adds: Venture-capital screening, a domain the benchmark lacks
