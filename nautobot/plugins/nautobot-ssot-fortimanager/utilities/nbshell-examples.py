# All Components of a Model
from typing import Any

from nautobot_firewall_models.models import PolicyRule
from rich import inspect

pol: Any = PolicyRule.objects.all()
# inspect(pol)
inspect(pol.__dict__)

from nautobot_firewall_models.models import PolicyRule

PolicyRule.