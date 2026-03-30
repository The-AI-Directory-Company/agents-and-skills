# Framework Entry Points Reference

Quick reference for locating manifest files, entry points, directory conventions, and test commands across common stacks. Use this when exploring an unfamiliar repository to know where to look first.

---

## Next.js (App Router)

| Aspect | Location |
|--------|----------|
| Manifest | `package.json` |
| Lockfile | `pnpm-lock.yaml`, `package-lock.json`, or `yarn.lock` |
| Entry point | `src/app/layout.tsx` (root layout), `src/app/page.tsx` (index route) |
| Routing | File-system based: `src/app/**/page.tsx` (or `app/` without `src/`) |
| API routes | `src/app/api/**/route.ts` |
| Middleware | `src/middleware.ts` (root level) |
| Config | `next.config.js` or `next.config.mjs` |
| Environment | `.env.local`, `.env.development`, `.env.production` |
| Static assets | `public/` |
| Directory convention | `(group)/` for route groups, `_components/` for colocated non-routes, `loading.tsx`, `error.tsx`, `not-found.tsx` for route-level UI |
| Test command | `npx vitest` or `npx jest` (check `package.json` scripts) |
| Build output | `.next/` |

**Key signal:** If `app/` exists alongside `pages/`, the project is mid-migration. Check `next.config.js` for `experimental.appDir`.

---

## Ruby on Rails

| Aspect | Location |
|--------|----------|
| Manifest | `Gemfile` |
| Lockfile | `Gemfile.lock` |
| Entry point | `config/routes.rb` (all URL mappings), `config/application.rb` (app config) |
| Routing | Centralized in `config/routes.rb` |
| Controllers | `app/controllers/` |
| Models | `app/models/` |
| Views | `app/views/` (ERB/Haml/Slim templates) |
| Migrations | `db/migrate/` (timestamped SQL/Ruby files) |
| Config | `config/database.yml`, `config/credentials.yml.enc`, `config/initializers/` |
| Background jobs | `app/jobs/` (ActiveJob), Sidekiq config in `config/sidekiq.yml` |
| Directory convention | `app/services/`, `app/serializers/`, `app/policies/` are common additions |
| Test command | `bundle exec rspec` (RSpec) or `bin/rails test` (Minitest) |
| Build output | None (interpreted) — `tmp/` for cache |

**Key signal:** Check `config/initializers/` for third-party setup (Stripe, Sentry, Redis). Check `lib/tasks/` for Rake tasks that reveal batch operations.

---

## Django

| Aspect | Location |
|--------|----------|
| Manifest | `requirements.txt`, `pyproject.toml`, or `Pipfile` |
| Lockfile | `requirements.txt` (pinned), `Pipfile.lock`, or `poetry.lock` |
| Entry point | `manage.py` (CLI), `config/urls.py` or `project_name/urls.py` (URL routing) |
| Routing | `urls.py` in each app, aggregated by the root `urls.py` |
| Views | `views.py` in each app (function or class-based views) |
| Models | `models.py` in each app |
| Migrations | `<app>/migrations/` (auto-generated numbered files) |
| Config | `settings.py` (or `settings/base.py`, `settings/production.py` split) |
| Static assets | `static/`, collected to `STATIC_ROOT` |
| Directory convention | Each Django app: `models.py`, `views.py`, `urls.py`, `serializers.py`, `admin.py`, `tests.py` |
| Test command | `python manage.py test` or `pytest` (with `pytest-django`) |
| Build output | None (interpreted) — `staticfiles/` for collected static assets |

**Key signal:** The `INSTALLED_APPS` list in `settings.py` is the definitive inventory of what the project contains. Third-party apps appear here too.

---

## FastAPI (Python)

| Aspect | Location |
|--------|----------|
| Manifest | `pyproject.toml` or `requirements.txt` |
| Lockfile | `poetry.lock`, `uv.lock`, or pinned `requirements.txt` |
| Entry point | `main.py` or `app/main.py` (creates the `FastAPI()` instance) |
| Routing | `app.include_router()` calls in `main.py`, router files in `app/routers/` or `app/api/` |
| Models | `app/models/` (SQLAlchemy/SQLModel), `app/schemas/` (Pydantic) |
| Migrations | `alembic/versions/` (Alembic) |
| Config | `app/config.py` or `app/settings.py` (Pydantic `BaseSettings`) |
| Dependency injection | `Depends()` in route signatures — check for auth, DB session, and service deps |
| Directory convention | `routers/`, `models/`, `schemas/`, `services/`, `repositories/`, `dependencies/` |
| Test command | `pytest` |
| Build output | None (interpreted) |

**Key signal:** Follow `Depends()` chains to understand how auth, database sessions, and services are wired. The dependency graph is the architecture.

---

## Go (stdlib / Chi / Gin)

| Aspect | Location |
|--------|----------|
| Manifest | `go.mod` |
| Lockfile | `go.sum` |
| Entry point | `cmd/<app>/main.go` or `main.go` at root |
| Routing | `http.HandleFunc` / `chi.NewRouter()` / `gin.Default()` in main or a `routes.go` file |
| Handlers | `internal/handler/` or `internal/api/` |
| Domain logic | `internal/service/` or `internal/<domain>/` |
| Data access | `internal/repository/` or `internal/store/` |
| Migrations | `migrations/` (goose, golang-migrate, or Atlas) |
| Config | `config/config.go` (env vars via `envconfig` or `viper`) |
| Directory convention | `cmd/` (entrypoints), `internal/` (private packages), `pkg/` (public packages) |
| Test command | `go test ./...` |
| Build output | Binary in `bin/` or project root |

**Key signal:** `internal/` packages cannot be imported from outside the module — this is Go's built-in encapsulation. Check `cmd/` for multiple binaries (API server, worker, CLI tool).

---

## Spring Boot (Java/Kotlin)

| Aspect | Location |
|--------|----------|
| Manifest | `pom.xml` (Maven) or `build.gradle.kts` (Gradle) |
| Lockfile | `gradle.lockfile` (Gradle) or `pom.xml` pins (Maven) |
| Entry point | Class annotated with `@SpringBootApplication` (search for it) |
| Routing | `@RestController` classes with `@RequestMapping` / `@GetMapping` |
| Domain logic | `service/` package (classes annotated `@Service`) |
| Data access | `repository/` package (interfaces extending `JpaRepository`) |
| Models | `entity/` or `model/` package (classes annotated `@Entity`) |
| Migrations | `src/main/resources/db/migration/` (Flyway) or `db/changelog/` (Liquibase) |
| Config | `src/main/resources/application.yml` (or `.properties`), profile-specific: `application-dev.yml` |
| Directory convention | Package by layer: `controller/`, `service/`, `repository/`, `entity/`, `dto/`, `config/` |
| Test command | `mvn test` or `gradle test` |
| Build output | `target/*.jar` (Maven) or `build/libs/*.jar` (Gradle) |

**Key signal:** Read `application.yml` first — it reveals database URLs, enabled profiles, feature flags, and third-party integration config. Check for `@Configuration` classes in a `config/` package.

---

## Laravel (PHP)

| Aspect | Location |
|--------|----------|
| Manifest | `composer.json` |
| Lockfile | `composer.lock` |
| Entry point | `public/index.php` (HTTP), `routes/web.php` and `routes/api.php` (routing) |
| Routing | `routes/web.php` (browser routes), `routes/api.php` (API routes) |
| Controllers | `app/Http/Controllers/` |
| Models | `app/Models/` (Eloquent) |
| Migrations | `database/migrations/` (timestamped PHP files) |
| Config | `config/` directory (per-service config files), `.env` |
| Middleware | `app/Http/Middleware/` |
| Background jobs | `app/Jobs/` (Laravel Queue) |
| Directory convention | `app/Services/`, `app/Actions/`, `app/Policies/`, `app/Events/`, `app/Listeners/` |
| Test command | `php artisan test` or `./vendor/bin/phpunit` |
| Build output | None (interpreted) — `storage/` for cache and logs |

**Key signal:** Check `app/Providers/` — service providers wire the entire application. `AppServiceProvider` and custom providers reveal binding, event, and scheduling configuration.

---

## NestJS (TypeScript)

| Aspect | Location |
|--------|----------|
| Manifest | `package.json` |
| Lockfile | `pnpm-lock.yaml`, `package-lock.json`, or `yarn.lock` |
| Entry point | `src/main.ts` (creates the Nest app), `src/app.module.ts` (root module) |
| Routing | `@Controller()` classes with `@Get()`, `@Post()` decorators |
| Modules | `src/<feature>/<feature>.module.ts` — each feature is a self-contained module |
| Services | `src/<feature>/<feature>.service.ts` (annotated `@Injectable()`) |
| Data access | TypeORM entities or Prisma schema in `prisma/schema.prisma` |
| Config | `src/config/` module, `.env`, or `ConfigModule.forRoot()` |
| Guards & middleware | `src/common/guards/`, `src/common/middleware/` |
| Directory convention | Feature modules: `<feature>/` with `controller`, `service`, `module`, `dto/`, `entities/` |
| Test command | `npx jest` (unit: `*.spec.ts`, e2e: `test/*.e2e-spec.ts`) |
| Build output | `dist/` |

**Key signal:** The module dependency graph IS the architecture. Read `app.module.ts` imports to see every feature module. Use `@Module({ imports: [...] })` to trace the dependency tree.

---

## Quick Lookup: "I Just Cloned This Repo"

For any repository, check these files in order:

1. **README.md** — Setup instructions, architecture overview
2. **CLAUDE.md** — AI-specific context (if present)
3. **package.json / Cargo.toml / go.mod / pyproject.toml** — Language, dependencies, scripts
4. **Dockerfile / docker-compose.yml** — Services and runtime environment
5. **CI config** (`.github/workflows/`, `.gitlab-ci.yml`) — Build and test commands
6. **.env.example** — Required environment variables (reveals external dependencies)
