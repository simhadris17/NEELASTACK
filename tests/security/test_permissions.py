def test_tool_permission():
    from packages.neelastack.tools.permissions import allowed
    assert allowed('echo') and not allowed('shell')
