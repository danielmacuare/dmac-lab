## Debugggin Nautobot Model
from nautobot_ssot_fortimanager.diffsync.models.base import IPAddressDiffSyncModel

IPAddressDiffSyncModel.create(
    adapter=None,
    ids={
        "host": "104.16.123.108/32",
        "parent__namespace__name": "FortiManager",
    },
    attrs={
        "description": "DMAC Test",
    },
)


## Debugging FortiManager Adapter
from nautobot_ssot_fortimanager.diffsync.adapters.fmanager import (
    FortiManagerFWRulesAdapter,
)

FortiManagerFWRulesAdapter()
