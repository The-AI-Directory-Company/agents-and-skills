# License Compatibility Matrix

Rules for combining open-source licenses in a single project. This reference covers the most common licenses, their compatibility with each other, and practical guidance for proprietary, open-source, and SaaS projects.

---

## License Categories

### Permissive Licenses

Allow use in proprietary software with minimal obligations (usually attribution only).

| License | SPDX ID | Obligations |
|---------|---------|-------------|
| MIT | MIT | Include copyright notice and license text |
| Apache 2.0 | Apache-2.0 | Include notice, state changes, patent grant |
| BSD 2-Clause | BSD-2-Clause | Include copyright notice |
| BSD 3-Clause | BSD-3-Clause | Include copyright notice, no endorsement clause |
| ISC | ISC | Include copyright notice |
| 0BSD | 0BSD | No obligations (public domain equivalent) |
| Unlicense | Unlicense | No obligations (public domain dedication) |

### Weak Copyleft Licenses

Require sharing modifications to the licensed library itself, but not the larger work that uses it.

| License | SPDX ID | Obligations |
|---------|---------|-------------|
| LGPL 2.1 | LGPL-2.1-only | Share modifications to the library; linking is OK |
| LGPL 3.0 | LGPL-3.0-only | Share modifications to the library; linking is OK |
| MPL 2.0 | MPL-2.0 | Share modifications to MPL-licensed files only |
| EPL 2.0 | EPL-2.0 | Share modifications; secondary license option |

### Strong Copyleft Licenses

Require the entire combined work to be released under the same license.

| License | SPDX ID | Obligations |
|---------|---------|-------------|
| GPL 2.0 | GPL-2.0-only | Entire combined work must be GPL 2.0 |
| GPL 3.0 | GPL-3.0-only | Entire combined work must be GPL 3.0 |
| AGPL 3.0 | AGPL-3.0-only | GPL 3.0 + network use triggers distribution |
| SSPL 1.0 | SSPL-1.0 | Service use triggers source release of entire stack |

### Non-Open-Source / Restricted

| License | Notes |
|---------|-------|
| BSL 1.1 (Business Source License) | Becomes open source after change date; production use restricted |
| Elastic License 2.0 | No managed service use |
| Commons Clause | Restricts selling the software |
| UNLICENSED / No license | All rights reserved — cannot be used legally |

---

## Compatibility Rules by Project Type

### Proprietary / Closed-Source Project

Your project is not distributed under an open-source license.

| Dependency license | Compatible? | Notes |
|-------------------|-------------|-------|
| MIT, BSD, ISC, Apache-2.0 | Yes | Include required notices in your NOTICES file |
| LGPL-2.1, LGPL-3.0 | Yes, with conditions | Must dynamically link (not statically bundle). Users must be able to replace the LGPL library. |
| MPL-2.0 | Yes, with conditions | Must keep MPL-licensed files in separate files. Modifications to those files must be shared. |
| GPL-2.0, GPL-3.0 | No | Your entire project would need to be GPL. Do not use. |
| AGPL-3.0 | No | Even server-side use triggers copyleft. Do not use. |
| SSPL-1.0 | No | Offering as a service triggers source release. Do not use. |
| UNLICENSED / No license | No | No rights granted. Do not use. |

### SaaS / Server-Side Application

Software runs on your servers, never distributed to users.

| Dependency license | Compatible? | Notes |
|-------------------|-------------|-------|
| MIT, BSD, ISC, Apache-2.0 | Yes | Standard attribution |
| LGPL-2.1, LGPL-3.0 | Yes | Dynamic linking requirement is moot (no distribution) |
| MPL-2.0 | Yes | Share modifications to MPL files if you distribute |
| GPL-2.0, GPL-3.0 | Yes (technically) | GPL is triggered by distribution. Server-side use without distribution does not trigger copyleft. However, many organizations ban GPL in SaaS as a policy decision due to legal ambiguity and the risk of accidental distribution. |
| AGPL-3.0 | No | Network interaction triggers copyleft. Your server code must be released under AGPL. |
| SSPL-1.0 | No | Service use triggers full stack source release. |

### Open-Source Project (MIT/Apache-2.0)

Your project is permissively licensed.

| Dependency license | Compatible? | Notes |
|-------------------|-------------|-------|
| MIT, BSD, ISC, Apache-2.0 | Yes | No conflict |
| Apache-2.0 + MIT | Yes | Apache-2.0 is compatible with MIT |
| LGPL-2.1, LGPL-3.0 | Yes | The LGPL library remains LGPL; your code stays permissive |
| MPL-2.0 | Yes | MPL files stay MPL; your code stays permissive |
| GPL-2.0, GPL-3.0 | Complicated | The combined work must be GPL. Your code can still be MIT, but anyone using the combined work must follow GPL. This effectively makes the distribution GPL. |
| AGPL-3.0 | Same as GPL | Combined work is AGPL |

### Open-Source Project (GPL-3.0)

Your project is GPL-licensed.

| Dependency license | Compatible? | Notes |
|-------------------|-------------|-------|
| MIT, BSD, ISC | Yes | Permissive licenses are GPL-compatible |
| Apache-2.0 | Yes (GPL-3.0 only) | Apache-2.0 is compatible with GPL-3.0 but NOT with GPL-2.0-only |
| LGPL-2.1, LGPL-3.0 | Yes | LGPL is a subset of GPL |
| MPL-2.0 | Yes | MPL 2.0 has a secondary license clause for GPL compatibility |
| GPL-2.0-only | Not with GPL-3.0 | GPL-2.0-only and GPL-3.0-only are incompatible. GPL-2.0-or-later is compatible. |
| AGPL-3.0 | Yes | AGPL is compatible with GPL-3.0 |

---

## Known Conflicts

### Apache-2.0 and GPL-2.0

Apache-2.0 contains patent retaliation and indemnification clauses that impose "additional restrictions" under GPL-2.0's terms. This means:
- Apache-2.0 code **cannot** be included in a GPL-2.0-only project
- Apache-2.0 code **can** be included in a GPL-3.0 project (the FSF explicitly resolved this in GPL-3.0)
- If the GPL code says "GPL-2.0-or-later", you can use it under GPL-3.0 and include Apache-2.0

### LGPL and Static Linking

LGPL requires users to be able to replace the LGPL library with a modified version. This is straightforward with dynamic linking (shared libraries) but problematic with:
- **Static linking** (Go binaries, Rust binaries) — the LGPL library is baked into the binary
- **Bundling** (webpack, esbuild) — JavaScript bundlers inline the library code
- **Tree-shaking** — extracting only used functions makes replacement impossible

For statically linked languages, using LGPL dependencies in proprietary projects is legally risky. Consult legal counsel or find an alternative.

### Dual-Licensed Packages

Some packages offer dual licenses (e.g., "MIT OR Apache-2.0"). You choose which license to accept. Pick the one most compatible with your project. In `package.json`, dual licenses appear as `(MIT OR Apache-2.0)`.

---

## Approved / Banned Patterns

### Recommended "Allow List" for Proprietary Projects

```
MIT
ISC
BSD-2-Clause
BSD-3-Clause
Apache-2.0
0BSD
Unlicense
CC0-1.0
BlueOak-1.0.0
```

### Conditional (Requires Review)

```
MPL-2.0         — OK if modifications to MPL files can be shared
LGPL-2.1        — OK if dynamically linked (not for Go/Rust/bundled JS)
LGPL-3.0        — Same as LGPL-2.1
CC-BY-4.0       — OK for content/docs, not code
```

### Banned for Proprietary Projects

```
GPL-2.0-only
GPL-3.0-only
AGPL-3.0-only
SSPL-1.0
EUPL-1.2
OSL-3.0
UNLICENSED       — No license means no rights
```

### Enforcement in CI

```bash
# npm — fail build on banned licenses
license-checker --failOn 'GPL-2.0;GPL-3.0;AGPL-3.0;SSPL-1.0;UNLICENSED'

# Python — fail on banned
pip-licenses --fail-on 'GNU General Public License v3 (GPLv3)'

# Rust — use deny.toml
# [licenses]
# deny = ["GPL-2.0", "GPL-3.0", "AGPL-3.0"]
cargo deny check licenses
```

---

## When in Doubt

1. **No license declared** = all rights reserved. You cannot use it. Contact the author or find an alternative.
2. **"Artistic License"** or **"Public Domain"** without a recognized identifier = ambiguous. Verify the actual license text.
3. **License changed between versions** = check the specific version in your lockfile, not the latest.
4. **This is not legal advice.** For high-stakes decisions (enterprise, IPO preparation, acquisition due diligence), consult an attorney who specializes in open-source licensing.
