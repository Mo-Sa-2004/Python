# Changelog

All notable changes to this project are documented here.

## [Unreleased]

### Fixed

- **`validate_ipv6` rejected standard compressed IPv6 addresses.** The
  original regex only matched the fully-expanded, 8-group form, so
  everyday addresses like `::1` (loopback), `::` (unspecified), and
  `fe80::1` (link-local) were incorrectly reported as invalid.
  `validate_ipv6` now delegates to Python's standard `ipaddress` module,
  which correctly handles RFC 4291 `::` zero-compression.
- **`get_ip_info` mislabeled loopback and reserved addresses as "Class
  E (Experimental)".** `127.0.0.1` was returned with `class: "E
  (Experimental)"` while simultaneously flagged `is_loopback: True` -
  a contradiction. `127.0.0.0/8` is now reported as `"A (Loopback)"`
  and `0.0.0.0/8` as `"Reserved (0.0.0.0/8)"`; genuine Class E
  (`240.0.0.0` - `255.255.255.255`) is unaffected.
- `requirements.txt` listed `pandas` as a dependency even though it is
  never imported anywhere in the codebase. Removed it; `pytest` (only
  needed to run the test suite, not to use the library) moved to a new
  `requirements-dev.txt`.
- `LICENSE` had a malformed copyright symbol (`(x)` instead of `(c)`),
  an out-of-date author name, and was missing the standard MIT
  warranty disclaimer paragraph.
- **`validate_ip` accepted non-ASCII Unicode decimal digits** (e.g.
  full-width Unicode digits) as IPv4 octets, silently normalizing a lookalike
  string into a real address. Only plain ASCII `0`-`9` is accepted now.
- A real `mypy` type-narrowing issue in the new CLI's `main()` (see
  below), where the type checker couldn't prove `get_ip_info` had
  already returned non-`None` after a successful `validate_ip` check.

### Added

- GitHub Actions CI running the test suite on every push and pull
  request, across Python 3.9-3.12.
- Regression tests for the IPv6 and classification fixes above.
- `is_link_local` (169.254.0.0/16), `is_cgnat` (100.64.0.0/10), and
  `is_multicast` (224.0.0.0/4) flags on `get_ip_info`, consistent with
  the existing `is_private`/`is_loopback` booleans. `is_reserved`
  covers 0.0.0.0/8 and 240.0.0.0/4.
- `pyproject.toml` packaging - the project is now pip-installable
  (`pip install -e .`) and exposes an `ip-validator` CLI command.
- Ruff linting and mypy type-checking, both run in CI; the 3 lint
  issues and 1 type issue they found on first run are fixed.
- `pytest-cov` coverage reporting (99%, enforced at a 90% minimum in
  CI) and a new `test_cli.py` covering the CLI end to end.
- `CONTRIBUTING.md`.