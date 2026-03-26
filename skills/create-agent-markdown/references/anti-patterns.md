# Anti-Patterns in Agent Definitions

Common mistakes that make agent definitions generic, unhelpful, or ineffective — and how to fix them.

## 1. Job description, not persona

**The problem:** The definition reads like an HR job posting — lists of responsibilities without establishing how the agent *thinks*.

**Before (bad):**
```markdown
You are responsible for:
- Code reviews
- Security assessments
- Performance optimization
- Mentoring junior developers
```

**After (good):**
```markdown
You are a senior code reviewer with the rigor and judgment of a staff
engineer who has seen thousands of pull requests. You care deeply about
correctness, security, and maintainability — in that order.
```

**Why it matters:** The bad version tells the model WHAT to do. The good version tells it HOW to think. LLMs already know what code review is — they need the opinionated perspective.

## 2. Generic advice

**The problem:** Phrases like "be thorough," "ensure quality," "follow best practices" add zero information. Every role should be thorough. This is noise.

**Red flag phrases to eliminate:**
- "Ensure quality and consistency"
- "Be thorough in your analysis"
- "Follow industry best practices"
- "Provide comprehensive feedback"
- "Maintain high standards"
- "Use appropriate tools and techniques"

**Fix:** Replace each with a SPECIFIC principle. "Be thorough" becomes "Check the data flow from input to output. Where does user input enter? How is it validated?"

## 3. Feature list

**The problem:** Describes the agent like a product marketing page — what it CAN do, not how it BEHAVES.

**Before (bad):**
```markdown
## What This Agent Does
- Reviews code for bugs and security issues
- Provides actionable feedback
- Supports multiple programming languages
- Integrates with CI/CD pipelines
```

**After (good):**
```markdown
## Your review philosophy
- **Correctness first**. Does the code do what it claims?
  Logic errors, race conditions, unhandled edge cases.
- **Security second**. Injection, auth bypasses, data exposure?
  You treat security issues as blockers, never suggestions.
```

**Why it matters:** The "feature list" format is for humans choosing a tool. The agent needs behavioral guidance, not marketing copy.

## 4. Missing boundaries

**The problem:** The agent tries to be everything. Without "refuse to do" constraints, it over-extends into areas where its persona isn't strong, producing mediocre output.

**Fix:** Every agent should have 3-5 clear refusals. Each refusal should name what the agent DOESN'T do and redirect to what it DOES.

## 5. Flat structure

**The problem:** All concerns are at the same priority level. The model can't tell what matters most.

**Before (bad):**
```markdown
When reviewing code, check for:
- Bugs
- Security issues
- Style violations
- Test coverage
- Documentation
- Performance
- Accessibility
```

**After (good):**
```markdown
## Your review philosophy
1. **Correctness first** — logic errors, race conditions
2. **Security second** — vulnerabilities are blockers
3. **Maintainability third** — readability in 6 months
4. **Style last** — defer to linter if one exists
```

**Why it matters:** Prioritization IS the expertise. Anyone can list things to check. A senior reviewer knows correctness matters more than style.

## 6. Over-engineering

**The problem:** 200+ lines of exhaustive rules, edge cases, and exceptions. The model can't meaningfully follow all of it, and the important signals get lost in noise.

**The research says:** Anthropic's guidance explicitly recommends "the minimal set of information that fully outlines your expected behavior." Keep agent bodies to 60-120 lines. Above that, you're either including filler or trying to cover too many scenarios.

**Fix:** If your definition exceeds 120 lines, split it:
- Core behavioral prompt stays in the body (60-120 lines)
- Detailed checklists, reference material, or extended scenarios go in supporting files

## 7. Persona without substance

**The problem:** Assigns a persona ("You are a world-class security expert") without backing it up with domain-specific knowledge. Research shows demographics-only personas explain ~1.5% of behavioral variance. The expertise content is what drives quality.

**Before (bad):**
```markdown
You are a world-class security expert with decades of experience.
You are extremely thorough and always find vulnerabilities.
```

**After (good):**
```markdown
You are a security auditor who thinks like an attacker first, then a defender.

For every change, you check:
- [ ] User input is validated and sanitized before use
- [ ] SQL queries use parameterized statements
- [ ] Auth is enforced at the right layer
- [ ] Sensitive data is not logged or exposed in errors
```

**Why it matters:** "World-class expert" is empty. The checklist IS the expertise.
