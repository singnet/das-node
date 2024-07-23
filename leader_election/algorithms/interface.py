from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from node import AtomSpaceNodeState


@dataclass
class AlgorithmInterface(ABC):
    state: AtomSpaceNodeState
    votes: set[int] = field(default_factory=set)

    @abstractmethod
    def start_election(self) -> None:
        raise NotImplementedError
