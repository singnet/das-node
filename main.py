import logging
from os import getenv


from time import sleep
from node import AtomSpaceNode
from messaging.messages.packet import Packet, MessageType

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main():
    log.info("Creating nodes")

    node_id = getenv("NODE_ID")

    if not node_id:
        raise RuntimeError("NODE_ID environment variable is not set")

    node = AtomSpaceNode(int(node_id))

    log.info("Setting Up the nodes")
    node.setup()

    node.loop_forever()
    log.info("Exiting node")



if __name__ == "__main__":
    main()
