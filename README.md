# Python IP Address Validator Utility

[![Tests](https://github.com/Mo-Sa-2004/Python/actions/workflows/tests.yml/badge.svg)](https://github.com/Mo-Sa-2004/Python/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A lightweight, dependency-free Python library for validating IPv4/IPv6 addresses and extracting network metadata.

## Features

- Validate IPv4 address format and boundary range [0, 255].
- Enforce strict octet formatting (disallows leading zeros).
- Validate full IPv6 format, including the compressed `::` notation
  (e.g. `::1`, `fe80::1`) as defined by RFC 4291.
- Extract IP class, binary representation, and private/loopback flags.

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
#   'octets': [192, 168, 1, 1],
#   'binary': '11000000.10101000.00000001.00000001'
# }

# 127.0.0.1 is correctly reported as loopback, not Class E
print(get_ip_info("127.0.0.1")["class"])  # 'A (Loopback)'
```

## Installation

This library has no runtime dependencies - just copy `ip_validator.py` into
your project, or clone the repo:

```bash
git clone https://github.com/Mo-Sa-2004/Python.git
```

## Running the tests

```bash
pip install -r requirements-dev.txt
pytest -v
```

Tests run automatically in GitHub Actions on every push and pull request.

## License

[MIT](LICENSE) - see [CHANGELOG.md](CHANGELOG.md) for version history.
