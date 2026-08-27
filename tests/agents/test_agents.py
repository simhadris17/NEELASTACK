def test_agents():
    from packages.neelastack.agents.registry import AGENTS
    assert {'planner','researcher','coder','analyst','reviewer','executor'} <= set(AGENTS)
