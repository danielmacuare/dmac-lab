"""This scripts generates a table with Concrete fields and with local fields for an Object"""

from nautobot_firewall_models.models.address import (
    FQDN as model_name,
)  # Assuming this is your model_name
from rich import print
from rich.console import Console
from rich.table import Table

console = Console()  # Create a Console instance for more control

print("\n--- CONCRETE FIELDS (_meta.concrete_fields) ---")
# Create a new Table instance
table_concrete = Table(
    title="Django Model Fields (Concrete)", show_lines=True, header_style="bold magenta"
)
table_concrete.add_column("Field Name", style="cyan", no_wrap=True)
table_concrete.add_column("Field Type", style="green")
table_concrete.add_column("Is Relation?", style="yellow")
table_concrete.add_column("Related Model", style="blue")

for field in model_name._meta.concrete_fields:
    # Determine if it's a relation and get the related model name
    is_relation_str = "Yes" if field.is_relation else "No"
    related_model_name = field.related_model.__name__ if field.is_relation else ""

    table_concrete.add_row(
        field.name, type(field).__name__, is_relation_str, related_model_name
    )

console.print(table_concrete)  # Print the table using the console

print("\n### LOCAL FIELDS (_meta.local_fields) ###")
# Create a new Table instance for local fields
table_local = Table(
    title="Django Model Fields (Local)", show_lines=True, header_style="bold magenta"
)
table_local.add_column("Field Name", style="cyan", no_wrap=True)
table_local.add_column("Field Type", style="green")
table_local.add_column("Is Relation?", style="yellow")
table_local.add_column("Related Model", style="blue")

for field in model_name._meta.local_fields:
    is_relation_str = "Yes" if field.is_relation else "No"
    related_model_name = field.related_model.__name__ if field.is_relation else ""

    table_local.add_row(
        field.name, type(field).__name__, is_relation_str, related_model_name
    )

console.print(table_local)  # Print the table using the console
