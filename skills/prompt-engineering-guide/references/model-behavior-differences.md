# Model Behavior Differences for Prompt Engineering

Quick reference for how GPT-4, Claude, and Gemini differ in ways that affect prompt design. These observations reflect general tendencies as of early 2025 and may shift with model updates.

---

## Instruction Following

| Behavior | GPT-4 | Claude | Gemini |
|----------|-------|--------|--------|
| System prompt adherence | Strong. Follows system prompts reliably, including complex multi-rule instructions. | Very strong. Tends to follow system prompts closely, especially explicit constraints. | Good. Occasionally drifts from system instructions on longer outputs. |
| Output format compliance | Reliable with JSON, XML, markdown. Native JSON mode available via API. | Reliable. Follows schemas well when given an explicit example. | Generally reliable. Structured output can occasionally include preamble text. |
| Handling contradictory instructions | Tends to follow the last instruction when system and user prompts conflict. | Tends to prioritize system prompt over user prompt when they conflict. | May blend conflicting instructions rather than choosing one. |

## Reasoning and Chain-of-Thought

| Behavior | GPT-4 | Claude | Gemini |
|----------|-------|--------|--------|
| Step-by-step reasoning | Strong with explicit "think step by step" prompting. | Strong. Often reasons step-by-step without prompting, but explicit instruction improves consistency. | Good. Benefits from explicit chain-of-thought prompts. |
| Math and logic | Strong on standard problems. Can struggle with novel multi-step logic without scaffolding. | Comparable. Performs well when reasoning steps are explicit. | Strong, especially on math benchmarks. May over-simplify explanation steps. |
| Self-correction | Responds well to "review your answer for errors." | Responds well to self-critique instructions. May over-correct (add unnecessary caveats). | Less consistent with self-correction prompts. May not change its answer. |

## Safety and Refusals

| Behavior | GPT-4 | Claude | Gemini |
|----------|-------|--------|--------|
| Refusal threshold | Moderate. Refuses clearly harmful content; occasional false positives on edge cases. | Conservative on some topics. More likely to add safety caveats or decline borderline requests. | Moderate to conservative. Refusal patterns vary by topic. |
| Workaround for false refusals | Rephrase the task in professional/academic framing. Provide explicit context for why the request is legitimate. | Provide clear context in the system prompt explaining the legitimate use case. Direct, professional framing helps. | Rephrase with explicit professional context. |

## Output Style

| Behavior | GPT-4 | Claude | Gemini |
|----------|-------|--------|--------|
| Default verbosity | Moderate. Tends toward thorough but structured responses. | Tends toward longer, more detailed responses. Explicit length constraints help. | Moderate. Can be concise or verbose depending on prompt. |
| Tone | Neutral-professional by default. Adjusts well to tone instructions. | Slightly more conversational by default. Adjusts well to formal tone instructions. | Neutral. Adjusts to tone instructions but may revert on long outputs. |
| Lists and structure | Uses bullet points and headers readily. | Uses bullet points and headers readily. May over-structure simple responses. | Uses structure but sometimes produces wall-of-text for complex topics. |
| Hedging | Moderate hedging ("it's worth noting," "however"). | Higher tendency to hedge and add caveats ("it's important to note," "I should mention"). Reduce with explicit "be direct" instructions. | Low to moderate hedging. |

## Context Window and Long Inputs

| Behavior | GPT-4 | Claude | Gemini |
|----------|-------|--------|--------|
| Effective context use | Good across the window. Some degradation for information buried in the middle of very long contexts. | Strong long-context performance. Handles document-length inputs well. | Very large context window (up to 1M+ tokens). Good retrieval but can lose precision on dense documents. |
| Document Q&A | Reliable extraction from provided documents. | Strong. Tends to quote sources from the provided context. | Good. May paraphrase more than quote directly. |

## Practical Prompt Engineering Tips by Model

### GPT-4

- Use JSON mode (`response_format: { type: "json_object" }`) for structured output instead of relying on prompt instructions alone.
- Place the most important instructions at the beginning and end of the system prompt (middle content gets less attention in very long prompts).
- For complex tasks, use numbered step instructions rather than paragraph descriptions.

### Claude

- Put behavioral constraints in the system prompt rather than the user message --- Claude prioritizes system prompt instructions.
- Explicitly state "Be direct. Do not add caveats or hedging." if you want concise output.
- Use XML tags (`<input>`, `<output>`, `<instructions>`) to structure complex prompts --- Claude responds well to XML-delimited sections.
- For extraction tasks, instruct "Quote directly from the source" to reduce paraphrasing.

### Gemini

- Use explicit output format examples rather than schema descriptions alone.
- For long documents, place the question/instruction after the document content (recency effect).
- Add "Do not include any text outside the requested format" to prevent preamble/postamble in structured outputs.
- Test with both short and long inputs --- behavior can differ significantly by input length.

---

## When to Test Across Models

Always test your prompt on the target model. Cross-model testing is useful when:

- You are building a product that may switch providers.
- You want to verify that your prompt captures the task correctly (not just exploits one model's quirks).
- You are evaluating cost/performance tradeoffs (a simpler model with a better prompt may beat a frontier model with a generic prompt).

A prompt that requires model-specific tricks is fragile. Prefer prompts that work across models when possible, and document model-specific optimizations separately.
