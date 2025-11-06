from abc import ABC, abstractmethod
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import pytz

from weather_cli.models import Record, Station

class Configuration:
    BASE_URL = "https://data.toulouse-metropole.fr/api/explore/v2.1/catalog/datasets/42-station-meteo-toulouse-parc-compans-cafarelli/records"

class IDataExtractor(ABC):
    @abstractmethod
    def extract(self, date: datetime, station_name: Optional[str] = None) -> List[Dict[str, Any]]:
        pass

class ApiDataExtractor(IDataExtractor):
    def __init__(self, base_url: str):
        self.base_url = base_url

    def extract(self, date: datetime, station_name: Optional[str] = None) -> List[Dict[str, Any]]:
        try:
            params = {
                "limit": 20,
                "order_by": "-heure_de_paris",
                "timezone": "Europe/Paris"
            }

            if station_name:
                params["refine.nom_de_la_station"] = station_name

            response = requests.get(self.base_url, params=params)
            response.raise_for_status()

            records = response.json().get("results", [])

            paris_tz = pytz.timezone('Europe/Paris')
            now_aware = paris_tz.localize(datetime.now())
            one_week_ago_aware = now_aware - timedelta(days=7)

            target_date_aware = paris_tz.localize(date.replace(hour=0, minute=0, second=0, microsecond=0))
            end_of_target_day_aware = target_date_aware + timedelta(days=1, microseconds=-1)

            filtered_records = []

            for record in records:
                record_date_str = record.get("heure_de_paris")
                if not record_date_str:
                    continue

                record_datetime = datetime.fromisoformat(record_date_str.replace("Z", "+00:00"))
                record_datetime = record_datetime.astimezone(paris_tz)

                if target_date_aware <= record_datetime <= end_of_target_day_aware:
                    filtered_records.append(record)

            return filtered_records

        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur lors de la récupération des données API: {e}")
            return []

class IDataMapper(ABC):
    @abstractmethod
    def to_object(self, data: Dict[str, Any]) -> Any:
        pass

class RecordMapper(IDataMapper):
    def to_object(self, data: Dict[str, Any]) -> Optional[Record]:
        try:
            temperature = data.get("temperature_en_degre_c")
            humidity = data.get("humidite")
            pressure = data.get("pression") # Assurez-vous que cette clé existe dans les données API
            timestamp_str = data.get("heure_de_paris")

            if all([temperature is not None, humidity is not None, pressure is not None, timestamp_str]):
                timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
                return Record(
                    temperature=float(temperature),
                    humidity=float(humidity),
                    pressure=float(pressure),
                    timestamp=timestamp
                )
            return None
        except (ValueError, TypeError) as e:
            print(f"⚠️ Erreur lors du mappage des données de record: {e} — Données brutes: {data}")
            return None 