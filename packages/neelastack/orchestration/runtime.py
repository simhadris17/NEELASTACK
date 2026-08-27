from packages.neelastack.agents.registry import AGENTS
class AgentRuntime:
    async def run(self, goal: str):
        plan = await AGENTS["planner"].run(goal, {})
        research = await AGENTS["researcher"].run(goal, {"plan": plan})
        review = await AGENTS["reviewer"].run(goal, {"plan": plan, "research": research})
        return {"plan": plan, "research": research, "review": review}
