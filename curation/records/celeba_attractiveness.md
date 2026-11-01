---
unique_name: celeba_attractiveness
name: Celeb Attractiveness
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
- https://mmlab.ie.cuhk.edu.hk/projects/CelebA.html
- https://www.kaggle.com/datasets/jessicali9530/celeba-dataset
- https://arxiv.org/abs/2605.10616
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Image`, SEL-13): every feature and the target are annotators' labels of what they see in a celebrity face photo ("40 binary attributes annotations per image"), released for computer vision; a human scoring what they see in an image is an image feature.
- Source: CelebA, MMLAB, The Chinese University of Hong Kong (https://mmlab.ie.cuhk.edu.hk/projects/CelebA.html); paper Liu, Luo, Wang and Tang, "Deep Learning Face Attributes in the Wild", ICCV 2015 (https://arxiv.org/abs/1411.7766, first version 2014-11-28). The page: "CelebFaces Attributes Dataset (CelebA) is a large-scale face attributes dataset with more than 200K celebrity images, each with 40 attribute annotations"; "10,177 number of identities, 202,599 number of face images, and 5 landmark locations, 40 binary attributes annotations per image"; it "can be employed as the training and test sets for the following computer vision tasks: face attribute recognition, face recognition, face detection, landmark (or facial part) localization, and face editing & synthesis". As used by MulTaBench (core image-tabular; https://huggingface.co/datasets/multabench/core-img-cls-celeb-attractiveness): 99,999 images subsampled from the release, 39 binary attribute flags (`Smiling`, `Male`, `Young`, `Heavy_Makeup`, ...), the face image, target `Attractive`.
- Why out: the task as published is face attribute recognition from the image (SEL-8, SEL-12), and the 39 tabular columns are annotations of the same image (SEL-13). No actor decides anything with a predicted attractiveness label (USE-2), and rating faces for attractiveness raises an ethics concern of its own (SEL-1), which the curator may want to record as well.
- Siblings and duplicates: none (grep over the records for celeba). External collections: MulTaBench (core image-tabular).
- Better data: a candidate of the benchmark MulTaBench; no further search for this run's finds.
- Papers and pages: Liu et al. 2015 (abstract); the CelebA project page; the Kaggle copy jessicali9530/celeba-dataset; MulTaBench (https://arxiv.org/abs/2605.10616), Table 3, Table 11.
- Reject check (AI, 2026-10-31): stands. CelebA has '40 binary attributes annotations per image' and is offered for 'face attribute recognition, face recognition, face detection, landmark (or facial part) localization, and face editing & synthesis' (https://mmlab.ie.cuhk.edu.hk/projects/CelebA.html): all 39 features and the target are annotators' readings of the same face photo, which SEL-13 names ('a human scoring what they see in an image is an image feature'). SEL-14 does not apply: no tabular model uses such flags for a decision. The ethics point (SEL-1) is the curator's to add.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark MulTaBench (https://arxiv.org/abs/2605.10616).
- as published: 99,999 rows; 39 structured, 0 text, 1 image features (MulTaBench Table 3); target: Attractive (annotator label, binary).
- Why: Predict the crowd 'Attractive' label of a celebrity face from the image and the other attribute flags
- Notes: Image-tabular: one image column per row (released as image files); out of scope for a tabular-only container unless the image is dropped or embedded. Liu et al. ICCV 2015 (arXiv 1411.7766). Features and target are all annotator labels on face images (subsample); attractiveness rating of faces raises an ethics question.
