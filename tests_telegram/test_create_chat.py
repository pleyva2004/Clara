from unittest.mock import MagicMock
from telethon.tl.types import Channel, User
from telethon.tl.functions.channels import CreateChannelRequest, InviteToChannelRequest
from telegram_bot.create_chat import create_group



# Helper to create a mocked TelegramClient
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


def test_create_group_with_valid_users():
    # Arrange
    mock_users = {
        "@user1": MagicMock(spec=User),
        "@user2": MagicMock(spec=User)
    }
    client = make_mock_client(user_map=mock_users)

    # Act
    result = create_group(client, "Test Group", ["@user1", "@user2"])

    # Assert
    assert result.title == "Test Group"
    assert client.get_input_entity.call_count == 2

def test_create_group_with_all_invalid_users():
    # Arrange
    client = make_mock_client(user_map={})

    # Act
    result = create_group(client, "Test Group", ["@invalid"])

    # Assert
    assert result.title == "Test Group"
    assert client.get_input_entity.call_count == 1

def test_create_group_with_some_invalid_users():
    # Arrange
    mock_users = {
        "@user1": MagicMock(spec=User)
    }
    client = make_mock_client(user_map=mock_users)

    # Act
    result = create_group(client, "Test Group", ["@user1", "@invalid"])

    # Assert
    assert result.title == "Test Group"
    assert client.get_input_entity.call_count == 2

def test_create_group_with_no_users():
    # Arrange
    client = make_mock_client()

    # Act
    result = create_group(client, "Test Group", [])

    # Assert
    assert result.title == "Test Group"
    assert client.get_input_entity.call_count == 0

def test_create_group_failure():
    # Arrange
    client = make_mock_client(raise_on_create=True)

    # Act
    result = create_group(client, "Test Group", ["@user1"])

    # Assert
    assert result is None

def test_create_group_with_blank_and_invalid_usernames():
    client = make_mock_client()
    result = create_group(client, "Test Group", ["@", " "])
    assert result.title == "Test Group"
    assert client.get_input_entity.call_count == 2
