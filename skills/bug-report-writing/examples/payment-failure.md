# [Checkout] Stripe payment fails silently when billing address contains accented characters

## Summary

Users with accented characters in their billing address (e.g., "Rue de la Paix, 3e etage") see a blank error state after clicking "Pay now." No charge is created, but the user receives no feedback explaining the failure. First reported on March 11, 2026. Affects approximately 14% of EU-based customers. Revenue impact estimated at $38K/week in abandoned checkouts.

## Reproduction Steps

1. Log in as any customer with a saved EU billing address, or create a new account.
2. Add any item to cart and proceed to `/checkout/payment`.
3. Enter valid test card `4242 4242 4242 4242`, expiry `12/27`, CVC `123`.
4. In the billing address field, enter: `Rue Francois-Gerard, Batiment C, 3eme etage`.
5. Click "Pay now."
6. Observe: the button spinner appears for ~2 seconds, then the page returns to the idle state. No success page, no error toast, no console error visible to the user.

Reproduction rate: 10/10 when address contains characters with diacritical marks (e, a, u, etc.). Works correctly with ASCII-only addresses.

## Expected vs Actual Behavior

```
Expected: Payment is processed successfully regardless of address characters. User sees the confirmation page.
Actual:   The Stripe API call returns a 400 error due to unescaped Unicode in the address payload. The frontend catches the error but renders nothing — the catch block calls `setLoading(false)` without setting an error message.
```

## Environment

- **App version**: v2.14.3 (commit `a8f2c1d`)
- **API environment**: Production (also reproducible on staging)
- **Browser**: Chrome 124, Firefox 125, Safari 17.4 (all affected)
- **OS**: macOS 14.4, Windows 11, iOS 17.4
- **Stripe SDK**: `@stripe/stripe-js` v3.1.0
- **Feature flags**: `new_checkout_flow=true` (enabled for 100% of users since March 8)

## Severity

**Critical** — Active revenue loss ($38K/week), no automated workaround, affects all EU customers with accented characters in their address. Users are not told the payment failed, so they assume the order went through and receive nothing.

## Screenshots / Logs

**Server log (sanitized)**:
```
2026-03-11T14:22:07Z ERROR stripe_client: PaymentIntent creation failed
  error_type: invalid_request_error
  message: "Invalid characters in billing_details.address.line1"
  customer_id: cus_***redacted***
  request_id: req_8fKz2mNpQx
```

**Frontend**: No error rendered. Network tab shows the `/api/create-payment-intent` endpoint returning HTTP 400, but the response body is swallowed by the catch block in `useCheckout.ts:87`.

## Root Cause Analysis

- **Root cause**: The `formatAddress()` utility in `lib/checkout/address.ts:42` passes raw Unicode to the Stripe API without normalizing. Stripe's API rejects certain combining characters in address fields. The frontend catch block at `useCheckout.ts:87` calls `setLoading(false)` but does not call `setError()`.
- **Fix**: Normalize address strings with `String.normalize('NFC')` before sending to Stripe. Add error state handling in the catch block to display the error toast with a retry prompt.
- **Prevention**: Add integration tests with non-ASCII address fixtures. Add a global error boundary for payment API calls that guarantees user-visible feedback on any failure.
