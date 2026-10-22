---
unique_name: autonomous_shopper_prediction_by_cape_ai
name: Autonomous Shopper Prediction by Cape AI
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Image
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: technology & internet
required_split:
- '?'
problem_type: Binary Classification
source_links:
- https://zindi.africa/competitions/indabax-south-africa-2021
source_row: 1006
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Image`, SEL-13): pose keypoints extracted from shop camera video, classified as 30-frame sequences ("take" or not); video-derived kinematics are a vision task even as numeric columns.
- Source: Zindi, "Autonomous Shopper Prediction" (IndabaX South Africa 2021, Cape AI / Moonshop), private hackathon 2021-09-03 to 2021-11-21; as published: Train.csv with one row per frame (66 keypoint coordinates from MediaPipe BlazePose GHUM 3D, [0.0, 0.0] for missing), frames grouped in 30 under one ID, Train_Target.csv with one label per sequence, Data_Dictionary.csv.
- Use case: Moonshop's camera-based checkout decides whether a shopper took a product; the decision is real, but the data is video recast as keypoints, and the source frames it as "human action recognition" and "time series prediction", solved with sequence models.
- Siblings and duplicates: none in curation/records/; no external collection.
- Metric: AUC on the predicted probability (Zindi Evaluation page).
- Also fits `Time-series (Classification)` (a sequence of readings classified as a whole).
- Reject check (AI, 2026-10-22): stands. SEL-13 names 'video-derived kinematics'. Zindi (https://zindi.africa/competitions/indabax-south-africa-2021): 'a stream of 30 video frames ... 2D Pose Estimation model (MediaPipe ... BlazePose GHUM 3D) over each frame'. SEL-14 does not apply: the inputs are a model's pose keypoints, not a human reading that tabular models use in practice.

Zindi/IndabaX 'Autonomous Shopper Prediction' (Cape AI): predict whether a customer has taken a product from the shelf, i.e. a binary classification for autonomous/cashier-less retail. The concern is the underlying data could be derived from camera/sensor (computer-vision) feeds rather than genuine tabular features, which would make it not representative of tabular ML. The target is clear, but the modality is uncertain. A human must verify the features are tabular sensor/aggregate signals (not raw video/image) and check the cleaned size and split.

---

predict if a customer has taken a product from the shelf
