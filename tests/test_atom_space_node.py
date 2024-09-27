from unittest import TestCase
from hyperon_das_node import AtomSpaceNode, LeadershipBrokerType, MessageBrokerType

class TestNode(AtomSpaceNode):

    def __init__(
        self, 
        node_id: str,
        server_id: str,
        leadership_algorithm: LeadershipBrokerType,
        messaging_backend: MessageBrokerType,
        is_server: bool):

        super().__init__(node_id, leadership_algorithm, messaging_backend)

        self.is_server = is_server;
        if is_server:
            self.server_id = ""
        else:
            self.add_peer(server_id)
            self.server_id = server_id

    def cast_leadership_vote(self) -> str:
        if self.is_server:
            return self.node_id()
        else:
            return self.server_id;

    def node_joined_network(self, node_id: str) -> None:
        self.add_peer(node_id)

class TestAtomSpaceNode(TestCase):

    def test_basics(self):

        server_id = "localhost:30700"
        client1_id = "localhost:30701"
        client2_id = "localhost:30702"

        # Run the same tests using RAM and GRPC messaging backend
        # (Senna) GRPC is unstable, I'm already trying to fix it
        # for messaging_type in [MessageBrokerType.RAM, MessageBrokerType.GRPC]:
        for messaging_type in [MessageBrokerType.RAM]:

            server = TestNode(server_id, server_id, LeadershipBrokerType.SINGLE_MASTER_SERVER, messaging_type, False)
            client1 = TestNode(client1_id, server_id, LeadershipBrokerType.SINGLE_MASTER_SERVER, messaging_type, False)
            client2 = TestNode(client2_id, server_id, LeadershipBrokerType.SINGLE_MASTER_SERVER, messaging_type, False)

            # Check state before joining network
            assert not server.is_leader()
            assert not client1.is_leader()
            assert not client2.is_leader()
            assert not server.has_leader()
            assert not client1.has_leader()
            assert not client2.has_leader()
            assert server.leader_id() == ""
            assert client1.leader_id() == ""
            assert client2.leader_id() == ""
            assert server.node_id() == server_id
            assert client1.node_id() == client1_id
            assert client2.node_id() == client2_id

            server.join_network()
            client1.join_network()
            client2.join_network()

            # Check state after joining network
            assert server.is_leader()
            assert not client1.is_leader()
            assert not client2.is_leader()
            assert server.has_leader()
            assert client1.has_leader()
            assert client2.has_leader()
            assert server.leader_id() == server_id
            assert client1.leader_id() == server_id
            assert client2.leader_id() == server_id
            assert server.node_id() == server_id
            assert client1.node_id() == client1_id
            assert client2.node_id() == client2_id

