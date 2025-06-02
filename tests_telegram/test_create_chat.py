from unittest.mock import MagicMock
from telethon.tl.types import Channel, User
from telethon.tl.functions.channels import CreateChannelRequest, InviteToChannelRequest
from telegram_bot.create_chat import create_group
import pytest

def make_mock_client(raise_on_create=False, user_map=None):
    mock_client = MagicMock()

    if raise_on_create:
        # Simulate an error when trying to create a channel
        mock_client.side_effect = Exception("Creation failed")
    else:
        # Simulate a successful channel creation
        mock_group = MagicMock(spec=Channel)
        mock_group.title = "Test Group"
        mock_result = MagicMock()
        mock_result.chats = [mock_group]

        # Mock the CreateChannelRequest and InviteToChannelRequest
        def call_side_effect(request):
            if isinstance(request, CreateChannelRequest):
                return mock_result
            elif isinstance(request, InviteToChannelRequest):
                return None
        mock_client.side_effect = call_side_effect

        if user_map is not None: 
            # If there are users to mock
            def get_input_entity(username):
                if username in user_map:
                    return user_map[username]
                raise Exception(f"{username} not found")
            mock_client.get_input_entity.side_effect = get_input_entity

    return mock_client

@pytest.mark.parametrize("usernames, user_map, expected_calls_count", [
    # Test with a valid user
    (["@user1"], {"@user1": MagicMock(spec=User)}, 1),

    # Test with multiple valid users
    (["@user1", "@user2"], {"@user1": MagicMock(spec=User), "@user2": MagicMock(spec=User)}, 2),
    
    # Test with a invalid user
    (["@invalidUser1"], {}, 1),

    #Test with multiple invalid users
    (["@invalidUser1", "@invalidUser2"], {}, 2),

    # Test with a valid and invlaid user
    (["@user1", "@invalidUser1"], {"@user1": MagicMock(spec=User)}, 2),
    (["@invalidUser1", "@user1"], {"@user1": MagicMock(spec=User)}, 2),

    # Test with no usernames
    ([], {}, 0),

    # Test with a invalid username format
    (["@", " "], {}, 2),
])

def test_create_group(usernames, user_map, expected_calls_count):
    # Arrange
    client = make_mock_client(user_map=user_map)

    # Act
    result = create_group(client, "Test Group", usernames)

    # Assert
    assert result.title == "Test Group"
    assert client.get_input_entity.call_count == expected_calls_count

def test_create_group_failure():
    # Arrange
    client = make_mock_client(raise_on_create=True)
    
    # Act
    result = create_group(client, "Test Group", ["@user1"])
    
    # Assert
    assert result is None
