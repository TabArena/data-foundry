---
unique_name: nhanes_dxa_body_fat
name: NHANES DXA Body Composition + Body Measures
checked_by:
- Andrej
data_foundry_status:
- WIP (Triage)
claimed_by: Andrej
suggestion: TBD -> Yes
original_source: GOV Website
year: '2013'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2005/DataFiles/DXX_D.htm
- https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2005/DataFiles/BMX_D.htm
- https://doi.org/10.1038/ijo.2015.231
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-10-15, Andrej): Replacement candidate for `body_density_prediction` (252 men, 1985): the same task, body fat from cheap tape measurements instead of an expensive reference test, on a public US survey of thousands of people of both sexes aged 8+. Target: DXA total percent fat (`DXDTOPF` in DXX). Features from BMX and DEMO: age, sex, ethnicity, weight, height, waist and arm circumference; 1999-2006 also has thigh and calf circumference and triceps/subscapular skinfolds, 2017-18 has hip instead. Public domain (US government).

Established as a predictive task: Stevens et al. 2016 build percent-fat equations from anthropometry on NHANES 1999-2006 DXA (Abstract, Background/Objectives: "The objective of this study was to develop sets of equations that are generalizable to the American population").

Data inspected (2026-10-15; XPT files of DXX, BMX, DEMO for all 8 DXA cycles, in `local-data-warehouse/nhanes_dxa_body_fat/`):
- Imputation is real and must be filtered. In 1999-2006 the five `_MULT_` copies of an imputed person differ by 4.4 points of percent fat on average (up to 23). Everyone not scanned for weight > 300 lb is imputed, so the 5-copy data invents targets for the heaviest people. Keep `_MULT_` 1, `DXAEXSTS` 1 (scan completed) and imputation flag 0 (`DXITOT` in 1999-2004, `DXITOTST` in 2005-06), and drop 90 flag-0 rows of 2003-06 whose copies still differ. 2011-2018 has no imputation: one row per person, keep `DXAEXSTS` 1 with `DXDTOPF` present.
- Clean size: 1999-2006 21,768 people (age 8-85, 14,195 adults, 54% male), max weight 138 kg; features under 1% missing except triceps (4.7%) and subscapular (12%) skinfolds. 2011-2018 17,833 people (age 8-59), max weight 188 kg (newer scanners), but only weight, height, waist, arm circumference and limb lengths (hip only in 2017-18, 83% missing pooled).
- Not trivial. 5-fold CV R2 on percent fat, linear / gradient boosting: 1999-2006 sex+age+BMI 0.71 / 0.82, all tape and scale measures 0.80 / 0.87, plus skinfolds 0.86 / 0.90; 2011-2018 all measures 0.76 / 0.85. Models spread, and the remaining error (RMSE 2.8-3.4 points) is above DXA's own measurement error. Same check on bodyfat (OpenML 560, 252 men): all measures 0.71 / 0.65.

Join: no aggregation needed. DXX (after the filter above), BMX and DEMO each have one row per person and join 1:1 on `SEQN` (21,768 rows before and after the join); the rounds stack with the same columns. Drop the other DXX columns (regional fat and lean mass, a leak) and DEMO's survey weights and design variables.

Proposal: 1999-2006 pooled, all ages or adults only (adults R2 0.83-0.90, same picture), skinfolds kept; `cycle` as a column, IID split. The weight cap (no one above 300 lb) belongs in the use-case notes. Still open: survey weights (NHANES oversamples some groups, so the rows are not a simple random sample of the US).

Features differ between survey blocks: 1999-2006 has thigh and calf circumference and skinfolds, 2011-2018 has none of these (hip only in 2017-18), and the scanners changed in between. So we might need to define different splits (or separate datasets) per block rather than one split over pooled data.

Split. NHANES samples whole households, so relatives who share genes and diet could land on both sides of a random split. We tested it: grouping by a household key rebuilt from DEMO, or by masked sampling unit (`SDMVSTRA` x `SDMVPSU`), gives the same RMSE as a random split (2.82-2.83, within the fold-to-fold spread), and holding out whole survey rounds does too. CC (2026-10-15, Andrej): random split; grouping adds nothing measurable.

## Reference

@article{stevens2016prediction,
  title={Prediction of percent body fat measurements in Americans 8 years and older},
  author={Stevens, June and Ou, Fang-Shu and Cai, Jianwen and Heymsfield, Steven B and Truesdale, Kimberly P},
  journal={International Journal of Obesity},
  volume={40},
  number={4},
  pages={587--594},
  year={2016},
  doi={10.1038/ijo.2015.231}
}
