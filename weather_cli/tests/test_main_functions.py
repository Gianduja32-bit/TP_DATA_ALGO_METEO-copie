import pytest
import os
import sys
from datetime import datetime
from unittest.mock import Mock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from weather_cli.__main__ import get_station_choice

@patch('weather_cli.__main__.console.input')
@patch('weather_cli.__main__.console.print')
def test_get_station_choice(mock_print, mock_input):
    mock_service = Mock()
    mock_service.get_available_stations.return_value = ["Station A", "Station B"]
    
    mock_input.return_value = "Station A"
    
    result = get_station_choice(mock_service)
    
    is_correct = (result == "Station A")
    assert is_correct == True
