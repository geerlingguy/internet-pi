# Containers time out due to missing nameserver setting

### Error Messages
> Docker container time out and have no network connection.

### Problem
The most common causes of this error message is:

* Nameserver setting is missing

### Solution
To solve this problem:

In `/etc/dhcpcd.conf` and add the following:
```
interface eth0
static domain_name_servers=127.0.0.1
```
Note, you'll need to replace the interface above with the interface you're using for your internet connection.

### Related issues

* [Issue 349 : internet-monitoring - grafana context deadline exceeded](https://github.com/geerlingguy/internet-pi/issues/349)