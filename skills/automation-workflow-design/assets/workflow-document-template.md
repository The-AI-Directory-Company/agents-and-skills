# Workflow Document Template

Copy this template to document a new automation workflow.

---

```markdown
# Workflow: [Descriptive name — verb + object, e.g., "Sync New Orders to Warehouse"]

## Overview

| Field | Value |
|-------|-------|
| **Trigger** | [Event that starts the workflow: webhook, schedule, database event, etc.] |
| **Platform** | [n8n / Make / Zapier / Power Automate] |
| **Schedule** | [If cron-based: "Every 15 minutes" / "Daily at 06:00 UTC" / N/A] |
| **Owner** | [Team or person responsible for maintenance] |
| **Systems involved** | [List all APIs, databases, and SaaS tools] |
| **Created** | [YYYY-MM-DD] |
| **Last updated** | [YYYY-MM-DD] |

## Trigger Details

- **Type**: [Webhook / Polling / Cron / Event subscription]
- **Source**: [System that fires the trigger]
- **Payload shape** (sample):

```json
{
  "field1": "example_value",
  "field2": 123,
  "nested": {
    "field3": true
  }
}
```

- **Expected frequency**: [N per hour/day/week]
- **Idempotency handling**: [How duplicates are detected and handled — e.g., dedup by record ID]

## Steps

| # | Stage | Action | Node/Module | Input | Output | Error Handling |
|---|-------|--------|-------------|-------|--------|----------------|
| 1 | Intake | [Describe action] | [Platform-specific node name] | [Fields from trigger or previous step] | [Fields produced] | [Retry N times / skip / halt] |
| 2 | Intake | [Describe action] | [...] | [...] | [...] | [...] |
| 3 | Processing | [Describe action] | [...] | [...] | [...] | [...] |
| 4 | Processing | [Describe action] | [...] | [...] | [...] | [...] |
| 5 | Output | [Describe action] | [...] | [...] | [...] | [...] |
| 6 | Notification | [Describe action] | [...] | [...] | [...] | [...] |

## Branches

| # | After Step | Condition | True Path (steps) | False Path (steps) | Rejoin? |
|---|------------|-----------|--------------------|--------------------|---------|
| 1 | [Step #] | [Boolean expression using available fields] | [Step sequence] | [Step sequence] | [Yes — at step # / No — terminates] |

## Error Handling

### Global Error Handler
- **Mechanism**: [Error Trigger workflow (n8n) / Break handler (Make) / Code try-catch (Zapier) / Scope run-after (Power Automate)]
- **Captures**: Workflow name, execution ID, failed step, error message, original payload

### Per-Step Retry Policy
- **Default retries**: [N] with [N-second] backoff
- **Steps with custom retry**: [List any steps that differ from default]

### Dead Letter Handling
- **Destination**: [Error queue / database table / Slack channel / email]
- **Retention**: [N days before cleanup]

### Alerting
- **Channel**: [Slack #channel / email / PagerDuty]
- **Threshold**: [Alert on every failure / alert if >N failures in M minutes]

### Circuit Breaker
- **Condition**: [If failure rate exceeds N% over M minutes]
- **Action**: [Pause workflow, alert on-call, require manual re-enable]

## Workflow Diagram

```
[Trigger: description]
  |
  v
[Step 1: description]
  |
  v
[Step 2: description] --error--> [Error handler: description]
  |
  v
[Branch: condition?]
  |yes              |no
  v                 v
[Step 3a]           [Step 3b]
  |                 |
  v                 v
[Step 4: rejoin or end]
  |
  v
[Step 5: notification]
```

## Volume & Limits

| Metric | Value |
|--------|-------|
| Expected runs per day | [N] |
| Peak runs per hour | [N] |
| Average payload size | [N KB/MB] |
| Rate limits to respect | [API-specific limits, e.g., "Shopify: 40 requests/sec"] |
| Maximum items per batch | [N, if batching] |
| Estimated execution time | [N seconds per run] |

## Credentials & Secrets

| System | Credential Type | Storage Location |
|--------|----------------|-----------------|
| [API/Service name] | [API key / OAuth2 / Service account] | [Platform credential store / vault reference] |

Note: Never embed credentials in workflow steps. Use the platform's built-in credential store or reference an external vault.

## Maintenance Notes

- [Any known quirks, seasonal volume changes, or planned migrations]
- [Dependencies on external systems that may change]
- [Date of last review]
```
