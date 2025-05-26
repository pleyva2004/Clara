from telegram_bot.group_exists import isGroup
from unittest.mock import MagicMock
from telethon.tl.custom.dialog import Dialog

def test_group_exists():
    mock_client = MagicMock()
    mock_dialog = MagicMock(spec=Dialog)
    mock_dialog.name = "Test Group"
    mock_client.iter_dialogs.return_value = [mock_dialog]
    result = isGroup(mock_client, "Test Group")
    assert result is not None

def test_group_does_not_exist():
    mock_client = MagicMock()
    mock_dialog = MagicMock(spec=Dialog)
    mock_dialog.name = "Test Group"
    mock_client.iter_dialogs.return_value = [mock_dialog]
    result = isGroup(mock_client, "Test Group2")
    assert result is None