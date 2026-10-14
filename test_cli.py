"""Tests for the `ip-validator` CLI (ip_validator.main)."""

import json
import subprocess
import sys

import pytest

from ip_validator import main


def test_cli_valid_ipv4_table_output(capsys):
    main(["192.168.1.1"])
    out = capsys.readouterr().out
    assert "class: C" in out
    assert "is_private: True" in out


def test_cli_valid_ipv4_json_output(capsys):
    main(["169.254.1.1", "--json"])
    data = json.loads(capsys.readouterr().out)
    assert data["ip"] == "169.254.1.1"
    assert data["is_link_local"] is True


def test_cli_valid_ipv6(capsys):
    main(["::1"])
    out = capsys.readouterr().out
    assert "version: 6" in out


def test_cli_invalid_input_exits_nonzero(capsys):
    with pytest.raises(SystemExit) as exc_info:
        main(["not-an-ip"])
    assert exc_info.value.code == 1
    assert "not a valid" in capsys.readouterr().err


def test_cli_version_flag(capsys):
    with pytest.raises(SystemExit) as exc_info:
        main(["--version"])
    assert exc_info.value.code == 0
    assert "ip-validator" in capsys.readouterr().out


def test_cli_end_to_end_smoke():
    # One true subprocess invocation of the actual entry point, exactly as
    # a real user would run it. Not tracked by coverage.py (separate
    # process) - the tests above cover the logic - but this confirms the
    # module is genuinely invocable via `python -m ip_validator`.
    result = subprocess.run(
        [sys.executable, "-m", "ip_validator", "8.8.8.8"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "class: A" in result.stdout