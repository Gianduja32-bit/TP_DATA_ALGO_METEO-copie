from datetime import datetime
from typing import List, Optional

from weather_cli.api_manager import IDataExtractor, IDataMapper
from weather_cli.models import Record, Station

class WeatherDataService:
    def __init__(self, data_extractor: IDataExtractor, data_mapper: IDataMapper):
        self.data_extractor = data_extractor
        self.data_mapper = data_mapper

    def get_weather_data_for_station_and_date(self, date: datetime, station_name: str) -> Optional[Station]:
        raw_records = self.data_extractor.extract(date, station_name)
        if not raw_records:
            return None

        station = Station(nom=station_name)
        for raw_record in raw_records:
            record = self.data_mapper.to_object(raw_record)
            if record:
                station.add_mesure(record)
        return station

    def get_available_stations(self) -> List[str]:
        # Pour l'instant, on sait que c'est toujours "Compans-Caffarelli"
        # Dans un cas réel, cela viendrait d'une API ou d'une source de données
        return ["Compans-Caffarelli"]
