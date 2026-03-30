---
name: performance-optimization-guide
description: Hands-on procedure for frontend and backend performance tuning — profiling bottlenecks, applying targeted optimizations, and verifying improvements with before/after measurements.
metadata:
  displayName: "Performance Optimization Guide"
  categories: ["engineering"]
  tags: ["performance", "optimization", "profiling", "bottleneck", "latency", "rendering", "caching"]
  worksWellWithAgents: ["cloud-architect", "frontend-engineer", "performance-engineer", "sre-engineer"]
  worksWellWithSkills: ["performance-audit", "system-design-document", "technical-spec-writing"]
---

# Performance Optimization Guide

## Before you start

Gather the following from the user. If anything is missing, ask before proceeding:

1. **What is slow?** — Specific page, endpoint, query, or user action with measured latency
2. **What is the target?** — Quantified goal (e.g., "LCP under 2s", "API p95 under 200ms")
3. **What does the profile show?** — Existing flame graphs, traces, or Lighthouse reports (if available)
4. **What is the stack?** — Frontend framework, backend runtime, database, hosting/CDN
5. **What has been tried?** — Previous optimization attempts and their measured results

This skill assumes a performance audit has already identified the bottleneck. If the bottleneck is unknown, run a performance audit first.

## Optimization procedure

### 1. Reproduce and Baseline

Before changing anything:

- Reproduce the slow behavior in a consistent environment (same data, same traffic, same hardware)
- Record the baseline metric with the exact tool you will use to verify the fix
- Run the measurement 3 times minimum — single measurements are unreliable due to variance
- Document: metric name, value, tool, timestamp, conditions

Never optimize without a reproducible baseline. If you cannot measure it, you cannot verify the fix.

### 2. Profile to Find the Root Cause

Use the appropriate profiler for the layer:

**Frontend rendering:**
- Chrome DevTools Performance panel — record the slow interaction, look for long tasks (>50ms)
- React Profiler / Vue Devtools — identify components re-rendering unnecessarily
- Lighthouse — automated scoring for LCP, CLS, TBT, TTFB

**JavaScript bundle:**
- Webpack Bundle Analyzer, `next build --analyze`, or equivalent — find largest modules
- Source map explorer — trace bundle size to specific imports
- Check for duplicate dependencies bundled multiple times

**Backend latency:**
- APM tool (Datadog, New Relic, OpenTelemetry) — distributed trace of the slow request
- Language profiler (Node.js `--prof`, Python `cProfile`, Go `pprof`) — CPU time per function
- Log timestamps at each stage of the request to find where time accumulates

**Database queries:**
- `EXPLAIN ANALYZE` on the slow query — check for sequential scans, missing indexes, row estimates
- Query log with execution times — find the top queries by total time (frequency x duration)
- Connection pool metrics — check for exhaustion or excessive wait times

The profile tells you what to fix. Without it, optimization is guessing.

### 3. Apply Targeted Fixes

Apply one fix at a time. Measure after each. Common optimization patterns by category:

**Frontend — reduce what ships:**
- Code-split routes with dynamic `import()` — load only the code for the current page
- Tree-shake unused exports — verify with bundle analyzer that dead code is eliminated
- Replace heavy libraries with lighter alternatives (e.g., date-fns instead of moment)
- Lazy-load below-fold images and components with `loading="lazy"` or `Intersection Observer`

**Frontend — reduce what renders:**
- Memoize expensive computations with `useMemo`/`React.memo` — only where the profiler shows re-render cost
- Virtualize long lists with `react-window` or equivalent — do not render 1000 DOM nodes
- Debounce rapid-fire events (scroll, resize, keystroke search)
- Eliminate layout thrashing — batch DOM reads before DOM writes

**Backend — reduce work per request:**
- Add caching at the right layer: HTTP cache headers, CDN, application cache (Redis), or query cache
- Parallelize independent operations — `Promise.all` / goroutines / async gather instead of sequential awaits
- Move heavy computation to background jobs — respond immediately, process later
- Paginate large result sets — never return unbounded lists

**Database — reduce query cost:**
- Add indexes on columns in WHERE, JOIN, ORDER BY — verify with EXPLAIN that the index is used
- Eliminate N+1 queries — batch with `WHERE id IN (...)` or use JOIN/eager loading
- Denormalize read-heavy data — precompute aggregations instead of computing on every request
- Use connection pooling — prevent new connection overhead per query

### 4. Verify the Improvement

After each fix:

- Run the same measurement from step 1 with identical conditions
- Compare before vs. after — record both values side by side
- Run 3+ measurements to confirm the improvement is consistent, not noise
- Check for regressions in adjacent metrics (e.g., fixing latency but increasing error rate)

| Fix Applied | Metric | Before | After | Change |
|-------------|--------|--------|-------|--------|
| Code-split dashboard route | JS bundle (dashboard) | 842 KB | 214 KB | -74% |
| Add index on orders.user_id | GET /orders p95 | 1,800ms | 120ms | -93% |
| Redis cache for product list | GET /products p95 | 450ms | 12ms | -97% |

### 5. Prevent Regressions

Optimization without regression prevention is temporary:

- Add performance budgets to CI (e.g., Lighthouse CI, bundle size checks)
- Set alerting thresholds on the metrics you just improved
- Document what was optimized and why — next developer needs context to avoid reverting it
- Add a performance test for the specific scenario if the toolchain supports it

## Quality checklist

Before delivering optimization results, verify:

- [ ] Baseline was recorded before any changes, with measurement tool and conditions documented
- [ ] A profiler identified the root cause — optimization was targeted, not speculative
- [ ] Each fix was applied individually and measured separately
- [ ] Before/after comparison uses the same tool, environment, and conditions
- [ ] No regressions introduced in adjacent metrics
- [ ] Regression prevention is in place (CI budget, alert, or test)

## Common mistakes

- **Optimizing without profiling.** Intuition about bottlenecks is wrong more often than right. The profiler shows where time actually goes.
- **Applying multiple fixes at once.** If you change three things and performance improves, you do not know which fix helped. One change, one measurement.
- **Caching without invalidation.** Every cache needs an invalidation strategy. Stale data bugs are harder to diagnose than the original latency.
- **Premature memoization.** `React.memo` and `useMemo` add complexity. Only memoize where the profiler shows expensive re-renders — not everywhere.
- **Optimizing dev mode.** Development builds include extra checks, source maps, and HMR overhead. Always measure production builds.
- **Declaring success without regression prevention.** An optimization without a CI check or alert will be silently undone within weeks.
