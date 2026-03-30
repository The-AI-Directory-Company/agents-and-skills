# Profiling Tools by Layer

Detailed workflows for the most common profiling tools, organized by the layer you are investigating.

---

## Chrome DevTools Performance Panel

**Use for:** Frontend rendering bottlenecks, long tasks, layout thrashing, paint storms.

### Key Workflow

1. Open DevTools (`F12`) > **Performance** tab.
2. Click **Record** (or `Ctrl+E`), perform the slow interaction, then **Stop**.
3. In the flame chart, look for:
   - **Red triangles** on the top row -- these mark long tasks (> 50 ms blocking the main thread).
   - **Yellow (Scripting)** blocks -- JavaScript execution. Click to see the call stack.
   - **Purple (Layout/Rendering)** blocks -- forced reflows. Look for interleaved read/write patterns.
   - **Green (Paint)** blocks -- large paint areas suggest missing `will-change` or excessive DOM changes.
4. Check the **Summary** tab at the bottom for time breakdown: Scripting, Rendering, Painting, Idle.
5. Use **Bottom-Up** tab to find the most expensive functions by self-time.

### Tips

- Enable **CPU throttling** (4x/6x slowdown) to simulate slower devices.
- Enable **Network throttling** to simulate real-world connections.
- Record with the **Screenshots** checkbox on to correlate visual changes with activity.

---

## React Profiler

**Use for:** Identifying unnecessary component re-renders and expensive render cycles.

### Key Workflow

1. Install React DevTools browser extension.
2. Open DevTools > **Profiler** tab (in the React DevTools panel).
3. Click **Record**, perform the interaction, then **Stop**.
4. Switch to **Ranked** view and sort by **Self time** -- these are the components spending the most time rendering.
5. For each expensive component:
   - Click it to see **"Why did this render?"** (requires `<Profiler>` or React DevTools setting).
   - Check if props/state actually changed -- unchanged props with re-renders indicate a missing `React.memo` or unstable reference.
6. Look for components that render on every keystroke, scroll, or unrelated state change.

### Tips

- Enable **"Record why each component rendered"** in React DevTools settings.
- Only add `React.memo` where the profiler shows a real cost -- not preventively.
- Check for new object/array/function creation in parent render (e.g., `style={{}}` inline) that defeats memoization.

---

## Webpack Bundle Analyzer

**Use for:** Understanding what is in your JavaScript bundle and finding bloat.

### Key Workflow

1. Generate a stats file:
   ```bash
   # Webpack
   npx webpack --json > stats.json
   npx webpack-bundle-analyzer stats.json

   # Next.js
   ANALYZE=true npx next build
   # or install @next/bundle-analyzer and configure next.config.js
   ```
2. In the treemap visualization:
   - **Largest rectangles** are your biggest modules -- target these first.
   - Look for **duplicate dependencies** (same library bundled twice at different versions).
   - Check for libraries that should be **lazy-loaded** (not needed on initial page load).
3. Right-click a module to see its import chain -- trace why it was included.

### Common Finds

- `moment.js` with all locales (replace with `date-fns` or `dayjs`).
- Full `lodash` imported instead of `lodash/specificFunction`.
- Polyfills for features supported by your browser target.
- Dev-only dependencies accidentally included in production bundle.

---

## Go `pprof`

**Use for:** CPU profiling, memory allocation analysis, goroutine leak detection in Go services.

### Key Workflow

1. Import the profiling endpoint:
   ```go
   import _ "net/http/pprof"
   ```
   This registers handlers at `/debug/pprof/` on the default `http.DefaultServeMux`.

2. Capture a CPU profile (30-second sample):
   ```bash
   go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30
   ```

3. Inside the `pprof` interactive shell:
   ```
   (pprof) top 20          # Top 20 functions by CPU time
   (pprof) list <funcName>  # Annotated source for a specific function
   (pprof) web              # Open flame graph in browser (requires graphviz)
   ```

4. For memory profiling:
   ```bash
   go tool pprof http://localhost:6060/debug/pprof/heap
   (pprof) top 20 -cum     # Sort by cumulative allocations
   ```

5. For goroutine leaks:
   ```bash
   go tool pprof http://localhost:6060/debug/pprof/goroutine
   (pprof) top              # See where goroutines are stuck
   ```

### Tips

- Compare two heap profiles to find leaks: `go tool pprof -base before.prof after.prof`.
- Use `-http=:8080` flag to get the web UI: `go tool pprof -http=:8080 profile.prof`.
- In production, protect `/debug/pprof/` behind authentication.

---

## PostgreSQL `EXPLAIN ANALYZE`

**Use for:** Understanding query execution plans, finding missing indexes, and diagnosing slow queries.

### Key Workflow

1. Run with full diagnostics:
   ```sql
   EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
   SELECT ... FROM ... WHERE ...;
   ```

2. Read the plan **bottom-up** (innermost operations execute first). Key things to check:

   | What to Look For | Meaning | Action |
   |-----------------|---------|--------|
   | `Seq Scan` on large table | Full table scan, no index used | Add an index on the filter/join column |
   | `Rows Removed by Filter` is high | Index exists but is not selective enough | Check if a composite index would help |
   | `actual rows` >> `planned rows` | Statistics are stale | Run `ANALYZE <table>` to update stats |
   | `Sort` with `external merge` | Sort spilling to disk | Increase `work_mem` or add index matching ORDER BY |
   | `Nested Loop` with high `loops` | Potentially an N+1 at the query planner level | Consider `Hash Join` via rewriting the query |
   | `Buffers: shared read` is high | Data not in cache, reading from disk | Check if `shared_buffers` is sized correctly |

3. For ongoing monitoring, enable `pg_stat_statements`:
   ```sql
   SELECT query, calls, mean_exec_time, total_exec_time
   FROM pg_stat_statements
   ORDER BY total_exec_time DESC
   LIMIT 10;
   ```

### Tips

- `EXPLAIN` without `ANALYZE` shows the plan without executing -- safe for destructive queries.
- Wrap destructive queries in a transaction and roll back: `BEGIN; EXPLAIN ANALYZE DELETE ...; ROLLBACK;`.
- Use `\timing` in `psql` for quick wall-clock measurements.
- Compare plans before and after adding an index to confirm it is used.
