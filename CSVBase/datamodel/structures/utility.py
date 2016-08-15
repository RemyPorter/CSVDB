def split(l):
    """car/cdr logic, because functional."""
    return l[0],l[1:]

def empty_path(path):
    return path is None or len(path) == 0

def format_op(target, operation):
    return "{0}_{1}".format(target, operation)