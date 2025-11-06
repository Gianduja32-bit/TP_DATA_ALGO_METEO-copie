from datetime import datetime, timedelta
from typing import List, Optional

from weather_cli.models import Station

def validate_date(date_str: str) -> Optional[datetime]:
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        return date
    except ValueError:
        return None

def validate_station_selection(input_str: str, stations: List[Station]) -> Optional[Station]:
    # Try to match by number
    try:
        index = int(input_str) - 1
        if 0 <= index < len(stations):
            return stations[index]
    except ValueError:
        pass

    # Try to match by name (case-insensitive)
    for station in stations:
        if station.name.lower() == input_str.lower():
            return station
            
    return None

def validate_date_range(date_str: str) -> datetime | None:
    try:
        chosen_date = datetime.strptime(date_str, "%Y-%m-%d")
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        seven_days_ago = today - timedelta(days=7)

        if seven_days_ago <= chosen_date <= today:
            return chosen_date
        else:
            print("❌ La date doit être au maximum 7 jours en arrière et pas dans le futur.")
            return None
    except ValueError:
        print("❌ Format de date invalide. Utilisez YYYY-MM-DD.")
        return None

def validate_station_name(station_name: str, available_stations: list[str]) -> str | None:
    if station_name in available_stations:
        return station_name
    else:
        print(f"❌ Station '{station_name}' non trouvée. Stations disponibles : {', '.join(available_stations)}")
        return None
