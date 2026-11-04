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

1. **Keep the target in decibels?**

   * **Problem:**
     - The target is the sound pressure level in decibels, as NASA reports it.
     - Should it get a further log?
   * **Background:** Decibels are already a log scale, so a further log changes how errors on loud and quiet
     airfoils are weighed[^1].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Decibels (implemented) | target as published | the unit engineers use | none found |
     | B | Log of decibels | target transformed | none found | a log of a log scale |

   * **Recommendation:** A, the source's unit. **Decision:** A or B?

   **Notes for the AI:** on B, set `target_transform` in `dataset.py` and re-run `dataset check`.

   [^1]: **MET-3** (Must): the score is on the scale the task means, the source's; the target may ship on the
     scale a practitioner models it on.

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

1. **Leave it out as a duplicate?**

   * **Problem:** Every row matches a row of `churn_telco_south_asia` once the values are renamed[^1].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Leave out (implemented) | the record gets `No` | no copy in the benchmark | none found |
     | B | Add it | a second folder | none found | the same rows twice |

   * **Recommendation:** A. **Decision:** A or B?

   [^1]: **PROV-3** (Must): the data is real, not a real table someone reworked (relabelled, columns renamed).
