# CI/CD Caching Strategies

Per-ecosystem cache key patterns, hit-rate targets, restore-key fallback rules, and optimization techniques.

---

## Core Principles

1. **Cache the dependency directory, not node_modules alone.** Some tools store caches outside the project (pip, Go, Gradle). Cache the tool's store directory.
2. **Key on the lockfile hash.** The lockfile is the fingerprint of your resolved dependency tree. When it changes, the cache should invalidate.
3. **Always set restore-keys.** A partial cache hit (from a previous lockfile) is faster than a cold install. Restore-keys provide fallback.
4. **Exclude build caches from artifact caches.** Build output caching (Next.js `.next/cache`, Gradle build cache) has different invalidation needs than dependency caching.
5. **Monitor hit rates.** Below 80% means your key strategy needs adjustment. Below 50% means caching is providing almost no benefit.

---

## Node.js (npm / yarn / pnpm)

### pnpm (recommended for monorepos)

```yaml
# GitHub Actions
- uses: actions/cache@v4
  with:
    path: |
      node_modules
      ~/.local/share/pnpm/store
    key: pnpm-${{ runner.os }}-${{ hashFiles('pnpm-lock.yaml') }}
    restore-keys: |
      pnpm-${{ runner.os }}-
```

Alternative: `actions/setup-node` with `cache: "pnpm"` handles this automatically.

### npm

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: npm-${{ runner.os }}-${{ hashFiles('package-lock.json') }}
    restore-keys: |
      npm-${{ runner.os }}-
```

Cache `~/.npm` (the global cache), not `node_modules`. npm reinstalls from the cache directory, which is faster than downloading from the registry.

### yarn (v1)

```yaml
- uses: actions/cache@v4
  with:
    path: |
      node_modules
      ~/.cache/yarn
    key: yarn-${{ runner.os }}-${{ hashFiles('yarn.lock') }}
    restore-keys: |
      yarn-${{ runner.os }}-
```

### yarn (Berry / v3+)

```yaml
- uses: actions/cache@v4
  with:
    path: .yarn/cache
    key: yarn-${{ runner.os }}-${{ hashFiles('yarn.lock') }}
    restore-keys: |
      yarn-${{ runner.os }}-
```

Berry stores cached packages in `.yarn/cache/` within the project. With zero-installs (`nodeLinker: pnp`), commit this directory to git and skip the cache step entirely.

### Next.js build cache

```yaml
- uses: actions/cache@v4
  with:
    path: apps/web/.next/cache
    key: nextjs-${{ runner.os }}-${{ hashFiles('pnpm-lock.yaml') }}-${{ hashFiles('apps/web/src/**') }}
    restore-keys: |
      nextjs-${{ runner.os }}-${{ hashFiles('pnpm-lock.yaml') }}-
      nextjs-${{ runner.os }}-
```

The Next.js build cache stores compiled pages and webpack chunks. Cache it separately from dependencies.

---

## Python (pip / poetry / uv)

### pip

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: pip-${{ runner.os }}-${{ hashFiles('requirements.txt') }}
    restore-keys: |
      pip-${{ runner.os }}-
```

### poetry

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache/pypoetry
    key: poetry-${{ runner.os }}-${{ hashFiles('poetry.lock') }}
    restore-keys: |
      poetry-${{ runner.os }}-
```

### uv

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache/uv
    key: uv-${{ runner.os }}-${{ hashFiles('uv.lock') }}
    restore-keys: |
      uv-${{ runner.os }}-
```

uv is significantly faster than pip even without caching. With caching, installs are near-instant.

---

## Go

```yaml
- uses: actions/cache@v4
  with:
    path: |
      ~/go/pkg/mod
      ~/.cache/go-build
    key: go-${{ runner.os }}-${{ hashFiles('go.sum') }}
    restore-keys: |
      go-${{ runner.os }}-
```

Cache both the module cache (`~/go/pkg/mod`) and the build cache (`~/.cache/go-build`). The build cache stores compiled packages and test results.

---

## Rust (cargo)

```yaml
- uses: actions/cache@v4
  with:
    path: |
      ~/.cargo/registry/index
      ~/.cargo/registry/cache
      ~/.cargo/git/db
      target/
    key: cargo-${{ runner.os }}-${{ hashFiles('Cargo.lock') }}
    restore-keys: |
      cargo-${{ runner.os }}-
```

The `target/` directory contains compiled artifacts. It can be large (several GB for complex projects). Consider using `sccache` for distributed compilation caching across CI runners.

Tip: Use `cargo-chef` in Docker builds to cache dependency compilation separately from application code compilation.

---

## Java (Maven / Gradle)

### Maven

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.m2/repository
    key: maven-${{ runner.os }}-${{ hashFiles('**/pom.xml') }}
    restore-keys: |
      maven-${{ runner.os }}-
```

### Gradle

```yaml
- uses: actions/cache@v4
  with:
    path: |
      ~/.gradle/caches
      ~/.gradle/wrapper
    key: gradle-${{ runner.os }}-${{ hashFiles('**/*.gradle*', '**/gradle-wrapper.properties') }}
    restore-keys: |
      gradle-${{ runner.os }}-
```

Gradle also supports a build cache (`--build-cache`). For CI, enable the local build cache and consider Gradle Enterprise's remote build cache for large teams.

---

## Docker

### GitHub Actions (BuildKit cache)

```yaml
- uses: docker/build-push-action@v5
  with:
    context: .
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

`mode=max` caches all layers, not just the final image layers. This is critical for multi-stage builds where intermediate layers (dependency install) should be cached.

### Registry-based cache

```yaml
- uses: docker/build-push-action@v5
  with:
    context: .
    cache-from: type=registry,ref=ghcr.io/org/app:cache
    cache-to: type=registry,ref=ghcr.io/org/app:cache,mode=max
```

Registry caching works across CI providers and self-hosted runners.

---

## Restore-Key Fallback Rules

Restore-keys are tried in order. The first prefix match wins. Design them from most-specific to least-specific:

```yaml
key: pnpm-linux-abc123def456        # Exact lockfile hash
restore-keys: |
  pnpm-linux-                        # Any lockfile on same OS
```

**Why this works:** A stale cache with most dependencies already present is faster than no cache at all. `pnpm install --frozen-lockfile` will add/update only the changed packages.

**When restore-keys hurt:** If the cache is very large and mostly stale (e.g., after a major dependency overhaul), restoring and then updating can be slower than a fresh install. This is rare.

### Multi-dimensional keys

For monorepos or projects with multiple lockfiles:

```yaml
key: deps-${{ runner.os }}-${{ hashFiles('**/pnpm-lock.yaml') }}-${{ hashFiles('apps/web/src/**') }}
restore-keys: |
  deps-${{ runner.os }}-${{ hashFiles('**/pnpm-lock.yaml') }}-
  deps-${{ runner.os }}-
```

---

## Hit-Rate Targets

| Hit rate | Assessment | Action |
|----------|-----------|--------|
| 90-100% | Excellent | Maintain current strategy |
| 80-89% | Good | Monitor — acceptable for active development |
| 60-79% | Needs attention | Check if lockfile changes too frequently, or if key includes volatile inputs |
| Below 60% | Caching is nearly useless | Audit cache keys — likely keying on something that changes every run |

### Common causes of low hit rates

1. **Keying on `package.json` instead of lockfile.** `package.json` changes when scripts or metadata change, not just dependencies.
2. **Including `node_modules` size in a workspace.** In monorepos, `node_modules` can be 1-2 GB. Some CI providers have cache size limits (5-10 GB). If the cache exceeds the limit, it is never stored.
3. **Renovate/Dependabot updates.** Automated dependency updates change the lockfile on every PR. This is expected — the cache warms up after merge.
4. **Hashring including non-dependency files.** `hashFiles('**/*')` invalidates the cache on every commit.

---

## Platform-Specific Notes

### GitHub Actions
- Cache size limit: 10 GB per repository
- Caches expire after 7 days of no access
- Caches are scoped to branches (PR caches can read from base branch)
- Use `actions/cache@v4` (v4 uses improved cache backend)

### GitLab CI
- Cache is per-runner by default (use `cache:key:files` for lockfile-based keys)
- `cache:policy: pull` in jobs that only read cached data (saves upload time)
- Consider using `cache:when: on_success` to avoid caching broken states

### CircleCI
- Use `save_cache` and `restore_cache` steps
- Caches are immutable — once saved with a key, they cannot be overwritten
- Use lockfile hash in key to ensure new dependencies trigger new cache
- `restore_cache` supports prefix matching (equivalent to restore-keys)
