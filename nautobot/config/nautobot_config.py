"""Nautobot development configuration file."""

# pylint: disable=invalid-envvar-default
import os
import sys

from nautobot.core.settings import *  # noqa: F403  # pylint: disable=wildcard-import,unused-wildcard-import
from nautobot.core.settings_funcs import is_truthy, parse_redis_connection

#
# Debug
#

DEBUG = is_truthy(os.getenv("NAUTOBOT_DEBUG", False))

TESTING = len(sys.argv) > 1 and sys.argv[1] == "test"

#
# Logging
#

LOG_LEVEL = "DEBUG" if DEBUG else "INFO"

#
INSTALLATION_METRICS_ENABLED = False

#
# Redis
#

# Redis Cacheops
CACHEOPS_REDIS = parse_redis_connection(redis_database=1)

#
# Celery settings are not defined here because they can be overloaded with
# environment variables. By default they use `CACHES["default"]["LOCATION"]`.
#

# Enable installed plugins. Add the name of each plugin to the list.
# PLUGINS = ["nautobot_example_plugin"]
PLUGINS = [
    "nautobot_plugin_nornir",
    "nautobot_golden_config",
    "nautobot_ssot",
    "nautobot_bgp_models",
    "nautobot_device_onboarding",
    "nautobot_firewall_models",
    "nautobot_ssot_fortimanager",
]

# Plugins configuration settings. These settings are used by various plugins that the user may have installed.
# Each key in the dictionary is the name of an installed plugin and its value is a dictionary of settings.

PLUGINS_CONFIG = {
    "nautobot_plugin_nornir": {
        "nornir_settings": {
            # "credentials": "nautobot_plugin_nornir.plugins.credentials.env_vars.CredentialsEnvVars",
            # Below comes from: https://docs.nautobot.com/projects/device-onboarding/en/latest/admin/install/#install-guide
            "credentials": "nautobot_plugin_nornir.plugins.credentials.nautobot_secrets.CredentialsNautobotSecrets",
            "runner": {
                "plugin": "threaded",
                "options": {
                    "num_workers": 20,
                },
            },
        },
    },
    # https://docs.nautobot.com/projects/golden-config/en/latest/admin/install/#app-configuration
    "nautobot_golden_config": {
        "per_feature_bar_width": 0.15,
        "per_feature_width": 13,
        "per_feature_height": 4,
        "enable_backup": True,
        "enable_compliance": True,
        "enable_intended": True,
        "enable_sotagg": True,
        "enable_plan": True,
        "enable_deploy": True,
        "enable_postprocessing": False,
        "sot_agg_transposer": None,
        "postprocessing_callables": [],
        "postprocessing_subscribed": [],
        "jinja_env": {
            "undefined": "jinja2.StrictUndefined",
            "trim_blocks": True,
            "lstrip_blocks": False,
        },
        # "default_deploy_status": "Not Approved",
        # "get_custom_compliance": "my.custom_compliance.func"
    },
    "nautobot_ssot": {"hide_example_jobs": True},
    "nautobot_bgp_models": {},
    "nautobot_device_onboarding": {},
    "nautobot_firewall_models": {
        "default_status": "Active",
        "allowed_status": ["Active"],  # default shown, `[]` allows all
        "capirca_remark_pass": True,
        "capirca_os_map": {
            "cisco_ios": "cisco",
            "arista_eos": "arista",
        },
        # "custom_capirca": "my.custom.func", # provides ability to overide capirca logic
    },
}
