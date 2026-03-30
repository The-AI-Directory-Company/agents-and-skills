---
name: stakeholder-interview
description: Design and conduct stakeholder interviews for requirements elicitation — with structured question frameworks, active listening techniques, assumption surfacing, and synthesis into actionable requirements.
metadata:
  displayName: "Stakeholder Interview Guide"
  categories: ["business", "product-management"]
  tags: ["interviews", "requirements", "stakeholders", "elicitation", "discovery"]
  worksWellWithAgents: ["account-executive", "brand-manager", "business-analyst", "content-strategist", "customer-success-manager"]
  worksWellWithSkills: ["content-calendar", "hiring-rubric", "prd-writing", "sales-playbook", "user-story-mapping"]
---

# Stakeholder Interview Guide

## Before you start

Gather the following from the user:

1. **Who is the stakeholder?** (Name, role, department, decision-making authority)
2. **What is the project or initiative?** (Brief context on what you are eliciting requirements for)
3. **What do you already know?** (Existing documents, previous interviews, known constraints)
4. **What is the interview goal?** (Discovery, validation, priority alignment, or constraint mapping)

If the user says "I just need to ask some questions," push back: "What decision will this interview inform? Start there — it shapes every question you ask."

## Interview guide template

### 1. Preparation (before the interview)

1. Review all available documentation: project briefs, prior meeting notes, org charts, and existing requirements.
2. Identify the stakeholder's likely concerns based on their role — executives care about ROI and timelines, operators care about workflows and edge cases, end users care about pain points and usability.
3. Draft 8-12 questions using the core question types below. Sequence them from broad to specific.
4. Prepare a one-paragraph project summary to share at the opening — the stakeholder should not have to guess why they are there.
5. Write down your top 3 assumptions about this stakeholder's perspective. You will test these during the interview.

### 2. Opening (first 5 minutes)

1. Thank the stakeholder for their time. State the interview purpose in one sentence.
2. Share the one-paragraph project summary. Ask: "Does this match your understanding, or would you frame it differently?"
3. Set expectations: approximate duration, how their input will be used, and that there are no wrong answers.
4. Ask permission to take notes or record.

### 3. Core questions by type

Choose 2-3 types per interview based on your goal. Do not try to cover all four in a single session.

#### Problem discovery

- "What is the biggest challenge your team faces with [process/system] today?"
- "Walk me through what happens when [problem scenario] occurs."
- "If you could fix one thing about how this works today, what would it be and why?"

#### Process mapping

- "Describe your typical workflow from [trigger event] to [end state], step by step."
- "Where do handoffs happen? What information gets lost or delayed at those points?"
- "Which steps feel unnecessary or redundant to you?"

#### Constraint surfacing

- "What would make this project fail in your view?"
- "Are there regulatory, contractual, or policy constraints we need to respect?"
- "What resources — people, budget, systems — are non-negotiable versus flexible?"

#### Priority alignment

- "If we could only deliver three capabilities, which three matter most to you?"
- "How would you rank these needs: [list known requirements]? What's missing from this list?"
- "What would 'good enough for launch' look like versus 'ideal state'?"

### 4. Follow-up techniques

Use these during the interview to go deeper. Never settle for the first answer.

- **5 Whys**: When a stakeholder states a requirement, ask "Why is that important?" repeatedly (up to five times) until you reach the underlying need. Stop when the answer becomes a business outcome or user pain.
- **"Show me"**: Ask the stakeholder to demonstrate, sketch, or screen-share the current process. Observed behavior reveals requirements that verbal descriptions miss.
- **Silence**: After the stakeholder finishes an answer, wait 3-5 seconds before responding. People often add their most important point in the pause.
- **Playback**: Rephrase what you heard and ask "Did I get that right?" Misunderstandings caught mid-interview save weeks of rework.

### 5. Assumption surfacing

Before closing, explicitly test your pre-written assumptions:

1. State each assumption plainly: "Going in, I assumed that [X]. Is that accurate?"
2. Note whether the stakeholder confirms, corrects, or adds nuance.
3. Ask: "What assumption do you think the project team is making that might be wrong?"

This step catches misalignment early. Skipping it is the most common source of requirements gaps.

### 6. Closing (last 5 minutes)

1. Summarize the top 3-5 takeaways: "Here is what I heard as most important to you..." Read them back and ask for corrections.
2. Ask: "Is there anything we didn't cover that you expected to discuss?"
3. Confirm next steps: when they will see a summary, whether a follow-up session is needed, and who else you should talk to.
4. Thank them again. Send a written summary within 24 hours.

### 7. Post-interview synthesis template

Complete this within 24 hours while the conversation is fresh:

```
Stakeholder:    [Name, role]
Date:           [Interview date]
Interviewer:    [Your name]

Key requirements identified:
1. [Requirement] — Priority: [High/Medium/Low] — Source quote: "[verbatim]"
2. ...

Assumptions tested:
- [Assumption] → [Confirmed / Corrected / Nuanced] — Detail: [what changed]

Constraints uncovered:
- [Constraint] — Impact: [what it rules out or limits]

Conflicts with other stakeholders:
- [Stakeholder A wants X, Stakeholder B wants Y] — Resolution needed: [Yes/No]

Open questions for follow-up:
- [Question] — Assigned to: [person] — Due: [date]
```

## Quality checklist

Before marking the interview complete, verify:

- [ ] You prepared questions in advance — you did not wing it
- [ ] The stakeholder spoke at least 70% of the time
- [ ] You tested at least one assumption explicitly
- [ ] You captured direct quotes for critical requirements, not just paraphrases
- [ ] You identified at least one conflict or tension with other stakeholders' input
- [ ] The closing summary was confirmed by the stakeholder, not just assumed accurate
- [ ] A written synthesis was sent within 24 hours

## Common mistakes

- **Leading questions.** "Don't you think we should use a dashboard?" tells the stakeholder what you want to hear. Ask "How would you want to see this information?" instead.
- **Interviewing in groups when you need individual perspectives.** Group interviews produce consensus answers, not honest ones. Interview individually first, then validate in groups.
- **Treating requirements as final after one interview.** A single interview captures a snapshot. Requirements solidify across multiple conversations — plan for at least two rounds.
- **Skipping the assumption surfacing step.** Teams build on untested assumptions more often than on missing requirements. Make assumptions explicit or pay for them later.
- **Recording everything except decisions.** Transcripts are useful but overwhelming. Synthesize into the template above — what matters is actionable output, not raw notes.
- **Not asking "who else should I talk to?"** Every stakeholder knows someone you missed. This question is your best discovery tool for identifying hidden influencers.
