# Hyperon Distributed Atomspace Node

The Distributed AtomSpace Node (aka DAS Node) is a component of DAS
(<https://github.com/singnet/das>) which allows the implementation of
distributed algorithms using one or more DAS as shared knowledge base.

This component is aimed at two different use cases:

DAS' query engine uses it to implement a distributed algorithm for query
resolution. Users of DAS libraries can use it to implement distributed
algorithms by exploring primitives like leadership election and message
exchanging built in the component.

## Features

### AtomSpaceNode

AtomSpaceNode is an abstract class that represents a node in a network,
designed for distributed processing. Users must extend this class to implement
custom distributed networks.

Communication between nodes is done through Message objects. These objects act
like commands exchanged between nodes, although the actual code isn't
transmitted. Instead, a command identifier is sent, and the receiving node
reconstructs and executes the corresponding Message object. The command format
resembles a command-line interface, with commands and arguments.

Key Points for Extending AtomSpaceNode:

  - AtomSpaceNode builds Message objects because it inherits from
  MessageFactory. The base class can create basic Message objects for common
  tasks, such as handling new nodes joining the network. However, subclasses
  should override message_factory() to handle application-specific messages.

  - Message execution is threaded. If commands update shared state in
  AtomSpaceNode or its subclasses, you must protect this state using mutual
  exclusion mechanisms.

  - The constructor for AtomSpaceNode requires a MessageBroker and a
  LeadershipBroker, both of which are abstract. You must choose concrete
  implementations or create your own, depending on the communication and
  leadership election strategies you want to use. Custom leadership algorithms
  may be needed, depending on the network topology and application
  requirements.

  - AtomSpaceNode has several pure virtual methods that must be implemented by
  subclasses. These methods handle fundamental tasks, such as leadership
  elections and notifying nodes when new peers join the network.

### Message

Message is an abstract class representing messages exchanged between nodes.
Each subclass should implement the act() method, which defines the behavior
that will be executed on the receiving node.

Messages aren't serialized for transmission. Instead, an identifier is sent,
allowing the recipient to instantiate the appropriate Message subclass and
invoke its act() method.

### LeadershipBroker

LeadershipBroker defines the API for leader election in the network. Users
typically don't interact with this class directly; it's managed by the
AtomSpaceNode.

#### SingleMasterServer

This is the only current implementation of LeadershipBroker. It assumes a
topology where a single master server (the leader) communicates with multiple
clients.

### MessageBroker

MessageBroker defines the API for the communication layer between nodes. Users
of AtomSpaceNode don't interact with MessageBroker directly.

Currently there are two implementations: RAM and GRPC

#### SynchronousSharedRAM (RAM)
 
This implementation uses shared memory to exchange Message objects between
nodes running within the same process. It's suitable for scenarios where all
nodes run in a shared memory space.

#### SynchronousGRPC (GRPC)

This implementation uses gRPC for inter-node communication. It sets up gRPC
servers and clients, using queues and threads to handle incoming and outgoing
messages asynchronously.

When broadcast() or send() methods are called, the command is added to the
outgoing queue and sent asynchronously. Each node listens for incoming requests
via a gRPC server, processes them, and queues them for execution.

No rpc answer is used in these GRPC calls. So if a command expects an answer to
return, this answer is supposed to be implemented as a separate Message going
back from the target node to the node that originated the request.

## Building from source

The build process involves two steps: first building the C++ code with Bazel,
and then building and installing the Python package.

We are using a docker image with `bazel` installed. To build the image you can run:

```sh
./scripts/docker_image_build.sh
# Once the image is built we can run the container
./scripts/container_tty.sh
# This will build the cpp code and copy files of interest to bazel_assets dir
cd src
../scripts/bazel_build.sh
cd ..
```

Once the image is built and the code is built, all the libraries will be copied to a folder named `bazel_assets`.
This folder will be used to build the python package.

To install the package inside the docker container, you can run:
```sh
pip install .
# This allows to run tests in python inside the container.
```

### Exporting the python package

If you wish to install the python package in another machine (currently only ubuntu is supported), run the following command:

```sh
pip wheel .

```

The output of the wheel can be copied to the local machine and installed manually. 

## Examples

Inside the examples folder you can find a number of examples of how to use the library. The `simple_node.py` shows a very simple example of how to use the library.
