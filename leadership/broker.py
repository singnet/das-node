from abc import ABC, abstractmethod

# from leadership.exceptions import InvalidLeaderAlgorithmException
from messaging.messages.packet import Packet


class LeadershipBroker(ABC):

    _leader_id: int | None = None

    """
    The id of the leader, if None, there is no leader.
    """

    node: "AtomSpaceNode"
    """
    Node this broker belongs to.
    """

    @abstractmethod
    def elect_leader(self) -> None:
        """
        Starts the election process asynchronously.
        """
        raise NotImplementedError

    @abstractmethod
    def vote(self) -> None:
        """
        Casts a vote to the leader.
        """
        raise NotImplementedError

    @abstractmethod
    def announce_leader(self) -> None:
        """
        Announces that this node is the leader.
        """
        raise NotImplementedError

    @abstractmethod
    def on_election_start(self, packet: Packet) -> None:
        """
        Handles the message when the election starts.
        """
        raise NotImplementedError

    @abstractmethod
    def on_vote_received(self, packet: Packet) -> None:
        """
        Handles the message when a vote is received.
        """
        raise NotImplementedError

    @abstractmethod
    def on_leader_announced(self, packet: Packet) -> None:
        """
        Handels the message when leader is announced.
        """
        raise NotImplementedError

    def reset_leader(self) -> None:
        """
        Resets the leader to None.
        """
        self._leader_id = None

    @property
    def has_leader(self) -> bool:
        """
        Check if there is a leader.

        returns: True if there is a leader
        """
        return self._leader_id is not None

    @property
    def leader_id(self) -> int | None:
        """
        The id of the leader, if None, there is no leader.
        """
        return self._leader_id

    @property
    def is_leader(self) -> bool:
        """
        Check if this node is the leader.

        returns: True if this node is the leader."""
        return self._leader_id == self.node.id

    @staticmethod
    def factory(node: "AtomSpaceNode") -> "LeadershipBroker":
        """
        Builds the LeadershipBroker with an specific election algorithm

        returns: broker instance

        """
        from leadership.algorithms import Bully
        return Bully(node)

