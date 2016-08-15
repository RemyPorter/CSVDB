BUCKET_COMMANDS = {
    "create": ["row"],
    "update": ["query_row", "data"],
    "delete": ["query_row"]
}

SYSTEM_COMMANDS = {
    "create_bucket": ["name"],
    "drop_bucket": ["name"]
}