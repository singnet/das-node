class LeadershipException(Exception):
    """
    Base class for all exceptions in the leadership module.
    """
    pass

class InvalidLeaderAlgorithmException(LeadershipException):
    """
    Raised when the leadership election algorithm is invalid.
    """
    pass
