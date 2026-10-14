# Contributing

Thanks for considering a contribution!

## Setup

```bash
git clone https://github.com/Mo-Sa-2004/Python.git
cd Python
pip install -e .
pip install -r requirements-dev.txt
```

## Before opening a pull request

```bash
pytest -v --cov=ip_validator --cov-report=term-missing
ruff check .
mypy ip_validator.py
```

All three run in CI on every push and pull request, so a PR that fails
any of them won't be mergeable as-is. If you add new behavior, please
add a test for it alongside the change - that's true for both the
library functions and the CLI (`test_ip_validator.py` and `test_cli.py`
respectively).

## Reporting a bug

Please include the exact input that triggers it and what you expected
vs. what actually happened. A short reproduction (even a one-line
`python3 -c "..."` call) is the fastest way to get it fixed.