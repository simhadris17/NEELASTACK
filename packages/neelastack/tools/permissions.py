ALLOWED_TOOLS = {
    "describe_code_task",
    "fetch",
    "read_text",
    "time",
    "filesystem_read",
    "echo",
}


def allowed(name):
    return name in ALLOWED_TOOLS
