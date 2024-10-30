#!/bin/bash

CONTAINER_NAME="das-node-wheeler"

docker run \
    --rm \
    --name=$CONTAINER_NAME \
    -e _USER=$(id -u) \
    -e GROUP=$(id -g) \
    --volume .:/opt/hyperon_das_node \
    --workdir /opt/hyperon_das_node \
    das-node-wheeler \
    ./scripts/wheeler_build_cmd.sh
