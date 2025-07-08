# Nautobot SSOT FortiManager

This app/plugin will help us pull information from FortiManager into the Nautobot Firewall Models

In this case we will use the [SSOT framework](https://github.com/nautobot/nautobot-app-ssot) which is built on top of the [DiffSync Library](https://github.com/networktocode/diffsync) which will provide us functionality to compare the data stored in Nautobot against the data received from FortiManager.

## TO-DO

- Create a diffsync model to load data from a source (JSON) and update the Target (Nautobot)
  - Update nautobot.ipam.IPAddress with an IP
- Fix use_cache
- Remove unnecessarey create(), updated(), delete() methods.

## Pre-Requisites

- The following variables are expected to be passed to the application

```bash
SOURCE_FILE_PATH: str = "/opt/nautobot/fw_addresses.json"
FORTIMANAGER_NAUTOBOT_NAMESPACE: str = "FortiManager"
```

- SOURCE_FILE_PATH: This variable will contain a Path to the  JSON Object that will hold the data. This path will then need to be mounted in the following containers (Nautobot and Celery BHeat containers)
- FORTIMANAGER_NAUTOBOT_NAMESPACE: This env var will hold the name of the IPAM Namespace that is already created where the Source Objects will be store.

## Useful Links

- [Nautobot App Development Docs](https://docs.nautobot.com/projects/core/en/stable/development/apps/)
- [Nautobot Docker Compose - App Installation](https://github.com/nautobot/nautobot-docker-compose/blob/main/docs/plugins.md)
- [SSOT framework](https://github.com/nautobot/nautobot-app-ssot)
- [DiffSync Library](https://github.com/networktocode/diffsync)

## How to create a custom App

- In this section we will create an app called `nautobot_ssot_fortimanager`
- Update the main nautobot_config.py file to add the app:

```bash
PLUGINS = [
    "nautobot_plugin_nornir",
    "nautobot_golden_config",
    "nautobot_ssot",
    "nautobot_bgp_models",
    "nautobot_device_onboarding",
    "nautobot_firewall_models",
    "nautobot_ssot_fortimanager",
]
```

- Add any config that the config is expecting under the `PLUGINS_CONFIG` key

```python
PLUGINS_CONFIG = {
    "nautobot_ssot_fortimanager" = {}
}
```

- Update the main pyproject.py file in the root of the project to indicate poetry where to find the custom app:

```python
nautobot-ssot-fortimanager = {path = "plugins/nautobot-ssot-fortimanager"}
```

- Re-build and re-deploy the container with:

```bash
invoke stop or ctr+c on an already opened invoke debug session.
invoke build --no-cache
invoke debug
```

## Gotchas

- I had some issues when dealing with different pyprojects (one pyproject per app + the root pyproject):
  - By default Nautobot-docker-compose comes with poetry version 1.8.4. This poetry usually configures the project and it's dependendencies under [tool.poetry.x].
  - Newer versions of poetry configure a project under [project] and [dependencies].
  - This causes issues when dealing with Nautobot so I had 2 options
    - Upgrade the base image to use a newer version of poetry and fix the main pyproject file.
    - (Simpler) Downgrade the poetry version I was using to generate the pyporject.toml to match what nautobot-docker-compose ships with (poetry 1.8.4)
    - In my case, I chose option 2, to use the same version than nautobot to make it simpler and avoid issues.

## Process to create a new Job

- pass use_cache (D)
- Add the common Diffsync Model to base.py (D)
- Add the DiffSync model to the top_level attribute (D)
  - Source Adapter top_level update (D)
  - Target Adapter top_level update (D)
- Add the Source Adapter code to translate daa into the Generic Diffsync model(D)

New Class(Done)
    FortiManagerIPAddressAdapter --> FortiManagerFWRulesAdapter (D)
    NautobotIPAddressAdapter --> NautobotFWRulesAdapter (D)

New Methods
    # Address
    - load_ip ---> load_ip_addresses (done)
    - load_fqdns
    - load_ip_ranges
    - load_address_objects
    - load_address_objects_groups

    # Service
    - load_service_objects
    - load_service_objects_groups
    
    # Zones
    - load_zones
    
    # Policy
    - load_policy_rules
    - load_policies