import logging
from time import sleep

from leadership.broker import LeadershipBroker
from messaging.broker import MessageBroker

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class AtomSpaceNode:
    """
    Distributed AtomSpace node class
    """

    id: int
    """ The id of the AtomSpaceNode """

    leadership_broker: LeadershipBroker
    """
    LeadershipBroker instance, so every other module can use it
    """

    message_broker: MessageBroker
    """
    MessagingBroker instance, so that every other module can use it
    """

    _shutdown: bool = False
    """
    Flag to shutdown the node
    """

    def __init__(self, node_id: int):
        """
        Args:
            node_id: Id of the node
        """
        self.id = node_id

    def setup(self, message_broker: MessageBroker, leadership_broker: LeadershipBroker):
        self.message_broker = message_broker
        self.leadership_broker = leadership_broker

    def shutdown(self):
        """
        Gracefully shutdown the node.
        """
        self._shutdown = True

    def loop_forever(self):
        """
        Creates a background thread and join it.
        """
        try:
            while not self._shutdown:
                sleep(0.5)
        except KeyboardInterrupt:
            pass
