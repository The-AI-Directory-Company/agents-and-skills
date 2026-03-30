# Example: Blocker Resolution Conversation

A structured 1:1 focused on identifying, classifying, and resolving blockers — with an escalation commitment pattern for issues outside the direct report's control.

---

## Context

```
Direct report:  Senior Backend Engineer, 18 months tenure
Meeting type:   Blocker resolution (report flagged "stuck" in standup)
Key event:      Report has been blocked for 3 days on a cross-team dependency
```

## Conversation Flow

### Step 1: Surface the Blocker

**Manager:** "You mentioned being stuck on the payments integration. Walk me through what's blocking you — not the technical details yet, just what's preventing progress."

**Report:** "I need the Payments team to expose a new endpoint for refund status. I asked them last Wednesday and they said they'd get to it, but nothing's happened. I've followed up twice."

### Step 2: Classify the Blocker

Blockers fall into four categories. Classification determines who owns the resolution.

| Category | Signal | Resolution Owner |
|----------|--------|-----------------|
| **Technical** | "I don't know how to do X" or "The system won't let me do X" | Report (with support from tech lead or buddy) |
| **Process** | "The process requires X and it's taking too long" or "I need approval that's stuck" | Manager (streamline or override the process) |
| **People** | "I need something from another team/person and they haven't delivered" | Manager (escalate or broker the conversation) |
| **Clarity** | "I'm not sure what we actually want here" or "The requirements keep changing" | Manager + Report (align on scope together) |

**In this case:** This is a **People** blocker. The report has done the right thing (asked directly, followed up), but the other team has not prioritized the work. This is now the manager's responsibility to unblock.

**Manager:** "That sounds like a cross-team dependency issue — you've done your part by asking and following up. This is mine to resolve now. Let me make sure I have the details right before I act on it."

### Step 3: Gather Specifics

Before escalating, get the precise information needed to make a clear request:

**Manager:** "A few questions so I can be specific when I reach out:
- What exactly do you need from their API? (endpoint name, data shape, or a rough spec)
- What's the impact on your timeline if this stays blocked through next week?
- Is there a partial workaround — can you stub the endpoint and continue on other parts of the integration?"

**Report:** "I need a `GET /refunds/{id}/status` endpoint that returns the refund state and timestamp. If I'm blocked through next week, the payments milestone slips by at least a week, which pushes the release past the sprint commitment. I can stub it for local development, but I can't write integration tests or deploy to staging without the real endpoint."

### Step 4: Make an Escalation Commitment

The escalation commitment pattern has three parts: **what you will do, by when, and what happens next**.

**Manager:** "Here's what I'm going to do:
1. I'll message the Payments team lead today — within the next 2 hours — with the specific endpoint request and our timeline constraint.
2. I'll ask for either a delivery date this week or an explicit signal that it won't happen this sprint, so we can adjust our plan.
3. I'll update you by end of day tomorrow with whatever I hear back.

If they can't deliver this week, let's talk Thursday morning about whether we stub the endpoint for staging and defer integration tests, or whether we re-scope the sprint. Does that work?"

**Report:** "Yeah, that works. I'll keep building against the stub in the meantime."

### Step 5: Document the Commitment

Write this down during the meeting — not after.

```
Action items from 1:1 (2024-07-15):

1. [Manager] Message Payments team lead re: GET /refunds/{id}/status endpoint.
   Ask for delivery date or explicit no-go. Deadline: today by 3pm.

2. [Manager] Update report on Payments team response.
   Deadline: EOD tomorrow (2024-07-16).

3. [Report] Continue development against stubbed endpoint.
   Deadline: ongoing until real endpoint available.

4. [Both] If endpoint not available this week, meet Thursday AM to decide:
   re-scope sprint or proceed with stub for staging.
```

### Step 6: Follow Through

At the next 1:1, the manager opens with the blocker status — not a new topic:

**Manager:** "Before anything else — the Payments endpoint. I spoke with their lead on Monday. They're delivering it Wednesday. I'll confirm with you once it's in staging. Is there anything else that's come up since then?"

If the manager did not follow through, they own it explicitly:

**Manager:** "I owe you an update on the Payments endpoint — I didn't hear back yesterday and I haven't followed up yet. That's on me. I'm pinging them right now and I'll have an answer for you by 2pm today."

---

## Blocker Classification Quick Reference

Use this framework for any blocker that comes up in a 1:1:

```
1. SURFACE:   "What's preventing progress?"
2. CLASSIFY:  Technical / Process / People / Clarity
3. ASSIGN:    Technical & Clarity → report (with support)
              Process & People → manager
4. SPECIFY:   What exactly is needed? What's the timeline impact?
5. COMMIT:    What will I do, by when, and what's the next check-in?
6. DOCUMENT:  Write action items with owners and deadlines
7. FOLLOW UP: Open the next 1:1 with blocker status
```

## Anti-Patterns

- **"Let me know if it's still stuck next week."** This is not an escalation commitment — it is a deferral. If the blocker is the manager's to resolve, resolve it now.
- **Escalating without specifics.** Sending a vague "can you prioritize this?" to the other team gives them nothing to act on. Include the exact request, the timeline, and the business impact.
- **Taking the blocker but not updating.** If you commit to an action and go silent, the report assumes nothing happened. Update them even if the answer is "I'm still waiting."
- **Classifying everything as the report's problem.** If the report has asked for help twice and the other party has not responded, this is no longer a "just follow up again" situation. Escalation is the manager's job.
