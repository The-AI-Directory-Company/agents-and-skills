# CRM Migration — Stakeholder Interview: VP of Sales

## Preparation

**Stakeholder:** Dana Whitfield, VP of Sales, 14 direct reports, approves all sales tooling changes
**Project:** Migrate from Salesforce Classic to HubSpot CRM across a 120-person sales org
**Known context:** Contract with Salesforce expires in 5 months. CEO approved migration budget of $380K. Sales ops has documented 43 custom Salesforce workflows.
**Interview goal:** Discovery — understand Dana's team's daily CRM usage, pain points, and non-negotiable requirements.

**Assumptions to test:**
1. The sales team's biggest frustration is Salesforce's reporting speed.
2. Pipeline forecasting accuracy will be the highest-priority capability to preserve.
3. Dana will resist the migration due to re-training costs.

**Project summary for opening:** "We are migrating from Salesforce Classic to HubSpot over the next 4 months to reduce licensing costs and improve sales workflow efficiency. This interview is about understanding what your team needs from the new system so we don't break what's working."

## Questions (sequenced broad to specific)

### Problem discovery (primary)
1. "What are the top 3 things your reps complain about with Salesforce today?"
2. "Walk me through what happens when a rep needs to log a deal from first contact to closed-won."
3. "If you could fix one thing about how your team uses the CRM today, what would it be?"

### Process mapping
4. "Describe how your team runs the Monday pipeline review — what data do you pull, and from where?"
5. "Where do handoffs between SDRs and AEs happen? What information gets lost at that point?"

### Constraint surfacing
6. "What would make this migration a failure in your eyes?"
7. "Are there integrations — Gong, Outreach, CPQ — that are non-negotiable?"
8. "What is the maximum amount of downtime your team can absorb during cutover?"

### Priority alignment
9. "If we could only migrate three capabilities on day one, which three matter most?"
10. "What does 'good enough for launch' look like versus the ideal state?"

## Post-Interview Synthesis

```
Stakeholder:    Dana Whitfield, VP of Sales
Date:           2026-02-12
Interviewer:    Marcus Chen, Business Analyst

Key requirements identified:
1. Pipeline forecasting must match current accuracy within 5% — Priority: High
   Source quote: "If my Monday forecast breaks, I lose the CEO's trust in a week."
2. Gong and Outreach integrations required at launch — Priority: High
   Source quote: "Reps will revolt if call recording stops syncing to deal records."
3. Custom lead scoring model must be replicated — Priority: Medium
   Source quote: "We spent 8 months tuning that model. Starting over is not an option."
4. Mobile CRM access for field reps — Priority: Medium
   Source quote: "Half my enterprise team lives in the app on their phones."

Assumptions tested:
- Reporting speed is the biggest frustration → Corrected — data entry burden is #1.
  Dana said reps spend 40 min/day on manual logging; slow reports ranked third.
- Forecasting accuracy is top priority → Confirmed — Dana was emphatic about this.
- Dana will resist migration → Nuanced — she supports it IF reps get fewer clicks
  per deal update. She's frustrated with Salesforce, not attached to it.

Constraints uncovered:
- No more than 4 hours of CRM downtime during cutover (weekend only)
- Outreach contract renews in 3 months — integration must be live before then
- Sales comp data cannot leave Salesforce until finance validates HubSpot reports

Conflicts with other stakeholders:
- Sales Ops wants a phased rollout by region; Dana wants a single cutover to
  avoid running two systems. Resolution needed: Yes.

Open questions for follow-up:
- How does the CPQ workflow interact with HubSpot's native quoting?
  Assigned to: James (Solutions Architect) — Due: 2026-02-19
- Which 43 custom workflows are actually used weekly vs. legacy?
  Assigned to: Sales Ops — Due: 2026-02-26
```
