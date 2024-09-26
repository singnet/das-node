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
                self._loop()
        except KeyboardInterrupt:
            pass

    def _loop(self) -> None:
        """
        Main loop of the node
        """
        self._sleep()

    def check_leader(self) -> None:
        """
        Checks if there is a leader on the network, if not, elect a new one
        """
        if not self.leadership_broker.has_leader:
            self.leadership_broker.elect_leader()
            self.wait_for_leader()

    def wait_for_leader(self):
        while not self.leadership_broker.has_leader:
            self._sleep()

    def _sleep(self, interval: int = 100) -> None:
        """
        Sleeps for interval milliseconds. This is a blocking function.
        Params:
            interval (int): Time in milliseconds to sleep, default value is 100ms
        """
        sleep(interval / 1000)
