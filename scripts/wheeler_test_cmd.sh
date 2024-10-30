#!/bin/bash

# install hyperon_das_node wheel
make install

# Discover and run tests inside the tests directory
python3 -m unittest discover tests
