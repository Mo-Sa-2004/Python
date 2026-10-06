# Python IP Address Validator Utility

A lightweight, dependency-free Python library for validating IPv4/IPv6 addresses and extracting network metadata.

## Features

- Validate IPv4 address format and boundary range [0, 255].
- Enforce strict octet formatting (disallows leading zeros).
- Validate full IPv6 format.
- Extract IP class, binary representations, and private/loopback flags.

## Usage

```python
from ip_validator import validate_ip, validate_ipv6, get_ip_info

# Validate IPv4
print(validate_ip("192.168.1.1"))  # True
print(validate_ip("192.168.01.1")) # False (leading zero)

# Validate IPv6
print(validate_ipv6("2001:0db8:85a3:0000:0000:8a2e:0370:7334")) # True

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
