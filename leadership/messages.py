from typing import Any

from messaging.messages import BaseMessage
from node import AtomSpaceNode


class StartElectionMessage(BaseMessage):
    def act(self, node: AtomSpaceNode, data: Any) -> None:
        node.leadership_broker.on_election_start()


class ElectionVoteMessage(BaseMessage):
    def act(self, node: AtomSpaceNode, data: Any) -> None:
        node.leadership_broker.on_vote_received(data)


class LeadershipAnnouncementMessage(BaseMessage):
    def act(self, node: AtomSpaceNode, data: Any) -> None:
        node.leadership_broker.on_leader_announced(data)
