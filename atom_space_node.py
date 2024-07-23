from leader_election.election import Election
from node import AtomSpaceNodeState


class AtomSpaceNode:
    """
    AtomSpaceNode
    """

    state: AtomSpaceNodeState
    """ The state of the AtomSpaceNode """

    election: Election
    """ The Leader Election algorithm """

    def __init__(self, node_id: int):
        self.state = AtomSpaceNodeState(id=node_id)
        self.election = Election(state=self.state)

    def __repr__(self) -> str:
        return self.state.__repr__()

if __name__ == "__main__":
    node = AtomSpaceNode(node_id=1)
    print(node)

    node.election.start()
    while not node.state.has_leader:
        pass

    print(node)
