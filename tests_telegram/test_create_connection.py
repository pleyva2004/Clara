from telegram_bot.create_connection import connect_telegram
from unittest.mock import patch, MagicMock
import pytest

@pytest.mark.parametrize("start_raises, constructor_raises, expected", [
    # Test case where the connection is successful
    (False, False, "instance"),

    # Test case where the start method raises an exception
    (True, False, None),

    # Test case where the constructor raises an exception
    (False, True, None),

    # Test case where both the start method and constructor raise exceptions
    (True, True, None),
])

def test_connect_telegram(start_raises, constructor_raises, expected):
    if constructor_raises:
        # Arrange
        with patch("telegram_bot.create_connection.TelegramClient", side_effect=Exception("Constructor Failed")) as mock_client:
            
            # Act
            client = connect_telegram("session", 123, "hash")
            mock_client.assert_called_once_with("session", 123, "hash")

            # Assert
            assert client is None
    else:
        with patch("telegram_bot.create_connection.TelegramClient") as mock_client:
            # Arrange
            mock_instance = MagicMock()
            if start_raises:
                mock_instance.start.side_effect = Exception("Connection Failed")
            mock_client.return_value = mock_instance

            # Act
            client = connect_telegram("session", 123, "hash")

            mock_client.assert_called_once_with("session", 123, "hash")
            mock_instance.start.assert_called_once()

            # Assert
            if expected == "instance":
                assert client == mock_instance
            else:
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