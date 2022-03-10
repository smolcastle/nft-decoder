#!/bin/bash
git pull origin master

# stop and remove existing container and image
docker stop decoder && docker rm decoder
docker rmi decoder-image

# build new image and run container
docker build -t "decoder-image" .
docker run -d -p 80:80 --name="decoder" decoder-image