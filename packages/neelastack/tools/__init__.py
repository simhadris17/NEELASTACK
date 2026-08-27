from packages.neelastack.tools.registry import registry
from packages.neelastack.tools.builtins.code import describe_code_task
from packages.neelastack.tools.builtins.filesystem import read_text
from packages.neelastack.tools.builtins.http import fetch


def register_builtin_tools():
    registry.register("describe_code_task", describe_code_task)
    registry.register("read_text", read_text)
    registry.register("fetch", fetch)


register_builtin_tools()
