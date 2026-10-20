# distribution_transformers_at_cauca_department

**Outcome:** added. A binary task on the 2020 file: which distribution transformers burn during the year, IID
within the year (two yearly files cannot make three temporal windows). `self_protected` is dropped as a mark of
replacement units; `power_kva` and `installation_type` stay with a potential-leak note. The AI recommends shipping
it with these concerns.

**Main points:** `self_protected` is dropped (it marks replacement units). `power_kva` and `installation_type` may
describe replacements too: kept, with dropping them as the alternative.

**Record fields that disagree with the definition:**

- `tag`: record `Non-IID (Temporal)`, definition `Random (IID)`.

**Record judgment:** valid with concerns: the one inventory was taken after the 2020 burns (issues 1 and 4), and
the source corrupted `lv_network_km` (issue 3).

**Issues for Lennart:**

1. **`self_protected` dropped as a post-outcome leak.**
   - **Question:** does the flag mark units installed after a burn?
   - **What the source says:** the flag is an internal low-voltage protection switch (Sec. 1, item C).
   - **What the data show:**
     - Share of self-protected units: 2.0% of the transformers never burned in 2015-2020, 25% of those burned in
       2015-2018, and 46% and 37% of those whose first burn was in 2019 and in 2020.
     - Self-protected units without an earlier burn burned at 42% in 2019 and 42% in 2020 (of those not burned in 2019).
       Self-protected units with an earlier burn burned at 13% and 9%; units without the flag at 2.5-3.3%.
     - 86% of the self-protected units burned in 2015-2020, against 24% of the others.
     - Within 2020 the flag alone gives a log loss of 0.1540, against 0.1560 for all other features together; LightGBM
       AUC is 0.752 with it and 0.699 without.
   - **Implemented:** dropped.
   - **Alternative:** keep it as a genuine risk factor. The 42% against 13% contrast speaks against that reading. The
     authors could be asked for the inventory date.

2. **Year and framing.**
   - **Implemented:** 2020 only, IID within the year. Two years cannot give the three temporal windows v2 requires.
   - **The real use** (train on last year, predict the next year) is a single split, AUC 0.687 for 2019 -> 2020. A
     random split within 2020 gives 0.699, and a split grouped by lightning area within 2020 gives 0.669-0.678 (two fold
     assignments).
   - **Alternative, 2019:** 807 positives, AUC 0.767. It is more affected by the post-burn inventory (self-protected
     share 46% against 37%).
   - **Alternative, both years stacked and grouped by transformer:** AUC 0.745 (0.710 on the 2020 rows). Every unit
     appears twice, and it is not the use case.
   - **Alternative, a framework exception:** allow a one-window temporal task.

3. **`lv_network_km` repair.**
   - **The defect:** 5,395 of the 5,436 lengths of 1.1 km or more are stored as integers of 4 to 6 digits (1103-717125;
     Excel `#,##0` in the 2019 file, General in the 2020 file). The other 41 (1.13-3.56 km) kept their decimal point.
   - **Implemented:** divide each integer by 10^(digits-1). The authors' own table (Datos2019.mat, dataTest) confirms
     this for all 479 matched six-digit values.
   - **A second source bug:** the zeros right after the decimal point were dropped (1.04202 -> 14202, 0.05866 ->
     0.5866).
     - It affects 178 of the 1,754 matched rows (103 of the 159 matched 4/5-digit values, 75 of the 1,116 values below
       1.1 km).
     - The stored value is always too high, by under 1 km (median 0.53 km).
     - The stored value depends only on the true length, so the bug blurs the column without carrying the label. It
       cannot be undone row by row.
   - **Alternatives:** keep the values as stored (LightGBM AUC 0.696 against 0.699 repaired), or set the ambiguous
     4/5-digit values to missing (0.694). The bug could be reported to the authors.

4. **`power_kva` and `installation_type`: major question, kept on purpose.**
   - **The concern:** both come from the inventory taken after the 2020 burns, so a transformer replaced in 2020 may
     show the size and mounting of its replacement. My first argument (2020 burns look like the 2015-2018 burns) could
     not separate risk from replacement, because those rows are replacements too. The verifier's evidence below replaces
     it.
   - **For a leak:**
     - The gain concentrates on the self-protected positives, the units where replacements show. Added to the site
       columns, `power_kva` raises LightGBM AUC by 0.107 for the 248 self-protected positives against all negatives, and
       by 0.023 for the other 381 positives.
     - `installation_type` on top adds 0.024 and 0.008.
     - 10 kVA units are 66.5% of the self-protected positives, 34.4% of the other positives and 21.1% of the negatives.
       H-structure mountings: 14.5%, 4.2%, 2.0%.
     - No 5 kVA unit is among the 163 self-protected first burns of 2020, against 25 among the 277 other first burns.
   - **Against:** kVA follows the load the same way in every group. 10 kVA units serve a median of 5-8 users whether
     never burned, burned in 2015-2018 or burned first in 2019 or 2020; 5 kVA units serve 3-4. So there is no sign of
     resizing on replacement.
   - **Implemented:** both kept, with these numbers in the "Potential leak, kept on purpose" bullet.
   - **Alternative:** drop `power_kva`, `installation_type` and `energy_not_supplied_kwh` (it carries kVA).
     - Without them, AUC is 0.628 within 2020 and 0.646 for 2019 -> 2020 (verifier: 0.626 and 0.650).
     - Keeping the outage hours EENS / (1.08 x kVA) gives 0.636 (verifier: 0.638).

5. **History markers in two columns (one marker).**
   - All 3,734 units burned in 2015-2018 have `removable_connectors` = 1 (34% of never-burned units). 99% have
     `energy_not_supplied_kwh` = 16.2 x kVA (36% of never-burned units).
   - EENS / (1.08 x kVA) is exactly 15 hours for 7,389 of the 7,719 units with connectors, and for 564 of the 8,154
     without. EENS is a planning formula whose restoration time is set by the connectors, so the two are one marker.
   - Neither is raised for the burns of 2019 or 2020 (16-17% and 20-21%).
   - Kept as history, in an Anomaly bullet.

6. **`burn_rate` is history, not a leak.**
   - For every transformer, 5 x rate2020 - 4 x rate2019 equals its number of burns in 2019. 440 of the 629 burned in
     2020 have rate 0.
   - A "failures in 2019" lag feature adds nothing (AUC 0.6985), so it is not added.

7. **Lightning period (cannot verify).** The article does not say which years the average and maximum ground discharge
   densities cover (Sec. 1, items D and E). They are one value per area, the same in both files. If they include 2020,
   they carry a little same-year information. This is noted in the lightning bullet.

8. **Source notes for the record.**
   - The IEEE DataPort link is a 2025 derivative, so the record should point to Mendeley v4 and the Data in Brief.
   - The paper says 15,869 transformers, the file holds 15,873: the authors' MATLAB table starts at the file's fifth
     row.
   - The authors' test table is a subset of their training table, so their reported accuracy is not a reference.

9. **Year convention.** `year = "2021"` (publication year); the data cover 2019-2020.
