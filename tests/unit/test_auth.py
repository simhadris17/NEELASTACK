def test_password():
    from packages.neelastack.auth import hash_password, verify_password
    h=hash_password('test-password'); assert verify_password('test-password',h)
