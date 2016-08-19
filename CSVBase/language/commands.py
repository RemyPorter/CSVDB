"""
Defines the grammar for basic commands.
>>> output = STATEMENT.runTests(test_commands, printResults=False)
>>> output[0]
True

TODO: add more of the test content to this,
but it's just terious to test.
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

CREATE, ROW, IN, UPDATE, SET, DELETE, WHERE, KEY, COLS, WITH, CREATE, BUCKET, DROP, AND, FROM = (
    map(CaselessKeyword, """
    CREATE ROW IN UPDATE SET DELETE WHERE KEY COLS WITH CREATE BUCKET DROP AND FROM
    """.split())
    )

CREATE_ROW = Suppress(CREATE + ROW + IN).setParseAction(set_op("create")) + \
    bucket_name("bucket") + \
    row("row")
UPDATE_ROW = Suppress(UPDATE).setParseAction(set_op("update")) + \
    bucket_name("bucket") + \
    Suppress(SET + ROW) + row("data") + \
    Suppress(WHERE) + row("query_row")
DELETE_ROW = Suppress(DELETE + FROM).setParseAction(set_op("delete")) + \
    bucket_name("bucket") + \
    Suppress(WHERE) + row("query_row")

KEY_EXPR = Suppress(KEY + COLS) + \
    Word(nums)("keysize").setParseAction(_to_int)
BUCKET_OPTS = (KEY_EXPR)
BUCKET_WITH_CLAUSE = Suppress(WITH) + BUCKET_OPTS + \
    ZeroOrMore(Suppress(AND) + BUCKET_OPTS)

CREATE_BUCKET = Suppress(CREATE + BUCKET).setParseAction(set_op("create_bucket")) + \
    bucket_name("bucket") + \
    Optional(BUCKET_WITH_CLAUSE)
DROP_BUCKET = Suppress(DROP + BUCKET).setParseAction(set_op("drop_bucket")) + \
    bucket_name("bucket")

DDL = (CREATE_BUCKET | DROP_BUCKET)
DML = (CREATE_ROW | UPDATE_ROW | DELETE_ROW)
STATEMENT = (DML | DDL)

if __name__ == '__main__':
    test_commands = """
    CREATE ROW IN foo 1, "2", 3, "this should work, right?"
    UPDATE foo SET ROW 1, 2, 4 WHERE 1, 2
    DELETE FROM foo WHERE 1, 2, 4
    CREATE BUCKET foo
    CREATE BUCKET foo WITH KEY COLS 3
    DROP BUCKET foo
    """
    import doctest
    doctest.testmod()