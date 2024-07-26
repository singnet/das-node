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

    def __init__(self, node_id: int):
        """
        Args:
            node_id: Id of the node
        """
        self.id = node_id

    def setup(self):
        self.message_broker = MessageBroker.factory(self)
        self.message_broker.start()

        self.leadership_broker = LeadershipBroker.factory(self)


    def loop_forever(self):
        """
        Creates a background thread and join it.
        """
        try:
            while True:
                sleep(.5)
        except KeyboardInterrupt:
            pass

