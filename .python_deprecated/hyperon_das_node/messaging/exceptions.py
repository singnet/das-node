class MessagingException(Exception):
    """
    Base class for all exceptions in the messaging module.
    """


class SendMessageException(MessagingException):
    """
    Raised when the message cannot be sent.
    """


class InvalidMessagingFramework(MessagingException):
    """
    Raised when trying to create a broker with an invalid messaging framework.
    """


class InvalidMessageTypeException(MessagingException):
    """
    Raised when an invalid message type is used.
    """
