# Metrics Framework Template

> Fill in each section below. Delete the instructional notes (in italics) once completed.

---

## Business Objective

_State the business objective in one sentence. Every metric in this framework must connect to this objective._

**Objective:** [                                                                          ]

---

## Primary Metric

_Exactly one. The single metric that defines success for this objective._

| Field | Value |
|-------|-------|
| **Metric name** | |
| **Formula** | |
| **Data source** | |
| **Owner** | |
| **Review cadence** | |
| **Alerting threshold** | |
| **Segmentation** | |
| **Baseline** | |
| **Target** | |
| **Notes** | |

---

## Guardrail Metrics

_2-4 metrics that must not degrade while pursuing the primary metric. Each has a threshold (floor or ceiling), not a target._

### Guardrail 1

| Field | Value |
|-------|-------|
| **Metric name** | |
| **Formula** | |
| **Data source** | |
| **Owner** | |
| **Review cadence** | |
| **Alerting threshold** | |
| **Segmentation** | |
| **Baseline** | |
| **Notes** | |

### Guardrail 2

| Field | Value |
|-------|-------|
| **Metric name** | |
| **Formula** | |
| **Data source** | |
| **Owner** | |
| **Review cadence** | |
| **Alerting threshold** | |
| **Segmentation** | |
| **Baseline** | |
| **Notes** | |

### Guardrail 3

| Field | Value |
|-------|-------|
| **Metric name** | |
| **Formula** | |
| **Data source** | |
| **Owner** | |
| **Review cadence** | |
| **Alerting threshold** | |
| **Segmentation** | |
| **Baseline** | |
| **Notes** | |

### Guardrail 4

| Field | Value |
|-------|-------|
| **Metric name** | |
| **Formula** | |
| **Data source** | |
| **Owner** | |
| **Review cadence** | |
| **Alerting threshold** | |
| **Segmentation** | |
| **Baseline** | |
| **Notes** | |

---

## Diagnostic Metrics

_4-8 metrics that explain why the primary metric is moving. Organize in causal order: inputs (actions) before outputs (results)._

### Diagnostic 1

| Field | Value |
|-------|-------|
| **Metric name** | |
| **Formula** | |
| **Data source** | |
| **Owner** | |
| **Review cadence** | |
| **Segmentation** | |
| **Baseline** | |
| **Causal relationship** | _How does this metric influence the primary metric?_ |
| **Notes** | |

### Diagnostic 2

| Field | Value |
|-------|-------|
| **Metric name** | |
| **Formula** | |
| **Data source** | |
| **Owner** | |
| **Review cadence** | |
| **Segmentation** | |
| **Baseline** | |
| **Causal relationship** | |
| **Notes** | |

### Diagnostic 3

| Field | Value |
|-------|-------|
| **Metric name** | |
| **Formula** | |
| **Data source** | |
| **Owner** | |
| **Review cadence** | |
| **Segmentation** | |
| **Baseline** | |
| **Causal relationship** | |
| **Notes** | |

### Diagnostic 4

| Field | Value |
|-------|-------|
| **Metric name** | |
| **Formula** | |
| **Data source** | |
| **Owner** | |
| **Review cadence** | |
| **Segmentation** | |
| **Baseline** | |
| **Causal relationship** | |
| **Notes** | |

### Diagnostic 5

| Field | Value |
|-------|-------|
| **Metric name** | |
| **Formula** | |
| **Data source** | |
| **Owner** | |
| **Review cadence** | |
| **Segmentation** | |
| **Baseline** | |
| **Causal relationship** | |
| **Notes** | |

### Diagnostic 6

| Field | Value |
|-------|-------|
| **Metric name** | |
| **Formula** | |
| **Data source** | |
| **Owner** | |
| **Review cadence** | |
| **Segmentation** | |
| **Baseline** | |
| **Causal relationship** | |
| **Notes** | |

---

## Dashboard Specification

### Executive Dashboard

| Field | Value |
|-------|-------|
| **Tool** | |
| **Refresh frequency** | |
| **Access control** | |
| **Responsible person** | |
| **Metrics shown** | _Primary + guardrails only_ |

### Team Dashboard

| Field | Value |
|-------|-------|
| **Tool** | |
| **Refresh frequency** | |
| **Access control** | |
| **Responsible person** | |
| **Metrics shown** | _All three tiers_ |
| **Filters available** | |

### Investigation View

| Field | Value |
|-------|-------|
| **Tool** | |
| **Capabilities** | _Cohort breakdowns, funnel analysis, event-level detail_ |
| **Access control** | |
| **Responsible person** | |

---

## Review Process

| Review | Cadence | Duration | Attendees | Standing Agenda | Output |
|--------|---------|----------|-----------|-----------------|--------|
| Standup | Weekly | 15 min | | Primary trend + guardrail check | Investigation owners assigned |
| Deep-dive | Monthly | 45 min | | Cohort analysis + diagnostic review | Priority adjustments |
| Calibration | Quarterly | 90 min | | Framework validity check | Framework revisions |

---

## Anti-Metrics

_Metrics considered and explicitly rejected. Document why to prevent them from being re-proposed._

| Rejected Metric | Reason for Rejection |
|-----------------|---------------------|
| | |
| | |
| | |

---

## Instrumentation Gaps

_Aspirational metrics that cannot be computed today. Track as work items._

| Metric | Missing Capability | Tracking Ticket | Owner | Target Date |
|--------|--------------------|-----------------|-------|-------------|
| | | | | |
| | | | | |
