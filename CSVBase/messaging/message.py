class Message:
    """A simple class to hold data as a message.

    Operation is the key used by subscribers to
    be notified of the message.

    >>> m = Message("dummy_create", row=[1, 2, 3])
    >>> m["row"]
    [1, 2, 3]
    """
    def __init__(self, operation, **kwargs):
        self.operation = operation
        self.data = kwargs

    def __getitem__(self, key):
        return self.data[key]

if __name__ == '__main__':
    import doctest
    doctest.testmod()