def validate_station_name(station_name: str, available_stations: list[str]) -> str | None:
    if station_name in available_stations:
        return station_name
    else:
        print(f"Station '{station_name}' non trouvée. Stations disponibles : {', '.join(available_stations)}")
        return None
