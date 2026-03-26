---
name: prompt-engineering-guide
description: Design, test, and optimize LLM prompts systematically — with evaluation frameworks, chain-of-thought patterns, output formatting, and iteration methodology for reliable AI outputs.
metadata:
  displayName: "Prompt Engineering Guide"
  categories: ["engineering", "data"]
  tags: ["prompts", "LLM", "evaluation", "chain-of-thought", "AI", "optimization"]
  worksWellWithAgents: ["ai-engineer", "ml-engineer", "prompt-engineer"]
  worksWellWithSkills: ["experiment-design", "test-plan-writing"]
---

# Prompt Engineering Guide

## Before you start

Gather the following from the user. If anything is missing, ask before proceeding:

1. **What task should the prompt accomplish?** (Classification, generation, extraction, transformation, summarization)
2. **What model will run the prompt?** (GPT-4, Claude, Gemini, open-source — capabilities differ)
3. **What does the input look like?** (Free text, structured data, documents, code)
4. **What does the ideal output look like?** (JSON, markdown, plain text — provide 2-3 real examples)
5. **What are the failure modes?** (Hallucinations, wrong format, refusals, missing edge cases)
6. **How will you evaluate quality?** (Human review, automated checks, ground truth comparison)

## Prompt design template

### 1. Task Definition

Write a clear system prompt that defines the task, role, and constraints:

```
You are a [role] that [core task].
Your job is to [specific action] given [input description].

Rules:
- [Constraint 1: e.g., respond only in valid JSON]
- [Constraint 2: e.g., never fabricate information not in the source]
- [Constraint 3: e.g., if uncertain, say "I don't know"]

Output format:
[Exact schema or structure the model must follow]
```

Every sentence should constrain behavior or clarify expectations. Avoid vague instructions like "be helpful."

### 2. Few-Shot Examples

Include 2-5 input-output examples in the prompt. Examples teach format and edge cases more reliably than instructions alone.

```
Input: "The product crashed twice today and support hasn't responded."
Output: {"sentiment": "negative", "topics": ["reliability", "support"], "urgency": "high"}

Input: "Love the new dashboard — the filters are exactly what I needed."
Output: {"sentiment": "positive", "topics": ["dashboard", "filters"], "urgency": "low"}
```

Cover the typical case, a boundary case, and the hardest case. If the model gets the hard example right, it handles easy cases.

### 3. Chain-of-Thought Patterns

For reasoning tasks, instruct the model to show its work before answering:

- **Step-by-step:** "Think through this step by step before giving your final answer." Best for math and multi-step analysis.
- **Explain-then-answer:** "First explain your reasoning, then provide the answer on a new line starting with 'Answer:'." Best when you need to audit logic.
- **Self-critique:** "After drafting your response, review it for errors before outputting the final version." Best for generation tasks.

When chain-of-thought adds tokens without improving accuracy (simple classification), skip it.

### 4. Output Formatting

Specify the exact output structure. Ambiguity in format is the top cause of parsing failures.

```
Respond with a JSON object matching this schema exactly:
{
  "summary": "string (1-2 sentences)",
  "confidence": "number (0.0-1.0)",
  "categories": ["string array, from: billing, technical, feature-request, other"],
  "requires_escalation": "boolean"
}
Do not include any text outside the JSON object.
```

For structured outputs, provide the schema and a completed example. For free-text, specify length, tone, and inclusions/exclusions.

### 5. Evaluation Framework

Define how you will measure prompt quality before deploying. Build a test set of 20-50 examples with expected outputs.

```
| Metric              | Method                  | Pass Threshold |
|---------------------|-------------------------|----------------|
| Format compliance   | JSON schema validation  | 100%           |
| Classification acc. | Match against labels    | >90%           |
| Hallucination rate  | Human review sample     | <5%            |
| Latency (p95)       | API response time       | <3s            |
| Cost per request    | Token count * price     | <$0.02         |
```

Run the full test set after every prompt change. A prompt that improves accuracy but breaks format compliance is a regression, not an improvement.

### 6. Iteration Methodology

Follow this loop for every prompt revision:

1. **Run the current prompt** against the full test set. Record scores.
2. **Identify failure patterns.** Group errors by type: format, accuracy, hallucination, edge cases.
3. **Change one thing.** One modification per iteration — instructions, examples, or structure.
4. **Re-run the test set.** Compare scores to the previous version.
5. **Keep or revert.** If any metric degrades, revert and try a different approach.

Log every iteration: what changed, the hypothesis, and results. Prompt engineering without records is guessing.

## Quality checklist

Before delivering a prompt, verify:

- [ ] System prompt states task, role, and constraints concretely — no vague instructions
- [ ] Output format specified with a schema or example, not just described
- [ ] 2-5 few-shot examples cover typical, boundary, and difficult cases
- [ ] Chain-of-thought included only when it measurably improves accuracy
- [ ] Test set of 20+ examples exists with expected outputs
- [ ] Evaluation metrics and thresholds defined before testing begins
- [ ] Prompt tested on the target model — not assumed to transfer from another
- [ ] Token usage and cost within budget for expected volume

## Common mistakes to avoid

- **Writing instructions instead of showing examples.** When instructions and examples conflict, the model follows examples. One example teaches format better than a paragraph of description.
- **Optimizing on vibes.** "This feels better" is not evaluation. Build a test set and compare versions quantitatively.
- **Changing multiple things at once.** One change per iteration — otherwise you cannot attribute improvement or regression.
- **Ignoring model differences.** A prompt tuned for GPT-4 may underperform on Claude or Gemini. Test on the target model.
- **Skipping edge cases in examples.** Happy-path-only examples cause hallucination on unusual inputs. Include the hardest realistic cases.
- **Over-engineering simple tasks.** Start minimal and add complexity only when the test set demands it.
