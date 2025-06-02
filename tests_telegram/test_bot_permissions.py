import pytest
from unittest.mock import MagicMock
from telegram_bot.bot_permissions import bot_get_admin
from telethon.tl.types import Channel
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

@pytest.fixture
def mock_group():
    group = MagicMock(spec=Channel)
    group.title = "Test Group"
    return group

@pytest.mark.parametrize("group, bot_usernames, bot_behavior, expected_promotions, expected_errors", [
    # Test case where the bot is successfully promoted to admin
    ("valid_group", ["@bot1"], {"@bot1": "ok"}, 1, 0),

    # Test case where multiple bots are successfully promoted to admin
    ("valid_group", ["@bot1", "@bot2"], {"@bot1": "ok", "@bot2": "ok"}, 2, 0),

    # Test case where the bot does not exist and does not get promoted
    ("valid_group", ["@bot1"], {"@bot1": "fail"}, 0, 1),

    # Test case where multiple bots do not exist and do not get promoted
    ("valid_group", ["@bot1", "@bot2"], {"@bot1": "fail", "@bot2": "fail"}, 0, 2),

    # Test case where there are some bots that are good and some that are not
    ("valid_group", ["@bot1", "@bot2"], {"@bot1": "fail", "@bot2": "ok"}, 1, 1),
    ("valid_group", ["@bot1", "@bot2"], {"@bot1": "ok", "@bot2": "fail"}, 1, 1),

    # Test case where no bots are provided
    ("valid_group", [], {}, 0, 0),

    # Test case where the group is None
    (None, ["@bot1"], {"@bot1": "ok"}, 0, 0),
])

def test_bot_get_admin(group, bot_usernames, bot_behavior, expected_promotions, expected_errors, mock_group):
    # Arrange
    client = MagicMock()
    success_entity = MagicMock()

    def side_effect(username):
        if bot_behavior.get(username) == "ok":
            return success_entity
        else:
            raise Exception("failed")
    
    client.get_input_entity.side_effect = side_effect

    group_object = mock_group if group == "valid_group" else None
    
    # Act
    output = capture_stdout(bot_get_admin, client, group_object, bot_usernames)

    # Assert
    assert output.count("Bot promoted to admin.") == expected_promotions
    assert output.count("Admin Promotion Error:") == expected_errors
    assert client.get_input_entity.call_count == (len(bot_usernames) if group_object else 0)
