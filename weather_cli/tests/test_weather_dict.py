import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from weather_cli.src.domain.weather_dict import WeatherDictionary

def test_set_and_get():
    """Test l'ajout et la récupération de valeurs."""
    wd = WeatherDictionary()
    wd.set("station1", "Toulouse")
    
    result = wd.get("station1")
    
    is_correct = (result == "Toulouse")
    assert is_correct == True

def test_multiple_entries():
    """Test l'ajout de plusieurs entrées."""
    wd = WeatherDictionary()
    wd.set("station1", "Toulouse")
    wd.set("station2", "Paris")
    wd.set("station3", "Lyon")
    
    assert wd.get("station1") == "Toulouse"
    assert wd.get("station2") == "Paris"
    assert wd.get("station3") == "Lyon"

def test_update_value():
    """Test la mise à jour d'une valeur existante."""
    wd = WeatherDictionary()
    wd.set("station1", "Toulouse")
    wd.set("station1", "Bordeaux")
    
    result = wd.get("station1")
    assert result == "Bordeaux"

def test_delete():
    """Test la suppression d'une entrée."""
    wd = WeatherDictionary()
    wd.set("station1", "Toulouse")
    
    deleted = wd.delete("station1")
    
    assert deleted == True
    assert wd.get("station1") is None

def test_contains():
    """Test la vérification de présence d'une clé."""
    wd = WeatherDictionary()
    wd.set("station1", "Toulouse")
    
    assert wd.contains("station1") == True
    assert wd.contains("station2") == False

def test_keys():
    """Test la récupération de toutes les clés."""
    wd = WeatherDictionary()
    wd.set("station1", "Toulouse")
    wd.set("station2", "Paris")
    
    keys = wd.keys()
    
    assert "station1" in keys
    assert "station2" in keys
    assert len(keys) == 2
