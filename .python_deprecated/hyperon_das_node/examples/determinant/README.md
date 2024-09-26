# How to run this example?

## On the parent directory (das-node)
Build and start the nodes using docker-compose. The -f flag is needed to
specify a custom docker-compose file.

```sh
docker-compose -f examples/determinant/docker-compose.yml build
docker-compose -f examples/determinant/docker-compose.yml up
```

After the nodes are running, run the example:

```sh
docker-compose -f examples/determinant/docker-compose.yml run job_start
```

