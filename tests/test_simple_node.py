from unittest import TestCase
from examples import simple_node


class TestSimpleNode(TestCase):

    def test_cache_node(self):
        self.server_id: str = "localhost:35700"
        self.client1_id: str = "localhost:35701"
        self.client2_id: str = "localhost:35702"

        self.server = cache_node.SimpleNodeServer(self.server_id)
        self.client1 = cache_node.SimpleNodeClient(self.client1_id, self.server_id)
        self.client2 = cache_node.SimpleNodeClient(self.client2_id, self.server_id)

        # There should be no leader
        self.assertFalse(self.server.has_leader())
        self.assertFalse(self.client1.has_leader())
        self.assertFalse(self.client2.has_leader())

        self.assertFalse(self.server.is_leader())
        self.assertFalse(self.client1.is_leader())
        self.assertFalse(self.client2.is_leader())

        self.assertEqual(self.server.leader_id(), "")
        self.assertEqual(self.client1.leader_id(), "")
        self.assertEqual(self.client2.leader_id(), "")

        # Test id assignment
        self.assertEqual(self.server.node_id(), self.server_id)
        self.assertEqual(self.client1.node_id(), self.client1_id)
        self.assertEqual(self.client2.node_id(), self.client2_id)

        # Create network

        self.server.join_network()
        self.client1.join_network()
        self.client2.join_network()

        # Server should be leader

        self.assertTrue(self.server.has_leader())
        self.assertTrue(self.client1.has_leader())
        self.assertTrue(self.client2.has_leader())

        self.assertTrue(self.server.is_leader())
        self.assertFalse(self.client1.is_leader())
        self.assertFalse(self.client2.is_leader())

        self.assertEqual(self.server.leader_id(), self.server_id)
        self.assertEqual(self.client1.leader_id(), self.server_id)
        self.assertEqual(self.client2.leader_id(), self.server_id)


        # Test id assignment
        self.assertEqual(self.server.node_id(), self.server_id)
        self.assertEqual(self.client1.node_id(), self.client1_id)
        self.assertEqual(self.client2.node_id(), self.client2_id)
