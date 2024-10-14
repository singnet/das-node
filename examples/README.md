# Simple example running on two separate docker containers

## Build Docker Images

The `Dockerfile` contains one `base` image and two targets: `client` and `server`

```sh
docker build --target server -t das-node-test-server --load -f examples/Dockerfile .
docker build --target client -t das-node-test-client --load -f examples/Dockerfile .
```

Then run the respective containers with:

```sh
docker run --net=host -it das-node-test-server
```
On another terminal:

```sh
docker run --net=host -it das-node-test-client
```
