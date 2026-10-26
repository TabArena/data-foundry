# Added datasets: issues (2026-10-01)

Open review issues, collected by `collect_reviews.py` on 2026-10-01 from the REVIEW.md of 1 dataset, the open issues of 1 record without a folder and the working copy's REVIEW.md. Edit those files, not this report.

**Open:** 2 records, 2 issues, 1 record field, 1 cross-dataset item.

## Summary per record

| Record | Outcome | Main points |
|---|---|---|
| [`airfoil_self_noise`](#airfoil_self_noise) | added | The target is in decibels; keep it? |
| [`churn_telco_south_asia_duplicate`](#churn_telco_south_asia_duplicate) | not added; duplicate | The files are the 2,000 rows of `churn_telco_south_asia` with renamed values. |

## Record fields that disagree with the definition

- `airfoil_self_noise`: year `2014`, definition `1989`.

## Across datasets

### Framework (`src/data_foundry/v2/`)

- **`dataset new` leaves `domain` as `"TODO"`.** A fresh scaffold then fails to import. Proposal: fill it from the
  record.

## Per dataset

### airfoil_self_noise

**Outcome:** added. NASA's wind-tunnel table as published; the AI recommends shipping it.

**Record judgment:** valid. NASA wind-tunnel measurements of airfoil noise.

**Issues for the curator:**

1. **Keep the target in decibels?** The source reports the scaled sound pressure level in dB; a log scale is the
   alternative.

**Review panel:** ship (mediator). Claim audit: 2 claims, 2 hold. Blind review: would benchmark; main concern the
decibel scale. Debate: agreed on the random split; disputed: the target scale (issue 1).

<details><summary>Claim audit</summary>

| Claim | Source | Test | Result | Rule |
|---|---|---|---|---|
| 1,503 rows | UCI page | row count | holds | |
| target in dB | NASA report, p. 3 | column range | holds | |

</details>

<details><summary>Mediator</summary>

Ship. The advocate and the critic agree on the split; the target scale stays open as issue 1.

</details>

### churn_telco_south_asia_duplicate

**Outcome:** not added; duplicate. The files are the 2,000 rows of `churn_telco_south_asia` with renamed values.

**Issues:**

1. **Leave it out as a duplicate?** Every row matches a row of `churn_telco_south_asia` once the values are
   renamed.
