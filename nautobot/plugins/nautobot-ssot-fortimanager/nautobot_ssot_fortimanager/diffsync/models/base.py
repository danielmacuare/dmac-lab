"""Common data model that will be used by the source and target adapters"""

from typing import override

from nautobot.ipam.models import IPAddress
from nautobot_firewall_models.models import FQDN, ServiceObject
from nautobot_ssot.contrib import NautobotModel
from nautobot_ssot.contrib.typeddicts import TagDict

"""
## Process

- Create IP Addresses (Done)
- Create FQDNs (Done)
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


class FqdnFWDiffSyncModel(NautobotModel):
    """
    Model to store IPAddresses
    """

    _model = FQDN
    _modelname = "fqdn_fw"
    _identifiers = ("name",)
    _attributes = ("description", "tags", "status__name")

    name: str
    description: str
    tags: list[TagDict] = []
    status__name: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # The line below will leave untouched any object that only exists in the Target but not the source
        # self.model_flags = DiffSyncModelFlags.SKIP_UNMATCHED_DST

    # Filter only IPs with FortiManager used as a Namespace
    # @classmethod
    # def get_queryset(cls):
    # return IPAddress.objects.filter(parent__namespace__name="FortiManager")


class ServiceDiffSyncModel(NautobotModel):
    """Diffsync model to sync custom service objects as Nautobot comes with some predefined ones."""

    _model = ServiceObject
    _modelname = "service_object_fw"
    _identifiers = ("name", "ip_protocol")
    _attributes = ("port", "status__name", "description", "tags")

    name: str
    ip_protocol: str
    port: str | None = None
    status__name: str
    description: str
    tags: list[TagDict] = []

    @classmethod
    @override
    def get_queryset(cls):
        return ServiceObject.objects.filter(tags__name="FortiManager")
