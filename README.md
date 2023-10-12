poetry install

poetry run python bot/start.py

ENVs:
* TELEGRAM_TOKEN=
* ZABBIX_URL=
* ZABBIX_TOKEN=

Commands:
* /list - show active Zabbix problems
* /ping \<hostname\> [count] - icmp check for \<hostname\>
