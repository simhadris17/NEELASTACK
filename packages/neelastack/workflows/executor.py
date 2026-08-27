import inspect


class WorkflowExecutionError(ValueError):
    pass


class WorkflowExecutor:
    async def run(self, steps, context=None):
        if not isinstance(steps, list):
            raise WorkflowExecutionError("Workflow steps must be a list")

        result = []

        for index, step in enumerate(steps):
            if isinstance(step, str):
                result.append({
                    "step": step,
                    "status": "completed",
                })
                continue

            if isinstance(step, dict):
                name = step.get("name")

                if not isinstance(name, str) or not name.strip():
                    raise WorkflowExecutionError(
                        f"Workflow step {index} must have a non-empty name"
                    )

                result.append({
                    "step": name.strip(),
                    "status": "completed",
                })
                continue

            raise WorkflowExecutionError(
                f"Unsupported workflow step at index {index}"
            )

        return {
            "steps": result,
            "context": context or {},
        }
