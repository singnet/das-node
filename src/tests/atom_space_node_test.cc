#include <cstdlib>
#include <cmath>

#include "gtest/gtest.h"
#include "Utils.h"
#include "AtomSpaceNode.h"

using namespace atom_space_node;

class TestNode : public AtomSpaceNode {
public:
    string server_id;
    bool is_server;
    TestNode(
        const string &node_id,
        const string &server_id,
        LeadershipBrokerType leadership_algorithm,
        MessageBrokerType messaging_backend,
        bool is_server) : AtomSpaceNode(
            node_id, 
            leadership_algorithm,
            messaging_backend) {

        this->is_server = is_server;
        if (! is_server) {
            this->add_peer(node_id);
            this->server_id = server_id;
        }
    }

    string cast_leadership_vote() {
        if (this->is_server) {
            return this->node_id();
        } else {
            return this->server_id;
        }
    }
    void node_joined_network(const string &node_id) {
        this->add_peer(node_id);
    }
};

TEST(AtomSpaceNode, basics) {
    string server_id = "localhost:30700";
    string client1_id = "localhost:30701";
    string client2_id = "localhost:30702";
    for (auto messaging_type: {MessageBrokerType::RAM , MessageBrokerType::GRPC}) {

        TestNode server(
            server_id, 
            server_id, 
            LeadershipBrokerType::SINGLE_MASTER_SERVER, 
            messaging_type,
            true);
        TestNode client1(
            client1_id, 
            server_id, 
            LeadershipBrokerType::SINGLE_MASTER_SERVER, 
            messaging_type,
            false);
        TestNode client2(
            client2_id, 
            server_id, 
            LeadershipBrokerType::SINGLE_MASTER_SERVER, 
            messaging_type,
            false);

        EXPECT_FALSE(server.is_leader());
        EXPECT_FALSE(client1.is_leader());
        EXPECT_FALSE(client2.is_leader());
        EXPECT_FALSE(server.has_leader());
        EXPECT_FALSE(client1.has_leader());
        EXPECT_FALSE(client2.has_leader());
        EXPECT_TRUE(server.leader_id() == "");
        EXPECT_TRUE(client1.leader_id() == "");
        EXPECT_TRUE(client2.leader_id() == "");
        EXPECT_TRUE(server.node_id() == server_id);
        EXPECT_TRUE(client1.node_id() == client1_id);
        EXPECT_TRUE(client2.node_id() == client2_id);

        server.join_network();
        client1.join_network();
        client2.join_network();

        EXPECT_TRUE(server.is_leader());
        EXPECT_FALSE(client1.is_leader());
        EXPECT_FALSE(client2.is_leader());
        EXPECT_TRUE(server.has_leader());
        EXPECT_TRUE(client1.has_leader());
        EXPECT_TRUE(client2.has_leader());
        EXPECT_TRUE(server.leader_id() == server_id);
        EXPECT_TRUE(client1.leader_id() == server_id);
        EXPECT_TRUE(client2.leader_id() == server_id);
        EXPECT_TRUE(server.node_id() == server_id);
        EXPECT_TRUE(client1.node_id() == client1_id);
        EXPECT_TRUE(client2.node_id() == client2_id);
    }
}
