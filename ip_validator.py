"""
IP Address Validator and Parser Utility Module.
"""

import argparse
import ipaddress
import json
import sys
from typing import Any, Dict, Optional

__version__ = "0.1.0"


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
        # (e.g. full-width "\uff11\uff19\uff12"), which would let a
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

    # Identify Private/Loopback/special-use flags
    is_private = (
        (first == 10)
        or (first == 172 and 16 <= octets[1] <= 31)
        or (first == 192 and octets[1] == 168)
    )
    is_loopback = first == 127
    # 169.254.0.0/16 - link-local (APIPA)
    is_link_local = first == 169 and octets[1] == 254
    # 100.64.0.0/10 - shared address space for carrier-grade NAT (RFC 6598)
    is_cgnat = first == 100 and 64 <= octets[1] <= 127
    # 224.0.0.0/4 - multicast
    is_multicast = 224 <= first <= 239
    # 0.0.0.0/8 and 240.0.0.0/4 - reserved/"this network"/experimental
    is_reserved = first == 0 or first >= 240

    return {
        "ip": ip,
        "valid": True,
        "class": ip_class,
        "is_private": is_private,
        "is_loopback": is_loopback,
        "is_link_local": is_link_local,
        "is_cgnat": is_cgnat,
        "is_multicast": is_multicast,
        "is_reserved": is_reserved,
        "octets": octets,
        "binary": ".".join(f"{o:08b}" for o in octets),
    }


def _parse_args(argv: Optional[list] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="ip-validator",
        description="Validate an IPv4/IPv6 address and print its metadata.",
    )
    parser.add_argument("ip", help="IP address to check, e.g. 192.168.1.1 or ::1")
    parser.add_argument(
        "--json", action="store_true", help="Print the result as JSON."
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    return parser.parse_args(argv)


def main(argv: Optional[list] = None) -> None:
    args = _parse_args(argv)

    if validate_ip(args.ip):
        info = get_ip_info(args.ip)
    elif validate_ipv6(args.ip):
        info = {"ip": args.ip, "valid": True, "version": 6}
    else:
        print(f"'{args.ip}' is not a valid IPv4 or IPv6 address.", file=sys.stderr)
        raise SystemExit(1)

    if args.json:
        print(json.dumps(info, indent=2))
    else:
        for key, value in info.items():
            print(f"{key}: {value}")


if __name__ == "__main__":
    main()
