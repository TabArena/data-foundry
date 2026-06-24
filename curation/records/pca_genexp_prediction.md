---
unique_name: pca_genexp_prediction
name: Prostate
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
suggestion: 'No'
decision_markers:
- Too Small
tags:
- New IID
- Many features
collections:
- FS Benchmark
original_source: OpenML
year: '2002'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.openml.org/d/45099
source_row: 1037
type_adapter_id: curation-record-v1
---

# Prostate

## Comments

OpenML Source Rel: https://arxiv.org/abs/2311.12879

CC: "We use OpenML version of the dataset for binary classification as the URLs from the original reference are outdated."


Too small -> few-shot prediction task

## Reference

@article{singh2002gene,
  title={Gene expression correlates of clinical prostate cancer behavior},
  author={Singh, Dinesh and Febbo, Phillip G and Ross, Kenneth and Jackson, Donald G and Manola, Judith and Ladd, Christine and Tamayo, Pablo and Renshaw, Andrew A and D'Amico, Anthony V and Richie, Jerome P and others},
  journal={Cancer cell},
  volume={1},
  number={2},
  pages={203--209},
  year={2002},
  publisher={Elsevier}
}
