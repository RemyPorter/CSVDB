def bucket_message(bucket, bus):
    """
    Bind a bucket to the message bus.
    >>> from .bus import InternalBus
    >>> from .message import Message
    >>> create = Message("dummy_create", row=[1,2,3])
    >>> update = Message("dummy_update", query_row=[1,2,3], data=[3,4,5])
    >>> bus = InternalBus()
    >>> bucket = __dummybucket()
    >>> bucket_message(bucket, bus)
    >>> bus.publish(None, create)
    [1, 2, 3]
    >>> bus.publish(None, update)
    [1, 2, 3] [3, 4, 5]
    """
    ops = [("create", "row"), ("update", "query_row", "data"), ("delete", "query_row")]
    for op in ops:
        bucketop = "{0}_{1}".format(bucket.name, op[0])
        def make_callback(op):
            def callback(message):
                opname,paramnames = op[0],op[1:]
                if len(paramnames) == 1:
                    param = message[paramnames[0]]
                    getattr(bucket, opname)(param)
                else: #it's an update
                    old,new = paramnames
                    oldval,newval = message[old], message[new]
                    getattr(bucket, opname)(oldval, newval)
            return callback
        bus.subscribe(bucketop, make_callback(op))

class __dummybucket:
    def __init__(self):
        self.name = "dummy"
    def create(self, row):
        print(row)
    def read(self, query_row):
        print(query_row)
    def update(self, query_row, new_data):
        print(query_row, new_data)
    def delete(self, query_row):
        print(query_row)

if __name__ == '__main__':
    import doctest
    doctest.testmod()