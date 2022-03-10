#!/bin/bash
git pull origin master

docker rmi decoder-image
docker build -t "decoder-image" .

docker stop decoder && docker rm decoder
docker run -d -p 80:80 --name="decoder" decoder-image