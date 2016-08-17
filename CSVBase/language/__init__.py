from .commands import *
from .row import *
from ..message_types import *
from ..datamodel.structures.utility import format_op
from ..messaging.message import Message, build_message

def parse(command_string):
    return STATEMENT.parseString(command_string)

def compile(parsed):
    assert(parsed["operation"] in ALL_TYPES.keys())
    if parsed["operation"] in BUCKET_COMMANDS.keys():
        return compile_dml(parsed)
    elif parsed["operation"] in DDL_COMMANDS.keys():
        return compile_ddl(parsed)

def compile_dml(parsed):
    bucket = parsed["bucket"]
    op = parsed["operation"]
    m = build_message(bucket, operation, parsed)
    return m

def compile_ddl(parsed):
    op = parsed["operation"]
    m = build_message("system", op, parsed)
    return m

def execute(client, database, string):
    msg = compile(parse(string))
    database.bus.publish(client, msg)