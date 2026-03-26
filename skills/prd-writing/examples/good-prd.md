# Example: Auto-Reassignment PRD

> This is an example of a well-written PRD using the template.

## Auto-Reassignment — Product Requirements Document

### 1. Problem Statement

Enterprise customers with 50+ team members report spending 20+ minutes per week manually reassigning tickets when team members go on PTO, leading to SLA breaches in 12% of cases.

### 2. Goals & Success Metrics

| Metric | Baseline | Target | How to measure |
|--------|----------|--------|----------------|
| Time to reassign | 20 min/week | < 2 min/week | Activity logs |
| SLA breach rate | 12% | < 3% | Monthly SLA report |

### 3. User Stories

- As a team lead, I want tickets to be automatically reassigned when someone goes OOO so that SLAs aren't breached. (P0)
- As an engineer, I want to be notified when I receive reassigned tickets so that I can plan my work. (P1)

### 4. Scope

**In scope:** Calendar-based OOO detection, automatic reassignment, notifications.

**Out of scope:** Manual reassignment UI, workload balancing algorithm.
