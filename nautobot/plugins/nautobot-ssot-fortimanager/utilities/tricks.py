## All Devices and ID
from nautobot.dcim.models import Device, Location
from rich import print as rprint

all_devices = Device.objects.all()

for dev in all_devices:
    rprint(f"Device: {dev.name} - ID: {dev.id}")


## All Roles
from nautobot.extras.models import Role

# all_roles =
