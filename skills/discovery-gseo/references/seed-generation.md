# Seed Generation

Seed keywords are the raw starting points for the entire discovery process. Get seeds wrong and every downstream expansion, evaluation, and prioritization step operates on the wrong foundation.

Your seeds do not need to be clever. They need to be obvious. If you sell invoicing software, "invoicing software" is a perfect seed. Start obvious, let the tools find the clever stuff.

## The 5 sources of keyword ideas

Every keyword you will ever target comes from one of these five sources. Understanding this mental model prevents you from skipping a source and missing an entire category of opportunities.

**Source 1 — Your own brain.** You know your product, your market, and the problems you solve. This produces initial seeds: rough, obvious terms that describe what you do.

**Source 2 — Your competitors.** Other websites already rank for keywords that should be yours. Studying what works for them is the fastest shortcut to a good keyword list. Competitors have done the validation for you.

**Source 3 — Google itself.** Autocomplete suggestions, People Also Ask boxes, and Related Searches reveal what people actually search for. Free, real-time, intent-rich data.

**Source 4 — Communities.** Reddit, forums, Twitter/X, Hacker News, Slack groups — places where potential customers describe problems in their own words. The language they use maps directly to search queries that keyword tools miss.

**Source 5 — Keyword research tools.** Ahrefs, Semrush, Ubersuggest, Google Keyword Planner — these take your seeds and expand them into hundreds or thousands of related keywords with volume and difficulty data attached.

The process starts broad (many raw ideas from all five sources), then narrows through evaluation and filtering until you have a focused, prioritized list.

## Seed generation methodology

### The 5 questions

Ask yourself these questions and write down every answer. Do not filter or evaluate yet.

**"What do I sell or offer?"**
Write down the name of your product category, service type, the problem you solve. Multiple variations are good. If you sell project management software: "project management software", "task management tool", "team collaboration app", "project tracker."

**"What problem does my product solve?"**
Think about pain points. Not what you sell — what pain you eliminate. "How to manage remote teams", "track project deadlines", "assign tasks to team members", "keep projects on schedule."

**"How would a stranger describe what I do?"**
Your customers do not use your internal jargon. A CI/CD platform user might search "automate code deployment" or "continuous integration tool" — not your internal product name. Use plain language.

**"What alternatives or competitors exist?"**
Competitor names and their product categories become seeds. "[Competitor] alternative", "[Competitor A] vs [Competitor B]", "[product category] comparison." These are high-intent commercial keywords.

**"What technologies, methods, or concepts are relevant?"**
If your product uses or integrates with specific technologies, those are seeds. "Django email backend", "React form builder", "Stripe subscription management." These attract technical audiences searching for solutions within their existing stack.

### Think like your customer, not like yourself

The biggest mistake in seed generation is using internal language. You call it a "workflow orchestration engine." Your customers search for "project management tool." Use the language real people use, not your marketing copy.

Techniques to find customer language:
- Read your own support tickets — the words customers use to describe their problems
- Check your reviews on G2, Capterra, Product Hunt — the language reviewers use
- Read competitor reviews — same pattern, different brand
- Ask your sales team what words prospects use in initial conversations

### Seed format

Keep seeds simple: 1 to 4 words each. Do not worry about search volume, competition, or whether anyone actually searches for them. That comes later. You are creating starting points for expansion, not final targets.

**Target:** 15-30 seeds. This is enough to generate a large expanded list. You can always add more seeds later as you discover new angles.

## GEO seed validation

This is the step that separates modern keyword discovery from traditional keyword research. Before you rely solely on search data, probe AI platforms to understand how AI sees your market.

### Why GEO seed validation matters

AI platforms (ChatGPT, Perplexity, Gemini, Copilot) are becoming a discovery channel. When someone asks "What are the best tools for [your category]?", the AI's answer influences which products get evaluated. If your product is not in that answer, you lose a prospect before they ever reach Google.

GEO seed validation tells you:
- Which brands AI already recommends in your space
- Which topics AI covers when answering questions about your category
- What language AI uses to describe the problem you solve
- Where the gaps are — topics AI should cover but cites weak or outdated sources

### How to probe AI platforms

**ChatGPT:** Ask broad questions about your space:
- "What are the best tools for [category]?"
- "How do I [problem your product solves]?"
- "What should I look for in [product category]?"
- "Compare [Competitor A] and [Competitor B] for [use case]."

Record: which brands mentioned, which features highlighted, what topics covered, what language used.

**Perplexity:** Same queries. Perplexity shows its sources explicitly, so you can see exactly which websites get cited. This is the most actionable GEO data — you can see the pages you need to outperform.

**Gemini:** Same queries, yet another perspective. Different AI platforms cite different sources.

### Turning AI probes into GEO-validated seeds

Topics that AI platforms actively discuss become GEO-validated seeds. If ChatGPT mentions "recurring billing" when discussing invoicing tools, "recurring billing" is a GEO-validated seed — content targeting it has AI citation potential from day one.

Run `scripts/probe-ai-discovery.py --queries queries.txt` to automate this. The script tests your queries against AI platforms and records citations, brands, and topics.

### Example seed list with GEO validation

```
invoicing software          [GEO: AI mentions in tool recommendations]
invoice generator           [GEO: AI recommends free generators]
online invoicing            [GEO: AI discusses as category]
billing software            [GEO: AI covers in comparisons]
send invoices online        [NO GEO: AI doesn't address this phrasing]
freelancer invoice tool     [GEO: AI recommends tools for freelancers]
invoice template            [GEO: AI provides template advice]
recurring billing           [GEO: AI discusses as feature category]
payment reminder            [NO GEO: AI discusses but doesn't cite tools]
invoice tracking            [NO GEO: minimal AI coverage]
```

Seeds with GEO validation flags get priority in the expansion phase. They have dual traffic potential: organic search + AI citation.

## Common seed generation mistakes

**Starting with long-tail keywords instead of seeds.** "Best free invoicing software for freelancers who use Stripe" is not a seed — it is a finished keyword. Seeds are broad: "invoicing software", "freelancer billing." Long-tail variants emerge from the expansion phase.

**Using internal product names.** Your product's internal feature name is not what customers search for. If your team calls it "Smart Reconciliation Engine," search for what that means to a user: "automatic invoice matching", "payment reconciliation tool."

**Stopping at 5 seeds.** Five seeds produce a narrow keyword universe. Push to 15-30. The more seeds you start with, the more opportunities the expansion phase reveals. Use all 5 seed questions, and you will naturally reach 15+ seeds.

**Ignoring competitor brand names.** "[Competitor] alternative" and "[A] vs [B]" are high-intent commercial keywords. They belong in your seed list from the start.

**Not running GEO validation.** If you skip the AI probing step, you miss the earliest signal of which topics have AI citation potential. This takes 15 minutes and can reshape your entire seed list.
