# Permission denied

### Error Messages
The error message will state something like:

> Failed to connect to the host via ssh ... Permission denied

> Missing sudo password

### Problem
The most common causes of this error message is:

* You have not specified the correct user for the host
* One of the Ansible playbook tasks requires the sudo password

### Solution
To solve this problem:

* Check that you specified the correct `ansible_user` in the `inventory.ini`, this is most likely different if you are using a Debian distro for example
* Start the playbook with the `-K` option: `ansible-playbook main.yml -K`

### Related issues

* [Issue 323](https://github.com/geerlingguy/internet-pi/issues/323) : Unkonwn errors if tried to run main.yml
* [Issue 325](https://github.com/geerlingguy/internet-pi/issues/235) : Missing sudo