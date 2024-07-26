from enum import Enum, auto

class MessageFramework(Enum):
    """
    Enum of all available message frameworks.
    """
    MQTT = auto()

class MessageType(Enum):
    """
    Enum of all available message types.
    """
    ANY = auto()

    # Leadership Election types
    LEADERSHIP_ELECTION_START = auto()
    LEADERSHIP_ELECTION_VOTE = auto()
    LEADERSHIP_ANNOUNCEMENT = auto()

    # Node discovery types

    # Job Manager types

