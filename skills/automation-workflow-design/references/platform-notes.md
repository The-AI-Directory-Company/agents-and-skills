# Platform-Specific Notes

Detailed reference for node names, error handling patterns, timeout limits, and syntax for each supported automation platform.

---

## n8n

### Node Names (use exact names in workflow specs)

| Purpose | Node Name |
|---------|-----------|
| HTTP call | HTTP Request |
| Conditional logic | IF |
| Multi-branch conditional | Switch |
| Combine branches | Merge |
| Loop over items | Split In Batches |
| Code execution | Code (JavaScript or Python) |
| Wait/delay | Wait |
| Set variables | Set |
| Transform data | Item Lists |
| Webhook trigger | Webhook |
| Cron trigger | Schedule Trigger |
| Error handler | Error Trigger |
| Sub-workflow | Execute Workflow |
| Send email | Send Email |
| Database query | Postgres / MySQL / MongoDB (by name) |
| Spreadsheet | Google Sheets / Microsoft Excel |

### Error Handling

- **Global error handler:** Create a separate workflow with an Error Trigger node. It receives the failed workflow name, execution ID, error message, and the node that failed.
- **Per-node retry:** Configure on any node: retry count (1-3 recommended), wait between retries (in ms).
- **Continue on fail:** Toggle per node. When enabled, the node outputs `{ error: ... }` instead of halting. Use an IF node downstream to check `{{ $json.error }}`.
- **Error workflow:** Set in workflow settings > Error Workflow. Points to the global error handler workflow ID.

### Expression Syntax

```
{{ $json.fieldName }}              — access current item field
{{ $node["NodeName"].json.field }} — access output of a specific node
{{ $now.toISO() }}                 — current timestamp
{{ $execution.id }}                — current execution ID
{{ $workflow.name }}                — current workflow name
```

### Limits

| Limit | Value |
|-------|-------|
| Default execution timeout | None (configurable via `EXECUTIONS_TIMEOUT` env var) |
| Max payload size (webhook) | 16 MB default (configurable) |
| Max items per node output | No hard limit, but memory-bound |
| Concurrent executions | Configurable (default: unlimited in self-hosted) |

---

## Make (formerly Integromat)

### Module Naming Convention

Modules are referenced as **[App name] > [Action]**:

| Purpose | Module Reference |
|---------|-----------------|
| HTTP call | HTTP > Make a request |
| JSON parse | JSON > Parse JSON |
| JSON create | JSON > Create JSON |
| Conditional (router) | Flow Control > Router |
| Iterator (loop) | Flow Control > Iterator |
| Aggregator | Flow Control > Array aggregator |
| Sleep/delay | Tools > Sleep |
| Set variable | Tools > Set variable |
| Get variable | Tools > Get variable |
| Error handling | (route-level, see below) |
| Trigger: webhook | Webhooks > Custom webhook |
| Trigger: schedule | (scenario scheduling settings) |

### Error Handling

Make uses **error handler routes** attached to modules. Four handler types:

| Handler | Behavior |
|---------|----------|
| **Break** | Stops execution, rolls back (if using transactions), stores in incomplete executions queue |
| **Resume** | Provides a fallback output value and continues the scenario |
| **Ignore** | Swallows the error silently and continues (use sparingly) |
| **Rollback** | Stops execution and rolls back all transactions (requires data store or commit/rollback support) |

- Attach error handlers by right-clicking a module > Add error handler.
- Incomplete executions are stored for 15 days by default (viewable in scenario settings).
- Use a Router after error-prone modules to create explicit error/success paths.

### Limits

| Limit | Value |
|-------|-------|
| Scenario execution timeout | 15 minutes (default) |
| Maximum operations per execution | 100,000 (varies by plan) |
| Webhook payload size | 5 MB |
| File size for processing | 50 MB (varies by plan) |
| Minimum polling interval | 15 minutes (free), 1 minute (paid) |
| Concurrent scenario runs | 1 per scenario (sequential by default) |

---

## Zapier

### Action/Trigger Naming Convention

Zapier actions are referenced as **[App] > [Event]**:

| Purpose | Reference |
|---------|-----------|
| Conditional logic | Paths by Zapier > Path |
| Filter | Filter by Zapier > Only continue if... |
| Code execution | Code by Zapier > Run JavaScript / Run Python |
| Formatter | Formatter by Zapier > [Transform type] |
| Delay | Delay by Zapier > Delay For / Delay Until |
| Looping | Looping by Zapier > Loop |
| Webhook trigger | Webhooks by Zapier > Catch Hook |
| Webhook send | Webhooks by Zapier > POST / GET / PUT |
| Sub-zap | Sub-Zap by Zapier > Call a Sub-Zap |
| Storage | Storage by Zapier > Get Value / Set Value |

### Error Handling

Zapier has limited native error handling:

- **Auto-replay:** Failed tasks can be replayed from the task history (manual or automatic for certain errors).
- **Error notifications:** Zapier emails the account owner when a zap fails. Configure in zap settings.
- **Workaround for try-catch:** Use a Code step wrapped in try/catch. Output `{ success: true/false, error: "message" }`. Follow with a Filter or Path step to branch on the result.
- **No native global error handler.** Each step must handle its own errors or use the Code workaround.
- **Fallback values:** In Formatter steps, you can set default values for empty fields.

### Limits

| Limit | Value |
|-------|-------|
| Per-step execution timeout | 30 seconds |
| Code step timeout | 10 seconds (JavaScript), 10 seconds (Python) |
| Webhook payload size | 10 MB |
| Code step memory | 128 MB |
| Zap history retention | 7 days (free), 30-365 days (paid) |
| Polling trigger interval | 15 minutes (free), 1-2 minutes (paid) |
| Tasks per month | Plan-dependent (100 - unlimited) |

---

## Power Automate

### Action/Connector Naming Convention

Actions are referenced by their display name in the designer:

| Purpose | Action Name |
|---------|-------------|
| HTTP call | HTTP (premium connector) |
| Conditional logic | Condition |
| Switch | Switch |
| Loop (for each) | Apply to each |
| Loop (until) | Do until |
| Parallel branches | Parallel branch |
| Variable init | Initialize variable |
| Variable set | Set variable |
| Variable increment | Increment variable |
| Try-catch | Scope (see below) |
| Delay | Delay / Delay until |
| Compose (transform) | Compose |
| Parse JSON | Parse JSON |
| Trigger: manual | Manually trigger a flow |
| Trigger: recurrence | Recurrence |
| Trigger: HTTP | When a HTTP request is received |
| Terminate | Terminate (set status: Succeeded / Failed / Cancelled) |

### Error Handling

Power Automate uses **Scope actions** for try-catch patterns:

```
Scope: "Try"
  [Steps that might fail]

Scope: "Catch"
  Configure run after: runs only when "Try" scope has failed
  [Error handling steps]

Scope: "Finally" (optional)
  Configure run after: runs after "Try" has succeeded, failed, skipped, or timed out
  [Cleanup steps]
```

- **Run-after configuration:** Every action can be configured to run after the previous action has: Succeeded, Failed, Skipped, or Timed Out. This is the core mechanism for error branching.
- **Error inspection expressions:**
  - `@outputs('ActionName')['statusCode']` -- HTTP status code
  - `@actions('ActionName')['error']['message']` -- error message
  - `@result('ScopeName')` -- array of all action results within a scope
- **Terminate action:** Use to end the flow with a specific status (Succeeded / Failed / Cancelled) and a custom error message.

### Expression Syntax

```
@triggerOutputs()                    — trigger payload
@body('ActionName')                  — action response body
@outputs('ActionName')['headers']    — response headers
@variables('varName')                — variable value
@utcNow()                            — current UTC timestamp
@json(string)                        — parse string to JSON
@if(condition, trueVal, falseVal)    — inline conditional
```

### Limits

| Limit | Value |
|-------|-------|
| Flow run duration | 30 days (cloud), varies by license |
| Single action timeout | 120 seconds (default for HTTP) |
| Actions per flow | 500 |
| Nesting depth | 8 levels |
| Apply to each concurrency | 50 (default: 20) |
| HTTP request size | 100 MB |
| Trigger polling interval | 1 minute (minimum for most connectors) |
| Flow runs per 5 minutes | 100,000 (per user, non-premium) |
| API call rate | 6,000 per flow run (across all connectors) |
