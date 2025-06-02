from telegram_bot.add_users import add_users_to_group
from unittest.mock import MagicMock
from telethon.errors import UserPrivacyRestrictedError, UserNotMutualContactError
import pytest

import io
import sys

# Helper function to capture the standard output
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
    group = MagicMock()
    group.title = "Test Group"
    return group

@pytest.mark.parametrize("usernames, user_behavior, expected_output", [
    # Test with no usernames
    ([], {}, ["No usernames provided to add."]),

    # Test with a valid user
    (["@user1"], {"@user1": "ok"}, ["Added @user1 to group"]),

    # Test with multiple valid users
    (["@user1", "@user2"], {"@user1": "ok", "@user2": "ok"}, ["Added @user1 to group", "Added @user2 to group"]),

    # Test with an invalid user
    (["@invalidUser1"], {"@invalidUser1": "error"}, ["@invalidUser1: Failed to add due to error:"]),

    # Test with multiple invalid users
    (["@invalidUser1", "@invalidUser2"], {"@invalidUser1": "error", "@invalidUser2": "error"}, ["@invalidUser1: Failed to add due to error:", "@invalidUser2: Failed to add due to error:"]),

    # Tests with a valid and invalid users
    (["@user1", "@invalidUser2"], {"@user1": "ok", "@invalidUser2": "error"}, ["Added @user1 to group", "@invalidUser2: Failed to add due to error:"]),
    (["@invalidUser1", "@user2"], {"@user2": "ok", "@invalidUser1": "error"}, ["@invalidUser1: Failed to add due to error:", "Added @user2 to group"]),

    # Test with a valid user (privacy settings)
    (["@user1"], {"@user1": "privacy"}, ["@user1: Cannot be added due to privacy settings."]),

    # Test with a valid user (not mutual contact)
    (["@user1"], {"@user1": "mutual"}, ["@user1: Cannot be added because they are not a mutual contact."]),

    # Test with valid users, one with privacy settings and one not mutual contact
    (["@valid", "@privacy", "@mutual"], {"@valid": "ok", "@privacy": "privacy", "@mutual": "mutual"}, ["Added @valid to group", "@privacy: Cannot be added due to privacy settings.", "@mutual: Cannot be added because they are not a mutual contact."]),
    # Test with a mix of all scenarios
    (["@valid", "@privacy", "@mutual", "@bad"], {"@valid": "ok", "@privacy": "privacy", "@mutual": "mutual", "@bad": "error"}, ["Added @valid to group", "@privacy: Cannot be added due to privacy settings.", "@mutual: Cannot be added because they are not a mutual contact.", "@bad: Failed to add due to error:"]),
])

def test_add_users_to_group(mock_group, usernames, user_behavior, expected_output):
    # Arrange
    client = MagicMock()

    def get_user_type(username):
        behavior = user_behavior.get(username, "error")
        if behavior == "ok":
            return MagicMock()
        elif behavior == "privacy":
            raise UserPrivacyRestrictedError("mocked privacy error")
        elif behavior == "mutual":
            raise UserNotMutualContactError("mocked mutual contact error")
        else:
            raise Exception("simulated error")
    
    client.get_input_entity.side_effect = get_user_type

    # Act
    output = capture_stdout(add_users_to_group, client, mock_group, usernames)

    # Assert
    for expected in expected_output:
        assert expected in output        
