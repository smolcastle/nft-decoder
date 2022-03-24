#!/bin/bash
git pull origin master

# add SSH keys from host machine
cat ~/.ssh/id_ed25519 >> id_ed25519

# build new image
docker build -t "decoder-image" .

# remove ssh keys
rm id_ed25519

# stop and remove existing container
docker stop decoder && docker rm decoder

# run container
docker run -d -p 80:80 --name="decoder" decoder-image