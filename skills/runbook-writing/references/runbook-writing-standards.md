# Runbook Writing Standards

Conventions and formatting rules for writing runbooks that work at 3am. These standards ensure consistency across all runbooks and make them reliable for on-call engineers.

---

## Decision Branch Syntax

Use a consistent format for every decision point in a runbook. The engineer must be able to scan the branch and immediately know which path to take.

### Standard Format

```
N. [Action description]:
   $ [command to run]

   Expected output: [what success looks like]

   - IF [condition A]: proceed to step N+1 ([brief description]).
   - IF [condition B]: skip to step M ([brief description]).
   - IF neither: escalate to [team] via [method] — [reason this is out of scope].
```

### Rules

1. **Every branch must lead somewhere.** A step number, a different runbook (linked), or an explicit escalation. Never leave the engineer hanging.
2. **Branches are mutually exclusive and exhaustive.** If conditions A and B do not cover all possibilities, add a catch-all branch (typically an escalation).
3. **Include the step description in the branch.** "Skip to step 7 (restart the service)" is better than "skip to step 7" because the engineer can confirm they are going to the right place without scrolling.
4. **Limit branches to 3 paths per step.** If a step has more than 3 branches, it is likely combining multiple failure modes — split into separate runbooks.

### Anti-patterns

| Bad | Why | Fix |
|-----|-----|-----|
| `IF the output looks wrong, investigate further` | "Looks wrong" is subjective; "investigate" has no steps | Specify the exact condition and next step |
| `IF high, go to step 5; IF low, go to step 5` | Both branches go to the same place — the branch is pointless | Remove the branch; proceed directly to step 5 |
| `IF something else happens...` | Vague catch-all with no action | Replace with: "IF neither condition matches: escalate to [team]" |

---

## Placeholder Formatting

Placeholders mark values the engineer must supply. Use a consistent format so placeholders are immediately visible and never accidentally executed as-is.

### Format

```
<ALL_CAPS_DESCRIPTION>
```

- Angle brackets + all caps + underscores between words
- Immediately after the placeholder, state where to find the real value

### Examples

```
$ psql -h <DB_HOST> -U <DB_USER> -d <DB_NAME>
  # <DB_HOST>: kubectl get configmap checkout-service -n production -o jsonpath='{.data.DB_HOST}'
  # <DB_USER>: "readonly" for investigation, "admin" for remediation (requires DBA approval)
  # <DB_NAME>: "checkout" for production, "checkout_staging" for staging
```

### Anti-patterns

| Bad | Why | Fix |
|-----|-----|-----|
| `psql -h db-host-here` | Looks like a real hostname; could be pasted as-is | Use `<DB_HOST>` |
| `psql -h $DB_HOST` | Looks like a shell variable; engineer may expect it to resolve | Use `<DB_HOST>` with a comment showing where to get the value |
| `psql -h <host>` | Too generic; which host? | Use `<CHECKOUT_DB_HOST>` — be specific about which host |

---

## "Last Verified" Discipline

Runbooks rot. Commands change, dashboards move, services get renamed. A "last verified" date tells the on-call engineer how much to trust the runbook.

### Required Fields

Every runbook must include at the top:

```
Last verified: YYYY-MM-DD
Verified by: [Name or team]
Verified against: [Environment — production, staging, etc.]
```

### Verification Cadence

| Runbook Type | Recommended Cadence |
|-------------|-------------------|
| Critical path (revenue, data integrity) | Monthly |
| Frequently triggered (weekly alerts) | Quarterly |
| Rare scenarios (disaster recovery) | Every 6 months or after any infrastructure change |

### What Verification Means

Verification is not reading the runbook. It is executing the procedure (or a dry-run equivalent) against the specified environment and confirming:

1. Every command runs without error
2. Expected output matches actual output
3. Placeholders resolve to real values using the documented methods
4. Tool versions and permissions are current
5. Escalation contacts are still valid

### Staleness Indicators

If a runbook has not been verified within its cadence window, mark it:

```
⚠️ STALE — Last verified: 2024-08-15 (exceeds quarterly cadence).
   Steps may reference outdated commands or systems. Verify before executing.
   If you find errors, update the runbook and reset the verification date.
```

---

## Command Documentation Standards

### Include Expected Output

Every command must show what the engineer should see. Without expected output, the engineer cannot distinguish "working correctly" from "broken in a new way."

```
3. Check active connections:
   $ psql -h <DB_HOST> -U readonly -c "SELECT count(*) FROM pg_stat_activity WHERE datname = 'checkout';"

   Expected output:
    count
   -------
       42
   (1 row)

   Normal range: 10-60 connections.
   - IF count > 80: connection exhaustion likely — proceed to step 4.
   - IF count < 5: the service may not be connecting at all — skip to step 7.
```

### Mark Dangerous Commands

If a command modifies state, drops data, or restarts a service, flag it before the command line:

```
5. Kill long-running queries (⚠️ DESTRUCTIVE — active transactions will be rolled back):
   $ psql -h <DB_HOST> -U admin -c "SELECT pg_terminate_backend(pid)
     FROM pg_stat_activity
     WHERE datname = 'checkout'
     AND state = 'active'
     AND query_start < now() - interval '5 minutes';"
```

### Separate Investigation from Remediation

Structure runbooks in two phases:

1. **Investigation steps** (read-only commands that gather information)
2. **Remediation steps** (commands that change system state)

This prevents the 3am engineer from accidentally executing a remediation command while still diagnosing. Label the transition clearly:

```
--- Steps 1-5: Investigation (read-only) ---
--- Steps 6-9: Remediation (modifies system state) ---
```

---

## Cross-Linking Conventions

When referencing another runbook, use this format:

```
See: [Runbook Name — Brief Description](relative/path/to/runbook.md)
```

Cross-link in three places:

1. **In decision branches** — when a branch leads to a different failure mode
2. **In the Related Runbooks section** — for adjacent scenarios
3. **In escalation paths** — when the escalation team has their own runbook for the next level of response
