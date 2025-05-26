from telegram_bot.group_exists import isGroup
from unittest.mock import MagicMock
from telethon.tl.custom.dialog import Dialog
import pytest

@pytest.mark.parametrize("dialog_names, search_name, expected_result", [
    (["Test Group"], "Test Group", True), # Group exists
    (["Test Group"], "Other Group", False), # Group does not exist
    (["Test Group 1", "Test Group 2"], "Test Group 1", True), # Multiple groups, one matches
    (["Test Group 1", "Test Group 2"], "Test Group 3", False), # Multiple groups, none match
    ([], "Any Group", False), # No groups at all
    (["Test Group 1", "Test Group 2"], "test group 1", False) # Case sensitivity check
])

def test_group_exists(dialog_names, search_name, expected_result):
    # Arrange
    mock_client = MagicMock()
    dialogs = []

    for name in dialog_names:
        mock_dialog = MagicMock(spec=Dialog)
        mock_dialog.name = name
        dialogs.append(mock_dialog)
    mock_client.iter_dialogs.return_value = dialogs

    # Act
    result = isGroup(mock_client, search_name)

    # Assert
    if expected_result:
        assert result is not None
        assert result.name == search_name
    else:
        assert result is None
