#!/bin/bash

cd src

bazel test --noenable_bzlmod --cache_test_results=no //...

cd -