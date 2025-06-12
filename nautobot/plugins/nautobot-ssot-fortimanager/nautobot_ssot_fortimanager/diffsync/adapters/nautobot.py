from nautobot_ssot.contrib import NautobotAdapter

from nautobot_ssot_fortimanager.diffsync.models.base import FortiManagerIPAddress


class FortiManagerToNautobotAdapter(NautobotAdapter):
    ip_address = FortiManagerIPAddress

    top_level = ["ip_address"]
