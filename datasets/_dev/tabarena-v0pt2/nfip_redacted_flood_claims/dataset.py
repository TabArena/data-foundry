"""Curated dataset definition for `nfip_redacted_flood_claims` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    SplitPlan,
    TaskSummary,
    Temporal,
    TemporalSplits,
    decode,
    drop_columns,
    set_missing,
)

TARGET = "amount_paid_building_contents_usd"

HISTORY_START = pd.Timestamp("2010-01-01")
"""The first date of loss kept (History bullet)."""

RELEASE_CUT = pd.Timestamp("2024-01-01")
"""The first date of loss left out: claims of 2024 to 2026 are still being paid (LEAK-24, notes)."""

POST_OPENING = [
    # The payments and what is set with them (the target's parts, the ICC claim, the net amounts and recoveries).
    "amountPaidOnBuildingClaim",
    "amountPaidOnContentsClaim",
    "amountPaidOnIncreasedCostOfComplianceClaim",
    "netBuildingPaymentAmount",
    "netContentsPaymentAmount",
    "netIccPaymentAmount",
    "nonPaymentReasonBuilding",
    "nonPaymentReasonContents",
    "mostRecentPaymentDate",
    "mostRecentRecoveryDate",
    "totalSalvageRecovery",
    "totalBldgClaimPmtRecovery",
    "totalContentsClaimPmtRecovery",
    "totalIccClaimPmtRecovery",
    "totalSubrogationRecovery",
    "replacementCostBasis",
    # The adjuster's report: damage, values before the flood, replacement costs (filled exactly where the damage is).
    "buildingDamageAmount",
    "contentsDamageAmount",
    "buildingPropertyValue",
    "contentsPropertyValue",
    "buildingReplacementCost",
    "contentsReplacementCost",
    # The adjuster's reading of the flood at the building, and the cause and handling code of the loss.
    "waterDepth",
    "exteriorWaterDepth",
    "interiorWaterDepth",
    "floodWaterDuration",
    "floodCharacteristicsIndicator",
    "causeOfDamage",
    # Values of today's flood map and community, looked up at extraction (filled for 21% of the 2010 claims).
    "floodZoneCurrent",
    "nfipCommunityNumberCurrent",
]

COPIES_AND_IDS = [
    "id",  # the record id
    "asOfDate",  # the extraction date, one value
    "reportedCity",  # "Currently Unavailable" on every record
    "yearOfLoss",  # in dateOfLoss
    "nfipCommunityName",  # the name of nfipRatedCommunityNumber
    "eventDesignationNumber",  # in event_code
    "ficoNumber",  # in event_code
    "openDate",  # in days_loss_to_open
    "iccCoverage",  # $30,000 on every claim that has a value
]

DEDUCTIBLE_USD = {
    "0": 500,
    "1": 1_000,
    "2": 2_000,
    "3": 3_000,
    "4": 4_000,
    "5": 5_000,
    "9": 750,
    "A": 10_000,
    "B": 15_000,
    "C": 20_000,
    "D": 25_000,
    "E": 50_000,
    "F": 1_250,
    "G": 1_500,
    "H": 200,
}
"""The data dictionary's deductible codes in dollars (H: $200, Group Flood Insurance Policies only)."""

ELEVATION_SENTINEL = 9_000
"""Elevation fields at or beyond +-9,000 ft are the dictionary's "not reported" values (9999.0 and the like)."""

ELEVATIONS = ["elevationDifference", "baseFloodElevation", "lowestAdjacentGrade", "lowestFloorElevation"]

HIGHEST_POINT_FT = {
    "AL": 2_413, "AK": 20_310, "AZ": 12_633, "AR": 2_753, "CA": 14_505, "CO": 14_440, "CT": 2_380, "DE": 448,
    "DC": 409, "FL": 345, "GA": 4_784, "HI": 13_796, "ID": 12_662, "IL": 1_235, "IN": 1_257, "IA": 1_670,
    "KS": 4_039, "KY": 4_145, "LA": 535, "ME": 5_267, "MD": 3_360, "MA": 3_489, "MI": 1_979, "MN": 2_301,
    "MS": 806, "MO": 1_772, "MT": 12_807, "NE": 5_427, "NV": 13_147, "NH": 6_288, "NJ": 1_803, "NM": 13_161,
    "NY": 5_344, "NC": 6_684, "ND": 3_506, "OH": 1_549, "OK": 4_973, "OR": 11_249, "PA": 3_213, "RI": 812,
    "SC": 3_560, "SD": 7_244, "TN": 6_643, "TX": 8_751, "UT": 13_528, "VT": 4_395, "VA": 5_729, "WA": 14_411,
    "WV": 4_863, "WI": 1_951, "WY": 13_809, "PR": 4_390, "VI": 1_556, "GU": 1_332, "AS": 3_170, "MP": 3_166,
}  # fmt: skip
"""Each state's or territory's highest point in feet (USGS); a building elevation above it is impossible (CLEAN-11)."""

LATE_FIELDS = [
    "elevatedBuildingIndicator",
    "postFIRMConstructionIndicator",
    "preFirmIndicator",
    "elevationCertificateIndicator",
    "baseFloodElevation",
    "lowestFloorElevation",
    "lowestAdjacentGrade",
    "elevationDifference",
    "foundationType",
    "obstructionType",
    "basementEnclosureCrawlspaceType",
    "floodproofedIndicator",
    "originalConstructionDate",
    "originalNBDate",
]
"""The building fields a large loss can change (elevating or rebuilding after substantial damage, a new policy):
blanked on the rows whose policy block is located as a later term (LEAK-10)."""

RR2_START = pd.Timestamp("2021-10-01")
"""Risk Rating 2.0 began on 2021-10-01: a rating method "RE" on an earlier loss marks a later policy term."""

WINDOW_STARTS = ("2022-07-01", "2023-01-01", "2023-07-01")
"""The test windows, half-years of losses (2022H2, 2023H1, 2023H2)."""

SPANNING_EVENT_DAYS = 31
"""A training claim with a test window's event name and a loss this close before the window start is the same storm
(the California Atmospheric River of DR-4683, 2022-12-27 to 2023-01-31, carries no event code)."""

CODE_LABELS = {
    "basementEnclosureCrawlspaceType": {
        0: "None",
        1: "Finished basement/enclosure",
        2: "Unfinished basement/enclosure",
        3: "Crawlspace",
        4: "Subgrade crawlspace",
    },
    "elevationCertificateIndicator": {
        "1": "No EC, policy before 1 Oct 1982",
        "2": "No EC, policy on or after 1 Oct 1982",
        "3": "EC with BFE",
        "4": "EC without BFE",
        "A": "Basement or subgrade crawlspace",
        "B": "Fill or crawlspace",
        "C": "Piles, piers or columns with enclosure",
        "D": "Piles, piers or columns without enclosure",
        "E": "Slab on grade",
    },
    "locationOfContents": {
        1: "Basement/enclosure/crawlspace only",
        2: "Basement/enclosure/crawlspace and above",
        3: "Lowest floor only above ground level",
        4: "Lowest floor above ground level and higher floors",
        5: "Above ground level more than one full floor",
        6: "Manufactured (mobile) home or travel trailer on foundation",
        7: "Enclosure/crawlspace and above",
    },
    "numberOfFloorsInTheInsuredBuilding": {
        1: "One floor",
        2: "Two floors",
        3: "Three or more floors",
        4: "Split-level",
        5: "Manufactured (mobile) home or travel trailer on foundation",
        6: "Townhouse/rowhouse with three or more floors",
    },
    "obstructionType": {
        10: "Free of obstruction",
        15: "Enclosure/crawlspace with proper openings, not used for rating",
        20: "Under 300 sq ft breakaway walls, no M&E below lowest elevated floor",
        24: "Under 300 sq ft breakaway walls or finished, M&E below BFE",
        30: "300 sq ft or more breakaway walls, no M&E below BFE",
        34: "300 sq ft or more breakaway walls or finished, M&E below BFE",
        40: "No walls, M&E below BFE",
        50: "Non-breakaway walls/crawlspace or finished enclosure, no M&E",
        54: "Non-breakaway walls/crawlspace or finished enclosure, with M&E",
        60: "With obstruction",
        70: "Subgrade crawlspace with certification",
        80: "Subgrade crawlspace without certification",
        90: "Enclosure: elevator below BFE in A zone, no other enclosure",
        91: "Free of obstruction: elevator enclosed by lattice below BFE in V zone",
        92: "Enclosure: elevator below BFE in A zone, improper or finished enclosure",
        94: "Obstruction: elevator below BFE in V zone, nothing else",
        95: "Obstruction: elevator and unfinished breakaway walls below BFE in V zone",
        96: "Obstruction: elevator below BFE in V zone, finished breakaway walls",
        97: "Obstruction: elevator and M&E below BFE in V zone",
        98: "Obstruction: elevator, breakaway walls and M&E below BFE in V zone",
    },
    "occupancyType": {
        1: "Single family residence",
        2: "2 to 4 unit residential building",
        3: "Residential building with more than 4 units",
        4: "Non-residential building",
        6: "Non-residential business",
        11: "Single-family residential building (RR2.0)",
        12: "Residential non-condo building, 2-4 units (RR2.0)",
        13: "Residential non-condo building, 5 or more units (RR2.0)",
        14: "Residential mobile/manufactured home (RR2.0)",
        15: "Residential condo association building (RR2.0)",
        16: "Single residential unit in a multi-unit building (RR2.0)",
        17: "Non-residential mobile/manufactured home (RR2.0)",
        18: "Non-residential building (RR2.0)",
        19: "Non-residential unit in a multi-unit building (RR2.0)",
    },
    "condominiumCoverageTypeCode": {
        "N": "Not a condominium",
        "U": "Individual condominium unit",
        "A": "Condominium association",
        "H": "Condominium master policy (RCBAP), high-rise",
        "L": "Condominium master policy (RCBAP), low-rise",
    },
    "disasterAssistanceCoverageRequired": {
        0: "Not required",
        1: "SBA",
        2: "FEMA",
        3: "Code 3 (not in the data dictionary)",
        4: "HHS",
        5: "Other agency",
    },
    "buildingDescriptionCode": {
        1: "Main house",
        2: "Detached guest house",
        3: "Detached garage",
        4: "Agricultural building",
        5: "Warehouse",
        6: "Pool house, clubhouse, recreation building",
        7: "Tool/storage shed",
        8: "Other",
        9: "Barn",
        10: "Apartment building",
        11: "Apartment unit",
        12: "Cooperative building",
        13: "Cooperative unit",
        14: "Commercial building",
        15: "Condominium (entire building)",
        16: "Condominium unit",
        17: "House of worship",
        18: "Manufactured (mobile) home",
        19: "Travel trailer",
        20: "Townhouse/rowhouse",
        21: "Code 21 (not in the data dictionary)",
    },
    "foundationType": {
        "1": "Slab",
        "2": "Basement",
        "3": "Crawlspace",
        "4": "Elevated without enclosure, post, pile or pier",
        "5": "Elevated with enclosure, post, pile or pier",
        "6": "Elevated with enclosure, not post, pile or pier",
    },
}
"""The data dictionary's words for each coded field (CLEAN-12), shortened; codes it does not list are named so."""

CATEGORICAL = [
    *CODE_LABELS,
    "ratedFloodZone",
    "state",
    "reportedZipCode",
    "countyCode",
    "censusGeoid",
    "nfipRatedCommunityNumber",
    "floodEvent",
    "event_code",
]


class NfipRedactedFloodClaims(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "How much will the US National Flood Insurance Program pay on a flood claim, building and contents "
            "together, judged when the claim is opened?"
        ),
        use_case=(
            "When a flood claim is opened, the NFIP's claims staff (FEMA and the Write Your Own insurers) set its "
            "first reserve and add up the expected loss of a flood event; FEMA's bulletins W-08095 and W-10008 "
            "describe this first reserve as a system-generated amount or a desk estimate (the model is ours)."
        ),
        row=(
            "One flood insurance claim on one building, with a loss between 2010 and 2023, closed with or without "
            "payment (OpenFEMA's redacted claims, extract of September 2026)."
        ),
        predicted=(
            "The dollars paid on the building and contents coverages together, as recorded in September 2026; 0 for "
            "a claim closed without payment (16% of the claims)."
        ),
        known=(
            "The policy (coverage, deductibles, flood zone, elevation), the building (use, floors, foundation, "
            "construction date), the place (state to census block group, rounded coordinates), the date of loss, the "
            "flood event's name and code, and how many days after the loss the claim was opened."
        ),
        split=(
            "Each test window is half a year of losses (2022H2, 2023H1, 2023H2), trained on the claims with a loss "
            "from 2010 that were opened before the window starts, without the window's own flood events."
        ),
        changes=(
            "We add the building and contents payments, count a claim closed without payment as 0, leave out claims "
            "still open, clerical records and negative payments, drop every field the adjuster or the payment sets, "
            "and keep the losses of 2010 to 2023."
        ),
        fit="approximate",
        fit_reason=(
            "The fields are a claim's at opening and the windows test new flood events, but the record holds the "
            "policy's latest term (blanked where it is located, not everywhere), a claims desk also sees the "
            "property's earlier claims and the first notice of loss (both redacted), and the newest payments may "
            "still grow."
        ),
    )

    # Dataset
    unique_name = "nfip_redacted_flood_claims"
    year = "2019"
    domain = "insurance"
    source = "GOV Website"
    source_url = "https://www.fema.gov/openfema-data-page/nfip-redacted-claims-v3"
    license = "OpenFEMA Terms and Conditions (https://www.fema.gov/about/openfema/terms-conditions); no licence named"
    data_tags = ("Spatial",)
    download_description = r"""
        The OpenFEMA entity NfipClaims v3 (catalogue https://www.fema.gov/api/open/v1/DataSets, 2,725,989 records, data refreshed 2026-09-09, read 2026-11-09). The bulk files of the catalogue (https://www.fema.gov/about/reports-and-data/openfema/v3/NfipClaimsV3.parquet and .csv) answered 403 to this machine, and the API's one-file stream ($allrecords=true) broke off, so we read the API per year of loss as parquet, from 2011 in pages of 10,000 records ordered by id:

        mkdir -p local-data-warehouse/nfip_redacted_flood_claims && cd local-data-warehouse/nfip_redacted_flood_claims
        for y in $(seq 1978 2010); do curl -sS --fail -o NfipClaims_v3_yearOfLoss_$y.parquet "https://www.fema.gov/api/open/v3/NfipClaims?\$filter=yearOfLoss%20eq%20$y&\$format=parquet&\$allrecords=true"; done
        # from 2011, per year y with n records (n from ...&$inlinecount=allpages&$top=1&$format=json), for skip = 0, 10000, ...:
        curl -sS --fail -o NfipClaims_v3_yearOfLoss_${y}_skip$(printf %06d $skip)_top10000.parquet "https://www.fema.gov/api/open/v3/NfipClaims?\$filter=yearOfLoss%20eq%20$y&\$orderby=id&\$skip=$skip&\$top=10000&\$format=parquet"

        Two pages (2011 from record 40,000, 2023 from record 10,000) break off reproducibly, because one record of each holds a value beyond the parquet schema's 16-bit integer in `numberOfUnits` (99,999 and 34,970). Those pages are read in smaller pages ($top=1000, 100, 10, 1: the files `_skip<n>_top<k>.parquet`), and the two records alone as JSON ($format=json), written as parquet with the API's schema and the 16-bit fields widened to 32 bits. Every year's rows were checked against the API's count, and the ids are unique (2,725,989). The script is in the run folder (local-data-warehouse/_runs/2026-11-08_large_add/nfip_redacted_flood_claims/scripts/download3.py). The table is refreshed monthly: a later download holds newer payments of the same claims.
    """
    bibtex = r"""
        @misc{fema2026NfipClaimsV3,
          author       = {{Federal Emergency Management Agency}},
          title        = {{OpenFEMA} Dataset: {NFIP} Redacted Claims - v3},
          year         = {2026},
          howpublished = {\url{https://www.fema.gov/openfema-data-page/nfip-redacted-claims-v3}},
          note         = {API endpoint \url{https://www.fema.gov/api/open/v3/NfipClaims}, data refreshed 2026-09-09, accessed 2026-11-09. This product uses the Federal Emergency Management Agency's OpenFEMA API, but is not endorsed by FEMA.},
        }
    """
    curation_comments = """
        We start with the 2,725,989 records of OpenFEMA's "FIMA NFIP Redacted Claims - v3" (entity NfipClaims, 84 fields, losses 1978 to 2026, read through the API on 2026-11-09), with its data dictionary (the v3 page and the DataSetFields API). FEMA publishes the table for transparency and defines no prediction task. One record is "a claims transaction" (v3 page); no record shares its id, and no claim id links records.

        - Prediction point: the claim is opened (`openDate`), before an adjuster inspects the building. A field is kept only if it holds what was known then: the policy and the building as rated, the place, the date of loss and the flood event.
        - Target: `amountPaidOnBuildingClaim` plus `amountPaidOnContentsClaim`, in dollars, untransformed (`amount_paid_building_contents_usd`). The two amounts are missing together (never one alone), on claims closed without payment: 108,690 of the kept claims carry a "Claim Closed Without Payment Reason" (`nonPaymentReasonBuilding` or `nonPaymentReasonContents`) and count as 0, and 19,777 more have 0 paid on both; 15.7% of the kept claims are 0. The median is $18,560, the 99th percentile $350,000 and the largest $10.8 million (a condominium association insuring 198 units, Hurricane Ian); 48,250 claims (5.9%) are paid exactly a coverage limit and hold 21.2% of the dollars (residential building coverage is at most $250,000). The ICC payment (Increased Cost of Compliance, money to elevate or demolish a substantially damaged building, a separate coverage paid later) is not in the target (17,746 claims with one).
        - Dropped rows: claims with neither an amount nor a non-payment reason (2,771; open or unsettled, in every year); claims with a negative amount (73: "a check issued to a policy holder is not cashed and has to be re-issued", data dictionary, so the record is not the claim's payout); claims closed at 0 with reason 98 "Error-delete claim (no assignment)" or 99 "Erroneous assignment" on either coverage (37,328, 4.35% of the 2010-2023 records): clerical records, not a flood loss (2,276 claims with such a code on one coverage and a payment on the other stay); and 1,338 records equal to another in every field but the id (double entries).
        - History: losses from 2010-01-01. The claims' policy and building fields are filled far more often from 2009-2011 on (the building description 8% in 2000, 44% in 2009, 61% in 2010, 78% in 2011; the basement type 14% in 2000, 56% in 2010), and the median building coverage grows towards the $250,000 limit of today's residential policies ($104,000 in 2000, $191,200 in 2010, $250,000 first in 2012). Risk Rating 2.0 (October 2021) is a second break, inside the history: the rating fields change their codes (bullet "Later policy term"). The 1,746,181 claims of 1978-2009 are left out; with them every train side would exceed 1M rows (a `_1m` version).
        - Release cut (LEAK-24): losses up to 2023-12-31. The payments keep growing for years after a loss: of the claims of 2017-2021, those last paid more than 712 days after the loss (the median age of a 2024 loss in the September 2026 extract) hold 2.9% to 4.9% of the year's dollars, and of 2022 (Hurricane Ian) 17.3%; more than 982 days after (the youngest 2023 loss) 1.5% to 2.7%, and 9.0% for 2022. These are the claims still being paid, an upper bound on the dollars still missing. So 2024 (Helene and Milton) is left out with 2025 and 2026 (121,354 claims). Within the kept windows the newest losses still lose a few percent of their dollars to later payments: 3.61% of 2022's dollars are in claims last paid in 2026. A second download to measure how the labels move (LEAK-24) was not available (no archived extract); revisit in 2027, when 2024 has settled.
        - Dropped, set after the claim is opened (LEAK-10; `POST_OPENING`): the payments, net payments, recoveries, the ICC payment, the payment and recovery dates and the non-payment reasons (the outcome); the adjuster's report: the building and contents damage, their values before the flood "as estimated by an adjuster", the replacement costs (filled on the same claims as the damage amounts, 99.9% agreement, so from the same report) and whether the claim settled at replacement cost or actual cash value; the water depths (inside, outside, at the building) and the hours the water stayed; `causeOfDamage` (how the building was damaged, set in adjustment: code 0 "Other causes" is 38.7% zeros against 8.7% to 14.3% for the flood codes, the 5,831 missing codes are 91.4% zeros, and the field is worth 541 / 3,045 / 1,838 RMSE on the old yearly windows); `floodCharacteristicsIndicator` (empty from 2010). Earlier triage (2026-10-27/30) measured the damage amounts at ROC AUC 0.983 for a payout, and water depth and duration lifting a model at opening from 0.578 to 0.772 (train 2021-22, test 2023).
        - Dropped, looked up at extraction (LEAK-10): `floodZoneCurrent` and `nfipCommunityNumberCurrent`, the property's flood zone and community on today's maps ("where the insured property is currently located", data dictionary), filled for 21% of the claims of 2010 and 99% of 2018; the zone that rated the policy (`ratedFloodZone`) and the rated community stay.
        - Dropped as copies, identifiers or constants: `id`; `asOfDate` (one date); `reportedCity` ("Currently Unavailable" on every record); `yearOfLoss` (in `dateOfLoss`); `nfipCommunityName` (the name of the rated community number); `iccCoverage` ($30,000 on every claim with a value); `openDate` (in `days_loss_to_open`); `eventDesignationNumber` and `ficoNumber` (in `event_code`).
        - Built: `event_code`, the catastrophe's code, the Event Designation Number from June 2020 ("TX0220") and before it "FICO " and the Flood Insurance Claims Office number (one per affected state); `days_loss_to_open`, the days from the loss to the opening (310 openings before the loss are set missing); `building_deductible_usd` and `contents_deductible_usd`, the deductible codes as the dictionary's dollar amounts (missing when the code is).
        - Codes to words (CLEAN-12): the basement, elevation certificate, contents location, floors, obstruction, occupancy, condominium, disaster assistance, building description and foundation codes as the dictionary's words, shortened (`CODE_LABELS`). Codes the dictionary does not list are named so: building description 21 (2 claims), disaster assistance 3 (9 claims). Foundation code 0 (58.4% of the claims) is "not collected": 99.97% of the rows rated before Risk Rating 2.0 carry it and none rated by it, so it is set missing. The occupancy codes mix two schemes: the 2-digit codes belong to Risk Rating 2.0, the NFIP's rating since October 2021, and stay as decoded (a model may merge them). `numberOfFloorsInTheInsuredBuilding` stays unordered: beside one, two and three or more floors it holds split-level, mobile home and townhouse, a second dimension (CLEAN-14).
        - ZIP codes: five digits, as published apart from 130 empty values (set missing), 135 ZIP+4 codes (cut to five digits) and 47 codes that lost their leading zeros ("7631" for 07631, restored); a category, with the rounded coordinates for nearness.
        - Missing values (CLEAN-10): the elevation fields at +-9,000 ft or beyond (the dictionary's "9999.0 ... not reported" and its like: 2,945 base flood elevations, 1,370 lowest floors, 167 lowest adjacent grades, 5 elevation differences); the construction date 1492-10-12 (4,161 claims, a placeholder) and 4 dates before 1700; 28 policy dates before 1968, when the NFIP began; `numberOfUnits` of 34,970 and 99,999 (the next largest is 5,000). Impossible elevations (CLEAN-11): a base flood elevation, lowest floor or lowest adjacent grade above the highest point of its state (302, 185 and 95 values, most in Louisiana and Florida, with a cluster at 990 ft), the one -999.9, and an elevation difference beyond 100 ft (87); two coordinates outside the US (an NC claim at -36.0/174.0, a GU claim at 14.6/121.0).
        - Later policy term (LEAK-10): a claim's record holds the policy as of its latest term, not always the term of the loss. Located three ways: 264,880 claims before October 2021 carry Risk Rating 2.0's rating method "RE" (44% of the 2015-2019 claims; decision table), 24,358 policies started after the loss (`originalNBDate`), and 5,218 buildings were built after it (rebuilt; median paid $81,000 against $18,000, 3.8% zeros against 15.8%). On these rows the 14 fields a large loss can change (elevating or rebuilding after substantial damage) are blanked (`LATE_FIELDS`): elevation and floodproofing indicators, pre- and post-FIRM, the elevation certificate, the four elevations, foundation, obstruction, basement type, construction date and policy start date; a blank there marks such a row. `rateMethod` is dropped: in the test windows 99.5% of the rows are rated "RE", so it carries only the scheme marker. With the yearly windows of the first build, 71.8% of the 2021 test claims were located as a later term and blanking did not cure it (the scheme stayed readable at AUC 0.999), so the windows start in July 2022, when every renewal has passed to Risk Rating 2.0: no test row is located by its rating, and 1,381, 184 and 81 by a policy or building date after the loss. Not located: Ian's claims (2022H2) are 96.8% coded by Risk Rating 2.0 against about 60% that the renewal schedule allows, so a share of their fields may come from a term after the loss; the coverage, deductibles, zone and community are kept on located rows (no traced mechanism; 4,026 claims paid above their building coverage). Revisit if FEMA documents the term.
        - Kept, known at opening: `floodEvent` and `event_code`. A catastrophe gets its name and code when the event is designated, by a bulletin issued with the event (dictionary), and 13% of the claims of a named event are 0 against 24% of the others. The training side of a window leaves out the claims of the window's events (same code, or same name within 31 days of the start: the California Atmospheric River of DR-4683, 2022-12-27 to 2023-01-31, has 356 training claims before 2023H1 and no code).
        - Protocol (LEAK-9, an evaluation leak): each test claim is predicted from the training rows and its own features only; no feature or fit uses the test rows (counts of claims, event sizes or other aggregates over them). Counting each event's claims over the test block gave a participant +10,396 RMSE on the Ian window of the first build (4.7%). The count of claims opened so far is a real deployment input that this batch protocol leaves out.
        - Note: the target is in nominal dollars, not adjusted for inflation; the mean claim moves with the year's events ($94,360 in 2022, Hurricane Ian, against $21,000 to $55,000 in most years of 2010-2023).
        - Note: no amount at risk (MET-14, MET-15): the target is one claim's payment, and the coverage and deductibles that cap it are known at opening, so they are features; no weight.
        - Note: duplicate rows are kept otherwise: 2,113 rows (0.3%) equal another row in every kept column and the target; as records they differ in a dropped field (the adjuster's report, a payment date), so they are separate records; with the same date of loss they never fall on both sides of a window. After the blanking, 11,107 rows (1.4%) share all features with another and differ in the target: claims of the same event and place whose differences sit in the adjuster's report.
        - Note: some properties claim more than once (no property id, so repeats cannot be found); a repeat claim of a building is a known building, which a reserving model would also see (SPLIT-13).
        - Note: the data are redacted by FEMA (no names or addresses; coordinates rounded to one decimal); the census block group and the ZIP code are published as they are. The OpenFEMA terms forbid re-identification and the use of the data "to make determinations that might affect an individual's rights or eligibility for benefits"; the terms also say "The data can be used to make decisions on program management", and a reserve is one. Advance payments and inspection triage are left outside the use case: they decide for an individual claimant.
        - Note: the record links `nfip_redacted_claims` (Andrej) as a duplicate of this task (`No`, Duplicate; CC 2026-11-08, Lennart); its notes (negative amounts on reissued checks, water depth sometimes in feet) are covered here.
    """

    # Task
    target = TARGET
    problem_type = "regression"
    metric = Metric.fallback(
        reason=(
            "FEMA publishes the claims for transparency and defines no task or metric (the v3 data page, its data "
            "dictionary and the OpenFEMA catalogue, read 2026-11-09); no competition on the table was found (web "
            "search 2026-11-09). The papers on NFIP claims model other units: Wing et al. (2020, Nature "
            "Communications 11:1444) fit depth-damage relations with the adjuster's water depth, and Salas, Saha and "
            "Ravela (2022, arXiv 2212.08660) the claims of a county and year from rainfall (abstracts read). So the "
            "regression fallback, RMSE on the dollars: a reserve is set in dollars and an event's loss is the sum of "
            "the reserves, which the mean minimises. The mean Poisson deviance, also minimised by the mean, is the "
            "alternative from context (curator issue): on the half-year windows, early-stopped LightGBM beats the "
            "training mean on 2023H1 and 2023H2 and loses on 2022H2 (Hurricane Ian) under either metric (RMSE +1.0%, "
            "+1.3%, -1.6% with squared error; Poisson deviance +3.6%, +4.0%, -12.4% with the Poisson loss)."
        ),
    )

    # Splits
    temporal = Temporal(on="dateOfLoss", horizon=6, horizon_unit="months")
    splits_comment = """
        Three test windows of half a year of losses, 2023H2, 2023H1 and 2022H2 (newest first), with 12,782, 7,115 and 52,972 claims; each trained on the claims with a loss from 2010-01-01 before the window's start (98.4%, 97.3% and 91.0% of the rows). The half-year cadence is ours (FEMA refreshes monthly and names no refit); the windows start in July 2022 because before that a claim's policy fields may hold a Risk Rating 2.0 term after the loss (notes, "Later policy term"). Each window is dominated by one event: Hurricane Ian holds 98.5% of 2022H2's squared error of the training mean, the April 2023 Florida flooding 62% of 2023H1's and Idalia 51% of 2023H2's. Two filters per training side (SPLIT-9, SPLIT-10): the claims of the window's events (same event code, or same event name within 31 days before the start: the California Atmospheric River of DR-4683 spans 2023-01-01), and the claims opened on or after the window's start; together 431, 2,502 and 710 rows. The 98 claims these filters leave in no split are dropped. No gap (SPLIT-10, measured on the first build's yearly windows at equal training size): RMSE 72,976, 221,188 and 68,556 trained up to the window (2023, 2022, 2021), against 67,845, 223,197 and 70,411 with a 6-month gap; mixed, so no consistent cost of the newest months. Revisit in 2027: yearly windows 2022, 2023, 2024 once 2024 has settled.
    """

    def _make_splits(self, df: pd.DataFrame) -> SplitPlan:
        """The half-year windows; each train side leaves out the test window's events and the claims opened later."""
        windows = TemporalSplits(window=6, unit="months", cutoffs=WINDOW_STARTS).splits(df, "dateOfLoss")
        loss = df["dateOfLoss"]
        opened = loss + pd.to_timedelta(df["days_loss_to_open"].fillna(0), unit="D")
        codes, names = df["event_code"].astype("string"), df["floodEvent"].astype("string")
        splits = {}
        for split, folds in windows.items():
            train, test = (np.asarray(part) for part in folds[0])
            start = loss.iloc[test].min().normalize()
            same_code = codes.isin(set(codes.iloc[test].dropna())).fillna(False)
            near_start = loss.ge(start - pd.Timedelta(days=SPANNING_EVENT_DAYS))
            same_storm = (names.isin(set(names.iloc[test].dropna())) & near_start).fillna(False)
            keep = ~(same_code | same_storm | opened.ge(start)).to_numpy()[train]
            splits[split] = (train[keep], test)
        # Claims that no split uses (opened after every window start they precede) leave the frame.
        used = np.zeros(len(df), dtype=bool)
        for train, test in splits.values():
            used[train] = used[test] = True
        position = np.cumsum(used) - 1
        splits = {
            split: {0: (position[train].tolist(), position[test].tolist())} for split, (train, test) in splits.items()
        }
        return SplitPlan(splits=splits, df=df[used].reset_index(drop=True))

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        files = sorted(raw_dir.glob("NfipClaims_v3_yearOfLoss_*.parquet"))
        return pd.concat([pd.read_parquet(f) for f in files], ignore_index=True)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.copy()
        for col in ("dateOfLoss", "openDate", "originalConstructionDate", "originalNBDate"):
            df[col] = pd.to_datetime(df[col])
        # 1. The history and the release cut, by date of loss.
        df = df[(df["dateOfLoss"] >= HISTORY_START) & (df["dateOfLoss"] < RELEASE_CUT)]
        # 2. Rows with no claim outcome of a flood.
        building, contents = df["amountPaidOnBuildingClaim"], df["amountPaidOnContentsClaim"]
        reasons = df[["nonPaymentReasonBuilding", "nonPaymentReasonContents"]]
        unpaid = building.isna() & contents.isna()
        still_open = unpaid & reasons.isna().all(axis=1)
        negative = (building < 0) | (contents < 0)
        total = building.fillna(0) + contents.fillna(0)
        clerical = reasons.isin(["98", "99"]).any(axis=1) & (total == 0)
        df = df[~(still_open | negative | clerical)].copy()
        # 3. The target: building plus contents paid, a claim closed without payment counted as 0.
        df[TARGET] = df["amountPaidOnBuildingClaim"].fillna(0) + df["amountPaidOnContentsClaim"].fillna(0)
        # 4. Double entries: the same record in every column but the id.
        df = df[~df.drop(columns=["id"]).duplicated(keep="first")]
        # 5. Derived: the event's code (EDN from June 2020, FICO number before) and the reporting delay.
        fico = "FICO " + df["ficoNumber"].astype("Int64").astype("string")
        df["event_code"] = df["eventDesignationNumber"].astype("string").fillna(fico)
        delay = (df["openDate"] - df["dateOfLoss"]).dt.days
        df["days_loss_to_open"] = delay.where(delay >= 0)
        # 6. Deductibles in dollars.
        for col, new in (
            ("buildingDeductibleCode", "building_deductible_usd"),
            ("contentsDeductibleCode", "contents_deductible_usd"),
        ):
            df[new] = df[col].map(DEDUCTIBLE_USD).astype("float64")
        # 7. Proxy and impossible values: sentinels, elevations above the state's highest point, -999.9, an
        # elevation difference beyond 100 ft, two coordinates outside the US (NC at -36/174, GU at 14.6/121).
        highest = df["state"].map(HIGHEST_POINT_FT)
        for col in ELEVATIONS:
            df[col] = df[col].mask(df[col].abs() >= ELEVATION_SENTINEL)
            df[col] = df[col].mask(df[col].eq(-999.9))
            if col != "elevationDifference":
                df[col] = df[col].mask(df[col] > highest)
        df["elevationDifference"] = df["elevationDifference"].mask(df["elevationDifference"].abs() > 100)
        outside = (df["state"].eq("NC") & df["latitude"].lt(0)) | (df["state"].eq("GU") & df["longitude"].lt(140))
        df[["latitude", "longitude"]] = df[["latitude", "longitude"]].mask(outside)
        # The placeholder 1492-10-12 and four typed years (1069, 1070); a policy before the NFIP began (1968).
        df["originalConstructionDate"] = df["originalConstructionDate"].mask(
            df["originalConstructionDate"] < pd.Timestamp("1700-01-01")
        )
        df["originalNBDate"] = df["originalNBDate"].mask(df["originalNBDate"] < pd.Timestamp("1968-01-01"))
        df["numberOfUnits"] = df["numberOfUnits"].mask(df["numberOfUnits"] > 10_000)
        # ZIP codes: 130 empty; ZIP+4 (135) cut to five digits; leading zeros lost in 47 (NJ "7631") restored.
        df = set_missing(df, {"reportedZipCode": [""]})
        df["reportedZipCode"] = df["reportedZipCode"].str.slice(0, 5).str.zfill(5)
        # 8. Codes to words; foundation code 0 is "not collected" (99.97% of the rows rated before Risk Rating 2.0).
        df = set_missing(df, {"foundationType": ["0"]})
        df = decode(df, CODE_LABELS)
        # 9. A later policy term, located: rated "RE" before Risk Rating 2.0 began, a policy started after the loss,
        # or a building built after it. The fields a large loss changes are blanked there (LEAK-10).
        loss = df["dateOfLoss"]
        located = (
            (df["rateMethod"].eq("RE") & loss.lt(RR2_START)).fillna(False)
            | df["originalNBDate"].gt(loss).fillna(False)
            | df["originalConstructionDate"].gt(loss).fillna(False)
        )
        for col in LATE_FIELDS:
            values = df[col].astype("boolean") if df[col].dtype == bool else df[col]
            df[col] = values.mask(located)
        # 10. Fields set after the claim is opened, the rating scheme marker, and copies and identifiers.
        df = drop_columns(
            df, [*POST_OPENING, *COPIES_AND_IDS, "rateMethod", "buildingDeductibleCode", "contentsDeductibleCode"]
        )
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=CATEGORICAL,
            datetime=["dateOfLoss", "originalConstructionDate", "originalNBDate"],
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        loss = pd.to_datetime(raw["dateOfLoss"])
        year = loss.dt.year.astype("int64")
        paid = raw["amountPaidOnBuildingClaim"].clip(lower=0).fillna(0) + raw["amountPaidOnContentsClaim"].clip(
            lower=0
        ).fillna(0)
        last_paid = (pd.to_datetime(raw["mostRecentPaymentDate"]) - loss).dt.days
        extract = pd.Timestamp("2026-09-08")  # asOfDate of every record
        years = list(range(2012, 2027))
        late = pd.DataFrame(
            {
                "claims": year.value_counts().reindex(years),
                "youngest loss, days old": (extract - loss).dt.days.groupby(year).min().reindex(years),
                "dollars of claims last paid > 712 days": paid.where(last_paid > 712, 0).groupby(year).sum()
                / paid.groupby(year).sum(),
                "dollars of claims last paid > 982 days": paid.where(last_paid > 982, 0).groupby(year).sum()
                / paid.groupby(year).sum(),
            }
        ).reindex(years)
        late = late.round(3).rename_axis("year of loss").reset_index()
        rated = raw["rateMethod"].eq("RE")
        window = (year >= 2015) & (year <= 2019)
        band = pd.cut(
            paid[window],
            [-1, 0, 10_000, 50_000, 150_000, float("inf")],
            labels=["0", "1-10k", "10k-50k", "50k-150k", "over 150k"],
        )
        later_term = pd.DataFrame(
            {
                "claims": band.value_counts().sort_index(kind="stable"),
                "rated RE (Risk Rating 2.0)": rated[window].groupby(band, observed=False).mean(),
            }
        )
        later_term = later_term.round(3).rename_axis("paid, 2015-2019 losses (USD)").reset_index()
        return [
            Decision(
                title="Release cut at 2024: payments keep coming for years",
                why=(
                    "Losses of 2024 and later are left out (LEAK-24): the claims still being paid hold a larger share "
                    "of a year's dollars the younger the year; 2022 (Hurricane Ian) and 2012 (Sandy) show how long a "
                    "large hurricane's claims are paid."
                ),
                evidence=late,
            ),
            Decision(
                title="Policy fields of a later term (blanked where located)",
                why=(
                    "Risk Rating 2.0 began in October 2021, yet claims of 2015-2019 carry its rating method, so their "
                    "policy fields come from a later term; the share differs a little with the payment. The test windows start "
                    "in July 2022, and the fields a large loss changes are blanked on the located rows."
                ),
                evidence=later_term,
            ),
        ]
