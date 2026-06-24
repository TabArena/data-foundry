---
unique_name: kickstarter
name: kickstarter
checked_by:
- Lennart
- Alex
- Mustafa
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Non-IID (Temporal)
- Free Text (Sentences)
collections:
- TexTabBench
- TabSTAR
- AutoML_MM
original_source: Company
year: '2019'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/yashkantharia/kickstarter-campaigns
- https://webrobots.io/terms-and-conditions/
- https://webrobots.io/kickstarter-datasets/
- https://www.kaggle.com/datasets/codename007/funding-successful-projects
- https://www.openml.org/search?type=data&id=46668
source_row: 736
type_adapter_id: curation-record-v1
---

# kickstarter

## Comments

Scraped Kickstarter results, 2014–Feb 2019, needs to be shuffled since all successful campaigns come first; we should get the newest data from the website; likely need to adjust currency for inflation and time drift and currency; we could try to make the data time-independent by some slight preprocessing to create an IID task; might need to remove length-columns?; might need to change date preprocessing and use proper date preprocessing/encoding from skrub; TODO check raw data again

## Reference

Webrobots Website
