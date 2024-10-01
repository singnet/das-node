#include "gtest/gtest.h"
#include "MessageBroker.h"

using namespace atom_space_node;

TEST(MessageBroker, basics) {

    try {
        MessageBroker::factory((MessageBrokerType) -1, NULL, "");
        FAIL() << "Expected exception";
    } catch(std::runtime_error const &error) {
    } catch(...) {
        FAIL() << "Expected std::runtime_error";
    }

    shared_ptr<MessageBroker> message_broker_ram = 
        MessageBroker::factory(MessageBrokerType::RAM, shared_ptr<MessageFactory>{}, "");

    shared_ptr<MessageBroker> message_broke_grpc = 
        MessageBroker::factory(MessageBrokerType::GRPC, shared_ptr<MessageFactory>{}, "");
}
