from unittest import TestCase
import hyperon_das_node


class TestHyperonDasNodeBinding(TestCase):

    def test_hyperon_das_node(self):

        self.assertTrue(hasattr(hyperon_das_node, "AtomSpaceNode"))
        self.assertTrue(hasattr(hyperon_das_node, "Message"))
        self.assertTrue(hasattr(hyperon_das_node, "MessageFactory"))
        self.assertTrue(hasattr(hyperon_das_node, "MessageBrokerType"))
        self.assertTrue(hasattr(hyperon_das_node, "LeadershipBrokerType"))

    def test_atom_space_node(self):
        AtomSpaceNode = hyperon_das_node.AtomSpaceNode

        self.assertTrue(hasattr(AtomSpaceNode, "join_network"))
        self.assertTrue(hasattr(AtomSpaceNode, "is_leader"))
        self.assertTrue(hasattr(AtomSpaceNode, "leader_id"))
        self.assertTrue(hasattr(AtomSpaceNode, "has_leader"))
        self.assertTrue(hasattr(AtomSpaceNode, "add_peer"))
        self.assertTrue(hasattr(AtomSpaceNode, "node_id"))
        self.assertTrue(hasattr(AtomSpaceNode, "broadcast"))
        self.assertTrue(hasattr(AtomSpaceNode, "send"))
        self.assertTrue(hasattr(AtomSpaceNode, "node_joined_network"))
        self.assertTrue(hasattr(AtomSpaceNode, "cast_leadership_vote"))
        self.assertTrue(hasattr(AtomSpaceNode, "message_factory"))

    def test_message(self):
        Message = hyperon_das_node.Message

        self.assertTrue(hasattr(Message, "act"))

    def test_message_factory(self):
        MessageFactory = hyperon_das_node.MessageFactory

        self.assertTrue(hasattr(MessageFactory, "message_factory"))

    def test_message_broker_type(self):
        MessageBrokerType = hyperon_das_node.MessageBrokerType

        self.assertTrue(hasattr(MessageBrokerType, "GRPC"))
        self.assertTrue(hasattr(MessageBrokerType, "RAM"))

    def test_leadership_broker_type(self):
        LeadershipBrokerType = hyperon_das_node.LeadershipBrokerType

        self.assertTrue(hasattr(LeadershipBrokerType, "SINGLE_MASTER_SERVER"))

    def test_atom_space_node_instance(self):
        leadership_algorithm = hyperon_das_node.LeadershipBrokerType.SINGLE_MASTER_SERVER
        message_backend = hyperon_das_node.MessageBrokerType.RAM
        node = hyperon_das_node.AtomSpaceNode(
            node_id="node_id",
            leadership_algorithm=leadership_algorithm,
            messaging_backend=message_backend,
        )

        self.assertTrue(isinstance(node, hyperon_das_node.AtomSpaceNode))

    def test_atom_space_node_mro(self):

        self.assertTrue(hyperon_das_node.MessageFactory in hyperon_das_node.AtomSpaceNode.__mro__)


