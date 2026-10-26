# aeolus_rebuilt

**Outcome:** added as `aeolus_rebuilt_1m`. The Aeolus task rebuilt from its origins at Lennart's ask (aeolus issue 8,
2026-10-26): US domestic flights of 2023-2024 from the BTS on-time table (13,708,650 operated flights, March 2024
included; a random 1M sample trains each window), target `ARR_DEL15`, the same three two-week windows as `aeolus_1m`,
with Meteostat's hourly weather at both airports joined in UTC at the full hour before the scheduled departure, BTS's
airport coordinates, and five columns on the aircraft's previous flight from its tail number, each known at that hour.
`dataset check` is clean; no task-probe flag (LightGBM ROC AUC 0.819, linear 0.760); no leak-probe flag that reads as a
leak. Steps 0-6 of /add-dataset ran; the review panel has not run yet.

**Main points:** Keep the operated flights only (issue 1); keep the prediction point at the full hour before departure
(issue 2); keep the previous flight's columns with a note on aircraft swaps (issue 3); keep Meteostat's
forecast-filled values (issue 4); retire `aeolus_1m` once this is accepted (issue 5).

**Record fields that disagree with the definition:**

- `year`: record `(empty)`, definition `2026`.

**Record judgment:** valid. A real delay-prediction task from the US DOT's own records, with the weather at the right
hour; what the Aeolus release adds is built from the same BTS fields (its flight chains and daily graphs), so the
origins hold everything the task needs, plus March 2024, 43 airports the release dropped, tail numbers,
cancellations and BTS coordinates (record assessment of 2026-10-26).

**Issues for Lennart:**

1. **Cancelled and diverted flights are not rows: keep it that way?** They are 1.6% of 2023-2024 (184,258 cancelled,
   34,051 diverted) and 0.4-1.4% of a test window, most in the holiday window; counted as late they would raise a
   window's late share by 0.3-1.1 points.
   - Implemented: operated flights only. BTS leaves `ArrDel15` empty for them, the paper's cohort has none (LEAK-22),
     and when a cancellation was decided is not recorded, so one decided before the prediction point cannot be told
     apart.
   - Alternative: count them as late, as DOT's Air Travel Consumer Report does (seen only in snippets of 2009-2011
     reports; not verified).
   - Rule: USE-5 and LEAK-22 (Must). Recommendation: keep; the fit stays approximate for it (USE-8).
   - Decision: keep, or count them as late.

2. **The prediction point: the full hour before the scheduled departure?** It lies 0-59 minutes before departure
   (median 27). By then 84% of the previous flights have landed, so this is a last-hour estimate for a passenger app
   or a gate, not an operations centre's plan hours ahead.
   - Implemented: the full UTC hour at or before the scheduled departure.
   - Alternative: a fixed earlier point, such as 2 hours before departure (a variant; the previous-flight columns
     would then hold less).
   - Rule: USE-1, USE-3. Recommendation: keep, and name the earlier variant in the notes.
   - Decision: keep, or move the point earlier.

3. **The previous flight's columns: keep them with a note on aircraft swaps?** BTS records the aircraft that flew. If
   a swap was decided after the prediction point, the row carries information from after it, and BTS does not say
   when swaps were decided. 2.6-3.4% of a window's rows are re-planned (the previous flight ended elsewhere or was
   scheduled to land after this departure); 54-61% of them are late.
   - Effect: setting their five `INBOUND_*` columns to none/missing costs 0.0002-0.0013 ROC AUC; scored without these
     rows the windows lose 0.007-0.011, about what they carry. All five columns add 0.15-0.17 (0.647-0.654 without).
   - Implemented: kept, with a `Potential leak, kept on purpose:` note.
   - Alternatives: mask the re-planned rows' columns, or drop the `INBOUND_*` columns (back to about 0.64).
   - Rule: LEAK-10 against LEAK-6 (a suspected leak, measured small; planned tail assignments, which would settle it,
     are not published). Recommendation: keep with the note.
   - Decision: keep with the note, mask the re-planned rows, or drop the columns.

4. **Meteostat's forecast-filled values: keep them?** Meteostat fills gaps with model forecasts: 97% of the condition
   codes, 41% of cloud cover, 5.9% of precipitation and 0.2% of temperature at the origin. A forecast for an hour is
   issued before it, but the issue times are not in the files.
   - Implemented: kept, as Aeolus kept Meteostat's values.
   - Alternatives: drop the condition code and cloud cover, or mask the model-sourced values.
   - Rule: USE-3, LEAK-10 (maybe; EV-6). Recommendation: keep.
   - Decision: keep, drop the two columns, or mask.

5. **Retire `aeolus_1m` once this is accepted?** Both come from the BTS on-time table and predict the same delay, so
   they are versions of one dataset (PROV-6, Must); this is option (b) of aeolus_1m's issue 8. airlines,
   airlines_depdelay_10m and pnwflights14 are already `Duplicate` of aeolus.
   - Recommendation: retire `aeolus_1m` (`No (Retired)` is not needed: it never shipped) when you accept this one.
   - Decision: retire aeolus_1m, or keep both.

6. **Metric origin (minor).** The definition declares `Metric.source("roc_auc")`, as aeolus_1m. The paper reports AUC
   and accuracy side by side, which MET-5 reads as no single choice, so the label would be `fallback`; the metric is
   the same ROC AUC either way.
   - Recommendation: relabel it as the fallback. Decision: relabel, or keep.
