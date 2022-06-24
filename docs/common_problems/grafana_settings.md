# Changes to the Grafana settings

### Problem
You'd like to change some settings of the Grafana frontend, like:

* General settings like enabling anonymous access

* Enable SSL encryption of the Grafana front-end

### Solution
To solve this problem:

* For general settings, just research which setting for the Grafana docker container you need and update the file `templates\grafana-config.monitoring.j2`
    * for the example of enabling anonymous access this would be `GF_AUTH_ANONYMOUS_ENABLED=true`
    <br><br>
* To enable SSL encryption of the front-end, perform the following steps:
    * create a ssl key within the main internet-pi folder (from which you run the Ansible playbook):
        ```
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 -subj /CN=localhost -keyout internet-monitoring/grafana/provisioning/grafana.key -out internet-monitoring/grafana/provisioning/grafana.crt
        chmod a+r ./internet-monitoring/grafana/provisioning/grafana.key
        ```
    * Add the following to the `config.yml` in the section '# Internet monitoring configuration.':
        ```
        monitoring_grafana_ssl_file: /etc/grafana/provisioning/grafana.crt
        monitoring_grafana_ssl_key: /etc/grafana/provisioning/grafana.key
        ```
    * Add to `templates/grafana-config.monitoring.j2`:
        ```
        GF_SERVER_PROTOCOL=https
        GF_SERVER_CERT_FILE={{ monitoring_grafana_ssl_file }}
        GF_SERVER_CERT_KEY={{ monitoring_grafana_ssl_key }} 
        ```
    * Re-run the playbook

### Related issues

* [Issue 331]((https://github.com/geerlingguy/internet-pi/issues/331)) : Run internet-pi with SSL enabled
* [Issue 344](https://github.com/geerlingguy/internet-pi/issues/344) : how do we go about changing the Grafana server settings? I can't seem to locate the grafana.ini or custom.ini to make a dashboard public?