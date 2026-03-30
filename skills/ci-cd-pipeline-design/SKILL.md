---
name: ci-cd-pipeline-design
description: Design CI/CD pipeline configurations for GitHub Actions, GitLab CI, and CircleCI. Covers build, test, and deploy stages with caching strategies, parallelization, environment promotion, and secret management.
metadata:
  displayName: "CI/CD Pipeline Design"
  categories: ["engineering", "operations"]
  tags: ["ci-cd", "github-actions", "gitlab-ci", "circleci", "pipeline", "deployment", "devops"]
  worksWellWithAgents: ["ci-cd-engineer", "devops-engineer", "platform-engineer"]
  worksWellWithSkills: ["monorepo-setup-guide", "release-checklist", "runbook-writing"]
---

# CI/CD Pipeline Design

## Before you start

Gather the following from the user:

1. **Which CI/CD platform?** (GitHub Actions, GitLab CI, CircleCI, or platform-agnostic)
2. **What language/runtime?** (Node.js, Python, Go, Java, Rust, multi-language)
3. **What needs to happen?** (Lint, test, build, deploy — which of these?)
4. **Where does it deploy?** (Vercel, AWS, GCP, Kubernetes, static hosting)
5. **What is the branching strategy?** (Trunk-based, GitFlow, feature branches)
6. **What is slow today?** (If optimizing an existing pipeline, what takes the longest?)

If the user says "set up CI/CD," push back: "For which platform, language, and deployment target? I also need your branching strategy to design the trigger rules."

## Procedure

### Step 1: Define trigger rules

Map git events to pipeline runs:

```yaml
# GitHub Actions example
on:
  pull_request:
    branches: [main]          # Run tests on PRs to main
  push:
    branches: [main]          # Deploy on merge to main
    tags: ["v*"]              # Deploy releases on version tags
  workflow_dispatch:           # Manual trigger for ad-hoc runs
```

Rules:
- PRs trigger lint + test + build (no deploy)
- Merge to main triggers lint + test + build + deploy to staging
- Tags trigger deploy to production
- Never auto-deploy to production on push to main

### Step 2: Design the stage graph

Organize jobs into stages with dependency edges:

```
[Lint] ──┐
         ├──> [Build] ──> [Deploy Staging] ──> [Smoke Test] ──> [Deploy Prod]
[Test] ──┘
```

For each stage, document:

| Stage | Trigger | Depends on | Timeout | Runs on |
|-------|---------|------------|---------|---------|
| Lint | PR + push | None | 5 min | ubuntu-latest |
| Test | PR + push | None | 15 min | ubuntu-latest |
| Build | PR + push | Lint + Test pass | 10 min | ubuntu-latest |
| Deploy staging | Push to main | Build | 10 min | ubuntu-latest |
| Smoke test | After staging deploy | Deploy staging | 5 min | ubuntu-latest |
| Deploy prod | Tag v* or manual | Smoke test pass | 10 min | ubuntu-latest |

Run Lint and Test in parallel. They have no dependency on each other.

### Step 3: Configure caching

Caching is the single highest-impact optimization. For each ecosystem, cache the dependency directory with a key based on the lockfile hash:

- **Node.js:** Cache `node_modules`, key on `hashFiles('pnpm-lock.yaml')`
- **Python:** Cache `~/.cache/pip`, key on `hashFiles('requirements.txt')`
- **Go:** Cache `~/go/pkg/mod` + `~/.cache/go-build`, key on `hashFiles('go.sum')`
- **Docker:** Use `cache-from: type=gha` and `cache-to: type=gha,mode=max`

Always set `restore-keys` for partial cache hits. Monitor cache hit rates — below 80% means the key strategy needs adjustment.

### Step 4: Implement test parallelization

Split tests across parallel runners to reduce wall-clock time:

**GitHub Actions matrix:**
```yaml
test:
  strategy:
    matrix:
      shard: [1, 2, 3, 4]
  steps:
    - run: npx jest --shard=${{ matrix.shard }}/4
```

**CircleCI parallelism:**
```yaml
test:
  parallelism: 4
  steps:
    - run: |
        TESTS=$(circleci tests glob "**/*.test.ts" | circleci tests split --split-by=timings)
        npx jest $TESTS
```

Split by timing data when available. Fall back to file count splitting. Rebalance shards when test distribution becomes uneven.

### Step 5: Configure secrets and environment variables

Use the platform's secret store (`${{ secrets.X }}` in GitHub Actions, CI/CD variables in GitLab). Rules:
- Never echo secrets in logs — use `add-mask` or equivalent
- Scope secrets per environment (staging vs production)
- For OIDC-capable targets (AWS, GCP), use identity federation instead of static credentials
- Document secret rotation procedure in the pipeline README

### Step 6: Add deploy gates

Between staging and production, require at least one gate:

- **Smoke test**: Automated health check hitting critical endpoints on staging
- **Manual approval**: Required for production deploys (GitHub: `environment` with reviewers; GitLab: `when: manual`)
- **Canary verification**: Deploy to a subset, verify metrics, then proceed

```yaml
# GitHub Actions environment protection
deploy-prod:
  environment:
    name: production
    url: https://app.example.com
  needs: [smoke-test]
```

### Step 7: Handle artifacts

Build once, deploy the same artifact to all environments. Upload build output as a pipeline artifact with a retention policy. Download in deploy jobs. The artifact deployed to production must be byte-identical to what was tested in staging — never rebuild per environment.

## Quality checklist

Before delivering the pipeline configuration, verify:

- [ ] PRs run lint + test + build but never deploy
- [ ] Lint and test run in parallel where possible
- [ ] Caching is configured for dependencies with lockfile-based keys
- [ ] Secrets use the platform's secret store, never hardcoded
- [ ] Production deploy requires a gate (manual approval or automated canary)
- [ ] Build artifacts are created once and reused across environments
- [ ] Timeouts are set on every job to prevent hung pipelines
- [ ] The pipeline YAML is syntactically valid for the target platform

## Common mistakes

- **Deploying to production on push to main.** Always gate production deploys behind manual approval or automated verification. A broken merge should not reach users automatically.
- **No caching.** Installing dependencies from scratch on every run wastes 2-5 minutes. Cache aggressively and monitor hit rates.
- **Rebuilding per environment.** Building separately for staging and production means you are deploying untested artifacts to production. Build once, deploy everywhere.
- **Sequential lint and test.** These have no dependency on each other. Run them in parallel to cut pipeline time.
- **Secrets in pipeline YAML.** Even "temporary" secrets in YAML files end up in git history. Use the platform's secret management from day one.
- **No timeout on jobs.** A hung test suite or a stuck deploy can block the pipeline for hours. Set explicit timeouts on every job.
