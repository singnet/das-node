from abc import ABC, abstractmethod

from node import AtomSpaceNode


class BaseMessage(ABC):
    """
    Abstract class to represent a message.
    """

    @abstractmethod
    def act(node: AtomSpaceNode, data: Any) -> None:
        """ """
        raise NotImplementedError


class StartElectionMessage(BaseMessage):
    def act(node: AtomSpaceNode, data: Any) -> None:
        node.leadership_broker.on_elect_leader(data)


class ElectionVoteMessage(BaseMessage):
    def act(node: AtomSpaceNode, data: Any) -> None:
        node.leadership_broker.on_vote_received(data)
