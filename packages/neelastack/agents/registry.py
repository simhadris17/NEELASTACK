from .analyst import AnalystAgent
from .coder import CoderAgent
from .executor import ExecutorAgent
from .planner import PlannerAgent
from .researcher import ResearcherAgent
from .reviewer import ReviewerAgent

_AGENT_TYPES = (
    PlannerAgent,
    ResearcherAgent,
    CoderAgent,
    AnalystAgent,
    ReviewerAgent,
    ExecutorAgent,
)

AGENTS = {agent_type.name: agent_type() for agent_type in _AGENT_TYPES}
