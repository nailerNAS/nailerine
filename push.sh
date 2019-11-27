#!/usr/bin/env bash

function bp()
{
    docker build -t nailer/nailerine:latest .
    docker push nailer/nailerine:latest
    docker system prune -f
}

sudo bash -c "$(declare -f bp); bp"