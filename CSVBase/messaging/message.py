from ..commands import *
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


_actual_commands = merge_dicts_of_lists(BUCKET_COMMANDS,SYSTEM_COMMANDS)
def build_message(target, operation, *args):
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
    params = _actual_commands[operation]
    m = Message(op)
    assert(len(params) == len(args))
    for p,v in zip(params, args):
        m[p] = v
    return m

if __name__ == '__main__':
    import doctest
    doctest.testmod()