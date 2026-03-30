---
name: email-campaign-writing
description: Write email drip sequences including welcome series, re-engagement, nurture, and promotional campaigns with subject line testing variants and performance benchmarks.
metadata:
  displayName: "Email Campaign Writing"
  categories: ["business", "communication"]
  tags: ["email", "campaigns", "drip-sequences", "subject-lines", "nurture"]
  worksWellWithAgents: ["copywriter", "email-marketer", "growth-engineer", "marketing-strategist"]
  worksWellWithSkills: ["content-calendar", "go-to-market-plan", "product-launch-brief"]
---

# Email Campaign Writing

## Before you start

Gather the following from the user:

1. **Campaign type?** (Welcome series, re-engagement, nurture, promotional, onboarding, abandoned cart)
2. **Who is the audience?** (Segment definition — new signups, churned users, leads from specific channel)
3. **What action should the recipient take?** (Activate account, book a demo, upgrade, read content)
4. **How many emails in the sequence?** (Typical: welcome 3-5, nurture 5-8, re-engagement 3-4)
5. **What is the sending cadence?** (Daily, every 2 days, weekly)
6. **What data do you have for personalization?** (First name, company, plan type, last action)

If the user says "we need to send more emails," push back: "More emails without segmentation and a clear action per email just increases unsubscribes. What specific behavior should this sequence drive?"

## Email sequence architecture

Define the full sequence before writing any individual email.

```
Sequence: [Name]
Goal: [Primary conversion action]
Audience: [Segment definition]
Emails: [Count]
Cadence: [Timing between emails]
Exit condition: [When to stop — e.g., user converts, unsubscribes]

| #  | Send Timing   | Purpose           | Subject Line (A)          | CTA              |
|----|---------------|-------------------|---------------------------|------------------|
| 1  | Immediately   | Welcome + orient  | Welcome to [Product]      | Complete setup   |
| 2  | Day 2         | Quick win         | Try [feature] in 2 min    | Start tutorial   |
| 3  | Day 5         | Social proof      | How [Customer] uses [X]   | Read case study  |
| 4  | Day 8         | Value reminder    | You're missing [benefit]  | Activate feature |
| 5  | Day 14        | Nudge to convert  | Your trial ends in 3 days | Upgrade now      |
```

## Single email template

Every email follows this structure. Keep total length under 200 words for transactional, under 400 for nurture.

```
FROM: [Sender name] <[email]>
SUBJECT: [Subject line — 6-10 words, under 50 chars]
PREVIEW TEXT: [First 90 chars visible in inbox — complements subject, never repeats it]

---

[Opening line — 1 sentence, references the recipient's situation or last action]

[Body — 2-3 short paragraphs. One idea per email. No walls of text.]

[CTA — single, clear button or link. One CTA per email, not three.]

[Sign-off — human name, not "The Team"]
```

## Subject line testing

Write 3 variants per email. Test with at least 20% of the audience before full send.

```
| Variant | Subject Line                    | Strategy           |
|---------|--------------------------------|---------------------|
| A       | Welcome to [Product]           | Straightforward     |
| B       | Your [Product] account is ready | Action-oriented    |
| C       | [First name], let's get started | Personalized       |
```

Subject line rules:
- Under 50 characters (mobile truncation starts at 35-40)
- No ALL CAPS, no excessive punctuation (!!!), no spam trigger words ("free," "act now")
- Preview text must add information, not repeat the subject

## Sequence templates by type

### Welcome series (3-5 emails)
```
Email 1 (Day 0): Welcome + single setup action
Email 2 (Day 2): Quick win — show the fastest path to value
Email 3 (Day 5): Social proof — customer story or testimonial
Email 4 (Day 8): Feature highlight they haven't tried
Email 5 (Day 12): Summary of value + upgrade or next step CTA
```

### Re-engagement series (3-4 emails)
```
Email 1 (Day 0): "We noticed you've been away" + what's new
Email 2 (Day 4): Specific feature or content relevant to their past behavior
Email 3 (Day 10): Final value pitch + clear CTA
Email 4 (Day 20): Last chance — will reduce email frequency unless they re-engage
```

### Nurture series (5-8 emails)
```
Email 1: Educational content — solve a problem they have
Email 2: Framework or template — actionable resource
Email 3: Case study — someone like them succeeded
Email 4: Comparison — how your approach differs
Email 5: Objection handling — address common hesitations
Email 6-8: Rotate between education, proof, and soft CTA
```

## Performance benchmarks

Set expectations before launching. Compare results against these industry medians.

```
| Metric          | Good       | Average    | Concerning |
|-----------------|------------|------------|------------|
| Open rate       | >25%       | 18-25%     | <18%       |
| Click rate      | >3.5%      | 2-3.5%     | <2%        |
| Unsubscribe     | <0.3%      | 0.3-0.5%   | >0.5%      |
| Bounce rate     | <1%        | 1-3%       | >3%        |
```

## Quality checklist

Before sending any sequence, verify:

- [ ] Each email has exactly one CTA — not two, not zero
- [ ] Subject lines are under 50 characters with distinct preview text
- [ ] The sequence has an exit condition (stop sending when the user converts)
- [ ] Personalization tokens have fallback values (e.g., "there" if first name is missing)
- [ ] Unsubscribe link is present and functional in every email
- [ ] Emails are tested on mobile — most opens happen on phones
- [ ] At least 2 subject line variants exist for the first email

## Common mistakes

- **Multiple CTAs per email.** Every email should drive one action. "Read the blog, follow us on Twitter, and book a demo" means the reader does nothing.
- **No exit condition.** If someone already upgraded, stop sending the upgrade sequence. Map conversion events to sequence exits.
- **Preview text that repeats the subject.** "Welcome to Acme" as subject and "Welcome to Acme — we're glad you're here" as preview wastes the inbox real estate. Use preview text to add new information.
- **Sending to unsegmented lists.** A welcome email to someone who signed up yesterday is relevant. The same email to a 2-year customer is insulting. Segment first, write second.
- **Walls of text.** If an email takes more than 30 seconds to read, it's too long. One idea, short paragraphs, one CTA.
