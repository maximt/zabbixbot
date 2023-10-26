import pytest

from bot.parsers import PING_COUNT_DEFAULT, parse_ping_command, parse_ping_reply_command

REPLY_TEXT = """
Problem name: High ICMP ping response time
Host: Server (192.168.1.71)
Severity: Warning
"""

REPLY_TEXT_INVALID_HOST = """
Problem name: High ICMP ping response time
Host: Server (qwe..qwe)
Severity: Warning
"""

REPLY_TEXT_NO_HOST = """
Hello world
"""


def test_parse_ping_command_valid() -> None:
    hostname, count = parse_ping_command("ping example.com")
    assert hostname == "example.com"
    assert count == PING_COUNT_DEFAULT


def test_parse_ping_command_with_count() -> None:
    hostname, count = parse_ping_command("ping example.com 5")
    assert hostname == "example.com"
    assert count == 5


def test_parse_ping_command_invalid_hostname() -> None:
    with pytest.raises(ValueError, match="Invalid hostname"):
        parse_ping_command("ping invalid..hostname")


def test_parse_ping_command_wrong_arguments_count() -> None:
    with pytest.raises(ValueError, match="Wrong number of arguments."):
        parse_ping_command("ping example.com 5 10")


def test_parse_ping_command_missing_hostname() -> None:
    with pytest.raises(ValueError, match="Wrong number of arguments."):
        parse_ping_command("ping")


def test_parse_ping_reply_command_valid() -> None:
    hostname, count = parse_ping_reply_command("ping", REPLY_TEXT)
    assert hostname == "192.168.1.71"
    assert count == PING_COUNT_DEFAULT


def test_parse_ping_reply_command_invalid() -> None:
    with pytest.raises(ValueError, match="Host not found in this message"):
        parse_ping_reply_command("ping", REPLY_TEXT_NO_HOST)


def test_parse_ping_reply_command_invalid_hostname() -> None:
    with pytest.raises(ValueError, match="Invalid hostname"):
        parse_ping_reply_command("ping", REPLY_TEXT_INVALID_HOST)
