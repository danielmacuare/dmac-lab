from typing import Any, TypeAlias

from nautobot.apps import NautobotAppConfig


class NautobotSSOTFortimanager(NautobotAppConfig):
    name: str = "nautobot_ssot_fortimanager"
    verbose_name: str = "Nautobot SSOT FortiManager"
    description: str = "Nautobot App to pull data from Fortimanager"
    version: str = "0.0.1"
    author: str = "Daniel Macuare"
    author_email: str = "daniel280187@hotmail.com"
    required_settings: list[Any] = []
    default_settings: dict[str, Any] = {"loud": False}


config: TypeAlias = NautobotSSOTFortimanager
