# Added datasets: issues (2026-10-01)

A test run of `/add-dataset` on two records: one added, one left out.

**Counts:** 1 added, 1 not added.

## Summary per record

| Record | Outcome | Main points for the curator |
|---|---|---|
| [`airfoil_self_noise`](#airfoil_self_noise) | added | The target is in decibels; keep it? |
| [`churn_telco_nigeria`](#churn_telco_nigeria) | not added; duplicate | The rows of `churn_telco_south_asia` with renamed values. |

## Record fields that disagree with the definition

- `airfoil_self_noise`: year `2014`, definition `1989`.

## Across datasets

### Framework (`src/data_foundry/v2/`)

- **`dataset new` leaves `domain` as `"TODO"`.** A fresh scaffold then fails to import. Proposal: fill it from the
  record.

## Per dataset

### airfoil_self_noise

**Outcome:** added and checked.

**Record judgment:** valid. NASA wind-tunnel measurements of airfoil noise.

**Issues for the curator:**

1. **Keep the target in decibels?** The source reports the scaled sound pressure level in dB; a log scale is the
   alternative.

### churn_telco_nigeria

**Outcome:** not added. The files are the 2,000 rows of `churn_telco_south_asia` with renamed values.
