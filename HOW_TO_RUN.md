Build Docker images

```sh
./scripts/docker_image_build.sh
```

Build gpp with bazel
-- docker container will run on interactive mode, so we don't loose bazel's cache (Don't close it if you are going to build multiple times)
```sh
./scripts/docker_image_build.sh
./scripts/build.sh
```
Inside the container

```sh
../scripts/bazel_build.sh
```

On another terminal window, build nanobind with Cmake
-- docker will run on interactive mode, so we can build multiple times

```sh
./scripts/build.sh /scripts/bind.sh
```
Inside the container run:

```sh
cmake -S . -B build
cmake --build build
```

Still inside the binder container, run Python shell and import `hyperon_das_node` module and verify that it is showing an error like below

```python
>>> import build.hyperon_das_node
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ImportError: /opt/das-node/build/hyperon_das_node.cpython-312-x86_64-linux-gnu.so: undefined symbol: _ZTIN8dasproto13AtomSpaceNode7ServiceE
```
