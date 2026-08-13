---
unique_name: diabetes
name: diabetes
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
suggestion: No (Retired)
decision_markers:
- Ethical Issue
original_source: Kaggle
year: '1988'
required_split:
- Random (IID)
problem_type: Binary Classification
source_links:
- https://www.openml.org/search?type=data&id=37
- https://doi.org/10.24432/C5T59G
notebook_path: datasets/_maintenance/_old_collections/tabarena-v0pt1/diabetes/diabetes.ipynb
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1).

TabArena curation verdict: Tabular.

Rather interpretability than predictive performance task, nowadays done differently

Potential issue: Outdated

Lennart: No objection

Andrej: Fits our criteria, but TabRepo resutls for this dataset are pretty random as there are only 768 samples

CC (2026-07-27, Lennart): **Removed from TabArena (v0.1) on ethical grounds -> suggestion No.** This is the Pima (Akimel O'odham) Indians Diabetes data; its reuse raises ethical concerns about the politics of reusing indigenous / medical data, raised by Radin (2017), "'Digital natives': how medical and indigenous histories matter for big data", Osiris. Kept the `TabArena (v0.1)` tag (it did ship); the `No (Retired)` verdict marks the post-shipping change.

## Reference

Smith, J.W., Everhart, J.E., Dickson, W.C., Knowler, W.C., & Johannes, R.S. (1988). Using the ADAP learning algorithm to forecast the onset of diabetes mellitus. In Proceedings of the Symposium on Computer Applications and Medical Care (pp. 261--265). IEEE Computer Society Press.
