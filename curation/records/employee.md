---
unique_name: employee
name: Employee
suggestion: 'No'
decision_markers:
- Data Quality Issue
original_source: Kaggle
year: '2023'
required_split:
- Random (IID)
source_links:
- https://www.kaggle.com/datasets/tawfikelmetwally/employee-dataset
type_adapter_id: curation-record-v1
---

# Employee

## Comments

Imported from the TabArena curation workbook.

TabArena curation verdict: None-dataquality.

Provided by a real company. Predict whether an employee will leave the company. But originally, there are different analytics questions associated with this dataset. As the joining year is given some analysis is requried prior to creating a predictive task. The main question is which time frame the target spans. I would expect the task to be conceptualized to predict whether a customer leaves next year - but unsure whether thats possible

Potential issue: -

Lennart: Seems usable for at least some predictive task that is time invariant

Andrej: Missing information on the target

## Reference

https://www.kaggle.com/datasets/tawfikelmetwally/employee-dataset
