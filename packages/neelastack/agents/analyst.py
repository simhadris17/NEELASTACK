from .base import Agent
class AnalystAgent(Agent):
    name = "analyst"
    async def run(self, goal, context):
        return f"Analysis task prepared for: {goal}"
