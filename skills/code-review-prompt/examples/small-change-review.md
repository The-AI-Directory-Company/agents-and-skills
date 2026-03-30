# Example: Small Change Review (28 lines)

Demonstrates the quick review prompt applied to a real-world small change: adding rate limiting to a login endpoint.

---

## The Filled-In Prompt

```
Review this code change.

## Context
- **What changed**: Added rate limiting to the POST /api/auth/login endpoint — max 5 attempts per IP per 15-minute window.
- **Why**: Credential stuffing attacks were hitting the login endpoint at ~200 req/s from rotating IPs (SEC-447).
- **What must NOT change**: Legitimate login attempts within the limit must succeed exactly as before. Existing session handling must not be affected.

## Review focus
1. Correctness — does the code do what the description says?
2. Safety — any security issues, null access, data integrity risks, or unhandled errors?
3. Edge cases — what inputs or conditions would break this?
4. Missing pieces — is there validation, error handling, or a test that should exist but does not?

## Output format
For each issue found, respond with:
- **Severity**: BLOCK (must fix) / WARN (should fix) / NOTE (optional)
- **Location**: file:line
- **What**: what is wrong
- **Why**: why it matters
- **Fix**: specific suggestion

If no issues are found, say "No issues found" — do not invent problems to appear thorough.

End with a one-line summary:
- "Approve" — no issues
- "Approve with notes" — only NOTE/WARN items, no blockers
- "Request changes" — BLOCK items exist, list them

## The diff

diff --git a/src/api/auth/login.ts b/src/api/auth/login.ts
index 4a2c3f1..8b7e2d9 100644
--- a/src/api/auth/login.ts
+++ b/src/api/auth/login.ts
@@ -1,6 +1,8 @@
 import { Router } from 'express';
 import { authenticateUser } from '../services/auth';
 import { validateLoginInput } from '../validators/auth';
+import { RateLimiter } from '../middleware/rateLimiter';
+
+const loginLimiter = new RateLimiter({ windowMs: 15 * 60 * 1000, max: 5 });

 const router = Router();

@@ -8,6 +10,14 @@ const router = Router();
 router.post('/login', validateLoginInput, async (req, res) => {
   const { email, password } = req.body;

+  const clientIp = req.headers['x-forwarded-for'] || req.socket.remoteAddress;
+  const isLimited = await loginLimiter.check(clientIp);
+
+  if (isLimited) {
+    return res.status(429).json({ error: 'Too many login attempts. Try again later.' });
+  }
+
   try {
     const { user, token } = await authenticateUser(email, password);
     res.json({ user, token });
@@ -15,6 +25,8 @@ router.post('/login', validateLoginInput, async (req, res) => {
     if (err.code === 'INVALID_CREDENTIALS') {
       return res.status(401).json({ error: 'Invalid email or password' });
     }
+
+    await loginLimiter.increment(clientIp);
     return res.status(500).json({ error: 'Internal server error' });
   }
 });
```

---

## The Review Output

**BLOCK** `src/api/auth/login.ts:27` — Rate limit increment is inside the generic error catch block, not after failed authentication.

**What**: `loginLimiter.increment(clientIp)` is called on line 27 inside the catch block, after the `INVALID_CREDENTIALS` check. This means the rate limiter only increments on unexpected server errors (500s), not on actual failed login attempts. A credential stuffing attack that triggers 401s will never hit the rate limit.

**Why**: The rate limiter provides no protection against the attack described in SEC-447. Attackers receiving 401s can make unlimited attempts.

**Fix**: Move `loginLimiter.increment(clientIp)` into the `INVALID_CREDENTIALS` branch (after the 401 response), or move it before the `try` block so every attempt counts. The typical pattern is to increment on every attempt and reset on success:

```typescript
const isLimited = await loginLimiter.check(clientIp);
if (isLimited) {
  return res.status(429).json({ error: 'Too many login attempts. Try again later.' });
}

await loginLimiter.increment(clientIp); // count every attempt

try {
  const { user, token } = await authenticateUser(email, password);
  await loginLimiter.reset(clientIp); // reset on successful login
  res.json({ user, token });
} catch (err) { ... }
```

---

**WARN** `src/api/auth/login.ts:13` — `x-forwarded-for` can contain multiple IPs and is spoofable.

**What**: `req.headers['x-forwarded-for']` may return a comma-separated list like `"203.0.113.1, 198.51.100.2"`. Using the full string as a rate limit key means the same client with different proxy chains gets different rate limit buckets. Additionally, if the app is not behind a trusted reverse proxy, clients can set this header to arbitrary values to bypass rate limiting.

**Why**: Attackers can rotate `X-Forwarded-For` values to get unlimited rate limit buckets.

**Fix**: Use `req.ip` (which Express resolves based on the `trust proxy` setting) or parse the first IP from the header. Ensure `trust proxy` is configured correctly for your deployment:

```typescript
// In app setup:
app.set('trust proxy', 1); // trust first proxy

// In route:
const clientIp = req.ip; // Express handles X-Forwarded-For parsing
```

---

**WARN** `src/api/auth/login.ts:14` — No error handling if `loginLimiter.check()` throws.

**What**: If the rate limiter's backing store (Redis, memory) is down, `loginLimiter.check(clientIp)` will throw an unhandled error, causing a 500 response. Users cannot log in when the rate limiter is unavailable.

**Why**: Rate limiting should be a safety net, not a single point of failure. If it is down, logins should still work (fail-open).

**Fix**: Wrap the rate limiter call in a try-catch that fails open:

```typescript
let isLimited = false;
try {
  isLimited = await loginLimiter.check(clientIp);
} catch (err) {
  logger.warn('Rate limiter unavailable, allowing request', { error: err.message });
}
```

---

**NOTE** `src/api/auth/login.ts:16` — Consider including `Retry-After` header in the 429 response.

**What**: The 429 response includes a JSON error message but no `Retry-After` header.

**Why**: Well-behaved clients (and some automated tools) use `Retry-After` to know when to retry. It is a standard practice for 429 responses and helps reduce unnecessary retry traffic.

**Fix**: Add `res.set('Retry-After', String(remainingSeconds))` where `remainingSeconds` is the time until the rate limit window resets.

---

**Summary**: Request changes — 1 BLOCK (rate limit increment in wrong location), 2 WARNs (IP parsing, error handling). The core rate limiting logic is sound, but the increment placement means it currently provides no protection against the attack it was designed to stop.
