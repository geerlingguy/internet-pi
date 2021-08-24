#!/bin/bash

#Backup script to retrieve, archive and export configuration files
#from Pi-Hole, Grafana, Prometheus, etc

#Find the Container ID of Pi-Hole and connect to it
#Source: https://stackoverflow.com/questions/34496882/get-docker-container-id-from-container-name
#docker ps -aqf "name=pihole" > $1 | docker exect -it $1 sh
docker container ls -aqf "pihole"

#docker ps -aqf "pihole"

#Connect to Pi-Hole container's shell prompt
#docker exec -it $1 sh

#Created and cd's into the Backup directory
mkdir /backup && cd /backup

#Backups the Pi-Hole configuration via Teleporter
pihole -a -t

#Copies/exports the backup file to Docker Host
#docker cp $1:/backup <host>/target/backup
#sudo cp $1:/backup .