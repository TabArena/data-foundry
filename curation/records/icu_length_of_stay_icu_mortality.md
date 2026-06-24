---
unique_name: icu_length_of_stay_icu_mortality
name: ICU Length of Stay ICU Mortality
checked_by:
- Lennart
suggestion: TBD -> Yes
decision_markers:
- Duplicate
tags:
- Non-IID (Grouped)
- Non-IID (Temporal)
- '?'
collections:
- TableShift
source_links:
- https://tableshift.org/datasets.html#icu-length-of-stay
- MIMIC-extract data / MIMIC-III
- https://physionet.org/content/mimiciii/1.4/
source_row: 610
type_adapter_id: curation-record-v1
---

## Comments

Data from MIMIC likely duplicated with data from sepsis_prediction task. Unclear how to handle such duplicates with very different data. This data only uses 24k patients and from/with a different feature set and subset

TableShift: MIMIC-Extract (https://github.com/MLforHealth/MIMIC_Extract#pre-processed-output); "An individual patient might be admitted to the ICU at multiple times in the dataset; however, MIMIC-extract focuses on each subject's first UCI visit only, since those who make repeat visits typically require additional considerations with respect to modeling and care."; create a "shift" using a categorical variable; is not grouped otherwise as far as I can see; real-world task was not created such that this is a shift, thus again made to be a shift by benchmark authors.

Otherwise data looks great, if we can even get it

TableShift also creates a second task from this dataset (ICU Mortality). Same problem as before regarding creating a shift. Just a different target, otherwise identical.

Given the way the data must be obtained/distributed and the questionable case of a duplicate, we need to decide how to go about it

## Reference

MIMIC-3 Extract (https://www.nature.com/articles/sdata201635)
