from .structures.trie import Item

def keysize_dependent(func):
    def wrapper(self, *args):
        for a in args:
            if self._keysize and len(a) < self._keysize:
                raise BucketKeyLengthError("Input parameter insufficient length for this bucket.")
        return func(self, *args)
    return wrapper

class Bucket:
    """
    In-memory representation of a bucket.
    >>> b = Bucket("foo", 2)
    >>> b.create([1, 2])
    >>> try:
    ...   b.create([1])
    ... except:
    ...   print("Error!")
    ...
    Error!
    """
    def __init__(self, name, keysize=None):
        self.name = name
        self._data = Item(name)
        self._keysize = keysize

    @keysize_dependent
    def create(self, row):
        self._data.append(row)

    def read(self, query_row):
        return self._data.search(query_row)

    @keysize_dependent
    def update(self, query_row, new_data):
        self._data.remove(query_row)
        self._data.append(new_data)

    def delete(self, query_row):
        self._data.remove(query_row)

    def reset(self):
        self._data = Item(name)

class BucketKeyLengthError(Exception):
    pass

if __name__ == '__main__':
    import doctest
    doctest.testmod()