import logging
from os import getenv

from examples.determinant.determinant_node import DeterminantNode
from leadership.factory import LeadershipAlgorithm, LeadershipBrokerFactory
from messaging.factory import MessageBrokerFactory, MessageFramework

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main():
    log.info("Creating node")

    node_id = getenv("NODE_ID")

    if not node_id:
        raise RuntimeError("NODE_ID environment variable is not set")

    node = DeterminantNode(int(node_id))

    log.info("Factoring brokers")
    # MessageBroker
    message_broker = MessageBrokerFactory.get_broker(node, MessageFramework.MQTT)
    message_broker.activate()

    # LeadershipBroker
    leadership_broker = LeadershipBrokerFactory.get_broker(node, LeadershipAlgorithm.BULLY)

    log.info("Setting Up the node")
    node.setup(message_broker, leadership_broker)

    log.info("Awaiting messages on node:%s", node.id)
    node.loop_forever()
    log.info("Exiting node")


if __name__ == "__main__":
    main()
