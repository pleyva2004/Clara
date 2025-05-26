from telegram_bot.create_connection import connect_telegram

def test_connection():
    client = connect_telegram("session_name", 24829326, "4bc9bc068c98b8ed0ad8841e410a64a1")
    assert client is not None


def test_connection_failure():
    client = connect_telegram("session_name", "invalid_app_id", "invalid_api_hash")
    assert client is None