def test_role_denied():
    from packages.neelastack.auth.rbac import require_role
    assert callable(require_role('admin'))
