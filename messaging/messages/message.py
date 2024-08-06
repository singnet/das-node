from abc import ABC, abstractmethod
from typing import Any


class BaseMessage(ABC):
    """
    Abstract class to represent a message.
    """

    @abstractmethod
    def act(self, node: "AtomSpaceNode", data: Any) -> None:
        """What should be done when receiving a message."""
        raise NotImplementedError
