---
name: monorepo-setup-guide
description: Scaffold and configure monorepos using Turborepo or Nx. Covers workspace structure, package organization, build caching, task pipelines, dependency management, and incremental adoption strategies.
metadata:
  displayName: "Monorepo Setup Guide"
  categories: ["engineering"]
  tags: ["monorepo", "turborepo", "nx", "workspace", "build-cache", "task-pipeline", "pnpm"]
  worksWellWithAgents: ["developer-experience-engineer", "monorepo-architect", "platform-engineer"]
  worksWellWithSkills: ["architecture-decision-record", "ci-cd-pipeline-design"]
---

# Monorepo Setup Guide

## Before you start

Gather the following from the user:

1. **Which tool?** (Turborepo, Nx, or help deciding)
2. **What packages will exist?** (Apps, shared libraries, configs)
3. **Package manager?** (pnpm, npm, yarn — pnpm recommended for monorepos)
4. **What language/framework?** (TypeScript, React, Next.js, Node.js, mixed)
5. **Existing repo or greenfield?** (Migrating from multi-repo or starting fresh)
6. **Team size?** (Affects caching and CI strategy)

If the user says "set up a monorepo," push back: "What packages do you need? I need to know the apps, shared libraries, and your package manager to design the workspace structure."

**Turborepo vs Nx decision guide:**
- Turborepo: Simpler mental model, zero-config caching, good for TypeScript/JS monorepos under 20 packages.
- Nx: More features (generators, affected commands, module boundary rules), better for large monorepos (20+ packages) or polyglot stacks.

## Procedure

### Step 1: Define the workspace structure

```
monorepo/
  apps/
    web/                  # Next.js frontend
    api/                  # Express/Fastify backend
    mobile/               # React Native app
  packages/
    ui/                   # Shared component library
    config-eslint/        # Shared ESLint config
    config-typescript/    # Shared tsconfig
    shared-utils/         # Shared utility functions
    database/             # Database client and schema
  tooling/
    scripts/              # Build and maintenance scripts
  turbo.json              # or nx.json
  package.json            # Root workspace config
  pnpm-workspace.yaml     # Workspace package globs
```

Rules for package organization:
- `apps/` contains deployable applications. Each has its own build output.
- `packages/` contains shared libraries consumed by apps or other packages.
- Config packages (`config-*`) export shared tool configurations.
- Every package has its own `package.json` with a `name` field using a scope: `@repo/ui`.

### Step 2: Configure the workspace root

Create `pnpm-workspace.yaml` listing `apps/*`, `packages/*`, and `tooling/*`. Root `package.json` should be `private: true`, define scripts that delegate to turbo (`turbo build`, `turbo dev`, etc.), pin `packageManager` version, and install only workspace-level tools (turbo) as devDependencies. All other dependencies go in the package that uses them.

### Step 3: Configure the task pipeline

Define tasks in `turbo.json` (or `nx.json` with `targetDefaults`). Essential task definitions:

- **build:** `dependsOn: ["^build"]`, `outputs: ["dist/**", ".next/**"]`
- **dev:** `cache: false`, `persistent: true`
- **lint:** `dependsOn: ["^build"]`
- **test:** `dependsOn: ["build"]`
- **clean:** `cache: false`

Key pipeline concepts:
- `^build` means "run build in my dependencies first" (topological dependency)
- `dependsOn: ["build"]` means "run my own build first"
- `outputs` defines what gets cached — must include all build artifacts
- `cache: false` for dev servers and clean commands
- `persistent: true` for long-running dev servers

### Step 4: Set up internal package references

Each package that depends on another workspace package:

Each shared package needs a scoped `name` (`@repo/ui`), `main`, `types`, and `exports` fields pointing to source entry points. Consumer packages reference them with `"@repo/ui": "workspace:*"` in dependencies. The `workspace:*` protocol tells the package manager to resolve from the workspace, not the registry.

### Step 5: Configure shared TypeScript

Create a `packages/config-typescript/base.json` with strict settings: `strict: true`, `target: ES2022`, `module: ESNext`, `moduleResolution: bundler`, `declaration: true`, `isolatedModules: true`. Each package extends it with `"extends": "@repo/config-typescript/base.json"` and adds its own `outDir` and `include` paths. Different packages override as needed (React packages add `jsx`, Node packages adjust `module`).

### Step 6: Enable remote caching

**Turborepo:** `npx turbo login && npx turbo link` to connect Vercel Remote Cache. **Nx:** `npx nx connect` for Nx Cloud. Both support self-hosted alternatives. Remote caching shares build artifacts across developers and CI — expected impact is 40-70% CI time reduction after warm cache.

### Step 7: Configure CI for monorepos

Use filtering to only build/test affected packages. Turborepo: `turbo build --filter=...[origin/main]`. Nx: `nx affected --target=build --base=origin/main`. CI pipeline should restore remote cache, run affected commands, and only deploy apps whose build output changed.

## Quality checklist

Before delivering the monorepo setup, verify:

- [ ] Every package has a scoped `name` in its package.json
- [ ] `pnpm-workspace.yaml` (or equivalent) lists all package directories
- [ ] Task pipeline defines `dependsOn` with correct topological order
- [ ] Build `outputs` are specified so caching works correctly
- [ ] Internal packages use `workspace:*` protocol for references
- [ ] TypeScript configs extend a shared base config
- [ ] Dev command is marked `cache: false` and `persistent: true`
- [ ] CI uses affected/filter commands, not full rebuild

## Common mistakes

- **Missing `outputs` in task config.** If `outputs` is empty or wrong, the cache stores nothing. Builds re-run every time despite "cache hit" messages.
- **Circular dependencies between packages.** Package A imports from B, B imports from A. This breaks topological builds. Refactor shared code into a third package.
- **Installing dependencies at the root.** Putting `react` in the root `package.json` makes all packages implicitly depend on it. Install dependencies in the package that uses them.
- **Not using `workspace:*` protocol.** Referencing internal packages by version (`"@repo/ui": "^1.0.0"`) causes the package manager to look in the registry instead of the workspace.
- **Skipping remote cache setup.** Without remote caching, every CI run and every developer rebuilds from scratch. This is the single biggest monorepo performance win.
- **One tsconfig for everything.** Different packages need different settings (React needs JSX, Node packages do not). Use a shared base config that each package extends with overrides.
