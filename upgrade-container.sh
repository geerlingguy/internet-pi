#Script to update and upgrade pi-hole and internet-monitoring containers


#Moves into the pi-hole directory
cd ~/pi-hole

#Pulls the latest images
docker-compose pull

#Restarts the necessary containers with newer images
docker-compose up -d --no-deps

#Moves to the internet-monitoring directory
cd ..
cd ~/internet-monitoring

#Pulls the latest images
docker-compose pull

#Restarts the necessary containers with newer images
docker-compose up -d --no-deps

#Delets unused/deprecated container images
docker system prune -f