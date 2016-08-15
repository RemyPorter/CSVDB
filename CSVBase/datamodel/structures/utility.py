from collections import defaultdict
def split(l):
    """car/cdr logic, because functional."""
    return l[0],l[1:]

def empty_path(path):
    return path is None or len(path) == 0

def format_op(target, operation):
    return "{0}_{1}".format(target, operation)

def merge_dicts_of_lists(*args):
    """
    Given a dictionary where each key is a list,
    merge them together.

    >>> d1 = {"k1": [0,1,2], "k2": [3,4,5]}
    >>> d2 = {"k1": [6,7,8], "k2": [9,10,11]}
    >>> d12 = merge_dicts_of_lists(d1,d2)
    >>> d12["k1"]
    [0, 1, 2, 6, 7, 8]
    >>> d12["k2"]
    [3, 4, 5, 9, 10, 11]
    """
    result = defaultdict(list)
    for d in args:
        for k,v in d.items():
            result[k] += v
    return result

if __name__ == '__main__':
    import doctest
    doctest.testmod()