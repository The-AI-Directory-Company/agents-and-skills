# Market Sizing Guide: Bottom-Up TAM/SAM/SOM

How to size your market for a pitch deck using bottom-up methodology. Top-down is for context. Bottom-up is for credibility.

---

## Definitions

| Term | Definition | Analogy |
|---|---|---|
| **TAM** (Total Addressable Market) | Total revenue opportunity if every possible customer bought your product. Theoretical ceiling. | The entire ocean |
| **SAM** (Serviceable Addressable Market) | The portion of TAM you can reach with your current business model, geography, and go-to-market. | The part of the ocean your boat can sail |
| **SOM** (Serviceable Obtainable Market) | The realistic share of SAM you can capture in 3-5 years given competition, resources, and execution. | The fish you can actually catch |

---

## Bottom-Up vs. Top-Down

### Top-down (what investors are skeptical of)

Start with a large market report number and take a percentage.

"The global project management software market is $7.6B (Gartner, 2025). We will capture 1% = $76M."

**Why this fails:** It does not explain how you get to 1%. It assumes penetration without mechanism. Every startup claims 1% of a big market. Investors have heard it thousands of times.

### Bottom-up (what investors want to see)

Start with the smallest countable unit and multiply up.

"There are 180,000 B2B SaaS companies in the US with 50-500 employees (Census Bureau). 62% use project management tools (Gartner survey). Our average deal is $6,000/year. TAM = 180,000 x 62% x $6,000 = $669M."

**Why this works:** Every number is sourced, challengeable, and tied to a unit. An investor can disagree with any single assumption and recalculate. The methodology is transparent.

---

## Step-by-Step Procedure

### Step 1: Define your target customer precisely

Do not start with "all companies." Start with:
- Industry or vertical
- Company size (employees or revenue)
- Geography
- Role of the buyer
- Problem they must have

Example: "B2B SaaS companies in the US and EU with 50-500 employees that have a product team of 5+ people."

### Step 2: Count the target customers (for TAM)

Sources for customer counts:

| Source | What it provides | Best for |
|---|---|---|
| US Census Bureau (NAICS codes) | Company counts by industry, size, geography | US-focused B2B |
| Eurostat Structural Business Statistics | Company counts across EU | EU markets |
| LinkedIn Sales Navigator | Company counts by industry, size, headcount | Any B2B segment |
| Crunchbase / PitchBook | Startup and tech company counts | Tech-focused markets |
| Bureau of Labor Statistics (BLS) | Employment data by industry | Labor-related products |
| Industry associations | Member counts, market surveys | Niche verticals |
| Gartner / IDC / Forrester | Market size reports with adoption rates | Software categories |
| Government registries | Business registrations by type | Regulated industries |

**Important:** Cross-reference at least two sources. If LinkedIn says 150,000 companies and Census says 180,000, use the more conservative number and note the range.

### Step 3: Apply your price (for TAM and SAM)

Multiply the number of target customers by your annual contract value (ACV).

```
TAM = [Number of potential customers] x [ACV]
```

For SAM, narrow the customer count to the segment you can actually reach:
- Geographic constraints (if you only operate in the US, exclude EU)
- Language constraints
- Channel constraints (if you only sell self-serve, exclude enterprise-only buyers)
- Model constraints (if you require an API integration, exclude non-technical teams)

```
SAM = [Reachable customers] x [ACV]
```

### Step 4: Estimate obtainable share (for SOM)

SOM is the hardest number and the one investors scrutinize most. It must be defensible with a bottoms-up acquisition model.

Method:
1. Start with your current customer acquisition rate (or planned rate for pre-revenue).
2. Apply a realistic growth trajectory (not constant 10% monthly growth for 5 years).
3. Factor in churn.
4. Project 3-5 years out.

```
SOM = [Year 3-5 active customers] x [ACV]
```

Cross-check: SOM should typically be 1-5% of SAM for early-stage companies. If your SOM is 20% of SAM, your SAM is probably too narrow or your growth assumptions are too aggressive.

### Step 5: Document sources and assumptions

Every number needs a source. Every assumption needs a confidence level.

| Input | Value | Source | Confidence |
|---|---|---|---|
| US B2B SaaS companies, 50-500 employees | 180,000 | Census Bureau NAICS 5112, 2024 | High |
| % using project management tools | 62% | Gartner PM Software Survey, 2025 | Medium |
| Average contract value | $6,000/yr | Internal pricing model | Medium |
| Year 3 customer count | 2,800 | Growth model (15% declining to 8%) | Low |

---

## Worked Example

**Company:** FlowMetrics (fictional) -- product analytics for B2B SaaS teams
**Segment:** B2B SaaS companies, US + EU, 50-500 employees, with a product team

### TAM

| Input | Value | Source |
|---|---|---|
| B2B SaaS companies, US (50-500 emp) | 180,000 | Census Bureau NAICS 5112 |
| B2B SaaS companies, EU (50-500 emp) | 120,000 | Eurostat SBS |
| Total target companies | 300,000 | |
| % with dedicated product team (5+) | 55% | LinkedIn Sales Navigator sample (n=500) |
| Target customer count | 165,000 | |
| Average contract value | $7,200/yr ($600/mo) | FlowMetrics pricing model |
| **TAM** | **$1.19B** | |

### SAM

| Narrowing Factor | Reduction | Remaining |
|---|---|---|
| Starting pool | -- | 165,000 |
| English-speaking markets only (US, UK, Ireland, Nordics, NL) | -40% | 99,000 |
| Companies using a product analytics tool today (replacement market) or actively evaluating (greenfield) | 45% adoption rate (Gartner) | 44,550 |
| **SAM customer count** | | **44,550** |
| x $7,200 ACV | | |
| **SAM** | | **$321M** |

### SOM (3-year)

| Year | New Customers | Churned | Active | ARR |
|---|---|---|---|---|
| Year 1 | 350 | 40 | 310 | $2.2M |
| Year 2 | 800 | 120 | 990 | $7.1M |
| Year 3 | 1,400 | 280 | 2,110 | $15.2M |

Assumptions: 15% monthly growth declining to 8% by Year 3. 3.5% monthly churn improving to 2.5%. ACV grows from $7,200 to $7,800 due to upsell.

**SOM: $15.2M (4.7% of SAM)** -- within the typical 1-5% range for a Series A company.

### Summary for the slide

```
TAM: $1.2B — 165K B2B SaaS companies with product teams (US + EU)
SAM: $321M — English-speaking markets, companies using or evaluating analytics
SOM: $15M — 2,100 customers in 3 years at $7,200 ACV

Sources: Census Bureau, Eurostat, LinkedIn Sales Navigator, Gartner
```

---

## The "We Estimated" Anti-Pattern

"We estimated the market at $500M" is not a source. It is a restatement of the conclusion.

Every time you see "we estimated" in a market sizing section, replace it with the actual inputs:

| Bad | Good |
|---|---|
| "We estimate a $500M TAM" | "68,000 target companies (Census) x $7,200 ACV = $490M TAM" |
| "We believe we can capture 5% market share" | "Our growth model projects 2,100 active customers by Year 3 (see assumptions table), representing 4.7% of SAM" |
| "The market is growing 15% annually" | "Gartner projects the product analytics market growing 14.8% CAGR through 2028 (Report ID: G00XXX)" |
| "We estimate strong demand" | "In our survey of 200 product managers, 67% said they would evaluate a new analytics tool in the next 12 months" |

The rule: **if a sentence contains "we estimated" or "we believe," it needs a source or it needs to be rewritten as a transparent calculation.**

---

## Common Mistakes

1. **Using TAM as the headline number.** "We are going after a $10B market" tells investors nothing about your realistic opportunity. Lead with SOM, support with SAM, provide TAM for context.

2. **Citing a market report without checking the definition.** Gartner's "$7.6B project management market" may include categories you do not compete in (enterprise resource planning, time tracking, etc.). Read the methodology section of any report you cite.

3. **Constant growth rate assumptions.** No company grows at 15% monthly for 36 months straight. Use a declining growth curve. If your SOM requires sustained hypergrowth, your number is not credible.

4. **Forgetting churn in the SOM calculation.** SOM = cumulative new customers minus cumulative churn, not just new customers added up. A 3% monthly churn rate means you lose ~31% of customers annually.

5. **Mixing revenue and bookings.** TAM/SAM/SOM should use the same revenue definition throughout. Annual recurring revenue (ARR) is the standard for SaaS.

6. **Inflating ACV with "enterprise potential."** If your average deal today is $5,000/year, do not use $25,000/year because "we plan to move upmarket." Use current ACV for SOM and note upmarket ACV as upside in the appendix.
