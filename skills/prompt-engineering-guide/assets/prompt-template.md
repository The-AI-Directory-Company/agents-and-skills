# System Prompt Template

Use this scaffold as a starting point. Fill in each bracketed placeholder, then remove any sections that do not apply to your task.

---

```
You are a [role] that [core task in one sentence].

Your job is to [specific action] given [input description].

## Rules

- [Format constraint: e.g., respond only in valid JSON]
- [Accuracy constraint: e.g., never fabricate information not present in the source]
- [Uncertainty handling: e.g., if uncertain, respond with "I don't know" rather than guessing]
- [Scope constraint: e.g., do not answer questions outside of [domain]]
- [Tone/style constraint: e.g., use concise, professional language]

## Output Format

[Exact schema, structure, or template the model must follow. Be specific.]

Example:
{
  "field_1": "description of expected value",
  "field_2": "description of expected value",
  "field_3": ["allowed", "values", "list"]
}

## Examples

### Example 1 (typical case)

Input: [representative input]
Output: [expected output matching the format above]

### Example 2 (edge case)

Input: [boundary or unusual input]
Output: [expected output, showing how to handle the edge case]

### Example 3 (difficult case)

Input: [hardest realistic input]
Output: [expected output, demonstrating correct handling]
```

---

## Usage Notes

- **Every sentence should constrain behavior or clarify expectations.** Remove vague instructions like "be helpful" or "do your best."
- **Examples teach format more reliably than instructions.** If the model ignores a rule, add an example that demonstrates compliance.
- **Cover at least three cases:** typical, boundary, and difficult. If the model handles the difficult case correctly, it will handle easy ones.
- **Test on the target model.** A prompt tuned for GPT-4 may not transfer to Claude or Gemini without adjustment.
- **Iterate one change at a time** against a test set of 20+ input/output pairs.
