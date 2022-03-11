# Ports already in use

### Error Messages
The error message most likely states something like:

> Cannot start service ... Host is already in use by another container ... port is already allocated

### Problem
The most common causes of this error message is:

* You have another Docker container using the port, like another Pi-hole, Grafana, or Prmetheus container from a previous install;

* You have another service using the port, e.g. you already installed Pi-hole previously without a Docker container.

Steps to confirm the problem:
* Check if you have any other docker containers running that use the port: `docker ps`;

* Check if any other service is using the port: `sudo netstat -tulp | grep [port number]`, replacing [port number] with the port number shown in the error message.

### Solution
To solve this problem:

* Stop the other docker container, if you don't need it:
    * Find the docker container id with `docker ps`;
    * Stop the docker container with `docker stop container_id`;
    * You might even want to remove the docker container with `docker rm container_id`;
    * Re-run the Ansible playbook.

* Deactivate the other service that is using the port and re-run the Ansible playbook.

* Re-configure internet-pi to use differnt ports for the containers:
    * Change the external port a container is using in:
        * **Pi-hole**: `templates\pi-hole-docker-compose.yml.j2`. This only applies to ports 80 and 443. Don't change ports 53 and 67, because having them in use means you already have another nameserver server running.
        * **Grafana and Prometheus**: `internet-monitoring\docker-compose.yml`.
    * Change other configuration files referencing the ports:
        * **Pi-hole**: No further updates needed;
        * **Grafana**: No further updates needed;
        * **Prometheus**: Change the setting 
        `targets: ['localhost:9090']` in 
        `./templates/prometheus.yml.j2`;
    * Re-run the Ansbile playbook;
    * For **Pi-hole** and **Grafana**: Remember that you will now need to enter the updated port, when you access the frontend.

### Related issues

* [Issue 306](https://github.com/geerlingguy/internet-pi/issues/306): Install on top of existing Prometheus and grafana docker?
* [Issue 349](https://github.com/geerlingguy/internet-pi/issues/349) : internet-monitoring - grafana context deadline exceeded