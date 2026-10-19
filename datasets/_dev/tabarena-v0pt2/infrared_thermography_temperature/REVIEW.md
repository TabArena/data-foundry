# infrared_thermography_temperature

**Outcome:** added. PhysioNet's FLIR file of an FDA fever-screening study (1,018 subjects): regression of the oral
temperature `aveOralM` from the round-1 facial temperatures, the room conditions and what the person states, IID
over subjects. The AI recommends including it, with concerns: the split regime, the 17 retake rows and the modality
marker are open.

**Main points:** IID over subjects, with temporal or day-grouped splits as alternatives. The 17 retake rows are
kept. The modality marker is open.

**Issues for Lennart:**

1. **Split regime: IID over subjects, a temporal split on the measurement date (a calibration fitted once and used later), or folds grouped by measurement day?**
   - Implemented: IID over subjects, 10 x 3 random folds. Each prediction is for a new person who is in the file once.
     PhysioNet keeps the date as a time stamp for seasonal studies. The day's conditions (T_atm, Humidity, Distance,
     T_offset1) are features. The source's random 60/40 calibration split is cited together with its Sec. 4.5 best-case
     caveat.
   - Alternative: (a) Temporal: keep Date as a datetime and declare temporal = Temporal(on="Date",
     splits=TemporalSplits(window=None, unit="unique", n_windows=6, min_train_fraction=0.5)). This gives 6 windows of 12
     days over the newest half of the 154 days. (b) Grouped: grouping = Grouping(on="day", labels="per_sample",
     definition=...), with the yymmdd part of SubjectID, described as stricter than Wang 2022's random split.
   - Numbers: Temporal windows: 68-116 test subjects each, 4-26 of them at or above 37.5 °C. On the same test rows,
     training on all earlier subjects instead of a random set of the same size changes RMSE by -0.2% to +2.5% (5 models,
     20 random sets per window); with 10 windows (26-69 rows) the change is -1.0% to +2.8%. A year-1 calibration used on
     year 2 has RMSE +3% to +9%, over-predicts by 0.06-0.08 °C, and is worse on 11-14 of 15 folds. The set-up changed:
     two places (Wang 2022 Sec. 2.4), and the median distance went from 0.80 to 0.60-0.65 m. February 2018 holds 43 of
     the 111 febrile subjects. Grouped by day against random (10x3): R^2 within 0.004 for all 5 models. Day ICC: 0.03
     for the target, 0.14 for aveOralM - T_Max1; out-of-day residual ICC 0.00-0.06.

2. **The 17 subjects without a complete round-1 image: keep their round-2/3 image (taken after the first oral reading), drop them, or leave the image missing?**
   - Implemented: Keep, under the round-1 names, with no round indicator. The source counted these subjects in its
     round-1 analysis (Zhou 2020 Table 5: 47/30/19 febrile subjects = all 544 group-1 subjects). The timing and the bias
     are documented in curation_comments and Decision 2.
   - Alternative: Drop the 17 rows, which keeps every image before the prediction point. Or leave their 27 image values
     missing, as in the source file.
   - Numbers: Models over-predict the 17 by 0.07-0.14 °C, against at most 0.01 °C elsewhere. Their RMSE is 0.33-0.39
     kept and 0.77-0.90 left missing; overall R^2 is 0.66-0.71 against 0.63-0.67. Dropping them loses 5 of the 111
     subjects at or above 37.5 °C and 4 of the 49 at or above 38 °C. If left missing, the missingness marks a group that
     is 29% febrile (10.6% elsewhere). Retake rows are hard to detect from the features (reviewer: LightGBM AUC 0.58).

3. **Does the record's Wrong Domain / Source Modality marker exclude the dataset? The guidelines exclude features measured from images; satimage and wilt (pixel values) are No.**
   - Implemented: In scope as an exception, since Lennart asked to add the dataset. The curation_comments note names the
     conflict with the guidelines and gives the reasons: radiometric site temperatures in °C, sites named by ISO/TR
     13154, no images released, and the task is the source's calibration.
   - Alternative: Exclude under criterion 4A: set No with Wrong Domain / Image and remove the folder.
   - Numbers: The face maximum T_Max1 alone, with the source's segmented calibration, reaches R^2 0.700. All features
     reach 0.709 (RF), and an additive model 0.727, which beats the calibration on 28/30 splits. Key points were placed
     by hand for about half the images (Zhou 2020 Sec. 2.2). Precedent: biomechanical_orthopaedic_prediction ships as
     Yes (Disagreement) with the same marker.
