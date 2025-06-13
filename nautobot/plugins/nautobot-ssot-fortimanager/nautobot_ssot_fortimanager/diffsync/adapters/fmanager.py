from typing import override

from diffsync import Adapter

from nautobot_ssot_fortimanager.diffsync.models.base import IPAddressDiffSyncModel


class FortiManagerBaseAdapter(Adapter):
    def __init__(
        self,
        url=None,
        username=None,
        password=None,
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
        self.json_file = "fw_addresses.json"


class FortiManagerIPAddressAdapter(FortiManagerBaseAdapter):
    ip_address = IPAddressDiffSyncModel

    top_level = ["ip_address"]

    @override
    def load(self):
        self.job.logger.info("This is the load routine")
        self.job.logger.info(f"Job logger instance: {self.job.logger}")  # You can inspect the logger
        self.job.logger.info(f"Adapter URL: {self.url}")
        self.job.logger.info(f"Adapter Username: {self.username}")
        # self.job.logger.info(f"Use cache: {self.use_cache}")
        self.job.logger.info(f"Reading data from JSON File at: {self.json_file}")
