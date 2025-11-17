"""Source Adapter where we translate data from FortiManager Data model into Nautobots DM"""

# Ds
from ipaddress import ip_network
from os import getenv
from pathlib import Path
from typing import Any, override

from diffsync import Adapter
from nautobot.extras.models.tags import Tag
from nautobot.ipam.models import IPAddress

from nautobot_ssot_fortimanager.diffsync.models.base import (
    FqdnFWDiffSyncModel,
    IPAddressDiffSyncModel,
    ServiceDiffSyncModel,
)

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
    fqdn_fw = FqdnFWDiffSyncModel
    service_object_fw = ServiceDiffSyncModel
    top_level = ["ip_address", "fqdn_fw", "service_object_fw"]

    def read_json_file(self, path: Path):
        """Read the JSON file and return its content."""
        import json

        with open(path, "r") as file:
            data = json.load(file)
        return data

    def load_ip_addresses(self, data: dict[str, dict[str, Any]]):
        """
        Processes the raw JSON data, extracts IP addresses, and creates
        IPAddressDiffSyncModel instances.
        """

        for param in data.values():
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

    def ip_exists_in_nautobot(self, ip_address_str: str):
        """Check if an IP Address exists in Nautobot IPAM"""
        try:
            ip_object = ip_network(ip_address_str, strict=False)
            normalized_ip = str(ip_object)

            ipam_nautobot_ip: IPAddress = IPAddress.objects.filter(address=normalized_ip).first()

            if ipam_nautobot_ip:
                self.job.logger.debug("IP Address %s exists", normalized_ip)
                return ipam_nautobot_ip
            else:
                self.job.logger.debug("IP Address %s doesn't exist", normalized_ip)
                return None
        except Exception as e:
            self.job.logger.debug("An unexpected error occurred when checking if IP Exists: %s", e)

    def load_fqdns(self, data: dict[str, dict[str, Any]]):
        """This will load FQDNs to be updated into the nautobot_ssot_firewalls_model."""

        print(data)
        for param in data.values():
            fqdn = param.get("fqdn", None)
            fqdn_description = param.get("description", None)

            # Checking if the record has FQDNs parse_fqdns
            if not param.get("fqdn"):
                self.job.logger.debug("SKIPPED: Entry processed is not an FQDN. Entry %s", param)
            else:
                self.job.logger.debug("ADDING: Entry processed is an FQDN. Entry %s", param)
                fqdn_model = self.fqdn_fw(
                    name=fqdn, description=f"FQDN Description: {fqdn_description}", status__name="Active"
                )
                self.add(obj=fqdn_model)

                # Check if there are ip addresses associated to an fqdn
                if not param.get("ip_addresses"):
                    self.job.logger.debug("SKIPPED: No IP Addresses are associated to this FQDN: %s", fqdn)
                else:
                    for ip in param["ip_addresses"]:
                        # Add this IP to the object
                        print(f"IP: {ip} is associated with {fqdn} - {fqdn_description}")
                        self.ip_exists_in_nautobot(ip)
                        # Check if IP already exists in Nautobot

    def load_service_objects(self, data: dict[str, dict[str, Any]]):
        self.job.logger.debug("HI FROM INSIDE")

        for key, param in data.items():
            if not param.get("service"):
                continue

            try:
                service_object = self.service_object_fw(
                    name=str(param.get("service")),
                    ip_protocol=str(param.get("ip_protocol")),
                    status__name="Active",
                    description=str(param.get("description")),
                    tags=[{"name": "FortiManager"}],
                )

                if param.get("port"):
                    service_object.port = param["port"]

                # service_object.tags.append({"name": "FortiManager"})
                self.add(service_object)
                self.job.logger.debug(
                    f"SUCCESS: Added Service Object: {service_object.name} (from key: {key})"
                )
            except Exception as e:
                self.job.logger.error(
                    f"ERROR: Failed to process Service Object from data entry '{key}'. ",
                    f"Data: {param}. Error: {e}",
                    exc_info=True,  # This will print the full traceback
                )
                # You might choose to continue or break here depending on desired behavior
                continue  # Continue to the next item even if one fails

    @override
    def load(self):
        json_data = self.read_json_file(path=self.json_file)
        if not json_data:
            self.job.logger.error("No data found in the JSON file.")
            return

        # Error Handling- Can't Open file, no content in file, file not correctly formatted as JSON, etc

        self.job.logger.info(f"Data from json: {json_data}")

        # Ensure FortiManager exists, if it doesn't create it.
        fortimanager_tag, created = Tag.objects.get_or_create(
            name="FortiManager",
            defaults={
                "description": "Objects synchronized from FortiManager",
                "color": "ff0000",  # Example color (red), choose as appropriate
            },
        )

        if created:
            self.job.logger.info(f"Created missing Tag: {fortimanager_tag.name}")
        else:
            self.job.logger.debug(f"Tag '{fortimanager_tag.name}' already exists.")

        self.load_ip_addresses(data=json_data)
        self.load_fqdns(data=json_data)
        self.load_service_objects(data=json_data)

        # self.job.logger.info("Job logger instance: %s", self.job.logger)  # You can inspect the logger
        # self.job.logger.info(f"Adapter URL: {self.url}")
        # self.job.logger.info(f"Adapter Username: {self.username}")
        self.job.logger.info(f"Use cache: {self.use_cache}")
        # self.job.logger.info(f"Reading data from JSON File at: {self.json_file}")
