"""Nautobot DiffSync Models for FortiManager SSOT"""

from typing import Any, override

from nautobot.ipam.models import IPAddress

from nautobot_ssot_fortimanager.diffsync.models.base import IPAddressDiffSyncModel


class NautobotIPAddressDiffSyncModel(IPAddressDiffSyncModel):
    """Model to deal with Nautobot IP Addresses from the ipam.IPAddress Model"""

    @classmethod
    @override
    def create(cls, adapter, ids, attrs):
        """
        This method overrides the create method on the base classes DiffSync.DiffSyncModel.create()
        Without this class, this method will be handled by the DiffSync class that will
        create an instance if the sync process requires it.
        """

        adapter.job.logger.info("Creating IP Address: %s %s", ids, attrs)
        # Getting current objects Loaded into the Diffsync instances Nautobot
        ip_add_obj = IPAddress.objects.get(
            name=ids["host"], parent__namespace__name=ids["parent__namespace__name"]
        )
        adapter.log.info("IP Address Created: %s", ip_add_obj)

        try:
            adapter.log.info("IP Add Obj: %s", ip_add_obj)
        except Exception as ip_address_err:
            adapter.job.logger.info(f" Could not create IP Address. Error {ip_address_err}")

    # MOdify
    @override
    def update(self, attrs: Any):
        """Modify IP Addresses in Nautobot"""

        self.adapter.log.info(
            f"DEBUG: Entering update method for IP: {self.host} ({self.parent__namespace__name})"
        )
        self.adapter.log.info(f"DEBUG: Attributes received for update: {attrs}")

        obj = self.get_from_db()

        # Update description if it's present in attrs (meaning it changed in source and DiffSync detected it)
        if "description" in attrs:
            updated_description = attrs["description"]
            self.adapter.log.info(
                f"DEBUG: Updating description from '{obj.description}' to '{updated_description}'"
            )
            obj.description = updated_description
        else:
            self.adapter.log.info("DEBUG: 'description' not in attrs for this update. No change from source.")

        return super().update_base(attrs)

    @override
    def delete(self):
        return super().delete_base()

    # Delete

    # Test that only what's in the JSON Gets created
