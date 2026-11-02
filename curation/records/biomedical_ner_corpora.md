---
unique_name: biomedical_ner_corpora
name: bc5chem, bc5disease, chemdner, ncbi_disease, nlmchem
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- NLP (Text)
tags:
- AI-Filled (Verify)
collections:
- ChemPile
source_links:
- https://doi.org/10.1093/database/baw068 (BC5CDR); https://doi.org/10.1186/1758-2946-7-S1-S1 (CHEMDNER); https://doi.org/10.1016/j.jbi.2013.12.006 (NCBI Disease); https://doi.org/10.1038/s41597-021-00875-1 (NLM-Chem)
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/<config> (configs: bc5chem, bc5disease, chemdner, ncbi_disease, nlmchem) ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/bc5chem ; original: https://huggingface.co/datasets/bigbio/blurb ; https://huggingface.co/datasets/bigbio/chemdner ; https://ftp.ncbi.nlm.nih.gov/pub/lu/NLMChem/'
- https://arxiv.org/abs/2505.12534
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`NLP (Text)`, SEL-12): five corpora of PubMed abstracts and full texts annotated with chemical and disease mentions; a row is a sentence and the target is the entity span, so language models are the tool and there is no tabular target (SEL-3 as well).
- Source: five text corpora, each with its own publication. BC5CDR: Li et al. 2016, Database, doi 10.1093/database/baw068, "BioCreative V CDR task corpus: a resource for chemical disease relation extraction". CHEMDNER: Krallinger et al. 2015, J Cheminform, doi 10.1186/1758-2946-7-S1-S1, "CHEMDNER: The drugs and chemical names extraction challenge"; the ChemNLP card: "The CHEMDNER corpus comprises 10,000 PubMed abstracts, which have been meticulously annotated by expert chemistry literature curators according to task-specific guidelines, identifying a total of 84,355 mentions of chemical entities". NCBI Disease: Dogan et al. 2014, J Biomed Inform, "NCBI disease corpus: A resource for disease name recognition and concept normalization". NLM-Chem: Islamaj et al. 2021, Sci Data, "we present the NLM-Chem corpus, a full-text resource to support the development and evaluation of automated chemical entity taggers ... 150 full-text articles, doubly annotated by ten expert NLM indexers, with ~5000 unique chemical name annotations, mapped to ~2000 MeSH identifiers". Sizes in the ChemPile cut: bc5chem 13,755, bc5disease 13,755, chemdner 19,440, ncbi_disease 7,075, nlmchem 2,695. The ChemNLP metas give the identifier `sentence` and the target `matched_words` ("matched entity"); nlmchem's only non-span target is the full form of an abbreviation given its MeSH identifier, a lookup rather than a prediction.
- Use case: none for a tabular model: the decision is an annotation of free text (SEL-3, USE-2).
- Siblings and duplicates: `bio_ner`, proposed as a reject on the same ground. Five sources in one record, each its own corpus (PROV-7); no merge is needed since the record goes. External collections: ChemPile / ChemNLP, BigBio (bigbio/blurb, bigbio/chemdner).
- Better data: a candidate of the benchmark ChemPile; no further search this round.
- Papers and pages: the four papers above; the ChemNLP builders `data/tabular/{bc5chem,bc5disease,chemdner,ncbi_disease,nlmchem}`.
- Metric: the corpora are scored by entity-level precision, recall and F1 in their shared tasks (BioCreative V CDR, CHEMDNER), a text-annotation metric that no tabular task of ours uses.
- Reject check (AI, 2026-10-31): stands. Each of the five corpora was published for text tagging, e.g. NLM-Chem 'a full-text resource to support the development and evaluation of automated chemical entity taggers' (https://doi.org/10.1038/s41597-021-00875-1); every ChemNLP meta gives identifier `sentence` and target `matched_words`, and nlmchem's only other target, an abbreviation's full form from its MeSH id, is a lookup. Nothing tabular to keep.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534).
- as published: bc5chem 13,755; bc5disease 13,755 (BC5CDR); chemdner 19,440 (10,000 abstracts); ncbi_disease 7,075; nlmchem 2,695; in ChemPile-LIFT 299,739 text prompts over 5 config(s); target: entity spans (chemical, disease) / MeSH identifier of an abbreviation.
- Why: Named entity recognition of chemical and disease mentions in PubMed abstracts and full texts
- Notes: Five NER corpora, all text. Out of scope.
