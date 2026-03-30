# Turborepo vs Nx — Full Comparison

Decision guide for choosing between Turborepo and Nx for monorepo orchestration. Both are production-ready; the right choice depends on scale, team needs, and polyglot requirements.

---

## Feature Matrix

| Feature | Turborepo | Nx |
|---------|-----------|-----|
| **Task orchestration** | Yes — `turbo.json` pipeline | Yes — `nx.json` targetDefaults |
| **Local caching** | Yes (default on) | Yes (default on) |
| **Remote caching** | Vercel Remote Cache (free tier), self-hostable | Nx Cloud (free tier), self-hostable via Nx Replay |
| **Affected/changed detection** | `--filter=...[origin/main]` | `nx affected` (project graph-based) |
| **Dependency graph visualization** | `turbo run build --graph` (outputs DOT format) | `nx graph` (interactive web UI) |
| **Code generators** | None built-in (use `plop` or manual) | `nx generate` — scaffolds apps, libs, components |
| **Module boundary rules** | None built-in | `@nx/enforce-module-boundaries` ESLint rule |
| **Distributed task execution** | Not built-in (Vercel CI does parallelization) | Nx Agents — splits tasks across CI machines |
| **Polyglot support** | JavaScript/TypeScript only | JS/TS, Go, Rust, Java, .NET, Python (via plugins) |
| **Configuration** | `turbo.json` only | `nx.json` + `project.json` per project (or inferred from `package.json`) |
| **Plugins ecosystem** | None (relies on npm ecosystem) | 50+ official/community plugins |
| **Incremental builds** | Via caching (hash-based) | Via caching + Nx buildable libraries |
| **Watch mode** | `turbo watch` (since 2.0) | `nx watch` |
| **Package manager support** | npm, yarn, pnpm | npm, yarn, pnpm |
| **Monorepo style** | Package-based (each package has `package.json`) | Package-based or integrated (single version policy) |

---

## Scale Thresholds

### Small (1-10 packages, 1-5 developers)

**Recommendation: Turborepo**

At this scale, Turborepo's simplicity wins. You get caching and task pipelines with a single `turbo.json` file. There is nothing to learn beyond the pipeline config and filter syntax. Nx's advanced features (generators, module boundaries, distributed execution) add complexity without payoff at this size.

### Medium (10-30 packages, 5-15 developers)

**Recommendation: Either works — decide based on needs**

Both tools handle this scale well. Choose Turborepo if your team values simplicity and is pure TypeScript. Choose Nx if you want:
- Code generators to enforce package structure consistency
- Module boundary rules to prevent circular dependencies
- `nx affected` for precise change detection (Turborepo's `--filter` works but is less granular)

### Large (30-100+ packages, 15+ developers)

**Recommendation: Nx**

At this scale, Nx's advanced features become necessary:
- **Module boundary enforcement** prevents the dependency graph from becoming a hairball
- **Nx Agents** distribute CI across multiple machines (Turborepo has no equivalent)
- **Code generators** ensure new packages follow conventions without manual setup
- **Project graph visualization** helps developers understand the dependency structure
- **Consistent versioning** via integrated monorepo style avoids version drift

### Enterprise (100+ packages, multiple teams)

**Recommendation: Nx with Nx Cloud**

The combination of distributed task execution, fine-grained affected detection, and module boundary rules makes Nx the standard choice for enterprise monorepos. Turborepo can work at this scale but requires more custom tooling to fill the gaps.

---

## Migration Complexity

### Migrating to Turborepo

**From a single repo:**
1. Create `turbo.json` with task pipeline (~30 min)
2. Move code into `apps/` and `packages/` directories
3. Add `workspace:*` references between packages
4. Set up `pnpm-workspace.yaml`

Effort: 1-2 days for a typical project.

**From multiple repos:**
1. All of the above, plus resolving version conflicts between repos
2. Unifying CI pipelines
3. Resolving duplicate dependencies

Effort: 1-2 weeks depending on divergence between repos.

**From Nx to Turborepo:**
1. Replace `nx.json` with `turbo.json`
2. Replace `project.json` files with `package.json` scripts
3. Remove `@nx/*` plugins
4. Lose: generators, module boundaries, distributed execution

Effort: 1-3 days. Main risk is losing features you relied on.

### Migrating to Nx

**From a single repo:**
1. Run `npx nx@latest init` (auto-detects project structure)
2. Configure `nx.json` targetDefaults
3. Optionally add `project.json` per package for fine-grained config

Effort: 1-2 days. Nx's `init` command handles most of the boilerplate.

**From Turborepo to Nx:**
1. Run `npx nx@latest init` — it can migrate `turbo.json` pipeline config
2. Replace `turbo.json` with `nx.json`
3. Optionally add plugins for additional features

Effort: 1-2 days. The core concepts (caching, task deps) map directly.

**From multiple repos:**
Same as Turborepo migration, plus Nx provides `nx migrate` for automated dependency updates.

Effort: 1-3 weeks.

---

## Remote Cache Options

### Turborepo

| Option | Cost | Setup |
|--------|------|-------|
| Vercel Remote Cache | Free (with Vercel account) | `npx turbo login && npx turbo link` |
| Self-hosted (ducktape/turborepo-remote-cache) | Free (your infra) | Deploy the cache server, set `TURBO_API` and `TURBO_TOKEN` env vars |
| Custom API | Free (your infra) | Implement the Turborepo Remote Cache API (simple REST: GET/PUT artifacts by hash) |

### Nx

| Option | Cost | Setup |
|--------|------|-------|
| Nx Cloud | Free (up to 500 CI hours/month) | `npx nx connect` — adds access token to `nx.json` |
| Nx Replay (self-hosted) | Enterprise license | Deploy Nx Cloud on-prem, configure API endpoint |
| Custom runner | Free (your infra) | Implement custom task runner (more complex than Turborepo's cache API) |

### Cache hit-rate expectations

Both tools achieve 80-95% cache hit rates in CI after initial warm-up. Expected impact:
- **First CI run after setup:** 0% hit rate (cold cache)
- **Subsequent PR CI runs:** 60-80% (only changed packages rebuild)
- **Main branch CI runs:** 90-95% (incremental changes)
- **Developer local builds:** 70-90% (pulling from remote cache)

---

## Generator Support

### Turborepo

Turborepo has no built-in generators. Common alternatives:

| Tool | Use case |
|------|----------|
| `plop` | Template-based scaffolding with Handlebars |
| `hygen` | File-based code generator |
| Custom scripts | Shell scripts in `tooling/scripts/` |
| `turbo gen` (experimental) | Basic workspace generator (added in Turbo 1.x, limited) |

### Nx

Nx has first-class generator support:

```bash
# Scaffold a new React library
nx generate @nx/react:library my-lib --directory=packages/my-lib

# Scaffold a new Next.js app
nx generate @nx/next:application my-app --directory=apps/my-app

# Create a custom workspace generator
nx generate @nx/workspace:library --name=generators --directory=tools/generators
```

Generators enforce:
- Consistent file structure across packages
- Correct `tsconfig.json` and `project.json` setup
- Proper dependency wiring
- Test file scaffolding

For teams adding packages frequently (weekly), Nx generators save meaningful time and prevent configuration drift.

---

## Decision Checklist

Choose **Turborepo** if:
- [x] TypeScript/JavaScript only
- [x] Under 20 packages
- [x] Team values minimal configuration
- [x] Using Vercel for deployment (native remote cache integration)
- [x] No need for code generators or module boundary enforcement

Choose **Nx** if:
- [x] More than 20 packages or growing rapidly
- [x] Multiple languages (polyglot monorepo)
- [x] Need module boundary enforcement to prevent circular deps
- [x] Need distributed CI task execution
- [x] Team adds new packages frequently and wants scaffolding generators
- [x] Want interactive dependency graph visualization
