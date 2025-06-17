"""Source Adapter where we translate data from FortiManager Data model into Nautobots DM"""

from ipaddress import ip_network
from pathlib import Path
from typing import Any, override

from diffsync import Adapter

from nautobot_ssot_fortimanager.diffsync.models.base import IPAddressDiffSyncModel


class FortiManagerBaseAdapter(Adapter):
    def __init__(
        self,
        url: str | None = None,
        username: str | None = None,
        password: str | None = None,
        # use_cache=True,
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
        # self.use_cache = use_cache

        self.job = job
        # self.sync = sync
        self.json_file = Path(__file__).parent / "fw_addresses.json"


class FortiManagerIPAddressAdapter(FortiManagerBaseAdapter):
    ip_address = IPAddressDiffSyncModel

    top_level = ["ip_address"]

    def read_json_file(self, path: Path):
        """Read the JSON file and return its content."""
        import json

        with open(path, "r") as file:
            data = json.load(file)
        return data

    def load_ip(self, ip_addresses: dict[str, dict[str, Any]]):
        """
        Processes the raw JSON data, extracts IP addresses, and creates
        IPAddressDiffSyncModel instances.
        """
        FORTIMANAGER_NAUTOBOT_NAMESPACE: str = "FortiManager"

        for address, param in ip_addresses.items():
            self.job.logger.info("From  Inside load_ip - Processing Dict Key: %s", address)
            self.job.logger.info("From  Inside load_ip: - Processing Dict Value: %s", param)

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
                    description=(f"{FORTIMANAGER_NAUTOBOT_NAMESPACE} - {param['name']}"),
                    parent__namespace__name=FORTIMANAGER_NAUTOBOT_NAMESPACE,
                    status__name="Active",
                )

                self.add(ip)

                self.job.logger.info("IP Name %s", ip.host)
                self.job.logger.info("IP Description %s", ip.description)
                self.job.logger.info("Object Added")

    @override
    def load(self):
        json_data = self.read_json_file(path=self.json_file)
        if not json_data:
            self.job.logger.error("No data found in the JSON file.")
            return

        # Error Handling- Can't Open file, no content in file, file not correctly formatted as JSON, etc

        # Valid code

        self.job.logger.info(f"Data from json: {json_data}")
        # address_name: str | None = json_data.get("address1.name")
        # ip_address: str | None = json_data.get("address1.ip_address")
        # ip_range: str | None = json_data.get("address1.ip_range")
        # prefix: str | None = json_data.get("address1.prefix")

        self.load_ip(ip_addresses=json_data)

        self.job.logger.info(f"Job logger instance: {self.job.logger}")  # You can inspect the logger
        self.job.logger.info(f"Adapter URL: {self.url}")
        self.job.logger.info(f"Adapter Username: {self.username}")
        # self.job.logger.info(f"Use cache: {self.use_cache}")
        self.job.logger.info(f"Reading data from JSON File at: {self.json_file}")
