# Blameless Writing Guide

Ten before/after rewrites that transform blame-oriented language into system-observation language. Use this as a reference when writing contributing factors, root causes, and timelines in incident postmortems.

## The Principle

Blameless writing describes **what the system allowed to happen**, not **what a person did wrong**. The goal is not to remove accountability — it is to focus attention on the systemic conditions that enabled the failure, because those are the conditions you can actually fix.

A person making a mistake is a symptom. The system that let the mistake reach production is the cause.

---

## 10 Before/After Rewrites

### 1. Certificate Expiry

**Blame language:**
> "The engineer forgot to renew the TLS certificate, causing a 47-minute outage."

**System-observation language:**
> "Certificate renewal relied on manual tracking in a spreadsheet with no automated expiry alerting. The system had no defense against expiry because lifecycle management was treated as a one-time setup rather than a recurring process."

**Why it matters:** The fix is an automated alert, not a reminder to the engineer. The blame version hides this.

---

### 2. Bad Deploy

**Blame language:**
> "The developer pushed a broken migration to production without testing it."

**System-observation language:**
> "The deployment pipeline did not include a migration validation step. The migration passed CI because the test database schema was out of sync with production. No pre-deploy check compared migration state against the target environment."

**Why it matters:** Even if this developer had tested locally, the next one might not. The system needs a gate.

---

### 3. Slow Escalation

**Blame language:**
> "The on-call engineer waited too long to escalate and the outage lasted an extra 40 minutes."

**System-observation language:**
> "The escalation policy did not define a time threshold for engaging the secondary on-call. The runbook for this alert type described diagnostic steps but did not specify when to stop diagnosing and escalate. The 40-minute diagnosis window exceeded the severity threshold for this service."

**Why it matters:** Without a defined escalation trigger, every on-call engineer will make a different judgment call. Define the threshold.

---

### 4. Wrong Configuration

**Blame language:**
> "Someone changed the feature flag without realizing it affected production."

**System-observation language:**
> "The feature flag system did not distinguish between staging and production environments in its UI. A flag change intended for staging was applied globally because the interface defaulted to all environments. No confirmation step or environment selector was presented before applying the change."

**Why it matters:** The interface design caused the error. A different person would make the same mistake.

---

### 5. Missed Alert

**Blame language:**
> "The on-call engineer had their notifications silenced and missed the critical alert."

**System-observation language:**
> "The alerting system relied on a single notification channel (push notification) with no fallback escalation when the primary page was not acknowledged within 5 minutes. The system did not verify alert receipt or automatically escalate to the secondary on-call."

**Why it matters:** People silence phones, lose battery, or sleep through vibrations. The system needs a fallback path.

---

### 6. Untested Rollback

**Blame language:**
> "The team didn't test their rollback plan, so when the deploy failed, they couldn't revert."

**System-observation language:**
> "The deployment process did not include mandatory rollback verification as part of the release checklist. Rollback procedures had not been exercised in the last 6 months, and the rollback script referenced a deprecated API endpoint that no longer existed."

**Why it matters:** Untested rollbacks are the norm unless the system enforces testing. Build rollback verification into the deploy process.

---

### 7. Capacity Planning

**Blame language:**
> "The team underestimated traffic for the product launch and the service fell over."

**System-observation language:**
> "Capacity planning for the launch used baseline traffic projections without a load test against the projected peak. The service auto-scaling policy had a 10-minute cooldown that could not respond to the traffic ramp-up, which occurred in under 3 minutes. No pre-scaling step was included in the launch checklist."

**Why it matters:** Every launch has traffic uncertainty. The system needs pre-scaling and faster auto-scaling, not better guessing.

---

### 8. Stale Documentation

**Blame language:**
> "The engineer followed an outdated runbook, which made the problem worse."

**System-observation language:**
> "The runbook for this procedure was last updated 14 months ago and referenced a tool that had been deprecated in Q3. No review cadence or ownership was assigned to runbook maintenance. The runbook did not display a last-reviewed date, so the engineer had no signal that it might be outdated."

**Why it matters:** Engineers will follow runbooks. If the runbook is wrong, the system for maintaining runbooks is the failure.

---

### 9. Permission Gap

**Blame language:**
> "The responder didn't have access to the database, so they had to wait for someone who did."

**System-observation language:**
> "The on-call role did not include read access to the production database, which was required for the diagnostic steps in the incident runbook. Granting emergency access required approval from a database administrator, adding 25 minutes to the response time. The access model had not been reviewed against the on-call responsibilities since the last team reorganization."

**Why it matters:** If the runbook requires database access and the on-call does not have it, that is a system design gap.

---

### 10. Dependency Assumption

**Blame language:**
> "The team assumed the third-party API would be reliable and didn't build a fallback."

**System-observation language:**
> "The integration with the third-party API was designed without a circuit breaker, fallback response, or cached-result path. The vendor SLA of 99.9% uptime was treated as a guarantee rather than a probabilistic commitment. No failure mode analysis was conducted during the integration design phase."

**Why it matters:** Every external dependency will fail eventually. The system must account for this in its design.

---

## Writing Checklist

When reviewing your postmortem for blameless language, check each contributing factor and root cause statement:

- [ ] Does it name a system condition rather than a person's action?
- [ ] Could a different person in the same situation have made the same mistake?
- [ ] Does the description point toward a systemic fix (process, tooling, automation)?
- [ ] Is intent absent from the description? (Remove words like "forgot," "didn't bother," "neglected," "carelessly")
- [ ] Would the person involved feel comfortable reading this statement aloud to their team?

## Words to Replace

| Blame Word | System-Observation Alternative |
|------------|-------------------------------|
| forgot | was not tracked by / had no automated reminder for |
| failed to | the process did not include a step for |
| neglected | no ownership was assigned for |
| should have known | the information was not surfaced in the workflow |
| carelessly | the interface did not prevent / warn against |
| didn't bother | the procedure did not require |
| was unaware | the system did not communicate / surface |
| made a mistake in | the validation step did not catch |
| wasn't paying attention | the alert / signal was not prominent enough to |
| broke | the change interacted with [system] in an unexpected way |
