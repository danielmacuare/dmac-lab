# netbox-docker

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/netbox-community/netbox-docker)][github-release]
[![GitHub stars](https://img.shields.io/github/stars/netbox-community/netbox-docker)][github-stargazers]
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed-raw/netbox-community/netbox-docker)
![Github release workflow](https://img.shields.io/github/actions/workflow/status/netbox-community/netbox-docker/release.yml?branch=release)
![Docker Pulls](https://img.shields.io/docker/pulls/netboxcommunity/netbox)
[![GitHub license](https://img.shields.io/github/license/netbox-community/netbox-docker)][netbox-docker-license]

[The GitHub repository][netbox-docker-github] houses the components needed to build NetBox as a container.
Images are built regularly using the code in that repository
and are pushed to [Docker Hub][netbox-dockerhub],
[Quay.io][netbox-quayio] and [GitHub Container Registry][netbox-ghcr].
_NetBox Docker_ is a project developed and maintained by the _NetBox_ community.

Do you have any questions?
Before opening an issue on GitHub,
please join [our Slack][netbox-docker-slack]
and ask for help in the [`#netbox-docker`][netbox-docker-slack-channel] channel,
or start a new [GitHub Discussion][github-discussions].

[github-stargazers]: https://github.com/netbox-community/netbox-docker/stargazers
[github-release]: https://github.com/netbox-community/netbox-docker/releases
[netbox-dockerhub]: https://hub.docker.com/r/netboxcommunity/netbox/
[netbox-quayio]: https://quay.io/repository/netboxcommunity/netbox
[netbox-ghcr]: https://github.com/netbox-community/netbox-docker/pkgs/container/netbox
[netbox-docker-github]: https://github.com/netbox-community/netbox-docker/
[netbox-docker-slack]: https://join.slack.com/t/netdev-community/shared_invite/zt-mtts8g0n-Sm6Wutn62q_M4OdsaIycrQ
[netbox-docker-slack-channel]: https://netdev-community.slack.com/archives/C01P0GEVBU7
[netbox-slack-channel]: https://netdev-community.slack.com/archives/C01P0FRSXRV
[netbox-docker-license]: https://github.com/netbox-community/netbox-docker/blob/release/LICENSE
[github-discussions]: https://github.com/netbox-community/netbox-docker/discussions


## Custom User Notes
- For simplicity all vars have been moved to a single file called netbox.env
- This is how Netbox creates the initial superuser: [HERE](https://github.com/netbox-community/netbox-docker/blob/0b70f722f91cf90e5fa0178f3db84d28517e191d/docker/docker-entrypoint.sh#L53-L72)
- Some Env Vars Defaults [HERE](https://artifacthub.io/packages/helm/bootc/netbox)
- I have modified the default config using a docker-compose.override.yml to expose Netbox over port 8001 instead of the default 8000
- I have enabled memory overcommit to sort the issue below: `echo "vm.overcommit_memory=1" | sudo tee -a /etc/sysctl.conf` then reload the config `sudo sysctl -p`

```bash
 ✔ Container netbox-docker-redis-1                 Created                                                                                                                   0.0s
 ✔ Container netbox-docker-netbox-1                Created                                                                                                                   0.0s
 ✔ Container netbox-docker-netbox-housekeeping-1   Created                                                                                                                   0.0s
 ✔ Container netbox-docker-netbox-worker-1         Created                                                                                                                   0.0s
Attaching to netbox-1, netbox-housekeeping-1, netbox-worker-1, postgres-1, redis-1, redis-cache-1
redis-cache-1          | 1:C 13 Feb 2025 22:35:52.042 # WARNING Memory overcommit must be enabled! Without it, a background save or replication may fail under low memory condition. Being disabled, it can also cause failures without low memory condition, see https://github.com/jemalloc/jemalloc/issues/1328. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.
```
- TODO:
  - Continue installing plugins

- FIX:
  - After enabling the memmory overcommit the netbox-docker-redis-cache-1 sitll is marked as unhealthy. After checking the logs, there are no indications of errrors. Not sure if this is really an issue.
  - Fix CSRF Errors: https://github.com/netbox-community/netbox/discussions/9043


## Quickstart

To get _NetBox Docker_ up and running run the following commands.
There is a more complete [_Getting Started_ guide on our wiki][wiki-getting-started] which explains every step.

```bash
git clone -b release https://github.com/netbox-community/netbox-docker.git
cd netbox-docker
tee docker-compose.override.yml <<EOF
services:
  netbox:
    ports:
      - 8000:8080
EOF
docker compose pull
docker compose up
```

The whole application will be available after a few minutes.
Open the URL `http://0.0.0.0:8000/` in a web-browser.
You should see the NetBox homepage.

To create the first admin user run this command:

```bash
docker compose exec netbox /opt/netbox/netbox/manage.py createsuperuser
```

If you need to restart Netbox from an empty database often,
you can also set the `SUPERUSER_*` variables in your `docker-compose.override.yml`.

[wiki-getting-started]: https://github.com/netbox-community/netbox-docker/wiki/Getting-Started

## Container Image Tags

New container images are built and published automatically every ~24h.

> We recommend to use either the `vX.Y.Z-a.b.c` tags or the `vX.Y-a.b.c` tags in production!

- `vX.Y.Z-a.b.c`, `vX.Y-a.b.c`:
  These are release builds containing _NetBox version_ `vX.Y.Z`.
  They contain the support files of _NetBox Docker version_ `a.b.c`.
  You must use _NetBox Docker version_ `a.b.c` to guarantee the compatibility.
  These images are automatically built from [the corresponding releases of NetBox][netbox-releases].
- `latest-a.b.c`:
  These are release builds, containing the latest stable version of NetBox.
  They contain the support files of _NetBox Docker version_ `a.b.c`.
  You must use _NetBox Docker version_ `a.b.c` to guarantee the compatibility.
- `snapshot-a.b.c`:
  These are prerelease builds.
  They contain the support files of _NetBox Docker version_ `a.b.c`.
  You must use _NetBox Docker version_ `a.b.c` to guarantee the compatibility.
  These images are automatically built from the [`main` branch of NetBox][netbox-main].

For each of the above tag, there is an extra tag:

- `vX.Y.Z`, `vX.Y`:
  This is the same version as `vX.Y.Z-a.b.c` (or `vX.Y-a.b.c`, respectively).
- `latest`
  This is the same version as `latest-a.b.c`.
  It always points to the latest version of _NetBox Docker_.
- `snapshot`
  This is the same version as `snapshot-a.b.c`.
  It always points to the latest version of _NetBox Docker_.

[netbox-releases]: https://github.com/netbox-community/netbox/releases
[netbox-main]: https://github.com/netbox-community/netbox/tree/main

## Documentation

Please refer [to our wiki on GitHub][netbox-docker-wiki] for further information on how to use the NetBox Docker image properly.
The wiki covers advanced topics such as using files for secrets, configuring TLS, deployment to Kubernetes, monitoring and configuring LDAP.

Our wiki is a community effort.
Feel free to correct errors, update outdated information or provide additional guides and insights.

[netbox-docker-wiki]: https://github.com/netbox-community/netbox-docker/wiki/

## Getting Help

Feel free to ask questions in our [GitHub Community][netbox-community]
or [join our Slack][netbox-docker-slack] and ask [in our channel `#netbox-docker`][netbox-docker-slack-channel],
which is free to use and where there are almost always people online that can help you.

If you need help with using NetBox or developing for it or against it's API
you may find [the `#netbox` channel][netbox-slack-channel] on the same Slack instance very helpful.

[netbox-community]: https://github.com/netbox-community/netbox-docker/discussions

## Dependencies

This project relies only on _Docker_ and _docker-compose_ meeting these requirements:

- The _Docker version_ must be at least `20.10.10`.
- The _containerd version_ must be at least `1.5.6`.
- The _docker-compose version_ must be at least `1.28.0`.

To check the version installed on your system run `docker --version` and `docker compose version`.

## Updating

Please read [the release notes][releases] carefully when updating to a new image version.
Note that the version of the NetBox Docker container image must stay in sync with the version of the Git repository.

If you update for the first time, be sure [to follow our _How To Update NetBox Docker_ guide in the wiki][netbox-docker-wiki-updating].

[releases]: https://github.com/netbox-community/netbox-docker/releases
[netbox-docker-wiki-updating]: https://github.com/netbox-community/netbox-docker/wiki/Updating

## Rebuilding the Image

`./build.sh` can be used to rebuild the container image.
See `./build.sh --help` for more information or `./build-latest.sh` for an example.

For more details on custom builds [consult our wiki][netbox-docker-wiki-build].

[netbox-docker-wiki-build]: https://github.com/netbox-community/netbox-docker/wiki/Build

## Tests

We have a test script.
It runs NetBox's own unit tests and ensures that NetBox starts:

```bash
IMAGE=docker.io/netboxcommunity/netbox:latest ./test.sh
```

## Support

This repository is currently maintained by the community.
The community is expected to help each other.

Please consider sponsoring the maintainers of this project.
