class WorkflowRegistry:
    def __init__(self): self.items={}
    def add(self,name,definition): self.items[name]=definition
registry=WorkflowRegistry()
