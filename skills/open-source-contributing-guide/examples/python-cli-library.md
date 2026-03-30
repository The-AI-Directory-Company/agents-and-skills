# Example: Python CLI Library Project

A complete contributing setup for a Python CLI library using modern tooling: pyproject.toml, pytest, ruff, and pre-commit hooks.

---

## Project Structure

```
my-cli-tool/
├── src/
│   └── my_cli_tool/
│       ├── __init__.py
│       ├── cli.py
│       └── core.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_cli.py
│   └── test_core.py
├── pyproject.toml
├── .pre-commit-config.yaml
├── .github/
│   └── workflows/
│       └── ci.yml
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

---

## pyproject.toml

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "my-cli-tool"
version = "0.1.0"
description = "A CLI tool that does useful things"
readme = "README.md"
license = "MIT"
requires-python = ">=3.11"
authors = [
    { name = "Your Name", email = "you@example.com" },
]
dependencies = [
    "click>=8.1",
    "httpx>=0.27",
]

[project.scripts]
my-cli-tool = "my_cli_tool.cli:main"

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov>=5.0",
    "ruff>=0.4",
    "pre-commit>=3.7",
    "mypy>=1.10",
]

[tool.ruff]
target-version = "py311"
line-length = 100

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes
    "I",    # isort
    "N",    # pep8-naming
    "UP",   # pyupgrade
    "B",    # flake8-bugbear
    "SIM",  # flake8-simplify
    "TCH",  # flake8-type-checking
    "RUF",  # ruff-specific rules
]
ignore = [
    "E501",  # line too long (handled by formatter)
]

[tool.ruff.lint.isort]
known-first-party = ["my_cli_tool"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=my_cli_tool --cov-report=term-missing --strict-markers"

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
```

---

## .pre-commit-config.yaml

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: ['--maxkb=500']
      - id: check-merge-conflict

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.8
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.10.0
    hooks:
      - id: mypy
        additional_dependencies: [click, httpx]
```

---

## CI Workflow (.github/workflows/ci.yml)

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev]"

      - name: Lint (ruff check)
        run: ruff check .

      - name: Format check (ruff format)
        run: ruff format --check .

      - name: Type check (mypy)
        run: mypy src/

      - name: Test (pytest)
        run: pytest --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          file: coverage.xml
```

---

## Test Examples

### conftest.py

```python
import pytest
from click.testing import CliRunner


@pytest.fixture
def cli_runner():
    """Click CLI test runner."""
    return CliRunner()


@pytest.fixture
def mock_api(httpx_mock):
    """Pre-configured mock for the external API."""
    httpx_mock.add_response(
        url="https://api.example.com/v1/data",
        json={"data": [{"id": 1, "name": "Test"}]},
    )
    return httpx_mock
```

### test_cli.py

```python
from my_cli_tool.cli import main


def test_cli_version(cli_runner):
    result = cli_runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.output


def test_cli_help(cli_runner):
    result = cli_runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output


def test_cli_fetch_command(cli_runner, mock_api):
    result = cli_runner.invoke(main, ["fetch", "--limit", "10"])
    assert result.exit_code == 0
    assert "Test" in result.output


def test_cli_invalid_option(cli_runner):
    result = cli_runner.invoke(main, ["--nonexistent"])
    assert result.exit_code != 0
```

### test_core.py

```python
import pytest
from my_cli_tool.core import parse_response, validate_input


class TestParseResponse:
    def test_valid_response(self):
        raw = {"data": [{"id": 1, "name": "Alice"}], "meta": {"total": 1}}
        result = parse_response(raw)
        assert len(result) == 1
        assert result[0]["name"] == "Alice"

    def test_empty_response(self):
        raw = {"data": [], "meta": {"total": 0}}
        result = parse_response(raw)
        assert result == []

    def test_missing_data_key(self):
        with pytest.raises(KeyError):
            parse_response({"meta": {"total": 0}})


class TestValidateInput:
    @pytest.mark.parametrize("value,expected", [
        ("valid@email.com", True),
        ("not-an-email", False),
        ("", False),
    ])
    def test_email_validation(self, value, expected):
        assert validate_input(value, "email") == expected
```

---

## Development Setup Instructions

Include these in `CONTRIBUTING.md`:

```markdown
## Development Setup

### Prerequisites
- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### Steps

1. Fork and clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/my-cli-tool.git
   cd my-cli-tool
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e ".[dev]"
   ```

3. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

4. Verify the setup works:
   ```bash
   pytest                  # Run tests
   ruff check .            # Lint
   ruff format --check .   # Format check
   mypy src/               # Type check
   ```

   All four commands should pass with no errors.

### Common Issues

| Error | Fix |
|-------|-----|
| `ModuleNotFoundError: my_cli_tool` | Run `pip install -e ".[dev]"` (editable install) |
| `ruff: command not found` | Activate the virtual environment first |
| Pre-commit hook fails on first run | Run `pre-commit run --all-files` once to initialize |
| mypy reports missing stubs | Run `mypy --install-types` |

---

## Commit Message Convention

```
feat(cli): add --format flag for JSON output
fix(core): handle empty API response without crashing
docs: update installation instructions for Windows
test: add edge case tests for pagination
refactor(core): extract HTTP client into separate module
chore: update ruff to v0.5
```

Format: `<type>(<scope>): <description>`

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `ci`
