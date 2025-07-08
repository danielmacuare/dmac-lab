from nautobot_ssot.contrib import NautobotAdapter

from nautobot_ssot_fortimanager.diffsync.models.base import FqdnFWDiffSyncModel, IPAddressDiffSyncModel


class NautobotFWRulesAdapter(NautobotAdapter):
    ip_address = IPAddressDiffSyncModel
    fqdn_fw = FqdnFWDiffSyncModel
    # address_object = AddressObjectDiffSyncModel
    # address_groups = AddressGroupsDiffSyncModel

    top_level = ["ip_address", "fqdn_fw"]
