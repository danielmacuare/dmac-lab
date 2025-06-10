# Nautobot SSOT FortiManager
This app/plugin will help us pull information from FortiManager into the Nautobot Firewall Models

In this case we will use the [SSOT framework](https://github.com/nautobot/nautobot-app-ssot) which is built on top of the [DiffSync Library](https://github.com/networktocode/diffsync) which will provide us functionality to compare the data stored in Nautobot against the data received from FortiManager.

## Useful Links
- [Nautobot App Development Docs](https://docs.nautobot.com/projects/core/en/stable/development/apps/)
- [Nautobot Docker Compose - App Installation](https://github.com/nautobot/nautobot-docker-compose/blob/main/docs/plugins.md)
- [SSOT framework](https://github.com/nautobot/nautobot-app-ssot)
- [DiffSync Library](https://github.com/networktocode/diffsync) 

## How to create a custom App:
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
```
PLUGINS_CONFIG = {
    nautobot_ssot_fortimanager = {}
}
```
- Update the main pyproject.py file in the root of the project to indicate poetry where to find the custom app:
```
nautobot-ssot-fortimanager = {path = "plugins/nautobot-ssot-fortimanager"}
```
- Re-build and re-deploy the container with:
```
invoke stop or ctr+c on an already opened invoke debug session.
invoke build --no-cache
invoke debug
```
- Apps need to be also 


## Gotchas
- I had some issues when dealing with different pyprojects (one pyproject per app + the root pyproject):
    - By default Nautobot-docker-compose comes with poetry version 1.8.4. This poetry usually configures the project and it's dependendencies under [tool.poetry.x].
    - Newer versions of poetry configure a project under [project] and [dependencies].
    - This causes issues when dealing with Nautobot so I had 2 options
        - Upgrade the base image to use a newer version of poetry and fix the main pyproject file.
        - (Simpler) Downgrade the poetry version I was using to generate the pyporject.toml to match what nautobot-docker-compose ships with (poetry 1.8.4)
        - In my case, I chose option 2, to use the same version than nautobot to make it simpler and avoid issues.