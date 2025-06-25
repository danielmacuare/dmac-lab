"""Source Adapter where we translate data from FortiManager Data model into Nautobots DM"""

from ipaddress import ip_network
from os import getenv
from pathlib import Path
from typing import Any, override

from diffsync import Adapter

from nautobot_ssot_fortimanager.diffsync.models.base import IPAddressDiffSyncModel

_SOURCE_FILE_PATH: str | None = getenv("SOURCE_FILE_PATH")
FORTIMANAGER_NAUTOBOT_NAMESPACE: str | None = getenv("FORTIMANAGER_NAUTOBOT_NAMESPACE")
# SOURCE_FILE_PATH: str = "/opt/nautobot/fw_addresses.json"
# FORTIMANAGER_NAUTOBOT_NAMESPACE: str = "FortiManager"

if _SOURCE_FILE_PATH is None:
    raise ValueError("Environment Variable 'SOURCE_FILE_PATH' is not set")
if FORTIMANAGER_NAUTOBOT_NAMESPACE is None:
    raise ValueError("Environment Variable 'FORTIMANAGER_NAUTOBOT_NAMESPACE' is not set")

SOURCE_FILE_PATH: Path = Path(_SOURCE_FILE_PATH)

if not SOURCE_FILE_PATH.exists():
    raise FileNotFoundError(f"SOURCE_FILE_PATH: {_SOURCE_FILE_PATH} does not exists")
if not SOURCE_FILE_PATH.is_file():
    raise ValueError(f"SOURCE_FILE_PATH: {_SOURCE_FILE_PATH} is not a file")


class FortiManagerBaseAdapter(Adapter):
    def __init__(
        self,
        url: str | None = None,
        username: str | None = None,
        password: str | None = None,
        use_cache: bool = False,
        *args,
        job=None,
        sync=None,
        client=None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.url = url
        self.username = username
        self.password = password
        self.use_cache = use_cache

        self.job = job
        # self.sync = sync
        self.json_file = SOURCE_FILE_PATH


class FortiManagerFWRulesAdapter(FortiManagerBaseAdapter):
    ip_address = IPAddressDiffSyncModel

    top_level = ["ip_address"]

    def read_json_file(self, path: str):
        """Read the JSON file and return its content."""
        import json

        with open(path, "r") as file:
            data = json.load(file)
        return data

    def load_ip_addresses(self, ip_addresses: dict[str, dict[str, Any]]):
        """
        Processes the raw JSON data, extracts IP addresses, and creates
        IPAddressDiffSyncModel instances.
        """

        for param in ip_addresses.values():
            # self.job.logger.info("From  Inside load_ip_addresses - Processing Dict Key: %s", address)
            # self.job.logger.info("From  Inside load_ip_addresses: - Processing Dict Value: %s", param)

            # Creating the IPAddressDiffSyncModel for the source adapter

            # Check if the address is an IP Addresss

            if not param.get("ip_address"):
                self.job.logger.info("SKIPPED: Entry processed is not an IP. Entry %s", param)
            else:
                ip_object = ip_network(param["ip_address"], strict=False)
                ip_add: str = str(ip_object.network_address)
                ip_mask: int = ip_object.prefixlen

                # Instantiate Dyffsync model if ip_address exists in the dictionary
                ip = self.ip_address(
                    host=ip_add,
                    mask_length=ip_mask,
                    description=(f"{param['description']}"),
                    parent__namespace__name=FORTIMANAGER_NAUTOBOT_NAMESPACE,
                    status__name="Active",
                )

                self.add(obj=ip)

                # self.job.logger.info("IP Name %s - IP Description %s", ip.host, ip.description)
                # self.job.logger.info("Object Added")

    @override
    def load(self):
        json_data = self.read_json_file(path=self.json_file)
        if not json_data:
            self.job.logger.error("No data found in the JSON file.")
            return

        # Error Handling- Can't Open file, no content in file, file not correctly formatted as JSON, etc

        self.job.logger.info(f"Data from json: {json_data}")

        self.load_ip_addresses(ip_addresses=json_data)

        # self.job.logger.info("Job logger instance: %s", self.job.logger)  # You can inspect the logger
        # self.job.logger.info(f"Adapter URL: {self.url}")
        # self.job.logger.info(f"Adapter Username: {self.username}")
        self.job.logger.info(f"Use cache: {self.use_cache}")
        # self.job.logger.info(f"Reading data from JSON File at: {self.json_file}")
