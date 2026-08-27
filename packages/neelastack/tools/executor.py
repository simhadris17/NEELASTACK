import inspect

from .permissions import allowed


async def execute(name, fn, *args, **kwargs):
    if not allowed(name):
        raise PermissionError(f"Tool denied: {name}")

    result = fn(*args, **kwargs)

    if inspect.isawaitable(result):
        return await result

    return result
