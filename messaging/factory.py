from messaging.broker import MessageBroker
from messaging.brokers.mqtt import MQTTBroker
from node import AtomSpaceNode

def message_broker_factory(node: AtomSpaceNode) -> MessageBroker:
    return MQTTBroker(node)
