def validate_tool_name(name: str):
    if not name or len(name) > 100 or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789_-" for c in name):
        raise ValueError("Invalid tool name")
    return name
