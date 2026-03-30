# Anti-Pattern Example: A Bad ADR

This is an intentionally flawed ADR that violates multiple quality criteria. Each problem is annotated below the document.

---

## The Bad ADR

```markdown
# ADR: Kafka

- **Status**: Accepted
- **Date**: January 2025

## Context

We need a message queue. The current system is slow.

## Decision

We decided to use Kafka because it is the industry standard
for event streaming and handles high throughput well.

## Consequences

- Better performance
- More scalable
- Industry standard, so easy to hire for

## Next Steps

- Set up Kafka cluster
- Migrate existing events
```

---

## What Is Wrong (and Why It Matters)

### 1. Title states the topic, not the decision

**Problem:** "Kafka" is a technology name. The title does not say what decision was made or what problem it solves.

**Fix:** "Use Kafka for Order Event Streaming Instead of RabbitMQ"

### 2. No decision makers listed

**Problem:** When this decision is questioned in 6 months, nobody knows who to ask for context.

**Fix:** List specific people with roles: `@alice (tech lead), @bob (architect)`.

### 3. Context is one sentence with no specifics

**Problem:** "The current system is slow" gives a future engineer nothing to work with. How slow? What system? What is the bottleneck? What constraints exist?

**Fix:** "Our RabbitMQ cluster processes 50K events/hour but order volume has grown to 200K events/hour during peak. Messages queue for 45+ minutes during Black Friday. We need a solution that handles 500K events/hour within our $2K/month infrastructure budget. The team has 2 engineers with JVM experience but none with Kafka operations experience."

### 4. No alternatives considered

**Problem:** The ADR jumps straight to Kafka. Was RabbitMQ tuning considered? What about Amazon SQS? What about Pulsar? Without alternatives, this reads as a predetermined conclusion, not an evaluated decision.

**Fix:** Evaluate at least 3 options (including "do nothing" -- keep tuning RabbitMQ) with specific pros, cons, and effort estimates for each.

### 5. Missing "do nothing" option

**Problem:** Maybe tuning the existing RabbitMQ cluster, adding more consumers, or optimizing message sizes would solve the throughput problem at a fraction of the migration cost. Without evaluating "do nothing," the ADR cannot prove the migration is worth the effort.

**Fix:** Add "Option C: Do Nothing -- continue with RabbitMQ and optimize consumer throughput. Pros: no migration risk, no new operational knowledge needed. Cons: ceiling is estimated at 150K events/hour even with optimization, which does not meet the 500K target."

### 6. Vague consequences with no negatives

**Problem:** "Better performance" and "more scalable" are meaningless without numbers. And there are zero negative consequences listed -- as if adopting a complex distributed system has no downsides.

**Fix:** Positive: "Kafka handles 1M+ events/sec per partition, exceeding our 500K/hour target by 100x." Negative: "Requires 3-month migration with dual-write period. Adds Zookeeper/KRaft operational complexity. Team has no Kafka ops experience -- budget $15K for training. Increases infrastructure cost from $800/month to $2,100/month."

### 7. No risks or mitigation

**Problem:** What if the migration fails halfway? What if Kafka ops complexity causes outages? What if the team cannot hire Kafka-experienced engineers?

**Fix:** "Risk: Team lacks Kafka operational experience. Mitigation: Engage contractor for initial setup, complete Confluent training for 2 engineers before go-live, establish runbook for common failure scenarios."

### 8. Follow-up actions have no owners or deadlines

**Problem:** "Set up Kafka cluster" is assigned to nobody with no timeline. This ADR will sit in a docs folder and nothing will happen.

**Fix:** "Set up staging Kafka cluster -- @bob -- by Feb 15. Complete team Kafka training -- @alice to schedule -- by Feb 28. Implement dual-write for order events -- @carol -- by March 15."

### 9. No rationale for why alternatives were rejected

**Problem:** Even if alternatives had been listed, the ADR does not explain why Kafka was chosen _over_ them. "Industry standard" is not a technical rationale.

**Fix:** "RabbitMQ tuning was rejected because internal benchmarks showed a ceiling of 150K events/hour, below our 500K target. SQS was rejected because our event consumers require ordering guarantees within partitions, which SQS FIFO queues support only up to 3,000 messages/sec per group."

---

## Checklist Failures Summary

| Checklist Item | Status |
|----------------|--------|
| Title states the decision | FAIL -- states the technology name only |
| Context explains the problem | FAIL -- one vague sentence |
| 3+ options including "do nothing" | FAIL -- zero alternatives |
| Each option has pros, cons, effort | FAIL -- no options evaluated |
| Rejected options have reasons | FAIL -- no rejected options |
| Consequences are positive and negative | FAIL -- only positives, all vague |
| Risks have mitigations | FAIL -- no risks mentioned |
| Actions have owners and deadlines | FAIL -- no owners or dates |
| Status is clearly marked | PASS -- "Accepted" is stated |

**Result:** 1 of 9 checks passed. This ADR provides almost no value to future engineers. It documents _what_ was chosen but none of the reasoning, context, or tradeoffs that make ADRs useful.
