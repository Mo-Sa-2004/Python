# Python IP Address Validator Utility

A lightweight, zero-dependency Python utility and library for validating IPv4 and IPv6 addresses, validating CIDR notation, and extracting network metadata.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)

## Features

- **IPv4 Validation:** Checks standard dotted-decimal format (`0.0.0.0`–`255.255.255.255`) and enforces strict octet rules (disallows leading zeros like `192.168.01.1`).
- **IPv6 Validation:** Supports standard and compressed IPv6 formats (including double-colon `::` notation).
- **CIDR Notation Parsing:** Validates IP addresses paired with subnet prefixes (e.g., `192.168.1.0/24` or `2001:db8::/32`).
- **Zero External Dependencies:** Built using Python standard libraries for maximum portability.
- **Unit Tested:** Includes comprehensive unit tests covering valid, invalid, and edge-case inputs.

---

## Project Structure

```text
.
├── .gitignore
├── LICENSE
├── README.md
├── ip_validator.py       # Core IP validation module
├── requirements.txt      # Dependency configurations
└── test_ip_validator.py  # Comprehensive test suite
