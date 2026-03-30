# Workflow Quality Checklist

Run through these 7 checks before delivering any automation workflow design. Every item must pass.

---

## 1. Every step has explicit input fields, output fields, and error behavior

- [ ] Each step in the step table specifies which fields it receives from previous steps.
- [ ] Each step documents the fields it produces for downstream steps.
- [ ] Each step has an error handling strategy: retry count, skip, or halt.
- [ ] No step has "TBD" or blank cells in the input, output, or error columns.

**Why:** A step without defined inputs and outputs cannot be implemented. A step without error behavior will silently fail in production.

## 2. Conditional branches document both paths and specify rejoin

- [ ] Every branch states the condition as a boolean expression using available field names.
- [ ] Both the true-path and false-path are documented with their step sequences.
- [ ] Each branch explicitly states whether the paths rejoin downstream or terminate independently.
- [ ] Edge cases are covered: what happens when the condition field is null or unexpected?

**Why:** Undocumented false-paths are the top source of silent data loss. If a branch does not rejoin, that must be intentional, not accidental.

## 3. Error handling covers retries, timeouts, dead letters, and alerting

- [ ] A global error handler is defined (captures workflow name, execution ID, failed step, and payload).
- [ ] Per-step retry counts and backoff intervals are specified for every external call.
- [ ] Timeouts are set for every step that calls an external service.
- [ ] Failed items have a destination (dead letter queue, error table, or notification channel).
- [ ] An alerting mechanism is defined with a clear channel and threshold.

**Why:** Individual step retries without a global handler means some failures go unnoticed. Without dead letter handling, failed payloads are lost forever.

## 4. The workflow diagram matches the step table exactly

- [ ] Every step in the table appears in the diagram.
- [ ] Every branch in the table appears in the diagram.
- [ ] Error paths are shown in the diagram (labeled or dashed).
- [ ] The diagram does not include steps absent from the table (and vice versa).

**Why:** A diagram that does not match the step table creates confusion during implementation. One source of truth, two representations.

## 5. Platform-specific node names and syntax are correct

- [ ] Node/module names match the exact names used by the target platform (e.g., "HTTP Request" for n8n, "HTTP > Make a request" for Make).
- [ ] Expression syntax matches the platform (e.g., `{{ $json.field }}` for n8n, `@body('Action')` for Power Automate).
- [ ] Error handling patterns are platform-appropriate (Error Trigger for n8n, Break/Resume for Make, Scope run-after for Power Automate, Code try-catch for Zapier).
- [ ] Platform limits are respected (timeout ceilings, payload size limits, concurrent execution limits).

**Why:** Generic node names like "API Call" force the implementer to guess. Platform-specific names enable direct implementation without interpretation.

## 6. Idempotency is addressed for the trigger and all create/update operations

- [ ] The trigger documents whether duplicates are possible and how they are detected.
- [ ] Create operations check for existing records before inserting (dedup by ID or unique key).
- [ ] Update operations use conditional updates or last-modified checks to prevent overwrites.
- [ ] The workflow can be safely re-run on the same input without creating duplicate side effects.

**Why:** Webhooks fire twice, cron jobs overlap, and manual replays happen. Without idempotency, every re-trigger creates duplicate records or sends duplicate notifications.

## 7. Volume estimates and rate limits are documented

- [ ] Expected runs per hour/day are stated.
- [ ] Peak volume scenarios are identified (batch imports, seasonal spikes).
- [ ] Per-API rate limits are documented for every external service called.
- [ ] The workflow design respects those limits (throttling, batching, or queuing where needed).
- [ ] Estimated execution time per run is stated.

**Why:** A workflow that works at 10 runs/hour breaks at 1,000 runs/hour. Documenting the ceiling prevents production surprises.

---

## Quick-Scan Format

For embedding in review checklists or PR templates:

```
- [ ] Every step has input fields, output fields, and error behavior
- [ ] Branches document both paths and rejoin behavior
- [ ] Error handling: retries, timeouts, dead letters, alerting
- [ ] Diagram matches step table exactly
- [ ] Platform-specific node names and syntax are correct
- [ ] Idempotency addressed for trigger and create/update ops
- [ ] Volume estimates and rate limits documented
```
