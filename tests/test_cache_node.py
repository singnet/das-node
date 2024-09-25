from unittest import TestCase
from hyperon_das_node.cache_node import CacheNodeServer, CacheNodeClient


class TestCacheNode(TestCase):

    def setUp(self):
        self.server_id: str = "localhost:35700"
        self.client1_id: str = "localhost:35701"
        self.client2_id: str = "localhost:35702"

        self.server = CacheNodeServer(self.server_id)
        self.client1 = CacheNodeClient(self.client1_id, self.server_id)
        self.client2 = CacheNodeClient(self.client2_id, self.server_id)

    def test_initial_state(self):
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


    def test_join_network(self):
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
