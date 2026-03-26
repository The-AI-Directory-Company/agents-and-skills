---
name: runbook-writing
description: Write operational runbooks for the on-call engineer at 3am — step-by-step procedures with decision trees, escalation paths, and rollback instructions that assume no prior context.
metadata:
  displayName: "Runbook Writing"
  categories: ["operations", "engineering"]
  tags: ["runbooks", "operations", "on-call", "incident-response", "procedures"]
  worksWellWithAgents: ["devops-engineer", "incident-commander", "infrastructure-engineer", "release-manager", "sre-engineer", "support-engineer"]
  worksWellWithSkills: ["disaster-recovery-plan", "incident-postmortem", "release-checklist", "ticket-writing"]
---

# Runbook Writing

## Before you start

Gather the following from the user:

1. **What system or service does this cover?** (Service name, what it does, where it runs)
2. **What scenario triggers this runbook?** (Alert name, error condition, user-reported symptom)
3. **Who is the intended audience?** (On-call generalist, team-specific engineer, external vendor)
4. **What access or permissions are required?** (SSH keys, cloud console roles, VPN, database credentials)
5. **What is the blast radius if the procedure goes wrong?** (Data loss risk, downtime scope, affected users)

If the user says "just write a runbook for the payments service," push back: "Which failure mode? A runbook covers one specific scenario — database connection exhaustion is a different runbook than payment gateway timeouts."

## Runbook template

Use the following structure for every runbook:

### Purpose

One to two sentences stating what this runbook fixes and when to use it. Include the alert name or trigger condition verbatim so engineers can grep for it. Add a "last verified" date.

### Prerequisites

List every tool, permission, and access requirement. The on-call engineer should read this list and immediately know if they can execute the runbook or need to escalate. Example items: cloud console role, SSH/VPN access, specific dashboard URLs, PagerDuty escalation policy membership.

### Symptoms and Triggers

Describe observable signals — alert text, log patterns (exact searchable strings), dashboard anomalies, and user-reported behavior.

### Step-by-Step Procedure

Number every step. Each step must include:

- The exact command or UI action (copy-pasteable)
- Expected output so the engineer can confirm the step worked
- What to do if the output differs

Use decision branches with explicit if/then routing:

```
3. Check pg_stat_activity for connection state:
   $ psql -h <DB_HOST> -U readonly -c "SELECT state, count(*)
     FROM pg_stat_activity WHERE datname = 'checkout' GROUP BY state;"
   - IF active queries > 40: proceed to step 4 (kill long-running queries).
   - IF idle connections > 40: skip to step 5 (restart service).
   - IF neither: escalate — the connection pool issue is not database-side.
```

Every branch must lead somewhere — a next step number, a different runbook, or an escalation. Never leave the engineer at a dead end.

### Verification Steps

Define how the engineer confirms resolution. Include specific metric thresholds and observation windows:

```
- [ ] Connection pool utilization < 70% for 5 consecutive minutes
- [ ] No new 500 errors in service logs for 5 minutes
- [ ] Monitoring alert auto-resolves
```

### Rollback

Describe how to undo the procedure if it makes things worse. Reference steps by number. If a step is irreversible, say so explicitly and state the safe alternative.

### Escalation

Specify when to escalate (time thresholds, permission gaps, out-of-scope root causes), who to contact (specific team or role, not "engineering"), and how (PagerDuty policy name, Slack channel, phone bridge). Include a fallback if the first contact does not respond within a stated time.

### Related Runbooks

Link to runbooks covering adjacent failure modes or downstream effects so the engineer can pivot quickly if the symptoms do not match this scenario.

## Quality checklist

Before delivering the runbook, verify:

- [ ] Every command is copy-pasteable — no unmarked placeholder values
- [ ] Decision branches have explicit outcomes with next-step references for each path
- [ ] Prerequisites list every permission and tool needed before step 1
- [ ] Verification steps include specific thresholds and observation windows
- [ ] Escalation section names specific teams or roles with contact methods and time bounds
- [ ] The runbook covers exactly one failure scenario, not a general troubleshooting guide
- [ ] Someone unfamiliar with the service can follow the steps without asking questions

## Common mistakes to avoid

- **Writing for the expert, not the 3am responder.** "Check the HPA" means nothing to a generalist on-call. Write "Check the Horizontal Pod Autoscaler: `kubectl get hpa -n checkout`" instead.
- **Omitting expected output.** Every command needs the expected result. Without it, the engineer cannot tell if the step succeeded or if they are looking at a new problem.
- **Unmarked placeholders.** If a command contains values the engineer must replace, use `<ALL_CAPS_WITH_BRACKETS>` and state where to find the real value.
- **Combining multiple failure modes.** A runbook that says "if X, do A; if Y, do B; if Z, do C" is three runbooks. Split them and cross-link in Related Runbooks.
- **Missing rollback instructions.** If a step can make things worse, the engineer needs to know how to undo it. If it is irreversible, say so before they execute.
- **Stale commands.** Runbooks rot. Include a "last verified" date and flag commands that depend on specific tool versions.
