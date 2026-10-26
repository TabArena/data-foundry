---
unique_name: human_genome_annotation
name: Human genome annotation
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
tags:
- 2nd Tier / Scientific Discovery
- AI-Filled (Verify)
collections:
- New (BeyondArena)
domain: biology & life sciences
required_split:
- '?'
problem_type: TBD
original_data_state: Other
source_links:
- https://www.kaggle.com/datasets/alfrandom/human-genome-annotation
source_row: 834
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`No Good Target / Scientific Discovery`, SEL-3): a CSV conversion of the Ensembl GRCh38.92 genome annotation, published to "explore the structure within the annotations"; a reference listing with no target and no decision.
- Source: Ensembl release 92 GTF (2018), converted with the uploader's `gtf2csv` script and posted on Kaggle (dataset 31883, DbCL-1.0, one file `Homo_sapiens.GRCh38.92.csv`, 501 MB, 2019). As published: one row per annotated feature (gene, transcript, exon, CDS, UTR, ...) with chromosome, start, end, strand, source and the GTF attributes as columns.
- Use case: none; the card's "Inspiration" is visualization and analysis. Any label (feature type, biotype) is the annotation itself, read off coordinates and attributes, not an outcome someone predicts.
- Siblings and duplicates: none among `curation/records/`.
- Papers and pages: the Kaggle card; Ensembl release 92.
- Metric: none found (Kaggle card).
- Reject check (AI, 2026-10-22): stands. The Kaggle card's stated aim is "to encourage data scientists who are interested in genomics to explore the structure within the annotations", and the rows are Ensembl GRCh38.92 GTF features (https://www.kaggle.com/datasets/alfrandom/human-genome-annotation). It is a reference listing. Any label (feature type, biotype) is the annotation itself, and predicting it in practice is a sequence task. SEL-3.

Kaggle 'Human genome annotation' dataset, already tagged 2nd Tier / Scientific Discovery, with no task description in the record. Genome-annotation tables are typically descriptive feature/coordinate listings (gene/region annotations) without a canonical predictive target, leaning toward scientific discovery; there is also a risk the underlying signal is sequence-based rather than genuinely tabular. There is too little information to confirm a usable target or split. A human must inspect whether a real predictive label exists and whether the features are tabular; keep in 2nd tier.
