from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from node import AtomSpaceNode


class BaseMessage(ABC):
    """
    Abstract class to represent a message.
    """

    @abstractmethod
    def act(self, node: AtomSpaceNode, data: Any) -> None:
        """What should be done when receiving a message."""
        raise NotImplementedError
