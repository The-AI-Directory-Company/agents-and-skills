# STRIDE Categories Reference

Complete reference for all six STRIDE threat categories with definitions, typical attack patterns, and detection controls.

---

## S -- Spoofing

### Definition

An attacker pretends to be someone or something they are not. Violates **authentication** -- the system cannot verify the claimed identity.

### Typical Attack Patterns

| Attack | Description | Example |
|--------|-------------|---------|
| Credential stuffing | Automated login attempts using leaked username/password pairs from other breaches | Attacker uses a list of 10M credentials against `/api/login` endpoint |
| Session hijacking | Stealing or guessing a valid session token to impersonate an authenticated user | Attacker captures session cookie via XSS and replays it |
| Token forgery | Creating or manipulating authentication tokens (JWT, API keys) | Attacker modifies JWT payload without proper signature verification |
| Phishing | Tricking users into submitting credentials to a fake login page | Clone of the real login page hosted on a lookalike domain |
| IP spoofing | Forging source IP to bypass IP-based access controls | Attacker sets `X-Forwarded-For` header to an internal IP |

### Detection Controls

| Control | Type | Description |
|---------|------|-------------|
| Multi-factor authentication | Preventive | Require second factor beyond password |
| Login anomaly detection | Detective | Alert on impossible travel, new device, or brute-force patterns |
| Session binding | Preventive | Bind sessions to fingerprint (IP + User-Agent), invalidate on mismatch |
| Certificate pinning | Preventive | Pin server certificates to prevent MITM impersonation |
| Rate limiting on auth endpoints | Preventive | Throttle login attempts per IP and per account |

---

## T -- Tampering

### Definition

An attacker modifies data, code, or configuration without authorization. Violates **integrity** -- the system cannot guarantee data has not been altered.

### Typical Attack Patterns

| Attack | Description | Example |
|--------|-------------|---------|
| Parameter manipulation | Modifying request parameters (query, body, headers) to alter behavior | Changing `price=9.99` to `price=0.01` in a checkout request |
| SQL injection | Injecting SQL through unsanitized input to modify queries | `'; DROP TABLE users; --` in a search field |
| Man-in-the-middle | Intercepting and modifying data in transit | Attacker on public WiFi alters API responses before they reach the client |
| File upload tampering | Uploading malicious files disguised as allowed types | Uploading a `.php` shell renamed to `.jpg` |
| Configuration tampering | Modifying environment variables, config files, or feature flags | Changing `ADMIN_ENABLED=true` via exposed config endpoint |

### Detection Controls

| Control | Type | Description |
|---------|------|-------------|
| Input validation + parameterized queries | Preventive | Reject unexpected input; never interpolate user data into queries |
| HTTPS everywhere + HSTS | Preventive | Encrypt all data in transit; prevent downgrade attacks |
| Digital signatures / HMAC | Detective | Sign payloads server-side; verify signatures on receipt |
| File type validation (magic bytes) | Preventive | Validate file content, not just extension |
| Immutable infrastructure | Preventive | Deploy from verified images; reject runtime configuration changes |

---

## R -- Repudiation

### Definition

An attacker performs an action and denies having done it, and the system cannot prove otherwise. Violates **non-repudiation** -- the system lacks evidence of who did what and when.

### Typical Attack Patterns

| Attack | Description | Example |
|--------|-------------|---------|
| Log tampering | Deleting or modifying log entries to erase evidence of an attack | Attacker with shell access clears `/var/log/auth.log` |
| Missing audit trail | Performing sensitive actions in systems with no logging | Admin deletes user data with no record of who initiated it |
| Shared credentials | Multiple users sharing an account, making attribution impossible | Team uses a single `admin@company.com` login for the dashboard |
| Timestamp manipulation | Altering timestamps to create false alibis or hide activity timing | Backdating a transaction to before a policy change |
| Anonymous actions | Performing state-changing actions without authentication | Unauthenticated API endpoint that accepts data modification requests |

### Detection Controls

| Control | Type | Description |
|---------|------|-------------|
| Append-only audit logs | Preventive | Write logs to immutable storage (write-once, no delete) |
| Centralized logging | Detective | Ship logs to a separate system the application cannot modify (SIEM) |
| Per-user authentication | Preventive | Eliminate shared accounts; every action traces to an individual |
| Signed log entries | Preventive | Cryptographically sign log entries to detect tampering |
| Mandatory action logging | Preventive | Log all state-changing operations with actor, timestamp, and payload |

---

## I -- Information Disclosure

### Definition

An attacker gains access to data they should not see. Violates **confidentiality** -- the system exposes information to unauthorized parties.

### Typical Attack Patterns

| Attack | Description | Example |
|--------|-------------|---------|
| Verbose error messages | Stack traces, SQL errors, or internal paths leaked to users | `500 Internal Server Error: relation "users" does not exist at /app/src/db.js:42` |
| Directory traversal | Accessing files outside the intended directory via path manipulation | `GET /api/files?path=../../../etc/passwd` |
| IDOR (Insecure Direct Object Reference) | Accessing other users' data by guessing or enumerating IDs | `GET /api/invoices/1002` returns another user's invoice |
| Exposed secrets | API keys, tokens, or credentials in client-side code or public repos | AWS key hardcoded in JavaScript bundle or committed to GitHub |
| Side-channel leaks | Timing differences, error messages, or response sizes that reveal hidden state | Login returns "user not found" vs. "wrong password" -- confirms account existence |

### Detection Controls

| Control | Type | Description |
|---------|------|-------------|
| Generic error responses | Preventive | Return consistent error format; log details server-side only |
| Authorization on every data access | Preventive | Verify the requesting user owns or has access to the requested resource |
| Secret scanning in CI | Detective | Scan commits for API keys, tokens, passwords before merge |
| Data classification + encryption at rest | Preventive | Encrypt sensitive data; restrict access by classification level |
| Response filtering | Preventive | Never return more fields than the client needs; use explicit allowlists |

---

## D -- Denial of Service

### Definition

An attacker makes the system unavailable to legitimate users. Violates **availability** -- the system cannot serve its intended purpose.

### Typical Attack Patterns

| Attack | Description | Example |
|--------|-------------|---------|
| Volumetric flood | Overwhelming the system with a high volume of requests | 100K req/s to the homepage from a botnet |
| Resource exhaustion | Triggering expensive operations that consume CPU, memory, or connections | Regex denial of service (ReDoS) via crafted input to a search field |
| Application-layer DoS | Targeting specific expensive endpoints | Repeated calls to `/api/export` that generate large reports |
| Connection exhaustion | Opening connections without closing them, exhausting the pool | Slowloris attack: send partial HTTP requests, hold connections open |
| Dependency DoS | Overloading a downstream service that the application depends on | Flooding a third-party API, causing it to rate-limit your production service |

### Detection Controls

| Control | Type | Description |
|---------|------|-------------|
| Rate limiting (per-IP and per-user) | Preventive | Cap request rates at gateway level |
| CDN / DDoS mitigation (Cloudflare, AWS Shield) | Preventive | Absorb volumetric attacks before they reach origin |
| Request size limits | Preventive | Cap payload size, query complexity, and pagination limits |
| Circuit breakers on dependencies | Preventive | Stop calling a failing dependency; fail fast instead of queuing |
| Auto-scaling with cost limits | Reactive | Scale up under load but set maximum to prevent bill shock |
| Timeouts on all operations | Preventive | Set request, query, and connection timeouts; never wait indefinitely |

---

## E -- Elevation of Privilege

### Definition

An attacker gains higher access than they are authorized for. Violates **authorization** -- the system grants permissions beyond what was intended.

### Typical Attack Patterns

| Attack | Description | Example |
|--------|-------------|---------|
| IDOR with write access | Modifying another user's data by changing the resource ID | `PUT /api/users/456/role` -- user 123 promotes user 456 to admin |
| Broken access control | Missing or incorrect permission checks on sensitive operations | Admin endpoint `/api/admin/users` accessible to any authenticated user |
| JWT claim manipulation | Modifying token claims (role, permissions) when signature is not verified | Changing `"role": "user"` to `"role": "admin"` in an unsigned JWT |
| SQL injection for privilege escalation | Using SQL injection to modify user roles or extract admin credentials | `'; UPDATE users SET role='admin' WHERE id=123; --` |
| Dependency vulnerability | Exploiting a known CVE in a library to gain code execution | Unpatched deserialization vulnerability allowing remote code execution |
| Container escape | Breaking out of a container to access the host system | Exploiting a kernel vulnerability from within a container with excessive privileges |

### Detection Controls

| Control | Type | Description |
|---------|------|-------------|
| Server-side authorization on every request | Preventive | Check permissions in middleware/interceptor; never trust client-side checks alone |
| Principle of least privilege | Preventive | Grant minimum permissions needed; default to deny |
| Role-based access control (RBAC) with tests | Preventive | Define roles explicitly; test that each role can only access its permitted resources |
| Dependency scanning (Dependabot, Snyk) | Detective | Detect known CVEs in dependencies before deployment |
| Container hardening | Preventive | Run as non-root, drop capabilities, use read-only filesystem, apply seccomp profiles |
| Anomaly detection on privilege changes | Detective | Alert when user roles change, especially self-promotion or bulk changes |
