from enum import Enum, auto


class LeadershipAlgorithm(Enum):
    """
    List of available leader election algorithms implemented in this library.
    """

    BULLY = auto()
