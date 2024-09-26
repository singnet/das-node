class LeadershipException(Exception):
    """
    Base class for all exceptions in the leadership module.
    """


class InvalidLeadershipAlgorithmException(LeadershipException):
    """
    Raised when the leadership election algorithm is invalid.
    """
