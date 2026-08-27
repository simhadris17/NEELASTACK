from .base import Agent
class ResearcherAgent(Agent):
    name = "researcher"
    async def run(self, goal, context):
        return f"Research task prepared for: {goal}"
