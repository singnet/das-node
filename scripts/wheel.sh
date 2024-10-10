#!/bin/bash

CONTAINER_NAME="das-node-wheel"

docker run \
    --name=$CONTAINER_NAME \
    --volume .:/opt/hyperon_das_node \
    --workdir /opt/hyperon_das_node \
    das-node-wheeler

sleep 1
docker rm $CONTAINER_NAME
