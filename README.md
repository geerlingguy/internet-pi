# Internet Pi

[![CI](https://github.com/geerlingguy/internet-pi/workflows/CI/badge.svg?event=push)](https://github.com/geerlingguy/internet-pi/actions?query=workflow%3ACI)

**A Raspberry Pi Configuration for Internet connectivity**

I have had a couple Pis doing random Internet-related duties for years. It's finally time to formalize their configs and make all the DNS/ad-blocking/monitoring stuff encapsulated into one Ansible project.

So that's what this is.

## Features

**Internet Monitoring**: Installs Prometheus and Grafana, along with a few Docker containers to monitor your Internet connection with Speedtest.net speedtests and HTTP tests so you can see uptime, ping stats, and speedtest results over time.

![Internet Monitoring Dashboard in Grafana](images/internet-monitoring.png)

**Pi-hole**: Installs the Pi-hole Docker configuration so you can use Pi-hole for network-wide ad-blocking and local DNS. Make sure to update your network router config to direct all DNS queries through your Raspberry Pi if you want to use Pi-hole effectively!

![Pi-hole on the Internet Pi](images/pi-hole.png)

Other features:

  - **Shelly Plug Monitoring**: Installs a [`shelly-plug-prometheus` exporter](https://github.com/geerlingguy/shelly-plug-prometheus) and a Grafana dashboard, which tracks and displays power usage on a Shelly Plug running on the local network. (Disabled by default. Enable and configure using the `shelly_plug_*` vars in `config.yml`.)
  - **AirGradient Monitoring**: Configures [`airgradient-prometheus`](https://github.com/geerlingguy/airgradient-prometheus) and a Grafana dashboard, which tracks and displays air quality over time via one or more AirGradient DIY monitors. (Disabled by default. Enable and configure using the `airgradient_enable` var in `config.yml`. See example configuration for ability to monitor multiple AirGradient DIY stations.)
  - **Starlink Monitoring**: Installs a [`starlink_exporter`](https://github.com/joshuasing/starlink_exporter) and a Grafana dashboard, which tracks and displays Starlink statistics. (Disabled by default. Enable and configure using the `starlink_enable` var in `config.yml`.)

**IMPORTANT NOTE**: If you use the included Internet monitoring, it will download a decently-large amount of data through your Internet connection on a daily basis. Don't use it, or tune the `internet-monitoring` setup to not run the speedtests as often, if you have a metered connection!

## Recommended Pi and OS

You should use a Raspberry Pi 4 model B or better. The Pi 4 and later generations of Pi include a full gigabit network interface and enough I/O to reliably measure fast Internet connections.

Older Pis work, but have many limitations, like a slower CPU and sometimes very-slow NICs that limit the speed test capability to 100 Mbps or 300 Mbps on the Pi 3 model B+.

Other computers and VMs may run this configuration as well, but it is only regularly tested on a Raspberry Pi.

The configuration is tested against Raspberry Pi OS, both 64-bit and 32-bit, and runs great on that or a generic Debian installation.

It should also work with Ubuntu for Pi, or Arch Linux, but has not been tested on other operating systems.

## Setup

  1. [Install Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html). The easiest way (especially on Pi or a Debian system) is via Pip:
     1. (If on Pi/Debian): `sudo apt-get install -y python3-pip`
     2. (Everywhere): `pip3 install ansible`
     3. If you get an error like "externally-managed-environment", follow [this guide to fix it](https://www.jeffgeerling.com/blog/2023/how-solve-error-externally-managed-environment-when-installing-pip3), then run `pip3 install ansible` again.
     4. Make sure Ansible is in your PATH: `export PATH=$PATH:~/.local/bin` (and consider [adding it permanently](https://askubuntu.com/a/1113838)).
  2. Clone this repository: `git clone https://github.com/geerlingguy/internet-pi.git`, then enter the repository directory: `cd internet-pi`.
  3. Install requirements: `ansible-galaxy collection install -r requirements.yml` (if you see `ansible-galaxy: command not found`, restart your SSH session or reboot the Pi and try again)
  4. Make copies of the following files and customize them to your liking:
     - `example.inventory.ini` to `inventory.ini` (replace IP address with your Pi's IP, or comment that line and uncomment the `connection=local` line if you're running it on the Pi you're setting up).
     - `example.config.yml` to `config.yml`
  5. Run the playbook: `ansible-playbook main.yml`

> **If running locally on the Pi**: You may encounter an error like "Error while fetching server API version" or "connect: permission denied". If you do, please either reboot or log out and log back in, then run the playbook again. If you continue to receive a "permission denied while trying to connect to the Docker daemon socket" error, then you may need to first add your user to the `docker` user group: `sudo usermod -aG docker $USER`, as outlined in the [Docker documentation](https://docs.docker.com/engine/install/linux-postinstall/).

> **If DNS stops working after the first run on Raspberry Pi OS Trixie (Debian 13)**: The playbook installs `resolvconf`, which can leave `/etc/resolv.conf` empty until NetworkManager regenerates it, so name resolution fails on the Pi and the playbook stops while pulling images, with an error containing `lookup registry-1.docker.io on [::1]:53` and `connection refused`. Check with `cat /etc/resolv.conf`: if it has no `nameserver` lines, restart NetworkManager and Docker with `sudo systemctl restart NetworkManager && sudo systemctl restart docker` (or reboot), then run the playbook again if it failed. This only happens on the first run.

## Usage

### Pi-hole

Visit the Pi's IP address (e.g. http://192.168.1.10/admin) and use the `pihole_password` you configured in your `config.yml` file. An existing pi-hole installation can be left unaltered by disabling the setup of this project's installation in your `config.yml` (`pihole_enable: false`)

### Grafana

Visit the Pi's IP address with port 3030 (e.g. http://192.168.1.10:3030/), and log in with username `admin` and the password `monitoring_grafana_admin_password` you configured in your `config.yml`.

To find the dashboard, navigate to Dashboards, click Browse, then go to the Internet connection dashboard. If you star this dashboard, it will appear on the Grafana home page.

> Note: The `monitoring_grafana_admin_password` is only used the first time Grafana starts up; if you need to change it later, do it via Grafana's admin UI.

### Prometheus

A number of default Prometheus job configurations are included out of the box, but if you would like to add more to the `prometheus.yml` file, you can add a block of text that will be added to the end of the `scrape_configs` using the `prometheus_extra_scrape_configs` variable, for example:

```yaml
prometheus_extra_scrape_configs: |
  - job_name: 'customjob'
    scrape_interval: 5s
    static_configs:
      - targets: ['192.168.1.1:9100']
```

You can also add more targets to monitor via the node exporter dashboard, say if you have a number of servers or other Pis you want to monitor on this instance. Just add them to the list, after the `nodeexp:9100` entry for the main Pi:

```yaml
prometheus_node_exporter_targets:
  - 'nodeexp:9100'
  # Add more targets here
  - 'another-server.local:9100'
```

### Monitoring multiple uplinks (dual WAN)

If the Pi is connected to more than one uplink (for example one network port per WAN, or one port per VLAN where each VLAN is routed through a different WAN), set `monitoring_uplinks` in `config.yml` to measure each uplink separately:

```yaml
monitoring_uplinks:
  - name: cable
    parent_interface: eth0
    subnet: 192.0.2.0/24
    gateway: 192.0.2.1
    probe_address: 192.0.2.250
    contract_download_mbps: 600          # optional
    contract_upload_mbps: 40             # optional
    expected_isp_pattern: 'Example Cable'  # optional
    display_name: 'Example Cable (WAN1)'   # optional
  - name: dsl
    parent_interface: eth1
    subnet: 198.51.100.0/24
    gateway: 198.51.100.1
    probe_address: 198.51.100.250
    dns_servers:                         # optional
      - 198.51.100.1
```

`dns_servers` is only needed when an uplink's network cannot reach the Pi's own DNS servers; without it, the probes use the same DNS servers as the Pi.

Each uplink gets its own ping (blackbox) and speedtest exporter. The two share a container network namespace attached to a macvlan network on `parent_interface`, with `probe_address` as a static address and the uplink's `gateway` as the default route, so their traffic always leaves through that uplink. While `monitoring_uplinks` is set, the single default-route `speedtest` and `ping` containers are not started; with it empty, nothing changes.

#### What you get

The "Internet connection by uplink" dashboard shows every uplink side by side, under its `display_name`. It replaces the single-uplink "Internet connection" dashboard while `monitoring_uplinks` is set.

| Feature | What it measures | Configured with |
|---|---|---|
| Speed tests | Download, upload, ping and jitter, one uplink after another | `monitoring_speedtest_interval`, `monitoring_uplink_speedtest_offset` |
| HTTP checks | Whether websites answer, and how fast, as in the single-uplink setup | `monitoring_ping_hosts` |
| Latency and packet loss | ICMP round-trip time and loss, which measure the line itself | `monitoring_uplink_icmp_hosts` |
| % of contract (optional) | Average speed as a percentage of the speed you pay for | `contract_download_mbps`, `contract_upload_mbps` |
| Failover check (optional) | Every 5 minutes, whether the uplink's traffic still leaves through its own ISP | `expected_isp_pattern`, `monitoring_uplink_egress_lookup_url` |

Speed tests never run at the same time, so they do not compete for the Pi's CPU. They run once per `monitoring_speedtest_interval`, `monitoring_uplink_speedtest_offset` after each interval boundary; boundaries are aligned to UTC, so `60m` and `5m` mean every hour at :05. Results are kept in a Prometheus Pushgateway, which Prometheus scrapes.

##### Alerts:

  - `uplink_down`: no ping target reachable through the uplink.
  - `uplink_speedtest_failed`: the last speed test did not complete.
  - `uplink_speedtest_stale`: no speed test result for two intervals.
  - `uplink_unexpected_isp`: the uplink's traffic leaves through another ISP, for example after your router failed it over to another WAN (needs `expected_isp_pattern`).

In Prometheus, every series carries an `uplink` label with the uplink's `name`; the readable name comes from the `uplink_info` series.

#### Requirements

  - **One wired port per uplink**: Either built in, PCIe, or a USB Ethernet adapter. The tested setup is a board whose second port is a USB 3 gigabit chip, like a Raspberry Pi 4 with a USB 3 gigabit adapter.
    - Wi-Fi interfaces cannot be used, because macvlan does not work on them.
    - The adapter must accept extra MAC addresses (common gigabit chipsets do).
    - With several USB adapters, names like `eth1` and `eth2` can swap between boots; use their `enx...` names or fixed names from a udev rule.
    - A single port carrying tagged VLANs (for example `parent_interface: eth0.5`) is untested, and the playbook expects `parent_interface` to exist already.
  - **A reserved `probe_address` per uplink**: It needs to be outside your router's DHCP pool. Docker assigns it statically.
  - **Docker Engine 28.0 or newer and Docker Compose 2.33.1 or newer**: For `gw_priority`. The playbook checks this and stops with a message if Docker is older; it does not upgrade an existing Docker installation.

#### Limitations

  - **The Pi itself cannot reach the probe addresses**: This is a macvlan limitation. Prometheus reaches the probes over the internal `back-tier` network instead, so monitoring is not affected. The per-uplink ping exporter listens only on that internal network, so other devices on the uplink's LAN cannot use its `/probe` endpoint.
  - **The speedtest exporter port is reachable from the uplink's LAN**: The exporter has no option to choose its listening address, so anyone on that LAN can open `http://<probe_address>:9798/metrics`, which starts an extra speed test (it uses bandwidth but exposes nothing). If that matters on your network, block that port for other devices on the same network, if your switches or access points support such rules.
  - **Failover changes what an uplink measures**: If your router fails an uplink's network over to another WAN, that uplink's probes keep reporting, but with the other WAN's numbers. Set `expected_isp_pattern` to be alerted, or disable failover for that network on the router.
  - **"% of contract" is a quick indicator, not a legal measurement**: Where regulators define how to prove a slow connection (for example the Breitbandmessung app in Germany), use their tool for any claim.

#### Changing ISP on an uplink

Display names and contract speeds are read at the end of the dashboard's time range, so the whole range follows the `config.yml` in effect at that moment (the current one, for a range that ends now):

  - **Keep the uplink's `name`**: The old ISP's history appears under the new `display_name`, and its "% of contract" is measured against the new contract.
  - **Give the uplink a new `name`**: It starts a fresh history. The old ISP's data stays in Prometheus until `prometheus_tsdb_retention_time` removes it (Grafana's Explore view can still query it), but the dashboard no longer shows it.

Either way, update `expected_isp_pattern`, or the `uplink_unexpected_isp` alert fires.

## Updating

### pi-hole

To upgrade Pi-hole to the latest version, run the following commands:

```bash
cd ~/pi-hole # 
docker compose pull             # pulls the latest images
docker compose up -d --no-deps  # restarts containers with newer images
docker system prune --all       # deletes unused images
```

### Configurations and internet-monitoring images

Upgrades for the other configurations are similar (go into the directory, and run the same `docker compose` commands. Make sure to `cd` into the `config_dir` that you use in your `config.yml` file. 

Alternatively, you may update the initial `config.yml` in the the repo folder and re-run the main playbook: `ansible-playbook main.yml`. At some point in the future, a dedicated upgrade playbook may be added, but for now, upgrades may be performed manually as shown above.

## Backups

A guide for backing up the configurations and historical data will be posted here as part of [Issue #194: Create Backup guide](https://github.com/geerlingguy/internet-pi/issues/194).

## Uninstall

To remove `internet-pi` from your system, run the following commands (assuming the default install location of `~`, your home directory):

```bash
# Enter the internet-monitoring directory.
cd ~/internet-monitoring

# Shut down internet-monitoring containers and delete data volumes.
docker compose down -v

# Enter the pi-hole directory.
cd ~/pi-hole

# Shutdown pi-hole containers and delete data volumes.
docker compose down -v

# Delete all the unused container images, volumes, etc. from the system.
docker system prune -af
```

Do the same thing for any of the other optional directories added by this project (e.g. `shelly-plug-prometheus`, `starlink-exporter`, etc.).

You can then delete the `internet-monitoring`, `pi-hole`, etc. folders and everything will be gone from your system.

## License

MIT

## Author

This project was created in 2021 by [Jeff Geerling](https://www.jeffgeerling.com/).
