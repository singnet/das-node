#!/bin/bash

CONTAINER_NAME="das-node-bash"

if [ -n "$1" ]; then
    CMD="$1"
else
    CMD="bash"
fi

docker run \
    --net="host" \
    --name=$CONTAINER_NAME \
    --volume .:/opt/hyperon_das_node \
    --volume /tmp:/tmp \
    -it das-node-builder \
   bash -c "$CMD"

sleep 1
docker rm $CONTAINER_NAME >& /dev/null
