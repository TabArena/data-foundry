# airfoil_self_noise

**Outcome:** added. NASA's wind-tunnel table as published; the AI recommends shipping it.

**Main points:** The target is in decibels; keep it?

**Record fields that disagree with the definition:**

- `year`: record `2014`, definition `1989`.

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
