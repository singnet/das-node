# Atom Space Node

## How to run this

### Build the docker image
```sh
./scripts/docker_image_build.sh
#Once the image is built we can run the container interactively
./scripts/build.sh
```

### Inside the container build the cpp code
```sh
# This will build the cpp code and copy files of interest to bazel_assets dir
./scripts/bazel_build.sh
```

### Build and install the python package
```sh
pip install .
# If you want to build the wheel
pip wheel .
```

The output of the wheel can be copied to the local machine and installed manually. Only if you are running on a ubuntu machine (for now).
