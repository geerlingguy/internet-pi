# Internet Pi

**A Raspberry Pi Configuration for Internet connectivity**

TODO: Description here.

## Features

  - **Internet Monitoring**: TODO.
  - **Pi-hole**: TODO.

## Setup

  1. Install Ansible (either full version or ansible-base).
  2. Install requirements: `ansible-galaxy collection install -r requirements.yml`
  3. Make copies of the following files and customize them to your liking:
    - `example.inventory.ini` to `inventory.ini` (replace IP address with your Pi's IP).
    - `example.config.yml` to `config.yml`
  4. Run the playbook: `ansible-playbook main.yml`

## License

MIT

## Author

TODO.
