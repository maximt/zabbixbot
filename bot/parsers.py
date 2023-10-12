from typing import Tuple

from fqdn import FQDN


def parse_ping_command(text: str) -> Tuple[str, int]:
    args = text.split()

    if not (2 <= len(args) <= 3):
        raise ValueError("Wrong number of arguments. Usage: ping <hostname> [count]")

    hostname: str = args[1]
    domain: FQDN = FQDN(hostname)

    if not domain.is_valid:
        raise ValueError("Invalid hostname")

    count: int = 3
    if len(args) == 3:
        count = int(args[2])
        if not (1 <= count <= 10):
            count = 3

    return hostname, count
