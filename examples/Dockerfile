# Base image for docker example
FROM python:3.10 AS base

RUN pip install --no-cache-dir hyperon_das_node

WORKDIR /opt/hyperon_das_node

COPY examples .


# Server image for docker example, exposes server port
FROM base AS server

EXPOSE 35700

ENTRYPOINT ["python", "-i", "docker_server.py"]


# Client image for docker example, exposes client port
FROM base AS client

EXPOSE 35701

ENTRYPOINT ["python", "-i", "docker_client.py"]
