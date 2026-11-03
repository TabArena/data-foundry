---
unique_name: iwildcam_2020_camera_trap_species
name: iWildCam 2020 (FGVC7 camera-trap species classification, LILA)
checked_by:
- Andrej
suggestion: 'No'
decision_markers:
- Image
tags:
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
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `No` (`Image`, SEL-12; SEL-8): the iWildCam 2020 challenge classifies species in
camera-trap images; the release is images with per-image labels and location ids, detector boxes and satellite image
patches, with no count table and no site covariate.
- Source: Beery, Cole and Gjoka, "The iWildCam 2020 Competition Dataset", FGVC7 workshop at CVPR 2020, arXiv:2004.10340;
  Kaggle competition iwildcam-2020-fgvc7; images from the Wildlife Conservation Society. As published (competition
  readme, github.com/visipedia/iwildcam_comp, 2020): "The WCS training set contains 217,959 images from 441 locations,
  and the WCS test set contains 62,894 images from 111 locations"; files train.zip and test.zip (images), metadata.zip
  (COCO-style JSON: image `id`, `file_name`, `location`, `datetime`, `seq_id`, `seq_num_frames`, `frame_num`, and
  annotations with `category_id`), MegaDetector output ("We have run the detector over the WCS dataset, and provide the
  top 100 boxes and associated confidences"), Landsat 8 patches ("Each patch is 200x200x9 pixels", images too) and
  iNaturalist 2017 and 2018 image subsets.
- Deciding words: "The challenge is to correctly classify species in the test camera traps." (arXiv abstract);
  "Submissions will be evaluated based on their categorization accuracy." (readme).
- Use case: species identification in images (SEL-8). A count or occupancy table could be derived from the labels, but
  it would carry only location ids, timestamps and image patches, and no source publishes such a task; the zeros are
  empty frames in a classification, not a zero-inflated target.
- Siblings and duplicates: `wildlife_insights_camera_trap_detections` (a platform of identifications),
  `southeast_asia_predator_prey_camera_trap_counts` and `freiburg_urban_mammal_camera_trap_events` (other data).
  External collections: WILDS carries a version (iWildCam2020-WILDS), as an image task.
- Metric: categorization accuracy, the leaderboard metric (readme), on images.
- Access: "The original competition dataset files are unfortunately no longer accessible." (readme); the LILA iWildCam
  2022 page answered on 2026-10-27.
- Reject check (AI, 2026-10-27): stands. SEL-12 (Must). The source's task is per-image species classification ("The
  challenge is to correctly classify species in the test camera traps.", https://arxiv.org/abs/2004.10340), and the
  release (https://github.com/visipedia/iwildcam_comp/tree/master/2020) holds images, image labels, detector boxes and
  image patches, with no count table and no site covariate.

CC (2026-10-30, Andrej): `No`, as screened (verified on the zero-inflated screening review page).

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
