"""Curated dataset definition for `ga_merchandise_store_sessions` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    FeatureTypes,
    Metric,
    Source,
    TaskSummary,
    Temporal,
    TemporalSplits,
    decode,
    drop_columns,
)

# The export's counts over the hits up to and including the 3rd pageview, renamed to what they count.
CUT_FEATURES = {
    "c_ev_promo": "promotion_clicks",
    "c_ev_quickview": "quickview_clicks",
    "c_ev_other": "other_events",
    "c_secs": "seconds_on_site",
    "c_paths": "distinct_pages",
    "c_list_click": "product_list_clicks",
    "c_detail": "product_detail_views",
    "c_add": "cart_adds",
    "c_remove": "cart_removes",
    "c_basket": "basket_pageviews",
    "c_account": "account_pageviews",
    "c_home": "home_pageviews",
    "c_apparel": "apparel_pageviews",
    "c_electronics": "electronics_pageviews",
    "c_bags": "bags_pageviews",
    "c_other_cat": "other_category_pageviews",
    "c_quickview": "product_pageviews",
    "c_search_brand": "search_brand_pageviews",
    "c_listing": "listing_pageviews",
}
# The visit's start fields.
START_FIELDS = {
    "visitNumber": "visit_number",
    "channelGrouping": "channel",
    "src": "source",
    "os": "operating_system",
}
# The visitor's visits of the sample that started before this one (USE-10, LEAK-34).
HISTORY = {
    "prev_visits": "previous_visits",
    "prev_purchases": "previous_purchases",
    "prev_days": "days_since_previous_visit",
}
# Google Analytics writes "(not set)" where it has no value.
NOT_SET_COLUMNS = ["source", "medium", "operating_system", "continent", "subcontinent", "country"]


class GaMerchandiseStoreSessions(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will a visit to Google's online merchandise store, seen up to its third page, end in a purchase?",
        use_case=(
            "At a visitor's third pageview, before any checkout step, the store's site estimates whether the visit "
            "will buy, to decide whether to intervene (an offer or a chat prompt)."
        ),
        row=(
            "One visit to the Google Merchandise Store that reaches a third pageview with no checkout step before it, "
            "August 2016 to July 2017 (305,819 visits of 240,212 visitors; Google's obfuscated GA360 sample)."
        ),
        predicted="Whether the visit records a transaction after its third pageview (11,392 visits, 3.7%).",
        known=(
            "The visit's start time, channel, source and medium, device, browser, operating system, country and visit "
            "number; the visitor's earlier visits in the sample (count, purchases before this visit, days since the "
            "last); and the first three pages: seconds on site, promotion clicks, quickview clicks and other events, "
            "distinct pages, product list clicks and views, cart adds and removes, and the kinds of pages opened."
        ),
        split=(
            "Each month from December 2016 to July 2017 is predicted from the visits that started at least a day "
            "before it: the store's model, refit monthly, scores the next month's visits."
        ),
        changes=(
            "We cut each visit at its third pageview and count its hits up to there; the visit's final totals "
            "(pageviews, time on site, revenue) are never features. A visit stored as two rows at midnight is one. "
            "We add the visitor's earlier visits from the sample, and set the traffic sources the export masks to "
            "missing."
        ),
        fit="approximate",
        fit_reason=(
            "A real store's export with its hits in order, so the features end where the site would act; but Google "
            "names no task, the third pageview is our choice, the data predicts the purchase, not whether an offer "
            "changes it, and masked Referral visits (16% of visits, 44% of buyers) are probably Google's employee "
            "store, a hypothesis."
        ),
    )

    # Dataset
    unique_name = "ga_merchandise_store_sessions"
    domain = "business & marketing"
    sources = (
        Source(
            role="publication",
            platform="Other",
            url="https://support.google.com/analytics/answer/7586738",
            license=None,
            year="2018",
            bibtex=r"""
                @misc{google2018gasample,
                  title = {Google Analytics Sample Dataset for {BigQuery}},
                  author = {{Google}},
                  year = {2018},
                  howpublished = {\url{https://support.google.com/analytics/answer/7586738}},
                  note = {BigQuery public dataset bigquery-public-data.google\_analytics\_sample: obfuscated Google Analytics 360 data of the Google Merchandise Store, 2016-08-01 to 2017-08-01}
                }
            """,
            files=("ga_sessions_cut.csv",),
        ),
    )
    data_tags = ("Spatial",)
    download_description = r"""
        The rows are a query of Google's public BigQuery tables, run with the bq tool of the Google Cloud SDK under
        any Google Cloud project (BigQuery's free tier covers it; the query scans about 0.37 GB). Save the SQL below as
        ga_sessions_cut.sql and pipe it through stdin (its leading comment breaks the argument form):

        mkdir -p local-data-warehouse/ga_merchandise_store_sessions
        bq query --use_legacy_sql=false --format=csv --max_rows=2000000 < ga_sessions_cut.sql > local-data-warehouse/ga_merchandise_store_sessions/ga_sessions_cut.csv

        ga_sessions_cut.sql:

        -- One row per visit of the Google Merchandise Store GA360 sample that reaches a 3rd pageview, with the visit's
        -- start (traffic source, device, country, visit number), the visitor's earlier visits in the sample, its hits up to
        -- and including the 3rd pageview, and the label.
        -- A visit stored as two rows (one visitId over two dates, split at midnight) is one visit: its hits in order.
        WITH p AS (
          SELECT fullVisitorId AS uid, visitId, date, visitStartTime, visitNumber, channelGrouping,
            trafficSource.source AS src, trafficSource.medium AS medium, IFNULL(trafficSource.isTrueDirect, FALSE) AS true_direct,
            device.deviceCategory AS device, device.browser AS browser, device.operatingSystem AS os,
            geoNetwork.continent AS continent, geoNetwork.subContinent AS subcontinent, geoNetwork.country AS country,
            IFNULL(totals.transactions, 0) AS transactions, hits,
            ROW_NUMBER() OVER (PARTITION BY fullVisitorId, visitId ORDER BY date) AS part,
            COUNT(*) OVER (PARTITION BY fullVisitorId, visitId) AS parts,
            FIRST_VALUE(visitStartTime) OVER (PARTITION BY fullVisitorId, visitId ORDER BY date) AS start0
          FROM `bigquery-public-data.google_analytics_sample.ga_sessions_*`
        ),
        s AS (  -- the visit: its first row's start fields, transactions summed over its rows
          SELECT CONCAT(p.uid, '-', CAST(p.visitId AS STRING)) AS vid, p.uid, MAX(parts) AS parts,
            ARRAY_AGG(STRUCT(date, visitStartTime, visitNumber, channelGrouping, src, medium, true_direct, device, browser, os,
              continent, subcontinent, country) ORDER BY part LIMIT 1)[OFFSET(0)].*,
            SUM(transactions) AS transactions
          FROM p GROUP BY p.uid, p.visitId
        ),
        h AS (  -- every hit of the visit, in order: row, then hit number; time in ms from the visit's start
          SELECT CONCAT(p.uid, '-', CAST(p.visitId AS STRING)) AS vid, p.part, x.hitNumber AS hn,
            (p.visitStartTime - p.start0) * 1000 + x.time AS t, x.type AS typ, LOWER(x.page.pagePath) AS path,
            x.eCommerceAction.action_type AS act, x.transaction.transactionId AS tx, x.eventInfo.eventAction AS eact
          FROM p, UNNEST(p.hits) x
        ),
        o AS (
          SELECT *, ROW_NUMBER() OVER (PARTITION BY vid ORDER BY part, hn) AS k,
            COUNTIF(typ = 'PAGE') OVER (PARTITION BY vid ORDER BY part, hn ROWS UNBOUNDED PRECEDING) AS pv_so_far
          FROM h
        ),
        cut AS (SELECT vid, MIN(k) AS cut_k FROM o WHERE typ = 'PAGE' AND pv_so_far = 3 GROUP BY vid),
        funnel AS (  -- the first checkout hit: a checkout step or purchase action, a transaction, or a checkout page
          SELECT vid, MIN(k) AS f_k FROM o
          WHERE act IN ('5', '6', '8') OR tx IS NOT NULL OR REGEXP_CONTAINS(path, r'yourinfo|payment|revieworder|ordercompleted|checkout')
          GROUP BY vid
        ),
        lab AS (SELECT vid, COUNTIF(tx IS NOT NULL) AS tx_hits, MIN(IF(tx IS NOT NULL, t, NULL)) AS tx_t FROM o GROUP BY vid),
        hist AS (  -- the visitor's visits of the sample (all of them, kept or not) that started at least a second earlier
          SELECT vid, COUNT(*) OVER w AS prev_visits, (visitStartTime - MAX(visitStartTime) OVER w) / 86400 AS prev_days
          FROM s WINDOW w AS (PARTITION BY uid ORDER BY visitStartTime RANGE BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING)
        ),
        buys AS (  -- the time of each visit's first transaction hit, in epoch seconds
          SELECT s.uid, s.visitStartTime + lab.tx_t / 1000 AS tx_time FROM s JOIN lab USING (vid) WHERE lab.tx_t IS NOT NULL
        ),
        prev_buy AS (  -- the visitor's earlier visits whose transaction came before this visit started
          SELECT s.vid, COUNT(*) AS prev_purchases FROM s JOIN buys ON buys.uid = s.uid AND buys.tx_time < s.visitStartTime
          GROUP BY s.vid
        ),
        feat AS (  -- the hits up to and including the 3rd pageview
          SELECT o.vid, MIN(o.hn) AS first_hit,
            COUNT(*) AS c_hits, COUNTIF(typ = 'EVENT') AS c_events,
            COUNTIF(typ = 'EVENT' AND eact = 'Promotion Click') AS c_ev_promo,
            COUNTIF(typ = 'EVENT' AND eact = 'Quickview Click') AS c_ev_quickview,
            COUNTIF(typ = 'EVENT' AND IFNULL(eact, '') NOT IN ('Promotion Click', 'Quickview Click')) AS c_ev_other,
            MAX(t) / 1000 AS c_secs, COUNT(DISTINCT path) AS c_paths,
            COUNTIF(act = '1') AS c_list_click, COUNTIF(act = '2') AS c_detail, COUNTIF(act = '3') AS c_add,
            COUNTIF(act = '4') AS c_remove,
            COUNTIF(typ = 'PAGE' AND REGEXP_CONTAINS(path, r'basket')) AS c_basket,
            COUNTIF(typ = 'PAGE' AND REGEXP_CONTAINS(path, r'signin|register|myaccount')) AS c_account,
            COUNTIF(typ = 'PAGE' AND REGEXP_CONTAINS(path, r'^/home$|^/$|^/home\?|^/home-2')) AS c_home,
            COUNTIF(typ = 'PAGE' AND REGEXP_CONTAINS(path, r'apparel|wear|shirt|hat')) AS c_apparel,
            COUNTIF(typ = 'PAGE' AND REGEXP_CONTAINS(path, r'electronics')) AS c_electronics,
            COUNTIF(typ = 'PAGE' AND REGEXP_CONTAINS(path, r'bags')) AS c_bags,
            COUNTIF(typ = 'PAGE' AND REGEXP_CONTAINS(path, r'drinkware|office|accessories|lifestyle')) AS c_other_cat,
            COUNTIF(typ = 'PAGE' AND REGEXP_CONTAINS(path, r'\.axd$|quickview')) AS c_quickview,
            COUNTIF(typ = 'PAGE' AND REGEXP_CONTAINS(path, r'search|shop\+by\+brand|brand')) AS c_search_brand,
            COUNTIF(typ = 'PAGE' AND REGEXP_CONTAINS(path, r'store\.html|asearch|google\+redesign/(?:[^/]+)$')) AS c_listing
          FROM o JOIN cut USING (vid)
          WHERE o.k <= cut.cut_k
          GROUP BY o.vid
        )
        SELECT s.vid, s.uid, s.parts, s.date, s.visitStartTime, s.visitNumber, s.channelGrouping, s.src, s.medium,
          s.true_direct, s.device, s.browser, s.os, s.continent, s.subcontinent, s.country,
          hist.prev_visits, IFNULL(prev_buy.prev_purchases, 0) AS prev_purchases, hist.prev_days,
          feat.* EXCEPT (vid),
          CAST(s.transactions > 0 AS INT64) AS buy, lab.tx_hits,
          funnel.f_k IS NOT NULL AND funnel.f_k <= cut.cut_k AS funnel_before_cut
        FROM s JOIN cut USING (vid) JOIN feat USING (vid) JOIN lab USING (vid) JOIN hist USING (vid)
          LEFT JOIN funnel USING (vid) LEFT JOIN prev_buy USING (vid)
        ORDER BY s.vid
    """
    curation_comments = """
        We start with ga_sessions_cut.csv, the result of the query in the download notes on Google's GA360 sample of
        the Google Merchandise Store (`bigquery-public-data.google_analytics_sample.ga_sessions_*`, one table a day
        from 2016-08-01 to 2017-08-01, 903,653 visit rows of 714,167 visitors; queried 2026-11-25).

        - Prediction point: the visit's 3rd pageview, before any checkout step. Every feature is the visit's start
          (traffic source, device, browser, operating system, geography, the visitor's visit number), the visitor's
          visits of the sample that started before it, or a count over the visit's hits up to and including that
          pageview, in the order of the hits; nothing recorded after it (LEAK-10). Hit times rise with the hit number in every visit of the sample (measured), so that order is the
          order of time.
        - Not shipped: the visit's final totals (`totals.pageviews`, `hits`, `timeOnSite`, `transactions`,
          `transactionRevenue`), which the query reads only for the label. They give the visit's own purchase away:
          on the six test months of the time (February to July 2017) untuned LightGBM reaches ROC AUC 0.977 with them
          (0.936 from the final pageviews alone) against 0.873 at the cut (measured 2026-11-25, before the history
          columns, the masking fix and the eight windows).
        - The checkout pattern, settled on the data: every hit with a checkout or purchase action (Enhanced Ecommerce
          action types 5 and 6; 7 and 8 never occur) or a transaction id is on one of four pages, `/yourinfo.html`,
          `/payment.html`, `/revieworder.html` and `/ordercompleted.html` (titled "Checkout Your Information",
          "Payment Method", "Checkout Review" and "Checkout Confirmation"), but one purchase hit on a category page,
          which its transaction id marks. The query flags a visit whose first such hit comes at or before its 3rd
          pageview, and we drop those 234 visits (115 buy): the site acts before checkout. No page a kept visit opens
          before the cut belongs to the funnel: among page paths opened before the cut by at least 50 kept visits,
          the highest buy rate is 27% (an infant apparel quick view), against 94% of the visits that open
          `/ordercompleted.html`, 85% `/revieworder.html`, 65% `/payment.html` and 49% `/yourinfo.html`.
        - The label: the visit's transactions (`totals.transactions`, summed over its rows) above 0. It agrees with
          the hits on every kept visit (the visits with a transaction count are the visits with a transaction hit),
          and the funnel filter puts every such hit after the cut.
        - Midnight splits: Google Analytics stores a visit that runs over midnight as two rows with one visitId; the
          second row goes on numbering the hits but restarts the clock. The query joins the two rows of each of the
          898 such visits: hits in order (row, then hit number), time from the visit's start, the start fields of the
          first row, transactions summed. Cut row by row, 317 of them appeared twice.
        - We drop 2017-08-01 (959 visits), the last table of the sample: one day, not a month.
        - Dropped columns: the visit and visitor ids (`vid`, `uid`; Google obfuscated them), the date and the start in
          epoch seconds (the start ships as `visit_start`), the number of stored rows (`parts`), the two checks
          (`tx_hits`, `funnel_before_cut`), `first_hit`, the number of a visit's first stored hit, `c_hits`, which
          is 3 plus `c_events` in every row (up to the cut there are pageviews and events only), and `c_events`,
          which the three event counts split by action.
        - Anomaly: 2,264 kept visits (0.7%) start at a later hit than 1, most at hit 2: Google's sample lacks their
          first hit, so the cut falls one pageview later where the missing hit was a pageview. Kept: they buy at
          3.1%, against 3.7% for all visits.
        - Anomaly (CLEAN-10): Google's export masks the traffic source of 112,478 visits whose `channel` is not
          Direct: `source` is "(direct)" and `medium` "(none)", while `channel` keeps the true channel. Three
          patterns (measured 2026-11-25): Organic Search and Paid Search are masked by month, 0% in August 2016 and
          March and May 2017, up to 96-97% in November 2016 and 53-56% in June 2017 (organic-search visits buy at
          2.3% masked and 2.4% unmasked); Display is masked in June 2017 only (17%); Referral is masked at 72-84% in
          every month, and these 48,947 visits (16% of all) buy at 10.3% against 1.4% for the referrals with a
          visible source, are 93% from the United States and hold 5,052 of the 11,392 buyers (44%). So the masking
          follows the label within Referral: a referrer the export hides, known when the visit starts and stable
          over the months, which a deployed site would see. That it is Google's employee store
          (`mall.googleplex.com`, absent from all 198 visible sources) is a hypothesis, not checked. We set both
          values to missing where `channel` is not Direct: the deployed site sees the true source, and a Referral
          visit with a missing source still marks the hidden group (untuned LightGBM, 6 windows, 2 seeds: 0.8740
          against 0.8739 as published; dropping `source` and `medium` costs 0.002 and is worse in 5 of 6 windows).
          The masked share still moves by month, so `source` and `medium` stay the start fields that drift most
          against a window's train side (population stability index up to 0.80 in March 2017 with the masked values
          missing, 0.64 as published).
        - `visit_start` is the visit's start in the store's time zone (America/Los_Angeles; it gives the sample's
          `date` on every row), a model input and the time key.
        - Features built in the query from the hits up to the cut, the counts a store's analyst builds from its hits:
          `promotion_clicks`, `quickview_clicks` and `other_events` (event hits by event action),
          `seconds_on_site` (the time of the last hit up to the cut), `distinct_pages`,
          `product_list_clicks`, `product_detail_views`, `cart_adds` and `cart_removes` (Enhanced Ecommerce action
          types 1 to 4), and pageviews by page path: basket, account (sign-in, register, my account), home, apparel,
          electronics, bags, other categories (drinkware, office, accessories, lifestyle), product pages (`.axd`
          pages and quick views), search and brand, and listings. A path can count in more than one group. The home
          group counts `/home-2`, a home page variant of November 2016 to February 2017 (about 5,400 visits). The site
          stopped opening its top-level category pages (`/google+redesign/bags` and the like, counted as listings)
          in August-September 2016, so listing pageviews fall from 25% of the pageviews before the cut in August
          2016 to 11-14% later.
        - Events by action: "Promotion Click" events before the cut are in 5,057-5,962 visits a month from August
          to November 2016, 2,854 in December and none from January 2017 on (the share of visits with any event
          falls from 33% to 13-17%), so they are a column of their own, `promotion_clicks`, and the other events do
          not change meaning; `other_events` holds add to cart, remove from cart, product click, contact-us click
          and unlabelled events (the cart and product clicks also count in the action-type columns). No test month
          after December 2016 has a promotion click, so `promotion_clicks` is the feature that drifts most against
          the train side of January to May 2017 (population stability index 0.73 to 1.34, measured without the gap).
        - "(not set)", Google Analytics' empty value, is missing (source 23 visits, medium 45, operating system 976,
          continent, subcontinent and country 331 each).
        - Ids and fields: Google obfuscated `fullVisitorId` and removed `clientId`, `adWordsClickInfo` and parts of
          `geoNetwork` ("Not available in demo dataset", the help page); country is set for 99.9% of the visits.
          Whether Google drew the sample at random from the store's traffic is not stated.
        - Returning visitors (`Entities: Recur`; SPLIT-13): 32.7% of the visits belong to one of 34,485 visitors
          with several, and 9.3% to 11.8% of a test month's visits (December 2016 to July 2017) come from a visitor
          seen in an earlier month (they buy at 7.2% to 11.4%, against 2.3% to 4.0% for new visitors; 20% to 28%
          after an earlier purchase, February to July 2017). The store knows its returning visitors (its cookie) and
          their visit number, which ships, so they stay; the visitor id does not ship. The model cannot single a visitor out: untuned
          LightGBM scores ROC AUC 0.869 over three random folds and 0.867 over three folds grouped by visitor.
        - The visitor's history (USE-10, LEAK-34): the store knows a returning visitor's earlier visits and orders,
          so three columns come from the same `fullVisitorId`'s visits of the sample that started at least a second
          before this one, all of them, kept or not (short visits and the 234 dropped funnel visits count too):
          `previous_visits`, `previous_purchases` (those whose first transaction hit came before this visit
          started) and `days_since_previous_visit` (missing without one). Earlier visits in the same test month
          count: the site knows them when the visit starts. The history starts with the sample in August 2016
          (`visit_number`, the store's own count, reaches 395), so it understates what the store knows: 70% to 74% of
          a test month's visits have no earlier visit in the sample and 96.2% to 97.5% no earlier purchase (December
          2016 to July 2017). Visits with an earlier purchase buy at 17.2%, against 3.3% without. As information, not as the reason: untuned
          LightGBM gains 0.002 to 0.007 ROC AUC with the three columns (mean 0.004, higher on 6 of the 6 windows of
          the time, February to July 2017, 2 seeds) and 0.005 to 0.022 on the visits with an earlier visit (measured
          2026-11-25). The missing
          `days_since_previous_visit` marks a first visit in the sample; its missing indicator alone scores ROC AUC
          0.66 (the leak probe), the new-visitor effect.
        - Protocol (LEAK-9, an evaluation leak): 14.2% to 18.3% of each test month's visits (December 2016 to July
          2017) have a later visit by the same visitor in the same month, and those visits buy at 5.4% to 7.2%
          against 2.3% to 4.2%. Reading that later visit through the visitor id adds 0.014 to 0.017 ROC AUC to LightGBM (March, May and July 2017,
          measured before the history columns); about 80% of such pairs can be linked from shipped columns
          (`visit_number` plus one, the same device, browser, operating system and country), and the later visit's
          `previous_purchases` counts this visit's purchase. Chains rebuilt from the shipped columns gained nothing
          before the history columns (0.8761 against 0.8763). Each test visit is predicted from the training rows
          and its own features only; no feature or model step may use other test rows.
        - Another task on the same visits: `google_analytics_customer_revenue_prediction` predicts each visitor's
          revenue in a later window (one row per visitor, regression); this task is one row per visit, cut inside
          it, binary (PROV-7). Kaggle's "Google Analytics Customer Revenue Prediction" files are a later copy: v1
          holds the same visits without hits, v2 adds hits and 15 more months (not read here).
        - The target (CLEAN-25): "Yes" when the visit buys, the event the metric scores.
    """

    # Task
    target = "purchase"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason=(
            "Google's sample defines no task or metric (help page and announcement read 2026-11-25); the Kaggle "
            "competition on the same visits scored the RMSE of each visitor's log revenue, another task "
            "(google_analytics_customer_revenue_prediction); Sakar et al. 2019, whose in-visit setting the use case "
            "follows, report accuracy, TPR, TNR and F1 with no single criterion. roc_auc is the binary fallback."
        )
    )

    # Splits
    temporal = Temporal(
        on="visit_start",
        splits=TemporalSplits(
            window=1,
            unit="months",
            cutoffs=(
                "2017-07-01",
                "2017-06-01",
                "2017-05-01",
                "2017-04-01",
                "2017-03-01",
                "2017-02-01",
                "2017-01-01",
                "2016-12-01",
            ),
            gap=1,
            gap_unit="days",
        ),
    )
    accepted_check_warnings = {
        "splits_train_under_half": (
            "The curator's exception for this dataset (Andrej, 2026-11-25): January 2017 trains on 46.0% and "
            "December 2016 on 35.7% of the visits (one-day gap), added to test the holiday season the newer months "
            "lack and to come closer to the target of 9 windows, as on the earlier exceptions."
        ),
        "splits_below_target": (
            "8 windows against a target of 9 (Andrej, 2026-11-25): November 2016 would train on 26.2% of the visits, "
            "under the 30% floor, so the eight months December 2016 to July 2017 are all the sample holds."
        ),
    }
    split_leaf = "L-ORDER.windows"
    splits_comment = """
        Eight test windows, each one calendar month from December 2016 to July 2017, each trained on the visits that
        started at least one day before it (an expanding train side). The window is a month because the store is
        assumed to refit its model monthly and score the visits of the month after (the source names no task,
        horizon or refit cadence). Gap (SPLIT-10, Andrej, 2026-11-25, as on fugaku_hpc_job_failure_1m): one day, the
        lag between building a model and applying it; the label alone needs none, as it is known when the visit
        ends, within the day. So each window's training side lacks the previous month's last day (424 to 1,320
        visits; later windows train on it). The windows and their train shares of the 305,819 visits: July 25,115 test visits (train
        91.5%), June 22,577 (84.1%), May 24,556 (76.2%), April 22,530 (68.8%), March 23,691 (61.0%), February
        21,919 (53.8%), January 24,276 (46.0%) and December 30,716 (35.7%). January and December train on less
        than half the visits: the curator's exception (Andrej, 2026-11-25, SPLIT-14), to test the holiday season,
        December's buy rate of 4.5% and its most visits of the year, which the newer months lack, and to come
        closer to the target count, as on the earlier exceptions. December trains on four months, before the
        traffic drop from about 950-990 visits a day in November and December 2016 to about 780 from January
        2017, a change of unknown cause (Google's sampling or real) the windows test across. The buy rate of the
        test months moves from 2.9% (January) to 4.5% (December and May). The target for an IID split of 305,819
        visits is 9 splits (SPLIT-33); November 2016 would train on less than the 30% floor, so the count is 8.
        The sample's last table, 2017-08-01 (959 visits), is dropped on purpose: one day is no month, and merging
        it into July would bend July's window. Protocol (LEAK-9): 14.2% to 18.3% of a test month's visits have a
        later visit by the same visitor in that month, whose features (among them `previous_purchases`) can give
        the earlier visit's purchase away; each test visit is predicted from the training rows and its own
        features only, and no feature or model step may use other test rows.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "ga_sessions_cut.csv", dtype={"vid": str, "uid": str, "date": str})

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # 1. Visits with a checkout step at or before the 3rd pageview: the site acts before checkout.
        df = raw[~raw["funnel_before_cut"]]
        # 2. The last table holds one day (2017-08-01), not a month.
        df = df[df["date"] < "20170801"]
        # The label agrees with the transaction hits; up to the cut there are 3 pageviews and the events, which the
        # three event counts split by action.
        assert ((df["buy"] > 0) == (df["tx_hits"] > 0)).all()
        assert (df["c_hits"] == 3 + df["c_events"]).all()
        assert (df["c_events"] == df["c_ev_promo"] + df["c_ev_quickview"] + df["c_ev_other"]).all()
        # 3. The start in the store's time zone, which gives the sample's date on every row.
        start = pd.to_datetime(df["visitStartTime"], unit="s", utc=True).dt.tz_convert("America/Los_Angeles")
        assert (start.dt.strftime("%Y%m%d") == df["date"]).all()
        df = df.assign(visit_start=start.dt.tz_localize(None))
        # 4. Names, the target's classes in words (CLEAN-25), "(not set)" missing.
        df = df.rename(columns={**START_FIELDS, **HISTORY, **CUT_FEATURES, "buy": self.target})
        df = decode(df, {self.target: {0: "No", 1: "Yes"}})
        df[NOT_SET_COLUMNS] = df[NOT_SET_COLUMNS].replace("(not set)", np.nan)
        # 5. The export's masked traffic source: "(direct)" / "(none)" on a visit whose channel is not Direct.
        masked = df["channel"] != "Direct"
        df.loc[masked & (df["source"] == "(direct)"), "source"] = np.nan
        df.loc[masked & (df["medium"] == "(none)"), "medium"] = np.nan
        # 6. Ids, the stored-row count, the checks, the first stored hit, the hit count (3 + events) and the events.
        return drop_columns(
            df,
            [
                "vid",
                "uid",
                "parts",
                "date",
                "visitStartTime",
                "tx_hits",
                "funnel_before_cut",
                "first_hit",
                "c_hits",
                "c_events",
            ],
        )

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "channel",
                "source",
                "medium",
                "true_direct",
                "device",
                "browser",
                "operating_system",
                "continent",
                "subcontinent",
                "country",
            ],
            datetime=["visit_start"],
        )
