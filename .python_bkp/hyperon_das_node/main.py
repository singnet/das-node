import logging
from os import getenv

from leadership.factory import LeadershipAlgorithm, LeadershipBrokerFactory
from messaging.factory import MessageBrokerFactory, MessageFramework
from node import AtomSpaceNode

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main():
    log.info("Creating nodes")

    node_id = getenv("NODE_ID")

    if not node_id:
        raise RuntimeError("NODE_ID environment variable is not set")

    node = AtomSpaceNode(int(node_id))

    log.info("Factoring brokers")
    # MessageBroker
    message_broker = MessageBrokerFactory.get_broker(MessageFramework.MQTT)(node)
    message_broker.activate()

    # LeadershipBroker
    leadership_broker = LeadershipBrokerFactory.get_broker(LeadershipAlgorithm.BULLY)(node)

    log.info("Setting Up the nodes")
    node.setup(message_broker, leadership_broker)

    node.loop_forever()
    log.info("Exiting node")


if __name__ == "__main__":
    main()
