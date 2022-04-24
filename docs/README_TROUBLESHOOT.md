# Troubleshooting
This page lists solutions to problems you might encounter with internet-pi.

## Debug
Learn how to get detailed information about what is happening when using internet-pi.

* [Debug Ansible](docs/debug/debug_ansible.md)
* [Debug Docker-Compose](docs/debug/debug_docker.md)
* [Debug the Docker containers](docs/debug/debug_docker_containers.md)

## Potential Problems
Here is a list of potential problems based on user issues.

* [Ansible-playbook main.yml fails to finish - permission denied](doc/common_problems/permission_denied.md)
* [Ports already in use](doc/common_problems/ports_already_in_use.md)
* [Internet-monitoring fails due to missing nameserver setting in target](doc/common_problems/target_nameserver_setting.md) issue 349
* [Change Grafana settings](docs/common_problems/grafana_settings.md)
* [Multiple Python versions are installed on the target](docs/common_problems/multiple_python_versions_installed.md)

## Specific Issues with other repos
If you have any usage specific issue, which is not related to the Ansible setup process, then please check the other repos and the issues mentioned there. The pages linked below provide detailed information about the repos that internet-pi relies on.

Issues with:
* [Grafana](https://github.com/grafana/grafana/issues?q=is%3Aissue) or [Grafana Docker](https://github.com/grafana/grafana-docker/issues?q=is%3Aissue)
* [Prometheus](https://github.com/prometheus/prometheus/issues?q=is%3Aissue), [Prometheus Blackbox Exporter](https://github.com/prometheus/blackbox_exporter/issues?q=is%3Aissue), or  [Prometheus Node Exporter](https://github.com/prometheus/node_exporter/issues?q=is%3Aissue)
* [Speedcheck](https://github.com/MiguelNdeCarvalho/speedtest-exporter/issues?q=is%3Aissue)

Search for issues that might be applicable to your problem. <br>
It might be also a good idea to perform an online search with your error message first, before opening issues for any repo.