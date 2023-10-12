import os
from datetime import datetime
from functools import cached_property

from dotenv import load_dotenv
from pyzabbix import ZabbixAPI

load_dotenv()

TOKEN = os.environ.get("ZABBIX_TOKEN")
ZABBIX_URL = os.environ.get("ZABBIX_URL")
ZABBIX_URL_PROBLEMS = "zabbix.php?action=problem.view&hostids[]={}"
PING_SCRIPT = os.environ.get("ZABBIX_PING_SCRIPT_ID")


class HostTrigger:
    def __init__(
        self, hostname: str, description: str, priority: int, hostid: int
    ) -> None:
        self.hostname: str = hostname
        self.description: str = description
        self.priority: int = priority
        self.hostid: int = hostid

    @cached_property
    def get_url(self) -> str:
        return "{}/{}".format(ZABBIX_URL, ZABBIX_URL_PROBLEMS.format(self.hostid))


class HostProblem:
    def __init__(
        self,
        problem_name: str,
        date: datetime,
        hostname: str,
        severity: int,
        opdata: str,
        hostid: int,
    ) -> None:
        self.problem_name: str = problem_name
        self.date: datetime = date
        self.hostname: str = hostname
        self.severity: int = severity
        self.opdata: str = opdata
        self.hostid: int = hostid


def get_triggers() -> list[HostTrigger]:
    if not ZABBIX_URL:
        raise ValueError("ZABBIX_URL is not set")

    with ZabbixAPI(ZABBIX_URL) as zapi:
        zapi.login(api_token=TOKEN)
        return list(
            map(
                lambda trigger: HostTrigger(
                    trigger["hosts"][0]["name"],
                    trigger["description"],
                    int(trigger["priority"]),
                    int(trigger["hosts"][0]["hostid"]),
                ),
                zapi.trigger.get(
                    only_true=1,
                    skipDependent=1,
                    monitored=1,
                    active=1,
                    output="extend",
                    expandDescription=1,
                    selectHosts=["hostid", "host", "name"],
                    sortfield="priority",
                    sortorder="DESC",
                ),
            )
        )


def ping(hostname: str) -> str:
    if not ZABBIX_URL:
        raise ValueError("ZABBIX_URL is not set")
    if not PING_SCRIPT:
        raise ValueError("ZABBIX_PING_SCRIPT is not set")

    with ZabbixAPI(ZABBIX_URL) as zapi:
        zapi.login(api_token=TOKEN)
        hosts = zapi.host.get(filter={"host": hostname}, output=["hostids", "host"])
        if not hosts:
            raise Exception("Host {} not found".format(hostname))
        host = hosts[0]
        pong = zapi.do_request(
            "script.execute", {"scriptid": PING_SCRIPT, "hostid": host["hostid"]}
        )
        result = pong["result"]
        if result["response"] != "success":
            raise Exception("Can't ping {}".format(hostname))
        return str(result["value"])
