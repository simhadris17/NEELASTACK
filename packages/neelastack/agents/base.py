from abc import ABC, abstractmethod
class Agent(ABC):
    name = "base"
    @abstractmethod
    async def run(self, goal: str, context: dict) -> str: ...
