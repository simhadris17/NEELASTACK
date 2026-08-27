from .base import Agent
class ReviewerAgent(Agent):
    name = "reviewer"
    async def run(self, goal, context):
        return f"Review checklist prepared for: {goal}"
