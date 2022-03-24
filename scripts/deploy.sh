#!/bin/bash
git pull origin master

# build new image
docker build -t "decoder-image" .

# stop and remove existing container
docker stop decoder && docker rm decoder

# run container
docker run -d -p 80:80 --name="decoder" decoder-image