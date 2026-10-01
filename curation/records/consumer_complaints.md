---
unique_name: consumer_complaints
name: Consumer Complaint Database
checked_by:
- Lennart
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
original_source: GOV Website
year: '2019'
domain: finance
required_split:
- Temporal (NON-IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/selener/consumer-complaint-database
- https://catalog.data.gov/dataset/consumer-complaint-database
- https://www.consumerfinance.gov/foia-requests/foia-electronic-reading-room/cfpb-consumer-complaint-database-narratives-archive/
notebook_path: datasets/beyond_iid/temporal/consumer_complaints/consumer_complaints_1m.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/consumer_complaints_1m/dataset.py
source_row: 735
type_adapter_id: curation-record-v1
---

## Comments

Real world complaints about financial products and services; data might contain sub-cohorts based on reporting category; we might want to filter to only a subset of cohorts; many missing values; data might have temporal drift; contains zip code to get more tabular features; temporal; we could get a new version of the data from the website

Needs a lot of preprocessing / feature engineering to become a usable task

We got the newer version from here: https://www.consumerfinance.gov/data-research/consumer-complaints/

Ref for descriptions https://cfpb.github.io/api/ccdb/fields.html

Only "Consumer complaint narrative" is a sentence field. "Company public response" is from one a predefined list of options

CC (2026-10-01, Lennart): **Original source changed.** The CFPB stopped publishing complaint narratives on 2026-08-14 (announcement: https://www.consumerfinance.gov/about-us/newsroom/the-cfpb-to-cease-discretionary-publication-of-complaint-narratives-and-visualizations/) and removed them from the live download on 2026-09-14. The live `complaints.csv` (checked 2026-09-30) has no narrative and no consent column, so it can no longer rebuild this text task. Every previously published complaint, narratives included, is archived in the FOIA reading room as 21 CCDB exports (exported 2026-09-14, with Complaint ID and the company response as of that date): https://www.consumerfinance.gov/foia-requests/foia-electronic-reading-room/cfpb-consumer-complaint-database-narratives-archive/
Newer data is not useful even from the archive: the share of complaints with a published narrative fell from 16% (Nov 2025) to 3.5% (Mar 2026), 1.5% (Jul 2026) and 0 (Aug 2026), and the label mix of those complaints shifted ("closed with explanation" 65% -> 81%).

CC (2026-10-01, Lennart): Leak audit: the build from the 2026-01-23 download had a right-censored test window. Complaints still "In progress" are filtered out, and that was 7% of Oct, 14% of Nov and 70% of Dec 2025, so the newest months kept mainly quickly closed complaints. The v2 definition now builds from the FOIA archive exports 1-14 (Dec 2011 - Dec 2025), keeps complaints received 2017-04-24 to 2025-12-31 and tests on Oct-Dec 2025 (3-month horizon); all those labels are settled (0 in progress). Against the January download the archive has identical labels for all 3.49M shared complaints, 64,743 more closed complaints (mostly Nov-Dec 2025), Windows line endings in 2017-2020 narratives (normalised) and fewer fully masked ZIP codes (1.8% instead of 4.8%). The archive has no "Consumer disputed?" or consent column: the dispute filter is now the date filter it was equivalent to, and the consent filter is "has a narrative" (drops 1,656 consented rows without text). Duplicates that disagree on the label are now all dropped, as the curation comments already said.

## Reference

Kaggle / Gov
