# Internet Pi

[![CI](https://github.com/geerlingguy/internet-pi/workflows/CI/badge.svg?event=push)](https://github.com/geerlingguy/internet-pi/actions?query=workflow%3ACI)

**A Raspberry Pi Configuration for Internet connectivity**

I have had a couple Pis doing random Internet-related duties for years. It's finally time to formalize their configs and make all the DNS/ad-blocking/monitoring stuff encapsulated into one Ansible project.

So that's what this is.

## Features

  - **Internet Monitoring**: Installs an [`internet-monitoring` Docker config](https://github.com/geerlingguy/internet-monitoring), which exposes a Grafana dashboard with historical uptime, ping stats, and speedtest results over time.
  - **Pi-hole**: Installs the Pi-hole Docker configuration so you can use Pi-hole for network-wide ad-blocking and local DNS. Make sure to update your network router config to direct all DNS queries through your Raspberry Pi if you want to use Pi-hole effectively!
  - **Shelly Plug Monitoring**: Installs a [`shelly-plug-prometheus` exporter](https://github.com/geerlingguy/shelly-plug-prometheus) and a Grafana dashboard, which tracks and displays power usage on a Shelly Plug running on the local network. (This is disabled by default. Enable and configure using the `shelly_plug_*` vars in `config.yml`.)
  - **Starlink Monitoring**: Installs a [`starlink` prometheus exporter](https://github.com/danopstech/starlink_exporter) and a Grafana dashboard, which tracks and displays Starlink statistics. (This is disabled by default. Enable and configure using the `starlink_enable` var in `config.yml`.)

**IMPORTANT NOTE**: If you use this playbook, it will download a decently-large amount of data through your Internet connection on a daily basis. Don't use it, or tune the `internet-monitoring` setup to not run the speedtests as often, if you have a metered connection!

## Setup

  1. [Install Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html) (either full version or ansible-base).
  2. Install requirements: `ansible-galaxy install -r requirements.yml`
  3. Make copies of the following files and customize them to your liking:
    - `example.inventory.ini` to `inventory.ini` (replace IP address with your Pi's IP).
    - `example.config.yml` to `config.yml`
  4. Run the playbook: `ansible-playbook main.yml`

## License

MIT

## Author

This project was created in 2021 by [Jeff Geerling](https://www.jeffgeerling.com/).
