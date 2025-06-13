from nautobot_ssot.contrib import NautobotAdapter

from nautobot_ssot_fortimanager.diffsync.models.base import IPAddressDiffSyncModel


class FortiManagerToNautobotAdapter(NautobotAdapter):
    ip_address = IPAddressDiffSyncModel

    top_level = ["ip_address"]
