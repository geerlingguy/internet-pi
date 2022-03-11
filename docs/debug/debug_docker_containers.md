# Debug Docker Containers

A few usefull docker commands to analyse any of your docker container related problems:

`docker ps` : show all running containers, their container_ids and the ports being used

`docker ps -a` : Show all containers (default shows just running)

`docker logs container_id` : Show the logs of the container specified by the container_id

`docker exec -it container_id sh` : Enter the shell of the docker container

`docker stop container_id` : stop a container

`docker rm container_id` : remove a stopped container