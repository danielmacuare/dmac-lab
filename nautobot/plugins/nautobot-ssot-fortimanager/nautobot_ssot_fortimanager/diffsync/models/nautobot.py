"""Nautobot DiffSync Models for FortiManager SSOT"""

from nautobot.ipam.models import IPAddress

from nautobot_ssot_fortimanager.diffsync.models.base import IPAddressDiffSyncModel


class NautobotIPAddressDiffSyncModel(IPAddressDiffSyncModel):
    """Model to deal with Nautobot IP Addresses from the ipam.IPAddress Model"""

    @classmethod
    def create(cls, adapter, ids, attrs):
        """Create IP Addresses in Nautobot"""

        adapter.log.logger.debug("Creating IP Address: %s %s", ids, attrs)
        # Getting current objects Loaded into the Diffsync instances Nautobot
        ip_add_obj = IPAddress.objects.get(name=ids["host"], parent__namespace__name=ids["parent__namespace__name"])

        try:
            adapter.log.info("IP Add Obj: %", ip_add_obj)
        except Exception as ip_address_err:
            adapter.job.logger.info(f" Could not create IP Address Mapping. Error {ip_address_err}")
