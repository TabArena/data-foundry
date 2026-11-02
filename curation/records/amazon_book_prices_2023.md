---
unique_name: amazon_book_prices_2023
name: Amazon Reviews 2023, item metadata of the Books category (meta_Books)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target (yet)
tags:
- AI-Filled (Verify)
year: '2024'
domain: business & marketing
problem_type: Regression
source_links:
- https://arxiv.org/abs/2403.03952
- https://amazon-reviews-2023.github.io/
- https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: the Books item metadata of Amazon Reviews 2023 (4.4M items, a price "at time of crawling"), the target of `book_price_prediction` on far more and newer books. The source published it for recommendation, so the price task is our framing of an item attribute, left to the curator against the recsys precedents (Consistency check below).
- Proposed reject (refuted): `No` (`Out-of-scope Task (CTR/RecSys/Ranking)`, SEL-9, SEL-8): Amazon Reviews 2023 is published for recommendation and retrieval, "Standard data splits to encourage RecSys benchmarking" (data card), and the book-price regression re-frames a metadata field, the case `yearprediction_the_million_song_dataset` settled. Reject check (AI, 2026-10-31): refuted. The source's words fix its purpose, but SEL-9 bars recommendation, ranking and CTR targets, and a book's price is an item attribute with an actor (a seller pricing a listing). The curators keep that task on `book_price_prediction` (`TBD -> Yes`, Lennart and Mustafa), and SEL-2 lets the use case decide; stretching the yearprediction case ("Of course not real") to a target with an accepted use case is a reading.
- Source: McAuley Lab (UC San Diego), Amazon Reviews 2023 (https://amazon-reviews-2023.github.io/, https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023); Hou, Li, He, Yan, Chen and McAuley, "Bridging Language and Items for Retrieval and Recommendation: Benchmarking LLMs as Semantic Encoders" (arXiv 2403.03952, v1 2024-03-06), whose benchmark covers "sequential recommendation, collaborative filtering, and product search". As published: 571.54M reviews, May 1996 to September 2023; Books 10.3M users, 4.4M items, 29.5M ratings; the item file `meta_Books.jsonl` (14.7 GB), one row per item: title, subtitle (format and date), author, average_rating, rating_number, features, description, `price` ("Price in US dollars (at time of crawling)"), images, videos, store, categories, details (publisher, language, pages, ISBNs, weight, dimensions); "Note that some items lack metadata"; no licence stated. A 2 MB preview (the first 527 items): 497 carry a price, 26 of them 0.0 (Kindle editions among them), median 13.50; mostly paperbacks and hardcovers, some Kindle, `Buy a Kindle` and `Audible Audiobooks` items.
- Use case: a publisher or seller pricing a book when listing it, from its metadata; the source names none, so the use case is ours (USE-1), the one MachineHack posed for `book_price_prediction`. Fit approximate: the crawled price may be a marketplace or used-copy offer rather than a list price, and the ratings accrue after listing. Regime: one crawl; IID, or temporal by the publication date in `details`, to decide.
- Siblings and duplicates: `book_price_prediction` (Lennart and Mustafa, `TBD -> Yes`, `No Good Target (yet)`; MachineHack 2019, 6,237 training rows), `amazon_bestseller_price` (this run, `TBD -> 2nd Tier`, priority 1); the recsys re-framings rejected: `yearprediction_the_million_song_dataset` (Lennart, `No`) and `hm_article_buyer_age` (this run, `No`, SEL-9 and SEL-8, reject check stood). No duplicate (PROV-4). External collections: none for this cut.
- Better data: found as better data for `book_price_prediction`; no further search this round.
- Papers and pages: the project page, the Hugging Face card, arXiv 2403.03952 (abstract).
- Metric: none for the price (the paper scores recommendation and retrieval), so the fallback `rmse` on a log-scaled price, scored on the price scale (MET-3); inputs none.
- Risks for /add-dataset: what "Price in US dollars (at time of crawling)" is (a list price, a marketplace or used offer; Kindle against print; the 0.0 values); how many Books items have a price over the whole file; drop `average_rating` and `rating_number`, which accrue after listing (LEAK-10); whether title and description dominate (SEL-12); the snapshot year (PROV-9); whether it replaces `book_price_prediction` as better data for the task.
- Priority: gap 0, use case 0 (written by the curation), source + (a lab paper and data card document the crawl), shape + (millions of books, mixed types: format, publisher, pages, dates, categories, text), risk - (unclear price, post-listing rating columns).

**Consistency check (AI, 2026-10-31):** `yearprediction_the_million_song_dataset` (Lennart: "Real task was recsys. Otherwise, the version that created a different task are just fake / duplicates") and `hm_article_buyer_age` (`No`, this run) reject a target re-framed from recommendation data; this record keeps one. What sets it apart? (a) The AI's best guess: a book's price has an actor and an accepted record of the task (`book_price_prediction`, `TBD -> Yes`), the song year and the buyer age have neither; keep it as second tier on that fact. (b) Treat it like yearprediction: `No`, SEL-8 and SEL-9, and then ask the same of `book_price_prediction`'s better data. (c) Amend SEL-8 to say whether an item attribute of a recommendation release, with a use case of its own, is in scope.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `book_price_prediction`.
- as published: Books: 4.4M items with reviews (some lack metadata; how many carry a price not counted), meta_Books.jsonl 14.7 GB; one row per book: title, subtitle (format and date, e.g. 'Hardcover - Import, ...; target: price in US dollars at crawl time; access: open (Hugging Face and the project page; no licence stated).
- Why: same target (a book's retail price) and the same kinds of inputs as MachineHack's (title, author, edition and format, rating and rating count, genre and category, synopsis)
- Adds: hundreds of times more books than MachineHack's 6,237 training rows, newer (2023 crawl against 2019), a citable academic source with the crawl documented, plus publisher, pages and publication date. Caveats: price is missing for some items and may be a marketplace or used-copy offer (the first record, a 2004 ...
