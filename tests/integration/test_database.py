def test_db_models_import():
    from packages.neelastack.database.models import User, Conversation, Message
    assert User and Conversation and Message
