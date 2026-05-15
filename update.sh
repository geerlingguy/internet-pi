#!/bin/bash

# Pi-hole update example
cd ~/pi-hole
docker compose pull  # pulls the latest images inside the compose file
docker compose up -d --no-deps  # restarts necessary containers with newer images
docker system prune --all  # deletes unused container images

cd ../internet-monitoring/
docker compose pull             # pulls the latest images
docker compose up -d --no-deps  # restarts necessary containers with newer images
docker system prune --all  # deletes unused container images
