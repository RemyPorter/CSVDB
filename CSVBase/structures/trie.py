from collections import defaultdict
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
    """
    def __init__(self, value=None):
        self.value = value
        self.children = dict()

    def append(self, children):
        if children is None or len(children) == 0:
            return
        start = children[0]
        rest = children[1:]
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

    def search(self, path):
        if path is None or len(path) == 0:
            if len(self.children) > 0:
                rows = []
                for k,v in self.children.items():
                    sr = v.search(None)
                    for r in sr:
                        rows.append([self.value] + r)
                return rows

            return [[self.value]]
        rows = []
        start, rest = path[0],path[1:]
        if self.value == start: #we're on the path
            for k,v in self.children.items():
                sr = v.search(rest)
                if sr is None:
                    continue
                for r in sr:
                    rows.append([self.value] + r)
            return rows
        return None


    def __str__(self):
        out = StringIO()
        self.__build_str__(out)
        return out.getvalue()

if __name__ == '__main__':
    import doctest
    doctest.testmod()