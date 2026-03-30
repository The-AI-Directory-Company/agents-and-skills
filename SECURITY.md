# Security Policy

## Scope

This repository contains markdown content (agent definitions and skill procedures) as well as executable helper scripts (primarily Python) bundled within skills. These scripts are designed to be invoked by AI agents as part of skill workflows — they are not standalone application services.

Security concerns for this project relate to:

- **Content integrity** — Ensuring contributed agents/skills do not contain instructions that could cause harm when used by AI systems
- **Script safety** — Ensuring executable files bundled with skills (e.g. `scripts/*.py`) do not perform destructive operations, exfiltrate data, or establish unauthorized network connections. Scripts should process input and write output without side effects beyond their stated purpose
- **Supply chain** — Ensuring the CI/CD pipeline and GitHub Actions are not compromised
- **Credentials** — Ensuring no secrets, API keys, or private data are committed. Scripts must accept credentials via agent-provided tools or environment variables, never hardcoded

## Executable Scripts in Skills

Skills may include helper scripts (typically Python) under a `scripts/` directory. These scripts serve as tools that AI agents call during skill execution — for example, parsing SERP data, validating structured markup, or scoring content quality.

**What reviewers should verify for contributed scripts:**

1. **No embedded credentials** — Scripts must not contain API keys, tokens, or secrets
2. **No persistent state** — Scripts should read input (stdin, arguments, or files) and write output (stdout or JSON). They should not create databases, write to unexpected locations, or maintain hidden state
3. **No unauthorized network access** — Network calls should be limited to the script's stated purpose (e.g. fetching a URL for analysis). Scripts must not phone home, upload telemetry, or contact undisclosed endpoints
4. **No system modification** — Scripts must not install packages, modify system files, or alter the host environment beyond their declared output
5. **Transparent dependencies** — Any required Python packages should be documented in the skill's references or the script itself

## Reporting

If you discover a security concern, please email **security@ai-directory.company** rather than opening a public issue.

We will acknowledge receipt within 48 hours and provide a detailed response within 5 business days.

## Supported Versions

| Branch | Supported |
| ------ | --------- |
| `main` | Yes       |
| Other  | No        |
