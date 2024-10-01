#include "Message.h"
#include "AtomSpaceNode.h"

using namespace atom_space_node;

Message::Message() {
}

Message::~Message() {
}

NodeWrapper::NodeWrapper(AtomSpaceNode *node) {
    this->node = node;
}

// -------------------------------------------------------------------------------------------------
// Specialized Message subclasses

NodeJoinedNetwork::~NodeJoinedNetwork() {
}

NodeJoinedNetwork::NodeJoinedNetwork(string &node_id) {
    this->joining_node = node_id;
}

void NodeJoinedNetwork::act(shared_ptr<NodeWrapper> node_wrapper) {
    node_wrapper->node->node_joined_network(this->joining_node);
}
