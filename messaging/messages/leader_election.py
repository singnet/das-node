from dataclasses import dataclass
from messaging.messages.base import Message, Topics


@dataclass(kw_only=True)
class ElectionStartMessage(Message):
    """
    Sent by a node that receives a job request, if there is no election in
    progress, or a leader already stabilished
    """

    topic: Topics = Topics.election_start


@dataclass(kw_only=True)
class ElectionVoteMessage(Message):
    """
    Sent by a node to all nodes with the ID when it starts an election
    """

    topic: Topics = Topics.election_vote

    @property
    def score(self) -> int:
        return self.payload["score"]


@dataclass(kw_only=True)
class LeaderAnnouncementMessage(Message):
    """
    Sent by the node with the highest ID (Leader) to all nodes
    """

    topic: Topics = Topics.leader_announcement

    @property
    def leader_id(self) -> int:
        return self.sender
