#!/bin/bash

CONTAINER_NAME="das-node-bash"

docker run \
    --net="host" \
    --name=$CONTAINER_NAME \
    --volume /tmp:/tmp \
    --volume .:/opt/das-node \
    -it das-node-builder \
    bash

sleep 1
docker rm $CONTAINER_NAME >& /dev/null
