from packages.neelastack.tools.builtins.code import describe_code_task


DB_TOOL_HANDLERS = {
    "describe_code_task": describe_code_task,
}


def get_db_tool_handler(tool_type: str):
    return DB_TOOL_HANDLERS.get(tool_type)
