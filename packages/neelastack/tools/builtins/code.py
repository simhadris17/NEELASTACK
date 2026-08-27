def describe_code_task(task: str, config: dict | None = None) -> dict:
    return {
        "task": task,
        "execution": "disabled-by-default",
        "config": config or {},
    }
