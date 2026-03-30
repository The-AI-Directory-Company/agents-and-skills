# Demo Frameworks Reference

Three frameworks for structuring demos, handling objections, and running discovery. Use these as building blocks — adapt the structure to the audience and time slot.

---

## 1. Problem > Solution > Proof (Walkthrough Structure)

Every section of a product walkthrough should follow this sequence. It prevents the most common demo failure: showing features without context.

### Structure

```
Problem:   Restate a specific pain the prospect mentioned during discovery.
Solution:  Show — do not describe — the feature that addresses it. Click through a real workflow.
Proof:     Cite a specific customer result, data point, or third-party validation.
```

### Why This Order Matters

- **Problem first** because the audience needs to care before they pay attention. If you show a feature before establishing the pain, the audience thinks "so what?"
- **Solution second** because seeing the product in action is more persuasive than describing it. Click, do not talk.
- **Proof last** because third-party evidence anchors the claim. Your audience trusts a customer quote more than your sales pitch.

### Example

```
Problem:  "You mentioned your PMs wait 2-3 days for a data analyst to build
           retention charts. That delay means product decisions sit idle."

Solution: [Open retention explorer, type a natural language query, chart
           renders in 3 seconds, drill into a cohort, save as a template]

Proof:    "Pipe, the fintech payments company, cut their time-to-insight
           from 2 days to 15 minutes. Their PMs now self-serve 90% of
           retention questions."
```

### Rules

- Show 3 sections maximum in a 30-minute demo. Each section is 5-8 minutes.
- Use realistic data that matches the prospect's industry and scale. "Acme Corp" test data signals you did not prepare.
- Pause after each section: "Does this match how your team would use it?" This checks relevance and prevents wasting time on features they do not care about.
- If the audience leans in, spend more time. If they disengage, skip to the next section.

---

## 2. Acknowledge > Reframe > Evidence (Objection Handling Pattern)

Objections are not attacks. They are buying signals — the prospect is thinking about how this would actually work. Handle them with this three-step pattern.

### Structure

```
Acknowledge:  Validate the concern without being defensive.
              Show you heard them and the concern is reasonable.

Reframe:      Shift the frame from their stated concern to the
              underlying business question. Most objections are
              about something deeper than the words used.

Evidence:     Provide a specific data point, customer example,
              or verifiable fact. Generic reassurance does not work.
```

### Why This Order Matters

- **Acknowledge first** because dismissing a concern ("that's not really an issue") makes the prospect defensive. You lose trust.
- **Reframe second** because the stated objection is rarely the real issue. "Too expensive" usually means "I'm not sure the ROI justifies the price." Reframing to the real question lets you address what matters.
- **Evidence last** because claims without evidence are marketing. Evidence without acknowledgment is tone-deaf. The sequence matters.

### Common Objections and Patterns

**Price objection: "This is expensive compared to [competitor]."**
```
Acknowledge: "Pricing is an important part of the decision."
Reframe:     "The real comparison is total cost — implementation time,
              maintenance, and productivity impact over 12 months."
Evidence:    "Customer Y calculated TCO and found we were 30% less over
              12 months once they factored in 2 fewer FTEs maintaining
              their internal solution."
```

**Build-vs-buy objection: "We could build this internally."**
```
Acknowledge: "Your engineering team is clearly capable."
Reframe:     "The question is whether building [category] is the best use
              of their time versus shipping [core product feature]."
Evidence:    "Customer Z estimated 3 months to build. They're 18 months in
              and still maintaining it. Their CTO told us he wishes he'd
              bought earlier."
```

**Incumbent objection: "We're happy with [competitor]."**
```
Acknowledge: "[Competitor] is a solid product — makes sense you'd be
              cautious about switching."
Reframe:     "Teams that switch typically aren't unhappy overall — they
              hit a specific limitation. For your use case, the gap we
              see most is [specific differentiator]."
Evidence:    "I can connect you with [reference customer] who made the
              same switch. They can speak to what the transition looked
              like and what changed."
```

**Timing objection: "Not a priority right now."**
```
Acknowledge: "Totally understand — timing has to be right."
Reframe:     "What would change to make this a priority? Is it a budget
              cycle, a headcount change, or a specific pain getting worse?"
Evidence:    "The cost of waiting is [quantified impact per month]. I'll
              set a reminder to reconnect on [specific date tied to their
              trigger event]."
```

**Security/compliance objection: "We need to clear this with security."**
```
Acknowledge: "Security review is a standard part of the process — happy
              to support it."
Reframe:     "What specific areas does your security team focus on? We can
              front-load the documentation they'll need."
Evidence:    "Here's our SOC 2 Type II report, penetration test summary,
              and security architecture doc. I can also set up a call with
              our security engineering lead."
```

### Anti-Patterns

- **Do not argue.** "That's not true" or "actually, we are cheaper" puts the prospect on the defensive.
- **Do not over-acknowledge.** "That's a great question" repeated 5 times sounds scripted. One sentence of acknowledgment is enough.
- **Do not use generic evidence.** "Many customers love us" is not evidence. Name a customer, cite a number, offer a reference.

---

## 3. Discovery Question Taxonomy

Discovery questions fall into six categories. A good discovery call covers 3-4 categories in depth — not all six superficially. Prioritize based on what you already know and what stage the deal is in.

### Categories and Example Questions

#### Current State (What they do today)

- "Walk me through how your team handles [process] today, step by step."
- "What tools are involved? Who touches this workflow?"
- "How long has this process been in place?"
- "When was the last time you tried to change it?"

**Purpose:** Understand the status quo. You cannot position your product until you know what it replaces.

#### Pain (What breaks and what it costs)

- "What breaks first when volume increases?"
- "How much time does your team spend on this per week?"
- "When [problem] happens, what is the downstream impact?"
- "What is the cost of this problem — in time, revenue, or headcount?"
- "What happens if you do not solve this in the next 6 months?"

**Purpose:** Quantify the pain. If the customer cannot articulate the cost of the problem, the deal will stall. Help them quantify it.

#### Decision Process (How they buy)

- "Who else needs to be involved in evaluating this?"
- "What does your purchasing process look like for tools at this price point?"
- "Have you bought anything similar in the last year? What did that process look like?"
- "Is there a formal security or legal review?"
- "What is the typical timeline from 'we like it' to 'contract signed'?"

**Purpose:** Map the buying process so you do not get surprised. A verbal "yes" from a champion means nothing if procurement takes 90 days and you are forecasting it for this quarter.

#### Decision Criteria (What they evaluate on)

- "What would success look like in the first 30 days?"
- "What are the must-have requirements versus nice-to-haves?"
- "How will you compare options — is there a formal scorecard?"
- "Are there specific technical requirements (integrations, compliance, performance)?"

**Purpose:** Know what you are being graded on. If security is the top criterion and you lead with UX, you are demoing the wrong features.

#### Competition (What else they are considering)

- "Are you evaluating other solutions right now?"
- "Have you considered building this internally?"
- "What did you like and dislike about [competitor] when you looked at them?"
- "Is doing nothing — keeping the current process — a realistic option?"

**Purpose:** Know your competition so you can position against it. "Doing nothing" is the most common competitor and the hardest to beat.

#### Timeline and Urgency (Why now)

- "Is there a deadline or event driving this decision?"
- "Where does this rank against other priorities this quarter?"
- "What happens if this slips to next quarter?"
- "Is there budget allocated, or would this need approval?"

**Purpose:** Determine if there is real urgency. If there is no event, no deadline, and no quantified pain, this deal will not close on your timeline.

### Discovery Rules

1. **Ask open-ended questions.** "Walk me through..." and "Tell me about..." get richer answers than yes/no questions.
2. **Go deep on 3 categories, not shallow on 6.** A prospect who deeply articulates their pain and decision process is more qualified than one who gave surface-level answers to every category.
3. **Listen more than you talk.** If you are talking more than 30% of the time during discovery, you are pitching, not discovering.
4. **Write down their exact words.** Use their language in the demo — "you mentioned [their phrase]" is more persuasive than paraphrasing in your vocabulary.
5. **Do not demo during discovery.** If they ask to see the product, say "I want to make sure I show you the right things — let me ask two more questions and then we'll jump in."
