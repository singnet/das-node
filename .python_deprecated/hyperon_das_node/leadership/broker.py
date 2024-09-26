from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from node import AtomSpaceNode


class LeadershipBroker(ABC):
    _leader_id: int | None = None

    """
    The id of the leader, if None, there is no leader.
    """

    node: AtomSpaceNode
    """
    Node this broker belongs to.
    """

    _election_in_progress: bool = False
    """
    Bool flag for election in progress
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
    def on_election_start(self) -> None:
        """
        Handles the message when the election starts.
        """
        raise NotImplementedError

    @abstractmethod
    def on_vote_received(self, data: Any) -> None:
        """
        Handles the message when a vote is received.
        """
        raise NotImplementedError

    @abstractmethod
    def on_leader_announced(self, data: Any) -> None:
        """
        Handels the message when leader is announced.
        """
        raise NotImplementedError

    def _reset_leader(self) -> None:
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
