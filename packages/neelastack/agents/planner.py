from .base import Agent
class PlannerAgent(Agent):
    name = "planner"
    async def run(self, goal, context):
        return f"Plan: clarify goal -> gather context -> execute -> review. Goal: {goal}"
