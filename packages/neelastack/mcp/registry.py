from packages.neelastack.tools import register_builtin_tools
from packages.neelastack.tools.registry import registry


def list_tools():
    register_builtin_tools()
    return sorted(registry.tools)
