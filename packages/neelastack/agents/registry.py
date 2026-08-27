from .planner import PlannerAgent
from .researcher import ResearcherAgent
from .coder import CoderAgent
from .analyst import AnalystAgent
from .reviewer import ReviewerAgent
from .executor import ExecutorAgent
AGENTS = {a.name: a() for a in [PlannerAgent, ResearcherAgent, CoderAgent, AnalystAgent, ReviewerAgent, ExecutorAgent]}
