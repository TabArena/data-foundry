---
unique_name: company_employees
name: Company Employees
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- No Good Target (yet)
tags:
- 2nd Tier / Scientfic Discovery
- Free Text (Short)
- Review Prio 1 (Atlas)
collections:
- CARTE/TARTE
original_source: Kaggle
year: '2019'
domain: business & marketing
required_split:
- '?'
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/peopledatalabssf/free-7-million-company-dataset
- https://medium.com/@peopledatalabs/2019-global-company-dataset-8acca1f1caf0
- https://docs.peopledatalabs.com/docs/free-company-dataset
- https://huggingface.co/datasets/inria-soda/carte-benchmark/blob/main/data_raw/company_employees.csv
- https://arxiv.org/abs/2402.16785
source_row: 472
type_adapter_id: curation-record-v1
---

## Comments

Minimal LinkedIn data from a bunch of companies

Lennart: Data does not seem to have any real task. Just scraped wiki-like tables from LinkedIn. There seems to be no predictive task or value in these, so let remove it for now and classify it as 2nd tier

CC (2026-09-22, Lennart): Source traced. Kaggle uploader `peopledatalabssf` is the official account of People Data Labs (PDL, a B2B data broker); the file is PDL's "7+ Million Company Dataset", released 2019-05-06 as a data-enrichment dump (PDL Medium post: use it to "enrich their dataset with company-specific information"), not for a predictive task. Its successor, PDL's Free Company Dataset, is CC BY 4.0 and updated quarterly (docs.peopledatalabs.com/docs/free-company-dataset); the 2019 Kaggle page's licence could not be checked (CARTE's HF card lists it as "unknown").

What the target measures (PDL company schema, `employee_count`): "The current number of employees working at the company based on our number of profiles" -- a count of LinkedIn-derived person profiles PDL holds, not the company's headcount. `size range` is the company's self-reported LinkedIn size bucket.

The prediction task is CARTE's construction (paper App. B.2, dataset 11: "Information on companies with over 1,000 employees. The task is to predict the number of employees of each company."; raw file `data_raw/company_employees.csv` on HF inria-soda/carte-benchmark, 11,269 x 11): subset with estimate >= 1000, log10 target, drops `country` and `total employee estimate` (log-corr 0.91 with the target), keeps `size range`, `linkedin url` (unique per row), `name`, `domain`, `industry`, `locality`, `year founded` (28% NA). `size range` is near-target: within-bucket log10 std 0.10-0.12 vs 0.34 overall, and every self-reported "5001-10000" company has an estimate <= 5000 (PDL undercounts). Without it, the ID and the total, what remains is industry/locality/year founded plus name/domain, i.e. looking up a company's size from its name.
