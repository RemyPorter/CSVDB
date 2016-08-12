from collections import defaultdict
from .utility import *
from io import StringIO
class Item:
    """
    A basic trie node class, implemented using dicts and lists.
    >>> i = Item(1)
    >>> i.append([2, 3, 4])
    >>> i.append([2,4,5])
    >>> print(str(i))
    1
     2
      3
       4
      4
       5
    <BLANKLINE>
    >>> i.rows()
    [[1, 2, 3, 4], [1, 2, 4, 5]]
    >>> i.search([1, 2, 3])
    [[1, 2, 3, 4]]
    >>> i.search([1, 2])
    [[1, 2, 3, 4], [1, 2, 4, 5]]
    >>> i.remove([1, 2, 3])
    >>> i.rows()
    [[1, 2, 4, 5]]
    """
    def __init__(self, value=None):
        self.value = value
        self.children = dict()

    def append(self, children):
        if children is None or len(children) == 0:
            return
        start,rest = split(children)
        if not start in self.children:
            root = Item(start)
            self.children[root.value] = root
        self.children[start].append(rest)

    def __getitem__(self, key):
        return self.children[key]

    def __build_str__(self, out, level=0):
        tabs = "".join([' ']*level)
        text = "{0}{1}\n".format(tabs, self.value)
        out.write(str(text))
        for k,v in self.children.items():
            v.__build_str__(out, level+1)

    def rows(self):
        if len(self.children) == 0:
            return [[self.value]]
        rows = []
        for k,v in self.children.items():
            cr = v.rows()
            for r in cr:
                rows.append([self.value] + r)
        return rows

    def __search_row(self, path):
        rows = []
        for k,v in self.children.items():
            sr = v.search(path)
            if sr is None:
                continue
            for r in sr:
                rows.append([self.value] + r)
        return rows

    def search(self, path):
        if empty_path(path):
            if len(self.children) > 0:
                return self.__search_row(None)
            return [[self.value]]
        rows = []
        start, rest = split(path)
        if self.value == start: #we're on the path
            return self.__search_row(rest)
        return None

    def remove(self, path):
        if empty_path(path):
            return
        start,rest = split(path)
        if self.value == start and rest[0] in self.children:
            if len(rest) > 1:
                self.children[rest[0]].remove(rest)
            else:
                del self.children[rest[0]]

    def __str__(self):
        out = StringIO()
        self.__build_str__(out)
        return out.getvalue()

if __name__ == '__main__':
    import doctest
    doctest.testmod()