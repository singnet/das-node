class LeadershipException(Exception):
    """
    Base class for all exceptions in the leadership module.
    """

    pass


class InvalidLeadershipAlgorithmException(LeadershipException):
    """
    Raised when the leadership election algorithm is invalid.
    """

    pass
