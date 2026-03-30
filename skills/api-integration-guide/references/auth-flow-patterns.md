# Authentication Flow Patterns

Step-by-step sequences for the four primary API authentication methods. Each flow includes the exact HTTP requests, token handling, and error recovery.

---

## 1. API Key

### Sequence

```
Client                                  API Server
  |                                        |
  |  GET /v1/users                         |
  |  Authorization: Bearer sk_live_abc123  |
  |  ------------------------------------> |
  |                                        |  Validate key
  |                                        |  Check scopes
  |  200 OK                                |
  |  <------------------------------------ |
```

### Setup

1. Obtain API key from the provider's dashboard or admin API
2. Store in environment variable (never in source code):
   ```
   API_KEY=sk_live_abc123
   ```
3. Include on every request in the `Authorization` header

### Request Format

```http
GET /v1/users HTTP/1.1
Host: api.example.com
Authorization: Bearer sk_live_abc123
Content-Type: application/json
```

Some APIs use a custom header instead:
```http
X-API-Key: sk_live_abc123
```

Check the API documentation for the expected header name.

### Error Recovery

| Response | Action |
|----------|--------|
| 401 | Key is invalid or revoked. Verify the key. Regenerate if needed. |
| 403 | Key lacks required scopes. Check permissions in the dashboard. |

### Key Rotation

1. Generate a new key in the dashboard
2. Update the environment variable with the new key
3. Deploy the change
4. Verify requests succeed with the new key
5. Revoke the old key

Some APIs support two active keys simultaneously to enable zero-downtime rotation.

---

## 2. OAuth 2.0 Authorization Code (with PKCE)

### Sequence

```
User        Client App              Auth Server           API Server
 |              |                        |                     |
 |  Click Login |                        |                     |
 |  ----------> |                        |                     |
 |              |  Generate:             |                     |
 |              |    code_verifier       |                     |
 |              |    code_challenge      |                     |
 |              |    state               |                     |
 |              |                        |                     |
 |  Redirect to Auth Server              |                     |
 |  <---------- |                        |                     |
 |              |                        |                     |
 |  GET /authorize                       |                     |
 |    ?response_type=code                |                     |
 |    &client_id=CLIENT_ID               |                     |
 |    &redirect_uri=CALLBACK             |                     |
 |    &scope=read+write                  |                     |
 |    &state=STATE                       |                     |
 |    &code_challenge=CHALLENGE          |                     |
 |    &code_challenge_method=S256        |                     |
 |  ---------------------------------->  |                     |
 |                                       |                     |
 |  Login + Consent Screen               |                     |
 |  <----------------------------------  |                     |
 |  Grant consent                        |                     |
 |  ---------------------------------->  |                     |
 |                                       |                     |
 |  Redirect to callback                 |                     |
 |    ?code=AUTH_CODE&state=STATE        |                     |
 |  <----------------------------------  |                     |
 |              |                        |                     |
 |  Follow redirect                      |                     |
 |  ----------> |                        |                     |
 |              |  Verify state matches  |                     |
 |              |                        |                     |
 |              |  POST /token           |                     |
 |              |  {                      |                     |
 |              |    grant_type: authorization_code             |
 |              |    code: AUTH_CODE      |                     |
 |              |    redirect_uri: CALLBACK                     |
 |              |    client_id: CLIENT_ID |                     |
 |              |    code_verifier: VERIFIER                    |
 |              |  }                      |                     |
 |              |  --------------------> |                     |
 |              |                        |                     |
 |              |  {                      |                     |
 |              |    access_token: "eyJ.." |                    |
 |              |    token_type: "Bearer" |                     |
 |              |    expires_in: 3600     |                     |
 |              |    refresh_token: "rt_x" |                    |
 |              |  }                      |                     |
 |              |  <-------------------- |                     |
 |              |                        |                     |
 |              |  GET /v1/users                                |
 |              |  Authorization: Bearer eyJ..                  |
 |              |  ------------------------------------------>  |
 |              |                                               |
 |              |  200 OK                                       |
 |              |  <------------------------------------------  |
```

### Token Refresh

Refresh proactively when `expires_in` minus a 60-second buffer is reached:

```http
POST /token HTTP/1.1
Content-Type: application/x-www-form-urlencoded

grant_type=refresh_token&
refresh_token=rt_abc123&
client_id=CLIENT_ID
```

Response returns a new `access_token` and optionally a new `refresh_token` (rotate both).

### Error Recovery

| Response | Action |
|----------|--------|
| Token exchange returns error | Restart the authorization flow from the beginning |
| 401 on API call | Attempt token refresh. If refresh fails, re-authorize the user. |
| Refresh token expired | Redirect user to login again |

---

## 3. OAuth 2.0 Client Credentials

### Sequence

```
Client (Backend)              Auth Server           API Server
  |                                |                     |
  |  POST /token                   |                     |
  |  {                             |                     |
  |    grant_type: client_credentials                     |
  |    client_id: CLIENT_ID        |                     |
  |    client_secret: CLIENT_SECRET|                     |
  |    scope: "read write"         |                     |
  |  }                             |                     |
  |  ----------------------------> |                     |
  |                                |                     |
  |  {                             |                     |
  |    access_token: "eyJ..."      |                     |
  |    token_type: "Bearer"        |                     |
  |    expires_in: 3600            |                     |
  |  }                             |                     |
  |  <---------------------------- |                     |
  |                                |                     |
  |  Cache token until:            |                     |
  |    expires_in - 60s buffer     |                     |
  |                                |                     |
  |  GET /v1/data                                        |
  |  Authorization: Bearer eyJ...                        |
  |  -------------------------------------------------> |
  |                                                      |
  |  200 OK                                              |
  |  <------------------------------------------------- |
```

### Token Caching Strategy

```
token_expiry = current_time + expires_in - 60  # 60-second safety buffer

before each API call:
  if current_time >= token_expiry:
    fetch new token from /token endpoint
    update cached token and expiry

  make API call with cached token
```

### Error Recovery

| Response | Action |
|----------|--------|
| Token request fails | Check client_id and client_secret. Verify they are not revoked. |
| 401 on API call | Token may have been revoked server-side. Fetch a new token and retry once. |

### Key Differences from Auth Code Flow

- No user interaction — purely machine-to-machine
- No refresh token — just fetch a new access token when the current one expires
- client_secret is used (only safe for backend services, never in browsers or mobile)

---

## 4. JWT (Pre-Signed)

### Sequence

For service-to-service auth where the client signs its own JWT using a private key:

```
Client Service                   API Server
  |                                   |
  |  Create JWT:                      |
  |    Header: { alg: RS256, kid: k1 }|
  |    Payload: {                     |
  |      iss: "client-service",       |
  |      sub: "client-service",       |
  |      aud: "api.example.com",      |
  |      exp: now + 300,              |
  |      iat: now,                    |
  |      jti: "unique-request-id"     |
  |    }                              |
  |  Sign with private key            |
  |                                   |
  |  GET /v1/data                     |
  |  Authorization: Bearer eyJ...     |
  |  -------------------------------> |
  |                                   |  Fetch public key from JWKS
  |                                   |  Verify signature
  |                                   |  Check exp, iss, aud
  |  200 OK                           |
  |  <------------------------------- |
```

### JWT Construction

```
Header (base64url):
{
  "alg": "RS256",
  "typ": "JWT",
  "kid": "key-2024-06"
}

Payload (base64url):
{
  "iss": "my-service",
  "sub": "my-service",
  "aud": "https://api.example.com",
  "exp": 1719878700,
  "iat": 1719878400,
  "jti": "req_unique_id_123"
}

Signature:
RS256(base64url(header) + "." + base64url(payload), private_key)
```

### Token Lifetime

- Generate a new JWT for each request, or cache for short periods (5 minutes max)
- Set `exp` to 5-15 minutes from `iat`
- Include `jti` (JWT ID) for replay protection

### Error Recovery

| Response | Action |
|----------|--------|
| 401 (signature invalid) | Verify the correct private key is being used. Check key rotation. |
| 401 (token expired) | Generate a new JWT. Check for clock drift between services. |
| 401 (audience mismatch) | Verify `aud` claim matches the API server's expected value. |

### Key Rotation

1. Generate a new key pair
2. Add the new public key to the JWKS endpoint
3. Start signing with the new private key (use the new `kid`)
4. After all outstanding tokens signed with the old key have expired, remove the old public key from JWKS
