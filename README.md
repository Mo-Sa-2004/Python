# Python IP Address Validator Utility

[![Tests](https://github.com/Mo-Sa-2004/Python/actions/workflows/tests.yml/badge.svg)](https://github.com/Mo-Sa-2004/Python/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)

A lightweight, dependency-free Python library for validating IPv4/IPv6 addresses and extracting network metadata.

## Features

- Validate IPv4 address format and boundary range [0, 255], using only
  plain ASCII digits (lookalike Unicode digits are rejected).
- Enforce strict octet formatting (disallows leading zeros).
- Validate full IPv6 format, including the compressed `::` notation
  (e.g. `::1`, `fe80::1`) as defined by RFC 4291.
- Extract IP class, binary representation, and private/loopback/
  link-local/CGNAT/multicast/reserved flags.
- A small CLI (`ip-validator`) for checking an address from the terminal.

## Usage

```python
from ip_validator import validate_ip, validate_ipv6, get_ip_info

# Validate IPv4
print(validate_ip("192.168.1.1"))  # True
print(validate_ip("192.168.01.1")) # False (leading zero)

# Validate IPv6 - compressed "::" addresses are supported
print(validate_ipv6("2001:0db8:85a3:0000:0000:8a2e:0370:7334")) # True
print(validate_ipv6("::1"))  # True (loopback)
print(validate_ipv6("fe80::1"))  # True (link-local)

# Get IP Metadata
info = get_ip_info("192.168.1.1")
print(info)
# Output:
# {
#   'ip': '192.168.1.1',
#   'valid': True,
#   'class': 'C',
#   'is_private': True,
#   'is_loopback': False,
#   'is_link_local': False,
#   'is_cgnat': False,
#   'is_multicast': False,
#   'is_reserved': False,
#   'octets': [192, 168, 1, 1],
#   'binary': '11000000.10101000.00000001.00000001'
# }

# 127.0.0.1 is correctly reported as loopback, not Class E
print(get_ip_info("127.0.0.1")["class"])  # 'A (Loopback)'
```

## Installation

This library has no runtime dependencies. Either copy `ip_validator.py`
into your project, or install it as a package (adds the `ip-validator`
command):

```bash
git clone https://github.com/Mo-Sa-2004/Python.git
cd Python
pip install -e .
```

## Command-line use

```bash
ip-validator 192.168.1.1
ip-validator 169.254.1.1 --json
ip-validator ::1
```

An invalid address exits with a non-zero status and an error on stderr,
so it's safe to use in scripts.

## Running the tests

```bash
pip install -r requirements-dev.txt
pytest -v --cov=ip_validator --cov-report=term-missing
ruff check .
mypy ip_validator.py
```

All three (tests + coverage, lint, type-checking) run automatically in
GitHub Actions on every push and pull request. See
[CONTRIBUTING.md](CONTRIBUTING.md) if you'd like to submit a PR.

## License

[MIT](LICENSE) - see [CHANGELOG.md](CHANGELOG.md) for version history.