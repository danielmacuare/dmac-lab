"""Nautobot Job to update an Address Object in the Firewall Data Modell"""

from nautobot.apps.jobs import BooleanVar, ObjectVar, register_jobs
from nautobot.extras.choices import SecretsGroupAccessTypeChoices, SecretsGroupSecretTypeChoices
from nautobot.extras.models import SecretsGroup
from nautobot_ssot.jobs.base import DataSource

# FMG_URL
# FMG_USER
# FMG_PASS


class FortiManagerDataSource(DataSource):
    "FortiManager SSOT Data Source"

    fmg_details = ObjectVar(model=SecretsGroup, description="Select FortiManager Details")

    use_cache = BooleanVar(description="Use cache file if available for FortiManager Data")

    class Meta:
        name: str = "FortiManger to Nautobot"
        data_source: str = "FortiManager"
        data_target: str = "Nautobot"
        descritpion: str = "Sync data from FortiManager into Nautobot"
        has_sensitive_variables: bool = False
        soft_time_limit: int = 7200
        time_limit: int = 7500

    def load_source_adapter(self):
        url = self.fmg_details.get_secret_value(
            SecretsGroupAccessTypeChoices.TYPE_HTTP, SecretsGroupSecretTypeChoices.TYPE_URL
        )
        username = self.fmg_details.get_secret_value(
            SecretsGroupAccessTypeChoices.TYPE_HTTP, SecretsGroupSecretTypeChoices.TYPE_USERNAME
        )
        password = self.fmg_details.get_secret_value(
            SecretsGroupAccessTypeChoices.TYPE_HTTP, SecretsGroupSecretTypeChoices.TYPE_PASSWORD
        )

        self.logger.info(msg=f"Will connect to {url} with {username} and pass: {password}")


jobs = [FortiManagerDataSource]
register_jobs(*jobs)
