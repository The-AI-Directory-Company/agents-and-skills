# Rollback Strategies Comparison

## Strategy Overview

| Strategy | Rollback Speed | Complexity | Data Risk | Best For |
|----------|---------------|------------|-----------|----------|
| Feature flags | Seconds | Low | None (code stays deployed) | Application logic changes, UI features |
| Blue-green | Seconds to minutes | Medium | Low (stateless) | Stateless services, full version swaps |
| Canary | Minutes | Medium | Low | Gradual rollouts, performance-sensitive changes |
| Redeploy previous version | Minutes to hours | Low | Low | Simple deployments, small teams |

---

## Feature Flags

**How it works**: New code is deployed but gated behind a flag. Rollback means flipping the flag to off -- no deployment needed.

**Advantages**:
- Fastest rollback (seconds, no deployment pipeline)
- Granular control (per-user, per-region, percentage-based)
- Decouples deploy from release
- Enables A/B testing during rollout

**Tradeoffs**:
- Requires feature flag infrastructure (LaunchDarkly, Unleash, custom)
- Code complexity increases (branching logic in application code)
- Stale flags become tech debt -- must schedule cleanup
- Not suitable for schema changes or infrastructure-level changes

**When to avoid**: Database migrations, infrastructure changes, changes that cannot be cleanly toggled at the application layer.

---

## Blue-Green Deployment

**How it works**: Two identical environments (blue and green). One serves traffic while the other is idle. Deploy to idle, verify, then switch traffic. Rollback means switching traffic back to the previous environment.

**Advantages**:
- Clean rollback -- previous version is still running and warm
- Full environment validation before cutover
- No mixed-version traffic during deploy

**Tradeoffs**:
- Doubles infrastructure cost (two full environments)
- Database schema must be compatible with both versions during cutover
- Session state and in-flight requests need draining during switch
- Not practical for stateful services without shared data layer

**When to avoid**: When database schema changes are not backward-compatible, or when infrastructure cost constraints prevent running two full environments.

---

## Canary Deployment

**How it works**: New version is deployed to a small subset of infrastructure (1-5% of traffic). Gradually increase traffic percentage if metrics are healthy. Rollback means routing all traffic back to the stable version.

**Advantages**:
- Real production traffic validation with limited blast radius
- Gradual confidence building with metric thresholds at each stage
- Can detect issues that staging environments miss

**Tradeoffs**:
- Requires traffic routing infrastructure (service mesh, load balancer rules)
- Mixed-version traffic means API contracts must be backward-compatible
- Monitoring must be granular enough to compare canary vs. baseline cohorts
- Longer rollout time compared to blue-green

**When to avoid**: When you cannot isolate canary traffic for metric comparison, or when the change is all-or-nothing (e.g., a protocol change that all nodes must adopt simultaneously).

---

## Redeploy Previous Version

**How it works**: Roll forward by deploying the last known good version through the standard deployment pipeline.

**Advantages**:
- No additional infrastructure required
- Uses the same deployment process as any other release
- Simple to understand and execute

**Tradeoffs**:
- Slowest rollback -- limited by CI/CD pipeline speed (minutes to hours)
- Previous artifacts must be available (container images, build outputs)
- Pipeline failures during rollback create a cascading incident
- No instant recovery -- downtime or degradation persists during redeployment

**When to avoid**: When RTO is under 5 minutes, or when the deployment pipeline itself is unreliable.

---

## Choosing a Strategy

Use this decision flow:

1. **Is the change behind a feature flag?** Use feature flags as the primary rollback. Fast rollback, no deployment.
2. **Is the service stateless with blue-green infrastructure?** Use blue-green. Instant switch, clean separation.
3. **Is the change high-risk and needs gradual validation?** Use canary. Limited blast radius, real traffic validation.
4. **None of the above?** Redeploy previous version as the fallback. Slower but always available.

For high-risk releases, combine strategies: deploy behind a feature flag **and** use canary rollout. The flag provides instant rollback; the canary limits blast radius during validation.
