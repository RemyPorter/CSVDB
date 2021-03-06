from ..message_types import *
from ..datamodel.structures.utility import *
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

    def __setitem__(self, key, value):
        self.data[key] = value

    def __str__(self):
        fmt = "{0}:{1}"
        return fmt.format(self.operation, str(self.data))


_actual_commands = ALL_TYPES
def build_message(target, operation, data):
    """
    Helper method for constructing messages based on param
    definition lists, driven by our basic syntax.

    >>> m = build_message("system", "create_bucket", "foo")
    >>> m.operation
    'system_create_bucket'
    >>> m["name"]
    'foo'
    >>> m = build_message("foo", "update", [1,2,3], [1,5,6])
    >>> m["query_row"]
    [1, 2, 3]
    >>> m["data"]
    [1, 5, 6]
    """
    op = format_op(target, operation)
    m = Message(op)
    for k,v in data.items():
        m[k] = v
    return m

if __name__ == '__main__':
    import doctest
    doctest.testmod()