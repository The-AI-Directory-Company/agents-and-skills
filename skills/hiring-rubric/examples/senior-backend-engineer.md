# Hiring Rubric: Senior Backend Engineer

## Role Profile

**Title:** Senior Backend Engineer (L5)
**Team:** Payments Platform, reporting to Engineering Manager
**Level:** Senior IC, no direct reports
**6-month goals:**
1. Own and ship the ledger reconciliation service (replacing a manual process costing 20 eng-hours/week)
2. Reduce P95 latency on payment processing endpoints from 800ms to under 200ms
3. Mentor one mid-level engineer through their first system design project

## Evaluation Dimensions

| Dimension                  | Weight | Assessed In              |
|----------------------------|--------|--------------------------|
| Backend systems depth      | 30%    | Technical interview      |
| System design              | 25%    | Design interview         |
| Debugging & problem-solving| 20%    | Technical interview      |
| Communication & clarity    | 15%    | All rounds               |
| Mentorship & collaboration | 10%    | Behavioral interview     |

## Scoring Criteria

### Backend Systems Depth (30%)

- **4 - Strong Hire:** Writes correct, production-quality code for the problem. Proactively identifies edge cases (race conditions, failure modes). Discusses tradeoffs of data structures and concurrency approaches without prompting.
- **3 - Hire:** Solves the problem with minor issues. Handles most edge cases when prompted. Explains their approach clearly.
- **2 - Weak:** Reaches a partial solution with hints. Misses concurrency or error-handling concerns. Struggles to compare alternatives.
- **1 - No Hire:** Cannot make meaningful progress. Shows gaps in fundamentals (SQL, HTTP, concurrency) expected at the senior level.

### System Design (25%)

- **4 - Strong Hire:** Structures the design top-down, identifies bottlenecks early, proposes monitoring and failure recovery strategies. Quantifies capacity estimates and names specific technologies with justified reasoning.
- **3 - Hire:** Produces a reasonable architecture covering key components. Addresses scalability when prompted. Makes sound technology choices.
- **2 - Weak:** Designs a working system but misses critical non-functional requirements (fault tolerance, observability). Needs significant guidance.
- **1 - No Hire:** Cannot decompose the problem into services or identify data flow. Design would not survive production traffic.

### Debugging & Problem-Solving (20%)

- **4 - Strong Hire:** Systematically isolates the bug, forms hypotheses, and validates them. Identifies the root cause and proposes a fix plus a preventive measure.
- **3 - Hire:** Finds the bug with a logical approach. May need one hint. Proposes a reasonable fix.
- **2 - Weak:** Uses trial-and-error. Finds the symptom but not the root cause.
- **1 - No Hire:** Cannot form a debugging strategy. Gets stuck without heavy guidance.

## Interview Questions

### Technical Round — Backend Depth
1. "Design and implement an idempotent payment processing endpoint that handles retries safely." Follow-up: "How would you test this under concurrent requests?"
2. "Given this slow SQL query on a 50M-row transactions table, walk me through how you'd diagnose and fix it." Follow-up: "What monitoring would you add to prevent this from recurring?"

### Design Round — System Design
1. "Design a ledger reconciliation system that compares internal records against bank statements daily, flagging discrepancies." Follow-up: "How does this system behave when the bank API is down for 6 hours?"

### Behavioral Round — Mentorship & Collaboration
1. "Tell me about a time you helped a less experienced engineer grow. What did you do, and what was the outcome?"
2. "Tell me about a time you disagreed with a technical decision on your team. How did you handle it, and what happened?"
3. "Tell me about a production incident where you had to coordinate across teams. What was your role, and what did you learn?"

## Scorecard

```
Candidate: _______________    Interviewer: _______________
Role: Senior Backend Eng     Date: _______________
Round: _______________

| Dimension                   | Score (1-4) | Evidence (required)            |
|-----------------------------|-------------|--------------------------------|
| Backend systems depth       |             |                                |
| System design               |             |                                |
| Debugging & problem-solving |             |                                |
| Communication & clarity     |             |                                |
| Mentorship & collaboration  |             |                                |

Overall recommendation:  [ ] Strong Hire  [ ] Hire  [ ] Weak  [ ] No Hire

Key strengths:
Key concerns:
```
