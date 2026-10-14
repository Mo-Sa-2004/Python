import unittest
from ip_validator import validate_ip, validate_ipv6, get_ip_info


class TestIPValidator(unittest.TestCase):

    # --- IPv4 Tests ---
    def test_valid_ipv4(self):
        self.assertTrue(validate_ip("192.168.1.1"))
        self.assertTrue(validate_ip("0.0.0.0"))
        self.assertTrue(validate_ip("255.255.255.255"))
        self.assertTrue(validate_ip("8.8.8.8"))

    def test_invalid_ipv4_out_of_bounds(self):
        self.assertFalse(validate_ip("256.100.0.1"))
        self.assertFalse(validate_ip("192.168.1.-1"))

    def test_invalid_ipv4_leading_zeros(self):
        self.assertFalse(validate_ip("192.168.01.1"))

    def test_invalid_ipv4_malformed(self):
        self.assertFalse(validate_ip("192.168.1"))
        self.assertFalse(validate_ip("192.168.1.1.1"))
        self.assertFalse(validate_ip("abc.def.ghi.jkl"))
        self.assertFalse(validate_ip(""))

    def test_invalid_ipv4_types(self):
        self.assertFalse(validate_ip(None))
        self.assertFalse(validate_ip(123456))
        self.assertFalse(validate_ip(["192.168.1.1"]))

    # --- IPv6 Tests ---
    def test_valid_ipv6(self):
        self.assertTrue(validate_ipv6("2001:0db8:85a3:0000:0000:8a2e:0370:7334"))

    def test_valid_ipv6_compressed(self):
        # "::" (RFC 4291 zero-compression) covers the most common real-world
        # IPv6 addresses - loopback, unspecified, and link-local - none of
        # which the old regex-only validator accepted.
        self.assertTrue(validate_ipv6("::1"))  # loopback
        self.assertTrue(validate_ipv6("::"))  # unspecified address
        self.assertTrue(validate_ipv6("fe80::1"))  # link-local
        self.assertTrue(validate_ipv6("2001:db8::1"))

    def test_invalid_ipv6(self):
        self.assertFalse(validate_ipv6("192.168.1.1"))
        self.assertFalse(validate_ipv6("2001:0db8:85a3"))
        self.assertFalse(validate_ipv6("2001::db8::1"))  # "::" used twice

    # --- Metadata Tests ---
    def test_ip_info(self):
        info = get_ip_info("192.168.1.1")
        self.assertIsNotNone(info)
        self.assertEqual(info["class"], "C")
        self.assertTrue(info["is_private"])

        invalid_info = get_ip_info("invalid_ip")
        self.assertIsNone(invalid_info)


if __name__ == "__main__":
    unittest.main()
