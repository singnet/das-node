from typing import List
from unittest import TestCase
from hyperon_das_node import AtomSpaceNode, LeadershipBrokerType, MessageBrokerType, Message
import time

class TestMessage(Message):

    def __init__(
        self,
        command: str,
        args: List[str]):

        super().__init__()
        self.command = command
        self.args = args

    def act(self, node: AtomSpaceNode):
        node.command = self.command
        node.args = self.args

class TestNode(AtomSpaceNode):

    def __init__(
        self, 
        node_id: str,
        server_id: str,
        leadership_algorithm: LeadershipBrokerType,
        messaging_backend: MessageBrokerType,
        is_server: bool):

        super().__init__(node_id, leadership_algorithm, messaging_backend)

        self.node_joined_network_count = 0
        self.is_server = is_server;
        if is_server:
            self.server_id = ""
        else:
            self.add_peer(server_id)
            self.server_id = server_id
        self.command = ""
        self.args = []

    def cast_leadership_vote(self) -> str:
        if self.is_server:
            return self.node_id()
        else:
            return self.server_id;

    def node_joined_network(self, node_id: str) -> None:
        self.node_joined_network_count += 1
        if self.is_server:
            self.add_peer(node_id)

    def message_factory(self, command: str, args: List[str]) -> Message:
        message = super().message_factory(command, args);
        if message:
            return message
        elif command in ["c1", "c2", "c3"]:
            return TestMessage(command, args)
        else:
            return None

class TestAtomSpaceNode(TestCase):

    def test_basics(self):

        server_id = "localhost:30700"
        client1_id = "localhost:30701"
        client2_id = "localhost:30702"

        for messaging_type in [MessageBrokerType.RAM, MessageBrokerType.GRPC]:

            server = TestNode(server_id, server_id, LeadershipBrokerType.SINGLE_MASTER_SERVER, messaging_type, True)
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

            # Join network
            server.join_network()
            client1.join_network()
            client2.join_network()
            time.sleep(1)


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

class TestAtomSpaceNode(TestCase):

    def test_communication(self):

        server_id = "localhost:30700"
        client1_id = "localhost:30701"
        client2_id = "localhost:30702"

        for messaging_type in [MessageBrokerType.RAM, MessageBrokerType.GRPC]:

            server = TestNode(server_id, server_id, LeadershipBrokerType.SINGLE_MASTER_SERVER, messaging_type, True)
            client1 = TestNode(client1_id, server_id, LeadershipBrokerType.SINGLE_MASTER_SERVER, messaging_type, False)
            client2 = TestNode(client2_id, server_id, LeadershipBrokerType.SINGLE_MASTER_SERVER, messaging_type, False)

            server.join_network()
            client1.join_network()
            client2.join_network()
            time.sleep(1)

            assert server.command == ""
            assert server.args == []
            assert client1.command == ""
            assert client1.args == []
            assert client2.command == ""
            assert client2.args == []

            assert server.node_joined_network_count == 2
            assert client1.node_joined_network_count == 1
            assert client2.node_joined_network_count == 0

            args1 = ["a", "b"]
            server.broadcast("c1", args1)
            time.sleep(1)

            assert server.command == ""
            assert server.args == []
            assert client1.command == "c1"
            assert client1.args == args1
            assert client2.command == "c1"
            assert client2.args == args1

            args2 = ["a2", "b2"]
            server.send("c2", args2, client1_id);
            time.sleep(1);

            assert server.command == ""
            assert server.args == []
            assert client1.command == "c2"
            assert client1.args == args2
            assert client2.command == "c1"
            assert client2.args == args1
