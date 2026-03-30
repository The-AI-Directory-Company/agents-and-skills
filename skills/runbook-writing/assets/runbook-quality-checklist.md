# Runbook Quality Checklist

Standalone checklist for reviewing a runbook before publishing. Every item must pass. If any item fails, the runbook is not ready for on-call use.

---

## Structure

- [ ] **Single scenario.** The runbook covers exactly one failure mode. If it contains multiple "if X, do A; if Y, do B" branches for unrelated root causes, split into separate runbooks.
- [ ] **Purpose statement present.** States what this runbook fixes, when to use it, and includes the alert name or trigger condition verbatim (so engineers can search for it).
- [ ] **Last verified date.** Includes the date someone last executed or validated the procedure against the actual system.
- [ ] **Prerequisites listed.** Every tool, permission, VPN, SSH key, cloud console role, and dashboard URL needed before step 1 is documented.

## Commands and Steps

- [ ] **Every command is copy-pasteable.** No unmarked values that the engineer must replace. If a value is environment-specific, it uses the `<ALL_CAPS_WITH_BRACKETS>` placeholder format.
- [ ] **Placeholders have sources.** Every `<PLACEHOLDER>` states where to find the real value (e.g., "Find `<DB_HOST>` in the `checkout-service` ConfigMap: `kubectl get configmap checkout-service -n production -o jsonpath='{.data.DB_HOST}'`").
- [ ] **Expected output documented.** Every command includes what the engineer should see when the step succeeds.
- [ ] **Unexpected output handled.** Each step states what to do if the output differs from expected — a next step, an alternative action, or an escalation.

## Decision Branches

- [ ] **Explicit if/then routing.** Every decision branch states the condition, the action, and the next step number.
- [ ] **No dead ends.** Every branch leads somewhere — a step number, a different runbook, or an escalation path. No branch leaves the engineer without a next action.
- [ ] **Branches are mutually exclusive.** Conditions do not overlap. If they could, there is a "none of the above" path with an escalation.

## Verification

- [ ] **Verification steps present.** Defines how to confirm the issue is resolved after completing the procedure.
- [ ] **Specific thresholds.** Verification uses measurable criteria (e.g., "connection pool < 70% for 5 minutes"), not vague statements ("system looks normal").
- [ ] **Observation window defined.** States how long to watch after the fix before declaring success (e.g., "monitor for 10 minutes").

## Rollback

- [ ] **Rollback procedure present.** Describes how to undo the procedure if it makes things worse.
- [ ] **Rollback references step numbers.** "To undo step 4, run..." — not generic advice.
- [ ] **Irreversible steps flagged.** Any step that cannot be undone is marked as irreversible before the engineer executes it, with the safe alternative stated.

## Escalation

- [ ] **Escalation triggers defined.** States when to escalate: time thresholds, permission gaps, or out-of-scope root causes.
- [ ] **Specific contacts.** Names a team or role (not "engineering"), a PagerDuty policy, a Slack channel, or a phone bridge.
- [ ] **Fallback contact.** States what to do if the first contact does not respond within a defined time.

## Readability

- [ ] **Accessible to a generalist.** An on-call engineer unfamiliar with this service can follow the steps without asking questions. Abbreviations and service names are explained on first use.
- [ ] **No assumed context.** The runbook does not assume the reader has just read another runbook, attended a meeting, or "knows how this works."
- [ ] **Related runbooks linked.** Adjacent failure modes and downstream effects have cross-references so the engineer can pivot if this runbook does not match.
