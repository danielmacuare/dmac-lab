from nautobot_ssot.contrib import NautobotAdapter

from nautobot_ssot_fortimanager.diffsync.models.base import IPAddressDiffSyncModel


class NautobotIPAddressAdapter(NautobotAdapter):
    ip_address = IPAddressDiffSyncModel
    # address_object = AddressObjectDiffSyncModel
    # address_groups = AddressGroupsDiffSyncModel

    top_level = ["ip_address"]
