from abc import ABC

from leadership.algorithms import Bully, LeadershipAlgorithm
from leadership.broker import LeadershipBroker
from leadership.exceptions import InvalidLeadershipAlgorithmException


class LeadershipBrokerFactory(ABC):
    """
    Factory class to create message brokers.
    """

    @staticmethod
    def get_broker(framework: LeadershipAlgorithm) -> type[LeadershipBroker]:
        """
        Factory method to create a leadership broker
        Instance of the broker class is returned and there is no reference to this class.

        Args:
            node: The node this broker belongs to
            framework: The framework this broker uses
        Returns:
            Instance of the leadership broker.
        Raises:
            InvalidMessagingFramework: if framework is not valid.
        """
        class_name = {LeadershipAlgorithm.BULLY: Bully}
        try:
            return class_name[framework]
        except KeyError:
            raise InvalidLeadershipAlgorithmException(framework)
