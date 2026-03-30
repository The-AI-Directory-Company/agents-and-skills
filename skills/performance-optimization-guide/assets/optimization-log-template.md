# Optimization Log Template

Copy this template to track each optimization fix with before/after measurements.

## Optimization Metadata

| Field | Value |
|-------|-------|
| Feature / Endpoint | |
| Baseline Date | |
| Target Metric | |
| Target Value | |
| Engineer | |
| Environment | (production / staging / local) |
| Measurement Tool | |

## Baseline (3-run minimum)

| Run | Metric Value | Conditions |
|-----|-------------|------------|
| 1 | | |
| 2 | | |
| 3 | | |
| **Average** | | |

## Optimization Log

Record each fix individually. Apply one fix, measure, then move to the next.

### Fix 1

| Field | Value |
|-------|-------|
| Fix Applied | |
| Description | |

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| | | | |
| | | | |

### Fix 2

| Field | Value |
|-------|-------|
| Fix Applied | |
| Description | |

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| | | | |
| | | | |

### Fix 3

| Field | Value |
|-------|-------|
| Fix Applied | |
| Description | |

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| | | | |
| | | | |

<!-- Copy the fix block above for additional fixes. -->

## Summary Table

| # | Fix Applied | Metric | Before | After | Change |
|---|-------------|--------|--------|-------|--------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

## Final Before/After

| Metric | Baseline (start) | Final (all fixes) | Total Change | Target | Met? |
|--------|-------------------|-------------------|-------------|--------|------|
| | | | | | |
| | | | | | |

## Regression Prevention

| Prevention Measure | Details | Status |
|-------------------|---------|--------|
| CI performance budget | | |
| Monitoring alert | | |
| Performance test | | |
| Documentation | | |

## Notes

<!-- Additional context, caveats, dependencies, or follow-up items. -->
