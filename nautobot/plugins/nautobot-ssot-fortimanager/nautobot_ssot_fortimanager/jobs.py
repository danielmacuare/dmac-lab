"""Nautobot Job to update an Address Object in the Firewall Data Modell"""

from typing import override

from nautobot.apps.jobs import BooleanVar, ObjectVar, register_jobs
from nautobot.extras.choices import SecretsGroupAccessTypeChoices, SecretsGroupSecretTypeChoices
from nautobot.extras.models import SecretsGroup
from nautobot_ssot.jobs.base import DataSource

# FMG_URL
# FMG_USER
# FMG_PASS
# FMG-SEC-GROUP
name = "Nautobot SSOT - FortiManager"


class FortiManagerDataSource(DataSource):
    "FortiManager SSOT Data Source"

    fmg_details = ObjectVar(model=SecretsGroup, description="Select FortiManager Details")

    use_cache = BooleanVar(description="Use cache file if available for FortiManager Data")

    class Meta:
        name: str = "FortiManager into Nautobot"
        data_source: str = "FortiManager"
        data_target: str = "Nautobot"
        description: str = "Sync data from FortiManager into Nautobot"
        has_sensitive_variables: bool = False
        soft_time_limit: int = 7200
        time_limit: int = 7500

    @override
    def load_source_adapter(self):
        # --- START DEBUGGING ---
        self.logger.info(f"Value of self.fmg_details: {self.fmg_details}")
        self.logger.info(f"Type of self.fmg_details: {type(self.fmg_details)}")
        # --- END DEBUGGING ---

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

    @override
    def load_target_adapter(self):
        self.logger.info("Create Target Adapter Nautobot")
        self.logger.info("Loading Target Data from Nautobot")
        self.logger.info("Nautobot Data Load")

    @override
    def run(self, fmg_details, use_cache, dryrun, memory_profiling, *args, **kwargs):
        self.fmg_details = fmg_details
        self.use_cache = use_cache
        self.dryrun = dryrun
        self.memory_profiling = memory_profiling
        self.logger.debug(f"Secrets group: {fmg_details} selecte")
        super().run(dryrun=self.dryrun, memory_profiling=self.memory_profiling, **kwargs)


jobs = [FortiManagerDataSource]
register_jobs(*jobs)
