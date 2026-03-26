# Prompt Engineering — Support Ticket Classifier, Helios SaaS

## Task Definition

**Goal:** Classify incoming support tickets into one of 6 categories for automatic queue routing.
**Model:** Claude 3.5 Sonnet. **Volume:** ~800 tickets/day, budget $0.01/ticket max.

### System Prompt (v4 — final)

```
You are a support ticket classifier for Helios, a project management SaaS product.
Given a support ticket (subject and body), classify it into exactly one category.

Categories:
- billing: Payments, invoices, subscriptions, refunds, pricing
- bug: Something broken, errors, crashes, unexpected behavior
- feature_request: Requests for new functionality
- account: Login, password resets, SSO, permissions
- integration: API questions, webhooks, third-party connections
- how_to: Usage questions, workflow guidance

Rules:
- If a ticket spans two categories, choose the one requiring action first.
- Broken integrations are "bug" not "integration."
- If uncertain, respond with "unknown".

Respond with JSON only:
{"category": "string", "confidence": "high | medium | low", "reasoning": "1 sentence"}
```

## Few-Shot Examples

```
Ticket: "Can't export CSV anymore" / "Export button throws 500 error since yesterday."
Output: {"category": "bug", "confidence": "high", "reasoning": "Specific error on previously working feature."}

Ticket: "Add Gantt chart view" / "Would love a timeline view for projects."
Output: {"category": "feature_request", "confidence": "high", "reasoning": "Requesting new functionality."}

Ticket: "Slack notifications stopped" / "Integration was fine until last week, nothing changed."
Output: {"category": "bug", "confidence": "high", "reasoning": "Previously working integration is broken."}

Ticket: "How do I set up recurring tasks?" / "I want tasks to recreate every Monday."
Output: {"category": "how_to", "confidence": "high", "reasoning": "Asking how to use an existing feature."}
```

## Evaluation Framework

Test set: 50 manually labeled tickets, stratified by category.

| Metric | Method | Threshold |
|--------|--------|-----------|
| Format compliance | JSON schema validation | 100% |
| Accuracy | Exact match vs. human labels | > 90% |
| High-confidence accuracy | Accuracy on "high" confidence only | > 95% |
| Latency (p95) | API response time | < 2s |
| Cost per ticket | Token count * price | < $0.01 |

## Iteration Log

| Version | Change | Accuracy | Key Issue |
|---------|--------|----------|-----------|
| v1 | Category list only, no examples | 74% | Confused integration/bug (6 errors), inconsistent JSON (3 errors) |
| v2 | Added 3 few-shot examples | 84% | how_to/feature_request confusion on "Can I do X?" tickets |
| v3 | Added how_to example + broken-integration rule | 90% | 2 billing/account edge cases, 2 ambiguous bug/feature |
| v4 | Added Slack edge case + confidence field | 92% | 4 remaining errors are genuine ambiguities (60% human agreement) |

**v4 accepted.** High-confidence accuracy: 96%. Format compliance: 100%. Avg cost: $0.003/ticket. Avg latency: 680ms.

## Production Configuration

- **Temperature:** 0 (deterministic)
- **Max tokens:** 150
- **Fallback:** "low" confidence tickets route to human triage
- **Monitoring:** Alert if any category exceeds 2x its 30-day average volume
- **Re-evaluation:** Monthly with 10 fresh test tickets added per cycle
