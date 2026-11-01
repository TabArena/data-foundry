# qsar_bioconcentration

**Outcome:** added; the structure now ships as a `SMILES` column and RDKit's 193 descriptors are gone (CLEAN-24 as
amended, 2026-11-01). One question is left over from that change: `logKOW`, the one feature that is not derived from
the structure, is a measurement for 652 chemicals and a model's prediction for 122.

**Main points:** whether the 122 predicted `logKOW` values stay, go to missing, or take the column with them.

**Issues for Lennart:**

1. **Keep the 122 predicted `logKOW` values?** You asked where they come from. From the source paper, read on
   2026-11-01 (Grisoni et al. 2015, Chemosphere 127:171-179, Sec. 3.1): "Experimental KOW values were obtained from
   VEGA log P dataset. If no experimental value was provided, a consensus KOW was predicted, as suggested by (Cronin
   and Livingstone, 2004)." So the predicted values are VEGA's consensus logP, an average over its logP QSAR models,
   computed from the structure. The arithmetic of the shipped numbers agrees: 64% of the 402 predicted values in the
   authors' table are exact thirds of three-decimal numbers, the mean of three model predictions, while every
   experimental value has two decimals.

   What this is **not**: the models are trained on external logP measurements, not on this dataset, and they predict an
   input property, not our target. So no row's feature is built from another row's label, and no all-row statistic is
   involved (LEAK-27 to LEAK-31 do not apply).

   It is also **not circular with the label**, which matters here because the class is read from a band around the TGD
   line through logBCF and logKOW. If the authors had assigned the class of these rows from their predicted logKOW, the
   rule would reconstruct it. Measured on 2026-11-01: the band reproduces the shipped class for 94.7% of the 638 rows
   with a measured logKOW, but only 72.5% of the 120 with a predicted one. So the predicted value did not define those
   labels.

   What is left is a column of mixed provenance: a measurement for 84% of rows, a structure-derived estimate for 16%.
   Since 2026-11-01 the structure itself ships, so a benchmark can compute a logP for every chemical by one method,
   consistently, instead of getting a precomputed one for some rows only. Under CLEAN-24 as amended, columns computed
   from the structure leave and measured properties stay, which splits this column in two.

   Implemented: all 774 values ship, with `logKOW_type` marking which is which (652 measured, 122 predicted, 2
   missing), as you decided on 2026-10-26 under USE-6 and USE-3: the assessor of the use case holds the chemical's
   logKOW, a cheap lab test that REACH requires from one tonne a year.

   Alternative A: set the 122 predicted values to missing and keep `logKOW` as a pure measurement, with `logKOW_type`
   dropped or kept as a missingness flag. Then every structure-derived number reaches the model by one route, the
   encoding of the SMILES. Against it: the use case's assessor would also use a predicted logKOW when no measurement
   exists, so the task becomes slightly easier than reality, and 16% of rows lose a feature.

   Alternative B: drop `logKOW` and `logKOW_type` entirely and ship the structure alone, as the four other molecule
   datasets now do. Against it: the logKOW is genuinely measured for 84% of rows and is the first tier of the real
   bioaccumulation screen, so dropping it removes a real input rather than a modelling choice. Alone it scores macro
   ROC AUC 0.659, so it carries signal.

   One related number, for completeness: the share of classes differs between the two groups (lipid storage 61% of
   measured rows against 48% of predicted ones). That reflects which chemicals get measured in the first place, not
   information about the label.
