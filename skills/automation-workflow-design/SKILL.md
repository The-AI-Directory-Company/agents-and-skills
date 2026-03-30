---
name: automation-workflow-design
description: Design and document automation workflows for n8n, Make, Zapier, and Power Automate. Covers trigger-action chain mapping, conditional branching, error handling, retry logic, and workflow diagrams with platform-specific node references.
metadata:
  displayName: "Automation Workflow Design"
  categories: ["engineering", "operations"]
  tags: ["automation", "workflow", "n8n", "make", "zapier", "power-automate", "integration", "no-code"]
  worksWellWithAgents: ["integration-engineer", "no-code-builder", "workflow-automator"]
  worksWellWithSkills: ["integration-specification", "runbook-writing"]
---

# Automation Workflow Design

## Before you start

Gather the following from the user:

1. **What is the trigger?** (Webhook, schedule, database event, form submission, file upload)
2. **What is the desired outcome?** (Record created, notification sent, file transformed, data synced)
3. **Which platform?** (n8n, Make, Zapier, Power Automate, or platform-agnostic)
4. **What systems are involved?** (APIs, databases, SaaS tools, file storage)
5. **What is the expected volume?** (Runs per hour/day, payload sizes)
6. **What happens on failure?** (Retry, alert, fallback, manual queue)

If the user says "automate this process," push back: "Which trigger starts it, what systems are involved, and what should happen when a step fails?"

## Workflow mapping procedure

### Step 1: Define the trigger

Identify the event that starts the workflow. Document:

- **Trigger type**: Webhook, polling, cron schedule, event subscription
- **Payload shape**: Fields available from the trigger (provide a sample JSON)
- **Frequency**: Expected invocations per time window
- **Idempotency**: Whether duplicate triggers are possible and how to handle them

### Step 2: Map the action chain

For each step after the trigger, document in sequence:

```
Step [N]: [Action name]
  Platform node: [Specific node/module name for the target platform]
  Input: [Which fields from previous steps]
  Transform: [Any data mapping or formatting]
  Output: [Fields produced for downstream steps]
  Error behavior: [Retry N times / skip / halt workflow]
```

Group related steps into logical stages: Intake, Processing, Output, Notification.

### Step 3: Add conditional branches

For each decision point:

- State the condition as a boolean expression using available fields
- Document the true-path and false-path step sequences
- Identify whether branches rejoin or terminate independently

### Step 4: Design error handling

For every step that calls an external service:

- **Retry strategy**: Count, backoff interval, max wait
- **Timeout**: Maximum seconds before treating as failure
- **Dead letter handling**: Where failed items go (error queue, log table, notification)
- **Circuit breaker**: If failure rate exceeds threshold, pause workflow and alert

### Step 5: Draw the workflow diagram

Produce a text-based diagram showing the flow:

```
[Trigger: New form submission]
  |
  v
[Validate payload] --invalid--> [Log error + notify]
  |valid
  v
[Enrich: Fetch customer from CRM]
  |
  v
[Branch: Is enterprise?]
  |yes                |no
  v                   v
[Create Jira ticket]  [Add to Mailchimp list]
  |                   |
  v                   v
[Notify #sales]       [Send welcome email]
```

Include error paths as dashed or labeled branches.

## Platform-specific notes

**n8n**: Use Error Trigger node for global error handling. Reference nodes by exact name (HTTP Request, IF, Switch, Merge). Use expressions with `{{ $json.field }}` syntax.

**Make (Integromat)**: Use error handler routes (Break, Resume, Ignore, Rollback). Reference modules by app name + action. Note the 15-minute default scenario timeout.

**Zapier**: Use Paths for conditional logic. Note that error handling requires Formatter + Filter workarounds or custom code steps. Multi-step zaps have a 30-second per-step timeout.

**Power Automate**: Use Scope actions for try-catch patterns. Configure run-after settings (succeeded, failed, skipped, timed out) on each action. Use `@outputs('step')['statusCode']` for error inspection.

## Workflow document template

```markdown
# Workflow: [Name]

## Overview
- **Trigger**: [Event description]
- **Platform**: [n8n / Make / Zapier / Power Automate]
- **Schedule**: [If applicable]
- **Owner**: [Team or person]

## Steps
| # | Action | Node/Module | Input | Output | Error Handling |
|---|--------|-------------|-------|--------|----------------|
| 1 | ...    | ...         | ...   | ...    | ...            |

## Branches
| Condition | True path | False path |
|-----------|-----------|------------|

## Error handling
- Global error handler: [Description]
- Dead letter destination: [Queue / table / channel]
- Alert channel: [Slack / email / PagerDuty]

## Volume & limits
- Expected runs: [N per hour/day]
- Rate limits: [Per-API limits to respect]
- Payload size limits: [If applicable]
```

## Quality checklist

Before delivering the workflow design, verify:

- [ ] Every step has explicit input fields, output fields, and error behavior
- [ ] Conditional branches document both paths and specify whether they rejoin
- [ ] Error handling covers retries, timeouts, dead letters, and alerting
- [ ] The workflow diagram matches the step table exactly
- [ ] Platform-specific node names and syntax are correct for the target platform
- [ ] Idempotency is addressed for the trigger and any create/update operations
- [ ] Volume estimates and rate limits are documented

## Common mistakes

- **No error handling on HTTP steps.** Every external call can fail. Skipping retry and timeout config means silent data loss in production.
- **Ignoring idempotency.** Webhooks can fire twice. Without deduplication (check by ID before create), you get duplicate records.
- **Hardcoding credentials in workflow steps.** Use the platform's credential store or environment variables. Never embed API keys in node configurations.
- **Linear-only thinking.** Real workflows branch. If you have zero conditional nodes, you probably have not considered validation failures or edge cases.
- **Missing the "what if the whole workflow fails" path.** Individual step retries are not enough. Design a global error handler that captures the workflow run ID, failed step, and payload for manual replay.
- **Not documenting rate limits.** A workflow that runs fine at 10/hour breaks at 1000/hour when a batch import triggers it. State the ceiling.
