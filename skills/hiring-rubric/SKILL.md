---
name: hiring-rubric
description: Build structured hiring rubrics — defining evaluation dimensions, behavioral interview questions, scoring criteria, and calibration processes that maximize signal and minimize bias.
metadata:
  displayName: "Hiring Rubric"
  categories: ["leadership", "business"]
  tags: ["hiring", "interviews", "rubrics", "recruiting", "evaluation"]
  worksWellWithAgents: ["career-coach", "technical-recruiter"]
  worksWellWithSkills: ["one-on-one-coaching", "stakeholder-interview"]
---

# Hiring Rubric

## Before you start

Gather the following from the user:

1. **What role are you hiring for?** (Title, level, team)
2. **What does success look like at 6 months?** (3-5 concrete outcomes the hire should achieve)
3. **What are the must-have vs nice-to-have skills?** (Technical and non-technical)
4. **How many interview rounds?** (Phone screen, technical, system design, behavioral, culture)
5. **Who is on the interview panel?** (Names and which dimensions they'll evaluate)

If the user says "we need a strong engineer," push back: "Strong at what? Backend systems? Cross-team collaboration? Debugging production issues? Define 3-4 specific capabilities that matter most for this role."

## Hiring rubric template

### 1. Role Profile

Write a concise profile that anchors the rubric to actual job needs, not a generic job description. Include: role title, team, level, reporting line, and 2-3 concrete 6-month goals the hire should achieve.

### 2. Evaluation Dimensions

Define 4-6 dimensions. Each dimension must be independent — avoid overlap. Assign a weight reflecting its importance to the role.

```
| Dimension              | Weight | Assessed In          |
|------------------------|--------|----------------------|
| Technical depth        | 30%    | Technical interview  |
| System design          | 25%    | Design interview     |
| Problem-solving        | 20%    | Technical interview  |
| Communication          | 15%    | All rounds           |
| Collaboration          | 10%    | Behavioral interview |
```

### 3. Scoring Criteria

For each dimension, define what a 1 through 4 looks like. Avoid vague language — describe observable behaviors.

```
Dimension: Technical Depth

4 - Strong Hire:  Solves the problem correctly with clean, production-quality
                  code. Identifies edge cases proactively. Discusses tradeoffs
                  of their approach without prompting.

3 - Hire:         Solves the problem with minor issues. Handles most edge
                  cases when prompted. Can articulate why they chose their
                  approach.

2 - Weak:         Reaches a partial solution with significant guidance.
                  Misses important edge cases. Struggles to compare
                  alternative approaches.

1 - No Hire:      Cannot make meaningful progress on the problem. Shows
                  gaps in fundamentals expected at this level.
```

Write a scoring rubric like this for every dimension. Use concrete behaviors, not personality traits.

### 4. Interview Questions

For each dimension, provide 2-3 questions with follow-ups. Behavioral questions must use the "Tell me about a time..." format to elicit past behavior, not hypotheticals.

For technical dimensions, use role-specific coding or debugging problems with follow-ups like "How would you test this in production?" For behavioral dimensions, use "Tell me about a time..." questions that elicit past behavior with follow-ups exploring outcomes and lessons learned.

### 5. Scorecard

Create a standardized scorecard every interviewer fills out within 24 hours of the interview.

```
Candidate: _______________    Interviewer: _______________
Role: _______________         Date: _______________
Round: _______________

| Dimension              | Score (1-4) | Evidence (required)           |
|------------------------|-------------|-------------------------------|
| Technical depth        |             |                               |
| System design          |             |                               |
| Problem-solving        |             |                               |
| Communication          |             |                               |
| Collaboration          |             |                               |

Overall recommendation:  [ ] Strong Hire  [ ] Hire  [ ] Weak  [ ] No Hire

Key strengths:
Key concerns:
```

The "Evidence" column is mandatory. A score without a specific observation is not valid.

### 6. Calibration Process

Before interviews begin, have all interviewers score the same mock interview independently, then compare. Align on what a "3" looks like for each dimension with a concrete example. During the process, interviewers submit scorecards before the debrief — the most junior interviewer presents first to prevent anchoring.

## Quality checklist

Before using the rubric, verify:

- [ ] Every dimension maps to a real job requirement, not a generic trait
- [ ] Scoring criteria describe observable behaviors at each level
- [ ] No two dimensions overlap significantly (test: could one score high on dimension A and low on dimension B?)
- [ ] Behavioral questions ask about past experiences, not hypothetical scenarios
- [ ] The scorecard requires written evidence for every score
- [ ] Weights total 100% and reflect actual role priorities
- [ ] The calibration process is documented and scheduled before interviews begin
- [ ] At least one dimension assesses collaboration or communication

## Common mistakes to avoid

- **Generic dimensions.** "Technical skills" is too broad. "Ability to design fault-tolerant distributed systems" is specific enough to evaluate. Tie every dimension to what the person will actually do in the role.
- **Hypothetical interview questions.** "What would you do if..." invites rehearsed answers. "Tell me about a time when..." surfaces real behavior. Always prefer behavioral questions for non-technical dimensions.
- **Missing the evidence requirement.** Without mandatory evidence, scorecards become gut-feel ratings. Require interviewers to write the specific moment or statement that justified their score.
- **Anchoring in debriefs.** If the hiring manager shares their opinion first, everyone adjusts toward it. Always have the most junior interviewer present first, and submit scores before the meeting.
- **Overweighting technical skills.** A brilliant engineer who can't communicate or collaborate will slow the team down. Ensure at least 20-25% of the weight covers non-technical dimensions.
