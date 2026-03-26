# ADR-0023: Use RabbitMQ for Order Processing Instead of Kafka

- **Status**: Accepted
- **Date**: 2025-11-08
- **Decision makers**: @priya (tech lead), @marcus (architect), @jen (platform eng)
- **Consulted**: Order fulfillment team, Data engineering team, SRE team

## 1. Context

The order processing service currently uses a PostgreSQL-backed job queue (pg-boss) to coordinate order state transitions: payment captured, inventory reserved, shipment created, confirmation sent. At current volume (~800 orders/hour), the queue works. However, projected holiday traffic will reach 5,000 orders/hour, and pg-boss is already the primary source of database connection pressure during peak loads.

We need a dedicated message broker to decouple order processing steps, handle burst traffic, and allow independent scaling of consumers. The solution must support at-least-once delivery, dead-letter handling, and per-consumer retry policies. The team has no prior experience operating a dedicated message broker in production.

Constraints: 90-day deadline before holiday traffic ramp, 3-person platform team, existing infrastructure runs on AWS ECS with Terraform, and total budget for new infrastructure is $2,000/month.

## 2. Options Considered

### Option A: Do Nothing (keep pg-boss)

- **Pros**: No migration effort; team already knows it; no new infrastructure cost
- **Cons**: Database connection exhaustion at 3,000+ orders/hour based on load tests; no independent consumer scaling; couples queue health to database health
- **Estimated effort**: 0 weeks
- **Estimated cost**: $0 additional, but risk of outage during peak

### Option B: Apache Kafka (self-managed on ECS)

- **Pros**: High throughput (100K+ msg/sec); durable log allows replay; strong ecosystem for event sourcing
- **Cons**: Operational complexity (ZooKeeper/KRaft, partition management, offset tracking); 6-8 week ramp-up for team with no Kafka experience; minimum 3-broker cluster costs ~$1,800/month; over-engineered for 5,000 orders/hour
- **Estimated effort**: 8-10 weeks including learning curve
- **Estimated cost**: ~$1,800/month infrastructure

### Option C: Amazon SQS

- **Pros**: Zero operational overhead; pay-per-message pricing (~$40/month at our volume); native AWS integration
- **Cons**: No native routing/exchange patterns — requires one queue per consumer type; no built-in priority queues; 256KB message size limit; vendor lock-in
- **Estimated effort**: 3-4 weeks
- **Estimated cost**: ~$40/month

### Option D: RabbitMQ (Amazon MQ)

- **Pros**: Flexible routing via exchanges and bindings; built-in dead-letter queues and per-queue TTL; team can learn core concepts in days; Amazon MQ handles patching and failover; supports priority queues natively; 5,000 msg/sec is well within a single-node capacity
- **Cons**: Not designed for event log replay (messages are consumed and gone); Amazon MQ costs more than self-hosted (~$350/month for mq.m5.large); lower ceiling than Kafka at extreme scale
- **Estimated effort**: 4-5 weeks
- **Estimated cost**: ~$350/month (Amazon MQ)

## 3. Decision

**We will use RabbitMQ via Amazon MQ for order processing message brokering.**

RabbitMQ's exchange/binding model maps directly to our order processing topology: a single topic exchange routes order events to dedicated queues per processing step (payment, inventory, shipping, notification). Dead-letter exchanges handle failures without custom retry logic. Amazon MQ eliminates the operational burden that disqualified self-managed Kafka given our 3-person team and 90-day deadline.

We rejected Kafka because the operational complexity and learning curve exceed what the team can absorb in 90 days, and our throughput requirements (5,000 msg/sec peak) do not justify it. We rejected SQS because the lack of routing primitives would force us to build exchange-like logic in application code. We rejected "do nothing" because load testing confirmed pg-boss failures above 3,000 orders/hour.

## 4. Consequences

**Positive consequences**
- Order processing steps are decoupled — each consumer scales independently
- Dead-letter queues provide automatic failure isolation with visibility into poisoned messages
- Database connection pressure drops by ~40% by removing pg-boss polling

**Negative consequences**
- New infrastructure dependency; Amazon MQ uptime becomes critical path for order processing
- No event replay capability — if we need event sourcing later, we will need a separate system
- Team must learn AMQP concepts (exchanges, bindings, acknowledgments, prefetch)

**Risks**
- Amazon MQ single-node failover takes 1-2 minutes; during that window, order events queue in producers. **Mitigation**: implement local retry buffer in the publisher with 5-minute capacity.
- If throughput grows beyond 50,000 msg/sec, RabbitMQ will need replacement. **Mitigation**: abstract broker behind an interface; revisit at 20,000 msg/sec sustained.

## 5. Follow-Up Actions

| Action | Owner | Deadline |
|--------|-------|----------|
| Provision Amazon MQ instance in staging via Terraform | @jen | 2025-11-15 |
| Implement order event publisher with local retry buffer | @priya | 2025-11-29 |
| Build payment, inventory, and shipping consumers | @marcus | 2025-12-13 |
| Load test at 7,500 msg/sec (1.5x projected peak) | @jen | 2025-12-20 |
| Migrate production traffic with pg-boss fallback | @priya | 2026-01-03 |
| Decommission pg-boss after 2-week parallel run | @marcus | 2026-01-17 |
