from dataclasses import dataclass, field


@dataclass(kw_only=True)
class AtomSpaceNodeState:
    id: int
    """ The id of the AtomSpaceNode """
    leader_id: int = -1
    """ The current leader of the network """
    nodes_ids: set[int] = field(default_factory=lambda: {1, 2, 3, 4, 5, 6})
    """ A list of other known nodes in the network """

    @property
    def has_leader(self) -> bool:
        """Returns if the node has a leader"""
        return self.leader_id > 0

    @property
    def is_leader(self) -> bool:
        """Returns if the node is the leader"""
        return self.id == self.leader_id

    def reset_leader(self) -> None:
        self.leader_id = -1

    def set_leader(self, leader_id: int) -> None:
        """ Sets the leader of the node, if there isn't one already """
        if self.has_leader:
            # log.waring("Node %s already has a leader %s", self.id, self.leader_id)
            return

        self.leader_id = leader_id
