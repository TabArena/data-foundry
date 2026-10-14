---
unique_name: colleges
name: colleges
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Duplicate
collections:
- TabSTAR
- TabArena Reject
source_links:
- https://www.openml.org/search?type=data&id=42727&sort=runs&status=active
- https://beachpartyserver.azurewebsites.net/VueBigData/DataFiles/Colleges.txt
source_row: 587
type_adapter_id: curation-record-v1
---

## Comments

CC: "Predict faculty salary from 7800 US colleges. Not whole information displayed on OpenML. Lat long features included so spatial patterns may be relevant. Would actually require temporal split? Duplicate with prior colleges version? cannot find origin"

Was used in the AutoML benchmark.

**Assessment (AI, 2026-10-12):** OpenML 42727 is the College Scorecard file of 2013-14 (MERGED2013_14_PP.csv of the Scorecard release) with renamed columns. OpenML names its original as https://beachpartyserver.azurewebsites.net/VueBigData/DataFiles/Colleges.txt (still online: 7,804 rows, 48 columns such as UNITID, faculty_salary, agege24, faminc and the 6- and 10-year earnings, all Scorecard fields). All 7,804 UNITIDs are in the 2013-14 Scorecard file, against at most 7,577 for any other year, and faculty salary, undergraduate size and admission rate agree for 97-99% of the colleges where both files have a value. So it is a one-year cut of college_scorecard.

CC (2026-10-12, Lennart): No: duplicate of college_scorecard (its 2013-14 file).
