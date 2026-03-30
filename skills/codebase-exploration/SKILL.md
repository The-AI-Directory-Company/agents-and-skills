---
name: codebase-exploration
description: Systematic methodology for understanding unfamiliar repositories — finding entry points, mapping architecture layers, tracing data flows, and identifying patterns and conventions used across the codebase.
metadata:
  displayName: "Codebase Exploration"
  categories: ["engineering"]
  tags: ["onboarding", "architecture", "code-reading", "codebase", "exploration", "reverse-engineering"]
  worksWellWithAgents: ["code-explainer", "codebase-onboarder", "software-architect", "tech-lead"]
  worksWellWithSkills: ["architecture-decision-record", "code-review-checklist", "system-design-document"]
---

# Codebase Exploration

## Before you start

Gather the following from the user. If anything is missing, ask before proceeding:

1. **What is the repository?** — URL or local path to the codebase
2. **What is the goal?** — Bug fix, feature addition, general understanding, onboarding, or audit
3. **What do you already know?** — Language, framework, or prior context (even partial)
4. **What is the scope?** — Entire repo, a specific subsystem, or a single feature flow
5. **What is the time budget?** — Quick orientation (30 min) or deep mapping (hours)

## Exploration procedure

### 1. Read the Project Manifest

Start with the files that declare what the project is and how it runs:

- `README.md`, `CONTRIBUTING.md`, `CLAUDE.md` — stated architecture, setup, conventions
- `package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod` — language, dependencies, scripts
- `Dockerfile`, `docker-compose.yml`, `.env.example` — runtime environment and services
- CI config (`.github/workflows/`, `.gitlab-ci.yml`) — build steps reveal the dependency graph

Record: language, framework, build tool, test runner, deployment target.

### 2. Map the Directory Structure

Run a shallow tree (depth 2-3) and classify each top-level directory:

- **Entry points**: `src/index.*`, `app/`, `cmd/`, `main.*`
- **Configuration**: config files, env schemas, feature flags
- **Domain logic**: models, services, use-cases, controllers
- **Data access**: repositories, queries, migrations, ORM schemas
- **API surface**: routes, handlers, resolvers, RPC definitions
- **Shared utilities**: libs, helpers, utils, common
- **Tests**: test directories, fixture files, factories

Sketch a layer diagram: entry point -> routing -> handlers -> domain -> data access -> external services.

### 3. Trace the Primary Data Flow

Pick the most important user action (e.g., "user signs up", "order is placed") and trace it end-to-end:

1. Find the route or entry point that handles it
2. Follow the handler into service/domain logic
3. Identify every database query, API call, or side effect
4. Note the response path back to the caller
5. Record each file touched and its role in the flow

This single trace reveals naming conventions, error handling patterns, and the project's layering strategy.

### 4. Identify Patterns and Conventions

Look for recurring structural patterns across 3-5 files of the same type:

- **Naming**: How are files, functions, variables, and types named?
- **Error handling**: Exceptions, result types, error codes, or error boundaries?
- **State management**: Global store, context, dependency injection, or passed parameters?
- **Authentication/authorization**: Middleware, decorators, guards, or inline checks?
- **Testing style**: Unit-heavy, integration-heavy, or end-to-end? Mocks or real dependencies?

Document each pattern with a concrete file reference.

### 5. Map External Dependencies

Identify every external system the codebase communicates with:

- Databases and caches (connection strings, ORM config)
- Third-party APIs (HTTP clients, SDK imports)
- Message queues or event buses
- File storage (S3, local disk)
- Authentication providers

For each, note: what module owns the integration, how errors are handled, and whether there is a fallback.

### 6. Locate the Test Suite

Find where tests live and assess coverage:

- Run the test command from the manifest (e.g., `npm test`, `pytest`)
- Identify which areas have dense coverage and which have none
- Check for test utilities, factories, or fixtures that reveal domain assumptions

### 7. Produce the Exploration Summary

Deliver a structured summary:

| Section | Content |
|---------|---------|
| Stack | Language, framework, runtime, key libraries |
| Architecture | Layer diagram or description |
| Entry points | Main files that start the application |
| Primary data flow | Step-by-step trace of the core user action |
| Patterns | Naming, error handling, state, auth conventions |
| External deps | Every external system and its integration module |
| Test coverage | Where tests exist, where they are missing |
| Risks/concerns | Dead code, circular deps, missing docs, unclear ownership |

## Quality checklist

Before delivering the exploration summary, verify:

- [ ] The project manifest was read and stack is identified correctly
- [ ] Directory structure is classified by responsibility, not just listed
- [ ] At least one end-to-end data flow is traced with specific file references
- [ ] Patterns are documented with concrete examples, not guessed
- [ ] External dependencies are enumerated with owning modules
- [ ] Test coverage gaps are identified
- [ ] The summary is structured and scannable, not a wall of text

## Common mistakes

- **Jumping straight to code without reading the manifest.** The README, package manager config, and CI files answer half your questions in 5 minutes.
- **Listing files instead of classifying them.** A directory listing is not understanding. Every folder should have a role label.
- **Stopping at the surface layer.** Reading route definitions without tracing into handlers and data access misses the actual architecture.
- **Assuming conventions from one file.** Check at least 3 files of the same type before declaring a pattern. One file might be an exception.
- **Ignoring the test suite.** Tests are executable documentation. They reveal intended behavior, edge cases, and which parts the team considers important.
- **Producing an unstructured brain dump.** The output should be a reference someone can scan in 2 minutes, not a narrative essay.
