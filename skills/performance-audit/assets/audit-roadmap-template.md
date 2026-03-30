# Performance Audit Roadmap Template

Copy this template and fill in findings from your performance audit.

## Audit Metadata

| Field | Value |
|-------|-------|
| System / Feature | |
| Audit Date | |
| Auditor | |
| Environment | (production / staging / local) |
| Traffic Conditions | (peak / average / off-peak) |
| Tools Used | |

## Baselines

Record current measurements before any optimization work begins.

### Frontend

| Metric | Value | Tool | Timestamp |
|--------|-------|------|-----------|
| LCP | | | |
| INP | | | |
| CLS | | | |
| TTFB | | | |
| TBT | | | |
| Total Page Weight | | | |
| JS Bundle Size | | | |
| CSS Size | | | |
| Image Weight | | | |

### Backend

| Endpoint | p50 | p95 | p99 | Throughput (req/s) | Error Rate |
|----------|-----|-----|-----|--------------------|------------|
| | | | | | |
| | | | | | |
| | | | | | |

### Database

| Query Description | Avg Latency | Frequency | Total Time (avg x freq) |
|-------------------|-------------|-----------|------------------------|
| | | | |
| | | | |
| | | | |

## Prioritized Optimization Roadmap

| Priority | Finding | Layer | Impact | Effort | Expected Gain | Owner | Status |
|----------|---------|-------|--------|--------|---------------|-------|--------|
| P0 | | | High | Low | | | Not started |
| P0 | | | High | Low | | | Not started |
| P1 | | | High | Medium | | | Not started |
| P1 | | | High | Medium | | | Not started |
| P2 | | | Medium | Low | | | Not started |
| P2 | | | Medium | Low | | | Not started |
| P3 | | | Low | High | | | Backlog |

### Priority Definitions

- **P0** -- High impact, low effort. Free wins. Do first.
- **P1** -- High impact, higher effort. Schedule immediately.
- **P2** -- Medium impact, low effort. Batch into one sprint.
- **P3** -- Lower impact or high effort. Add to backlog.

## Targets and Monitoring

| P0/P1 Finding | Baseline | Target | Alert Condition | Verification Date | Verified? |
|---------------|----------|--------|-----------------|-------------------|-----------|
| | | | | | |
| | | | | | |
| | | | | | |

## Notes

<!-- Additional context, caveats, or dependencies for the optimization work. -->
