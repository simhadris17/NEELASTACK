class ToolRegistry:
    def __init__(self): self.tools = {}
    def register(self, name, fn): self.tools[name] = fn
    def get(self, name): return self.tools[name]
registry = ToolRegistry()
