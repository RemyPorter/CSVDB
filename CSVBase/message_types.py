from .datamodel.structures.utility import merge_dicts_of_lists

BUCKET_COMMANDS = {
    "create": ["row"],
    "update": ["query_row", "data"],
    "delete": ["query_row"]
}

DDL_COMMANDS = {
    "create_bucket": ["bucket"],
    "drop_bucket": ["bucket"]
}

ALL_TYPES = merge_dicts_of_lists(BUCKET_COMMANDS, DDL_COMMANDS)