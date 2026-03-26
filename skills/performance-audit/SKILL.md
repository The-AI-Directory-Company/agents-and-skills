---
name: performance-audit
description: Conduct systematic performance audits — profiling frontend rendering, backend latency, and database queries to produce a prioritized optimization roadmap with measurable targets.
metadata:
  displayName: "Performance Audit"
  categories: ["engineering"]
  tags: ["performance", "profiling", "optimization", "latency", "Core-Web-Vitals"]
  worksWellWithAgents: ["frontend-engineer", "performance-engineer", "sre-engineer"]
  worksWellWithSkills: ["system-design-document", "technical-seo-audit", "test-plan-writing"]
---

# Performance Audit

## Before you start

Gather the following from the user. If anything is missing, ask before proceeding:

1. **What is slow?** — Specific page, endpoint, query, or workflow (not "the app feels sluggish")
2. **How slow is it?** — Current measured latency, load time, or throughput numbers
3. **What is the target?** — Acceptable performance threshold (e.g., "page load under 2 seconds at p95")
4. **What is the architecture?** — Frontend framework, backend services, database(s), CDN, caching layers
5. **What is the traffic profile?** — Average and peak request volume, geographic distribution
6. **What has already been tried?** — Previous optimization attempts and their outcomes

## Audit template

### 1. Establish Baselines

Measure before you optimize. Record current metrics for every area under audit:

**Frontend** (Lighthouse, WebPageTest, or RUM): LCP, FID, CLS, TTFB, TBT, total page weight broken down by JS/CSS/images/fonts. Include Core Web Vitals targets: LCP <2500ms, FID <100ms, CLS <0.1.

**Backend** (APM, logs, or load testing): For each slow endpoint, record p50/p95/p99 latency, throughput (req/s), and error rate.

**Database**: List the top 3-5 slowest queries by total time (avg latency x call frequency), not single-execution time.

Record all baselines with timestamps, traffic level, and environment.

### 2. Frontend Audit

- [ ] Run bundle analyzer — identify largest modules and duplicate dependencies
- [ ] Verify code splitting: route-specific modules lazy-loaded, tree-shaking eliminating unused exports
- [ ] Identify unnecessary re-renders using React Profiler or equivalent
- [ ] Check for layout thrashing: interleaved DOM reads/writes in loops
- [ ] Verify images use modern formats (WebP/AVIF), correct sizing, and lazy loading
- [ ] Check fonts: limit weights, use `font-display: swap`
- [ ] Verify assets served from CDN with cache headers, no render-blocking resources in critical path
- [ ] Check for unnecessary API calls on page load

### 3. Backend Audit

- [ ] Trace slow requests end-to-end — where does time accumulate?
- [ ] Check middleware chain for unexpectedly slow steps (auth, logging, parsing)
- [ ] Identify synchronous operations that could be asynchronous
- [ ] Check for missing timeouts on external service calls
- [ ] Identify repeatedly computed results that could be cached
- [ ] Verify cache hit rates — low rates indicate poor key design or short TTLs
- [ ] Check connection pool sizes against actual demand
- [ ] Identify sequential operations that could be parallelized

### 4. Database Audit

- [ ] Run EXPLAIN/ANALYZE on the top 10 slowest queries
- [ ] Check for missing indexes on columns in WHERE, JOIN, and ORDER BY
- [ ] Identify N+1 query patterns — loops issuing individual queries instead of batch/JOIN
- [ ] Check for full table scans on tables with >100K rows
- [ ] Verify connection pooling is configured and sized appropriately
- [ ] Check for lock contention on frequently updated rows

### 5. Prioritized Optimization Roadmap

Rank every finding by impact and effort:

| Priority | Finding | Impact | Effort | Expected Gain |
|----------|---------|--------|--------|---------------|
| P0 | N+1 queries on /dashboard | High | Low | p95 from 3200ms to 800ms |
| P1 | No CDN for static assets | High | Medium | LCP from 4100ms to 2200ms |
| P2 | Unoptimized images | Medium | Low | Page weight -40% |

- **P0**: High impact, low effort — free wins, do first
- **P1**: High impact, higher effort — schedule immediately
- **P2**: Medium impact, low effort — batch into one sprint
- **P3**: Lower impact or high effort — backlog

### 6. Set Targets and Monitoring

For each P0/P1 item, define: baseline measurement, target threshold, monitoring alert condition, and verification date. Never optimize without a way to measure the result.

## Quality checklist

Before delivering a performance audit, verify:

- [ ] Baselines are recorded with timestamps, conditions, and tools used
- [ ] Frontend, backend, and database layers are each assessed
- [ ] Every finding includes measured data, not subjective impressions
- [ ] The roadmap is prioritized by impact/effort, not listed in discovery order
- [ ] P0/P1 items have specific, measurable targets (not "make it faster")
- [ ] Monitoring is defined so regressions are caught

## Common mistakes

- **Optimizing without measuring first.** Intuition about what is slow is wrong more often than right. Profile, then optimize.
- **Focusing on micro-optimizations.** Shaving 2ms off a function while a 3-second database query runs unchecked is wasted effort.
- **Ignoring p99 latency.** p50 looks fine, but p99 reveals the worst user experience. Report percentile distributions, not averages.
- **Missing the N+1 pattern.** The most common backend performance bug. Every loop that issues a query is suspect.
- **Caching without invalidation strategy.** Stale data creates bugs harder to diagnose than slowness.
- **Declaring victory after one test.** Verify improvements under realistic load, data volume, and conditions.
