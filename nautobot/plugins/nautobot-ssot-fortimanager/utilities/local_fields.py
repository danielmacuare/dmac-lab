"""This scripts generates a table with Concrete fields and with local fields for an Object"""

from nautobot.ipam.models import IPAddress
from nautobot_firewall_models.models import AddressObject, FQDN, IPRange, ServiceObject
from rich import print
from rich.console import Console
from rich.table import Table

# Only Edit the model in the following line
model = IPAddress
model_name: str = model.__name__


console = Console()  # Create a Console instance for more control

rich_table = Table(
    title=f"Django Model Fields (Concrete) - MODEL: {model_name}",
    show_lines=True,
    header_style="bold magenta",
)
rich_table.add_column("Field Name", style="cyan", no_wrap=True)
rich_table.add_column("Field Type", style="green")
rich_table.add_column("Is Relation?", style="yellow")
rich_table.add_column("Related Model", style="blue")

for field in model._meta.concrete_fields:
    # Determine if it's a relation and get the related model name
    is_relation_str = "Yes" if field.is_relation else "No"
    related_model_name = field.related_model.__name__ if field.is_relation else ""

    rich_table.add_row(
        field.name, type(field).__name__, is_relation_str, related_model_name
    )

console.print(rich_table)  # Print the table using the console

# Create a new Table instance for local fields
rich_table_local = Table(
    title=f"Django Model Fields (Local) - MODEL: {model_name}",
    show_lines=True,
    header_style="bold magenta",
)
rich_table_local.add_column("Field Name", style="cyan", no_wrap=True)
rich_table_local.add_column("Field Type", style="green")
rich_table_local.add_column("Is Relation?", style="yellow")
rich_table_local.add_column("Related Model", style="blue")

for field in model._meta.local_fields:
    is_relation_str = "Yes" if field.is_relation else "No"
    related_model_name = field.related_model.__name__ if field.is_relation else ""

    rich_table_local.add_row(
        field.name, type(field).__name__, is_relation_str, related_model_name
    )

console.print(rich_table_local)  # Print the table using the console
