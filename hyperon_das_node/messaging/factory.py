from abc import ABC

from messaging.broker import MessageBroker
from messaging.brokers.mqtt import MQTTBroker
from messaging.enums import MessageFramework
from messaging.exceptions import InvalidMessagingFramework


class MessageBrokerFactory(ABC):
    """
    Factory class to create message brokers.
    """

    @staticmethod
    def get_broker(framework: MessageFramework) -> type[MessageBroker]:
        """
        Factory method to create a message broker
        Instance of the broker class is returned and there is no reference to this class.

        Args:
            node: The node this broker belongs to
            framework: The framework this broker uses
        Returns:
            Instance of the message broker.
        Raises:
            InvalidMessagingFramework: if framework is not valid.
        """
        class_name = {
            MessageFramework.MQTT: MQTTBroker,
        }
        try:
            return class_name[framework]
        except KeyError:
            raise InvalidMessagingFramework(framework)
