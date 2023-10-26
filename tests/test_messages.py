from typing import Any
from unittest.mock import patch

import pytest

from bot.messages import trigger_message, triggers_message
from bot.zabbix import ZABBIX_URL_PROBLEMS, HostTrigger

EXPECTED_MESSAGE = """🖥️  <a href="https://example.com/zabbix/zabbix.php?action=problem.view&hostids[]=123"><b>example.com</b></a>
🟡  Problem name: High ICMP ping response time"""  # noqa: E501

EXPECTED_MESSAGES = """🖥️  <a href="https://example.com/zabbix/zabbix.php?action=problem.view&hostids[]=123"><b>example1.com</b></a>
🟡  Problem name: High ICMP ping response time

🖥️  <a href="https://example.com/zabbix/zabbix.php?action=problem.view&hostids[]=456"><b>example2.com</b></a>
🟠  Problem name: Unavailable by ICMP ping"""  # noqa: E501


@pytest.fixture  # type: ignore[misc]
def mock_env() -> Any:
    with patch("bot.zabbix.ZABBIX_URL", "https://example.com/zabbix"):
        yield


def test_HostTrigger_constructor(mock_env: Any) -> None:
    hostname = "example.com"
    description = "Problem name: High ICMP ping response time"
    priority = 2
    hostid = 123
    url = f"https://example.com/zabbix/{ZABBIX_URL_PROBLEMS.format(hostid)}"

    trigger = HostTrigger(hostname, description, priority, hostid)

    assert trigger.hostname == hostname
    assert trigger.description == description
    assert trigger.priority == priority
    assert trigger.hostid == hostid
    assert trigger.get_url == url


def test_trigger_message(mock_env: Any) -> None:
    trigger = HostTrigger(
        "example.com", "Problem name: High ICMP ping response time", 2, 123
    )

    assert trigger_message(trigger) == EXPECTED_MESSAGE


def test_triggers_message(mock_env: Any) -> None:
    triggers = [
        HostTrigger(
            "example1.com", "Problem name: High ICMP ping response time", 2, 123
        ),
        HostTrigger("example2.com", "Problem name: Unavailable by ICMP ping", 3, 456),
    ]

    assert triggers_message(triggers) == EXPECTED_MESSAGES
