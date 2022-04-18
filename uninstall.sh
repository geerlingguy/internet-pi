#Uninstall script to remove all Internet-Pi directories and files

#Moves to pi-hole first
cd ~/internet-monitoring

#Shutting down containers
docker-compose down -v

#Moving onto pi-hole
cd ~/pi-hole

#Shutting down containers
docker-compose down -v

#Moving onto Shelly Plug directories
cd ~/shelly-plug-prometheus

#Shutting down containers
docker-compose down -v

#Moving onto Starlink
cd ~/Starlink-exporter

#Shutting down containers
docker-compose down -v

#Cleaning up Docker
docker system prune -f