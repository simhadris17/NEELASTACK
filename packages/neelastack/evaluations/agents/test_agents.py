def test_agent_registry_imports():
    from packages.neelastack.agents.registry import AGENTS
    assert 'planner' in AGENTS
