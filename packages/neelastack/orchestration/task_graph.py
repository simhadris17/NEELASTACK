class TaskGraph:
    def __init__(self): self.tasks = []
    def add(self, name, fn): self.tasks.append((name, fn))
    async def run(self, context=None):
        result = context or {}
        for name, fn in self.tasks: result[name] = await fn(result)
        return result
