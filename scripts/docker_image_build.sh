#!/bin/bash

docker buildx build -t das-node-builder --load -f docker/Dockerfile .
