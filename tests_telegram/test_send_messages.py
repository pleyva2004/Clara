from unittest.mock import patch
from telegram_bot.send_messages import send_bot_message
import requests
import pytest
import io
import sys

# Helper to capture print output
def capture_stdout(func, *args, **kwargs):
    buffer = io.StringIO()
    sys.stdout = buffer
    try:
        func(*args, **kwargs)
    finally:
        sys.stdout = sys.__stdout__
    return buffer.getvalue()

@pytest.mark.parametrize("message, status_code, response_text, should_raise, expected_output, should_call", [
    # Successfully sent message
    ("Test Message", 200, "ok", False, "Message sent successfully!", True),

    # Failed to send message with various error codes
    ("Test Message", 400, "Bad Request", False, "Failed to send message: Bad Request", True),
    ("Test Message", 500, "Internal Server Error", False, "Failed to send message: Internal Server Error", True),

    # Empty or whitespace-only message
    ("", None, None, False, "Message is empty", False),
    ("   ", None, None, False, "Message is empty", False),

    # Network error
    ("Test Message", None, None, True, "Request failed: Network down", True),

])

@patch("telegram_bot.send_messages.requests.post")
def test_send_bot_message(mock_post, message, status_code, response_text, should_raise, expected_output, should_call):
    # Arrange
    if should_raise:
        mock_post.side_effect = requests.RequestException("Network down")
    elif status_code is not None:
        mock_post.return_value.status_code = status_code
        mock_post.return_value.text = response_text

    # Act
    output = capture_stdout(send_bot_message, "dummy-token", 123, message)

    # Assert
    assert expected_output in output

    if should_call:
        mock_post.assert_called_once_with(
            "https://api.telegram.org/botdummy-token/sendMessage", 
            json={"chat_id": 123, "text": message}
        )
    else:
        mock_post.assert_not_called()

