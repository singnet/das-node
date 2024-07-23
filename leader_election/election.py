from dataclasses import dataclass, field

from algorithms import AlgorithmInterface, Bully
from node import AtomSpaceNodeState


@dataclass(kw_only=True)
class Election:
    state: AtomSpaceNodeState
    algorithm: AlgorithmInterface = field(init=False)

    def __post_init__(self, **kwargs):
        self.algorithm = Bully(state=self.state)

    def set_algorithm(self, algorithm: AlgorithmInterface) -> None:
        self.algorithm = algorithm

    def start(self) -> None:
        """ "Starts the election Process"""
        self.algorithm.start_election()
