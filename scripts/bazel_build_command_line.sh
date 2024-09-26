#!/bin/bash

echo '============================================================================================================================'; 
/opt/bazel/bazelisk build --jobs 6 --noenable_bzlmod :hyperon_das_node
