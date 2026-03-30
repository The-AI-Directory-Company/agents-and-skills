---
name: integration-specification
description: Write integration specifications — defining data flows, API contracts, authentication, error handling, retry logic, and monitoring requirements for system-to-system connections.
metadata:
  displayName: "Integration Specification"
  categories: ["engineering"]
  tags: ["integration", "specification", "API", "data-flow", "error-handling", "contracts"]
  worksWellWithAgents: ["api-developer", "api-tester", "integration-engineer", "no-code-builder", "solutions-architect"]
  worksWellWithSkills: ["api-design-guide", "api-integration-guide", "automation-workflow-design", "system-design-document"]
---

# Integration Specification

## Before you start

Gather the following from the user. Do not proceed until you have answers to at least items 1-4:

1. **Which two systems are being connected?** Name the source and destination. Include versions if relevant.
2. **What data flows between them?** Entities, fields, direction (one-way or bidirectional), and expected volume.
3. **What triggers the data flow?** Event-driven (webhook, message queue), scheduled (cron, polling), or on-demand (API call)?
4. **Authentication on both sides?** API keys, OAuth, mutual TLS, service accounts — what does each system support?
5. **SLA requirements?** Max acceptable latency, throughput targets, and uptime expectations.
6. **What happens when one system is down?** Must data be queued, retried, or is loss acceptable?

If the user says "integrate system A with system B" without specifics, push back: "What data needs to move, in which direction, and what triggers the transfer?"

## Integration specification template

### 1. Overview

Write 2-3 sentences covering:
- The two systems being connected and their roles (producer vs. consumer)
- The business purpose of the integration
- The integration pattern: synchronous request/response, asynchronous messaging, event-driven, or batch ETL

### 2. Data Flow Diagram

Define each data flow as a row:

| Flow | Source | Destination | Trigger | Payload | Frequency |
|------|--------|-------------|---------|---------|-----------|
| Create order | Order Service | Fulfillment API | Order placed event | Order JSON | ~500/hour peak |
| Sync inventory | Warehouse DB | Product Service | Scheduled (every 5 min) | Inventory delta CSV | 288/day |

Include the direction arrow in the diagram. For bidirectional flows, document each direction as a separate row.

### 3. API Contracts

For each endpoint or message in the integration, specify:

- **Method and URL** (or queue/topic name for async)
- **Request headers** — Content-Type, Authorization, idempotency keys
- **Request body** — Full schema with field names, types, required/optional, and constraints
- **Response body** — Success shape and error shape
- **Status codes** — Every expected code with its meaning in this integration's context

Provide a concrete example request and response for each contract. Do not leave schemas abstract.

### 4. Authentication and Authorization

Document for each system:

- Auth mechanism (API key, OAuth 2.0 client credentials, mutual TLS)
- Token/key rotation procedure and frequency
- Scopes or permissions required
- Where credentials are stored (vault, environment variables — never hardcoded)

### 5. Error Handling

Classify errors into three categories and define the response for each:

| Category | Examples | Action |
|----------|----------|--------|
| Transient | 429, 503, timeout, connection reset | Retry with backoff |
| Permanent | 400, 401, 404, schema validation failure | Alert and dead-letter |
| Partial | Batch with some failed records | Process successes, retry failures separately |

### 6. Retry Logic

Specify the exact retry policy:

- **Strategy**: Exponential backoff with jitter
- **Initial delay**: e.g., 1 second
- **Max retries**: e.g., 5
- **Max delay cap**: e.g., 60 seconds
- **Circuit breaker threshold**: e.g., 10 consecutive failures opens the circuit for 5 minutes
- **Dead-letter handling**: Where do permanently failed messages go? Who gets alerted?

### 7. Monitoring and Alerting

Define what to measure and when to alert:

| Metric | Threshold | Alert |
|--------|-----------|-------|
| End-to-end latency (P99) | > 2 seconds | Warning |
| Error rate | > 1% over 5 minutes | Critical |
| Queue depth / dead-letter size | > 10,000 / > 0 | Warning / Critical |

### 8. Data Mapping

Map fields between source and target systems:

| Source Field | Source Type | Target Field | Target Type | Transform |
|-------------|------------|-------------|------------|-----------|
| `user.email` | string | `contact_email` | varchar(255) | Lowercase, trim |
| `created_at` | Unix epoch (ms) | `creation_date` | ISO 8601 | Convert with UTC timezone |
| `status` | enum (1,2,3) | `order_status` | string | Map: 1=pending, 2=active, 3=closed |

Document every transformation, default value, and nullable field explicitly.

## Quality checklist

Before delivering the specification, verify:

- [ ] Every data flow has a defined trigger, direction, payload, and frequency
- [ ] API contracts include concrete request/response examples, not just abstract schemas
- [ ] Authentication covers both systems with rotation procedures documented
- [ ] Errors are classified (transient, permanent, partial) with specific handling for each
- [ ] Retry policy specifies strategy, delays, max attempts, and circuit breaker thresholds
- [ ] Dead-letter handling is defined — failed messages are never silently dropped
- [ ] Monitoring covers latency, error rate, queue depth, and auth token expiry
- [ ] Data mapping documents every field transformation, not just the obvious ones
- [ ] Idempotency requirements are stated — can the consumer safely receive the same message twice?

## Common mistakes to avoid

- **Assuming both systems share the same data model.** Document every field mapping and transformation, including timezone handling and enum translations.
- **No retry policy.** "We'll handle errors" is not a spec. Define the exact backoff strategy, max retries, and what happens after all retries are exhausted.
- **Ignoring partial failures in batch operations.** A batch of 100 records where 3 fail needs a clear strategy — do you reject the whole batch or process the 97 successes?
- **Missing idempotency.** If a webhook fires twice, will the consumer create duplicate records? Specify idempotency keys for every write operation.
- **Monitoring as an afterthought.** If you cannot tell whether the integration is healthy without checking logs, you do not have monitoring.
