#!/bin/bash

CONTAINER_NAME="das-node-build"

mkdir -p bin
docker run \
    --name=$CONTAINER_NAME \
    --volume .:/opt/das-node \
    --workdir /opt/das-node \
    das-node-builder \
    ./bin/hyperon_das_node $1

sleep 1
docker rm $CONTAINER_NAME
