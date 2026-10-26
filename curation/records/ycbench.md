---
unique_name: ycbench
name: ycbench
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- TBD
- Too Small
tags:
- AI-Filled (Verify)
original_source: Github
year: '2026'
required_split:
- '?'
problem_type: TBD
source_links:
- https://www.ycbench.com/
- https://arxiv.org/abs/2604.02378
- https://github.com/benstaf/ycbench
source_row: 1041
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 1: the source is now known (an arXiv paper and a GitHub repo), but it is a live forecasting leaderboard over one Y Combinator batch of 196 startups, scored as a top-k ranking on a composite web-traction score; tiny and of doubtful target.
- Source: Mostapha Benhenda, "YC Bench: a Live Benchmark for Forecasting Startup Outperformance in Y Combinator Batches", arXiv 2604.02378 (April 2026), code and data at https://github.com/benstaf/ycbench; the site (https://www.ycbench.com/) says "YC Bench is a live benchmark to forecast the top 10% Y Combinator startups at Demo Day". As published: the YC W26 batch, 196 startups; files `yc_w26_startups.csv`, `yc_mentions.csv`, `yc_mentions_early.csv`, `yc_w26_traction.csv`, `yc_w26_pre_demo_scores.csv`, `yc_all_companies.json`; the target is the "Pre-Demo Day Score", "a short-term proxy metric that combines public traction signals and Google web mentions"; the baseline ranks by pre-application Google mentions.
- Use case: investors "Identify and access hot deals before Demo Day" (site); fit approximate (the label is a web-visibility proxy measured over 90 days, not an investment outcome); regime: cohort-relative, one batch, so a grouped-by-batch or temporal setup only once several batches exist.
- Siblings and duplicates: none (grep ycbench, Y Combinator). External collections: none found.
- Papers and pages: the arXiv paper (abstract read, text not), the README, the site.
- Metric: precision@20 (70%) and recall@11 (55%) of the Demo Day top performers (abstract, README): a ranking cut-off, not one of our task metrics, so the fallback if the task were kept (MET-5, MET-6); inputs: the batch, as a group.
- Risks for /add-dataset: 196 rows and about 11-20 positives (TP-5, `Too Small`); the label is a composite of the same public signals that would serve as features (SEL-5, LEAK); a top-k-within-cohort framing close to ranking (SEL-9); a live benchmark whose ground truth is published after the predictions, by design for LLM forecasters.
- Priority: gap 0, use case 0 (a proxy label), source + (paper and code), shape - (196 rows, one batch), risk - (proxy target built from the features).

The record only gives the name 'ycbench' and a link to ycbench.com, with no comments, collection, problem type, target, or size. It is not a Zindi competition and I have no reliable knowledge of what ycbench contains or whether it is a tabular predictive task. There is too little information to decide, and the criteria say not to reject solely for missing info. A human must open the source and determine the task type, target, modality, and size before any verdict; provisionally 2nd Tier.
