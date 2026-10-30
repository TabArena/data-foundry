---
unique_name: hiva_agnostic
name: hiva_agnostic
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Anonymized
year: '2007'
domain: chemistry & material science
required_split:
- Random (IID)
problem_type: Binary Classification
source_links:
- https://www.openml.org/search?type=data&id=1039
notebook_path: datasets/beyond_iid/old_iid/hiva_agnostic/hiva_agnostic.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/hiva_agnostic/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Data previously was 3-class, originally had a custom split, also was preprocessed to be binary. Was a challenge held in 2007 - https://www.agnostic.inf.ethz.ch/datasets.php - but may be still representative of similar tasks.Also submission might still be possible. Could ask organizers for hidden test data. However could also be solved differently nowadays. 1618 features. In TabRepo trees are much better than NNs. Either a result of the unfair time limits for NNs or a bias through random splits; original source data links point to scam websites now

Potential issue: Preprocessing

Lennart: Preprocessing and original data state seem problematic

Andrej: Might consider to restore it to be a 3-class problem

**Assessment (AI, 2026-10-14):** the challenge split the screen's 42,678 compounds into training (3,845, 135 active), validation (384, 14 active) and test (38,449, labels never released), as `hiva.param` lists them. The validation compounds have the same 1,617 descriptors; their labels are in ValidAgnos.zip, which the download already fetched. The fixed list of dropped descriptors removed 99 of the 191 copies in the training file; the definition now drops every descriptor that copies an earlier one over all 4,229 compounds (188).

CC (2026-10-14, Lennart): Add the 384 validation compounds (4,229 compounds, 149 active).

CC (2026-10-21, Lennart): one domain for the molecule-property datasets (the input is the molecule): "chemistry & material science", for all ten QSAR siblings.

CC (2026-10-21, Lennart): 0/1 presence flags are categorical ("Assuming it is binary, the categorical dtype might be best?"); CLEAN-14 amended. The bits were checked to hold only 0 and 1.

**Assessment (AI, 2026-10-21):** on the 23 repeated descriptor vectors (crosscut item x2-1, Lennart: "IF the copies dont make any sense from a task use case, we should drop them"). The challenge's prior-knowledge release gives the same 4,229 compounds as structures with NCI NSC numbers: every NSC number is distinct, so no compound is entered twice. Of the 4,156 structures RDKit reads, 7 repeat another's exact structure, 9 ignoring stereochemistry, 19 counting salt forms of one parent; fewer than 23, so at least 4 of the copies are different compounds the descriptors cannot tell apart. The two releases share no key, so the copies cannot be matched one by one. Kept, with this reason in curation_comments; the curator has the call.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source balanced_accuracy — BER (balanced error rate) = 0.5*(b/(a+b) + c/(c+d)); final ranking by test BER; AUC also reported (= 1-BER for hard predictions) (https://www.agnostic.inf.ethz.ch/evaluation.php ; Guyon et al. 2007 IJCNN, doi 10.1109/IJCNN.2007.4371065).

CC (2026-10-21, Lennart): the 23 repeated descriptor vectors stay: they are distinct screened compounds (every NSC number distinct), not copies of one compound ("IF the copies dont make any sense from a task use case, we should drop them"); LEAK-19 as written.

CC (2026-10-21, Lennart): the declared metric stays as it is (`balanced_accuracy`; the challenge most likely ranked by the balanced error rate, not verified; cross-dataset item "Metrics still to settle").

CC (2026-10-27, Lennart): marker Anonymized, from the AI review of PR #17: the agnostic track of the challenge gives the 1,617 binary structure descriptors without names (the prior knowledge track had the structures instead), so their meaning cannot be checked; the definition's fit_reason says so. Data tag Anonymized added to the definition.

## Reference

Datasets from the Agnostic Learning vs. Prior Knowledge Challenge (http://www.agnostic.inf.ethz.ch)
