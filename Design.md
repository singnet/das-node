# AtomSpaceNode Design

This is a design proposal of the Distributed AtomSpace (DAS) Node.

Initial design will focus on Messaging and Leader Election.

## Goals

- Ensure the AtomSpaceNode is resilient to network failures.
- Ensure the AtomSpaceNode is resilient to leader failures.
- Ensure the AtomSpaceNode is resilient to job failures.
- Ensure the AtomSpaceNode will satisfy the use case.
- Ensure Nodes run inside docker containers.
- Ensure speedup of at least 70% \* N considering the
  execution in a network with N (1 < N < 6) equally resourced NODEs against the
  execution in a single NODE.

### Use Case

For this use case we will assume that the nodes are already up and running,
the network topology is full mesh. All nodes can communicate with each other
and are all aware of each other. All nodes remain in a latent state until a
job is requested.

- USER: a person using the software we provide to execute JOBs in a network of
  NODEs.
- NODE: a server process running on a Docker container encompassing all
  components required to run a AtomSpaceNode.
- JOB: a data structure designed to contain a script in one of the script
  languages supported by AtomSpaceNode. This script contains all the code required to
  execute a given task.
- MESSAGE: a data structure to encapsulate pieces of information we want to
  transport from one NODE to another.

  1. USER submit a JOB to any of the NODEs in the network.
  2. NODE start processing the JOB. Eventually, other NODEs are contacted via
     MESSAGE exchanging to share the burden of processing the JOB.
  3. Once the JOB finishes, results are collected by the same NODE originally
     contacted by the USER and delivered to the USER.

## Architecture

### Node Structure

- The initial implementation will use Python language.
- Each node will be a Docker container.
- Nodes will have the following components:
  - **Reliable message exchanging**: Manages communication between nodes.
  - **Leader election**: Manages the process of electing a leader.
  - **Job management**: Manages the process of submitting and processing jobs.
  - **Atomic commit operations**:
  - **Mutual exclusion in the use of shared resources**
  - **Consensus**
  - **Replication**
- Each component will be a separate module, that way we can easily swap modules
  for alternatives, different communication protocols, leader election
  algorithms, etc.

### Messaging Layer

- Nodes will communicate using a messaging protocol that supports reliable
  and ordered delivery.
- The messaging system will abstract the underlying network topology.
- The messaging layer will be an external library. That way we can easily
  change it, without changing the code of the AtomSpaceNode.

#### Considered Topologies

1. **Full Mesh**:

   - **Protocol**: gRPC or HTTP/2
   - **Reason**: Full mesh requires each node to communicate directly with
     every other node. gRPC supports HTTP/2, which provides multiplexing and
     efficient binary communication, making it suitable for full mesh networks.

2. **Ring**:

   - **Protocol**: HTTP/1.1 or TCP
   - **Reason**: In a ring topology, each node communicates with its two
     neighbors. HTTP/1.1 or raw TCP connections are sufficient for this topology,
     providing simplicity and reliability.

3. **Tree**:

   - **Protocol**: gRPC or MQTT
   - **Reason**: Tree topologies benefit from protocols that support
     hierarchical communication. gRPC provides efficient communication, while
     MQTT (Message Queuing Telemetry Transport) is designed for lightweight and
     efficient communication, especially in IoT and hierarchical networks.

4. **Torus/Grid**:

   - **Protocol**: gRPC or ZeroMQ
   - **Reason**: Torus or grid topologies require efficient communication
     between nodes arranged in a grid. gRPC is suitable for its performance,
     while ZeroMQ provides high-performance asynchronous messaging, making it
     ideal for grid networks.

5. **Arbitrary/Custom Topologies**:

   - **Protocol**: gRPC or AMQP
   - **Reason**: For arbitrary topologies, gRPC offers flexibility and
     performance. AMQP (Advanced Message Queuing Protocol) provides robust
     message queuing and routing capabilities, supporting complex topologies
     effectively.

#### Choosing a Protocol

For the initial implementation, **MQTT** was chosen, since it is easy
to start using, and it is very low latency, with high performance. It is also
a good match for a number of topologies. MQTT does not guarantee the ordering
of messages, so that would be required in the message itself. Note that the
default max size of a message is 256 MB.

For this initial version, the messaging layer will have to implement methods for:
leader election, job management, and telemetry.

Messaging layer API:

1. **LeaderElection**:

   - Election Message: Sent by a node to all nodes with higher IDs when it
     starts an election.
   - OK Message: Sent by a node with a higher ID in response to an Election
     message to indicate that it is still alive and will start its own election.
   - Coordinator Message: Sent by the node with the highest ID (the new leader)
     to all other nodes to announce itself as the leader.

2. **Telemetry**:

   - Heartbeat Messages: Heartbeat messages are sent periodically by each node
     to indicate that it is alive and functioning.
   - Status Messages: Status messages provide more detailed information about
     the node's current state, including resource usage and operational status.
   - Metrics Messages: Metrics messages provide detailed performance data for
     monitoring and analysis.
   - Alert Messages: Alert messages are sent when a node detects a condition
     that requires immediate attention.
   - Log Messages: Log messages provide detailed logging information for
     debugging and auditing purposes.

3. **JobManagement**:
   - Job Submission Message: Sent by the user to any node to submit a job for
     processing.
   - Job Assignment Message: Sent by the leader node to assign job parts to
     other nodes.
   - Job Progress Message: Sent by a node to report the progress of a job
     part.
   - Job Result Message: Sent by a node to report the result of a job part.
   - Job Cancellation Message: Sent by the user or leader node to cancel a
     job.

### Leader Election

Leader election is a fundamental problem in distributed systems. It involves
designating a single node as the coordinator (leader) of some task distributed
among several nodes. The leader coordinates the work among the other nodes,
ensuring efficient and reliable task completion. Below, I’ll cover some
essential concepts, common algorithms, and implementation considerations for
leader election.

#### Common Leader Election Algorithms

1. **Bully Algorithm**:

   - **Description**: Nodes have unique IDs. The node with the highest ID
     becomes the leader. If a node suspects the leader has failed, it starts an
     election by sending an election message to all nodes with higher IDs. If
     none of the higher-ID nodes respond, it becomes the leader.
   - **Pros**: Simple to understand and implement.
   - **Cons**: High network traffic in large networks, especially during
     elections.

2. **Raft Algorithm**:

   - **Description**: Raft is a consensus algorithm designed to be
     understandable. It breaks down into leader election, log replication, and
     safety.
   - **Leader Election**: Nodes start in a follower state. If they don’t hear
     from a leader, they become candidates and request votes from other nodes.
     The candidate with the majority votes becomes the leader.
   - **Pros**: Robust and widely used, well-documented.
   - **Cons**: More complex than the bully algorithm.

3. **Paxos Algorithm**:

   - **Description**: Paxos is a family of protocols for solving consensus in a
     network of unreliable or failing nodes. Nodes propose leaders, and through
     a series of messages, agree on a single leader.
   - **Pros**: Proven correctness and used in many critical systems.
   - **Cons**: Complex to implement and understand.

4. **ZooKeeper**:
   - **Description**: Apache ZooKeeper is a distributed coordination service
     that includes leader election as one of its features. Nodes use ZooKeeper
     to create ephemeral nodes; the node that successfully creates the first
     ephemeral node becomes the leader.
   - **Pros**: High reliability, widely used in industry.
   - **Cons**: Requires running and maintaining a ZooKeeper ensemble.

#### Choosing an Algorithm

For the initial implementation, **Bully** was chosen for it's simplicity and
ease of development, as the project evolves, a new algorithm can be added.
Since we opted for a modular design, we can add new algorithms as needed.

### The Job

Perform a single query to the remote DAS Server, process all the results and
perform some extra computation on each result in order to evaluate each
result's quality.

JOB should be defined as a script in some programming language. AtomSpaceNode should
be able to support multiple programming languages here so the design must be
flexible. Initially we'll support only Python scripts doing queries to a remote
DAS Server.

This baseline test case should run with speedup of at least 70% \* N considering
the execution in a network with N (1 < N < 6) equally resourced NODEs against
the execution in a single NODE.
