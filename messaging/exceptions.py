class MessagingException(Exception):
    """
    Base class for all exceptions in the messaging module.
    """
    pass

class SendMessageException(MessagingException):
    """
    Raised when the message cannot be sent.
    """
    pass

class InvalidMessagingFramework(MessagingException):
    """
    Raised when trying to create a broker with an invalid messaging framework.
    """
    pass

class InvalidMessageTypeException(MessagingException):
    """
    Raised when an invalid message type is used.
    """
    pass



