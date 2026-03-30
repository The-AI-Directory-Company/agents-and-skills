# Bloom's Taxonomy Verbs

Complete verb reference for writing measurable learning objectives. Use these verbs in the format: "By the end of [module], learners will be able to [verb] [specific outcome]."

---

## Level 1: Remember

Recall facts, terms, and basic concepts.

| Verbs |
|-------|
| cite, define, describe, enumerate, identify, label, list, match, name, outline, quote, recall, recognize, recite, reproduce, select, state, tabulate |

**When to use:** Foundation modules where learners need to know terminology, definitions, or facts before applying them.

**Example objectives:**
- List the five phases of the incident response lifecycle
- Define "eventual consistency" in the context of distributed systems
- Identify the HTTP status codes in the 4xx range and their meanings

---

## Level 2: Understand

Explain ideas or concepts in your own words.

| Verbs |
|-------|
| classify, compare, contrast, demonstrate, discuss, distinguish, estimate, exemplify, explain, extend, generalize, illustrate, infer, interpret, paraphrase, predict, restate, summarize, translate |

**When to use:** After foundational knowledge is established. Learners should be able to explain concepts to others, not just recite them.

**Example objectives:**
- Explain the difference between authentication and authorization
- Compare relational and document databases in terms of consistency guarantees
- Summarize the tradeoffs of monolithic vs. microservice architectures

---

## Level 3: Apply

Use knowledge in new situations.

| Verbs |
|-------|
| apply, calculate, carry out, complete, compute, configure, construct, demonstrate, deploy, execute, implement, install, modify, operate, perform, produce, resolve, run, schedule, solve, use, utilize |

**When to use:** Hands-on modules where learners practice using tools, writing code, or following procedures.

**Example objectives:**
- Configure a CI/CD pipeline that runs tests and deploys to staging on merge
- Implement a retry mechanism with exponential backoff for API calls
- Deploy a containerized application to a Kubernetes cluster using Helm charts

---

## Level 4: Analyze

Break information into parts and examine relationships.

| Verbs |
|-------|
| analyze, attribute, audit, benchmark, break down, categorize, compare, correlate, debug, deconstruct, detect, diagnose, differentiate, discriminate, dissect, distinguish, examine, experiment, inspect, integrate, investigate, map, organize, probe, question, separate, survey, test, trace |

**When to use:** Troubleshooting and investigation modules where learners must diagnose problems or evaluate system behavior.

**Example objectives:**
- Debug a CrashLoopBackOff by analyzing pod logs, events, and resource limits
- Analyze a slow database query using EXPLAIN output and identify optimization opportunities
- Differentiate between network latency, application latency, and database latency in a distributed trace

---

## Level 5: Evaluate

Make judgments based on criteria.

| Verbs |
|-------|
| appraise, argue, assess, challenge, choose, conclude, convince, critique, debate, decide, defend, determine, evaluate, grade, judge, justify, measure, monitor, persuade, prioritize, rank, rate, recommend, review, score, select, support, validate, verify, weigh |

**When to use:** Decision-making modules where learners must choose between approaches, evaluate tradeoffs, or defend recommendations.

**Example objectives:**
- Evaluate whether a workload should use synchronous or asynchronous processing based on latency and throughput requirements
- Recommend an appropriate caching strategy given the data consistency requirements and access patterns
- Assess the security posture of an API design and prioritize vulnerabilities by risk

---

## Level 6: Create

Produce new or original work.

| Verbs |
|-------|
| architect, assemble, author, build, combine, compose, construct, create, design, develop, devise, elaborate, formulate, generate, hypothesize, integrate, invent, model, originate, plan, produce, propose, prototype, rearrange, reconstruct, reorganize, revise, synthesize, write |

**When to use:** Capstone modules, projects, and assessments where learners synthesize everything learned into original work.

**Example objectives:**
- Design a multi-region disaster recovery architecture that meets a 15-minute RTO
- Architect a data pipeline that ingests, transforms, and serves real-time analytics for 10M events/day
- Create a technical proposal for migrating a monolithic application to microservices, including risk analysis and phased rollout plan

---

## Level Selection Guidance

| Module Position | Recommended Levels | Rationale |
|----------------|-------------------|-----------|
| Module 1 (Foundations) | Remember + Understand | Build vocabulary and mental models before hands-on work |
| Modules 2-3 (Core Skills) | Apply + Analyze | Practice doing the work and diagnosing problems |
| Module 4 (Advanced) | Analyze + Evaluate | Make decisions, evaluate tradeoffs, defend choices |
| Capstone / Final Assessment | Evaluate + Create | Synthesize all learning into original work |

### Progression Rule

Each module should target the same or higher Bloom's level as the previous module. Never regress — a Module 3 objective at the Remember level suggests the curriculum sequence is wrong.

---

## Vague Verb Anti-patterns

These verbs are common in poorly written objectives. They are not observable, not measurable, and produce objectives that cannot be assessed.

| Vague Verb | Problem | Replace With |
|-----------|---------|-------------|
| understand | Not observable — you cannot watch someone "understand" | explain, compare, distinguish, summarize |
| learn | Describes a process, not an outcome | [use the appropriate level verb for the actual outcome] |
| know | Not measurable — how do you test "knowing"? | define, identify, list, describe |
| be familiar with | No threshold for success — how familiar is enough? | identify, recognize, describe, explain |
| be aware of | Passive — awareness does not demonstrate competence | identify, describe, explain the implications of |
| appreciate | Subjective — cannot be assessed objectively | evaluate, justify, explain the importance of |
| gain exposure to | Describes an activity, not an outcome | [rewrite as what the learner can DO after the exposure] |
| explore | Activity, not outcome | investigate, compare, analyze |

### Test for Good Objectives

A well-written objective passes this test:

1. **Observable:** Can you watch the learner do it? (Write code, explain a concept, configure a system)
2. **Measurable:** Can you determine if they did it correctly? (Code runs, explanation is accurate, configuration works)
3. **Specific:** Does it describe a concrete outcome? ("Configure Kubernetes RBAC" not "understand security")
4. **Level-appropriate:** Does the verb match the expected cognitive level for this point in the curriculum?

If any answer is "no," rewrite the objective.
