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

### Added

- GitHub Actions CI running the test suite on every push and pull
  request, across Python 3.9-3.12.
- Regression tests for the IPv6 and classification fixes above.
