# API Authentication Schemes

Flow descriptions, implementation patterns, and security gotchas for the four primary API auth mechanisms.

---

## 1. API Keys

### Flow

```
1. Developer registers and receives an API key (e.g., sk_live_abc123)
2. Client includes key in every request:
   Authorization: Bearer sk_live_abc123
3. Server validates key against the database and checks scopes/permissions
4. Server processes the request or returns 401/403
```

### Best For

- Server-to-server communication
- Internal microservices
- Simple integrations where the client is a backend service

### Implementation Notes

- Prefix keys to indicate environment: `sk_live_`, `sk_test_`
- Store hashed keys server-side (bcrypt or SHA-256 with salt) — never plaintext
- Support key rotation: allow two active keys simultaneously during rotation windows
- Scope keys to minimum required permissions (read-only, write, admin)

### Security Gotchas

- **Never accept keys in query strings.** URLs are logged in server access logs, browser history, proxy logs, and referrer headers.
- **Never embed keys in client-side code.** Browser source is public. Mobile apps can be decompiled.
- **Set expiration dates.** Keys without expiry accumulate risk. Default to 90-day rotation.
- **Rate limit per key.** A compromised key without rate limits enables unlimited data exfiltration.
- **Log key usage but never log the key itself.** Log the key prefix or a hash for audit trails.

---

## 2. OAuth 2.0 with PKCE (Authorization Code Flow)

### Flow

```
1. Client generates a random code_verifier (43-128 chars, URL-safe)
2. Client computes code_challenge = BASE64URL(SHA256(code_verifier))
3. Client redirects user to authorization server:
   GET /authorize?
     response_type=code&
     client_id=CLIENT_ID&
     redirect_uri=https://app.example.com/callback&
     scope=read+write&
     state=RANDOM_STATE&
     code_challenge=CHALLENGE&
     code_challenge_method=S256

4. User authenticates and consents
5. Authorization server redirects to callback with auth code:
   GET /callback?code=AUTH_CODE&state=RANDOM_STATE

6. Client verifies state matches what it sent
7. Client exchanges code for tokens:
   POST /token
   {
     "grant_type": "authorization_code",
     "code": "AUTH_CODE",
     "redirect_uri": "https://app.example.com/callback",
     "client_id": "CLIENT_ID",
     "code_verifier": "ORIGINAL_VERIFIER"
   }

8. Authorization server validates code_verifier against stored challenge
9. Authorization server returns:
   {
     "access_token": "eyJ...",
     "token_type": "Bearer",
     "expires_in": 3600,
     "refresh_token": "rt_abc123"
   }

10. Client uses access_token in Authorization header for API calls
11. Before expiry: client uses refresh_token to get a new access_token
```

### Best For

- Third-party integrations
- User-facing applications (SPAs, mobile apps, CLIs)
- Any scenario where the user grants scoped access to their data

### Implementation Notes

- PKCE is mandatory for public clients (SPAs, mobile, CLI) — it replaces the client_secret
- Store refresh tokens encrypted at rest
- Implement token rotation: each refresh returns a new refresh_token and invalidates the old one
- Set access token lifetime to 15-60 minutes; refresh token to 7-30 days
- Validate `state` parameter to prevent CSRF attacks

### Security Gotchas

- **Never use the Implicit flow.** It exposes tokens in URL fragments. Use Authorization Code + PKCE instead.
- **Validate redirect_uri exactly.** Partial matching (e.g., allowing subpaths) enables open redirect attacks.
- **Refresh token rotation is critical.** Without it, a stolen refresh token provides indefinite access.
- **Check token audience (`aud`) and issuer (`iss`).** A valid token from the wrong issuer is not valid for your API.
- **Revoke tokens on logout.** Clients should call the revocation endpoint, not just delete local copies.

---

## 3. JWT (JSON Web Tokens)

### Flow

```
1. Client authenticates (via login, OAuth, or API key exchange)
2. Server issues a signed JWT:
   Header:  { "alg": "RS256", "typ": "JWT", "kid": "key-2024-06" }
   Payload: {
     "sub": "user_42",
     "iss": "https://auth.example.com",
     "aud": "https://api.example.com",
     "exp": 1719882000,
     "iat": 1719878400,
     "scope": "read write"
   }
   Signature: RS256(header + payload, private_key)

3. Client includes JWT in every request:
   Authorization: Bearer eyJhbGciOi...

4. Server validates:
   a. Signature (using public key from JWKS endpoint)
   b. Expiration (exp > now)
   c. Issuer (iss matches expected)
   d. Audience (aud matches this API)
   e. Scopes match the requested operation

5. Server processes the request — no database lookup needed
```

### Best For

- Stateless auth between microservices
- Short-lived access tokens in OAuth flows
- Scenarios where reducing database lookups per request matters

### Implementation Notes

- Use asymmetric signing (RS256 or ES256) so services can verify without knowing the signing key
- Publish public keys at a JWKS endpoint (`/.well-known/jwks.json`) with key rotation via `kid`
- Keep payloads small — JWTs are sent on every request
- Never store sensitive data in the payload (it is base64-encoded, not encrypted)

### Security Gotchas

- **Never use `alg: none`.** Always validate the algorithm. Reject tokens with `alg: none` or unexpected algorithms.
- **Short expiration is essential.** JWTs cannot be revoked once issued. A stolen JWT with a 24-hour expiry is a 24-hour breach. Use 15-minute expiry with refresh tokens.
- **Do not put secrets in the payload.** JWTs are encoded, not encrypted. Anyone can decode the payload.
- **Validate `kid` (key ID) against your JWKS.** An attacker can craft a token with a forged `kid` pointing to their own key.
- **Clock skew tolerance.** Allow 30-60 seconds of clock skew when checking `exp` and `iat` — but no more.
- **JWTs grow with claims.** Each additional claim increases every request's size. Keep claims minimal.

---

## 4. Session Cookies

### Flow

```
1. Client submits credentials:
   POST /login
   { "email": "user@example.com", "password": "..." }

2. Server validates credentials
3. Server creates a session record (in Redis, database, etc.)
4. Server returns a Set-Cookie header:
   Set-Cookie: session_id=sess_abc123;
     HttpOnly;
     Secure;
     SameSite=Lax;
     Path=/;
     Max-Age=86400

5. Browser automatically includes the cookie on subsequent requests:
   Cookie: session_id=sess_abc123

6. Server looks up the session, validates it, and processes the request
7. On logout: server deletes the session record and clears the cookie
```

### Best For

- Traditional web applications with same-origin frontends
- Server-rendered apps (Next.js, Rails, Django)
- Scenarios where the client is always a browser

### Implementation Notes

- Session IDs must be cryptographically random (minimum 128 bits of entropy)
- Store sessions server-side (Redis for performance, database for durability)
- Set session expiry (absolute: 24 hours; idle: 30 minutes of inactivity)
- Regenerate session ID after login to prevent session fixation
- Support concurrent sessions with a "sign out all devices" option

### Security Gotchas

- **`HttpOnly` is mandatory.** Without it, JavaScript can read the cookie — enabling XSS-based session theft.
- **`Secure` is mandatory.** Without it, the cookie is sent over plaintext HTTP.
- **`SameSite=Lax` or `Strict`.** Without it, the cookie is sent on cross-origin requests — enabling CSRF.
- **CSRF tokens are still needed for state-changing requests** even with `SameSite=Lax` (Lax allows top-level navigations).
- **Never store session data in the cookie itself** (except with signed, encrypted cookie stores like Rails' encrypted cookies).
- **Session fixation:** Always regenerate the session ID after authentication state changes (login, privilege escalation).

---

## Comparison Matrix

| Factor | API Keys | OAuth 2.0 PKCE | JWT | Session Cookies |
|--------|----------|----------------|-----|-----------------|
| Stateless | No (DB lookup) | No (token storage) | Yes | No (session store) |
| User consent flow | No | Yes | No (delegated) | No |
| Token revocation | Immediate (delete key) | Immediate (revoke token) | Not possible until expiry | Immediate (delete session) |
| Best client type | Backend services | Any (web, mobile, CLI) | Microservices | Browsers only |
| Complexity | Low | High | Medium | Low |
| Credential rotation | Manual key rotation | Automatic via refresh | Key rotation via JWKS | Session regeneration |
