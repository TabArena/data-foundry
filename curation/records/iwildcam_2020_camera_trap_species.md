---
unique_name: iwildcam_2020_camera_trap_species
name: iWildCam 2020 (FGVC7 camera-trap species classification, LILA)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Image
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
original_source: Kaggle
year: '2020'
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
problem_type: Multiclass Classification
original_data_state: Other
source_links:
- https://github.com/visipedia/iwildcam_comp/tree/master/2020
- https://www.kaggle.com/c/iwildcam-2020-fgvc7
- https://arxiv.org/abs/2004.10340
- https://lila.science/datasets/iwildcam-2022/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

iWildCam 2020 (Beery, Cole and Gjoka, Caltech; images from WCS): camera-trap images with COCO Camera Traps JSON
(category, location, datetime, sequence), Landsat 8 patches per site and iNaturalist images. Paper Sec. 2: 217,959
training images from 441 locations and 62,894 test images from 111 locations, about half of them empty. The task is
vision: "The challenge is to correctly classify species in the test camera traps" (abstract); the 2022 successor
counts animals per image sequence. There are no tabular features at all. The workbook's LILA link returns 404, and
the 2020 readme says "The original competition dataset files are unfortunately no longer accessible". Not
downloaded (image archive).

Zero mechanism: empty frames in a classification task; there is no zero-inflated target. Licence: CDLA-Permissive 1.0
for the WCS and remote-sensing data (2020 readme).

## Reference

Beery S., Cole E., Gjoka A. (2020). The iWildCam 2020 Competition Dataset. FGVC7 workshop at CVPR 2020.
arXiv:2004.10340.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 23 (iWildCam / LILA).
