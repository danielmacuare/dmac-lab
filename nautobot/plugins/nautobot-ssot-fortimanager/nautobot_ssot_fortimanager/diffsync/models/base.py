"""Common data model that will be used by the source and target adapters"""

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
    _identifiers = ("host", "parent__namespace__name")
    _attributes = ("description", "tags", "mask_length", "status__name")

    host: str
    parent__namespace__name: str
    description: str
    tags: list[TagDict] = []
    mask_length: int
    # status__name ---> Performs obj.status.name in the background
    status__name: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # The line below will leave untouched any object that only exists in the Target but not the source
        # self.model_flags = DiffSyncModelFlags.SKIP_UNMATCHED_DST

    # Filter only IPs tagged with FortiManager
    @classmethod
    def get_queryset(cls):
        return IPAddress.objects.filter(parent__namespace__name="FortiManager")


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
