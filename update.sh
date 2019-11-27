#!/usr/bin/env bash

sudo docker-compose down
sudo docker-compose rm -f
sudo docker-compose pull
sudo docker-compose up -d

sudo docker ps -a