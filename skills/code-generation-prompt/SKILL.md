---
name: code-generation-prompt
description: Step-by-step prompt engineering template for generating production-quality code from requirements — covering input gathering, constraint specification, output formatting, and iterative refinement.
metadata:
  displayName: "Code Generation Prompt"
  categories: ["engineering"]
  tags: ["code-generation", "prompt-engineering", "ai-prompts", "templates"]
  worksWellWithAgents: ["code-generator", "prompt-engineer", "vibe-coder"]
  worksWellWithSkills: ["prd-writing", "technical-spec-writing"]
---

# Code Generation Prompt

## Before you start

Gather the following from the user before generating any code:

1. **What does the code need to do?** — Specific behavior, not vague goals
2. **What language and framework?** — Including version constraints
3. **What are the inputs and outputs?** — Data types, formats, example values
4. **What are the constraints?** — Performance requirements, dependencies allowed, compatibility targets
5. **Where does this code live?** — Standalone script, library function, API endpoint, UI component
6. **Are there existing patterns to follow?** — Link to existing code in the repo or style guide

If any of these are missing, ask before proceeding. Generating code from incomplete requirements produces throwaway output.

## Procedure

### 1. Define the requirement in structured form

Write the requirement as a structured block before generating code. This prevents drift between what was asked and what gets built.

```
TASK: [one sentence describing the function]
LANGUAGE: [language + version]
FRAMEWORK: [framework + version, or "none"]
INPUTS: [list each input with type and example value]
OUTPUTS: [return type with example value]
CONSTRAINTS: [performance, security, compatibility requirements]
ERROR CASES: [what should happen when inputs are invalid]
```

### 2. Choose the generation strategy

Select one based on complexity:

- **Direct generation** — For isolated functions under 50 lines. Write the full implementation in one pass.
- **Scaffold-then-fill** — For modules with multiple functions. Generate the interface (function signatures, types, exports) first, then implement each function.
- **Test-first generation** — For logic-heavy code. Generate test cases from the requirements first, then write the implementation to pass them.

### 3. Write the prompt

Structure the prompt in this order:

1. **Role and context** — What the code is part of, what conventions to follow
2. **Exact task** — What to implement, referencing the structured requirement
3. **Input/output contract** — Types, validation rules, example values
4. **Constraints** — What NOT to do (no external dependencies, no async, no mutation, etc.)
5. **Output format** — Single file, multiple files, include tests, include types

### 4. Generate and validate

After receiving generated code:

1. Read the code line by line — do not assume correctness
2. Verify every input is validated before use
3. Verify every error case from the requirement is handled
4. Check that no hallucinated imports or APIs are referenced
5. Run the code or tests if possible

### 5. Iterate with targeted follow-ups

If the output needs changes, do not re-prompt from scratch. Use targeted corrections:

- "The function handles the happy path but does not validate that `email` is non-empty. Add input validation for all string parameters."
- "Replace the `lodash.groupBy` dependency with a native `Object.groupBy` or manual reduce."
- "The error messages are generic. Use specific messages: 'Email is required', 'Email must contain @'."

## Prompt templates

### Template A: Standalone function

```
Write a [LANGUAGE] function called [NAME] that:
- Takes: [PARAM1: TYPE], [PARAM2: TYPE]
- Returns: [RETURN_TYPE]
- Behavior: [EXACT DESCRIPTION]
- Edge cases: [LIST EACH CASE AND EXPECTED BEHAVIOR]
- Do not use external dependencies.
- Include JSDoc/docstring with parameter descriptions.
```

### Template B: API endpoint

```
Write a [FRAMEWORK] [METHOD] endpoint at [PATH] that:
- Accepts: [REQUEST BODY/PARAMS SCHEMA]
- Returns: [RESPONSE SCHEMA] with status [CODE]
- Validation: [RULES FOR EACH FIELD]
- Error responses: [STATUS CODE + BODY FOR EACH ERROR CASE]
- Authentication: [REQUIRED/OPTIONAL, METHOD]
- Follow the existing patterns in [REFERENCE FILE].
```

### Template C: UI component

```
Write a [FRAMEWORK] component called [NAME] that:
- Props: [LIST EACH PROP WITH TYPE AND DEFAULT]
- Renders: [DESCRIBE THE VISUAL OUTPUT]
- Interactions: [CLICK, HOVER, FOCUS BEHAVIORS]
- States: loading, error, empty, populated
- Accessibility: [ARIA LABELS, KEYBOARD NAVIGATION]
- Use [STYLING APPROACH] for styles.
```

## Quality checklist

Before delivering generated code, verify:

- [ ] Every input from the requirement is used in the implementation
- [ ] Every output matches the specified type and format
- [ ] Error cases are handled with specific messages, not silent failures
- [ ] No hallucinated imports — every dependency actually exists
- [ ] No hardcoded values that should be parameters or constants
- [ ] Code follows the language's naming conventions and idioms
- [ ] The code is readable without the prompt — someone seeing it for the first time can understand it

## Common mistakes

- **Prompting with vague requirements.** "Write a function that processes data" produces useless code. Specify exact inputs, outputs, and edge cases.
- **Accepting generated code without reading it.** AI-generated code compiles but may contain subtle logic errors, hallucinated APIs, or security gaps. Read every line.
- **Over-constraining the prompt.** Specifying implementation details (use a for loop, use reduce) instead of behavior leads to awkward code. Specify WHAT, not HOW.
- **Ignoring the iteration step.** First-pass generation is rarely production-ready. Plan for 2-3 rounds of targeted refinement.
- **Skipping error handling in the prompt.** If the prompt does not mention error cases, the generated code will not handle them. Always specify what happens when things go wrong.
- **Not including examples.** One concrete input/output example in the prompt eliminates more ambiguity than three sentences of description.
