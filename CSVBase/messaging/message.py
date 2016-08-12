class Message:
    """A simple class to hold data as a message.

    Operation is the key used by subscribers to
    be notified of the message.
    """
    def __init__(self, operation, **kwargs):
        self.operation = operation
        self.data = kwargs

    def __getitem__(self, key):
        return self.data[key]