from .base import Agent
class CoderAgent(Agent):
    name = "coder"
    async def run(self, goal, context):
        return f"Implementation task prepared for: {goal}"
