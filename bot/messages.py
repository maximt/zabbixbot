from icmplib.models import Host
from zabbix import HostTrigger

PRIORITY_ICONS = [
    "⚪ ",
    "🔵 ",
    "🟡 ",
    "🟠 ",
    "🟤 ",
    "🔴 ",
]

HOST_ICON = "🖥️ "


def trigger_message(trigger: HostTrigger) -> str:
    return '{} <a href="{}"><b>{}</b></a>\n{} {}'.format(
        HOST_ICON,
        trigger.get_url,
        trigger.hostname,
        PRIORITY_ICONS[trigger.priority],
        trigger.description,
    )


def triggers_message(triggers: list[HostTrigger]) -> str:
    return "\n\n".join(map(trigger_message, triggers))


def ping_message(pong: Host) -> str:
    return str(pong)


def error_message(e: Exception) -> str:
    return str(e)


def help_message() -> str:
    return """
/list
/ping <hostname> [count]

You can reply to zabbix's message using the following commands:

/ping [count]
"""
