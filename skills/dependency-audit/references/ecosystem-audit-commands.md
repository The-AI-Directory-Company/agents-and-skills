# Ecosystem Audit Commands Reference

Per-ecosystem commands for security auditing, outdated package detection, and license checking. Each section lists the tool, install command, usage, and output format.

---

## Node.js (npm / yarn / pnpm)

### Security audit

| Tool | Command | Install |
|------|---------|---------|
| npm audit | `npm audit` | Built-in (npm >= 6) |
| npm audit (JSON) | `npm audit --json` | Built-in |
| npm audit (fix) | `npm audit fix` | Built-in |
| yarn audit | `yarn audit` | Built-in (yarn v1) |
| pnpm audit | `pnpm audit` | Built-in (pnpm >= 7) |

**Output format (npm audit --json):**
```json
{
  "vulnerabilities": {
    "package-name": {
      "name": "package-name",
      "severity": "high",
      "via": ["CVE-2024-XXXXX"],
      "range": ">=1.0.0 <1.2.3",
      "fixAvailable": { "name": "package-name", "version": "1.2.3" }
    }
  },
  "metadata": {
    "vulnerabilities": { "critical": 0, "high": 2, "moderate": 5, "low": 3, "total": 10 }
  }
}
```

### Outdated packages

| Tool | Command | Output |
|------|---------|--------|
| npm outdated | `npm outdated` | Table: current, wanted, latest |
| npm outdated (JSON) | `npm outdated --json` | JSON with current/wanted/latest per package |
| yarn outdated | `yarn outdated` | Table format |
| pnpm outdated | `pnpm outdated` | Table format |

### License checking

| Tool | Command | Install |
|------|---------|---------|
| license-checker | `license-checker --summary` | `npm install -g license-checker` |
| license-checker (JSON) | `license-checker --json` | Same |
| license-checker (CSV) | `license-checker --csv --out licenses.csv` | Same |
| license-checker (fail) | `license-checker --failOn 'GPL-3.0'` | Same |

---

## Python (pip / poetry / uv)

### Security audit

| Tool | Command | Install |
|------|---------|---------|
| pip-audit | `pip-audit` | `pip install pip-audit` |
| pip-audit (JSON) | `pip-audit --format json` | Same |
| pip-audit (requirements) | `pip-audit -r requirements.txt` | Same |
| safety | `safety check` | `pip install safety` |
| safety (JSON) | `safety check --json` | Same |

**Output format (pip-audit --format json):**
```json
{
  "dependencies": [
    {
      "name": "requests",
      "version": "2.25.0",
      "vulns": [
        {
          "id": "PYSEC-2024-XXXXX",
          "fix_versions": ["2.31.0"],
          "description": "..."
        }
      ]
    }
  ]
}
```

### Outdated packages

| Tool | Command | Output |
|------|---------|--------|
| pip list | `pip list --outdated` | Table: package, version, latest |
| pip list (JSON) | `pip list --outdated --format json` | JSON array |
| poetry show | `poetry show --outdated` | Table format |

### License checking

| Tool | Command | Install |
|------|---------|---------|
| pip-licenses | `pip-licenses` | `pip install pip-licenses` |
| pip-licenses (JSON) | `pip-licenses --format json` | Same |
| pip-licenses (table) | `pip-licenses --format markdown` | Same |
| pip-licenses (fail) | `pip-licenses --fail-on 'GPL-3.0'` | Same |

---

## Rust (cargo)

### Security audit

| Tool | Command | Install |
|------|---------|---------|
| cargo-audit | `cargo audit` | `cargo install cargo-audit` |
| cargo-audit (JSON) | `cargo audit --json` | Same |
| cargo-deny | `cargo deny check advisories` | `cargo install cargo-deny` |

**Output format (cargo audit --json):**
```json
{
  "vulnerabilities": {
    "found": 2,
    "list": [
      {
        "advisory": {
          "id": "RUSTSEC-2024-XXXX",
          "package": "crate-name",
          "title": "...",
          "severity": "HIGH"
        },
        "versions": {
          "patched": [">=1.2.3"]
        }
      }
    ]
  }
}
```

### Outdated packages

| Tool | Command | Install |
|------|---------|---------|
| cargo outdated | `cargo outdated` | `cargo install cargo-outdated` |
| cargo outdated (root) | `cargo outdated --root-deps-only` | Same |

### License checking

| Tool | Command | Install |
|------|---------|---------|
| cargo-license | `cargo license` | `cargo install cargo-license` |
| cargo-deny (licenses) | `cargo deny check licenses` | `cargo install cargo-deny` |

`cargo-deny` is the most comprehensive tool for Rust — it checks advisories, licenses, bans, and sources in a single config file (`deny.toml`).

---

## Go

### Security audit

| Tool | Command | Install |
|------|---------|---------|
| govulncheck | `govulncheck ./...` | `go install golang.org/x/vuln/cmd/govulncheck@latest` |
| govulncheck (JSON) | `govulncheck -json ./...` | Same |

**Key behavior:** `govulncheck` analyzes which vulnerable functions are actually called in your code, not just which packages are imported. This produces fewer false positives than other ecosystems.

### Outdated packages

| Tool | Command | Install |
|------|---------|---------|
| go list | `go list -m -u all` | Built-in |
| go-mod-outdated | `go list -m -u -json all \| go-mod-outdated` | `go install github.com/psampaz/go-mod-outdated@latest` |

### License checking

| Tool | Command | Install |
|------|---------|---------|
| go-licenses | `go-licenses check ./...` | `go install github.com/google/go-licenses@latest` |
| go-licenses (csv) | `go-licenses csv ./...` | Same |

---

## Java (Maven / Gradle)

### Security audit

| Tool | Command | Install |
|------|---------|---------|
| OWASP Dependency-Check (Maven) | `mvn dependency-check:check` | Add plugin to `pom.xml` |
| OWASP Dependency-Check (Gradle) | `gradle dependencyCheckAnalyze` | Add plugin to `build.gradle` |
| OWASP (HTML report) | Report at `target/dependency-check-report.html` | — |

**Maven plugin config:**
```xml
<plugin>
  <groupId>org.owasp</groupId>
  <artifactId>dependency-check-maven</artifactId>
  <version>9.0.9</version>
  <configuration>
    <failBuildOnCVSS>7</failBuildOnCVSS>
  </configuration>
</plugin>
```

### Outdated packages

| Tool | Command | Output |
|------|---------|--------|
| Maven versions | `mvn versions:display-dependency-updates` | Console output |
| Gradle versions | `gradle dependencyUpdates` | Requires `com.github.ben-manes.versions` plugin |

### License checking

| Tool | Command | Install |
|------|---------|---------|
| Maven license plugin | `mvn license:aggregate-third-party-report` | `org.codehaus.mojo:license-maven-plugin` |
| Gradle license report | `gradle generateLicenseReport` | `com.github.jk1.dependency-license-report` plugin |

---

## CI Integration Pattern

For any ecosystem, the CI audit step follows the same structure:

```yaml
# Generic pattern — adapt tool names per ecosystem
audit:
  steps:
    - name: Install dependencies
      run: <install-command>

    - name: Security audit
      run: <audit-command> --json > audit-results.json
      continue-on-error: true  # Don't fail yet — triage first

    - name: Check for critical vulns
      run: |
        # Parse JSON, fail only on critical/high
        <parse-and-threshold-command>

    - name: License check
      run: <license-command> --failOn 'GPL-3.0,AGPL-3.0'

    - name: Upload report
      uses: actions/upload-artifact@v4
      with:
        name: audit-report
        path: audit-results.json
```
