---
unique_name: antt_interstate_bus_ticket_sales
name: 'ANTT Monitriip: interstate bus ticket sales (venda de passagem), Brazil'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- Time-series (Regression)
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: GOV Website
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://dados.antt.gov.br/
- https://www.kaggle.com/datasets/danlessa/brazil-interstate-bus-travels
- https://www.gov.br/antt/pt-br/assuntos/passageiros/monitriip
- https://dados.antt.gov.br/dataset/monitriip-bilhetes-de-passagem
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: per-ticket sales of Brazil's regulated interstate buses from the transport agency, counted into tickets per trip as in the Nairobi task; the same forecasting-like demand panel, and the current ANTT files could not be opened.
- Source: ANTT (Agência Nacional de Transportes Terrestres), Monitriip, open-data dataset `monitriip-bilhetes-de-passagem` on dados.antt.gov.br ("arquivo com os dados de bilhetes de passagens comercializados do serviço regular", one file per month, a data dictionary PDF; as indexed by a search engine). The Kaggle mirror (danlessa, 2020, CC0) holds four months (03/2019, 11/2019, 12/2019, 01/2020; 0.4 to 1 GB each) with "Ticket identifier", "Bus trip identifier", "Ticket emission timestamp", "Trip start and end timestamps", origin and destination municipality and "Paid values". Target: tickets per trip, counted from the ticket rows. The portal rejected our requests, so the files of 2025-2026 (Jan25 to Mar26 in the index) were not opened; a search snippet suggests monthly aggregates (fare mean and standard deviation) rather than tickets: to check.
- Use case: an operator, before a scheduled departure, plans vehicles and fares from the expected load; not named by ANTT (Monitriip is regulatory monitoring); fit approximate; regime temporal.
- Siblings and duplicates: `traffic_jam_predicting_peoples_movement_into_nairobi` (TBD -> 2nd Tier, priority 2, the same target on Mobiticket's 14 routes) and its rerun `total_energies_revolution_hackathon` (No); no ANTT record (grep for antt, monitriip). External collections: none found.
- Better data: found as better data for `traffic_jam_predicting_peoples_movement_into_nairobi`; no further search this round.
- Papers and pages: ANTT's Monitriip pages; the Kaggle mirror; no paper.
- Metric: none found (ANTT portal as indexed, the mirror; no task published); the Nairobi record's Zindi MAE belongs to another source; fallback `rmse` (MET-8); inputs none.
- Risks for /add-dataset: tickets per route and departure slot is a demand series (SEL-10 against SEL-11): TP-10 comes first; trips without sales are absent (USE-7); emission time and paid value are per ticket and not known before sales (LEAK-1); no capacity column in the mirror's list; the grain of the current release is unverified; several GB per year.
- Priority: gap 0 (temporal regression not thin), use case 0 (none named by the source), source + (a federal agency's register with a data dictionary), shape 0 (many trips, but the features only index route and time), risk - (forecasting-like, SEL-10, TP-10).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `traffic_jam_predicting_peoples_movement_into_nairobi`.
- as published: one row per ticket of the regulated interstate bus trips: ticket id, trip id, ticket emission time, trip start and end times, origin and destination municipality, paid value (ANTT data dictionary ...; target: tickets sold per scheduled trip (count of ticket rows per trip id), as number_of_ticket per ride_id in the Nairobi task; access: open (ANTT open data; the Kaggle mirror is CC0).
- Why: the Nairobi task (tickets per ride from route, departure date and time, operator) on a national register instead of one ticketing app's 14 routes
- Adds: millions of tickets per month on thousands of routes, from a government agency, against Mobiticket's ~6 months on 14 routes. Same risks as the record: forecasting-like demand per route and slot (TP-10), rides without sales absent, per-ticket columns (emission time, paid value) not known before sales. The first ...
