from collections.abc import AsyncIterator

from packages.neelastack.agents.registry import AGENTS
from packages.neelastack.providers.router import get_provider


class AgentRuntime:
    async def _context(self, goal: str) -> dict[str, str]:
        plan = await AGENTS["planner"].run(goal, {})
        research = await AGENTS["researcher"].run(goal, {"plan": plan})
        implementation = await AGENTS["coder"].run(
            goal, {"plan": plan, "research": research}
        )
        execution = await AGENTS["executor"].run(
            goal,
            {"plan": plan, "research": research, "implementation": implementation},
        )
        review = await AGENTS["reviewer"].run(
            goal,
            {
                "plan": plan,
                "research": research,
                "implementation": implementation,
                "execution": execution,
            },
        )
        return {
            "plan": plan,
            "research": research,
            "implementation": implementation,
            "execution": execution,
            "review": review,
        }

    def _prompt(
        self, goal: str, context: dict[str, str], history: list[dict[str, str]] | None = None
    ) -> str:
        conversation = "\n".join(
            f"{item.get('role', 'user').upper()}: {item.get('content', '')}"
            for item in (history or [])[-8:]
        )
        return f"""You are NEELASTACK, a senior coding assistant. Act like Claude:
deliver the implementation, do not ask clarification questions, and do not mention
internal agent stages.

Previous conversation:
{conversation or "(none - this is the first request)"}

User request: {goal}

Context:
{context}

Create a complete, runnable project. Assume React + TypeScript + Vite for web app
requests unless another stack is explicitly requested. Return a short summary,
assumptions, complete project tree, and complete contents for every essential file
in fenced code blocks. Keep code concise but runnable: never use TODO, FIXME,
placeholders, pseudo-code, empty components, unexplained ellipses, or truncated
files. Include package.json, index.html, source entry point, main UI, styles, and
required utilities. For calculator requests include working operators, decimals,
clear, equals, safe parsing, and division-by-zero handling. Also include exact npm
install, run, build, and test commands plus a verification checklist. Use current
Vite conventions: src/main.tsx, ReactDOM.createRoot, and @vitejs/plugin-react.
Never tell the user to choose between options."""

    async def stream(
        self, goal: str, history: list[dict[str, str]] | None = None
    ) -> AsyncIterator[str]:
        context = await self._context(goal)
        async for chunk in get_provider().stream(
            self._prompt(goal, context, history), max_tokens=2048
        ):
            yield chunk

    async def run(self, goal: str, history: list[dict[str, str]] | None = None):
        context = await self._context(goal)
        final_response = await get_provider().generate(
            self._prompt(goal, context, history), max_tokens=2048
        )
        return {"response": final_response, **context}
