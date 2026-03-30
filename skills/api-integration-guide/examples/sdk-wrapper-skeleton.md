# SDK Wrapper Skeleton

Production-ready API client wrappers in Python and TypeScript. Each implements: constructor validation, automatic retry with exponential backoff, token refresh on 401, rate limit handling, and cursor-based pagination.

---

## Python

```python
"""
API Client Wrapper

Usage:
    client = APIClient(
        base_url="https://api.example.com/v1",
        api_key="sk_live_abc123",
        # Or for OAuth:
        # access_token="eyJ...",
        # refresh_token="rt_abc123",
        # token_refresh_url="https://auth.example.com/token",
        # client_id="CLIENT_ID",
    )

    # Single resource
    user = client.get("/users/42")

    # Paginate all results
    all_orders = client.paginate("/orders", params={"status": "active"})
"""

import time
import random
import logging
from typing import Any, Iterator
from urllib.parse import urljoin

import httpx  # pip install httpx

logger = logging.getLogger(__name__)


class APIError(Exception):
    """Raised for non-retryable API errors."""

    def __init__(self, status_code: int, code: str, message: str, request_id: str | None = None):
        self.status_code = status_code
        self.code = code
        self.message = message
        self.request_id = request_id
        super().__init__(f"[{status_code}] {code}: {message}")


class APIClient:
    def __init__(
        self,
        base_url: str,
        api_key: str | None = None,
        access_token: str | None = None,
        refresh_token: str | None = None,
        token_refresh_url: str | None = None,
        client_id: str | None = None,
        timeout: float = 30.0,
        max_retries: int = 3,
    ):
        if not base_url:
            raise ValueError("base_url is required")
        if not api_key and not access_token:
            raise ValueError("Either api_key or access_token is required")

        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_refresh_url = token_refresh_url
        self.client_id = client_id
        self.max_retries = max_retries

        self._client = httpx.Client(
            timeout=timeout,
            headers={"Content-Type": "application/json"},
        )

    # ── Auth ──────────────────────────────────────────────

    def _auth_header(self) -> dict[str, str]:
        token = self.api_key or self.access_token
        return {"Authorization": f"Bearer {token}"}

    def _refresh_access_token(self) -> bool:
        """Attempt to refresh the OAuth access token. Returns True on success."""
        if not self.refresh_token or not self.token_refresh_url:
            return False

        try:
            resp = self._client.post(
                self.token_refresh_url,
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": self.refresh_token,
                    "client_id": self.client_id,
                },
            )
            resp.raise_for_status()
            data = resp.json()
            self.access_token = data["access_token"]
            if "refresh_token" in data:
                self.refresh_token = data["refresh_token"]
            logger.info("Access token refreshed successfully")
            return True
        except Exception:
            logger.exception("Failed to refresh access token")
            return False

    # ── Core request with retry ───────────────────────────

    def _request(self, method: str, path: str, **kwargs) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        headers = {**self._auth_header(), **kwargs.pop("headers", {})}
        token_refreshed = False

        for attempt in range(self.max_retries + 1):
            try:
                resp = self._client.request(method, url, headers=headers, **kwargs)
            except httpx.TimeoutException:
                if attempt == self.max_retries:
                    raise
                self._backoff(attempt)
                continue
            except httpx.ConnectError:
                if attempt == self.max_retries:
                    raise
                self._backoff(attempt)
                continue

            # Success
            if resp.status_code in (200, 201, 202):
                return resp.json()
            if resp.status_code == 204:
                return {}

            # 401: try token refresh once
            if resp.status_code == 401 and not token_refreshed:
                if self._refresh_access_token():
                    headers.update(self._auth_header())
                    token_refreshed = True
                    continue

            # 429: respect Retry-After
            if resp.status_code == 429:
                retry_after = self._parse_retry_after(resp)
                if attempt < self.max_retries:
                    time.sleep(retry_after + random.uniform(0, 1))
                    continue

            # 5xx: retryable
            if resp.status_code >= 500:
                if attempt < self.max_retries:
                    self._backoff(attempt)
                    continue

            # Non-retryable error
            self._raise_api_error(resp)

        # Exhausted retries
        self._raise_api_error(resp)

    def _backoff(self, attempt: int) -> None:
        delay = min(1.0 * (2 ** attempt) + random.uniform(0, 1), 60.0)
        logger.info(f"Retry attempt {attempt + 1}, sleeping {delay:.1f}s")
        time.sleep(delay)

    def _parse_retry_after(self, resp: httpx.Response) -> float:
        header = resp.headers.get("Retry-After", "")
        try:
            return float(header)
        except ValueError:
            return 1.0

    def _raise_api_error(self, resp: httpx.Response) -> None:
        try:
            body = resp.json()
            error = body.get("error", {})
            raise APIError(
                status_code=resp.status_code,
                code=error.get("code", "UNKNOWN"),
                message=error.get("message", resp.text),
                request_id=error.get("request_id"),
            )
        except (ValueError, KeyError):
            raise APIError(
                status_code=resp.status_code,
                code="UNKNOWN",
                message=resp.text,
            )

    # ── Convenience methods ───────────────────────────────

    def get(self, path: str, params: dict | None = None) -> dict[str, Any]:
        return self._request("GET", path, params=params)

    def post(self, path: str, json: dict | None = None) -> dict[str, Any]:
        return self._request("POST", path, json=json)

    def put(self, path: str, json: dict | None = None) -> dict[str, Any]:
        return self._request("PUT", path, json=json)

    def patch(self, path: str, json: dict | None = None) -> dict[str, Any]:
        return self._request("PATCH", path, json=json)

    def delete(self, path: str) -> dict[str, Any]:
        return self._request("DELETE", path)

    # ── Pagination ────────────────────────────────────────

    def paginate(
        self,
        path: str,
        params: dict | None = None,
        limit: int = 100,
        max_pages: int = 1000,
    ) -> list[dict[str, Any]]:
        """Fetch all pages using cursor-based pagination. Returns a flat list."""
        return list(self.paginate_iter(path, params, limit, max_pages))

    def paginate_iter(
        self,
        path: str,
        params: dict | None = None,
        limit: int = 100,
        max_pages: int = 1000,
    ) -> Iterator[dict[str, Any]]:
        """Iterate through all pages using cursor-based pagination."""
        params = {**(params or {}), "limit": limit}
        cursor = None

        for page_num in range(max_pages):
            if cursor:
                params["cursor"] = cursor

            resp = self.get(path, params=params)
            items = resp.get("data", [])

            yield from items

            meta = resp.get("meta", {})
            cursor = meta.get("next_cursor")
            has_more = meta.get("has_more", False)

            if not cursor or not has_more or not items:
                break
        else:
            logger.warning(f"Reached max pages ({max_pages}) for {path}")

    # ── Cleanup ───────────────────────────────────────────

    def close(self):
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
```

---

## TypeScript

```typescript
/**
 * API Client Wrapper
 *
 * Usage:
 *   const client = new APIClient({
 *     baseUrl: "https://api.example.com/v1",
 *     apiKey: "sk_live_abc123",
 *   });
 *
 *   const user = await client.get("/users/42");
 *   const allOrders = await client.paginate("/orders", { status: "active" });
 */

interface APIClientConfig {
  baseUrl: string;
  apiKey?: string;
  accessToken?: string;
  refreshToken?: string;
  tokenRefreshUrl?: string;
  clientId?: string;
  timeout?: number;       // milliseconds, default 30000
  maxRetries?: number;    // default 3
}

interface APIErrorBody {
  code: string;
  message: string;
  request_id?: string;
  details?: Array<{ field?: string; reason: string }>;
}

class APIError extends Error {
  constructor(
    public statusCode: number,
    public code: string,
    public override message: string,
    public requestId?: string,
  ) {
    super(`[${statusCode}] ${code}: ${message}`);
    this.name = "APIError";
  }
}

class APIClient {
  private baseUrl: string;
  private apiKey?: string;
  private accessToken?: string;
  private refreshToken?: string;
  private tokenRefreshUrl?: string;
  private clientId?: string;
  private timeout: number;
  private maxRetries: number;

  constructor(config: APIClientConfig) {
    if (!config.baseUrl) throw new Error("baseUrl is required");
    if (!config.apiKey && !config.accessToken) {
      throw new Error("Either apiKey or accessToken is required");
    }

    this.baseUrl = config.baseUrl.replace(/\/+$/, "");
    this.apiKey = config.apiKey;
    this.accessToken = config.accessToken;
    this.refreshToken = config.refreshToken;
    this.tokenRefreshUrl = config.tokenRefreshUrl;
    this.clientId = config.clientId;
    this.timeout = config.timeout ?? 30_000;
    this.maxRetries = config.maxRetries ?? 3;
  }

  // ── Auth ──────────────────────────────────────────────

  private authHeaders(): Record<string, string> {
    const token = this.apiKey ?? this.accessToken;
    return { Authorization: `Bearer ${token}` };
  }

  private async refreshAccessToken(): Promise<boolean> {
    if (!this.refreshToken || !this.tokenRefreshUrl) return false;

    try {
      const resp = await fetch(this.tokenRefreshUrl, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({
          grant_type: "refresh_token",
          refresh_token: this.refreshToken,
          client_id: this.clientId ?? "",
        }),
      });

      if (!resp.ok) return false;

      const data = await resp.json();
      this.accessToken = data.access_token;
      if (data.refresh_token) this.refreshToken = data.refresh_token;
      return true;
    } catch {
      return false;
    }
  }

  // ── Core request with retry ───────────────────────────

  private async request<T = Record<string, unknown>>(
    method: string,
    path: string,
    options?: {
      params?: Record<string, string | number>;
      body?: Record<string, unknown>;
    },
  ): Promise<T> {
    let url = `${this.baseUrl}${path}`;
    if (options?.params) {
      const qs = new URLSearchParams(
        Object.entries(options.params).map(([k, v]) => [k, String(v)]),
      ).toString();
      url += `?${qs}`;
    }

    let tokenRefreshed = false;
    let lastResponse: Response | undefined;

    for (let attempt = 0; attempt <= this.maxRetries; attempt++) {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), this.timeout);

      try {
        const resp = await fetch(url, {
          method,
          headers: {
            "Content-Type": "application/json",
            ...this.authHeaders(),
          },
          body: options?.body ? JSON.stringify(options.body) : undefined,
          signal: controller.signal,
        });
        clearTimeout(timeoutId);
        lastResponse = resp;

        // Success
        if (resp.status === 204) return {} as T;
        if (resp.ok) return (await resp.json()) as T;

        // 401: try token refresh once
        if (resp.status === 401 && !tokenRefreshed) {
          if (await this.refreshAccessToken()) {
            tokenRefreshed = true;
            continue;
          }
        }

        // 429: respect Retry-After
        if (resp.status === 429 && attempt < this.maxRetries) {
          const retryAfter = parseFloat(resp.headers.get("Retry-After") ?? "1");
          await this.sleep((retryAfter + Math.random()) * 1000);
          continue;
        }

        // 5xx: retryable
        if (resp.status >= 500 && attempt < this.maxRetries) {
          await this.backoff(attempt);
          continue;
        }

        // Non-retryable error
        await this.throwAPIError(resp);
      } catch (err) {
        clearTimeout(timeoutId);
        if (err instanceof APIError) throw err;

        // Network or timeout error — retryable
        if (attempt < this.maxRetries) {
          await this.backoff(attempt);
          continue;
        }
        throw err;
      }
    }

    // Exhausted retries
    if (lastResponse) await this.throwAPIError(lastResponse);
    throw new Error("Request failed after all retries");
  }

  private async backoff(attempt: number): Promise<void> {
    const delay = Math.min(1000 * 2 ** attempt + Math.random() * 1000, 60_000);
    await this.sleep(delay);
  }

  private sleep(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  private async throwAPIError(resp: Response): Promise<never> {
    try {
      const body = await resp.json();
      const error = body.error ?? {};
      throw new APIError(
        resp.status,
        error.code ?? "UNKNOWN",
        error.message ?? resp.statusText,
        error.request_id,
      );
    } catch (err) {
      if (err instanceof APIError) throw err;
      throw new APIError(resp.status, "UNKNOWN", resp.statusText);
    }
  }

  // ── Convenience methods ───────────────────────────────

  async get<T = Record<string, unknown>>(
    path: string,
    params?: Record<string, string | number>,
  ): Promise<T> {
    return this.request<T>("GET", path, { params });
  }

  async post<T = Record<string, unknown>>(
    path: string,
    body?: Record<string, unknown>,
  ): Promise<T> {
    return this.request<T>("POST", path, { body });
  }

  async put<T = Record<string, unknown>>(
    path: string,
    body?: Record<string, unknown>,
  ): Promise<T> {
    return this.request<T>("PUT", path, { body });
  }

  async patch<T = Record<string, unknown>>(
    path: string,
    body?: Record<string, unknown>,
  ): Promise<T> {
    return this.request<T>("PATCH", path, { body });
  }

  async delete<T = Record<string, unknown>>(path: string): Promise<T> {
    return this.request<T>("DELETE", path);
  }

  // ── Pagination ────────────────────────────────────────

  async paginate<T = Record<string, unknown>>(
    path: string,
    params?: Record<string, string | number>,
    options?: { limit?: number; maxPages?: number },
  ): Promise<T[]> {
    const items: T[] = [];
    for await (const item of this.paginateIter<T>(path, params, options)) {
      items.push(item);
    }
    return items;
  }

  async *paginateIter<T = Record<string, unknown>>(
    path: string,
    params?: Record<string, string | number>,
    options?: { limit?: number; maxPages?: number },
  ): AsyncGenerator<T> {
    const limit = options?.limit ?? 100;
    const maxPages = options?.maxPages ?? 1000;
    let cursor: string | undefined;

    for (let page = 0; page < maxPages; page++) {
      const reqParams: Record<string, string | number> = {
        ...params,
        limit,
        ...(cursor ? { cursor } : {}),
      };

      const resp = await this.get<{
        data: T[];
        meta: { next_cursor?: string; has_more?: boolean };
      }>(path, reqParams);

      const items = resp.data ?? [];
      for (const item of items) {
        yield item;
      }

      cursor = resp.meta?.next_cursor;
      const hasMore = resp.meta?.has_more ?? false;

      if (!cursor || !hasMore || items.length === 0) break;
    }
  }
}

export { APIClient, APIError, type APIClientConfig };
```

---

## What Both Implementations Handle

| Concern | Implementation |
|---------|---------------|
| Constructor validation | Rejects missing base_url and credentials at initialization |
| Retry with backoff | `delay = min(base * 2^attempt + jitter, max)` for 5xx and network errors |
| Token refresh on 401 | Refreshes once, retries the original request with new token |
| Rate limit (429) | Reads `Retry-After` header, sleeps, retries |
| Pagination | Cursor-based with `has_more` / `next_cursor` stop conditions |
| Timeout | Configurable per-client timeout on all requests |
| Error classification | Raises structured `APIError` with status, code, message, request_id |
| Safety valve | `max_pages` limit prevents infinite pagination loops |
