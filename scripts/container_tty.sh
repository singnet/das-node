#!/bin/bash

CONTAINER_NAME="das-node-bash"

if [ -n "$1" ]; then
    CMD="$1"
    INTERACTIVE="-i" 
else
    CMD="bash"
    INTERACTIVE="-it" 
fi

docker run \
    --net="host" \
    --name=$CONTAINER_NAME \
    --volume .:/opt/hyperon_das_node \
    --volume /tmp:/tmp \
    $INTERACTIVE das-node-builder \
    bash -c "$CMD"

sleep 1
docker rm $CONTAINER_NAME >& /dev/null
