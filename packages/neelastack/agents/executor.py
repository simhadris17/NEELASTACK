from .base import Agent
class ExecutorAgent(Agent):
    name = "executor"
    async def run(self, goal, context):
        return f"Execution boundary prepared for: {goal}"
