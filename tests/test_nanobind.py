from unittest import TestCase
import hyperon_das_node


class TestHyperonDasNodeBinding(TestCase):

    def test_hyperon_das_node(self):

        self.assertTrue(hasattr(hyperon_das_node, "DistributedAlgorithmNode"))
        self.assertTrue(hasattr(hyperon_das_node, "Message"))
        self.assertTrue(hasattr(hyperon_das_node, "MessageFactory"))
        self.assertTrue(hasattr(hyperon_das_node, "MessageBrokerType"))
        self.assertTrue(hasattr(hyperon_das_node, "LeadershipBrokerType"))

    def test_distributed_algorithm_node(self):
        DistributedAlgorithmNode = hyperon_das_node.DistributedAlgorithmNode

        self.assertTrue(hasattr(DistributedAlgorithmNode, "join_network"))
        self.assertTrue(hasattr(DistributedAlgorithmNode, "is_leader"))
        self.assertTrue(hasattr(DistributedAlgorithmNode, "leader_id"))
        self.assertTrue(hasattr(DistributedAlgorithmNode, "has_leader"))
        self.assertTrue(hasattr(DistributedAlgorithmNode, "add_peer"))
        self.assertTrue(hasattr(DistributedAlgorithmNode, "node_id"))
        self.assertTrue(hasattr(DistributedAlgorithmNode, "broadcast"))
        self.assertTrue(hasattr(DistributedAlgorithmNode, "send"))
        self.assertTrue(hasattr(DistributedAlgorithmNode, "node_joined_network"))
        self.assertTrue(hasattr(DistributedAlgorithmNode, "cast_leadership_vote"))
        self.assertTrue(hasattr(DistributedAlgorithmNode, "message_factory"))

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

    def test_distributed_algorithm_node_instance(self):
        leadership_algorithm = hyperon_das_node.LeadershipBrokerType.SINGLE_MASTER_SERVER
        message_backend = hyperon_das_node.MessageBrokerType.RAM
        node = hyperon_das_node.DistributedAlgorithmNode(
            node_id="node_id",
            leadership_algorithm=leadership_algorithm,
            messaging_backend=message_backend,
        )

        self.assertTrue(isinstance(node, hyperon_das_node.DistributedAlgorithmNode))

    def test_distributed_algorithm_node_mro(self):

        self.assertTrue(hyperon_das_node.MessageFactory in hyperon_das_node.DistributedAlgorithmNode.__mro__)


