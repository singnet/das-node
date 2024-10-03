#!/bin/bash

CONTAINER_NAME="das-node-bash"

docker run \
    --net="host" \
    --name=$CONTAINER_NAME \
    --volume .:/opt/hyperon_das_node \
    --volume /tmp:/tmp \
    -it das-node-builder \
    bash

sleep 1
docker rm $CONTAINER_NAME >& /dev/null
