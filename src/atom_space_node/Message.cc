#include "Message.h"
#include "AtomSpaceNode.h"

using namespace atom_space_node;

Message::Message() {
}

Message::~Message() {
}

// -------------------------------------------------------------------------------------------------
// Specialized Message subclasses

NodeJoinedNetwork::~NodeJoinedNetwork() {
}

NodeJoinedNetwork::NodeJoinedNetwork(string &node_id) {
    this->joining_node = node_id;
}

void NodeJoinedNetwork::act(shared_ptr<MessageFactory> node) {
    auto atom_space_node = dynamic_pointer_cast<AtomSpaceNode>(node);
    atom_space_node->node_joined_network(this->joining_node);
}
