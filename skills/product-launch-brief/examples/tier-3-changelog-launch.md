# Product Launch Brief: Relay Bulk Import via CSV

## 1. Launch Summary

- **Product/Feature:** Bulk Import — upload a CSV to create up to 5,000 jobs in one action
- **Launch Date:** May 6, 2026, 10:00 AM ET
- **Launch Tier:** Tier 3 (minor — changelog, docs update, in-app tooltip)
- **Launch Owner:** Aisha Patel, Senior Product Manager
- **One-Line Pitch:** "Import thousands of jobs from a spreadsheet in under a minute — no API setup needed."

## 2. Positioning

**For** operations managers at field service companies running 200+ jobs per week **who** currently enter jobs manually one-by-one or wait for an engineering team to build an API integration,
**this feature provides** a drag-and-drop CSV import that creates up to 5,000 jobs in a single upload,
**unlike** the existing manual entry or API-only bulk path, **it** requires zero technical setup — upload, map columns, confirm.

**Changelog version:** "New: Bulk Import via CSV. Upload a spreadsheet to create up to 5,000 jobs at once. Map columns in the UI, preview before confirming, and skip jobs with errors without losing the rest of the batch."

## 3. Target Audience

| Segment | Description | Current Behavior | Desired Behavior | Key Message |
|---------|-------------|-----------------|------------------|-------------|
| Primary | Operations managers (non-technical) | Enter jobs one at a time or email CSVs to support for manual import | Self-serve bulk import directly in the app | "No more one-by-one entry — upload your spreadsheet and go" |
| Secondary | Customer success managers (internal) | Handle CSV import requests from customers as support tickets | Point customers to self-serve import instead | "Redirect import requests to the in-app feature" |

## 4. Key Messages

1. **Message:** "Upload a CSV, map your columns, import up to 5,000 jobs in one action."
   - **Proof point:** Beta tested with 3 customers — average import time for 2,000 jobs was 47 seconds.
   - **Objection:** "What if my CSV has errors?" — The preview step flags invalid rows. You can fix or skip them without restarting the upload.

## 5. Launch Timeline

| Date | Milestone | Owner |
|------|----------|-------|
| Apr 29 (L-7) | Feature complete and behind feature flag | Aisha Patel (Product) |
| Apr 30 (L-6) | Help docs article published | Nina Torres (Support) |
| May 5 (L-1) | Changelog entry drafted and reviewed | Aisha Patel (Product) |
| May 6 (L-Day) | Feature flag enabled for all accounts, changelog published, in-app tooltip activated | Aisha Patel (Product) |
| May 7 (L+1) | Check support volume and import error rates | Aisha Patel + Nina Torres |

## 6. Channel Plan

| Channel | Asset | Owner | Date | CTA | Audience |
|---------|-------|-------|------|-----|----------|
| Changelog | Feature announcement (3 sentences + screenshot) | Aisha Patel | May 6 | "Try it now" | All users |
| In-app tooltip | New badge on Jobs page pointing to import button | Aisha Patel | May 6 | "Import jobs from CSV" | Active users on Jobs page |
| Help docs | "How to bulk import jobs" article with step-by-step screenshots | Nina Torres | Apr 30 | — | Users who need guidance |

No blog post, no email blast, no social. Tier 3 launches stay lightweight.

## 7. Success Metrics

| Metric | Target | Underperformance | Method | Timeframe |
|--------|--------|------------------|--------|-----------|
| Import feature usage | 50 unique accounts use it | < 15 accounts | Product analytics | 30 days |
| Import-related support tickets | < 5 per week | > 15 per week | Zendesk | 14 days |
| Import success rate (rows imported / rows uploaded) | > 92% | < 80% | Backend logs | 14 days |

## 8. Cross-Functional Responsibilities

| Team | Deliverable | Due Date | Contact |
|------|------------|----------|---------|
| Product | Feature flag ready, changelog entry | May 5 | Aisha Patel |
| Engineering | Import processing stable at 5K rows, error handling tested | Apr 29 | Jun Park |
| Support | Help docs article, awareness of known edge cases | Apr 30 | Nina Torres |

No press, no sales enablement, no legal review needed for this tier. If adoption exceeds targets, consider promoting to a Tier 2 email announcement in the monthly product update.
