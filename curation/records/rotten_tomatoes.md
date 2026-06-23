---
unique_name: rotten_tomatoes
name: Rotten Tomatoes
checked_by:
- Lennart
suggestion: TBD -> 2nd Tier
decision_markers:
- No Good Target (yet)
tags:
- Free Text (Short)
collections:
- CARTE/TARTE
source_links:
- https://sites.google.com/site/anhaidgroup/useful-stuff/the-magellan-data-repository?authuser=0 / https://huggingface.co/datasets/inria-soda/carte-benchmark
- https://www.rottentomatoes.com/
source_row: 489
type_adapter_id: curation-record-v1
---

# Rotten Tomatoes

## Comments

Contain information on movies that can be found in Rotten Tomatoes movie rating website

Again, predicting rating might not translate / be usable with such features in the real-world. So very artificial / not a real dataset. Furthermore, mostly an entity matching problem. Also again collected by thest students via web scraping

name, directors, actors, creators and description. for directores actors and creators makes sense to swap with stats, as for the name not sure how informative it's, what's left is description

The description is mostly a blurb and not much more.

## Reference

https://dl.acm.org/doi/10.14778/2994509.2994535
