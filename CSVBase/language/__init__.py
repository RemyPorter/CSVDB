from .commands import *
from .row import *
from ..message_types import *
from ..datamodel.structures.utility import format_op
from ..messaging.message import Message

def parse(command_string):
    return STATEMENT.parseString(command_string)

def compile(parsed):
    assert(parsed["operation"] in ALL_TYPES.keys())
    if parsed["operation"] in BUCKET_COMMANDS.keys():
        return compile_dml(parsed)
    elif parsed["operation"] in DDL_COMMANDS.keys():
        return compile_ddl(parsed)

def compile_dml(parsed):
    op = parsed["operation"]
    del parsed["operation"]
    bucket = parsed["bucket"]
    m = Message(format_op(bucket, op), **parsed)
    return m

def compile_ddl(parsed):
    op = parsed["operation"]
    del parsed["operation"]
    bucket = parsed["bucket"]
    m = Message(format_op("system", op), **parsed)
    return m

def execute(client, database, string):
    msg = compile(parse(string))
    database.bus.publish(client, msg)