# Failure Modes Catalog

Common failure patterns in distributed systems, with detection strategies and mitigations. Use this as a checklist when writing Section 8 (Failure Modes & Mitigation) of a system design document.

---

## 1. Database Primary Failover

**What happens:** The primary database instance becomes unavailable (hardware failure, OOM, network partition from the application tier).

**Impact:**
- All writes fail until failover completes
- Reads fail if not routed to replicas
- In-flight transactions are rolled back
- Connection pools may fill with stale connections

**Detection:**
- Health check failures (TCP + query-level)
- Replication lag spikes to infinity
- Application error rate on write operations

**Mitigation:**
- Automated failover (RDS Multi-AZ, Patroni, Cloud SQL HA) --- target: < 30s
- Application-level retry with backoff for transient write failures
- Connection pool configured to evict stale connections on error
- Read traffic routed to replicas (can continue serving during failover)

**Recovery time:** 15-60 seconds (automated), 5-30 minutes (manual)

**Testing:** Trigger failover in staging on a regular schedule. Verify application reconnects without manual intervention.

---

## 2. Cache Stampede (Thundering Herd)

**What happens:** A popular cache key expires. Multiple concurrent requests miss the cache simultaneously and all hit the database to regenerate the value.

**Impact:**
- Database load spikes (potentially 100-1000x normal for that query)
- Cascading latency increase across all requests
- Can trigger database connection exhaustion
- If the database query is slow, the problem compounds (requests pile up)

**Detection:**
- Cache miss rate spike on specific keys
- Database query rate spike correlated with cache TTL boundaries
- Latency increase on endpoints that use the affected cache key

**Mitigation:**
- **Lock-based recomputation:** Only one request recomputes; others wait or serve stale data
- **Stale-while-revalidate:** Serve the expired value while one background request refreshes it
- **Jittered TTLs:** Add random jitter to expiration times so keys do not expire simultaneously
- **Warm-up on deploy:** Pre-populate critical cache keys during deployment

**Testing:** Expire a high-traffic cache key in staging and observe database load.

---

## 3. Message Queue Backlog

**What happens:** Producers publish messages faster than consumers can process them. The queue depth grows continuously.

**Impact:**
- Processing delay increases (minutes to hours)
- End-user-visible delays for async operations (emails, notifications, data sync)
- Queue storage fills up --- oldest messages may be dropped or the queue rejects new publishes
- Downstream systems receive a burst when the backlog drains

**Detection:**
- Queue depth (number of unconsumed messages) exceeds threshold
- Consumer lag metric (Kafka: consumer group lag, SQS: ApproximateNumberOfMessagesVisible)
- Age of oldest unprocessed message

**Mitigation:**
- **Auto-scale consumers** based on queue depth or consumer lag
- **Back-pressure:** If consumers cannot keep up, slow down producers (reject or throttle publishes)
- **Dead-letter queue (DLQ):** Route repeatedly failing messages to a DLQ instead of blocking the main queue
- **Priority queues:** Separate high-priority messages from bulk processing
- **Batch processing:** Consumers process messages in batches rather than one at a time

**Testing:** Artificially inject 10x normal message volume in staging. Verify auto-scaling triggers and DLQ works.

---

## 4. Upstream API Returns 5xx

**What happens:** A third-party or internal dependency starts returning server errors (500, 502, 503).

**Impact:**
- Features depending on the upstream degrade or fail
- Retry storms from your service can worsen the upstream's condition
- If the upstream is on the critical path, your API returns errors to end users

**Detection:**
- Error rate on outbound HTTP calls exceeds threshold
- Circuit breaker trips
- Latency increase (5xx often preceded by timeout-length delays)

**Mitigation:**
- **Circuit breaker:** After N consecutive failures, stop calling the upstream for a cooldown period. Return a fallback response.
- **Cached fallback:** Serve the last known good response from cache for read operations
- **Graceful degradation:** Disable the affected feature and show a user-friendly message rather than a generic error
- **Retry with exponential backoff + jitter:** Retry transient errors, but cap retries (2-3 max) and add jitter to prevent synchronized retry storms
- **Timeout budget:** Set aggressive timeouts (e.g., 2s) so a slow upstream does not consume your thread pool

**Testing:** Use fault injection (Toxiproxy, Envoy fault injection) to simulate upstream failures. Verify circuit breaker behavior and fallback responses.

---

## 5. Network Partition

**What happens:** Network connectivity between components is lost --- services cannot reach each other even though both are running.

**Impact:**
- Varies by architecture: in CP systems, writes are rejected to preserve consistency; in AP systems, reads may return stale data
- Split-brain risk: if two instances of a service both believe they are the primary, data corruption can occur
- Service discovery may route traffic to unreachable instances

**Detection:**
- Health check failures across availability zones or regions
- Increased timeout errors between specific service pairs
- Cluster membership changes (e.g., Kafka ISR shrinks, etcd/Consul leader election triggers)

**Mitigation:**
- **Multi-AZ deployment:** Services span availability zones so a single-AZ partition does not take down the system
- **Fencing tokens:** Prevent split-brain writes by requiring a monotonically increasing token for write operations
- **Quorum-based systems:** Use consensus protocols (Raft, Paxos) that require majority agreement
- **Client-side failover:** Clients detect unreachable endpoints and reroute to healthy ones
- **DNS failover:** Update DNS records to point away from the partitioned region

**Testing:** Block network traffic between AZs in staging (iptables rules, security group changes). Verify the system degrades gracefully.

---

## 6. Clock Skew

**What happens:** System clocks on different machines diverge beyond acceptable bounds. Timestamps generated on different hosts are not comparable.

**Impact:**
- Distributed locks may be acquired by multiple holders simultaneously (lease expiration calculated incorrectly)
- Event ordering is wrong --- logs, audit trails, and event streams show incorrect sequences
- Certificate validation fails (TLS certificates appear expired or not-yet-valid)
- Cache TTLs behave unexpectedly (items expire too early or too late)
- Scheduled jobs fire at the wrong time

**Detection:**
- NTP offset monitoring (alert if offset > 100ms)
- Clock drift rate monitoring
- Unexpected TLS handshake failures
- Distributed lock contention anomalies

**Mitigation:**
- **NTP or PTP synchronization:** All hosts must run NTP and alert on synchronization failures. Cloud providers offer precision time services (AWS Time Sync, Google TrueTime).
- **Logical clocks for ordering:** Use Lamport timestamps or vector clocks for event ordering instead of wall-clock time
- **Lease-based locks with safety margins:** Set lock TTLs with sufficient margin to tolerate expected clock skew (e.g., if max skew is 100ms, add 500ms to the TTL)
- **Server-side timestamps:** Generate all authoritative timestamps on a single service rather than trusting client clocks
- **Bounded staleness:** Systems like Google Spanner use TrueTime with known uncertainty bounds to make safe ordering decisions

**Testing:** Manually skew the clock on a staging host (`date --set`) and verify that locks, caches, and event ordering remain correct.

---

## Quick Reference Table

| Failure | Blast Radius | Detection Speed | Typical Recovery | Preventable? |
|---------|-------------|-----------------|------------------|-------------|
| DB failover | Write path | Seconds | 15-60s (auto) | No, but mitigatable |
| Cache stampede | Read path + DB | Seconds | Self-resolving (minutes) | Yes, with proper caching patterns |
| Queue backlog | Async processing | Minutes | Minutes-hours | Partially (auto-scaling) |
| Upstream 5xx | Dependent features | Seconds | Depends on upstream | No, but isolatable |
| Network partition | Cross-zone communication | Seconds-minutes | Minutes-hours | Partially (multi-AZ) |
| Clock skew | Distributed coordination | Minutes-hours (silent) | Seconds (once detected) | Yes, with NTP monitoring |
