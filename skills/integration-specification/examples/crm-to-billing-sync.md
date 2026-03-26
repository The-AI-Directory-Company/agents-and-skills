# Integration Spec — HubSpot CRM to Stripe Billing Sync

## Overview

One-way sync from HubSpot CRM (source) to Stripe (destination). When a deal closes in HubSpot, a Stripe customer and subscription are created automatically. Eliminates 15-20 min of manual data entry per deal and ~8% error rate.

**Pattern:** Event-driven via HubSpot webhooks, processed by internal integration service.

## Data Flow

| Flow | Source | Destination | Trigger | Frequency |
|------|--------|-------------|---------|-----------|
| Create customer | HubSpot | Stripe | Deal stage = "Closed Won" | ~40/week |
| Create subscription | HubSpot | Stripe | Same trigger, after customer created | ~40/week |
| Update customer | HubSpot | Stripe | Contact property change | ~120/week |

## API Contracts

**Webhook receipt** — `POST https://api.acme.io/webhooks/hubspot`
```json
{"eventId": 981723, "subscriptionType": "deal.propertyChange",
 "propertyName": "dealstage", "propertyValue": "closedwon",
 "objectId": 5048723901}
```

**Create Stripe customer** — `POST /v1/customers`
```
name=Northwind+Traders&email=billing@northwind.io
&metadata[hubspot_company_id]=8827364012&metadata[hubspot_deal_id]=5048723901
```

**Create subscription** — `POST /v1/subscriptions`
```
customer=cus_R4xKj8mNvQ2p&items[0][price]=price_pro_monthly
&items[0][quantity]=25&idempotency_key=deal_5048723901_sub
```

Price ID mapped from HubSpot line item product name via config lookup table.

## Authentication

| System | Mechanism | Rotation | Storage |
|--------|-----------|----------|---------|
| HubSpot (inbound) | HMAC-SHA256 signature verification | Quarterly | AWS Secrets Manager |
| HubSpot (outbound) | OAuth 2.0 + refresh token | Access: 30 min, refresh: 6 mo | AWS Secrets Manager |
| Stripe | Restricted API key (customers + subscriptions write) | Quarterly | AWS Secrets Manager |

## Data Mapping

| HubSpot Field | Stripe Field | Transform |
|---------------|-------------|-----------|
| `contact.email` | `customer.email` | Lowercase, trim |
| `company.name` | `customer.name` | Trim whitespace |
| `company.company_id` | `customer.metadata.hubspot_company_id` | Cast to string |
| `deal_line_item.product_name` | `subscription.items[].price` | Lookup: "Pro Monthly" -> `price_pro_monthly` |
| `company.country` | `customer.address.country` | Convert to ISO 3166-1 alpha-2 |

## Error Handling

| Category | Examples | Action |
|----------|----------|--------|
| Transient | Stripe 429, 503, network timeout | Retry with backoff |
| Permanent | Stripe 400 (invalid email), 402 | Dead-letter queue + alert #billing-ops |
| Data issue | Deal missing email or line items | Reject, notify deal owner via HubSpot task |
| Duplicate | Webhook fires twice | Idempotency key `deal_{id}_sub` prevents duplicates |

## Retry & Circuit Breaker

- **Strategy:** Exponential backoff with jitter (2s, 4s, 8s, 16s, 32s + 0-1s random)
- **Max retries:** 5. After exhaustion, message moves to `crm-sync-dlq` SQS queue.
- **Circuit breaker:** 8 consecutive failures opens for 5 min. Messages queue in SQS during open state.
- **Webhook deduplication:** Processed `eventId` values stored in Redis with 72-hour TTL.

## Monitoring

| Metric | Threshold | Alert |
|--------|-----------|-------|
| Sync latency (webhook to Stripe created) | > 30s p95 | Slack warning |
| Error rate | > 5% / 15 min | PagerDuty critical |
| DLQ depth | > 0 | Slack warning |
| DLQ depth | > 10 | PagerDuty critical |
| OAuth token refresh failure | Any | PagerDuty critical |
| Daily sync count vs. closed deals | Mismatch > 2 | Slack warning |
