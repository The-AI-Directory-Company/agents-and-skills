# ADR Quality Checklist

Run through these 9 checks before finalizing any Architecture Decision Record. Every item must pass.

## The Checklist

### 1. Title states the decision, not just the topic

- **Pass:** "Use PostgreSQL for Event Storage Instead of DynamoDB"
- **Fail:** "Event Storage" / "Database Decision" / "ADR about our data layer"

The title should let someone scanning an ADR index understand what was decided without opening the document.

### 2. Context explains the problem without jumping to the solution

- **Pass:** Describes the business driver, current limitations, and constraints before mentioning any options.
- **Fail:** Opens with "We decided to use X because..." or immediately describes the chosen option.

A reader should understand _why a decision was needed_ before learning what was decided.

### 3. At least 3 options are evaluated, including "do nothing"

- **Pass:** Three or more options, each with a substantive description.
- **Fail:** Only the chosen option is described. Or "do nothing" is mentioned but dismissed in one sentence.

"Do nothing" is a real option. Sometimes the cost of change exceeds the cost of the current pain. Make that evaluation explicit.

### 4. Each option includes pros, cons, and cost/effort estimate

- **Pass:** Every option has specific, evidence-based pros and cons, plus an effort estimate (time, people, or complexity).
- **Fail:** Pros/cons are vague ("more scalable," "harder to maintain") without specifics. Or effort is missing entirely.

Vague tradeoffs cannot be evaluated. "More scalable" means nothing without "handles 10x current load" or a benchmark.

### 5. Rationale explicitly explains why rejected options were not chosen

- **Pass:** For each rejected option, the ADR states the specific reason it was eliminated, tied back to the constraints.
- **Fail:** Only the chosen option is justified. Rejected options are listed but not discussed.

Future engineers need to know _why_ an option was rejected, not just that it was. If circumstances change, they can revisit the decision.

### 6. Consequences include both positive and negative outcomes

- **Pass:** Lists concrete benefits gained _and_ costs/limitations accepted.
- **Fail:** Only lists benefits ("this will improve performance and reduce costs") with no acknowledged downsides.

Every decision has tradeoffs. An ADR that lists only positives is either dishonest or incomplete.

### 7. Risks are identified with mitigation strategies

- **Pass:** Each risk has a description and a specific mitigation plan (monitoring, fallback, threshold for revisiting).
- **Fail:** "There are some risks" with no details. Or risks listed without mitigation.

A risk without a mitigation plan is just a worry. A risk with a plan is managed.

### 8. Follow-up actions have owners and deadlines

- **Pass:** Every action item names a specific person (not "the team") and a date.
- **Fail:** "We need to migrate the data" with no owner or timeline. Or actions assigned to "TBD."

An ADR that does not lead to action is just documentation theater.

### 9. Status is clearly marked

- **Pass:** One of: Proposed, Accepted, Deprecated, Superseded (with link to replacement ADR).
- **Fail:** No status field. Or "Draft" status that never gets updated.

Superseded ADRs must link to the new ADR. Never delete a superseded ADR -- its context and reasoning remain valuable.

## Quick-Scan Format

For embedding in PR templates or review checklists:

```
- [ ] Title states the decision, not the topic
- [ ] Context describes the problem before any solution
- [ ] 3+ options evaluated, including "do nothing"
- [ ] Each option has specific pros, cons, and effort estimate
- [ ] Rejected options have explicit reasons
- [ ] Consequences cover both positive and negative outcomes
- [ ] Risks have mitigation strategies
- [ ] Follow-up actions have owners and deadlines
- [ ] Status is set (proposed / accepted / deprecated / superseded)
```
