from telegram_bot.send_messages import send_bot_message
from unittest.mock import patch, MagicMock

def test_send_bot_message_success():
    with patch("telegram_bot.send_messages.requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "ok"
        mock_post.return_value = mock_response
    
        send_bot_message("dummy-token", 123, "hello")

        mock_post.assert_called_once_with(
            "https://api.telegram.org/botdummy-token/sendMessage",
            json={"chat_id": 123, "text": "hello"}
        )