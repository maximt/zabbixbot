import re
from typing import Tuple

from fqdn import FQDN

PING_COUNT_DEFAULT = 3


def parse_ping_command(text: str) -> Tuple[str, int]:
    args = text.split()
    if not (2 <= len(args) <= 3):
        raise ValueError("Wrong number of arguments. Usage: ping <hostname> [count]")

    args.pop(0)  # pop "ping"

    hostname: str = args.pop(0)
    if not FQDN(hostname).is_valid:
        raise ValueError("Invalid hostname")

    count: int = int(args.pop(0)) if args else PING_COUNT_DEFAULT

    return hostname, count


def parse_ping_reply_command(text: str, reply_text: str) -> Tuple[str, int]:
    result = re.search(
        r"host:.+\(([a-z\d\.\-]+?)\)", reply_text, re.MULTILINE | re.IGNORECASE
    )
    if not result:
        raise ValueError("Host not found in this message")

    hostname: str = result.group(1)
    if not FQDN(hostname).is_valid:
        raise ValueError("Invalid hostname")

    args = text.split()
    args.pop(0)  # pop "ping"

    count: int = int(args.pop(0)) if args else PING_COUNT_DEFAULT

    return hostname, count
