# Standard Clause Benchmarks

Market-standard ranges for common contract terms. Use these benchmarks when evaluating whether a contract's provisions are reasonable or require negotiation.

---

## Liability Caps

| Contract Value | Acceptable Cap Range | Notes |
|---------------|---------------------|-------|
| < $50K annually | 1-2x annual contract value | Small contracts often have caps equal to fees paid in the prior 12 months |
| $50K-$500K annually | 1-2x annual contract value | Standard SaaS range; 12 months of fees paid is the most common formulation |
| $500K-$5M annually | 1x annual contract value | Higher-value contracts typically cap at 12 months of fees |
| > $5M annually | Negotiated; often 1x with specific carve-outs | Enterprise deals frequently include uncapped carve-outs for specific liabilities |

### Common Carve-Outs (Excluded from Cap)

These liabilities are typically excluded from the general liability cap and may be uncapped or subject to a higher "super cap":

- Indemnification obligations (IP infringement, data breach)
- Breach of confidentiality / NDA obligations
- Willful misconduct or gross negligence
- Violation of applicable law
- Death or bodily injury caused by negligence

### Red Flags

- Liability cap below total contract value (vendor retains more than they risk)
- One-sided cap (vendor capped, customer uncapped)
- No carve-outs for data breach or IP infringement
- Cap applies to indemnification obligations (effectively neutering them)

---

## SLA Tiers

### Uptime SLAs

| Tier | Uptime | Max Downtime/Month | Typical Use Case |
|------|--------|-------------------|-----------------|
| Standard | 99.5% | ~3.6 hours | Non-critical internal tools |
| Business | 99.9% | ~43.6 minutes | Business applications, SaaS platforms |
| Enterprise | 99.95% | ~21.9 minutes | Revenue-critical systems, financial services |
| Mission-critical | 99.99% | ~4.3 minutes | Healthcare, real-time trading, emergency services |

### SLA Credit Structures

| Model | How It Works | Market Standard |
|-------|-------------|----------------|
| Tiered credits | Credit percentage increases with severity of breach | 5% credit per 0.1% below target, capped at 30% of monthly fee |
| Flat credit | Fixed credit for any SLA miss | 10% of monthly fee for any month below target |
| Service credits + termination right | Credits for minor breaches, termination for persistent failure | Credits for individual months; termination right if SLA missed 3+ months in 12-month period |

### Red Flags

- No SLA at all — the vendor makes no performance commitment
- SLA measured by vendor self-reporting with no independent verification
- Credits are the **sole and exclusive remedy** with no termination right for persistent failure
- SLA excludes scheduled maintenance windows without defining the maintenance schedule
- SLA measured on a quarterly or annual basis (masks individual bad months)

---

## Breach Notification Windows

| Benchmark | Timeline | Context |
|-----------|----------|---------|
| Best practice | 24-48 hours | Aggressive but achievable for organizations with mature incident response |
| Market standard | 72 hours | Aligns with GDPR processor-to-controller timeline |
| Acceptable | 5 business days | Common in non-regulated industries; may be insufficient for GDPR compliance |
| Concerning | 30 days | Too slow for any contract involving personal data |
| Unacceptable | "Reasonable time" or undefined | No commitment at all; flag as Critical |

### What Notification Must Include

The contract should specify what information the breach notification must contain at minimum:

- Nature of the breach (what happened)
- Categories and approximate number of data subjects affected
- Categories and approximate number of records affected
- Name and contact details of the vendor's point of contact
- Likely consequences of the breach
- Measures taken or proposed to address the breach

---

## Auto-Renewal and Termination

### Auto-Renewal Benchmarks

| Provision | Market Standard | Red Flag |
|-----------|----------------|----------|
| Auto-renewal term | Renews for same period as initial term, or 1-year periods | Renews for multi-year terms without negotiation |
| Notice period to cancel | 30-90 days before renewal date | 180+ days (easy to miss) |
| Price increase on renewal | CPI adjustment or capped at 3-5% annually | Uncapped ("then-current pricing") or >10% |
| Renewal notification | Vendor notifies customer 60-90 days before renewal | No notification obligation |

### Termination Provisions

| Provision | Market Standard | Red Flag |
|-----------|----------------|----------|
| Termination for convenience | Either party with 30-90 days written notice | Not permitted, or only vendor has this right |
| Termination for cause | 30-day cure period after written notice of material breach | No cure period, or cure period >60 days |
| Termination for insolvency | Immediate termination right if other party becomes insolvent | No insolvency termination clause |
| Effect of termination | Data return/export within 30 days, transition assistance | No data portability, immediate data deletion |

### Data Portability on Exit

| Provision | Acceptable | Concerning |
|-----------|-----------|------------|
| Export format | Standard formats (CSV, JSON, SQL dump) via API or admin console | Proprietary format requiring vendor tools to read |
| Export window | 30-90 days post-termination | Less than 14 days, or no defined window |
| Export cost | Included in contract | Charged at vendor's "then-current professional services rate" |
| Transition assistance | 60-90 days of reasonable assistance at agreed rates | No transition support; immediate cutoff |

---

## Indemnification Benchmarks

| Indemnification Type | Who Typically Provides | Standard Scope |
|---------------------|----------------------|----------------|
| IP infringement | Vendor indemnifies customer | Vendor defends and indemnifies customer against claims that the service infringes third-party IP |
| Data breach | Vendor indemnifies customer (when vendor is at fault) | Vendor covers costs arising from a breach caused by vendor's failure to maintain required safeguards |
| Regulatory fines | Negotiated | Often excluded; if included, typically limited to fines resulting from vendor's breach of the DPA |
| Third-party claims | Mutual | Each party indemnifies the other for claims arising from their own negligence or misconduct |

### Red Flags

- No IP indemnification from vendor (customer bears all infringement risk)
- IP indemnification limited to "defend" but not "indemnify" (vendor provides a lawyer but customer pays damages)
- Indemnification subject to the general liability cap (effectively worthless for large claims)
- Customer required to indemnify vendor for claims arising from vendor's own service
