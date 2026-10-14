"""
IP Address Validator and Parser Utility Module.
"""

import ipaddress
from typing import Any, Dict, Optional


def validate_ip(ip: Any) -> bool:
    """
    Checks for valid IPv4 address format and ensures each octet is
    within range [0, 255] without leading zeros.
    """
    if not isinstance(ip, str):
        return False

    parts = ip.split(".")
    if len(parts) != 4:
        return False

    for part in parts:
        # `str.isdigit()`/`int()` accept non-ASCII Unicode decimal digits
        # (e.g. full-width "１９２" or Devanagari "०"), which would let a
        # lookalike string silently pass as a normal IPv4 octet. Require
        # plain ASCII 0-9 only.
        if not (part.isascii() and part.isdigit()):
            return False
        # Disallow leading zeros unless the octet is strictly '0'
        if len(part) > 1 and part.startswith("0"):
            return False
        val = int(part)
        if val < 0 or val > 255:
            return False

    return True


def validate_ipv6(ip: Any) -> bool:
    """
    Checks if a given string is a valid IPv6 address, including the
    compressed "::" notation (RFC 4291), e.g. "::1" or "fe80::1".
    """
    if not isinstance(ip, str):
        return False

    try:
        ipaddress.IPv6Address(ip)
    except ValueError:
        return False

    return True


def get_ip_info(ip: str) -> Optional[Dict[str, Any]]:
    """
    Returns detailed structural metadata for a valid IPv4 address.
    """
    if not validate_ip(ip):
        return None

    octets = [int(p) for p in ip.split(".")]
    first = octets[0]

    # Determine Address Class
    if first == 0:
        ip_class = "Reserved (0.0.0.0/8)"
    elif 1 <= first <= 126:
        ip_class = "A"
    elif first == 127:
        ip_class = "A (Loopback)"
    elif 128 <= first <= 191:
        ip_class = "B"
    elif 192 <= first <= 223:
        ip_class = "C"
    elif 224 <= first <= 239:
        ip_class = "D (Multicast)"
    else:
        ip_class = "E (Experimental)"

    # Identify Private/Loopback flags
    is_private = (
        (first == 10)
        or (first == 172 and 16 <= octets[1] <= 31)
        or (first == 192 and octets[1] == 168)
    )
    is_loopback = first == 127

    return {
        "ip": ip,
        "valid": True,
        "class": ip_class,
        "is_private": is_private,
        "is_loopback": is_loopback,
        "octets": octets,
        "binary": ".".join(f"{o:08b}" for o in octets),
    }
