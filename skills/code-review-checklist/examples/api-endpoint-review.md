# Code Review: POST /api/v2/workspaces/:id/invitations

**PR**: #1847 — Add workspace invitation endpoint
**Author**: @danielk
**Reviewer**: @sarahc
**Ticket**: TEAM-312 — Allow workspace admins to invite users by email
**Blast radius**: Workspace service, email service, user permissions

---

## First Pass: Intent

This PR adds an endpoint for workspace admins to invite new members by email. It creates an invitation record, sends an email via the notification service, and handles the case where the invitee already has an account. The endpoint should NOT modify existing member roles or allow duplicate invitations.

---

## Correctness

- [x] Logic matches the stated requirement
- [x] Edge cases handled: duplicate email, self-invitation, already-a-member
- [ ] **[Blocker]** Error path on line 47 returns `res.json({ error: "failed" })` with a 200 status code. The client cannot distinguish success from failure. Return `res.status(500).json({ error: "invitation_send_failed", message: "..." })`.
- [x] State mutations are atomic — invitation record and audit log are created in a transaction
- [ ] **[Major]** No check for the case where the workspace has reached its seat limit (plan allows 10 members). An admin on the free plan could send unlimited invitations. Add a seat count check before creating the invitation.

## Security

- [x] User input is validated — email format checked via zod schema
- [ ] **[Blocker]** Authorization check uses `req.user.workspaceId` from the JWT but does not verify it matches `:id` in the URL path. A user in workspace A can send invitations for workspace B by crafting the URL. Compare `req.user.workspaceId === req.params.id` or use the existing `requireWorkspaceMember` middleware.
- [x] No secrets hardcoded or logged
- [x] SQL uses parameterized queries via Prisma
- [ ] **[Major]** The invitation token is generated with `Math.random().toString(36)`. This is cryptographically weak and predictable. Use `crypto.randomBytes(32).toString('hex')` instead.
- [x] Rate limiting already applied via the global API rate limiter (50 req/min)

## Performance

- [x] Database queries use indexes — `invitations` table indexed on `(workspace_id, email)`
- [x] No N+1 queries — single insert operation
- [ ] **[Minor]** The endpoint queries `SELECT * FROM users WHERE email = ?` to check if the invitee exists. Only `id` and `email` are used. Select only needed columns to avoid transferring unnecessary data.
- [x] No unbounded data loading

## Maintainability

- [ ] **[Minor]** The function `handleInvite` is 94 lines. Extract email-sending logic into a separate `sendInvitationEmail` function — it is reused in the "resend invitation" endpoint on line 201.
- [x] Names describe intent — `createWorkspaceInvitation`, `checkExistingMember`
- [ ] **[Nit]** Magic string `"pending"` on line 62 — extract to a constant `INVITATION_STATUS.PENDING` alongside the existing `INVITATION_STATUS.ACCEPTED` on line 15.
- [x] Complex permission logic has comments explaining the business rules

## Testing

- [x] Happy path covered — admin creates invitation, record persists, email sent
- [ ] **[Major]** No test for the authorization bypass — add a test where user from workspace A attempts to create an invitation in workspace B and expects a 403.
- [ ] **[Minor]** No test for expired invitation re-send behavior. The ticket mentions invitations expire after 7 days, but no test verifies that re-sending resets the expiry.
- [x] Tests are deterministic — email service is mocked
- [x] Test names describe scenarios: `"returns 409 when email already invited"`

## Compatibility and Deployment

- [x] Database migration adds `invitations` table — backward compatible, no drops
- [x] Endpoint is versioned under `/api/v2/`
- [ ] **[Minor]** No feature flag. Since this touches permissions and email sending, consider gating behind `ENABLE_WORKSPACE_INVITATIONS` for the initial rollout.
- [x] Email template path is environment-configured

---

## Summary

**Verdict**: Request changes — 2 blockers must be fixed before merge.

| Severity | Count | Key Findings |
|----------|-------|-------------|
| Blocker | 2 | Auth bypass via URL path mismatch; error response returns 200 |
| Major | 3 | No seat limit check; weak token generation; missing auth test |
| Minor | 4 | Column over-selection; extract email function; magic string; missing feature flag |
| Nit | 1 | Extract status constant |
