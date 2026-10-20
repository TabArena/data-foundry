# aeolus

**Outcome:** added as `aeolus_1m`. US domestic flights from 2023 on (1,785,315 rows), binary target `ARR_DEL15`
(arrival 15 minutes or more late), three two-week test windows at the end of 2024, weather as released. The AI
recommends shipping it.

**Main points:** The Kaggle card and the paper give different licences (noted only); the Kaggle download has no
pinned version.

**Record judgment:** valid: delay prediction with a temporal split, from the authors' release of BTS flights and
Meteostat weather (Xu et al., NeurIPS 2025).

**Issues for Lennart:**

5. **Licence conflict (noted only).** The Kaggle card says Apache-2.0, the paper says CC BY-NC 4.0. BTS data are US
   government works. Meteostat's page states CC BY 4.0 (dev.meteostat.net/license).

6. **No pinned version.** kaggle 2.2.2 refuses `owner/slug/versions/N` (the verifier tested it).
   - `download_description` lists SHA-256 prefixes of the nine CSVs; the verifier re-hashed all nine and they match.
   - A local backup of the 15.2 GB of CSVs is the safeguard.
