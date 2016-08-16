"""
Defines the grammar for basic commands.
>>> cr = test_create
>>> parsed = STATEMENT.parseString(cr)
>>> parsed["bucket"]
'foo'
>>> parsed["row"]
(['1', '2', '3', 'this should work, right?'], {})
>>> parsed = STATEMENT.parseString(test_update)
>>> parsed["query_row"]
(['1', '2'], {})
>>> parsed = STATEMENT.parseString(test_delete)
>>> parsed["query_row"]
(['1', '2', '4'], {})
>>> parsed = STATEMENT.parseString(test_buck_create)
>>> parsed["bucket"]
'foo'
>>> parsed = STATEMENT.parseString(test_buck_opt_create)
>>> parsed["bucket"]
'foo'
>>> parsed["keysize"]
3
>>> parsed = STATEMENT.parseString(test_drop)
>>> parsed["bucket"]
'foo'
"""

from pyparsing import *
from .row import row


bucket_name = Word(alphanums + "_")
_to_int = lambda x: int(x[0])

def set_op(op_name):
    def fn(toks):
        toks["operation"] = op_name
        return toks
    return fn

CREATE_ROW = Suppress("CREATE ROW IN").setParseAction(set_op("create")) + \
    bucket_name("bucket") + \
    row("row")
UPDATE_ROW = Suppress("UPDATE").setParseAction(set_op("update")) + \
    bucket_name("bucket") + \
    Suppress("SET ROW") + row("data") + \
    Suppress("WHERE") + row("query_row")
DELETE_ROW = Suppress("DELETE FROM").setParseAction(set_op("delete")) + \
    bucket_name("bucket") + \
    Suppress("WHERE") + row("query_row")

KEY_EXPR = Suppress("KEY COLS") + \
    Word(nums)("keysize").setParseAction(_to_int)
BUCKET_OPTS = (KEY_EXPR)
BUCKET_WITH_CLAUSE = Suppress("WITH") + BUCKET_OPTS + \
    ZeroOrMore(Suppress("AND") + BUCKET_OPTS)

CREATE_BUCKET = Suppress("CREATE BUCKET").setParseAction(set_op("create_bucket")) + \
    bucket_name("bucket") + \
    Optional(BUCKET_WITH_CLAUSE)
DROP_BUCKET = Suppress("DROP BUCKET") + bucket_name("bucket")

DDL = (CREATE_BUCKET | DROP_BUCKET)
DML = (CREATE_ROW | UPDATE_ROW | DELETE_ROW)
STATEMENT = (DML | DDL)

if __name__ == '__main__':
    test_create = """CREATE ROW IN foo
        1, "2", 3, "this should work, right?"!
    """
    test_update = """UPDATE foo
        SET ROW 1, 2, 4!
        WHERE 1, 2!"""
    test_delete = """DELETE FROM foo
        WHERE 1, 2, 4!"""
    test_buck_create = """CREATE BUCKET foo"""
    test_buck_opt_create = """CREATE BUCKET foo
        WITH KEY COLS 3"""
    test_drop = """DROP BUCKET foo"""
    import doctest
    doctest.testmod()