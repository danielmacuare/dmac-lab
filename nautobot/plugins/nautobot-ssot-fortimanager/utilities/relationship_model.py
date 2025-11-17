"""This script will print the relationships of the model"""

from nautobot.ipam.models import IPAddress
from nautobot_firewall_models.models import AddressObject
from nautobot_firewall_models.models.address import FQDN
from rich import print as rprint
from rich.console import Console
from rich.table import Table

# Only Edit the model in the following line
model = FQDN
model_name: str = model.__name__


console = Console()
rich_table = Table(
    title=f"{model_name} Model Fields and Relationships",
    show_lines=True,
    header_style="bold magenta",
)
rich_table.add_column("Field Name", style="cyan", no_wrap=True)
rich_table.add_column("Type", style="green")
rich_table.add_column("Relation Type", style="yellow")
rich_table.add_column("Related Model", style="blue")
rich_table.add_column("Related Field on Model", style="purple")

for field in model._meta.get_fields():
    field_name = field.name
    field_type = type(field).__name__
    relation_type = "N/A"
    related_model_name = "N/A"
    related_field_on_model = "N/A"

    if field.is_relation:
        relation_type = field_type
        if field.related_model:
            related_model_name = field.related_model.__name__
        if (
            hasattr(field, "field") and field.field
        ):  # For reverse relations (e.g., ManyToOneRel)
            related_field_on_model = field.field.name

        rich_table.add_row(
            field_name,
            "Relation",
            relation_type,
            related_model_name,
            related_field_on_model,
        )
    elif field.concrete:
        # For concrete fields, field_type is already the type name (e.g., 'CharField', 'IntegerField')
        rich_table.add_row(
            field_name,
            "Direct Attribute",
            relation_type,  # N/A
            related_model_name,  # N/A
            related_field_on_model,  # N/A
        )

console.print(rich_table)
