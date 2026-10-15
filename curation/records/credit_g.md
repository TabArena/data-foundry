---
unique_name: credit_g
name: credit-g
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
original_source: UCI
year: '1994'
required_split:
- Random (IID)
- Temporal (NON-IID)
problem_type: Binary Classification
source_links:
- https://www.openml.org/search?type=data&id=31
- https://doi.org/10.24432/C5NC77
notebook_path: datasets/beyond_iid/old_iid/credit_g/credit_g.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/credit_g/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Comes with a cost matrix. TabRed says that task requires time based split, but no time feature given. However, if time-invariant features are used that might not matter. Also might be outdated as nowadays other features might be used; only time dependency could be the bank's and the world's financial state as a confounding factor

Potential issue: Outdated (Deutsche Mark)

Lennart: Temporal impact unclear and not resolvable, otherwise ok and not too old

Andrej: Fits criteria, but honestly this dataset with only 1000 samples from 1994 is not representative of a credit scoring task anymore. If no better dataset is available I would not use it

CC (2026-10-15, Andrej): Keep, with the corrected code table. Grömping (2019) traced the data back to their original sources.
- Code table, corrected in the v2 definition (container not rebuilt yet):
  - Problem: the Statlog code table mislabels 8 of the 20 features and reverses people_liable. Our "no checking account" was the safest group (11.7% bad; in fact a balance of at least 200 DM), and 96.3% were "foreign workers" (in fact 3.7%). This mattered only for models that read the category text.
  - Fix: relabelled with Grömping's corrected table, checked against South German Credit row by row; nothing else in the data changes (the banded scores stay integer codes, their bands are documented). The task summary states the period, the sample, the target and that credit amounts are transformed. `year` stays 1994, the donation year, as the v2 convention asks.
- Remaining issues, none of which excludes it:
  - Age: the loans were granted in 1973-1975 by a regional bank in southern Germany (Häußler 1979; Fahrmeir & Hamerle 1984); 1994 is only the year of the UCI donation. Not severe on its own.
  - Size: 1,000 loans from one bank. Not "Too Small": about 100 bad loans per test fold. It is our small-data finance task; other datasets like heloc, give_me_some_credit, home_credit_default_risk and lending_club_1m cover modern credit.
  - Only granted loans: outcomes for rejected applicants are missing. Not severe: credit data are built this way, and the target is well defined (bad = did not comply with the loan contract as required).
  - Oversampling: bad loans are 30% here, against about 5% in the bank's portfolio. The source drew a fixed number of good and bad loans; how the loans within each group were chosen is undocumented. Predicted probabilities therefore refer to the 30% sample, not to the portfolio. Not severe: every row is a real, distinct loan (no copied or synthetic rows), sampling more of the rare class is a common design for credit data, and all methods are compared on the same sample.
  - Hand-typed data: Hofmann typed the rows in from a book appendix. Against the Open Data LMU copy (= South German Credit), 10 rows differ in one amount or age each (e.g. 731 vs 713, 50 vs 40) and 45 other values differ. Only one value (a housing level) is shown to be wrong in Statlog; the published tables cannot decide the others. Not severe, and left as is: we treat these as a data-quality issue that real data has too.

## Reference

10.24432/C5NC77

Grömping, U. (2019). South German Credit Data: Correcting a Widely Used Data Set. Reports in Mathematics, Physics and Chemistry, Report 4/2019. Department II, Beuth University of Applied Sciences Berlin. http://www1.beuth-hochschule.de/FB_II/reports/Report-2019-004.pdf

Grömping, U. (2019). South German Credit [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5X89F

Häußler, W. M. (1979). Empirische Ergebnisse zu Diskriminationsverfahren bei Kreditscoringsystemen. Zeitschrift für Operations Research, 23, B191-B210. https://doi.org/10.1007/BF01917956

Fahrmeir, L., & Hamerle, A. (1984). Multivariate statistische Verfahren (1st ed., Ch. 8 and Appendix C). De Gruyter, Berlin.
