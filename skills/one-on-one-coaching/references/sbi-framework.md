# SBI Framework: Deep Reference

The Situation-Behavior-Impact (SBI) framework is the core feedback delivery method used in 1:1 coaching conversations. This reference covers correct application, common misapplications, the SBIE extension, positive vs. corrective feedback, and cultural considerations.

## The Framework

```
Situation:  When and where — anchor the feedback to a specific moment
Behavior:   What the person did — observable actions only, never intent
Impact:     The effect on the team, project, outcome, or you
```

Each element must be concrete. If any element is vague, the feedback loses its power and becomes indistinguishable from an opinion.

---

## Correct Application

### Positive Feedback

```
Situation:  During Friday's architecture review
Behavior:   You presented three design options with a clear tradeoff matrix
            and recommended option B with a specific rationale tied to our
            latency SLA
Impact:     The team made a decision in 20 minutes instead of the usual
            60-minute debate. Two engineers told me afterward that it was
            the clearest design discussion we've had this quarter.
```

### Corrective Feedback

```
Situation:  In Monday's sprint planning
Behavior:   You committed to owning the search migration and the API
            refactor — both estimated at 8 points each — without raising
            the open dependency on the platform team
Impact:     The sprint plan now has 16 points of work assigned to you with
            an unresolved dependency. If the platform work slips, both
            items are at risk, and we won't know until mid-sprint.
```

---

## 7 Common Misapplications

### 1. Vague Situation

**Wrong:** "Lately..."
**Right:** "In yesterday's client demo at 2pm..."

"Lately" or "in general" removes the anchor. The recipient cannot recall the specific moment, so they cannot learn from it. Always name the meeting, date, or event.

### 2. Intent Instead of Behavior

**Wrong:** "You didn't care about the deadline."
**Right:** "You submitted the deliverable two days after the agreed date without flagging the delay in advance."

You cannot observe someone's intent. You can observe their actions. Attributing intent ("didn't care," "was trying to undermine") triggers defensiveness and derails the conversation.

### 3. Judgment Disguised as Behavior

**Wrong:** "You were unprofessional in the meeting."
**Right:** "You interrupted the client twice while they were explaining their requirements."

"Unprofessional" is a judgment, not a behavior. Replace adjectives with the specific actions that led to your judgment. The recipient may disagree with the judgment but cannot disagree with the observable action.

### 4. Impact on Feelings Only

**Wrong:** "It made me feel frustrated."
**Right:** "The client paused and did not finish their point. After the meeting, they emailed asking to reschedule the requirements discussion."

Your feelings are valid context, but impact is strongest when tied to business outcomes, team dynamics, or project results. If the only impact is "I felt frustrated," consider whether the feedback is about a real problem or a personal preference.

### 5. Stacking Multiple Behaviors

**Wrong:** "You were late to the meeting, you hadn't read the pre-read, and your section of the presentation was incomplete."
**Right:** Pick the single most important behavior and deliver feedback on that one. Address others in a separate conversation or at a later date.

Stacking overwhelms the recipient and dilutes each point. One well-delivered SBI is more effective than three rushed ones.

### 6. Using SBI for Patterns Without Specifics

**Wrong:** "You're always late to meetings." (No specific situation.)
**Right:** "In Tuesday's standup and Thursday's design review, you joined 10-15 minutes after the scheduled start." (Two specific, recent situations.)

Patterns are important to name, but each instance must be grounded in a specific situation. "Always" and "never" are red flags that you have skipped the Situation element.

### 7. Delivering SBI as a Monologue

**Wrong:** Manager delivers the SBI, then moves to the next topic.
**Right:** Manager delivers the SBI, then asks: "What's your perspective on this?" and listens.

SBI is the opening of a dialogue, not a verdict. The recipient may have context you lack. After delivering the impact, pause and ask for their view.

---

## SBIE: The Expectation Extension

SBIE adds a fourth element — **Expectation** — that makes corrective feedback actionable by specifying what you want to see going forward.

```
Situation:   In Monday's sprint planning
Behavior:    You committed to 16 points without raising the platform dependency
Impact:      The sprint plan has unresolved risk that we won't see until mid-sprint
Expectation: Going forward, when you see an unresolved dependency, flag it during
             planning — even if it means we take on less work. I'd rather adjust
             scope upfront than discover the problem at standup in Week 2.
```

### When to Use SBIE vs. SBI

| Scenario | Use |
|----------|-----|
| First time raising this behavior | SBI — ask for their perspective first, then co-create the expectation |
| Repeated behavior after previous SBI conversation | SBIE — the expectation was already discussed; restate it clearly |
| Positive feedback | SBI only — adding an expectation to positive feedback ("keep doing this") can feel patronizing |
| Performance conversation or formal review | SBIE — document the expectation for the record |

---

## Positive vs. Corrective Feedback

### Positive Feedback

- **Purpose:** Reinforce specific behaviors you want to see repeated.
- **Timing:** Deliver within 1-2 days of the situation. Delayed praise loses its connection to the behavior.
- **Frequency:** More often than corrective. A healthy ratio is roughly 3:1 to 5:1 (positive to corrective), but never fabricate praise — it must be genuine and specific.
- **Common mistake:** Generic praise ("Great job on the project") is not SBI. It does not tell the person what specifically to repeat.

**Good positive SBI:**
```
Situation:  During Thursday's incident
Behavior:   You wrote a clear summary in the incident channel every 15 minutes,
            including what you'd tried, what you were trying next, and what you
            needed from others
Impact:     The rest of the team could follow along without interrupting you,
            and the VP of Engineering told me he didn't need to escalate because
            the updates gave him confidence the response was on track
```

### Corrective Feedback

- **Purpose:** Change a specific behavior that is causing a negative impact.
- **Timing:** Deliver within 1 week of the situation. Waiting longer makes the feedback feel stale or like you were accumulating grievances.
- **Setting:** Always in private. Never deliver corrective SBI in a group setting, a public Slack channel, or a meeting with others present.
- **Follow-up:** Check in at the next 1:1: "After our conversation last time about [topic], how has it been going? Have you had a chance to try the approach we discussed?"

**Common mistake:** Sandwiching corrective feedback between two positives ("The feedback sandwich"). Most people see through it, and it trains them to brace for criticism whenever you start with a compliment. Deliver positive and corrective feedback as separate, genuine conversations.

---

## Cultural Considerations

SBI was developed in a Western, direct-communication context (Center for Creative Leadership, US). When using it across cultures, adapt the delivery while preserving the structure.

### Direct vs. Indirect Communication Cultures

In **high-context cultures** (e.g., Japan, Korea, many Middle Eastern and Latin American contexts), delivering corrective feedback directly — even with SBI structure — can feel confrontational or disrespectful, particularly if there is a seniority gap.

**Adaptations:**
- Frame the impact in terms of the team or shared goal, not the individual: "The team's plan now carries risk" rather than "Your commitment created risk."
- Use questions to surface the behavior rather than stating it: "I noticed the sprint plan has 16 points assigned to you — how are you thinking about the platform dependency?" This allows the person to identify the issue themselves.
- Provide feedback through a trusted intermediary (buddy, senior peer) if direct feedback from a manager would cause loss of face.

### Hierarchical Cultures

In cultures with strong hierarchical norms, a junior team member may not feel comfortable responding to "What's your perspective?" from a senior leader. They may agree with the feedback regardless of their actual view.

**Adaptations:**
- After delivering the SBI, give the person time: "I'd like to hear your perspective. You don't need to respond now — let's revisit this at our next 1:1."
- Frame the expectation as a collaboration: "How can we set things up so this is easier next time?" rather than "Here's what I expect."
- Watch for nonverbal signals of disagreement (silence, hedging) and create a safe path to voice concerns later.

### Remote and Async Considerations

SBI delivered over text (Slack, email) loses tone and risks being read more harshly than intended.

**Adaptations:**
- Deliver corrective feedback synchronously (video call or in-person). Never over text.
- Positive feedback can be delivered asynchronously, but be specific — a Slack message with full SBI is better than a generic "nice work" in a thread.
- If the team is across time zones and synchronous is difficult, record a short video or voice message. Tone carries better than text.

---

## Quick Reference Card

```
PREPARING SBI:
  [ ] Can I name the specific date, meeting, or event? (Situation)
  [ ] Am I describing an action, not an intention or trait? (Behavior)
  [ ] Can I point to a team, project, or business consequence? (Impact)
  [ ] For corrective: Am I prepared to listen after delivering?
  [ ] For corrective: Am I delivering in private?

DELIVERING SBI:
  1. State the situation (anchor to time and place)
  2. Describe the behavior (observable, not interpreted)
  3. Explain the impact (on team, project, or outcome)
  4. Ask: "What's your perspective on this?"
  5. Listen. Do not defend or re-explain immediately.
  6. (If SBIE) State the expectation for next time
  7. Agree on next steps and write them down
```
