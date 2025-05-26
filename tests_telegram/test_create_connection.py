from telegram_bot.create_connection import connect_telegram
from unittest.mock import patch, MagicMock
import pytest

@pytest.fixture
def patched_telegram_client():
    with patch("telegram_bot.create_connection.TelegramClient") as mock_client:
        mock_instance = MagicMock()
        mock_client.return_value = mock_instance
        yield mock_client, mock_instance


def test_connection_success(patched_telegram_client):
    # Arrange
    mock_client, mock_instance = patched_telegram_client

    # Act
    client = connect_telegram("session_name", 123, "hash")
    
    # Assert
    mock_client.assert_called_once_with("session_name", 123, "hash")
    mock_instance.start.assert_called_once()
    assert client == mock_instance

def test_connection_failure(patched_telegram_client):
    # Arrange
    mock_client, mock_instance = patched_telegram_client
    mock_instance.start.side_effect = Exception("Connection Failed")

    # Act
    client = connect_telegram("session_name", 123, "hash")

    # Assert
    mock_client.assert_called_once_with("session_name", 123, "hash")
    mock_instance.start.assert_called_once()
    assert client is None

def test_TelegramClient_failure():
    # Arrange
    with patch("telegram_bot.create_connection.TelegramClient", side_effect=Exception("Constructor Failed")) as mock_client:
        # Act
        client = connect_telegram("session_name", 123, "hash")

        # Assert
        mock_client.assert_called_once_with("session_name", 123, "hash")
        assert client is None

def test_multiple_sessions():
    # Arrange
    with patch("telegram_bot.create_connection.TelegramClient") as mock_client:
        mock_instance1 = MagicMock()
        mock_instance2 = MagicMock()
        mock_client.side_effect = [mock_instance1, mock_instance2]

        # Act
        client1 = connect_telegram("session1", 123, "hash1")
        client2 = connect_telegram("session2", 123, "hash2")


        # Assert
        assert mock_client.call_count == 2
        assert client1 == mock_instance1
        assert client2 == mock_instance2
        assert mock_instance1.start.called
        assert mock_instance2.start.called