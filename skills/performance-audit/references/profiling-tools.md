# Profiling Tools by Layer

Quick reference for choosing the right profiling tool based on the layer you are investigating.

## Frontend

| Tool | What It Shows | Key Command / Workflow |
|------|--------------|----------------------|
| Chrome DevTools Performance | Flame chart of main-thread activity, long tasks, layout/paint events | `F12` > Performance > Record > interact > Stop. Look for red triangles (long tasks > 50 ms). |
| Lighthouse | Automated CWV scores, opportunities, diagnostics | `F12` > Lighthouse > Analyze. Or CLI: `npx lighthouse https://example.com --output=html` |
| React Profiler | Component render times, wasted re-renders, commit phases | `React DevTools` > Profiler > Record > interact > Stop. Sort by "self time" to find expensive components. |
| Vue Devtools | Component render timeline, event tracking | Vue Devtools > Performance > Start Recording. |
| Webpack Bundle Analyzer | Treemap of bundle contents by module size | `npx webpack-bundle-analyzer stats.json` or `ANALYZE=true next build` (Next.js). |
| Source Map Explorer | Trace bundle bytes to individual source files | `npx source-map-explorer bundle.js bundle.js.map` |
| WebPageTest | Real-browser filmstrip, waterfall, CWV breakdown | webpagetest.org > enter URL > select location/connection > Run Test. |

## Backend

| Tool | What It Shows | Key Command / Workflow |
|------|--------------|----------------------|
| Node.js `--prof` | V8 CPU profile (tick-based sampling) | `node --prof app.js` then `node --prof-process isolate-*.log > profile.txt`. Look for top "ticks" functions. |
| Node.js `--inspect` | Live CPU/heap profiling via Chrome DevTools | `node --inspect app.js` then open `chrome://inspect`. Record CPU profile or take heap snapshot. |
| Clinic.js (Node) | Doctor (event loop), Flame (CPU), Bubbleprof (async) | `npx clinic doctor -- node app.js`, then `npx clinic flame -- node app.js`. |
| Python `cProfile` | Function-level call counts and cumulative time | `python -m cProfile -s cumtime app.py`. Sort by `cumtime` for wall-clock bottlenecks. |
| Python `py-spy` | Sampling profiler, no code changes needed | `py-spy top --pid <PID>` for live view, `py-spy record -o profile.svg --pid <PID>` for flame graph. |
| Go `pprof` | CPU, memory, goroutine, block profiles | Import `net/http/pprof`, then: `go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30`. Use `top`, `web`, or `list <func>`. |
| Java VisualVM / async-profiler | CPU sampling, memory allocation, thread dumps | `async-profiler -d 30 -f profile.html <PID>` for flame graph. |
| OpenTelemetry / Jaeger | Distributed traces across services | Instrument with OTel SDK, export to Jaeger. Look for span durations and service-to-service latency. |
| Datadog / New Relic APM | Request traces, error rates, throughput, latency percentiles | Install agent, view Service > Traces. Filter by p95/p99. |

## Database

| Tool | What It Shows | Key Command / Workflow |
|------|--------------|----------------------|
| `EXPLAIN ANALYZE` (PostgreSQL) | Query execution plan with actual row counts and timing | `EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) SELECT ...;` Look for Seq Scan on large tables, high "actual rows" vs "planned rows". |
| `EXPLAIN` (MySQL) | Query execution plan, index usage, join type | `EXPLAIN SELECT ...;` Check `type` column: `ALL` = full scan (bad), `ref`/`eq_ref` = index used (good). |
| `pg_stat_statements` (PostgreSQL) | Aggregated query stats: call count, total/mean time, rows | `SELECT query, calls, mean_exec_time, total_exec_time FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 10;` |
| MySQL Slow Query Log | Queries exceeding a time threshold | Set `slow_query_log = 1` and `long_query_time = 0.5` in `my.cnf`. Review with `mysqldumpslow`. |
| MongoDB Profiler | Slow operations with execution stats | `db.setProfilingLevel(1, { slowms: 100 })` then `db.system.profile.find().sort({ ts: -1 }).limit(10)` |
| Redis `SLOWLOG` | Commands exceeding a latency threshold | `SLOWLOG GET 10` shows the 10 slowest recent commands with execution time in microseconds. |
| Connection pool metrics | Pool exhaustion, wait time, active/idle connections | Check your pool library's stats endpoint (e.g., HikariCP metrics, pgBouncer `SHOW STATS`). |

## Infrastructure / Network

| Tool | What It Shows | Key Command / Workflow |
|------|--------------|----------------------|
| `curl -w` timing | DNS, TCP, TLS, TTFB breakdown for a single request | `curl -o /dev/null -w "dns: %{time_namelookup}s\ntcp: %{time_connect}s\ntls: %{time_appconnect}s\nttfb: %{time_starttransfer}s\ntotal: %{time_total}s\n" https://example.com` |
| `k6` / `wrk` / `ab` | Load testing: throughput, latency percentiles under concurrency | `k6 run script.js` or `wrk -t4 -c100 -d30s https://example.com/api` |
| `htop` / `top` | CPU and memory usage per process | `htop` then sort by CPU (`P`) or memory (`M`). |
| `iostat` | Disk I/O throughput and utilization | `iostat -x 1` to see per-device stats every second. Watch `%util` and `await`. |
