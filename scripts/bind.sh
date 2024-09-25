#!/bin/bash

# CONTAINER_NAME="das-node-binder"

docker run \
    -it \
    # --name=$CONTAINER_NAME \
    --volume .:/opt/das-node \
    --entrypoint="/bin/bash" \
    python:3.10

sleep 1
docker rm $CONTAINER_NAME
