---
unique_name: amazon_bin_weight
name: Amazon Packages
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Image
tags:
- AI-Filled (Verify)
collections:
- MulTaBench
source_links:
- https://registry.opendata.aws/amazon-bin-imagery/
- https://www.kaggle.com/datasets/dhruvildave/amazon-bin-image-dataset
- https://arxiv.org/abs/2605.10616
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Image`, SEL-12): the Amazon Bin Image Dataset was released for image recognition research, and without the bin photo MulTaBench's table is one integer column and the item names, whose catalog weights the source's metadata already lists and which sum to the target.
- Source: Amazon Fulfillment Technologies, Registry of Open Data on AWS (https://registry.opendata.aws/amazon-bin-imagery/; documentation https://github.com/awslabs/open-data-docs/tree/main/docs/aft-vbi-pds): "Amazon Fulfillment Technologies has made the bin images available free of charge on Amazon S3 to encourage recognition research in a variety of areas, including counting generic items and learning from weakly-tagged data"; "Over 500,000 bin JPEG images and corresponding JSON metadata files describing items in the bin". The metadata (preview of `metadata/523.json`) lists per item the ASIN, name, quantity, height, length, width and weight in pounds, plus `EXPECTED_QUANTITY`. The Kaggle copy dhruvildave/amazon-bin-image-dataset holds 50,000 images. As used by MulTaBench (core image-tabular; https://huggingface.co/datasets/multabench/core-img-reg-amazon-packages): 46,398 rows, `Expected Quantity`, `product descriptions`, the bin image, target `Total Weight in Pounds`.
- Why out: the source's task is recognition and counting on the images (SEL-8, SEL-12). MulTaBench Table 7 reports no structured-only score; the image alone gives R² 43.2 and 47.5 (LightGBM, TabPFN-2.5) against 17.5 and 21.1 for the item text alone. The target is the sum of quantity times catalog weight over the items the metadata lists, computed from data the source ships (SEL-5) and known to the warehouse from its inventory record, so no decision fits a model of it (USE-2).
- Siblings and duplicates: none (grep over the records for amazon bin, aft-vbi-pds, the Kaggle slug). External collections: MulTaBench (core image-tabular).
- Better data: a candidate of the benchmark MulTaBench; no further search for this run's finds.
- Papers and pages: the AWS registry page and documentation; the "Amazon Bin Image Dataset Challenge" and "Amazon Inventory Reconciliation using AI" listed on the registry page; MulTaBench (https://arxiv.org/abs/2605.10616), Table 3, Table 7.
- Reject check (AI, 2026-10-31): stands. The source released the bins 'to encourage recognition research in a variety of areas, including counting generic items and learning from weakly-tagged data' (https://github.com/awslabs/open-data-docs/tree/main/docs/aft-vbi-pds); in MulTaBench's table the only structured column is `Expected Quantity` beside the item names (text) and the photo, and the per-item catalog weights the target sums are in the source's own metadata, so without the image no tabular task remains.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark MulTaBench (https://arxiv.org/abs/2605.10616).
- as published: 46,398 rows; 1 structured, 1 text, 1 image features (MulTaBench Table 3); target: Total weight of bin contents (pounds).
- Why: Predict the total weight of a fulfilment-centre bin from its photo, item description and expected quantity
- Notes: Image-tabular: one image column per row (released as image files); out of scope for a tabular-only container unless the image is dropped or embedded. Amazon Bin Image Dataset (AWS Open Data, 2017; Kaggle copy CC BY-NC-SA). Trimodal per the paper.
