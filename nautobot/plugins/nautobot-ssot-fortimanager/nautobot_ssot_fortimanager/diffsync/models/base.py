"""Common data model that will be used by the source and target adapters"""

from diffsync.enum import DiffSyncModelFlags
from nautobot.ipam.models import IPAddress
from nautobot_firewall_models.models import AddressObject
from nautobot_ssot.contrib import NautobotModel
from nautobot_ssot.contrib.typeddicts import TagDict

"""
## Process
- Create IP Addresses
- Create FQDNs
- Create Prefixes
- Create IP Ranges
- Create AddressObject 
- Create AddressGroup
"""


class IPAddressDiffSyncModel(NautobotModel):
    """
    Model to store IPAddresses
    """

    _model = IPAddress
    _modelname = "ip_address"
    _identifiers = ("host",)
    _attributes = ("description", "tags")

    host: str
    description: str
    tags: list[TagDict] = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_flags = DiffSyncModelFlags.SKIP_UNMATCHED_DST


class FortiManagerAddressObject(NautobotModel):
    """The AddressObject can have 4 types of IPs:
    - fqdn
    - ip_address
    - ip_range
    - prefix
    I need to filter by name and tag source =  FortiManager
    """

    _model = AddressObject
    _modelname = "adress_object"
    _identifiers = ("name",)
    _attributes = ("address", "description", "ip_address", "tags")

    name: str
    address: str
    description: str
    ip_address: str
    tags: list[TagDict] = []
