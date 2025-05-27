from unittest.mock import patch, MagicMock
from data_pipeline.database_functions.connect import get_connection
from mysql.connector import Error
import pytest

@pytest.mark.parametrize("is_connected, should_raise_exception, expected_result", [
    # Successful connection
    (True, False, "CONNECTED"),

    # Connection returned but is not connected
    (False, False, None),

    # Connection fails and raises an exception
    (None, True, None),
])

@patch('data_pipeline.database_functions.connect.mysql.connector.connect')
def test_get_connection(mock_connect, is_connected, should_raise_exception, expected_result):
    # Arrange
    if should_raise_exception:
        mock_connect.side_effect = Error("Simulated connection error")
    else:
        mock_conn = MagicMock()
        mock_conn.is_connected.return_value = is_connected
        mock_connect.return_value = mock_conn
    
    # Act
    result = get_connection("localhost", "user", "password", "test_db")

    # Assert
    if expected_result == "CONNECTED":
        assert result is not None
        assert result.is_connected() == is_connected
    else:
        assert result is None