# Greenfield Monorepo: Next.js + Express API

Complete example of a monorepo with a Next.js frontend, Express API backend, and shared packages. Uses pnpm workspaces and Turborepo.

---

## Folder Structure

```
acme-platform/
├── apps/
│   ├── web/                          # Next.js 14 frontend
│   │   ├── src/
│   │   │   ├── app/                  # App Router pages
│   │   │   ├── components/           # UI components
│   │   │   └── lib/                  # Client-side utilities
│   │   ├── next.config.mjs
│   │   ├── tailwind.config.ts
│   │   ├── tsconfig.json             # Extends @repo/tsconfig/nextjs.json
│   │   └── package.json
│   │
│   └── api/                          # Express API server
│       ├── src/
│       │   ├── index.ts              # Server entry point
│       │   ├── routes/               # Route handlers
│       │   ├── middleware/            # Auth, logging, error handling
│       │   └── services/             # Business logic
│       ├── tsconfig.json             # Extends @repo/tsconfig/node.json
│       └── package.json
│
├── packages/
│   ├── ui/                           # Shared React component library
│   │   ├── src/
│   │   │   ├── button.tsx
│   │   │   ├── input.tsx
│   │   │   └── index.ts              # Barrel export
│   │   ├── tsconfig.json
│   │   └── package.json
│   │
│   ├── shared-types/                 # TypeScript types shared between frontend and API
│   │   ├── src/
│   │   │   ├── user.ts
│   │   │   ├── invoice.ts
│   │   │   └── index.ts
│   │   ├── tsconfig.json
│   │   └── package.json
│   │
│   ├── validation/                   # Zod schemas shared between frontend forms and API validation
│   │   ├── src/
│   │   │   ├── user.ts
│   │   │   ├── invoice.ts
│   │   │   └── index.ts
│   │   ├── tsconfig.json
│   │   └── package.json
│   │
│   ├── config-eslint/                # Shared ESLint config
│   │   ├── base.js
│   │   ├── next.js
│   │   ├── node.js
│   │   └── package.json
│   │
│   └── config-typescript/            # Shared TypeScript configs
│       ├── base.json
│       ├── nextjs.json
│       ├── node.json
│       └── package.json
│
├── turbo.json
├── pnpm-workspace.yaml
├── package.json                      # Root workspace config
├── .github/
│   └── workflows/
│       └── ci.yml
└── .gitignore
```

---

## Root package.json

```json
{
  "name": "acme-platform",
  "private": true,
  "packageManager": "pnpm@9.1.0",
  "scripts": {
    "build": "turbo build",
    "dev": "turbo dev",
    "lint": "turbo lint",
    "test": "turbo test",
    "typecheck": "turbo typecheck",
    "clean": "turbo clean && rm -rf node_modules"
  },
  "devDependencies": {
    "turbo": "^2.0.0"
  }
}
```

No application dependencies at the root. Only `turbo` is installed here. Everything else goes in the package that uses it.

---

## apps/web/package.json

```json
{
  "name": "@repo/web",
  "version": "0.0.0",
  "private": true,
  "scripts": {
    "build": "next build",
    "dev": "next dev --port 3000",
    "lint": "eslint . --max-warnings 0",
    "typecheck": "tsc --noEmit",
    "test": "vitest run",
    "clean": "rm -rf .next .turbo node_modules"
  },
  "dependencies": {
    "@repo/ui": "workspace:*",
    "@repo/shared-types": "workspace:*",
    "@repo/validation": "workspace:*",
    "next": "^14.2.0",
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    "zod": "^3.23.0"
  },
  "devDependencies": {
    "@repo/config-eslint": "workspace:*",
    "@repo/config-typescript": "workspace:*",
    "@types/react": "^18.3.0",
    "@types/react-dom": "^18.3.0",
    "tailwindcss": "^3.4.0",
    "typescript": "^5.4.0",
    "vitest": "^1.6.0"
  }
}
```

---

## apps/api/package.json

```json
{
  "name": "@repo/api",
  "version": "0.0.0",
  "private": true,
  "scripts": {
    "build": "tsc -p tsconfig.json",
    "dev": "tsx watch src/index.ts",
    "lint": "eslint . --max-warnings 0",
    "typecheck": "tsc --noEmit",
    "test": "vitest run",
    "clean": "rm -rf dist .turbo node_modules"
  },
  "dependencies": {
    "@repo/shared-types": "workspace:*",
    "@repo/validation": "workspace:*",
    "express": "^4.19.0",
    "zod": "^3.23.0"
  },
  "devDependencies": {
    "@repo/config-eslint": "workspace:*",
    "@repo/config-typescript": "workspace:*",
    "@types/express": "^4.17.0",
    "tsx": "^4.11.0",
    "typescript": "^5.4.0",
    "vitest": "^1.6.0"
  }
}
```

---

## packages/ui/package.json

```json
{
  "name": "@repo/ui",
  "version": "0.0.0",
  "private": true,
  "main": "./src/index.ts",
  "types": "./src/index.ts",
  "exports": {
    ".": {
      "types": "./src/index.ts",
      "default": "./src/index.ts"
    }
  },
  "scripts": {
    "lint": "eslint . --max-warnings 0",
    "typecheck": "tsc --noEmit",
    "test": "vitest run",
    "clean": "rm -rf .turbo node_modules"
  },
  "dependencies": {
    "react": "^18.3.0"
  },
  "devDependencies": {
    "@repo/config-eslint": "workspace:*",
    "@repo/config-typescript": "workspace:*",
    "@types/react": "^18.3.0",
    "typescript": "^5.4.0",
    "vitest": "^1.6.0"
  }
}
```

Note: `main` and `types` point to source TypeScript files, not compiled output. The consuming bundler (Next.js, tsx) compiles them. This avoids a separate build step for internal packages.

---

## packages/shared-types/package.json

```json
{
  "name": "@repo/shared-types",
  "version": "0.0.0",
  "private": true,
  "main": "./src/index.ts",
  "types": "./src/index.ts",
  "exports": {
    ".": {
      "types": "./src/index.ts",
      "default": "./src/index.ts"
    }
  },
  "scripts": {
    "typecheck": "tsc --noEmit",
    "clean": "rm -rf .turbo node_modules"
  },
  "devDependencies": {
    "@repo/config-typescript": "workspace:*",
    "typescript": "^5.4.0"
  }
}
```

---

## packages/validation/package.json

```json
{
  "name": "@repo/validation",
  "version": "0.0.0",
  "private": true,
  "main": "./src/index.ts",
  "types": "./src/index.ts",
  "exports": {
    ".": {
      "types": "./src/index.ts",
      "default": "./src/index.ts"
    }
  },
  "scripts": {
    "lint": "eslint . --max-warnings 0",
    "typecheck": "tsc --noEmit",
    "test": "vitest run",
    "clean": "rm -rf .turbo node_modules"
  },
  "dependencies": {
    "@repo/shared-types": "workspace:*",
    "zod": "^3.23.0"
  },
  "devDependencies": {
    "@repo/config-typescript": "workspace:*",
    "typescript": "^5.4.0",
    "vitest": "^1.6.0"
  }
}
```

---

## Cross-Package Imports

### Frontend importing shared UI

```typescript
// apps/web/src/app/page.tsx
import { Button } from "@repo/ui";
import type { User } from "@repo/shared-types";
import { userCreateSchema } from "@repo/validation";
```

### API importing shared validation

```typescript
// apps/api/src/routes/users.ts
import { Router } from "express";
import type { User } from "@repo/shared-types";
import { userCreateSchema } from "@repo/validation";

const router = Router();

router.post("/users", (req, res) => {
  const result = userCreateSchema.safeParse(req.body);
  if (!result.success) {
    return res.status(400).json({ errors: result.error.flatten() });
  }
  // ... create user
});
```

### Shared validation schema used by both

```typescript
// packages/validation/src/user.ts
import { z } from "zod";

export const userCreateSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  role: z.enum(["admin", "member", "viewer"]),
});

export type UserCreateInput = z.infer<typeof userCreateSchema>;
```

The same Zod schema validates the form on the frontend and the request body on the API. One definition, two consumers, zero drift.

---

## Next.js Config for Workspace Packages

```javascript
// apps/web/next.config.mjs
/** @type {import('next').NextConfig} */
const nextConfig = {
  transpilePackages: ["@repo/ui", "@repo/shared-types", "@repo/validation"],
};

export default nextConfig;
```

`transpilePackages` tells Next.js to compile workspace packages through its bundler instead of expecting pre-built output.

---

## CI Configuration (GitHub Actions)

```yaml
# .github/workflows/ci.yml
name: CI

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

env:
  TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
  TURBO_TEAM: ${{ vars.TURBO_TEAM }}

jobs:
  ci:
    name: Lint, Type Check, Test, Build
    runs-on: ubuntu-latest
    timeout-minutes: 15

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup pnpm
        uses: pnpm/action-setup@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: "pnpm"

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Lint
        run: pnpm lint

      - name: Type check
        run: pnpm typecheck

      - name: Test
        run: pnpm test

      - name: Build
        run: pnpm build
```

With Turborepo remote caching enabled (`TURBO_TOKEN` and `TURBO_TEAM`), subsequent CI runs only rebuild changed packages.

---

## Dependency Graph

```
@repo/web ──────┐
  ├── @repo/ui  │
  ├── @repo/shared-types
  └── @repo/validation ──┐
                         ├── @repo/shared-types
@repo/api ───────────────┘
  ├── @repo/shared-types
  └── @repo/validation
```

`@repo/shared-types` is a leaf node — it depends on nothing else. `@repo/validation` depends on `@repo/shared-types`. Both apps depend on `@repo/validation` and `@repo/shared-types`. The UI package is only used by the frontend.
