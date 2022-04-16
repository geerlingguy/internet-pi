# Internet Pi

[![CI](https://github.com/geerlingguy/internet-pi/workflows/CI/badge.svg?event=push)](https://github.com/geerlingguy/internet-pi/actions?query=workflow%3ACI)

**A Raspberry Pi Configuration for Internet connectivity**

I have had a couple Pis doing random Internet-related duties for years. It's finally time to formalize their configs and make all the DNS/ad-blocking/monitoring stuff encapsulated into one Ansible project.

So that's what this is.

## Features

**Internet Monitoring**: Installs Prometheus and Grafana, along with a few Docker containers to monitor your Internet connection with Speedtest.net speedtests and HTTP tests so you can see uptime, ping stats, and speedtest results over time.

![Internet Monitoring Dashboard in Grafana](/images/internet-monitoring.png)

**Pi-hole**: Installs the Pi-hole Docker configuration so you can use Pi-hole for network-wide ad-blocking and local DNS. Make sure to update your network router config to direct all DNS queries through your Raspberry Pi if you want to use Pi-hole effectively!

![Pi-hole on the Internet Pi](/images/pi-hole.png)

Other features:

  - **Shelly Plug Monitoring**: Installs a [`shelly-plug-prometheus` exporter](https://github.com/geerlingguy/shelly-plug-prometheus) and a Grafana dashboard, which tracks and displays power usage on a Shelly Plug running on the local network. (Disabled by default. Enable and configure using the `shelly_plug_*` vars in `config.yml`.)
  - **AirGradient Monitoring**: Configures [`airgradient-prometheus`](https://github.com/geerlingguy/airgradient-prometheus) and a Grafana dashboard, which tracks and displays air quality over time via one or more AirGradient DIY monitors. (Disabled by default. Enable and configure using the `airgradient_enable` var in `config.yml`. See example configuration for ability to monitor multiple AirGradient DIY stations.)
  - **Starlink Monitoring**: Installs a [`starlink` prometheus exporter](https://github.com/danopstech/starlink_exporter) and a Grafana dashboard, which tracks and displays Starlink statistics. (Disabled by default. Enable and configure using the `starlink_enable` var in `config.yml`.)

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
  2. Clone this repository: `git clone https://github.com/geerlingguy/internet-pi.git`, then enter the repository directory: `cd internet-pi`.
  3. Install requirements: `ansible-galaxy collection install -r requirements.yml` (if you see `ansible-galaxy: command not found`, restart your SSH session or reboot the Pi and try again)
  4. Make copies of the following files and customize them to your liking:
     - `example.inventory.ini` to `inventory.ini` (replace IP address with your Pi's IP, or comment that line and uncomment the `connection=local` line if you're running it on the Pi you're setting up).
     - `example.config.yml` to `config.yml`
  5. Run the playbook: `ansible-playbook main.yml`

> **If running locally on the Pi**: You may encounter an error like "Error while fetching server API version". If you do, please either reboot or log out and log back in, then run the playbook again.

## Usage

### Pi-hole

Visit the Pi's IP address (e.g. http://192.168.1.10/) and use the `pihole_password` you configured in your `config.yml` file.

### Grafana

Visit the Pi's IP address with port 3030 (e.g. http://192.168.1.10:3030/), and log in with username `admin` and the password `monitoring_grafana_admin_password` you configured in your `config.yml`.

To find the dashboard, navigate to Dashboards, click Browse, then go to the Internet connection dashboard. If you star this dashboard, it will appear on the Grafana home page.

> Note: The `monitoring_grafana_admin_password` is only used the first time Grafana starts up; if you need to change it later, do it via Grafana's admin UI.

## Updating

To upgrade Pi-hole to the latest version, run the following commands:

```bash
cd ~/pi-hole # 
docker-compose pull             # pulls the latest images
docker-compose up -d --no-deps  # restarts containers with newer images
docker system prune --all       # deletes unused images
```

Upgrades for the other configurations are similar (go into the directory, and run the same `docker-compose` commands. Make sure to `cd` into the `config_dir` that you use in your `config.yml` file.

At some point in the future, a dedicated upgrade playbook may be added, but for now, upgrades may be performed manually as shown above.

## Backups

A guide for backing up the configurations and historical data will be posted here as part of [Issue #194: Create Backup guide](https://github.com/geerlingguy/internet-pi/issues/194).

## License

MIT

## Author

This project was created in 2021 by [Jeff Geerling](https://www.jeffgeerling.com/).
